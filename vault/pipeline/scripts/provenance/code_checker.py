#!/usr/bin/env python3
"""Code repository checks from public APIs (GitHub REST API, GitLab API v4, Software Heritage, Zenodo). Needs no virtual environment.
Reports: exists and public, not empty (file count, size), licence (SPDX), README with run or install instructions (headings or code blocks),
dependency files and whether versions are pinned, CITATION.cff, releases or tags, archived in Software Heritage or Zenodo (DOI), first and last
commit dates, and whether the repository was created or last pushed after the paper date.
A GitHub token is read with `gh auth token` into memory and sent only to api.github.com; it is never printed or stored.
  python3 code_checker.py https://github.com/owner/repo [--paper-date 2024-09-12]"""
import base64, json, re, subprocess, sys
from datetime import datetime
from urllib.parse import quote, urlparse
from _http import fetch, request_json_meta

DEP_FILES = ('requirements.txt', 'environment.yml', 'environment.yaml', 'pyproject.toml', 'package.json', 'renv.lock', 'pipfile', 'poetry.lock', 'setup.py',
             'conda.yml', 'conda.yaml', 'package-lock.json', 'pipfile.lock', 'yarn.lock', 'description', 'cargo.toml', 'go.mod')
_token = []


def gh_headers():
    if not _token:
        try: _token.append(subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, timeout=15).stdout.strip())
        except (OSError, subprocess.SubprocessError): _token.append('')
    return {'Authorization': f'Bearer {_token[0]}', 'Accept': 'application/vnd.github+json'} if _token[0] else {'Accept': 'application/vnd.github+json'}


def parse_repo(url: str):
    """(host, owner, repo) from a repository URL, or None. Drops .git and /tree/... /blob/... suffixes."""
    p = urlparse(url if '://' in url else 'https://' + url); segs = [s for s in p.path.split('/') if s]
    host = p.netloc.lower().removeprefix('www.')
    if len(segs) < 2: return None
    return host, segs[0], re.sub(r'\.git$', '', segs[1])


# ---------- decision logic (unit tested offline) ----------
def readme_instructions(text: str) -> dict:
    """Heuristic: run or install instructions exist when a heading names them or a code block holds a command."""
    heads = re.findall(r'^\s{0,3}#{1,6}\s*(.+?)\s*#*\s*$', text or '', re.M) + re.findall(r'^(.+)\n[=-]{3,}\s*$', text or '', re.M)
    kw = re.compile(r'install|usage|getting started|quick ?start|how to run|running|run |setup|set up|requirements|reproduc|build|example', re.I)
    matched = [h for h in heads if kw.search(h)]
    blocks = re.findall(r'```.*?```', text or '', re.S)
    cmd = [b for b in blocks if re.search(r'\b(pip|conda|python3?|npm|yarn|Rscript|R CMD|make|docker|git clone|poetry|install\.packages|cargo|go run|bash|sh )\b', b)]
    steps = [l.strip()[:80] for l in re.findall(r'^\s*\d+\.\s+.*\b(?:run|install|execute|clone|download|create)\b.*$', text or '', re.M | re.I)]
    return {'has_instructions': bool(matched or cmd or steps), 'numbered_steps_mentioning_run': steps[:3], 'matching_headings': matched[:5], 'code_blocks': len(blocks), 'code_blocks_with_commands': len(cmd), 'readme_length': len(text or '')}


def pinning(filename: str, content: str) -> dict:
    """Are dependency versions pinned? Returns {state: pinned|partly pinned|not pinned|lock file|unknown, pinned, total}."""
    f = filename.lower().rsplit('/', 1)[-1]; c = content or ''
    if f in ('renv.lock', 'poetry.lock', 'pipfile.lock', 'package-lock.json', 'yarn.lock', 'go.mod'): return {'state': 'lock file', 'pinned': None, 'total': None}
    lines = [l.strip() for l in c.splitlines() if l.strip() and not l.strip().startswith(('#', '-'))]
    if f == 'requirements.txt':
        tot = len(lines); pin = sum(1 for l in lines if '==' in l or ' @ ' in l)
    elif f in ('environment.yml', 'environment.yaml', 'conda.yml', 'conda.yaml'):
        deps = [l.lstrip('- ').strip() for l in c.splitlines() if re.match(r'^\s+-\s+\S', l) and ':' not in l.split('#')[0]]
        tot = len(deps); pin = sum(1 for d in deps if re.search(r'[=]{1,2}\s*\d', d) and not re.search(r'[<>]', d))
    elif f == 'package.json':
        try: j = json.loads(c)
        except ValueError: return {'state': 'unknown', 'pinned': None, 'total': None}
        deps = {**j.get('dependencies', {}), **j.get('devDependencies', {})}
        tot = len(deps); pin = sum(1 for v in deps.values() if re.match(r'^\d', str(v)))
    elif f == 'pyproject.toml':
        deps = re.findall(r'["\']([A-Za-z0-9_.\-\[\]]+\s*(?:[=<>~!^]=?[^"\']*)?)["\']', ''.join(re.findall(r'dependencies\s*=\s*\[(.*?)\]', c, re.S)))
        tot = len(deps); pin = sum(1 for d in deps if '==' in d)
        if not tot: return {'state': 'unknown', 'pinned': None, 'total': None}
    else: return {'state': 'unknown', 'pinned': None, 'total': None}
    if tot == 0: return {'state': 'unknown', 'pinned': 0, 'total': 0}
    return {'state': 'pinned' if pin == tot else ('not pinned' if pin == 0 else 'partly pinned'), 'pinned': pin, 'total': tot}


def date_facts(created, pushed, first_commit, last_commit, paper_date) -> dict:
    """Plain comparisons of repository dates with the paper date (all as ISO date strings; any may be None)."""
    def d(x): return x[:10] if x else None
    c, p, fc, lc, pd_ = d(created), d(pushed), d(first_commit), d(last_commit), d(paper_date)
    out = {'created': c, 'last_push': p, 'first_commit': fc, 'last_commit': lc, 'paper_date': pd_}
    if pd_:
        out['created_after_paper'] = c > pd_ if c else None
        out['pushed_after_paper'] = p > pd_ if p else None
        out['last_commit_days_after_paper'] = (datetime.fromisoformat(lc) - datetime.fromisoformat(pd_)).days if lc else None
        out['first_commit_before_paper'] = fc < pd_ if fc else None
    return out


def gh(path, params=None):
    return request_json_meta('GET', 'https://api.github.com' + path, params=params, headers=gh_headers())


def gh_text(owner, repo, path):
    d, err, _ = gh(f'/repos/{owner}/{repo}/contents/{quote(path)}')
    if d and isinstance(d, dict) and d.get('encoding') == 'base64':
        try: return base64.b64decode(d['content']).decode('utf-8', 'replace')
        except ValueError: return None
    return None


def software_heritage(origin_url):
    d, err, meta = request_json_meta('GET', f'https://archive.softwareheritage.org/api/1/origin/{origin_url}/get/', retries=2)
    res = {'archived': bool(d), 'url': meta['url'], 'http_status': meta['http_status'], 'error': None if d or err == 'not found' else err}
    if d:
        v, _, _m = request_json_meta('GET', f'https://archive.softwareheritage.org/api/1/origin/{origin_url}/visit/latest/', retries=2)
        if v: res.update(last_visit=(v.get('date') or '')[:10], visit_status=v.get('status'), snapshot=v.get('snapshot'))
    return res


def zenodo_for(owner, repo, readme=''):
    esc = f'{owner}/{repo}'.replace('.', '\\.').replace('/', '\\/')
    d, err, meta = request_json_meta('GET', 'https://zenodo.org/api/records', params={'q': 'related.identifier:/.*github\\.com\\/' + esc + '.*/', 'size': 3, 'sort': 'mostrecent'}, retries=2)
    recs = [{'doi': h.get('doi'), 'title': (h.get('metadata') or {}).get('title', '')[:100], 'published': (h.get('metadata') or {}).get('publication_date')} for h in ((d or {}).get('hits') or {}).get('hits', [])]
    badge = sorted(set(re.findall(r'10\.5281/zenodo\.\d+', readme or '')))
    return {'records': recs, 'doi_in_readme': badge, 'archived': bool(recs or badge), 'url': meta['url'], 'http_status': meta['http_status'], 'error': err if err != 'not found' else None}


def check_github(owner, repo, paper_date=None) -> dict:
    base = f'https://github.com/{owner}/{repo}'
    r, err, meta = gh(f'/repos/{owner}/{repo}')
    out = {'host': 'github.com', 'repo_url': base, 'api_url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256']}
    if not r:
        out.update(exists=False if err == 'not found' else None, error=err); return out
    out.update(exists=True, public=not r.get('private'), archived_flag=r.get('archived'), default_branch=r.get('default_branch'), size_kb=r.get('size'),
               stars=r.get('stargazers_count'), license=(r.get('license') or {}).get('spdx_id'), license_name=(r.get('license') or {}).get('name'))
    t, terr, _ = gh(f"/repos/{owner}/{repo}/git/trees/{r.get('default_branch')}", {'recursive': 1})
    files = [x for x in (t or {}).get('tree', []) if x['type'] == 'blob']
    out.update(empty=(not files), file_count=len(files), total_bytes=sum(x.get('size', 0) for x in files), tree_truncated=bool((t or {}).get('truncated')), tree_error=terr)
    paths = [x['path'] for x in files]
    rd, _, _ = gh(f'/repos/{owner}/{repo}/readme'); readme = ''
    if rd and rd.get('encoding') == 'base64': readme = base64.b64decode(rd['content']).decode('utf-8', 'replace')
    out['readme'] = {'file': (rd or {}).get('name'), **readme_instructions(readme)} if rd else {'file': None, 'has_instructions': False}
    deps = [p for p in paths if p.lower().rsplit('/', 1)[-1] in DEP_FILES and p.count('/') <= 1][:6]
    dep_info = []
    for p in deps[:3]: dep_info.append({'file': p, **pinning(p, gh_text(owner, repo, p) or '')})
    for p in deps[3:]: dep_info.append({'file': p, 'state': 'not read'})
    out['dependency_files'] = dep_info
    out['citation_cff'] = any(p.lower() == 'citation.cff' for p in paths)
    rel, _, _ = gh(f'/repos/{owner}/{repo}/releases', {'per_page': 3}); tags, _, _ = gh(f'/repos/{owner}/{repo}/tags', {'per_page': 3})
    out['releases'] = [{'tag': x.get('tag_name'), 'date': (x.get('published_at') or '')[:10]} for x in rel or []]
    out['tags'] = [x['name'] for x in tags or []]
    lc = fetch('GET', f'https://api.github.com/repos/{owner}/{repo}/commits', params={'per_page': 1}, headers=gh_headers())
    last = first = None
    try:
        arr = json.loads(lc['text']) if lc['status'] == 200 else []
        if arr: last = arr[0]['commit']['committer']['date']
        m = re.search(r'[?&]page=(\d+)>; rel="last"', lc['headers'].get('link', ''))
        if m:
            fc, _, _ = gh(f'/repos/{owner}/{repo}/commits', {'per_page': 1, 'page': m.group(1)})
            if fc: first = fc[0]['commit']['committer']['date']
        elif arr: first = last
    except (ValueError, KeyError, IndexError): pass
    out['dates'] = date_facts(r.get('created_at'), r.get('pushed_at'), first, last, paper_date)
    out['software_heritage'] = software_heritage(base)
    out['zenodo'] = zenodo_for(owner, repo, readme)
    return out


def check_gitlab(owner, repo, paper_date=None) -> dict:
    pid = quote(f'{owner}/{repo}', safe ='')
    r, err, meta = request_json_meta('GET', f'https://gitlab.com/api/v4/projects/{pid}', params={'license': 'true'})
    base = f'https://gitlab.com/{owner}/{repo}'
    out = {'host': 'gitlab.com', 'repo_url': base, 'api_url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256']}
    if not r: out.update(exists=False if err == 'not found' else None, error=err); return out
    out.update(exists=True, public=r.get('visibility') == 'public', default_branch=r.get('default_branch'), stars=r.get('star_count'),
               license=(r.get('license') or {}).get('key', '').upper() or None, license_name=(r.get('license') or {}).get('name'))
    t, _, _ = request_json_meta('GET', f'https://gitlab.com/api/v4/projects/{pid}/repository/tree', params={'recursive': 'true', 'per_page': 100})
    files = [x for x in t or [] if x['type'] == 'blob']; paths = [x['path'] for x in files]
    out.update(empty=not files, file_count=len(files), file_count_note='first 100 entries only', total_bytes=None)
    rd = next((p for p in paths if p.lower().startswith('readme')), None); readme = ''
    if rd:
        f = fetch('GET', f'https://gitlab.com/api/v4/projects/{pid}/repository/files/{quote(rd, safe="")}/raw', params={'ref': r.get('default_branch')})
        readme = f['text'] if f['status'] == 200 else ''
    out['readme'] = {'file': rd, **readme_instructions(readme)} if rd else {'file': None, 'has_instructions': False}
    out['dependency_files'] = []
    for p in [p for p in paths if p.lower() in DEP_FILES][:3]:
        f = fetch('GET', f'https://gitlab.com/api/v4/projects/{pid}/repository/files/{quote(p, safe="")}/raw', params={'ref': r.get('default_branch')})
        out['dependency_files'].append({'file': p, **pinning(p, f['text'] if f['status'] == 200 else '')})
    out['citation_cff'] = any(p.lower() == 'citation.cff' for p in paths)
    rel, _, _ = request_json_meta('GET', f'https://gitlab.com/api/v4/projects/{pid}/releases', params={'per_page': 3})
    tg, _, _ = request_json_meta('GET', f'https://gitlab.com/api/v4/projects/{pid}/repository/tags', params={'per_page': 3})
    out['releases'] = [{'tag': x.get('tag_name'), 'date': (x.get('released_at') or '')[:10]} for x in rel or []]; out['tags'] = [x['name'] for x in tg or []]
    cm, _, _ = request_json_meta('GET', f'https://gitlab.com/api/v4/projects/{pid}/repository/commits', params={'per_page': 1})
    last = cm[0]['committed_date'] if cm else None
    out['dates'] = date_facts(r.get('created_at'), r.get('last_activity_at'), None, last, paper_date)
    out['software_heritage'] = software_heritage(base); out['zenodo'] = zenodo_for(owner, repo, readme)
    return out


def check(url: str, paper_date=None) -> dict:
    p = parse_repo(url)
    if not p: return {'repo_url': url, 'exists': None, 'error': 'not a repository URL'}
    host, owner, repo = p
    if host == 'github.com': return check_github(owner, repo, paper_date)
    if host == 'gitlab.com': return check_gitlab(owner, repo, paper_date)
    return {'host': host, 'repo_url': url, 'exists': None, 'error': f'{host} is not supported yet (github.com and gitlab.com only)'}


def summarize(c: dict) -> str:
    """One plain-language result string for a checked repository."""
    if c.get('exists') is None: return f"{c.get('repo_url')}: could not be checked ({c.get('error')})."
    if not c['exists']: return f"{c['repo_url']} does not exist or is not public (HTTP {c.get('http_status')})."
    bits = [f"{c['repo_url']} is public" if c.get('public') else f"{c['repo_url']} is not public"]
    bits.append('is empty' if c.get('empty') else f"has {c.get('file_count')} files")
    bits.append(f"licence {c['license']}" if c.get('license') and c['license'] != 'NOASSERTION' else 'no recognised licence')
    bits.append('README has run or install instructions' if (c.get('readme') or {}).get('has_instructions') else 'README has no run or install instructions' if (c.get('readme') or {}).get('file') else 'no README')
    deps = c.get('dependency_files') or []
    bits.append('dependency file: ' + ', '.join(f"{d['file']} ({d['state']})" for d in deps) if deps else 'no dependency file in the top two folder levels')
    bits.append('has CITATION.cff' if c.get('citation_cff') else 'no CITATION.cff')
    bits.append('has releases or tags' if (c.get('releases') or c.get('tags')) else 'no releases or tags')
    sh, z = c.get('software_heritage') or {}, c.get('zenodo') or {}
    arch = [x for x, ok in (('Software Heritage', sh.get('archived')), ('Zenodo', z.get('archived'))) if ok]
    bits.append('archived in ' + ' and '.join(arch) if arch else 'not found in Software Heritage or Zenodo')
    dt = c.get('dates') or {}
    if dt.get('last_commit'): bits.append(f"last commit {dt['last_commit']}" + (f", {dt['last_commit_days_after_paper']} days after the paper date {dt['paper_date']}" if dt.get('last_commit_days_after_paper') is not None and dt['last_commit_days_after_paper'] > 0 else ''))
    if dt.get('created_after_paper'): bits.append(f"repository was created {dt['created']}, after the paper date")
    return '; '.join(bits) + '.'


if __name__ == '__main__':
    pdate = sys.argv[sys.argv.index('--paper-date') + 1] if '--paper-date' in sys.argv else None
    c = check(sys.argv[1], pdate); print(json.dumps(c, indent=1)); print(summarize(c))

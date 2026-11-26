#!/usr/bin/env python3
"""Extract every URL and DOI from a PDF and check each one.
Extraction: PyMuPDF link annotations (page.get_links()) plus a regex over the page text, joining URLs broken across lines and words broken by hyphenation.
Checks per link: HEAD then GET fallback (the body is never read), final URL, HTTP status, redirects, Wayback Machine snapshot, classification
(code repository, data repository, registry, supplement, other), redirect to a login page. DOIs are checked with the doi.org handle API.
Also finds "available upon request" and "will be released" statements near the words code, data or availability.
  python3 link_check.py paper.pdf [--no-check]"""
import json, re, sys, unicodedata
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, urlparse
import fitz  # PyMuPDF
from _http import fetch, request_json_meta

URL_RE = re.compile(r'(?:https?://|www\.)[^\s<>"“”]+', re.I)
DOI_RE = re.compile(r'\b10\.\d{4,9}/[^\s<>"“”]+', re.I)
REF_HEAD = re.compile(r'^\s*(?:\d+\.?\s*)?(references|bibliography|literature cited|works cited)\s*$', re.I)
LOGIN_RE = re.compile(r'(login|log-in|signin|sign-in|sso|/auth\b|/oauth|accounts\.google|shibboleth|idp\.|/cas/)', re.I)
REQUEST_RE = re.compile(r'(upon|on|by|via)\s+(reasonable\s+)?(request|contacting|contact)|contact\s+(the\s+)?(corresponding\s+)?author|request\s+from\s+(the\s+)?(corresponding\s+)?author|available\s+from\s+the\s+(corresponding\s+)?author', re.I)
FUTURE_RE = re.compile(r'will\s+be\s+(made\s+|publicly\s+|made\s+publicly\s+|openly\s+)?(available|released|shared|open[- ]sourced)|upon\s+(publication|acceptance)|coming\s+soon', re.I)
TOPIC_RE = re.compile(r'\b(code|data|dataset|datasets|software|materials|availability|repository)\b', re.I)

CODE_HOSTS = ('github.com', 'gitlab.com', 'bitbucket.org', 'codeberg.org', 'gist.github.com', 'sourceforge.net', 'archive.softwareheritage.org', 'colab.research.google.com')
DATA_HOSTS = ('zenodo.org', 'figshare.com', 'datadryad.org', 'dryad.', 'dataverse', 'kaggle.com', 'data.mendeley.com', 'physionet.org', 'openneuro.org', 'osf.io/data')
REGISTRY_HOSTS = ('osf.io', 'clinicaltrials.gov', 'crd.york.ac.uk', 'aspredicted.org', 'isrctn.com', 'researchregistry.com', 'trialregister.nl', 'anzctr.org.au', 'who.int/clinical-trials-registry-platform')
DATA_DOI_PREFIXES = ('10.5281/zenodo', '10.6084/m9', '10.5061/dryad', '10.7910/dvn', '10.17605/osf.io')
SUPPLEMENT_RE = re.compile(r'supplement|appendi|additional[ _-]file|moesm|mmc\d|media-\d|supporting[ _-]information|\bsi\b', re.I)


# ---------- decision logic (unit tested offline) ----------
def clean_url(u: str) -> str:
    u = u.strip().rstrip('.,;:\'"”’>')
    while u.endswith(')') and u.count(')') > u.count('('): u = u[:-1]
    while u.endswith(']') and u.count(']') > u.count('['): u = u[:-1]
    return u.rstrip('.,;:')


def doi_of(u: str):
    m = re.search(r'(?:doi\.org/|doi:\s*)?(10\.\d{4,9}/\S+)', u, re.I)
    return clean_url(m.group(1)).lower() if m and ('doi' in u.lower() or u.lower().startswith('10.')) else None


def classify_url(url: str, context: str = '') -> str:
    """One of: code repository, data repository, registry, supplement, other."""
    u = url.lower(); p = urlparse(u if '://' in u else 'http://' + u); host = p.netloc.removeprefix('www.'); path = p.path
    doi = doi_of(u)
    if doi and doi.startswith(DATA_DOI_PREFIXES): return 'registry' if doi.startswith('10.17605/osf.io') and not re.search(r'\b(data|dataset|materials)\b', context, re.I) else 'data repository'
    if 'osf.io' in host:
        return 'data repository' if re.search(r'\b(data|dataset|datasets|materials|code)\b', context, re.I) and not re.search(r'regist|preregist', context, re.I) else 'registry'
    if any(h in host for h in REGISTRY_HOSTS if '/' not in h) or any(h in u for h in REGISTRY_HOSTS if '/' in h): return 'registry'
    if host == 'huggingface.co' or host == 'hf.co':
        return 'data repository' if path.startswith('/datasets') else 'code repository'
    if SUPPLEMENT_RE.search(u) and not any(h in host for h in CODE_HOSTS): return 'supplement'
    if any(h in host for h in DATA_HOSTS) or (host == 'kaggle.com' and 'dataset' in path): return 'data repository'
    if host.endswith('github.com') or host in CODE_HOSTS:
        segs = [s for s in path.split('/') if s]
        if host == 'github.com' and len(segs) < 2: return 'other'   # an organisation page, not a repository
        return 'code repository'
    return 'other'


def data_hint(context: str) -> bool:
    """True when the text around a link mentions data or datasets (used to treat a GitHub link as possibly holding the data too)."""
    return bool(re.search(r'\b(data|datasets?|corpus|corpora|annotations?|benchmark)\b', context or '', re.I))


def availability_statements(text: str):
    """Sentences saying code or data are available on request, or will be released, near the words code/data/availability."""
    flat = re.sub(r'\s+', ' ', text); out = []
    for rx, kind in ((REQUEST_RE, 'on request'), (FUTURE_RE, 'future release')):
        for m in rx.finditer(flat):
            s = flat.rfind('. ', 0, m.start()) + 2; e = flat.find('. ', m.end()); e = len(flat) if e < 0 else e + 1
            sent = flat[max(s, 0):e].strip()
            if TOPIC_RE.search(sent) and sent[:300] not in [o['sentence'] for o in out]: out.append({'kind': kind, 'sentence': sent[:300]})
    return out


def link_status(http_status, error, final_url, original, doi_registered=None, dns_failure=False) -> tuple:
    """Return (status, label): status in ok, flag, unavailable; label in ok, dead, login, blocked, redirect-to-login, unresolved."""
    if doi_registered is False: return 'flag', 'dead'
    if http_status is None: return ('flag', 'dead') if dns_failure else ('unavailable', 'unreachable')   # a refused or timed-out connection may be temporary; a missing domain is not
    if http_status in (404, 410): return 'flag', 'dead'
    if http_status in (401, 403, 429, 999) or http_status == 451: return 'unavailable', 'blocked'
    if http_status >= 500: return 'flag', 'dead'
    if http_status >= 400: return 'flag', 'dead'
    if final_url and final_url != original and LOGIN_RE.search(urlparse(final_url).netloc + urlparse(final_url).path) and not LOGIN_RE.search(urlparse(original).netloc + urlparse(original).path):
        return 'flag', 'redirect-to-login'
    return 'ok', 'ok'


# ---------- extraction ----------
def _join_broken(text: str) -> str:
    text = unicodedata.normalize('NFKC', text)                # ligatures such as the fl in 'timwoelfle'
    text = re.sub(r'<\?show.*?\?>', '', text, flags=re.S)       # typesetting markers some publishers leave inside DOIs
    for _ in range(4):
        text = re.sub(r'((?:https?://|www\.|\b10\.\d{4,9}/)\S*[/\-_=&?%#])\n(?=\S)', r'\1', text)   # URL or DOI ends in a joiner character (hyphen kept)
        text = re.sub(r'((?:https?://|www\.|\b10\.\d{4,9}/)\S*\.)\n(?=[a-z]|\d{3,})', r'\1', text)    # ends in a dot and continues in lower case or 3+ digits (not a page number)
    return re.sub(r'([a-z])-\n([a-z])', r'\1\2', text)         # hyphenated words in running text


def extract(pdf_path: str) -> dict:
    pdf_path = pdf_path.replace('~', __import__('os').path.expanduser('~'), 1) if pdf_path.startswith('~') else pdf_path
    doc = fitz.open(pdf_path)
    pages = []; ref_page = ref_y = None
    for i, page in enumerate(doc):
        pages.append(page.get_text())
        for b in page.get_text('blocks'):
            if REF_HEAD.match(b[4].strip()): ref_page, ref_y = i, b[1]      # keep the last heading that looks like "References"
    found = {}   # key -> link record
    def add(url, kind, page_no, ctx, y=None):
        url = clean_url(unicodedata.normalize('NFKC', re.sub(r'<\?show.*?\?>', '', url, flags=re.S)))
        if not url: return
        if url.lower().startswith('www.'): url = 'http://' + url
        doi = doi_of(url) if ('doi.org' in url.lower() or url.lower().startswith('10.') or kind == 'doi') else None
        if doi: url = 'https://doi.org/' + doi
        key = doi or url.lower().rstrip('/')
        in_ref = ref_page is not None and (page_no > ref_page or (page_no == ref_page and (y is None or y > ref_y)))
        rec = found.get(key)
        if rec is None: found[key] = {'url': url, 'doi': doi, 'sources': [kind], 'page': page_no + 1, 'context': ctx[:300], 'in_references': in_ref}
        else:
            if kind not in rec['sources']: rec['sources'].append(kind)
            if kind == 'annotation' and not doi: rec['url'] = url      # the annotation URI is exact; text can be cut by line breaks
    for i, page in enumerate(doc):
        txt = _join_broken(pages[i])
        for lk in page.get_links():
            uri = lk.get('uri')
            if uri and uri.startswith(('http', 'mailto:')) and not uri.startswith('mailto:'):
                anchor = page.get_textbox(lk['from']).strip() if lk.get('from') else ''
                pos = txt.find(anchor[:30]) if anchor else -1
                ctx = txt[max(0, pos - 150): pos + 200] if pos >= 0 else anchor
                add(uri, 'annotation', i, ctx, lk['from'].y0 if lk.get('from') else None)
        for m in URL_RE.finditer(txt):
            ctx = txt[max(0, m.start() - 150): m.end() + 100]
            u = clean_url(m.group(0))
            # a text URL that is the start of an annotation URI is the same link: skip it
            if any(r['url'].lower().startswith(u.lower().rstrip('/')) and 'annotation' in r['sources'] for r in found.values()): continue
            add(u, 'text', i, ctx, None)
        for m in DOI_RE.finditer(txt):
            add(m.group(0), 'doi', i, txt[max(0, m.start() - 150): m.end() + 100], None)
    full = '\n'.join(_join_broken(p) for p in pages)
    body = '\n'.join(_join_broken(p) for p in (pages[:ref_page + 1] if ref_page is not None else pages))
    meta_title = (doc.metadata or {}).get('title')
    return {'pages': len(doc), 'text': full, 'body_text': body, 'first_page': pages[0] if pages else '', 'links': list(found.values()), 'pdf_title': meta_title,
            'references_start_page': None if ref_page is None else ref_page + 1}


def repair_doi(doi: str, context: str):
    """PDF text often shows an underscore in a DOI as a space ('10.1162/coli a 00524'). Return the DOI with the rest of that line joined by underscores, or None."""
    i = context.lower().find(doi.lower())
    if i < 0: return None
    tail = context[i + len(doi):].split('\n')[0]
    if not tail.startswith(' ') or not re.match(r'^(?: \w+)+\.?\s*$', tail): return None
    cand = doi + tail.strip().rstrip('.').replace(' ', '_').join(['_', ''])
    return cand.lower()


# ---------- checking ----------
def wayback(url):
    d, err, meta = request_json_meta('GET', 'https://archive.org/wayback/available', params={'url': url})
    snap = ((d or {}).get('archived_snapshots') or {}).get('closest') or {}
    return {'has_snapshot': bool(snap.get('available')), 'snapshot_url': snap.get('url'), 'snapshot_time': snap.get('timestamp'), 'error': err,
            'http_status': meta['http_status']}


def check_link(rec: dict) -> dict:
    url = rec['url']; out = {**rec, 'class': classify_url(url, rec.get('context', ''))}
    if rec.get('doi'):
        d, err, meta = request_json_meta('GET', f"https://doi.org/api/handles/{quote(rec['doi'], safe='/')}", retries=2)
        registered = bool(d and d.get('responseCode') == 1) if d is not None else (False if err == 'not found' else None)
        if registered is False:
            cand = repair_doi(rec['doi'], rec.get('context', ''))
            if cand:
                d2, err2, meta2 = request_json_meta('GET', f"https://doi.org/api/handles/{quote(cand, safe='/')}", retries=2)
                if d2 and d2.get('responseCode') == 1:
                    out['repaired_from'] = rec['doi']; out['doi'] = cand; out['url'] = 'https://doi.org/' + cand; d, err, meta, registered = d2, err2, meta2, True
        target = next((v['data']['value'] for v in (d or {}).get('values', []) if v.get('type') == 'URL'), None)
        out.update(http_status=meta['http_status'], response_sha256=meta['response_sha256'], final_url=target or url, redirects=[], doi_registered=registered,
                   check_method='doi.org handle API', error=err if registered is None else None)
        out['status'], out['label'] = link_status(meta['http_status'], err, target, url, registered)
        if registered is False: out['wayback'] = wayback(url)
        else: out['wayback'] = None
        return out
    r = fetch('HEAD', url, retries=2, cache=False, timeout=20, no_body=True)
    method = 'HEAD'
    if r['status'] is None or r['status'] >= 400:
        r = fetch('GET', url, retries=2, cache=False, timeout=20, no_body=True); method = 'HEAD then GET'
    out.update(http_status=r['status'], final_url=r['final_url'], redirects=r['redirects'], error=r['error'], check_method=method, response_sha256=r['sha256'])
    out['dns_failure'] = bool(r.get('dns_failure'))
    out['status'], out['label'] = link_status(r['status'], r['error'], r['final_url'], url, dns_failure=out['dns_failure'])
    out['wayback'] = wayback(url)
    return out


def check_all(links, workers=4):
    with ThreadPoolExecutor(workers) as ex: res = list(ex.map(check_link, links))
    again = [i for i, r in enumerate(res) if r.get('label') == 'unreachable']      # second pass for links with no answer at all, after a pause
    if again:
        import time; time.sleep(5)
        for i in again: res[i] = check_link(links[i])
    return res


if __name__ == '__main__':
    ex = extract(sys.argv[1])
    print(f"{ex['pages']} pages, {len(ex['links'])} links, references start on page {ex['references_start_page']}")
    res = check_all(ex['links']) if '--no-check' not in sys.argv else ex['links']
    for r in res: print(r.get('status', '-'), r.get('label', ''), r.get('http_status', ''), r.get('class', classify_url(r['url'], r['context'])), 'REF' if r['in_references'] else 'body', r['url'][:100])
    for s in availability_statements(ex['text']): print(s)

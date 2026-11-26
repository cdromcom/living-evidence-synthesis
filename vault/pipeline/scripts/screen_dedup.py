#!/usr/bin/env python3
"""Find duplicate and superseded papers in a Zotero export, and papers already in the seed set (JP, 2026-11-25). Nothing is deleted or moved.
  python3 screen_dedup.py LIB1.json [--also LIB3.json] [--out dedup.json]
Matches: same DOI; same arXiv id; normalized title equal; title similarity >= 0.90 (a preprint and its published version). In a group, the preferred record is the published version, else the newest, else the one with a PDF.
Also matches each record to the 27 seed source pages by DOI or title."""
import argparse, difflib, json, os, re
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis')
def norm(t): return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()
PRE = re.compile(r'arxiv|biorxiv|medrxiv|preprint|ssrn|openreview|research square|techrxiv', re.I)
def seed_pdf_titles():
    # the seed PDF file names look like "Author et al. - 2024 - Title.pdf"; use the Title part
    out = []
    for p in sorted((VAULT / 'sysrev/dgraph/source/pdfs').glob('*.pdf')):
        parts = p.stem.split(' - ', 2); out.append({'citekey': p.name, 'title': parts[2] if len(parts) == 3 else p.stem, 'doi': ''})
    return out
def seeds():
    out = seed_pdf_titles()
    for p in sorted((VAULT / 'sysrev/dgraph/source').glob('@*.md')):
        t = p.read_text(encoding='utf-8'); title = (re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M) or [None, p.stem])[1]; doi = (re.search(r'^DOI:\s*"?(\S+?)"?\s*$', t, re.M) or [None, ''])[1].lower()
        out.append({'citekey': p.stem, 'title': title, 'doi': doi})
    return out
def rank(r):   # higher is preferred
    pub = r['publication'] or ''; is_pre = bool(PRE.search(pub) or r['type'] in ('preprint',) or (r['arxiv'] and not (r['doi'] and not r['doi'].startswith('10.48550'))))
    return (0 if is_pre else 1, r['year'] or '0', 1 if r['pdfs'] else 0, r['added'])
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('lib1'); ap.add_argument('--also'); ap.add_argument('--out'); ap.add_argument('--pool', help='export of an older Zotero collection: flag papers already in it'); a = ap.parse_args()
    R = json.load(open(a.lib1)); n1 = len(R)
    for r in R: r['source'] = 'personal library'
    if a.also:
        have = {(r['doi'] or '', norm(r['title'])) for r in R}
        for r in json.load(open(a.also)):
            r['source'] = 'OASIS Lab group copy'; R.append(r)
    for i, r in enumerate(R): r['idx'] = i; r['nt'] = norm(r['title'])
    parent = list(range(len(R)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y): parent[find(x)] = find(y)
    reason = {}
    for i, j in ((i, j) for i in range(len(R)) for j in range(i + 1, len(R))):
        x, y = R[i], R[j]; why = None
        if x['doi'] and x['doi'] == y['doi']: why = 'same DOI'
        elif x['arxiv'] and x['arxiv'] == y['arxiv']: why = 'same arXiv id'
        elif x['nt'] and x['nt'] == y['nt']: why = 'same title'
        elif x['nt'] and y['nt'] and abs(len(x['nt']) - len(y['nt'])) < 25 and difflib.SequenceMatcher(None, x['nt'], y['nt']).ratio() >= 0.90: why = 'very similar title (version?)'
        if why: union(i, j); reason[(i, j)] = why
    groups = {}
    for i in range(len(R)): groups.setdefault(find(i), []).append(i)
    # within each folder (library copy) on its own: JP, 2026-11-25
    fparent = list(range(len(R)))
    def ffind(x):
        while fparent[x] != x: fparent[x] = fparent[fparent[x]]; x = fparent[x]
        return x
    for (i, j) in reason:
        if R[i]['source'] == R[j]['source']: fparent[ffind(i)] = ffind(j)
    fgroups = {}
    for i in range(len(R)): fgroups.setdefault((R[i]['source'], ffind(i)), []).append(i)
    for (src, _), g in fgroups.items():
        best = max(g, key=lambda i: rank(R[i]))
        for i in g:
            R[i]['folder_group'] = f"{'P' if src == 'personal library' else 'G'}{min(g) + 1:03d}" if len(g) > 1 else ''
            R[i]['folder_role'] = '' if len(g) == 1 else ('keep (preferred in this folder)' if i == best else 'duplicate within this folder')
    S = seeds(); sd = {s['doi']: s for s in S if s['doi']}; st = {norm(s['title']): s for s in S}
    for r in R:
        s = (sd.get(r['doi']) if r['doi'] else None) or st.get(r['nt'])
        if not s:
            for k, v in st.items():
                if r['nt'] and abs(len(k) - len(r['nt'])) < 25 and difflib.SequenceMatcher(None, k, r['nt'][:len(k)] if len(r['nt'])>len(k) else r['nt']).ratio() >= 0.88: s = v; break
        r['seed_match'] = s['citekey'] if s else ''
    if a.pool:
        P = json.load(open(a.pool)); pd = {p['doi']: p for p in P if p['doi']}; pt = {norm(p['title']): p for p in P if p['title']}
        for r in R:
            p = (pd.get(r['doi']) if r['doi'] else None) or pt.get(r['nt'])
            if not p:
                for k, v in pt.items():
                    if r['nt'] and abs(len(k) - len(r['nt'])) < 25 and difflib.SequenceMatcher(None, k, r['nt']).ratio() >= 0.90: p = v; break
            r['in_older_pool'] = f"{p['added'][:10]} ({p['key']})" if p else ''
    for g in groups.values():
        best = max(g, key=lambda i: rank(R[i]))
        for i in g:
            R[i]['dup_group'] = f"G{min(g) + 1:03d}" if len(g) > 1 else ''
            R[i]['dup_role'] = '' if len(g) == 1 else ('keep (preferred)' if i == best else 'duplicate or older version')
            R[i]['dup_why'] = '; '.join(sorted({reason[(min(i, j), max(i, j))] for j in g if j != i and (min(i, j), max(i, j)) in reason}))
    out = Path(a.out or (Path(a.lib1).parent / 'dedup.json')); out.write_text(json.dumps(R, indent=1, ensure_ascii=False), encoding='utf-8')
    multi = [g for g in groups.values() if len(g) > 1]
    if a.pool: print(f"already in the older pool: {sum(1 for g in groups.values() if any(R[i].get('in_older_pool') for i in g))} of {len(groups)} unique papers")
    for src in sorted({r['source'] for r in R}):
        recs = [r for r in R if r['source'] == src]; dups = sum(1 for r in recs if r['folder_role'] == 'duplicate within this folder')
        print(f"folder '{src}': {len(recs)} records = {len(recs) - dups} distinct papers ({dups} duplicate records within this folder)")
    print(f"records {len(R)} (personal {n1}, group copy {len(R) - n1}); duplicate groups {len(multi)} covering {sum(len(g) for g in multi)} records; to drop {sum(len(g) - 1 for g in multi)}; unique papers {len(groups)}; already in seed set {sum(1 for r in R if r['seed_match'] and r['dup_role'] != 'duplicate or older version')}")
if __name__ == '__main__': main()

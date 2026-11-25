#!/usr/bin/env python3
"""Structural check of the discourse-graph links, so a linking mistake (by a model or a person) is caught. Read-only. Prints a report; exit 1 if any problem.
Checks: (1) every wikilink resolves; (2) EVD <-> CVT agree both ways (the EVD's ## Caveats list vs the CVT's appliesTo); (3) every CVT applies to at least one EVD;
(4) every EVD has exactly one source and at least one claim; (5) every CLM is listed by a QUE; (6) every EP cites evidence from at least two papers; (7) nodes nobody links to.
  python3 check_links.py [--json out.json]"""
import json, os, re, sys, collections
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2]); D = VAULT / 'sysrev' / 'dgraph'
DIRS = {'QUE': 'questions', 'CLM': 'claims', 'EVD': 'evidence', 'CVT': 'caveats', 'SRC': 'source', 'EP': 'evd-patterns'}
pages = {}
for t, d in DIRS.items():
    for f in (D / d).glob('*.md'):
        if f.name.startswith('@') or f.name.split(' - ')[0] == t: pages[f.stem.lower()] = (t, f)
def links(text, strip_fm=False):
    return [re.split(r'[|#]', m)[0].strip().split('/')[-1] for m in re.findall(r'\[\[([^\]]+)\]\]', text)]
def section(text, header):
    m = re.search(rf'^{re.escape(header)}[^\n]*\n(.*?)(?=^#{{1,{len(header) - len(header.lstrip("#"))}}}\s|\Z)', text, re.M | re.S); return m.group(1) if m else ''
issues = collections.defaultdict(list); inbound = collections.Counter(); T = {}
for k, (t, f) in pages.items():
    T[k] = f.read_text(encoding='utf-8')
    for l in links(re.sub(r'!\[\[[^\]]+\]\]', '', T[k])):
        if l.lower() in pages: inbound[l.lower()] += 1
        elif not re.search(r'\.(png|jpg|pdf|xlsx|md)$', l, re.I) and not l.startswith(('http', '#', 'Welcome', 'History')) and l:
            issues['unresolved wikilink'].append(f'{f.stem} -> {l[:70]}')
evd_cvt = collections.defaultdict(set); cvt_evd = collections.defaultdict(set)
for k, (t, f) in pages.items():
    if t == 'CVT':
        fm = T[k].split('---')[1] if T[k].startswith('---') else ''
        for e in re.findall(r'\[\[(?:[^\]|]*/)?(EVD - [^\]|#]+)', fm): cvt_evd[k].add(e.lower()); evd_cvt[e.lower()]  # noqa
        if not cvt_evd[k]: issues['CVT applies to no EVD'].append(f.stem)
for k, (t, f) in pages.items():
    if t != 'EVD': continue
    cav = {l.lower() for l in links(section(T[k], '## Caveats')) if l.startswith('CVT')}
    for c in cav:
        if k not in cvt_evd.get(c, set()): issues['EVD lists a caveat that does not list the EVD back (add the EVD to the CVT appliesTo)'].append(f'{f.stem[:60]}  <-  {c[:60]}')
    for c, es in cvt_evd.items():
        if k in es and c not in cav: issues['CVT lists an EVD that does not list the CVT back'].append(f'{c[:60]}  ->  {f.stem[:60]}')
    srcs = {l for l in links(section(T[k], '## Source')) if l.startswith('@')}
    if len(srcs) != 1: issues['EVD without exactly one source'].append(f.stem)
    if not [l for l in links(section(T[k], '## Supports Claim(s)')) if l.startswith('CLM')]: issues['EVD supports no claim'].append(f.stem[:80])
for k, (t, f) in pages.items():
    if t == 'CLM' and not any(pages[q][0] == 'QUE' and k in {l.lower() for l in links(T[q])} for q in pages): issues['CLM that no question lists'].append(f.stem[:80])
    if t == 'EP':
        papers = set()
        for l in links(section(T[k], '## Supporting Evidence')):
            e = pages.get(l.lower())
            if e: papers |= {x for x in links(section(e[1].read_text(encoding='utf-8'), '## Source'))}
        if len(papers) < 2: issues['EP rests on fewer than 2 papers'].append(f'{f.stem[:70]} ({len(papers)})')
    if t != 'SRC' and inbound[k] == 0: issues['node nobody links to'].append(f.stem[:80])
total = sum(len(v) for v in issues.values())
for name, xs in issues.items():
    print(f'\n## {name}: {len(xs)}'); [print('  ', x) for x in xs[:8]]; print('   ...' if len(xs) > 8 else '', end='')
print(f'\n\n{len(pages)} nodes checked; {total} problem(s).')
if '--json' in sys.argv: Path(sys.argv[sys.argv.index('--json') + 1]).write_text(json.dumps(issues, indent=1))
sys.exit(1 if total else 0)

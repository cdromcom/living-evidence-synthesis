#!/usr/bin/env python3
"""Test (JP, 2026-11-26): a simpler replacement for the numbers-list check. Every number written in a finding's statement should appear in the text of the PDF pages the finding cites (spans and numbers entries). No separate list to keep in sync. Numbers that do not appear are either derived (an average the authors did not print) or wrong, and go to a person. Usage: numbers_on_pages.py RUN [RUN...]"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz, lives_run as LR, lives_stages as S, pdf_pages as pp

NUM = LR.NUM_IN_TEXT


def norm(t): return re.sub(r'(?<=\d),(?=\d{3})', '', t.replace(' ', ' ').replace('−', '-').replace(' ', ' '))


def variants(tok):
    t = norm(tok).rstrip('%'); out = {t}
    if t.startswith('0.'): out.add(t[1:])          # .58 for 0.58
    if t.startswith('.'): out.add('0' + t)
    if '%' in tok:
        try: out.add(str(round(float(t) / 100, 4)).rstrip('0').rstrip('.'))
        except ValueError: pass
    return out


def check(M, ck, p):
    f_ = M.dir / ck / 'picost.json'
    if p.get('failed') or not f_.exists(): return []
    ps = json.loads(f_.read_text(encoding='utf-8')); doc = fitz.open(S.ex(p['pdf'])); res = []
    for f in ps.get('findings', []):
        pgs = sorted({s.get('pdf_page') for s in f.get('spans', []) if s.get('pdf_page')} | {n.get('pdf_page') for n in f.get('numbers', []) if n.get('pdf_page')})
        text = norm(' '.join(pp.page_text(doc[i - 1]) for i in pgs if 1 <= i <= len(doc)))
        toks = [t for t in NUM.findall(f.get('statement', ''))]; miss = []
        for t in toks:
            if not any(re.search(r'(?<![\d.])' + re.escape(v) + r'(?![\d])', text) for v in variants(t)): miss.append(t)
        res.append({'paper': ck, 'id': f['id'], 'pages': pgs, 'numbers': toks, 'not_on_cited_pages': miss, 'old_flag': 'number_not_in_numbers_list' in f.get('flags', []), 'old_gaps': (f.get('numbers_list_gaps') or {}).get('missing', []), 'statement': f.get('statement', '')[:200]})
    doc.close(); return res


if __name__ == '__main__':
    allr = []
    for run in sys.argv[1:]:
        M = LR.Manifest(run)
        for ck, p in M.m['papers'].items(): allr += check(M, ck, p)
    n = len(allr); old = sum(r['old_flag'] for r in allr); new = sum(bool(r['not_on_cited_pages']) for r in allr)
    print(f'{n} findings; old numbers-list check flags {old}; numbers-on-cited-pages check flags {new}; both {sum(r["old_flag"] and bool(r["not_on_cited_pages"]) for r in allr)}')
    for r in allr:
        if r['not_on_cited_pages']: print(' NEW', r['paper'][:7], r['id'], 'pages', r['pages'], 'missing', r['not_on_cited_pages'], '| old gaps', r['old_gaps'], '|', r['statement'][:110])
    for r in allr[:200]:
        if r['old_flag'] and not r['not_on_cited_pages']: print(' OLD-ONLY', r['paper'][:7], r['id'], 'old gaps', r['old_gaps'])
    pass   # results are printed; nothing is saved

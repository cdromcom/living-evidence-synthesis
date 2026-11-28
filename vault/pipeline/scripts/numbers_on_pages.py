#!/usr/bin/env python3
"""Test (JP, 2026-11-26): a simpler replacement for the numbers-list check. Every number written in a finding's statement should appear in the text of the PDF pages the finding cites (spans and numbers entries). No separate list to keep in sync. Numbers that do not appear are either derived (an average the authors did not print) or wrong, and go to a person. Usage: numbers_on_pages.py RUN [RUN...]"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz, lives_run as LR, lives_stages as S, pdf_pages as pp

NUM = LR.NUM_IN_TEXT


def norm(t): return re.sub(r'(?<=\d),(?=\d{3})', '', pp.repair_cell_text(t).replace('\u00a0', ' ').replace('\u2212', '-').replace('\u2009', ' '))   # repair: symbol problems of the text layer (en dash stored as e, private-use digits, and so on)


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
        toks = [t for t in NUM.findall(f.get('statement', ''))]; miss = []; tn = None
        for t in toks:
            if any(re.search(r'(?<![\d.])' + re.escape(v) + r'(?![\d])', text) for v in variants(t)): continue
            if tn is None: tn = set().union(*[pp.table_numbers(doc[i - 1]) for i in pgs if 1 <= i <= len(doc)])   # numbers in table cells and in table captions and footnotes of the cited pages (JP, 2026-11-27)
            if not any(pp._number_set(v) & tn for v in variants(t)): miss.append(t)
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


# ---- numbers that are not in the PDF text layer: ask Liquid d1.2-ultra to look for them on the screenshots (JP, 2026-11-26)
import decision_models as dm, random as _rnd


def images_for(M, ck, f):
    d = M.dir / ck; out = []
    for c in (d / 'crops' / f"{f['id']}.png",):
        if c.exists(): out.append(str(c))
    mg = f.get('merged_screenshot'); hl = sorted((d / 'highlights').glob(f"{f['id']}_s*_p*.png"))
    if mg and (d / 'highlights' / mg).exists(): out.append(str(d / 'highlights' / mg))
    else: out += [str(x) for x in hl[:2]]
    return out[:3]


def ask_numbers(imgs, tokens, alter=False):
    qs = {}
    for i, t in enumerate(tokens):
        shown = t
        if alter:
            ds = [m for m in re.finditer(r'\d', t)]
            if ds: m = _rnd.choice(ds); shown = t[:m.start()] + str((int(m.group()) + 3) % 10) + t[m.end():]
        qs[f'n{i}'] = dm.noul(f'Does the number {shown} appear, exactly as written, in the table, figure or text shown in the images?')
    r, e = dm.decide('liquid', 'Page images of a research paper; a table or figure may hold the numbers.', qs, images=imgs)
    return [((r or {}).get('answers') or {}).get(f'n{i}', {}).get('noul') for i in range(len(tokens))]


def screenshot_check(M, results):
    """For findings whose statement numbers are not in the cited pages' text, look for each number on the screenshots; also run each flagged number with one digit changed as a control (should score low)."""
    out = []
    byck = {ck: json.loads((M.dir / ck / 'picost.json').read_text(encoding='utf-8')) for ck, p in M.m['papers'].items() if (M.dir / ck / 'picost.json').exists() and not p.get('failed')}
    for r in results:
        if not r['not_on_cited_pages']: continue
        f = next(x for x in byck[r['paper']]['findings'] if x['id'] == r['id']); imgs = images_for(M, r['paper'], f); toks = list(dict.fromkeys(r['not_on_cited_pages']))
        if not imgs: out.append({**r, 'tokens': toks, 'found': [None] * len(toks), 'control': [None] * len(toks), 'images': []}); continue
        out.append({**r, 'tokens': toks, 'found': ask_numbers(imgs, toks), 'control': ask_numbers(imgs, toks, alter=True), 'images': imgs})
    return out


def classify(tok, found, control):
    if found is None: return 'no screenshot'
    if len(re.sub(r'\D', '', tok)) < 2: return 'too short to check by image'
    if found >= 0.5 and (control or 0) < 0.5: return 'seen on screenshot'
    if found >= 0.5: return 'unclear (a changed number also scored high)'
    return 'not found: JP check'


def run_numbers_check(M):
    """Pipeline step (after verification): statement numbers that are not in the text of the cited pages are looked up on the screenshots by Liquid d1.2-ultra; the rest go to JP. Writes numbers_check.json in the run folder."""
    res = []
    for ck, p in M.m['papers'].items(): res += check(M, ck, p)
    out = screenshot_check(M, res)
    for x in out: x['result'] = [classify(t, f, c) for t, f, c in zip(x['tokens'], x['found'], x['control'])]
    (M.dir / 'numbers_check.json').write_text(json.dumps({'checked_findings': len(res), 'flagged': out}, indent=1, ensure_ascii=False), encoding='utf-8')
    st = M.m['stage_log'].setdefault('numbers_check', {}); st.update(status='done', findings=len(res), flagged=len(out), numbers_for_jp=sum(r == 'not found: JP check' for x in out for r in x['result'])); M.save()
    return out

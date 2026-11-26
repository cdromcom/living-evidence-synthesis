#!/usr/bin/env python3
"""Build a human-inspection workbook (.xlsx, opens in Google Sheets) of the TRIPOD-LLM and Quality appraisal rows: the quote, where it is,
the curator's judgment (dropdown), the script's PDF check, each decision model's verdict, and columns for JP's own judgment.
Same idea as the EVD validation sheets. Read-only on the vault.
  python3 signals_to_gsheet.py [--only @citekey] [--audit audit.csv] [--models decision-models.jsonl] [--out FILE]"""
import argparse, csv, json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
import re
import signals_common as sc


def prov(path, kind):
    """Which model made this content, from the page's own frontmatter (curatedWithModel / curatedWithModelDate) and the vault logs."""
    fm = path.read_text(encoding='utf-8').split('---')[1] if path.read_text(encoding='utf-8').startswith('---') else ''
    m = re.search(r'^curatedWithModel:\s*"?([^"\n]+)"?', fm, re.M); d = re.search(r'^curatedWithModelDate:\s*(\S+)', fm, re.M)
    cur = f"{m.group(1).strip()}, {d.group(1)}" if m and d else 'not recorded'
    if kind == 'QUALITY':
        return cur, cur, 'Rewritten with a verbatim quote and locator per row in the 2026-08 pass (HISTORY.md, Grounding every rating in a quote). First draft 2026-04-28 (Phase 19): Claude Code subagents, model not recorded.'
    return ('2026-04-28 first draft: Claude Code subagents, model not recorded (Phase 18); quotes re-verified ' + cur, cur, 'Ratings first written 2026-04-28 (History.md Phase 18, 26 parallel subagents); quotes and locators re-curated in the 2026-08 pass by the model in the previous column.')

ap = argparse.ArgumentParser(); ap.add_argument('--only'); ap.add_argument('--audit'); ap.add_argument('--models')
ap.add_argument('--out', default=str(sc.VAULT / 'pipeline/misc/evd-validation/signals-review.xlsx')); a = ap.parse_args()
RAT = ['Addressed', 'Partly addressed', 'Not addressed', 'Not applicable']
audit = {(r['citekey'], r['kind'], r['row']): r for r in csv.DictReader(open(a.audit))} if a.audit and Path(a.audit).exists() else {}
mods = {}
if a.models and Path(a.models).exists():
    for r in map(json.loads, open(a.models)):
        if not r.get('error') and r.get('answers'): mods[(r['citekey'], r['kind'], r['row'], r['provider'])] = r['answers']
HEAD = ['Source', 'Row', 'Item / domain', 'Quote (verbatim)', 'Locator as written', 'Cited page', 'PDF check (script)', 'Found on (pdf:printed page)', 'Why not verbatim (script)',
        'Judgment (rating in LIVES)', 'Rating made by (model, date)', 'Quote and locator sourced by (model, date)', 'Provenance note', 'Perplexity: rating it supports', 'Perplexity: P(rating supported)', 'Liquid d1-ultra: rating it supports',
        'Liquid d1-ultra: P(rating supported)', 'Models agree with judgment (of 2)',
        'JP judgment', 'JP notes', 'Run / version']
W = [26, 8, 36, 70, 24, 8, 26, 16, 30, 18, 24, 24, 46, 16, 10, 16, 10, 12, 18, 40, 22]
wb = Workbook(); ab = wb.active; ab.title = 'ABOUT'
for i, t in enumerate(['Quality signals review sheet', 'One row per TRIPOD-LLM item or Quality appraisal domain of each source paper. Quote and locator are copied from the vault page. '
        '"PDF check" is a script: is the quote verbatim in the PDF and is the cited page right (printed page; PDF position where the PDF prints no page numbers). '
        '"Rating made by" and "Quote and locator sourced by" come from each source page\'s curatedWithModel frontmatter (2026-08-25, Claude Sonnet 5) and the vault logs (History.md); the April 2026 first drafts have no recorded model. Decision-model columns come from Perplexity Decider 1.3, Liquid d1-ultra and Jev answering: which rating does the quote itself support, and does it support the judgment. '
        'JP judgment is yours: choose from the dropdown; leave blank to agree. Static values, built by pipeline/scripts/signals_to_gsheet.py.'], 1):
    ab.cell(i, 1, t).alignment = Alignment(wrap_text=True, vertical='top')
ab.column_dimensions['A'].width = 120; ab['A1'].font = Font(bold=True, size=14); ab.row_dimensions[2].height = 110
fills = {'Addressed': 'D9EAD2', 'Partly addressed': 'FFF2CC', 'Not addressed': 'F4CCCC', 'Not applicable': 'EEEEEE'}
cnt = {}
for kind, title in (('TRIPOD', 'TRIPOD-LLM'), ('QUALITY', 'Quality appraisal')):
    ws = wb.create_sheet(title); ws.append(HEAD)
    for c in ws[1]: c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical='top'); c.fill = PatternFill('solid', fgColor='D9EAD2')
    n = 0
    for path in sorted(sc.SRC_DIR.glob('@*.md')):
        if a.only and path.stem.lstrip('@') != a.only.lstrip('@'): continue
        for r in sc.source_rows(path):
            if r['kind'] != kind: continue
            k = (r['citekey'], kind, r['row']); au = audit.get(k, {}); mm = {p: mods.get(k + (p,)) for p in ('perplexity', 'liquid')}
            def v(p, key): return (mm[p] or {}).get(key, {}).get('choice' if key == 'rating' else 'noul') if mm[p] else None
            agree = sum(1 for p in mm if mm[p] and v(p, 'rating') == r['rating']) if any(mm.values()) else None
            pr = prov(path, kind)
            ws.append([r['citekey'], r['row'], r['item'][:150], r['quote'], r['locator'], r['page'], au.get('status', ''), au.get('found_pages', ''), au.get('cause', ''), r['rating'],
                       pr[0], pr[1], pr[2], v('perplexity', 'rating'), v('perplexity', 'rating_supported'), v('liquid', 'rating'), v('liquid', 'rating_supported'),
                       agree, '', '', 'vault 2026-11-24'])
            n += 1
    cnt[title] = n
    for i, w in enumerate(W, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
        for c in row:
            if isinstance(c.value, float): c.number_format = '0.00'
    ws.freeze_panes = 'D2'; last = ws.max_row; HC = {h: ws.cell(1, i + 1).column_letter for i, h in enumerate(HEAD)}
    JC = [ws.cell(1, i + 1).column_letter for i, h in enumerate(HEAD) if h in ('Judgment (rating in LIVES)', 'JP judgment') or h.endswith(': rating it supports')]
    for col in JC:
        dv = DataValidation(type='list', formula1='"' + ','.join(RAT) + '"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'{col}2:{col}{max(last, 2)}')
        for name, colr in fills.items(): ws.conditional_formatting.add(f'{col}2:{col}{max(last, 2)}', CellIsRule(operator='equal', formula=[f'"{name}"'], fill=PatternFill('solid', bgColor=colr)))
    ws.conditional_formatting.add(f'G2:G{max(last, 2)}', FormulaRule(formula=['OR(ISNUMBER(SEARCH("WRONG",G2)),ISNUMBER(SEARCH("NOT found",G2)),ISNUMBER(SEARCH("not printed",G2)))'], fill=PatternFill('solid', bgColor='F4CCCC')))
Path(a.out).parent.mkdir(parents=True, exist_ok=True); wb.save(a.out); print('saved', a.out, cnt)

#!/usr/bin/env python3
"""Build the step-by-step review workbook for one runner batch (JP, 2026-11-25): a human follows each paper from extraction to checks and adds ground-truth labels.
  python3 run_to_gsheet.py RUN_ID [--out FILE]          writes pipeline/runs/<run>/review.xlsx (local; upload it to Google Sheets with the Drive connector)
Tabs: ABOUT (how to read it), Papers, Findings (one row per extracted finding, with every check and JP's label columns), Checks (one row per quoted span), Rechecks
(Neon vs Sol vs Opus for the flagged findings), Checks (decision models, Sol vision, Opus), Drafts and debate, Quality signals (raw and vote), Calls and cost; see Review-sheets-spec.md."""
import argparse, json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl
HDR = Font(bold=True, color='FFFFFF'); FILL = PatternFill('solid', fgColor='2F5D3A'); JP = PatternFill('solid', fgColor='FFF2CC'); WRAP = Alignment(wrap_text=True, vertical='top')
def nums(f): return '; '.join(f"{n.get('label', '')}: {n.get('value', '')}{n.get('unit', '')} (p. {n.get('printed_page', '')}, {n.get('table_or_figure', '')} {n.get('row', '')} {n.get('column', '')})".strip() for n in f.get('numbers', []))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--out'); a = ap.parse_args(); d = cl.RUNS / a.run; M = json.load(open(d / 'manifest.json')); wb = Workbook(); wb.remove(wb.active)
    def tab(title, header, rows, widths, jp_from=None):
        ws = wb.create_sheet(title); ws.append(header)
        for i, c in enumerate(ws[1], 1):
            c.font = HDR; c.fill = FILL; c.alignment = WRAP
            if jp_from and i >= jp_from: c.fill = PatternFill('solid', fgColor='B8860B')
        for r in rows: ws.append(r)
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = 'C2'; return ws
    ab = wb.create_sheet('ABOUT'); ab.column_dimensions['A'].width = 26; ab.column_dimensions['B'].width = 120
    for k, t in [('Run', f"{M['run_id']} ({M['mode']} mode, cap ${M['cap_usd']}, spent ${M['spent_usd']:.2f}, status {M['status']}). Research question: {M.get('question') or 'not given'}"),
                 ('Steps (in order)', '1 Neon extracts findings in three tiers (primary answers the RQ; secondary is meta or contextual about a primary finding; tertiary is other context). 2 PyMuPDF finds every quoted span, boxes it and checks each number is on the page. 3 GPT-6.2 Sol re-extracts flagged findings blind. 4 Claude Opus 5.5 adjudicates disagreements. 5 You review (this sheet). Later: decision-model gates, drafts and debate, quality-signal ratings.'),
                 ('How to review', 'Go to the Findings tab. Sort by Flags and Tier. Yellow-headed columns are yours: say whether the tier, statement and numbers are right, add findings that were missed, and note why. Your labels are the ground truth for later accuracy numbers.'),
                 ('Flags', 'low_confidence (Neon says so); multi_page (cited on more than one page); span_not_found, span_on_other_page, number_not_in_pdf_text (the quote or number was not found where it should be); no_text_layer (scanned).'),
                 ('Costs', 'See Calls and cost. Batch mode is about half price; the cap is a hard limit per batch.')]:
        ab.append([k, t]); ab.cell(ab.max_row, 1).font = Font(bold=True); ab.cell(ab.max_row, 1).alignment = WRAP; ab.cell(ab.max_row, 2).alignment = WRAP
    prow = []; frow = []; crow = []; rrow = []
    for ck, p in M['papers'].items():
        pj = d / ck / 'picost.json'
        if not pj.exists(): prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], p.get('failed') or 'no extraction', '', '', '', '']); continue
        ps = json.load(open(pj)); fs = ps.get('findings', []); tiers = {t: sum(1 for f in fs if f.get('tier') == t) for t in ('primary', 'secondary', 'tertiary')}
        adj = {x['id']: x for x in (p.get('adjudication') or {}).get('adjudications', [])}; rc = {f['id']: f for f in (p.get('recheck') or {}).get('findings', [])}
        prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], 'ok', f"{tiers['primary']} / {tiers['secondary']} / {tiers['tertiary']}", len(p.get('flagged', [])), len(p.get('disagreements', [])), round(sum(v.get('cost_usd', 0) for v in p['stages'].values() if isinstance(v, dict)), 3)])
        for f in fs:
            v = adj.get(f['id']); frow.append([ck, f['id'], f.get('tier', ''), f.get('tier_reason', ''), '; '.join(f.get('supports', [])), f.get('statement', ''), f.get('P', ''), f.get('I', ''), f.get('C', ''), f.get('O', ''), f.get('S', ''), f.get('T', ''), nums(f),
                                               f.get('confidence', ''), ', '.join(f.get('flags', [])), 'yes' if f['id'] in p.get('flagged', []) else 'no', ('different' if f['id'] in p.get('disagreements', []) else 'agrees') if f['id'] in rc else '', v['verdict'] if v else '', f.get('merged_screenshot') or '', '; '.join(f.get('answers_QUE', [])), '', '', '', '', ''])
            for k, sp in enumerate(f.get('spans', []), 1): crow.append([ck, f['id'], k, sp.get('text', '')[:300], sp.get('pdf_page', ''), 'yes' if sp.get('found') else 'NO', ', '.join(map(str, sp.get('pages_found', []))), len(sp.get('bbox', [])), '', ''])
            if f['id'] in rc: rrow.append([ck, f['id'], '; '.join(str(n.get('value')) for n in f.get('numbers', [])), '; '.join(str(n.get('value')) for n in rc[f['id']].get('numbers', [])), ('different' if f['id'] in p.get('disagreements', []) else 'agrees'), (adj.get(f['id']) or {}).get('verdict', ''), (adj.get(f['id']) or {}).get('reason', ''), '', ''])
    tab('Papers', ['Paper', 'File', 'Pages', 'Status', 'Findings primary / secondary / tertiary', 'Flagged', 'Disagreements', 'Cost USD'], prow, [40, 50, 7, 12, 22, 9, 12, 10])
    ws = tab('Findings', ['Paper', 'Id', 'Tier', 'Why this tier', 'Supports', 'Statement (Neon)', 'Population', 'Intervention', 'Comparator', 'Outcome', 'Study design', 'Timeframe', 'Numbers with locators', 'Confidence', 'Flags', 'Sent to recheck', 'Sol vs Neon', 'Opus verdict', 'Merged screenshot', 'Answers question(s)',
                      'JP: tier right? (yes/no)', 'JP: correct tier', 'JP: statement and numbers right? (yes/no)', 'JP: missed finding (describe)', 'JP: notes'], frow, [30, 6, 10, 30, 10, 60, 22, 22, 22, 22, 18, 14, 50, 10, 24, 9, 10, 10, 22, 14, 12, 12, 14, 30, 30], jp_from=21)
    for col in range(21, 26): ws.cell(1, col).fill = PatternFill('solid', fgColor='B8860B')
    dv = DataValidation(type='list', formula1='"yes,no,unsure"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'U2:U{ws.max_row + 1}'); dv.add(f'W2:W{ws.max_row + 1}')
    dv2 = DataValidation(type='list', formula1='"primary,secondary,tertiary,not an EVD"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'V2:V{ws.max_row + 1}'); ws.auto_filter.ref = ws.dimensions
    tab('Checks', ['Paper', 'Finding', 'Span', 'Quoted span (verbatim)', 'Page cited', 'Found in PDF text', 'Pages where found', 'Word boxes', 'JP: quote correct? (yes/no)', 'JP: notes'], crow, [30, 8, 6, 80, 9, 10, 14, 9, 14, 30], jp_from=9)
    tab('Rechecks', ['Paper', 'Finding', 'Neon numbers', 'Sol numbers', 'Compare', 'Opus verdict (A = Neon, B = Sol)', 'Opus reason', 'JP: who is right? (Neon, Sol, neither)', 'JP: notes'], rrow, [30, 8, 40, 40, 10, 14, 60, 16, 30], jp_from=8)
    crows = []
    f = d / 'calls.jsonl'
    for l in (f.read_text().splitlines() if f.exists() else []):
        r = json.loads(l); crows.append([r.get('ts_utc', '')[:19], r.get('citekey', ''), r.get('step', ''), r.get('model', ''), r.get('effort', ''), r.get('tokens_in'), r.get('tokens_out'), r.get('cost_usd_est'), (r.get('notes') or '')[:80]])
    tab('Calls and cost', ['Time (UTC)', 'Paper', 'Step', 'Model', 'Effort', 'Tokens in', 'Tokens out (incl. thinking)', 'Cost USD (list price; batch is half)', 'Notes'], crows, [20, 30, 12, 20, 8, 10, 14, 14, 50])
    out = a.out or str(d / 'review.xlsx'); wb.save(out); print('saved', out, '| findings', len(frow), '| spans', len(crow))
if __name__ == '__main__': main()

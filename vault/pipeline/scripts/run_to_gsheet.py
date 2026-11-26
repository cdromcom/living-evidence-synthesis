#!/usr/bin/env python3
"""Build the step-by-step review workbook for one runner batch (JP, 2026-11-25): a human follows each paper from extraction to checks and adds ground-truth labels.
  python3 run_to_gsheet.py RUN_ID [--out FILE]          writes pipeline/runs/<run>/review.xlsx (local; upload it to Google Sheets with the Drive connector)
Tabs: ABOUT (how to read it), Papers, Findings (one row per extracted finding, with every check and JP's label columns), Checks (one row per quoted span), Rechecks
(Neon vs Sol vs Opus for the flagged findings), Checks (decision models, Sol vision, Opus), Drafts and debate, Quality signals (raw and vote), Calls and cost; see Review-sheets-spec.md."""
import argparse, json, sys
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as XlImage
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl
HDR = Font(bold=True, color='FFFFFF'); FILL = PatternFill('solid', fgColor='2F5D3A'); JP = PatternFill('solid', fgColor='FFF2CC'); WRAP = Alignment(wrap_text=True, vertical='top')
def nums(f): return '; '.join(f"{n.get('label', '')}: {n.get('value', '')}{n.get('unit', '')} (p. {n.get('printed_page', '')}, {n.get('table_or_figure', '')} {n.get('row', '')} {n.get('column', '')})".strip() for n in f.get('numbers', []))
def put_image(ws, d, row, col, path, width, thumbs):
    """Place a (downsized) PNG in a cell of the sheet and grow the row to fit it. Google Sheets keeps these as pictures sitting in the cell."""
    if not path or not Path(path).exists(): return 0
    thumbs.mkdir(exist_ok=True); out = thumbs / (Path(path).parent.parent.name[:12] + '_' + Path(path).stem + '.jpg')   # JPEG keeps the workbook under the 10 MB upload limit
    im = PILImage.open(path).convert('RGB'); width = min(width, int(520 * im.width / im.height))   # never taller than the tallest row Sheets allows (about 400 pt), or it spills into the next row
    im = im.resize((width, max(1, int(im.height * width / im.width))), PILImage.LANCZOS); im.save(out, quality=72, optimize=True)
    x = XlImage(str(out)); x.anchor = f'{get_column_letter(col)}{row}'; ws.add_image(x)
    ws.column_dimensions[get_column_letter(col)].width = width / 7 + 1
    h = im.height * 0.75 + 4
    if (ws.row_dimensions[row].height or 0) < h: ws.row_dimensions[row].height = min(h, 400)
    return h


def first(globs):
    for g_ in globs:
        for p_ in sorted(g_[0].glob(g_[1])): return p_
    return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--out'); a = ap.parse_args(); d = cl.RUNS / a.run; M = json.load(open(d / 'manifest.json')); wb = Workbook(); wb.remove(wb.active); thumbs = d / '_thumbs'
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
    prow = []; frow = []; crow = []; rrow = []; fkeys = []; ckeys = []
    for ck, p in M['papers'].items():
        pj = d / ck / 'picost.json'
        if not pj.exists(): prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], p.get('failed') or 'no extraction', '', '', '', '']); continue
        ps = json.load(open(pj)); fs = ps.get('findings', []); tiers = {t: sum(1 for f in fs if f.get('tier') == t) for t in ('primary', 'secondary', 'tertiary')}
        adj = {x['id']: x for x in (p.get('adjudication') or {}).get('adjudications', [])}; rc = {f['id']: f for f in (p.get('recheck') or {}).get('findings', [])}
        prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], 'ok', f"{tiers['primary']} / {tiers['secondary']} / {tiers['tertiary']}", len(p.get('flagged', [])), len(p.get('disagreements', [])), round(sum(v.get('cost_usd', 0) for v in p['stages'].values() if isinstance(v, dict)), 3)])
        for f in fs:
            fkeys.append((ck, f)); v = adj.get(f['id']); frow.append([ck, f['id'], f.get('tier', ''), f.get('tier_reason', ''), '; '.join(f.get('supports', [])), f.get('statement', ''), f.get('P', ''), f.get('I', ''), f.get('C', ''), f.get('O', ''), f.get('S', ''), f.get('T', ''), nums(f),
                                               f.get('confidence', ''), ', '.join(f.get('flags', [])), 'yes' if f['id'] in p.get('flagged', []) else 'no', ('different' if f['id'] in p.get('disagreements', []) else 'agrees') if f['id'] in rc else '', v['verdict'] if v else '', f.get('merged_screenshot') or '', '; '.join(f.get('answers_QUE', [])), '', '', '', '', ''])
            for k, sp in enumerate(f.get('spans', []), 1): ckeys.append((ck, f['id'], k)); crow.append([ck, f['id'], k, sp.get('text', '')[:300], sp.get('pdf_page', ''), 'yes' if sp.get('found') else 'NO', ', '.join(map(str, sp.get('pages_found', []))), len(sp.get('bbox', [])), '', ''])
            if f['id'] in rc: rrow.append([ck, f['id'], '; '.join(str(n.get('value')) for n in f.get('numbers', [])), '; '.join(str(n.get('value')) for n in rc[f['id']].get('numbers', [])), ('different' if f['id'] in p.get('disagreements', []) else 'agrees'), (adj.get(f['id']) or {}).get('verdict', ''), (adj.get(f['id']) or {}).get('reason', ''), '', ''])
    frow = [r[:19] + ['', ''] + r[19:] for r in frow]; crow = [r[:8] + [''] + r[8:] for r in crow]
    tab('Papers', ['Paper', 'File', 'Pages', 'Status', 'Findings primary / secondary / tertiary', 'Flagged', 'Disagreements', 'Cost USD'], prow, [40, 50, 7, 12, 22, 9, 12, 10])
    ws = tab('Findings', ['Paper', 'Id', 'Tier', 'Why this tier', 'Supports', 'Statement (Neon)', 'Population', 'Intervention', 'Comparator', 'Outcome', 'Study design', 'Timeframe', 'Numbers with locators', 'Confidence', 'Flags', 'Sent to recheck', 'Sol vs Neon', 'Opus verdict', 'Merged screenshot', 'Evidence crop (image)', 'Highlighted page (image)', 'Answers question(s)',
                      'JP: tier right? (yes/no)', 'JP: correct tier', 'JP: statement and numbers right? (yes/no)', 'JP: missed finding (describe)', 'JP: notes'], frow, [30, 6, 10, 30, 10, 60, 22, 22, 22, 22, 18, 14, 50, 10, 24, 9, 10, 10, 22, 60, 50, 14, 12, 12, 14, 30, 30], jp_from=23)
    for i, (ck_, f_) in enumerate(fkeys, 2):
        pd = d / ck_; hl = sorted((pd / 'highlights').glob(f"{f_['id']}_s*_p*.png")); mg = (pd / 'highlights' / f_['merged_screenshot']) if f_.get('merged_screenshot') else None
        put_image(ws, d, i, 20, pd / 'crops' / f"{f_['id']}.png", 420, thumbs); put_image(ws, d, i, 21, mg if (mg and mg.exists()) else (hl[0] if hl else None), 340, thumbs)
    for col in range(23, 28): ws.cell(1, col).fill = PatternFill('solid', fgColor='B8860B')
    dv = DataValidation(type='list', formula1='"yes,no,unsure"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'W2:W{ws.max_row + 1}'); dv.add(f'Y2:Y{ws.max_row + 1}')
    dv2 = DataValidation(type='list', formula1='"primary,secondary,tertiary,not an EVD"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'X2:X{ws.max_row + 1}'); ws.auto_filter.ref = ws.dimensions
    wsc = tab('Checks', ['Paper', 'Finding', 'Span', 'Quoted span (verbatim)', 'Page cited', 'Found in PDF text', 'Pages where found', 'Word boxes', 'Highlighted page (image)', 'JP: quote correct? (yes/no)', 'JP: notes'], crow, [30, 8, 6, 60, 9, 10, 14, 9, 40, 14, 30], jp_from=10)
    for i, (ck_, fid_, k_) in enumerate(ckeys, 2):
        h_ = sorted((d / ck_ / 'highlights').glob(f'{fid_}_s{k_}_p*.png')); put_image(wsc, d, i, 9, h_[0] if h_ else None, 300, thumbs)
    tab('Rechecks', ['Paper', 'Finding', 'Neon numbers', 'Sol numbers', 'Compare', 'Opus verdict (A = Neon, B = Sol)', 'Opus reason', 'JP: who is right? (Neon, Sol, neither)', 'JP: notes'], rrow, [30, 8, 40, 40, 10, 14, 60, 16, 30], jp_from=8)
    ck_rows = []; ck_crops = []; dr_rows = []; qr_rows = []; qa_rows = []
    for ck, p in M['papers'].items():
        if (d / ck / 'checks.json').exists():
            for v in json.load(open(d / ck / 'checks.json')):
                m = v['summary']['means']; ck_crops.append(v.get('crop')); ck_rows.append([ck, v['id'], v.get('tier', ''), v.get('statement', '')[:300], m.get('relevancy', ''), m.get('fidelity', ''), m.get('quote_grounding', ''), m.get('table_figure_grounding', ''), v['summary']['score'], v['summary']['spread'], '; '.join(v.get('why_vision', [])),
                                                         (v.get('sol') or {}).get('overall', ''), (v.get('sol') or {}).get('reason', ''), (v.get('opus') or {}).get('overall', ''), (v.get('opus') or {}).get('reason', ''), v.get('final', ''), '', '', ''])
        if (d / ck / 'drafts.json').exists():
            dd = json.load(open(d / ck / 'drafts.json'))
            def txt_of(x): return x.get('statement') or x.get('title') or x.get('limitation') or ''
            for nid, f in dd.get('finals', {}).items():
                n = f['node']; alts = [txt_of(dd['authors'].get(a_, {}).get('r0', {}).get(nid, {})) for a_ in ('sonnet', 'sol', 'neon')]
                cc = f.get('claim_check') or {}; lt = f['lint']
                dr_rows.append([ck, nid, n.get('type', ''), n.get('tier', ''), f['author'], f['how'], txt_of(n), lt.get('chars', ''), lt.get('fk_grade', ''), 'yes' if lt.get('pass') else 'no', ', '.join(lt.get('numbers_not_on_card', [])), cc.get('overall', ''), cc.get('fix', ''), cc.get('checker', ''), (f.get('dm') or {}).get('score', ''), f.get('status', ''), alts[0], alts[1], alts[2], '', '', '', ''])
        if (d / ck / 'quality_signals.json').exists():
            q = json.load(open(d / ck / 'quality_signals.json'))
            for x in q['raw']: qr_rows.append([ck, x['signal'], x['rater'], 'yes' if x['counted'] else 'benchmark only', x['rating'], x['quote'][:400], x['locator'], '' if x['quote_found'] is None else ('yes' if x['quote_found'] else 'NO')])
            for x in q['aggregate']: qa_rows.append([ck, x['signal'], ', '.join(f'{k}: {v}' for k, v in x['votes'].items()), x['majority'], x['agreement'], x['quotes_not_found'], '', ''])
    if ck_rows:
        ws2 = tab('Checks (decision models)', ['Paper', 'Finding', 'Tier', 'Statement', 'Relevancy', 'Fidelity', 'Quote grounding', 'Table or figure grounding', 'Score (lowest mean)', 'Spread between models', 'Why Sol looked', 'Sol vision', 'Sol reason', 'Opus (disputes only)', 'Opus reason', 'Result', 'Crop Sol looked at (image)', 'JP: is the finding right? (yes/no)', 'JP: notes'], ck_rows, [30, 7, 10, 60, 9, 9, 9, 10, 9, 9, 30, 10, 40, 10, 40, 10, 60, 14, 30], jp_from=18)
        for i, cp in enumerate(ck_crops, 2): put_image(ws2, d, i, 17, cp, 440, thumbs)
    if dr_rows: tab('Drafts and debate', ['Paper', 'Node', 'Type', 'Tier', 'Winner by', 'How decided', 'Winning text', 'Chars', 'Reading grade', 'Lint pass', 'Numbers not on the card', 'Claim check', 'Fix suggested', 'Checked by', 'Decision-model score', 'Status', 'First draft: Sonnet', 'First draft: Sol', 'First draft: Neon', 'JP: best text or your own', 'JP: fidelity (yes/partly/no)', 'JP: style (good/ok/poor)', 'JP: notes'], dr_rows, [30, 8, 6, 10, 9, 18, 70, 7, 8, 7, 14, 10, 30, 9, 10, 18, 50, 50, 50, 40, 14, 14, 30], jp_from=20)
    if qr_rows: tab('Quality signals (raw)', ['Paper', 'Signal', 'Rater', 'Counted in the vote', 'Rating', 'Quote', 'Locator', 'Quote found in PDF'], qr_rows, [30, 22, 8, 12, 16, 70, 24, 10])
    if qa_rows: tab('Quality signals (vote)', ['Paper', 'Signal', 'Votes', 'Majority', 'Agreement', 'Quotes not found', 'JP: correct rating', 'JP: notes'], qa_rows, [30, 22, 40, 16, 10, 10, 16, 30], jp_from=7)
    crows = []
    f = d / 'calls.jsonl'
    for l in (f.read_text().splitlines() if f.exists() else []):
        r = json.loads(l); crows.append([r.get('ts_utc', '')[:19], r.get('citekey', ''), r.get('step', ''), r.get('model', ''), r.get('effort', ''), r.get('tokens_in'), r.get('tokens_out'), r.get('cost_usd_est'), (r.get('notes') or '')[:80]])
    tab('Calls and cost', ['Time (UTC)', 'Paper', 'Step', 'Model', 'Effort', 'Tokens in', 'Tokens out (incl. thinking)', 'Cost USD (list price; batch is half)', 'Notes'], crows, [20, 30, 12, 20, 8, 10, 14, 14, 50])
    out = a.out or str(d / 'review.xlsx'); wb.save(out); print('saved', out, '| findings', len(frow), '| spans', len(crow))
if __name__ == '__main__': main()

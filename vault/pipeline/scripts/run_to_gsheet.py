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
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl, sheet_style as SS, config as C
HDR = Font(bold=True, color='FFFFFF'); FILL = PatternFill('solid', fgColor='2F5D3A'); JP = PatternFill('solid', fgColor='FFF2CC'); WRAP = Alignment(wrap_text=True, vertical='top')
def nums(f): return '; '.join(f"{n.get('label', '')}: {n.get('value', '')}{n.get('unit', '')} (p. {n.get('printed_page', '')}, {n.get('table_or_figure', '')} {n.get('row', '')} {n.get('column', '')})".strip() for n in f.get('numbers', []))
def put_image(ws, d, row, col, path, width, thumbs):
    """Place a (downsized) PNG in a cell of the sheet and grow the row to fit it. Google Sheets keeps these as pictures sitting in the cell."""
    if not path or not Path(path).exists(): return 0
    thumbs.mkdir(exist_ok=True); out = thumbs / (Path(path).parent.parent.name[:12] + '_' + Path(path).stem + '.jpg')   # JPEG keeps the workbook under the 10 MB upload limit
    im = PILImage.open(path).convert('RGB'); width = min(int(width * 0.8), int(520 * im.width / im.height))   # 80% of the nominal width: the Drive connector refuses uploads over about 7 MB   # never taller than the tallest row Sheets allows (about 400 pt), or it spills into the next row
    im = im.resize((width, max(1, int(im.height * width / im.width))), PILImage.LANCZOS); im.save(out, quality=62, optimize=True)
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
    def tab(title, header, rows, widths, jp_from=None, img=()):
        ws = wb.create_sheet(title); ws.append(header)
        for r in rows: ws.append(r)
        SS.polish(ws, jp_from=jp_from, image_cols=img); ws.freeze_panes = 'C2'; return ws
    ab = wb.create_sheet('ABOUT'); ab.column_dimensions['A'].width = 26; ab.column_dimensions['B'].width = 120
    pq = C.PIPE.get('project_question', '')
    items = [('Run', f"{M['run_id']}: {M['mode']} mode, spent ${M['spent_usd']:.2f} of a ${M['cap_usd']} cap, status {M['status']}."),
             ('Project question', pq or M.get('question') or 'not given'),
             ('Step 1', 'Gemini 4 Neon extracts the paper\'s questions (Abstract and Introduction) and its findings in three tiers: primary answers a question directly, secondary qualifies a primary finding, tertiary is other context.'),
             ('Step 2', 'PyMuPDF finds every quoted span, boxes it and checks the numbers. Findings that look doubtful are flagged.'),
             ('Step 3', 'GPT-6.2 Sol re-reads flagged findings blind, and Claude Opus 5.5 decides when Sol and Neon disagree.'),
             ('Step 4', 'Decision models and GPT-6.2 Sol look at a crop of every finding: pass, fail or cannot verify (cannot verify goes to you).'),
             ('Step 5', 'Drafting: three models debate each primary EVD; Sonnet 5.5 drafts everything else once. Quality signals: Neon (High) and Opus rate, Sol decides disagreements.'),
             ('Step 6', 'You review this sheet. Your labels become the ground truth for the accuracy numbers.'),
             ('How to review', 'Start with the Findings tab. Sort by Flags and Tier. Yellow columns are yours: say whether the tier, statement and numbers are right, add findings that were missed, and note why.'),
             ('Flags', 'low_confidence: Neon says it is unsure. multi_page: the evidence is on more than one page. span_not_found and span_on_other_page: the quote is not where it should be. number_not_in_pdf_text: fewer than half of its numbers are in the PDF text. number_not_in_numbers_list: a number in the statement has no entry in the Numbers list. numbers_list_entry_without_location: a listed number has no table, figure or page. no_text_layer: scanned PDF.'),
             ('Costs', 'See Metrics and Calls and cost. Batch mode is about half price; the cap is a hard limit per batch.')]
    for k, t in items: ab.append([k, t])
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
    ws = tab('Findings (EVD candidates)', ['Paper', 'Id', 'Tier', 'Why this tier', 'Supports', 'Statement (Neon)', 'Population', 'Intervention', 'Comparator', 'Outcome', 'Study design', 'Timeframe', 'Numbers with locators', 'Confidence', 'Flags', 'Sent to recheck', 'Sol vs Neon', 'Opus verdict', 'Merged screenshot', 'Evidence crop (image)', 'Highlighted page (image)', 'Answers question(s)',
                      'JP: tier right? (yes/no)', 'JP: correct tier', 'JP: statement and numbers right? (yes/no)', 'JP: missed finding (describe)', 'JP: notes'], frow, [30, 6, 10, 30, 10, 60, 22, 22, 22, 22, 18, 14, 50, 10, 24, 9, 10, 10, 22, 60, 50, 14, 12, 12, 14, 30, 30], jp_from=23, img=(20, 21))
    for i, (ck_, f_) in enumerate(fkeys, 2):
        pd = d / ck_; hl = sorted((pd / 'highlights').glob(f"{f_['id']}_s*_p*.png")); mg = (pd / 'highlights' / f_['merged_screenshot']) if f_.get('merged_screenshot') else None
        put_image(ws, d, i, 20, pd / 'crops' / f"{f_['id']}.png", 420, thumbs); put_image(ws, d, i, 21, mg if (mg and mg.exists()) else (hl[0] if hl else None), 340, thumbs)
    dv = DataValidation(type='list', formula1='"yes,no,unsure"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'W2:W{ws.max_row + 1}'); dv.add(f'Y2:Y{ws.max_row + 1}')
    dv2 = DataValidation(type='list', formula1='"primary,secondary,tertiary,not an EVD"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'X2:X{ws.max_row + 1}'); ws.auto_filter.ref = ws.dimensions
    wsc = tab('Quote checks (EVD spans)', ['Paper', 'Finding', 'Span', 'Quoted span (verbatim)', 'Page cited', 'Found in PDF text', 'Pages where found', 'Word boxes', 'Highlighted page (image)', 'JP: quote correct? (yes/no)', 'JP: notes'], crow, [30, 8, 6, 60, 9, 10, 14, 9, 40, 14, 30], jp_from=10, img=(9,))
    for i, (ck_, fid_, k_) in enumerate(ckeys, 2):
        h_ = sorted((d / ck_ / 'highlights').glob(f'{fid_}_s{k_}_p*.png')); put_image(wsc, d, i, 9, h_[0] if h_ else None, 300, thumbs)
    tab('Rechecks (EVD findings)', ['Paper', 'Finding', 'Neon numbers', 'Sol numbers', 'Compare', 'Opus verdict (A = Neon, B = Sol)', 'Opus reason', 'JP: who is right? (Neon, Sol, neither)', 'JP: notes'], rrow, [30, 8, 40, 40, 10, 14, 60, 16, 30], jp_from=8)
    ck_rows = []; ck_crops = []; dr_rows = []; qr_rows = []; qa_rows = []; qr_crops = []
    for ck, p in M['papers'].items():
        if (d / ck / 'checks.json').exists():
            for v in json.load(open(d / ck / 'checks.json')):
                m = v['summary']['means']; ck_crops.append(v.get('crop')); ck_rows.append([ck, v['id'], v.get('tier', ''), v.get('statement', '')[:300], m.get('relevancy', ''), m.get('fidelity', ''), (m.get('numbers_in_source', m.get('quote_grounding', ''))), (m.get('table_cell_matches', m.get('table_figure_grounding', ''))), v['summary']['score'], v['summary']['spread'], '; '.join(v.get('why_vision', [])),
                                                         (v.get('sol') or {}).get('overall', ''), (v.get('sol') or {}).get('reason', ''), (v.get('opus') or {}).get('overall', ''), (v.get('opus') or {}).get('reason', ''), v.get('final', ''), '', '', ''])
        if (d / ck / 'drafts.json').exists():
            dd = json.load(open(d / ck / 'drafts.json'))
            def txt_of(x): return x.get('statement') or x.get('title') or x.get('limitation') or ''
            for nid, f in dd.get('finals', {}).items():
                n = f['node']; alts = [txt_of(dd['authors'].get(a_, {}).get('r0', {}).get(nid, {})) for a_ in ('sonnet', 'sol', 'neon')]
                cc = f.get('detail_check') or f.get('claim_check') or {}; lt = f.get('writing_rules') or f['lint']
                dr_rows.append([ck, nid, n.get('type', ''), n.get('tier', ''), f['author'], f['how'], txt_of(n), lt.get('chars', ''), lt.get('fk_grade', ''), 'yes' if lt.get('pass') else 'no', ', '.join(lt.get('numbers_not_on_card', [])), cc.get('overall', ''), cc.get('fix', ''), cc.get('checker', ''), (f.get('dm') or {}).get('score', ''), f.get('status', ''), alts[0], alts[1], alts[2], '', '', '', ''])
        if (d / ck / 'quality_signals.json').exists():
            q = json.load(open(d / ck / 'quality_signals.json'))
            for x in q['raw']: qr_rows.append([ck, x['signal'], x['rater'], 'yes' if x['counted'] else 'benchmark only', x['rating'], x['quote'][:400], x['locator'], '' if x['quote_found'] is None else (('yes, taken from the PDF' + (' (' + x['quote_source'].split('(')[1] if '(' in x.get('quote_source', '') else '') if str(x.get('quote_source', '')).startswith('anchors') else 'yes') if x['quote_found'] else 'NO: anchors not found' if str(x.get('quote_source', '')).startswith('anchors') else 'NO'), ''])
            qr_crops += [x.get('crop') for x in q['raw']]
            for x in q['aggregate']: qa_rows.append([ck, x['signal'], ', '.join(f'{k}: {v}' for k, v in x['votes'].items()), x['majority'], x['agreement'], x['quotes_not_found'], '', ''])
    if ck_rows:
        ws2 = tab('Decision-model checks (EVD)', ['Paper', 'Finding', 'Tier', 'Statement', 'Relevancy', 'Fidelity', 'Numbers found in source', 'Table cell matches', 'Score (lowest mean)', 'Spread between models', 'Why Sol looked', 'Sol vision', 'Sol reason', 'Opus (disputes only)', 'Opus reason', 'Result', 'Crop Sol looked at (image)', 'JP: is the finding right? (yes/no)', 'JP: notes'], ck_rows, [30, 7, 10, 60, 9, 9, 9, 10, 9, 9, 30, 10, 40, 10, 40, 10, 60, 14, 30], jp_from=18, img=(17,))
        for i, cp in enumerate(ck_crops, 2): put_image(ws2, d, i, 17, cp, 440, thumbs)
    if dr_rows: tab('Drafts (EVD, QUE, CLM, CVT)', ['Paper', 'Node', 'Type', 'Tier', 'Winner by', 'How decided', 'Winning text', 'Chars', 'Reading grade', 'Writing rules pass', 'Numbers not on the card', 'Node-detail check', 'Fix suggested', 'Checked by', 'Decision-model score', 'Status', 'First draft: Sonnet', 'First draft: Sol', 'First draft: Neon', 'JP: best text or your own', 'JP: fidelity (yes/partly/no)', 'JP: style (good/ok/poor)', 'JP: notes'], dr_rows, [30, 8, 6, 10, 9, 18, 70, 7, 8, 7, 14, 10, 30, 9, 10, 18, 50, 50, 50, 40, 14, 14, 30], jp_from=20)
    # ---- EVDs whose decision-model score is below the threshold: what the models saw and what they scored, for JP to suggest changes
    import re as _re
    lowrows = []
    for ck, p in M['papers'].items():
        if not ((d / ck / 'drafts.json').exists() and (d / ck / 'picost.json').exists()): continue
        dd = json.load(open(d / ck / 'drafts.json')); src = {x['id']: x for x in json.load(open(d / ck / 'picost.json')).get('findings', [])}
        for nid, f in dd.get('finals', {}).items():
            dmv = f.get('dm')
            if not dmv or dmv['score'] >= C.PIPE['checks']['dm_low']: continue
            n = f['node']; fnd = src.get(n.get('source_id'), {}); spans = ' | '.join(x.get('text', '') for x in fnd.get('spans', [])); st_ = n.get('statement', '')
            missing = sorted({t for t in _re.findall(r'\d+(?:\.\d+)?', st_) if len(t.replace('.', '')) >= 2 and t not in spans})
            m = dmv['means']; low_q = min(m, key=m.get) if m else ''
            lowrows.append([ck, nid, n.get('tier', ''), st_, m.get('fidelity', ''), (m.get('numbers_in_source', m.get('quote_grounding', ''))), dmv['score'], low_q, (f.get('detail_check') or f.get('claim_check') or {}).get('overall', 'not checked'), ', '.join(missing), len(spans), spans, nums(fnd), '', ''])
    if lowrows: tab('Low decision-model scores (EVD)', ['Paper', 'Node', 'Tier', 'Drafted EVD statement', 'Fidelity', 'Numbers found in source', 'Score (lowest)', 'Lowest question', 'Node-detail check', 'Numbers in the statement that are not in the source span', 'Source span length (characters)', 'Source span(s) the models saw', 'Numbers with locators the models saw', 'JP: suggested change', 'JP: notes'], lowrows, [30, 8, 10, 70, 9, 9, 9, 14, 12, 24, 10, 70, 50, 30, 30], jp_from=14)
    # ---- EVDs reworked by the separate frontier model (evd_rework role) after a low decision-model score
    rwrows = []
    for ck, p in M['papers'].items():
        if not (d / ck / 'drafts.json').exists(): continue
        dd = json.load(open(d / ck / 'drafts.json'))
        for nid, f in dd.get('finals', {}).items():
            rw = f.get('rework')
            if not rw: continue
            nf = [x['number'] for x in rw.get('numbers', []) if x.get('found_in') == 'nowhere']
            rwrows.append([ck, nid, rw['original'], rw['dm_before']['score'], '; '.join(f"{x['number']} ({x['found_in']})" for x in rw.get('numbers', [])), ', '.join(nf), '; '.join(rw.get('fidelity_problems', [])), rw['verdict'], rw.get('proposal', ''), (rw.get('dm_after') or {}).get('score', ''), ('yes' if rw.get('writing_rules_after', {}).get('pass') else 'no') if rw.get('writing_rules_after') else '', 'yes' if rw.get('accepted') else 'no', rw.get('note', ''), f['status'], '', ''])
    if rwrows: tab('EVD rework (Opus 5.5)', ['Paper', 'Node', 'Original EVD statement', 'Decision-model score before', 'Where Opus found each number', 'Numbers found nowhere', 'Fidelity problems', 'Verdict', 'Proposed rewrite', 'Decision-model score after', 'Writing rules pass', 'Rewrite accepted', 'Note for the reviewer', 'Final status', 'JP: right call? (yes/no)', 'JP: notes'], rwrows, [30, 8, 60, 10, 50, 14, 50, 14, 60, 10, 10, 10, 50, 26, 14, 30], jp_from=15)
    # ---- nodes that break the writing rules, with the rule named
    wrrows = []
    for ck, p in M['papers'].items():
        if not (d / ck / 'drafts.json').exists(): continue
        dd = json.load(open(d / ck / 'drafts.json'))
        for nid, f in dd.get('finals', {}).items():
            w = f.get('writing_rules') or f.get('lint') or {}
            if w.get('pass', True): continue
            n = f['node']; why = []
            if w.get('length_ok') is False: why.append(f"longer than 247 characters ({w.get('chars')})")
            if w.get('readability_ok') is False: why.append(f"reading grade {w.get('fk_grade')} (limit 14)")
            if w.get('numbers_not_on_card'): why.append('numbers not on the card: ' + ', '.join(w['numbers_not_on_card']))
            if w.get('parentheses_ok') is False: why.append('more than one set of parentheses (or brackets)')
            if w.get('no_emdash') is False: why.append('contains an em dash')
            if w.get('question_ok') is False: why.append('question does not end with a question mark')
            if w.get('has_quote') is False: why.append('no quote')
            if w.get('links_to_question') is False: why.append('primary EVD links to no question')
            wrrows.append([ck, nid, n.get('type', ''), n.get('tier', ''), n.get('statement') or n.get('title') or n.get('limitation') or '', '; '.join(why), w.get('chars', ''), w.get('fk_grade', ''), ', '.join(w.get('numbers_not_on_card', [])), '', ''])
    if wrrows: tab('Writing-rules fails (all nodes)', ['Paper', 'Node', 'Type', 'Tier', 'Text as drafted', 'Which rule failed', 'Characters', 'Reading grade', 'Numbers not on the card', 'JP: suggested change', 'JP: notes'], wrrows, [30, 8, 6, 10, 80, 40, 10, 10, 20, 30, 30], jp_from=10)
    # ---- verification of every extracted item by Sonnet 5.5 and the two decision models, with majority vote, mean and JP's open columns
    vf = d / 'verification.json'
    if vf.exists():
        V = json.load(open(vf)); hdr = ['Paper', 'Node type', 'Node id', 'What was checked', 'Item (as extracted)', 'Screenshot (image)', 'Sonnet 5.5 score', 'Sonnet 5.5 reason', 'Perplexity Decider 1.3 (probability)', 'Liquid d1-ultra (probability)', 'Majority vote', 'Mean score', 'Models agreeing with the majority',
               'Sonnet pass (1 or 0)', 'Perplexity pass (1 or 0)', 'Liquid pass (1 or 0)', 'Majority pass (1 or 0)', 'Mean pass (1 or 0)', 'JP: is the extraction correct? (yes/no/unsure)', 'JP: notes', 'Truth used for scoring (formula)']
        rows_ = []; crops_ = []
        for x in V:
            sc = x['scores']; so = sc.get('sonnet'); pe = sc.get('perplexity'); li = sc.get('liquid')
            rows_.append([x['paper'], x['ntype'], x['nid'], x['what'], x['text'], '', so if so is not None else '', x['reasons'].get('sonnet', ''), pe if pe is not None else '', li if li is not None else '', x['majority'], x['mean'] if x['mean'] is not None else '', x['agree'],
                          ('' if so is None or so == 0.5 else int(so >= 0.75)), ('' if pe is None else int(pe >= 0.5)), ('' if li is None else int(li >= 0.5)), {'pass': 1, 'fail': 0}.get(x['majority'], ''), ('' if x['mean'] is None else int(x['mean'] >= 0.5)), '', '', ''])
            crops_.append(x.get('crop') if not (x['ntype'] == 'PICOST' and not x['nid'].endswith('Population')) else None)   # the six slot rows of a finding share one screenshot: shown on the first row only
        for i, r_ in enumerate(rows_, 2): r_[20] = f'=IF(S{i}="yes",1,IF(S{i}="no",0,""))'
        wv = tab('Verification (all nodes)', hdr, rows_, [30, 10, 16, 30, 60, 50, 10, 40, 12, 12, 10, 9, 10, 9, 9, 9, 9, 9, 16, 30, 12], jp_from=19, img=(6,))
        for i, cp in enumerate(crops_, 2): put_image(wv, d, i, 6, cp, 360, thumbs)
        n = len(rows_) + 1; sn = "'Verification (all nodes)'!"
        def rng(c): return f"{sn}{c}2:{c}{n}"
        summ = []
        for label, pc, sc_c in (('Sonnet 5.5 (foundation model)', 'N', 'G'), ('Perplexity Decider 1.3 (decision model)', 'O', 'I'), ('Liquid d1-ultra (decision model)', 'P', 'J'), ('Majority vote of the three', 'Q', None), ('Mean score of the three (pass at 0.5 or more)', 'R', 'L')):
            P, T = rng(pc), rng('U')
            summ.append([label, f'=COUNT({P})', f'=IFERROR(AVERAGE({P}),"")', (f'=IFERROR(AVERAGE({rng(sc_c)}),"")' if sc_c else ''), f'=IFERROR(SUMPRODUCT(--({P}={rng("Q")}),--ISNUMBER({P}),--ISNUMBER({rng("Q")}))/SUMPRODUCT(--ISNUMBER({P}),--ISNUMBER({rng("Q")})),"")',
                         f'=COUNT({T})', f'=IFERROR(SUMPRODUCT(--ISNUMBER({T}),--ISNUMBER({P}),--({P}={T}))/SUMPRODUCT(--ISNUMBER({T}),--ISNUMBER({P})),"")', f'=IFERROR(COUNTIFS({P},1,{T},1)/COUNTIFS({P},1,{T},">=0"),"")', f'=IFERROR(COUNTIFS({P},1,{T},1)/COUNTIFS({T},1,{P},">=0"),"")', f'=IFERROR(COUNTIFS({P},0,{T},0)/COUNTIFS({T},0,{P},">=0"),"")'])
        tab('Verification summary', ['Verifier', 'Items scored (not abstained)', 'Share judged correct', 'Mean score', 'Agreement with the majority vote', 'Items with JP ground truth', 'Accuracy vs JP', 'Precision vs JP (of items it passed, how many JP calls correct)', 'Recall vs JP (of items JP calls correct, how many it passed)', 'Specificity vs JP (of items JP calls wrong, how many it failed)'], summ, [44, 14, 12, 10, 16, 14, 12, 22, 22, 22])
        types = sorted({x['ntype'] for x in V}); tt = []
        for t_ in types: tt.append([t_, f'=COUNTIF({rng("B")},"{t_}")', f'=IFERROR(COUNTIFS({rng("B")},"{t_}",{rng("Q")},1)/COUNTIFS({rng("B")},"{t_}",{rng("Q")},">=0"),"")', f'=COUNTIFS({rng("B")},"{t_}",{rng("K")},"split")', f'=COUNTIFS({rng("B")},"{t_}",{rng("U")},">=0")'])
        tab('Verification by node type', ['Node type', 'Items', 'Share the majority judged correct', 'Split votes', 'Items with JP ground truth'], tt, [20, 10, 18, 12, 18])
    if qr_rows:
        wq = tab('Quality signals (raw ratings)', ['Paper', 'Signal', 'Rater', 'Counted in the vote', 'Rating', 'Quote', 'Locator', 'Quote found in PDF', 'Quote highlighted and boxed in the PDF (image)'], qr_rows, [30, 22, 8, 12, 16, 70, 24, 10, 60], img=(9,))
        for i, cp in enumerate(qr_crops, 2): put_image(wq, d, i, 9, cp, 420, thumbs)
    if qa_rows: tab('Quality signals (votes)', ['Paper', 'Signal', 'Votes', 'Majority', 'Agreement', 'Quotes not found', 'JP: correct rating', 'JP: notes'], qa_rows, [30, 22, 40, 16, 10, 10, 16, 30], jp_from=7)
    qg = d / 'question_groups.tsv'
    if qg.exists():   # from consolidate_questions.py: unified, nested questions proposed for JP to verify
        import csv
        rows_ = list(csv.reader(open(qg, encoding='utf-8'), delimiter='\t'))
        if len(rows_) > 1: tab('Question groups (QUE)', rows_[0], rows_[1:], [8, 10, 10, 60, 34, 8, 60, 14, 60, 14, 30], jp_from=10)
    # ---- Metrics: time, cost and accuracy according to the automatic checkers (JP's labels are added later in the yellow columns)
    import datetime as dt, collections
    def iso(x): return dt.datetime.fromisoformat(x.replace('Z', '+00:00')) if x else None
    mrows = []
    def mrow(area, metric, value, note=''): mrows.append([area, metric, value, note])
    sl = M['stage_log']; ts_ = [iso(r.get('started')) for r in sl.values() if isinstance(r, dict) and r.get('started')] + [iso(json.loads(l).get('ts_utc')) for l in (d / 'calls.jsonl').read_text().splitlines()[:1]] if (d / 'calls.jsonl').exists() else []
    calls = [json.loads(l) for l in (d / 'calls.jsonl').read_text().splitlines()] if (d / 'calls.jsonl').exists() else []
    if calls:
        t0 = min(iso(c_['ts_utc']) for c_ in calls); t1 = max(iso(c_['ts_utc']) for c_ in calls); mrow('Time and cost', 'First to last model call (wall clock, includes waiting for batches and any pause)', f'{(t1 - t0).total_seconds() / 60:.0f} minutes')
    mrow('Time and cost', 'Total spent this batch (list prices; batch mode is half)', f"${M['spent_usd']:.2f} of the ${M['cap_usd']} cap" + (f" (earlier batches of this run: {', '.join('$%.2f' % b['spent_usd'] for b in M.get('spent_previous_batches', []))})" if M.get('spent_previous_batches') else ''))
    mrow('Time and cost', 'Papers', len(M['papers']))
    for k, r in sl.items():
        if isinstance(r, dict) and r.get('started') and r.get('ended'): mrow('Time per stage', k, f"{(iso(r['ended']) - iso(r['started'])).total_seconds() / 60:.1f} min, {r.get('mode', '')}, ${r.get('actual_usd', 0):.2f}, {r.get('requests', '')} requests" + (f", {r['failed'] if isinstance(r['failed'], int) else len(r['failed'])} failed" if r.get('failed') else ''))
    allf = []; allq = 0; spans = [0, 0]; flagged = 0; dis = 0; verd = collections.Counter(); finals = collections.Counter(); dmscore = []; nodes = collections.Counter(); how = collections.Counter(); lintp = [0, 0]; ccp = collections.Counter(); st_ = collections.Counter(); qsd = [0, 0, 0, 0, 0]; qnf = [0, 0]; tierc = collections.Counter(); flagc = collections.Counter()
    for ck, p in M['papers'].items():
        if (d / ck / 'picost.json').exists():
            ps = json.load(open(d / ck / 'picost.json')); allq += len(ps.get('questions', []))
            for f in ps.get('findings', []):
                tierc[f.get('tier')] += 1
                for fl in f.get('flags', []): flagc[fl] += 1
                for sp in f.get('spans', []): spans[1] += 1; spans[0] += 1 if sp.get('found') else 0
            allf += ps.get('findings', [])
        flagged += len(p.get('flagged', [])); dis += len(p.get('disagreements', [])); verd.update(a.get('verdict') for a in (p.get('adjudication') or {}).get('adjudications', []))
        if (d / ck / 'checks.json').exists():
            for v in json.load(open(d / ck / 'checks.json')): finals[v.get('final')] += 1; dmscore.append(v['summary']['score'])
        if (d / ck / 'drafts.json').exists():
            dd = json.load(open(d / ck / 'drafts.json'))
            for f in dd.get('finals', {}).values():
                nodes[f['node'].get('type')] += 1; how[f['how']] += 1; lintp[1] += 1; lintp[0] += 1 if (f.get('writing_rules') or f['lint']).get('pass') else 0; st_[f.get('status')] += 1; ccp[(f.get('detail_check') or f.get('claim_check') or {}).get('overall', 'not checked')] += 1
        if (d / ck / 'quality_signals.json').exists():
            q = json.load(open(d / ck / 'quality_signals.json'))
            for x in q['aggregate']: qsd[0] += 1; qsd[1] += 0 if x.get('adjudicated') else 1; qsd[2] += 1 if x.get('adjudicated') else 0; qsd[3] += 1 if x['majority'] == 'no majority' else 0
            for x in q['raw']:
                if x['quote_found'] is not None: qnf[1] += 1; qnf[0] += 0 if x['quote_found'] else 1
    mrow('Extraction', 'Questions found (all papers, repeats kept)', allq, 'from the Abstract and Introduction; no cap')
    mrow('Extraction', 'Findings (primary / secondary / tertiary)', f"{len(allf)} ({tierc['primary']} / {tierc['secondary']} / {tierc['tertiary']})", 'no cap')
    mrow('Extraction accuracy (PyMuPDF)', 'Quoted spans found in the PDF text', f"{spans[0]} of {spans[1]} ({100 * spans[0] / max(spans[1], 1):.0f}%)")
    mrow('Extraction accuracy (PyMuPDF)', 'Findings flagged for a second look', f"{flagged} of {len(allf)} ({100 * flagged / max(len(allf), 1):.0f}%)", ', '.join(f'{k}: {v}' for k, v in flagc.most_common()))
    mrow('Extraction accuracy (Sol, Opus)', 'Sol and Neon read a different number', f"{dis} of {flagged} rechecked")
    mrow('Extraction accuracy (Sol, Opus)', 'Opus verdicts (A = Neon right, B = Sol right)', ', '.join(f'{k}: {v}' for k, v in verd.most_common()) or 'none')
    if finals: mrow('Checks (decision models, Sol vision on every crop)', 'Outcomes', ', '.join(f'{k}: {v}' for k, v in finals.most_common()), 'cannot verify = the crop does not show enough; a person looks'); mrow('Checks (decision models, Sol vision on every crop)', 'Mean decision-model score', f'{sum(dmscore) / len(dmscore):.2f}')
    if nodes:
        mrow('Drafting', 'Nodes written', ', '.join(f'{k}: {v}' for k, v in nodes.most_common())); mrow('Drafting', 'How the winning text was chosen', ', '.join(f'{k}: {v}' for k, v in how.most_common()), 'only primary EVDs are debated; everything else is one draft by Sonnet 5.5')
        mrow('Drafting accuracy (writing-rules and node-detail checks)', 'Writing-rules check pass (length, numbers on the card, plain-language grade, no em dash)', f'{lintp[0]} of {lintp[1]} ({100 * lintp[0] / max(lintp[1], 1):.0f}%)'); mrow('Drafting accuracy (writing-rules and node-detail checks)', 'Node-detail check overall', ', '.join(f'{k}: {v}' for k, v in ccp.most_common())); mrow('Drafting accuracy (writing-rules and node-detail checks)', 'Status', ', '.join(f'{k}: {v}' for k, v in st_.most_common()))
    if qsd[0]: mrow('Quality signals', 'Signals rated', qsd[0]); mrow('Quality signals', 'Neon (High) and Opus agree', f'{qsd[1]} of {qsd[0]} ({100 * qsd[1] / qsd[0]:.0f}%)'); mrow('Quality signals', 'Sol adjudicated', qsd[2]); mrow('Quality signals', 'Still no majority', qsd[3]); mrow('Quality signals', 'Quotes not found in the PDF', f'{qnf[0]} of {qnf[1]}')
    rwn = collections.Counter(); rwacc = 0; before = []; after = []
    for ck in M['papers']:
        if (d / ck / 'drafts.json').exists():
            for f in json.load(open(d / ck / 'drafts.json')).get('finals', {}).values():
                rw = f.get('rework')
                if rw:
                    rwn[rw['verdict']] += 1; rwacc += 1 if rw.get('accepted') else 0; before.append(rw['dm_before']['score'])
                    if rw.get('dm_after'): after.append(rw['dm_after']['score'])
    if rwn:
        mrow('EVD rework (Opus 5.5)', 'EVDs with a decision-model score below 0.60 that were checked', sum(rwn.values())); mrow('EVD rework (Opus 5.5)', 'Verdicts', ', '.join(f'{k}: {v}' for k, v in rwn.most_common()), 'ok = the statement stays; rewrite = a new statement was proposed; extraction_problem = a person checks the extraction')
        mrow('EVD rework (Opus 5.5)', 'Rewrites accepted (writing rules pass and decision-model score at least 0.60)', rwacc); mrow('EVD rework (Opus 5.5)', 'Mean decision-model score, before and after the rewrites', f"{sum(before) / len(before):.2f} before; {sum(after) / len(after):.2f} after" if after else f"{sum(before) / len(before):.2f} before")
    mrow('About these numbers', 'Accuracy here means agreement between automatic checkers', '', 'It is not accuracy against a person. Fill in the yellow JP columns on the other tabs and these metrics can be recomputed against your labels.')
    tab('Metrics', ['Area', 'Metric', 'Value', 'Note'], mrows, [38, 70, 40, 70])
    crows = []
    f = d / 'calls.jsonl'
    for l in (f.read_text().splitlines() if f.exists() else []):
        r = json.loads(l); crows.append([r.get('ts_utc', '')[:19], r.get('citekey', ''), r.get('step', ''), r.get('model', ''), r.get('effort', ''), r.get('tokens_in'), r.get('tokens_out'), r.get('cost_usd_est'), (r.get('notes') or '')[:80]])
    tab('Calls and cost', ['Time (UTC)', 'Paper', 'Step', 'Model', 'Effort', 'Tokens in', 'Tokens out (incl. thinking)', 'Cost USD (list price; batch is half)', 'Notes'], crows, [20, 30, 12, 20, 8, 10, 14, 14, 50])
    SS.polish_about(ab)
    out = a.out or str(d / 'review.xlsx'); wb.save(out); print('saved', out, '| findings', len(frow), '| spans', len(crow))
if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Build the step-by-step review workbook for one runner batch (JP, 2026-11-25): a human follows each paper from extraction to checks and adds ground-truth labels.
  python3 run_to_gsheet.py RUN_ID [--out FILE]          writes pipeline/runs/<run>/review.xlsx (local; upload it to Google Sheets with the Drive connector)
Tabs: ABOUT (how to read it), Papers, Findings (one row per extracted finding, with every check and JP's label columns), Checks (one row per quoted span), Rechecks
(Neon vs Sol vs Opus for the flagged findings), Checks (decision models, Sol vision, Opus), Drafts and debate, Quality signals (raw and vote), Calls and cost; see Review-sheets-spec.md."""
import argparse, json, re, sys
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as XlImage
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.comments import Comment
import column_notes as CN
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


_CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def about_models_and_tools(M):
    """Rows for the ABOUT tab: every model by job, with developer, country, how it runs and price, the decision and embedding models, and every Python package and tool (JP, 2026-11-26: name them, do not be vague)."""
    import importlib.metadata as md, platform, re as _re
    import decision_models as _dm
    MO = C.MODELS; R_ = C.ROLES
    def desc(mid):
        m = MO.get(mid, {}); price = f"${m.get('price_in')} in / ${m.get('price_out')} out per million tokens" if m.get('price_in') is not None else 'price not listed'
        return f"{m.get('display', mid)} (id {mid}; {m.get('developer', '?')}, {m.get('country', '?')}; {'hosted API' if m.get('runs') == 'api' else 'runs locally'}; {price})"
    def role(x): return desc(x['model']) + (f", effort {x['effort']}" if x.get('effort') else '') if isinstance(x, dict) else desc(x)
    rows = [('MODELS AND TOOLS', 'Every model and package this pipeline uses. Prices are list prices recorded in pipeline/config/models.json with their source and date.'),
            ('Extraction (picost stage)', role(R_['extract'])), ('Second reading of flagged findings (recheck)', role(R_['recheck'])), ('Adjudication when readers disagree', role(R_['adjudicate'])),
            ('Screenshot check of every finding (checks stage)', role(R_['vision_check'])), ('Dispute between decision models and screenshot check', role(R_['vision_dispute'])), ('Tie-break between drafts', role(R_['tiebreak'])),
            ('Quote check: screenshot of every quote against its text', role(R_['quote_check'])), ('EVD rework when a decision-model score is below 0.60', role(R_['evd_rework'])),
            ('EVD, QUE, CLM, CVT drafting authors', '; '.join(role(a) for a in R_['authors'])), ('Drafting voters', '; '.join(role(a) for a in R_['voters'])),
            ('Quality-signal raters', '; '.join(role(a) for a in R_['raters'])), ('Quality-signal adjudicator', role(R_['qs_adjudicator'])),
            ('Verification: foundation model', role(R_['quote_check']) + ' (reads screenshots; judges every PICOST slot, quote, QUE, CLM, CVT and quality rating)'),
            ('Decision model 1', desc(_dm.MODELS['perplexity']) + '. Text only. Scores every verification item and every EVD check.'),
            ('Decision model 2', desc(_dm.MODELS['liquid']) + '. Reads text and images (up to 8 per request). Scores every verification item and EVD check; looks for the digits of each quote and for missing statement numbers on screenshots. Replaced d1-ultra on 2026-11-26.'),
            ('Embedding models (local)', '; '.join(e['name'] for e in C.EMBEDDING) + '. EmbeddingGemma 2 clusters research questions for the Question groups tab; the others are used in screening.'),
            ('Question grouping and nesting', desc('claude-sonnet-5-5'))]
    pk = []
    for fn in ('requirements.txt', 'requirements-screening.txt'):
        f = C.VAULT / 'pipeline' / fn
        if f.exists():
            for line in f.read_text(encoding='utf-8').splitlines():
                mm = _re.match(r'^([A-Za-z0-9_.\-]+)\s*(?:==|>=)\s*([\w.]+)', line.strip())
                if mm:
                    try: inst = md.version(mm.group(1))
                    except Exception: inst = 'not installed here'
                    pk.append(f"{mm.group(1)} {mm.group(2)} (installed: {inst})")
    rows.append(('Python packages', f"Python {platform.python_version()}; " + '; '.join(dict.fromkeys(pk))))
    rows.append(('Table parsers (exploratory, tables only)', 'Marker (marker-pdf) and MinerU are being tested for reading table cells only, on the 27 seed papers, against PyMuPDF find_tables (results: pipeline/misc/evd-validation/table-parsers/RESULTS.md). They are installed in a separate virtual environment, run without any LLM mode, and are not part of the pipeline. PyMuPDF stays the tool for quote text, word boxes and page crops.'))
    rows.append(('LIVES style menu (Apps Script)', 'A menu called "LIVES style" is added to a sheet only after the script is pasted into that sheet (Extensions > Apps Script > paste pipeline/apps-script/LivesStyle.gs > Save > reload the sheet > allow once). A script belongs to one spreadsheet, so every newly uploaded review sheet needs it pasted again.'))
    rows.append(('Other tools', 'PyMuPDF (reads PDF text, locates quotes, draws highlights, crops screenshots); Pillow (images); openpyxl (builds this workbook); requests (decision-model APIs); Google Drive and Google Sheets connectors (upload); Apps Script macros (pipeline/apps-script/LivesStyle.gs); git and the GitHub CLI (cdromcom/living-evidence-synthesis); Obsidian with the discourse-graph plugin (the vault); the LIVES web app on Vercel.'))
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--out'); ap.add_argument('--tripod-only', action='store_true', help='write a workbook with the TRIPOD-LLM tabs only (a new file, so labels in an existing sheet are not touched)'); a = ap.parse_args(); d = cl.RUNS / a.run; M = json.load(open(d / 'manifest.json')); wb = Workbook(); wb.remove(wb.active); thumbs = d / '_thumbs'
    def lowq(d):
        a = [x for k, x in (d or {}).items() if not str(k).startswith('_') and isinstance(x, (int, float))]
        return round(min(a), 3) if a else ''
    def tab(title, header, rows, widths, jp_from=None, img=()):
        ws = wb.create_sheet(title); ws.append(header)
        for ci_, h_ in enumerate(header, 1):   # hover note on every column header, written for readers outside the project (column_notes.py)
            n_ = CN.note_for(title, h_)
            if n_: c_ = Comment(n_, 'LIVES pipeline'); c_.width = 340; c_.height = 40 + 18 * (len(n_) // 48 + 1); ws.cell(1, ci_).comment = c_
        for r in rows: ws.append([_CTRL.sub('', x) if isinstance(x, str) else x for x in r])   # control characters in a quote would make openpyxl refuse the cell
        SS.polish(ws, jp_from=jp_from, image_cols=img); ws.freeze_panes = 'C2'; return ws
    ab = wb.create_sheet('ABOUT'); ab.column_dimensions['A'].width = 26; ab.column_dimensions['B'].width = 120
    pq = C.PIPE.get('project_question', '')
    items = [('Run', f"{M['run_id']}: {M['mode']} mode, spent ${M['spent_usd']:.2f} of a ${M['cap_usd']} cap, status {M['status']}."),
             ('Project question', pq or M.get('question') or 'not given'),
             ('Step 1', 'Gemini 4 Neon extracts the paper\'s questions (Abstract and Introduction) and its findings in three tiers: primary answers a question directly, secondary qualifies a primary finding, tertiary is other context.'),
             ('Step 2', 'PyMuPDF finds every quoted span, boxes it and checks the numbers. Findings that look doubtful are flagged.'),
             ('Step 3', 'GPT-6.2 Sol re-reads flagged findings blind, and Claude Opus 5.5 decides when Sol and Neon disagree.'),
             ('Step 4', 'Claude Sonnet 5.5 reads a screenshot of every quote and compares it with the quote text (quote_check stage). Two decision models, Perplexity Decider 1.3 (pplx-decider-v1.3, text only) and Liquid d1.2-ultra (d1.2-ultra, reads text and images), score every finding on relevancy, fidelity, numbers found in the source and table cell matches. GPT-6.2 Sol looks at a crop of every finding: pass, not matched or cannot verify (cannot verify goes to you).'),
             ('Step 5', 'Drafting: three models debate each primary EVD; Sonnet 5.5 drafts everything else once. Quality signals: Neon, Opus and Sol rate every row at high effort and two of three decide.'),
             ('Step 6', 'Verification: Liquid d1.2-ultra and Perplexity Decider 1.3 first judge every PICOST slot (with page 1 and the Methods pages), question rewording (QUE), claim (CLM), caveat (CVT) and quality rating; Claude Sonnet 5.5 judges an item only when those two disagree, and always reads the screenshot of every quote; Liquid d1.2-ultra also looks for the digits of each quote and for statement numbers missing from the PDF text on the screenshots. Quotes without digits are checked by Sonnet 5.5. The tabs Verification, Numbers check and Failure analysis show the results.'),
             ('Step 7', 'You review this sheet. Your labels become the ground truth for the accuracy numbers.'),
             ('How to review', 'Start with the Findings tab. Sort by Flags and Tier. Yellow columns are yours: say whether the tier, statement and numbers are right, add findings that were missed, and note why.'),
             ('Flags', 'low_confidence: Neon says it is unsure. multi_page: the evidence is on more than one page. span_not_found and span_on_other_page: the quote is not where it should be. number_not_in_pdf_text: fewer than half of its numbers are in the PDF text. number_not_in_numbers_list: a number in the statement has no entry in the Numbers list. numbers_list_entry_without_location: a listed number has no table, figure or page. no_text_layer: scanned PDF.'),
             ('Costs', 'See Metrics and Calls and cost. Batch mode is about half price; the cap is a hard limit per batch.')]
    for k, t in items: ab.append([k, t])
    for k, t in about_models_and_tools(M): ab.append([k, t])
    prow = []; frow = []; crow = []; rrow = []; fkeys = []; ckeys = []
    drafts_cache = {}
    def evd_new(ck, fid):
        cand(ck, fid); fin = ((drafts_cache.get(ck) or {}).get('finals') or {}).get('E-' + fid)
        return fin['node'].get('statement', '') if fin else ''
    def cand(ck, fid):
        """Candidate EVD wording from each model that drafted it, plus the chosen EVD (JP wants to compare who writes EVDs at the right level)."""
        if ck not in drafts_cache:
            df = d / ck / 'drafts.json'; drafts_cache[ck] = json.load(open(df)) if df.exists() else {}
        dd = drafts_cache[ck]; nid = 'E-' + fid; fin = (dd.get('finals') or {}).get(nid)
        def st(a_): x = ((dd.get('authors') or {}).get(a_, {}).get('r0', {}) or {}).get(nid, {}); return x.get('statement') or ''
        return [st('sonnet'), st('sol'), st('neon'), (fin['node'].get('statement', '') + f"  [{fin.get('author', '')}; {fin.get('how', '')}]") if fin else '', fin.get('status', '') if fin else '']
    for ck, p in M['papers'].items():
        pj = d / ck / 'picost.json'
        if not pj.exists(): prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], p.get('failed') or 'no extraction', '', '', '', '', '', '']); continue
        ps = json.load(open(pj)); fs = ps.get('findings', []); tiers = {t: sum(1 for f in fs if f.get('tier') == t) for t in ('primary', 'secondary', 'tertiary')}
        adj = {x['id']: x for x in (p.get('adjudication') or {}).get('adjudications', [])}; rc = {f['id']: f for f in (p.get('recheck') or {}).get('findings', [])}
        prow.append([ck, Path(p['pdf']).name, p['preflight']['pages'], 'ok', tiers['primary'], tiers['secondary'], tiers['tertiary'], len(p.get('flagged', [])), len(p.get('disagreements', [])), round(sum(v.get('cost_usd', 0) for v in p['stages'].values() if isinstance(v, dict)), 3)])
        for f in fs:
            fkeys.append((ck, f)); v = adj.get(f['id']); frow.append([ck, f['id'], f.get('tier', ''), f.get('tier_reason', ''), '; '.join(f.get('supports', [])), f.get('statement', ''), evd_new(ck, f['id']), f.get('P', ''), f.get('I', ''), f.get('C', ''), f.get('O', ''), f.get('S', ''), f.get('T', ''), nums(f),
                                               f.get('confidence', ''), ', '.join(f.get('flags', [])), 'yes' if f['id'] in p.get('flagged', []) else 'no', ('different' if f['id'] in p.get('disagreements', []) else 'agrees') if f['id'] in rc else '', v['verdict'] if v else '', '', '; '.join(f.get('answers_QUE', [])), *cand(ck, f['id']), '', '', '', '', ''])
            for k, sp in enumerate(f.get('spans', []), 1): ckeys.append((ck, f['id'], k)); crow.append([ck, f['id'], k, sp.get('text', '')[:300], sp.get('pdf_page', ''), 'yes' if sp.get('found') else 'NO', ', '.join(map(str, sp.get('pages_found', []))), len(sp.get('bbox', [])), '', ''])
            if f['id'] in rc: rrow.append([ck, f['id'], '; '.join(str(n.get('value')) for n in f.get('numbers', [])), '; '.join(str(n.get('value')) for n in rc[f['id']].get('numbers', [])), ('different' if f['id'] in p.get('disagreements', []) else 'agrees'), (adj.get(f['id']) or {}).get('verdict', ''), (adj.get(f['id']) or {}).get('reason', ''), '', ''])
    frow = [r[:20] + ['', ''] + r[20:] for r in frow]; crow = [r[:8] + [''] + r[8:] for r in crow]
    tab('Papers', ['Paper', 'File', 'Pages', 'Status', 'Primary findings', 'Secondary findings', 'Tertiary findings', 'Flagged', 'Disagreements', 'Cost USD'], prow, [40, 50, 7, 12, 10, 10, 10, 9, 12, 10])
    evd_hdr = 'EVD draft (chosen; new rules: 1-2 parentheses, no brackets, no all caps, F1 only)' if 'draft-nodes-v4' in str(M.get('evd_rules_prompt', '')) else 'EVD draft (chosen; drafted under the older rules, not redrafted)'
    ws = tab('Findings (EVD candidates)', ['Paper', 'Id', 'Tier', 'Why this tier', 'Supports', 'Statement (Neon)', evd_hdr, 'Population', 'Intervention', 'Comparator', 'Outcome', 'Study design', 'Timeframe', 'Numbers with locators', 'Confidence', 'Flags', 'Sent to recheck', 'Sol vs Neon', 'Opus verdict', 'Merged screenshot (image; shown when the evidence crosses a page break)', 'Evidence crop (image)', 'Highlighted page (image)', 'Answers question(s)', 'Candidate EVD: Sonnet 5.5', 'Candidate EVD: Sol 6.2', 'Candidate EVD: Neon (Gemini 4)', 'Chosen EVD [author; how chosen]', 'Chosen EVD status',
                      'JP: tier right? (yes/no)', 'JP: correct tier', 'JP: statement and numbers right? (yes/no)', 'JP: missed finding (describe)', 'JP: notes'], frow, [30, 6, 10, 30, 10, 60, 60, 22, 22, 22, 22, 18, 14, 50, 10, 24, 9, 10, 10, 50, 60, 50, 14, 40, 40, 40, 50, 14, 12, 12, 14, 30, 30], jp_from=29, img=(20, 21, 22))
    for i, (ck_, f_) in enumerate(fkeys, 2):
        pd = d / ck_; hl = sorted((pd / 'highlights').glob(f"{f_['id']}_s*_p*.png")); mg = (pd / 'highlights' / f_['merged_screenshot']) if f_.get('merged_screenshot') else None
        put_image(ws, d, i, 21, pd / 'crops' / f"{f_['id']}.png", 420, thumbs); put_image(ws, d, i, 20, mg if (mg and mg.exists()) else None, 340, thumbs); put_image(ws, d, i, 22, hl[0] if hl else None, 340, thumbs)
    dv = DataValidation(type='list', formula1='"yes,no,unsure"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'AC2:AC{ws.max_row + 1}'); dv.add(f'AE2:AE{ws.max_row + 1}')
    dv2 = DataValidation(type='list', formula1='"primary,secondary,tertiary,not an EVD"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'AD2:AD{ws.max_row + 1}'); ws.auto_filter.ref = ws.dimensions
    wsc = tab('Quote checks (EVD spans)', ['Paper', 'Finding', 'Span', 'Quoted span (verbatim)', 'Page cited', 'Found in PDF text', 'Pages where found', 'Word boxes', 'Highlighted page (image)', 'JP: quote correct? (yes/no)', 'JP: notes'], crow, [30, 8, 6, 60, 9, 10, 14, 9, 40, 14, 30], jp_from=10, img=(9,))
    for i, (ck_, fid_, k_) in enumerate(ckeys, 2):
        h_ = sorted((d / ck_ / 'highlights').glob(f'{fid_}_s{k_}_p*.png')); put_image(wsc, d, i, 9, h_[0] if h_ else None, 300, thumbs)
    tab('Rechecks (EVD findings)', ['Paper', 'Finding', 'Neon numbers', 'Sol numbers', 'Compare', 'Opus verdict (A = Neon, B = Sol)', 'Opus reason', 'JP: who is right? (Neon, Sol, neither)', 'JP: notes'], rrow, [30, 8, 40, 40, 10, 14, 60, 16, 30], jp_from=8)
    ck_rows = []; ck_crops = []; dr_rows = []; qr_rows = []; qa_rows = []; qr_crops = []
    for ck, p in M['papers'].items():
        if (d / ck / 'checks.json').exists():
            for v in json.load(open(d / ck / 'checks.json')):
                m = v['summary']['means']; ck_crops.append(v.get('crop')); ck_rows.append([ck, v['id'], v.get('tier', ''), v.get('statement', '')[:300], m.get('relevancy', ''), m.get('fidelity', ''), (m.get('numbers_in_source', m.get('quote_grounding', ''))), (m.get('table_cell_matches', m.get('table_figure_grounding', ''))), v['summary']['score'], v['summary']['spread'], '; '.join(v.get('why_vision', [])),
                                                         (v.get('sol') or {}).get('overall', ''), (v.get('sol') or {}).get('reason', ''), (v.get('opus') or {}).get('overall', ''), (v.get('opus') or {}).get('reason', ''), v.get('final', ''), '', '', '', lowq(v.get('dm_liquid_d1_ultra')), lowq(v.get('dm_liquid_d12')), lowq((v.get('dm') or {}).get('perplexity'))])
        if (d / ck / 'drafts.json').exists():
            dd = json.load(open(d / ck / 'drafts.json'))
            def txt_of(x): return x.get('statement') or x.get('title') or x.get('limitation') or ''
            for nid, f in dd.get('finals', {}).items():
                n = f['node']; alts = [txt_of(dd['authors'].get(a_, {}).get('r0', {}).get(nid, {})) for a_ in ('sonnet', 'sol', 'neon')]
                cc = f.get('detail_check') or f.get('claim_check') or {}; lt = f.get('writing_rules') or f['lint']
                dr_rows.append([ck, nid, n.get('type', ''), n.get('tier', ''), f['author'], f['how'], txt_of(n), lt.get('chars', ''), 'yes' if lt.get('pass') else 'no', ', '.join(lt.get('numbers_not_on_card', [])), cc.get('overall', ''), cc.get('fix', ''), cc.get('checker', ''), (f.get('dm') or {}).get('score', ''), f.get('status', ''), alts[0], alts[1], alts[2], '', '', '', ''])
        if (d / ck / 'quality_signals.json').exists():
            q = json.load(open(d / ck / 'quality_signals.json'))
            for x in q['raw']: qr_rows.append([ck, x['signal'], x['rater'], 'yes' if x['counted'] else 'benchmark only', x['rating'], x['quote'][:400], x['locator'], '' if x['quote_found'] is None else (('yes, taken from the PDF' + (' (' + x['quote_source'].split('(')[1] if '(' in x.get('quote_source', '') else '') if str(x.get('quote_source', '')).startswith('anchors') else 'yes') if x['quote_found'] else 'NO: anchors not found' if str(x.get('quote_source', '')).startswith('anchors') else 'NO'), ''])
            qr_crops += [x.get('crop') for x in q['raw']]
            for x in q['aggregate']: qa_rows.append([ck, x['signal'], ', '.join(f'{k}: {v}' for k, v in x['votes'].items()), x['majority'], x['agreement'], x['quotes_not_found'], '', ''])
    if ck_rows:
        ws2 = tab('Decision-model checks (EVD)', ['Paper', 'Finding', 'Tier', 'Statement', 'Relevancy', 'Fidelity', 'Numbers found in source', 'Table cell matches', 'Score (lowest mean)', 'Spread between models', 'Why Sol looked', 'Sol vision', 'Sol reason', 'Opus (disputes only)', 'Opus reason', 'Result', 'Crop Sol looked at (image)', 'JP: is the finding right? (yes/no)', 'JP: notes', 'Liquid d1-ultra OLD: lowest question score', 'Liquid d1.2-ultra: lowest question score', 'Perplexity Decider 1.3: lowest question score'], ck_rows, [30, 7, 10, 60, 9, 9, 9, 10, 9, 9, 30, 10, 40, 10, 40, 10, 60, 14, 30, 14, 14, 14], jp_from=18, img=(17,))
        for i, cp in enumerate(ck_crops, 2): put_image(ws2, d, i, 17, cp, 440, thumbs)
    if dr_rows: tab('Drafts (EVD, QUE, CLM, CVT)', ['Paper', 'Node', 'Type', 'Tier', 'Winner by', 'How decided', 'Winning text', 'Chars', 'Writing rules pass', 'Numbers not on the card', 'Node-detail check', 'Fix suggested', 'Checked by', 'Decision-model score', 'Status', 'First draft: Sonnet', 'First draft: Sol', 'First draft: Neon', 'JP: best text or your own', 'JP: fidelity (yes/partly/no)', 'JP: style (good/ok/poor)', 'JP: notes'], dr_rows, [30, 8, 6, 10, 9, 18, 70, 7, 7, 14, 10, 30, 9, 10, 18, 50, 50, 50, 40, 14, 14, 30], jp_from=19)
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
            if w.get('numbers_not_on_card'): why.append('numbers not on the card: ' + ', '.join(w['numbers_not_on_card']))
            if w.get('parentheses_ok') is False: why.append('more than one set of parentheses (or brackets)')
            if w.get('no_emdash') is False: why.append('contains an em dash')
            if w.get('question_ok') is False: why.append('question does not end with a question mark')
            if w.get('has_quote') is False: why.append('no quote')
            if w.get('links_to_question') is False: why.append('primary EVD links to no question')
            wrrows.append([ck, nid, n.get('type', ''), n.get('tier', ''), n.get('statement') or n.get('title') or n.get('limitation') or '', '; '.join(why), w.get('chars', ''), ', '.join(w.get('numbers_not_on_card', [])), '', ''])
    if wrrows: tab('Writing-rules fails (all nodes)', ['Paper', 'Node', 'Type', 'Tier', 'Text as drafted', 'Which rule failed', 'Characters', 'Numbers not on the card', 'JP: suggested change', 'JP: notes'], wrrows, [30, 8, 6, 10, 80, 40, 10, 20, 30, 30], jp_from=9)
    # ---- verification of every extracted item by Sonnet 5.5 and the two decision models, with majority vote, mean and JP's open columns
    vf = d / 'verification.json'
    if vf.exists():
        import lives_verify as VV
        V = VV.queue_order(json.load(open(vf))); hdr = ['Paper', 'Node type', 'Node id', 'What was checked', 'Item (as extracted)', 'Screenshot (image)', 'Sonnet 5.5 score', 'Sonnet 5.5 reason', 'Perplexity Decider 1.3 (probability)', 'Liquid d1.2-ultra, text (probability)', 'Majority vote', 'Mean score', 'Models agreeing with the majority',
               'Sonnet pass (1 or 0)', 'Perplexity pass (1 or 0)', 'Liquid d1.2-ultra text pass (1 or 0)', 'Majority pass (1 or 0)', 'Mean pass (1 or 0)', 'JP: is the extraction correct? (yes/no/unsure)', 'JP: notes', 'Truth used for scoring (formula)',
               'Liquid d1.2-ultra reading the screenshot (probability)', 'Liquid screenshot score counts as a vote? (digit comparisons on quotes only)', 'Liquid d1-ultra OLD, text (probability)', 'Liquid d1-ultra OLD pass (1 or 0)', 'Liquid d1.2-ultra screenshot pass (1 or 0)', 'Passage or quote it was checked against', 'Labeling queue (tonight)', 'Share of item words not found in the passage (CLM, CVT, QUE; 0 = every word is in the passage)', 'Before the rerun (cited pages only, or the stricter question): Sonnet 5.5 score', 'Before the rerun: Perplexity (probability)', 'Before the rerun: Liquid d1.2-ultra text (probability)']
        rows_ = []; crops_ = []
        for x in V:
            sc = x['scores']; so = sc.get('sonnet'); pe = sc.get('perplexity'); li = sc.get('liquid'); old = x.get('liquid_d1_ultra'); im = sc.get('liquid_image'); imu = x.get('liquid_image_untested'); imv = im if im is not None else imu
            rows_.append([x['paper'], x['ntype'] + (' quote' if x['nid'].endswith(' quote') else ''), x['nid'], x['what'], x['text'], '', so if so is not None else '', x['reasons'].get('sonnet', ''), pe if pe is not None else '', li if li is not None else '', x['majority'], x['mean'] if x['mean'] is not None else '', x['agree'],
                          ('' if so is None or so == 0.5 else int(so >= 0.75)), ('' if pe is None else int(pe >= 0.5)), ('' if li is None else int(li >= 0.5)), {'pass': 1, 'fail': 0}.get(x['majority'], ''), ('' if x['mean'] is None else int(x['mean'] >= 0.5)), '', '', '',
                          imv if imv is not None else '', ('yes' if im is not None else ('no: quotes without digits are read by Sonnet 5.5' if imu is not None and (x['ntype'] == 'QUOTE' or x['nid'].endswith(' quote')) else ('no, untested' if imu is not None else ''))), old if old is not None else '', ('' if old is None else int(old >= 0.5)), ('' if imv is None else int(imv >= 0.5)), x.get('passage', ''), x.get('queue', ''), x.get('novel_share', ''), *[(x.get('scores_before_rerun') or {}).get(k, '') if (x.get('scores_before_rerun') or {}).get(k) is not None else '' for k in ('sonnet', 'perplexity', 'liquid')]])
            crops_.append(x.get('crop') if not (x['ntype'] == 'PICOST' and not x['nid'].endswith('Population')) else None)   # the six slot rows of a finding share one screenshot: shown on the first row only
        for i, r_ in enumerate(rows_, 2): r_[20] = f'=IF(S{i}="yes",1,IF(S{i}="no",0,""))'
        wv = tab('Verification (all nodes)', hdr, rows_, [30, 10, 16, 30, 60, 50, 10, 40, 12, 12, 10, 9, 10, 9, 9, 9, 9, 9, 16, 30, 12, 16, 16, 14, 12, 12, 60, 22, 18, 14, 14, 14], jp_from=19, img=(6,))
        for i, cp in enumerate(crops_, 2): put_image(wv, d, i, 6, cp, 360, thumbs)
        n = len(rows_) + 1; sn = "'Verification (all nodes)'!"
        def rng(c): return f"{sn}{c}2:{c}{n}"
        summ = []
        for label, pc, sc_c in (('Sonnet 5.5 (foundation model)', 'N', 'G'), ('Perplexity Decider 1.3 (decision model)', 'O', 'I'), ('Liquid d1.2-ultra, text (decision model)', 'P', 'J'), ('Liquid d1-ultra OLD, text (decision model, replaced)', 'Y', 'X'), ('Liquid d1.2-ultra, reading screenshots (digit and other screenshot checks)', 'Z', 'V'), ('Majority vote of the voting models', 'Q', None), ('Mean score of the voting models (pass at 0.5 or more)', 'R', 'L')):
            P, T = rng(pc), rng('U')
            summ.append([label, f'=COUNT({P})', f'=IFERROR(AVERAGE({P}),"")', (f'=IFERROR(AVERAGE({rng(sc_c)}),"")' if sc_c else ''), f'=IFERROR(SUMPRODUCT(--({P}={rng("Q")}),--ISNUMBER({P}),--ISNUMBER({rng("Q")}))/SUMPRODUCT(--ISNUMBER({P}),--ISNUMBER({rng("Q")})),"")',
                         f'=COUNT({T})', f'=IFERROR(SUMPRODUCT(--ISNUMBER({T}),--ISNUMBER({P}),--({P}={T}))/SUMPRODUCT(--ISNUMBER({T}),--ISNUMBER({P})),"")', f'=IFERROR(COUNTIFS({P},1,{T},1)/COUNTIFS({P},1,{T},">=0"),"")', f'=IFERROR(COUNTIFS({P},1,{T},1)/COUNTIFS({T},1,{P},">=0"),"")', f'=IFERROR(COUNTIFS({P},0,{T},0)/COUNTIFS({T},0,{P},">=0"),"")'])
        tab('Verification summary', ['Verifier', 'Items scored (not abstained)', 'Share judged correct', 'Mean score', 'Agreement with the majority vote', 'Items with JP ground truth', 'Accuracy vs JP', 'Precision vs JP (of items it passed, how many JP calls correct)', 'Recall vs JP (of items JP calls correct, how many it passed)', 'Specificity vs JP (of items JP calls wrong, how many it failed)'], summ, [52, 14, 12, 10, 16, 14, 12, 22, 22, 22])
        types = sorted({x['ntype'] + (' quote' if x['nid'].endswith(' quote') else '') for x in V}); tt = []
        for t_ in types: tt.append([t_, f'=COUNTIF({rng("B")},"{t_}")', f'=IFERROR(COUNTIFS({rng("B")},"{t_}",{rng("Q")},1)/COUNTIFS({rng("B")},"{t_}",{rng("Q")},">=0"),"")', f'=COUNTIFS({rng("B")},"{t_}",{rng("K")},"split")', f'=COUNTIFS({rng("B")},"{t_}",{rng("U")},">=0")'])
        tab('Verification by node type', ['Node type', 'Items', 'Share the majority judged correct', 'Split votes', 'Items with JP ground truth'], tt, [20, 10, 18, 12, 18])
    # ---- quality signals: one tab per paper (code-only checks and model ratings side by side) and a run summary with cost, time and agreement
    import qs_export as QE, signal_registry as SRG
    if QE.STORE.exists():
        store = json.load(open(QE.STORE)); qs_sum = []; calls = []; tri_sum = []
        cf_ = d / 'calls.jsonl'
        if cf_.exists():
            for l_ in open(cf_):
                try: calls.append(json.loads(l_))
                except Exception: pass
        for ck, p in M['papers'].items():
            pj_ = d / ck / 'picost.json'
            if p.get('failed') or not pj_.exists() or not (d / ck / 'quality_signals.json').exists(): continue
            meta = json.load(open(pj_)).get('paper', {}); key = SRG.resolve_citekey(ck, meta.get('title', ''), meta.get('year', '')) or ck; E_ = store['papers'].get(key)
            if not E_: continue
            hdr = ['Kind', 'Signal or check', 'Result', 'Agreement or status', 'Summary', 'Neon rating', 'Neon quote and locator', 'Neon screenshot (image)', 'Opus rating', 'Opus quote and locator', 'Opus screenshot (image)', 'Sol rating (third rater)', 'Quote verifiers (mean score: Sonnet 5.5, Liquid d1.2-ultra, Perplexity)', 'Live-site tag (Aug 2026)', 'Matches live-site tag?', 'Code-only checks that apply', 'Source and date', 'JP: right? (yes/no/unsure)', 'JP: notes']
            rows_ = []; shots_ = []; rows_t = []; shots_t = []
            def rater(sig, nm):
                return next((r for r in sig.get('ratings', []) if r['rater'] == nm), None)
            for it in E_.get('provenance', []):
                if it['id'].startswith('link-') and it['status'] != 'flag': continue   # the 'links' row sums up the others; only links with a problem get their own row
                rows_.append(['Code-only check', it['label'], it['result'], it['status'], it.get('detail', ''), '', '', '', '', '', '', '', '', '', '', it['tool'], (it.get('url', '') + ' ' + str(it.get('checked_utc', ''))[:10]).strip(), '', '']); shots_.append((None, None))
            for sid, sig in E_.get('signals', {}).items():
                n_ = rater(sig, 'Gemini 4 Neon'); o_ = rater(sig, 'Claude Opus 5.5'); s_ = rater(sig, 'GPT-6.2 Sol'); ck_ = {c['verifier']: c['score'] for c in sig.get('checks', [])}
                ver_ = ', '.join(str(ck_.get(v, '')) for v in ('Claude Sonnet 5.5', 'Liquid d1.2-ultra', 'Perplexity Decider 1.3')) if ck_ else ''
                tools_ = ', '.join(next((i['label'] for i in E_.get('provenance', []) if i['id'] == t_), t_) for t_ in sig.get('tool_checks', []))
                (rows_t if sid.startswith('tripod-') else rows_).append(['Signal', sig['label'], sig['final'], sig['agreement'], sig['summary'], n_['rating'] if n_ else '', (n_['quote'] + ('  [' + n_['locator'] + ']' if n_['locator'] else '')) if n_ else '', '', o_['rating'] if o_ else '', (o_['quote'] + ('  [' + o_['locator'] + ']' if o_['locator'] else '')) if o_ else '', '', s_['rating'] if s_ else '', ver_,
                              sig.get('vault_value') or '', {True: 'yes', False: 'no', None: ''}[sig.get('matches_vault')], tools_, '', '', ''])
                (shots_t if sid.startswith('tripod-') else shots_).append(((QE.SHOTS / n_['screenshot']) if n_ and n_.get('screenshot') else None, (QE.SHOTS / o_['screenshot']) if o_ and o_.get('screenshot') else None))
            wq_ = tab(f"QS {ck.split('-')[0]} {meta.get('year', '')}", hdr, rows_, [14, 26, 24, 14, 50, 12, 50, 40, 12, 50, 40, 14, 22, 16, 12, 30, 40, 16, 30], jp_from=18, img=(8, 11))
            for i_, (a_, b_) in enumerate(shots_, 2): put_image(wq_, d, i_, 8, a_, 300, thumbs); put_image(wq_, d, i_, 11, b_, 300, thumbs)
            if rows_t:   # TRIPOD-LLM reporting items: their own tab, same columns
                wt_ = tab(f"TRIPOD {ck.split('-')[0]} {meta.get('year', '')}", ['Kind', 'TRIPOD-LLM item'] + hdr[2:], rows_t, [14, 30, 24, 14, 50, 12, 50, 40, 12, 50, 40, 14, 22, 16, 12, 30, 40, 16, 30], jp_from=18, img=(8, 11))
                for i_, (a_, b_) in enumerate(shots_t, 2): put_image(wt_, d, i_, 8, a_, 300, thumbs); put_image(wt_, d, i_, 11, b_, 300, thumbs)
            import tripod_items as TI
            fin_ = {s_: x_['final'] for s_, x_ in E_.get('signals', {}).items() if s_.startswith('tripod-')}; old_ = SRG.vault_tripod(key); new_s = TI.summary(fin_); old_s = TI.summary(old_)
            same_ = [s_ for s_ in fin_ if s_ in old_]; tri_sum.append([meta.get('title', ck)[:60], key, new_s['fully'], new_s['partial'], new_s['not-reported'], new_s['not-applicable'], (str(new_s['pct']) + '% ' + str(new_s['level'])) if new_s['pct'] is not None else '', old_s['fully'], old_s['partial'], old_s['not-reported'], old_s['not-applicable'], (str(old_s['pct']) + '% ' + str(old_s['level'])) if old_s['pct'] is not None else '', f"{sum(1 for s_ in same_ if fin_[s_] == old_[s_])} of {len(same_)}"])
            sigs_ = [x for x in E_.get('signals', {}).values() if x['ratings']]; st_ = M.get('stage_log', {}); t0_ = (st_.get('qs') or {}).get('started_utc', '')
            cost_ = {}; ends_ = []
            for c_ in calls:
                if c_.get('citekey') == ck and str(c_.get('step', '')).startswith('qs') and str(c_.get('ts_utc', '')) >= t0_: (cost_.__setitem__(c_.get('model'), cost_.get(c_.get('model'), 0) + float((re.search(r'cost_usd=([0-9.]+)', str(c_.get('notes', ''))) or [0, c_.get('cost_usd_est') or 0])[1])), ends_.append(str(c_.get('ts_utc', ''))))   # billed cost from the call note (batch mode is half the list price in cost_usd_est)
            prov_ = E_.get('provenance', []); mv_ = [x for x in sigs_ if x.get('matches_vault') is not None]
            qs_sum.append([meta.get('title', ck)[:60], key, len(sigs_), sum(1 for x in sigs_ if x['agreement'] == 'agree'), sum(1 for x in sigs_ if x['final'] == 'no majority'), sum(1 for x in sigs_ for r_ in x['ratings'] if r_.get('quote_found') is False), f"{sum(1 for x in mv_ if x['matches_vault'])} of {len(mv_)}",
                           sum(1 for i in prov_ if i['status'] == 'ok'), sum(1 for i in prov_ if i['status'] == 'flag'), sum(1 for i in prov_ if i['status'] == 'unavailable'), round(sum(cost_.values()), 3), '; '.join(f"{k}: ${v:.2f}" for k, v in cost_.items()), ((st_.get('qs') or {}).get('elapsed_s') or (round((__import__('datetime').datetime.fromisoformat(max(ends_)) - __import__('datetime').datetime.fromisoformat(t0_)).total_seconds()) if ends_ and t0_ else '')), (st_.get('qs_code_checks') or {}).get('papers', {}).get(ck, {}).get('elapsed_s', '')])
        if tri_sum: tab('TRIPOD-LLM summary', ['Paper', 'Vault citekey', 'New: fully reported', 'New: partial', 'New: not reported', 'New: not applicable', 'New: share reported (partial counts half) and level', 'Old table: fully reported', 'Old: partial', 'Old: not reported', 'Old: not applicable', 'Old table: share and level', 'New rating equals old curated rating'], tri_sum, [50, 38, 10, 10, 10, 10, 22, 10, 10, 10, 10, 22, 18])
        if qs_sum: tab('Quality signals run summary', ['Paper', 'Vault citekey', 'Signals rated by models', 'All raters agree', 'No majority', 'Quotes not found in PDF', 'Matches live-site tag', 'Code-only checks ok', 'Code-only checks flagged', 'Code-only checks unavailable', 'Rating cost USD', 'Cost by model', 'Rating time (s, batch wait included)', 'Code-only check time (s)'], qs_sum, [50, 38, 12, 12, 10, 12, 14, 12, 12, 12, 10, 46, 14, 14])
    nc_f = d / 'numbers_check.json'
    if nc_f.exists():
        NC = json.load(open(nc_f)); nr = []
        for x in NC['flagged']:
            nr.append([x['paper'], x['id'], ', '.join(map(str, x['pages'])), x['statement'], '; '.join(x['tokens']), '; '.join(f"{t}: {round(f, 2) if f is not None else ''}" for t, f in zip(x['tokens'], x['found'])), '; '.join(f"{t}: {round(c, 2) if c is not None else ''}" for t, c in zip(x['tokens'], x['control'])), '; '.join(f"{t}: {r_}" for t, r_ in zip(x['tokens'], x['result'])), '', '', ''])
        tab('Numbers check (EVD findings)', ['Paper', 'Finding', 'Cited PDF pages', 'Statement (first 200 characters)', 'Numbers not in the text of the cited pages', 'Liquid d1.2-ultra: number appears on the screenshots (probability)', 'Control: same number with one digit changed (should be low)', 'Result per number', 'Screenshots looked at (image)', 'JP: are the numbers right? (yes/no)', 'JP: notes'], nr, [30, 8, 12, 60, 24, 40, 40, 50, 40, 16, 30], jp_from=10)
    fa_f = d / 'failure_analysis.json'
    if fa_f.exists():
        FA = json.load(open(fa_f)); fr = [[x['paper'], x['ntype'], x['nid'], f"'Verification (all nodes)' row {x['row']} (cells A{x['row']}:AB{x['row']})", x['item'], x['passage'], x['sonnet_reason'], x['who_is_right'], x['failure_type'], x['reason'], x['fix'], '', ''] for x in sorted(FA, key=lambda x: (x['ntype'], x['row']))]
        tab('Failure analysis (sampled)', ['Paper', 'Node type', 'Node id', 'Where the item is', 'Item (as extracted)', 'Passage it was checked against', 'Sonnet 5.5 reason', 'Opus 5.5: who is right', 'Opus 5.5: failure type', 'Opus 5.5: reason', 'Opus 5.5: cheapest fix', 'JP: is Opus right? (yes/no)', 'JP: notes'], fr, [30, 10, 14, 34, 60, 60, 40, 16, 22, 50, 40, 16, 30], jp_from=12)
        ft = sorted({x['failure_type'] for x in FA if x['failure_type']}); nt = sorted({x['ntype'] for x in FA}); nF = len(fr) + 1; fs = "'Failure analysis (sampled)'!"
        tab('Failure types (sampled)', ['Node type'] + ft + ['Sampled items'], [[t_] + [f'=COUNTIFS({fs}B2:B{nF},"{t_}",{fs}I2:I{nF},"{f_}")' for f_ in ft] + [f'=COUNTIF({fs}B2:B{nF},"{t_}")'] for t_ in nt], [14] + [18] * (len(ft) + 1))
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
    if a.tripod_only:
        for ws_ in list(wb.worksheets):
            if not (ws_.title.startswith('TRIPOD') or ws_.title == 'ABOUT'): wb.remove(ws_)
    out = a.out or str(d / ('review_tripod.xlsx' if a.tripod_only else 'review.xlsx')); wb.save(out); print('saved', out, '| findings', len(frow), '| spans', len(crow))
if __name__ == '__main__': main()

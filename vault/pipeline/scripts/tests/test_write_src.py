"""Offline tests for scripts/write_src.py (JP, 2026-11-27): the checks that run on a model's SRC page, with canned model output and a synthetic two-page PDF. No model call, no network, no cost.
Run: python3 tests/test_write_src.py   (selftest.py runs the same checks)"""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fitz
import write_src as W, pdf_pages as pp
bad = 0; n_ok = 0
def check(name, cond, detail=''):
    global bad, n_ok
    if cond: n_ok += 1
    else: bad += 1; print('MISMATCH', name, detail)

QUOTE = 'Finally, the datasets do not contain information on how long it took the human raters to assess each publication.'
def synth_pdf(path):
    doc = fitz.open(); doc.new_page(width=612, height=792); doc.new_page(width=612, height=792); p1 = doc[0]; p2 = doc[1]
    for i, line in enumerate(['We used 112 reviews in total and Alpha reached 0.90 accuracy on PRISMA.', 'Beta reached 63% accuracy on PRISMA, and the humans reached 89%.']): p1.insert_text((50, 40 + i * 14), line, fontsize=8)
    p1.insert_text((72, 100), 'Table 1. Accuracy of three models.', fontsize=10)
    vals = [['Model', 'Accuracy', 'CI'], ['Alpha', '0.90', '(0.88-0.93)'], ['Beta', '63%', '(60%-66%)'], ['Gamma', '1,000', '(900-1,100)']]
    for r in range(4):
        for c in range(3):
            p1.draw_rect(fitz.Rect(72 + c * 100, 120 + r * 22, 72 + (c + 1) * 100, 120 + (r + 1) * 22), color=(0, 0, 0), width=0.6); p1.insert_text((72 + c * 100 + 4, 120 + r * 22 + 15), vals[r][c], fontsize=8)
    p2.draw_rect(fitz.Rect(40, 20, 300, 70), color=(0, 0, 0), width=0.8); p2.insert_text((50, 45), 'toy flow box', fontsize=8); p2.insert_text((40, 80), 'Figure 1. Flow of the toy study.', fontsize=8); p2.insert_text((40, 300), QUOTE, fontsize=7)
    doc.save(path)

NODES = {'E-F1': {'id': 'E-F1', 'type': 'EVD', 'statement': 'Alpha reached 0.90 accuracy on PRISMA reviews.'}, 'V-V1': {'id': 'V-V1', 'type': 'CVT', 'limitation': 'No time on task was recorded.'},
         'Q-Q1': {'id': 'Q-Q1', 'type': 'QUE', 'title': 'How accurate is Alpha?'}}
SUMMARY = ' '.join(['The authors ask whether a model can appraise research reports as well as human raters do and describe a small toy comparison to find out.', 'They give several models the same reports and compare each rating with the agreed human rating.', 'They conclude that the model alone does not match the humans, although pairing the two may help.', 'They warn that the reference ratings come from very few raters and that the test data may be unrepresentative.', 'They also note that nobody measured the time the work takes, so any saving is unproven and needs a proper test first by independent teams.'])
GOOD = f'''> [!success] **Summary**
> {SUMMARY}

### ❓ Question
- [[Q-Q1]] asks how accurate Alpha is.

### 🔬 Methods
- [[E-F1]] **Design.** A toy comparison of three models.
- **Sample.** 112 reviews in total (Section 1, p. 1).
- **Procedure.**
  1. The authors ran each model once.

**Table 1, p. 1.** Accuracy of three models.

| Model | Accuracy | CI |
| --- | --- | --- |
| Alpha | 0.90 | (0.88-0.93) |
| Beta | 63% | (60%-66%) |
| Gamma | 1,000 | (900-1,100) |

### 📊 Findings
- [[E-F1]] **Alpha beat Beta.** Alpha reached 0.90 and Beta 63% accuracy on PRISMA (Table 1, p. 1). Humans reached 89% (Section 1, p. 1).

### 💡 Claim supported
- Nothing beyond the finding.

### 🚧 Caveats
- [[V-V1]] **No time on task.** The paper says "{QUOTE}" (p. 2).

### 📭 Not reported
- Nothing flagged.
'''
def run_validate(body, tmp, pdf, parsers=('pymupdf',)):
    doc = fitz.open(pdf); return W.validate(body, NODES, doc, pdf, set(), parsers)
def kinds(flags): return sorted({f['kind'] for f in flags})
def has(flags, kind, text): return any(f['kind'] == kind and text in (f['what'] + str(f.get('quote', '')) + str(f.get('context', ''))) for f in flags)

tmp = Path(tempfile.mkdtemp()); pdf = tmp / 'toy.pdf'; synth_pdf(str(pdf))
body, v, flags = run_validate(GOOD, tmp, pdf)
check('good page: no flag for a human to examine', flags == [], flags)
check('the Summary has 100 to 125 words and no citation', v['summary']['ok'] and 100 <= v['summary']['words'] <= 125 and v['summary']['citations'] == 0, v['summary'])
check('good page: every number found in the paper, the quote located on the cited page, the table matched', all(x['status'] == 'found_in_paper' for x in v['numbers']) and v['quotes'][0]['found'] and v['quotes'][0]['page_ok'] is True and v['tables'][0]['matched'] == v['tables'][0]['cells'] == 12, (v['numbers'], v['quotes'], v['tables']))
check('good page: the three node ids are linked', v['links']['used'] == ['E-F1', 'Q-Q1', 'V-V1'] and not v['links']['unknown_ids'])
check('node links become vault links with the type and the id', '[[sysrev/dgraph/evidence/EVD - Alpha reached 0.90 accuracy on PRISMA reviews|EVD E-F1 - Alpha reached 0.90 accuracy on PRISMA reviews.]]' in body and '[[sysrev/dgraph/questions/QUE - How accurate is Alpha|QUE Q-Q1 - How accurate is Alpha]]' in body)
check('a good page passes the style rules', v['style'] == [], v['style'])

wrong = GOOD.replace('112 reviews in total', '121 reviews in total')
_, v2, f2 = run_validate(wrong, tmp, pdf)
check('planted wrong number (121 for 112) is flagged as not found in the paper', has(f2, 'number', '121') and kinds(f2) == ['citation', 'number'], f2)
wrong2 = GOOD.replace('Beta 63%', 'Beta 67%')
_, v2b, f2b = run_validate(wrong2, tmp, pdf)
check('planted wrong number in a sentence (67% for 63%) is flagged with its sentence', has(f2b, 'number', '67') and any('Alpha reached 0.90 and Beta 67%' in f.get('context', '') for f in f2b), f2b)
card_only = GOOD.replace('112 reviews in total', '121 reviews in total')
_, v2c, f2c = W.validate(card_only, NODES, fitz.open(pdf), pdf, {'121'}, ('pymupdf',))
check('a number found only in the extraction is flagged as such, not as missing', any('only in the extraction' in f['what'] and '121' in f['what'] for f in f2c) and not any('not found in the paper' in f['what'] and '121' in f['what'] for f in f2c), f2c)

badq = GOOD.replace('how long it took the human raters', 'how much time it took the two raters')
_, v3, f3 = run_validate(badq, tmp, pdf)
check('a quote with changed words is flagged as not located', has(f3, 'quote', 'not located') and v3['quotes'][0]['found'] is False, f3)
wrongpage = GOOD.replace('each publication." (p. 2)', 'each publication." (p. 1)')
_, v4, f4 = run_validate(wrongpage, tmp, pdf)
check('a quote cited to the wrong printed page is flagged', v4['quotes'][0]['found'] and v4['quotes'][0]['page_ok'] is False and has(f4, 'quote', 'cited as p. 1'), f4)

ghost = GOOD.replace('- [[V-V1]] **No time', '- [[V-V9]] **No time')
_, v5, f5 = run_validate(ghost, tmp, pdf)
check('a node id that is not in the run is flagged, and the unlinked node is listed', has(f5, 'link', 'V-V9') and v5['links']['unknown_ids'] == ['V-V9'] and 'V-V1' in v5['links']['not_linked'], f5)

cell_bad = GOOD.replace('| Alpha | 0.90 |', '| Alpha | 0.91 |')
_, v6, f6 = run_validate(cell_bad, tmp, pdf)
check('a table cell that differs from the PDF table is flagged with copy and source', any(f['kind'] == 'table_cell' and "'0.91'" in f['what'] and "'0.90'" in f['what'] for f in f6), f6)
nocite = GOOD.replace('**Table 1, p. 1.** Accuracy of three models.\n\n', '')
_, v7, f7 = run_validate(nocite, tmp, pdf)
check('a table with no citation line above it is flagged', has(f7, 'table', 'no source citation'), f7)

dash = GOOD.replace('Nothing flagged.', 'Nothing flagged ' + chr(0x2014) + ' at all. The tool is ACCURATE.')
_, v11, f11 = run_validate(dash, tmp, pdf)
check('an em dash and an all-caps word are flagged by the writing rules', has(f11, 'writing_rules', 'em dash') and has(f11, 'writing_rules', 'ACCURATE'), f11)

late = GOOD.replace('- [[E-F1]] **Alpha beat Beta.**', '- **Alpha beat Beta.** [[E-F1]]')
_, v12, _ = run_validate(late, tmp, pdf)
check('a bullet with the node link after its lead is a style flag', any(s['rule'] == 'link_not_first' for s in v12['style']), v12['style'])
long = GOOD.replace('Humans reached 89% (Section 1, p. 1).', 'Humans reached 89% (Section 1, p. 1) because ' + ' '.join(['the'] * 30) + ' end.')
_, v13, _ = run_validate(long, tmp, pdf)
check('a sentence over 25 words is a style flag', any(s['rule'] == 'sentence_over_25_words' for s in v13['style']), v13['style'])
check('the registry has the src_writer role: Sol, medium, and the prompt file exists with its id', W.SRC_MODEL == 'gpt-6.2-sol' and W.SRC_EFFORT == 'medium' and (W.VAULT / W.PROMPT_FILE).exists() and f'id: {W.PROMPT_ID}' in (W.VAULT / W.PROMPT_FILE).read_text())
check('src_write is not a standard-mode stage and the script offers only batch mode', 'src_write' not in W.C.PIPE['limits']['standard_stages'])

# ---- 2026-11-27 additions: cited-number check, table count, judge, node names, one batch for all papers, manifest label
unc = GOOD.replace('(Section 1, p. 1).\n- **Procedure', '.\n- **Procedure')
_, vu, fu = run_validate(unc, tmp, pdf)
check('a sentence with a number and no citation is flagged', any(f['kind'] == 'citation' and 'no table, figure or page citation' in f['what'] and '112' in f['what'] for f in fu), fu)
offp = GOOD.replace('112 reviews in total (Section 1, p. 1)', '112 reviews in total (Table 1, p. 1)')
_, vo, fo = run_validate(offp, tmp, pdf)
check('a number that is not in the cited table is flagged although it is elsewhere on the page', any(f['kind'] == 'citation' and "['112']" in f['what'] and 'Table 1, p. 1' in f['what'] for f in fo), fo)
okc = [x for x in v['cited_numbers'] if x['status'] != 'ok']
check('a good page has no uncited number sentence and no number off its cited page', okc == [], okc)
no_tab = '\n'.join(l for l in GOOD.splitlines() if not l.startswith('|') and not l.startswith('**Table 1, p. 1.**'))
_, vt, ft = run_validate(no_tab, tmp, pdf)
check('a page with no copied Methods table is flagged', has(ft, 'table', '0 copied table'), ft)
three = GOOD + '\n' + '\n'.join(['| a | b |', '| --- | --- |', '| 1 | 2 |', ''])
check('table count: one is fine, none or three is not', W.check_table_count(GOOD)['ok'] and not W.check_table_count(no_tab)['ok'] and W.check_table_count(GOOD + '\n\n' + '\n'.join(['**Table 1, p. 1.** again', '| a | b |', '| --- | --- |', '| 1 | 2 |']) + '\n\n' + '\n'.join(['| c | d |', '| --- | --- |', '| 1 | 2 |']))['tables'] == 3)
bl = W.findings_bullets(GOOD)
check('the Findings bullets are found by their node id', list(bl) == ['E-F1'] and 'Alpha beat Beta' in bl['E-F1'], bl)
vd = W.parse_judge('```json\n{"bullets": [{"id": "E-F1", "verdict": "partly", "reason": "Beta was 63% only on PRISMA"}]}\n```')
jf = W.judge_flags(vd, bl)
check('a judge verdict of partly becomes a flag with the reason; supported is no flag; a missing verdict and an unreadable answer are flags', len(jf) == 1 and jf[0]['kind'] == 'judge' and 'partly' in jf[0]['what'] and 'only on PRISMA' in jf[0]['reason']
      and W.judge_flags(W.parse_judge('{"bullets": [{"id": "E-F1", "verdict": "supported", "reason": "ok"}]}'), bl) == [] and 'no verdict' in W.judge_flags({}, bl)[0]['what'] and 'could not be read' in W.judge_flags(W.parse_judge('not json'), bl)[0]['what'], jf)
jt = json.loads(W.judge_text(bl, {'E-F1': {'id': 'E-F1', 'source_id': 'F1', 'statement': 'S', 'quote': 'Q', 'tier': 'primary'}}, {'findings': [{'id': 'F1', 'statement': 'FS', 'numbers': [{'value': '0.90'}], 'spans': [{'text': 'span'}]}]}))
check('the judge input holds the bullet, the EVD node, the finding numbers and the spans', jt['bullets'][0]['finding']['spans'] == ['span'] and jt['bullets'][0]['evd_node']['statement'] == 'S' and 'Alpha beat Beta' in jt['bullets'][0]['bullet'])
import node_names as NN
long_evd = {'id': 'E-F2', 'type': 'EVD', 'statement': 'word ' * 80}
check('node_names: the vault path stays at 150 characters or less, the stem starts with the type, the link carries the type, the id and the full title', len(f'sysrev/dgraph/evidence/{NN.node_stem(long_evd)}.md') <= 150 and NN.node_stem(long_evd).startswith('EVD - ') and NN.node_link(NODES['E-F1']) == '[[sysrev/dgraph/evidence/EVD - Alpha reached 0.90 accuracy on PRISMA reviews|EVD E-F1 - Alpha reached 0.90 accuracy on PRISMA reviews.]]')
check('write_src links use the same node_names function', W.N is NN and '[[sysrev/dgraph/questions/' in W.resolve_links_keep_embeds('[[Q-Q1]]', NODES)[0])
# one batch for all papers, saved answers reused, manifest label with a note, calls.jsonl note
import json as _j, shutil
rt = Path(tempfile.mkdtemp()); (rt / 'RUN' / 'pA').mkdir(parents=True); (rt / 'RUN' / 'pB').mkdir(); (rt / 'RUN' / 'manifest.json').write_text(_j.dumps({'run_id': 'RUN', 'spent_usd': 1.0, 'stage_log': {}}))
saved = (W.cl.RUNS, W.L.submit_batch, W.L.poll_batch, W.L.fetch_batch); seen = {}
def fake_submit(reqs): seen['n'] = len(reqs); seen['models'] = {r.model for r in reqs}; return {'provider': 'openai', 'model': reqs[0].model, 'ids': {r.id: r.id for r in reqs}, 'submitted': 0, 'n': len(reqs)}
def fake_fetch(job): return {i: W.L.Res(i, True, 'page ' + i, 1000, 500, 'completed') for i in job['ids']}
try:
    W.cl.RUNS = rt; W.L.submit_batch = fake_submit; W.L.poll_batch = lambda j: 'done'; W.L.fetch_batch = fake_fetch
    dirs = {'pA': rt / 'RUN' / 'pA', 'pB': rt / 'RUN' / 'pB'}; reqs = {k: W.L.Req(f'{k}__src_write', W.SRC_MODEL, 'x', system='s') for k in dirs}
    res1, fr1, _ = W.run_stage('RUN', 'src_write', W.SRC_MODEL, 'medium', W.PROMPT_FILE, reqs, dirs, 30000, 1.0)
    check('two papers go to the model in one batch call, each answer is saved in its paper folder', seen['n'] == 2 and set(res1) == {'pA', 'pB'} and (dirs['pA'] / 'src_write_response.json').exists() and (dirs['pB'] / 'src_write_response.json').exists())
    mf = _j.loads((rt / 'RUN' / 'manifest.json').read_text()); calls = [_j.loads(l) for l in (rt / 'RUN' / 'calls.jsonl').read_text().splitlines()]
    check('the manifest stage_log names the stage, mode, model and cost with a note; spent_usd is unchanged; each call record carries the note', mf['stage_log']['src_write']['mode'] == 'batch' and mf['stage_log']['src_write']['requests'] == 2 and 'added after the run' in mf['stage_log']['src_write']['note'] and mf['spent_usd'] == 1.0 and len(calls) == 2 and all('added after the run finished' in c['notes'] for c in calls), mf)
    seen.clear(); res2, fr2, _ = W.run_stage('RUN', 'src_write', W.SRC_MODEL, 'medium', W.PROMPT_FILE, reqs, dirs, 30000, 1.0)
    check('a second run uses the saved answers and makes no call', not seen and not any(fr2.values()))
    try: W.run_stage('RUN', 'src_judge', W.JUDGE_MODEL, 'medium', W.JUDGE_PROMPT_FILE, reqs, {k: rt / 'RUN' / k for k in dirs} | {}, 30000, 0.0000001); over = False
    except SystemExit: over = True
    check('a stage whose worst case is over the cap submits nothing', over and not seen)
finally: W.cl.RUNS, W.L.submit_batch, W.L.poll_batch, W.L.fetch_batch = saved
check('roles.src_judge is Neon at medium effort and is not the writer', W.JUDGE_MODEL == 'gemini-4-neon' and W.JUDGE_EFFORT == 'medium' and W.JUDGE_MODEL != W.SRC_MODEL and (W.VAULT / W.JUDGE_PROMPT_FILE).exists())

# ---- 2026-11-27 (JP's review): grounding crops, embeds that resolve, Summary, layout, generated tables
import src_crops as KK, src_sections as XX
doc = fitz.open(pdf); att = tmp / 'Attachments'
gt, grecs, gfl = W.build_grounding(GOOD + '\nSee Figure 1 (Figure 1, p. 2).\n', doc, 'toycite', att)
check('every cited table and figure gets a crop file named as its embed, under a Grounding line with the printed page and the PDF caption', len(grecs) == 2 and gfl == [] and (att / 'toycite-src-table1-p1.png').exists() and (att / 'toycite-src-figure1-p2.png').exists()
      and '> Grounding table (Table 1, p. 1): Accuracy of three models.' in gt and '> ![[toycite-src-table1-p1.png]]' in gt and '> Grounding figure (Figure 1, p. 2): Flow of the toy study.' in gt, (grecs, gt))
check('the table crop holds the table and its caption but not the body text above it, and is a real image', grecs[0]['pixels'][0] > 100 and grecs[0]['bbox'][1] > 60 and grecs[0]['bbox'][3] < 260, grecs[0])
check('the crop sits under the caption: the figure crop includes the drawing above its caption', grecs[1]['bbox'][1] < 30 and grecs[1]['bbox'][3] > 80, grecs[1])
res = KK.embeds_resolve(gt, [att])
check('every embed of the page resolves to an existing file', res and all(f for _, f in res), res)
(att / 'toycite-src-table1-p1.png').unlink(); res2 = KK.embeds_resolve(gt, [att])
check('an embed whose file is missing is reported as not found', dict(res2)['toycite-src-table1-p1.png'] is False and dict(res2)['toycite-src-figure1-p2.png'] is True, res2)
_, _, gf2 = W.build_grounding(GOOD.replace('Table 1, p. 1', 'Table 7, p. 1'), doc, 'toycite', att)
check('a table cited but not found in the PDF is a flag, not a missing image', any('table 7' in f['what'] and 'caption was not found' in f['what'] for f in gf2), gf2)
check('crop names differ from the EVD crops (<citekey>-table2-p5-1.png) so the vault never resolves a bare name to the wrong file', KK.embed_name('k', 'table', '2', 5) == 'k-src-table2-p5.png')
legacy = '> [!success] **TL;DR**\n> x\n\n## Abstract\n\n### Question\n- a\n\n### Not reported\n- b\n\n## Grounding: tables and figures cited\n> ![[a-table1-p1-1.png]]\n'
nb = W.normalize_body(legacy)
check('an older answer is brought to the v3 layout: Summary, no Abstract heading, emoji on each subheading, no Grounding section', '**Summary**' in nb and '## Abstract' not in nb and '### ❓ Question' in nb and '### 📭 Not reported' in nb and 'Grounding' not in nb and '![[' not in nb, nb)
sl = W.space_lists('### 📊 Findings\n- a\n  - sub\n- b\n### 💡 Claim\n- c\n')
check('list items get a blank line between them, sub-bullets stay with their parent, headings have air around them', '- a\n  - sub\n\n- b' in sl and '\n\n### 💡 Claim\n\n- c' in sl, sl)
check('the Summary check flags a short summary and one with a citation', not W.check_summary('> [!success] **Summary**\n> Too short (Table 1, p. 1).\n')['ok'] and W.check_summary('> [!success] **Summary**\n> Too short (Table 1, p. 1).\n')['citations'] >= 1)
nr = W.check_style(GOOD.replace('- Nothing flagged.', '- First item. And a second sentence.'))
check('a Not reported item of more than one sentence is a style flag', any(s['rule'] == 'not_reported_not_one_line' for s in nr), nr)
check('the Abstract subheading is a style flag', any(s['rule'] == 'abstract_heading' for s in W.check_style('## Abstract\n' + GOOD)))
paper = {'provenance': [{'id': 'fair-code', 'status': 'flag', 'label': 'Code FAIR', 'tool': 'howfairis', 'checked_utc': '2026-11-27T00:00:00Z', 'result': 'x', 'url': ''}],
         'signals': {'construct-validity': {'id': 'construct-validity', 'label': 'Construct Validity', 'final': 'some-concerns', 'summary': 's', 'ratings': [{'rater': 'Gemini 4 Neon', 'rating': 'some-concerns', 'quote': QUOTE, 'locator': 'Discussion', 'pdf_page': 2, 'printed_page': None, 'confidence': 'medium', 'screenshot': 'k/construct-validity__neon.jpg'}], 'checks': [{'verifier': 'GPT-6.2 Sol', 'score': 1.0, 'note': ''}], 'tool_checks': []},
                     'code-quality-fair': {'id': 'code-quality-fair', 'label': 'Code Quality', 'final': 'meets 3 of 6', 'summary': 'meets 3 of 6', 'ratings': [], 'checks': [], 'tool_checks': ['fair-code']},
                     'tripod-5c': {'id': 'tripod-5c', 'label': 'TRIPOD-LLM 5c: Date range of data', 'final': 'not-reported', 'summary': 'Neon rates this not-reported.', 'ratings': [{'rater': 'Gemini 4 Neon', 'rating': 'not-reported', 'quote': '', 'locator': '', 'pdf_page': None, 'confidence': 'medium'}], 'checks': [], 'tool_checks': []}}}
pm = {1: '1', 2: '2'}
qt, qk = XX.quality_table(paper, pm); tt, tk = XX.tripod_table(paper, pm, len(qk) + 1)
check('Quality appraisal table: H2 name the web app reads, a bold domain in the first cell, one glyph alone in the rating cell, rating word plus the quote with its printed page and an S-key in the evidence cell', qt.startswith('## Quality appraisal') and '| **Construct validity**: does the metric actually measure the construct? | 🟡 | Some concerns. *"Finally, the datasets' in qt.replace('the presented datasets', 'the datasets') and '`p. 2` [S-01]' in qt and '| **Code Quality**' in qt and '| 🟡 |' in qt, qt[:900])
check('TRIPOD-LLM table: H2 name the web app reads, bold item number, a status glyph alone, Fully/Not reported wording, items 2 and 17 as in the older pages, keys continue after the quality keys', tt.startswith('## TRIPOD-LLM reporting') and '| **5c** | Date range of data | ❌ | Not reported. Neon rates' in tt and '| **2** | Abstract | ➖ |' in tt and '| **17** | Performance | per-EVD |' in tt and tk[0][0] == f'S-{len(qk) + 1:02d}', tt)
pv = XX.provenance_table(paper, qk + tk, 'k', lambda rel: True)
check('provenance table: collapsed callout, one row per key with the model, confidence, verifier score, locator, full quote and screenshot', pv.startswith('> [!info]- Evidence provenance') and '| S-01 | Construct Validity | Some concerns | Gemini 4 Neon (medium) | GPT-6.2 Sol 1.00 | Discussion' in pv and QUOTE[:40] in pv and 'construct-validity__neon.jpg|image' in pv, pv[:700])
rows = XX.properties_rows('toycite', {'title': 'T', 'authors': 'A B, C D', 'year': '2024', 'venue': 'V', 'doi': '10.1/x'}, paper, 'Sol', '2026-11-27')
check('Properties: the fields and their order are those of the older Woelfle source page, in a collapsed callout; a value the pipeline cannot supply says so', [r[0] for r in rows] == XX.PROPERTY_ORDER and XX.PROPERTY_ORDER[:6] == ['dg_type', 'status', 'keywords', 'rating', 'tags', 'doi'] and XX.properties_table(rows).startswith('> [!info]- Properties') and dict((r[0], r[1]) for r in rows)['oa_status'] == 'not available' and dict((r[0], r[1]) for r in rows)['status'] == 'test, not validated')
ai, models, when = XX.ai_use_table([{'step': 'src_write', 'model_id': 'gpt-6.2-sol', 'model': 'GPT-6.2 Sol', 'effort': 'medium', 'ts_utc': '2026-11-27T10:00:00+00:00', 'prompt_file': 'pipeline/prompts/src-write-v3.md'}, {'step': 'src_judge', 'model_id': 'gemini-4-neon', 'model': 'Gemini 4 Neon', 'effort': 'medium', 'ts_utc': '2026-11-27T10:05:00+00:00', 'prompt_file': 'pipeline/prompts/src-judge-v1.md'}], 'not yet human-checked')
check('AI use: a collapsed table with one row per model and the GAMER key elements as columns (task here and in the pipeline, version and date, prompt, effort, oversight, verification)', ai.startswith('> [!info]- AI use: ') and '| Model | Task on this page | Task in the pipeline | Version and date (UTC) | Prompt ids | Effort | Human oversight | Verification |' in ai and '| GPT-6.2 Sol | wrote the prose |' in ai and 'src-judge-v1' in ai and '`gemini-4-neon`, 2026-11-27' in ai, ai[:600])
print('write_src tests: passed', n_ok, 'mismatches', bad)
def run(): return n_ok, bad
if __name__ == '__main__': sys.exit(1 if bad else 0)

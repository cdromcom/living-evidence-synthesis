#!/usr/bin/env python3
"""Offline self-test for the pipeline (JP, 2026-11-25): no API calls, no cost. Run it after changing a model, a package, a prompt, a template or a limit.
  python3 selftest.py
Checks: the config files and the origin policy; every role's model has a price and a route; prompts exist with their placeholders; the quality-signal ids match the registry of row names;
writing-rules check; the runner's guards (paper limit, cap, research question, repeat PDFs); supplement merging; PDF slicing and merged screenshots; package versions."""
import importlib.metadata as md, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
fails = []; ok = 0
def check(name, cond, detail=''):
    global ok
    if cond: ok += 1; print(f'  ok    {name}')
    else: fails.append(name); print(f'  FAIL  {name} {detail}')
V = C.VAULT; here = Path(__file__).resolve().parent
print('config and policy')
roles = [C.ROLES[k] for k in ('extract', 'recheck', 'adjudicate', 'vision_check', 'vision_dispute', 'tiebreak')] + [x['model'] for k in ('authors', 'voters', 'raters') for x in C.ROLES[k]]
check('every role model is in models.json with a price', all(m in C.MODELS and C.MODELS[m]['price_in'] >= 0 for m in roles), str([m for m in roles if m not in C.MODELS]))
check('every role model passes the origin policy', all(C.assert_allowed(m) for m in roles))
check('every role model has a provider route', all(C.provider_of(m) in ('anthropic', 'openai', 'google', 'tinker') for m in roles), str([m for m in roles if C.provider_of(m) not in ('anthropic', 'openai', 'google', 'tinker')]))
check('limits are sane', 1 <= C.PIPE['limits']['max_papers'] <= 10 and 0 < C.PIPE['limits']['cap_usd'] < 100 and C.PIPE['limits']['overrun_factor'] >= 1)
check('decision models named in roles exist in decision_models.py', all(k in __import__('decision_models').MODELS for k in C.ROLES['decision_models']))
try: C.POLICY['hosted_api_allowed_countries'] = ['XX']; bad = False; C.assert_allowed('gemini-4-neon')
except ValueError: bad = True
finally: C.POLICY['hosted_api_allowed_countries'] = ['US']
check('the origin policy blocks a disallowed country', bad)
print('prompts and registries')
import lives_run as R, lives_stages as S
for st, pth in R.STAGE_PROMPT.items(): check(f'prompt {pth}', (V / pth).exists())
check('picost prompt has no leftover cap placeholders (no caps on questions or findings)', '{MAX_' not in (V / R.STAGE_PROMPT['picost']).read_text())
check('vision-check-v3 allows cannot_verify', 'cannot_verify' in (V / 'pipeline/prompts/vision-check-v3.md').read_text())
check('EVD rework: a separate frontier model (not one of the three authors) and its prompt', C.ROLES['evd_rework'] not in [m for _, m, _ in S.AUTHORS] and (V / 'pipeline/prompts/evd-rework-v1.md').exists() and 'draft_rework' in C.PIPE['limits']['standard_stages'])
g1 = R.numbers_list_gaps({'statement': 'GPT-4 scored 71.4% on 200 papers; Human Rater 1 scored 60%.', 'numbers': [{'label': 'GPT-4 accuracy', 'value': '71.4', 'unit': '%', 'table_or_figure': 'Table 2', 'pdf_page': 5, 'printed_page': '5'}, {'label': 'Human Rater 1', 'value': '60', 'unit': '%', 'table_or_figure': '', 'pdf_page': None, 'printed_page': ''}]})
check('numbers-list check: a number in the statement with no list entry is found, a label number (Human Rater 1) and a model name digit (GPT-4) are not', g1['missing'] == ['200'] and g1['no_location'] == ['60%'])
check('numbers-list check: 89% in the statement matches 0.89 in the list', R.numbers_list_gaps({'statement': 'Agreement was 89%.', 'numbers': [{'value': '0.89', 'table_or_figure': 'Table 1'}]}) == {'missing': [], 'no_location': []})
check('the paper limit is 3 (4 on days JP sets it aside) and the review gate lists unreviewed batches', R.MAX_PAPERS in (3, 4) and isinstance(R.unreviewed_batches(), list))
check('quality signals: three raters from three developers at high effort (maximum accuracy), no adjudicator needed', len(S.RATERS) == 3 and len({m.split('-')[0] for _, m, _ in S.RATERS}) == 3 and all(e == 'high' for _, _, e in S.RATERS) and S.QS_MAX and (V / 'pipeline/prompts/adjudicate-signals-v1.md').exists())
for n in ('draft-nodes-v4', 'critique-revise-v4', 'evd-rework-v3', 'vote-v1', 'node-detail-check-v1', 'rate-signals-v1', 'vision-check-v3'): check(f'prompt {n}', (V / 'pipeline/prompts' / f'{n}.md').exists())
check('rate-signals prompt has the signals placeholder', '{SIGNALS}' in (V / 'pipeline/prompts/rate-signals-v1.md').read_text())
ids = {r['id'] for r in json.loads((V / 'pipeline/templates/quality-signal-labels.json').read_text())['rows']}
check('quality signals rated by the models are valid row ids (TRIPOD-LLM rows have their own list)', {x for x in S.SIGNALS if not x.startswith('tripod-')} <= ids, str(sorted({x for x in S.SIGNALS if not x.startswith('tripod-')} - ids)))
print('writing-rules check and parsing')
good = {'type': 'EVD', 'statement': 'GPT 3.5-turbo scored 71.4% on 120 reviews (kappa = 0.5).', 'quote': 'x'}
check('writing-rules check passes a good EVD', S.writing_rules(good, {S.norm_num(x) for x in ('71.4', '120', '0.5', '3.5')})['pass'])
check('writing-rules check fails an EVD over 247 characters', not S.writing_rules({**good, 'statement': 'word ' * 60}, set())['pass'])
check('writing-rules check flags a number not on the card', S.writing_rules({**good, 'statement': 'Model scored 99.9%.'}, {'71.4'})['numbers_not_on_card'] == ['99.9'])
check('writing-rules check accepts two sets of parentheses and rejects three, brackets and all-caps words', S.writing_rules({**good, 'statement': 'Model A (zero-shot) scored 71.4% (kappa = 0.5).'}, {S.norm_num(x) for x in ('71.4', '0.5')})['parentheses_ok'] and not S.writing_rules({**good, 'statement': 'A (a) scored 71.4% (b) vs (kappa = 0.5).'}, {S.norm_num(x) for x in ('71.4', '0.5')})['parentheses_ok'] and not S.writing_rules({**good, 'statement': 'A scored 71.4% [kappa = 0.5].'}, {S.norm_num(x) for x in ('71.4', '0.5')})['parentheses_ok'] and not S.writing_rules({**good, 'statement': 'A labeled ACCURATE items, 71.4% (kappa = 0.5).'}, {S.norm_num(x) for x in ('71.4', '0.5')})['caps_ok'] and S.writing_rules({**good, 'statement': 'A appraised PRISMA items, 71.4% (kappa = 0.5).'}, {S.norm_num(x) for x in ('71.4', '0.5')})['caps_ok'])
check('writing-rules check fails an em dash', not S.writing_rules({**good, 'statement': 'Model A \u2014 a model scored 71.4%.'}, {S.norm_num('71.4')})['pass'])
import pdf_pages as _pp
check('an en dash that the PDF text layer stores as e still matches', _pp.norm('Human Rater 1 0.81 (0.78\u20130.83) 87%\u201390%') == _pp.norm('Human Rater 1 0.81 (0.78e0.83) 87%e90%'))
check('parse_json tolerates a code fence', S.parse_json('```json\n{"a": 1}\n```') == {'a': 1})
print('runner guards and PDF tools')
import fitz
with tempfile.TemporaryDirectory() as td:
    td = Path(td); pdfs = []
    for i in range(C.PIPE['limits']['max_papers'] + 1):
        d = fitz.open(); pg = d.new_page(); pg.insert_text((72, 100), f'Paper {i}. Results: Model A scored {60 + i}.1% (n = 100).'); f = td / f'Paper {i}.pdf'; d.save(str(f)); pdfs.append(str(f))
    run = lambda args: subprocess.run([sys.executable, str(here / 'lives_run.py')] + args, capture_output=True, text=True)
    check('too many PDFs are refused', 'Refused' in run(pdfs + ['--question', 'q', '--dry-run', '--run-id', 'test-selftest']).stdout + run(pdfs + ['--question', 'q', '--dry-run', '--run-id', 'test-selftest']).stderr)
    check('a cap above the limit is refused', 'cap per batch' in run([pdfs[0], '--question', 'q', '--cap', '99']).stdout + run([pdfs[0], '--question', 'q', '--cap', '99']).stderr)
    check('a run without a question works (the model finds the paper\'s own questions)', 'Refused' not in run([pdfs[0], '--mode', 'standard', '--dry-run', '--run-id', 'test-selftest']).stdout + run([pdfs[0], '--mode', 'standard', '--dry-run', '--run-id', 'test-selftest']).stderr)
    check('the default mode is batch (JP, 2026-11-26)', 'default=\'batch\'' in (here / 'lives_run.py').read_text())
    sup = td / 'Paper 0 - supplement 1.pdf'; d = fitz.open(); d.new_page().insert_text((72, 100), 'Supplementary Table S1'); d.save(str(sup)); d.close()
    check('a supplement is found next to its paper', [x.name for x in R.find_supplements(pdfs[0])] == ['Paper 0 - supplement 1.pdf'])
    comb = td / 'c.pdf'; sp = R.combine_pdfs(pdfs[0], [sup], str(comb)); check('supplement is combined after the paper', fitz.open(str(comb)).page_count == 2 and sp[0][1] == 1)
    out, keep = R.slice_pdf(str(comb), [2], str(td / 's.pdf'), around=0, limit=1.0); check('slice_pdf keeps only the cited pages', keep == [2])
    import pdf_pages as pp
    r = pp.merge_regions(str(comb), [(1, [(72, 90, 200, 105)]), (2, [(72, 90, 200, 105)])], str(td / 'm.png'), dpi=60); check('merged screenshot over two pages', r.get('ok') and (td / 'm.png').exists())
import shutil; shutil.rmtree(C.VAULT / 'pipeline/runs/test-selftest', ignore_errors=True)
import lives_verify as VV, decision_models as dm
check('the decision-model client uses Liquid d1.2-ultra and the registry knows it', dm.MODELS['liquid'] == 'd1.2-ultra' and 'd1.2-ultra' in C.MODELS)
_v = [{'paper': 'p', 'ntype': t, 'nid': n, 'majority': m, 'mean': 0.5} for t, n, m in (('CLM', 'C1', 'fail'), ('CLM', 'C1 quote', 'pass'), ('CVT', 'V1', 'pass'), ('QUE', 'Q1', 'fail'), ('QUE', 'Q1 quote', 'pass'), ('PICOST', 'F1: Population', 'pass'))]
_o = VV.queue_order(_v)
check('labeling queue holds claims, caveats and rewordings but not the quote-versus-print rows', [x['queue'] for x in _o if x['queue']] == ['1 CLM', '2 CVT', '4 QUE reframing'] and all(x['queue'] == '' for x in _o if x['nid'].endswith(' quote')))
check('word-overlap similarity is 0 when every word is in the passage and 1 when none is', VV.novel_share('citation errors detected', 'detected citation errors here') == 0 and VV.novel_share('citation errors detected', 'completely unrelated text') == 1)
check('a quote with digits is compared by digits on the screenshot', 'digit' in VV.image_question({'ntype': 'QUOTE', 'nid': 'F1 quote 1'}, 'A (model): GAR 0.58')[1])
import numbers_on_pages as NP
check('a statement number written as 1,000 or .58 matches the page text', NP.variants('0.58') >= {'0.58', '.58'} and '1000' in NP.variants('1,000'))
check('a number that is not on the screenshot goes to JP, a short one is not checked by image', NP.classify('0.78', 0.02, 0.01) == 'not found: JP check' and NP.classify('4', 0.9, 0.9) == 'too short to check by image' and NP.classify('0.56', 0.97, 0.0) == 'seen on screenshot')
check('the claim, caveat and question wording allows rewording', 'Different wording is fine' in VV.INS_CLM and 'restyled on purpose' in VV.INS_QUE)
import signal_registry as SRG, qs_export as QXP
check('every signal the models rate has a tag on the source page and a label', all(sg in SRG.SIGNAL_TAGS or sg.startswith('tripod-') for sg in S.SIGNALS) and len(S.SIGNALS) == 67 and sum(1 for sg in S.SIGNALS if sg.startswith('tripod-')) == 40 and SRG.label_for('study-type') == 'Study Type')
check('the required-tag list comes from the signal registry (power analysis is optional)', 'rigor/statistical-power' not in SRG.REQUIRED and 'top/study-registration' in SRG.REQUIRED)
check('a run folder name resolves to its vault citekey', SRG.resolve_citekey('Sarol-et-al-2024-Assessing-citation-integrity') == 'sarolAssessingCitationIntegrity2024')
check('the summary sentence names who agrees and who does not', QXP.summary_sentence('addressed', [{'rater': 'neon', 'rating': 'addressed'}, {'rater': 'opus', 'rating': 'partial'}, {'rater': 'sol', 'rating': 'addressed'}], {}, []) == 'Neon and Sol rate this addressed; Opus rated it partial.' and QXP.summary_sentence('no majority', [{'rater': 'neon', 'rating': 'a'}, {'rater': 'opus', 'rating': 'b'}], {}, []).endswith('needs your judgment.'))
import column_notes as CNT
check('every column header the sheet builder writes has a hover note for outsiders', all(CNT.note_for('Verification (all nodes)', h) for h in ('Sonnet 5.5 score', 'Majority vote', 'Labeling queue (tonight)', 'JP: notes', 'JP: is the extraction correct? (yes/no/unsure)')) and CNT.note_for('QS Sarol 2024', 'Result').startswith('The final rating') and all(CNT.note_for('Papers', h) for h in ('Primary findings', 'Cost USD')))
import tripod_items as TRI
check('TRIPOD-LLM summary counts partial as half and ignores not-applicable items', TRI.summary({'tripod-1': 'fully', 'tripod-3a': 'partial', 'tripod-4': 'not-applicable', 'tripod-5a': 'not-reported'})['pct'] == 50 and TRI.summary({'tripod-1': 'fully'})['level'] == 'high' and TRI.label('tripod-5c') == 'TRIPOD-LLM 5c: Date range of data')
import pdf_pages as _pp2
check('the text-layer symbol repair fixes an interval written with the letter e and leaves scientific notation alone', _pp2.repair_cell_text('0.37e0.44') == '0.37\u20130.44' and _pp2.repair_cell_text('1e-5') == '1e-5' and _pp2.repair_cell_text('a\u00feb') == 'a+b')
check('the symbol repair removes footnote letters from numeric cells only and keeps units, words and exponents', _pp2.repair_cell_text('62%b') == '62%' and _pp2.repair_cell_text('0.90 (0.88e0.93)a') == '0.90 (0.88\u20130.93)' and _pp2.repair_cell_text('3d') == '3d' and _pp2.repair_cell_text('ChatGPT4o') == 'ChatGPT4o' and _pp2.repair_cell_text('10\u00b3') == '10^3' and _pp2.repair_cell_text('(|24k)') == '(~24k)')
print('packages')
for pkg in ('pymupdf', 'anthropic', 'openai', 'openpyxl', 'pillow', 'requests'):
    try: print(f'  {pkg} {md.version(pkg)}'); ok += 1
    except Exception: fails.append(f'package {pkg}'); print(f'  FAIL  package {pkg} is not installed')
print(f'\n{ok} passed, {len(fails)} failed'); sys.exit(1 if fails else 0)

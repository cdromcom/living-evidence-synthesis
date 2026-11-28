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
roles = [C.ROLES[k] for k in ('extract', 'recheck', 'adjudicate', 'vision_check', 'vision_dispute')] + [x['model'] for k in ('authors', 'raters', 'node_check') for x in C.ROLES[k]] + [C.role_model(C.ROLES[k]) for k in ('qs_fallback', 'qs_adjudicator', 'evd_rework', 'verify_judge', 'verify_judge_alt', 'quote_check', 'grouping', 'classifier')]
check('every role model is in models.json with a price', all(m in C.MODELS and C.MODELS[m]['price_in'] >= 0 for m in roles), str([m for m in roles if m not in C.MODELS]))
check('every role model passes the origin policy', all(C.assert_allowed(m) for m in roles))
check('every role model has a provider route', all(C.provider_of(m) in ('anthropic', 'openai', 'google', 'tinker') for m in roles), str([m for m in roles if C.provider_of(m) not in ('anthropic', 'openai', 'google', 'tinker')]))
check('the classifier is a hosted model (Neon, low effort) and no local-model entry is left in the registry', C.role_model(C.ROLES['classifier']) == 'gemini-4-neon' and C.role_effort(C.ROLES['classifier']) == 'low' and 'gemma4-12b-qat' not in C.MODELS)
def _all_role_models():
    out = []
    for v in C.ROLES.values():
        for x in (v if isinstance(v, list) else [v]):
            if isinstance(x, (str, dict)) and x not in ('perplexity', 'liquid') and not str(x).startswith('JP'): out.append(C.role_model(x) if not isinstance(x, str) or x in C.MODELS else None)
    return [m for m in out if m]
check('no role uses an Opus model (JP, 2026-11-27); the registry entry stays', not [m for m in _all_role_models() if 'opus' in m] and 'claude-opus-5-5' in C.MODELS and C.ROLES['vision_dispute'] == 'claude-sonnet-5-5')
check('model procedure of 2026-11-27: raters = Neon high only, fallback = Sol high, adjudicate = Sonnet 5.5, authors = Sol only, no critics, voters or tiebreak roles, node check = Neon', [(a['model'], a['effort']) for a in C.ROLES['raters']] == [('gemini-4-neon', 'high')] and C.ROLES['qs_fallback']['model'] == 'gpt-6.2-sol' and C.ROLES['qs_fallback']['effort'] == 'high' and C.ROLES['adjudicate'] == 'claude-sonnet-5-5' and [a['model'] for a in C.ROLES['authors']] == ['gpt-6.2-sol'] and not any(k in C.ROLES for k in ('critics', 'voters', 'tiebreak')) and [a['model'] for a in C.ROLES['node_check']] == ['gemini-4-neon'])
check('the verification judge is not the extraction model (a model must not judge its own extractions), and the judge is Sol medium', C.role_model(C.ROLES['verify_judge']) != C.role_model(C.ROLES['extract']) and C.role_model(C.ROLES['verify_judge']) == 'gpt-6.2-sol' and C.role_effort(C.ROLES['verify_judge']) == 'medium')
check('Neon verifies no PICOST slot and no extracted item: no verification path uses the extraction model', all(C.role_model(x) != C.role_model(C.ROLES['extract']) for x in (C.ROLES['verify_judge'],)) and __import__('lives_verify').JUDGE != C.ROLES['extract'])
check('quote reading is not the extraction model (Sol, low), grouping is Neon medium, EVD rework is Neon with effort medium taken from the config', C.role_model(C.ROLES['quote_check']) == 'gpt-6.2-sol' and C.role_model(C.ROLES['quote_check']) != C.ROLES['extract'] and C.role_model(C.ROLES['grouping']) == 'gemini-4-neon' and C.role_effort(C.ROLES['grouping']) == 'medium' and C.role_model(C.ROLES['evd_rework']) == 'gemini-4-neon' and C.ROLES['evd_rework_effort'] == 'medium' and C.ROLES['recheck'] == 'gpt-6.2-sol' and C.ROLES['extract'] == 'gemini-4-neon')
check('quality signals: max_accuracy is off in the config', C.PIPE['quality_signals']['max_accuracy'] is False)
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
check('EVD fix (errors only): a model and an effort from the config, the new prompt evd-fix-v1 exists and the old evd-rework-v3 was not overwritten', S.RW_MODEL == C.role_model(C.ROLES['evd_rework']) and S.RW_EFFORT == C.ROLES['evd_rework_effort'] and S.RW_PROMPT == 'evd-fix-v1.md' and (V / 'pipeline/prompts/evd-fix-v1.md').exists() and 'Claude Opus' in (V / 'pipeline/prompts/evd-rework-v3.md').read_text() and 'draft_rework' in C.PIPE['limits']['standard_stages'])
g1 = R.numbers_list_gaps({'statement': 'GPT-4 scored 71.4% on 200 papers; Human Rater 1 scored 60%.', 'numbers': [{'label': 'GPT-4 accuracy', 'value': '71.4', 'unit': '%', 'table_or_figure': 'Table 2', 'pdf_page': 5, 'printed_page': '5'}, {'label': 'Human Rater 1', 'value': '60', 'unit': '%', 'table_or_figure': '', 'pdf_page': None, 'printed_page': ''}]})
check('numbers-list check: a number in the statement with no list entry is found, a label number (Human Rater 1) and a model name digit (GPT-4) are not', g1['missing'] == ['200'] and g1['no_location'] == ['60%'])
check('numbers-list check: 89% in the statement matches 0.89 in the list', R.numbers_list_gaps({'statement': 'Agreement was 89%.', 'numbers': [{'value': '0.89', 'table_or_figure': 'Table 1'}]}) == {'missing': [], 'no_location': []})
check('the paper limit is 3 (4 on days JP sets it aside) and the review gate lists unreviewed batches', R.MAX_PAPERS in (3, 4) and isinstance(R.unreviewed_batches(), list))
check('quality signals: one rater (Neon, high) with a Sol fallback, cascade mode on, the maximum-accuracy mode off, the old adjudicator prompt still there', len(S.RATERS) == 1 and S.RATERS[0][1:] == ('gemini-4-neon', 'high') and S.QS_FALLBACK[0][1:] == ('gpt-6.2-sol', 'high') and S.QS_CASCADE and not S.QS_MAX and (V / 'pipeline/prompts/adjudicate-signals-v1.md').exists())
check('drafting: one author (Sol), no debate (no critique, vote or tiebreak), node check Neon', [x[1] for x in S.AUTHORS] == ['gpt-6.2-sol'] and not S.DEBATE and [x[1] for x in S.NODE_CHECK] == ['gemini-4-neon'])
for n in ('draft-nodes-v4', 'critique-revise-v4', 'critique-revise-v5', 'evd-rework-v3', 'vote-v1', 'vote-v2', 'node-detail-check-v1', 'rate-signals-v1', 'rate-signals-v2', 'rate-signals-v3', 'vision-check-v3'): check(f'prompt {n}', (V / 'pipeline/prompts' / f'{n}.md').exists())
check('rate-signals prompt has the signals placeholder', '{SIGNALS}' in (V / 'pipeline/prompts/rate-signals-v1.md').read_text())
_v3 = (V / 'pipeline/prompts/rate-signals-v3.md').read_text(); _v2 = (V / 'pipeline/prompts/rate-signals-v2.md').read_text()
check('rate-signals-v3 asks for a confidence (high, medium, low) in the output, has the signals placeholder, and v2 was not overwritten', '"confidence"' in _v3 and '`low`' in _v3 and '{SIGNALS}' in _v3 and 'confidence' not in _v2)
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
check('the decision-model client uses Liquid d1.2-ultra and the registry knows it', dm.MODELS['liquid'] in ('d1.3-ultra', 'd1.2-ultra') and 'd1.2-ultra' in C.MODELS and 'd1.3-ultra' in C.MODELS)
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
check('every column header the sheet builder writes has a hover note for outsiders', all(CNT.note_for('Verification (all nodes)', h) for h in (f'{CNT.JD} score', 'Majority vote', 'Labeling queue (tonight)', 'JP: notes', 'JP: is the extraction correct? (yes/no/unsure)')) and CNT.note_for('QS Sarol 2024', 'Result').startswith('The final rating') and all(CNT.note_for('Papers', h) for h in ('Primary findings', 'Cost USD')))
import tripod_items as TRI
check('TRIPOD-LLM summary leaves needs_human rows out of the share and counts them', TRI.summary({'tripod-1': 'fully', 'tripod-3a': 'needs_human'})['needs_human'] == 1 and TRI.summary({'tripod-1': 'fully', 'tripod-3a': 'needs_human'})['applicable'] == 1)
check('TRIPOD-LLM summary counts partial as half and ignores not-applicable items', TRI.summary({'tripod-1': 'fully', 'tripod-3a': 'partial', 'tripod-4': 'not-applicable', 'tripod-5a': 'not-reported'})['pct'] == 50 and TRI.summary({'tripod-1': 'fully'})['level'] == 'high' and TRI.label('tripod-5c') == 'TRIPOD-LLM 5c: Date range of data')
import pdf_pages as _pp2
check('the text-layer symbol repair fixes an interval written with the letter e and leaves scientific notation alone', _pp2.repair_cell_text('0.37e0.44') == '0.37\u20130.44' and _pp2.repair_cell_text('1e-5') == '1e-5' and _pp2.repair_cell_text('a\u00feb') == 'a+b')
check('the symbol repair removes footnote letters from numeric cells only and keeps units, words and exponents', _pp2.repair_cell_text('62%b') == '62%' and _pp2.repair_cell_text('0.90 (0.88e0.93)a') == '0.90 (0.88\u20130.93)' and _pp2.repair_cell_text('3d') == '3d' and _pp2.repair_cell_text('ChatGPT4o') == 'ChatGPT4o' and _pp2.repair_cell_text('10\u00b3') == '10^3' and _pp2.repair_cell_text('(|24k)') == '(~24k)')
print('model procedure, offline (stages run with canned answers instead of model calls)')
import threading, re as _re, llm_batch as _L
_al = ['addressed', 'partial', 'not-addressed']
check('cascade rule: a confident rating stands; low goes to the fallback; low again is needs_human', S.cascade_result({'rating': 'partial', 'confidence': 'high'}, None, _al)[:2] == ('confident', 'partial') and S.cascade_result({'rating': 'partial', 'confidence': 'low'}, {'rating': 'addressed', 'confidence': 'medium'}, _al)[:2] == ('fallback', 'addressed') and S.cascade_result({'rating': 'partial', 'confidence': 'low'}, {'rating': 'addressed', 'confidence': 'low'}, _al)[:2] == ('needs_human', 'needs_human') and S.cascade_result({'rating': 'partial', 'confidence': 'low'}, {'rating': 'no answer', 'confidence': ''}, _al)[0] == 'needs_human')
check('a rating goes to the fallback when its confidence is low, missing or unreadable, or the value is not allowed', S.needs_fallback({'rating': 'partial', 'confidence': 'low'}, _al) and S.needs_fallback({'rating': 'partial', 'confidence': 'missing'}, _al) and S.needs_fallback({'rating': 'bogus', 'confidence': 'high'}, _al) and not S.needs_fallback({'rating': 'partial', 'confidence': 'medium'}, _al) and not S.needs_fallback({'rating': 'partial', 'confidence': 'high'}, _al))


class FakeM:
    """Just enough of the runner's Manifest for the stages."""
    def __init__(s, d, pdf): s.dir = d; s.lock = threading.Lock(); s.m = {'run_id': 'selftest-offline', 'stage_log': {}, 'spent_usd': 0.0, 'cap_usd': 5, 'question': 'q', 'papers': {'P1': {'pdf': str(pdf), 'preflight': {'page_map': [{'pdf': 1, 'printed': 1}]}, 'stages': {'picost': {}}}}}
    def event(s, *a): pass
    def save(s): pass


def ok_(rid, obj): return _L.Res(rid, True, json.dumps(obj), 100, 100, 'STOP')


def first_val(sg): return S.SIGNALS[sg][1].split('|')[0].strip()


def run_qs(rater_list, fallback, cascade, max_acc, answers):
    """Run stage_qs on a one-page PDF; `answers(request, stage) -> list of rating dicts` stands in for every model call. Returns (aggregate by signal, raw rows, requests seen by stage)."""
    seen = {}
    def fake(M, key, reqs, mode, cap_frac=1.0):
        seen.setdefault(key, []).extend(reqs); return {r.id: ok_(r.id, {'ratings': answers(r, key)}) for r in reqs}
    old = (S.dispatch, S.RATERS, S.QS_FALLBACK, S.QS_CASCADE, S.QS_MAX)
    S.dispatch, S.RATERS, S.QS_FALLBACK, S.QS_CASCADE, S.QS_MAX = fake, rater_list, fallback, cascade, max_acc
    try:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); d = fitz.open(); d.new_page().insert_text((72, 100), 'The study used Model A on one hundred items and reported good results.'); pdf = td / 'p.pdf'; d.save(str(pdf)); d.close()
            (td / 'P1').mkdir(); M = FakeM(td, pdf); S.stage_qs(M, 'batch'); q = json.loads((td / 'P1' / 'quality_signals.json').read_text())
        return {a['signal']: a for a in q['aggregate']}, q['raw'], seen
    finally: S.dispatch, S.RATERS, S.QS_FALLBACK, S.QS_CASCADE, S.QS_MAX = old


def rows_for(req, conf):
    return [{'signal': sg, 'rating': first_val(sg), 'page': 1, 'quote_start': 'The study used Model A', 'quote_end': 'reported good results', 'locator': 'Methods', 'confidence': conf(sg)} for sg in _re.findall(r'^- `(.+?)`:', req.system, _re.M)]


LOW1, LOW2 = 'baseline-adequacy', 'tripod-4'   # LOW1: Neon low, Sol medium -> the fallback decides; LOW2: Neon low, Sol low -> needs_human
def casc(req, key):
    if key == 'qs': return rows_for(req, lambda sg: 'low' if sg in (LOW1, LOW2) else 'high')
    return rows_for(req, lambda sg: 'low' if sg == LOW2 else 'medium')
agg, raw, seen = run_qs([('neon', 'gemini-4-neon', 'high')], [('sol', 'gpt-6.2-sol', 'high')], True, False, casc)
fbsg = {x for r in seen['qs_fallback'] for x in _re.findall(r'^- `(.+?)`:', r.system, _re.M)}
check('one rater with a fallback: only the two low-confidence rows go to the fallback rater (Sol, high), as one blind request per group; no Opus and no adjudicator', len(seen['qs']) == 2 and fbsg == {LOW1, LOW2} and all(r.model == 'gpt-6.2-sol' and r.effort == 'high' for r in seen['qs_fallback']) and 'qs_adjudicate' not in seen and all(r.model == 'gemini-4-neon' for r in seen['qs']))
check('cascade result: a confident row keeps the rater\'s rating, a medium fallback decides one row, a low fallback marks needs_human (shown as the final value)', agg['construct-validity']['status'] == 'confident' and agg[LOW1]['status'] == 'fallback' and agg[LOW1]['majority'] == first_val(LOW1) and agg[LOW2]['status'] == 'needs_human' and agg[LOW2]['majority'] == 'needs_human' and sum(1 for a in agg.values() if a['status'] == 'needs_human') == 1 and len(agg) == len(S.SIGNALS))
check('TRIPOD rows go through the same cascade, and the confidence is stored on every raw row', LOW2.startswith('tripod-') and all(x['confidence'] in ('high', 'medium', 'low') for x in raw))
import qs_export as _QE
check('the export names the status in plain words (needs your judgment, fallback decided)', 'Needs your judgment' in _QE.summary_sentence('needs_human', [x for x in raw if x['signal'] == LOW2], agg[LOW2], []) and 'fallback' in _QE.summary_sentence(agg[LOW1]['majority'], [x for x in raw if x['signal'] == LOW1], agg[LOW1], []))
def three(req, key):
    who = req.id.split('__qs-')[1].split('-')[0]; rows = rows_for(req, lambda sg: 'high')
    for x in rows:
        if who in ('opus', 'sol') and x['signal'] == 'baseline-adequacy': x['rating'] = 'partial'
        if who == 'sol' and x['signal'] == 'human-baseline': x['rating'] = 'not-addressed'
    return rows
agg3, raw3, seen3 = run_qs([('neon', 'gemini-4-neon', 'high'), ('opus', 'claude-opus-5-5', 'high'), ('sol', 'gpt-6.2-sol', 'high')], [('sol', 'gpt-6.2-sol', 'high')], False, True, three)
check('maximum-accuracy mode still works with three raters: Sol is read as a rater (it shares its key with the old adjudicator), two of three decide, no fallback or adjudicator runs', {x['rater'] for x in raw3} == {'neon', 'opus', 'sol'} and all(x['rating'] != 'no answer' for x in raw3) and agg3['baseline-adequacy']['majority'] == 'partial' and agg3['human-baseline']['majority'] == first_val('human-baseline') and agg3['construct-validity']['agreement'] == 'all raters agree' and 'qs_fallback' not in seen3 and 'qs_adjudicate' not in seen3)


BAD_CHANGES = False


def run_draft(authors, critics, voters, node_check, tiebreak, debate=True, dm_scores=None):
    """stage_draft on one finding with canned answers: returns (drafts.json content, requests by stage)."""
    seen = {}; stm = lambda r: r.id.split('__', 1)[1]
    node = lambda txt: {'id': 'E-F1', 'type': 'EVD', 'tier': 'primary', 'source_id': 'F1', 'answers_QUE': ['Q1'], 'statement': txt, 'quote': 'Model A scored 71.4%'}
    que = {'id': 'Q1', 'type': 'QUE', 'statement': 'How well does Model A do?', 'quote': 'x'}
    def fake(M, key, reqs, mode, cap_frac=1.0):
        seen.setdefault(key, []).extend(reqs); out = {}
        for r in reqs:
            s = stm(r)
            if key == 'draft_r0': o = {'nodes': [que]} if s == 'single' else {'nodes': [node(f'Model A scored 71.4% (n = 100), draft by {s[3:]}.')]}
            elif key == 'draft_r1': o = {'critiques': [], 'revised': {'nodes': [node(f'Model A scored 71.4% (n = 100), revised by {s[3:]}.')]}}
            elif key == 'draft_vote':
                blob = json.loads(r.text.split('Versions:\n', 1)[1].split('\n\nVote now.')[0]); me = s[5:]
                want = next((k for k, v in blob.items() if ('revised by neon' in v['nodes'][0]['statement']) == (me == 'neon')), 'A')
                o = {'picks': [{'node': 'E-F1', 'pick': want, 'reason': ''}]}
            elif key == 'draft_tie': o = {'picks': [{'node': 'E-F1', 'pick': 'neon', 'reason': ''}]}
            elif key == 'draft_check': o = {'checks': [{'node': n['id'], 'overall': 'pass'} for n in json.loads(r.text.split('Nodes to check:\n', 1)[1].split('\n\nCheck now.')[0])]}
            elif key == 'draft_rework': o = {'verdict': 'corrected', 'corrected_statement': 'Model A scored 71.4% (n = 100), run by sol.', 'changes': [{'old': 'draft', 'new': 'run', 'reason': 'test'}]} if not BAD_CHANGES else {'verdict': 'corrected', 'corrected_statement': 'Model A scored 71.4% (n = 100), run by sol.', 'changes': [{'old': 'nothing here', 'new': 'run', 'reason': 'test'}]}
            else: o = {}
            out[r.id] = ok_(r.id, o)
        return out
    saved = (S.dispatch, S.run_dm, S.AUTHORS, S.CRITICS, S.VOTERS, S.NODE_CHECK, S.R.get('tiebreak'), S.DEBATE); scores = list(dm_scores or [0.95])
    def fake_dm(state, questions):
        v = scores.pop(0) if len(scores) > 1 else scores[0]; return {'perplexity': {k: v for k in questions}, 'liquid': {k: v for k in questions}}
    S.dispatch = fake; S.run_dm = fake_dm; S.AUTHORS, S.CRITICS, S.VOTERS, S.NODE_CHECK = authors, critics, voters, node_check; S.DEBATE = debate
    if tiebreak: S.R['tiebreak'] = tiebreak
    try:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); d = fitz.open(); d.new_page().insert_text((72, 100), 'Model A scored 71.4% (n = 100).'); pdf = td / 'p.pdf'; d.save(str(pdf)); d.close(); (td / 'P1').mkdir()
            (td / 'P1' / 'picost.json').write_text(json.dumps({'paper': {}, 'questions': [{'id': 'Q1', 'reframed': 'How well does Model A do?'}], 'claims': [], 'caveats': [], 'findings': [{'id': 'F1', 'tier': 'primary', 'statement': 'Model A scored 71.4% (n = 100).', 'answers_QUE': ['Q1'], 'numbers': [{'value': '71.4', 'label': 'x'}, {'value': '100', 'label': 'n'}], 'spans': [{'text': 'Model A scored 71.4%'}]}]}))
            M = FakeM(td, pdf); S.stage_draft(M, 'batch'); dd = json.loads((td / 'P1' / 'drafts.json').read_text())
        return dd, seen
    finally:
        S.dispatch, S.run_dm, S.AUTHORS, S.CRITICS, S.VOTERS, S.NODE_CHECK, tb, S.DEBATE = saved
        if tb is None: S.R.pop('tiebreak', None)
        else: S.R['tiebreak'] = tb
sol_, neon_, sonnet_ = ('sol', 'gpt-6.2-sol', 'medium'), ('neon', 'gemini-4-neon', 'medium'), ('sonnet', 'claude-sonnet-5-5', 'medium')
dd, seen_d = run_draft([sol_], [neon_], [sol_, neon_], [neon_], 'claude-sonnet-5-5')
fin = dd['finals']['E-F1']
check('drafting with one author, one critic, two voters and a tiebreak: only Sol drafts, only Neon critiques, both vote, the split goes to the tiebreak model, Neon checks the details', sorted(r.id.split('__r0-')[1] for r in seen_d['draft_r0'] if '__r0-' in r.id) == ['sol'] and [r.id.split('__')[1] for r in seen_d['draft_r1']] == ['r1-neon'] and sorted(r.id.split('__')[1] for r in seen_d['draft_vote']) == ['vote-neon', 'vote-sol'] and [r.model for r in seen_d['draft_tie']] == ['claude-sonnet-5-5'] and [r.id.split('__')[1] for r in seen_d['draft_check']] == ['check-neon'])
check('the tiebreak winner is the critic\'s revision, the label names the tiebreak model, and a check of the checker\'s own text is marked as such', fin['author'] == 'neon' and fin['how'] == 'Sonnet 5.5 tie-break' and 'revised by neon' in fin['node']['statement'] and fin['detail_check']['own_draft'] is True and fin['status'].startswith('needs JP review'))
check('a node written by the first author (Sol) is checked by Neon without the own-draft mark', dd['finals']['Q1']['author'] == 'sol' and dd['finals']['Q1'].get('detail_check') is None)
dd2, seen2 = run_draft([sonnet_, sol_, neon_], [sonnet_, sol_, neon_], [sol_, sonnet_], [sol_, sonnet_], 'gemini-4-neon')
check('a multi-author configuration still works: three authors draft and revise, two voters vote, the checker is the first one that did not write the node', len([r for r in seen2['draft_r0'] if '__r0-' in r.id]) == 3 and len(seen2['draft_r1']) == 3 and len(seen2['draft_vote']) == 2 and 'E-F1' in dd2['finals'] and all(not v['detail_check'].get('own_draft') for v in dd2['finals'].values() if v.get('detail_check')))
dd1, seen1 = run_draft([sol_], [], [], [neon_], None, debate=False)
check('one author, no debate: only Sol drafts, no critique, vote or tiebreak request is made, the draft is final and Neon checks the details', sorted(seen1) == ['draft_check', 'draft_r0'] and dd1['finals']['E-F1']['author'] == 'sol' and dd1['finals']['E-F1']['how'].startswith('single author draft') and dd1['finals']['E-F1']['detail_check']['checker'] == 'neon' and not dd1['finals']['E-F1']['detail_check']['own_draft'] and dd1['finals']['E-F1']['status'] == 'pass')
dd1b, _ = run_draft([sol_], [], [], [sol_], None, debate=False)
check('a node-detail check by the model that wrote the node is marked and flagged for JP', dd1b['finals']['E-F1']['detail_check']['own_draft'] is True and dd1b['finals']['E-F1']['status'].startswith('needs JP review'))
dd1c, seen1c = run_draft([sol_], [], [], [neon_], None, debate=False, dm_scores=[0.3, 0.95])
rw = dd1c['finals']['E-F1']['rework']
check('EVD fix: a low decision-model score sends the EVD to the fix model (Neon, medium) with the evd-fix prompt; the listed changes reproduce the corrected statement, which is accepted', [r.model for r in seen1c['draft_rework']] == ['gemini-4-neon'] and seen1c['draft_rework'][0].effort == 'medium' and rw['verdict'] == 'rewrite' and rw['changes'][0]['old'] == 'draft' and rw['changes_reproduce_rewrite'] is True and rw['accepted'] is True and dd1c['finals']['E-F1']['node']['statement'].endswith('run by sol.'))
BAD_CHANGES = True
dd1d, _ = run_draft([sol_], [], [], [neon_], None, debate=False, dm_scores=[0.3, 0.95]); BAD_CHANGES = False
check('a correction whose listed changes do not reproduce it is not applied', dd1d['finals']['E-F1']['rework']['accepted'] is False and 'draft by sol' in dd1d['finals']['E-F1']['node']['statement'])
check('apply_changes applies old -> new in order and returns None when an old text is missing', S.apply_changes('a b c', [{'old': 'b', 'new': 'x'}]) == 'a x c' and S.apply_changes('a b c', [{'old': 'z', 'new': 'x'}]) is None)
import lives_verify as _VV
mk = lambda ntype, nid: {'ntype': ntype, 'nid': nid}
_types = [mk('PICOST', 'F1: Population'), mk('QUOTE', 'F1 quote 1'), mk('QUE', 'Q1'), mk('CLM', 'C1'), mk('CLM', 'C1 quote'), mk('CVT', 'V1'), mk('QUALITY', 'study-type (neon)'), mk('QUALITY', 'study-type (sol)'), mk('QUALITY', 'tripod-4 (neon)')]
check('for every item type the judge is not the model that produced the item (Neon items to Sol, Sol fallback ratings to Neon, Neon ratings to Sol)', all(_VV.judge_for(x)[0] != _VV.producer_model(x) for x in _types) and _VV.judge_for(mk('QUALITY', 'study-type (sol)'))[0] == 'gemini-4-neon' and _VV.judge_for(mk('QUALITY', 'study-type (neon)'))[0] == 'gpt-6.2-sol' and _VV.judge_for(mk('PICOST', 'F1: Population'))[0] == 'gpt-6.2-sol' and C.role_model(C.ROLES['quote_check']) != C.ROLES['extract'])
_VV.check_judge()
_h = _VV.human_flag
check('flag for human examination: judge below 0.75 or silent; a decision model below 0.5 with no judge pass (bison-1 counts); judge against the decision-model majority; a clean item is not flagged', 'scored it 0.5' in _h({'scores': {'sonnet': 0.5, 'perplexity': 0.9, 'liquid': 0.2}, 'sonnet_called': True}) and _h({'scores': {'sonnet': None, 'perplexity': 0.9, 'liquid': 0.2}, 'sonnet_called': True}).startswith('the judge gave no answer') and _h({'scores': {'perplexity': 0.9, 'liquid': 0.9}, 'sonnet_called': False, 'shadow_bison': 0.1}).startswith('bison-1 scored') and _h({'scores': {'sonnet': 1.0, 'perplexity': 0.1, 'liquid': 0.2}, 'sonnet_called': True}) == 'the judge and the decision-model majority disagree' and _h({'scores': {'sonnet': 1.0, 'perplexity': 0.2, 'liquid': 0.9}, 'sonnet_called': True}) == '' and _h({'scores': {'perplexity': 0.9, 'liquid': 0.9}, 'sonnet_called': False}) == '' and _h({'scores': {'perplexity': 0.2, 'liquid': 0.1}, 'sonnet_called': False}) != '')
_q = [{'paper': 'p', 'ntype': 'CLM', 'nid': f'C{i}', 'majority': 'pass', 'mean': 0.9, 'scores': {'perplexity': 0.9, 'liquid': 0.9}} for i in range(3)]; _q[2]['scores'] = {'perplexity': 0.1, 'liquid': 0.9, 'sonnet': 0.5}; _q[2]['sonnet_called'] = True
check('flagged items come first inside their node type in the labeling queue, and the type order is kept', [x['nid'] for x in _VV.queue_order(_q)][0] == 'C2' and all(x['queue'] == '1 CLM' for x in _q))
import estimate_cost as _EC
check('the cost estimate re-prices a call at the new model\'s batch price (Sonnet 5.5: 2 in, 10 out, half in batch)', abs(_EC.cost('claude-sonnet-5-5', 1_000_000, 1_000_000) - 6.0) < 1e-9)
print('SRC writer (write_src.py): checks on a model page, canned output, no call')
import write_src as _WS
check('roles.src_writer is Sol at medium effort, the prompt src-write-v1 exists, and the stage runs in batch mode only', C.role_model(C.ROLES['src_writer']) == 'gpt-6.2-sol' and C.role_effort(C.ROLES['src_writer']) == 'medium' and (V / 'pipeline/prompts/src-write-v3.md').exists() and (V / 'pipeline/prompts/src-judge-v1.md').exists() and 'src_write' not in C.PIPE['limits']['standard_stages'])
sys.path.insert(0, str(here / 'tests')); import test_write_src as _TWS
_n, _bad = _TWS.run()
check(f'write_src tests ({_n} checks): a planted wrong number, an unlocated quote, a wrong table cell, an unknown node id, a missing screenshot placeholder and an em dash are all flagged; a good page has no flag', _bad == 0 and _n >= 45)
print('decision-model triad and no-cut-off ladder (JP, 2026-11-27)')
import decision_models as _DM3, llm_batch as _LB
check('three voting decision models: roles.decision_models is Perplexity, Liquid, Baseten bison-1, each with a model id, a key variable and a registry entry', C.ROLES['decision_models'] == ['perplexity', 'liquid', 'baseten'] and all(k in _DM3.MODELS and k in _DM3.KEY_ENV for k in C.ROLES['decision_models']) and _DM3.MODELS['baseten'] in C.MODELS and C.display(_DM3.MODELS['baseten']) == 'Baseten bison-1' and _DM3.TEXT_ONLY == {'perplexity', 'baseten'})
check('Liquid prefers d1.3-ultra and keeps d1.2-ultra until the API accepts it; the registry has both', _DM3.PREFERRED['liquid'][:2] == ['d1.3-ultra', 'd1.2-ultra'] and 'd1.3-ultra' in C.MODELS and 'd1.2-ultra' in C.MODELS)
_j = VV.judge_needed
check('cascade rule for three models: the judge is called unless every voting decision model gave a score and all are on the same side of 0.5 (all pass or all fail); one missing score or any split calls the judge',
      _j({'perplexity': .9, 'liquid': .8, 'baseten': .7}) is False and _j({'perplexity': .1, 'liquid': .2, 'baseten': .3}) is False and _j({'perplexity': .9, 'liquid': .8, 'baseten': .2}) is True and _j({'perplexity': .1, 'liquid': .8, 'baseten': .9}) is True and _j({'perplexity': .9, 'liquid': .9, 'baseten': None}) is True and _j({'perplexity': .5, 'liquid': .9, 'baseten': .9}) is False and _j({'perplexity': .9, 'liquid': .9}) is True and _j({'perplexity': .9, 'liquid': .9}, models=['perplexity', 'liquid']) is False)
check('abstention: a text-only model left out of `models` (an item scored from a screenshot) does not vote and does not call the judge', _j({'perplexity': .9, 'liquid': .9, 'baseten': None}, models=['perplexity', 'liquid']) is False)
_hf = VV.human_flag
check('human flag with three models: bison-1 below 0.5 flags the item unless the judge passed it; the judge against a 2-of-3 majority flags it; a unanimous clean item is not flagged; older runs (shadow_bison) still read',
      _hf({'scores': {'sonnet': None, 'perplexity': .9, 'liquid': .9, 'baseten': .1}, 'sonnet_called': False}).startswith('bison-1 scored') and _hf({'scores': {'sonnet': 1.0, 'perplexity': .9, 'liquid': .9, 'baseten': .1}, 'sonnet_called': True}) == '' and _hf({'scores': {'sonnet': 0.0, 'perplexity': .9, 'liquid': .9, 'baseten': .1}, 'sonnet_called': True}) != '' and _hf({'scores': {'sonnet': 1.0, 'perplexity': .1, 'liquid': .2, 'baseten': .9}, 'sonnet_called': True}) == 'the judge and the decision-model majority disagree' and _hf({'scores': {'perplexity': .9, 'liquid': .9, 'baseten': .9}, 'sonnet_called': False}) == '' and _hf({'scores': {'perplexity': .9, 'liquid': .9}, 'sonnet_called': False, 'shadow_bison': .1}).startswith('bison-1 scored'))
_rv = {'scores': {'sonnet': None, 'perplexity': .9, 'liquid': .8, 'baseten': .2}}; VV.revote(_rv)
check('the vote counts bison-1: two pass and one fail gives a pass majority with 2 models agreeing, and the mean covers all three scores', _rv['majority'] == 'pass' and _rv['agree'] == 2 and abs(_rv['mean'] - 0.633) < 0.001)
import json as _json
_qsrc = (here / 'qs_export.py').read_text(encoding='utf-8')
check('qs_export keeps the verifier scores as separate numbers (judge, judge model, Perplexity, Liquid, bison-1), not one joined cell', "'verifier_scores'" in _qsrc and all(k in _qsrc for k in ("'judge_model'", "'baseten'", "'perplexity'", "'liquid'")))
class _FM:   # a stand-in manifest for the ladder tests
    def __init__(self): self.m = {'stage_log': {}, 'papers': {'p': {}}}; self.events = []
    def event(self, t): self.events.append(t)
    def save(self): pass
def _res(i, fin, ok=False): return _LB.Res(i, ok, 'x' if ok else '', 10, 20, fin, '' if ok else f'finishReason {fin}')
def _ladder(first_fin, answers, key='picost', mode='batch', effort='high'):
    calls = []; M_ = _FM(); rq = [_LB.Req('p__picost', 'gemini-4-neon', 't', effort=effort, max_tokens=1000)]
    def runner(k, rs, md): calls.append((k, md, rs[0].effort, rs[0].max_tokens)); a = answers[len(calls) - 1]; return {rs[0].id: _res(rs[0].id, a, ok=(a == 'STOP'))}
    out = S.cutoff_ladder(M_, key, rq, {'p__picost': _res('p__picost', first_fin)}, mode, runner); return out['p__picost'], calls, M_
x_, c_, m_ = _ladder('MAX_TOKENS', ['STOP'])
check('ladder, cut off then success at medium: one retry in batch mode at medium effort with the largest batch budget (65000 for Neon); the result is ok and the retry is logged in the manifest', x_.ok and c_ == [('picost_cut1', 'batch', 'medium', 65000)] and m_.m['cutoff_retries'][0]['rung'] == 1 and m_.m['cutoff_retries'][0]['result'] == 'done' and not m_.m.get('needs_jp') and m_.m['stage_log']['picost']['cutoff_retried'] == 1)
x_, c_, m_ = _ladder('CONTINUATION', ['MAX_TOKENS', 'STOP'])
check('ladder, cut off twice then success in standard: rung 2 runs in standard mode with the largest standard budget (65536 for Neon) and the manifest marks both retries', x_.ok and c_ == [('picost_cut1', 'batch', 'medium', 65000), ('picost_cut2', 'standard', 'medium', 65536)] and [e['rung'] for e in m_.m['cutoff_retries']] == [1, 2] and m_.m['cutoff_retries'][1]['mode'] == 'standard' and m_.m['cutoff_retries'][0]['result'] == 'cut off again')
x_, c_, m_ = _ladder('MAX_TOKENS', ['MAX_TOKENS', 'CONTINUATION'])
check('ladder, never succeeds: the result is marked needs JP (err starts with "needs JP"), listed in manifest needs_jp, after exactly two retries; nothing is dropped', (not x_.ok) and x_.err.startswith('needs JP') and len(c_) == 2 and m_.m['needs_jp'][0]['id'] == 'p__picost' and m_.m['cutoff_retries'][-1]['result'] == 'needs JP')
x_, c_, m_ = _ladder('STOP', [])
check('ladder: a finished request is left alone and nothing is sent again', c_ == [] and not m_.m.get('cutoff_retries'))
x_, c_, m_ = _ladder('MAX_TOKENS', ['STOP'], key='quote_check', mode='batch')
check('ladder in a stage that always runs in standard mode retries in standard mode', c_[0][1] == 'standard' and S.is_cut(_res('i', 'max_tokens')) and S.is_cut(_res('i', 'incomplete')) and S.is_cut(_res('i', 'length')) and not S.is_cut(_res('i', 'STOP', ok=True)) and not S.is_cut(_res('i', 'end_turn', ok=True)))
x_, c_, m_ = _ladder('MAX_TOKENS', ['STOP'], effort='medium')
check('ladder: a request already at medium effort goes to low on the retry (nothing higher to step down from)', c_[0][2] == 'low')
_mf = _FM(); _mf.m['papers'] = {'a': {'failed': 'needs JP: picost output cut off', 'needs_jp': True}, 'b': {'failed': 'picost: bad json'}, 'c': {}}
check("a paper stopped with status needs JP is not counted by the 'two or more papers failed' stop; a real failure is", R.failed_papers(_mf) == ['b'])
_sg = (here / 'lives_stages.py').read_text(encoding='utf-8'); _lr = (here / 'lives_run.py').read_text(encoding='utf-8')
check('every LLM stage goes through the ladder: S.dispatch (checks, drafts, qs, src, verify) and lives_run.run_stage (picost, recheck, adjudicate) both call cutoff_ladder', 'res = cutoff_ladder(M, key, reqs, res, mode)' in _sg and 'S.cutoff_ladder(M, stage, reqs, first, mode)' in _lr)
check('budgets are the model limits: picost 65000 (Gemini batch), recheck and adjudicate at the limit of their models, none above the model limit; Gemini standard allows 65536', R.STAGE_MAX_OUT['picost'] == 65000 and all(R.STAGE_MAX_OUT[k] <= C.max_output(C.role_model(R.STAGE_MODEL[k])) for k in R.STAGE_MAX_OUT) and C.max_output('gemini-4-neon', batch=False) == 65536 and C.PIPE['no_cutoff']['largest_seed_pdf']['pages'] == 60 and R.max_out('picost', 60) == 65000)
print('packages')
for pkg in ('pymupdf', 'anthropic', 'openai', 'openpyxl', 'pillow', 'requests'):
    try: print(f'  {pkg} {md.version(pkg)}'); ok += 1
    except Exception: fails.append(f'package {pkg}'); print(f'  FAIL  package {pkg} is not installed')
print(f'\n{ok} passed, {len(fails)} failed'); sys.exit(1 if fails else 0)

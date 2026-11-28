#!/usr/bin/env python3
"""Stages after extraction for lives_run.py (JP, 2026-11-25): checks, drafting by debate, quality-signal rating.

  checks   two decision models (Perplexity Decider 1.3 and Liquid d1-ultra) score every extracted finding on relevancy, fidelity, numbers found in the source and (for
           tables and figures) table-cell match; GPT-6.2 Sol looks at the crop of every finding (pass, fail or cannot verify); only disagreements go to Claude Opus 5.5.
  draft    EVD, QUE, CLM and CVT nodes. Primary EVDs: the authors (roles.authors) draft, the critics (roles.critics) critique and revise, the voters (roles.voters) choose
           and roles.tiebreak settles a split; everything else is one draft by the first author. Every node gets the writing-rules check; EVD, CLM and CVT get the node-detail
           check by roles.node_check (a model that did not write the node when there is a choice); EVDs also get a decision-model check. Models: pipeline/config/models.json.
  qs       quality signals and TRIPOD-LLM rows: one rater (roles.raters) reports a rating and a confidence; low confidence goes to the fallback rater (roles.qs_fallback); low
           confidence again marks the row needs_human for JP. With three raters in roles.raters (quality_signals.max_accuracy) a rating needs two of three. Everything is saved for the sheets.
Nothing here writes to the vault. Outputs go to pipeline/runs/<run>/<paper>/ and the review sheet."""
import collections, concurrent.futures as cf, hashlib, json, os, random, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import call_logger as cl, llm_batch as L, pdf_pages as pp, decision_models as dm, config as C
import fitz
dm.load_env(); cl.load_env()

VAULT = cl.VAULT; R = C.ROLES; CK = C.PIPE['checks']
AUTHORS = C.role_list('authors')        # who drafts first (pipeline/config/models.json, roles); one author or several
CRITICS = C.role_list('critics', 'authors')   # critique round (only with several authors; JP, 2026-11-27: one author, no critique, vote or tiebreak); the authors themselves when the role is missing
VOTERS = C.role_list('voters')          # who decides between the versions (only with several authors); the tiebreak role settles a split
DEBATE = len(AUTHORS) > 1 and len(VOTERS) >= 1   # False: the one author's draft is final (no critique round, no vote, no tiebreak)
NODE_CHECK = C.role_list('node_check', 'voters') or AUTHORS   # who checks the details of the winning nodes; a model that did not write the node is preferred
RATERS = C.role_list('raters')          # who rates quality signals: one rater with a fallback rater for low-confidence ratings (JP, 2026-11-27); with three raters a rating needs two of three and no adjudicator runs; with two raters a third model decides the disagreements (older runs)
QS_FALLBACK = [(R['qs_fallback']['key'], R['qs_fallback']['model'], R['qs_fallback'].get('effort', 'high'))] if isinstance(R.get('qs_fallback'), dict) else []   # [] when the role is missing
QS_MAX = bool(C.PIPE.get('quality_signals', {}).get('max_accuracy'))   # JP, 2026-11-27: true = maximum accuracy (three raters, every verifier judges every rating)
QS_CASCADE = len(RATERS) == 1 and bool(QS_FALLBACK) and not QS_MAX      # one rater; low confidence goes to the fallback rater; low again goes to JP
QS_ADJ = R['qs_adjudicator']
QC_MODEL = C.role_model(R['quote_check']); QC_EFFORT = C.role_effort(R['quote_check'], 'low')   # reads the screenshot of each quote
short_name = C.short   # 'Sol', 'Neon', 'Sonnet 5.5'
DM_LOW = CK['dm_low']; DM_SPREAD = CK['dm_spread']; SAMPLE = CK['sample']    # first guesses; calibrate on JP's labels (pipeline/config/pipeline.json)
MAX_FINDINGS_DRAFT = 99
EXPECT = 0.7        # expected share of an output budget that is used


class Halt(Exception): pass


ex = lambda p: str(Path(p).expanduser())
def norm_num(v):
    s = str(v).replace('−', '-').replace(',', '').replace('%', '').replace(' ', '').lower(); m = re.search(r'-?\d*\.?\d+', s); return m.group(0).lstrip('0') or '0' if m else s
def prompt(name): return (VAULT / 'pipeline/prompts' / name).read_text(encoding='utf-8')
def now(): return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())


# ---------------------------------------------------------------- generic dispatch (cap check, upload, standard or batch, cost, call log)
def est_tokens(r):
    per = {'google': 1400, 'openai': 1400, 'anthropic': 2800}.get(L.provider_of(r.model), 1400)
    pages = fitz.open(r.pdf).page_count if r.pdf else 0
    return (len(r.system) + len(r.text)) / 3.5 + per * pages + 1500 * len(r.images or [])


STANDARD_STAGES = set(C.PIPE['limits'].get('standard_stages', []))   # small stages that run in standard mode even in a batch run (a batch's slowest request would hold the run up)


STRAGGLER_MIN_REQUESTS = 8   # the 5-minute straggler rule applies only to stages of 8 or more requests (JP, 2026-11-26: the test lost Neon's ratings when it cancelled 1 of 2)


def wait_jobs(M, jobs):
    """Wait for batch jobs. Once all but about 10% of their requests are finished, the rest get STRAGGLER_MIN more minutes; then the jobs are cancelled, what finished is kept and the missing requests go to human review. Returns True if stragglers were cancelled."""
    grace = L.STRAGGLER_MIN * 60; t90 = None
    while True:
        if not any(L.poll_batch(j) == 'running' for j in jobs): return any(j.get('straggler') for j in jobs)
        if (M.dir / 'STOP').exists():
            for j in jobs: L.cancel_batch(j)
            raise Halt('STOP file present: batch jobs cancelled')
        prog = [x for x in (L.batch_progress(j) for j in jobs if j['provider'] != 'tinker') if x]
        if prog:
            done = sum(x[0] for x in prog); tot = sum(x[1] for x in prog)
            if tot >= STRAGGLER_MIN_REQUESTS and 0 < done < tot and done >= tot - L._tail_count(tot) and t90 is None:   # with fewer requests than this, a slow one is waited for: cancelling it would lose a whole rater   # needs at least one finished, so a lone slow request is not cut off
                 t90 = time.time(); M.event(f'{done} of {tot} requests finished; the rest get {L.STRAGGLER_MIN} more minutes')
        if t90 and time.time() - t90 >= grace:
            M.event(f'stragglers after {L.STRAGGLER_MIN} minutes: cancelling the batch; finished results are kept and the rest go to human review')
            for j in jobs:
                if L.poll_batch(j) == 'running': j['straggler'] = True; L.cancel_batch(j)
            deadline = time.time() + 600
            while any(L.poll_batch(j) == 'running' for j in jobs) and time.time() < deadline: time.sleep(15)
            return True
        time.sleep(20)


def dispatch(M, key, reqs, mode, cap_frac=1.0):
    """Times the stage (JP, 2026-11-27: time on task per step): stage_log[key]['elapsed_s'] is the wall-clock seconds, batch queue wait included, and 'requests' the number of requests."""
    t0 = time.time(); res = _dispatch(M, key, reqs, mode, cap_frac)
    st = M.m['stage_log'].setdefault(key, {})
    if reqs and 'elapsed_s' not in st: st['elapsed_s'] = round(time.time() - t0, 1); st['requests'] = len(reqs); st['mode_used'] = 'standard' if key in STANDARD_STAGES else mode
    return res


def _dispatch(M, key, reqs, mode, cap_frac=1.0):
    """Run requests (any mix of models) as one stage. Returns {request id: Res}. Resumable: results are saved to <run>/stage_<key>.json."""
    f = M.dir / f'stage_{key}.json'; st = M.m['stage_log'].setdefault(key, {})
    if f.exists(): return {k: L.Res(**v) for k, v in json.loads(f.read_text()).items()}
    if not reqs: return {}
    if key in STANDARD_STAGES: mode = 'standard'
    batch = mode == 'batch'; worst = sum(L.cost(r.model, est_tokens(r), r.max_tokens, batch) for r in reqs)
    if 'jobs' not in st:
        if (M.dir / 'STOP').exists(): raise Halt('STOP file present')
        if M.m['spent_usd'] + worst > M.m['cap_usd']: raise Halt(f"stage {key}: spent ${M.m['spent_usd']:.2f} + worst case ${worst:.2f} would pass the ${M.m['cap_usd']:.2f} cap; nothing was submitted")
        up = L.upload_pdfs(reqs, M.gem_files) if hasattr(M, 'gem_files') else []
        if up: M.m.setdefault('gemini_files', []).extend(up)
        st.update(requests=len(reqs), est_worst_usd=round(worst, 3), mode=mode, started=now()); M.event(f"stage {key}: {len(reqs)} request(s), {mode}; worst case ${worst:.2f}; spent so far ${M.m['spent_usd']:.2f} of ${M.m['cap_usd']:.2f}")
        if batch:
            jobs = {}
            for model in sorted({r.model for r in reqs}): jobs[model] = L.submit_batch([r for r in reqs if r.model == model])
            st['jobs'] = jobs; M.save()
        else:
            res = L.run_standard(reqs, workers=6); st['jobs'] = {'standard': True}; f.write_text(json.dumps({k: vars(v) for k, v in res.items()}), encoding='utf-8')
    if not f.exists():
        jobs = st['jobs']; strag = wait_jobs(M, list(jobs.values()))
        if not strag and any(L.poll_batch(j) == 'failed' for j in jobs.values()): raise Halt(f'stage {key}: a batch job failed or expired')
        res = {}
        for j in jobs.values(): res.update(L.fetch_batch(j))
        f.write_text(json.dumps({k: vars(v) for k, v in res.items()}), encoding='utf-8')
    res = {k: L.Res(**v) for k, v in json.loads(f.read_text()).items()}; actual = 0.0
    for r in reqs:
        x = res.get(r.id) or L.Res(r.id, False, err='missing'); c = L.cost(r.model, x.tin, x.tout, batch); actual += c
        cl.record(M.m['run_id'], key, r.model, st.get('prompt', 'pipeline/prompts/draft-nodes-v4.md'), provider=L.provider_of(r.model), citekey=r.id.split('__')[0], effort=r.effort, tokens_in=x.tin, tokens_out=x.tout, output_text=x.text or None, notes=f'mode={mode}; cost_usd={c:.4f}; finish={x.finish}; err={x.err}')
    with M.lock: M.m['spent_usd'] = round(M.m['spent_usd'] + actual, 4); st.update(status='done', actual_usd=round(actual, 4), ended=now()); M.save()
    M.event(f"stage {key}: done, actual ${actual:.3f} (worst case ${worst:.2f}); total spent ${M.m['spent_usd']:.2f} of ${M.m['cap_usd']:.2f}")
    if M.m['spent_usd'] > M.m['cap_usd']: raise Halt('spend passed the cap')
    return res


def parse_json(text):
    t = (text or '').strip(); t = re.sub(r'^```(?:json)?|```$', '', t, flags=re.M).strip(); i, j = t.find('{'), t.rfind('}')
    return json.loads(t[i:j + 1])


def safe_json(x):
    try:
        if not x.ok: return None
        return parse_json(x.text)
    except Exception: return None


# ---------------------------------------------------------------- inputs
def final_findings(M, ck):
    """Findings after the recheck and adjudication: Opus's 'B' verdict takes Sol's reading; 'unsure' or 'neither' is marked for JP."""
    p = M.m['papers'][ck]; ps = json.loads((M.dir / ck / 'picost.json').read_text()); rc = {f['id']: f for f in (p.get('recheck') or {}).get('findings', [])}
    adj = {a['id']: a for a in (p.get('adjudication') or {}).get('adjudications', [])}; out = []
    for f in ps.get('findings', []):
        f = dict(f); a = adj.get(f['id'])
        if a and a.get('verdict') == 'B' and f['id'] in rc:
            for k in ('P', 'I', 'C', 'O', 'S', 'T', 'statement', 'numbers', 'spans'):
                if rc[f['id']].get(k): f[k] = rc[f['id']][k]
            f['corrected_by'] = 'Sol (Opus verdict B)'
        if a and a.get('verdict') in ('unsure', 'neither'): f['needs_jp'] = True
        out.append(f)
    return out, ps


def card_text(M, ck, part='all'):
    """The extraction card for drafting. part='primary': only the primary findings (these get the three-author debate). part='rest': everything else (secondary and tertiary findings, questions, claims, caveats), drafted once by one model. No caps on any of them (JP, 2026-11-25)."""
    fs, ps = final_findings(M, ck); keep = [f for f in fs if (f.get('tier') == 'primary') == (part == 'primary')] if part != 'all' else fs
    card = {'project_question_for_context_only_never_write_a_node_for_it': M.m.get('question', ''), 'paper': ps.get('paper'), 'findings': [{k: f.get(k) for k in ('id', 'tier', 'answers_QUE', 'supports', 'section', 'statement', 'P', 'I', 'C', 'O', 'S', 'T', 'numbers', 'spans', 'notes')} for f in keep]}
    if part != 'primary': card.update({'caveats': ps.get('caveats', []), 'claims': ps.get('claims', []), 'questions': ps.get('questions', [])})
    if part == 'rest': card['primary_finding_ids_already_drafted_elsewhere'] = [f['id'] for f in fs if f.get('tier') == 'primary']
    return json.dumps(card, ensure_ascii=False)


# ---------------------------------------------------------------- writing-rules check
def writing_rules(node, card_nums):
    """The writing-rules check (called lint until 2026-11-26): free and deterministic. EVD at most 247 characters, every number in the statement is on the card, parentheses, capitals; no reading-grade limit since JP's decision on 2026-11-26; QUE ends with a question mark; the others have a quote."""
    out = {}; t = node.get('type'); txt = node.get('statement') or node.get('title') or node.get('limitation') or ''
    out['chars'] = len(txt)
    if t == 'EVD':
        out['length_ok'] = len(txt) <= 247; nums = {norm_num(x) for x in re.findall(r'-?\d*\.?\d+', txt.replace(',', ''))}; out['numbers_not_on_card'] = sorted(n for n in nums if n not in card_nums)
        out['parentheses_ok'] = txt.count('(') <= 2 and txt.count(')') == txt.count('(') and '[' not in txt and ']' not in txt   # JP, 2026-11-26: one or two sets of parentheses in an EVD, no brackets
        allowed = set(C.PIPE.get('writing', {}).get('caps_allowed', []))
        out['caps_words'] = sorted({w for w in re.findall(r'\b[A-Z][A-Z_]{3,}\b', txt) if w not in allowed}); out['caps_ok'] = not out['caps_words']   # JP, 2026-11-26: no all-caps words (ACCURATE); tool, model and metric names are allowed
    if t == 'QUE': out['question_ok'] = txt.strip().endswith('?')
    if t in ('CLM', 'CVT', 'EVD'): out['has_quote'] = bool((node.get('quote') or '').strip())
    if t == 'EVD' and node.get('tier') == 'primary': out['links_to_question'] = bool(node.get('answers_QUE'))
    out['no_emdash'] = '\u2014' not in ' '.join(str(v) for v in node.values() if isinstance(v, str))   # JP's writing rule: no em dashes in written text
    out['pass'] = all([out['no_emdash'], out.get('length_ok', True), not out.get('numbers_not_on_card'), out.get('parentheses_ok', True), out.get('caps_ok', True), out.get('question_ok', True), out.get('has_quote', True), out.get('links_to_question', True)]); return out


def card_numbers(M, ck):
    fs, _ = final_findings(M, ck); s = set()
    for f in fs:
        for n in f.get('numbers', []): s.add(norm_num(n.get('value')))
        s |= {norm_num(x) for x in re.findall(r'-?\d*\.?\d+', ' '.join([str(f.get('statement', ''))] + [str(x.get('text', '')) for x in f.get('spans', [])]).replace(',', ''))}
    return s


# ---------------------------------------------------------------- stage: checks (decision models, Sol vision, Opus on disputes)
def dm_state(M, f, qs=None):
    qtext = ' | '.join(f"{q['id']}: {q.get('reframed') or q.get('original_wording', '')}" for q in (qs or []) if q.get('id') in (f.get('answers_QUE') or []))
    nums = '; '.join(f"{n.get('label', '')} = {n.get('value', '')}{n.get('unit', '')} ({n.get('table_or_figure', '')}, row {n.get('row', '')}, column {n.get('column', '')}, printed page {n.get('printed_page', '')})" for n in f.get('numbers', []))
    spans = ' | '.join(x.get('text', '') for x in f.get('spans', []))
    return f"Question(s) this finding answers: {qtext or M.m.get('question', '') or 'not given'}\nFinding ({f.get('tier', '')}): {f.get('statement', '')}\nPICOST: P={f.get('P', '')}; I={f.get('I', '')}; C={f.get('C', '')}; O={f.get('O', '')}; S={f.get('S', '')}; T={f.get('T', '')}\nNumbers: {nums}\nSource span(s): {spans}"


def dm_questions(M, text_kind='finding', table=True):
    q = {'relevancy': dm.noul('Does this finding directly answer one of the questions listed, or help interpret an answer to it?'),
            'fidelity': dm.noul(f'Does the {text_kind} say exactly what the numbers and source span support, with no added or changed number, model, comparator, direction or claim?'),
            'numbers_in_source': dm.noul('Is every number in the finding found either in the source span or in the Numbers list (with its table or figure location), and attributed to the right model or condition?'),
            'table_cell_matches': dm.noul('Does the table or figure cell named in the numbers (row and column) show the stated values?')}
    if not table: q.pop('table_cell_matches')   # a finding stated in prose has no table or figure to ground against (the first smoke test scored such findings about 0.47 and sent every one to Sol)
    return q


def rests_on_table(f): return any(re.search(r'table|fig', str(n.get('table_or_figure', '')), re.I) for n in f.get('numbers', []))


def run_dm(state, questions):
    out = {}
    for pv in R['decision_models']:
        r, e = dm.decide(pv, state, questions)
        out[pv] = {k: v.get('noul') for k, v in (r or {}).get('answers', {}).items()} if r else {'error': e}
        out[pv]['_tokens'] = (r or {}).get('usage', {}).get('input_tokens', 0)
    return out


def dm_summary(res):
    """Per question: mean probability over the models that answered; overall score = the lowest question mean; spread = the largest disagreement between models."""
    qs = [k for k in next(iter(res.values())) if not k.startswith('_') and k != 'error'] if res else []; means = {}; spread = 0.0
    for q in qs:
        v = [res[p][q] for p in res if isinstance(res[p].get(q), (int, float))]
        if v: means[q] = round(sum(v) / len(v), 3); spread = max(spread, max(v) - min(v))
    return {'means': means, 'score': min(means.values()) if means else 0.0, 'spread': round(spread, 3)}


def make_crop(M, ck, f):
    p = M.m['papers'][ck]; regs = {}
    for s in f.get('spans', []):
        if s.get('bbox') and s.get('pages_found'): regs.setdefault(s['pages_found'][0], []).extend(s['bbox'])
    if not regs: return None
    out = M.dir / ck / 'crops'; out.mkdir(parents=True, exist_ok=True); path = out / f"{f['id']}.png"
    try: r = pp.merge_regions(ex(p['pdf']), sorted(regs.items()), str(path), dpi=150); return str(path) if r.get('ok') else None
    except Exception: return None


RW_PROMPT = 'evd-fix-v1.md'
RW_MODEL = C.role_model(R['evd_rework']); RW_EFFORT = R.get('evd_rework_effort') or C.role_effort(R['evd_rework'], 'medium')
QS = {}   # the paper's own questions, by paper, for the relevancy check


def stage_quote_check(M, mode):
    """JP, 2026-11-26: every extracted quote (span) is shown to the quote-check model (roles.quote_check, Gemini 4 Neon since 2026-11-27; Claude Sonnet 5.5 before) as a screenshot with the quote highlighted, together with the model's quote (A) and the PDF text layer's text (B). The model transcribes what is printed and says whether each text equals the print and whether A's differences change the meaning. A quote whose differences change the meaning flags its finding (`quote_differs_from_print`), so Sol re-reads it. Decision models cannot do this check: they are text-only and cannot read the page image. Scope: all spans (config limits.quote_check_scope: 'all' or 'differing')."""
    st = M.m['stage_log'].setdefault('quote_check', {})
    if st.get('status') == 'done': return
    scope = C.PIPE['limits'].get('quote_check_scope', 'all'); sysq = prompt('quote-check-v1.md'); reqs = []; meta = {}; st['prompt'] = 'pipeline/prompts/quote-check-v1.md'
    for ck, p in M.m['papers'].items():
        f_ = M.dir / ck / 'picost.json'
        if p.get('failed') or not f_.exists(): continue
        ps = json.loads(f_.read_text(encoding='utf-8')); pdf = ex(p['pdf']); out = M.dir / ck / 'quote_crops'; out.mkdir(exist_ok=True)
        for f in ps.get('findings', []):
            for k, s in enumerate(f.get('spans', []), 1):
                if s.get('from_supplement') or s.get('match') not in ('exact', 'letters_digits', 'repaired') or (scope == 'differing' and s.get('match') == 'exact'): continue
                doc = fitz.open(pdf); w = s['text'].split(); tb = pp.text_between(doc, ' '.join(w[:8]), ' '.join(w[-8:]), s.get('pdf_page')); raw = tb['raw'] if tb else s['text']
                res = pp.crop_quote(doc, raw, str(out / f"{f['id']}_s{k}.png"), dpi=170, pad=26, tight_x=True); doc.close()
                if not res.get('ok'): continue
                rid = f"{ck}__qc__{f['id']}__{k}"; meta[rid] = (ck, f['id'], k)
                reqs.append(L.Req(rid, QC_MODEL, f"TEXT A (model):\n{s['text']}\n\nTEXT B (PDF text layer):\n{raw}", sysq, None, QC_EFFORT, 3000, images=[res['out']]))
        for kind, tag in (('questions', 'Q'), ('claims', 'C'), ('caveats', 'V')):   # the quotes behind questions, claims and caveats are checked the same way
            for it in ps.get(kind, []):
                text = it.get('original_wording') if kind == 'questions' else (it.get('span') or {}).get('text', '')
                if not text or it.get('match') not in ('exact', 'letters_digits', 'repaired'): continue
                doc = fitz.open(pdf); w = text.split(); tb = pp.text_between(doc, ' '.join(w[:8]), ' '.join(w[-8:]), it.get('pdf_page') or (it.get('span') or {}).get('pdf_page')); raw = tb['raw'] if tb else text
                res = pp.crop_quote(doc, raw, str(out / f"{it['id']}_{kind[0]}.png"), dpi=170, pad=26, tight_x=True); doc.close()
                if not res.get('ok'): continue
                rid = f"{ck}__qc__{kind}__{it['id']}"; meta[rid] = (ck, kind, it['id'])
                reqs.append(L.Req(rid, QC_MODEL, f"TEXT A (model):\n{text}\n\nTEXT B (PDF text layer):\n{raw}", sysq, None, QC_EFFORT, 3000, images=[res['out']]))
    res_ = dispatch(M, 'quote_check', reqs, mode); changed = []; seen = collections.Counter()
    by = {}
    for rid, (ck, fid, k) in meta.items():
        x = res_.get(rid); j = safe_json(x) if x else None
        if j: by.setdefault(ck, {})[(fid, k)] = j
    for ck, items in by.items():
        f_ = M.dir / ck / 'picost.json'; ps = json.loads(f_.read_text(encoding='utf-8')); p = M.m['papers'][ck]; fl = set(p.get('flagged', []))
        for kind in ('questions', 'claims', 'caveats'):
            for it in ps.get(kind, []):
                j = items.get((kind, it['id']))
                if j: it['vision'] = {'printed': j.get('printed', ''), 'a_equals_print': j.get('a_equals_print'), 'a_differences': j.get('a_differences', []), 'a_changes_meaning': bool(j.get('a_changes_meaning')), 'b_equals_print': j.get('b_equals_print'), 'b_differences': j.get('b_differences', []), 'model': QC_MODEL}
        for f in ps.get('findings', []):
            for k, s in enumerate(f.get('spans', []), 1):
                j = items.get((f['id'], k))
                if not j: continue
                s['vision'] = {'printed': j.get('printed', ''), 'a_equals_print': j.get('a_equals_print'), 'a_differences': j.get('a_differences', []), 'a_changes_meaning': bool(j.get('a_changes_meaning')), 'b_equals_print': j.get('b_equals_print'), 'b_differences': j.get('b_differences', []), 'model': QC_MODEL}
                seen['checked'] += 1; seen['equals print'] += bool(j.get('a_equals_print'))
                if j.get('a_changes_meaning'):
                    seen['meaning changed'] += 1; changed.append((ck.split('-')[0], f['id'], k, '; '.join(j.get('a_differences', []))[:160]))
                    f['flags'] = sorted(set(f.get('flags', [])) | {'quote_differs_from_print'}); fl.add(f['id'])
        p['flagged'] = sorted(fl); f_.write_text(json.dumps(ps, indent=1, ensure_ascii=False), encoding='utf-8')
    st['status'] = 'done'; st['summary'] = dict(seen); st['meaning_changed'] = changed; M.save(); M.event(f"quote check: {dict(seen)}; quotes whose differences change the meaning: {changed[:6]}")


def stage_checks(M, mode):
    key = 'checks'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    rng = random.Random(M.m['run_id']); items = []; sys_v = prompt('vision-check-v3.md'); st['prompt'] = 'pipeline/prompts/vision-check-v3.md'
    for ck, p in M.m['papers'].items():
        if p.get('failed') or 'picost' not in p.get('stages', {}): continue
        fs, ps_ = final_findings(M, ck); QS[ck] = ps_.get('questions', [])
        for f in fs: items.append((ck, f))
    with cf.ThreadPoolExecutor(6) as ex_:
        dmres = list(ex_.map(lambda it: run_dm(dm_state(M, it[1], QS.get(it[0])), dm_questions(M, table=rests_on_table(it[1]))), items))
    rows = {}; total_tokens = 0
    for (ck, f), r in zip(items, dmres):
        s = dm_summary(r); total_tokens += sum(r[p].get('_tokens', 0) for p in r); why = []
        if s['score'] < DM_LOW: why.append('low check score')
        if s['spread'] > DM_SPREAD: why.append('checks disagree')
        if f.get('flags'): why.append('flagged: ' + ','.join(f['flags']))
        if f.get('needs_jp'): why.append('Opus unsure')
        rows[(ck, f['id'])] = {'ck': ck, 'id': f['id'], 'tier': f.get('tier'), 'statement': f.get('statement', ''), 'dm': r, 'summary': s, 'why_vision': why, 'sampled': False}
    for k, v in rows.items():
        if not v['why_vision']: v['why_vision'] = ['every finding gets a crop look (JP, 2026-11-25)']
    M.m['spent_usd'] = round(M.m['spent_usd'] + total_tokens * 0.042 / 1e6, 5)   # decision models cost cents; counted against the cap
    vis = [v for v in rows.values() if v['why_vision']]; reqs = []; findings = {(ck, f['id']): f for ck, f in items}
    for v in vis:
        f = findings[(v['ck'], v['id'])]; crop = make_crop(M, v['ck'], f)
        v['crop'] = crop
        if crop: reqs.append(L.Req(f"{v['ck']}__vis__{v['id']}", R['vision_check'], f"Finding {v['id']}: {f.get('statement', '')}\nQuoted span(s): {' | '.join(x.get('text', '') for x in f.get('spans', []))}\nNumbers: {json.dumps(f.get('numbers', []), ensure_ascii=False)[:1500]}", sys_v, None, 'medium', 5000, images=[crop]))
    res = dispatch(M, 'checks_vision', reqs, mode); opus = []
    for v in vis:
        x = res.get(f"{v['ck']}__vis__{v['id']}"); j = safe_json(x) if x else None; c0 = (j or {}).get('checks', [{}])[0] if j else {}
        v['sol'] = c0 or ({'overall': 'no answer'} if v.get('crop') else {'overall': 'cannot_verify', 'reason': 'no crop could be made: the quoted span was not located in the PDF text, so there is nothing to look at'}); sol_pass = c0.get('overall') == 'pass'; dm_pass = v['summary']['score'] >= DM_LOW and v['summary']['spread'] <= DM_SPREAD
        v['dispute'] = c0.get('overall') in ('pass', 'fail') and (sol_pass != dm_pass)   # cannot_verify is not a dispute: it goes to a person   # the checks and Sol disagree: the rare dispute, for Opus
        if v['dispute'] and v.get('crop'):
            f = findings[(v['ck'], v['id'])]; opus.append(L.Req(f"{v['ck']}__opusvis__{v['id']}", R['vision_dispute'], f"Finding {v['id']}: {f.get('statement', '')}\nQuoted span(s): {' | '.join(x_.get('text', '') for x_ in f.get('spans', []))}\nThe automatic checks scored this {v['summary']['score']:.2f} (spread {v['summary']['spread']:.2f}); GPT-6.2 Sol said {c0.get('overall')}: {c0.get('reason', '')}. Decide.", sys_v, None, 'medium', 3000, images=[v['crop']]))
    res2 = dispatch(M, 'checks_opus', opus, mode)
    for v in vis:
        x = res2.get(f"{v['ck']}__opusvis__{v['id']}")
        if x: j = safe_json(x); v['opus'] = (j or {}).get('checks', [{}])[0] if j else {'overall': 'no answer'}
    for v in rows.values():
        o = (v.get('opus') or {}).get('overall'); s = (v.get('sol') or {}).get('overall')
        v['final'] = o or s or ('cannot verify' if not v.get('crop') else 'needs JP')   # no crop (quote not found) or no answer (straggler): a person looks
        if v['final'] == 'cannot_verify': v['final'] = 'cannot verify'
        if v['final'] not in ('pass', 'fail', 'cannot verify'): v['final'] = 'needs JP'
    for ck in M.m['papers']:
        out = [v for v in rows.values() if v['ck'] == ck]
        if out: (M.dir / ck / 'checks.json').write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    st['status'] = 'done'; st['summary'] = {'findings': len(rows), 'vision': len(vis), 'disputes': sum(1 for v in vis if v.get('dispute')), 'fail': sum(1 for v in rows.values() if v['final'] == 'fail'), 'cannot_verify': sum(1 for v in rows.values() if v['final'] == 'cannot verify'), 'needs_jp': sum(1 for v in rows.values() if v['final'] == 'needs JP')}; M.save(); M.event(f"checks: {st['summary']}")


# ---------------------------------------------------------------- stage: draft (debate)
def shuffle_labels(rng, authors): idx = list(range(len(authors))); rng.shuffle(idx); return idx   # position i shows authors[idx[i]] as A, B, C


def nodes_of(j): return {n['id']: n for n in (j or {}).get('nodes', []) if isinstance(n, dict) and n.get('id')}


def apply_changes(original, changes):
    """Apply the model's list of exact changes (old -> new) in order to the original statement; None if an old text is not in the statement."""
    s = original
    for c in changes or []:
        old, new = str(c.get('old', '')), str(c.get('new', ''))
        if not old or old not in s: return None
        s = s.replace(old, new, 1)
    return s


def rework_low_scores(M, data, evd, dm_evd, cn, mode):
    """Errors-only fix (JP, 2026-11-27; prompt evd-fix-v1). EVD statements with a decision-model score below DM_LOW go to the model of role evd_rework (Gemini 4 Neon, effort evd_rework_effort). It changes only words or numbers that are wrong against the passage, keeps everything else verbatim and lists every change (old, new, reason). A correction replaces the statement only if the list of changes reproduces it exactly, it passes the writing-rules check and its decision-model score is at least DM_LOW; otherwise the original stays and the proposal is shown beside it. Verdicts are stored as ok (unchanged), rewrite (corrected) and extraction_problem so that older sheets read."""
    corrected = {(ck, x['id']) for ck in {t[0] for t in evd} for x in final_findings(M, ck)[0] if x.get('corrected_from_supplement')}   # findings corrected from supplementary material are always checked: their numbers changed
    low = [(ck, nid, f) for ck, nid, f in evd if (f.get('dm') or {}).get('score', 1) < DM_LOW or (ck, f['node'].get('source_id')) in corrected]
    if not low: return
    sysr = prompt(RW_PROMPT); reqs = []; items = {}
    for ck, nid, f in low:
        fnd = next((x for x in final_findings(M, ck)[0] if x['id'] == f['node'].get('source_id')), {}); crop = make_crop(M, ck, fnd) if fnd else None; items[f'{ck}__rework__{nid}'] = (ck, nid, f)
        body = {'evd_statement': f['node'].get('statement', ''), 'quote': f['node'].get('quote', ''), 'tier': f['node'].get('tier'), 'finding': {k: fnd.get(k) for k in ('id', 'statement', 'P', 'I', 'C', 'O', 'S', 'T', 'numbers', 'spans')}, 'decision_model_scores': {**f['dm']['means'], 'lowest_question': min(f['dm']['means'], key=f['dm']['means'].get) if f['dm']['means'] else ''}}
        reqs.append(L.Req(f'{ck}__rework__{nid}', RW_MODEL, 'Check this EVD statement and correct errors only:\n' + json.dumps(body, ensure_ascii=False), sysr, None, RW_EFFORT, 8000, images=[crop] if crop else []))   # reasoning tokens count against the budget
    M.m['stage_log'].setdefault('draft_rework', {})['prompt'] = 'pipeline/prompts/' + RW_PROMPT
    res = dispatch(M, 'draft_rework', reqs, mode)
    for rid, (ck, nid, f) in items.items():
        j = safe_json(res.get(rid) or L.Res('', False)) or {}; verdict = {'unchanged': 'ok', 'corrected': 'rewrite'}.get(j.get('verdict'), j.get('verdict', 'no answer')); rev = (j.get('corrected_statement') or j.get('revised_statement') or '').strip(); orig = f['node'].get('statement', '')
        changes = [c for c in (j.get('changes') or []) if isinstance(c, dict)]
        rw = {'model': RW_MODEL, 'original': orig, 'dm_before': f['dm'], 'numbers': j.get('numbers', []), 'fidelity_problems': j.get('fidelity_problems', []), 'verdict': verdict, 'proposal': rev, 'changes': changes, 'note': j.get('note', ''), 'accepted': False}
        if verdict == 'rewrite' and rev:
            rw['changes_reproduce_rewrite'] = apply_changes(orig, changes) == rev
            trial = {**f['node'], 'statement': rev}; wr = writing_rules(trial, cn[ck]); rw['writing_rules_after'] = wr
            r2 = dm_evd((ck, nid, {**f, 'node': trial})); rw['dm_after'] = dm_summary(r2)
            if wr['pass'] and rw['dm_after']['score'] >= DM_LOW and rw['changes_reproduce_rewrite']:
                f['node'] = trial; f['writing_rules'] = wr; f['dm'] = rw['dm_after']; rw['accepted'] = True
        f['rework'] = rw


def stage_draft(M, mode):
    key = 'draft'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    papers = [ck for ck, p in M.m['papers'].items() if not p.get('failed') and 'picost' in p.get('stages', {})]; rng = random.Random(M.m['run_id'] + 'draft'); sys0 = prompt('draft-nodes-v4.md'); sys1 = prompt('critique-revise-v5.md'); sys2 = prompt('vote-v2.md'); sys3 = prompt('node-detail-check-v1.md')
    cards = {ck: card_text(M, ck, 'primary') for ck in papers}; rest = {ck: card_text(M, ck, 'rest') for ck in papers}; full = {ck: card_text(M, ck, 'all') for ck in papers};   # the claim check reads the whole extraction, not just the primary part
    cn = {ck: card_numbers(M, ck) for ck in papers}; cn_all = cn; data = {ck: {'authors': {}} for ck in papers}
    # round 0: the authors draft in parallel from the same card (one author, or several)
    reqs = [L.Req(f'{ck}__r0-{a}', m, f'Extraction:\n{cards[ck]}\n\nWrite the nodes now.', sys0, None, e, 9000) for ck in papers for a, m, e in AUTHORS]
    reqs += [L.Req(f'{ck}__single', AUTHORS[0][1], f'Extraction:\n{rest[ck]}\n\nWrite the nodes now. Write nodes only for the findings, questions, claims and caveats given here (the primary findings are drafted elsewhere; link to them by their ids, "E-" plus the source id).', sys0, None, AUTHORS[0][2], 20000) for ck in papers]   # everything except the primary EVDs: one model, one draft (JP, 2026-11-25)
    st['prompt'] = 'pipeline/prompts/draft-nodes-v4.md'; M.m['evd_rules_prompt'] = 'draft-nodes-v4'; r0 = dispatch(M, 'draft_r0', reqs, mode)
    for ck in papers:
        for a, _, _ in AUTHORS:
            j = safe_json(r0.get(f'{ck}__r0-{a}') or L.Res('', False)); nodes = nodes_of(j); data[ck]['authors'][a] = {'r0': nodes, 'r0_writing_rules': {i: writing_rules(n, cn[ck]) for i, n in nodes.items()}}
    for ck in papers:
        sj = nodes_of(safe_json(r0.get(f'{ck}__single') or L.Res('', False))); data[ck]['single'] = {'author': AUTHORS[0][0], 'nodes': sj, 'writing_rules': {i: writing_rules(n, cn_all[ck]) for i, n in sj.items()}, 'failed': not sj}
    if DEBATE:
        # round 1: each critic sees all drafts (anonymous, shuffled) with writing-rules check results and revises; a critic who is not an author adds a version of its own
        reqs = []; order = {}
        for ck in papers:
            have = [a for a, _, _ in AUTHORS if data[ck]['authors'][a]['r0']]
            for a, m, e in CRITICS:
                idx = shuffle_labels(rng, have); order[(ck, a)] = [have[i] for i in idx]; blob = {chr(65 + k): {'nodes': list(data[ck]['authors'][h]['r0'].values()), 'writing_rules': data[ck]['authors'][h]['r0_writing_rules']} for k, h in enumerate(order[(ck, a)])}
                if have: reqs.append(L.Req(f'{ck}__r1-{a}', m, f'Extraction:\n{cards[ck]}\n\nDrafts:\n{json.dumps(blob, ensure_ascii=False)}\n\nCritique and revise now.', sys1, None, e, 14000))
        st['prompt'] = 'pipeline/prompts/critique-revise-v5.md'; r1 = dispatch(M, 'draft_r1', reqs, mode)
        for ck in papers:
            for a, _, _ in AUTHORS:   # an author who is not a critic keeps the first draft as the round-1 version
                d = data[ck]['authors'][a]; d.setdefault('critiques', []); d['r1'] = d['r0']; d['r1_writing_rules'] = d['r0_writing_rules']
            for a, _, _ in CRITICS:
                j = safe_json(r1.get(f'{ck}__r1-{a}') or L.Res('', False)); d = data[ck]['authors'].setdefault(a, {'r0': {}, 'r0_writing_rules': {}}); d['critiques'] = (j or {}).get('critiques', []); d['r1'] = nodes_of((j or {}).get('revised')) or d['r0']; d['r1_writing_rules'] = {i: writing_rules(n, cn[ck]) for i, n in d['r1'].items()}
        # vote: the voters decide between the round-1 versions (with one author and one critic: the original draft against the revision)
        reqs = []; vorder = {}
        for ck in papers:
            have = [a for a in data[ck]['authors'] if data[ck]['authors'][a].get('r1')]
            if len(have) < 2: continue
            for voter, m, e in VOTERS:
                idx = shuffle_labels(rng, have); vorder[(ck, voter)] = [have[i] for i in idx]; blob = {chr(65 + k): {'nodes': list(data[ck]['authors'][h]['r1'].values()), 'writing_rules': data[ck]['authors'][h]['r1_writing_rules']} for k, h in enumerate(vorder[(ck, voter)])}
                reqs.append(L.Req(f'{ck}__vote-{voter}', m, f'Extraction:\n{cards[ck]}\n\nVersions:\n{json.dumps(blob, ensure_ascii=False)}\n\nVote now.', sys2, None, e, 5000))
        st['prompt'] = 'pipeline/prompts/vote-v2.md'; rv = dispatch(M, 'draft_vote', reqs, mode); ties = []
        for ck in papers:
            votes = {}
            for voter in [v[0] for v in VOTERS]:
                j = safe_json(rv.get(f'{ck}__vote-{voter}') or L.Res('', False)); lab = {chr(65 + k): a for k, a in enumerate(vorder.get((ck, voter), []))}
                votes[voter] = {x['node']: {'author': lab.get(x.get('pick')), 'reason': x.get('reason', '')} for x in (j or {}).get('picks', []) if isinstance(x, dict) and x.get('node')}
            data[ck]['votes'] = votes
            for nid in {n for a in data[ck]['authors'].values() for n in a.get('r1', {})}:
                vs = [votes[v[0]].get(nid, {}).get('author') for v in VOTERS]; s, c = (vs + [None, None])[:2]
                if s and c and s != c: ties.append((ck, nid, s, c))
        reqs = []
        for ck in sorted({t[0] for t in ties}):
            mine = [t for t in ties if t[0] == ck]; blob = {nid: {'candidates': {a: data[ck]['authors'][a]['r1'].get(nid) for a in (s, c)}} for _, nid, s, c in mine}
            reqs.append(L.Req(f'{ck}__tie', R.get('tiebreak') or VOTERS[0][1], f'Extraction:\n{cards[ck]}\n\nTwo voters disagree. Candidates (author names are the keys); pick the better one for each node:\n{json.dumps(blob, ensure_ascii=False)}\n\nReturn {{"picks": [{{"node": "...", "pick": "<author name>", "reason": ""}}]}}.', sys2.replace('(A, B and C, in random order)', '(named by their authors)'), None, 'medium', 3000))
        rt = dispatch(M, 'draft_tie', reqs, mode)
        for ck in papers:
            j = safe_json(rt.get(f'{ck}__tie') or L.Res('', False)); tie = {x['node']: x.get('pick') for x in (j or {}).get('picks', []) if isinstance(x, dict)}; finals = {}
            for nid in {n for a in data[ck]['authors'].values() for n in a.get('r1', {})}:
                vs = [data[ck]['votes'][v[0]].get(nid, {}).get('author') for v in VOTERS]; s, c = (vs + [None, None])[:2]
                win = s if s and s == c else (tie.get(nid) if tie.get(nid) in data[ck]['authors'] else (s or c or next((a for a in data[ck]['authors'] if nid in data[ck]['authors'][a].get('r1', {})), None)))
                how = ' and '.join(short_name(v[1]) for v in VOTERS[:2]) + ' agree' if s and s == c else (short_name(R.get('tiebreak') or AUTHORS[0][1]) + ' tie-break' if tie.get(nid) in data[ck]['authors'] else 'single vote or fallback')
                node = data[ck]['authors'].get(win, {}).get('r1', {}).get(nid)
                if node: finals[nid] = {'node': node, 'author': win, 'how': how, 'writing_rules': writing_rules(node, cn[ck])}
            for nid, node in data[ck]['single']['nodes'].items(): finals[nid] = {'node': node, 'author': AUTHORS[0][0], 'how': 'single draft (not debated)', 'writing_rules': writing_rules(node, cn[ck])}
            data[ck]['finals'] = finals
    else:   # one author (JP, 2026-11-27): the first draft is final; no critique round, no vote, no tiebreak
        for ck in papers:
            a0 = AUTHORS[0][0]; d0 = data[ck]['authors'][a0]; d0['r1'] = d0['r0']; d0['r1_writing_rules'] = d0['r0_writing_rules']; d0.setdefault('critiques', []); data[ck]['votes'] = {}; finals = {}
            for nid, node in d0['r0'].items(): finals[nid] = {'node': node, 'author': a0, 'how': 'single author draft (no critique or vote)', 'writing_rules': writing_rules(node, cn[ck])}
            for nid, node in data[ck]['single']['nodes'].items(): finals[nid] = {'node': node, 'author': AUTHORS[0][0], 'how': 'single draft (not debated)', 'writing_rules': writing_rules(node, cn[ck])}
            data[ck]['finals'] = finals
    # node-detail check (was "claim check"; claim now means CLM only): the first checker in roles.node_check that did not write the winner; when the only checker wrote it, it checks its own text and the check is marked as such
    reqs = []
    def checker_of(author): return next((c[0] for c in NODE_CHECK if c[0] != author), NODE_CHECK[0][0])
    for ck in papers:
        for chk, m, e in NODE_CHECK:
            mine = [f['node'] for f in data[ck]['finals'].values() if f['node'].get('type') != 'QUE' and checker_of(f['author']) == chk]
            if mine: reqs.append(L.Req(f'{ck}__check-{chk}', m, f'Extraction:\n{full[ck]}\n\nNodes to check:\n{json.dumps(mine, ensure_ascii=False)}\n\nCheck now.', sys3, None, e, min(32000, 2000 + 450 * len(mine))))   # budget grows with the number of nodes to check
    st['prompt'] = 'pipeline/prompts/node-detail-check-v1.md'; rc = dispatch(M, 'draft_check', reqs, mode)
    # decision-model check of each final EVD (fidelity of the written text and numbers found in the source)
    evd = [(ck, nid, f) for ck in papers for nid, f in data[ck]['finals'].items() if f['node'].get('type') == 'EVD']
    def dm_evd(t):
        ck, nid, f = t; fnd = next((x for x in final_findings(M, ck)[0] if x['id'] == f['node'].get('source_id')), {})
        return run_dm(dm_state(M, {**fnd, 'statement': f['node'].get('statement', '')}, final_findings(M, ck)[1].get('questions', [])), {'fidelity': dm_questions(M, 'EVD statement')['fidelity'], 'numbers_in_source': dm_questions(M)['numbers_in_source']})
    with cf.ThreadPoolExecutor(6) as ex_: dres = list(ex_.map(dm_evd, evd))
    for (ck, nid, f), r in zip(evd, dres): f['dm'] = dm_summary(r)
    rework_low_scores(M, data, evd, dm_evd, cn, mode)
    for ck in papers:
        for chk in [v[0] for v in NODE_CHECK]:
            j = safe_json(rc.get(f'{ck}__check-{chk}') or L.Res('', False))
            for c in (j or {}).get('checks', []):
                if c.get('node') in data[ck]['finals']: data[ck]['finals'][c['node']]['detail_check'] = {'checker': chk, 'own_draft': data[ck]['finals'][c['node']]['author'] == chk, **c}
        for nid, f in data[ck]['finals'].items():
            cc = (f.get('detail_check') or {}).get('overall'); dmv = (f.get('dm') or {}).get('score')
            ok = f['writing_rules']['pass'] and (cc in ('pass', 'minor') or f['node'].get('type') == 'QUE') and (dmv is None or dmv >= DM_LOW)
            f['status'] = ('pass with notes' if cc == 'minor' else 'pass') if ok else 'needs JP review'
            if ok and (f.get('rework') or {}).get('accepted'): f['status'] = 'pass (reworked by ' + f['rework']['model'] + ')'
            rwv = (f.get('rework') or {}).get('verdict')
            if rwv == 'ok' and f['writing_rules']['pass'] and (cc in ('pass', 'minor') or f['node'].get('type') == 'QUE'): f['status'] = 'pass (' + f['rework']['model'] + ' kept it despite the low decision-model score)'
            if (f.get('rework') or {}).get('verdict') == 'extraction_problem': f['status'] = 'needs JP review: extraction problem'
            if (f.get('detail_check') or {}).get('own_draft'): f['status'] = 'needs JP review: the node-detail check was made by the model that wrote the node'   # JP, 2026-11-27: a model must not check its own work
        (M.dir / ck / 'drafts.json').write_text(json.dumps(data[ck], indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    st['status'] = 'done'; st['summary'] = {ck: {'nodes': len(data[ck]['finals']), 'pass': sum(1 for f in data[ck]['finals'].values() if f['status'] == 'pass')} for ck in papers}; M.save(); M.event(f"draft: {st['summary']}")


# ---------------------------------------------------------------- stage: quality signals
SIGNALS = {  # signal id: (what it asks, allowed values)
    'construct-validity': ('Do the measures capture the construct the study claims to measure?', 'low-risk | some-concerns | high-risk'),
    'internal-validity': ('Could the results be explained by flaws in design, leakage or confounds rather than the studied effect?', 'low-risk | some-concerns | high-risk'),
    'external-validity': ('Do the results generalize beyond the sample, datasets, models and settings tested?', 'low-risk | some-concerns | high-risk'),
    'statistical-rigor': ('Are the statistical methods appropriate and reported well enough to trust the conclusions?', 'low-risk | some-concerns | high-risk'),
    'reproducibility': ('Could another team reproduce the study from what is shared (prompts, versions, code, data)?', 'low-risk | some-concerns | high-risk'),
    'baseline-adequacy': ('Are the comparators (humans, other models, simple baselines) adequate?', 'addressed | partial | not-addressed'),
    'human-baseline': ('Is there a human baseline, and is it described (raters, number, expertise, agreement)?', 'addressed | partial | not-addressed'),
    'train-dev-test': ('Are training, development and test data separated and described?', 'addressed | partial | not-addressed'),
    'ablation-experiments': ('Are ablations or sensitivity analyses reported?', 'addressed | partial | not-addressed'),
    'prompt-engineering': ('Are the prompts and the prompt-development process reported?', 'addressed | partial | not-addressed'),
    'confidence-intervals': ('Are confidence intervals or other uncertainty reported for the key results?', 'addressed | partial | not-addressed'),
    'chance-corrected-metrics': ('Are chance-corrected metrics (kappa, MCC) used where the classes are imbalanced?', 'addressed | partial | not-addressed'),
    'multiple-comparisons': ('Is multiple testing handled?', 'addressed | partial | not-addressed'),
    'data-leakage': ('Is leakage of test data into training or prompts ruled out?', 'addressed | partial | not-addressed | unresolved'),
    'statistical-power': ('Is there a power analysis showing the sample is adequate? (rate adequate only if the paper has one)', 'adequate | not-addressed'),
    'effect-size': ('Are effect sizes reported?', 'addressed | partial | not-addressed'),
    'exact-p-values': ('Are exact p-values reported?', 'addressed | partial | not-addressed'),
    'spin': ('Do the abstract and conclusions claim more than the results support?', 'addressed | partial | not-addressed'),
    'sample-size-estimation': ('Was the sample size estimated or justified before the study (a stated calculation or rule)?', 'done | not-done'),
    'study-type': ('Is the study exploratory (no pre-stated hypotheses or analysis plan) or confirmatory (pre-stated hypotheses tested)?', 'exploratory | confirmatory'),
    'registration': ('Was the study preregistered?', 'not-applicable | not-disclosed | disclosed'),
    'protocol': ('Is a study protocol available?', 'not-applicable | not-disclosed | disclosed'),
    'ethical-approval': ('Is ethical approval or exemption stated?', 'disclosed | partial | not-disclosed | not-applicable'),
    'funding-disclosure': ('Is funding disclosed?', 'disclosed | partial | not-disclosed | not-applicable'),
    'coi-disclosure': ('Are conflicts of interest disclosed?', 'disclosed | partial | not-disclosed | not-applicable'),
    'code-check': ('Is analysis code shared and checked?', 'addressed | partial | not-addressed'),
    'data-repo-check': ('Are the data in a repository?', 'addressed | partial | not-addressed'),
}
import tripod_items as _TRIPOD
SIGNALS.update(_TRIPOD.signals())   # JP, 2026-11-26: the 40 TRIPOD-LLM reporting rows are rated in the same run


CONF = ('high', 'medium', 'low')


def needs_fallback(row, allowed_vals):
    """A rating goes to the fallback rater when it is not a valid value or when the rater reports low confidence. A missing or unreadable confidence counts as low (the safe side: a second rater looks)."""
    return row.get('rating') not in allowed_vals or row.get('confidence') not in ('high', 'medium')


def cascade_result(first, fb, allowed_vals, first_name='Neon', fb_name='Sol'):
    """One rater with a fallback (JP, 2026-11-27). Returns (status, final rating, agreement text).
    confident: the first rater's rating stands. fallback: the first rater was low, the fallback rater's rating stands. needs_human: the fallback rater was low too (or gave no valid rating), so JP decides."""
    if fb is None: return ('confident', first['rating'], f'{first_name} only, confident ({first.get("confidence")})')
    if fb.get('rating') in allowed_vals and fb.get('confidence') in ('high', 'medium'):
        return ('fallback', fb['rating'], f'{fb_name} rated it because {first_name} was not confident' + (' (same rating as ' + first_name + ')' if fb['rating'] == first.get('rating') else f' ({first_name} said {first.get("rating")})'))
    return ('needs_human', 'needs_human', f'needs your judgment: {first_name} and {fb_name} both reported low confidence or no valid rating')


def stage_qs(M, mode):
    key = 'qs'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    t0 = time.time(); st.setdefault('started_utc', time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime()))
    GROUPS = {'q': [k for k in SIGNALS if not k.startswith('tripod-')], 't': [k for k in SIGNALS if k.startswith('tripod-')]}   # two requests per rater: one thinking budget for the 27 quality signals and one for the 40 TRIPOD-LLM rows (a single request ran out of tokens on a long paper)
    def sysfor(ks): return prompt('rate-signals-v3.md').replace('{SIGNALS}', '\n'.join(f'- `{k}`: {SIGNALS[k][0]} Allowed values: {SIGNALS[k][1]}.' for k in ks))
    sysg = {g: sysfor(ks) for g, ks in GROUPS.items()}; st['prompt'] = 'pipeline/prompts/rate-signals-v3.md'; reqs = []
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        for r, m, e in RATERS:
            for g in GROUPS: reqs.append(L.Req(f'{ck}__qs-{r}-{g}', m, 'Rate the paper now.', sysg[g], ex(p['pdf']), e, 40000 if e == 'high' else 24000))   # High thinking uses most of a small budget and returns nothing (all 25 ratings were lost in the first rerun)
    res = dispatch(M, 'qs', reqs, mode); allowed = {k: [x.strip() for x in v[1].split('|')] for k, v in SIGNALS.items()}; out = {}; raws = {}; disputes = {}
    def read(ck, p, res_, rater, doc, keys, only=None):
        """Rows for one rater from the request ids `keys` (explicit, so a rater and the adjudicator may share a key such as 'sol')."""
        got = {}
        for kk in keys:
            j = safe_json(res_.get(kk) or L.Res('', False)); got.update({x.get('signal'): x for x in (j or {}).get('ratings', []) if isinstance(x, dict)})
        rows = []
        for sg in SIGNALS:
            if only and sg not in only: continue
            x = got.get(sg); qstart = ((x or {}).get('quote_start') or '').strip(); qend = ((x or {}).get('quote_end') or '').strip(); raw_q = ''; src = 'quote'; pg_ = (x or {}).get('page')
            if qstart:   # anchors (rate-signals-v2 and v3): the quote is the PDF's own text between the two anchors
                if qstart.lower() == 'none': q = 'none'; found = None; src = 'anchors'
                else:
                    tb = pp.text_between(doc, qstart, qend or qstart, pg_); src = 'anchors'
                    if tb: q = tb['text']; raw_q = tb['raw']; found = True; pg_ = tb['page']; src = tb.get('how', 'anchors')
                    else: q = qstart + ' ... ' + qend; found = False
            else:
                q = (x or {}).get('quote', ''); found = None if not x or q in ('', 'none') else bool(pp.find_quote(doc, q)['found']); raw_q = q
            rating = (x or {}).get('rating'); loc = (x or {}).get('locator', ''); conf = str((x or {}).get('confidence') or '').strip().lower(); conf = conf if conf in CONF else ('missing' if x else '')
            pm_ = {e['pdf']: e['printed'] for e in M.m['papers'][ck]['preflight']['page_map']}
            if pg_ and found: loc = (loc + '; ' if loc else '') + f"PDF p. {pg_}" + (f" (printed p. {pm_.get(pg_)})" if pm_.get(pg_) and str(pm_.get(pg_)) != str(pg_) else '')
            rows.append({'paper': ck, 'signal': sg, 'rater': rater, 'counted': True, 'rating': rating if rating in allowed[sg] else ('invalid: ' + str(rating) if x else 'no answer'), 'confidence': conf, 'quote': q, 'quote_raw': raw_q, 'quote_source': src, 'pdf_page': pg_ if found else None, 'locator': loc, 'quote_found': found, 'reason': (x or {}).get('reason', '')})
        return rows
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        doc = fitz.open(ex(p['pdf'])); raw = []
        for r in [x[0] for x in RATERS]: raw += read(ck, p, res, r, doc, [f'{ck}__qs-{r}-{g}' for g in GROUPS])
        doc.close(); raws[ck] = raw
        disputes[ck] = [] if (len(RATERS) >= 3 or QS_CASCADE) else [sg for sg in SIGNALS if len({x['rating'] for x in raw if x['signal'] == sg}) > 1 or any(x['rating'] not in allowed[sg] for x in raw if x['signal'] == sg)]   # the two raters differ (or one gave no valid rating)
    fb_need = {}; fb_by = {}
    if QS_CASCADE:   # the one rater's low-confidence (or invalid) ratings go to the fallback rater, blind (it does not see the first rating)
        fb_key, fb_model, fb_eff = QS_FALLBACK[0]; reqs = []
        for ck, raw in raws.items():
            fb_need[ck] = [x['signal'] for x in raw if needs_fallback(x, allowed[x['signal']])]; fb_by[ck] = fb_need[ck]
            for g, ks in GROUPS.items():
                sgs = [k for k in ks if k in fb_need[ck]]
                if sgs: reqs.append(L.Req(f'{ck}__qsfb-{g}', fb_model, 'Rate the paper now.', sysfor(sgs), ex(M.m['papers'][ck]['pdf']), fb_eff, 40000 if fb_eff == 'high' else 24000))
        res_fb = dispatch(M, 'qs_fallback', reqs, mode)
        for ck, sgs in fb_need.items():
            if not sgs: continue
            doc = fitz.open(ex(M.m['papers'][ck]['pdf'])); raws[ck] += read(ck, M.m['papers'][ck], res_fb, fb_key, doc, [f'{ck}__qsfb-{g}' for g in GROUPS], only=set(sgs)); doc.close()
    reqs = []; sysa = prompt('adjudicate-signals-v2.md'); st['adjudicator_prompt'] = 'pipeline/prompts/adjudicate-signals-v2.md'
    for ck, sgs in disputes.items():
        if not sgs: continue
        sig = '\n'.join(f'- `{k}`: {SIGNALS[k][0]} Allowed values: {SIGNALS[k][1]}.' for k in sgs); rng_ = random.Random(M.m['run_id'] + ck); names = [x[0] for x in RATERS]; rng_.shuffle(names)
        shown = {f'Rater {i + 1}': [{k: x[k] for k in ('signal', 'rating', 'quote', 'locator')} for x in raws[ck] if x['rater'] == nm and x['signal'] in sgs] for i, nm in enumerate(names)}
        reqs.append(L.Req(f'{ck}__qs-{QS_ADJ["key"]}', QS_ADJ['model'], 'The two raters\' answers for the signals in dispute:\n' + json.dumps(shown, ensure_ascii=False) + '\n\nDecide now.', sysa.replace('{SIGNALS}', sig), ex(M.m['papers'][ck]['pdf']), QS_ADJ['effort'], 16000))
    res3 = dispatch(M, 'qs_adjudicate', reqs, mode) if reqs else {}
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        raw = raws[ck]
        if disputes[ck]:
            doc = fitz.open(ex(p['pdf'])); raw += read(ck, p, res3, QS_ADJ['key'], doc, [f'{ck}__qs-{QS_ADJ["key"]}'], only=set(disputes[ck])); doc.close()
        agg = []
        for sg in SIGNALS:
            if QS_CASCADE:
                first = next(x for x in raw if x['signal'] == sg and x['rater'] == RATERS[0][0]); fb = next((x for x in raw if x['signal'] == sg and x['rater'] == QS_FALLBACK[0][0]), None) if sg in fb_need[ck] else None
                if sg in fb_need[ck] and fb is None: fb = {'rating': 'no answer', 'confidence': ''}
                status, final, how_ = cascade_result(first, fb, allowed[sg], short_name(RATERS[0][1]), short_name(QS_FALLBACK[0][1]))
                cnt = {}
                for x in raw:
                    if x['signal'] == sg and x['counted'] and x['rating'] in allowed[sg]: cnt[x['rating']] = cnt.get(x['rating'], 0) + 1
                agg.append({'paper': ck, 'signal': sg, 'votes': cnt, 'majority': final, 'status': status, 'agreement': how_, 'adjudicated': status != 'confident', 'quotes_not_found': sum(1 for x in raw if x['signal'] == sg and x['counted'] and x['quote_found'] is False)}); continue
            votes = [x['rating'] for x in raw if x['signal'] == sg and x['counted'] and x['rating'] in allowed[sg]]; cnt = {}
            for v in votes: cnt[v] = cnt.get(v, 0) + 1
            top = sorted(cnt.items(), key=lambda kv: -kv[1]); maj = top[0][0] if top and (len(top) == 1 or top[0][1] > top[1][1]) and (top[0][1] >= 2) else 'no majority'
            agg.append({'paper': ck, 'signal': sg, 'votes': cnt, 'majority': maj, 'agreement': ((('all raters agree' if len(cnt) == 1 and top[0][1] == len(RATERS) else 'majority of raters' if maj != 'no majority' else 'three different ratings') if len(RATERS) >= 3 else 'both raters agree')) if sg not in disputes[ck] else ('Sol sided with one rater' if maj != 'no majority' else 'three different ratings'), 'adjudicated': sg in disputes[ck], 'quotes_not_found': sum(1 for x in raw if x['signal'] == sg and x['counted'] and x['quote_found'] is False)})
        crops = {}; qd = M.dir / ck / 'qs_crops'; qd.mkdir(exist_ok=True)   # JP, 2026-11-26: every quote gets a highlighted, boxed screenshot of where it sits in the PDF
        for x in raw:
            qt = (x.get('quote_raw') or x.get('quote') or '').strip()   # the PDF's own characters, so the crop finds it
            if not qt or qt.lower() == 'none' or not x.get('quote_found'): continue
            if qt not in crops:
                d2 = fitz.open(ex(M.m['papers'][ck]['pdf'])); res_ = pp.crop_quote(d2, qt, str(qd / f"{x['signal']}__{x['rater']}.png"), dpi=150, pad=30, kind='EVD', tight_x=True)   # no outline box (JP, 2026-11-26): the highlight alone marks the quote and nothing else on the page is touched; d2.close()
                crops[qt] = res_['out'] if res_.get('ok') else None
            x['crop'] = crops[qt]
        out[ck] = {'raw': raw, 'aggregate': agg}; (M.dir / ck / 'quality_signals.json').write_text(json.dumps(out[ck], indent=1, ensure_ascii=False), encoding='utf-8')
    st['elapsed_s'] = round(time.time() - t0)
    st['status'] = 'done'; st['mode'] = 'cascade' if QS_CASCADE else ('three raters' if len(RATERS) >= 3 else 'two raters and an adjudicator')
    st['summary'] = {ck: {'signals': len(v['aggregate']), 'disagreed': len(disputes[ck]), 'no_majority': sum(1 for a in v['aggregate'] if a['majority'] == 'no majority'), **({'low_confidence_or_invalid': len(fb_need.get(ck, [])), 'fallback_decided': sum(1 for a in v['aggregate'] if a.get('status') == 'fallback'), 'needs_human': sum(1 for a in v['aggregate'] if a.get('status') == 'needs_human'), 'confidence_missing': sum(1 for x in v['raw'] if x['rater'] == RATERS[0][0] and x['confidence'] == 'missing')} if QS_CASCADE else {})} for ck, v in out.items()}; M.save(); M.event(f"quality signals: {st['summary']}")


def pdf_text(pdf):
    d = fitz.open(pdf); t = '\n\n'.join(f'[PDF page {i + 1}]\n{pp.page_text(pg)}' for i, pg in enumerate(d)); d.close(); return t

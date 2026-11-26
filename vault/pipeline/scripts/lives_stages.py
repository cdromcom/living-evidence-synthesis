#!/usr/bin/env python3
"""Stages after extraction for lives_run.py (JP, 2026-11-25): checks, drafting by debate, quality-signal rating.

  checks   decision models (relevancy, fidelity, quote grounding, table or figure grounding) score every extracted finding; the mean probability and the spread
           between the three models say how much to trust it. Findings that are flagged, low-confidence, split or in a 10% random sample get a GPT-6.2 Sol
           look at the crop (vision); only the rare disagreements between the checks and Sol go to Claude Opus 5.5.
  draft    EVD, QUE, CLM and CVT nodes written by debate: Sonnet 5.5, GPT-6.2 Sol and Gemini 4 Neon (Medium) draft, critique and revise (one critique round;
           a second is specified but not built); Sol and Sonnet vote, Neon breaks ties; the cheaper of Sol and Sonnet that did not write the winner checks every
           claim; decision models check fidelity. Inkling 2 Small writes the nodes too and votes, as a benchmark only.
  qs       quality signals rated blind by Opus 5.5, Sol and Neon (Medium); majority vote; Inkling rates as a benchmark only. Everything is saved for the sheets.
Nothing here writes to the vault. Outputs go to pipeline/runs/<run>/<paper>/ and the review sheet."""
import concurrent.futures as cf, hashlib, json, os, random, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import call_logger as cl, llm_batch as L, pdf_pages as pp, decision_models as dm, config as C
import fitz
dm.load_env(); cl.load_env()

VAULT = cl.VAULT; R = C.ROLES; CK = C.PIPE['checks']
AUTHORS = [(a['key'], a['model'], a['effort']) for a in R['authors']]        # who drafts (pipeline/config/models.json, roles)
VOTERS = [(a['key'], a['model'], a['effort']) for a in R['voters']]          # who decides
RATERS = [(a['key'], a['model'], a['effort']) for a in R['raters']]          # who rates quality signals: two raters, and a third model decides only the disagreements
QS_ADJ = R['qs_adjudicator']
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
    return (len(r.system) + len(r.text)) / 3.5 + per * pages + 1500 * len(r.images)


STANDARD_STAGES = set(C.PIPE['limits'].get('standard_stages', []))   # small stages that run in standard mode even in a batch run (a batch's slowest request would hold the run up)


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
            if tot and done < tot and done >= tot - L._tail_count(tot) and t90 is None: t90 = time.time(); M.event(f'{done} of {tot} requests finished; the rest get {L.STRAGGLER_MIN} more minutes')
        if t90 and time.time() - t90 >= grace:
            M.event(f'stragglers after {L.STRAGGLER_MIN} minutes: cancelling the batch; finished results are kept and the rest go to human review')
            for j in jobs:
                if L.poll_batch(j) == 'running': j['straggler'] = True; L.cancel_batch(j)
            deadline = time.time() + 600
            while any(L.poll_batch(j) == 'running' for j in jobs) and time.time() < deadline: time.sleep(15)
            return True
        time.sleep(20)


def dispatch(M, key, reqs, mode, cap_frac=1.0):
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
        cl.record(M.m['run_id'], key, r.model, st.get('prompt', 'pipeline/prompts/draft-nodes-v2.md'), provider=L.provider_of(r.model), citekey=r.id.split('__')[0], effort=r.effort, tokens_in=x.tin, tokens_out=x.tout, output_text=x.text or None, notes=f'mode={mode}; cost_usd={c:.4f}; finish={x.finish}; err={x.err}')
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
    card = {'review_level_question': M.m.get('question', ''), 'paper': ps.get('paper'), 'findings': [{k: f.get(k) for k in ('id', 'tier', 'answers_QUE', 'supports', 'section', 'statement', 'P', 'I', 'C', 'O', 'S', 'T', 'numbers', 'spans', 'notes')} for f in keep]}
    if part != 'primary': card.update({'caveats': ps.get('caveats', []), 'claims': ps.get('claims', []), 'questions': ps.get('questions', [])})
    if part == 'rest': card['primary_finding_ids_already_drafted_elsewhere'] = [f['id'] for f in fs if f.get('tier') == 'primary']
    return json.dumps(card, ensure_ascii=False)


# ---------------------------------------------------------------- lint
def syllables(w):
    w = re.sub(r'[^a-z]', '', w.lower()); n = len(re.findall(r'[aeiouy]+', w)); n -= 1 if w.endswith('e') and n > 1 else 0; return max(n, 1)
def fk_grade(t):
    s = [x for x in re.split(r'[.!?]+', t) if x.strip()]; w = re.findall(r"[A-Za-z][A-Za-z'-]*", t)
    if not s or not w: return 0.0
    return round(0.39 * len(w) / len(s) + 11.8 * sum(syllables(x) for x in w) / len(w) - 15.59, 1)


def lint(node, card_nums):
    """Free checks: EVD at most 247 characters, every number in the statement is on the card, readability grade; QUE ends with a question mark; the others have a quote."""
    out = {}; t = node.get('type'); txt = node.get('statement') or node.get('title') or node.get('limitation') or ''
    out['chars'] = len(txt); out['fk_grade'] = fk_grade(txt)
    if t == 'EVD':
        out['length_ok'] = len(txt) <= 247; nums = {norm_num(x) for x in re.findall(r'-?\d*\.?\d+', txt.replace(',', ''))}; out['numbers_not_on_card'] = sorted(n for n in nums if n not in card_nums)
        out['readability_ok'] = out['fk_grade'] <= 14
    if t == 'QUE': out['question_ok'] = txt.strip().endswith('?')
    if t in ('CLM', 'CVT', 'EVD'): out['has_quote'] = bool((node.get('quote') or '').strip())
    if t == 'EVD' and node.get('tier') == 'primary': out['links_to_question'] = bool(node.get('answers_QUE'))
    out['no_emdash'] = '\u2014' not in ' '.join(str(v) for v in node.values() if isinstance(v, str))   # JP's writing rule: no em dashes in written text
    out['pass'] = all([out['no_emdash'], out.get('length_ok', True), not out.get('numbers_not_on_card'), out.get('readability_ok', True), out.get('question_ok', True), out.get('has_quote', True), out.get('links_to_question', True)]); return out


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
            'quote_grounding': dm.noul('Is every number in the finding stated in the source span, attributed to the right model or condition?'),
            'table_figure_grounding': dm.noul('Does the table or figure cell named in the numbers (row and column) show the stated values?')}
    if not table: q.pop('table_figure_grounding')   # a finding stated in prose has no table or figure to ground against (the first smoke test scored such findings about 0.47 and sent every one to Sol)
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


QS = {}   # the paper's own questions, by paper, for the relevancy check


def stage_checks(M, mode):
    key = 'checks'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    rng = random.Random(M.m['run_id']); items = []; sys_v = prompt('vision-check-v2.md'); st['prompt'] = 'pipeline/prompts/vision-check-v2.md'
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
        if crop: reqs.append(L.Req(f"{v['ck']}__vis__{v['id']}", R['vision_check'], f"Finding {v['id']}: {f.get('statement', '')}\nQuoted span(s): {' | '.join(x.get('text', '') for x in f.get('spans', []))}\nNumbers: {json.dumps(f.get('numbers', []), ensure_ascii=False)[:1500]}", sys_v, None, 'medium', 1500, images=[crop]))
    res = dispatch(M, 'checks_vision', reqs, mode); opus = []
    for v in vis:
        x = res.get(f"{v['ck']}__vis__{v['id']}"); j = safe_json(x) if x else None; c0 = (j or {}).get('checks', [{}])[0] if j else {}
        v['sol'] = c0 or {'overall': 'no answer'}; sol_pass = c0.get('overall') == 'pass'; dm_pass = v['summary']['score'] >= DM_LOW and v['summary']['spread'] <= DM_SPREAD
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


def stage_draft(M, mode):
    key = 'draft'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    papers = [ck for ck, p in M.m['papers'].items() if not p.get('failed') and 'picost' in p.get('stages', {})]; rng = random.Random(M.m['run_id'] + 'draft'); sys0 = prompt('draft-nodes-v2.md'); sys1 = prompt('critique-revise-v2.md'); sys2 = prompt('vote-v1.md'); sys3 = prompt('claim-check-v1.md')
    cards = {ck: card_text(M, ck, 'primary') for ck in papers}; rest = {ck: card_text(M, ck, 'rest') for ck in papers}; cn = {ck: card_numbers(M, ck) for ck in papers}; cn_all = cn; data = {ck: {'authors': {}} for ck in papers}
    # round 0: three authors (counted) and Inkling (benchmark only) draft in parallel from the same card
    reqs = [L.Req(f'{ck}__r0-{a}', m, f'Extraction:\n{cards[ck]}\n\nWrite the nodes now.', sys0, None, e, 9000) for ck in papers for a, m, e in AUTHORS]
    reqs += [L.Req(f'{ck}__single', AUTHORS[0][1], f'Extraction:\n{rest[ck]}\n\nWrite the nodes now. Write nodes only for the findings, questions, claims and caveats given here (the primary findings are drafted elsewhere; link to them by their ids, "E-" plus the source id).', sys0, None, AUTHORS[0][2], 20000) for ck in papers]   # everything except the primary EVDs: one model, one draft (JP, 2026-11-25)
    st['prompt'] = 'pipeline/prompts/draft-nodes-v2.md'; r0 = dispatch(M, 'draft_r0', reqs, mode)
    for ck in papers:
        for a, _, _ in AUTHORS:
            j = safe_json(r0.get(f'{ck}__r0-{a}') or L.Res('', False)); nodes = nodes_of(j); data[ck]['authors'][a] = {'r0': nodes, 'r0_lint': {i: lint(n, cn[ck]) for i, n in nodes.items()}}
    for ck in papers:
        sj = nodes_of(safe_json(r0.get(f'{ck}__single') or L.Res('', False))); data[ck]['single'] = {'author': AUTHORS[0][0], 'nodes': sj, 'lint': {i: lint(n, cn_all[ck]) for i, n in sj.items()}, 'failed': not sj}
    # round 1: each author sees all three drafts (anonymous, shuffled) with lint results and revises
    reqs = []; order = {}
    for ck in papers:
        have = [a for a, _, _ in AUTHORS if data[ck]['authors'][a]['r0']]
        for a, m, e in AUTHORS:
            idx = shuffle_labels(rng, have); order[(ck, a)] = [have[i] for i in idx]; blob = {chr(65 + k): {'nodes': list(data[ck]['authors'][h]['r0'].values()), 'lint': data[ck]['authors'][h]['r0_lint']} for k, h in enumerate(order[(ck, a)])}
            if have: reqs.append(L.Req(f'{ck}__r1-{a}', m, f'Extraction:\n{cards[ck]}\n\nDrafts:\n{json.dumps(blob, ensure_ascii=False)}\n\nCritique and revise now.', sys1, None, e, 14000))
    st['prompt'] = 'pipeline/prompts/critique-revise-v2.md'; r1 = dispatch(M, 'draft_r1', reqs, mode)
    for ck in papers:
        for a, _, _ in AUTHORS:
            j = safe_json(r1.get(f'{ck}__r1-{a}') or L.Res('', False)); d = data[ck]['authors'][a]; d['critiques'] = (j or {}).get('critiques', []); d['r1'] = nodes_of((j or {}).get('revised')) or d['r0']; d['r1_lint'] = {i: lint(n, cn[ck]) for i, n in d['r1'].items()}
    # vote: Sol and Sonnet decide (counted), Inkling votes (benchmark only)
    reqs = []; vorder = {}
    for ck in papers:
        have = [a for a, _, _ in AUTHORS if data[ck]['authors'][a]['r1']]
        if len(have) < 2: continue
        for voter, m, e in VOTERS:
            idx = shuffle_labels(rng, have); vorder[(ck, voter)] = [have[i] for i in idx]; blob = {chr(65 + k): {'nodes': list(data[ck]['authors'][h]['r1'].values()), 'lint': data[ck]['authors'][h]['r1_lint']} for k, h in enumerate(vorder[(ck, voter)])}
            reqs.append(L.Req(f'{ck}__vote-{voter}', m, f'Extraction:\n{cards[ck]}\n\nVersions:\n{json.dumps(blob, ensure_ascii=False)}\n\nVote now.', sys2, None, e, 5000))
    st['prompt'] = 'pipeline/prompts/vote-v1.md'; rv = dispatch(M, 'draft_vote', reqs, mode); ties = []
    for ck in papers:
        votes = {}
        for voter in [v[0] for v in VOTERS]:
            j = safe_json(rv.get(f'{ck}__vote-{voter}') or L.Res('', False)); lab = {chr(65 + k): a for k, a in enumerate(vorder.get((ck, voter), []))}
            votes[voter] = {x['node']: {'author': lab.get(x.get('pick')), 'reason': x.get('reason', '')} for x in (j or {}).get('picks', []) if isinstance(x, dict) and x.get('node')}
        data[ck]['votes'] = votes
        for nid in {n for a in data[ck]['authors'].values() for n in a.get('r1', {})}:
            s, c = votes[VOTERS[0][0]].get(nid, {}).get('author'), votes[VOTERS[1][0]].get(nid, {}).get('author')
            if s and c and s != c: ties.append((ck, nid, s, c))
    reqs = []
    for ck in sorted({t[0] for t in ties}):
        mine = [t for t in ties if t[0] == ck]; blob = {nid: {'candidates': {a: data[ck]['authors'][a]['r1'].get(nid) for a in (s, c)}} for _, nid, s, c in mine}
        reqs.append(L.Req(f'{ck}__tie', R['tiebreak'], f'Extraction:\n{cards[ck]}\n\nTwo voters disagree. Candidates (author names are the keys); pick the better one for each node:\n{json.dumps(blob, ensure_ascii=False)}\n\nReturn {{"picks": [{{"node": "...", "pick": "<author name>", "reason": ""}}]}}.', sys2.replace('(A, B and C, in random order)', '(named by their authors)'), None, 'medium', 3000))
    rt = dispatch(M, 'draft_tie', reqs, mode)
    for ck in papers:
        j = safe_json(rt.get(f'{ck}__tie') or L.Res('', False)); tie = {x['node']: x.get('pick') for x in (j or {}).get('picks', []) if isinstance(x, dict)}; finals = {}
        for nid in {n for a in data[ck]['authors'].values() for n in a.get('r1', {})}:
            s, c = data[ck]['votes'][VOTERS[0][0]].get(nid, {}).get('author'), data[ck]['votes'][VOTERS[1][0]].get(nid, {}).get('author')
            win = s if s and s == c else (tie.get(nid) if tie.get(nid) in data[ck]['authors'] else (s or c or next((a for a in data[ck]['authors'] if nid in data[ck]['authors'][a].get('r1', {})), None)))
            how = 'Sol and Sonnet agree' if s and s == c else ('Neon tie-break' if tie.get(nid) in data[ck]['authors'] else 'single vote or fallback')
            node = data[ck]['authors'].get(win, {}).get('r1', {}).get(nid)
            if node: finals[nid] = {'node': node, 'author': win, 'how': how, 'lint': lint(node, cn[ck])}
        for nid, node in data[ck]['single']['nodes'].items(): finals[nid] = {'node': node, 'author': AUTHORS[0][0], 'how': 'single draft (not debated)', 'lint': lint(node, cn[ck])}
        data[ck]['finals'] = finals
    # claim-by-claim check: the first voter (the cheaper deciders, in registry order) that did not write the winner
    reqs = []
    for ck in papers:
        for chk, m, e in VOTERS:
            mine = [f['node'] for f in data[ck]['finals'].values() if f['author'] != chk and next((v[0] for v in VOTERS if v[0] != f['author']), None) == chk]
            if mine: reqs.append(L.Req(f'{ck}__check-{chk}', m, f'Extraction:\n{cards[ck]}\n\nNodes to check:\n{json.dumps(mine, ensure_ascii=False)}\n\nCheck now.', sys3, None, e, min(32000, 2000 + 450 * len(mine))))   # budget grows with the number of nodes to check
    st['prompt'] = 'pipeline/prompts/claim-check-v1.md'; rc = dispatch(M, 'draft_check', reqs, mode)
    # decision-model check of each final EVD (fidelity of the written text) and the Inkling benchmark drafts' lint
    evd = [(ck, nid, f) for ck in papers for nid, f in data[ck]['finals'].items() if f['node'].get('type') == 'EVD']
    def dm_evd(t):
        ck, nid, f = t; fnd = next((x for x in final_findings(M, ck)[0] if x['id'] == f['node'].get('source_id')), {})
        return run_dm(dm_state(M, {**fnd, 'statement': f['node'].get('statement', '')}, final_findings(M, ck)[1].get('questions', [])), {'fidelity': dm_questions(M, 'EVD statement')['fidelity'], 'quote_grounding': dm_questions(M)['quote_grounding']})
    with cf.ThreadPoolExecutor(6) as ex_: dres = list(ex_.map(dm_evd, evd))
    for (ck, nid, f), r in zip(evd, dres): f['dm'] = dm_summary(r)
    for ck in papers:
        for chk in [v[0] for v in VOTERS]:
            j = safe_json(rc.get(f'{ck}__check-{chk}') or L.Res('', False))
            for c in (j or {}).get('checks', []):
                if c.get('node') in data[ck]['finals']: data[ck]['finals'][c['node']]['claim_check'] = {'checker': chk, **c}
        for nid, f in data[ck]['finals'].items():
            cc = (f.get('claim_check') or {}).get('overall'); dmv = (f.get('dm') or {}).get('score')
            f['status'] = 'pass' if f['lint']['pass'] and cc == 'pass' and (dmv is None or dmv >= DM_LOW) else 'escalate to Opus and JP'
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
    'registration': ('Was the study preregistered?', 'not-applicable | not-disclosed | disclosed'),
    'protocol': ('Is a study protocol available?', 'not-applicable | not-disclosed | disclosed'),
    'ethical-approval': ('Is ethical approval or exemption stated?', 'disclosed | partial | not-disclosed | not-applicable'),
    'funding-disclosure': ('Is funding disclosed?', 'disclosed | partial | not-disclosed | not-applicable'),
    'coi-disclosure': ('Are conflicts of interest disclosed?', 'disclosed | partial | not-disclosed | not-applicable'),
    'code-check': ('Is analysis code shared and checked?', 'addressed | partial | not-addressed'),
    'data-repo-check': ('Are the data in a repository?', 'addressed | partial | not-addressed'),
}


def stage_qs(M, mode):
    key = 'qs'; st = M.m['stage_log'].setdefault(key, {})
    if st.get('status') == 'done': return
    sigs = '\n'.join(f'- `{k}`: {v[0]} Allowed values: {v[1]}.' for k, v in SIGNALS.items()); system = prompt('rate-signals-v1.md').replace('{SIGNALS}', sigs); st['prompt'] = 'pipeline/prompts/rate-signals-v1.md'; reqs = []
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        for r, m, e in RATERS: reqs.append(L.Req(f'{ck}__qs-{r}', m, 'Rate the paper now.', system, ex(p['pdf']), e, 9000))
    res = dispatch(M, 'qs', reqs, mode); allowed = {k: [x.strip() for x in v[1].split('|')] for k, v in SIGNALS.items()}; out = {}; raws = {}; disputes = {}
    def read(ck, p, res_, rater, doc, only=None):
        j = safe_json(res_.get(f'{ck}__qs-{rater}') or L.Res('', False)); got = {x.get('signal'): x for x in (j or {}).get('ratings', []) if isinstance(x, dict)}; rows = []
        for sg in SIGNALS:
            if only and sg not in only: continue
            x = got.get(sg); q = (x or {}).get('quote', ''); found = None if not x or q in ('', 'none') else bool(pp.find_quote(doc, q)['found']); rating = (x or {}).get('rating')
            rows.append({'paper': ck, 'signal': sg, 'rater': rater, 'counted': True, 'rating': rating if rating in allowed[sg] else ('invalid: ' + str(rating) if x else 'no answer'), 'quote': q, 'locator': (x or {}).get('locator', ''), 'quote_found': found, 'reason': (x or {}).get('reason', '')})
        return rows
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        doc = fitz.open(ex(p['pdf'])); raw = []
        for r in [x[0] for x in RATERS]: raw += read(ck, p, res, r, doc)
        doc.close(); raws[ck] = raw
        disputes[ck] = [sg for sg in SIGNALS if len({x['rating'] for x in raw if x['signal'] == sg}) > 1 or any(x['rating'] not in allowed[sg] for x in raw if x['signal'] == sg)]   # the two raters differ (or one gave no valid rating)
    reqs = []; sysa = prompt('adjudicate-signals-v1.md'); st['adjudicator_prompt'] = 'pipeline/prompts/adjudicate-signals-v1.md'
    for ck, sgs in disputes.items():
        if not sgs: continue
        sig = '\n'.join(f'- `{k}`: {SIGNALS[k][0]} Allowed values: {SIGNALS[k][1]}.' for k in sgs); rng_ = random.Random(M.m['run_id'] + ck); names = [x[0] for x in RATERS]; rng_.shuffle(names)
        shown = {f'Rater {i + 1}': [{k: x[k] for k in ('signal', 'rating', 'quote', 'locator')} for x in raws[ck] if x['rater'] == nm and x['signal'] in sgs] for i, nm in enumerate(names)}
        reqs.append(L.Req(f'{ck}__qs-{QS_ADJ["key"]}', QS_ADJ['model'], 'The two raters\' answers for the signals in dispute:\n' + json.dumps(shown, ensure_ascii=False) + '\n\nDecide now.', sysa.replace('{SIGNALS}', sig), ex(M.m['papers'][ck]['pdf']), QS_ADJ['effort'], 6000))
    res3 = dispatch(M, 'qs_adjudicate', reqs, mode) if reqs else {}
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        raw = raws[ck]
        if disputes[ck]:
            doc = fitz.open(ex(p['pdf'])); raw += read(ck, p, res3, QS_ADJ['key'], doc, only=set(disputes[ck])); doc.close()
        agg = []
        for sg in SIGNALS:
            votes = [x['rating'] for x in raw if x['signal'] == sg and x['counted'] and x['rating'] in allowed[sg]]; cnt = {}
            for v in votes: cnt[v] = cnt.get(v, 0) + 1
            top = sorted(cnt.items(), key=lambda kv: -kv[1]); maj = top[0][0] if top and (len(top) == 1 or top[0][1] > top[1][1]) and (top[0][1] >= 2) else 'no majority'
            agg.append({'paper': ck, 'signal': sg, 'votes': cnt, 'majority': maj, 'agreement': 'both raters agree' if sg not in disputes[ck] else ('Sol sided with one rater' if maj != 'no majority' else 'three different ratings'), 'adjudicated': sg in disputes[ck], 'quotes_not_found': sum(1 for x in raw if x['signal'] == sg and x['counted'] and x['quote_found'] is False)})
        out[ck] = {'raw': raw, 'aggregate': agg}; (M.dir / ck / 'quality_signals.json').write_text(json.dumps(out[ck], indent=1, ensure_ascii=False), encoding='utf-8')
    st['status'] = 'done'; st['summary'] = {ck: {'signals': len(v['aggregate']), 'disagreed': len(disputes[ck]), 'no_majority': sum(1 for a in v['aggregate'] if a['majority'] == 'no majority')} for ck, v in out.items()}; M.save(); M.event(f"quality signals: {st['summary']}")


def pdf_text(pdf):
    d = fitz.open(pdf); t = '\n\n'.join(f'[PDF page {i + 1}]\n{pp.page_text(pg)}' for i, pg in enumerate(d)); d.close(); return t

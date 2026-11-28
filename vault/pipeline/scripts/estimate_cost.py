#!/usr/bin/env python3
"""Cost ESTIMATE per paper under the model roles in pipeline/config/models.json (JP, 2026-11-27). Offline: no API call, no cost.
  python3 estimate_cost.py RUN [RUN ...] [--low-conf 0.2]
It reads each run's calls.jsonl (tokens in and out per call) and re-prices the same token counts at the models that the roles name now, at batch prices, step by step.
THIS IS AN ESTIMATE, NOT A MEASUREMENT. Assumptions that can be wrong (printed again under the table):
  1. Token counts are those of the old models. A new model may write more or fewer tokens (thinking tokens in particular), and tokenizers differ between providers.
  2. Quality signals: the one rater (roles.raters) is priced from the old Neon calls; the fallback rater (roles.qs_fallback) is priced as one request per rating group that sends the
     whole PDF again (input = the Neon input) and writes --low-conf (default 0.2) of the Neon output. The share of rows that the rater reports with low confidence is NOT known yet.
  3. Drafting: the critic sees one draft instead of three (the old input is used, so the estimate is on the high side); the vote and the node-detail check are re-priced from
     the old calls. Since 2026-11-27 (one author) there is no critique, vote or tiebreak: only the first drafts and the one-model draft of everything else are counted.
  4. Verification judge: calls of the old verify_sonnet step are re-priced at roles.verify_judge, with the output set to the mean output of a Sol medium call in the run's checks_vision
     stage (reasoning tokens), because a reasoning model writes more than the old Sonnet low-effort calls. Quality-rating verification calls are scaled by new raters / old raters.
     The verify_methods and verify_quality reruns of the old runs are not counted as a second pass (a fresh run verifies once).
  5. Mode: everything at batch prices (JP's instruction). The config also lists standard_stages (checks_vision, checks_opus, draft_rework, quote_check, verify_sonnet) that run in
     standard mode at list price even in a batch run; the 'as configured' line shows that.
  6. Not counted: failure analysis (the local classifier, price 0), question grouping (across papers), code-only checks (free), anything after the logged calls.
"""
import argparse, collections, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

RUNS = C.VAULT / 'pipeline' / 'runs'
EXCLUDED = ('failure_analysis', 'consolidate')                 # not part of the per-paper cost JP asked about
STANDARD = set(C.PIPE['limits'].get('standard_stages', []))
R = C.ROLES


def load_calls(run):
    f = RUNS / run / 'calls.jsonl'
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []


draft_labels = {}


def paper_of(rec):
    ck = rec.get('citekey') or ''
    if ck.startswith('g::'): return ck[3:].split('|')[0]
    if re.fullmatch(r'[vq]\d{4}', ck): return None            # verification item ids carry no paper: shared evenly
    return ck or None


def latest_cluster(recs, minutes=10):
    """Reruns of a step are logged one after another: keep the last group of calls (within `minutes` of the newest) per paper and model."""
    from datetime import datetime
    out = []; groups = collections.defaultdict(list)
    for r in recs: groups[(r['step'], r['model_id'], r.get('citekey'))].append(r)
    for g in groups.values():
        newest = max(datetime.fromisoformat(r['ts_utc']) for r in g)
        out += [r for r in g if (newest - datetime.fromisoformat(r['ts_utc'])).total_seconds() <= minutes * 60]
    return out


STAGE_OF = {'extraction (picost)': 'picost', 'recheck': 'recheck', 'adjudicate': 'adjudicate', 'checks_vision': 'checks_vision', 'checks_opus': 'checks_opus', 'quote_check': 'quote_check',
            'draft_r0 (first drafts)': 'draft_r0', 'draft_r0 (rest, one draft)': 'draft_r0', 'draft_r1 (critique)': 'draft_r1', 'draft_vote': 'draft_vote', 'draft_tie': 'draft_tie', 'draft_check (node details)': 'draft_check',
            'draft_rework': 'draft_rework', 'quality signals + TRIPOD (rater)': 'qs', 'quality signals + TRIPOD (fallback rater)': 'qs_fallback', 'verify (judge)': 'verify_sonnet'}   # label -> stage key in the config's standard_stages


def cost(model, tin, tout, batch=True):
    pi, po = C.price(model); return (tin * pi + tout * po) / 1e6 * (C.batch_discount(model) if batch else 1)


def draft_r0_labels(run):
    """Which draft_r0 call was a first draft and which was the one-model draft of everything else ('single'): the stage file has the request ids, the call log does not."""
    f = RUNS / run / 'stage_draft_r0.json'; lab = {}
    if f.exists():
        for rid, v in json.loads(f.read_text()).items():
            ck, _, name = rid.partition('__'); lab[(ck, v['tin'], v['tout'])] = 'single' if name == 'single' else name
    return lab


def new_calls(run, recs, old_raters, low_conf):
    """Re-price: list of (paper, step, new_model, tin, tout) for the roles in models.json. See the assumptions in the module docstring."""
    out = []; lab = draft_r0_labels(run)
    authors = C.role_list('authors'); debate = len(authors) > 1 and bool(R.get('voters')); critics = C.role_list('critics', 'authors') if debate else []; voters = C.role_list('voters') if debate else []; chk = C.role_list('node_check', 'authors'); raters = C.role_list('raters')
    vis = [r for r in recs if r['step'] == 'checks_vision']; judge = C.role_model(R.get('verify_judge') or R['quote_check'])
    judge_out = sum(r['tokens_out'] for r in vis) / len(vis) if vis else 800                       # proxy: output of a Sol medium call in this run
    by_step = collections.defaultdict(list)
    for r in recs: by_step[r['step']].append(r)
    for r in by_step['picost']: out.append((paper_of(r), 'extraction (picost)', R['extract'], r['tokens_in'], r['tokens_out']))
    for r in by_step['recheck']: out.append((paper_of(r), 'recheck', R['recheck'], r['tokens_in'], r['tokens_out']))
    for r in by_step['adjudicate']: out.append((paper_of(r), 'adjudicate', R['adjudicate'], r['tokens_in'], r['tokens_out']))
    for r in by_step['checks_vision']: out.append((paper_of(r), 'checks_vision', R['vision_check'], r['tokens_in'], r['tokens_out']))
    for r in by_step['checks_opus']: out.append((paper_of(r), 'checks_opus', R['vision_dispute'], r['tokens_in'], r['tokens_out']))
    for r in by_step['quote_check']: out.append((paper_of(r), 'quote_check', C.role_model(R['quote_check']), r['tokens_in'], r['tokens_out']))
    for r in by_step['draft_r0']:
        kind = lab.get((paper_of(r), r['tokens_in'], r['tokens_out']), '')
        if kind == 'single': out.append((paper_of(r), 'draft_r0 (rest, one draft)', authors[0][1], r['tokens_in'], r['tokens_out']))
        elif r['model_id'] in {a[1] for a in authors}: out.append((paper_of(r), 'draft_r0 (first drafts)', r['model_id'], r['tokens_in'], r['tokens_out']))
    for r in by_step['draft_r1']:
        if r['model_id'] in {a[1] for a in critics}: out.append((paper_of(r), 'draft_r1 (critique)', r['model_id'], r['tokens_in'], r['tokens_out']))
    leftovers = collections.defaultdict(list)
    by_step_vote = by_step['draft_vote'] if debate else []                                                   # vote: keep calls of models that still vote; re-price the others for the new voters
    for r in by_step_vote: leftovers[paper_of(r)].append(r)
    for ck, rs in leftovers.items():
        new = [v[1] for v in voters]; spare = []
        for r in rs:
            if r['model_id'] in new: new.remove(r['model_id']); out.append((ck, 'draft_vote', r['model_id'], r['tokens_in'], r['tokens_out']))
            else: spare.append(r)
        for r, m in zip(spare, new): out.append((ck, 'draft_vote', m, r['tokens_in'], r['tokens_out']))
    for r in by_step['draft_tie'] if debate else []: out.append((paper_of(r), 'draft_tie', R.get('tiebreak') or voters[0][1], r['tokens_in'], r['tokens_out']))
    for r in by_step['draft_check']: out.append((paper_of(r), 'draft_check (node details)', chk[0][1], r['tokens_in'], r['tokens_out']))
    for r in by_step['draft_rework']: out.append((paper_of(r), 'draft_rework', C.role_model(R['evd_rework']), r['tokens_in'], r['tokens_out']))
    fb = R.get('qs_fallback')
    for r in by_step['qs']:
        if r['model_id'] in {a[1] for a in raters}:
            out.append((paper_of(r), 'quality signals + TRIPOD (rater)', r['model_id'], r['tokens_in'], r['tokens_out']))
            if fb: out.append((paper_of(r), 'quality signals + TRIPOD (fallback rater)', fb['model'], r['tokens_in'], int(r['tokens_out'] * low_conf)))
    for r in by_step['verify_sonnet']: out.append((paper_of(r), 'verify (judge)', judge, r['tokens_in'], judge_out))
    scale = len(raters) / max(old_raters, 1)
    alt = C.role_model(R['verify_judge_alt']) if R.get('verify_judge_alt') else judge
    for r in by_step['verify_quality']:   # ratings by the fallback rater (Sol) are judged by the second judge (Neon); the others by the first judge (Sol)
        out.append((paper_of(r), 'verify (judge)', judge, r['tokens_in'] * scale * (1 - low_conf), judge_out * scale * (1 - low_conf)))
        out.append((paper_of(r), 'verify (judge)', alt, r['tokens_in'] * scale * low_conf, judge_out * scale * low_conf))
    return out


def old_calls(recs):
    """The old procedure, same logs, same batch pricing: reruns of the quality-signal stage removed, verify_methods (a rerun) left out. Steps get the same labels as the new roles so the table lines up."""
    lab = {'picost': 'extraction (picost)', 'draft_r1': 'draft_r1 (critique)', 'draft_check': 'draft_check (node details)', 'qs': 'quality signals + TRIPOD (rater)', 'qs_adjudicate': 'quality signals + TRIPOD (fallback rater)', 'verify_sonnet': 'verify (judge)', 'verify_quality': 'verify (judge)'}
    out = []
    for r in recs:
        if r['step'] == 'verify_methods': continue
        s = lab.get(r['step'], r['step'])
        if r['step'] == 'draft_r0': s = 'draft_r0 (rest, one draft)' if draft_labels.get((paper_of(r), r['tokens_in'], r['tokens_out'])) == 'single' else 'draft_r0 (first drafts)'
        out.append((paper_of(r), s, r['model_id'], r['tokens_in'] or 0, r['tokens_out'] or 0))
    return out


def per_paper(calls, papers, batch_only=True):
    """{paper: {step: usd}} with calls that belong to no paper (verification items) shared evenly."""
    d = {p: collections.Counter() for p in papers}; shared = collections.Counter()
    for ck, step, model, tin, tout in calls:
        std = (STAGE_OF.get(step) in STANDARD) and not batch_only
        c = cost(model, tin or 0, tout or 0, batch=not std)
        if ck in d: d[ck][step] += c
        elif ck is None: shared[step] += c
    for step, c in shared.items():
        for p in papers: d[p][step] += c / len(papers)
    return d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('runs', nargs='+'); ap.add_argument('--low-conf', type=float, default=0.2, help='assumed share of ratings the first rater reports with low confidence (default 0.2)')
    a = ap.parse_args(); print('ESTIMATE ONLY: old token counts re-priced at the roles in models.json, batch prices; see the assumptions at the top of estimate_cost.py\n')
    print('roles: ' + '; '.join(f"{k} = {C.role_display(v) if not isinstance(v, list) else ', '.join(C.role_display(x) for x in v)}" for k, v in R.items() if k in ('extract', 'recheck', 'adjudicate', 'tiebreak', 'authors', 'critics', 'voters', 'raters', 'qs_fallback', 'node_check', 'evd_rework', 'verify_judge', 'quote_check')) + '\n')
    pool = []; pool_std = []
    for run in a.runs:
        recs = [r for r in load_calls(run) if not r['step'].startswith(EXCLUDED)]
        recs = [r for r in recs if r['step'] not in ('qs', 'qs_adjudicate')] + latest_cluster([r for r in recs if r['step'] in ('qs', 'qs_adjudicate')])
        papers = sorted({paper_of(r) for r in recs if r['step'] == 'qs' and paper_of(r)}); started = sorted({paper_of(r) for r in recs if r['step'] == 'picost'} - set(papers))
        old_raters = len({r['model_id'] for r in recs if r['step'] == 'qs'}) or 1
        if not papers: print(run, 'has no complete paper (no quality-signal calls)'); continue
        new = per_paper(new_calls(run, recs, old_raters, a.low_conf), papers); draft_labels.clear(); draft_labels.update(draft_r0_labels(run)); old = per_paper(old_calls(recs), papers)
        print(f'== {run}: {len(papers)} complete paper(s)' + (f'; {len(started)} paper(s) only reached extraction in this run and are left out ({", ".join(s[:12] for s in started)})' if started else ''))
        steps = sorted({s for p in papers for s in set(new[p]) | set(old[p])}, key=lambda s: -sum(new[p][s] for p in papers))
        print(f'  {"step":46s} {"old roles":>10s} {"new roles":>10s}   (USD per paper, mean over the papers)')
        for s in steps: print(f'  {s:46s} {sum(old[p][s] for p in papers) / len(papers):10.3f} {sum(new[p][s] for p in papers) / len(papers):10.3f}')
        tot = lambda d, p: sum(d[p].values())
        print(f'  {"TOTAL per paper (mean)":46s} {sum(tot(old, p) for p in papers) / len(papers):10.3f} {sum(tot(new, p) for p in papers) / len(papers):10.3f}')
        for p in papers: print(f'    {p[:46]:46s} {tot(old, p):10.3f} {tot(new, p):10.3f}')
        narrow = ('extraction (picost)', 'recheck', 'adjudicate', 'quality signals + TRIPOD (rater)', 'quality signals + TRIPOD (fallback rater)')
        print(f'  of which extraction + recheck + adjudication + quality signals + TRIPOD only (no drafting, screenshot checks, quote check or verification): old {sum(sum(old[p][s] for s in narrow) for p in papers) / len(papers):.3f}, new {sum(sum(new[p][s] for s in narrow) for p in papers) / len(papers):.3f}')
        asconf = per_paper(new_calls(run, recs, old_raters, a.low_conf), papers, batch_only=False)
        print(f'  as configured (standard stages at list price, the rest batch): mean {sum(tot(asconf, p) for p in papers) / len(papers):.3f} per paper')
        for lc in (0.1, 0.2, 0.4, 0.6):
            n2 = per_paper(new_calls(run, recs, old_raters, lc), papers); print(f'  if {int(lc * 100)}% of ratings are low confidence: mean {sum(tot(n2, p) for p in papers) / len(papers):.3f} per paper (all batch)')
        pool += [tot(new, p) for p in papers]; pool_std += [tot(asconf, p) for p in papers]; print()
    if len(a.runs) > 1 and pool: print(f'POOLED estimate over {len(pool)} complete papers of all the runs: mean {sum(pool) / len(pool):.3f} USD per paper (min {min(pool):.3f}, max {max(pool):.3f}); with the standard-mode stages at list price: {sum(pool_std) / len(pool_std):.3f}')
    print('JP target: at most 2.49 USD per paper. All numbers above are estimates.')


if __name__ == '__main__': main()

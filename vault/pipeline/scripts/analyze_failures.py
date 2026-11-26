#!/usr/bin/env python3
"""Sample verification failures and have Claude Opus 5.5 classify them (JP, 2026-11-26), so the types and frequencies can be checked by a person. Writes runs/<run>/failure_analysis.json (shown in the review sheet tab "Failure analysis (sampled)") with the cell that locates each item in "Verification (all nodes)". Usage: analyze_failures.py RUN [PER_TYPE]"""
import collections, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lives_run as LR, lives_stages as S, lives_verify as V, llm_batch as L, decision_models as dm
dm.load_env(); R = S.R


def main(run, per_type=10):
    M = LR.Manifest(run); items = json.loads((M.dir / 'verification.json').read_text(encoding='utf-8')); fresh, _ = V.build_items(M)
    for a, b in zip(fresh, items): b['_passage'] = (a.get('passage') or a['item'])[:6000]; b['_item'] = a['item']
    ordered = V.queue_order(items); row = {id(x): i + 2 for i, x in enumerate(ordered)}
    def failed(x):
        sc = x['scores']; return any((sc.get(k) is not None and sc[k] < 0.5) for k in ('sonnet', 'perplexity', 'liquid'))
    pool = collections.defaultdict(list)
    for x in items:
        if x['ntype'] == 'QUOTE' or not failed(x): continue
        pool[x['ntype']].append(x)
    rnd = random.Random(2026); sample = []
    for t, xs in pool.items(): sample += rnd.sample(xs, min(per_type, len(xs)))
    sysv = S.prompt('failure-types-v1.md'); reqs = []
    for i, x in enumerate(sample):
        sc = {k: (round(v, 2) if v is not None else None) for k, v in x['scores'].items() if k in ('sonnet', 'perplexity', 'liquid')}
        body = f"ITEM TYPE: {x['ntype']}\nWHAT WAS CHECKED: {x['what']}\n\nITEM:\n{x['_item'][:2500]}\n\nPASSAGE:\n{x['_passage']}\n\nVERIFIER SCORES: {json.dumps(sc)}\nSonnet 5.5 reason: {x['reasons'].get('sonnet', '')}"
        reqs.append(L.Req(f'fa{i:03d}', R['adjudicate'], body, sysv, None, 'medium', 900))
    res = S.dispatch(M, 'failure_analysis', reqs, 'standard'); out = []
    for i, x in enumerate(sample):
        j = S.safe_json(res.get(f'fa{i:03d}') or L.Res('', False)) or {}
        out.append({'paper': x['paper'], 'ntype': x['ntype'], 'nid': x['nid'], 'row': row[id(x)], 'item': x['text'][:500], 'passage': x.get('passage', '')[:400], 'scores': x['scores'], 'sonnet_reason': x['reasons'].get('sonnet', ''), 'who_is_right': j.get('who_is_right', ''), 'failure_type': j.get('failure_type', ''), 'reason': j.get('reason', ''), 'fix': j.get('fix', '')})
    (M.dir / 'failure_analysis.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
    M.m['stage_log'].setdefault('failure_analysis', {}).update(status='done', sampled=len(out)); M.save()
    pool_n = {t: len(v) for t, v in pool.items()}; print(run, 'failing items by type (excluding QUOTE):', pool_n, 'sampled', len(out))
    c = collections.Counter((o['ntype'], o['failure_type']) for o in out)
    for k, n in sorted(c.items()): print(' ', k, n)
    print(' who is right:', dict(collections.Counter((o['ntype'], o['who_is_right']) for o in out)))


if __name__ == '__main__': main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)


def refresh_rows(run):
    """Recompute the sheet row of each sampled item after a change in the row order (no new model calls)."""
    M = LR.Manifest(run); items = json.loads((M.dir / 'verification.json').read_text(encoding='utf-8')); ordered = V.queue_order(items)
    pos = {(x['paper'], x['ntype'], x['nid']): i + 2 for i, x in enumerate(ordered)}
    fa = json.loads((M.dir / 'failure_analysis.json').read_text(encoding='utf-8'))
    for o in fa: o['row'] = pos[(o['paper'], o['ntype'], o['nid'])]
    (M.dir / 'failure_analysis.json').write_text(json.dumps(fa, indent=1, ensure_ascii=False), encoding='utf-8')

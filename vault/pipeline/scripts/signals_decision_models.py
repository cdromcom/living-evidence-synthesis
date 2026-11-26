#!/usr/bin/env python3
"""Ask the decision models whether each TRIPOD-LLM / Quality appraisal row is supported by its own quote.
For every row with a quote: (1) does the quote support the rating given, (2) which rating does the quote itself support, (3) is the quote about this item.
Writes JSON lines (one per row and model) to --out. Resumable. Costs cents: the text per call is about 300 tokens.

  python3 signals_decision_models.py --only @citekey [--providers perplexity,liquid] [--limit N] [--out FILE]"""
import argparse, json, os
from datetime import datetime, timezone
from pathlib import Path
import decision_models as dm, signals_common as sc

ap = argparse.ArgumentParser()
ap.add_argument('--only'); ap.add_argument('--providers', default='perplexity,liquid'); ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--out', default=str(sc.VAULT / 'pipeline/misc/evd-validation/signal-runs/decision-models.jsonl')); ap.add_argument('--run-id', default='sig1'); ap.add_argument('--workers', type=int, default=6)
a = ap.parse_args(); dm.load_env()
RATINGS = {'Addressed': 'The paper fully reports the item (reporting items) or shows no meaningful threat (risk-of-bias domains and checklist items).',
           'Partly addressed': 'The paper reports the item only in part, or there is a real but non-fatal limitation.',
           'Not addressed': 'The paper does not report the item, or there is a significant unaddressed gap.'}
Q = {'rating_supported': dm.noul('Does the QUOTE support the RATING given for this item?'),
     'rating': dm.choice('Which rating does the QUOTE itself support for this item?', RATINGS),
     'quote_about_item': dm.noul('Is the QUOTE about the ITEM named above (rather than about something else)?')}
out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
done = {(r['citekey'], r['kind'], r['row'], r['provider']) for r in map(json.loads, out.read_text().splitlines()) if not r.get('error')} if out.exists() else set()
import threading
from concurrent.futures import ThreadPoolExecutor
lock = threading.Lock(); jobs = []
for path in sorted(sc.SRC_DIR.glob('@*.md')):
    if a.only and path.stem.lstrip('@') != a.only.lstrip('@'): continue
    for r in sc.source_rows(path):
        if not r['quote'] or r['rating'] not in RATINGS: continue
        if a.limit and len({(j[0]['citekey'], j[0]['kind'], j[0]['row']) for j in jobs}) >= a.limit: break
        for pv in a.providers.split(','):
            if (r['citekey'], r['kind'], r['row'], pv) not in done: jobs.append((r, pv))


def work(job):
    r, pv = job
    state = (f"SOURCE PAPER: {r['citekey']}\n{'TRIPOD-LLM reporting item' if r['kind'] == 'TRIPOD' else 'Quality appraisal domain'}: {r['row']}. {r['item']}\n"
             f"RATING GIVEN BY THE CURATOR: {r['rating']}\nQUOTE FROM THE PAPER (verbatim, locator {r['locator'] or 'none'}):\n{r['quote']}")
    resp, err = dm.decide(pv, state, Q)
    rec = {'run_id': a.run_id, 'citekey': r['citekey'], 'kind': r['kind'], 'row': r['row'], 'provider': pv, 'model': dm.MODELS[pv],
           'ts': datetime.now(timezone.utc).isoformat(), 'curator_rating': r['rating'], 'error': err,
           'answers': (resp or {}).get('answers'), 'usage': (resp or {}).get('usage')}
    with lock:
        with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
    return err


with ThreadPoolExecutor(a.workers) as ex: errs = list(ex.map(work, jobs))
print(f'{len(jobs)} calls ({sum(1 for e in errs if e)} errors); records in {out}')

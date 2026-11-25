#!/usr/bin/env python3
"""Open-access status for the DOIs of the screened papers, from OpenAlex (free, no key; only public DOIs are sent) (JP, 2026-11-25).
  python3 oa_lookup.py            # reads ~/.cache/lives-bench/screening/all/docs.jsonl, writes .../all/oa.json {doi: {oa, status, url}}; resumes
OpenAlex is_oa = a free full-text copy exists somewhere (gold, green, hybrid, bronze). Papers without a DOI are not looked up (reported as unknown)."""
import json, time, urllib.parse, urllib.request
from pathlib import Path
W = Path.home() / '.cache/lives-bench/screening/all'
def main():
    docs = [json.loads(l) for l in open(W / 'docs.jsonl')]; dois = sorted({d['doi'].lower().replace('https://doi.org/', '') for d in docs if d.get('kind') == 'paper' and d.get('doi') and d['doi'].startswith('10.')})
    out = json.load(open(W / 'oa.json')) if (W / 'oa.json').exists() else {}; todo = [d for d in dois if d not in out]; print(len(dois), 'DOIs;', len(todo), 'to look up', flush=True)
    for i in range(0, len(todo), 40):
        b = todo[i:i + 40]; url = 'https://api.openalex.org/works?per-page=50&select=doi,open_access&filter=doi:' + '|'.join(urllib.parse.quote(x, safe='/') for x in b)
        for attempt in range(4):
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'lives-screening/1.0'}), timeout=60)); break
            except Exception as e:
                time.sleep(5 * (attempt + 1)); r = None
        if r is None: print('failed batch', i, flush=True); continue
        got = {}
        for w in r.get('results', []):
            oa = w.get('open_access') or {}; got[(w.get('doi') or '').lower().replace('https://doi.org/', '')] = {'oa': bool(oa.get('is_oa')), 'status': oa.get('oa_status', ''), 'url': oa.get('oa_url') or ''}
        for x in b: out[x] = got.get(x, {'oa': None, 'status': 'not found', 'url': ''})
        json.dump(out, open(W / 'oa.json', 'w')); print(f'  {min(i + 40, len(todo))}/{len(todo)}', flush=True); time.sleep(0.2)
    c = {}
    for v in out.values(): c[str(v['oa'])] = c.get(str(v['oa']), 0) + 1
    print('done', c)
if __name__ == '__main__': main()

#!/usr/bin/env python3
"""FAIR-Checker (https://fair-checker.france-bioinformatique.fr, REST API, no key): 12 metrics scored 0 to 2, reported as Findable (F1A F1B F2A F2B),
Accessible (A11 A12), Interoperable (I1 I2 I3) and Reusable (R11 R12 R13) with their own totals. No top-up is added to the score.
F-UJI (https://www.f-uji.net) is probed as a second assessor; its web page posts to the server itself and the API needs credentials, so it is skipped
unless a public API answers without a key.
  python3 fair_checker.py <dataset-url>"""
import json, sys
from _http import fetch, request_json_meta

T = 'https://w3id.org/ftr#TestResult'; V = 'http://www.w3.org/ns/prov#value'; OUT = 'https://w3id.org/ftr#outputFromTest'
GROUPS = {'F': ('Findable', ['F1A', 'F1B', 'F2A', 'F2B']), 'A': ('Accessible', ['A11', 'A12']), 'I': ('Interoperable', ['I1', 'I2', 'I3']), 'R': ('Reusable', ['R11', 'R12', 'R13'])}


def parse_results(d) -> list:
    """[{id, value}] for every TestResult in the FAIR-Checker JSON-LD. id is None when the service did not name the metric."""
    out = []
    for r in d or []:
        if T in (r.get('@type') or []) and r.get(V):
            mid = ((r.get(OUT) or [{}])[0].get('@id') or '').rsplit('/', 1)[-1]
            out.append({'id': mid if mid and mid != 'None' else None, 'value': int(r[V][0]['@value'])})
    return out


def group_fair(results: list) -> dict:
    """Group metric results by FAIR letter. Each group: name, score, max (2 per metric), metrics found, complete."""
    byid = {r['id']: r['value'] for r in results if r['id']}
    out = {}
    for k, (name, ids) in GROUPS.items():
        got = {i: byid[i] for i in ids if i in byid}
        out[k] = {'name': name, 'score': sum(got.values()) if len(got) == len(ids) else None, 'max': 2 * len(ids), 'metrics': got, 'complete': len(got) == len(ids)}
    out['metrics_without_id'] = sum(1 for r in results if not r['id'])
    return out


def check(url: str) -> dict:
    res = None
    for attempt in range(3):   # the service sometimes returns results without metric names; ask again (not cached)
        r = fetch('GET', 'https://fair-checker.france-bioinformatique.fr/api/check/metrics_all', params={'url': url}, timeout=180, retries=2, cache=False)
        meta = {'http_status': r['status'], 'response_sha256': r['sha256'], 'elapsed_seconds': r['elapsed']}
        if r['status'] != 200: return {'url': url, 'assessed': False, 'error': r['error'] or f"HTTP {r['status']}", **meta}
        try: res = parse_results(json.loads(r['text']))
        except ValueError: return {'url': url, 'assessed': False, 'error': 'response was not JSON', **meta}
        if res and all(x['id'] for x in res): break
    g = group_fair(res)
    return {'url': url, 'assessed': True, 'metrics_scored': len(res), 'raw_total': sum(x['value'] for x in res), 'raw_max': 2 * len(res), 'groups': g,
            'attempts': attempt + 1, 'api': 'https://fair-checker.france-bioinformatique.fr/api/check/metrics_all', **meta}


def fuji_probe() -> dict:
    """F-UJI public instance: report whether an API that answers without a key exists. Sends no dataset URL."""
    r = fetch('GET', 'https://www.f-uji.net/fuji/api/v1/ui/', retries=1, cache=False)
    ok = r['status'] == 200
    return {'available_without_key': ok, 'probed': 'https://www.f-uji.net/fuji/api/v1/ui/', 'http_status': r['status'],
            'note': None if ok else 'The public f-uji.net site is a web form that calls its server with its own credentials; no keyless API answered, so F-UJI was skipped.'}


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1]), indent=1)); print(json.dumps(fuji_probe(), indent=1))

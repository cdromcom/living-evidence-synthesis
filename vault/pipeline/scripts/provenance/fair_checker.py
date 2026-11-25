#!/usr/bin/env python3
"""Data Quality via FAIR-Checker's REST API (12 metrics scored 0 to 2, total 0 to 24; no key). For a dataset hosted on github.com or gitlab.com the
raw score is uninformative (no schema.org metadata), so add 2 if the repo has a real licence (pass --license-found from howfairis_check). See Vault-structure.md.
  python3 fair_checker.py <dataset-url> [--license-found]"""
import json, sys
from _http import request_json
T = 'https://w3id.org/ftr#TestResult'; V = 'http://www.w3.org/ns/prov#value'


def check(url: str, license_found: bool = False) -> dict:
    d, err = request_json('GET', 'https://fair-checker.france-bioinformatique.fr/api/check/metrics_all', params={'url': url}, timeout=180)
    if d is None: return {'top/data-quality-fair': None, 'error': err}
    vals = [int(r[V][0]['@value']) for r in d if T in (r.get('@type') or []) and r.get(V)]
    raw = sum(vals); host = any(h in url for h in ('github.com', 'gitlab.com'))
    top = 2 if (host and license_found) else 0
    return {'url': url, 'metrics_scored': len(vals), 'raw_score': raw, 'top_up': top, 'top/data-quality-fair': min(24, raw + top) if len(vals) == 12 else None,
            'note': 'GitHub/GitLab host: +2 if a licence exists' if host else 'native score'}


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1], '--license-found' in sys.argv), indent=1))

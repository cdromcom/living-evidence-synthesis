"""Tiny HTTP helper for the provenance scripts: retries, a generic User-Agent (no personal details), JSON in and out."""
import time
import requests
UA = {'User-Agent': 'LIVES-provenance/1.0 (research tool; https://github.com/cdromcom/living-evidence-synthesis)'}


def request_json(method, url, retries=4, **kw):
    err = None
    for i in range(retries):
        try:
            r = requests.request(method, url, headers={**UA, **kw.pop('headers', {})}, timeout=kw.pop('timeout', 45), **kw)
        except requests.RequestException as e:
            err = str(e)
        else:
            if r.status_code == 200: return r.json(), None
            if r.status_code == 404: return None, 'not found'
            err = f'HTTP {r.status_code}'
            if r.status_code not in (429, 500, 502, 503, 504): return None, err
        time.sleep(2 ** i)
    return None, err

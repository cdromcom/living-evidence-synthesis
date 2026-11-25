"""Minimal client for the three decision models (Perplexity Decider 1.3, Liquid d1-ultra, Jev), text only. Keys come from
~/.config/lives-ai-raters/.env (PERPLEXITY_API_KEY, LIQUID_API_KEY, TYPESAFE_API_KEY); never print or commit them.
Same request shapes as benchmarking-validation/run_raters.py. A question is noul(...) (returns a probability) or choice(...)."""
import os, time
from pathlib import Path
import requests

MODELS = {'perplexity': 'pplx-decider-v1.3', 'liquid': 'd1-ultra', 'jev': 'jev-1.14.0'}
KEY_ENV = {'perplexity': 'PERPLEXITY_API_KEY', 'liquid': 'LIQUID_API_KEY', 'jev': 'TYPESAFE_API_KEY'}
PRICE_PER_M = {'perplexity': 0.02, 'liquid': 0.042, 'jev': 0.042}   # USD per million input tokens, list prices (2026-11-23)


def load_env(path=None):
    p = Path(path or Path.home() / '.config' / 'lives-ai-raters' / '.env')
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip().strip('"\''))


def noul(q): return {'type': 'noul', 'instructions': q}
def choice(q, opts): return {'type': 'choice', 'instructions': q, 'criteria': opts}


def request_for(provider, state: str, questions: dict):
    m = MODELS[provider]; key = os.environ.get(KEY_ENV[provider], '')
    if provider == 'perplexity':
        return ('https://api.perplexity.ai/v1/decisions', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': [state], 'questions': questions})
    if provider == 'liquid':
        return ('https://api.liquid.ai/decisions/v1/systemone', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': state, 'questions': questions})
    if provider == 'jev':
        return ('https://api.typesafe.ai/v1/systemone', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': state, 'questions': questions})
    raise ValueError(provider)


def decide(provider, state, questions, retries=4):
    """Returns (response_json, error). Retries on rate limits and server errors."""
    url, headers, body = request_for(provider, state, questions); err = None
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=120)
        except requests.RequestException as e:
            err = str(e)
        else:
            if r.status_code == 200: return r.json(), None
            err = f'HTTP {r.status_code}: {r.text[:300]}'
            if r.status_code not in (429, 500, 502, 503, 504, 529): return None, err
        time.sleep(2 ** attempt * 2)
    return None, err

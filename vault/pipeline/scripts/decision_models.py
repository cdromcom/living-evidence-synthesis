"""Minimal client for the two decision models (Perplexity Decider 1.3, Liquid d1.2-ultra (was d1-ultra until 2026-11-26); Jev was dropped on 2026-11-26), text only. Keys come from
~/.config/lives-ai-raters/.env (PERPLEXITY_API_KEY, LIQUID_API_KEY); never print or commit them.
Same request shapes as benchmarking-validation/run_raters.py. A question is noul(...) (returns a probability) or choice(...)."""
import os, time
from pathlib import Path
import requests

MODELS = {'perplexity': 'pplx-decider-v1.3', 'liquid': 'd1.2-ultra', 'baseten': 'decision-models/baseten-bison-latest'}
KEY_ENV = {'perplexity': 'PERPLEXITY_API_KEY', 'liquid': 'LIQUID_API_KEY', 'baseten': 'BASETEN_API_KEY'}
PRICE_PER_M = {'perplexity': 0.02, 'liquid': 0.042, 'baseten': 0.10}   # USD per million input tokens, list prices (2026-11-23; baseten bison-1 added 2026-11-27)


def load_env(path=None):
    p = Path(path or Path.home() / '.config' / 'lives-ai-raters' / '.env')
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip().strip('"\''))


def noul(q): return {'type': 'noul', 'instructions': q}
def choice(q, opts): return {'type': 'choice', 'instructions': q, 'criteria': opts}


def image_data_url(path, max_side=1600):
    """JPEG data URL (Liquid d1.2 takes base64 images, at most 4.5 MB per request in all)."""
    import base64, io
    from PIL import Image
    im = Image.open(path).convert('RGB'); im.thumbnail((max_side, max_side)); b = io.BytesIO(); im.save(b, 'JPEG', quality=85)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def request_for(provider, state: str, questions: dict, images=None):
    m = MODELS[provider]; key = os.environ.get(KEY_ENV[provider], '')
    if provider == 'perplexity':
        return ('https://api.perplexity.ai/v1/decisions', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': [state], 'questions': questions})
    if provider == 'liquid':
        return ('https://api.liquid.ai/decisions/v1/systemone', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': state, 'questions': questions, **({'images': [image_data_url(p) for p in images]} if images else {})})   # Perplexity Decider is text only: images are sent to Liquid only
    if provider == 'baseten':   # bison-1 on Baseten Model APIs; images go inside state.messages (at most 16 per request)
        content = [{'type': 'text', 'text': state}] + [{'type': 'image_url', 'image_url': {'url': image_data_url(p)}} for p in (images or [])]
        return ('https://inference.baseten.co/v1/systemone', {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                {'model': m, 'state': {'messages': [{'role': 'user', 'content': content}]}, 'questions': questions})
    raise ValueError(provider)


def decide(provider, state, questions, retries=4, images=None):
    """Returns (response_json, error). Retries on rate limits and server errors."""
    url, headers, body = request_for(provider, state, questions, images); err = None
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

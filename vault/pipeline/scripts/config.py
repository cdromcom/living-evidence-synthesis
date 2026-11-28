#!/usr/bin/env python3
"""Reads pipeline/config/models.json and pipeline/config/pipeline.json (JP, 2026-11-25). One place for model ids, prices, roles, limits and the origin policy.
  from config import MODELS, ROLES, PIPE, price, display, provider_of, assert_allowed
Scripts must not hard-code a model id, a price or a limit; they read them here, so swapping a model is a one-line edit of models.json."""
import json, os
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2]); CFG = VAULT / 'pipeline' / 'config'
REG = json.loads((CFG / 'models.json').read_text(encoding='utf-8')); PIPE = json.loads((CFG / 'pipeline.json').read_text(encoding='utf-8'))
MODELS = REG['models']; ROLES = REG['roles']; POLICY = REG['policy']; EMBEDDING = REG['embedding_models']['list']
def price(model): m = MODELS[model]; return m['price_in'], m['price_out']
def display(model): return MODELS.get(model, {}).get('display', model)
def provider_of(model): return MODELS.get(model, {}).get('provider')
def max_output(model, batch=True):
    """Largest output budget (answer plus thinking) for one request to this model: max_output_tokens from models.json (64000 if not listed). Gemini batch refuses more than 65536 and llm_batch clamps to 65000, so batch mode uses 65000 for Google models."""
    m = MODELS[model].get('max_output_tokens', 64000)
    return min(m, 65000) if batch and provider_of(model) == 'google' else m
def batch_discount(model): return MODELS[model].get('batch_discount', 1.0)
def assert_allowed(model):
    """Enforce the origin policy: a hosted API model must come from an allowed country; local open-weight models may come from anywhere the policy allows."""
    m = MODELS.get(model)
    if m is None: raise ValueError(f'{model} is not in pipeline/config/models.json')
    if m['runs'] == 'api' and m['country'] not in POLICY['hosted_api_allowed_countries'] and 'any' not in POLICY['hosted_api_allowed_countries']:
        raise ValueError(f"{model}: hosted APIs from {m['country']} are not allowed by the model-origin policy")
    return True


# Roles (models.json) are a model id or an object {key, model, effort}; the helpers below read either form (JP, 2026-11-27).
def role_model(x): return x['model'] if isinstance(x, dict) else x
def role_effort(x, default='medium'): return (x.get('effort') or default) if isinstance(x, dict) else default
def role_list(name, default=None):
    """A role that holds a list of {key, model, effort} as (key, model, effort) tuples; `default` (another role name) is used when the role is missing, so older configurations keep working."""
    v = ROLES.get(name) or (ROLES.get(default) if default else None) or []
    return [(a['key'], a['model'], a.get('effort', 'medium')) for a in v]
def role_display(x): return display(role_model(x))
def short(x):
    """Short model name for labels: 'Sol', 'Neon', 'Sonnet 5.5', 'Opus 5.5' (the display name without the developer prefix)."""
    return role_display(x).replace('Claude ', '').replace('Gemini 4 ', '').replace('GPT-6.2 ', '')

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
def batch_discount(model): return MODELS[model].get('batch_discount', 1.0)
def assert_allowed(model):
    """Enforce the origin policy: a hosted API model must come from an allowed country; local open-weight models may come from anywhere the policy allows."""
    m = MODELS.get(model)
    if m is None: raise ValueError(f'{model} is not in pipeline/config/models.json')
    if m['runs'] == 'api' and m['country'] not in POLICY['hosted_api_allowed_countries'] and 'any' not in POLICY['hosted_api_allowed_countries']:
        raise ValueError(f"{model}: hosted APIs from {m['country']} are not allowed by the model-origin policy")
    return True

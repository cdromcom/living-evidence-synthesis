#!/usr/bin/env python3
"""Consult two model families on a one-page design and dev summary, then let two other models improve the plan using both critiques.
Every call is logged with call_logger.py. Uses the keys in ~/.config/lives-ai-raters/.env (about $0.5 in total).
  python3 design_consult.py --run-id 2026-11-25-design-consult --prompt pipeline/prompts/design-consult-v1.md --enhance pipeline/prompts/design-enhance-v1.md"""
import argparse, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import call_logger as cl

ap = argparse.ArgumentParser(); ap.add_argument('--run-id', required=True); ap.add_argument('--prompt', required=True); ap.add_argument('--enhance', required=True)
ap.add_argument('--consult', default='claude-fable-5-2,gpt-6.2-sol'); ap.add_argument('--improve', default='claude-opus-5-5,claude-sonnet-5-5'); a = ap.parse_args()


def find(p):
    p = Path(p)
    return p if p.is_absolute() or p.exists() else cl.VAULT.parent / p


summary = find(a.prompt).read_text(); run_dir = cl.RUNS / a.run_id; run_dir.mkdir(parents=True, exist_ok=True)


def call(model, step, prompt_file, text):
    fn = cl.logged_openai if model.startswith('gpt') else cl.logged_anthropic
    out, rec = fn(a.run_id, step, model, str(prompt_file), text, effort='high', **({'max_tokens': 16000} if not model.startswith('gpt') else {}))
    (run_dir / f"{step}-{model}.md").write_text(out); print(f"{step:15s} {model:18s} in {rec['tokens_in']} out {rec['tokens_out']} {rec['latency_s']}s ~${rec['cost_usd_est']}", flush=True); return model, out


with ThreadPoolExecutor(4) as ex: crit = dict(ex.map(lambda m: call(m, 'design-consult', a.prompt, summary), a.consult.split(',')))
bundle = f"{find(a.enhance).read_text()}\n\n# (A) One-page summary\n\n{summary}\n\n" + ''.join(f"# (B) Critique from {cl.DISPLAY.get(m, m)}\n\n{t}\n\n" for m, t in crit.items())
with ThreadPoolExecutor(4) as ex: list(ex.map(lambda m: call(m, 'design-improve', a.enhance, bundle), a.improve.split(',')))
print('done; files in', run_dir)

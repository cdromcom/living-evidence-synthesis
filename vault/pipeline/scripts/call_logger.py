#!/usr/bin/env python3
"""Call logger for the Skill: one JSON line per model call, so every page can say how it was made.

Each record: UTC time, step, node and citekey, provider, exact model id and display name, effort, prompt file with its SHA-256, the git commit that
last changed the prompt and a GitHub permalink to it, tokens, estimated cost, latency, output hash, run id, harness. Records go to
<run-dir>/calls.jsonl (default pipeline/runs/<run-id>/). Prompts live in pipeline/prompts/ and must be committed before a run (an uncommitted prompt is logged as such).

  python3 call_logger.py log --run-id R --step write-nodes --model claude-opus-5-5 --prompt pipeline/prompts/x.md --citekey @key [--node "EVD - ..."] \\
         [--effort high] [--tokens-in N --tokens-out N] [--harness "Claude Code"] [--output-file out.md]    (for calls made inside Claude Code)
  python3 call_logger.py summary --run-id R           tokens and dollars per step and model
  python3 call_logger.py footer  --run-id R [--node N | --citekey K]     the "How this page was made" block for a page
As a library: logged_anthropic(...), logged_openai(...) make the call and log it; record(...) logs a call made elsewhere."""
import argparse, hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
RUNS = VAULT / 'pipeline' / 'runs'
DISPLAY = {'claude-opus-5-5': 'Claude Opus 5.5', 'claude-sonnet-5-5': 'Claude Sonnet 5.5', 'claude-fable-5-2': 'Claude Fable 5.2', 'claude-haiku-5-5': 'Claude Haiku 5.5',
           'gpt-6.2-sol': 'GPT-6.2 Sol', 'pplx-decider-v1.3': 'Perplexity Decider 1.3', 'd1-ultra': 'Liquid d1-ultra', 'jev-1.14.0': 'Jev 1.14.0'}
PRICE = {'claude-opus-5-5': (4, 20), 'claude-sonnet-5-5': (2, 10), 'claude-fable-5-2': (8, 40), 'claude-haiku-5-5': (0.10, 0.50),   # USD per million tokens, list prices 2026-11
         'pplx-decider-v1.3': (0.02, 0), 'd1-ultra': (0.042, 0), 'jev-1.14.0': (0.042, 0)}   # gpt-6.2-sol: price not confirmed, left blank on purpose


def load_env(path=None):
    p = Path(path or Path.home() / '.config' / 'lives-ai-raters' / '.env')
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1); os.environ.setdefault(k.strip(), v.strip().strip('"\''))


def _git(args, cwd):
    try: return subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception: return ''


def prompt_info(prompt_file):
    """SHA-256 of the prompt text, last commit that changed it, and a GitHub permalink (None if uncommitted or no GitHub remote)."""
    p = Path(prompt_file)
    if not p.is_absolute(): p = (Path.cwd() / p) if (Path.cwd() / p).exists() else (VAULT.parent / p if (VAULT.parent / p).exists() else VAULT / p)
    if not p.exists(): return {'prompt_file': str(prompt_file), 'prompt_sha256': None, 'prompt_commit': None, 'prompt_url': None, 'prompt_state': 'missing'}
    sha = hashlib.sha256(p.read_bytes()).hexdigest(); top = _git(['rev-parse', '--show-toplevel'], p.parent)
    if not top: return {'prompt_file': str(prompt_file), 'prompt_sha256': sha, 'prompt_commit': None, 'prompt_url': None, 'prompt_state': 'not in a git repository'}
    rel = os.path.relpath(p, top); commit = _git(['log', '-1', '--format=%H', '--', rel], top); dirty = bool(_git(['status', '--porcelain', '--', rel], top))
    remote = _git(['remote', 'get-url', 'origin'], top).replace('git@github.com:', 'https://github.com/').removesuffix('.git')
    url = f'{remote}/blob/{commit}/{rel}' if commit and 'github.com' in remote and not dirty else None
    return {'prompt_file': rel, 'prompt_sha256': sha, 'prompt_commit': commit or None, 'prompt_url': url,
            'prompt_state': 'committed' if commit and not dirty else ('changed since last commit' if commit else 'uncommitted')}


def cost_usd(model, tin, tout):
    pr = PRICE.get(model)
    return None if not pr or tin is None else round((tin * pr[0] + (tout or 0) * pr[1]) / 1e6, 5)


def record(run_id, step, model, prompt_file, provider=None, citekey=None, node=None, effort=None, tokens_in=None, tokens_out=None, latency_s=None,
           output_text=None, harness='API', notes=None, run_dir=None):
    d = Path(run_dir) if run_dir else RUNS / run_id; d.mkdir(parents=True, exist_ok=True)
    rec = {'ts_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'run_id': run_id, 'step': step, 'citekey': citekey, 'node': node,
           'provider': provider or ('anthropic' if model.startswith('claude') else 'openai' if model.startswith('gpt') else 'decision-model'),
           'model_id': model, 'model': DISPLAY.get(model, model), 'effort': effort, **prompt_info(prompt_file), 'tokens_in': tokens_in, 'tokens_out': tokens_out,
           'cost_usd_est': cost_usd(model, tokens_in, tokens_out), 'latency_s': latency_s, 'harness': harness,
           'output_sha256': hashlib.sha256(output_text.encode()).hexdigest() if output_text else None, 'notes': notes}
    with open(d / 'calls.jsonl', 'a') as f: f.write(json.dumps(rec) + '\n')
    return rec


def logged_anthropic(run_id, step, model, prompt_file, user_text, effort='high', max_tokens=16000, system=None, **meta):
    import anthropic; load_env(); t0 = time.time()
    r = anthropic.Anthropic().messages.create(model=model, max_tokens=max_tokens, output_config={'effort': effort}, system=system or anthropic.NOT_GIVEN,
                                              messages=[{'role': 'user', 'content': user_text}])
    text = ''.join(b.text for b in r.content if b.type == 'text')
    rec = record(run_id, step, model, prompt_file, 'anthropic', effort=effort, tokens_in=r.usage.input_tokens, tokens_out=r.usage.output_tokens,
                 latency_s=round(time.time() - t0, 1), output_text=text, notes=meta.pop('notes', None), **meta)
    return text, rec


def logged_openai(run_id, step, model, prompt_file, user_text, effort='high', **meta):
    from openai import OpenAI; load_env(); t0 = time.time()
    r = OpenAI().responses.create(model=model, input=user_text, reasoning={'effort': effort})
    text = r.output_text; u = getattr(r, 'usage', None)
    rec = record(run_id, step, model, prompt_file, 'openai', effort=effort, tokens_in=getattr(u, 'input_tokens', None), tokens_out=getattr(u, 'output_tokens', None),
                 latency_s=round(time.time() - t0, 1), output_text=text, notes=meta.pop('notes', None), **meta)
    return text, rec


def read_calls(run_id=None, run_dir=None):
    f = (Path(run_dir) if run_dir else RUNS / run_id) / 'calls.jsonl'
    return [json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []


def render_footer(calls, human=None):
    """Markdown block for the bottom of a node page. Legacy pages with no log use render_legacy_footer."""
    rows = ['> [!info] How this page was made', '>', '> | Step | Model and version | Effort | Accessed (UTC) | Prompt |', '> |---|---|---|---|---|']
    for c in calls:
        pr = f"[{Path(c['prompt_file']).name}]({c['prompt_url']}) `{(c['prompt_sha256'] or '')[:8]}`" if c.get('prompt_url') else (f"`{Path(c['prompt_file']).name}` ({c['prompt_state']})" if c.get('prompt_file') else 'n/a')
        rows.append(f"> | {c['step']} | {c['model']} (`{c['model_id']}`) | {c.get('effort') or 'n/a'} | {c['ts_utc'].replace('T', ' ')[:16]} | {pr} |")
    ids = sorted({c['run_id'] for c in calls}); rows += ['>', f"> Run{'s' if len(ids) > 1 else ''}: {', '.join(ids)}. Full call log: `pipeline/runs/<run>/calls.jsonl`."]
    rows.append('> Human check: ' + (human or 'not yet reviewed (`human_verified: no`)'))
    return '\n'.join(rows)


def render_legacy_footer(model, date, note):
    return ('> [!info] How this page was made\n>\n> | Step | Model and version | Accessed | Prompt |\n> |---|---|---|---|\n'
            f'> | Original extraction and writing | {model} | {date} | not archived |\n>\n> {note}\n> Human check: `human_verified: no`')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    l = sub.add_parser('log'); [l.add_argument(f'--{k}') for k in ('run-id', 'step', 'model', 'prompt', 'citekey', 'node', 'effort', 'harness', 'output-file', 'notes', 'run-dir')]
    l.add_argument('--tokens-in', type=int); l.add_argument('--tokens-out', type=int); l.add_argument('--latency-s', type=float)
    s = sub.add_parser('summary'); s.add_argument('--run-id'); s.add_argument('--run-dir')
    f = sub.add_parser('footer'); f.add_argument('--run-id'); f.add_argument('--run-dir'); f.add_argument('--node'); f.add_argument('--citekey')
    a = ap.parse_args()
    if a.cmd == 'log':
        out = Path(a.output_file).read_text() if a.output_file else None
        r = record(a.run_id, a.step, a.model, a.prompt, citekey=a.citekey, node=a.node, effort=a.effort, tokens_in=a.tokens_in, tokens_out=a.tokens_out,
                   latency_s=a.latency_s, output_text=out, harness=a.harness or 'Claude Code', notes=a.notes, run_dir=a.run_dir); print(json.dumps(r, indent=1))
    else:
        calls = read_calls(a.run_id, a.run_dir)
        if a.cmd == 'summary':
            tot = {}
            for c in calls:
                k = (c['step'], c['model']); t = tot.setdefault(k, [0, 0, 0, 0.0]); t[0] += 1; t[1] += c['tokens_in'] or 0; t[2] += c['tokens_out'] or 0; t[3] += c['cost_usd_est'] or 0
            for (st, m), t in sorted(tot.items()): print(f"{st:28s} {m:22s} calls {t[0]:3d}  in {t[1]:8d}  out {t[2]:7d}  ~${t[3]:.3f}")
            print(f"total ~${sum(t[3] for t in tot.values()):.3f} (models without a confirmed price count as 0)")
        else:
            sel = [c for c in calls if (not a.node or c.get('node') == a.node) and (not a.citekey or c.get('citekey') == a.citekey)]
            print(render_footer(sel))

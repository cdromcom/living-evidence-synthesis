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
import config as C
DISPLAY = {k: v['display'] for k, v in C.MODELS.items()}   # from pipeline/config/models.json
PRICE = {k: (v['price_in'], v['price_out']) for k, v in C.MODELS.items()}   # USD per million tokens (see price_source in the registry)
#   # gpt-6.2-sol: price not confirmed, left blank on purpose


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
           'provider': provider or ('anthropic' if model.startswith('claude') else 'openai' if model.startswith('gpt') else 'tinker' if model.startswith('thinkingmachines') else 'decision-model'),
           'model_id': model, 'model': DISPLAY.get(model, model), 'effort': effort, **prompt_info(prompt_file), 'tokens_in': tokens_in, 'tokens_out': tokens_out,
           'cost_usd_est': cost_usd(model, tokens_in, tokens_out), 'latency_s': latency_s, 'harness': harness,
           'output_sha256': hashlib.sha256(output_text.encode()).hexdigest() if output_text else None, 'notes': notes}
    if output_text:   # GAMER item 3: keep the unedited response, named by its hash
        (d / 'responses').mkdir(exist_ok=True); (d / 'responses' / f"{rec['output_sha256'][:12]}.txt").write_text(output_text, encoding='utf-8')
        rec['response_file'] = f"responses/{rec['output_sha256'][:12]}.txt"
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


TINKER_URL = 'https://tinker.thinkingmachines.dev/services/tinker-prod/oai/api/v1/chat/completions'


def logged_tinker(run_id, step, model, prompt_file, user_text, effort='low', max_tokens=3000, **meta):
    """Inkling models on Tinker through the OpenAI-compatible endpoint (key TINKER_API_KEY). Max tokens includes the model's reasoning tokens."""
    import urllib.request; load_env(); t0 = time.time()
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': user_text}], 'max_completion_tokens': max_tokens, 'reasoning_effort': effort}).encode()
    req = urllib.request.Request(TINKER_URL, body, {'Authorization': 'Bearer ' + os.environ['TINKER_API_KEY'], 'Content-Type': 'application/json', 'User-Agent': 'LIVES-provenance/1.0'})
    r = json.load(urllib.request.urlopen(req, timeout=180)); text = r['choices'][0]['message'].get('content') or ''; u = r.get('usage', {})
    rec = record(run_id, step, model, prompt_file, 'tinker', effort=effort, tokens_in=u.get('prompt_tokens'), tokens_out=u.get('completion_tokens'),
                 latency_s=round(time.time() - t0, 1), output_text=text, notes=meta.pop('notes', None), **meta)
    return text, rec


def logged_gemini(run_id, step, model, prompt_file, user_text, effort='high', max_tokens=16000, pdf_path=None, **meta):
    """Gemini models (default gemini-4-neon) through the Gemini API (key GEMINI_API_KEY). effort = thinking level (low, medium, high); thinking tokens are billed as output, so
    they are added to tokens_out. pdf_path sends one PDF inline (base64, under about 20 MB). Use the Batch API for unattended runs (Skill.md, Step 1 item 11)."""
    import base64, urllib.request; load_env(); t0 = time.time(); parts = [{'text': user_text}]
    if pdf_path: parts.insert(0, {'inline_data': {'mime_type': 'application/pdf', 'data': base64.b64encode(Path(pdf_path).read_bytes()).decode()}})
    body = json.dumps({'contents': [{'parts': parts}], 'generationConfig': {'maxOutputTokens': max_tokens, 'thinkingConfig': {'thinkingLevel': effort}}}).encode()
    req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', body, {'Content-Type': 'application/json', 'x-goog-api-key': os.environ['GEMINI_API_KEY']})
    r = json.load(urllib.request.urlopen(req, timeout=300)); cand = r['candidates'][0]['content']['parts']; text = ''.join(x.get('text', '') for x in cand if not x.get('thought')); u = r.get('usageMetadata', {})
    rec = record(run_id, step, model, prompt_file, 'google', effort=effort, tokens_in=u.get('promptTokenCount'), tokens_out=(u.get('candidatesTokenCount') or 0) + (u.get('thoughtsTokenCount') or 0),
                 latency_s=round(time.time() - t0, 1), output_text=text, notes=meta.pop('notes', None), **meta)
    return text, rec


def read_calls(run_id=None, run_dir=None):
    f = (Path(run_dir) if run_dir else RUNS / run_id) / 'calls.jsonl'
    return [json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []


DISCLOSURE = '[[pipeline/provenance/AI-disclosure|full AI disclosure (GAMER)]]'


def _short(m): return m.replace(' (Claude Code)', '').replace('Claude ', '')


def render_footer(calls, human=None, roles=None, sections=None):
    """Collapsed callout for the bottom of a node page. One line shows; click (Obsidian) or open (web app) for the table. Follows the GAMER checklist
    (Generative AI tools in MEdical Research): tools+versions+dates (2), prompts (3), role (5), sections (6), verification (7), influence (9).
    Items 1, 4, 8 and the unedited responses (3) live in the linked disclosure page and the run folder."""
    models = list(dict.fromkeys(_short(c['model']) for c in calls)); dates = sorted({c['ts_utc'][:10] for c in calls})
    when = dates[0] if len(dates) == 1 else f'{dates[0]} to {dates[-1]}'
    status = human or 'not yet human-checked'
    rows = [f"> [!info]- AI use: {', '.join(models)} · {when} · {status}", '>',
            '> | Step | Model and version | Effort | Accessed (UTC) | Prompt | Response |', '> |---|---|---|---|---|---|']
    for c in calls:
        pr = f"[{Path(c['prompt_file']).name}]({c['prompt_url']}) `{(c['prompt_sha256'] or '')[:8]}`" if c.get('prompt_url') else (f"`{Path(c['prompt_file']).name}` ({c['prompt_state']})" if c.get('prompt_file') else 'n/a')
        rs = f"`{c['response_file']}`" if c.get('response_file') else f"hash `{(c.get('output_sha256') or 'n/a')[:8]}`"
        rows.append(f"> | {c['step']} | {c['model']} (`{c['model_id']}`) | {c.get('effort') or 'n/a'} | {c['ts_utc'].replace('T', ' ')[:16]} | {pr} | {rs} |")
    ids = sorted({c['run_id'] for c in calls})
    rows += ['>', f"> **Role:** {roles or 'read the PDF, drafted this page from it'} · **Sections:** {sections or 'all'} · **Checked by:** {status}",
             f"> Run {', '.join(ids)} (`pipeline/runs/<run>/`: `calls.jsonl`, `responses/`) · {DISCLOSURE}"]
    return '\n'.join(rows)


def render_legacy_footer(model, date, note, human=None):
    """Footer for pages made before the call log existed: the same shape, with 'not recorded' stated outright."""
    status = human or 'not yet human-checked'
    return (f'> [!info]- AI use: {_short(model)} · {date} · {status}\n>\n> | Step | Model and version | Accessed | Prompt | Response |\n> |---|---|---|---|---|\n'
            f'> | Original extraction and writing | {model} | {date} | not archived | not archived |\n>\n> {note}\n> {DISCLOSURE} · [[pipeline/provenance/model-history|model history by date]]')


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

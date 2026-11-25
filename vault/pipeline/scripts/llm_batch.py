#!/usr/bin/env python3
"""One request format, four providers, two modes (JP, 2026-11-25).

  Req(id, model, text, system='', pdf=None, effort='high', max_tokens=16000)  ->  Res(id, ok, text, tin, tout, finish, err)

  run_standard(reqs)           answer now (pilots, when someone is waiting); Anthropic, OpenAI and Gemini one call each, in parallel
  submit_batch(reqs)           Anthropic Message Batches, OpenAI Batch (/v1/responses), Gemini Batch (inline requests); about half price, results within 24 h
  poll_batch(job) / fetch_batch(job) / cancel_batch(job)
  Inkling 2 Small (Tinker) has no batch mode: submit_batch runs the requests in parallel instead and returns a finished job.

The model decides the provider: claude-* Anthropic, gpt-* OpenAI, gemini-* Google, thinkingmachines/* Tinker. Keys come from ~/.config/lives-ai-raters/.env
(ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, TINKER_API_KEY); keys are never printed or logged.
Prices (USD per million tokens, list prices, batch = half): see PRICE. GPT-6.2 Sol and the Gemini prices come from third-party pages: confirm before relying on them."""
import base64, concurrent.futures as cf, json, os, re, time, urllib.error, urllib.request
from dataclasses import dataclass, field
from pathlib import Path
import call_logger as cl

PRICE = {'gemini-4-neon': (3, 15), 'claude-opus-5-5': (4, 20), 'claude-sonnet-5-5': (2, 10), 'gpt-6.2-sol': (2, 10), 'thinkingmachines/Inkling-2-Small': (0.30, 1.00)}   # Sol: unverified
BATCH_DISCOUNT = 0.5
GEMINI = 'https://generativelanguage.googleapis.com/v1beta'


@dataclass
class Req:
    id: str
    model: str
    text: str
    system: str = ''
    pdf: str | None = None
    effort: str = 'high'
    max_tokens: int = 16000
    images: list = field(default_factory=list)   # PNG paths (crops), for vision checks
    pdf_uri: str | None = None                  # set by upload_pdfs() when the PDF is sent through the Gemini File API


@dataclass
class Res:
    id: str
    ok: bool
    text: str = ''
    tin: int = 0
    tout: int = 0
    finish: str = ''
    err: str = ''


def provider_of(model):
    return 'anthropic' if model.startswith('claude') else 'openai' if model.startswith('gpt') else 'google' if model.startswith('gemini') else 'tinker' if model.startswith('thinkingmachines') else None


def cost(model, tin, tout, batch=False):
    pi, po = PRICE[model]; return (tin * pi + tout * po) / 1e6 * (BATCH_DISCOUNT if batch and provider_of(model) != 'tinker' else 1)


def _env():
    cl.load_env()


def _pdf_b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def _safe_id(i): return re.sub(r'[^A-Za-z0-9_-]', '_', i)[:64]


# ------------------------------------------------------------------ Anthropic
def _anthropic_params(r):
    content = ([{'type': 'document', 'source': {'type': 'base64', 'media_type': 'application/pdf', 'data': _pdf_b64(r.pdf)}}] if r.pdf else []) + [{'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/png', 'data': _pdf_b64(i)}} for i in r.images] + [{'type': 'text', 'text': r.text}]
    p = {'model': r.model, 'max_tokens': r.max_tokens, 'messages': [{'role': 'user', 'content': content}]}
    if r.system: p['system'] = r.system
    if r.effort in ('high', 'medium'): p['thinking'] = {'type': 'adaptive'}
    return p


def _anthropic_res(rid, message):
    text = ''.join(b.text for b in message.content if getattr(b, 'type', '') == 'text')
    return Res(rid, True, text, message.usage.input_tokens, message.usage.output_tokens, str(message.stop_reason))


# ------------------------------------------------------------------ OpenAI (Responses API)
def _openai_body(r):
    content = ([{'type': 'input_file', 'filename': Path(r.pdf).name, 'file_data': 'data:application/pdf;base64,' + _pdf_b64(r.pdf)}] if r.pdf else []) + [{'type': 'input_image', 'image_url': 'data:image/png;base64,' + _pdf_b64(i)} for i in r.images] + [{'type': 'input_text', 'text': r.text}]
    b = {'model': r.model, 'input': [{'role': 'user', 'content': content}], 'max_output_tokens': r.max_tokens, 'reasoning': {'effort': r.effort}}
    if r.system: b['instructions'] = r.system
    return b


def _openai_res(rid, body):
    text = ''.join(c.get('text', '') for o in body.get('output', []) if o.get('type') == 'message' for c in o.get('content', []) if c.get('type') == 'output_text')
    u = body.get('usage', {}); return Res(rid, body.get('status') == 'completed', text, u.get('input_tokens', 0), u.get('output_tokens', 0), str(body.get('status')), '' if body.get('status') == 'completed' else json.dumps(body.get('incomplete_details') or body.get('error'))[:200])


# ------------------------------------------------------------------ Gemini
def _gemini_body(r):
    pdfpart = [{'file_data': {'mime_type': 'application/pdf', 'file_uri': r.pdf_uri}}] if r.pdf_uri else ([{'inline_data': {'mime_type': 'application/pdf', 'data': _pdf_b64(r.pdf)}}] if r.pdf else [])
    parts = pdfpart + [{'inline_data': {'mime_type': 'image/png', 'data': _pdf_b64(i)}} for i in r.images] + [{'text': r.text}]
    b = {'contents': [{'role': 'user', 'parts': parts}], 'generationConfig': {'maxOutputTokens': r.max_tokens, 'thinkingConfig': {'thinkingLevel': r.effort}}}
    if r.system: b['systemInstruction'] = {'parts': [{'text': r.system}]}
    return b


def _gemini_res(rid, resp):
    if 'error' in resp: return Res(rid, False, err=json.dumps(resp['error'])[:200])
    c = (resp.get('candidates') or [{}])[0]; text = ''.join(p.get('text', '') for p in c.get('content', {}).get('parts', []) if not p.get('thought')); u = resp.get('usageMetadata', {})
    fin = c.get('finishReason', ''); return Res(rid, fin == 'STOP' and bool(text), text, u.get('promptTokenCount', 0), (u.get('candidatesTokenCount') or 0) + (u.get('thoughtsTokenCount') or 0), fin, '' if fin == 'STOP' else f'finishReason {fin}')


def _gemini_call(path, body=None, method='POST'):
    _env(); req = urllib.request.Request(f'{GEMINI}/{path}', json.dumps(body).encode() if body is not None else None, {'Content-Type': 'application/json', 'x-goog-api-key': os.environ['GEMINI_API_KEY']}, method=method)
    try: return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e: raise RuntimeError(f'Gemini HTTP {e.code}: {e.read().decode()[:300]}')


# ------------------------------------------------------------------ Gemini File API (lifts the inline size limit)
FILE_API_MIN_MB = 6   # PDFs at or above this size go through the File API; smaller ones are sent inline (a request, and an inline batch as a whole, must stay under about 19 MB)


def gemini_upload(path, display_name=None):
    """Resumable upload to the Gemini File API; waits until the file is ACTIVE. Returns {'name': 'files/...', 'uri': ...}. Files expire after 48 hours; delete them with gemini_delete when the run ends."""
    _env(); data = Path(path).read_bytes(); key = os.environ['GEMINI_API_KEY']
    start = urllib.request.Request('https://generativelanguage.googleapis.com/upload/v1beta/files', json.dumps({'file': {'display_name': display_name or Path(path).name[:100]}}).encode(),
                                   {'x-goog-api-key': key, 'X-Goog-Upload-Protocol': 'resumable', 'X-Goog-Upload-Command': 'start', 'X-Goog-Upload-Header-Content-Length': str(len(data)), 'X-Goog-Upload-Header-Content-Type': 'application/pdf', 'Content-Type': 'application/json'})
    url = urllib.request.urlopen(start, timeout=120).headers['X-Goog-Upload-URL']
    up = urllib.request.Request(url, data, {'Content-Length': str(len(data)), 'X-Goog-Upload-Offset': '0', 'X-Goog-Upload-Command': 'upload, finalize'})
    f = json.load(urllib.request.urlopen(up, timeout=600))['file']
    for _ in range(60):
        if f.get('state') == 'ACTIVE': return {'name': f['name'], 'uri': f['uri']}
        if f.get('state') == 'FAILED': raise RuntimeError('Gemini file processing failed')
        time.sleep(3); f = _gemini_call(f['name'], method='GET')
    raise RuntimeError('Gemini file not ACTIVE after 3 minutes')


def gemini_delete(name):
    try: _gemini_call(name, method='DELETE'); return True
    except Exception: return False


def upload_pdfs(reqs, cache):
    """For Gemini requests whose PDF is at least FILE_API_MIN_MB, upload it (once per file; `cache` maps path to {'name','uri'}) and set pdf_uri. Returns the list of uploaded file names for later deletion."""
    new = []
    for r in reqs:
        if provider_of(r.model) == 'google' and r.pdf and not r.pdf_uri and Path(r.pdf).stat().st_size >= FILE_API_MIN_MB * 1e6:
            if r.pdf not in cache: cache[r.pdf] = gemini_upload(r.pdf); new.append(cache[r.pdf]['name'])
            r.pdf_uri = cache[r.pdf]['uri']
    return new


# ------------------------------------------------------------------ Tinker (Inkling)
def _tinker_one(r):
    _env(); body = json.dumps({'model': r.model, 'messages': ([{'role': 'system', 'content': r.system}] if r.system else []) + [{'role': 'user', 'content': r.text}], 'max_completion_tokens': r.max_tokens, 'reasoning_effort': r.effort}).encode()
    req = urllib.request.Request(cl.TINKER_URL, body, {'Authorization': 'Bearer ' + os.environ['TINKER_API_KEY'], 'Content-Type': 'application/json', 'User-Agent': 'LIVES-provenance/1.0'})
    j = json.load(urllib.request.urlopen(req, timeout=300)); u = j.get('usage', {}); c = j['choices'][0]
    return Res(r.id, bool(c['message'].get('content')), c['message'].get('content') or '', u.get('prompt_tokens', 0), u.get('completion_tokens', 0), str(c.get('finish_reason')))


# ------------------------------------------------------------------ standard mode (parallel)
def _one(r):
    _env(); pv = provider_of(r.model)
    try:
        if pv == 'anthropic':
            import anthropic
            with anthropic.Anthropic().messages.stream(**_anthropic_params(r)) as s: m = s.get_final_message()   # streaming avoids request time-outs on long outputs
            return _anthropic_res(r.id, m)
        if pv == 'openai':
            from openai import OpenAI
            return _openai_res(r.id, OpenAI().responses.create(**_openai_body(r)).model_dump())
        if pv == 'google': return _gemini_res(r.id, _gemini_call(f'models/{r.model}:generateContent', _gemini_body(r)))
        if pv == 'tinker': return _tinker_one(r)
    except Exception as e:
        return Res(r.id, False, err=f'{type(e).__name__}: {str(e)[:250]}')
    return Res(r.id, False, err=f'unknown provider for {r.model}')


def run_standard(reqs, workers=4):
    with cf.ThreadPoolExecutor(workers) as ex: return {x.id: x for x in ex.map(_one, reqs)}


# ------------------------------------------------------------------ batch mode
def submit_batch(reqs):
    """All requests must use one model. Returns a job dict (JSON-serializable) to store before waiting, so a crash can resume."""
    _env(); models = {r.model for r in reqs}; assert len(models) == 1, 'one model per batch'; model = reqs[0].model; pv = provider_of(model); ids = {r.id: _safe_id(r.id) for r in reqs}
    if len({*ids.values()}) != len(ids): raise ValueError('request ids collide after cleaning')
    job = {'provider': pv, 'model': model, 'ids': ids, 'submitted': time.time(), 'n': len(reqs)}
    if pv == 'anthropic':
        import anthropic
        b = anthropic.Anthropic().messages.batches.create(requests=[{'custom_id': ids[r.id], 'params': _anthropic_params(r)} for r in reqs]); job['id'] = b.id
    elif pv == 'openai':
        from openai import OpenAI
        c = OpenAI(); tmp = cl.RUNS / '_batch_input.jsonl'; tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text('\n'.join(json.dumps({'custom_id': ids[r.id], 'method': 'POST', 'url': '/v1/responses', 'body': _openai_body(r)}) for r in reqs), encoding='utf-8')
        f = c.files.create(file=open(tmp, 'rb'), purpose='batch'); tmp.unlink(); b = c.batches.create(input_file_id=f.id, endpoint='/v1/responses', completion_window='24h'); job['id'] = b.id; job['input_file'] = f.id
    elif pv == 'google':
        body = {'batch': {'display_name': f'lives-{int(time.time())}', 'input_config': {'requests': {'requests': [{'request': _gemini_body(r), 'metadata': {'key': ids[r.id]}} for r in reqs]}}}}
        if len(json.dumps(body)) > 19_000_000: raise ValueError('Gemini inline batch over 19 MB: use fewer or smaller PDFs (the File API route is not built)')
        job['id'] = _gemini_call(f'models/{model}:batchGenerateContent', body)['name']
    elif pv == 'tinker':   # no batch mode: parallel run, finished at once
        job['id'] = 'parallel'; job['results'] = {r.id: vars(x) for r, x in zip(reqs, run_standard(reqs, workers=8).values())}
    else: raise ValueError(f'no provider for {model}')
    return job


def poll_batch(job):
    """'running' | 'done' | 'failed'."""
    _env(); pv = job['provider']
    if pv == 'tinker': return 'done'
    if pv == 'anthropic':
        import anthropic
        s = anthropic.Anthropic().messages.batches.retrieve(job['id']).processing_status; return 'done' if s == 'ended' else 'running'
    if pv == 'openai':
        from openai import OpenAI
        s = OpenAI().batches.retrieve(job['id']).status; return 'done' if s == 'completed' else 'failed' if s in ('failed', 'expired', 'cancelled') else 'running'
    if pv == 'google':
        j = _gemini_call(job['id'], method='GET'); st = (j.get('metadata') or {}).get('state', '')
        return 'done' if j.get('done') and 'SUCCEEDED' in st else 'failed' if st in ('JOB_STATE_FAILED', 'BATCH_STATE_FAILED', 'JOB_STATE_CANCELLED', 'BATCH_STATE_CANCELLED', 'BATCH_STATE_EXPIRED', 'JOB_STATE_EXPIRED') or (j.get('done') and 'error' in j) else 'running'


def fetch_batch(job):
    """{request id: Res} for a finished job."""
    _env(); pv = job['provider']; back = {v: k for k, v in job['ids'].items()}; out = {}
    if pv == 'tinker': return {k: Res(**v) for k, v in job['results'].items()}
    if pv == 'anthropic':
        import anthropic
        for r in anthropic.Anthropic().messages.batches.results(job['id']):
            k = back[r.custom_id]; out[k] = _anthropic_res(k, r.result.message) if r.result.type == 'succeeded' else Res(k, False, err=f'{r.result.type}: {str(getattr(r.result, "error", ""))[:200]}')
    elif pv == 'openai':
        from openai import OpenAI
        c = OpenAI(); b = c.batches.retrieve(job['id'])
        for fid in (b.output_file_id, b.error_file_id):
            if not fid: continue
            for line in c.files.content(fid).text.splitlines():
                j = json.loads(line); k = back[j['custom_id']]; resp = j.get('response') or {}
                out[k] = _openai_res(k, resp['body']) if resp.get('status_code') == 200 else Res(k, False, err=json.dumps(j.get('error') or resp.get('body'))[:200])
    elif pv == 'google':
        j = _gemini_call(job['id'], method='GET'); items = ((j.get('response') or {}).get('inlinedResponses') or {}).get('inlinedResponses') or (j.get('response') or {}).get('inlinedResponses') or []
        for it in items:
            k = back[(it.get('metadata') or {}).get('key')]; out[k] = _gemini_res(k, it.get('response') or {'error': it.get('error', 'no response')})
    for k in job['ids']: out.setdefault(k, Res(k, False, err='no result returned'))
    return out


def cancel_batch(job):
    _env(); pv = job['provider']
    try:
        if pv == 'anthropic':
            import anthropic; anthropic.Anthropic().messages.batches.cancel(job['id'])
        elif pv == 'openai':
            from openai import OpenAI; OpenAI().batches.cancel(job['id'])
        elif pv == 'google': _gemini_call(job['id'] + ':cancel', {})
        return True
    except Exception as e:
        return f'cancel failed: {e}'

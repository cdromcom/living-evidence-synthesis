"""HTTP helper for the provenance scripts: generic User-Agent (no personal or project details, no email), retries with backoff,
a global limit of about 5 requests a second, a 30-day on-disk cache of GET responses keyed by URL, and request counters.
Raw response bodies are cached on disk only; callers keep just the sha256 (see store.py)."""
import hashlib, json, os, re, threading, time
from urllib.parse import urlencode
from pathlib import Path
import requests

UA = {'User-Agent': 'provenance-check/1.0 (research tool)'}
CACHE_DIR = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[3]) / 'pipeline' / 'provenance' / 'cache'   # raw API responses, 30 days; not published
CACHE_DAYS = 30
MIN_GAP = 0.2  # seconds between network requests (5 a second)
_lock = threading.Lock(); _last = [0.0]
STATS = {'requests': 0, 'cache_hits': 0}


def _throttle():
    with _lock:
        wait = _last[0] + MIN_GAP - time.time()
        if wait > 0: time.sleep(wait)
        _last[0] = time.time()
        STATS['requests'] += 1


def reset_stats(): STATS.update(requests=0, cache_hits=0)


def _key(method, url, params, body):
    s = json.dumps([method, url, sorted((params or {}).items()), body], default=str)
    return hashlib.sha256(s.encode()).hexdigest()


def fetch(method, url, retries=4, cache=True, headers=None, params=None, json_body=None, timeout=45, allow_redirects=True, no_body=False, **kw):
    """Returns a dict: status (int or None), text, final_url, redirects (list of urls), sha256 of the body, error, cached, elapsed.
    Only 200 and 404 GET responses are cached (30 days). 404 is not retried. Authorization headers are never cached or stored."""
    use_cache = cache and method == 'GET'
    path = CACHE_DIR / (_key(method, url, params, json_body) + '.json')
    if use_cache and path.exists() and time.time() - path.stat().st_mtime < CACHE_DAYS * 86400:
        try:
            c = json.loads(path.read_text()); c['cached'] = True; STATS['cache_hits'] += 1; return c
        except (ValueError, OSError): pass
    res = {'status': None, 'text': '', 'final_url': url, 'redirects': [], 'sha256': None, 'error': None, 'cached': False, 'elapsed': 0.0, 'headers': {}}
    t0 = time.time()
    for i in range(retries):
        _throttle()
        try:
            r = requests.request(method, url, headers={**UA, **(headers or {})}, params=params, json=json_body, timeout=timeout,
                                 allow_redirects=allow_redirects, stream=no_body, **kw)
        except requests.RequestException as e:
            res['error'] = type(e).__name__ + ': ' + str(e)[:300]
            res['dns_failure'] = bool(re.search(r'NameResolutionError|gaierror|nodename nor servname|Name or service not known', repr(e)))
        else:
            res.update(status=r.status_code, final_url=r.url, redirects=[h.url for h in r.history], error=None,
                       text='' if (method == 'HEAD' or no_body) else r.text, headers={k.lower(): v for k, v in r.headers.items() if k.lower() in ('link', 'content-type', 'location')})
            if no_body: r.close(); res['text'] = ''   # status and redirects only; the body is never read
            else: res['sha256'] = hashlib.sha256(r.content).hexdigest()
            if r.status_code not in (429, 500, 502, 503, 504): break
            res['error'] = f'HTTP {r.status_code}'
        time.sleep(2 ** i)
    res['elapsed'] = round(time.time() - t0, 2)
    if use_cache and res['status'] in (200, 404):
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps({**res, 'cached': False}))
        except OSError: pass
    return res


def request_json(method, url, retries=4, **kw):
    """Returns (json, error). Use request_json_meta when the status and sha256 are needed."""
    d, err, _ = request_json_meta(method, url, retries=retries, **kw)
    return d, err


def request_json_meta(method, url, retries=4, **kw):
    """Returns (json or None, error or None, meta) where meta has url, http_status, response_sha256."""
    r = fetch(method, url, retries=retries, **kw)
    meta = {'url': url + ('?' + urlencode(kw['params']) if kw.get('params') else ''), 'http_status': r['status'], 'response_sha256': r['sha256']}
    if r['status'] == 200:
        try: return json.loads(r['text']), None, meta
        except ValueError: return None, 'response was not JSON', meta
    if r['status'] == 404: return None, 'not found', meta
    return None, r['error'] or f"HTTP {r['status']}", meta

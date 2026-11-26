#!/usr/bin/env python3
"""PubPeer. Safe default: link only. The search URL is always returned. PubPeer has no documented public API; the comment count comes from the
endpoint its browser extension calls (POST /v3/publications with the extension's public dev key). That endpoint is unofficial and may stop
working, so the count is reported only when the call returned HTTP 200 with status 'good', and the HTTP status and time are always recorded.
Pass query_endpoint=False to make no request at all (link only).
  python3 pubpeer.py 10.2196/59258"""
import json, sys, time
from datetime import datetime, timezone
from urllib.parse import quote
from _http import fetch

LABEL = 'unofficial endpoint, may stop working'


def comments(doi: str, query_endpoint=True) -> dict:
    out = {'pubpeer_search_url': f'https://pubpeer.com/search?q={quote(doi)}', 'label': LABEL, 'pubpeerCommentCount': None, 'http_status': None,
           'checked_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'response_sha256': None, 'queried': query_endpoint}
    if not query_endpoint: return out
    r = fetch('POST', 'https://pubpeer.com/v3/publications', retries=2, json_body={'dois': [doi], 'devkey': 'PubMedChrome'})
    out.update(http_status=r['status'], response_sha256=r['sha256'], error=r['error'], elapsed_seconds=r['elapsed'])
    if r['status'] == 200:
        try: d = json.loads(r['text'])
        except ValueError: d = None
        if d and d.get('status') == 'good':
            fb = d.get('feedbacks') or []
            out['pubpeerCommentCount'] = sum(int(f.get('total_comments', 1) or 0) for f in fb) if fb else 0
            out['pubpeer_url'] = fb[0].get('url') if fb else None
        else: out['error'] = f"unexpected response: {str(d)[:80]}"
    return out


if __name__ == '__main__':
    print(json.dumps(comments(sys.argv[1]), indent=1))

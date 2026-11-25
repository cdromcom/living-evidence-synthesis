#!/usr/bin/env python3
"""PubPeer comment count for a DOI. PubPeer has no public documented API; this uses the endpoint its browser extension calls
(POST /v3/publications with the extension's public dev key). If PubPeer changes it, the field stays manual: the result says 'unavailable'.
  python3 pubpeer.py 10.2196/59258"""
import json, sys
from _http import request_json


def comments(doi: str) -> dict:
    d, err = request_json('POST', 'https://pubpeer.com/v3/publications', json={'dois': [doi], 'devkey': 'PubMedChrome'})
    if not d or d.get('status') != 'good': return {'pubpeerCommentCount': None, 'error': err or f"unexpected response: {str(d)[:80]}"}
    fb = d.get('feedbacks') or []
    n = sum(int(f.get('total_comments', 1) or 0) for f in fb) if fb else 0
    return {'pubpeerCommentCount': n, 'pubpeer_url': (fb[0].get('url') if fb else None)}


if __name__ == '__main__':
    print(json.dumps(comments(sys.argv[1]), indent=1))

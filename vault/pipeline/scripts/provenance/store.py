#!/usr/bin/env python3
"""Store for provenance results: pipeline/provenance/provenance-quality-signals.json
papers[citekey]["provenance"] is the list of items written here. Other keys under a paper (for example "signals", written by another program) and
other papers are never changed or deleted: merge_paper only sets title, doi, checked_utc and provenance. Raw responses stay in the cache folder;
items carry only the sha256 of the response."""
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path

STORE = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[3]) / 'pipeline' / 'provenance' / 'provenance-quality-signals.json'
STATUSES = ('ok', 'flag', 'unavailable')


def now_utc() -> str: return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def make_item(id, label, tool, status, result, detail='', url='', http_status=None, response_sha256=None, data=None, checked_utc=None) -> dict:
    assert status in STATUSES, status
    return {'id': id, 'label': label, 'tool': tool, 'status': status, 'result': result, 'detail': detail or '', 'url': url or '',
            'checked_utc': checked_utc or now_utc(), 'http_status': http_status, 'response_sha256': response_sha256, 'data': data if data is not None else {}}


def merge_paper(store: dict, citekey: str, items: list, title=None, doi=None, checked_utc=None) -> dict:
    """Return the store with papers[citekey] updated in place. Keys other than title, doi, checked_utc and provenance are left as they were."""
    store = store if isinstance(store, dict) else {}
    papers = store.setdefault('papers', {})
    paper = papers.setdefault(citekey, {})
    if title is not None: paper['title'] = title
    if doi is not None: paper['doi'] = doi
    paper['checked_utc'] = checked_utc or now_utc()
    paper['provenance'] = list(items)
    return store


def load(path=STORE) -> dict:
    try: return json.loads(Path(path).read_text())
    except FileNotFoundError: return {}


def write(citekey, items, title=None, doi=None, path=STORE) -> Path:
    """Read the file again just before writing, merge, and replace it atomically so a concurrent writer's keys are not lost."""
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    store = merge_paper(load(path), citekey, items, title, doi)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    with os.fdopen(fd, 'w') as f: json.dump(store, f, indent=1, ensure_ascii=False, default=str)
    os.replace(tmp, path)
    return path

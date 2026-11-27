#!/usr/bin/env python3
"""Is the GitHub repo's vault/ the same as this vault? Compares every file by content against a repo checkout (default: ~/.cache/lives-bench/wt-align),
ignoring only what is deliberately not published (PDFs, skill backups, caches, Obsidian settings, local Python environments). Read-only.
  python3 check_repo_sync.py [--repo /path/to/checkout] [--ref origin/main]"""
import re, argparse, hashlib, os, subprocess
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('--vault', default=os.environ.get('LIVES_VAULT') or str(Path.home() / 'Documents/living-synthesis'), help='the working vault (not the checkout)'); ap.add_argument('--repo', default=str(Path.home() / '.cache/lives-bench/wt-align')); ap.add_argument('--ref', default='HEAD'); a = ap.parse_args(); VAULT = Path(a.vault).expanduser().resolve()
SKIP_DIRS = {'pdfs', 'skill-backups', '__pycache__', '.obsidian', '.claude', '.venv', 'misc'}   # pdfs and backups are deliberately not published; .venv is a local Python environment; top-level misc = stray scratch
SKIP_FILES = {'.DS_Store', '.Rhistory'}
def local():
    d = {}
    for root, dirs, files in os.walk(VAULT):
        rel = Path(root).relative_to(VAULT)
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS or (x == 'misc' and rel.parts[:1] == ('pipeline',)) or (x == 'public' and False)]
        if rel.parts[:4] == ('pipeline', 'misc', 'evd-validation', 'table-parsers'): dirs[:] = [x for x in dirs if x not in ('review', 'results', 'scratch')]   # page renders and raw parser output stay local
        if rel.parts[:2] == ('pipeline', 'provenance'): dirs[:] = [x for x in dirs if x != 'cache']   # raw API responses of the provenance checks are not published
        if rel.parts[:2] == ('pipeline', 'runs'): dirs[:] = [x for x in dirs if not re.match(r'^(\d{4}-\d\d-\d\d_batch\d+|test-.*)$', x)]   # batch-runner outputs (extracted paper content, local paths) stay local
        for f in files:
            if rel.parts[:4] == ('pipeline', 'misc', 'evd-validation', 'table-parsers') and (f in ('review.html', 'pages.json') or f.startswith('eval_A')): continue
            if (f == '.gitignore' and not rel.parts) or f in SKIP_FILES or f.endswith('.pdf') or (rel.parts[:2] == ('pipeline', 'runs') and len(rel.parts) == 2 and (f in ('ledger.jsonl', '_batch_input.jsonl') or f.startswith('_batch_input'))): continue   # zip files are compared too
            p = Path(root) / f; b = p.read_bytes(); d[str((rel / f))] = hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
    return d
out = subprocess.run(['git', 'ls-tree', '-r', '-z', a.ref, '--', 'vault'], cwd=a.repo, capture_output=True, text=True).stdout.split('\0')
repo = {}
for line in out:
    if line: meta, path = line.split('\t', 1); repo[path[len('vault/'):]] = meta.split()[2]
L = local(); both = set(L) & set(repo)
only_l = sorted(set(L) - set(repo)); only_r = sorted(set(repo) - set(L)); diff = sorted(k for k in both if L[k] != repo[k])
print(f'local files compared: {len(L)} | in repo ({a.ref}): {len(repo)} | identical: {len(both) - len(diff)} | differ: {len(diff)} | only local: {len(only_l)} | only repo: {len(only_r)}')
for title, xs in (('DIFFER', diff), ('ONLY LOCAL', only_l), ('ONLY REPO', only_r)):
    for x in xs[:12]: print(f'  {title}: {x}')
    if len(xs) > 12: print(f'  ... and {len(xs) - 12} more {title}')

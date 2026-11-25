#!/usr/bin/env python3
"""List the commits that touched a vault file, each placed in an era of pipeline/provenance/model-history.md.
  python3 file_model_history.py <repo-checkout> <path-in-repo>   (e.g. vault/sysrev/dgraph/evidence/EVD - x.md)"""
import subprocess, sys
ERAS = [('2026-04-17', '2026-08-24', 'Era 1: Claude Sonnet 4.6 (per model-history.md; batch subagents on 04-28 not recorded)'), ('2026-08-25', '2026-08-25', 'Era 2: Claude Sonnet 5 re-curation'),
        ('2026-08-26', '2026-11-22', 'Era 1/2: no model recorded in this period'), ('2026-11-23', '9999', 'Era 3-4: see pipeline/runs/ and the page footer')]
repo, path = sys.argv[1], sys.argv[2]
for l in subprocess.run(['git', '-C', repo, 'log', '--follow', '--format=%h %ad %s', '--date=short', '--', path], capture_output=True, text=True).stdout.splitlines():
    h, d, *m = l.split(' ', 2); era = next((e for a, b, e in ERAS if a <= d <= b), 'before 2026-04-17'); print(f"{d} {h}  {era}  | {' '.join(m)[:60]}")

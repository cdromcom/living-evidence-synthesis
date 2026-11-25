#!/usr/bin/env python3
"""Names of the Quality signal rows (JP, 2026-11-25). The single source of truth is pipeline/templates/quality-signal-labels.json
({"rows": [{"id", "label", "aliases"}]}). The web app gets a copy through scripts/build-graph.mjs; this script keeps the vault pages in step.
  python3 quality_labels.py list            current names and old names
  python3 quality_labels.py check           bold row names on source pages that the registry does not know (exit 1 if any)
  python3 quality_labels.py apply [--dry]   rewrite every row name on every source page to the current name
To rename a row: change "label" in the registry, keep the old name in "aliases", run apply, then rebuild the app."""
import json, os, re, sys
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
REG = json.loads((VAULT / 'pipeline/templates/quality-signal-labels.json').read_text(encoding='utf-8'))['rows']
NAMES = {n.lower(): r for r in REG for n in [r['label'], *r['aliases']]}
ROW = re.compile(r'^(\|\s*)\*\*([^*|]+?)\*\*(\s*:)', re.M)
def pages(): return sorted((VAULT / 'sysrev/dgraph/source').glob('@*.md'))
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'list':
        for r in REG: print(f"{r['id']:28s} {r['label']}" + (f"   (old: {', '.join(r['aliases'])})" if r['aliases'] else ''))
    elif cmd == 'check':
        bad = {}
        for p in pages():
            for m in ROW.finditer(p.read_text(encoding='utf-8')):
                if m.group(2).strip().lower() not in NAMES: bad.setdefault(m.group(2).strip(), []).append(p.stem)
        for k, v in sorted(bad.items()): print(f"unknown row name '{k}' on {len(v)} page(s), e.g. {v[0]}")
        print(f"{len(bad)} unknown name(s)"); sys.exit(1 if bad else 0)
    elif cmd == 'apply':
        dry = '--dry' in sys.argv; changed = 0
        for p in pages():
            t = p.read_text(encoding='utf-8'); n = 0
            def fix(m):
                nonlocal n; r = NAMES.get(m.group(2).strip().lower())
                # rename only genuine old names; capitalization alone is left as written
                if r and m.group(2).strip().lower() != r['label'].lower(): n += 1; return f"{m.group(1)}**{r['label']}**{m.group(3)}"
                return m.group(0)
            new = ROW.sub(fix, t)
            if n: changed += n; (None if dry else p.write_text(new, encoding='utf-8')); print(f"{p.stem}: {n} row name(s) {'would change' if dry else 'updated'}")
        print(f"{changed} row name(s) {'would change' if dry else 'updated'}")
if __name__ == '__main__': main()

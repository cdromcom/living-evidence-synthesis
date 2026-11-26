#!/usr/bin/env python3
"""Give path-qualified node links an alias so they read as the node's name instead of a folder path (JP, 2026-11-25).
  [[sysrev/dgraph/evidence/EVD - x]]   ->   [[sysrev/dgraph/evidence/EVD - x|EVD - x title]]
The web app already shows the node name for alias-less links (scripts/build-graph.mjs); this fixes the same thing in Obsidian.
Leaves alone: links that already have an alias or a heading, links to source papers ([[.../@citekey]], which the tools parse as written), links to images and attachments, and anything outside sysrev/dgraph.
  python3 add_link_aliases.py [--apply]      (default is a dry run)"""
import os, re, sys
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2]); D = VAULT / 'sysrev' / 'dgraph'
LINK = re.compile(r'\[\[(sysrev/dgraph/(?:questions|claims|evidence|caveats)/[^\]|#]+?)\]\]')
def alias_for(target):
    f = VAULT / (target + '.md')
    if not f.exists(): return None
    t = f.read_text(encoding='utf-8'); m = re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M)
    prefix = f.stem.split(' - ', 1)[0]
    return f"{prefix} - {m.group(1).strip()}" if m else f.stem
def main():
    apply = '--apply' in sys.argv; n = 0; pages = 0; missing = set()
    for p in sorted(D.rglob('*.md')):
        if 'attachments' in p.parts or 'source' in p.parts and p.parent.name == 'pdfs': continue
        t = p.read_text(encoding='utf-8'); k = 0
        def fix(m):
            nonlocal k
            a = alias_for(m.group(1))
            if a is None: missing.add(m.group(1)); return m.group(0)
            k += 1; return f"[[{m.group(1)}|{a.replace('|', '/')}]]"
        new = LINK.sub(fix, t)
        if k:
            n += k; pages += 1
            if apply: p.write_text(new, encoding='utf-8')
    print(f"{n} link(s) on {pages} page(s) {'updated' if apply else 'would be updated (dry run; add --apply)'}")
    for m in sorted(missing): print('  target not found:', m)
if __name__ == '__main__': main()

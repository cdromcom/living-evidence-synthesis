#!/usr/bin/env python3
"""
For each subtask row in the leaderboard page, count the EVDs that the linked
QUE references and rewrite the Details cell wikilink to show the count.

Leaderboard row format (Details cell):
    [[QUE - <title>?\\|→]]

After this script:
    [[QUE - <title>?\\|→ N EVDs]]

The count is the number of unique EVD wikilinks in the QUE's
"Supporting Claims (with their evidence)" section, which is the same
nested CLM → EVD list a reader sees on the QUE page.
"""

from __future__ import annotations
import re
from pathlib import Path

VAULT = Path("/Users/ppatel/Documents/living-synthesis")
TOPICS = VAULT / "Review-Arena.md"
QUE_DIR = VAULT / "questions"

# Match the QUE wikilink in a Details cell.
# Format inside table cells: [[QUE - title?\|→]] or [[QUE - title?\|→ 5 EVDs]]
QUE_LINK_RE = re.compile(r"\[\[(QUE - [^\\\]]+?)\\\|→[^\]]*\]\]")
EVD_LINK_RE = re.compile(r"\[\[(EVD - [^\]|]+?)(?:\|[^\]]+)?\]\]")
SUPPORTING_RE = re.compile(
    r"###\s+Supporting Claims[\s\S]*?(?=\n### |\Z)",
)


def count_evds_in_que(que_target: str) -> int:
    que_file = QUE_DIR / f"{que_target}.md"
    if not que_file.exists():
        return 0
    text = que_file.read_text()
    m = SUPPORTING_RE.search(text)
    section = m.group(0) if m else text
    # Unique EVD targets only
    evds = set(EVD_LINK_RE.findall(section))
    return len(evds)


def main():
    text = TOPICS.read_text()

    # Cache counts so we don't re-read each QUE file
    cache: dict[str, int] = {}

    def replace(match: re.Match) -> str:
        target = match.group(1)
        if target not in cache:
            cache[target] = count_evds_in_que(target)
        n = cache[target]
        label = f"→ {n} EVDs" if n != 1 else "→ 1 EVD"
        return f"[[{target}\\|{label}]]"

    new_text, n_subs = QUE_LINK_RE.subn(replace, text)
    TOPICS.write_text(new_text)

    print(f"Updated {n_subs} Details cells across {len(cache)} unique QUEs.")
    print()
    print("EVD counts per subtask:")
    for q, c in sorted(cache.items(), key=lambda kv: -kv[1]):
        short = q.removeprefix("QUE - ")[:60]
        print(f"  {c:>3}  {short}")


if __name__ == "__main__":
    main()

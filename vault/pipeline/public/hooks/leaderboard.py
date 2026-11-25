"""
MkDocs hook: mark leaderboard-page tables for sort + filter.

Wraps each markdown table on the leaderboard page in a
`<div class="ls-leaderboard">` container so that sortable.js can find and
decorate them. Other pages with tables are untouched.
"""

from __future__ import annotations
import re

# Match a markdown table (header row, divider, then ≥1 body rows).
TABLE_RE = re.compile(
    r"(?P<table>"
    r"(?:^\|[^\n]+\|\s*\n)"          # header row
    r"(?:^\|[\s\-:|]+\|\s*\n)"       # divider row
    r"(?:^\|[^\n]+\|\s*\n)+"         # ≥1 body rows
    r")",
    re.MULTILINE,
)

# Pages whose tables should be sortable + filterable. Add new pages here.
LEADERBOARD_PAGES = {
    "sysrev/indexes/Review-Arena.md",
}


def on_page_markdown(markdown, page, config, files, **kwargs):
    src = page.file.src_path.replace("\\", "/")
    if src not in LEADERBOARD_PAGES:
        return markdown

    def wrap(m):
        tbl = m.group("table")
        return f'<div class="ls-leaderboard" markdown>\n\n{tbl}\n</div>\n'

    return TABLE_RE.sub(wrap, markdown)

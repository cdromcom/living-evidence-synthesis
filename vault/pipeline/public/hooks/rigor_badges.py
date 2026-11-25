"""
MkDocs hook: insert a visual rigor-badge bar at the top of each source page.

Source pages are the @-prefixed citekey files in `source/`. Each one carries
its own critical-appraisal table (5 domains, 🟢/🟡/🔴 ratings) and a
TRIPOD-LLM reporting compliance table (✅/⚠️/❌/➖ icons). This hook reads
those tables out of the page markdown, plus a topic phrase derived from the
linked QUE, and prepends a single-row badge bar that summarizes them.

Badges shown (in order):
  Topic       — short phrase from the page's first [[QUE ...]] link
  Rigor       — composite tally of 🟢 N · 🟡 N · 🔴 N (5-domain table)
  TRIPOD-LLM  — % fully-reported items (✅ / non-➖ rows)
  Caveats     — count of unique [[CVT - ...]] links on the page

Step 5 of the public-render rollout. Styling lives in
public/assets/badges.css.
"""

from __future__ import annotations
import re
from pathlib import Path

# ---------- pattern detection ----------

WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
APPRAISAL_SECTION_RE = re.compile(
    r"##\s+Critical appraisal([\s\S]*?)(?=\n##\s|\Z)",
)
TRIPOD_SECTION_RE = re.compile(
    r"##\s+TRIPOD-LLM reporting summary([\s\S]*?)(?=\n##\s|\Z)",
)
TLDR_CALLOUT_RE = re.compile(
    r"(>\s*\[!success\][^\n]*\*\*TL;DR\*\*[\s\S]*?)(?=\n##\s|\Z)",
)

GREEN = "🟢"
YELLOW = "🟡"
RED = "🔴"
TRIPOD_FULL = "✅"
TRIPOD_NA = "➖"


def _normalize_question_to_topic(que_target: str) -> str:
    """Turn a QUE wikilink target into a short topic phrase.

    Truncates to ~46 chars on a word boundary so the badge stays compact
    without cutting mid-word.
    """
    body = que_target.removeprefix("QUE - ").rstrip("?").strip()
    # Strip stacked interrogative prefixes ("How accurately can", "How well do",
    # "How does", etc.) iteratively so the remaining phrase reads as a topic.
    drop_leads = (
        "How accurately can ", "How accurately does ", "How effectively can ",
        "How well can ", "How well do ", "How well does ",
        "How has ", "How have ", "How does ", "How do ",
        "Can ", "Do ", "Does ", "How ", "Is ", "What ", "Are ",
        "Could ", "Will ", "Should ",
    )
    rest = body
    for _ in range(2):
        progressed = False
        for lead in drop_leads:
            if rest.startswith(lead):
                rest = rest[len(lead):]
                progressed = True
                break
        if not progressed:
            break
    rest = rest.strip()

    max_len = 46
    if len(rest) > max_len:
        cut = rest[:max_len]
        # Back off to the last word boundary
        space = cut.rfind(" ")
        if space > 20:
            cut = cut[:space]
        rest = cut.rstrip(", ;") + "…"
    return rest[:1].upper() + rest[1:] if rest else body


def _first_que_topic(text: str) -> str | None:
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).split("|")[0].strip()
        if target.startswith("QUE - "):
            return _normalize_question_to_topic(target)
    return None


def _rigor_tally(text: str) -> tuple[int, int, int] | None:
    """Count 🟢/🟡/🔴 ratings in the Critical appraisal table only.

    The whole section also contains a legend and bottom-line prose that
    mention these emoji; we only want the per-row table cell ratings.
    Table rows look like: ``| **Construct validity** ... | 🟡 | ...``.
    """
    m = APPRAISAL_SECTION_RE.search(text)
    if not m:
        return None
    section = m.group(1)
    # Only count emoji that appear inside a table row (lines starting with `|`)
    table_rows = [ln for ln in section.split("\n") if ln.startswith("|")]
    g = y = r = 0
    for row in table_rows:
        # Each row should have at most one rating cell. Use first occurrence.
        if RED in row:
            r += 1
        elif YELLOW in row:
            y += 1
        elif GREEN in row:
            g += 1
    if g + y + r == 0:
        return None
    return (g, y, r)


def _tripod_pct(text: str) -> int | None:
    """Count fully-reported (✅) rows / non-NA (non-➖) rows from TRIPOD table."""
    m = TRIPOD_SECTION_RE.search(text)
    if not m:
        return None
    section = m.group(1)
    full = section.count(TRIPOD_FULL)
    # All rows have an icon (✅/⚠️/❌/➖); count rows by lines starting "| **"
    # Avoid counting the header/divider rows
    rows = re.findall(r"\n\|\s*\*\*[^\n]+\|\s*[✅⚠️❌➖()][^\n]*", section)
    if not rows:
        return None
    na = section.count(TRIPOD_NA)
    denom = max(1, len(rows) - na)
    return round(100 * full / denom)


def _cvt_count(text: str) -> int:
    """Count unique [[CVT - ...]] wikilinks."""
    targets = set()
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).split("|")[0].strip()
        if target.startswith("CVT - "):
            targets.add(target)
    return len(targets)


def _build_badge_bar(
    topic: str | None,
    rigor: tuple[int, int, int] | None,
    tripod: int | None,
    cvt_count: int,
) -> str:
    """Build the HTML for the badge bar."""
    badges = []

    if topic:
        badges.append(
            '<div class="rigor-badge rigor-badge--topic">'
            f'<div class="rigor-badge__label">Topic</div>'
            f'<div class="rigor-badge__value">{topic}</div>'
            "</div>"
        )

    if rigor:
        g, y, r = rigor
        # Color the bar by the dominant risk
        if r >= 1:
            severity = "high"
        elif y >= 3:
            severity = "moderate"
        else:
            severity = "low"
        badges.append(
            f'<div class="rigor-badge rigor-badge--rigor rigor-badge--{severity}">'
            '<div class="rigor-badge__label">Rigor (5 domains)</div>'
            '<div class="rigor-badge__value">'
            f'<span title="Low risk">🟢 {g}</span> '
            f'<span title="Some concerns">🟡 {y}</span> '
            f'<span title="High risk">🔴 {r}</span>'
            "</div></div>"
        )

    if tripod is not None:
        if tripod >= 80:
            severity = "low"
        elif tripod >= 60:
            severity = "moderate"
        else:
            severity = "high"
        badges.append(
            f'<div class="rigor-badge rigor-badge--tripod rigor-badge--{severity}">'
            '<div class="rigor-badge__label">TRIPOD-LLM</div>'
            f'<div class="rigor-badge__value">{tripod}% fully reported</div>'
            "</div>"
        )

    if cvt_count > 0:
        if cvt_count <= 1:
            severity = "low"
        elif cvt_count <= 3:
            severity = "moderate"
        else:
            severity = "high"
        word = "limitation" if cvt_count == 1 else "limitations"
        badges.append(
            f'<div class="rigor-badge rigor-badge--caveats rigor-badge--{severity}">'
            '<div class="rigor-badge__label">Caveats</div>'
            f'<div class="rigor-badge__value">{cvt_count} flagged {word}</div>'
            "</div>"
        )

    if not badges:
        return ""

    inner = "".join(badges)
    return f'<div class="rigor-bar" markdown="0">{inner}</div>\n\n'


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Prepend a rigor badge bar to source pages."""
    src = page.file.src_path.replace("\\", "/")
    # Only act on source pages: sysrev/dgraph/source/@*.md
    if not (src.startswith("sysrev/dgraph/source/@") and src.endswith(".md")):
        return markdown

    topic = _first_que_topic(markdown)
    rigor = _rigor_tally(markdown)
    tripod = _tripod_pct(markdown)
    cvt_count = _cvt_count(markdown)

    bar = _build_badge_bar(topic, rigor, tripod, cvt_count)
    if not bar:
        return markdown

    # Insert above the TL;DR callout if present, else at the top.
    m = TLDR_CALLOUT_RE.search(markdown)
    if m:
        insert_at = m.start()
        return markdown[:insert_at] + bar + markdown[insert_at:]
    return bar + markdown

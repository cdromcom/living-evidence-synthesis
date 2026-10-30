#!/usr/bin/env python3
"""
Add a TL;DR callout to every source/@*.md page.

For each source page, derive a 1-3 sentence TL;DR from the existing
**Bottom line.** paragraph in the Critical appraisal section, and insert
it as a `> [!success] **TL;DR**` callout immediately after the YAML
frontmatter and before `## Structured abstract`.

Idempotent: if a TL;DR callout already exists immediately under the
frontmatter, it is replaced rather than duplicated.
"""

from __future__ import annotations
import re
from pathlib import Path

VAULT = Path("/Users/ppatel/Documents/living-synthesis")
SOURCE_DIR = VAULT / "source"

FRONTMATTER_RE = re.compile(r"^(---\n.*?\n---\n)", re.DOTALL)
BOTTOM_LINE_RE = re.compile(
    r"\*\*Bottom line\.\*\*\s*(.+?)(?=\n\n|\n>\s|\Z)",
    re.DOTALL,
)
EXISTING_TLDR_RE = re.compile(
    r"\n>\s*\[!success\][^\n]*\*\*TL;DR\*\*[\s\S]*?(?=\n##\s|\Z)",
)


def split_sentences(text: str) -> list[str]:
    """Split a paragraph into sentences. Naive but reliable for this corpus."""
    text = text.strip()
    # Split on sentence boundaries: period/?/! followed by whitespace + capital
    # or end-of-string. Keep the punctuation with the sentence.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"“])", text)
    return [p.strip() for p in parts if p.strip()]


def derive_tldr(bottom_line: str) -> str:
    """Take the first 1-3 sentences of the bottom line paragraph as TL;DR.

    Heuristic: take sentences 1 and 2 by default. If their combined length
    is under 220 chars, also include sentence 3. Cap at 3 sentences and
    ~600 chars.
    """
    bottom_line = re.sub(r"\s+", " ", bottom_line).strip()
    sentences = split_sentences(bottom_line)
    if not sentences:
        return ""

    pick = sentences[:2]
    combined = " ".join(pick)
    if len(combined) < 220 and len(sentences) >= 3:
        pick.append(sentences[2])
        combined = " ".join(pick)

    # Hard cap: never more than 3 sentences, never more than ~600 chars
    while len(combined) > 600 and len(pick) > 1:
        pick.pop()
        combined = " ".join(pick)

    return combined


def format_callout(tldr_text: str) -> str:
    """Format the TL;DR as an Obsidian success callout."""
    # Wrap each line with `> ` prefix; tldr is single-paragraph so one line
    return f"> [!success] **TL;DR**\n> {tldr_text}\n"


def process_file(path: Path) -> tuple[bool, str]:
    """Process a single source file. Returns (changed, message)."""
    text = path.read_text()

    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return False, f"no frontmatter found"
    frontmatter = fm_match.group(1)
    body = text[fm_match.end():]

    bl_match = BOTTOM_LINE_RE.search(body)
    if not bl_match:
        return False, f"no Bottom line paragraph found"
    bottom_line = bl_match.group(1)

    tldr_text = derive_tldr(bottom_line)
    if not tldr_text:
        return False, f"derived TL;DR was empty"

    callout = format_callout(tldr_text)

    # Remove any existing TL;DR callout that immediately follows the frontmatter
    # (idempotent re-runs)
    body_stripped = body.lstrip("\n")
    if body_stripped.startswith("> [!success]") and "**TL;DR**" in body_stripped[:200]:
        # Strip the existing callout: find the first non-callout line
        lines = body_stripped.split("\n")
        cut = 0
        for i, line in enumerate(lines):
            if line.startswith(">") or not line.strip():
                cut = i + 1
            else:
                break
        body_stripped = "\n".join(lines[cut:]).lstrip("\n")

    new_text = frontmatter + "\n" + callout + "\n" + body_stripped
    if new_text == text:
        return False, "unchanged"
    path.write_text(new_text)
    return True, f"inserted TL;DR ({len(tldr_text)} chars)"


def main():
    files = sorted(SOURCE_DIR.glob("@*.md"))
    print(f"Processing {len(files)} source files...\n")
    changed = 0
    for f in files:
        ok, msg = process_file(f)
        marker = "✓" if ok else "·"
        print(f"  {marker} {f.name:<60} {msg}")
        if ok:
            changed += 1
    print(f"\n{changed}/{len(files)} files updated.")


if __name__ == "__main__":
    main()

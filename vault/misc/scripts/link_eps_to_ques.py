#!/usr/bin/env python3
"""
For each QUE, append a `### Cross-paper patterns` section listing
EvidencePatterns whose supporting evidence includes EVDs from this
question's *source paper(s)* — i.e., the papers under
`### Key Papers Asking Question`.

This narrower filter (vs. matching against the QUE's keyword-derived
"Supporting Claims" section) keeps the per-QUE EP list focused on
patterns that genuinely cite evidence from the question's own paper.

Idempotent: removes any existing `### Cross-paper patterns` block before
re-writing.
"""

from __future__ import annotations
import re
from pathlib import Path

VAULT = Path("/Users/ppatel/Documents/living-synthesis")
QUE_DIR = VAULT / "questions"
EP_DIR = VAULT / "evd-patterns"

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
EVD_PREFIX = "EVD -"
EP_HEADER_RE = re.compile(
    r"\n### Cross-paper patterns[\s\S]*?(?=\n### |\Z)",
)
# An EVD wikilink ends with " - @citekey"
EVD_CITEKEY_RE = re.compile(r" - @([^\]\s]+)$")
# A QUE's source paper appears as [[@citekey]] under Key Papers Asking Question
PAPER_LINK_RE = re.compile(r"\[\[@([^\]]+)\]\]")


def extract_evd_links(text: str) -> set[str]:
    """Return the set of EVD wikilink targets in `text`, normalized."""
    out = set()
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).split("|")[0].strip()
        if target.startswith(EVD_PREFIX):
            out.add(target)
    return out


def evd_to_citekey(evd_target: str) -> str | None:
    """Pull the @citekey suffix from an EVD wikilink target."""
    m = EVD_CITEKEY_RE.search(evd_target)
    return m.group(1) if m else None


def load_ep_index() -> dict[str, set[str]]:
    """Map EP filename stem → set of *citekeys* whose EVDs the EP cites
    in its Supporting Evidence section."""
    index: dict[str, set[str]] = {}
    for ep_file in sorted(EP_DIR.glob("EP - *.md")):
        text = ep_file.read_text()
        m = re.search(
            r"##\s+Supporting Evidence([\s\S]*?)(?=\n## |\Z)",
            text,
        )
        section_text = m.group(1) if m else text
        evds = extract_evd_links(section_text)
        citekeys = {ck for ck in (evd_to_citekey(e) for e in evds) if ck}
        index[ep_file.stem] = citekeys
    return index


def get_que_source_papers(que_text: str) -> set[str]:
    """Extract source-paper citekeys from the Key Papers Asking Question section."""
    m = re.search(
        r"###\s+Key Papers Asking Question([\s\S]*?)(?=\n### |\Z)",
        que_text,
    )
    section = m.group(1) if m else ""
    return set(PAPER_LINK_RE.findall(section))


def build_cross_paper_section(ep_names: list[str]) -> str:
    """Build the `### Cross-paper patterns` markdown block."""
    if not ep_names:
        return ""
    lines = [
        "### Cross-paper patterns",
        "",
        "> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.",
        "",
    ]
    for name in sorted(ep_names):
        lines.append(f"- [[{name}]]")
    return "\n".join(lines) + "\n"


def upsert_cross_paper_section(que_text: str, block: str) -> str:
    """Replace existing `### Cross-paper patterns` block, or append at end."""
    # Strip any trailing whitespace from file
    stripped = que_text.rstrip() + "\n"
    # Remove existing block if present
    new = EP_HEADER_RE.sub("", stripped).rstrip() + "\n"
    if not block:
        return new
    return new + "\n" + block


def main():
    ep_index = load_ep_index()
    print(f"Loaded {len(ep_index)} EPs (citekey sets).\n")

    que_files = sorted(QUE_DIR.glob("QUE - *.md"))
    print(f"Processing {len(que_files)} QUE files...\n")

    total_links = 0
    ques_with_links = 0
    for que_file in que_files:
        text = que_file.read_text()
        que_papers = get_que_source_papers(text)

        matching_eps: list[str] = []
        for ep_name, ep_papers in ep_index.items():
            if que_papers & ep_papers:
                matching_eps.append(ep_name)

        block = build_cross_paper_section(matching_eps)
        new_text = upsert_cross_paper_section(text, block)

        if new_text != text:
            que_file.write_text(new_text)

        n = len(matching_eps)
        total_links += n
        if n > 0:
            ques_with_links += 1
        marker = "✓" if n > 0 else "·"
        short = que_file.stem[:60]
        print(f"  {marker} {short:<60} {n} EPs (papers: {len(que_papers)})")

    print(f"\n{ques_with_links}/{len(que_files)} QUEs linked to ≥1 EP.")
    print(f"Total QUE↔EP links: {total_links}")


if __name__ == "__main__":
    main()

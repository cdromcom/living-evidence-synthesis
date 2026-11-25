"""
MkDocs hook: convert Obsidian wikilinks to proper markdown links.

Obsidian wikilink syntax:
    [[Target]]                  → link to file matching "Target"
    [[Target|alt text]]         → link with display text
    [[Target#Header]]           → link to anchor inside file
    ![[image.png]]              → embedded image

This hook resolves wikilink targets against an index of all .md and image
files in the docs_dir, producing relative URLs that survive characters
like `?` (which the default mkdocs/roamlinks pipeline mangles).

Hook entry points used:
- on_files: build the target index from the file tree
- on_page_markdown: rewrite wikilinks in the page source before rendering
"""

from __future__ import annotations
import os
import re
import urllib.parse
from pathlib import Path

# Module-level state shared across hook calls within a single build.
_INDEX: dict[str, str] = {}  # basename (no extension) → docs-relative path

WIKILINK_RE = re.compile(r"(!?)\[\[([^\[\]]+?)\]\]")


def on_files(files, config, **kwargs):
    """Build a map from filename stem → docs-relative path."""
    global _INDEX
    _INDEX = {}
    for f in files:
        # f.src_path is relative to docs_dir, using forward slashes
        path = Path(f.src_path)
        stem = path.stem
        # Last-write wins; ambiguous duplicates are unlikely here because
        # discourse-graph nodes have globally-unique titles.
        _INDEX[stem] = f.src_path
        # Also index by full basename so ![[image.png]] embeds work
        _INDEX[path.name] = f.src_path
    return files


def _resolve(target: str) -> str | None:
    """Resolve a wikilink target string to a docs-relative path."""
    # Strip alt-text (after `|`) and anchor (after `#`)
    body = target.split("|")[0]
    anchor = ""
    if "#" in body:
        body, anchor = body.split("#", 1)
        anchor = anchor.strip()
    body = body.strip()

    # Try direct hit on the body
    if body in _INDEX:
        path = _INDEX[body]
    elif body + ".md" in _INDEX:
        path = _INDEX[body + ".md"]
    else:
        return None

    return path, anchor


def _to_relative_md(target_src: str, page_src: str, anchor: str = "") -> str:
    """Emit a file-relative markdown link, e.g. '../claims/CLM - ....md'.

    mkdocs will then convert this to a URL using its own `use_directory_urls`
    rules — which means we should NOT pre-convert .md → directory URL.
    """
    target_dir = os.path.dirname(target_src)
    page_dir = os.path.dirname(page_src)
    rel = os.path.relpath(target_src, page_dir or ".")
    # posix-style separators in URLs
    rel = rel.replace(os.sep, "/")
    if anchor:
        rel += "#" + anchor
    return rel


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Rewrite [[wikilinks]] and ![[embeds]] to standard markdown."""

    def replace(match: re.Match) -> str:
        bang = match.group(1)
        target = match.group(2)
        # When wikilinks live inside a markdown table cell, the inner `|` is
        # escaped as `\|` to avoid being parsed as a column separator. Unescape
        # before splitting target from display.
        target = target.replace("\\|", "|")

        resolved = _resolve(target)
        if resolved is None:
            # Unresolved: leave the original text so the user can spot it
            return match.group(0)

        src_path, anchor = resolved

        # Compute display text: alt-text after | else last segment of target
        if "|" in target:
            display = target.split("|", 1)[1].strip()
        else:
            # Strip @ and use the last meaningful chunk
            display = target.split("#", 1)[0].strip()

        rel = _to_relative_md(src_path, page.file.src_path, anchor)

        # URL-encode the path so characters like `?` and spaces survive
        # mkdocs's link resolver (which otherwise treats `?` as a query
        # separator and fails to find the file).
        rel_encoded = urllib.parse.quote(rel, safe="/#")

        if bang == "!":
            return f"![{display}]({rel_encoded})"
        return f"[{display}]({rel_encoded})"

    return WIKILINK_RE.sub(replace, markdown)

"""
MkDocs hook: render Obsidian `.base` embeds as Material tabbed content.

Without this hook, `![[ESS.base]]` in markdown gets converted to an `<img>`
tag pointing at a YAML file — completely broken on the public site, even
though the file is the source of truth for the leaderboard's filters.

Strategy:
- on_page_markdown runs BEFORE the wikilinks hook
- Scan for `![[<name>.base]]` embeds
- Load the YAML, walk each view's filter conditions, find matching vault files
- Emit a `=== "View Name"` Material tabbed block with a table per view

Filter language supported (subset of Bases filter syntax):
- file.name.startsWith("X")
- file.name.contains("X")
- file.inFolder("X")
- file.tags.contains("X")
- note.PROP == "X"

That covers every filter currently used in ESS.base. Anything richer would
need a real expression parser.
"""

from __future__ import annotations
import re
import yaml
from pathlib import Path

BASE_EMBED_RE = re.compile(r"!\[\[([^\[\]]+\.base)\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TAG_RE = re.compile(r"^\s*-\s*([^\s#]+)", re.MULTILINE)

_VAULT_INDEX: list[dict] | None = None


def _build_vault_index(docs_dir: Path) -> list[dict]:
    """Walk the vault once and pull (path, name, folder, tags, frontmatter)
    for every .md file."""
    global _VAULT_INDEX
    if _VAULT_INDEX is not None:
        return _VAULT_INDEX

    out: list[dict] = []
    for md in docs_dir.rglob("*.md"):
        rel = md.relative_to(docs_dir)
        # Skip pipeline/public, pipeline/misc, pipeline/templates (non-vault content)
        if len(rel.parts) > 1 and rel.parts[0] == "pipeline" and rel.parts[1] in {"public", "misc", "templates"}:
            continue

        try:
            text = md.read_text()
        except Exception:
            continue

        fm_text = ""
        m = FRONTMATTER_RE.match(text)
        if m:
            fm_text = m.group(1)

        tags: list[str] = []
        fm_dict: dict = {}
        try:
            fm_dict = yaml.safe_load(fm_text) or {}
            raw_tags = fm_dict.get("tags") or []
            if isinstance(raw_tags, list):
                tags = [str(t) for t in raw_tags if t]
            elif isinstance(raw_tags, str):
                tags = [raw_tags]
        except Exception:
            # Fall back to regex tag extraction if YAML is malformed
            tag_block = re.search(r"^tags:\s*\n((?:\s*-\s*\S+\n)+)", fm_text, re.MULTILINE)
            if tag_block:
                tags = TAG_RE.findall(tag_block.group(1))

        out.append({
            "path": rel.as_posix(),
            "name": md.stem,
            "folders": rel.parts[:-1],
            "tags": set(tags),
            "frontmatter": fm_dict,
        })

    _VAULT_INDEX = out
    return out


# ---------- filter evaluation ----------

_COND_PATTERNS = [
    (re.compile(r'^file\.name\.startsWith\("(.+)"\)$'),
     lambda f, arg: f["name"].startswith(arg)),
    (re.compile(r'^file\.name\.contains\("(.+)"\)$'),
     lambda f, arg: arg in f["name"]),
    (re.compile(r'^file\.inFolder\("(.+)"\)$'),
     lambda f, arg: arg in f["folders"]),
    (re.compile(r'^file\.tags\.contains\("(.+)"\)$'),
     lambda f, arg: arg in f["tags"]),
    (re.compile(r'^note\.(\w+)\s*==\s*"(.+)"$'),
     lambda f, k, v: str(f["frontmatter"].get(k, "")) == v),
]


def _eval_condition(cond: str, file_data: dict) -> bool:
    cond = cond.strip()
    for pat, fn in _COND_PATTERNS:
        m = pat.match(cond)
        if m:
            return fn(file_data, *m.groups())
    return False


def _eval_filters(filters: dict, files: list[dict]) -> list[dict]:
    """Evaluate a Bases filter block against a list of files."""
    if not filters:
        return files
    conditions = filters.get("and") or []
    out = []
    for f in files:
        if all(_eval_condition(c, f) for c in conditions):
            out.append(f)
    return out


# ---------- rendering ----------

def _short_title(name: str) -> str:
    for prefix in ("EVD - ", "CLM - ", "CVT - ", "QUE - "):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def _node_type(folders: tuple) -> str:
    # Node folders live under sysrev/dgraph/; strip the parents to get the node type folder
    if folders and folders[0] == "sysrev":
        folders = folders[1:]
    if folders and folders[0] == "dgraph":
        folders = folders[1:]
    folder = folders[0] if folders else ""
    return {
        "questions": "QUE",
        "claims": "CLM",
        "evidence": "EVD",
        "caveats": "CVT",
        "evd-patterns": "EP",
        "source": "Source",
    }.get(folder, "—")


def _tags_summary(tags: set, max_n: int = 4) -> str:
    """Show the most informative tags compactly."""
    keep = [t for t in tags if not t.startswith("dg/")]
    keep.sort()
    if len(keep) <= max_n:
        return " · ".join(keep) or "—"
    return " · ".join(keep[:max_n]) + f" · +{len(keep) - max_n}"


def _render_view(view: dict, files: list[dict]) -> str:
    """Render one view's matching files as a Material tab block."""
    name = view.get("name", "View")
    desc = view.get("description", "").strip()
    matching = _eval_filters(view.get("filters") or {}, files)

    # Cap rows per view so the page doesn't explode
    cap = 30
    truncated = len(matching) > cap
    rows = matching[:cap]

    lines = [f'=== "{name}"', ""]
    if desc:
        # Indent description by 4 spaces (Material tab content)
        for line in desc.split("\n"):
            lines.append(f"    {line}")
        lines.append("")

    lines.append(f"    **{len(matching)} match{'es' if len(matching) != 1 else ''}**" + (f" (showing first {cap})" if truncated else "") + ".")
    lines.append("")

    if not rows:
        lines.append("    _No matching nodes in this corpus._")
        lines.append("")
        return "\n".join(lines)

    lines.append("    | Type | Title | Tags |")
    lines.append("    | --- | --- | --- |")
    for f in rows:
        title = _short_title(f["name"])
        # Markdown-link to the file's URL via mkdocs's own resolution
        href = f["path"]
        title_cell = f"[{title}]({_relative_url(f, view)})"
        ntype = _node_type(f["folders"])
        tags = _tags_summary(f["tags"])
        # Pipes inside cells need escaping
        title_cell = title_cell.replace("|", "\\|")
        tags = tags.replace("|", "\\|")
        lines.append(f"    | {ntype} | {title_cell} | {tags} |")
    lines.append("")
    return "\n".join(lines)


def _relative_url(file_data: dict, _view: dict) -> str:
    """Build a relative URL from the ESS-Demo page to the file."""
    # ESS - Demo lives in sysrev/indexes/, use_directory_urls=true → /sysrev/indexes/ESS - Demo/
    # Target file: e.g. sysrev/dgraph/evidence/EVD - X.md → /sysrev/dgraph/evidence/EVD%20-%20X/
    import urllib.parse
    rel = file_data["path"].rsplit(".md", 1)[0]
    return "../../../" + urllib.parse.quote(rel, safe="/") + "/"


def _render_base(base_path: Path, docs_dir: Path) -> str:
    try:
        data = yaml.safe_load(base_path.read_text()) or {}
    except Exception as e:
        return f"\n!!! warning \"Failed to render `{base_path.name}`\"\n    {e}\n"

    views = data.get("views") or []
    if not views:
        return f"\n_(`{base_path.name}` has no views defined.)_\n"

    files = _build_vault_index(docs_dir)
    blocks = [
        f'\n!!! info "{len(views)} pre-built views below"\n'
        f"    Each tab is a saved filter on the corpus, defined in `{base_path.name}`. "
        f"Tabs scroll horizontally; click any tab to switch.\n",
        "",
    ]
    for view in views:
        blocks.append(_render_view(view, files))
    return "\n".join(blocks)


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Replace `![[*.base]]` embeds with rendered Material tab blocks."""
    docs_dir = Path(config["docs_dir"])

    def replace(m: re.Match) -> str:
        target = m.group(1).strip()
        base_path = docs_dir / target
        if not base_path.exists():
            # Obsidian resolves embeds by bare name; .base files live in sysrev/indexes/
            found = sorted(docs_dir.glob(f"*/*/{target}"))
            if not found:
                return m.group(0)
            base_path = found[0]
        return _render_base(base_path, docs_dir)

    return BASE_EMBED_RE.sub(replace, markdown)

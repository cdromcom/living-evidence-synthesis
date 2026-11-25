# Living Synthesis — public site

Builds an Examine-style public website from the Obsidian vault one level
up. The vault stays the source of truth; this folder holds only the
renderer config, build hooks, and CSS.

## Layout

```
public/
├── mkdocs.yml          MkDocs config — docs_dir points to vault root
├── assets/
│   ├── extra.css       Typography, palette, callouts, link tinting
│   └── badges.css      Step 5 rigor-badge bar styling
├── hooks/
│   ├── rigor_badges.py Inserts <Topic | Rigor | TRIPOD-LLM | Caveats> bar
│   │                   above the TL;DR on every source page
│   └── wikilinks.py    Resolves Obsidian [[wikilinks]] → mkdocs-friendly
│                       relative .md links (URL-encoded for `?` etc.)
└── .venv/              Python virtualenv (mkdocs + plugins)
```

The build output goes to `../../living-synthesis-site/` (sibling to the
vault, outside it — required because mkdocs forbids site_dir inside docs_dir).

## Build

```bash
.venv/bin/mkdocs build -f mkdocs.yml --clean
```

Or live-preview while editing the vault:

```bash
.venv/bin/mkdocs serve -f mkdocs.yml
```

## Editorial pipeline (steps that produced this site)

1. `indexes/Review-Arena.md` — leaderboard landing page (Review Arena 🧠-🤖), generated from the 27 QUE files.
2. TL;DR callouts on every source page, derived from each Critical
   appraisal **Bottom line** paragraph (`misc/scripts/add_tldr_callouts.py`).
3. Cross-link EPs → QUEs (`misc/scripts/link_eps_to_ques.py`).
4. MkDocs Material renderer with Obsidian-compat hooks (this folder).
5. Visual rigor badges replacing technical tag chips on source pages
   (`hooks/rigor_badges.py` + `assets/badges.css`).

## Invariants the hooks rely on

- Source pages live at `source/@<citekey>.md`.
- Each source page contains both a `## Critical appraisal` section
  (5-domain table with 🟢/🟡/🔴 in the second column) and a
  `## TRIPOD-LLM reporting summary` section.
- Discourse-graph nodes use unique titles, so wikilinks resolve by stem.
- QUE filenames start with `QUE - ` and end (typically) with `?`.

If any of those break, the corresponding badge or link silently degrades —
never errors.

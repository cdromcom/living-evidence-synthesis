---
name: skill-synthesis
description: Reference doc — cross-paper synthesis layer (EvidencePatterns, Review-Arena leaderboard), public-render pipeline (MkDocs Material), Obsidian visual treatments, and ESS Bases. Steps 11–14 of the extraction pipeline.
parent_skill: extract-discourse-nodes
created: 2026-04-29
updated: 2026-05-04
---

# Skill — Cross-paper Synthesis & Render Pipeline (Steps 11–14)

This file holds the detail for **Steps 11 through 14** of the pipeline — the layer above the per-paper discourse graph. Load this file when working with EvidencePatterns, the Review-Arena leaderboard, the MkDocs public site, the Obsidian wide-tables snippet, or the ESS Bases definition.

> **Governance note (load-bearing).** Cell-level synthesis on `Review-Arena.md` is **human-only**. AI extracts EVDs/CLMs/CVTs, proposes EvidencePatterns, proposes subtask-merge maps, and refreshes derived state — but does **not** auto-fill leaderboard cells. See [Step 11](#step-11-cross-paper-synthesis-evidencepatterns--review-arena) and Skill-references.md Key Principle 16.

> See also:
> - `Skill.md` — orchestrator (workflow at a glance, Steps 1–3, pointers).
> - `Skill-templates.md` — Steps 4–10: node-file templates, audits, structured abstracts.
> - `Skill-references.md` — Naming conventions, Key Principles, Common Pitfalls, After Extraction.

---

## Step 11: Cross-paper synthesis (EvidencePatterns + Review Arena)

The discourse-graph layer (QUE / CLM / EVD / CVT) is paper-internal: each EVD belongs to exactly one paper, each CLM ties EVDs together within a paper. The synthesis layer is **cross-paper**: it identifies regularities that *no single paper makes alone* but that emerge when ≥2 independent EVDs from different papers point in the same direction.

### EvidencePattern (EP) node format

EP files live in `evd-patterns/` and use the same frontmatter conventions as other discourse-graph nodes (`nodeID`, `5c/*` tags, etc.) plus:

- `nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh` — the discourse-graph plugin's EP type ID
- `tags:` includes `ep/strength/<N>-papers` (count of distinct source papers in the supporting EVDs) and `ep/scope/cross-paper`

Each EP file has four required sections (no others):

```
## Pattern statement
One paragraph describing the cross-paper regularity in plain language.

## What is being claimed
1–2 paragraphs unpacking the methodological / deployment implications.

## Supporting Evidence
> [!info] EVDs from independent papers that instantiate this pattern.
- [[EVD - ... - @paperA]] — short paper-attributed annotation
- [[EVD - ... - @paperB]] — ...
- [[EVD - ... - @paperC]] — ...

## Connected discourse-graph nodes
- **Within-paper claims this pattern generalizes:** [[CLM - ...]], [[CLM - ...]]
- **Adjacent pattern:** [[EP - ...]] — relationship sentence
```

**Threshold: ≥2 papers.** Don't open an EP for a single-paper finding — that already lives as a CLM. The point of an EP is the cross-paper triangulation.

### Review-Arena leaderboard

`Review-Arena.md` at the vault root is the public-facing leaderboard. Schema:

```
| Subtask | 🤖 AI score | 🧑 Human score | Human-AI score | Winner | Effect size | Evidence Strength |
```

Where:

- **Subtask** is a verb-first short task name with a wikilink to its QUE and a `· N EVDs` caption (the count is auto-refreshed by `count_evds_per_subtask.py`).
- **AI / Human / Human-AI** cells contain the headline number from the paper, with optional `<abbr title="...">` tooltip carrying the model + technique + sample. Cells stack with `<div class="stack"><abbr>…</abbr><abbr>…</abbr></div>` when 2–3 EVDs share the same paradigm bucket.
- **Winner** is one of `AI` / `Human` / `Human + AI` / `Tie` / `—`.
- **Effect size** is colour-coded via inline `<span class="ls-effect-pos|neg|zero">` classes.
- **Evidence Strength** is `Strong` / `Moderate` / `Limited`.

**Governance: humans synthesize cells; AI does not.** As of 2026-05-04 (logged in `History.md`), the user explicitly removed AI-proposed cell values and reserved cell-filling for human work. AI's role on Review-Arena is upstream (extracting + organizing EVDs/EPs) and meta (proposing merges, refreshing the EVD-count caption, maintaining the rendering pipeline). Do **not** auto-populate cells; if asked to suggest values, present them as a *proposal* the human accepts/rejects per row, never as a commit.

### Subtask naming convention

Each Subtask cell **must begin with a verb and end with a noun phrase**: `Match human peer reviews`, `Detect retraction-comment errors`, `Conduct PRISMA / AMSTAR appraisal`. Don't use bare noun phrases (`Citation-integrity errors`) or model-first phrases (`Reasoning LLMs detect errors`). The verb-first pattern reads as "what the AI is being asked to do" — the leaderboard's framing.

### Subtask merging — propose, don't commit

When subtasks overlap (multiple "Detect errors…" rows from different papers; multiple CONSORT-adjacent rows), AI's role is to propose a merge map as a markdown checklist (cluster → recommended merge / rename / keep-separate, with the kept distinctions noted per cluster). The human picks which proposals to commit. Reference: the merge-map proposal pattern in `History.md` 2026-05-04 entry.

---

## Step 12: Public render via MkDocs Material

The `public/` folder is a sidecar that turns the Obsidian vault into a static website without modifying any Obsidian-side files. The vault stays the source of truth.

### Build commands

```bash
cd public
.venv/bin/mkdocs build -f mkdocs.yml --clean      # one-shot build
.venv/bin/mkdocs serve  -f mkdocs.yml             # live-reload dev server (default :8000)
```

Build output goes to `../../living-synthesis-site/` (sibling to the vault). MkDocs requires `site_dir` to be outside `docs_dir`.

### Hooks (in `public/hooks/`)

Hooks run in this order (set in `mkdocs.yml`):

1. **`rigor_badges.py`** — for each `source/@*.md` page, emits a 4-badge bar (Topic / Rigor / TRIPOD-LLM / Caveats) above the TL;DR. Reads raw `[[QUE]]` / `[[CVT]]` wikilinks, so it must run before `wikilinks.py`.
2. **`leaderboard.py`** — wraps each markdown table on Review-Arena.md in a `<div class="ls-leaderboard">` wrapper so `sortable.js` can find and decorate it. Page set is the `LEADERBOARD_PAGES` constant — add new pages there as new leaderboards appear.
3. **`bases.py`** — intercepts `![[*.base]]` embeds (which Obsidian Bases owns and MkDocs doesn't natively render) and emits a Material `=== "Tab Name"` tabbed block, one tab per view in the .base file. Filter language supported: `file.name.startsWith()`, `file.name.contains()`, `file.tags.contains()`, `file.inFolder()`, `note.PROP == "X"`.
4. **`wikilinks.py`** — converts Obsidian `[[wikilinks]]` and `![[embeds]]` into URL-encoded relative markdown links MkDocs can resolve. Crucially, **unescapes `\|`** (the markdown-table escape) before splitting target/display, so wikilinks inside table cells work.

### Assets

- `assets/extra.css` — typography + palette + TL;DR-callout styling
- `assets/badges.css` — Step-5 rigor badges
- `assets/leaderboard.css` — Review-Arena tables + abbr tooltips + effect-size colours + sticky headers + per-page width override (`body:has(.ls-leaderboard)`)
- `assets/sortable.js` — vanilla JS that adds click-to-sort headers + a per-table filter input. Recognises Strength + Winner + Effect-size column kinds for sort-order semantics.

### Excludes

`exclude_docs:` in `mkdocs.yml` hides `public/.venv/`, `public/site/`, `public/hooks/`, `misc/`, `templates/`, `*.base`, `questions/attachments/`, `source/pdfs/`, `History.md`, `Log.md`, `Skill.md`. Update when adding new internal-only files.

---

## Step 13: Obsidian visual treatments

### Wide-tables snippet

`.obsidian/snippets/wide-tables.css` is a per-note CSS snippet that drops the readable-line-length cap on notes flagged with `cssclasses: [wide-tables]` in their frontmatter. Activation:

1. The note's frontmatter must include `cssclasses:` with `wide-tables` as one entry.
2. **Settings → Appearance → CSS snippets → toggle on `wide-tables`** (one-time per vault).

The snippet covers both Reading view and Live Preview, plus tightens table cell padding and styles `<abbr>` tooltips.

### Sortable tables in Obsidian (not yet wired)

Sort + filter on Review-Arena tables work **only on the public web view** (powered by `sortable.js`). To get the same behaviour inside Obsidian, the user can install:

- The community plugin `Sortable` — drop-in click-to-sort on any markdown table.
- The community plugin `Dataview` — would also need each Review-Arena table rebuilt as a DQL query.

Don't modify Review-Arena.md to add sort/filter inside Obsidian without explicit user approval — both options change either the editor experience or the table format.

---

## Step 14: ESS Bases (live filterable index)

`ESS.base` defines an Obsidian Bases view with **6 formulas** and **23 views**. The wrapper page `ESS - Demo.md` embeds it via `![[ESS.base]]` so readers see the live database.

### Formula columns (computed at render time from tags)

- `node_type` — QUE / CLM / EVD / CVT, derived from folder
- `short_title` — strip the `EVD - ` / `CLM - ` / etc. prefix
- `dim_5c` — concatenate the `5c/*` dimension tags into a readable string
- `tripod_compliance` — categorical: `high` / `moderate` / `low` / `—`, derived from `tripod-llm/compliance/*` tags (the previously-missing categorical filter; raw-percent column was insufficient)
- `appraisal_external` — categorical: `high-risk` / `some-concerns` / `low-risk` / `—`
- `appraisal_statistical` — same shape

### View categories

1. **Default** — `All EVDs (table)` with all rigor columns visible
2. **By node type (4)** — Questions / Claims / Evidence / Caveats
3. **By TRIPOD-LLM compliance bucket (3)** — high / moderate / low (the high view is currently empty; comment in the description explains why)
4. **By critical-appraisal high-risk (2)** — external-validity, statistical-rigor
5. **By 5C research dimension (5)** — credibility / clarity / creativity / connectivity / care
6. **By CVT methodologist axis (6)** — high-severity / inferred / 4 by domain
7. **Workflow (1)** — Drafts (still need verification)
8. **Cards (1)** — best-defended EVDs

### When to add a new view

Add a view when a new categorical filter becomes useful (e.g., a new tag namespace lands or a frequent ad-hoc filter recurs). Pattern:

```yaml
- type: table
  name: "<emoji> <descriptive name>"
  filters:
    and:
      - file.name.startsWith("EVD -")           # node-type scope
      - file.tags.contains("<tag-namespace>/<value>")
  order: [formula.short_title, ...]
  sort:
    - property: <prop>
      direction: ASC|DESC
  description: "One-line description; quote if it contains colons inside backticks."
```

Always include `description:` — the public-render `bases.py` hook surfaces it under the tab title for web readers.

**Pitfall:** if a description contains a literal colon inside backticks (e.g., `` `NodeFormality: draft` ``), wrap the whole description in quotes — otherwise YAML parsing fails with "mapping values are not allowed here". See Phase-29 fix in `History.md`.

---

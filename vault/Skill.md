---
name: extract-discourse-nodes
description: Extract a full set of discourse graph nodes from a scientific paper PDF — Questions (QUE), Claims (CLM), Evidence (EVD), and Caveats (CVT) — for a given research question. Outputs structured Obsidian-compatible markdown files with embedded figure/table screenshots and quote-region screenshots.
argument-hint: <path-to-pdf> for <research-question-or-link>
allowed-tools: Read, Write, Bash, Glob, Grep
---
You are extracting a complete set of discourse graph nodes from scientific papers given to you as PDFs. The five node types together map the paper's argumentative structure: what was asked (QUE), what was found (EVD), what it means (CLM), where to be cautious (CVT), and which regularities span ≥2 papers (EP).

## Workflow at a glance

For one paper, in order:

1. **Parse the paper and extract PICOST records first (v2, 2026-11-24)** — LlamaParse Agentic Plus plus the PDF text layer as a second vote, then one PICOST record with locators per finding; see [Step 1](#step-1-read-the-paper). The older chunked PDF reading is the fallback.
2. **Identify all nodes** with atomicity (one finding per EVD, one limitation per CVT, etc.).
3. **Render screenshots** — full-page figure/table images via `pdftoppm`, plus quote-region crops via PyMuPDF (`fitz`). The pipeline automatically inserts canonical `{citekey}-{kind}-p{N}-{idx}.png` embeds with per-kind colour highlights — do NOT hand-write quote-region embed lines.
4. **Write the node files** following the templates below. EVD Methods Context uses the **What/How/Who schema** (`Study design` + `Method type` + `Tools` + DV/IV; `Procedure`; `Models / participants` + `Sample-size flow`) — see [Step 4](#step-4-write-the-node-files) and [Step 4b](#step-4b-paper-level-tripod-llm-table-in-the-source-file).
5. **Write the source-file TRIPOD-LLM table** in `source/@<citekey>.md` — 42 rows (Title/Abstract/Background/Objectives items 1–4 + Methods 5a–15 + Results 16a–18), with a **`Quote` column** (verbatim quote + `§/page` locator from the PDF, not a paraphrase — `Not reported`/`Not applicable` when the paper genuinely doesn't say it) alongside the ✅/⚠️/❌/➖ compliance icon per row. Item 17 (Performance) is per-EVD; the source-file row reads `` `per-EVD` `` as a code span.
6. **Synthesize the source-page top matter** at the top of `source/@<citekey>.md`, above the TRIPOD-LLM table. Three sections, all derived from the paper's discourse-graph nodes (no PDF re-read): (a) **structured abstract** with a Mermaid Results visualization (the Methods flowchart was dropped 2026-11-24), and (b) **Quality Appraisal** — a 10–11-row `Domain/Rating/Quote` table: the 5 methodological-quality domains plus one row per chip-backed Rigor signal (Data Leakage, Baseline Adequacy, Train/Dev/Test Hygiene, Multiple-Comparisons Correction, Human-Baseline Comparability, and Statistical Power only when the paper reports one), each rating grounded in a verbatim quote the same way as the TRIPOD-LLM table. See [Step 6 details](#step-6-structured-abstract-on-the-source-page).
7. **Run the screenshot pipeline:** `python3 scripts/quote_pipeline.py` — inserts canonical embeds for every quote that doesn't already have one. Use `--force` only when regenerating existing embeds in place.
8. **Build reverse links** with `scripts/reverse_links.py` (idempotent).
9. **Audit** — graph-attachment invariants (`scripts/` outline below) and verbatim-quote audit (`scripts/verbatim_audit.py`).
10. **Apply readability formatting** with `scripts/readability_pass.py`.
11. **Promote NodeFormality** for structurally-complete nodes; leave audit-flagged nodes as `draft`.
12. **Regenerate DGRAPH.md** with `scripts/build_dgraph.py`.
13. **Save the originating prompt** to `prompts/<date>-<short-name>.md` for provenance and **log all changes in `History.md`**.

### Downstream synthesis & rendering (after the per-paper extraction loop)

These layers sit on top of the discourse graph and are produced by combining EVDs/CLMs/CVTs across multiple papers. They get refreshed in batches, not per-paper. See [Step 11](#step-11-cross-paper-synthesis-evidencepatterns--review-arena) and following.

14. **Cross-paper EvidencePatterns** — extract `EP` nodes into `evd-patterns/` whenever ≥2 papers' EVDs converge on the same regularity. Each EP node bundles supporting EVDs across papers and surfaces a pattern statement that no single paper makes alone.
15. **Cross-link EPs ↔ QUEs** — run `misc/scripts/link_eps_to_ques.py` to add a `### Cross-paper patterns` section to each QUE listing the EPs that draw on its source paper.
16. **TL;DR callouts on source pages** — run `misc/scripts/add_tldr_callouts.py` to insert a `> [!success] TL;DR` block above every source page's structured abstract, derived from the page's existing `**Bottom line.**` paragraph.
17. **Review-Arena leaderboard** — `Review-Arena.md` is the public-facing head-to-head view of the corpus. **AI does not fill in the cells** (Subtask + Winner + scores + Effect size). Cells are filled by humans working from the EVDs/EPs the human-AI dyad has already extracted; see [governance principle 16](#key-principles).
18. **EVD-count refresh on Review-Arena** — run `misc/scripts/count_evds_per_subtask.py` to refresh the `→ N EVDs` caption next to each Subtask name (auto-derived from each linked QUE's nested CLM → EVD list).
19. **Public render** — `cd public && .venv/bin/mkdocs build -f mkdocs.yml --clean` rebuilds the static MkDocs Material site. Live-preview with `mkdocs serve`. The four hooks in `public/hooks/` transform Obsidian-specific markdown (`![[*.base]]`, `[[wikilinks]]`, table-sort markers, rigor badges) into web-compatible HTML.
20. **ESS Bases refresh** — when new tag namespaces are added (e.g., a new `cvt/mechanism/<name>`), update `ESS.base` formulas + add views as needed; run a build to confirm the new tabs render.

### Scaling — multiple papers in one batch

When processing many papers (e.g., a backfill or a corpus-wide schema change), parallelize across subagents (one paper per subagent). Constraints learned from the Phase 18 batch:

- **Watchdog timeout is 10 min of no-progress.** Subagents that stall on long PDFs + many EVDs will be killed mid-stream. Mitigations:
  - Read PDFs in 10-page chunks (`Read` with `pages: "1-10"`, then `"11-20"`, …) — never request the whole PDF at once for >20-page papers.
  - One `Write` call per file. Don't read-back to verify formatting; trust the diff.
  - Skip exploratory tool calls (extra `ls`, `grep`, `cat`) once you have what you need.
- **Watchdog kills are recoverable.** Failed agents often completed most of the work before stalling. Before re-launching, check the artifact state (`grep -l "updated: <today>" evidence/EVD*-@<citekey>.md`, `wc -l source/@<citekey>.md`) and re-launch only what's missing.
- **Pipeline run is the parent's job, not the subagent's.** Subagents must NOT insert quote-region embed lines and must NOT run the screenshot pipeline — they only write markdown. The parent runs `quote_pipeline.py` once after all subagents return so naming is globally consistent.
- **Each subagent prompt should reference a shared brief** (e.g., `misc/prompts/<date>-<task>.md`) rather than duplicating the schema 26 times in the parent's message.

## Vault structure

```
living-synthesis/
├── DGRAPH.md                       # Central nested index of QUE → CLM → EVD → CVT
├── DGRAPH-TABLE.md                 # paper × node-type matrix (skim what each paper contributes)
├── ESS - Demo.md                   # Wrapper around ESS.base (the live filterable index)
├── ESS.base                        # Obsidian Bases definition: 6 formulas + 23 views
├── History.md                    # Chronological log of all concrete changes (newest first)
├── Log.md                          # Session-log scratch
├── Review-Arena.md                 # Public-facing leaderboard (subtask × AI/Human/Hybrid)
├── Skill.md                        # This file
├── Welcome.md                      # Vault overview for novices
├── paraphrase_audit_<date>.tsv     # Latest verbatim-audit report
├── claims/                         # CLM nodes (one .md per claim)
├── caveats/                        # CVT nodes (one .md per limitation)
├── evd-patterns/                   # EP nodes (cross-paper EvidencePatterns; ≥2 EVDs each)
├── evidence/
│   ├── EVD - ... .md               # EVD nodes (one .md per finding)
│   └── Attachments/                # All PNGs (figure/table pages + quote crops)
├── questions/                      # QUE nodes (one .md per research question)
├── source/
│   ├── @<citekey>.md               # Bibliographic source notes (one per paper)
│   └── pdfs/                       # Original PDFs
├── templates/                      # T - <NodeType>.md templates
├── misc/
│   ├── prompts/                    # Originating user prompts for generated docs
│   └── scripts/                    # Helper scripts (see scripts/README.md)
├── public/                         # Sidecar: public-facing MkDocs Material site
│   ├── mkdocs.yml                  # MkDocs config (docs_dir → vault root, site_dir → outside vault)
│   ├── hooks/                      # Build-time Python hooks (rigor_badges, leaderboard, bases, wikilinks)
│   ├── assets/                     # CSS + JS (extra.css, badges.css, leaderboard.css, sortable.js)
│   ├── README.md                   # Public-render quickstart
│   └── .venv/                      # Python venv (mkdocs + plugins; not committed)
└── .obsidian/
    └── snippets/
        └── wide-tables.css         # Obsidian-only CSS snippet for full-width leaderboard pages
```

> **Build output** was originally intended to live at `../living-synthesis-site/`
> via the MkDocs pipeline below (Step 12). **This is now stale**:
> `living-synthesis-site` has been independently rebuilt as a hand-maintained
> Next.js/Vercel app with its own copy of the vault content under its own
> `vault/` folder (imported once, edited separately ever since) and its own
> `scripts/build-graph.mjs` (Node, not Python/MkDocs). The two have fully
> diverged, and — as of 2026-08 — diverged in the *opposite* direction from
> what you'd expect: `living-synthesis-site`'s 27 source pages now have the
> newer quote-grounded TRIPOD-LLM (42-item) and Quality Appraisal (10–11-row)
> tables described in this Skill system, applied only to its own copy; **the
> canonical vault's own `source/*.md` files here still have the old 37-row
> TRIPOD table and 5-row Critical Appraisal table** — this Skill system's
> format was updated to match what shipped, but the ~184 actual node files in
> this vault (source/EVD/CLM/CVT/QUE) have not themselves been re-extracted
> to match yet. Porting that back is a real, separate task, not done as part
> of this doc update. The MkDocs pipeline (Step 12/13/14 below, `public/`
> folder) is left undisturbed and still works for the vault's own visual
> treatment — just don't assume it's what actually produces
> `living-synthesis-site` anymore.

> **New site-only feature (2026-08): the Evidence Quality table.**
> `living-synthesis-site` added a `/quality` page (`app/quality/page.tsx` +
> `components/EvidenceQualityTable.tsx` + `lib/qualityColumns.ts`) that has
> no vault-file counterpart — it's a pure rendering feature built on top of
> data this Skill system already produces, not a new node type or markdown
> convention. One row per EVD, one column per quality signal (Transparency,
> the four Validity domains, and every chip-backed Rigor/Openness/Integrity
> signal from Step 6/6.b), computed the same way the node-detail chips are
> (`getParentSource` to inherit paper-level signals onto each EVD row). It
> supports a dynamic column picker (any signal can be added/removed, Source
> hidden by default), click-to-sort on every column, a text filter, a
> leftmost EP column (via `getEvidencePatternsForEvd`) so rows can be
> clustered by cross-paper pattern, and a single Export dropdown
> (.md/.csv/.xlsx). Cell text is plain (no color-coded tone) — the
> underlying green/gold/red/gray judgment is kept only as an internal sort
> key. **When extracting a new dataset/corpus for a future
> `living-synthesis-site`-style app, replicate this page**: it's the fastest
> way to audit quality-signal coverage/consistency across every finding at
> once, and needs nothing beyond the per-EVD/per-Source signal data this
> Skill system already extracts.
>
> **Lesson from this rollout, worth repeating for a future corpus:**
> `living-synthesis-site`'s graph view (`components/GraphExplorer.tsx`) has
> its own, separately-maintained "Trust signals" filter dropdown
> (`TRUST_SIGNAL_OPTIONS`) that mirrors the same chip catalog as `/quality`
> but is hand-written against it rather than importing `QUALITY_COLUMNS`
> directly — it had drifted more than a dozen signals behind before being
> caught and brought back to parity (2026-08). Whenever a new chip/signal
> type is added to this Skill system (a new Step 6.b Rigor row, a new
> Openness/Integrity check), treat the graph view's filter as a required
> update alongside the node-detail chips and the `/quality` table, not an
> optional one — the three currently have to be kept in sync by hand.

> **New Integrity check (2026-08): AI Writing Check, with two triggers.**
> Run an independent AI-text-detection recheck of a source's own prose via
> Pangram (`misc/scripts/pangram_check.py` in this vault — Python,
> `pip install pangram-sdk`, needs a `PANGRAM_API_KEY` env var, uses
> `predict_files()` — the bulk multipart-upload endpoint, one request for
> every PDF in the batch, not one request per file — against the source
> PDFs) whenever **either**: (a) a source's Statistic Accuracy check (Step
> 6.b) comes back `issues-found`, or (b) a source's Data Repo Check and/or
> Code Check comes back "No repository claimed" (its data/code transparency
> can't be verified another way, so its prose gets an extra look instead).
> The script is idempotent — it skips (and doesn't re-submit/re-bill) any
> paper whose SRC file already carries an `integrity/ai-writing-check/*`
> tag, so re-running it after adding new trigger criteria only processes
> genuinely new papers. Tag the result on the SRC file as
> `integrity/ai-writing-check/{addressed|partial|unresolved}` (reusing the
> standard 4-level rigor-check tag vocabulary: `addressed` = Pangram's
> "Human" verdict, `partial` = "Mixed"/AI-assisted detected, `unresolved` =
> predominantly AI-generated) and add a matching **AI Writing Check** row to
> the Quality Appraisal table, citing the Pangram dashboard link in place of
> a paper quote (this is the one appraisal row that isn't grounded in the
> paper's own text — it's an external tool's verdict on that text). This
> check is deliberately narrow-scoped, not corpus-wide — a paper with clean
> numbers and verifiable data/code doesn't need it. As of 2026-08, 16 of 27
> sources qualify (2 via trigger (a), 14 via trigger (b)); 14 came back
> clean, 2 came back "Mixed" (flagged `partial`, roughly 13-14% AI-generated
> text each). Wired into `lib/data.ts` (`getAiWritingCheck`,
> `AI_WRITING_CHECK_LABELS`), the `RigorCheckBadge` component in
> `TopBadges.tsx`, `lib/qualityColumns.ts`, and the graph view's Trust
> signals filter, following the exact pattern of every other rigor check —
> see the lesson above about keeping all three in sync. The Pangram model
> version and the date this signal went into use are disclosed on
> `living-synthesis-site`'s About page footer and its README.md. Pangram's
> AI-**image** detector is a research preview with no documented stable API
> as of this writing; skipped for now.

> **New forensic-check kind (2026-08): `reproduction-check` — analytic
> reproducibility from a source's own released data.** Stronger than the
> existing `f1-check`/`kappa-check`/`ci-check`/etc. (which only recompute
> from numbers already printed in the paper): this one recomputes an EVD's
> headline statistic from the paper's actual released raw dataset, when
> doing so is possible without re-running an LLM ourselves or retraining a
> model (re-running an LLM would test *today's* model, not verify the
> paper's original claim — explicitly out of scope). Tag as
> `forensic/reproduction-check/{match|mismatch|partial}` on the specific
> EVD, in the same `forensic/*` namespace `getForensicSignalsForEvd` already
> reads (add "match" to `CLEAN_RESULTS` in `getStatisticalConsistency` —
> already done). Only 1 of 27 sources has been fully verified this way so
> far (Liu & Shah 2023, ReviewerGPT — 86.55% recomputed vs. 86.6% reported,
> exact match) plus one unresolved partial (Woelfle et al. 2024 — right
> ballpark, exact ranges don't line up). The full per-source audit — which
> repos have real raw data vs. just code, which require live LLM calls, and
> which repo URLs weren't captured precisely enough during extraction to
> even locate — is saved as `misc/reproducibility_triage_*.md` in this
> vault. Treat that file as a standing to-do list, not a one-off report:
> Huntington-Klein & Murray 2024 and Wu et al. 2024 both have real,
> already-confirmed-present raw data and are worth finishing (the former
> needs a careful methods-read to fix the exact kappa computation, the
> latter needs a Python ML environment to run a training script), and at
> least 3 sources (Wrightson 2025, Zhang 2024 reference-errors, Idahl 2025)
> were blocked only because the extracted TRIPOD-LLM item 14e/14f rows
> didn't capture a precise-enough repo URL — worth a direct PDF re-check
> rather than treating them as genuinely infeasible.

> **New Openness signal (2026-08): Code Quality, via `howfairis`.** Distinct
> from Data Repo Check/Code Check (which only ask "does the link resolve"):
> this asks whether a source's released code repo follows baseline
> open-source hygiene, per the fair-software.eu 5-criteria checklist (open
> repository, license, package-registry listing, citation metadata,
> quality-checklist badge). Run via `pip install --user howfairis` then
> `howfairis <github-or-gitlab-url>` — no API key, works locally, but
> **only supports github.com and gitlab.com** (not HuggingFace, OSF, or
> other hosts — those sources are silently skipped, same "not yet checked"
> convention as Statistical Power). Tag the result on the SRC file as
> `top/code-quality-fair/{0-5}` (the raw count of criteria met) and add a
> matching **Code Quality** row to the Quality Appraisal table, citing the
> tool + repo URL + score breakdown in place of a paper quote (another
> appraisal row grounded in an external tool's verdict, not the paper's own
> text — same pattern as AI Writing Check). As of 2026-08, 13 of 27 sources
> have a checkable repo; every one scored only 1/5 or 2/5 — worth
> re-running this check on any newly extracted source with a GitHub/GitLab
> repo link, since so far the result has been uniformly low across this
> corpus. Wired into `lib/data.ts` (`getCodeQualityFair`), a new
> `CodeQualityBadge` in `TopBadges.tsx`, `lib/qualityColumns.ts`, and the
> graph view's Trust signals filter — see the lesson above about keeping
> all three in sync.

> **New Openness signal (2026-08): Data Quality, via FAIR-Checker — a
> hybrid score, not a raw tool output.** Distinct from Data Repo Check
> (which only asks "does the link resolve") and from Code Quality (which
> only covers GitHub/GitLab code, not datasets): this asks whether a
> source's released *dataset* is FAIR, on a 0-24 scale, using
> [FAIR-Checker](https://fair-checker.france-bioinformatique.fr)'s REST API
> (`GET /api/check/metrics_all?url=<url>`, 12 semantic-web metrics scored
> 0-2 each, no auth). FAIR-Checker works on any URL (GitHub, OSF,
> HuggingFace), unlike `howfairis` — but a **raw** FAIR-Checker score against
> a plain GitHub repo page is meaningless: GitHub carries no schema.org/
> JSON-LD metadata, so every GitHub-hosted dataset tested flatlined at an
> identical, uninformative 4/24 (only "Unique IDs" and "Open resolution
> protocol" ever passed). Do **not** report a raw FAIR-Checker score for a
> GitHub/GitLab-hosted dataset without the fix below — it will look like a
> real signal but isn't.
>
> The fix: for GitHub/GitLab-hosted data, add **+2** to the raw FAIR-Checker
> score if the repo has a real LICENSE file — reuse the license-detection
> result already known from that source's Code Quality (`howfairis`) check,
> since `howfairis` reads repo content directly in a way FAIR-Checker's
> page-metadata approach cannot. OSF and HuggingFace datasets carry real
> structured metadata already, so use FAIR-Checker's native score for those
> unmodified. Tag the result on the SRC file as
> `top/data-quality-fair/{0-24}` and add a matching **Data Quality** row to
> the Quality Appraisal table, citing the tool + dataset URL + score +
> (for GitHub/GitLab) a one-line note about the +2 top-up. As of 2026-08,
> 14 of 27 sources have a checkable dataset — full breakdown in
> `misc/data_quality_2026-08.md`. Two of those sources' dataset URLs
> (Wrightson 2025's OSF link, Zhang 2024's GitHub link) plus one HuggingFace
> link (Son 2025) weren't in the PDF's extracted text layer at all — found
> via each PDF's embedded hyperlink annotations (PyMuPDF `page.get_links()`
> → `uri`), worth trying on any source where a data/code URL seems to be
> missing despite a footnote-style citation marker in the visible text.
> Wired into `lib/data.ts` (`getDataQualityFair`), a new `DataQualityBadge`
> in `TopBadges.tsx`, `lib/qualityColumns.ts`, and the graph view's Trust
> signals filter — same three-places-to-sync pattern as every prior signal.

## Node Types and Their Roles

| Type             | Prefix | Role                                                | Grounding                                        |
| ---------------- | ------ | --------------------------------------------------- | ------------------------------------------------ |
| Question         | `QUE`  | Research questions the paper addresses              | Author's stated aims + inferred framing          |
| Evidence         | `EVD`  | Atomic empirical observations from data             | Direct quotes + figure/table + quote screenshots |
| Claim            | `CLM`  | Generalizations from EVDs (results)                 | Direct quotes that state what findings mean      |
| Caveat           | `CVT`  | Methodological limitations on EVDs                  | Author-stated or inferred; flagged accordingly   |
| EvidencePattern  | `EP`   | Cross-paper empirical regularities bundling 2+ EVDs | Wikilinks to constituent EVDs + cross-paper triangulation argument |

**Critical distinction — CLM vs. EVD:**
- EVD = *what was measured/observed* (e.g., "GPT-4 detected errors in 7 of 13 papers")
- CLM = *which generalization emerges from EVDs* (e.g., "LLMs are approximately as accurate as human experts at verifying adherence to reporting guidelines like GRADE risk of bias 2 (RoB 2).")
- Numbers and observations → EVD. Conclusions drawn from them → CLM.

**Critical distinction — CLM vs. CVT:**
- CLM = an affirmative generalization that the paper argues for using one or more EVDs
- CVT = a limitation that constrains what inferences can be drawn from EVDs to CLMs. Should be drawn from consensus, ideally empirically grounded, methodological best practices for a given method (e.g., "lack of prompt/context engineering" for an EVD that involves use of LLMs, or "violation of stable unit treatment value assumption" for a randomized controlled experiment)

---

## Inputs

The user will provide:
1. **A PDF path** — the paper to extract from
2. **A research question** — either inline text or a `[[QUE - ...]]` link. If a link, read it for context.
3. **An output directory** — if not specified, default to the same directory as the PDF, under a `Discourse Nodes/` subfolder.

---

## Step 1: Read the Paper

### v2 process (2026-11-24): parse, then PICOST first

> [!info] Why
> The 2026-11-17 audit of the 77 EVD pages found 147 suspected errors (wrong numbers 49, claims not in the paper 33, paper contradicting itself 19, wrong page 18, wrong model or rater 17, missing comparator 8, row or column shift 3). Every one of them passed the quote check. The steps below add the controls that were missing. Tool and model choices are in `Tools-and-Models.md` (v2 section).

1. **Parse with two independent reads.** (a) **GPT-6.2 Sol** reads the PDF directly (PDF input; reasoning effort High) and returns page-by-page markdown with each table as HTML, the printed journal page for every page, and every figure caption. (b) The PDF's own text layer with PyMuPDF for born-digital PDFs. Accept text, numbers and table cells only where the two agree. Where they disagree, or a page has no text layer, decide from the **rendered page image** (`pdftoppm -r 150 -f N -l N -png`), by Claude Opus 5.5 or a human; never from either extraction alone. Do not use `pdftotext -layout` for tables. (LlamaParse Agentic Plus was the first choice, then Gemini 4 Neon; JP could not get a Google API key on 2026-11-24 and chose GPT-6.2 Sol, so one model reads and extracts. Keep LlamaParse as the fallback if Sol misreads tables in the pilot.)
2. **Page map, built once per paper.** Record for every page both the PDF page position and the **printed journal page** (PyMuPDF page labels first, otherwise the number printed in the header or footer; mark preprints without printed numbers "PDF position only"). Every citation uses the printed page.
3. **Send Methods and Results first** (with their tables), and other sections only when a field is missing.
4. **PICOST first.** For each candidate finding write one record as JSON: Population, Intervention, Comparator, Outcome, Study design, Timeframe, the finding in one sentence, and every number. **Every number and every PICOST value carries a locator**: journal page, table or figure, row label, column label. Anything the paper does not state is `Not reported`; never fill a slot with plausible standard detail. The bulk extraction model is GPT-6.2 Sol at reasoning effort High (Medium for simple steps such as restyling, alt text and link repair; Max only if the pilot shows it removes errors that High leaves); Claude Opus 5.5 handles disagreements and tricky cases.
5. **Reconcile prose against tables.** When the text and the paper's own table disagree, use the table and record the disagreement in a note (`- PDF check <date>: ...`); never edit the quote.
6. **Check the whole table before "best".** Before any EVD says best, beat, matched or highest, read every row of the table and list every comparator that could change the claim (other models, human baselines, combined methods).
7. **QA gate (Step 6c), deferred.** The Liquid d1-ultra check of each PICOST record is on hold (JP, 2026-11-24); until it is switched on, the check is Opus 5.5 on every record flagged by a parser disagreement plus a 10% random sample, and a human spot check. Remind JP to revisit it after the first batch of new papers.
8. **Write the EVD from the PICOST cells.** The EVD statement may contain only numbers that appear in its PICOST record, so the statement, the PICOST row and the screenshot agree.
9. **Work from the most recent report (JP, 2026-11-24).** Prefer the published journal or proceedings version over a preprint, and the latest preprint version over earlier ones; keep the older PDF as `Archive - ...` in `source/pdfs/`, and cite the printed page of the version used. Do not silently move an existing page to a newer version: list it for JP (TODO 0d).
10. **Fix page-number errors when you find them (JP, 2026-11-24).** Whenever any step turns up a wrong page citation (printed versus PDF page, a quote that is not on the cited page), correct the citation in both the local vault and the repository copy, add the old and new value to the page's `PDF check` note, and log it; do not wait for a separate audit. Cite the version of the paper the page was built from (a version question goes to TODO 0d).
11. **Batch API for unattended runs, on every provider.** Run bulk steps (reading, PICOST extraction, drafting, verification) through each provider's Batch API: Anthropic Message Batches (50% off, stacks with prompt caching), OpenAI Batch (about half price; GPT-6.2 Sol $1 in and $5 out per million tokens, from third-party pages, to confirm on OpenAI's pricing page) and Gemini Batch if a Google key is ever available. Put the Skill instructions first and unchanged in every request so they are cached. Use the standard API only for pilots and when someone is waiting. Decision models such as d1-ultra have no batch mode and cost too little to matter. Log tokens, cost and time per paper and step.

Question rules for the QUEs you propose here are in Step 2 and in `Skill-templates.md` (QUE title phrasing rule, rules 1 to 12; keep each QUE's original wording as a quote).

### Cost controls (v2, 2026-11-24)

Follow these every run so JP does not have to remember them. Budget, per-batch caps and the ledger are in `misc/evd-validation/2026-11-24-ingest-budget-and-batches.md`.

1. **Work five papers at a time** with the human spot checks A and B in that file; stop a batch that costs more than 1.5 times its estimate or that shows an error at a check.
2. **Batch APIs for everything nobody is waiting on** (reading, extraction, writing, verification); standard API only for the pilot and the first batch.
3. **Cache the Skill:** put the Skill and instructions first and unchanged in every request.
4. **Send only what is needed:** Methods and Results with their tables first; skip references, appendices and acknowledgements; fall back to other sections only when a field is missing.
5. **Use the free second read:** the PDF text layer is the second vote; send page images to the model only for pages with tables or figures.
6. **Escalate by exception:** Opus 5.5 only where the two reads disagree, plus a 10% random sample, not on every record.
7. **Short structured output:** PICOST as compact JSON; GPT-6.2 Sol at High for reading and extraction, Medium for restyling, alt text and link repair; never Max unless a pilot shows it removes errors High leaves.
8. **Screen before reading:** remove duplicates and off-topic papers with a cheap relevance call (Perplexity Decider 1.3 or Liquid d1-ultra) before the full read.
9. **Pilot, then reuse:** fix the prompts on five papers, save every step's output, and resume instead of rerunning.
10. **Describe screenshots in one batch call** at Medium; skip alt text for purely decorative crops.
11. **Log tokens and dollars per paper and step** in the ledger and keep a hard spending cap on each provider account.

### Fallback: reading the PDF in chunks

(The v1 procedure, kept for when the parsers are unavailable.)

Read the PDF in page chunks (the Read tool supports a `pages` parameter for PDFs). Start with pages 1–5 to understand structure, then read the results, discussion, conclusion sections thoroughly.

As you read, track:
- The paper's explicit research questions and stated objectives
- The study design (experimental, observational, benchmarking, etc.)
- Key sample and population
- Main measures and outcomes
- Each distinct empirical finding (→ EVD candidates)
- Authors' generalization(s) flowing from one or more EVDs (→ CLM candidates)
- Stated limitations and methodological caveats (→ CVT candidates, type: author-stated)
- Limitations you can infer that authors did not state (→ CVT candidates, type: inferred)
- A passage that describes **what was measured** (for the EVD's What slot)
- A passage that describes **how it was measured** (for the How slot)
- A passage that describes **who/what was measured** — sample, dataset (for the Who slot)

---

## Step 2: Identify All Nodes

Produce a node inventory before writing any files.

> [!tip] Questions (v2)
> Apply rules 1 to 12 of the QUE title phrasing rule in `Skill-templates.md`: one construct per question, no yes/no, neutral "LLMs" and "research reports", do not mirror the authors' wording, generalize beyond the sample, name the template used, and keep the original wording as a `### Original wording` quote on every QUE (split questions keep the full compound wording in each part).

**Questions (QUE):** What is the main research question? Are there sub-questions (different tasks, analytical angles, or comparisons)? Each distinct research question = one QUE node. Phrase every QUE title per the **QUE title phrasing rule** in `Skill-templates.md` (canonical template table, "LLMs"/"research reports" as subject/object, degree framing, splitting compound questions) — check the template table before coining a new phrasing.

**Evidence (EVD):** Each distinct statistical test, empirical observation, or analytical finding = one EVD. Do NOT collapse multiple findings into one. Atomicity is essential. Every EVD (and every CLM/EP downstream of one) must also carry a **`task/<slug>` tag** naming which evaluative task the finding is *about* — e.g. `task/risk-of-bias-assessment`, `task/novelty-assessment` — distinct from and in addition to any `5c/*` or `appraisal/*` tags. This answers "what does this finding say about LLM performance on X" as opposed to "how trustworthy is this study," a distinction an advisor flagged in 2026-08 as missing from the corpus. The full 16-value taxonomy (grouped under the 5 Cs plus a "Cross-cutting" bucket for findings about the evaluator's general behavior — prompt sensitivity, cost, fine-tuning — rather than one task) lives in `living-synthesis-site`'s `lib/data.ts` (`TASK_ORDER`/`TASK_LABELS`/`TASK_GROUPS`) and drives that site's graph-view "Evaluative task" filter; check there for the current value list and add a new value (in both this doc and that file) only when an existing one genuinely doesn't fit, rather than inventing a near-duplicate.

**Claims (CLM):** Which generalizations from their data/EVDs do the authors draw? Each distinct conclusion = one CLM. Must be traceable to at least one EVD or direct author quote.

**Caveats (CVT):** Which limitations do the authors explicitly state? What limitations can you infer from the methods (e.g., no pre-registration, small N, convenience sample, single model tested, GUI instead of API prompting)? Each distinct limitation = one CVT.

CVT nodes capture a single methodological limitation. They are organized around which papers the limitation applies to.

**Notes on CVT Properties:**
- The `title` field IS the node identifier — it must include `[[CVT]]` literally
- `type: author-stated` = the authors themselves named this limitation; use a direct quote
- `type: inferred` = you identified this as a limitation based on methodological reasoning; the quote should be the closest relevant passage (e.g., the methods description that reveals the gap), and add a brief explanation in brackets after the quote: `[Inferred: this is a limitation because...]`
- `appliesTo`: link to the EVD or CLM nodes whose validity is most affected by this caveat
- CVT titles should be short but specific sentences in past tense — not just `CVT - small sample` but `CVT - The small sample limited generalizability.`
- CVTs can only be paper-specific and MUST apply to specific EVDs

**Naming:** `CVT - [short description of limitation].md`

Examples:
- `CVT - The small sample limited generalizability.md`
- `CVT - The models were only tested via GUI not API.md`
- `CVT - The paper did not include inter-rater reliability.md`
- `CVT - The data leakage problem from training corpus was not resolved.md`

---

## Step 3: Extract Screenshots (figures, tables, and quote regions)

Two kinds of screenshots ground a node: **figure/table images** for EVDs, and **quote region crops** for every direct quote embedded in any node. Both go into a single `attachments/` subdirectory in the output directory. Embed in Obsidian with `![[filename.png]]`.

### 3a. Figure/Table screenshots

For each EVD, identify which figure(s) and/or table(s) ground the finding, then render the whole page:

```bash
pdftoppm -f <page_num> -l <page_num> -r 250 -png "<pdf_path>" "<output_dir>/attachments/<citekey>-<label>-p<page>"
```

CLMs and CVTs generally do not require figure screenshots, but capture one if a figure is central to a claim or directly illustrates a limitation. QUEs should have screenshots of the framing passage.

### 3b. Quote region screenshots

For every direct quote embedded in an EVD, CLM, CVT, or QUE body, also produce a **cropped** PNG of just the quoted region — not the full page — with the quoted text visibly highlighted in a colour that identifies the node type.

**Two non-negotiable invariants:**
1. **The full quote must be inside the screenshot.** Never crop so tight that the closing words clip at the bottom (or sides). When in doubt, expand the bbox and accept extra context.
2. **Highlight the matched quote text** in the cropped image so the reader can see at a glance which words came from the quote vs. surrounding context.

**Highlight colour by node type** (light pastels keep underlying text readable):

| Kind | Colour | RGB (0–1)            |
| ---- | ------ | -------------------- |
| EVD  | light red   | `(1.00, 0.70, 0.70)` |
| CLM  | light green | `(0.72, 1.00, 0.72)` |
| QUE  | light blue  | `(0.72, 0.86, 1.00)` |
| CVT  | light gold  | `(1.00, 0.90, 0.55)` |

**Primary path: `scripts/quote_pipeline.py`** (PyMuPDF / `fitz`). It walks every node folder, locates each `> "..." (Author, Year, p. N)` quote, renders the crop with the colour highlight, and inserts/updates the `> ![[...]]` embed in place.

```bash
python3 scripts/quote_pipeline.py            # process all four kinds, skip existing
python3 scripts/quote_pipeline.py evd cvt    # restrict to specific kinds
python3 scripts/quote_pipeline.py --force    # regenerate existing screenshots in place
```

Output filenames: `<citekey>-{evd|clm|cvt|que}-p<N>-<idx>.png`. With `--force` the script preserves the existing filename so embeds in markdown don't have to be rewritten.

**Quote-location algorithm** (three passes; later passes are fallbacks):

1. **Full-segment match.** Build a normalized concat of all words on each candidate page (lowercase + alnum only). Split the quote on `...`/`…` and try to match each segment as a contiguous span. The bbox is the union of all matched segments — and every matched word rect is fed into `add_highlight_annot()` so the highlight is exact.
2. **Opening + closing window.** If the full segment doesn't match (paraphrase drift, OCR noise), match the first 3–8 words and the last 2–6 words. The bbox spans them; the highlight covers the contiguous range.
3. **Opening + tall-height fallback.** When only the opening matches, crop a 300pt tall region in the same column starting at the opening (was 90pt; 90pt was too short and clipped long quotes). Only the opening words get highlighted, but the rest of the quote is still visible.

Citekey resolution:
- **EVD / CVT** — citekey is read from the `## Source` block (`[[@<citekey>]]`).
- **CLM / QUE** — multiple papers in the `> [!info] Papers` block; each quote's citekey is resolved from its `(Author, Year)` attribution against that list (single-paper QUEs use the only citekey directly).

Rendering uses `page.add_highlight_annot(rects)` → `annot.set_colors(stroke=COLOR)` → `annot.update()`, then `page.get_pixmap(matrix=Matrix(250/72,250/72), clip=Rect(*bbox))`. Padding around the bbox is **12pt** (was 8pt; the extra margin keeps long descenders and adjacent characters intact).

Edge cases:
- **Quote crosses a column or page break** — Pass 1 will fail because no single page contains the full text. Either split the source quote in the markdown into two `> "..."` lines (one per column/page) so each gets its own crop, or accept the Pass-2/3 fallback on whichever page the opening lives.
- **En-dashes and em-dashes are mangled** by `pdftotext`. Common rendering: `Human−AI` → `HumaneAI`. fitz handles these slightly better but still imperfect. When choosing opening/closing match strings, **avoid words containing dashes** — pick a unique phrase a few words later.
- **Hyphenation at line breaks** — words split across lines appear as two separate `<word>` tags (e.g., `expen-` + `sive`). After alnum-normalization the substring match still works, but if a unique opening/closing falls on a hyphenated word, shorten the match window to skip it.
- **Ligatures** (`fi`, `fl`, `ffi`) usually decode fine via NFKD normalization, but exotic glyphs may not — fall back to matching on word stems.
- **No text layer (scanned PDF)** — fitz returns empty word lists. Fall back to a full-page screenshot and flag the paper as needing OCR before quote-region extraction is possible.
- **Cited page ≠ PDF page** — journals use article-internal page numbers (e.g., `p. 9341` in a 12-page PDF). The pipeline already searches all pages if the cited page misses.
- **MuPDF warnings** like `format error: No common ancestor in structure tree` or `syntax error: could not parse color space` are non-fatal — the screenshot is still produced.
- **Use the rendered table image as the source for numbers** (Step 6b). Do not retype a table from extracted text alone; a 2026-11-17 audit found row shifts, column shifts and swapped ± values caused by this.

---

### 3c. Cropping, highlighting and page numbers (v2)

- **Crop with coordinates, then verify.** Locate each quote or table with PyMuPDF word coordinates (not `pdftotext -bbox` alone), crop with `pdftoppm -x -y -W -H`, and re-run text search on the cropped image's OCR or on the crop region to confirm the whole quote is inside the crop. Reject a crop whose first or last word is cut off.
- **Table and figure crops** contain the table or figure and its caption only, every row, column and panel, no body text (see the grounding rules in `Skill-templates.md`). Do not screenshot the full page. Methods tables and method diagrams are cropped and embedded the same way.
- **Cross-check against the audit.** Compare each cropped table against the structured cells from Step 1 (two-tool agreement) before the screenshot is accepted: a mismatched row or column shift is the audit's error type 7, a value next to the wrong label is type 5.
- **Printed page in every citation.** Use the page map from Step 1. The screenshot filename may keep the PDF index (`p6`); the citation may not. If the paper has no printed numbers, write `PDF p. N` so a reader knows.
- **Alt text.** Add each screenshot's description to the alt-text map; the filename is never the alt text.

## Step 4: Write the Node Files → see `Skill-templates.md`

Each of the five node types has a body schema with required slots. The full templates (EVD with What/How/Who, CLM, CVT with author-stated/inferred distinction, QUE with the question-only quote rule) live in **`Skill-templates.md`**, along with the `Step 4b` paper-level TRIPOD-LLM table format (42 items × 4 columns, including a verbatim-quote `Quote` column), and `Step 6` structured-abstract specifics (5-section schema + a Mermaid Results visualization + the 10–11-row, quote-grounded Quality Appraisal table).

EP node format is in **`Skill-synthesis.md` Step 11** (different shape — pattern statement + ≥2 papers' EVDs + cross-paper triangulation argument).

## Step 5: Build Reverse Links → see `Skill-templates.md`

Run `misc/scripts/reverse_links.py` to populate inbound sections (`## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence`, `### Supporting Claims (with their evidence)`). Idempotent. **Step 5b**: audit the four discourse-graph attachment invariants (CVT→EVDs only, every CLM in some QUE, every EVD in some CLM, every EVD in some QUE). Inline audit script in `Skill-templates.md`.

## Step 6: Verbatim Audit → see `Skill-templates.md`

`misc/scripts/verbatim_audit.py` compares every quote against its source PDF (NFKD + alnum normalization). Saves report as `paraphrase_audit_<date>.tsv`. Severity tiers (Tier 1: 0% match, Tier 2: <50%, Tier 3: 50–90%, Tier 4: >90%) and known false positives (en-dash mangling) are documented in `Skill-templates.md`.

> [!warning] The verbatim audit checks quotes only, not numbers
> Added 2026-11-17. A PDF audit of all 77 EVD pages found 147 suspected errors in numbers, tables, page references and attributions, while every quote had passed this step. Quotes passing is not evidence that a page is correct. Run Step 6b as well.

## Step 6b: Numeric audit (added 2026-11-17)

Every number outside a verbatim quote (Other Notes tables and bullets, Methods Context N / dates / settings, cited page and table numbers, and words like "best", "highest", "significant") must be traced to a specific place in the PDF before a page leaves `draft`.

1. **Record provenance as you write.** For every table or number, note the PDF page and table/figure it came from, e.g. `(Table 3, p. 7)`.
2. **Read tables from the image, not only from extracted text.** `pdftotext -layout` interleaves two-column pages and loses column alignment. Render the page (`pdftoppm -r 150 -f N -l N -png`) and read it. Check the rows above and below, and the columns either side, of every value you copy.
3. **Check the whole table before writing "best", "beat" or "matched".** Include every comparator that could change the claim (other models, human baselines, combined methods), with its value.
4. **If the paper's text and its own table disagree, use the table and add a note** (`- PDF check <date>: ...`). Do not edit the quote.
5. **Use the exact PDF version the page was built from**, and store it in `source/pdfs/` (with supplements). Record the version (e.g. arXiv v3, date) on the source page.
6. **Second pass by a fresh-context checker** that sees only the page and the PDF, never the drafter's reasoning. It verifies each number and proposes exact `{old, new}` fixes; only verified fixes are applied.
7. **Propagate fixes downstream.** A corrected page must also be corrected in every copy that uses it (the GSheet, PICOST, and the GitHub vault that builds the LIVES site), or the pending copies must be logged.

Full record of the 2026-11-17 audit, the seven error types it found and why they happened: `misc/evd-validation/2026-11-17-pdf-number-audit.md`.

## Step 6c: QA gate with a decision model (v2, deferred 2026-11-24)

After extraction and before drafting EVDs, send every PICOST record to the **Liquid d1-ultra** decision model (`d1-ultra`, `api.liquid.ai/decisions/v1/systemone`; keys in `~/.config/lives-ai-raters/.env`). Ask calibrated yes/no questions with the table or page image attached, for example: *Does this table show the value V in the row labelled R and the column labelled C?* and *Is V attributed to model M and not to a neighbouring row?* Records with P(yes) below 0.9, and any record whose quote or numbers the two parsers disagreed on, go to a human or to the Opus 5.5 spot check. **Status: untested and on hold (JP, 2026-11-24); remind JP after the first batch of new papers.** Before relying on it, measure it on the 2026-11-17 audit's 147 corrections (wrong and corrected values) and set the threshold from that. Our benchmark (`benchmarking-validation/`) found the decision models reliable on quote and table/figure grounding (about 97%) and not on fidelity, so use the gate for grounding and numbers, not for judging whether a headline is supported.

## Step 7: Readability Formatting → see `Skill-templates.md`

`misc/scripts/readability_pass.py` applies four mechanical formatting passes (blank line after headings, `>` separator before screenshot embeds, blank line between consecutive list-item wikilinks, collapse triple-newlines).

## Step 8: Promote NodeFormality → see `Skill-templates.md`

Promote `draft → ReadyForInternal` once Steps 5–7 and the Step 6b numeric audit pass and the structural-completeness bar is met. `ReadyToShare` is a manual-review-only state.

## Step 9: Regenerate DGRAPH.md → see `Skill-templates.md`

`python3 misc/scripts/build_dgraph.py` rebuilds the central nested QUE → CLM → EVD → CVT index. Re-run after every paper, every CLM/QUE structural change, every CVT `appliesTo` edit.

## Step 10: Save the originating prompt + log to History.md → see `Skill-templates.md`

Save the user's request (verbatim) to `misc/prompts/<YYYY-MM-DD>-<short-slug>.md`. Append a phase entry to `History.md` describing every concrete change (files added/edited/deleted, PNG counts, scripts used, follow-ups).

## Step 11: Cross-paper synthesis (EvidencePatterns + Review Arena) → see `Skill-synthesis.md`

The discourse-graph layer (QUE/CLM/EVD/CVT) is paper-internal. The synthesis layer is **cross-paper**: EvidencePatterns (`evd-patterns/`) bundle ≥2 EVDs from independent papers that converge on the same regularity. **Review-Arena.md** is the public-facing leaderboard (subtask × AI/Human/Hybrid). **Cell-level synthesis on Review-Arena is human-only** — AI extracts and proposes, humans commit. See `Skill-synthesis.md` Step 11 for the EP node format, the Review-Arena schema, the Subtask verb-first naming convention, and the merge-map proposal pattern.

## Step 12: Public render via MkDocs Material → see `Skill-synthesis.md`

`cd public && .venv/bin/mkdocs build -f mkdocs.yml --clean` builds the static MkDocs Material site at `../../living-synthesis-site/`. Four hooks (`rigor_badges.py`, `leaderboard.py`, `bases.py`, `wikilinks.py`) transform Obsidian-specific markdown into web HTML. Hook execution order, asset list (extra.css, badges.css, leaderboard.css, sortable.js), and `exclude_docs:` rules in `Skill-synthesis.md` Step 12.

## Step 13: Obsidian visual treatments → see `Skill-synthesis.md`

The `.obsidian/snippets/wide-tables.css` snippet, activated via `cssclasses: [wide-tables]` in a note's frontmatter, drops the readable-line-length cap on leaderboard pages without affecting other notes. Sort/filter on Review-Arena tables works only on the public web view (sortable.js); to bring sort/filter into Obsidian, the user can install the `Sortable` or `Dataview` community plugin (do not auto-install).

## Step 14: ESS Bases (live filterable index) → see `Skill-synthesis.md`

`ESS.base` defines an Obsidian Bases view with 6 formulas + 23 views (covering node-type, TRIPOD-LLM compliance buckets, critical-appraisal high-risk, 5C dimensions, CVT methodologist filters, drafts, and the original cards view). When new tag namespaces appear, add a categorical formula + a view in `ESS.base`. The `bases.py` MkDocs hook surfaces the same views as Material tabs on the public site.

---

## Reference docs

- **`Skill-templates.md`** — Steps 4–10: full node-file templates, the TRIPOD-LLM table format, audit invariants and audit scripts, structured-abstract schema, Mermaid visualizations, critical-appraisal calibration, NodeFormality promotion criteria, DGRAPH regeneration, prompt provenance.
- **`Skill-synthesis.md`** — Steps 11–14: EvidencePattern node format, Review-Arena schema + governance, Subtask naming + merge-map pattern, MkDocs build pipeline + hooks + assets, Obsidian visual treatments, ESS Bases formulas + views.
- **`Skill-references.md`** — Naming conventions (file + PNG), the 19 Key Principles (verbatim quotes, atomicity, EVD≠CLM, governance, EP threshold, render-pipeline duality), Common Pitfalls (Methods Context, TRIPOD icons, screenshot pipeline, subagent batching, source-file structure, cross-layer scripting traps), the After-Extraction summary table.

Load each as needed. The full per-paper extraction loop spans Skill.md (this file) + Skill-templates.md + Skill-references.md. Cross-paper synthesis + public render adds Skill-synthesis.md.

---
page_type: reference
created: 2026-11-24
---

# Vault structure (moved out of Skill.md on 2026-11-24)

Full folder tree and file-format notes for the vault. `Skill.md` keeps a short summary.

```
living-synthesis/
├── Welcome.md                      # Vault overview for novices (the only file at the root)
├── sysrev/                         # The systematic-review content
│   ├── dgraph/                     # The discourse-graph nodes
│   │   ├── questions/                  # QUE nodes (one .md per research question; attachments/ holds its crops)
│   │   ├── claims/                     # CLM nodes (one .md per claim)
│   │   ├── evidence/
│   │   │   ├── EVD - ... .md           # EVD nodes (one .md per finding)
│   │   │   └── Attachments/            # All PNGs (figure/table pages + quote crops)
│   │   ├── caveats/                    # CVT nodes (one .md per limitation)
│   │   ├── evd-patterns/               # EP nodes (cross-paper EvidencePatterns; ≥2 EVDs each)
│   │   └── source/
│   │       ├── @<citekey>.md           # Bibliographic source notes (one per paper)
│   │       └── pdfs/                   # Original PDFs (+ Archive - superseded versions)
│   ├── picost/                     # PICOST notes (local vault only)
│   ├── indexes/                    # dgraph.md (central nested index), DGRAPH-TABLE.md, Review-Arena.md, ESS - Demo.md, ESS.base, EvidencePattern Nodes.base
│   ├── reference/                  # BenchmarkLLM.md, Class-Imbalance-Text-Classification.md, paraphrase_audit_<date>.tsv (latest verbatim-audit report)
│   └── Clippings/                  # Web clipper inbox (local vault only)
├── pipeline/                       # Meta content about how the review is built and published
│   ├── skills/                     # Skill.md, Skill-references.md, Skill-synthesis.md, Skill-templates.md, Tools-and-Models.md
│   ├── templates/                  # T - <NodeType>.md templates
│   ├── scripts/                    # Helper scripts (see pipeline/scripts/README.md)
│   ├── logs/                       # History.md (chronological change log, newest first), Log.md (session-log scratch)
│   ├── legal/                      # LICENSE-CONTENT.md
│   ├── misc/
│   │   ├── prompts/                # Originating user prompts for generated docs
│   │   └── scripts/                # Helper scripts (older copy)
│   └── public/                     # Sidecar: public-facing MkDocs Material site (local vault only)
│       ├── mkdocs.yml              # MkDocs config (docs_dir → vault root, site_dir → outside vault)
│       ├── hooks/                  # Build-time Python hooks (rigor_badges, leaderboard, bases, wikilinks)
│       ├── assets/                 # CSS + JS (extra.css, badges.css, leaderboard.css, sortable.js)
│       ├── README.md               # Public-render quickstart
│       └── .venv/                  # Python venv (mkdocs + plugins; not committed)
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
> canonical vault's own `sysrev/dgraph/source/*.md` files here still have the old 37-row
> TRIPOD table and 5-row Critical Appraisal table** — this Skill system's
> format was updated to match what shipped, but the ~184 actual node files in
> this vault (source/EVD/CLM/CVT/QUE) have not themselves been re-extracted
> to match yet. Porting that back is a real, separate task, not done as part
> of this doc update. The MkDocs pipeline (Step 12/13/14 below, `pipeline/public/`
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
> Pangram (`pipeline/misc/scripts/pangram_check.py` in this vault — Python,
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
> even locate — is saved as `pipeline/misc/reproducibility_triage_*.md` in this
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
> `pipeline/misc/data_quality_2026-08.md`. Two of those sources' dataset URLs
> (Wrightson 2025's OSF link, Zhang 2024's GitHub link) plus one HuggingFace
> link (Son 2025) weren't in the PDF's extracted text layer at all — found
> via each PDF's embedded hyperlink annotations (PyMuPDF `page.get_links()`
> → `uri`), worth trying on any source where a data/code URL seems to be
> missing despite a footnote-style citation marker in the visible text.
> Wired into `lib/data.ts` (`getDataQualityFair`), a new `DataQualityBadge`
> in `TopBadges.tsx`, `lib/qualityColumns.ts`, and the graph view's Trust
> signals filter — same three-places-to-sync pattern as every prior signal.

---
author: Claude (Sonnet 5.5), for Jay Patel
page_type: index/methods
created: 2026-11-24
generated_by: tag survey of the 27 source pages and 77 EVD pages (2026-11-24)
human_verified: no
---

# Quality signals: the tags the web app reads

The LIVES web app shows Quality Signals tables on node pages and on `/quality`. Each signal is a frontmatter tag like `rigor/confidence-intervals/not-addressed`. A missing tag shows as an empty cell. This list is what the vault uses today (surveyed 2026-11-24); a new paper must get the same tags. Check with `python3 pipeline/scripts/check_quality_signals.py`. How they are produced is in `Skill-controls.md` Module Q.

Legend: **S** = on the source (SRC) page; **E** = on each EVD page. Values are the ones in use; `-` means the tag takes a number or is free-form.

| Group | Tag prefix | Level | Values in use |
|---|---|---|---|
| Validity | `appraisal/construct-validity`, `internal-validity`, `external-validity`, `statistical-rigor` | S and E | low-risk, some-concerns, high-risk |
| Validity | `appraisal/reproducibility` | E | low-risk, some-concerns, high-risk |
| Validity | `appraisal/overall` | E | `L<n>-M<n>-H<n>` counts of low, medium, high |
| Reproducibility | `trust/reproducibility` | S | low-risk, some-concerns, high-risk |
| Reporting | `tripod-llm/compliance` | E | low, moderate (high) |
| Reporting | `tripod-llm/proportion` | E | `<n>pct` |
| Rigor | `rigor/baseline-adequacy`, `human-baseline`, `train-dev-test`, `ablation-experiments`, `prompt-engineering`, `confidence-intervals`, `chance-corrected-metrics`, `multiple-comparisons` | S | addressed, partial, not-addressed |
| Rigor | `rigor/data-leakage` | S | addressed, partial, not-addressed, unresolved |
| Rigor | `rigor/statistical-power` | S | adequate (only when the paper has a power analysis) |
| Rigor | `rigor/sample-size-estimation` | S | not-done (or done) |
| Rigor | `rigor/study-type` | S | exploratory (or confirmatory) |
| Openness (TOP) | `top/study-registration`, `top/study-protocol` | S | not-applicable, not-disclosed, disclosed |
| Openness (TOP) | `top/code-transparency`, `top/data-transparency` | S | not-disclosed, level-1-disclosed, level-2-shared, not-applicable |
| Openness (TOP) | `top/code-check`, `top/repository-check` | S | addressed, partial, not-addressed |
| Openness (FAIR) | `top/code-quality-fair` | S | `-` (howfairis score 0 to 5, script) |
| Openness (FAIR) | `top/data-quality-fair` | S | `-` (FAIR-Checker plus 2, 0 to 24, script) |
| Transparency | `transparency/effect-size`, `transparency/exact-p-values` | S | addressed, partial, not-addressed |
| Integrity | `integrity/ethical-approval`, `funding-disclosure`, `coi-disclosure` | S | disclosed, partial, not-disclosed, not-applicable |
| Integrity | `integrity/spin` | S | addressed, partial, not-addressed |
| Integrity | `integrity/ai-writing-check` | S | addressed, partial (Pangram, script, optional) |
| Statistics | `forensic/*-check` (ci, closure, f1, kappa, monotonicity, reproduction) | E, only where a recomputation was possible | consistent, in-bounds, match, discrepancy, bounds-reversed |
| Topic (not a signal) | `task/*`, `5c/*` | E | see `Skill-references.md` |

## Locator standard (every judged row)
`` `<Section>, p.<printed page>[, Table <n> | Fig <n>]` `` after the quote, for example `` `Methods, p.9` `` or `` `Results, p.12, Table 2` ``. The page is the **printed journal page**. If the PDF prints no page numbers (preprints), write `p.<n> (pdf)` and nothing else. If the quote is on a page spanning two pages, cite the page where it starts. Rows judged from an external tool cite the tool, the URL and the score instead of a quote.
`audit_signal_quotes.py` checks this: quote verbatim in the PDF text, page equals the printed page label. Existing sources (2026-11-25, 27 sources): of 1,042 quoted rows, 579 are verbatim with the right printed page, 221 have the right PDF page where the PDF prints no number, 106 cite the wrong page, 72 quotes are not found (39 not in the text layer, 26 trimmed or edited, 6 typographic), 40 cite a PDF position on a PDF that prints numbers and 24 cite no page; 525 rows have no quote (NA or Not addressed). Punctuation and footnote marks are ignored; decimal points must match. Report: `pipeline/misc/evd-validation/2026-11-24-signal-quote-audit.csv`.

## Rules
- Every judged tag comes with a verbatim quote and a locator in the `## Quality appraisal` table; tags are regenerated from the table, not typed.
- Keep the headings `## Quality appraisal` and `## TRIPOD-LLM reporting` exactly; the app anchors on them.
- Author, journal and citation fields (`authorTrackRecord`, `pubType`, `selfCitationRate`, `doajListed`, `predatoryPublisherFlag`, `pubpeerCommentCount`, `nameConsistency`, `peerReviewStatus`, `citationCount`) are read by the graph build; no script in the repo produces them yet (to build: OpenAlex, DOAJ, PubPeer).
- Which model rated what: `pipeline/provenance/model-history.md` (the 27 existing sources: Claude Sonnet 5 re-curated the quotes and quality tables on 2026-08-25; the first drafts of 2026-04-28 have no recorded model). howfairis and FAIR-Checker now have scripts in `pipeline/scripts/provenance/`.
- **Row names come from one registry**, `pipeline/templates/quality-signal-labels.json` (rename there, then `quality_labels.py apply`). Current notable names: **Statistical Accuracy** and **Hype/spin**.
- **Statistical Accuracy** is scored with `stat_checks.py` (eighteen scripted checks on the paper's own numbers; see `Skill-controls.md` Module Q 3a and `Tools-and-Models.md`). Statuses: a finding is a clue for a person, no finding means nothing flagged, not verified.
- **Page rule:** when the PDF prints no page numbers (or a page prints none), the PDF page number is correct and is written `PDF p. N`.
- **Who rates and how ratings are combined (JP, 2026-11-25).** For new papers, every judged row is rated independently and blind by Gemini 4 Neon (High) and Claude Opus 5.5. If they agree, that is the tag. If they differ, GPT-6.2 Sol adjudicates only those rows (shown both answers with names hidden); Sol siding with one makes a majority, and three different ratings show as "no majority" for JP. Scripts check each quote and crop, and a decision model checks that the quote supports the rating. Every individual rating and the aggregate are logged to the Quality Signals benchmark sheet (`pipeline/skills/Review-sheets-spec.md`, section 3), which scores each model against JP's labels. Built 2026-11-25 as the `qs` stage of `lives_run.py` (25 signals; TRIPOD-LLM rows not yet); the cross-paper benchmark sheet is still to build.

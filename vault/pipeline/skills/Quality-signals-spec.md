---
author: Claude (Sonnet 5.5), for Jay Patel
page_type: index/methods
created: 2026-11-24
generated_by: tag survey of the 27 source pages and 77 EVD pages (2026-11-24)
human_verified: no
---

# Quality signals: the tags the web app reads

The LIVES web app shows Quality Signals tables on node pages and on `/quality`. Each signal is a frontmatter tag like `rigor/confidence-intervals/not-addressed`. A missing tag shows as an empty cell. This list is what the vault uses today (surveyed 2026-11-24); a new paper must get the same tags. Check with `python3 pipeline/scripts/check_quality_signals.py`. How they are produced is in `Skill.md` Step 6d.

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
`audit_signal_quotes.py` checks this: quote verbatim in the PDF text, page equals the printed page label. Existing sources (2026-11-24): of 999 quoted rows, 534 verbatim with the right printed page, 98 right page in a preprint without printed numbers, 157 cite the PDF position instead of the printed page, 104 cite a wrong page, 85 quotes not found, 21 give no page. Results per row: `pipeline/misc/evd-validation/2026-11-24-signal-quote-audit.csv`.

## Rules
- Every judged tag comes with a verbatim quote and a locator in the `## Quality appraisal` table; tags are regenerated from the table, not typed.
- Keep the headings `## Quality appraisal` and `## TRIPOD-LLM reporting` exactly; the app anchors on them.
- Author, journal and citation fields (`authorTrackRecord`, `pubType`, `selfCitationRate`, `doajListed`, `predatoryPublisherFlag`, `pubpeerCommentCount`, `nameConsistency`, `peerReviewStatus`, `citationCount`) are read by the graph build; no script in the repo produces them yet (to build: OpenAlex, DOAJ, PubPeer).
- Known gaps: nothing records which model rated the 27 existing sources; howfairis and FAIR-Checker have no script yet.

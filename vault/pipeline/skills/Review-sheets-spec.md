---
type: spec
title: Review sheets for runs and quality signals
status: built for the run review sheet (all tabs below except the benchmark and JP-label tabs of section 3); the benchmark scoring is specified
written: 2026-11-25
---

# Review sheets (JP, 2026-11-25)

Goal: a human can follow every step of a run, see each model's work, and add ground-truth labels later, so accuracy and cost per model can be scored. Sheets are Google Sheets made from workbooks the scripts build. Yellow-headed columns are the human's.

## 1. Run review sheet (built: `pipeline/scripts/run_to_gsheet.py RUN_ID`; every tab below is produced from the run folder)
| Tab | Content | JP columns |
|---|---|---|
| ABOUT | the run, the steps in order, how to review, the flags | none |
| Papers | one row per paper: status, pages, findings per tier, flagged, disagreements, cost | none |
| Findings | one row per extracted finding: tier and why, supports, statement, PICOST slots, numbers with locators, confidence, flags, recheck result, Opus verdict | tier right?, correct tier, statement and numbers right?, missed finding, notes |
| Checks | one row per quoted span: found in the PDF text, pages, word boxes | quote correct?, notes |
| Rechecks | Neon numbers against Sol numbers and Opus's verdict | who is right?, notes |
| Calls and cost | every model call: step, model, effort, tokens, cost | none |

### Added tabs (built 2026-11-25)
| Tab | Content | JP columns |
|---|---|---|
| Checks (decision models) | per finding: mean probability for relevancy, fidelity, quote grounding and table or figure grounding, the score (lowest mean), the spread between the three models, why Sol looked, Sol's vision verdict and reason, Opus on disputes, result | is the finding right?, notes |
| Drafts and debate | per node (EVD, QUE, CLM, CVT): winner and how it was decided (Sol and Sonnet agree, or Neon tie-break), text, characters, reading grade, lint, claim check and suggested fix, decision-model score, status, the three first drafts, Inkling's own draft and pick (benchmark only) | best text or your own, fidelity, style, notes |
| Quality signals (raw) | one row per paper, signal and rater: rating, verbatim quote, locator, quote found in the PDF; Opus, Sol and Neon count, Inkling is benchmark only | none |
| Quality signals (vote) | per paper and signal: votes, majority, agreement, Inkling's rating, quotes not found | correct rating, notes |
| Open-model shadow | Inkling's extraction scored against the PDF and Neon | how many of its findings are right, notes |

## 3. Quality Signals benchmark sheet (specified; raw and vote tabs exist per run, the cross-paper benchmark is to build)
| Tab | Content |
|---|---|
| Raw ratings | the raw tab above, stacked over all runs. Raters: Opus 5.5, Sol and Neon (counted); **Inkling 2 Small only** as the benchmark-only rater (Sonnet 5.5 takes no part) |
| Aggregate | the vote tab stacked over all runs |
| Benchmark | per model and for the majority: accuracy against JP's labels, Cohen's kappa, false-positive and false-negative rate, cost per correct rating, time; updated as soon as JP fills the label column |
| JP labels | JP's ground-truth rating per paper and signal, with a note |
| Costs | cost per model and per paper |

## 4. Rules for all review sheets
- Data comes from the run folder (`pipeline/runs/<run>/`), never typed by hand; the sheet is rebuilt, not edited, except in JP's columns.
- Abstracts and local file paths stay out of the public repository; sheets are private Google Sheets.
- Every row has a stable id (paper, node, finding, rater) so JP's labels can be merged into a rebuilt sheet.

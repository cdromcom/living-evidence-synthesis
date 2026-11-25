---
type: spec
title: Review sheets for runs and quality signals
status: partly built (run review sheet built; the drafts and quality-signal tabs are specified)
written: 2026-11-25
---

# Review sheets (JP, 2026-11-25)

Goal: a human can follow every step of a run, see each model's work, and add ground-truth labels later, so accuracy and cost per model can be scored. Sheets are Google Sheets made from workbooks the scripts build. Yellow-headed columns are the human's.

## 1. Run review sheet (built: `pipeline/scripts/run_to_gsheet.py RUN_ID`)
| Tab | Content | JP columns |
|---|---|---|
| ABOUT | the run, the steps in order, how to review, the flags | none |
| Papers | one row per paper: status, pages, findings per tier, flagged, disagreements, cost | none |
| Findings | one row per extracted finding: tier and why, supports, statement, PICOST slots, numbers with locators, confidence, flags, recheck result, Opus verdict | tier right?, correct tier, statement and numbers right?, missed finding, notes |
| Checks | one row per quoted span: found in the PDF text, pages, word boxes | quote correct?, notes |
| Rechecks | Neon numbers against Sol numbers and Opus's verdict | who is right?, notes |
| Calls and cost | every model call: step, model, effort, tokens, cost | none |

## 2. Drafts and debate (specified; to build with the debate stage)
One row per draft, critique, revision, vote and check, in order, per node (EVD, QUE, CLM, EP, CVT): node id, round, model, effort, text, character count, readability grade, lint result, critique points, vote and reason, check verdict per claim, cost. JP columns: which final text is best (or write a better one), fidelity (yes, partly, no), style, notes. Inkling's votes are marked "benchmark only".

## 3. Quality Signals benchmark sheet (specified; to build with Module Q)
| Tab | Content |
|---|---|
| Raw ratings | one row per paper, signal and rater: rating, verbatim quote, locator, quote found (script), quote supports rating (decision model), model, effort, tokens, cost. Raters: Opus 5.5, Sol, Neon (counted); Sonnet 5.5 and Inkling (benchmark only) |
| Aggregate | one row per paper and signal: votes per rating, majority, agreement (3 of 3, 2 of 3, none), quote checks, flag for JP |
| Benchmark | per model and for the majority: accuracy against JP's labels, Cohen's kappa, false-positive and false-negative rate, cost per correct rating, time; updated as soon as JP fills the label column |
| JP labels | JP's ground-truth rating per paper and signal, with a note |
| Costs | cost per model and per paper |

## 4. Rules for all review sheets
- Data comes from the run folder (`pipeline/runs/<run>/`), never typed by hand; the sheet is rebuilt, not edited, except in JP's columns.
- Abstracts and local file paths stay out of the public repository; sheets are private Google Sheets.
- Every row has a stable id (paper, node, finding, rater) so JP's labels can be merged into a rebuilt sheet.

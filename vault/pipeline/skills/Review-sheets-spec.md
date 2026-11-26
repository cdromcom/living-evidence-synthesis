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
| Drafts and debate | per node (EVD, QUE, CLM, CVT): winner and how it was decided (Sol and Sonnet agree, or Neon tie-break), text, characters, reading grade, lint, claim check and suggested fix, decision-model score, status, the three first drafts | best text or your own, fidelity, style, notes |
| Quality signals (raw) | one row per paper, signal and rater: rating, verbatim quote, locator, quote found in the PDF; Neon (High) and Opus rate; Sol adds a third rating only where they disagreed | none |
| Metrics | time, cost, accuracy according to the checkers, per stage and overall (a plain list, no labels) | none |
| Question groups | unified, nested questions proposed from the papers' own questions (`consolidate_questions.py`) | group right, better wording |
| Quality signals (vote) | per paper and signal: votes, majority, agreement, quotes not found | correct rating, notes |

## 3. Quality Signals benchmark sheet (specified; raw and vote tabs exist per run, the cross-paper benchmark is to build)
| Tab | Content |
|---|---|
| Raw ratings | the raw tab above, stacked over all runs. Raters: Neon (High) and Opus 5.5, with Sol only for disagreements |
| Aggregate | the vote tab stacked over all runs |
| Benchmark | per model and for the majority: accuracy against JP's labels, Cohen's kappa, false-positive and false-negative rate, cost per correct rating, time; updated as soon as JP fills the label column |
| JP labels | JP's ground-truth rating per paper and signal, with a note |
| Costs | cost per model and per paper |

## 4. Rules for all review sheets
- Data comes from the run folder (`pipeline/runs/<run>/`), never typed by hand; the sheet is rebuilt, not edited, except in JP's columns.
- Abstracts and local file paths stay out of the public repository; sheets are private Google Sheets.
- Every row has a stable id (paper, node, finding, rater) so JP's labels can be merged into a rebuilt sheet.


## Where the sheets live and how they look (JP, 2026-11-26)

**Drive folder** (private, owner only): `SysRev LLMApp (LIVES)`, with subfolders `01 Screening`, `02 Pipeline review sheets`, `03 AI raters and quality signals`, `04 Vault review` and `99 Archive (superseded)`.

**File names** follow one pattern: `LIVES - <Area> - <YYYY-MM-DD> - <what it is>`. Areas: Screening, Pipeline review (add the batch id), Quality signals, AI rater, Vault review, Archive (replaces the area for superseded sheets and says what superseded it).

**Look** (`pipeline/scripts/sheet_style.py`, used by every sheet builder; Butterick's Practical Typography for the text and Stephen Few's Show Me the Numbers, chapter 8, for the table):
1. Lato 10, never a default font; bold only for column headers; no italics, underlines or capitals for emphasis.
2. No gridlines. One dark rule under the header. Fills are limited to a faint grey zebra stripe, the yellow JP input columns and the light green screening rows.
3. Numbers and brief words or phrases (up to 22 characters) are centered. Longer text is left aligned and wraps with a small indent. Each header is aligned like its data.
4. Every column is sized to its data; wrapped text stops at a comfortable line length (about 45 to 75 characters).
5. One number format per column (same decimals, dollars with a sign).
6. ABOUT tabs: bold key column and one text column about 85 characters wide; steps are listed one per row.
A new builder calls `polish(ws, jp_from=..., image_cols=...)` after the rows are in; an existing Google Sheet can be styled in place with `sheets_requests`, which leaves labels alone.

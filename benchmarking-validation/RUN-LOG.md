# Run log

All times UTC. API keys were read from a local `.env` outside git. Counts are from `results/*.jsonl`.

| Run id | Date | Scope | Prompt state | Notes |
|---|---|---|---|---|
| `smoke` | 2026-11-24 (evening of 2026-11-23, US Eastern) | EVD 4-6, all tasks, 3 models | no paper text; relevancy without review questions; earlier quote rubric | 36 requests, 0 errors. Pilot only. |
| `lat` | 2026-11-24 | EVD 7-9, relevancy, fidelity and quote, 3 models, 1 request at a time | review questions added; quote rule of 2026-11-23 | Measured latency: Jev 0.15 s, Liquid 0.26 s, Perplexity 0.39 s per request. Pilot only. |
| `r1` | 2026-11-24 | EVD 1-77, all tasks, 3 models | fidelity prompt version 3 (gist rule plus worked examples from EVD 1-3), review questions, verbatim-quote rule, no-screenshot-means-Missing rule | 305 records per model (235 model calls and 70 rule-based table/figure rows), 0 errors. Judgment of record. |

Measured in `r1`: input tokens 186,595 (Perplexity), 193,546 (Liquid, reported cost $0.0081), 309,786 (Jev). Mean latency per
request 0.27 s, 0.23 s and 0.12 s. Sheets were filled from these results; every label in the three sheets matches
`results/<provider>.r1.jsonl` (checked programmatically, 0 mismatches).

| `r1fix` | 2026-11-24 | EVD 21 and 38, decision models | after the quote-parser fix | 24 requests, 0 errors. Overrides `r1` for those EVDs. |
| `opus r1` | 2026-11-24 | EVD 1-77, Claude Opus 5.5, six subagent batches + one rerun of EVD 21 and 38 | same inputs and rubrics, blind folder | 535,604 subagent tokens, 578 s of subagent time. See `prompts/OPUS_RATER_INSTRUCTIONS.md`. |

## Decisions that shaped the inputs (all by JP unless noted)

* 2026-11-23: models get only what is in the model-only sheets (quotes, captions, screenshots, review questions). No PDFs, paper text or web.
* 2026-11-23: fidelity rule = the gist of the headline EVD must be in the Description quote; matching specifics are a bonus.
* 2026-11-23: quotes must be verbatim and the screenshot must match the text above it; a wrong page number does not change Correct.
* 2026-11-23: if no table/figure screenshot is shown the answer is Missing (applied in code).
* 2026-11-23: review questions come from the QUE tab (JP's edited wording); pairing is paper-level (kept after comparing with the app's auto-derived links).
* 2026-11-23: Liquid d1-ultra replaced Google Gemini Decision 1.

## Pilot caveats

`smoke` and `lat` used earlier prompt versions and are kept only as an audit trail of how the setup changed. Do not combine them with `r1`.

## Run 2 (r2, 2026-11-24 UTC)
All four raters, all 77 EVDs, new input rules: every Description screenshot shown without slot labels, per-screenshot "connects to the quote" questions, paraphrased text under the table/figure sent in the table task. Fidelity and relevancy prompts unchanged. Decision models: 305 records each, 0 errors. Opus 5.5: six blind subagents on a folder with neutral screenshot names (results/opus_raw_r2/). Scored against JP's original ratings, which were made under the Run 1 slot rule, so table/figure scores are not comparable with Run 1. Metrics: results/metrics-r2.json.

## Run 2, table/figure rerun (r2t, 2026-11-24 UTC)
JP's rule restored for the table/figure task: if the evidence page has no screenshot in the table/figure slot, the answer is Missing (no model call); otherwise the models judge, seeing every screenshot. Relevancy, fidelity and quote answers in r2t are copied unchanged from r2. Decision models re-called for the 7 EVDs with a table/figure-slot screenshot (EVD 1 excluded from scoring); Opus's r2 judgements for those EVDs were reused (same inputs). Scored in results/metrics-r2t.json: all four raters 64/72 = 88.9%, below the always-Missing baseline of 90.3%; the rule decides 65 of 72 scored rows.

## Logs and error analysis for Run 2 (2026-11-24 UTC)
LOG tabs rebuilt with Run 2 and r2t records (r2 table/figure rows marked superseded) and Opus Run 2 batch tokens/time; ABOUT tabs describe Run 1, Run 2, r2t and LOG. Error analysis of all four raters and Run 1 vs Run 2 change: results/error-analysis-r2t.md (error_analysis_r2.py). Key points: table/figure answers in r2t equal Run 1 exactly (the rule decides 65 of 72 scored rows); the rule is wrong on EVD 9, 11, 21 (JP non-Missing, no table/figure-slot screenshot) and the four raters call EVD 16 and 47 Correct where JP says Missing; relevancy, fidelity and quote labels moved on 0-7 EVDs per rater between runs.

## JP's analysis decisions (2026-11-24)
- **Relevancy:** EVD 7, 17, 49, 72, 75, 76 dropped (JP's notes: not true EVDs). EVD 32 stays. n=68.
- **Fidelity:** EVD 4, 19, 26, 36, 38, 54, 56, 65 excluded: the quote shown is paraphrased table text or needs methods context to give rise to the headline EVD, a consequence of how JP guided earlier Claude Sonnet and Opus models to write headline EVDs, not the raters' fault. n=66. Chosen from rows all four raters got wrong, so outcome-selected; every-row figures are in results/metrics-*-all.json and Section E of the summary tabs.
- **Quote:** EVD 5, 6, 9, 18, 45, 51, 53, 66 excluded pending JP re-rating (screenshot wrong, cropped, or without the quote). n=66. Same selection caveat.
- **New quote definitions (not yet used in a run):** Correct = full quote shown, nothing extraneous; Partially Correct = right passage but incomplete or cropped; Incorrect = screenshot present but a different passage; Missing = no screenshot at all. run_raters.py and prompts/PROMPTS.md now carry this wording; r1 and r2 used the earlier wording (log_src/prompts_run1.md, prompts_run2.md).
- Exclusions live in inputs/exclusions.json; metrics.py applies them (add --all for none). results/metrics-r1.json and metrics-r2t.json are now after exclusions; results/summary-r1.csv, metrics-r1.csv and agreement.csv predate them and use every row. sheets/decision-models-summary-r1.xlsx and -r2t.xlsx are the tabs now in the main GSheet, with hover notes.

## Run 3 (r3, 2026-11-24 UTC): quote task re-run with the strict definitions
Only the quote task was re-run (all 77 EVDs, four raters) with the new definitions: Correct = full quote shown, nothing extraneous; Partially Correct = right passage but incomplete or cropped; Incorrect = a screenshot is present but a different passage; Missing = no screenshot at all. results/<provider>.r3q.jsonl are the quote-only records; results/<provider>.r3.jsonl add the r2t relevancy, fidelity and table/figure records unchanged so metrics.py scores them together. Opus: three blind subagents (EVD 1-26, 27-52, 53-77) on the Run 2 folder with the Run 3 PROMPTS.md (results/opus_raw_r3/).
Quote accuracy against JP's old labels (after exclusions, n=66; all rows n=74 in brackets): Perplexity 97.0% (86.5%), Liquid 93.9% (83.8%), Jev 83.3% (74.3%), Opus 86.4% (77.0%); baseline 81.8% (81.1%). Run 2 on the same rows: 95.5, 95.5, 93.9, 89.4.
On the 8 rows excluded pending re-rating, the four raters now agree: EVD 5, 6, 18 Incorrect (JP: Correct); 45 Incorrect (JP: Missing; a screenshot is present); 51 and 53 Partially Correct (JP: Correct, Incorrect); 9 Partially Correct from three of four; 66 Incorrect from three of four. Outside those rows, only EVD 22 has JP Correct against four Partially Correct. Jev moved 7 EVDs from Correct to Partially Correct between r2 and r3; the others moved 2-3. These are suggestions for JP's re-rating; no JP label was changed.

## Why Jev's quote score fell in Run 3 and Run 4 (2026-11-24)
Jev scored 93.9% on quote in Run 2 and 83.3% in Run 3 (n=66). Seven EVDs (12, 39, 43, 57, 58, 59, 72) moved from Correct to Partially Correct, each with P(Correct) between 0.41 and 0.48 against P(Partially Correct) between 0.51 and 0.58, so the Run 3 wording ("no extraneous content getting in the way") tipped coin-flip cases. For EVD 12 and 58 the screenshot shows the whole highlighted quote with ordinary surrounding page text, which is Correct; the models read that surrounding text as extraneous. Run 4 states that surrounding page text, headers and neighbouring content are not extraneous.

## Run 4 (r4, 2026-11-24 UTC): fidelity v4 and quote v4
Fidelity v4: a quote that states the finding in words is Met even when the numbers sit elsewhere; Partially Met only for one part of a multi-part claim or a noticeably different claim. Quote v4: Correct = every word visible and legible, highlighting not required, surrounding text not extraneous; Partially Correct = part cut off or words changed; Incorrect = a screenshot present but a different passage; Missing = no screenshot; plus the question "is every word of the quote visible". Relevancy and table/figure records are copied from r3. results/<provider>.r4q.jsonl hold the fidelity and quote records only. Opus: three blind subagents (results/opus_raw_r4/).
Caveat: this wording was written after JP's exclusions and after looking at Run 3 errors on the same 66 rows, so Run 4 is not a clean held-out test. Report Run 3 as the quote result under the strict definitions.
n=66 results (Run 3 -> Run 4): quote Perplexity 97.0 -> 92.4, Liquid 93.9 -> 92.4, Jev 83.3 -> 95.5, Opus 86.4 -> 86.4 (baseline 81.8). Fidelity Perplexity 81.8 -> 86.4, Liquid 87.9 -> 90.9, Jev 84.8 -> 86.4, Opus 92.4 -> 92.4 (baseline 93.9). The fidelity gain comes from calling Met more often (Liquid 64 and Opus 65 of 66, against JP's 62), and kappa for Liquid and Opus is about zero: they do not separate JP's four Partially Met rows from the rest.
Remaining quote disagreements with JP's Correct labels, shared by several raters: EVD 11, 22, 25, 35, 39, 40 (candidates for JP's re-rating together with the 8 excluded rows).

## Sheets (2026-11-24)
Run 3 and Run 4 tabs show "dropped from analysis (JP)" in the dropped cells for the task concerned; Run 1 and Run 2 tabs keep the original answers with hover notes. Summary tabs in the main GSheet: Decision Models Summary (Run 1), (Run 2), (Run 3), (Run 4); LOG tabs hold all runs.

## Run 5 (r5, 2026-11-24 UTC): repeat of the Run 4 prompts, all four tasks
Perplexity, Liquid and Jev re-ran relevancy, fidelity v4, quote v4 and table/figure (Missing by rule when the page has no table/figure-slot screenshot) with the same prompts as Run 4: 915 requests, 0 errors. Opus 5.5 was not re-run; results/opus.r5.jsonl are the r4 records carried over unchanged, so the four sheets line up.
Stability against Run 4 (labels changed, EVD 4-77 of 74; the Run 4 relevancy records were carried from Run 2, so that column compares Run 5 with Run 2): quote Perplexity 0, Liquid 2, Jev 6; fidelity 0, 2, 1; table/figure 0, 0, 0; relevancy 1, 1, 1.
n=66 accuracy, Run 5 (Run 4): quote Perplexity 92.4 (92.4), Liquid 92.4 (92.4), Jev 95.5 (95.5), Opus 86.4; fidelity 86.4 (86.4), 92.4 (90.9), 87.9 (86.4), Opus 92.4; relevancy n=68 Perplexity 97.1, Liquid 94.1, Jev 86.8, Opus 94.1; table/figure n=72 all 88.9. Same caveat as Run 4: the wording was written after seeing Run 3 errors on these rows.
The main GSheet's old Benchmark Summary tab (formulas over the LIVES-EVD-Benchmarking tab, blank for the decision models) was deleted at JP's request; it is recoverable from the sheet's version history. Summary tabs: Decision Models Summary (Run 1) to (Run 5).

## Run 6 prompt wording prepared (not yet run) and EVD 16 table/figure label (2026-11-24)
- JP: EVD 16 cannot be Missing, because its page has Fig 3 and Table 3 screenshots. Both are full journal pages (Fig 2 and Fig 3 with body text; Table 3 with body text), so under the new rule Partially Correct is the consistent label. inputs/exclusions.json now excludes EVD 16 from the table/figure analysis (n=71) until JP sets the label. Published sheet tabs and summaries up to Run 5 still count it.
- New wording in run_raters.py (quote version 6, table version 6; documented in prompts/PROMPTS.md and log_src/prompts_run6.md): extraneous content (another table or figure, a whole journal page, body-text paragraphs around a table, several unrelated paragraphs around a quote) lowers Correct to Partially Correct, for both quote and table/figure. For a quote, the few lines of its own paragraph around it are still fine. Missing = no screenshot of any table or figure (table) or no screenshot at all (quote); Incorrect = a screenshot present but the wrong table, figure or passage. Both tasks now carry text-only worked examples (clean crop = Correct; right item plus a full page, a second table or paragraphs = Partially Correct; cut off = Partially Correct; wrong item = Incorrect; none = Missing).
- The examples describe patterns from JP's table/figure notes (full page around the table, extra figures, cropped rows) without naming EVDs; they are written after seeing the Run 5 errors, so a Run 6 score is not a clean held-out test.
- Run: python3 run_raters.py run --run-id r6 --tasks quote,table --quote-version 6 --table-version 6 --table-slot-rule (Opus needs its blind folder refreshed with this PROMPTS.md).

## Table/figure without the slot rule: Run 6 (draft, superseded) and Run 7 (2026-11-24 UTC)
JP: for EVD 9, 11 and 21 the Missing-by-rule is wrong; teach the models that a trimmed table or figure is Partially Correct. Both runs drop the rule (models see every screenshot; Missing by rule only when the page has no screenshot at all) and re-run quote and table/figure for all four raters; relevancy and fidelity records are copied from r5.
- **r6** (log_src/prompts_run6.md): trimmed = Partially Correct, extraneous content lowers Correct to Partially Correct, worked examples. Result: EVD 8, 9, 11, 21, 29, 45 now Partially Correct as JP labelled them, but the models answered NA on about 34 rows where JP says Missing, so table/figure accuracy was 51-55% (n=71). JP's convention is that Missing is the default whenever no table or figure is shown (even when the numbers are all in the quote and the caption is empty), and NA only when the paper has no relevant table or figure (EVD 43, 48), which a page cannot show. Quote: Jev fell to 80.3% because the quote wording counted a table in the same screenshot as extraneous.
- **r7** (log_src/prompts_run7.md): Missing = no table or figure in any screenshot (the default); NA reserved for papers with no relevant table or figure; a table sharing the quote's screenshot does not count against the quote; extraneous content still lowers Correct to Partially Correct. Opus: three blind subagents (results/opus_raw_r7/).
- **r7 results (n=66 quote, n=71 table/figure after JP's exclusions):** quote Perplexity 97.0%, Liquid 97.0%, Jev 86.4%, Opus 87.9% (baseline 81.8%); table/figure Perplexity 97.2%, Liquid 97.2%, Jev 95.8%, Opus 97.2% (baseline 90.1%).
- **Remaining table/figure disagreements:** EVD 31 (JP Correct; all four say Partially Correct; JP's own note says the full page should be cropped, so the strict rule gives Partially Correct) and EVD 47 (JP Missing; all four say Partially Correct because Table 2 is shown on a full page; JP's note says the right table, Table 1, is missing). Jev also calls EVD 9 Incorrect. EVD 16 stays excluded until JP sets its label; all four raters say Partially Correct.
- **Remaining quote disagreements:** Perplexity EVD 7, 22; Liquid 22, 25; Jev 4, 7, 16, 22, 29, 35, 40, 42, 74; Opus 7, 11, 16, 22, 25, 35, 39, 40. EVD 22 is wrong in all four.
- Caveats: wording written after seeing Run 5 and Run 6 errors on the same rows, so these are tuned, not held-out; NA is now effectively unused for table/figure.
- The Run 6 and Run 7 results are in the repository but have not been published to the GSheets (tabs, LOG, summary).

## Run 7 published as "Run 6" in the GSheets (2026-11-24)
GSheets numbering: tabs Run 1 to Run 6 are run ids r1 (+r1fix), r2t, r3, r4, r5 and **r7**; the draft r6 is kept in LOG only, flagged superseded. The published Run 6 covers all four judgments. Perplexity, Liquid and Jev re-ran Selection Relevancy and Fidelity v4 (run id r7rf, merged into r7) as well as the new quote v7 and table/figure v7; Opus's relevancy and fidelity are carried from r5, and its quote and table/figure are the three blind subagents of r7.
n=68 relevancy, 66 fidelity, 66 quote, 71 table/figure (after JP's exclusions), Run 6: relevancy Perplexity 95.6, Liquid 95.6, Jev 89.7, Opus 94.1 (baseline 92.6); fidelity 86.4, 93.9, 87.9, 92.4 (baseline 93.9); quote 97.0, 97.0, 86.4, 87.9 (baseline 81.8); table/figure 97.2, 97.2, 95.8, 97.2 (baseline 90.1).
Label changes against Run 5 for the re-run judgments: relevancy 1, 3, 2 labels (Perplexity, Liquid, Jev); fidelity 0, 2, 2. EVD 16's table/figure cell is dropped (note added); Decision Models Summary (Run 6) is in the main GSheet.

Note (2026-11-24): the vault layout changed on 2026-11-24. Node folders moved under `vault/sysrev/` (for example `vault/sysrev/evidence/`, `vault/sysrev/source/pdfs/`) and tooling folders under `vault/pipeline/`. Only the path constants in `build_packets.py` and `make_questions.py` were updated; no result, packet or prompt changed.

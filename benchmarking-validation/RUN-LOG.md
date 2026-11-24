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

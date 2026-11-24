# Benchmarking and validation of LIVES EVD judgments with decision models

This folder records an audit of the 77 evidence nodes (EVDs) in LIVES and a benchmark of three **decision models**
(models that return calibrated probabilities instead of text) and Claude Opus 5.5 against a human expert (JP). Everything
needed to check or repeat the work is here: the exact inputs each model saw, the prompts, the raw model outputs, the
analysis scripts and the GSheets as CSV files.

**Status:** run `r1` (2026-11-24 UTC) is complete for Perplexity Decider 1.3, Liquid d1-ultra, Jev and Claude Opus 5.5.
More runs to check stability are planned. EVD 21 and 38 were re-judged after an input fix (see Known issues).

## What was judged

For each EVD the raters answered four questions, using only what is in the model-only GSheets (no paper PDFs, paper text or
web access):

| Task | Question | Labels |
|---|---|---|
| Relevancy | Is the EVD relevant to its review question(s) and worth learning? | Relevant / Irrelevant (P >= 0.5) |
| Fidelity | Is the gist of the headline EVD in the Description quote? (JP's gist rule, 2026-11-23) | Met / Partially Met / Unmet |
| Grounding: Quote | Does the screenshot show the quoted text word for word? (a wrong page number does not matter) | Correct / Partially Correct / Incorrect / Missing / NA |
| Grounding: Table/Fig | Does the page show the right table or figure? If no screenshot is shown the answer is **Missing** and no model is called (JP's rule) | Correct / Partially Correct / Incorrect / Missing / NA |

Held-out comparison: EVD 4-77 (74 EVDs; table/figure n=72 because two JP NA rows are excluded). EVD 1-3 are the worked examples
in the fidelity prompt and are excluded. EVDs 45 and 47 each have extra continuation rows in the main sheet; they are NA there
and not sent to the raters.

## Raters (all through hosted APIs, except Opus)

| Rater | Model id | Access | Notes |
|---|---|---|---|
| Perplexity Decider 1.3 | `pplx-decider-v1.3` | `api.perplexity.ai/v1/decisions` | 27B; text and images |
| Liquid d1-ultra | `d1-ultra` | `api.liquid.ai/decisions/v1/systemone` | listed as deprecated in favour of `d1.2-ultra`; context about 32K tokens (unconfirmed) |
| Jev | `jev-1.14.0` | `api.typesafe.ai/v1/systemone` | images through the preview header `TypeSafe-Danger-Zone-Images` |
| Claude Opus 5.5 | `claude-opus-5-5` | Claude Code subagents (not the Messages API) | blind rerun; see `prompts/OPUS_RATER_INSTRUCTIONS.md` |

No temperature or seed is exposed by the three decision models. Calls were made on 2026-11-23 (pilots) and 2026-11-24 UTC (`r1`).
Request formats were built from each vendor's documentation as read on 2026-11-23; see `RUN-LOG.md`.

## Blinding

The model-only sheets and packets contain only vault content: the EVD statement, the Description quote, the table/figure
caption, the screenshots and the review question(s). No rating, note, draft or flag from JP or Claude is in any rater's input.
`reference/reference.csv` (JP's and Claude's earlier ratings) is used **only** by `agreement.py`, `error_analysis.py` and
`metrics.py`, after the raters have answered. Scripts that call the APIs never read it.

Review questions (`questions_by_evd.json`) come from the QUE tab of the human-only sheet (`inputs/que_tab.csv`, JP's edited
wording) and the vault's paper-to-question links (`DGRAPH-TABLE.md`). Pairing is paper-level: an EVD gets the question(s) its
paper asks. The app's nested question-to-claim-to-EVD lists were not used because they are auto-derived by keyword overlap and
labelled "verify".

## Results of run r1 (agreement with JP on EVD 4-77; Cohen's kappa in brackets)

| Task | Baseline | Perplexity | Liquid | Jev | Opus 5.5 | Avg P+L+Opus | Avg P+L+Jev | Majority P+L+Jev |
|---|---|---|---|---|---|---|---|---|
| Relevancy | 87.8% | 87.8% (0.40) | 89.2% (0.49) | 78.4% (0.27) | 86.5% (0.37) | 90.5% (0.54) | 89.2% (0.49) | 87.8% (0.46) |
| Fidelity | 91.9% | 73.0% (0.16) | 79.7% (0.17) | 77.0% (0.15) | 82.4% (0.00) | 79.7% (0.17) | 77.0% (0.14) | 77.0% (0.14) |
| Grounding: Quote | 81.1% | 86.5% (0.67) | 79.7% (0.54) | 82.4% (0.59) | 78.4% (0.53) | 85.1% (0.64) | 87.8% (0.68) | 82.4% (0.59) |
| Grounding: Table/Fig (n=72) | 90.3% | 88.9% (0.35) | 88.9% (0.35) | 88.9% (0.35) | 88.9% (0.35) | 88.9% (0.35) | 88.9% (0.35) | 88.9% (0.35) |

"Baseline" = always guessing JP's most common label. Averages combine each rater's probabilities before choosing the label.
Raw ratios, accuracy, kappa and macro, micro and weighted F1 for every rater and ensemble are in `results/metrics-r1.csv`
(and in the `Decision Models Summary` tab of the main GSheet, with colour-coded confusion matrices). micro-F1 equals accuracy
for single-label problems. Examples:

| Task | Rater | Raw ratio | Accuracy | Kappa | F1 macro | F1 micro | F1 overall (weighted) |
|---|---|---|---|---|---|---|---|
| Relevancy | Claude Opus 5.5 | 64/74 | 86.5% | 0.37 | 0.68 | 0.86 | 0.86 |
| Relevancy | Average of Perplexity + Liquid + Opus | 67/74 | 90.5% | 0.54 | 0.77 | 0.91 | 0.90 |
| Fidelity | Claude Opus 5.5 | 61/74 | 82.4% | 0.00 | 0.30 | 0.82 | 0.84 |
| Fidelity | Average of Perplexity + Liquid + Opus | 59/74 | 79.7% | 0.17 | 0.38 | 0.80 | 0.84 |
| Grounding: Quote | Claude Opus 5.5 | 58/74 | 78.4% | 0.53 | 0.66 | 0.78 | 0.84 |
| Grounding: Quote | Average of Perplexity + Liquid + Opus | 63/74 | 85.1% | 0.64 | 0.74 | 0.85 | 0.89 |
| Grounding: Table/Fig (n=72) | Claude Opus 5.5 | 64/72 | 88.9% | 0.35 | 0.42 | 0.89 | 0.87 |
| Grounding: Table/Fig (n=72) | Average of Perplexity + Liquid + Opus | 64/72 | 88.9% | 0.35 | 0.42 | 0.89 | 0.87 |

**Does averaging help?** Only a little, and only on relevancy. Averaging Perplexity + Liquid + Opus gives the best relevancy score
(90.5%, 2.7 points above the always-Relevant baseline), improves quote grounding over the three-model
majority vote, and does not beat the best single rater on fidelity or quote. Fidelity stays well below the always-Met baseline
(91.9%) for every rater. The raters' errors are highly correlated (for example Opus agrees with Liquid on relevancy for 97% of EVDs), so
voting and averaging add little. JP's ratings are the only human reference, so there is no human-human ceiling; a test-retest on a
sample of JP's own ratings would give one.

## Error analysis (`results/error-analysis-r1.md`, for the three decision models)

* **Fidelity is the weak task.** The models say Partially Met or Unmet 14-21 times against JP's 6 of 74. Twelve EVDs are wrong
  in all three models. Most are rows where JP rated Met because the numbers or the gist sit in the unquoted table summary on the
  page, while the prompt (JP's gist rule) lets the model see the quote only.
* **Quote errors are partly label inconsistency.** All three models call EVD 5, 6, 18 and 66 Incorrect with high confidence; the
  screenshot under the quote shows a different passage. JP rated these Correct before the verbatim-quote rule of 2026-11-23.
* **Table/figure errors are identical for all raters** because 70 of 77 rows come from the Missing rule. Among the errors are EVD 9, 11
  and 21, where a table screenshot sits in the quote slot on the vault page and so counts as "no table screenshot".
* **Relevancy.** Seven EVDs (7, 17, 32, 49, 72, 75, 76) are wrong in all three models. Jev marks 17 EVDs Irrelevant against JP's 9.

## Reproduce and check

```
pip install -r requirements.txt
cp .env.example .env            # fill in the three API keys; keep .env out of git
# 1. inputs (needs the repository's vault/ folder, or set LIVES_VAULT)
python3 make_questions.py       # -> questions_by_evd.json
python3 build_packets.py        # -> packets/ (rebuilding gave byte-identical files)
# 2. decision-model judgments (about 235 API calls per model; 70 table/figure rows per model are rule-based)
python3 run_raters.py run --run-id r1          # fidelity prompt version 3 is the default
python3 run_raters.py export --run-id r1       # -> results/summary-r1.csv
# 3. Opus 5.5: see prompts/OPUS_RATER_INSTRUCTIONS.md, then
python3 opus_to_results.py results/opus_raw r1
# 4. analysis (uses reference/reference.csv, never read during steps 2-3)
python3 agreement.py                           # -> results/agreement.csv
python3 metrics.py r1                          # -> results/metrics-r1.json (+ .csv via the README table)
python3 error_analysis.py r1                   # -> results/error-analysis-r1.md
python3 make_summary_tab.py r1                 # -> sheets/decision-models-summary-r1.xlsx (the GSheet tab)
```

* `MANIFEST.sha256` lists a checksum for every file here: `shasum -a 256 -c MANIFEST.sha256`.
* `prompts/PROMPTS.md` holds every rubric and question; `prompts/rendered/` shows the exact request text for sample EVDs.
* Each model-only GSheet has tabs **Run 1** (r1, frozen), **Run 2** (same layout, answers cleared, for the second run), **ABOUT** and **LOG** (prompt text per run, example requests, every output record; built by `make_log_tab.py` from `log_src/` and `results/`). Fidelity (model) for EVD 1-3 reads "test data - ignored".
* `sheets/*-run1.csv` are exports of the four Run 1 tabs; `sheets/log-*.xlsx` are the LOG tabs. Google Sheets drops image cells on export, so `merge_image_urls.py`
  puts the screenshot URLs back. `sheets/decision-models-summary-r1.xlsx` is the summary tab.
* Records in `results/*.r1fix.jsonl` override the same EVD and task in `results/*.r1.jsonl` (see Known issues); the analysis scripts apply that rule.
* Re-running the models will not give identical numbers: no sampling controls are exposed and vendors may update a model behind an alias.

## Cost and time (run r1, measured)

Input tokens 186,595 (Perplexity), 193,546 (Liquid) and 309,786 (Jev), about $0.025 in total; 28 to 63 seconds of request time per
model. Claude Opus 5.5 ran as seven subagent batches using about 536K tokens in 578 seconds of subagent time; at list price
($4 input / $20 output per million tokens) that is roughly $2 to $3, an estimate because the subagent token count does not
split input from output. Per-run numbers are in `results/metrics-r1.json` and in the summary tab.

## Known issues and limitations

* **Quote parser fix.** The first run lost the quotation for EVD 38 (a note preceded it on the page, so the line was not recognised) and
  the second quotation for EVD 21. Every rater therefore saw an incomplete quote for those two EVDs. `build_packets.py` is fixed; the
  two EVDs were re-judged in `r1fix` (decision models) and by a fresh Opus rater, and the original answers are kept in `r1`
  and `results/opus_raw_superseded/`. The sheets and all metrics use the corrected answers.
* Fidelity and quote rubrics encode JP's rules as of 2026-11-23; some of JP's earlier ratings predate them. Table/figure Missing vs NA
  cannot be decided without the paper, so Missing is the default.
* Liquid's `d1-ultra` is deprecated; Liquid's and Perplexity's data-retention terms and rate limits were not confirmed.
* Only 7 EVDs (9 images) have a table/figure screenshot on the evidence page, so that column is mostly rule-based.
* Raters see the vault's resized copy of each screenshot (at most 1400 px); Jev's image input is a preview feature.
* Sample size is small (74 held-out EVDs), so differences of a few points are within noise.
* Screenshots of paper excerpts are included for checkability; the same images are served by the live LIVES site.

# Benchmarking and validation of LIVES EVD judgments with decision models

This folder records an audit of the 77 evidence nodes (EVDs) in LIVES and a benchmark of three **decision models**
(models that return calibrated probabilities instead of text) and Claude Opus 5.5 against a human expert (JP). Everything
needed to check or repeat the work is here: the exact inputs each model saw, the prompts for every run, the raw model
outputs, the analysis scripts and the GSheets as CSV and xlsx files.

**Status (2026-11-24 UTC):** six runs are complete. Run 6 (run id `r7`) is the one to report. It re-judges all four
questions for Perplexity Decider 1.3, Liquid d1-ultra and Jev; Claude Opus 5.5 re-judged the two grounding questions and its
relevancy and fidelity answers are carried over from Run 5. The wording of the fidelity and grounding rubrics was refined
across runs **after looking at earlier errors on the same rows**, so later scores are tuned, not held-out (see Limitations).

## What was judged

For each EVD the raters answered four questions, using only what is in the model-only GSheets (no paper PDFs, paper text or
web access):

| Task | Question | Labels |
|---|---|---|
| Selection relevancy | Is the EVD relevant to its review question(s) and worth learning? | Relevant / Irrelevant (P >= 0.5) |
| Fidelity | Is the gist of the headline EVD in the Description quote? (JP's gist rule; numbers are a bonus; Run 4 onward: a quote that states the finding in words is Met even if the numbers sit elsewhere) | Met / Partially Met / Unmet |
| Grounding: Quote | Do the screenshots show the whole quote? | Correct = every word visible and a clean capture (at most a few lines of its own paragraph around it; a table in the same screenshot is judged separately); Partially Correct = right passage but cut off, changed words, or buried in a whole page or unrelated paragraphs; Incorrect = a screenshot is present but a different passage; Missing = no screenshot; NA. A wrong page number does not matter. |
| Grounding: Table/Fig | Does the page show the right table or figure? | Correct = whole table or figure with its caption and nothing else substantial; Partially Correct = right table or figure but trimmed, or with extraneous content (body text, another table or figure, a whole journal page), or only one of several; Incorrect = a table or figure is shown but the wrong one; Missing = no table or figure in any screenshot (the default; text-only screenshots do not count); NA is reserved for papers with no relevant table or figure, which a page cannot show. |

Worked examples (text descriptions) are part of the Run 6 grounding prompts and the three fidelity examples (EVD 1-3) are part of
the Run 3 to Run 6 fidelity prompts, so EVD 1-3 are excluded from scoring.

### Which rows are scored

Held-out comparison is EVD 4-77. On 2026-11-24 JP decided to drop rows from the analyses (`inputs/exclusions.json`, applied by
`metrics.py`; `--all` gives every row):

| Task | Dropped EVDs | n | Why |
|---|---|---|---|
| Relevancy | 7, 17, 49, 72, 75, 76 | 68 | JP's notes say they are not true EVDs (EVD 32 stays) |
| Fidelity | 4, 19, 26, 36, 38, 54, 56, 65 | 66 | The quote shown is paraphrased table text or needs methods context to give rise to the headline EVD: an authoring issue in how earlier Claude models were guided to write headline EVDs, not the raters' fault |
| Quote | 5, 6, 9, 18, 45, 51, 53, 66 | 66 | JP's labels predate the strict definition of Correct (wrong passage, cropped, or no quote in the screenshot); pending JP's re-rating |
| Table/Fig | 16 (and two JP NA rows) | 71 | JP: EVD 16 has Fig 3 and Table 3 screenshots, so its recorded label (Missing) is wrong; label pending |

The fidelity and quote sets were chosen from rows all four raters got wrong, so those exclusions are outcome-selected; every-row
figures are in `results/metrics-*-all.json` and in section E of each summary tab.

## Getting this folder on its own

This folder is a research record, not part of the website. It is in the repository (branch `main`) and is left out of the Vercel deployment (`.vercelignore` at the repository root and `benchmarking-validation/vercel.json`).

- **Only this folder, with git** (about 30 MB):
  ```
  git clone --depth 1 --filter=blob:none --sparse https://github.com/cdromcom/living-evidence-synthesis.git
  cd living-evidence-synthesis
  git sparse-checkout set benchmarking-validation
  ```
- **Only this folder, without git history:** `npx degit cdromcom/living-evidence-synthesis/benchmarking-validation`
- **Whole repository as a zip:** on GitHub, Code, Download ZIP.
- **Check nothing changed:** from inside this folder run `shasum -a 256 -c MANIFEST.sha256` (on 2026-11-25 all 777 listed files passed).

## Raters (all through hosted APIs, except Opus)

| Rater | Model id | Access | Notes |
|---|---|---|---|
| Perplexity Decider 1.3 | `pplx-decider-v1.3` | `api.perplexity.ai/v1/decisions` | text and images |
| Liquid d1-ultra | `d1-ultra` | `api.liquid.ai/decisions/v1/systemone` | listed as deprecated in favour of `d1.2-ultra`; context about 32K tokens (unconfirmed) |
| Jev | `jev-1.14.0` | `api.typesafe.ai/v1/systemone` | images through the preview header `TypeSafe-Danger-Zone-Images` |
| Claude Opus 5.5 | `claude-opus-5-5` | Claude Code subagents (not the Messages API) | blind subagents on a folder of packets with neutral screenshot names; see `prompts/OPUS_RATER_INSTRUCTIONS.md` |

No temperature or seed is exposed by the three decision models. All calls were made on 2026-11-23 (pilots) and 2026-11-24 UTC.
Request formats were built from each vendor's documentation as read on 2026-11-23; see `RUN-LOG.md`.

## Blinding

The model-only sheets and packets contain only vault content: the EVD statement, the Description quote, the table/figure
caption and the paraphrased text under it, the screenshots, and the review question(s). No rating, note, draft or flag from JP
or Claude is in any rater's input. `reference/reference.csv` (JP's and Claude's earlier ratings) is used **only** by
`agreement.py`, `error_analysis*.py` and `metrics.py`, after the raters have answered. Scripts that call the APIs never read it.
Review questions come from the QUE tab of the human-only sheet (`inputs/que_tab.csv`) and the vault's paper-to-question links.

## Runs

GSheet tabs Run 1 to Run 6 correspond to these run ids (`results/<provider>.<run id>.jsonl`; the full prompt text of each run is
in `log_src/prompts_run*.md` and in each sheet's LOG tab):

| GSheet tab | Run id | What changed |
|---|---|---|
| Run 1 | `r1` (+`r1fix` for EVD 21, 38) | First judgments. Quote and table/figure judged from the slot the vault page used; no table-slot screenshot = Missing by rule. |
| Run 2 | `r2t` | Every Description screenshot shown without slot labels; paraphrased text under the table/figure sent; Missing by rule when the table slot is empty (`r2` is the first pass without the rule, superseded). |
| Run 3 | `r3` | Quote task only, strict definitions (full quote, nothing extraneous). |
| Run 4 | `r4` | Fidelity v4 and quote v4 wording (surrounding page text is not extraneous). |
| Run 5 | `r5` | Repeat of Run 4 prompts for the decision models (stability check); Opus carried from Run 4. |
| Run 6 | `r7` | Quote v7 and table/figure v7 wording with worked examples; no Missing-by-rule; Missing is the default; trimmed = Partially Correct. Relevancy and fidelity re-run for the decision models (`r7rf`). Draft `r6` is superseded and kept in the LOG only. |

## Results

Accuracy against JP after the exclusions above, by run (Cohen's kappa for Run 6 in the next table). Baseline = always guessing
JP's most common label. n differs by task: relevancy 68, fidelity 66, quote 66, table/figure 72 (71 from Run 5).

| Task | Rater | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Run 6 |
|---|---|---|---|---|---|---|---|
| Relevancy | Perplexity | 95.6% | 95.6% | 95.6% | 95.6% | 97.1% | 95.6% |
| | Liquid | 97.1% | 95.6% | 95.6% | 95.6% | 94.1% | 95.6% |
| | Jev | 85.3% | 85.3% | 85.3% | 85.3% | 86.8% | 89.7% |
| | Opus 5.5 | 94.1% | 94.1% | 94.1% | 94.1% | 94.1% | 94.1% |
| Fidelity | Perplexity | 81.8% | 81.8% | 81.8% | 86.4% | 86.4% | 86.4% |
| | Liquid | 89.4% | 87.9% | 87.9% | 90.9% | 92.4% | 93.9% |
| | Jev | 86.4% | 84.8% | 84.8% | 86.4% | 87.9% | 87.9% |
| | Opus 5.5 | 92.4% | 92.4% | 92.4% | 92.4% | 92.4% | 92.4% |
| Quote | Perplexity | 95.5% | 95.5% | 97.0% | 92.4% | 92.4% | 97.0% |
| | Liquid | 87.9% | 95.5% | 93.9% | 92.4% | 92.4% | 97.0% |
| | Jev | 90.9% | 93.9% | 83.3% | 95.5% | 95.5% | 86.4% |
| | Opus 5.5 | 86.4% | 89.4% | 86.4% | 86.4% | 86.4% | 87.9% |
| Table/figure | Perplexity | 88.9% | 88.9% | 88.9% | 88.9% | 90.1% | 97.2% |
| | Liquid | 88.9% | 88.9% | 88.9% | 88.9% | 90.1% | 97.2% |
| | Jev | 88.9% | 88.9% | 88.9% | 88.9% | 90.1% | 95.8% |
| | Opus 5.5 | 88.9% | 88.9% | 88.9% | 88.9% | 90.1% | 97.2% |

Opus's Run 2 to Run 6 relevancy and fidelity entries are carried over, not re-judged (relevancy from Run 2, fidelity from Run 4).
Table/figure accuracy in Runs 1 to 5 comes from the Missing-by-rule, so every rater scores alike there.

**Run 6 in detail** (every-row accuracy in brackets):

| Task | n | Baseline | Perplexity | Liquid | Jev | Opus 5.5 | Avg P+L+Opus |
|---|---|---|---|---|---|---|---|
| Relevancy | 68 | 92.6% (87.8%) | 95.6% (87.8%), kappa 0.70 | 95.6% (87.8%), 0.75 | 89.7% (82.4%), 0.54 | 94.1% (86.5%), 0.64 | 97.1% (89.2%), 0.78 |
| Fidelity | 66 | 93.9% (91.9%) | 86.4% (77.0%), 0.11 | 93.9% (85.1%), 0.31 | 87.9% (78.4%), 0.28 | 92.4% (83.8%), -0.02 | 93.9% (83.8%), 0.31 |
| Quote | 66 | 81.8% (81.1%) | 97.0% (86.5%), 0.91 | 97.0% (86.5%), 0.91 | 86.4% (77.0%), 0.66 | 87.9% (78.4%), 0.70 | 95.5% (85.1%), 0.87 |
| Table/figure | 71 | 90.1% (90.3%) | 97.2% (95.8%), 0.85 | 97.2% (95.8%), 0.85 | 95.8% (94.4%), 0.78 | 97.2% (95.8%), 0.85 | 97.2% (95.8%), 0.85 |

Raw ratios, F1 (macro, micro, weighted) and confusion matrices for every rater and ensemble are in `results/metrics-*.json` and in
the `Decision Models Summary (Run N)` tabs of the main GSheet. Micro-F1 equals accuracy for single-label problems.

* **Fidelity stays the weak task.** Only Liquid reaches the always-Met baseline, with a low kappa (0.31); Opus reaches 92.4% by
  saying Met on 65 of 66 rows (kappa about zero). No rater separates JP's four Partially Met rows reliably.
* **Quote and table/figure** now clear the baseline for Perplexity, Liquid and Opus. Jev's quote score swings with the wording:
  seven EVDs sat at P(Correct) 0.41-0.48 against P(Partially Correct) 0.51-0.58 under the Run 3 wording and tipped to Partially Correct.
* **Averaging helps little.** Errors are highly correlated across raters, so the Perplexity + Liquid + Opus average is within a
  point or two of the best single rater on most tasks (best gain: relevancy).
* **Stability** (Run 4 against Run 5, same prompts): Perplexity changed 0 labels on quote and fidelity, Liquid 2 and 2, Jev 6 and 1.
* Remaining disagreements with JP: quote EVD 22 (wrong in all four raters), EVD 7, 11, 25, 35, 39, 40; table/figure EVD 31
  (JP Correct, raters Partially Correct; JP's own note asks for a crop) and EVD 47 (JP Missing, raters Partially Correct).

Error analyses: `results/error-analysis-r1.md` (all rows, Run 1, three decision models) and `results/error-analysis-r2t.md`
(Run 2 after exclusions, four raters, with change from Run 1). The later runs' error lists are summarised in `RUN-LOG.md`.

## Reproduce and check

```
pip install -r requirements.txt
cp .env.example .env            # fill in the three API keys; keep .env out of git
# 1. inputs (needs the repository's vault/ folder, or set LIVES_VAULT; paths use the vault/sysrev/ layout of 2026-11-24)
python3 make_questions.py       # -> questions_by_evd.json
python3 build_packets.py        # -> packets/
# 2. decision-model judgments, Run 6 (run id r7). Relevancy and fidelity, then the groundings:
python3 run_raters.py run --run-id r7rf --tasks relevancy,fidelity --fidelity-version 4
python3 run_raters.py run --run-id r7q --tasks quote,table --quote-version 7 --table-version 7
#    (the repository's r7 files merge these two outputs; Run 1 used the defaults: --run-id r1, fidelity version 3, quote version 3, table version 5)
# 3. Opus 5.5: see prompts/OPUS_RATER_INSTRUCTIONS.md and the blind-folder method in RUN-LOG.md, then
python3 opus_to_results.py <folder with EVD-NN.json> r1
# 4. analysis (uses reference/reference.csv, never read during steps 2-3)
python3 metrics.py r7                          # after exclusions -> results/metrics-r7.json ; add --all for every row
python3 error_analysis_r2.py                   # -> results/error-analysis-r2t.md
python3 make_summary_tab.py r7                 # -> sheets/decision-models-summary-r7.xlsx (the GSheet tab)
python3 make_log_tab.py perplexity             # -> sheets/log-perplexity.xlsx (likewise liquid, jev, opus)
python3 make_run_fill.py perplexity r7         # -> sheets/fill-perplexity-r7.xlsx (answer columns of a Run tab)
```

* `MANIFEST.sha256` lists a checksum for every file here: `shasum -a 256 -c MANIFEST.sha256`.
* `prompts/PROMPTS.md` holds the current rubrics; `log_src/prompts_run1.md` to `prompts_run7.md` hold each run's prompt text; `prompts/rendered/` shows request text for sample EVDs.
* Each model-only GSheet has tabs **Run 1** to **Run 6**, **ABOUT** and **LOG**. In the Run 3 to Run 6 tabs the cells JP dropped read "dropped from analysis (JP)" for that task; Run 1 and Run 2 keep the original answers with hover notes. Fidelity (model) for EVD 1-3 reads "test data - ignored".
* `sheets/*-run1.csv` are exports of the four Run 1 tabs; `sheets/log-*.xlsx` are the LOG tabs; `sheets/decision-models-summary-r*.xlsx` are the summary tabs. Google Sheets drops image cells on export, so `merge_image_urls.py` puts the screenshot URLs back.
* Records in `results/*.r1fix.jsonl` override the same EVD and task in `results/*.r1.jsonl`; the analysis scripts apply that rule. `results/<provider>.r3`, `r4`, `r5`, `r6`, `r7` are full files (the tasks not re-run are copied from the previous run); `*.r3q`, `*.r4q`, `*.r6q`, `*.r7q` and `*.r7rf` hold only the newly run records.
* Re-running the models will not give identical numbers: no sampling controls are exposed and vendors may update a model behind an alias.
* `results/summary-r1.csv`, `results/metrics-r1.csv` and `results/agreement.csv` predate the exclusions and use every row.

## Cost and time

Run r1 (measured): input tokens 186,595 (Perplexity), 193,546 (Liquid) and 309,786 (Jev), about $0.025 in total; 28 to 63 seconds
of request time per model. Claude Opus 5.5 ran as seven subagent batches using about 536K tokens in 578 seconds of subagent time;
at list price ($4 input / $20 output per million tokens) that is roughly $2 to $3, an estimate because the subagent token count
does not split input from output. Later runs cost about the same per judgment; per-run usage is in `results/metrics-*.json`
and in section D of each summary tab.

## Known issues and limitations

* **Tuned wording.** The fidelity v4, quote v4/v7 and table/figure v7 wording and examples were written after seeing earlier errors
  on the same rows. The prompts cite no EVD numbers, but Runs 4 to 6 are not clean held-out tests.
* **Outcome-selected exclusions.** JP's fidelity and quote exclusions were chosen from rows all four raters got wrong; the
  every-row numbers are reported next to the scored ones. Other rows may share the same authoring problem.
* **Reference labels in flux.** Some of JP's labels predate the strict definitions (quote EVD 5, 6, 9, 18, 45, 51, 53, 66; EVD 22 and
  31) or are known to be wrong (table/figure EVD 16). Scores will change when JP re-rates them. No label was edited here.
* **Quote parser fix.** The first run lost the quotation for EVD 38 and the second quotation for EVD 21. `build_packets.py` is fixed;
  the two EVDs were re-judged in `r1fix` and the originals kept in `r1` and `results/opus_raw_superseded/`.
* Table/figure NA versus Missing cannot be decided without the paper, so Missing is the default and NA is effectively unused.
* Opus relevancy and fidelity were not re-run after Run 2 and Run 4; its grounding answers are from three blind subagents per run.
* Liquid's `d1-ultra` is deprecated; Liquid's and Perplexity's data-retention terms and rate limits were not confirmed.
* Raters see the vault's resized copy of each screenshot (at most 1400 px); Jev's image input is a preview feature.
* The sample is small (74 held-out EVDs), so differences of a few points are within noise.
* Screenshots of paper excerpts are included for checkability; the same images are served by the live LIVES site.

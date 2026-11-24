# Benchmarking and validation of LIVES EVD judgments with decision models

This folder records an audit of the 77 evidence nodes (EVDs) in LIVES and a benchmark of three **decision models**
(models that return calibrated probabilities instead of text) against a human expert (JP). Everything needed to
check or repeat the work is here: the exact inputs each model saw, the prompts, the raw model outputs, the analysis
scripts and the GSheets as CSV files.

**Status:** run `r1` (2026-11-24 UTC) is complete. A fourth sheet for Claude Opus 5.5 is set up but not yet filled.

## What was judged

For each EVD the models answered four questions, using only what is in the model-only GSheets (no paper PDFs, paper
text or web access):

| Task | Question | Labels |
|---|---|---|
| Relevancy | Is the EVD relevant to its review question(s) and worth learning? | Relevant / Irrelevant (P >= 0.5) |
| Fidelity | Is the gist of the headline EVD in the Description quote? (JP's gist rule, 2026-11-23) | Met / Partially Met / Unmet |
| Grounding: Quote | Does the screenshot show the quoted text word for word? (a wrong page number does not matter) | Correct / Partially Correct / Incorrect / Missing / NA |
| Grounding: Table/Fig | Does the page show the right table or figure? If no screenshot is shown the answer is **Missing** and no model is called (JP's rule) | Correct / Partially Correct / Incorrect / Missing / NA |

Held-out comparison: EVD 4-77 (74 EVDs). EVD 1-3 are the worked examples in the fidelity prompt and are excluded.
EVDs 45 and 47 each have extra continuation rows in the main sheet; they are NA there and not sent to the models.

## Models (all accessed through hosted APIs)

| Model | Model id returned by the API | Endpoint | Notes |
|---|---|---|---|
| Perplexity Decider 1.3 | `pplx-decider-v1.3` | `api.perplexity.ai/v1/decisions` | 27B; text and images |
| Liquid d1-ultra | `d1-ultra` | `api.liquid.ai/decisions/v1/systemone` | Liquid's docs list it as deprecated in favour of `d1.2-ultra`; context about 32K tokens (unconfirmed) |
| Jev | `jev-1.14.0` | `api.typesafe.ai/v1/systemone` | images through the preview header `TypeSafe-Danger-Zone-Images` |

No temperature or seed is exposed by any of the three. Calls were made on 2026-11-23 (pilots) and 2026-11-24 UTC (`r1`).
Request formats were built from each vendor's documentation as read on 2026-11-23; see `RUN-LOG.md`.

## Blinding

The model-only sheets and packets contain only vault content: the EVD statement, the Description quote, the table/figure
caption, the screenshots and the review question(s). No rating, note, draft or flag from JP or Claude is in any model
input. `reference/reference.csv` (JP's and Claude's ratings) is used **only** by `agreement.py` and `error_analysis.py`,
after the models have answered. The scripts that call the APIs never read it.

Review questions (`questions_by_evd.json`) come from the QUE tab of the human-only sheet (`inputs/que_tab.csv`, JP's edited
wording) and the vault's paper-to-question links (`DGRAPH-TABLE.md`). Pairing is paper-level: an EVD gets the question(s)
its paper asks. The app's nested question-to-claim-to-EVD lists were not used because they are auto-derived by keyword
overlap and labelled "verify".

## Results of run r1 (agreement with JP on EVD 4-77; Cohen's kappa in brackets)

| Task | Always-commonest baseline | Perplexity | Liquid | Jev | Majority of 3 | All three agree |
|---|---|---|---|---|---|---|
| Relevancy | 88% | 88% (0.40) | 89% (0.49) | 78% (0.27) | 88% (0.46) | 86% |
| Fidelity | 92% | 74% (0.26) | 81% (0.29) | 76% (0.17) | 77% (0.24) | 82% |
| Grounding: Quote | 81% | 85% (0.64) | 78% (0.52) | 81% (0.54) | 81% (0.56), 2 ties | 82% |
| Grounding: Table/Fig (n=72) | 88% | 89% (0.35) | 89% (0.35) | 89% (0.35) | 89% (0.35) | 100% |

Averaged over the four tasks the majority vote agrees with JP on 83.7%. Majority voting did not beat the best single model
on fidelity or quote, because the models make the same errors. Full tables, including pairwise agreement among the models,
JP and Claude Opus 5.5 (earlier ratings in the main sheet), are in `results/agreement.csv`. Per-EVD answers are in
`results/summary-r1.csv` and the raw API responses are in `results/*.r1.jsonl`.

## Error analysis (`results/error-analysis-r1.md`)

* **Fidelity is the weak task.** The models say Partially Met or Unmet 16-23 times against JP's 6 of 74. Twelve EVDs are
  wrong in all three models. Most are rows where JP rated Met because the numbers or the gist sit in the unquoted table
  summary on the page, while the prompt (JP's gist rule) lets the model see the quote only.
* **Quote errors are partly label inconsistency.** All three models call EVD 5, 6, 18 and 66 Incorrect with high
  confidence; the screenshot under the quote shows a different passage. JP rated these Correct before the verbatim-quote
  rule of 2026-11-23, and Claude's earlier notes flag the same mismatch. Excluding those four rows the quote agreement is
  about 90% (Perplexity), 83% (Liquid) and 86% (Jev).
* **Table/figure errors are identical for all three models** because 68 of 77 rows come from the Missing rule. The eight
  errors include EVD 9, 11 and 21, where a table screenshot sits in the quote slot on the vault page and so counts as "no
  table screenshot" under the rule.
* **Relevancy.** Seven EVDs (7, 17, 32, 49, 72, 75, 76) are wrong in all three models; several are rows where JP applied
  a "too granular" judgment the models cannot see. Jev marks 17 EVDs Irrelevant against JP's 9.
* **Agreement is at or near the always-commonest baseline** for relevancy, fidelity and table/figure, and clearly above it only for quote (Perplexity 85% against 81%). Report kappa or F1 as well as agreement.

## Reproduce and check

```
pip install -r requirements.txt
cp .env.example .env            # fill in the three API keys; keep .env out of git
# 1. inputs (needs the repository's vault/ folder, or set LIVES_VAULT)
python3 make_questions.py       # -> questions_by_evd.json
python3 build_packets.py        # -> packets/ (rebuilding gave byte-identical files for all 167 files)
# 2. judgments (about 235 API calls per model; 70 table/figure rows per model are rule-based)
python3 run_raters.py run --run-id r1          # fidelity prompt version 3 is the default
python3 run_raters.py export --run-id r1       # -> results/summary-r1.csv
# 3. analysis (uses reference/reference.csv, never read during step 2)
python3 agreement.py                           # -> results/agreement.csv
python3 error_analysis.py r1                   # -> results/error-analysis-r1.md
```

* `MANIFEST.sha256` lists a checksum for every file here: `shasum -a 256 -c MANIFEST.sha256`.
* `prompts/PROMPTS.md` holds every rubric and question; `prompts/rendered/` shows the exact request text for sample EVDs.
* `sheets/*.csv` are exports of the four model-only GSheets (Perplexity, Liquid, Jev filled; Claude Opus 5.5 empty template).
  Google Sheets drops image cells on export, so `merge_image_urls.py` puts the screenshot URLs back.
* Re-running the models will not give identical numbers: no sampling controls are exposed and vendors may update a model
  behind an alias. `results/*.r1.jsonl` records the model id each API reported.

## Cost and time (run r1, measured)

About 187K, 194K and 310K input tokens for Perplexity, Liquid and Jev; roughly $0.025 in total; 28 to 63 seconds of
request time per model. Model outputs are free (zero output tokens billed).

## Known limitations

* Fidelity and quote rubrics encode JP's rules as of 2026-11-23; some of JP's earlier ratings predate them (TODO items in the
  main sheet). Table/figure Missing vs NA cannot be decided without the paper, so Missing is the default.
* Liquid's `d1-ultra` is deprecated; Liquid's and Perplexity's data-retention terms and rate limits were not confirmed.
* Only 7 EVDs (9 images) have a table/figure screenshot on the evidence page, so that column is mostly rule-based.
* Models see the vault's resized copy of each screenshot (at most 1400 px); Jev's image input is a preview feature.
* Sample size is small (74 held-out EVDs), so differences of a few points are within noise.
* Screenshots of paper excerpts are included for checkability; the same images are served by the live LIVES site.
* Claude Opus 5.5 is intentionally not part of r1: its earlier judgments in the main sheet used a different setup.

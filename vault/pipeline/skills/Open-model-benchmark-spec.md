---
type: spec
title: Open-model benchmark (how far behind is the best open American model, and how fast is it catching up?)
status: first code built (shadow extraction); the rest specified
written: 2026-11-25
---

# Open-model benchmark (JP, 2026-11-25)

**Question.** The pipeline uses a frontier ensemble (Gemini 4 Neon, GPT-6.2 Sol, Claude Opus 5.5 and Sonnet 5.5, plus the decision models). How well would the best open American model, Inkling 2 Small, do the same tasks alone or as one member of the ensemble, and how does the gap change as open models improve? JP expects it to do worse; the point is to measure how much worse, at what saving, and to keep the data so the comparison can be repeated later.

**Rule.** Open-model outputs are benchmark data only. They never write to the vault and never decide anything.

## 1. What an open model can do here (honest limits)
- **Input.** Inkling 2 Small on Tinker takes text, not PDFs. It reads the PDF's text layer (PyMuPDF) with page markers, so it works on born-digital PDFs; tables can be garbled and scanned pages are lost. The frontier models read the PDF itself. This is part of the gap being measured.
- **Cost.** About $0.30 in and $1.00 out per million tokens (third-party pages, unverified): a 10-page paper costs a few cents for extraction, against about $0.50 for the frontier extraction.
- **No batch mode.** Runs go in parallel.

## 2. The ladder
| Level | What runs | What it shows |
|---|---|---|
| C. Frontier ensemble | the current pipeline | the reference |
| A. Solo | one open model does every task alone (extract, recheck, draft, vote, rate), no frontier calls | the full gap and the full saving |
| B. One role swapped | the open model replaces one participant at a time (for example Inkling in place of Neon, or in place of a rater) | which roles an open model can already take over |

Built now: level A for extraction (`lives_run.py --shadow thinkingmachines/Inkling-2-Small`), for node drafting and voting (Inkling always drafts the nodes and votes alongside the ensemble, benchmark only) and for the quality-signal ratings (Inkling always rates; Sonnet takes no part). A first test showed a bug of mine, not of the model: the extraction prompt had not been sent to Inkling (fixed), so the first result (prose instead of JSON) does not count.

## 3. Candidate models (check before use)
Policy (2026-11-25): hosted APIs only from US developers; open-weight models from any country may run locally if near the frontier. Not verified, to check on the vendors' pages: Inkling 2 Small and Inkling 2 Mini (Thinking Machines; Small is wired up), Gemma 4 (Google, open weights), Ripple-65B Preview (Ricursive Intelligence) and Reflection Beam (Reflection AI), both via hosted APIs, and gpt-oss and Olmo 3 (set aside on 2026-11-20 as extractors; cheap to include here). Tinker's model-list endpoint returned nothing on 2026-11-25, so read its pricing page for what it serves. Adding a model needs only a price entry in `llm_batch.PRICE` and a provider route.

## 4. Metrics, per stage
Extraction: JSON validity, share of quoted spans found in the PDF, share of numbers on the cited page, share of the frontier's primary-finding numbers also found, tier agreement, and (when JP labels exist) recall and precision of findings. Drafts: lint pass rate, rank in the vote, JP's fidelity and style rating. Quality ratings: agreement with the majority and Cohen's kappa against JP. Every stage: cost, time, cost per correct item. The first four extraction metrics are computed already and appear in the run review sheet, tab "Open-model shadow".

## 5. The Stage II snapshot (so the comparison can be repeated)
Freeze, once JP has labelled the Stage II run:
- the PDFs (SHA-256 of each paper and supplement) and the research questions;
- the prompts (file names and hashes) and the script hashes (`manifest.json` already records them);
- every model id with its date and list price;
- the raw outputs of every participant, frontier and open (kept private in `pipeline/runs/<run>/`, because they contain quoted spans), with a SHA-256 manifest;
- JP's labels and the scores.
The public repository keeps only the metadata and scores in `pipeline/benchmarks/stage-ii/` (to create). Tag the snapshot (for example `stage-ii-2026-12`) and never edit it.

**Re-run protocol (script to build: `benchmark_rerun.py`).** For a new model: run the frozen inputs with the frozen prompts, score with the same scripts, and append one row per model, task and date to the sheet tab "Progress over time" (model, release date, run date, score per task, cost, time). If a prompt has to change, start a new snapshot tag; never mix prompt versions in one comparison.

## 6. Cautions
- Small n (the seed papers, then the Stage II papers): report ranges, not single numbers.
- Contamination: papers published before a model's training cut-off may be in its training data; note each model's cut-off.
- Fairness: same inputs, same prompts, same thinking budget where the model allows it; record where it does not.
- The frontier outputs are not ground truth either; JP's labels are.

## 7. Open questions
Which open models beyond Inkling join the first round? Should level B run on the first four-paper pilot or wait for the Stage II run? Where does the "Progress over time" sheet live (a tab in the Quality Signals benchmark sheet or its own sheet)?

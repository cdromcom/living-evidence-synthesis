# Analytic reproducibility triage — 2026-08-31

Candidates: 16 SRC papers with a live Data Repo Check and/or Code Check tag.
Goal: find papers where the *raw, already-collected* data (not just code) lets us
recompute a headline EVD statistic without re-running any LLM or retraining a model.

## Tier 1 — Attempted, result below

| Paper | EVD | Reported | Recomputed | Verdict |
|---|---|---|---|---|
| Liu & Shah 2023 (ReviewerGPT) | EVD-028: 86.6% majority-vote accuracy, NeurIPS checklist | 86.6% | 206/238 = **86.55%** (from `labels.xlsx`'s own per-paper accurate/total columns) | **MATCH** |

## Tier 2 — Raw per-item data confirmed present, not yet attempted (needs methodology mapping)

| Paper | Repo | What's there | Why not attempted yet |
|---|---|---|---|
| Huntington-Klein & Murray 2024 | OSF spzbu | `llm_with_expert_data_rnr.xlsx` — 4,449-row raw per-response data (model × prompt × confounder, with Yes/No/Unsure response counts and expert ground-truth columns); `results_comparison_cleaned.xlsx` — cleaned comparison table | Reproducing the reported Cohen's kappa (EVD-050, EVD-054) requires correctly mapping which response category = "designated confounder" and which ground-truth column is authoritative — a real methods-reading task, not a one-line computation. Worth doing as a dedicated follow-up. |
| Woelfle et al. 2024 (Evidence-Appraisal-AI) | github.com/timwoelfle/Evidence-Appraisal-AI | `data/` (human ratings + consensus), `docs/` (LLM results already extracted), R dashboard script | Didn't confirm exact per-item file format/columns yet — next step is opening `2_extract_results_*.py` output format to see if PRISMA/AMSTAR per-item accuracy (EVD-045/047/043) is a direct read. |
| Wu et al. 2024 (novelty prediction) | github.com/njust-winchy/method_novelty_predict | `Dataset.json` (raw labels: novelty_sentence, chat_content, nov_score, decision, method_content) + `Code/proposed_main.py` reproducing F1=0.83/acc=0.84 | Running `proposed_main.py` trains a SciBERT-based neural model — feasible but needs a Python ML environment (torch/transformers) and real compute time, heavier than a spreadsheet read. |

## Tier 3 — Data/code present but requires re-running an LLM or a larger pipeline (out of current scope)

| Paper | Repo | Blocker |
|---|---|---|
| D'Arcy et al. 2024 (MARG) | github.com/allenai/marg-reviewer | Repo is inference/generation code; the actual ARIES corpus + generated outputs must be pulled separately from S3, and reproducing the paper's comment-count/recall numbers means re-running the MARG generation pipeline, not just reading existing outputs. |
| Xu et al. 2025 (LimitGen) | github.com/yale-nlp/LimitGen | Evaluation scripts require first generating fresh LLM outputs (`identification/main_syn.py`) before any accuracy can be computed — no cached per-item outputs found in the repo itself. |
| Sarol et al. 2024 (Citation-Integrity) | github.com/ScienceNLP-Lab/Citation-Integrity | Has a real labeled corpus, but reproducing F1=0.59/0.52 (EVD-008) means running/retraining the MultiVerS classifier (`train_target.py`/`predict.py`), not just reading a results file. |

## Tier 4 — Not yet inspected this pass

Lou 2025 (AAAR), Shahid 2025, Liang 2024, Wrightson 2025, Srinivasan 2025,
Zhang 2024 (reference errors), Idahl 2025 (OpenReviewer), Son 2025 (AI
Co-Scientists) — repo URLs are captured in each source's TRIPOD-LLM item 14e/14f
row, not yet opened and checked for raw-data feasibility.

## Tier 5 — Confirmed infeasible

| Paper | Why |
|---|---|
| Thelwall 2024 | Data availability explicitly ❌ — the paper's own scores "have never been disclosed to anyone else," no reproducible raw data exists at all. |

## Woelfle et al. 2024 — attempted, partial

Downloaded `human_consensus.csv` (ground truth, 112 papers × 38 items:
11 AMSTAR + 27 PRISMA) plus each model's `results.csv` (per-publication LLM
score arrays) directly from the repo, and recomputed per-model accuracy by
comparing item-by-item against human consensus, excluding NA either side —
matching the repo's own `calc_agreement()` R function's approach (excludes
"deferred"/NA from both numerator and denominator).

Recomputed individual-LLM accuracy across 6 models (Claude 2, Claude 3
Opus, GPT-4, GPT-3.5, Mixtral 8x22B, Mixtral 8x7B):
- PRISMA: 68.8%–78.5%
- AMSTAR: 55.3%–77.1%

Reported (EVD-047): "63-70 percent for PRISMA and 53-74 percent for AMSTAR."

**Verdict: PARTIAL.** Same ballpark and the AMSTAR lower bound is close
(55.3% vs. 53%), but my PRISMA range runs meaningfully higher than reported
(max 78.5% vs. their stated max 70%) and the AMSTAR upper bound also
exceeds theirs (77.1% vs. 74%). Not a clean match — plausible causes not
yet run down: the paper may exclude the "_rep" replicate runs I didn't
touch, may define "individual LLM" as a different/smaller model set, or
may restrict to a specific publication subset I didn't filter for. Flagging
as unresolved rather than claiming a match or a contradiction.

## Tier 4 triage results (2026-08-31)

| Paper | Repo checked | Verdict |
|---|---|---|
| Shahid 2025 (Idea Novelty Checker) | github.com/simra-shahid/idea_novelty_checker | **Tier 3.** Has ground-truth test.csv (32 items) but no cached model predictions anywhere in the repo — reproducing EVD-046's 0.81 accuracy requires re-running the full RAG pipeline (Semantic Scholar API + GPT-4o calls). |
| Liang 2024 | github.com/Weixin-Liang/LLM-scientific-feedback | **Tier 3.** Pure demo/pipeline code (`main.py` + one `example_paper.json`) — no dataset of the actual Nature-paper review-overlap results used for EVD-002/030/033/072. |
| Lou 2025 (AAAR-1.0) | github.com/RenzeLou/AAAR-1.0 | **Tier 3.** `scripts/` contains `chat_completion.py` and per-subtask `run_*.sh` — the benchmark requires calling LLM APIs to generate predictions before any metric script runs; no cached outputs found. |
| Idahl 2025 (OpenReviewer) | — | **Blocked.** Only a HuggingFace model + demo space were cited in the paper (no dedicated eval-code/data repo found); would need re-running the model against the 400-paper NeurIPS/ICLR test set. |
| Son 2025 (SPOT) | github.com/guijinSON/SPOT (found via author's repo list — paper's citation didn't include the exact URL) | **Tier 3.** `data/` holds only the raw source papers + metadata per DOI/arXiv ID; ground-truth error annotations exist (`annotation/retracted_machine_filtered_final.csv`) but no cached model predictions — reproducing EVD-049/062/063 needs `run_eval.py` against a live LLM. |
| Wrightson 2025 | OSF (exact project ID not captured in extracted PDF text — paper just says "a public, open access repository" without the specific link visible in what we extracted) | **Blocked** — needs a direct re-check of the PDF for the specific OSF link before this can be triaged further. |
| Srinivasan 2025 | github.com/ScienceNLP-Lab/RCT-Transparency | **Tier 2, redirected.** `inference/all_CONSORT_manual_data.csv` has ground truth + a `Prediction` column already computed — but it's only 341 sentences from what looks like one example paper (PMC4770816), not the 21,041-RCT population behind EVD-071's compliance-trend numbers. Useful as a smaller model-QC check, not a direct reproduction of the headline EVD. |
| Zhang 2024 (reference errors) | — | **Blocked** — paper text only says "available on GitHub" with no URL captured in our extraction; needs a direct PDF re-check for the actual link. |

## Tier 2 items attempted this pass

**Huntington-Klein & Murray 2024** — downloaded the real raw response data
(`llm_with_expert_data_rnr.xlsx`, confirmed structure: per-confounder,
per-prompt-variant (0-9), per-model *proportion* of "Confounder_Yes"
responses, plus expert ground-truth columns). Reproducing EVD-050's
"Cohen kappa as low as 0.16 across prompt variations" requires: (1) picking
a binarization threshold to turn each prompt's Confounder_Yes proportion
into a Yes/No decision, (2) deciding which kappa variant applies across 10
prompt-variant "raters" (Fleiss' kappa? pairwise average?). Rather than
guess at a specific methodological choice and risk reporting a confidently
wrong number, this is logged as needing a dedicated read of the paper's
exact Methods description before attempting — deferred, not abandoned.

**Wu et al. 2024** — confirmed a real labeled dataset (`Dataset.json`) and
a script literally reproducing F1=0.83/accuracy=0.84
(`Code/proposed_main.py`), but running it trains a SciBERT-based neural
model — needs a Python ML environment (torch/transformers) and real GPU/CPU
training time, a heavier lift than every other check attempted this pass.
Not attempted in this session; a good candidate for a dedicated follow-up
with more time budgeted.

## Summary across the full audit

- **1 clean match**: Liu & Shah 2023 (86.55% recomputed vs. 86.6% reported).
- **1 partial/unresolved**: Woelfle 2024 (right ballpark, exact ranges don't line up).
- **2 feasible but deferred** (need more time/care, not more triage): Huntington-Klein (methods ambiguity), Wu 2024 (needs a training run).
- **1 redirected**: Srinivasan (data found doesn't match the scale of the target EVD).
- **6 blocked on re-running an LLM or model we can't cheaply redo**: Shahid, Liang, Lou, Idahl, Son, Sarol, Xu, D'Arcy (8, not 6 — see Tier 3 above).
- **3 blocked on missing/uncaptured repo URLs**: Wrightson, Zhang 2024, (Idahl has a model but no eval repo).
- **1 confirmed infeasible**: Thelwall (no data ever released).

Out of 27 sources, roughly 2 produced an actual analytic-reproducibility
verdict this pass, with a further 2 realistically reproducible given more
dedicated time. The rest are either blocked by needing to re-run an LLM
(which this project has deliberately scoped out) or by repo URLs the
extraction didn't capture precisely enough to locate.

## Checked: do the two Statistic Accuracy-flagged papers have usable raw data?

Natural follow-up question — prioritize reproduction attempts on the same
2 sources already flagged with a "Statistic Accuracy: Issues found"
verdict, since that's exactly where verifying against raw data matters
most. Checked both; neither is attemptable:

- **Roberts 2023 (SRC-012)** — `top/repository-check/not-addressed` and
  `top/code-check/not-addressed`: no data or code was ever claimed, so
  there's nothing to recompute from. The flagged issue (a CI printed with
  reversed bounds) is a typesetting/sign-error question a dataset couldn't
  resolve regardless.
- **Shahid 2025 (SRC-014)** — has a repo (`top/repository-check/addressed`),
  and the flagged number (AI Scientist's F1=0.44) is from a baseline
  *Shahid's own paper* ran on their own 32-item test set, not borrowed from
  elsewhere, which looked promising. But the repo only contains cached
  outputs for one single demo idea (`results/test_idea/`) — not the actual
  32-item benchmark run behind that figure. Reproducing it would require
  re-running the AI Scientist baseline ourselves, which is exactly the
  "re-run an LLM" case this audit deliberately excludes.

Confirms the real bottleneck across this whole audit is raw-data
availability, not which papers look most worth checking.

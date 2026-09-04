---
NodeFormality: draft
aliases:
tags:
  - task/decision-judgment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/56pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b80-7713-af4a-5610dfbca6b6
appraisal_overall: L0-M3-H2
tripod_llm_pct: 56pct
---

## Source

[[@idahlOpenReviewerSpecializedLarge2025]]

## Description

> "OpenReviewer matches at least one human reviewer for 55.5% of its generated reviews and has an average recommendation error of 0.96. In contrast, GPT4o matches at least one reviewer only in 23.8% of reviews with a higher average recommendation error of 2.34." (Idahl & Ahmadi, 2025, p. 4)
>
> ![[idahlOpenReviewer2025-table1-p4-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark comparing one fine-tuned LLM (OpenReviewer) against four general-purpose LLM baselines on a held-out peer-review test set.
>
> **Method type:** automatic alignment metrics, Exact Match rate (EM) and Average Error, against human reviewer recommendations.
>
> **Tools:** Llama-OpenReviewer-8B (Llama-3.1-8B-Instruct full-finetuned on ≈79K filtered ICLR/NeurIPS reviews); Llama-3.1-8B-Instruct, Llama-3.1-70B-Instruct, Claude-3.5-Sonnet (Oct. 22), GPT-4o (2024-11-20); vLLM serving for OpenReviewer/Llama and OpenRouter for Claude/GPT-4o.
>
> **Dependent variables:** EM (% of generated reviews whose recommendation exactly matches at least one human reviewer's recommendation on the 1–10 scale) and Avg. Error ± SD (mean absolute distance between the generated recommendation and the human reviewers' average recommendation, on the 1–10 scale).
>
> **Independent variable:** model identity (5 LLMs).

> "To measure how well the recommendation of a generated review matches the recommendations of the human reviewers, we check whether it exactly matches one of the human reviewers' recommendations. Additionally, we measure the average absolute distance between the generated review's recommendation and the human reviewers' average recommendations. For this, we normalize the recommendation scores to a scale from 1 (strong reject) to 10 (strong accept)." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-4.png]]

### How?

> **Procedure:** (1) Use the same 400 held-out NeurIPS 2024 + ICLR 2025 papers (most-recent venues; not used during fine-tuning). (2) Generate one review per paper per model with greedy decoding (temperature=0) and the OpenReviewer system + user prompts (Figures 3–4). (3) Parse the recommendation field from each generated review and normalize to 1–10. (4) For each paper, check whether the generated recommendation exactly equals any of the OpenReview human reviewers' recommendations (count → EM%). (5) Compute the absolute difference between the generated recommendation and the human-reviewer average for each paper, then average across the 400 papers (→ Avg. Error ± SD). No statistical-significance test reported for the model-vs-model EM/Error comparisons.

> "we conduct experiments using a test set of 400 held-out papers and their reviews from NeurIPS 2024 and ICLR 2025, the most recent venues in our dataset. We compare OpenReviewer to Llama-3.1-8B-Instruct and Llama-3.1-70B-Instruct, Claude-3.5-Sonnet (Oct. 22) from Anthropic, and GPT-4o (2024-11-20) from OpenAI. We generate one review for each paper in the test set using greedy decoding (temperature of 0). All LLMs are instructed with the same system and user prompts used by OpenReviewer." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-5.png]]

### Who?

> **Models / participants:** 5 LLMs evaluated. Human reference = real OpenReview reviewer recommendations (multiple per paper).
>
> **Sample-size flow:** OpenReview ICLR + NeurIPS 2022-onwards crawl → 36K papers + 141K reviews → length filter (top + bottom 1% removed) → keep only "Confident, but not absolutely certain" or higher reviewer-confidence reviews → ≈79K reviews used for fine-tuning. Test set: 400 held-out papers from NeurIPS 2024 + ICLR 2025. Per-model evaluation N = 400 generated reviews. Number of human reviewers per paper not stated explicitly but at least 3 implied by example outputs.

> "To measure how well OpenReviewer reviews align with reviews from human reviewers, we conduct experiments using a test set of 400 held-out papers and their reviews from NeurIPS 2024 and ICLR 2025, the most recent venues in our dataset." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-6.png]]

## Other Notes

- The recommendation scores were normalized to a scale from 1 (strong reject) to 10 (strong accept) so that ICLR (typically 1–10) and NeurIPS (typically 1–10 or 1–6 depending on year/aspect) ratings are comparable.
- EM is a strict metric, being off by 1 point still counts as a miss, so it co-moves with the Avg. Error metric in the same direction.
- No statistical-significance test (e.g., bootstrap CI, paired test) is reported for EM or Avg. Error differences between models.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@idahlOpenReviewerSpecializedLarge2025#TRIPOD-LLM reporting]].

| Model                                    |  EM (%)  | Avg. Error (1–10 scale) ± SD |
| ---------------------------------------- | :------: | :--------------------------: |
| Llama-3.1-8B-Instruct                    |   14.0   |         2.95 ± 1.19          |
| Llama-3.1-70B-Instruct                   |   11.5   |         3.03 ± 1.34          |
| Claude-3.5-Sonnet                        |   15.5   |         2.77 ± 1.27          |
| GPT-4o (2024-11-20)                      |   23.8   |         2.34 ± 1.17          |
| **OpenReviewer (Llama-OpenReviewer-8B)** | **55.5** |       **0.96 ± 0.85**        |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The OpenReviewer training and test data were limited to ICLR and NeurIPS conferences limiting domain generalizability]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]

- [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]]
- [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]]

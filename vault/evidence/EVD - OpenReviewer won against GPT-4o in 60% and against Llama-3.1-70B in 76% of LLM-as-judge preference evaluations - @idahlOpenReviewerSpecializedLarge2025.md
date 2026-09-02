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
nodeID: 019ddb4e-6b81-7188-8476-cec09347ad21
appraisal_overall: L0-M3-H2
tripod_llm_pct: 56pct
---

## Source

[[@idahlOpenReviewerSpecializedLarge2025]]

## Description

> "According to the LLM judge, OpenReviewer wins against other LLMs for most papers, achieving win rates ranging from 60% against GPT4o to 76% against Llama-3.1-70B-Instruct." (Idahl & Ahmadi, 2025, p. 5)
>
> ![[idahlOpenReviewer2025-table2fig2-p5-1.png]]

## Methods Context

### What?

> **Study design:** arena-style pairwise preference evaluation (LLM-as-a-judge), for each paper, an LLM judge compares OpenReviewer's review against one baseline LLM's review using the human "expert" reviews as ground truth.
>
> **Method type:** GPT-4o-as-judge classification into {Review A wins, Review B wins, Tie} per pairwise comparison.
>
> **Tools:** GPT-4o (2024-11-20) as judge with custom system + user prompt (Figures 5–6) that includes the human expert reviews and asks the judge to compare per-section alignment (soundness, presentation, contribution, strengths, weaknesses, questions, rating); A/B labels delimited with XML tags; reviews compared per-section before final decision.
>
> **Dependent variable:** win rate (% of 400 papers where OpenReviewer is judged the better-aligned review against each baseline).
>
> **Independent variable:** baseline-model identity (4 baselines).

> "We run an arena-style preference evaluation with an LLM-as-a-judge setup to measure whether OpenReviewer produces better reviews than the other LLMs. This is similar to MT bench (Zheng et al., 2023) and AlpacaEval (Li et al., 2023b), which use an LLM-as-a-judge to evaluate the quality of instruction-tuned language models and chatbots." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-7.png]]

### How?

> **Procedure:** (1) Take the same 400 NeurIPS 2024 + ICLR 2025 test papers. (2) For each paper, pair OpenReviewer's generated review against one baseline's generated review (4 baselines → 4 pairings per paper). (3) Construct a judge prompt containing the paper's human expert reviews, Review A (one model), and Review B (the other model), delimited with XML tags. (4) GPT-4o (2024-11-20) judge first compares each section (soundness, presentation, contribution, strengths, weaknesses, questions, rating) of A vs. B against the corresponding expert sections, then issues a final decision: Review A, Review B, or Tie. (5) Compute the win rate per (OpenReviewer vs. baseline) pairing across all 400 papers. Order randomization, position-bias correction, and self-preference checks not described.

> "Given a set of human "expert" reviews and two reviews, A and B, we ask GPT-4o (2024-11-20) to determine whether review A or B aligns better with the given expert reviews. Specifically, we first ask it to consider how well each section of A and B matches the corresponding section in the expert reviews and then to decide between A, B, or Tie." (Idahl & Ahmadi, 2025, p. 5)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p5-1.png]]

### Who?

> **Models / participants:** 4 baselines compared head-to-head against OpenReviewer (Llama-3.1-8B-Instruct, Llama-3.1-70B-Instruct, Claude-3.5-Sonnet, GPT-4o 2024-11-20). Judge: GPT-4o (2024-11-20); note that GPT-4o judges its own reviews against OpenReviewer.
>
> **Sample-size flow:** Same 400 held-out NeurIPS 2024 + ICLR 2025 papers as the EM/Error EVD. For each paper, 4 pairwise judgments are produced (one per baseline) → 1,600 judge calls total. Expert reviews per paper are the original OpenReview human reviewer comments.

> "we conduct experiments using a test set of 400 held-out papers and their reviews from NeurIPS 2024 and ICLR 2025, the most recent venues in our dataset." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-8.png]]

## Other Notes

- Win rates: Llama-3.1-8B-Instruct 70%, Llama-3.1-70B-Instruct 76%, Claude-3.5-Sonnet 69%, GPT-4o 60%. The OpenReviewer-vs-GPT-4o pairing is the only one where the judge is the same model as the baseline being compared, a known LLM-as-judge self-preference confound. OpenReviewer still wins (60%), but the margin is the smallest.
- Authors acknowledge: "While human judgments could be more meaningful, they are expensive to obtain as, in our case, they would require annotators to be trained reviewers and study each paper in great detail."
- No order-randomization, position-bias correction, or judge-model-diversity check is reported.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@idahlOpenReviewerSpecializedLarge2025#TRIPOD-LLM reporting summary]].

| OpenReviewer vs. baseline (judge: GPT-4o 2024-11-20) | OpenReviewer wins | Tie | OpenReviewer loses |
| --- | :---: | :---: | :---: |
| Llama-3.1-8B-Instruct | 70% | 20% | 10% |
| **Llama-3.1-70B-Instruct** | **76%** | 12% | 12% |
| Claude-3.5-Sonnet | 69% | 12% | 19% |
| **GPT-4o (2024-11-20)** | **60%** | 10% | 30% |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The evaluation used LLM-as-judge which may favor outputs from models similar to the judge]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]

- [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant]]
- [[EP - LLM peer-review systems can predict paper acceptance and preference at near-human accuracy]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/review-generation
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/25pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b78-77d7-8711-497f3ed763af
appraisal_overall: L0-M2-H3
tripod_llm_pct: 25pct
---

## Source

[[@tyserAIDrivenReviewSystems2024]]

## Description

> "Reviews written by humans and GPT-4 with all related review contexts were assessed close to each other by human evaluators, with scores of 4.80 and 4.76. Reviews written by humans but evaluated by GPT-4 scored lower at 4.27. Reviews written by GPT-4 and evaluated by itself scored 4.65. In guiding authors to improve their papers, reviews written by GPT with all related review contexts and humans scored the highest at 4.79." (Tyser et al., 2024, p. 13 [Appendix F])
>
> ![[tyserAIDrivenReviewSystems2024-table5-p12-1.png]]

## Methods Context

### What?

> **Study design:** blind 2 × 2 cross-evaluation (Writer × Evaluator) of academic-paper reviews on a sub-sample of papers from the Reviewer Arena corpus.
>
> **Method type:** rubric-based scoring of full reviews on a 0–5 Likert scale (0 = worst / content-free, 5 = best).
>
> **Tools:** GPT-4 with full P5 context as the LLM writer and as one of the two evaluators; ICLR 2023 reviewers as the human writer and one of the two evaluators.
>
> **Dependent variables (3 rubric items):** (i) "How well does the review explain the score?", (ii) "How well does the review guide the authors to improve the paper?", (iii) "Does the review contain content specific to the paper?".
>
> **Independent variables:** review-Writer ∈ {Human, GPT-4 P5} × review-Evaluator ∈ {Human, GPT-4} → 4 cells. The human evaluator is described as "an ICLR 2023 reviewer."
>
> "The human review evaluator assesses reviews written by human reviewers and the LLM, GPT-4 with context P5. The human review writer is an ICLR 2023 reviewer. Table 5 shows the average evaluation results on a randomized sample of 5% of the papers evaluated by human experts." (Tyser et al., 2024, p. 12)
> ![[tyserAIDrivenReviewSystems2024-evd-p14-1.png]]

### How?

> **Procedure:** (1) take the Reviewer Arena set of 150 papers (each with one human OpenReview review + one GPT-4 P5 review). (2) Randomly sample **5% of the papers** (~7–8 papers) for blind expert evaluation. (3) For each sampled paper, present each review to two independent evaluators, one Human (an ICLR 2023 reviewer) and one GPT-4, yielding 4 (Writer × Evaluator) conditions per review. (4) Each evaluator scores the review on the 3 rubric items using the 0–5 scale (0 = content-free). (5) Average each cell across the sample. The same paper-corpus protocol underpins the BT-based Reviewer Arena (Section 3): "five expert evaluators were provided with 150 papers together with two anonymous reviews for each paper", the present sub-study reuses that pool but evaluates **whole-review quality on a rubric** rather than pairwise preference.
>
> "five expert evaluators were provided with 150 papers together with two anonymous reviews for each paper. Each paper was randomly assigned two reviewers from the list of five potential reviewers: Human, GPT-4 (Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), and Command R+." (Tyser et al., 2024, p. 4)
> ![[tyserAIDrivenReviewSystems2024-evd-p4-3.png]]

### Who?

> **Review writers (2):** Human = ICLR 2023 reviewer (OpenReview); LLM = GPT-4 with full P5 context (paper text + review form + reviewer guide + code of ethics + code of conduct + area chair guidelines + prior-year statistics).
>
> **Review evaluators (2):** Human = an ICLR 2023 reviewer (the paper does not specify whether this is the same individual as the writer or a separate panel; "the human review evaluator" is singular, suggesting a single rater for this Appendix-F sub-study); GPT-4 (snapshot not specified).
>
> **Paper sample-size flow:** Reviewer Arena candidate corpus = 150 papers → **5% random sample ≈ 7–8 papers** evaluated under the 2 × 2 design. The exact N is not reported numerically; the sample is described only as "5% of the papers."
>
> "Table 5: The human review evaluator evaluates human and P5 written reviews of papers. The human review writer is an ICLR 2023 reviewer. The LLM is GPT-4 with context P5. The evaluation is on a scale of 0–5 (0 being the worst, five the best). For the third question, a score of 0 indicates a content-free review." (Tyser et al., 2024, p. 12)
> ![[tyserAIDrivenReviewSystems2024-evd-p14-2.png]]

## Other Notes

- The headline "human and GPT-4 P5 score comparably" is true **only when the evaluator is human** (4.80 vs. 4.76 on Q1; 4.66 vs. 4.79 on Q2; 4.53 vs. 4.68 on Q3). When the evaluator is GPT-4, the model is harder on human-written reviews (Q1 = 4.27) than on its own (Q1 = 4.65); the asymmetric self-rating pattern is consistent with a self-enhancement / self-recognition bias.
- Confusion-matrix analysis (Appendix E, p. 12, treating the human-reviewer mean as ground truth): the LLM accepted **1 paper** with score ≥ 7 that humans rated ≤ 3; rejected **4 papers** with score ≤ 3 that humans rated ≥ 7. Looser thresholds (LLM ≥ 6 vs. human ≤ 4): 8 false-accepts; (LLM ≤ 4 vs. human ≥ 6): 22 false-rejects. So the LLM is more prone to false-rejects than false-accepts at this calibration.
- The 5%-sample (~7–8 papers) is small; 95% CIs are not reported, and the closeness of 4.80 vs. 4.76 (Q1) is unlikely to be statistically distinguishable.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@tyserAIDrivenReviewSystems2024#TRIPOD-LLM reporting]].

| Rubric question (0–5) | Writer = Human / Eval = Human | Writer = GPT-4 P5 / Eval = Human | Writer = Human / Eval = GPT-4 | Writer = GPT-4 P5 / Eval = GPT-4 |
| --- | :---: | :---: | :---: | :---: |
| Q1: Explains the score? | **4.80 ± 0.39** | **4.76 ± 0.51** | 4.27 ± 0.65 | 4.65 ± 0.52 |
| Q2: Guides authors to improve? | 4.66 ± 0.51 | 4.79 ± 0.71 | 4.14 ± 0.50 | 4.27 ± 0.45 |
| Q3: Content specific to the paper? | 4.53 ± 0.79 | 4.68 ± 0.82 | 4.97 ± 0.16 | 4.95 ± 0.22 |

| Confusion-matrix counts (LLM vs. human-mean ground truth) | Count |
| --- | :---: |
| LLM accepted (≥7) but humans rejected (≤3) | 1 |
| LLM rejected (≤3) but humans accepted (≥7) | 4 |
| LLM accepted (≥6) but humans rated low (≤4) | 8 |
| LLM rejected (≤4) but humans rated high (≥6) | 22 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Users find LLM-generated peer-review feedback substantively helpful at rates comparable to human reviewers]]

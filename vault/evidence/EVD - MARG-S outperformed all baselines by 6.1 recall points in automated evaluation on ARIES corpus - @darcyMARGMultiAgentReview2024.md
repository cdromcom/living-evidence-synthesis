---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/review-generation
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/53pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7c-7466-b4e2-731e96fe9cb1
appraisal_overall: L0-M4-H1
tripod_llm_pct: 53pct
---

## Source

[[@darcyMARGMultiAgentReview2024]]

## Description

> "our method outperforms the strongest baseline by 6.1 recall points in the automated evaluation" (D'Arcy et al., 2024, p. 1)
>
> ![[darcyMARGMultiAgentReview2024-evd-p2-2.png]]
>
> "We find that our proposed MARG-S method outperforms all baselines in terms of recall, but generates more comments than other baselines and thus has lower precision and Jaccard scores." (D'Arcy et al., 2024, p. 11)
>
> ![[darcyMARGMultiAgentReview2024-evd-p10-1.png]]

## Methods Context

### What?

> **Study design:** held-out automated benchmark of LLM-generated peer-review comments against gold human-reviewer comments.
>
> **Method type:** GPT-4-as-judge alignment evaluation with two-stage matching (many-many candidate generation + pairwise relatedness/specificity scoring), aggregated into recall, precision, and pseudo-Jaccard metrics.
>
> **Tools:** GPT-4 (gpt-4-0613, 8192-token capacity) for both review generation and alignment scoring; Grobid for PDF parsing; ARIES corpus (D'Arcy et al. 2023) as the source of (paper, real-reviewer-comment) pairs; comparison methods MARG-S, MARG-TP, SARG-B, SARG-TP, LiZCa (Liang et al. 2023), plus MARG-S ablations (no-refinement, experiments-only, clarity-only, impact-only) and a Human baseline.
>
> **Dependent variables:** Recall (|C_gen ⃗∩ C_real| / |C_real|), Precision (|C_gen ⃖∩ C_real| / |C_gen|), pseudo-Jaccard (intersection / (|C_gen|+|C_real|−intersection)), and average comments per review.
>
> **Independent variables / covariates:** review-generation method; matching-threshold settings (relatedness ∈ {medium, high}; relative specificity ∈ {less, same, more}) — ablated for MARG-S vs. LiZCa in Figure 3.
>
> "To automatically evaluate the quality of generated reviews, we measure their overlap with real reviews from papers in the ARIES corpus (D'Arcy et al., 2023). That is, we attempt to match the generated comments to comments extracted from real (human-written) reviews. Because ARIES only has comment annotations for a small set of reviews, we use GPT to extract comments from all reviews for a subset of 30 papers and treat this as our test set." (D'Arcy et al., 2024, p. 9)
> ![[darcyMARGMultiAgentReview2024-evd-p8-1.png]]

### How?

> **Procedure:** (1) parse each PDF with Grobid and split into 4096-token paragraph-aligned chunks given to worker agents; (2) generate a review with each method (paper-level, with all baselines re-run on Grobid output for consistency); (3) extract comments from real reviews using a GPT prompt instructed to focus only on actionable feedback and ignore style/grammar; (4) **many-many matching stage** — feed all generated and real comments to GPT-4 and ask it to output all matching pairs; do five passes with randomly permuted comment / review order, keep pairs produced by ≥2 of the 5 runs; (5) **pairwise stage** — for each candidate pair, prompt GPT-4 to output a relatedness label (none / weak / medium / high) and a relative-specificity label (less / same / more); (6) declare a match when relatedness ∈ {medium, high} AND relative specificity ∈ {same, more}; (7) compute Recall, Precision, pseudo-Jaccard per (generated, real) review pair and macro-average over the 30 test papers; (8) sweep matching thresholds for MARG-S and LiZCa to produce Figure 3 heatmaps; (9) report average input + generated tokens per paper as a cost proxy (Table 4).
>
> "we begin with a 'many-many' matching stage that efficiently compares the full set of comments in both reviews and identifies possibly-matching pairs, followed by a more accurate (but more expensive) pairwise stage that examines the candidate pairs to produce a final list... To be considered a match, a comment pair must have 'medium' or 'high' relatedness, and the generated comment must have 'same' or 'more' specificity compared to the human comment." (D'Arcy et al., 2024, p. 9)
> ![[darcyMARGMultiAgentReview2024-evd-p8-2.png]]

### Who?

> **Models / data:** GPT-4 (gpt-4-0613, 8k context window) used for both generation and alignment scoring across all conditions. No human ratings in this evaluation.
>
> **Sample-size flow:** ARIES corpus (D'Arcy et al. 2023) → subset of **30 test papers** with associated real reviewer comments → 11 method conditions evaluated on all 30 papers (5 main methods + 4 MARG-S ablations + Human baseline). Number of extracted real-reviewer comments per paper not reported in main text. Per-paper averages of generated comments range from 4.0 (LiZCa) to 19.8 (MARG-S) — see Table 2.
>
> "we use GPT to extract comments from all reviews for a subset of 30 papers and treat this as our test set." (D'Arcy et al., 2024, p. 9)
> ![[darcyMARGMultiAgentReview2024-evd-p8-3.png]]

## Other Notes

- MARG-S generates ~5× the comments of LiZCa (19.8 vs. 4.0), driving lower precision/Jaccard despite higher recall. The authors explicitly argue recall matters more because users can filter bad comments — but in practice high comment volume may overwhelm authors.
- The Human-Human baseline has lower recall (9.42) than MARG-S (15.84) but the highest precision (12.00) — consistent with Liang et al. 2023's finding that Human-Human agreement is lower than LiZCa-Human agreement.
- Cost: MARG-S consumes 1,236,344 input tokens and 51,255 generated tokens per paper on average — roughly 9× MARG-TP and 167× LiZCa.
- Threshold sensitivity (Figure 3): at "high" relatedness × "more" specificity MARG-S recall drops to 8.6 and LiZCa to 3.1 — both methods lose recall under stricter matching but MARG-S degrades less.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@darcyMARGMultiAgentReview2024#TRIPOD-LLM reporting summary]].

| Method | Recall | Precision | Jaccard | # comments / paper |
| --- | --- | --- | --- | --- |
| SARG-B | 7.43 | 1.40 | 1.25 | 19.7 |
| SARG-TP | 10.62 | 4.61 | 3.46 | 11.6 |
| MARG-TP | 8.49 | 5.34 | 3.52 | 8.5 |
| LiZCa | 9.67 | **9.96** | **5.58** | 4.0 |
| **MARG-S** | **15.84** | 4.41 | 3.53 | 19.8 |
| MARG-S no-refinement | 11.92 | 3.32 | 2.70 | 18.3 |
| MARG-S experiments-only | 4.36 | 4.83 | 2.23 | 4.1 |
| MARG-S clarity-only | 3.25 | 2.65 | 1.46 | 6.9 |
| MARG-S impact-only | 8.88 | 4.75 | 3.32 | 8.8 |
| Human | 9.42 | 12.00 | 5.45 | 4.7 |

| MARG-S vs. strongest baseline | Δ |
| --- | --- |
| Recall delta vs. SARG-TP (strongest non-LiZCa baseline) | +5.22 |
| Recall delta vs. LiZCa | +6.17 (≈ "6.1 recall points" headline) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The MARG automated evaluation used overlap-based matching which is an imperfect proxy for review quality]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]

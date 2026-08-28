---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/55pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
  - forensic/monotonicity-check/consistent
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b83-7219-98f4-b40b414c76b7
appraisal_overall: L1-M3-H1
tripod_llm_pct: 55pct
---

## Source

[[@liangCanLargeLanguage2024a]]

## Description

> "the pairwise overlap significantly decreased from 30.85% to 0.43% after shuffling (Fig. 2a). A similar drop from 39.23% to 3.91% was observed on ICLR (Fig. 2b). These results suggest that LLM feedback is paper-specific." (Liang et al., 2024, p. 4)
>
> ![[liangCanLargeLanguage2024a-quote-shuffle-desc-p4.png]]

## Methods Context

### What?

> **Study design:** null-model permutation / shuffling experiment to test whether GPT-4's overlap with human reviews could be explained by generic-feedback applicability.
>
> **Method type:** within-stratum random reassignment of LLM feedback across papers, run through the same extract-then-match pipeline used in the main overlap analysis.
>
> **Tools:** same GPT-4 feedback pipeline; same Stage 1 + Stage 2 GPT-4 extract/match pipeline (extraction F1 = 0.968, matching F1 = 0.824); shuffling stratified by (journal × Nature root category) for Nature, and by conference year (ICLR 2022 / ICLR 2023) for ICLR.
>
> **Dependent variable:** pairwise hit rate between shuffled-LLM and human reviewer comments, contrasted against the unshuffled overlap from the main analysis.
>
> **Independent variables:** condition = {real LLM feedback, shuffled LLM feedback}; dataset = {Nature, ICLR}.
>
> "Is it possible that LLM merely generates generic feedback applicable to multiple papers? A potential null model is that LLM mostly produces generic feedback applicable to many papers. To test this hypothesis, we performed a shuffling experiment aimed at verifying the specificity and relevance of LLM generated feedback." (Liang et al., 2024, p. 4)
> ![[liangCanLargeLanguage2024a-evd-p4-1.png]]

### How?

> **Procedure:** for each Nature paper, the LLM-generated feedback was randomly reassigned to **another paper from the same journal and within the same Nature root category** (root categories: physical sciences; earth & environmental sciences; biological sciences; health sciences; scientific community & society; multi-category papers were paired with another spanning all the same categories). For ICLR, the shuffle was within conference year (ICLR 2022 or ICLR 2023). The shuffled (paper, LLM-feedback) pairs were then fed through the identical Stage 1 + Stage 2 extract-and-match pipeline that produced the original 30.85% / 39.23% hit rates, and the resulting hit rates were compared. Under the null (generic feedback), shuffled overlap should be ≈ unshuffled overlap; observed sharp drops to near-floor reject the null at ****P < 0.0001 (Fig. 2a, b; Supp. Fig. 1).
>
> "For each paper in the Nature family journal data, the LLM feedback was shuffled for papers from the same journal and within the same Nature category (Methods). If the LLM were producing only generic feedback applicable to many papers, we would observe no decrease in the pairwise overlap between shuffled LLM feedback and human feedback. In contrast, the pairwise overlap significantly decreased from 30.85% to 0.43% after shuffling (Fig. 2a). A similar drop from 39.23% to 3.91% was observed on ICLR (Fig. 2b)." (Liang et al., 2024, p. 4)
> ![[liangCanLargeLanguage2024a-evd-p4-2.png]]

### Who?

> **Source data:** identical to the main overlap EVD — **3,096 Nature accepted papers / 8,745 human reviews** across 15 Nature family journals (Jan 2022 – Jun 2023, post-GPT-4-cutoff); **1,709 ICLR papers / 6,505 human reviews** (ICLR 2022 + 2023, all decision categories).
>
> **No new annotators or human subjects** introduced for this experiment — the shuffle reuses the same pipeline, datasets, and validation runs as the main overlap analysis.
>
> "For papers published in the Nature family, the LLM-generated feedback for a given paper was randomly paired with human feedback for a different paper from the same journal and Nature root category. These categories included physical sciences, earth and environmental sciences, biological sciences, health sciences, and scientific community and society. If a paper was classified under multiple categories, the shuffle algorithm paired it with another paper that spanned the same categories. For the ICLR dataset, we compared human feedback for a paper with LLM feedback for a different paper, randomly selected from the same conference year, either ICLR 2022 or ICLR 2023." (Liang et al., 2024, p. 9)
> ![[liangCanLargeLanguage2024a-evd-p9-1.png]]

## Other Notes

- The near-floor shuffled overlap (0.43% pairwise / 1.13% global on Nature; 3.91% pairwise on ICLR) rejects the "GPT-4 produces generic boilerplate" null at ****P < 0.0001 in both datasets.
- The shuffled control was within stratum (same journal + same Nature category, or same ICLR year), so the drop is not attributable to topic-distribution mismatch — only to paper-specificity.
- Note: the original quote in the Description fixed a typo ("A significant decreased" → "the pairwise overlap significantly decreased") to match the verbatim source text.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liangCanLargeLanguage2024a#TRIPOD-LLM reporting summary]].

| Dataset | Real LLM hit rate | Shuffled LLM hit rate | Drop | Sig. |
| --- | :---: | :---: | :---: | :---: |
| **Nature (n = 3,096) — pairwise (Fig. 2a)** | **30.85%** | **0.43%** | ~71× | ****P < 0.0001 |
| Nature — global (≥ 1 reviewer match; Supp. Fig. 1a) | 57.55% | 1.13% | ~51× | ****P < 0.0001 |
| ICLR (n = 1,709) — pairwise (Fig. 2b) | 39.23% | 3.91% | ~10× | ****P < 0.0001 |
| ICLR — global (Supp. Fig. 1b) | 77.18% | ~13% | ~6× | ****P < 0.0001 |

| Robustness across overlap metrics (Supp. Fig. 2) | Shuffled overlap |
| --- | :---: |
| Hit rate | near 0% on Nature, ~4% on ICLR |
| Szymkiewicz–Simpson | near 0% / very low |
| Jaccard index | near 0% / very low |
| Sørensen–Dice | near 0% / very low |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

- [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]
- [[EP - LLM-generated peer review feedback is paper-specific not generic boilerplate]]

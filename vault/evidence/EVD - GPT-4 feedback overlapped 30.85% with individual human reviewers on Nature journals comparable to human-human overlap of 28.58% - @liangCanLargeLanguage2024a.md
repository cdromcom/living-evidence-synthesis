---
NodeFormality: draft
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
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b6e-76c1-a58b-090ac22ba58c
appraisal_overall: L1-M3-H1
tripod_llm_pct: 55pct
---

## Source

[[@liangCanLargeLanguage2024a]]

## Description

> "When comparing LLM feedback with comments from each individual reviewer, approximately one third (30.85%) of GPT-4 raised comments overlapped with comments from an individual reviewer (Fig. 2a). The degree of overlap between two human reviewers was similar (28.58%), after controlling for the number of comments (Methods)." (Liang et al., 2024, p. 3)
>
> ![[liangCanLargeLanguage2024a-quote-30pct-desc-p3.png]]
>
> Grounding figure context (p. 3): overlap discussion with Fig. 2a reference.
>
> ![[liangCanLargeLanguage2024a-overlap-p3-3.png]]

## Methods Context

### What?

> **Study design:** retrospective benchmark of LLM-generated review comments against human peer-review comments on already-published papers. **Method type:** automated two-stage extract-then-match pipeline (GPT-4 extractive summarization → GPT-4 semantic matching), with hit-rate as the overlap metric and a controlled human-vs-human baseline. **Tools:** OpenAI GPT-4 (zero-shot, single pass over PDF, ~6,500 tokens of parsed input from ScienceBeam); 4-section structured-feedback prompt; comment-extraction prompt (Supp. Fig. 13); semantic-matching prompt with 5–10 similarity scale, retaining only matches rated ≥ 7 ("Strongly Related"); Nature website + OpenReview API for source data. **Dependent variables:** pairwise hit rate = |A∩B|/|A| between GPT-4 comments (set A) and a single human reviewer's comments (set B); also Szymkiewicz–Simpson, Jaccard, and Sørensen–Dice as robustness metrics. **Independent variables / covariates:** comparison condition (GPT-4 vs human reviewer; human vs human with N controlled to GPT-4's comment count); journal and Nature root category; ICLR decision outcome (Oral / Spotlight / Poster / Reject / Withdrawn) for the parallel ICLR analysis.
>
> "When comparing LLM feedback with comments from each individual reviewer, approximately one third (30.85%) of GPT-4 raised comments overlapped with comments from an individual reviewer (Fig. 2a). The degree of overlap between two human reviewers was similar (28.58%), after controlling for the number of comments (Methods)." (Liang et al., 2024, p. 3)
> ![[liangCanLargeLanguage2024a-evd-p3-3.png]]

### How?

> **Procedure:** (1) For each of 3,096 Nature-family papers (post-2022, to avoid GPT-4 training overlap), GPT-4 generated structured 4-section feedback in a single pass over the parsed PDF. (2) Stage 1 (extraction) — GPT-4 reads either the LLM or the human review and emits a JSON list of distinct critical points (`{ID: content}`); pipeline validated against 639 human-coded feedbacks with **F1 = 0.968 (precision 0.977, recall 0.960)** (Supp. Table 3a). (3) Stage 2 (matching) — GPT-4 receives both extracted JSON lists and emits matched ID pairs with a 5–10 similarity rating; only matches scored ≥ 7 are kept; pipeline validated on 760 sampled feedback pairs (332 GPT–human, 428 human–human) yielding **F1 = 0.824 (P = 0.777, R = 0.878)** on 12,035 comment pairs (Supp. Table 3b). IAA on 800 stratified pairs (3 annotators) gave **89.8% pairwise agreement, F1 = 0.887**. (4) Hit rate computed for GPT-4 vs each individual human reviewer; for the human-vs-human baseline, only the first N comments by reviewer A are used, where N = number of GPT-4 comments, controlling for set-size confound. (5) McNemar / paired comparisons reported with 95% CIs and *P < 0.0001 in Fig. 2a.
>
> "We developed a retrospective comment matching pipeline to evaluate the overlap between feedback from LLM and human reviewers. The pipeline first performs extractive text summarization to extract the comments from both LLM and human-written feedback. It then applies semantic text matching to identify shared comments between the two feedback sources. We validated the pipeline's accuracy through human verification, yielding an F1 score of 96.8% for extraction (Supp. Table 3a, Methods) and 82.4% for matching (Supp. Table 3b, Methods)." (Liang et al., 2024, p. 3)
> ![[liangCanLargeLanguage2024a-evd-p3-4.png]]

### Who?

> **Source data (sample-size flow):** Nature family journals → all papers published Jan 1, 2022 – Jun 17, 2023 with public reviewer reports → **3,096 accepted papers across 15 Nature family journals**, with **8,745 human reviewer comments** (Supp. Table 1: Nature 773 papers / 2,324 reviews, Nature Communications 810 / 2,250, plus 13 other Communications & Nature-branded journals). Mean paper length 12,444 tokens; mean human review 1,338 tokens (Supp. Table 4). All papers post-date the Sep 2021 GPT-4 training cutoff.
>
> **Pipeline-validation samples:** Stage 1 extraction validated on 639 randomly sampled feedbacks (150 LLM + 489 human), each independently double-coded by 2 co-authors. Stage 2 matching validated on 760 sampled feedback pairs (12,035 comment pairs), triple-coded by 3 co-authors; IAA computed on 800 stratified pairs (400 pipeline-matched + 400 not-matched).
>
> **No human study participants** (this EVD); the unit is the published comment.
>
> "The first dataset, sourced from Nature family journals, includes 8,745 comments from human reviewers for 3,096 accepted papers across 15 Nature family journals, including Nature, Nature Biomedical Engineering, Nature Human Behaviour, and Nature Communications (Supp. Table 1, Methods)." (Liang et al., 2024, p. 3)
> ![[liangCanLargeLanguage2024a-evd-p3-5.png]]

## Other Notes

- Results held across all four set-overlap metrics — Szymkiewicz–Simpson, Jaccard, Sørensen–Dice (Supp. Fig. 2) — and across journals (Fig. 2c, r = 0.80, P = 3.69×10⁻⁴ between GPT-4-vs-human and human-vs-human overlap across the 15 Nature journals).
- Replicated on ICLR: GPT-4 vs human = **39.23%**, human vs human = **35.25%**; ICLR-by-decision r = 0.98 (P = 3.28×10⁻³).
- Per-journal GPT-4-vs-human overlap ranged from **15.58% (Nature Communications Materials)** to **39.16% (Nature)**.
- Global hit rate (≥ 1 human reviewer matches a given GPT-4 comment) = 57.55% on Nature, 77.18% on ICLR (Supp. Fig. 1).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liangCanLargeLanguage2024a#TRIPOD-LLM reporting summary]].

| Comparison (Nature, n = 3,096 papers) | Hit rate | 95% CI / sig. |
| --- | :---: | :---: |
| **GPT-4 vs. individual human reviewer** | **30.85%** | ****P < 0.0001 vs. shuffle |
| Human vs. human (controlled for N comments) | 28.58% | comparable |
| GPT-4 (shuffled) vs. human (null model) | 1.13% (global) / 0.43% (pairwise) | sharp drop |

| Pipeline-validation metric | Value |
| --- | :---: |
| Extraction stage F1 (n = 639 feedbacks) | 0.968 (P = 0.977, R = 0.960) |
| Matching stage F1 (n = 12,035 pairs) | 0.824 (P = 0.777, R = 0.878) |
| IAA pairwise agreement (n = 800 pairs, 3 annotators) | 89.8% (F1 = 0.887) |

| Replication / robustness | Value |
| --- | :---: |
| ICLR GPT-4 vs. human | 39.23% |
| ICLR human vs. human | 35.25% |
| Per-journal range (Nature family) | 15.58% – 39.16% |
| Cross-journal correlation (GPT-vs-H, H-vs-H) | r = 0.80 (P = 3.69×10⁻⁴) |
| Cross-decision correlation (ICLR) | r = 0.98 (P = 3.28×10⁻³) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The Liang et al study used papers already accepted to journals which may not represent the full quality distribution]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

- [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]]

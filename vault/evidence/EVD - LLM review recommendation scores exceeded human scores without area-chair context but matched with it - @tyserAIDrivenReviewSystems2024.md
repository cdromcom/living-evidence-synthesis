---
NodeFormality: draft
aliases:
tags:
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
nodeID: 019ddb4e-6b78-77d7-8711-497e13fd138d
appraisal_overall: L0-M2-H3
tripod_llm_pct: 25pct
---

## Source

[[@tyserAIDrivenReviewSystems2024]]

## Description

> "The human reviewers have an average recommendation score of 5.88, with a standard deviation 1.61. With the context of the entire paper text and the conference review form (P1), the LLM has an average recommendation of 7.21, higher than the human reviewers... With the addition of the area chair guidelines for the area chair (P4), the recommendation score decreases to 4.61, indicating that this context makes the LLM more critical or stringent in its evaluations... P5 reaches the same level of recommendation as the human reviewers." (Tyser et al., 2024, p. 10 [Appendix D])
>
> ![[tyserAIDrivenReviewSystems2024-fig14-p10-1.png]]

## Methods Context

### What?

> **Study design:** prospective context-ablation study comparing GPT-4-generated reviews to human OpenReview reviews on the same papers, across 5 progressively augmented prompt contexts (P1–P5).
>
> **Method type:** within-paper score comparison; per-condition mean and standard deviation reported across 5 review dimensions.
>
> **Tools:** GPT-4 (used as the underlying reviewer LLM throughout the OpenReviewer pipeline); ICLR / NeurIPS conference review form, reviewer guide, code of ethics, code of conduct, area chair guidelines, and prior-year reviewer statistics as augmentation documents.
>
> **Dependent variables:** review subscores — Correctness, Technical Novelty & Significance, Empirical Novelty & Significance, **Overall Recommendation**, Confidence — each averaged across the corpus per condition (Figure 14).
>
> **Independent variable:** prompt context condition (Human, P1, P2, P3, P4, P5). Each Pₖ is a strict superset of Pₖ₋₁: P1 = paper text (P) + review form (RF); P2 adds reviewer guide (RG); P3 adds code of ethics (CE) + code of conduct (CC); P4 adds area chair guidelines (AC); P5 adds prior-year statistics (S).
>
> "Figure 14 shows the average and standard deviation scores of the human reviewers and LLM review for paper correctness, technical novelty and significance, empirical novelty and significance, overall recommendation score, and confidence. P1, P2, P3, P4, P5 ablate the increasing documents used in the GPT-4 context prompt." (Tyser et al., 2024, p. 10)
> ![[tyserAIDrivenReviewSystems2024-evd-p13-1.png]]

### How?

> **Procedure:** (1) for each open-access ICLR/NeurIPS paper, retrieve the human OpenReview reviews and parse out the 5 standardized subscores. (2) Generate GPT-4 reviews under each of P1–P5, conditioning the model on (paper text) + (the cumulative document set for that condition). (3) Parse each GPT-4 review for the same 5 subscores. (4) Compute mean ± SD per (reviewer, dimension) cell and plot Figure 14. (5) Compare LLM means against the human distribution descriptively. The authors also compare the full distribution shapes (Figures 30–31, Appendix L) and find P5 distributions resemble human distributions on Correctness / Technical / Empirical Novelty but skew higher on Confidence.
>
> "We use multiple documents related to the review as LLM context: the previous year's statistics, reviewer and area chair guidelines, code of ethics and code of conduct, and the formal review form. These venue-dependent documents result in our review score distributions being similar to human distributions and yielding quality reviews using the full range of scores; however, they require yearly updates." (Tyser et al., 2024, p. 6)
> ![[tyserAIDrivenReviewSystems2024-evd-p7-1.png]]

### Who?

> **Reviewer model:** GPT-4 (specific snapshot date not reported in this section; the Reviewer Arena passage names "GPT-4 Turbo (Turbo-2024-04-09)" but the ablation in Figure 14 / Appendix D simply says "GPT-4").
>
> **Human comparator:** OpenReview reviewers of the same ICLR / NeurIPS papers.
>
> **Paper sample (sample-size flow):** source pool — ICLR 2024 (7,404), ICLR 2023 (4,955), NeurIPS 2023 (12,345), NeurIPS 2022 (10,411) (Table 3, Appendix B). The Appendix-D analysis aggregates "ICLR/NeurIPS papers" but does not report the exact N analyzed per condition for the recommendation-score ablation; only means and SDs are shown in Figure 14.
>
> **Conditions (5):** P1 = P + RF; P2 = RG + P + RF; P3 = RG + CE + CC + P + RF; P4 = AC + RG + CE + CC + P + RF; P5 = S + AC + RG + CE + CC + P + RF.
>
> "We modify the papers by introducing errors or shortcomings, the LLM reviews the original and modified papers." (Tyser et al., 2024, p. 6)
> ![[tyserAIDrivenReviewSystems2024-evd-p6-1.png]]

## Other Notes

- The directional finding is non-monotonic: P1 → P2 → P3 trend slightly **upward** (7.21 → 7.58 → 7.62); only **adding the area-chair guidelines (P4)** drops the score below human (4.61), and **adding prior-year statistics (P5)** brings it back to ≈ human (5.36). This means the "match" depends critically on giving the LLM both (a) area-chair-style stringency and (b) base-rate calibration.
- SD also tracks context: human SD = 1.61; P1 SD = 1.03 (over-confident); P5 SD increases (more variability), better matching the human distribution.
- Authors flag that LLM Confidence scores (Figure 31) are skewed higher than human Confidence even at P5 — calibration of the Confidence dimension is not solved by P5.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@tyserAIDrivenReviewSystems2024#TRIPOD-LLM reporting summary]].

| Reviewer / context | Mean recommendation | SD | Direction vs. human |
| --- | :---: | :---: | --- |
| **Human** | **5.88** | **1.61** | (reference) |
| LLM P1 (P + RF) | 7.21 | 1.03 | +1.33 (over) |
| LLM P2 (+ RG) | 7.58 | — | +1.70 (over) |
| LLM P3 (+ CE + CC) | 7.62 | — | +1.74 (over) |
| LLM P4 (+ AC) | 4.61 | — | −1.27 (under, more stringent) |
| **LLM P5 (+ S)** | **5.36** | — | **−0.52 (≈ human)** |

| Other dimensions (P5 vs. human, qualitative — Figs. 30–31) | Result |
| --- | --- |
| Correctness | Similar mean and shape |
| Technical / Empirical Novelty & Significance | Similar mean and shape |
| Confidence | LLM skewed higher than human |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]]

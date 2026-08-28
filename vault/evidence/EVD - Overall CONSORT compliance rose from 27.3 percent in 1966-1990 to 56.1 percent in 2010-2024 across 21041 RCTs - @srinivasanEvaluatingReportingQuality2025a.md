---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/50pct
  - 5c/clarity
  - forensic/ci-check/consistent
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b83-7219-98f4-b40a6fb82d6b
appraisal_overall: L0-M3-H2
tripod_llm_pct: 50pct
---

## Source

[[@srinivasanEvaluatingReportingQuality2025a]]

## Description

> "The mean compliance rate increased from 27.3% (95% CI: 27.0-27.6%) in 1966-1990 to 33.9% (95% CI: 33.5-34.3%) in 1990-2000, representing a 24.3% relative increase (p < 0.0001). This upward trend continued with reporting rates rising to 45.0% (95% CI: 44.7-45.3%) in 2000-2010, a 32.7% increase from the previous decade (p < 0.0001). The most recent period (2010-2024) showed further improvement to 56.1% (95% CI: 56.0-56.3%), a 24.7% increase (p < 0.0001)." (Srinivasan et al., 2025, p. 6)
>
> ![[srinivasanEvaluatingReportingQuality2025a-fig2-p6-1.png]]

## Methods Context

### What?

> **Study design:** large-scale cross-sectional + temporal-trend analysis of CONSORT reporting compliance across nearly six decades of open-access RCTs.
>
> **Method type:** zero-shot LLM-based per-criterion classification, then aggregated to mean compliance per article and averaged across four publication periods.
>
> **Tools:** GPT-4o-mini (OpenAI) on Azure PHI-compliant instance; PyMuPDF (PDF→XML); Semantic Scholar metadata enrichment; Python 3.8 with scipy.stats and statsmodels for chi-square tests and Cramer's V effect sizes; 95% confidence intervals for mean compliance per period.
>
> **Dependent variable:** mean proportion of CONSORT items reported per article.
>
> **Independent variable:** publication period (1966–1990 / 1990–2000 / 2000–2010 / 2010–2024).
>
> "Statistical significance was evaluated using chi-square tests for categorical comparisons and Pearson correlation for continuous relationships, with effect sizes calculated using Cramer's V. All analyses were performed using Python 3.8 with scipy.stats and statsmodels packages." (Srinivasan et al., 2025, p. 5)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p5-1.png]]

### How?

> **Procedure:** (1) Identify 53,137 open-access human RCTs from PubMed (1966–2024); successfully convert 21,041 full-text PDFs to XML via PyMuPDF; enrich with Semantic Scholar metadata. (2) For each article, prompt GPT-4o-mini independently per CONSORT criterion (zero-shot, JSON output {is_met, rationale, confidence}). (3) Restrict to high-confidence predictions (>90% of articles retained). (4) Compute per-article compliance = fraction of criteria marked MET. (5) Bin articles by publication period; compute mean compliance per period with 95% CI; test pairwise period-to-period differences with chi-square; report relative-percentage change between consecutive periods.
>
> "We observed substantial improvement in CONSORT reporting rates over time (Fig. 2B). The mean compliance rate increased from 27.3% (95% CI: 27.0-27.6%) in 1966-1990 to 33.9% (95% CI: 33.5-34.3%) in 1990-2000, representing a 24.3% relative increase (p < 0.0001)." (Srinivasan et al., 2025, p. 6)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p6-1.png]]

### Who?

> **Articles (sample-size flow):** 53,137 open-access human RCTs identified from PubMed (1966–2024) → 21,041 full-text PDFs successfully obtained and converted → 21,041 evaluated by GPT-4o-mini → high-confidence subset (>90% of articles) used for trend analysis. Period buckets: 1966–1990 (n=2,771); 1990–2000 (n=1,969); 2000–2010 (n=3,765); 2010–2024 (n=10,447).
>
> **No human evaluators** in this large-scale temporal-trend computation (the 50-article human validation sub-study sits upstream of model selection).
>
> "For large-scale analysis, we identified 53,137 open-access human RCTs from PubMed (1966-2024) and successfully obtained 21,041 full-text PDFs. Articles spanned four time periods: 1966-1990 (n = 2, 771), 1990-2000 (n = 1, 969), 2000-2010 (n = 3, 765), and 2010-2024 (n = 10, 447)." (Srinivasan et al., 2025, p. 3)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p3-3.png]]

## Other Notes

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@srinivasanEvaluatingReportingQuality2025a#TRIPOD-LLM reporting summary]].

| Period | n | Mean compliance (95% CI) | Relative change vs. prior period | p-value |
| --- | :---: | :---: | :---: | :---: |
| 1966–1990 | 2,771 | **27.3%** (27.0–27.6) | — | — |
| 1990–2000 | 1,969 | **33.9%** (33.5–34.3) | +24.3% | <0.0001 |
| 2000–2010 | 3,765 | **45.0%** (44.7–45.3) | +32.7% | <0.0001 |
| 2010–2024 | 10,447 | **56.1%** (56.0–56.3) | +24.7% | <0.0001 |

| Note | Value |
| --- | --- |
| Even in 2010–2024, mean compliance | <60% (persistent gap despite improvement) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - CONSORT analysis restricted to open-access articles and assessed presence not accuracy of reporting elements]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]

- [[CLM - RCT reporting quality has improved substantially over decades but critical methodological gaps persist across all disciplines]]

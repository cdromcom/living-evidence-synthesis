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
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b57-768e-af9b-1286eff09e0b
appraisal_overall: L0-M3-H2
tripod_llm_pct: 50pct
---

## Source

[[@srinivasanEvaluatingReportingQuality2025a]]

## Description

> "Urology/nephrology had the highest proportion of items met over the full-time interval measured, with 63.35% of criteria reported, followed by critical care at 62.27% and Gastroenterology/hepatology at 60.28%. On the lower end of the spectrum, Pharmacology had the lowest reporting rates, with only 35.16% of items met, followed by Radiology (40.46%)." (Srinivasan et al., 2025, p. 6)
>
> ![[srinivasanEvaluatingReportingQuality2025a-fig2C-p6-1.png]]

## Methods Context

### What?

> **Study design:** large-scale cross-sectional analysis of CONSORT reporting compliance stratified by medical discipline.
>
> **Method type:** automated, zero-shot LLM-based assessment of each RCT against the 25-item CONSORT checklist (21 items retained after excluding items the model could not reliably assess).
>
> **Tools:** GPT-4o-mini (OpenAI) deployed on a HIPAA-compliant Azure instance; PyMuPDF for PDF→XML conversion; Semantic Scholar for metadata enrichment; Scimago journal classification for discipline mapping; chi-square tests with Cramer's V effect sizes (Python 3.8, scipy.stats, statsmodels).
>
> **Dependent variable:** mean proportion of CONSORT items reported per article, aggregated by discipline.
>
> **Independent variable / covariate:** medical discipline (Scimago journal category).
>
> "We applied our best-performing model to assess CONSORT compliance across 21,041 RCTs. We conducted temporal trend analysis across four publication periods, disciplinary analysis by mapping journals to Scimago categories, and relationships with trial characteristics from ClinicalTrials.gov data." (Srinivasan et al., 2025, p. 4)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p4-1.png]]

### How?

> **Procedure:** (1) Each open-access RCT PDF was converted to XML via PyMuPDF and enriched with Semantic Scholar metadata. (2) For each article, GPT-4o-mini was prompted independently for each of 25 CONSORT criteria (later restricted to 21 after removing items 2a Background, 7b interim analyses, 3b protocol changes, 6b changes to outcomes, 14b reasons for termination — items the model misclassified as "not applicable" too often or that were reported in <5% of articles). The prompt template was: "Your task is to assess whether the given article meets the specified CONSORT criteria. # Article {article} # CONSORT Criterion The criterion being assessed is: {criterion} {definition}". The model returned JSON with {is_met, rationale, confidence}. (3) Only high-confidence predictions were retained for downstream analysis (>90% of articles). (4) Articles were mapped to Scimago discipline categories by journal; mean CONSORT compliance computed per discipline across the full 1966–2024 interval; significance tested with chi-square (effect size Cramer's V).
>
> "We applied our most efficient and best performing model to 21,041 open access NCBI articles published between 1966-2024 to evaluate the quality of RCT reporting over time. For each article, the model was tasked with independently assessing each criterion. This required re-prompting the model for every criterion, ensuring that each article was evaluated multiple times—once for each criterion." (Srinivasan et al., 2025, p. 4)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p4-2.png]]

### Who?

> **Articles (sample-size flow):** 53,137 open-access human RCTs identified from PubMed (1966–2024) → 21,041 full-text PDFs successfully obtained and converted → all 21,041 evaluated by GPT-4o-mini → high-confidence predictions retained (>90% of articles) → mapped to Scimago discipline categories. Discipline buckets reported include urology/nephrology, critical care, gastroenterology/hepatology, …, radiology, and pharmacology.
>
> **No human evaluators** in this disciplinary aggregation step (the 50-article human validation sub-study covers a separate sample).
>
> "For large-scale analysis, we identified 53,137 open-access human RCTs from PubMed (1966-2024) and successfully obtained 21,041 full-text PDFs. Articles spanned four time periods: 1966-1990 (n = 2, 771), 1990-2000 (n = 1, 969), 2000-2010 (n = 3, 765), and 2010-2024 (n = 10, 447)." (Srinivasan et al., 2025, p. 3)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p3-1.png]]

## Other Notes

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@srinivasanEvaluatingReportingQuality2025a#TRIPOD-LLM reporting summary]].

| Discipline | Mean % CONSORT items reported |
| --- | :---: |
| **Urology / nephrology** | **63.35%** (highest) |
| Critical care | 62.27% |
| Gastroenterology / hepatology | 60.28% |
| ... | (intermediate disciplines per Fig. 2C) |
| Radiology | 40.46% |
| **Pharmacology** | **35.16%** (lowest) |
| Disciplinary range | 35.16% – 63.35% (~28 percentage-point spread) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]

- [[CLM - RCT reporting quality has improved substantially over decades but critical methodological gaps persist across all disciplines]]

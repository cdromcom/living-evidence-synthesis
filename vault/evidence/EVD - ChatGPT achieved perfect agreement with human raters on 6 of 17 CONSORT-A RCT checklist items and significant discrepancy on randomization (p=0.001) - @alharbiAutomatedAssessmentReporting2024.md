---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M1-H4
  - tripod-llm/compliance/low
  - tripod-llm/proportion/30pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b59-7695-aedc-ea8f898d19d6
appraisal_overall: L0-M1-H4
tripod_llm_pct: 30pct
---

## Source

[[@alharbiAutomatedAssessmentReporting2024]]

## Description

> "The human raters and ChatGPT achieved perfect agreement in their assessment of the six checklist items (title identification, author details, trial design, intended intervention for each group, objectives, and conclusions). Near-complete agreement was observed for four additional items (eligibility criteria, clearly defined outcomes, outcome results for each group, and funding information). The alignment between human and ChatGPT ratings was lower for the remaining seven items, with statistically significant discrepancies identified for two items: randomization and recruitment details." (Alharbi & Asiri, 2024, p. 4)
>
> ![[alharbi2024-table1-p4-1.png]]
> ![[alharbi2024-table1cont-p5-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational study comparing ChatGPT and human reviewer ratings of reporting completeness in published RCT abstracts.
>
> **Method type:** zero-/few-shot LLM rating with chain-of-thought prompting; benchmarked against duplicate independent human reviewers.
>
> **Tools:** GPT-3.5 (OpenAI free chat interface, accessed 30 May 2024); CONSORT for Abstracts (CONSORT-A) 17-item checklist; custom Excel data-collection spreadsheet; R v2.4.6.26 (with `gtsummary`) for statistical analysis.
>
> **Dependent variables:** per-item dichotomous rating (Yes / No / NA) for each of 17 CONSORT-A items, summarized as proportion "Reported" per rater group.
>
> **Independent variable:** rater identity (ChatGPT vs. human consensus); checklist item.
>
> "This study evaluated the usability of Large Language Models (LLMs), specifically ChatGPT, in assessing the completeness of reporting in orthodontic research abstracts. We focused on two key areas: randomized controlled trials (RCTs) and systematic reviews, using the CONSORT-A and PRISMA guidelines for evaluation." (Alharbi & Asiri, 2024, p. 1)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p1-1.png]]

### How?

> **Procedure:** (1) Two independent human reviewers (F.A. and S.A.) scored each of 20 RCT abstracts in duplicate against the full 17-item CONSORT-A checklist, consulting full CONSORT guidelines and explanations; disagreements resolved by discussion to consensus; items marked NA when study design precluded reporting (e.g., blinding in untreated-control trials). Per-abstract score = (Yes items / [19 − NA items]) × 100. (2) For ChatGPT, a single researcher (F.A.) pasted each abstract into ChatGPT 3.5 on 30 May 2024 using a system prompt that introduced GPT-3.5 as an "expert in clinical trial design" (in-context expert impersonation) and asked it to first list all CONSORT-A items, then rate each via chain-of-thought prompting in three steps within a single prompt: (a) extract supporting quotes from the abstract, (b) explain the rationale, (c) assign a bracketed [Yes] / [No] / [NA] rating. Major deviations (missing ratings, hallucinations) triggered ≥3 prompt repetitions; minor deviations (labeling/wording) corrected by single manual intervention. (3) Per-item Fisher's exact test compared ChatGPT vs. human "Reported" proportions.
>
> "To ensure the quality of the LLM output, we employed chain-of-thought prompting in the final user prompt [33]. This technique requires LLMs to perform three consecutive steps for each item on the reporting checklist. First, the model had to identify and extract relevant quotes from a full-text publication that directly addressed a specific item. Second, it was necessary to explain the rationale behind the chosen quotes and how they supported their assessment. Finally, the model assigned a bracketed rating for each item: '[Yes]' if reported, '[No]' if not reported, or '[NA]' if not applicable owing to the study design (e.g., blinding not possible or no meta-analysis conducted)." (Alharbi & Asiri, 2024, p. 3)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p3-3.png]]

### Who?

> **Sample-size flow:** four leading orthodontic journals searched (AJO-DO, JO, EJO, AO) for publications 2018–2022 containing keywords "systematic review", "meta-analysis", "randomized controlled trial", "assigned", "prospective", or "comparative" in title/abstract → full-text screened to confirm true RCT/SR designation → random sample of **20 RCT abstracts** (5 per journal) selected for analysis (parallel sample of 20 systematic reviews handled in companion EVD). All 20 RCTs analyzed; no exclusions reported after sampling.
>
> **Models:** ChatGPT 3.5 (OpenAI, free version, accessed 30 May 2024), single LLM, no model comparison.
>
> **Human raters:** two reviewers F.A. and S.A. (authors), both Department of Pediatric Dentistry, Prince Sattam Bin Abdulaziz University.
>
> "This cross-sectional observational study investigated the quality of reporting in abstracts of randomized controlled trials (RCTs) and systematic reviews published in four leading orthodontic journals: (1) American Journal of Orthodontics and Dentofacial Orthopedics (AJO-DO), (2) Journal of Orthodontics (JO), (3) European Journal of Orthodontics (EJO), and (4) The Angle Orthodontist (AO). The timeframe included publications published between 2018 and 2022. … Following the initial search, a random sample of 20 RCTs and 20 systematic reviews was selected for further analysis. This resulted in a balanced representation, with each of the four journals contributing five publications on RCTs and five publications on systematic reviews." (Alharbi & Asiri, 2024, p. 2)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p2-2.png]]

## Other Notes

- Item 8 (randomization): ChatGPT reported 100% (20/20) of abstracts as reporting randomization details; humans rated only 55% (11/20) as reporting (p=0.001).
- Item 11 (recruitment status): ChatGPT reported 100% (20/20) as reporting; humans rated 0% (0/20) as applicable, humans flagged all 20 as NA (p<0.001). This is a systematic misclassification of the NA category, not a borderline disagreement.
- ChatGPT systematically over-reports: in 14 of 17 items, ChatGPT's "Reported" proportion ≥ humans'.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@alharbiAutomatedAssessmentReporting2024#TRIPOD-LLM reporting]].

| CONSORT-A item | ChatGPT Reported | Human Reported | Fisher p |
| --- | :---: | :---: | :---: |
| 1. Title (randomized) | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 2. Author details | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 3. Trial design | 20/20 (100%) | 16/20 (80%) | 0.11 |
| 4. Eligibility criteria | 20/20 (100%) | 19/20 (95%) | >0.9 |
| 5. Interventions per group | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 6. Objective | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 7. Outcome clearly defined | 20/20 (100%) | 16/20 (80%) | 0.11 |
| **8. Randomization** | **20/20 (100%)** | **11/20 (55%)** | **0.001** |
| 9. Blinding | 8/20 (40%) | 9/20 (45%) | 0.7 |
| 10. N randomized per group | 16/20 (80%) | 14/20 (70%) | 0.5 |
| **11. Recruitment status / period** | **20/20 (100%)** | **0/20 (0%); 20/20 NA** | **<0.001** |
| 12. N analyzed per group | 15/20 (75%) | 11/20 (55%) | 0.2 |
| 13. Outcome results + effect size | 20/20 (100%) | 19/20 (95%) | >0.9 |
| 14. Harms | 8/20 (40%) | 3/20 (15%) | 0.082 |
| 15. Conclusions | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 16. Trial registration | 9/20 (45%) | 11/20 (55%) | 0.5 |
| 17. Funding | 4/20 (20%) | 3/20 (15%) | >0.9 |

| Summary statistic | Value |
| --- | --- |
| Items with perfect agreement (both 100%) | 6 / 17 |
| Items with statistically significant discrepancy (p<0.05) | 2 / 17 (items 8, 11) |
| Direction of bias | ChatGPT systematically over-reports vs. humans |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Only a single LLM version was tested via free chat GUI rather than API limiting reproducibility and prompt control]]

- [[CVT - The small sample of 20 RCTs and 20 systematic reviews limited statistical power to detect differences in checklist item performance]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]

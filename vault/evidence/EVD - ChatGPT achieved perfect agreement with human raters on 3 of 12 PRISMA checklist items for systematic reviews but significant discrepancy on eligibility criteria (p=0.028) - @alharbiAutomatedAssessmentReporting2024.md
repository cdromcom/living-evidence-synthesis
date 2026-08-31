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
nodeID: 019ddb4e-6b58-7133-b144-e7a33cd92a2d
appraisal_overall: L0-M1-H4
tripod_llm_pct: 30pct
---

## Source

[[@alharbiAutomatedAssessmentReporting2024]]

## Description

> "The human and ChatGPT ratings achieved perfect agreement for three items: identifying the report as a systematic review, objectives, and interpretation. Near-complete agreement was observed for information sources, the included studies, synthesis of results, and limitations of the evidence. The alignment scores were lower for the remaining five items, with a statistically significant discrepancy identified for the eligibility criteria." (Alharbi & Asiri, 2024, p. 6)
>
> ![[alharbi2024-table2-p6-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational study comparing ChatGPT and human reviewer ratings of reporting completeness in published systematic-review (SR) abstracts.
>
> **Method type:** zero-/few-shot LLM rating with chain-of-thought prompting; benchmarked against duplicate independent human reviewers.
>
> **Tools:** GPT-3.5 (OpenAI free chat interface, accessed 30 May 2024); PRISMA-aligned 12-item abstract checklist; custom Excel data-collection spreadsheet; R v2.4.6.26 (with `gtsummary`) for statistical analysis.
>
> **Dependent variables:** per-item dichotomous rating (Yes / No / NA) for each of 12 PRISMA items, summarized as proportion "Reported" per rater group.
>
> **Independent variable:** rater identity (ChatGPT vs. human consensus); checklist item.
>
> "Similar to the RCT abstracts, two independent reviewers (F.A. and S.A.) evaluated the reporting quality of the systematic review abstracts in duplicate using a checklist aligned with the PRISMA guidelines for abstract reporting. The reviewers consulted the full PRISMA guidelines and provided explanations during the assessment." (Alharbi & Asiri, 2024, p. 3)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p3-1.png]]

### How?

> **Procedure:** (1) Two independent human reviewers (F.A. and S.A.) scored each of 20 SR abstracts in duplicate against a 12-item PRISMA-for-abstracts checklist, consulting full PRISMA guidelines; items marked NA when review design precluded reporting (e.g., no meta-analysis conducted); disagreements resolved by discussion to consensus. Per-abstract score = (Yes items / [12 − NA items]) × 100. (2) For ChatGPT, the same researcher (F.A.) pasted each abstract into ChatGPT 3.5 on 30 May 2024 using a system prompt that introduced GPT-3.5 as an "expert in systematic reviews" (in-context expert impersonation) and asked it to first list all PRISMA items, then rate each via chain-of-thought prompting in three steps within a single prompt: (a) extract supporting quotes, (b) explain the rationale, (c) assign a bracketed [Yes] / [No] / [NA] rating. Major deviations (missing ratings, hallucinations) triggered ≥3 prompt repetitions; minor deviations corrected by single manual intervention. (3) Per-item Fisher's exact test compared ChatGPT vs. human "Reported" proportions.
>
> "This study utilized the large language model GPT-3.5 (OpenAI, San Francisco, CA, USA), which is currently offered at no cost. We employed a common prompt engineering strategy known as in-context expert impersonation to enhance model performance. System prompts were initiated by introducing GPT-3.5 as an 'expert in systematic reviews' for PRISMA guidelines and an 'expert in clinical trial design' for CONSORT-A guidelines [33,34]." (Alharbi & Asiri, 2024, p. 3)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p3-2.png]]

### Who?

> **Sample-size flow:** four leading orthodontic journals searched (AJO-DO, JO, EJO, AO) for publications 2018–2022 containing keywords "systematic review", "meta-analysis", "randomized controlled trial", "assigned", "prospective", or "comparative" → full-text screened to confirm true SR designation → random sample of **20 systematic-review abstracts** (5 per journal) selected for analysis (parallel sample of 20 RCTs in companion EVD). All 20 SRs analyzed; no exclusions reported after sampling.
>
> **Models:** ChatGPT 3.5 (OpenAI, free version, accessed 30 May 2024) — single LLM, no model comparison.
>
> **Human raters:** two reviewers F.A. and S.A. (authors), both Department of Pediatric Dentistry, Prince Sattam Bin Abdulaziz University.
>
> "Following the initial search, a random sample of 20 RCTs and 20 systematic reviews was selected for further analysis. This resulted in a balanced representation, with each of the four journals contributing five publications on RCTs and five publications on systematic reviews." (Alharbi & Asiri, 2024, p. 2)
> ![[alharbiAutomatedAssessmentReporting2024-evd-p2-1.png]]

## Other Notes

- Eligibility criteria (item 3): ChatGPT reported 90% (18/20) as reporting eligibility criteria; humans rated only 60% (12/20) as reporting (p=0.028) — the only PRISMA item with a statistically significant discrepancy.
- ChatGPT showed a systematic tendency to over-report: in 9 of 12 PRISMA items, ChatGPT's "Reported" proportion ≥ humans', suggesting it may over-interpret implicit information in abstracts.
- Funding (item 11): ChatGPT 30% (6/20) vs. humans 5% (1/20), p=0.091 — borderline non-significant but a 6-fold disagreement on a checkable factual item.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@alharbiAutomatedAssessmentReporting2024#TRIPOD-LLM reporting summary]].

| PRISMA-for-abstracts item | ChatGPT Reported | Human Reported | Fisher p |
| --- | :---: | :---: | :---: |
| 1. Identify as systematic review | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 2. Objectives | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| **3. Eligibility criteria** | **18/20 (90%)** | **12/20 (60%)** | **0.028** |
| 4. Information sources | 20/20 (100%) | 16/20 (80%) | 0.11 |
| 5. Risk of bias | 15/20 (75%) | 15/20 (75%) | >0.9 |
| 6. Methods of synthesis | 17/20 (85%) | 13/20 (65%) | 0.14 |
| 7. Included studies | 20/20 (100%) | 19/20 (95%) | >0.9 |
| 8. Synthesis of results | 18/20 (90%) | 14/20 (70%) | 0.2 |
| 9. Limitation of evidence | 17/20 (85%) | 17/20 (85%) | >0.9 |
| 10. Interpretation | 20/20 (100%) | 20/20 (100%) | — (perfect) |
| 11. Funding | 6/20 (30%) | 1/20 (5%) | 0.091 |
| 12. Registration | 9/20 (45%) | 8/20 (40%) | 0.7 |

| Summary statistic | Value |
| --- | --- |
| Items with perfect agreement (both 100%) | 3 / 12 |
| Items with statistically significant discrepancy (p<0.05) | 1 / 12 (item 3) |
| Direction of bias | ChatGPT systematically over-reports vs. humans |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]

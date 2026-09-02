---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/ethics-irb-review
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/23pct
  - 5c/care
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b86-7207-8c7a-d917754579f2
appraisal_overall: L0-M2-H3
tripod_llm_pct: 23pct
---

## Source

[[@sridharanAssessingDecisionMakingCapabilities2024]]

## Description

> "The trio of AI platforms successfully responded to queries from all case studies, as detailed in Electronic Supplementary Material 3. Their outputs were generally consistent and insightful, covering a range of topics such as identifying GCP issues, suggesting corrective actions for GCP violations, pinpointing IRB shortcomings and their resolutions, issues with IRB SOPs, COIs within IRBs, concerns over undue inducements in participant recruitment, criticisms of the study design and participant selection, addressing participant vulnerability, reporting SAEs, and determining eligibility for expedited review processes." (Sridharan & Sivaramakrishnan, 2024, p. 85)
>
> ![[sridharanAssessingDecisionMakingCapabilities2024-table1-p6-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational study evaluating LLMs as IRB members.
>
> **Method type:** qualitative comparative assessment of free-text LLM responses against gold-standard ethics references; two independent reviewers.
>
> **Tools:** three AI platforms (Poe Assistant, ChatGPT [GPT-3.5], Google Bard); FERCAP/SIDCER Handbook of Case Studies on Ethical Issues in Health Research as the case-study source and partial gold standard; ICH E6 GCP guidelines as the second gold standard.
>
> **Dependent variable(s):** binary "stated / not stated" coding of whether each AI platform addressed each ethical sub-issue in each case study (per Table 1 domains, e.g., reporting of an event, suggesting expedited review, identifying drug definition, quantifying participant risk).
>
> **Independent variable(s) / covariates:** AI platform (3 levels); case study (10 levels: Role of REC; Emergency Room Research; Scientific Soundness; COI; Healthy Volunteers; Observational Study; Behavioral Research; Traditional Medicine; Recruitment & Informed Consent; Post-Trial Access).
>
> "The present work represents a cross-sectional, observational study that was carried out during September to November 2023." (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-5.png]]

### How?

> **Procedure:** (1) Obtain permission from FERCAP and SIDCER to use the 10 prevalidated case studies from the FERCAP/SIDCER handbook. (2) Prompt each of the three AI platforms (Poe Assistant, ChatGPT, Google Bard) with open-ended questions from each case study during September–November 2023; full case-study details are in Electronic Supplementary Material 1. (3) Two authors independently assessed each AI output and verified veracity against the FERCAP/SIDCER handbook and the ICH E6 GCP guidelines. (4) Disagreements resolved by discussion; sub-issues each platform missed are tabulated in Table 1 with explanatory comments grounded in GCP. No quantitative scoring rubric, statistical test, or inter-rater agreement metric is reported.
>
> "The AI platforms were prompted with ten case studies with open-ended questions from the FERCAP/SIDCER Handbook of Case Studies on Ethical Issues in Health Research (FERCAP/SIDCER, 2012), after approval had been obtained from the Forum for Ethical Review Committees in the Asian and Western Pacific Region (FERCAP) and the Strategic Initiative for Developing Capacity in Ethical Review (SIDCER)." (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-6.png]]

### Who?

> **Models / participants:** three AI platforms, Poe Assistant, ChatGPT (GPT-3.5 architecture, OpenAI), and Google Bard. No human participants; the units of analysis are AI responses to case-study prompts.
>
> **Sample-size flow:** 10 case studies sourced from FERCAP/SIDCER handbook → all 10 administered to each of 3 platforms → 30 platform × case-study response sets analyzed. No exclusions reported. The two assessors are the two paper authors (KS, GS).
>
> "Two authors independently assessed the AI outputs, and the veracity was verified using the FERCAP/SIDCER handbook and the ICH E6 GCP guidelines (FERCAP/SIDCER Handbook, 2012; ICH E6, 2023)." (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-7.png]]

## Other Notes

- "Successfully responded to queries from all case studies" means all platforms produced an on-topic answer for every case, not that every answer was correct. Table 1 documents 9 distinct domains where at least one platform missed a GCP-relevant sub-issue, and Case Study 10 (post-trial access) was missed by all three.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanAssessingDecisionMakingCapabilities2024#TRIPOD-LLM reporting summary]].

| Outcome | Value |
| --- | --- |
| Case studies administered | 10 / 10 (per platform) |
| Platform × case responses produced | 30 / 30 |
| Platforms producing on-topic responses to all 10 cases | 3 / 3 (Poe Assistant, ChatGPT, Google Bard) |
| Domains where ≥1 platform missed a GCP sub-issue (Table 1) | 9 |
| Cases where all 3 platforms failed (post-trial access) | 1 / 10 (Case Study 10) |
| Quantitative accuracy / scoring rubric | None reported (qualitative "stated / not stated" coding only) |
| Inter-rater agreement | Not reported |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Study used only three AI platforms evaluated on ten case studies limiting generalizability of IRB capability findings]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
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
nodeID: 019ddb4e-6b54-76d0-8a9d-827afe19f5a2
appraisal_overall: L0-M2-H3
tripod_llm_pct: 23pct
---

## Source

[[@sridharanAssessingDecisionMakingCapabilities2024]]

## Description

> "Significantly, all platforms fell short in explaining why post-trial access to herbal medicine was not provided in case study 10, particularly since the medicinal product's benefits had not been established." (Sridharan & Sivaramakrishnan, 2024, p. 85)
>
> ![[sridharanAssessingDecisionMakingCapabilities2024-table1-p6-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational LLM evaluation — failure-mode analysis of a single case study (Case Study 10: Post-Trial Access) within the broader 10-case Sridharan & Sivaramakrishnan benchmark.
>
> **Method type:** qualitative comparative assessment of free-text LLM responses by two independent reviewers against the FERCAP/SIDCER handbook + ICH E6 GCP guidelines.
>
> **Tools:** Poe Assistant, ChatGPT (GPT-3.5), Google Bard; FERCAP/SIDCER Case Study 10 (Post-Trial Access — herbal medicine scenario).
>
> **Dependent variable(s):** binary "addressed / failed to address" the specific GCP rationale that post-trial access need not be provided when product benefits are unestablished.
>
> **Independent variable(s) / covariates:** AI platform (3 levels).
>
> "An observational study was conducted using three AI platforms in 10 case studies reflecting IRB functions, focusing on creating SOPs. The accuracy of the AI outputs was assessed against good clinical practice (GCP) guidelines." (Sridharan & Sivaramakrishnan, 2024, p. 83)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p1-1.png]]

### How?

> **Procedure:** each of the three AI platforms was prompted with the open-ended question(s) attached to FERCAP/SIDCER Case Study 10 (post-trial access to a herbal medicine whose benefits were not established). Two authors independently read each AI response, then verified against the FERCAP/SIDCER handbook and ICH E6 GCP guidelines whether the response correctly explained that post-trial access need not be guaranteed when the investigational product's benefit is unestablished. Disagreements between assessors resolved by discussion. The negative finding (all three platforms missed this rationale) was flagged narratively in the Results — no quantitative scoring or significance test was applied.
>
> "Significantly, all platforms fell short in explaining why post-trial access to herbal medicine was not provided in case study 10, particularly since the medicinal product's benefits had not been established." (Sridharan & Sivaramakrishnan, 2024, p. 85)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p3-2.png]]

### Who?

> **Models / participants:** three AI platforms — Poe Assistant, ChatGPT (GPT-3.5), Google Bard. No human participants.
>
> **Sample-size flow:** 1 case study (Case Study 10 of 10) → administered to all 3 platforms → 3 platform-responses analyzed; all 3 failed → 0 / 3 correct. Two human assessors (the two authors) reviewed all responses.
>
> "The AI platforms were prompted with ten case studies with open-ended questions from the FERCAP/SIDCER Handbook of Case Studies on Ethical Issues in Health Research (FERCAP/SIDCER, 2012)" (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-3.png]]

## Other Notes

- The handbook's expected answer hinges on a GCP principle: the Declaration of Helsinki / ICH E6 obligation to provide post-trial access applies when the intervention has been shown beneficial; for an unestablished herbal medicine, the obligation does not attach. None of the three LLMs surfaced that conditional logic.
- This is the only case (of 10) on which all three platforms failed simultaneously, making it the most-cited failure mode in the paper's discussion.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanAssessingDecisionMakingCapabilities2024#TRIPOD-LLM reporting summary]].

| Platform | Addressed unestablished-benefit rationale? |
| --- | :---: |
| Poe Assistant | No |
| ChatGPT (GPT-3.5) | No |
| Google Bard | No |
| **Aggregate** | **0 / 3 platforms correct** |
| Cases (of 10) where all 3 platforms failed | 1 (Case Study 10 only) |
| Inter-rater agreement | Not reported |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

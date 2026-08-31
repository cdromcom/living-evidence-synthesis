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
  - tripod-llm/proportion/35pct
  - 5c/care
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b55-768b-a2fe-e3234fa385dc
appraisal_overall: L0-M2-H3
tripod_llm_pct: 35pct
---

## Source

[[@sridharanLeveragingArtificialIntelligence2025]]

## Description

> "All four LLMs were able to provide answers to the queries related to all seven cases following a single prompt (online supplemental file 2). In general, the responses were homogeneous with respect to appropriateness of the study designs, the risks and benefits of the proposed research, the identification of vulnerability issues and the information to be disclosed in the ICD." (Sridharan & Sivaramakrishnan, 2025, p. 127)
>
> ![[sridharanLeveragingArtificialIntelligence2025-table2-p4-1.png]]

## Methods Context

### What?

> **Study design:** observational cross-sectional pilot study (no human subjects; LLM-output evaluation).
>
> **Method type:** structured single-prompt querying of four general-purpose chatbots against a fixed set of validated ethics case studies, with two-rater human adjudication.
>
> **Tools:** Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0; FERCAP–SIDCER handbook of case studies on ethical issues in health research (first edition, 2012); US HHS Office for Human Research Protections (OHRP) informed-consent checklist.
>
> **Dependent variable(s):** binary judgement of whether the LLM identified each expected ethical issue (study design appropriateness, eligibility criteria, vulnerability issues, risk–benefit assessment, placebo justification, ICD content) per case.
>
> **Independent variable(s) / covariates:** LLM identity (4 levels) × case scenario (7 levels).
>
> "The present study was conducted as an observational, cross-sectional design between October and November 2023." (Sridharan & Sivaramakrishnan, 2025, p. 126)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p1-1.png]]

### How?

> **Procedure:** investigators selected 7 case studies from the FERCAP–SIDCER handbook (with reproduction approval) and posed a series of queries per case covering eligibility criteria, sample size, vulnerability, ICD content, risk–benefit, and placebo justification. Six queries were posed for cases 1–2; five for cases 3, 4, 6; four for case 7; two for case 5. Each LLM was first given all queries together as a **single prompt**; outputs were independently rated by two authors against expected key responses (Table 1) plus the FERCAP–SIDCER handbook and HHS ICD checklist, with consensus reached on disagreements. Online supplemental files 1–4 contain queries, raw outputs, and ICDs.
>
> "We compared the responses of the LLMs with a single prompt containing all of the queries together and multiple prompts in which each query was posted one by one, such as engaging in a series of dialogue. Two authors independently evaluated the response of four LLMs, and a consensus was reached." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-1.png]]

### Who?

> **Models / participants:** 4 LLMs evaluated — Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0 (the last paid; the first three free at evaluation time). No human participants.
>
> **Sample-size flow:** FERCAP–SIDCER handbook (case-study count not stated) → 7 prototypical cases selected covering allergic-rhinitis nasal irrigation (case 1), Tourette dose optimisation (2), measles vaccine route (3), Phase II vitamin X in oncology (4), oral iron chelation in MDS (5), IPV intervention (6), pesticide exposure (7) → all 7 analysed. Each of the 4 LLMs returned a response to every query for every case (28 LLM-case cells; no exclusions reported).
>
> "Four AI platforms were evaluated as follows: 1. Google Bard… 2. ChatGPT 3.5… 3. Claude-Instant-100k… 4. ChatGPT 4.0… Seven case studies were selected from the FERCAP–SIDCER handbook of case studies on ethical issues in health research published by the Forum for Ethical Review Committees in the Asian and Western Pacific Region (FERCAP) and the Strategic Initiative for Developing Capacity in Ethical Review (SIDCER)." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-2.png]]

## Other Notes

- "Failure-to-identify" patterns are domain-specific rather than model-specific in the single-prompt condition: only Claude-Instant-100k flagged the need for first-time-procedure observation in case 1; only ChatGPT 3.5 identified researcher risk in case 6 (IPV); only ChatGPT 3.5 and Google Bard flagged the need for separate consent for biological samples in case 7.
- Several "homogeneous" failures are shared across all four models (e.g., none caught the inappropriate non-randomised design in case 4; none flagged the school-site coercion risk in case 3).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanLeveragingArtificialIntelligence2025#TRIPOD-LLM reporting summary]].

| Domain (single-prompt) | ChatGPT 4.0 | Google Bard | ChatGPT 3.5 | Claude-Instant-100k |
| --- | :---: | :---: | :---: | :---: |
| Study-design appropriateness (case 4) | missed | missed | missed | missed |
| Eligibility criteria (cases 1, 3) | missed both | missed both | missed both | missed both |
| Placebo appropriateness (case 5) | missed | identified | missed | partial (unsubstantiated) |
| Sample-size calculation (case 1) | missed | missed | missed | missed |
| Risk-mitigation in vulnerable population (cases 1, 2, 3 + 2 + 4) | mostly missed | mostly missed | mostly missed | mostly missed |
| Essential ICD content (case 2) | missed | missed | missed | missed |
| Essential ICD content (case 3) | missed | missed | identified | missed |
| Overall response coverage | 7/7 cases answered | 7/7 cases answered | 7/7 cases answered | 7/7 cases answered |

Source-file table: see Table 2 (p. 128).

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - LLM evaluation used only cloud-based models on pilot sample of seven cases limiting multicentric and cultural applicability]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

- [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

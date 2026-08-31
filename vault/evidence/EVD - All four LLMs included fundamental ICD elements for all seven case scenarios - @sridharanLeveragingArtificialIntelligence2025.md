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
nodeID: 019ddb4e-6b56-71c3-9d05-1e7fa20ace95
appraisal_overall: L0-M2-H3
tripod_llm_pct: 35pct
---

## Source

[[@sridharanLeveragingArtificialIntelligence2025]]

## Description

> "Each of the LLMs included all of the fundamental elements of the ICD for all case scenarios. Use of jargon, understatement of benefits and failure to state potential risks were the key observations in the AI-generated ICDs." (Sridharan & Sivaramakrishnan, 2025, p. 127)
>
> ![[sridharanLeveragingArtificialIntelligence2025-table4-p7-1.png]]

## Methods Context

### What?

> **Study design:** observational cross-sectional pilot evaluation of LLM-generated ICDs (no human subjects).
>
> **Method type:** single-prompt LLM generation followed by checklist-based human rating against the US HHS OHRP informed-consent checklist.
>
> **Tools:** Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0; HHS informed-consent regulations / checklist (https://www.hhs.gov/ohrp/regulations-and-policy/guidance/checklists).
>
> **Dependent variable(s):** presence/absence of each "fundamental element" of the ICD (study procedures, benefits, risks, statement of consent, study site, critical adverse-event information, jargon usage, word count).
>
> **Independent variable(s) / covariates:** LLM identity (4 levels) × case scenario (7 levels) × ICD element.
>
> "A separate query was posed to the LLMs for conceiving ICDs for each of the seven case scenarios as follows: 'Below is the summary of a research proposal. Can you generate an ICD for the study participants?' The output generated for this query was independently evaluated by the authors, and a consensus was reached using the checklist for informed consent from the US Department of Health and Human Services." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-3.png]]

### How?

> **Procedure:** for each of the 7 case scenarios, a single prompt summarising the research proposal was sent to each of the 4 LLMs with the request "Can you generate an ICD for the study participants?" The two authors then independently checked each generated ICD against the HHS checklist (fundamental elements + recommended readability) and reached consensus. Recorded checks: presence of every fundamental element; jargon use (e.g., "tardive dyskinesia", "intrahepatic cholangiocarcinoma", "Yale Global Tic Severity Scale"); whether benefits were correctly described as not-guaranteed; word count vs. the 1250-word readability target. Findings tabulated in Table 4 (p. 132); raw ICDs in online supplemental file 4.
>
> "We compared the responses of the LLMs with a single prompt containing all of the queries together and multiple prompts in which each query was posted one by one, such as engaging in a series of dialogue. Two authors independently evaluated the response of four LLMs, and a consensus was reached." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-4.png]]

### Who?

> **Models / participants:** 4 LLMs — Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0 — generating ICDs; no human subjects.
>
> **Sample-size flow:** FERCAP–SIDCER handbook → 7 prototypical case scenarios → 28 ICDs generated (4 LLMs × 7 cases) → all 28 evaluated against the HHS checklist; none excluded. All 28 ICDs were within the recommended 1250-word ceiling.
>
> "Four AI platforms were evaluated as follows: 1. Google Bard… 2. ChatGPT 3.5… 3. Claude-Instant-100k… 4. ChatGPT 4.0…" (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-5.png]]

## Other Notes

- All four LLMs used jargon ("randomised", "double-blind", "placebo", "phase II clinical trial", "open-label", "non-randomised", "cross-sectional", "Tourette syndrome", "intrahepatic cholangiocarcinoma", "myelodysplastic syndrome", "clonal stem cell disorders", "MED patch", "Yale Global Tic Severity Scale", "tardive dyskinesia", "serological response", "hypercalcemia", "event-free survival", "interim analysis", "composite primary endpoint") despite the recommended ≤8th-grade reading level. Some technical terms in Google Bard came with plain-language explanations (e.g., "under the skin" for subcutaneous, "inhaled" for aerosol).
- None of the LLMs mentioned the number of participants to be recruited.
- Google Bard and Claude-Instant-100k did not mention IRB contact details in the ICD.
- ChatGPT 3.5 and ChatGPT 4.0 inappropriately included eligibility criteria in the ICD for all cases.
- Case-2-specific failures: none of the LLMs explicitly stated that the natural course of Tourette is waxing/waning, nor that the experimental drug is symptomatic and not curative, nor that participants might receive placebo. ChatGPT 3.5 made a misleading "optimal-dose" statement; ChatGPT 4.0 corrected this.
- Case-6-specific error: ChatGPT 3.5 (but not 4.0) erroneously claimed interviews would be audio-recorded for transcription/analysis.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanLeveragingArtificialIntelligence2025#TRIPOD-LLM reporting summary]].

| ICD element | ChatGPT 4.0 | Google Bard | ChatGPT 3.5 | Claude-Instant-100k |
| --- | :---: | :---: | :---: | :---: |
| Fundamental ICD elements present (all 7 cases) | yes | yes | yes | yes |
| Word count ≤ 1250 (HHS readability) | met | met | met | met |
| Procedure description (case 1) | specified | not stated | specified | not stated |
| "Benefits not guaranteed" stated (all 7 cases) | not stated (except case 5) | not stated | specified | not stated (except cases 4, 5) |
| Statement of consent (all 7 cases) | partially specified | not stated | partially specified | not stated |
| Risks to study participants (case 6 IPV emotional distress) | specified | not stated | specified | specified |
| Serious AE flagged (case 2 tardive dyskinesia) | not stated | specified | not stated | not stated |
| Serious AE flagged (case 5 iron overload in placebo arm) | not stated | not stated | not stated | specified |
| Study site (case 3 school) | not stated | not stated | specified | not stated |
| Critical info (case 4 no insurance for AEs) | specified | not stated | not stated | not stated |

Source-file table: see Table 4 (p. 132).

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

- [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

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
nodeID: 019ddb4e-6b53-7236-a205-c04af0a5a2a7
appraisal_overall: L0-M2-H3
tripod_llm_pct: 23pct
---

## Source

[[@sridharanAssessingDecisionMakingCapabilities2024]]

## Description

> "The SOP-related outputs from the AI platforms are set out in Electronic Supplementary Material 4. Overall, these platforms managed to cover the fundamental sections of the SOPs requested, including purpose, scope, definitions, procedures, and responsibilities. Despite variations in wording, the core content remained strikingly similar. Distinctive differences in the SOPs crafted by the AI tools are presented in Table 2." (Sridharan & Sivaramakrishnan, 2024, p. 85)
>
> ![[sridharanAssessingDecisionMakingCapabilities2024-table2-p7-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational LLM evaluation, generative-output coverage assessment.
>
> **Method type:** prompt-elicited SOP drafting by three LLMs, with each output qualitatively compared against two reference institutional SOP corpora by two independent authors.
>
> **Tools:** Poe Assistant, ChatGPT (GPT-3.5), Google Bard; Mayo Clinic IRB Policy Manual (2023) and Harvard Longwood Medical Area Standard Operating Procedures (2023) as reference SOPs; ICH E6 GCP guidelines for normative checks.
>
> **Dependent variable(s):** (a) presence of fundamental SOP sections (purpose, scope, definitions, procedures, responsibilities); (b) per-topic content differences between platforms (Table 2 rows).
>
> **Independent variable(s) / covariates:** AI platform (3 levels); SOP topic (16 prompted IRB-related tasks).
>
> "In addition, we used specific prompts (Electronic Supplementary Material 2) of the AI platforms to generate the SOPs for IRBs related to the following tasks" (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-1.png]]

### How?

> **Procedure:** (1) For each of 16 IRB-relevant SOP topics (constitution of IRB and IRB membership; management of initial protocol submissions; conflicting interests of IRB members; expedition of proposal reviews; exemption of proposals from IRB reviews; continuing review; review of study completion reports; protocol-deviation management; protocol-violation management; SAE review; UAE review; clinical trial site monitoring visit; vulnerable-population proposals; informed-consent waiver review; phase I trials in healthy humans; quality assurance of IRB functions), the authors used the prompts in Electronic Supplementary Material 2 to elicit a draft SOP from each of the three AI platforms. (2) Each platform's draft SOP was independently read by two authors and compared section-by-section against the Mayo Clinic and Harvard Longwood reference SOPs. (3) Common coverage (purpose / scope / definitions / procedures / responsibilities) was tallied; distinctive per-platform differences and omissions common to all three platforms were extracted into Table 2. No quantitative scoring rubric, statistical comparison, or inter-rater agreement metric is reported.
>
> "Two authors independently assessed the outputs of SOPs and compared them with the IRB SOPs from the Mayo Clinic (IRB Mayo Clinic, 2023) and Harvard Medical School (Harvard Longwood Medical Area Standard Operating Procedures, 2023)." (Sridharan & Sivaramakrishnan, 2024, p. 85)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p3-1.png]]

### Who?

> **Models / participants:** three AI platforms, Poe Assistant, ChatGPT (GPT-3.5, OpenAI), Google Bard. No human participants.
>
> **Sample-size flow:** 16 SOP topics prompted → administered to all 3 platforms → 48 platform × topic SOP drafts produced and reviewed. Reference corpora: 2 institutional SOP sets (Mayo Clinic, Harvard Longwood). Two human reviewers (the two paper authors).
>
> "The following three AI platforms were used in this study: • Poe Assistant©… • ChatGPT©: This language model is based on the GPT-3.5 architecture developed by OpenAI… • Google Bard©: Bard is a transformer-based large language model" (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-2.png]]

## Other Notes

- "Strikingly similar" core content masked clinically meaningful divergences, e.g., on COI handling Poe Assistant said the conflicted member could participate in discussion (only barred from voting), while ChatGPT and Bard correctly required the member to leave the room and not be counted in quorum.
- Omissions common to all three platforms (per Table 2 right-hand column): no mention that the IRB chairperson should be independent of the institution; no mention of scope of proposals reviewed; no member appointment / disqualification criteria; COI member should not be counted in quorum and meeting minutes should record the recusal; expedited-approval decisions should be disclosed at the next full IRB meeting; in multi-centric studies AE / SAE reports from other sites should be submitted.
- ChatGPT was the only platform to mention KPIs for IRB quality assurance.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanAssessingDecisionMakingCapabilities2024#TRIPOD-LLM reporting summary]].

| Outcome | Value |
| --- | --- |
| SOP topics prompted | 16 |
| Platforms × topics → SOP drafts produced | 48 |
| Drafts covering all 5 fundamental sections (purpose / scope / definitions / procedures / responsibilities) | All drafts (qualitative narrative) |
| Reference SOP corpora used as gold | Mayo Clinic IRB Policy Manual; Harvard Longwood Medical Area SOPs |
| SOP topics with distinctive per-platform differences (Table 2) | 7 (Constitution; COI; Expedited review; Exemption from review; Continuing review; Study-completion report review; SAE review) |
| SOP topics with omissions common to all 3 platforms | 6+ items aggregated in Table 2 right column |
| Quantitative coverage / accuracy score | Not reported |
| Inter-rater agreement | Not reported |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

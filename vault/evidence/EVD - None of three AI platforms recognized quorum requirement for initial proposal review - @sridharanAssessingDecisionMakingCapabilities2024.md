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
nodeID: 019ddb4e-6b7e-7568-87fd-f542f9230f18
appraisal_overall: L0-M2-H3
tripod_llm_pct: 23pct
---

## Source

[[@sridharanAssessingDecisionMakingCapabilities2024]]

## Description

> "Concerning the SOP for the initial review of proposals, none of the AI platforms recognized the necessity of achieving a quorum for conducting a full board review." (Sridharan & Sivaramakrishnan, 2024, p. 85)
>
> ![[sridharanAssessingDecisionMakingCapabilities2024-table2-p7-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional observational LLM evaluation — single-topic failure-mode analysis nested in the broader 16-SOP Sridharan & Sivaramakrishnan benchmark.
>
> **Method type:** prompt-elicited SOP draft per platform, qualitatively reviewed by two independent authors against Mayo Clinic and Harvard Longwood reference SOPs and ICH E6 GCP.
>
> **Tools:** Poe Assistant, ChatGPT (GPT-3.5), Google Bard; Mayo Clinic IRB Policy Manual; Harvard Longwood Medical Area SOPs.
>
> **Dependent variable(s):** binary "mentions quorum requirement / does not" coding for the SOP on management of initial protocol submissions to IRB.
>
> **Independent variable(s) / covariates:** AI platform (3 levels).
>
> "Management of initial protocol submissions to IRB" (Sridharan & Sivaramakrishnan, 2024, p. 84)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p2-4.png]]

### How?

> **Procedure:** the prompt for "management of initial protocol submissions to IRB" (Electronic Supplementary Material 2) was administered to each of the three AI platforms. Two authors independently reviewed each draft and checked whether the SOP mentioned the requirement that a quorum be achieved before a full board review may proceed — a known requirement under both Mayo Clinic and Harvard Longwood SOPs and standard IRB regulation. None of the three drafts surfaced the quorum requirement; this omission is reported narratively in Results and tabulated in Table 2's right-hand "common to all three" column.
>
> "Concerning the SOP for the initial review of proposals, none of the AI platforms recognized the necessity of achieving a quorum for conducting a full board review." (Sridharan & Sivaramakrishnan, 2024, p. 85)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p3-3.png]]

### Who?

> **Models / participants:** three AI platforms — Poe Assistant, ChatGPT (GPT-3.5), Google Bard. No human participants.
>
> **Sample-size flow:** 1 SOP topic (initial review of proposals) → administered to all 3 platforms → 3 platform-drafts analyzed; 0 / 3 mentioned the quorum requirement. Two human reviewers (the two paper authors).
>
> "Two authors independently assessed the outputs of SOPs and compared them with the IRB SOPs from the Mayo Clinic (IRB Mayo Clinic, 2023) and Harvard Medical School (Harvard Longwood Medical Area Standard Operating Procedures, 2023)." (Sridharan & Sivaramakrishnan, 2024, p. 85)
> ![[sridharanAssessingDecisionMakingCapabilities2024-evd-p3-4.png]]

## Other Notes

- The quorum omission is one of several "common to all three platforms" failures called out in Table 2's rightmost column, alongside: chairperson independence, scope of reviewable proposals, and member appointment / disqualification criteria.
- The COI section of Table 2 also notes a related quorum failure — none of the three platforms stated that a member with declared COI should not be counted in the quorum, even when ChatGPT and Bard correctly required the conflicted member to leave the room.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanAssessingDecisionMakingCapabilities2024#TRIPOD-LLM reporting summary]].

| Platform | Mentions quorum requirement for full board review? |
| --- | :---: |
| Poe Assistant | No |
| ChatGPT (GPT-3.5) | No |
| Google Bard | No |
| **Aggregate** | **0 / 3 platforms** |
| Related "common to all" SOP omissions (Table 2) | Chairperson institutional independence; scope of proposals reviewed; member appointment / disqualification criteria; COI-member exclusion from quorum |
| Quantitative scoring / IAA | Not reported |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

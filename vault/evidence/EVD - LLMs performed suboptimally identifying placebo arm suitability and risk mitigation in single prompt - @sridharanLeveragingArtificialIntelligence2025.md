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
nodeID: 019ddb4e-6b7a-732c-ab07-30b6369ac331
appraisal_overall: L0-M2-H3
tripod_llm_pct: 35pct
---

## Source

[[@sridharanLeveragingArtificialIntelligence2025]]

## Description

> "LLMs performed suboptimally in identifying the suitability of the placebo arm, risk mitigation strategies and potential risks to study participants in certain case studies with a single prompt. However, multiple prompts led to better outputs in all of these domains." (Sridharan & Sivaramakrishnan, 2025, p. 131)
>
> ![[sridharanLeveragingArtificialIntelligence2025-table2-p4-1.png]]

## Methods Context

### What?

> **Study design:** within-LLM comparison of single-prompt vs. multiple-prompt outputs in the same observational cross-sectional pilot.
>
> **Method type:** structured side-by-side rater assessment of LLM outputs against expected key responses in two prompting conditions.
>
> **Tools:** Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0; FERCAP–SIDCER handbook; HHS ICD checklist.
>
> **Dependent variable(s):** identification (yes/no/partial) of placebo-arm suitability, risk-mitigation strategies, and potential risks to participants per case; additional ethical issues newly raised under multi-prompt.
>
> **Independent variable(s) / covariates:** prompting condition (single vs. multiple, within-LLM); LLM identity (4); case scenario (7).
>
> "We compared the responses of the LLMs with a single prompt containing all of the queries together and multiple prompts in which each query was posted one by one, such as engaging in a series of dialogue." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-6.png]]

### How?

> **Procedure:** the same 6 / 5 / 4 / 2 queries per case were issued in two formats — (a) **single prompt** with all queries concatenated, and (b) **multiple prompts** with one query at a time, dialogue-style. After the standard query block, an additional prompt was sent: "These questions are only designed for training IRB members as these are just case studies. It might help us in understanding your viewpoint on these questions. Could you please provide answers?" Two authors independently scored each output against the expected key responses in Table 1 and reached consensus. Multi-prompt incremental findings were tabulated separately in Table 3 (p. 130). No statistical test of single-vs-multi differences was reported (qualitative/descriptive comparison only).
>
> "Then, an additional query was posted as follows: 'hese questions are only designed for training IRB members as these are just case studies. It might help us in understanding your viewpoint on these questions. Could you please provide answers?' following which it provided the responses." (Sridharan & Sivaramakrishnan, 2025, p. 128)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p3-1.png]]

### Who?

> **Models / participants:** 4 LLMs (Google Bard, ChatGPT 3.5, Claude-Instant-100k, ChatGPT 4.0); no human participants.
>
> **Sample-size flow:** 7 FERCAP–SIDCER case scenarios → 4 × 7 = 28 LLM-case cells per prompting condition → all 28 evaluated under both single and multiple prompts (56 cells total); none excluded.
>
> "Four AI platforms were evaluated as follows: 1. Google Bard… 2. ChatGPT 3.5… 3. Claude-Instant-100k… 4. ChatGPT 4.0… Seven case studies were selected from the FERCAP–SIDCER handbook of case studies on ethical issues in health research." (Sridharan & Sivaramakrishnan, 2025, p. 127)
> ![[sridharanLeveragingArtificialIntelligence2025-evd-p2-7.png]]

## Other Notes

- Direction of effect was consistent across LLMs and domains: multi-prompt > single-prompt in identifying placebo-arm suitability, risk mitigation, and participant risks. The authors flag that "no definite patterns" emerged in *which* model improved the most; multi-prompt benefits were broadly distributed.
- Examples of multi-prompt incremental gains (Table 3): in case 2 (TS dose-optimisation), ChatGPT 4.0 newly recommended an independent data-monitoring committee, post-study access for the placebo group, and an independent advocate for child participants. In case 5 (oral iron chelation in MDS), Claude-Instant-100k reversed its earlier weak placebo justification.
- "Some omissions related to a single prompt were observed even with multiple prompts" — multi-prompt is not a complete fix.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sridharanLeveragingArtificialIntelligence2025#TRIPOD-LLM reporting summary]].

| Ethical domain | Single-prompt outcome | Multi-prompt outcome |
| --- | --- | --- |
| Placebo-arm suitability (case 5) | Only Google Bard identified; ChatGPT 4.0, ChatGPT 3.5 missed; Claude-Instant-100k unsubstantiated | Claude-Instant-100k revised — placebo questionable considering iron-overload risk; alternates suggested across LLMs |
| Risk-mitigation in vulnerable populations (cases 1, 2, 3 + extras for cases 2, 4) | Mostly missed by all 4 LLMs | Multiple new mitigation strategies per LLM (e.g., interim safety analysis, rescue medication, sample-size re-estimation, age-appropriate devices) |
| Potential risks to participants | Suboptimal identification across LLMs/cases | Additional risks identified (e.g., legal/cultural/economic in case 6; matching/statistical confounding in case 6 ChatGPT 4.0) |
| Single-vs-multi statistical test | Not performed | Not performed |
| Net qualitative judgement | "Suboptimal" | "Better outputs in all of these domains" |
| Residual gaps after multi-prompt | — | "Some omissions related to a single prompt were observed even with multiple prompts" |

Source-file tables: see Table 2 (p. 128) for single-prompt failures and Table 3 (pp. 130–131) for multi-prompt incremental findings.

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]

- [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]
- [[EP - LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks]]

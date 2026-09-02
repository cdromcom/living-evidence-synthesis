---
NodeFormality: draft
TruthValue: 0.75
aliases:
tags:
  - task/ethics-irb-review
  - 5c/care
  - ep/strength/2-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cd20e454a37
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cd20e454a37
---

## Pattern statement

When evaluated on clinical-ethics tasks (IRB review of case studies, drafting Standard Operating Procedures, generating informed consent documents), LLMs reliably produce outputs that *follow* the expected protocol structure, covering the standard sections of an IRB response or an ICD, but consistently *miss* substantive content requirements that depend on specific case details (post-trial access provisions, quorum requirements, placebo-arm risk mitigation). Surface compliance without substantive completeness.

## What is being claimed

The pattern is that protocol-structure compliance is much easier for LLMs than substantive content correctness. An LLM can write an SOP that hits all the standard sections, or an ICD that includes all the standard fields, and look qualitatively reasonable to a checklist-style review. But the moment an evaluator asks whether the *specific* substantive requirements of the case were met (did the response correctly address that this specific protocol involves herbal medicine? did it correctly identify quorum needed? did it weigh placebo arm suitability?), the LLMs fail. For deployment in clinical-ethics settings, structure-of-output is not a useful signal for trust; specific-requirement-coverage is.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - Three AI platforms responded correctly to all 10 IRB case study queries - @sridharanAssessingDecisionMakingCapabilities2024]], Sridharan & Sivaramakrishnan 2024 (decision-making): all three AI platforms produced structurally-correct responses to all 10 IRB case queries.
- [[EVD - All AI platforms failed to address post-trial herbal medicine access in case study 10 - @sridharanAssessingDecisionMakingCapabilities2024]], Sridharan & Sivaramakrishnan 2024 (decision-making): the *same* platforms missed the substantive content requirement on post-trial access, a high-stakes item that requires reasoning about specific case details.
- [[EVD - None of three AI platforms recognized quorum requirement for initial proposal review - @sridharanAssessingDecisionMakingCapabilities2024]], Sridharan & Sivaramakrishnan 2024 (decision-making): none of the three platforms identified the quorum-requirement requirement when drafting the SOP for initial protocol review.
- [[EVD - AI platforms drafted SOPs covering fundamental sections with variations across platforms - @sridharanAssessingDecisionMakingCapabilities2024]], Sridharan & Sivaramakrishnan 2024 (decision-making): the SOPs covered the fundamental sections expected of an SOP, protocol-shape compliance.
- [[EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous responses - @sridharanLeveragingArtificialIntelligence2025]], Sridharan & Sivaramakrishnan 2025 (leveraging): all four LLMs produced answers to all seven IRB ethics case queries, structural completeness.
- [[EVD - All four LLMs included fundamental ICD elements for all seven case scenarios - @sridharanLeveragingArtificialIntelligence2025]], Sridharan & Sivaramakrishnan 2025 (leveraging): all four LLMs covered the fundamental ICD elements, protocol-shape compliance.
- [[EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt - @sridharanLeveragingArtificialIntelligence2025]], Sridharan & Sivaramakrishnan 2025 (leveraging): the *same* four LLMs underperformed on the substantive content questions about placebo arm suitability and risk mitigation.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]], [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]].
- **Methodologically related:** [[EP - Per-item LLM-human agreement varies sharply by item type]]; the substantive-content-vs-protocol-structure split is one instance of the broader item-type variance pattern, applied to the clinical-ethics domain.

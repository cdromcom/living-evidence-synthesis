---
NodeFormality: draft
TruthValue: 0.75
aliases:
tags:
  - task/rare-class-reliability
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cd4391c9493
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cd4391c9493
---

## Pattern statement

Inter-rater agreement on subjective scientific-judgment tasks (citation-accuracy categorization, methodological-bias scoring, confounder selection, pragmatism judgment) is empirically low — for both humans and LLMs. Cohen's kappa values cluster in the "fair" range (0.16–0.37), and human inter-rater reliability declines as the task moves from objective reporting checks (PRISMA at 91%) toward subjective methodological judgment (PRECIS-2 at 57%). LLM inter-prompt agreement falls in the same range when the LLM is asked the same question in slightly different wordings.

## What is being claimed

The pattern is a measurement-ceiling argument: if humans don't reliably agree with each other on these tasks, no model trained against human labels can do much better than the agreement floor. This means (1) any benchmark using these labels carries irreducible label noise; (2) reports of LLM-vs-human disagreement should be benchmarked against human-vs-human disagreement before being interpreted as LLM failure; (3) tasks with intrinsically low IAA may be poor targets for full automation regardless of how good the LLM gets. The pattern explains why so many papers in this corpus report "moderate" rather than "high" performance: the underlying task isn't fully tractable.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2 - @sarolAssessingCitationIntegrity2024]] — Sarol et al. 2024: human kappa 0.18–0.31 on citation-accuracy categorization, even after multiple reconciliation phases — fair agreement, not strong.
- [[EVD - Human inter-rater reliability dropped from 91 percent on PRISMA to 57 percent on PRECIS-2 - @woelfleBenchmarkingHumanAICollaboration2024]] — Woelfle et al. 2024: human IRR drops from 91% on objective PRISMA-style reporting checks to 57% on subjective PRECIS-2 pragmatism judgment — IRR is a function of task subjectivity.
- [[EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.16 across prompt variations - @huntington-kleinLLMsActRepositories2024]] — Huntington-Klein & Murray 2024: LLM-vs-LLM inter-prompt agreement is as low as 0.16 — LLMs themselves disagree at the same fair-agreement level as humans on subjective tasks.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]] — Sarol's IAA finding is a partial explanation for why citation-error detection is hard for any model, including LLMs.
- **Caveats that flag this constraint structurally:** [[CVT - Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data]] — the IAA limitation is a CVT on the EVDs that depend on the affected labels.
- **Adjacent pattern (related mechanism):** [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]] — both patterns point at the labeling step as the upstream constraint on what any LLM-evaluation can show.

---
NodeFormality: draft
TruthValue: 0.65
aliases:
tags:
  - task/prompt-sensitivity
  - 5c/credibility
  - ep/strength/2-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec736233ff49
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec736233ff49
---
1
## Pattern statement

A counterintuitive cross-paper finding: **adding more input context (full paper text rather than abstract; abstract + retrieved excerpts rather than title alone) can *degrade* rather than improve LLM performance on structured scientific-evaluation tasks.** Two independent papers in this corpus, with different LLMs and different tasks, both report that the *less-information* condition outperformed the *more-information* condition.

## What is being claimed

The pattern challenges the default practitioner assumption that "more context = better LLM performance." On research-quality scoring (Thelwall) and quotation-error detection (Zhang2024), the LLM did better with less. The likely mechanism is task-specific: the LLM is being asked to perform a structured judgment (does this abstract describe high-quality research? does this citation accurately reflect the source?) where the *summary* contains the load-bearing signal and the additional context dilutes attention or introduces distractors. For tooling, the implication is to test the abstract-only or title-only condition before assuming RAG or full-text input will help.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - Full text input produced lower Spearman correlations than abstracts for all three ChatGPT models tested - @thelwallEvaluatingResearchQuality2024]] — Thelwall 2024: full-text input *lowered* Spearman correlation with human quality scores below abstract-only input — across all three GPT models tested.
- [[EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0% - @zhangDetectingReferenceErrors2024]] — Zhang & Abernethy 2024: GPT-3.5 Turbo peaks at 68.0% with title-only input and drops to 54.0% as more context (abstract + retrieved excerpts) is added.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - Abstracts are the optimal input for LLM-based research quality assessment outperforming full text]].
- **Adjacent pattern (the opposing direction):** [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]] — RAG-style augmentation often helps, but this EP flags that it does not always help; the structured-task / summary-suffices condition can flip the sign.

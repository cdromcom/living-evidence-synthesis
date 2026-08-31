---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/prompt-sensitivity
  - 5c/credibility
  - 5c/creativity
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1ccfc8ade618
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1ccfc8ade618
---

## Pattern statement

Retrieval augmentation (RAG), few-shot prompting, multi-agent decomposition, and chain-of-thought reasoning consistently *improve* LLM performance on scientific-evaluation tasks — but the size of the improvement is typically smaller than the remaining gap to human-expert performance. The takeaway is that scaffolding helps, but does not by itself convert a zero-shot LLM into a human-equivalent reviewer.

## What is being claimed

Three measurement frames support the same conclusion. (1) RAG: adding domain-relevant retrieval to GPT-4o for limitation identification adds ~12 percentage points but leaves the model 22 percentage points below human level. (2) Multi-agent decomposition: MARG-S more than doubles the rate of useful-and-specific feedback compared to a single-agent baseline, but is still rated below human reviewer feedback. (3) Specialized retrieval architecture: facet-based RankGPT re-ranking is essential — removing it causes performance to collapse from 89.66% to 13.79% — yet even with it the system is benchmarked on a 32-idea test set rather than against expert reviewers at scale. Scaffolding is necessary, not sufficient.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]] — Xu et al. 2025: RAG adds 12.2 pp to GPT-4o on limitation identification — but the resulting accuracy still sits well below the 86% human ceiling on the same task.
- [[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]] — Shahid et al. 2025: a RAG-based novelty system reaches 0.81 accuracy, well above zero-shot LLM baselines (AI Scientist 0.47).
- [[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]] — Shahid et al. 2025: removing the retrieval scaffolding collapses performance from 89.66% to 13.79% — confirming that the gain is *driven by* the retrieval step, not by raw LLM capability.
- [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]] — D'Arcy et al. 2024: multi-agent prompting more than doubles the rate of useful, specific peer-review feedback comments compared to a single-agent GPT-4 baseline.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - RAG augmentation improves LLM limitation identification by grounding generation in domain-relevant literature]], [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]], [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]].
- **Companion pattern (when scaffolding still leaves the gap):** [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]] — RAG helps the average; the rare-class deficit may persist.

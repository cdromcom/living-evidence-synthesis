---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/error-detection
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec76d5080213
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec76d5080213
---

## Pattern statement

On *zero-shot* scientific-evaluation benchmarks, **closed-source proprietary LLMs (GPT-4o, Claude 3.5/3.7, o-series, Gemini) outperform open-source LLMs (Llama, Mixtral, Mistral, Qwen, OLMo) by substantial margins**, often a factor-of-2 or larger gap on the deployment-relevant metric. The exception is *fine-tuned* open-source models, which can flip the result entirely.

## What is being claimed

The pattern says: at zero-shot inference time, closed-source frontier LLMs are the strong default for scientific evaluation tasks. Open-source models do not currently match them when both are run as plug-and-play APIs. The exception is the fine-tuning path, where a smaller open-source model trained on task-specific data can win head-to-head against a much larger closed-source model. The pattern shapes the model-selection decision: zero-shot deployment → closed-source; fine-tunable budget + task-specific data → open-source.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]], Son et al. 2025: closed-source o3 leads SPOT; open-source Qwen2.5-VL-72B / Llama-4 / OLMo all score in the low single-digit percentages.
- [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]], Lou et al. 2025: open-source LLMs cannot beat the trivial all-positive baseline (40% F1) on EqInfer; closed-source o3-mini reaches 47.98%.
- [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]], Zhang & Abernethy 2025: Zhang only tested closed-source models, all of which lead.
- *Counter-example (the fine-tuning exception):* [[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]], Idahl & Ahmadi 2025: fine-tuned 8B open-source OpenReviewer beats zero-shot GPT-4o on the deployment metric.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]].
- **The fine-tuning exception:** [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]], fine-tuning is the path through which open-source models flip the closed-source default.
- **Reproducibility caveat:** [[CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives]], not all papers in the corpus tested open-source models, so the gap may be partially under-measured.

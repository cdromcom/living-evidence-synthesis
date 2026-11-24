---
NodeFormality: draft
human_reviewed: no
TruthValue: 0.7
aliases:
tags:
  - task/cost-scalability
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-11-24
nodeID: 019ddc81-bad6-76e4-b874-ec7416080a00
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec7416080a00
---

## Pattern statement

LLM cost-effectiveness on scientific-evaluation tasks varies by **two orders of magnitude** across model choices, and the Pareto frontier is repeatedly held by *smaller, cheaper, or specialized models*, not by the absolute-largest frontier model. Across at least three independent papers, the most expensive option is rarely the most cost-effective option, and the smallest-acceptable model often beats the largest-available model on the cost-adjusted metric.

## What is being claimed

The pattern shifts the deployment-decision frame. The default question "which LLM is best for this task?" treats best as raw accuracy. The cross-paper signal says: ask "which LLM is best per dollar?" and the answer changes substantially. Zhang2026 (arXiv v3) reports o4-mini at about 59% of o3's per-paper cost ($0.038 vs $0.064) with a 10.2 pp lower PDF hit rate, and Gemini 2.5 Flash matching o4-mini's hit rate at a lower cost (v1 of the paper had reported o4-mini at one-eighth of o3's cost with a 5 pp gap); Woelfle reports a 100× gap between GPT-4 and Mixtral on per-100-papers cost; Idahl shows an 8B fine-tuned model winning a head-to-head against GPT-4o. For applied tooling, the cost dimension is decisive when accuracy gaps are small.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - o4-mini reached 38.0% HR@5 at 0.038 USD per paper vs 0.064 USD for o3|EVD - o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper]], Zhang & Abernethy 2026 (arXiv v3): o4-mini achieves 38.0% HR@5 at $0.038 per paper vs o3's 48.2% at $0.064 (about 10 pp of HR@5 for 1.7× the cost), and Gemini 2.5 Flash matches o4-mini's hit rate (38.4%) at $0.033. v1 (2025) reported o3 at $0.321 and a 5 pp gap, an 8× cost ratio; v3 re-priced o3 at June-2025 rates and no longer calls o4-mini the most cost-effective choice, so this EVD supports the pattern more weakly than before.
- [[EVD - GPT-4 cost about 100x more than Mixtral-8x22B|EVD - GPT-4 cost approximately 100x more than Mixtral-8x22B per 100 papers in evidence appraisal]], Woelfle et al. 2024: GPT-4 costs ~100× more than Mixtral-8x22B per 100 papers in evidence appraisal, a two-orders-of-magnitude cost gap.
- [[EVD - OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons|EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations]], Idahl & Ahmadi 2025: an 8B-parameter fine-tuned reviewer beats GPT-4o (much larger, much more expensive) on the deployment-relevant preference metric.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - Fine-tuning on review data overcomes overly favorable LLM assessments|CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]], fine-tuned smaller models are part of the cost-effective Pareto frontier.
- **Compatible pattern:** [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]], fine-tuning is a key path to a Pareto-dominant smaller model.
- **Practical caveat:** for closed-source pricing, the cost gap is at the API-list-price level; deployment-time cost may differ with caching, batching, or self-hosted alternatives.

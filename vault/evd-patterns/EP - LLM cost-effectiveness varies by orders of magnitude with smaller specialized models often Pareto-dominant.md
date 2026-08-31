---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/cost-scalability
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec7416080a00
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec7416080a00
---

## Pattern statement

LLM cost-effectiveness on scientific-evaluation tasks varies by **two orders of magnitude** across model choices, and the Pareto frontier is repeatedly held by *smaller, cheaper, or specialized models* — not by the absolute-largest frontier model. Across at least three independent papers, the most expensive option is rarely the most cost-effective option, and the smallest-acceptable model often beats the largest-available model on the cost-adjusted metric.

## What is being claimed

The pattern shifts the deployment-decision frame. The default question "which LLM is best for this task?" treats best as raw accuracy. The cross-paper signal says: ask "which LLM is best per dollar?" and the answer changes substantially. Zhang2025 explicitly reports o4-mini Pareto-dominating o3 at one-eighth the cost; Woelfle reports a 100× gap between GPT-4 and Mixtral on per-100-papers cost; Idahl shows an 8B fine-tuned model winning a head-to-head against GPT-4o. For applied tooling, the cost dimension is decisive when accuracy gaps are small.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]] — Zhang & Abernethy 2025: o4-mini achieves 59.6% HR@5 at $0.038 per paper vs o3's 64.9% at $0.321 — ~5pp accuracy for ~8× cost.
- [[EVD - GPT-4 cost approximately 100x more than Mixtral-8x22B per 100 papers in evidence appraisal - @woelfleBenchmarkingHumanAICollaboration2024]] — Woelfle et al. 2024: GPT-4 costs ~100× more than Mixtral-8x22B per 100 papers in evidence appraisal — a two-orders-of-magnitude cost gap.
- [[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]] — Idahl & Ahmadi 2025: an 8B-parameter fine-tuned reviewer beats GPT-4o (much larger, much more expensive) on the deployment-relevant preference metric.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]] — fine-tuned smaller models are part of the cost-effective Pareto frontier.
- **Compatible pattern:** [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]] — fine-tuning is a key path to a Pareto-dominant smaller model.
- **Practical caveat:** for closed-source pricing, the cost gap is at the API-list-price level; deployment-time cost may differ with caching, batching, or self-hosted alternatives.

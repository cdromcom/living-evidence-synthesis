---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - 5c/credibility
  - 5c/creativity
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1ccb1f19e36b
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1ccb1f19e36b
---

## Pattern statement

When tasked with peer-review-style scoring of academic papers, general-purpose LLMs (GPT-4, GPT-4o, Claude-3.5, Llama-3.1-70B) systematically produce more positive recommendations and feedback than the human reviewers they are compared against — independent of whether the comparison is a direct recommendation score, a per-paper match rate against human reviewer recommendations, or feedback emphasis on positives vs. weaknesses.

## What is being claimed

The pattern shows up in three different measurement frames, all pointing the same direction. (1) Average recommendation: general-purpose LLMs assign systematically higher scores than humans on the same papers. (2) Match rate: general-purpose LLMs match a human reviewer recommendation less often than a fine-tuned reviewer model does. (3) Feedback emphasis: general-purpose LLMs comment on research implications and contributions far more often than humans do, and on novelty / limitations far less often. Anyone deploying a general-purpose LLM as a reviewer should expect that it will be a more lenient reviewer than a human counterpart, even when prompted to be critical.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers - @idahlOpenReviewerSpecializedLarge2025]] — Idahl & Ahmadi 2025: GPT-4o averages 7.7 vs human reviewers 5.4 on the same 400 papers (a >2-point gap on the recommendation scale).
- [[EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o - @idahlOpenReviewerSpecializedLarge2025]] — Idahl & Ahmadi 2025: a fine-tuned reviewer matches human recommendations more than twice as often as GPT-4o (55.5% vs 23.8%).
- [[EVD - GPT-4 commented on research implications 7.27x more than humans and on novelty 10.69x less on ICLR papers - @liangCanLargeLanguage2024a]] — Liang et al. 2024: GPT-4 over-emphasizes positives (implications) and under-emphasizes weaknesses (novelty / limitations) in scientific feedback.
- [[EVD - LLM review recommendation scores exceeded human scores without area-chair context but matched with it - @tyserAIDrivenReviewSystems2024]] — Tyser et al. 2024: LLM recommendation scores systematically exceed human scores in default conditions; only when explicit venue calibration context is added do they match.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]], [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]].
- **Mitigating pattern (when fine-tuning closes the gap):** [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]] — Idahl's OpenReviewer is the canonical example; fine-tuning on real peer reviews recovers human-distribution match.

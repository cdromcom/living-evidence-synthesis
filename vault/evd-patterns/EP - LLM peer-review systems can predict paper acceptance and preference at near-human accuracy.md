---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - 5c/credibility
  - 5c/creativity
  - ep/strength/4-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec72724c3ee7
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec72724c3ee7
---

## Pattern statement

When LLM-based peer-review systems are scored on *acceptance prediction* or *preference ranking* — predicting which paper got into a venue, or which paper's review will be preferred — they achieve accuracy substantially better than chance and often comparable to humans on the same task, across at least four independent papers and four different framings (F1 on acceptance, Bradley-Terry preference, LLM-judge win rate, aspect-score Pearson correlation).

## What is being claimed

The pattern is the cousin of the helpfulness pattern (#3). Helpfulness is about content quality; this is about prediction accuracy. The LLM's reviews track the same underlying paper-quality signal that humans use, well enough to outperform untrained baselines on acceptance prediction and to win head-to-head preference comparisons. The pattern does not claim LLMs are well-calibrated reviewers — it claims they have signal. Combined with the over-rating pattern, the implication is: LLM scores need recalibration, but the *ranking* induced by LLM scores carries useful information.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49 - @bougieGenerativeAdversarialReviews2024a]] — Bougie & Watanabe 2024: GAR predicts ICLR-23 paper acceptance at F1=0.66, significantly above the human baseline of 0.49.
- [[EVD - GPT-4 Turbo ranked first in human preference for academic review quality with score 0.558 - @tyserAIDrivenReviewSystems2024]] — Tyser et al. 2024: GPT-4 Turbo wins the Bradley-Terry preference contest at 0.558 — humans prefer its reviews to alternatives.
- [[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]] — Idahl & Ahmadi 2025: OpenReviewer wins 60% vs GPT-4o, 76% vs Llama-3.1-70B in LLM-judge preference comparisons.
- [[EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given the human-written review - @zhouLLMReliableReviewer2024]] — Zhou et al. 2024: GPT-3.5 achieves Pearson r=0.651 with human aspect scores when given the human-written review as input — strong rank-correlation evidence.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]].
- **Compatible with (does not contradict):** [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]] — predictive signal does not imply calibrated scores; ranks can be informative even when raw scores are biased upward.

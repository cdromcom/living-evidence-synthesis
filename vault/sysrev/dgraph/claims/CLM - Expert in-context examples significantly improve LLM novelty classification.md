---
NodeFormality: ReadyForInternal
human_reviewed: no
TruthValue: 0.5
aliases:
  - "CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines"
tags:
  - task/novelty-assessment
  - 5c/creativity
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6b93-7738-80f6-9e0d7d196afa
title: "Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines"
---
### Key Papers Making This Claim

> [!info] Papers
> [[sysrev/dgraph/source/@shahidLiteratureGroundedNoveltyAssessment2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "Our experiments show that incorporating expert-annotated data as in-context examples significantly enhances novelty classification accuracy compared to zero-shot prompts, DSPY, TextGRAD, and setups using OpenReview examples (Table 1)." (Shahid et al., 2025, p. 101)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-clm-p6-1.png]]

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim; verify before citing)

- [[sysrev/dgraph/evidence/EVD - AI Scientist reached 0.47 accuracy on novelty test set|EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set]]

- [[sysrev/dgraph/evidence/EVD - Idea Novelty Checker reached 0.81 accuracy beating baselines|EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset]]

- [[sysrev/dgraph/evidence/EVD - Swapping facet-based for general-relevance RankGPT cut accuracy 89.66% to 13.79%|EVD - Swapping the facet-based RankGPT re-ranker for a general-relevance RankGPT dropped not-novel prediction accuracy from 89.66% to 13.79%]]

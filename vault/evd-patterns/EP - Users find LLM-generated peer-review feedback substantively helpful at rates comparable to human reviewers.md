---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/review-generation
  - 5c/credibility
  - 5c/creativity
  - ep/strength/4-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec71e5d407b0
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec71e5d407b0
---

## Pattern statement

When researchers, expert raters, or LLM judges evaluate the *substantive helpfulness* of LLM-generated peer-review feedback, ratings consistently land at or near human-reviewer levels — across direct user surveys, expert-criteria comparison, human-likeness ratings, and good-comments-per-paper counts. The positive counterpart to the "LLMs over-rate papers" pattern: feedback *content* can be useful even when feedback *recommendations* are too lenient.

## What is being claimed

The pattern separates two questions that the over-rating pattern conflates: (1) does the LLM produce helpful, paper-specific feedback content? and (2) does the LLM produce well-calibrated overall recommendations? This pattern says yes to (1) — users find LLM feedback substantively helpful, raters rate it comparable to human reviews on multiple criteria, and judges rate it human-like — even when the over-rating pattern says no to (2). For deployment, the implication is that LLMs are usable as *feedback-generators for authors* (where helpfulness matters and recommendations don't) more than as *gatekeeping reviewers for editors* (where recommendation calibration is decisive).

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - 57.4% of 308 researchers found GPT-4 feedback helpful and 82.4% found it more beneficial than at least some human reviewers - @liangCanLargeLanguage2024a]] — Liang et al. 2024: 57.4% of 308 researchers found GPT-4 feedback helpful, 82.4% found it more beneficial than at least some of their actual human reviewers.
- [[EVD - LLM reviews scored comparably to human reviews on all three expert evaluation criteria - @tyserAIDrivenReviewSystems2024]] — Tyser et al. 2024: LLM reviews scored comparably to human reviews across all three expert evaluation criteria.
- [[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines - @bougieGenerativeAdversarialReviews2024a]] — Bougie & Watanabe 2024: GAR achieves human-likeness scores of 3.89–4.02 (out of 5) across three datasets — significantly above all LLM baselines.
- [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]] — D'Arcy et al. 2024: 3.7 user-rated-good-and-specific comments per paper from MARG-S vs 1.7 from single-agent GPT-4.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]], [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]].
- **Companion pattern (separable axis):** [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]] — *recommendation calibration* is a different axis from *feedback helpfulness*; a paper can fail on the former while succeeding on the latter.
- **Mechanism this pattern relies on:** [[EP - LLM-generated peer review feedback is paper-specific not generic boilerplate]] — feedback can only be helpful if it's actually about the paper at hand.

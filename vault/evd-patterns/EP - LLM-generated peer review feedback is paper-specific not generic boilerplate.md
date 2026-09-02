---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/review-generation
  - 5c/credibility
  - 5c/creativity
  - ep/strength/2-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cd36e6d59ad
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cd36e6d59ad
---

## Pattern statement

LLM-generated scientific peer-review feedback is empirically paper-specific rather than generic boilerplate. When the same LLM is asked to review two different papers and the feedback is matched against itself or against human reviewer comments, the resulting overlap reflects paper-aware content rather than a paper-independent template, overlap drops sharply when feedback for one paper is matched against another, and human raters perceive multi-agent-generated feedback as more specific to the paper at hand than single-agent baselines.

## What is being claimed

A common skeptical reading of LLM peer review is "the LLM just gives boilerplate critique, not paper-specific analysis." This pattern empirically rejects that reading at the gross-content level. When you shuffle the pairing of LLM feedback to papers, the pairwise content overlap collapses from the order-of-30% level to the order-of-0.4% level, meaning the content was driven by the paper, not by a fixed template. Multi-agent decomposition further increases the specificity: more than doubling the rate of comments human raters classify as useful and specific. The pattern does not say LLM feedback is *good*; only that it is paper-aware.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - Pairwise GPT-4 feedback overlap dropped from 30.85% to 0.43% after shuffling confirming paper-specificity - @liangCanLargeLanguage2024a]], Liang et al. 2024: pairwise overlap collapses from 30.85% (matched papers) to 0.43% (shuffled papers), direct empirical evidence that GPT-4 feedback is paper-driven.
- [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]], D'Arcy et al. 2024: multi-agent prompting generates 3.7 user-rated-as-specific-and-useful comments per paper vs. 1.7 for single-agent GPT-4, multi-agent decomposition produces more paper-specific feedback than single-agent prompting.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]], [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]].
- **Adjacent pattern (does not contradict):** [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]], feedback being paper-specific does not mean feedback is well-calibrated; specificity and accuracy are separable.

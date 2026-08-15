---
NodeFormality: draft
TruthValue: 0.65
aliases:
tags:
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddb86-7a01-7c34-a821-5e8bc2f9d401
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddb86-7a01-7c34-a821-5e8bc2f9d401
---

## Pattern statement

Across multiple independent scientific-error and paper-quality benchmarks, OpenAI's o-series reasoning models (o3, o3-mini, o4-mini) consistently lead other tested LLMs — including frontier non-reasoning models like Claude 3.7 Sonnet, GPT-4o, and Gemini 2.5 — at identifying errors, unsoundness problems, and structural defects in scientific papers.

## What is being claimed

Three different research groups, using three different benchmarks (one constructed-error dataset, one author-confirmed-retraction dataset, one expert-task suite) all report that **the highest absolute scores belong to an o-series reasoning model**. The pattern holds across:

- different error types (equation/proof, methodological, factual)
- different input formats (PDF, LaTeX)
- different scoring rules (precision/recall, hit rate, F1)
- different baselines (other closed-source LLMs, all-positive baseline, human reviewers)

The pattern is not "reasoning LLMs are good at this in absolute terms" — performance is still well below human level on most measures. The pattern is **comparative**: among current LLM options, an o-series model is the best LLM tool for these tasks.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]] — Zhang & Abernethy 2025: o3 leads on the WITHDRARXIV-CHECK quality-checker benchmark.
- [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]] — Son et al. 2025: o3 leads on the SPOT author-confirmed-error benchmark.
- [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]] — Lou et al. 2025: o3-mini leads on the AAAR-1.0 EqInfer task (equation correctness).

## Connected discourse-graph nodes

- **Within-paper claim that motivates this pattern (single paper):** [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]] — Zhang & Abernethy's claim, which this EP generalizes across two more papers.
- **Adjacent claim (broader and more skeptical):** [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]] — even with the o-series lead, the absolute scores remain too low for unsupervised deployment.
- **Caveats common to all three constituent EVDs:** closed-source-only evaluation, single-domain skew (math/physics for Zhang and Son; AI/ML for Lou), data-leakage risk from arXiv pretraining.

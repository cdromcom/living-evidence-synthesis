---
NodeFormality: draft
TruthValue: 0.8
aliases:
tags:
  - task/reporting-compliance-checking
  - 5c/clarity
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec6f131dcae9
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec6f131dcae9
---

## Pattern statement

When a scientific-evaluation task is formulated as **structured presence/absence checklist verification** ("is item X reported in this paper, yes or no?") frontier LLMs reach high accuracy (≥85% F1 or ≥85% match rate) across three independent benchmarks. The pattern is the positive counterpart to the per-item-variance EP: where the variance pattern says LLMs fail on methodologically-loaded items, this pattern says LLMs *succeed* on items that are concretely defined and extractable.

## What is being claimed

The pattern identifies a deployment niche where LLM-based scientific evaluation already works. Reporting-completeness checks (CONSORT, PRISMA, NeurIPS-checklist-style author attestations) are by their nature presence/absence questions about whether specific text exists in the paper. LLMs are good at this because the task reduces to retrieval + simple boolean classification, with low semantic ambiguity. The implication for tooling: a CONSORT-or-PRISMA compliance pre-screener is closer to deployment-ready than a substantive-quality reviewer.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper pairs - @liuReviewerGPTExploratoryStudy2023]], Liu & Shah 2023: GPT-4 hits 86.6% on NeurIPS author-checklist verification (the most concretely-defined of Liu's three sub-tasks).
- [[EVD - GPT-4 Turbo achieved F1=0.89 and 90% accuracy pooled across 9 CONSORT text questions on held-out clinical trial reports - @wrightsonGPTRCTsUsing2025]], Wrightson et al. 2025: GPT-4 Turbo reaches F1=0.89 / 90% accuracy across 9 CONSORT text questions on a held-out test set.
- [[EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent - @srinivasanEvaluatingReportingQuality2025a]], Srinivasan et al. 2025: GPT-4o-mini achieves F1=0.85 with precision=0.96 on CONSORT-TM, outperforming the prior state-of-the-art by 40 percentage points.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]], [[CLM - LLMs can assess clinical trial reporting guideline adherence with acceptable accuracy approaching 90%]].
- **Counter-pattern (where presence-absence breaks down):** [[EP - Per-item LLM-human agreement varies sharply by item type]], high accuracy on the *structured-extractable* subset of items co-exists with low accuracy on the methodologically-loaded subset; a complete picture requires reading both EPs together.

---
NodeFormality: draft
TruthValue: 0.8
aliases:
tags:
  - task/rare-class-reliability
  - 5c/credibility
  - ep/strength/5-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1ccc72642e27
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1ccc72642e27
---

## Pattern statement

When LLMs are evaluated on tasks where the deployment-relevant class is rare (the inaccurate-citation class, the limitation-present class, the error-present class, the equation-incorrect class), LLMs produce reasonable aggregate scores but collapse on the rare positive class — meaning headline metrics like accuracy and micro-F1 systematically overstate practical utility. The "deployment-critical class" is the one a real user actually cares about: errors to flag, weaknesses to surface, citations to verify.

## What is being claimed

The pattern is a measurement-vs-construct mismatch. A reasonable-looking 0.65 micro-F1 on a citation-accuracy benchmark can hide an 0.09 F1 on the inaccurate-citation class, which is the class anyone deploying the tool actually cares about. The same logic generalizes to limitation-detection (where the LLM rarely surfaces a real limitation), error-detection (where the LLM defaults to "no problem"), and equation-correctness (where reasoning models barely beat the trivial all-positive baseline). When evaluating LLM-as-tool feasibility for any of these tasks, never trust an aggregate metric — demand the per-class breakdown for the rare-but-important class.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations - @sarolAssessingCitationIntegrity2024]] — Sarol et al. 2024: 0.80 F1 on the easy class, **0.09** on the deployment-critical class (inaccurate citations).
- [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]] — Zhang & Abernethy 2025: Claude defaults to "no problem" 64.9% of the time when papers contain known errors.
- [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]] — Xu et al. 2025: GPT-4o catches 52% of limitations while humans catch 86% — the rare positive (limitation present) is where LLMs miss most often.
- [[EVD - GPT-4 correctly detected errors in 7 of 13 constructed short CS papers - @liuReviewerGPTExploratoryStudy2023]] — Liu & Shah 2023: GPT-4 misses errors in nearly half of papers with planted errors.
- [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]] — Lou et al. 2025: even the best reasoning LLM is only ~8 percentage points above the trivial all-positive baseline on equation correctness.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]], [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]], [[CLM - Current LLMs fall far short of requirements for dependable AI-assisted academic error verification]].
- **Adjacent pattern:** [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]] — both patterns describe ways that headline numbers hide failure modes; this one is class-imbalance, the other is per-instance correlation.

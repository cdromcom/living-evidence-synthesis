---
NodeFormality: draft
TruthValue: 0.6
aliases:
tags:
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec75d4a8d928
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec75d4a8d928
---

## Pattern statement

When LLMs are asked to commit to a judgment on scientific-error or scientific-quality tasks — *is there an error here? is this citation accurate? is this a real limitation?* — their confidence distributions are poorly calibrated. Either they refuse to commit (defaulting to "no problem", "fully accurate", "no limitation") or they over-commit on the easy class while under-recalling on the hard class. The pattern is distinct from the rare-class-failure pattern (EP4): EP4 is about F1 mismatch; this EP is about the upstream calibration mechanism that produces it.

## What is being claimed

The pattern says LLMs do not produce honest "I'm uncertain" or "this is borderline" responses on scientific-error tasks. They produce confident-looking outputs that are right when the answer is easy and wrong when the answer is hard, with no calibrated probability separating the two. For deployment, the implication is that LLM confidence scores are not a useful triage signal — you cannot rank LLM judgments by confidence and trust the top decile. Practical workarounds shift to repeated sampling (pass@k), majority voting across temperature variants, or independent verification.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]] — Son et al. 2025: across 498 model-instance evaluations on SPOT, only 2 produced a full-confidence response — the rest hover near zero confidence regardless of correctness.
- [[EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations - @sarolAssessingCitationIntegrity2024]] — Sarol et al. 2024: GPT-4 over-commits on the ACCURATE class (recall 0.90) while almost completely refusing to commit on the NOT_ACCURATE class (F1 0.09) — a calibration failure not a capability failure.
- [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]] — Zhang & Abernethy 2025: Claude 3.7 defaults to "no problem" 64.9% of the time on papers known to contain errors — refusal-to-commit on the hard class.

## Connected discourse-graph nodes

- **Adjacent pattern (mechanism vs. outcome):** [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]] — the rare-class F1 collapse is the *measurement* of poor calibration; this EP names the *mechanism*.
- **Mitigation path:** [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]] — scaffolding helps the average but doesn't typically fix calibration; pass@k and ensemble approaches may be needed.

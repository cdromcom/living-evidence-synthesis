---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/reporting-compliance-checking
  - 5c/credibility
  - 5c/clarity
  - ep/strength/2-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cd1cd10de79
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cd1cd10de79
---

## Pattern statement

Pairing one human rater with one LLM rater (or combining human-derived signal with LLM-derived signal in a single prediction) outperforms either source alone on structured scientific-appraisal tasks. The combination beats both individual humans and individual LLMs, suggesting the two sources contribute partially-independent information and the right deployment frame is augmentation, not replacement.

## What is being claimed

The pattern argues against a "humans vs. LLMs" framing of these tasks and toward a "humans + LLMs" framing. In Woelfle's evidence-appraisal benchmark, human-AI collaboration reaches 96% on PRISMA and 95% on AMSTAR, surpassing the average individual human rater. In Wu's novelty-prediction work, fusing peer-review-derived knowledge (a proxy for human judgment) with LLM-generated method summaries achieves F1 0.83, beating either source alone. The mechanism is partially-independent failure modes: LLMs miss methodologically loaded items, humans miss subtle structural details, the union catches more of both.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters - @woelfleBenchmarkingHumanAICollaboration2024]], Woelfle et al. 2024: pairing one human with one LLM exceeds individual human accuracy on the same systematic-review-appraisal task.
- [[EVD - Ours-SciBERT with combined human and LLM knowledge achieved F1=0.83 and accuracy=0.84 on method novelty prediction - @wuAutomatedNoveltyEvaluationa]], Wu et al. 2024: combining peer-review-derived knowledge (human judgment proxy) with LLM-generated method summaries reaches F1 0.83, beating LLM-only and human-knowledge-only baselines.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]], [[CLM - Combining human reviewer knowledge with LLM-generated method summaries improves automated novelty prediction beyond either source alone]].
- **Practical implication, complementary pattern:** [[EP - Per-item LLM-human agreement varies sharply by item type]], the partial-independence mechanism likely runs through this pattern: LLMs win on simple/structured items, humans win on methodologically-loaded items, and the combination covers both halves.

---
NodeFormality: draft
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-conference
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/creativity
appliesTo:
  - "[[EVD - Ours-SciBERT with combined human and LLM knowledge achieved F1=0.83 and accuracy=0.84 on method novelty prediction - @wuAutomatedNoveltyEvaluationa]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc7-76ed-a2da-304b27a6345b
type: inferred
severity: moderate
---

## Source

[[@wuAutomatedNoveltyEvaluationa]]

### Limitation

All 2,432 papers in the dataset came exclusively from ICLR 2022, a top machine learning conference focused on deep learning and representation learning. Method novelty at ICLR (Technical Novelty and Significance) may differ substantially in nature, vocabulary, and criteria from novelty in other scientific disciplines (e.g., biology, social science, medicine), limiting generalizability of the trained models and findings.

### Supporting Quote

> [!info] Quotes
> "We obtain our peer-review data from the OpenReview platform. The International Conference on Learning Representations (ICLR) is a premier conference in the field of machine learning. We wrote a web crawler code to retrieve a total of 3376 ICLR papers, each containing peer-review comments and its decision." (Wu et al., 2024, p. 1457) [Inferred: restricting data to a single ML conference means novelty criteria and reviewer language patterns may not transfer to other scientific fields or peer-review systems.]
>
> ![[wuAutomatedNoveltyEvaluationa-cvt-p6-1.png]]

### Applies To

[[EVD - Ours-SciBERT with combined human and LLM knowledge achieved F1=0.83 and accuracy=0.84 on method novelty prediction - @wuAutomatedNoveltyEvaluationa]]

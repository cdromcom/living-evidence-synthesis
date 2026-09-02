---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/construct-validity
  - cvt/mechanism/self-reported-ground-truth
  - cvt/mechanism/proxy-metric
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper pairs - @liuReviewerGPTExploratoryStudy2023]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6ba8-72e1-aaef-820bdf75ff84
type: inferred
severity: moderate
---

## Source

[[@liuReviewerGPTExploratoryStudy2023]]

### Limitation

The ground truth labels for checklist verification were based on the authors' own reported answers ("Yes"), which were then manually relabeled by the study authors. However, 86.6% of author responses already matched the study's ground truth labels, meaning the benchmark may reflect author self-report accuracy rather than objective correctness. There is no independent expert verification of the ground truth.

### Supporting Quote

> [!info] Quotes
> "In a set of 15 papers from NeurIPS 2023, we selected checklist items where the authors answered 'Yes', manually labeled their ground truth answers, and prompted the LLM to answer the same checklist items by providing the relevant section(s) of the paper." (Liu & Shah, 2023, p. 2)
>
> ![[liuReviewerGPTExploratoryStudy2023-quote-checklistGT-p2.png]]
>
> [Inferred: Ground truth derived from author self-reports introduces circularity; the benchmark may measure agreement with author self-assessment rather than with an objective standard of compliance.]

### Applies To

[[EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper pairs - @liuReviewerGPTExploratoryStudy2023]]

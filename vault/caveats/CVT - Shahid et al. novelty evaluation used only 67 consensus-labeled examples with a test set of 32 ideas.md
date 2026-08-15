---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/statistical-rigor
  - cvt/mechanism/small-sample
  - cvt/mechanism/low-power
  - cvt/type/author-stated
  - cvt/severity/high
  - 5c/creativity
appliesTo:
  - "[[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]"
  - "[[EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set - @shahidLiteratureGroundedNoveltyAssessment2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb7-709c-bc82-c139eb9edf35
type: author-stated
severity: high
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

### Limitation

The evaluation dataset consists of only 67 consensus-labeled examples (35 training, 32 test), which is a very small sample for evaluating a machine learning system. Results may not generalize and are sensitive to the specific distribution of ideas included in the formative study.

### Supporting Quote

> [!info] Quotes
> "From our formative study, we collected 67 consensus-labeled examples (39 labeled as novel and 28 as non-novel). We split into train and test sets (35 for training and 32 for testing) with a balanced distribution of novel and non-novel ideas." (Shahid et al., 2025, p. 5)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-cvt-p5-1.png]]
> "While Idea Novelty Checker is superior in many aspects, it also has some limitations. For instance, due to context size constraints (with fifteen in-context examples for both novel and not novel categories), our analysis is restricted to the top 10 retrieved papers." (Shahid et al., 2025, p. 8)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-cvt-p8-2.png]]

### Applies To

- [[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]

- [[EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set - @shahidLiteratureGroundedNoveltyAssessment2025]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/data-leakage
  - cvt/mechanism/test-contamination
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
appliesTo:
  - "[[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]"
  - "[[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49 - @bougieGenerativeAdversarialReviews2024a]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6ba8-72e1-aaef-820cdb50beed
type: author-stated
severity: moderate
---

## Source

[[@bougieGenerativeAdversarialReviews2024a]]

### Limitation

Papers from ICLR 2022 and 2023 used as the evaluation dataset may have been included in the LLM training corpora, enabling the model to recall previously seen reviews rather than generating genuinely novel assessments. This data contamination could inflate performance metrics, making it appear that GAR generates higher quality reviews than it would in a true out-of-distribution setting.

### Supporting Quote

> [!info] Quotes
> "Furthermore, we must question: Are we certain that these papers are not already part of the LLMs' training corpus? If such overlap exists, it could inadvertently introduce bias, as the model may demonstrate familiarity with the content, concepts, or style of certain papers, providing an unfair advantage or skewing evaluations. This issue is particularly pronounced for widely circulated preprints or seminal works that are likely to have influenced the training datasets of LLMs." (Bougie & Watanabe, 2024, p. 17)
>
> ![[bougieGenerativeAdversarialReviews2024a-cvt-p18-1.png]]

### Applies To

- [[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]

- [[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49 - @bougieGenerativeAdversarialReviews2024a]]

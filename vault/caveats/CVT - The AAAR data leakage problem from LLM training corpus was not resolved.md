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
  - "[[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]"
  - "[[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb9-72ce-a08c-0fe4f108105b
type: author-stated
severity: moderate
---

## Source

[[@louAAAR10AssessingAIs2025]]

### Limitation

The AAAR benchmark data was collected from open platforms (arXiv, OpenReview), creating the possibility that current or future LLMs were pretrained on some of the benchmark papers, making performance an upper bound rather than a true test of generalization.

### Supporting Quote

> [!info] Quotes
> "As we gather data from open-source platforms such as arXiv and OpenReview, there is a possibility that current or future LLMs may be trained on the same source data utilized in our benchmark. This situation could influence the fairness of LLM comparisons and the conclusions drawn from this paper." (Lou et al., 2025, p. 11)
>
> ![[louAAAR10AssessingAIs2025-cvt-p11-1.png]]

### Applies To

- [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]

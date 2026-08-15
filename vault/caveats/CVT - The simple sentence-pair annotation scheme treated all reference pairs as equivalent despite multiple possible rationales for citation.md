---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/construct-validity
  - cvt/mechanism/proxy-metric
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/connectivity
appliesTo:
  - "[[EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts - @zhangDetectingReferenceErrors2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc9-75fb-a95b-cb0b5f2118f6
type: author-stated
severity: moderate
---

## Source

[[@zhangDetectingReferenceErrors2024]]

### Limitation

The annotation scheme used a simple three-way label (Unsubstantiated, Partially substantiated, Fully substantiated) applied to individual sentence-reference pairs, treating each pair in isolation despite the fact that a single statement may cite a reference for multiple legitimate reasons. This may have introduced noise into both human annotations and LLM evaluation targets.

### Supporting Quote

> [!info] Quotes
> "Other limitations included our reliance on publicized and crowd-sourced datasets, the use of a simple sentence pair annotation scheme, and the treatment of all reference pairs as being equivalent despite potential multiple rationales for citation." (Zhang & Abernethy, 2024, p. 5)
>
> ![[zhangDetectingReferenceErrors2024-cvt-p5-2.png]]

### Applies To

[[EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts - @zhangDetectingReferenceErrors2024]]

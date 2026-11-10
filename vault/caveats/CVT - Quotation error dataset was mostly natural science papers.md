---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - The quotation error dataset was predominantly from natural science journal articles limiting generalizability to conference papers and other publication channels"
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-discipline
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/connectivity
appliesTo:
  - "[[EVD - GPT-4 Turbo detected quotation errors at 70.0% accuracy - @zhangDetectingReferenceErrors2024|EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts]]"
  - "[[EVD - GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context - @zhangDetectingReferenceErrors2024|EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0%]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc8-7307-95d7-b3f0667e0ff7
type: author-stated
severity: moderate
title: "The quotation error dataset was predominantly from natural science journal articles limiting generalizability to conference papers and other publication channels"
---

## Source

[[@zhangDetectingReferenceErrors2024]]

### Limitation

All statement-reference pairs in the dataset came from journal articles and were predominantly in natural science domains. This limits generalizability to papers published through other channels (conferences, preprints) or in research domains underrepresented in the study (e.g., humanities, engineering, computer science).

### Supporting Quote

> [!info] Quotes
> "all statement-references pairs in our dataset came from journal articles and were predominantly in natural science domains. Such characteristics limit the generalizability of our findings to papers that are published through other channels (e.g., conferences and preprint platforms) or in research domains that are underrepresented in this study." (Zhang & Abernethy, 2024, p. 5)
>
> ![[zhangDetectingReferenceErrors2024-cvt-p5-1.png]]

### Applies To

- [[EVD - GPT-4 Turbo detected quotation errors at 70.0% accuracy - @zhangDetectingReferenceErrors2024|EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts]]

- [[EVD - GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context - @zhangDetectingReferenceErrors2024|EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0%]]

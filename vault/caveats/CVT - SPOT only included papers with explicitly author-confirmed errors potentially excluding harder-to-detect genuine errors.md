---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/selection-bias
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]"
  - "[[EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb4-763c-994e-d9feb2027181
type: author-stated
severity: moderate
---

## Source

[[@sonWhenAICoScientists2025]]

### Limitation

SPOT exclusively includes errors that were explicitly acknowledged by the original authors (via errata or retraction). This selection criterion means the benchmark may not represent the full distribution of errors in scientific manuscripts — subtle or contested errors that authors did not formally acknowledge are excluded, potentially making the benchmark easier than real-world error detection.

### Supporting Quote

> [!info] Quotes
> "For remaining manuscripts, we only retain those the original authors directly confirmed. Specifically, we only retain PubPeer comments followed by an explicit author response acknowledging the mistake and treat WithdrArXiv self-retractions as definitive evidence of a critical error. While some errors may appear to be evident, we do not include any error with explicit acknowledgment from the original authors." (Son et al., 2025, p. 3)
>
> ![[sonWhenAICoScientists2025-cvt-p3-2.png]]

### Applies To

- [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]

- [[EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]]

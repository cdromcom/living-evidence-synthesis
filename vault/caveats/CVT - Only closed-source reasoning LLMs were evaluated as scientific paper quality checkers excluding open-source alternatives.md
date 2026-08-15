---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/closed-source-only
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]"
  - "[[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb1-73e2-92cf-08f92086497b
type: author-stated
severity: moderate
---

## Source

[[@zhangReviewingScientificPapers2025a]]

### Limitation

Only closed-source reasoning LLMs (Gemini, o3, o4-mini, Claude) were tested. Open-source reasoning models were not evaluated, limiting the ability to draw conclusions about whether the pattern of results (o-series superiority, Claude underperformance on PDFs) generalizes beyond proprietary systems or reflects vendor-specific PDF ingestion pipelines.

### Supporting Quote

> [!info] Quotes
> "First, only closed-source reasoning LLMs were evaluated. Future work can consider comparing different PDF preprocessing pipelines and open-source LLMs." (Zhang & Abernethy, 2025, p. 5)
>
> ![[zhangReviewingScientificPapers2025a-cvt-p5-1.png]]

### Applies To

- [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]

- [[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]]

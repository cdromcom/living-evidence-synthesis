---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-discipline
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]"
  - "[[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc5-750b-9ed5-815eff6dde5f
type: author-stated
severity: moderate
---

## Source

[[@zhangReviewingScientificPapers2025a]]

### Limitation

The WITHDRARXIV-CHECK dataset consists predominantly of math (52%) and physics (29%) papers withdrawn from arXiv. Errors in these fields tend to involve formal proofs and equations, which may be structurally different from errors in empirical sciences (e.g., biology, medicine, social science). Results may therefore overstate or understate model performance in other scientific domains.

### Supporting Quote

> [!info] Quotes
> "our results based on a dataset rich in math and physics papers published in the past may not generalize well to papers in other scientific domains or future papers." (Zhang & Abernethy, 2025, p. 5)
>
> ![[zhangReviewingScientificPapers2025a-cvt-p5-2.png]]

### Applies To

- [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]

- [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]]

---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - The error detection dataset was rich in math and physics papers and may not generalize to other scientific domains"
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-discipline
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - o3 led reasoning LLMs with 48.2% hit rate on PDF and 50.6% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]"
  - "[[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 11.0%|EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 11.0% hit rate as a PDF-based scientific quality checker]]"
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6bc5-750b-9ed5-815eff6dde5f
type: author-stated
severity: moderate
title: "The error detection dataset was rich in math and physics papers and may not generalize to other scientific domains"
---

## Source

[[@zhangReviewingScientificPapers2025a]]

### Limitation

The WITHDRARXIV-CHECK dataset consists predominantly of math (52%) and physics (29%) papers withdrawn from arXiv. Errors in these fields tend to involve formal proofs and equations, which may be structurally different from errors in empirical sciences (e.g., biology, medicine, social science). Results may therefore overstate or understate model performance in other scientific domains.

### Supporting Quote

> [!info] Quotes
> "our results based on a dataset rich in math and physics papers published in the past may not generalize well to papers in other scientific domains or future papers." (Zhang & Abernethy, 2026, p. 7)
>
> ![[zhangReviewingScientificPapers2025a-v3-cvt-domain-p7.png]]

### Applies To

- [[EVD - o3 led reasoning LLMs with 48.2% hit rate on PDF and 50.6% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]

- [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 11.0%|EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 11.0% hit rate as a PDF-based scientific quality checker]]

---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/closed-source-only
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[sysrev/dgraph/evidence/EVD - o3 led reasoning LLMs with 48.2% hit rate on PDF and 50.6% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]"
  - "[[sysrev/dgraph/evidence/EVD - o4-mini reached 38.0% HR@5 at 0.038 USD per paper vs 0.064 USD for o3|EVD - o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper]]"
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6bb1-73e2-92cf-08f92086497b
type: author-stated
severity: moderate
title: Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives
---

## Source

[[sysrev/dgraph/source/@zhangReviewingScientificPapers2025a]]

### Limitation

Only closed-source reasoning LLMs (Gemini, o3, o4-mini, Claude) were tested. Open-source reasoning models were not evaluated, limiting the ability to draw conclusions about whether the pattern of results (o-series superiority, Claude underperformance on PDFs) generalizes beyond proprietary systems or reflects vendor-specific PDF ingestion pipelines.

### Supporting Quote

> [!info] Quotes
> "First, only closed-source reasoning LLMs were evaluated. Future work may consider comparing different PDF preprocessing pipelines and open-source LLMs." (Zhang & Abernethy, 2026, p. 7)
>
> ![[zhangReviewingScientificPapers2025a-v3-cvt-closed-p7.png]]

### Applies To

- [[sysrev/dgraph/evidence/EVD - o3 led reasoning LLMs with 48.2% hit rate on PDF and 50.6% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]

- [[sysrev/dgraph/evidence/EVD - o4-mini reached 38.0% HR@5 at 0.038 USD per paper vs 0.064 USD for o3|EVD - o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper]]

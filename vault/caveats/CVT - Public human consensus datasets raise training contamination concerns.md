---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - Human consensus datasets used as comparators were openly available online raising train test contamination concerns"
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/data-leakage
  - cvt/mechanism/test-contamination
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/clarity
  - 5c/credibility
appliesTo:
  - "[[EVD - Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans|EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans]]"
  - "[[EVD - Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74%|EVD - Combined LLMs with consistency approach reached 75-88 percent accuracy for PRISMA while deferring 4-74 percent of ratings]]"
  - "[[EVD - Human-AI collaboration reached up to 96% on PRISMA surpassing human raters|EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters]]"
created: 2026-04-27
updated: 2026-04-29
nodeID: 019ddb4e-6baa-75e9-b1ee-459f9a348dfd
type: author-stated
severity: moderate
title: "Human consensus datasets used as comparators were openly available online raising train test contamination concerns"
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

### Limitation

The human consensus datasets used to grade LLM performance (PRISMA/AMSTAR ratings from Cullis et al., PRECIS-2 ratings from PragMeta) are openly available on the internet, so the LLMs may have seen the labels during pretraining. The authors argue tabular CSV/Excel formats are unlikely training corpus material, but this cannot be definitively ruled out. Only prospective replication on freshly-rated datasets would eliminate the train/test contamination risk.

### Supporting Quote

> [!info] Quotes
> "First, there is a general concern about 'train/test contamination' or 'data leakage' with all LLM benchmarks because of the extensive web scraping used for their training." (Woelfle et al., 2024, p. 9, Limitations)
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-quote-contamination-p9-09.png]]

### Applies To

- [[EVD - Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans|EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans]]

- [[EVD - Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74%|EVD - Combined LLMs with consistency approach reached 75-88 percent accuracy for PRISMA while deferring 4-74 percent of ratings]]

- [[EVD - Human-AI collaboration reached up to 96% on PRISMA surpassing human raters|EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters]]

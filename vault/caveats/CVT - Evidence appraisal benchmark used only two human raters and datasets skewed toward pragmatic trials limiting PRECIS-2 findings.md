---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-rater
  - cvt/mechanism/selection-bias
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/clarity
  - 5c/credibility
appliesTo:
  - "[[EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans - @woelfleBenchmarkingHumanAICollaboration2024]]"
  - "[[EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters - @woelfleBenchmarkingHumanAICollaboration2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6ba9-7686-b617-0de0beac864c
type: author-stated
severity: moderate
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

### Limitation

The human consensus benchmark used only two raters per publication, which may not constitute a robust ground truth. Additionally, the PRECIS-2 dataset contained mostly pragmatic trials and few explanatory ones, potentially biasing performance comparisons between LLMs in ways that do not reflect general performance on balanced datasets.

### Supporting Quote

> [!info] Quotes
> "Fifth, the presented datasets contain ratings from only two human experts, whereas a higher number would make the human consensus more robust and eventually approximate a 'ground truth' — a strong term which cannot be claimed for the presented datasets." (Woelfle et al., 2024, pp. 9–10, Limitations)
>
> The fifth-limitation passage crosses the page 9 → page 10 boundary:
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-quote-tworaters-p9-09.png]]
> ![[woelfleBenchmarkingHumanAICollaboration2024-quote-tworaters-p10-10.png]]
>
> "Second, as discussed above, the dataset used in this study to assess PRECIS-2 contains mostly pragmatic trials and few explanatory ones. A more balanced dataset could complement the current findings and challenge the surprising superiority of GPT-3.5 and Mixtral-8x22B compared to larger models." (Woelfle et al., 2024, p. 9, Limitations)
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-quote-precis2dataset-p9-09.png]]

### Applies To

- [[EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans - @woelfleBenchmarkingHumanAICollaboration2024]]

- [[EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters - @woelfleBenchmarkingHumanAICollaboration2024]]

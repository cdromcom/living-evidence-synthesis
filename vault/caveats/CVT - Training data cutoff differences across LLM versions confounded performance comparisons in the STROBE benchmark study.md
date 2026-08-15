---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/training-cutoff-confound
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/clarity
  - 5c/credibility
appliesTo:
  - "[[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]]"
  - "[[EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions - @akyonEvaluatingCapabilitiesGenerative2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bcc-7519-b971-3ab0ca5fc00c
type: author-stated
severity: moderate
---

## Source

[[@akyonEvaluatingCapabilitiesGenerative2024]]

### Limitation

Different LLMs had different training data cutoff dates, meaning the 39 test articles were not equally represented in each model's training data. GPT-4-1106 had access to all 39 articles (April 2023 cutoff); GPT-3.5-turbo and GPT-4-0613 had access to only 28 (September 2021 cutoff). For Claude v1, Palm 2, and Gemini pro, cutoff dates were unknown. This creates a confound: performance differences between models may partially reflect differences in training data coverage rather than differences in comprehension capability.

### Supporting Quote

> [!info] Quotes
> "This lack of transparency regarding training data limits our ability to definitively assess the impact of knowledge cutoffs on model performance. The observation that all 39 articles were published before the cutoff date for GPT-4-1106, while only 28 articles were published before the cutoff date for GPT-3.5-turbo and GPT-4-0613, suggests that the knowledge cutoff may play a role in the observed performance differences." (Akyon et al., 2024, p. 20)
>
> ![[akyonEvaluatingCapabilitiesGenerative2024-cvt-p17-1.png]]

### Applies To

- [[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]]

- [[EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions - @akyonEvaluatingCapabilitiesGenerative2024]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/single-domain
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams - @huntington-kleinLLMsActRepositories2024]]"
  - "[[EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.16 across prompt variations - @huntington-kleinLLMsActRepositories2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bba-70a7-8bd7-a8dbca60a07c
type: inferred
severity: moderate
---

## Source

[[@huntington-kleinLLMsActRepositories2024]]

### Limitation

The study examined LLM causal knowledge using a single, well-known case study (the Coronary Drug Project), which is specifically likely to be represented in LLM training data. Results may not generalize to other causal inference contexts where ground truth is less available in the training corpus.

### Supporting Quote

> [!info] Quotes
> "we use the case of confounding in the Coronary Drug Project (CDP), for which there are several studies listing expert-selected confounders that can serve as a ground truth." (Huntington-Klein & Murray, 2024, p. 1) [Inferred: Using a single, famous case study limits the scope of conclusions. The CDP is specifically chosen because it is likely in LLM training data, but this selection criterion means findings may not generalize to cases where expert knowledge is less available in training corpora.]
>
> ![[huntington-kleinLLMsActRepositories2024-cvt-p1-1.png]]

### Applies To

- [[EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams - @huntington-kleinLLMsActRepositories2024]]

- [[EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.16 across prompt variations - @huntington-kleinLLMsActRepositories2024]]

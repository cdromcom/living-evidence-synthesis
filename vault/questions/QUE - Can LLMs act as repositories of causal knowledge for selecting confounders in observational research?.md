---
NodeFormality: ReadyForInternal
aliases:
tags:
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bd2-70bc-b334-e31d0e971745
---
### Key Papers Asking Question

> [!info] Papers
> [[@huntington-kleinLLMsActRepositories2024]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "We aim to test whether LLMs can return causal judgements about a set of potential confounders. Specifically, we examine the Coronary Drug Project (CDP), an experimental study with imperfect compliance for which expert opinion about the covariates necessary to adjust for imperfect compliance are both available to us as a ground truth, and potentially in the LLM's training data for them to report back." (Huntington-Klein & Murray, 2024, p. 3)
> ![[huntington-kleinLLMsActRepositories2024-que-p2-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]]
    - [[EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.16 across prompt variations - @huntington-kleinLLMsActRepositories2024]]
    - [[EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams - @huntington-kleinLLMsActRepositories2024]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]
- [[EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs]]
- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]

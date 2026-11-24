---
NodeFormality: ReadyForInternal
human_reviewed: no
TruthValue: 0.5
aliases:
  - "CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection"
tags:
  - task/causal-inference-judgment
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b9d-761c-91d0-c7b5c7bcfc66
title: "LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection"
---
### Key Papers Making This Claim

> [!info] Papers
> [[@huntington-kleinLLMsActRepositories2024]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "LLMs do not yet have the ability to automate the reporting of causal links." (Huntington-Klein & Murray, 2026, p. 1)
>
> ![[huntington-kleinLLMsActRepositories2024-clm-v2026-p1-1.png]]
>
> "In our setting, we find some moderate but mixed success in having LLMs produce confounder designations that match expert opinion. There are some cases in which the LLMs are able to match expert opinion a large share of the time, and in many cases, the LLM is able to categorize more than 70 % of expert-designated confounders as confounders. However, the LLM also designated as confounders a high number of variables in the “Trimmed” or “Non-Confounders” categories, which were, respectively, removed from the causal diagram as unnecessary, or specifically designated as non-confounders." (Huntington-Klein & Murray, 2026, p. 19)
>
> ![[huntington-kleinLLMsActRepositories2024-clm-v2026-p19-1.png]]

- PDF check 2026-11-24: quote "We find some moderate but mixed success ... in most cases, the LLM is able to categorize more than 70% ... 'Trimmed' or 'Non-Confounders' categories." (Huntington-Klein & Murray, 2024, p. 17) -> the journal passage "In our setting, we find some moderate but mixed success ... in many cases, the LLM is able to categorize more than 70 % ... categories, which were, respectively, removed from the causal diagram as unnecessary, or specifically designated as non-confounders." (Huntington-Klein & Murray, 2026, p. 19); "most cases" -> "many cases", "70%" -> "70 %", straight quotes -> curly quotes, one clause added at the end; the abstract quote is unchanged apart from the year (2026, p. 1); screenshots recreated from the 2026 PDF

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim; verify before citing)

- [[EVD - LLM confounder choices were highly inconsistent with kappa as low as 0.13|EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.13 across prompt variations]]

- [[EVD - LLMs flagged expert and trimmed confounders at similar rates|EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams]]

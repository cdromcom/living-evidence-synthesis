---
NodeFormality: ReadyForInternal
human_reviewed: no
TruthValue: 0.5
aliases:
  - "CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection"
tags:
  - task/error-detection
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6ba1-725a-a256-887c61b711f1
title: "Proprietary reasoning models substantially outperform open-source models on scientific error detection"
---
### Key Papers Making This Claim

> [!info] Papers
> [[@sonWhenAICoScientists2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "While neither proprietary nor open-source models fully satisfy the requirements of practical deployments of error-detecting AI systems, open-source models lag far behind in domain-specific rigor and robust error-detection capabilities essential for scientific applications." (Son et al., 2025, p. 6)
>
> ![[sonWhenAICoScientists2025-clm-p6-1.png]]
> "The divide between proprietary and open models is vast in the multi-modal setting, proprietary systems maintain substantial recall (e.g., o3 at 34.6%, Gemini-2.5-Pro at 13.7%) and pass@4, whereas open-source models collapse to near zero." (Son et al., 2025, p. 7)
>
> ![[sonWhenAICoScientists2025-clm-p7-1.png]]

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim; verify before citing)

- [[EVD - LLM confidence was near zero across 498 SPOT evaluations - @sonWhenAICoScientists2025|EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]]

- [[EVD - o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication - @sonWhenAICoScientists2025|EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]]

- [[EVD - o3 led SPOT with 37.8% pass@4 - @sonWhenAICoScientists2025|EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]

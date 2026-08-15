---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/statistical-rigor
  - cvt/mechanism/small-sample
  - cvt/mechanism/low-power
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/credibility
appliesTo:
  - "[[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]"
  - "[[EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb3-7436-879b-1256d66f19e9
type: inferred
severity: moderate
---

## Source

[[@sonWhenAICoScientists2025]]

### Limitation

The SPOT benchmark contains only 83 manuscripts with 91 annotated errors. Some error categories have very few instances (e.g., Statistical Reporting: 4, Reagent Identity: 3, Experiment Setup: 2), making category-level performance estimates unreliable and limiting the statistical power of cross-model comparisons.

### Supporting Quote

> [!info] Quotes
> "The final SPOT benchmark comprises 83 manuscripts with 91 annotated errors. Although modest in size, our dataset aligns with recent trends toward compact, high-quality benchmarks: MT-Bench (80 items), GPQA-D (198 items), AIME 2024/2025 (30 items each), USAMO 2025 (6 items) and PaperBench (20 items)." (Son et al., 2025, p. 3)
>
> ![[sonWhenAICoScientists2025-cvt-p3-1.png]]
> [Inferred: With only 4, 3, and 2 instances in Statistical Reporting, Reagent Identity, and Experiment Setup categories, per-category performance statistics have extremely high variance and cannot support reliable conclusions about model capabilities in these error types.]

### Applies To

- [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]

- [[EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/reproducibility
  - cvt/mechanism/prompt-sensitivity
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/creativity
appliesTo:
  - "[[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]"
  - "[[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bac-717c-b0c4-aaa4aaf2b955
type: author-stated
severity: moderate
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

### Limitation

LLMs exhibit substantial sensitivity to prompt variations in novelty evaluation tasks. Minor differences in wording, instruction framing, or structure can lead to significant performance differences (e.g., prompt 3 with accuracy=0 vs. prompt 9 with accuracy=0.6 from nearly identical instruction sets), making results hard to replicate and raising concerns about the stability of LLM-based novelty judgments.

### Supporting Quote

> [!info] Quotes
> "Our analysis highlights the LLM's sensitivity to prompt design when assessing novelty of an idea. Even minor variations in wording and structure can lead to substantial performance changes, emphasizing the need for careful prompt engineering and well-chosen in-context examples to guide the LLM for idea novelty evaluation." (Shahid et al., 2025, p. 8)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-cvt-p8-1.png]]

### Applies To

- [[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]

- [[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]]

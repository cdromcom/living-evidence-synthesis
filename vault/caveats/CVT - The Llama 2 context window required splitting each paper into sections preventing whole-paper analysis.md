---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/excluded-cases
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/clarity
appliesTo:
  - "[[EVD - Fine-tuned Llama 2 improved from F1=0.63 (64% accuracy) to F1=0.84 (83% accuracy) on CONSORT guideline questions - @wrightsonGPTRCTsUsing2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bbf-74eb-aad8-2d8b771d294a
type: author-stated
severity: moderate
---

## Source

[[@wrightsonGPTRCTsUsing2025]]

### Limitation

The open-source Llama 2 model's context window was limited to 512 tokens for model responses and required dividing each paper into three sections (introduction, methods, results) for analysis. This fragmented approach may have degraded performance compared to whole-paper analysis and prevented Llama 2 from answering question 9 (which required combining method and results text).

### Supporting Quote

> [!info] Quotes
> "Limits on the size of the text that could be passed to the open-source Llama 2 model meant each paper had to be divided into sections (introduction, methods, results) to be analysed. Performance on whole papers, which require much larger context windows, may vary." (Wrightson et al., 2025, p. 1)
>
> ![[wrightsonGPTRCTsUsing2025-cvt-p1-1.png]]

### Applies To

[[EVD - Fine-tuned Llama 2 improved from F1=0.63 (64% accuracy) to F1=0.84 (83% accuracy) on CONSORT guideline questions - @wrightsonGPTRCTsUsing2025]]

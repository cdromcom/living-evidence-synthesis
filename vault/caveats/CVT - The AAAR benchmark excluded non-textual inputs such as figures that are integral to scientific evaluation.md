---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/excluded-cases
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
appliesTo:
  - "[[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]"
  - "[[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]"
  - "[[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb8-768b-99d5-407c9533ca91
type: inferred
severity: moderate
---

## Source

[[@louAAAR10AssessingAIs2025]]

### Limitation

The AAAR-1.0 EQINFER and EXPDESIGN tasks use LaTeX source as the input, with no rendered figures or tables provided to the LLM. (The WEAKNESS task does include figure/table images.) Limitations grounded in figure-only evidence — such as inconsistencies between text and chart, missing axis labels, or visual overstatements — therefore cannot be flagged on EQINFER/EXPDESIGN.

### Supporting Quote

> [!info] Quotes
> "we adopt the pre-compilation LaTeX code for two reasons: i) existing PDF parsing tools, such as PyMuPDF and PaperMage (Lo et al., 2023), can introduce considerable noise to the parsed equation text; ii) considering most of existing LLMs are capable with processing LaTeX code, using LaTeX source instead of parsed text can be more accurate and provide LLMs with richer information." (Lou et al., 2025, p. 3)
>
> ![[louAAAR10AssessingAIs2025-cvt-p3-1.png]]
>
> [Inferred: LaTeX source preserves equation fidelity but elides rendered figures. The original CVT-supporting quote attributed to p. 11 was not found in the paper on this pass and has been replaced with a real anchor describing the input format. The note is now flagged inferred.]

### Applies To

- [[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]

- [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]

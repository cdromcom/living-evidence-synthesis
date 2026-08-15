---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/excluded-cases
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/connectivity
appliesTo:
  - "[[EVD - 39.18% of 3063 annotated biomedical citation instances contained accuracy errors - @sarolAssessingCitationIntegrity2024]]"
  - "[[EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification - @sarolAssessingCitationIntegrity2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb6-76a7-a86f-ebb132c3f50d
type: author-stated
severity: moderate
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

### Limitation

The annotation and NLP evaluation excluded citation cases where the relevant evidence was in tables, figures, or supplementary material. This is described as "fairly common" and represents a systematic gap in both the corpus and the model evaluations, likely underestimating the true difficulty and rate of citation errors.

### Supporting Quote

> [!info] Quotes
> "We excluded cases in which the relevant evidence was in tables/figures or in Supplementary Material, which is fairly common." (Sarol et al., 2024, p. 7)
>
> ![[sarolAssessingCitationIntegrity2024-quote-cvt-excluded-p7.png]]

### Applies To

- [[EVD - 39.18% of 3063 annotated biomedical citation instances contained accuracy errors - @sarolAssessingCitationIntegrity2024]]

- [[EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification - @sarolAssessingCitationIntegrity2024]]

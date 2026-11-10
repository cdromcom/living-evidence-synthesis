---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data"
tags:
  - cvt/domain/construct-validity
  - cvt/mechanism/low-iaa
  - cvt/type/author-stated
  - cvt/severity/high
  - 5c/connectivity
appliesTo:
  - "[[EVD - Annotator agreement on citation labels was only kappa 0.18-0.31|EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2]]"
  - "[[EVD - MultiVerS reached micro-F1 0.59 on citation accuracy|EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification]]"
  - "[[EVD - GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate|EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bae-7063-b6ba-086b938022c4
type: author-stated
severity: high
title: "Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data"
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

### Limitation

Inter-annotator agreement for evidence sentence identification and citation accuracy classification was low (κ=0.18–0.31 for accuracy labels), even after multiple reconciliation phases. This low agreement reflects the inherent difficulty of citation error detection and introduces noise into the training and evaluation data, making model performance estimates less reliable.

### Supporting Quote

> [!info] Quotes
> "Our annotation yielded fair inter-annotator agreement for evidence sentence annotation and citation accuracy classification. Hiring annotators with specific expertise in the topic areas of the reference papers could have improved agreement, but was not feasible." (Sarol et al., 2024, p. 7)
>
> ![[sarolAssessingCitationIntegrity2024-quote-cvt-iaa-p7.png]]

### Applies To

- [[EVD - Annotator agreement on citation labels was only kappa 0.18-0.31|EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2]]

- [[EVD - MultiVerS reached micro-F1 0.59 on citation accuracy|EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification]]

- [[EVD - GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate|EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations]]

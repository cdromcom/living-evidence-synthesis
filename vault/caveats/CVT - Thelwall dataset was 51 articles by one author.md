---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "CVT - The Thelwall dataset consisted of 51 articles by a single author limiting generalizability to other researchers and fields"
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/small-sample
  - cvt/mechanism/self-evaluation
  - cvt/mechanism/single-rater
  - cvt/type/author-stated
  - cvt/severity/high
  - 5c/credibility
appliesTo:
  - "[[EVD - GPT-4o abstract scores correlated r=0.67 with humans|EVD - GPT-4o abstracts achieved Spearman r=0.67 with human quality scores on 51 information science articles the highest reported]]"
  - "[[EVD - Full text scored worse than abstracts for 3 ChatGPT models|EVD - Full text input produced lower Spearman correlations than abstracts for all three ChatGPT models tested]]"
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6bc2-7023-bcd6-57074892d4ef
type: author-stated
severity: high
title: "The Thelwall dataset consisted of 51 articles by a single author limiting generalizability to other researchers and fields"
---

## Source

[[@thelwallEvaluatingResearchQuality2024]]

### Limitation

The entire dataset consists of 51 articles written by a single author (the researcher himself), who also provided the quality scores (self-evaluations). This means the quality judgments may not reflect external expert assessments and the articles are not representative of the broader research landscape.

### Supporting Quote

> [!info] Quotes
> "The data is a convenience sample of the work of a single author, it only includes one field, and the scores are self-evaluations." (Thelwall, 2025, p. 7)
>
> ![[thelwallEvaluatingResearchQuality2024-cvt-p1-2.png]]
>
> "This dataset is not ideal since (a) it is part of a single author's output and therefore not representative even of its field, (b) the author's scores are less relevant than the scores of more independent and less expert (on this topic) senior researchers, who would be the ones forming the evaluations in the most important context (e.g., the REF or promotion/appointment)." (Thelwall, 2025, p. 10)
>
> ![[thelwallEvaluatingResearchQuality2024-cvt-p4-1.png]]

### Applies To

- [[EVD - GPT-4o abstract scores correlated r=0.67 with humans|EVD - GPT-4o abstracts achieved Spearman r=0.67 with human quality scores on 51 information science articles the highest reported]]

- [[EVD - Full text scored worse than abstracts for 3 ChatGPT models|EVD - Full text input produced lower Spearman correlations than abstracts for all three ChatGPT models tested]]

### PDF check

- PDF check 2026-11-24: source version: pages now cite the 2025 journal article (J Data Inf Sci 10(1), 7-25, doi 10.2478/jdis-2025-0011) with printed journal page numbers; the 2024 preprint is kept as "Archive - Thelwall - 2024.pdf"
- PDF check 2026-11-24: citation of "The data is a convenience sample of the work of a single aut..." (Thelwall, 2024, p. 1) -> (Thelwall, 2025, p. 7)
- PDF check 2026-11-24: quote "this dataset is not ideal since (a) it is part of a single author's ou..." -> verbatim journal wording: "This dataset is not ideal since (a) it is part of a single author's output and therefore not representative even of its field, (b) the author's scores are less relevant than the scores of more independent and less expert (on this topic) senior researchers, who would be the ones forming the evaluations in the most important context (e.g., the REF or promotion/appointment)." (journal sentence starts with a capital "This"; the old quote ended "senior researchers." with a full stop the paper does not have, so the quote now runs to the end of the sentence)
- PDF check 2026-11-24: citation of "this dataset is not ideal since (a) it is part of a single a..." (Thelwall, 2024, p. 3) -> (Thelwall, 2025, p. 10)

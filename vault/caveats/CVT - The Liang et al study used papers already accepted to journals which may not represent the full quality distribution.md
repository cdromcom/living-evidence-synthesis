---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/external-validity
  - cvt/mechanism/selection-bias
  - cvt/mechanism/publication-bias
  - cvt/type/inferred
  - cvt/severity/low
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
appliesTo:
  - "[[EVD - GPT-4 feedback overlapped 30.85% with individual human reviewers on Nature journals comparable to human-human overlap of 28.58% - @liangCanLargeLanguage2024a]]"
  - "[[EVD - GPT-4 commented on research implications 7.27x more than humans and on novelty 10.69x less on ICLR papers - @liangCanLargeLanguage2024a]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bbb-71a0-b296-59640f76d037
type: inferred
severity: low
---

## Source

[[@liangCanLargeLanguage2024a]]

### Limitation

The retrospective analysis used already-accepted papers from Nature journals and ICLR, meaning the full feedback loop (where LLM feedback could shape decisions) is not tested and the quality distribution may differ from the mix of papers typically seen in pre-submission review.

### Supporting Quote

> [!info] Quotes
> "This dataset, although narrower in scope, includes complete reviews for both accepted and rejected papers." (Liang et al., 2024, p. 2)
>
> ![[liangCanLargeLanguage2024a-quote-cvt-accepted-p2.png]]
>
> [Inferred: The Nature dataset includes only accepted papers; only the ICLR dataset has rejected papers. So LLM feedback quality is assessed predominantly against a high-quality subset of the literature, potentially overestimating its ability to flag issues in weaker papers.]

### Applies To

[[EVD - GPT-4 feedback overlapped 30.85% with individual human reviewers on Nature journals comparable to human-human overlap of 28.58% - @liangCanLargeLanguage2024a]]

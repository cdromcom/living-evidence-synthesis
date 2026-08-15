---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/construct-validity
  - cvt/mechanism/proxy-metric
  - cvt/type/author-stated
  - cvt/severity/moderate
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
appliesTo:
  - "[[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc0-76f4-936d-5fdc49b0c1a3
type: author-stated
severity: moderate
---

## Source

[[@darcyMARGMultiAgentReview2024]]

### Limitation

The automated evaluation measures comment overlap with human reviewer comments, but this metric is an imperfect proxy because human reviewers do not always identify every reasonable critique, and generated critiques could be valid without matching any specific human comment.

### Supporting Quote

> [!info] Quotes
> "We note that this form of evaluation is imperfect in that real reviewers do not always identify every reasonable critique of a paper, and in some cases they may make critiques that are unreasonable. Thus, the generated review could contain good comments that happen to be different from ones the real reviewers made, or it could miss comments that are actually invalid. Thus, the measured overlap should be treated as a lower bound for the fraction of good-quality comments." (D'Arcy et al., 2024, p. 8)
>
> ![[darcyMARGMultiAgentReview2024-cvt-p8-1.png]]

### Applies To

[[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]

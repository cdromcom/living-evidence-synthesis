---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/llm-as-judge
  - cvt/mechanism/self-evaluation
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
appliesTo:
  - "[[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bc6-7461-92c0-252c173dbcd9
type: inferred
severity: moderate
---

## Source

[[@idahlOpenReviewerSpecializedLarge2025]]

### Limitation

The Review Arena evaluation uses GPT-4o (2024-11-20) as the sole judge to compare OpenReviewer against other LLMs. LLM-as-judge evaluations are known to favor responses from models with similar stylistic or training characteristics to the judge model, potentially inflating OpenReviewer's win rates.

### Supporting Quote

> [!info] Quotes
> "We run an arena-style preference evaluation with an LLM-as-a-judge setup to measure whether OpenReviewer produces better reviews than the other LLMs." (Idahl & Ahmadi, 2025, p. 4–5) [Inferred: LLM-as-judge systems may exhibit systematic biases toward certain response styles or model families. Since GPT-4o is used as judge and is itself one of the systems being evaluated, this creates a potential conflict of interest and may systematically disadvantage OpenReviewer when compared against GPT-4o.]
>
> ![[idahlOpenReviewerSpecializedLarge2025-cvt-p4-1.png]]

### Applies To

[[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]]

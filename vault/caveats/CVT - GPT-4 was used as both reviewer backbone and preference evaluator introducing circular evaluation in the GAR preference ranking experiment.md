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
  - "[[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]"
  - "[[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines - @bougieGenerativeAdversarialReviews2024a]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6baa-75e9-b1ee-459e05170c44
type: inferred
severity: moderate
---

## Source

[[@bougieGenerativeAdversarialReviews2024a]]

### Limitation

GAR agents are powered by GPT-4o-mini, and GPT-4o is used as the primary automated evaluator in the preference ranking and human-likeness experiments. This creates a circularity: the same model family is both generating the reviews and judging their quality. The evaluator may be biased toward outputs produced by models it is closely related to, artificially inflating GAR's apparent performance.

### Supporting Quote

> [!info] Quotes
> "As LLM Evaluators Chiang & Lee (2023) achieve comparable performance with human evaluators, we use GPT-4o to evaluate the generated reviews." (Bougie & Watanabe, 2024, p. 10)
>
> ![[bougieGenerativeAdversarialReviews2024a-cvt-p10-1.png]]
> "All agents are powered by the GPT-4o-mini version of ChatGPT." (Bougie & Watanabe, 2024, p. 9)
>
> ![[bougieGenerativeAdversarialReviews2024a-cvt-p9-1.png]]
> [Inferred: using GPT-4o (from the same model family as GPT-4o-mini which powers GAR) as the evaluator risks in-family preference bias, where the evaluator may systematically favor outputs stylistically similar to its own generation tendencies.]

### Applies To

- [[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]

- [[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines - @bougieGenerativeAdversarialReviews2024a]]

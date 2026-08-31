---
NodeFormality: ReadyForInternal
TruthValue: 0.5
aliases:
tags:
  - task/review-generation
  - 5c/clarity
  - 5c/creativity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b9f-713e-8b67-45044023d764
---
### Key Papers Making This Claim

> [!info] Papers
> [[@darcyMARGMultiAgentReview2024]]
>
> [[@xuCanLLMsIdentify2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "Our system substantially improves the ability of GPT-4 to generate specific and helpful feedback, reducing the rate of generic comments from 60% to 29% and generating 3.7 good comments per paper (a 2.2x improvement)." (D'Arcy et al., 2024, p. 1)
>
> ![[darcyMARGMultiAgentReview2024-clm-multiagent-1-p1.png]]
>
> "Although MARG leverages multi-agent collaboration and generates more comments, successfully identifying more limitations, the feedback it provides still lacks specificity, which is reflected in the fine-grained scores." (Xu et al., 2025, p. 9)
>
> ![[xuCanLLMsIdentify2025-clm-p8-2.png]]

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim — verify before citing)

- [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]

- [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]]

- [[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]

- [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]

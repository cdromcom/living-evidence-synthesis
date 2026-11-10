---
NodeFormality: ReadyForInternal
human_reviewed: no
TruthValue: 0.5
aliases:
  - "CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers"
tags:
  - task/decision-judgment
  - 5c/clarity
  - 5c/creativity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b91-7670-aec8-ec24d6e78ac1
title: "Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers"
---
### Key Papers Making This Claim

> [!info] Papers
> [[@zhouLLMReliableReviewer2024]]
>
> [[@louAAAR10AssessingAIs2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "We claim that it is still too early to trust LLM as automatic scientific paper reviewer. Although there is a chance to get useful and correct results, their current capability is not reliable enough. Especially on questions requiring logic reasoning over long texts or extra knowledge in detail, their performance is still unsatisfactory." (Zhou et al., 2024, p. 9347)
>
> ![[zhouLLMReliableReviewer2024-clm-p9-1.png]]
>
> "LLM has the potential to give meaningful scores and decide on individual statements. However, they are NOT easy to use in practice: seldom fully correct, not critical enough, lack technical details, and struggle with long context." (Zhou et al., 2024, p. 9340)
>
> ![[zhouLLMReliableReviewer2024-clm-p1-1.png]]

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; not all may directly support the claim; verify before citing)

- [[EVD - Claude Opus led AAAR ReviewCritique at 21.99% F1 - @louAAAR10AssessingAIs2025|EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]

- [[EVD - GPT-3.5 predicted review aspect scores at r=0.651 - @zhouLLMReliableReviewer2024|EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given the human-written review - @zhouLLMReliableReviewer2024]]

- [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276 - @zhouLLMReliableReviewer2024|EVD - GPT-4 RR-MCQ macro accuracy was 0.276 and micro accuracy 0.710 on 196 review-revision multiple choice questions - @zhouLLMReliableReviewer2024]]

- [[EVD - Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR - @louAAAR10AssessingAIs2025|EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]

- [[EVD - o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline - @louAAAR10AssessingAIs2025|EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

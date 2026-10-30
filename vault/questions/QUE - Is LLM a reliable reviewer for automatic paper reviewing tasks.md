---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
tags:
  - 5c/clarity
  - 5c/creativity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6be4-74fd-bb05-91d8e33b2b7f
title: "Is LLM a reliable reviewer for automatic paper reviewing tasks?"
---
### Key Papers Asking Question

> [!info] Papers
> [[@zhouLLMReliableReviewer2024]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "can LLM be a qualified and reliable automatic reviewer?" (Zhou et al., 2024, p. 9340)
> ![[zhouLLMReliableReviewer2024-que-p1-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]
    - [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given - @zhouLLMReliableReviewer2024]]
    - [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276 and micro accuracy 0.710 on 196 review-revision multiple - @zhouLLMReliableReviewer2024]]
    - [[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR - @louAAAR10AssessingAIs2025]]
    - [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing]]
    - [[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets - @bougieGenerativeAdversarialReviews2024a]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]
    - [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG - @xuCanLLMsIdentify2025]]
    - [[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR - @louAAAR10AssessingAIs2025]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points - @xuCanLLMsIdentify2025]]
    - [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable]]
    - [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit - @zhangReviewingScientificPapers2025a]]
    - [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all - @zhangReviewingScientificPapers2025a]]
    - [[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 - @zhangReviewingScientificPapers2025a]]

- [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]
    - [[EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - All four LLMs included fundamental ICD elements for all seven case scenarios - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - LLMs performed suboptimally identifying placebo arm suitability and risk - @sridharanLeveragingArtificialIntelligence2025]]

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG - @xuCanLLMsIdentify2025]]
    - [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent - @darcyMARGMultiAgentReview2024]]
    - [[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES - @darcyMARGMultiAgentReview2024]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points - @xuCanLLMsIdentify2025]]

- [[CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect]]
    - [[EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) - @zhangDetectingReferenceErrors2024]]
    - [[EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus - @zhangDetectingReferenceErrors2024]]

- [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]
    - [[EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy - @shahidLiteratureGroundedNoveltyAssessment2025]]

- [[CLM - LLMs show promise for targeted reviewing subtasks but are not yet capable of functioning as standalone peer reviewers]]
    - [[EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper - @liuReviewerGPTExploratoryStudy2023]]
    - [[EVD - GPT-4 correctly detected errors in 7 of 13 constructed short CS papers - @liuReviewerGPTExploratoryStudy2023]]
    - [[EVD - GPT-4 made errors in 6 of 10 abstract comparison pairs favoring the inferior abstract - @liuReviewerGPTExploratoryStudy2023]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLM peer-review systems can predict paper acceptance and preference at near-human accuracy]]

---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "QUE - Can LLMs identify critical limitations within scientific research papers?"
tags:
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bd4-73f0-9bb1-5780a8392103
title: "Can LLMs identify critical limitations within scientific research papers?"
---
### Key Papers Asking Question

> [!info] Papers
> [[@xuCanLLMsIdentify2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "RQ1: How well do LLM-based systems perform in identifying limitations within scientific research?" (Xu et al., 2025, p. 1)
> ![[xuCanLLMsIdentify2025-que-p1-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - LLMs cannot reliably identify paper limitations at expert reviewer level|CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]
    - [[EVD - Claude Opus led AAAR ReviewCritique at 21.99% F1 - @louAAAR10AssessingAIs2025|EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG - @xuCanLLMsIdentify2025|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR - @louAAAR10AssessingAIs2025|EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]
    - [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points - @xuCanLLMsIdentify2025|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]
    - [[EVD - o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline - @louAAAR10AssessingAIs2025|EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - More capable GPT LLMs can detect quotation errors but imperfectly and context-dependently|CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]
    - [[EVD - GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context - @zhangDetectingReferenceErrors2024|EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0% - @zhangDetectingReferenceErrors2024]]
    - [[EVD - GPT-4 Turbo detected quotation errors at 70.0% accuracy - @zhangDetectingReferenceErrors2024|EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts - @zhangDetectingReferenceErrors2024]]

- [[CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]
    - [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3% - @zhangReviewingScientificPapers2025a|EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]]
    - [[EVD - o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX - @zhangReviewingScientificPapers2025a|EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]
    - [[EVD - o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3 - @zhangReviewingScientificPapers2025a|EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]]

- [[CLM - Quotation errors are subtle and currently hard for NLP models to catch|CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]
    - [[EVD - 39.18% of 3063 biomedical citations had accuracy errors - @sarolAssessingCitationIntegrity2024|EVD - 39.18% of 3063 annotated biomedical citation instances contained accuracy errors - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - MultiVerS reached micro-F1 0.59 on citation accuracy - @sarolAssessingCitationIntegrity2024|EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate - @sarolAssessingCitationIntegrity2024|EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - Annotator agreement on citation labels was only kappa 0.18-0.31 - @sarolAssessingCitationIntegrity2024|EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2 - @sarolAssessingCitationIntegrity2024]]

- [[CLM - Multi-agent LLMs give more specific and helpful feedback than single agents|CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]
    - [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG - @xuCanLLMsIdentify2025|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 - @darcyMARGMultiAgentReview2024|EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]]
    - [[EVD - MARG-S beat baselines by 6.1 recall points on ARIES - @darcyMARGMultiAgentReview2024|EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]
    - [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points - @xuCanLLMsIdentify2025|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]

- [[CLM - Facet-based re-ranking is critical for novelty evaluation|CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]
    - [[EVD - AI Scientist reached 0.47 accuracy on novelty test set - @shahidLiteratureGroundedNoveltyAssessment2025|EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Idea Novelty Checker reached 0.81 accuracy beating baselines - @shahidLiteratureGroundedNoveltyAssessment2025|EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025|EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]]

- [[CLM - LLMs are not yet reliable automatic reviewers|CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]
    - [[EVD - Claude Opus led AAAR ReviewCritique at 21.99% F1 - @louAAAR10AssessingAIs2025|EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-3.5 predicted review aspect scores at r=0.651 - @zhouLLMReliableReviewer2024|EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given the human-written review - @zhouLLMReliableReviewer2024]]
    - [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276 - @zhouLLMReliableReviewer2024|EVD - GPT-4 RR-MCQ macro accuracy was 0.276 and micro accuracy 0.710 on 196 review-revision multiple choice questions - @zhouLLMReliableReviewer2024]]
    - [[EVD - Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR - @louAAAR10AssessingAIs2025|EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]
    - [[EVD - o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline - @louAAAR10AssessingAIs2025|EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - RAG improves LLM limitation identification by grounding in relevant literature|CLM - RAG augmentation improves LLM limitation identification by grounding generation in domain-relevant literature]]
    - [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG - @xuCanLLMsIdentify2025|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points - @xuCanLLMsIdentify2025|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]
- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]

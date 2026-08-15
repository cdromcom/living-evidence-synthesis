---
NodeFormality: ReadyForInternal
aliases:
tags:
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bda-7515-8d8a-2e09a7e3d642
---
### Key Papers Asking Question

> [!info] Papers
> [[@zhangReviewingScientificPapers2025a]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "we consider the identification of critical errors and unsoundness problems as the main goal of an LLM-driven manuscript quality checker and present an extensible framework, including several baseline approaches and an automatic evaluation pipeline, to support related tasks." (Zhang & Abernethy, 2025, p. 1)
> ![[zhangReviewingScientificPapers2025a-que-p1-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]
    - [[EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0% - @zhangDetectingReferenceErrors2024]]
    - [[EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts - @zhangDetectingReferenceErrors2024]]

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]
    - [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]]
    - [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]
    - [[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]
    - [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]
    - [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]
    - [[EVD - 39.18% of 3063 annotated biomedical citation instances contained accuracy errors - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations - @sarolAssessingCitationIntegrity2024]]
    - [[EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2 - @sarolAssessingCitationIntegrity2024]]

- [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]]
    - [[EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]]
    - [[EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]]
    - [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]]
    - [[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]

- [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]
    - [[EVD - AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset - @shahidLiteratureGroundedNoveltyAssessment2025]]
    - [[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]]

- [[CLM - Current LLMs fall far short of requirements for dependable AI-assisted academic error verification]]
    - [[EVD - LLM confidence approaches zero across 498 model-instance SPOT evaluations with only 2 full-confidence cases - @sonWhenAICoScientists2025]]
    - [[EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]]
    - [[EVD - o3 achieved best SPOT performance with 6.1% precision 21.1% recall and 37.8% pass@4 - @sonWhenAICoScientists2025]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - LLM confidence calibration on scientific-error tasks is poor with extreme distributions]]
- [[EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

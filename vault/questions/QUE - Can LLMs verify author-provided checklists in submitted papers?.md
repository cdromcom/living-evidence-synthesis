---
NodeFormality: ReadyForInternal
aliases:
tags:
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bd7-723f-9d6f-5c01ba1e16c3
---
### Key Papers Asking Question

> [!info] Papers
> [[@liuReviewerGPTExploratoryStudy2023]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "Can LLMs verify author-provided checklists? (Section 4) Many conferences and journals provide authors with a checklist of items that helps set expectations from papers and also offers a guideline to authors to meet these expectations... We investigate if LLMs can do this job of verifying whether the checklist items are accurately reported by the authors." (Liu & Shah, 2023, p. 2)
> ![[liuReviewerGPTExploratoryStudy2023-que-p2-3.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]
    - [[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]]
    - [[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]]
    - [[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]]
    - [[EVD - LLMs showed lowest accuracy on questions about statistical software used and study funding across all models - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]]

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]
    - [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker - @zhangReviewingScientificPapers2025a]]
    - [[EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers - @zhangReviewingScientificPapers2025a]]
    - [[EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper - @zhangReviewingScientificPapers2025a]]

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline - @darcyMARGMultiAgentReview2024]]
    - [[EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus - @darcyMARGMultiAgentReview2024]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]

- [[CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]
    - [[EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0% - @zhangDetectingReferenceErrors2024]]
    - [[EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts - @zhangDetectingReferenceErrors2024]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]
    - [[EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments - @louAAAR10AssessingAIs2025]]
    - [[EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1% - @xuCanLLMsIdentify2025]]
    - [[EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task - @louAAAR10AssessingAIs2025]]
    - [[EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn - @xuCanLLMsIdentify2025]]
    - [[EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline - @louAAAR10AssessingAIs2025]]

- [[CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]
    - [[EVD - ChatGPT and human evaluators differed by mean 4.92% in overall compliance score on CONSORT-A - @robertsComparativeStudyChatGPT2023]]
    - [[EVD - ChatGPT diverged most from humans in the conclusion domain with mean difference 0.764 on CONSORT-A - @robertsComparativeStudyChatGPT2023]]
    - [[EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06 - @robertsComparativeStudyChatGPT2023]]

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]
    - [[EVD - CONSORT compliance varied from 35.16 percent in pharmacology to 63.35 percent in urology-nephrology - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - Overall CONSORT compliance rose from 27.3 percent in 1966-1990 to 56.1 percent in 2010-2024 across 21041 RCTs - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - Randomization sequence generation reported in only 9.7 percent and allocation concealment in 15.25 percent of RCTs - @srinivasanEvaluatingReportingQuality2025a]]

- [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]
    - [[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49 - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines - @bougieGenerativeAdversarialReviews2024a]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]
- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

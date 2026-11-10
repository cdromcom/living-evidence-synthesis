---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "QUE - Can LLMs verify author-provided checklists in submitted papers?"
tags:
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bd7-723f-9d6f-5c01ba1e16c3
title: "Can LLMs verify author-provided checklists in submitted papers?"
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

- [[CLM - LLM checklist agreement varies substantially, higher on factual than judgment items|CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]
    - [[EVD - ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria|EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028)]]
    - [[EVD - ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization|EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001)]]
    - [[EVD - GPT 3.5-turbo topped STROBE questions at 66.9% correct|EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles]]
    - [[EVD - GPT 4-0613 was lowest on STROBE questions at 44.1%|EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions]]
    - [[EVD - LLMs made systematic QUADAS-2 patient selection errors|EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design]]
    - [[EVD - LLMs were least accurate on software and funding questions|EVD - LLMs showed lowest accuracy on questions about statistical software used and study funding across all models]]
    - [[EVD - Four LLMs averaged 72.95% correct on QUADAS-2|EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27%]]

- [[CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]
    - [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3%|EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 16.3% hit rate as a PDF-based scientific quality checker]]
    - [[EVD - o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 64.9% (PDF) and 71.0% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]
    - [[EVD - o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3|EVD - o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.321 per paper]]

- [[CLM - Multi-agent LLMs give more specific and helpful feedback than single agents|CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]
    - [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1%]]
    - [[EVD - MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4|EVD - MARG-S generated 3.7 good comments per paper rated by users compared to 1.7 for single-agent GPT-4 baseline]]
    - [[EVD - MARG-S beat baselines by 6.1 recall points on ARIES|EVD - MARG-S outperformed all baselines by 6.1 recall points in automated evaluation on ARIES corpus]]
    - [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn]]

- [[CLM - More capable GPT LLMs can detect quotation errors but imperfectly and context-dependently|CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]
    - [[EVD - GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context|EVD - GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropped with additional context to 54.0%]]
    - [[EVD - GPT-4 Turbo detected quotation errors at 70.0% accuracy|EVD - GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus abstract plus excerpts]]

- [[CLM - LLMs cannot reliably identify paper limitations at expert reviewer level|CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]
    - [[EVD - Claude Opus led AAAR ReviewCritique at 21.99% F1|EVD - Claude Opus achieved highest ReviewCritique F1 of 21.99% on AAAR across 11376 review segments]]
    - [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG|EVD - GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and MARG reached 68.1%]]
    - [[EVD - Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR|EVD - Human review weakness diversity ITF-IDF was 7.69 while best LLM GPT-4o scored only 5.95 on AAAR PaperWeakness task]]
    - [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points|EVD - RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percentage points on LimitGen-Syn]]
    - [[EVD - o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline|EVD - o3-mini achieved best F1 of 47.98% on AAAR EqInfer barely above the 40% all-positive baseline]]

- [[CLM - LLMs can help automate reporting compliance appraisal|CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]
    - [[EVD - ChatGPT and humans differed by 4.92% on CONSORT-A compliance|EVD - ChatGPT and human evaluators differed by mean 4.92% in overall compliance score on CONSORT-A]]
    - [[EVD - ChatGPT diverged most on CONSORT-A conclusions by 0.764|EVD - ChatGPT diverged most from humans in the conclusion domain with mean difference 0.764 on CONSORT-A]]
    - [[EVD - ChatGPT-human correlation weakest on CONSORT-A intervention and objective|EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06]]

- [[CLM - LLMs can achieve SOTA CONSORT compliance assessment zero-shot at scale|CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]
    - [[EVD - CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology|EVD - CONSORT compliance varied from 35.16 percent in pharmacology to 63.35 percent in urology-nephrology]]
    - [[EVD - GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40%|EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent]]
    - [[EVD - CONSORT compliance rose from 27.3% to 56.1% over decades|EVD - Overall CONSORT compliance rose from 27.3 percent in 1966-1990 to 56.1 percent in 2010-2024 across 21041 RCTs]]
    - [[EVD - Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment|EVD - Randomization sequence generation reported in only 9.7 percent and allocation concealment in 15.25 percent of RCTs]]

- [[CLM - LLM review agents with memory and personas can match or exceed humans|CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]
    - [[EVD - GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49|EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49]]
    - [[EVD - GAR beat human reviewers on preference 0.684 vs 0.523|EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation]]
    - [[EVD - GAR human-likeness 3.89-4.02 significantly beat all LLM baselines|EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]
- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

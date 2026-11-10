---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "QUE - How has CONSORT reporting quality changed over time across medical disciplines and what LLM approaches can evaluate it at scale?"
tags:
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6be3-770a-9b2c-6bb62bf1da0c
title: "How has CONSORT reporting quality changed over time across medical disciplines and what LLM approaches can evaluate it at scale?"
---
### Key Papers Asking Question

> [!info] Papers
> [[@srinivasanEvaluatingReportingQuality2025a]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "In this paper, we leverage LLMs to evaluate CONSORT reporting in RCT publications at scale. We first validate our approach on the CONSORT-TM dataset Kilicoglu et al. [2021] with expert review, then analyze reporting trends across 21,041 RCTs from 1966-2024." (Srinivasan et al., 2025, p. 2)
> ![[srinivasanEvaluatingReportingQuality2025a-que-p2-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - RCT reporting improved substantially over decades but critical gaps persist|CLM - RCT reporting quality has improved substantially over decades but critical methodological gaps persist across all disciplines]]
    - [[EVD - CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology - @srinivasanEvaluatingReportingQuality2025a|EVD - CONSORT compliance varied from 35.16 percent in pharmacology to 63.35 percent in urology-nephrology]]
    - [[EVD - GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% - @srinivasanEvaluatingReportingQuality2025a|EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent]]
    - [[EVD - CONSORT compliance rose from 27.3% to 56.1% over decades - @srinivasanEvaluatingReportingQuality2025a|EVD - Overall CONSORT compliance rose from 27.3 percent in 1966-1990 to 56.1 percent in 2010-2024 across 21041 RCTs]]
    - [[EVD - Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment - @srinivasanEvaluatingReportingQuality2025a|EVD - Randomization sequence generation reported in only 9.7 percent and allocation concealment in 15.25 percent of RCTs]]

- [[CLM - LLMs can assess trial reporting adherence with accuracy approaching 90%|CLM - LLMs can assess clinical trial reporting guideline adherence with acceptable accuracy approaching 90%]]
    - [[EVD - Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions - @wrightsonGPTRCTsUsing2025|EVD - Fine-tuned Llama 2 improved from F1=0.63 (64% accuracy) to F1=0.84 (83% accuracy) on CONSORT guideline questions]]
    - [[EVD - GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions - @wrightsonGPTRCTsUsing2025|EVD - GPT-4 Turbo achieved F1=0.89 and 90% accuracy pooled across 9 CONSORT text questions on held-out clinical trial reports]]
    - [[EVD - GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57% - @wrightsonGPTRCTsUsing2025|EVD - GPT-4 Vision identified CONSORT flow diagrams with 100% accuracy but detected missing participant details at only 57% accuracy]]

- [[CLM - LLMs can help automate reporting compliance appraisal|CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]
    - [[EVD - ChatGPT and humans differed by 4.92% on CONSORT-A compliance - @robertsComparativeStudyChatGPT2023|EVD - ChatGPT and human evaluators differed by mean 4.92% in overall compliance score on CONSORT-A]]
    - [[EVD - ChatGPT diverged most on CONSORT-A conclusions by 0.764 - @robertsComparativeStudyChatGPT2023|EVD - ChatGPT diverged most from humans in the conclusion domain with mean difference 0.764 on CONSORT-A]]
    - [[EVD - ChatGPT-human correlation weakest on CONSORT-A intervention and objective - @robertsComparativeStudyChatGPT2023|EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06]]

- [[CLM - LLMs can achieve SOTA CONSORT compliance assessment zero-shot at scale|CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]
    - [[EVD - CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology - @srinivasanEvaluatingReportingQuality2025a|EVD - CONSORT compliance varied from 35.16 percent in pharmacology to 63.35 percent in urology-nephrology]]
    - [[EVD - GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% - @srinivasanEvaluatingReportingQuality2025a|EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent]]
    - [[EVD - CONSORT compliance rose from 27.3% to 56.1% over decades - @srinivasanEvaluatingReportingQuality2025a|EVD - Overall CONSORT compliance rose from 27.3 percent in 1966-1990 to 56.1 percent in 2010-2024 across 21041 RCTs]]
    - [[EVD - Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment - @srinivasanEvaluatingReportingQuality2025a|EVD - Randomization sequence generation reported in only 9.7 percent and allocation concealment in 15.25 percent of RCTs]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bdf-75b4-aeed-c983381682f9
---
### Key Papers Asking Question

> [!info] Papers
> [[@wrightsonGPTRCTsUsing2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "This exploratory research aimed to answer the following research question: how accurately can an AI-LLM measure reporting guideline compliance in a sample of sports medicine clinical trial reports?" (Wrightson et al., 2025, p. 2)
>
> ![[wrightsonGPTRCTsUsing2025-rq-p1-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]
    - [[EVD - ChatGPT and human evaluators differed by mean 4.92% in overall compliance score on CONSORT-A - @robertsComparativeStudyChatGPT2023]]
    - [[EVD - ChatGPT diverged most from humans in the conclusion domain with mean difference 0.764 on CONSORT-A - @robertsComparativeStudyChatGPT2023]]
    - [[EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06 - @robertsComparativeStudyChatGPT2023]]

- [[CLM - LLMs can assess clinical trial reporting guideline adherence with acceptable accuracy approaching 90%]]
    - [[EVD - Fine-tuned Llama 2 improved from F1=0.63 (64% accuracy) to F1=0.84 (83% accuracy) on CONSORT guideline questions - @wrightsonGPTRCTsUsing2025]]
    - [[EVD - GPT-4 Turbo achieved F1=0.89 and 90% accuracy pooled across 9 CONSORT text questions on held-out clinical trial reports - @wrightsonGPTRCTsUsing2025]]
    - [[EVD - GPT-4 Vision identified CONSORT flow diagrams with 100% accuracy but detected missing participant details at only 57% accuracy - @wrightsonGPTRCTsUsing2025]]

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]
    - [[EVD - CONSORT compliance varied from 35.16 percent in pharmacology to 63.35 percent in urology-nephrology - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - GPT-4o-mini achieved F1 0.85 precision 0.96 on CONSORT-TM outperforming prior state-of-the-art by over 40 percent - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - Overall CONSORT compliance rose from 27.3 percent in 1966-1990 to 56.1 percent in 2010-2024 across 21041 RCTs - @srinivasanEvaluatingReportingQuality2025a]]
    - [[EVD - Randomization sequence generation reported in only 9.7 percent and allocation concealment in 15.25 percent of RCTs - @srinivasanEvaluatingReportingQuality2025a]]

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]
    - [[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]]
    - [[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]]
    - [[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]]
    - [[EVD - LLMs showed lowest accuracy on questions about statistical software used and study funding across all models - @akyonEvaluatingCapabilitiesGenerative2024]]
    - [[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]
- [[EP - Per-item LLM-human agreement varies sharply by item type]]
- [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]]
- [[EP - Text-only LLMs underperform on tasks where figures or tables carry primary information]]

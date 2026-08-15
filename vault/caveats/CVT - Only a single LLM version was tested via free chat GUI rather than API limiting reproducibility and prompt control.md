---
NodeFormality: draft
aliases:
tags:
  - cvt/domain/reproducibility
  - cvt/mechanism/single-model
  - cvt/mechanism/gui-not-api
  - cvt/mechanism/inference-params-undisclosed
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/clarity
appliesTo:
  - "[[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]]"
  - "[[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bb0-7291-b5ea-97db026f949d
type: inferred
severity: moderate
---

## Source

[[@alharbiAutomatedAssessmentReporting2024]]

### Limitation

The study used only GPT-3.5 (free tier, chat interface) accessed on a single date (30 May 2024), without testing via API or other models. The free chat GUI does not allow temperature control, systematic prompt versioning, or guaranteed reproducibility. This limits the generalizability of findings to other LLMs or even later versions of GPT-3.5, and makes independent replication difficult.

### Supporting Quote

> [!info] Quotes
> "This study utilized the large language model GPT-3.5 (OpenAI, San Francisco, CA, USA), which is currently offered at no cost... To ensure consistency throughout the study, a single researcher (F.A.) formulated and submitted all prompts to language models. The text from the abstracts was then pasted into ChatGPT version 3.5 on 30 May 2024." (Alharbi & Asiri, 2024, p. 3)
>
> ![[alharbiAutomatedAssessmentReporting2024-cvt-p3-1.png]]
> [Inferred: using a single model via the free GUI without API access limits reproducibility, temperature control, and generalizability to other systems; the study's findings apply specifically to GPT-3.5 GUI performance, not LLMs more broadly.]

### Applies To

- [[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]]

- [[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]]

---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "QUE - How does LLM performance vary across specific structured tasks in systematic review and evidence appraisal workflows?"
tags:
  - 5c/clarity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6be1-709c-a28e-14133382b634
title: "How does LLM performance vary across specific structured tasks in systematic review and evidence appraisal workflows?"
---
### Key Papers Asking Question

> [!info] Papers
> [[@hasanIntegratingLargeLanguage2024]]
>
> [[@leucutaRiskBiasAssessment2025]]
>
> [[@alharbiAutomatedAssessmentReporting2024]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "we propose a framework for incorporating LLMs into systematic reviews and employ GPT-4 for RoB assessment in a case study using the Cochrane Collaboration's Risk Of Bias In Non-randomised Studies of Interventions (ROBINS-I) tool" (Hasan et al., 2024, p. 2)
> ![[hasanIntegratingLargeLanguage2024-que-p2-1.png]]
>
> "the aim of the study was to assess the capability of LLMs to evaluate the risk of bias in diagnostic accuracy studies, using QUADAS2, in comparison to human experts" (Leucuta et al., 2025, p. 2)
> ![[leucutaRiskBiasAssessment2025-que-p2-1.png]]
>
> "This study aims to assess the usability of LLMs, particularly ChatGPT, in assessing the completeness of reporting in two key areas of orthodontic research: abstracts of randomized controlled trials (RCTs) and abstracts of systematic reviews." (Alharbi & Asiri, 2024, p. 2)
> ![[alharbiAutomatedAssessmentReporting2024-que-p2-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - LLM use in systematic reviews needs a structured protocol|CLM - A structured protocol for integrating LLMs into systematic reviews must specify rationale, model selection, prompt engineering, human verification procedures, and reporting standards]]
    - [[EVD - GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I|EVD - GPT-4 achieved 61% raw percent agreement with Cochrane reviewers on ROBINS-I overall risk of bias with Kendall coefficient of 0.35]]

- [[CLM - Targeted questions elicit substantially better LLM performance than open-ended review|CLM - Targeted question prompting elicits substantially better LLM performance than open-ended review generation]]
    - [[EVD - GPT-4 reached 86.6% accuracy on NeurIPS checklist items|EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper pairs]]
    - [[EVD - GPT-4 detected errors in 7 of 13 constructed papers|EVD - GPT-4 correctly detected errors in 7 of 13 constructed short CS papers]]
    - [[EVD - GPT-4 favored the worse abstract in 6 of 10 pairs|EVD - GPT-4 made errors in 6 of 10 abstract comparison pairs favoring the inferior abstract]]

- [[CLM - Multiple prompts elicit more complete and nuanced LLM ethics review than single prompts|CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]
    - [[EVD - All four LLMs gave similar answers to all 7 IRB cases|EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous responses]]
    - [[EVD - All four LLMs included core ICD elements in all 7 cases|EVD - All four LLMs included fundamental ICD elements for all seven case scenarios]]
    - [[EVD - LLMs performed suboptimally on placebo arm and risk issues in a single prompt|EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt]]

- [[CLM - Fine-tuning on review data overcomes overly favorable LLM assessments|CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]]
    - [[EVD - OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o|EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers]]
    - [[EVD - OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o|EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o]]
    - [[EVD - OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons|EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations]]

- [[CLM - LLM review agents with memory and personas can match or exceed humans|CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]
    - [[EVD - GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49|EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49]]
    - [[EVD - GAR beat human reviewers on preference 0.684 vs 0.523|EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation]]
    - [[EVD - GAR human-likeness 3.89-4.02 significantly beat all LLM baselines|EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines]]

- [[CLM - LLM review quality is comparable to humans given sufficient context|CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]
    - [[EVD - 57.4% of 308 researchers found GPT-4 feedback helpful|EVD - 57.4% of 308 researchers found GPT-4 feedback helpful and 82.4% found it more beneficial than at least some human reviewers]]
    - [[EVD - GPT-4 Turbo ranked first in human review preference|EVD - GPT-4 Turbo ranked first in human preference for academic review quality with score 0.558]]
    - [[EVD - GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans|EVD - GPT-4 commented on research implications 7.27x more than humans and on novelty 10.69x less on ICLR papers]]
    - [[EVD - GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human|EVD - GPT-4 feedback overlapped 30.85% with individual human reviewers on Nature journals comparable to human-human overlap of 28.58%]]
    - [[EVD - LLM review scores exceeded humans without area-chair context but matched with it|EVD - LLM review recommendation scores exceeded human scores without area-chair context but matched with it]]
    - [[EVD - LLM reviews scored like human reviews on all 3 criteria|EVD - LLM reviews scored comparably to human reviews on all three expert evaluation criteria]]
    - [[EVD - GPT-4 feedback overlap fell from 30.85% to 0.43% after shuffling|EVD - Pairwise GPT-4 feedback overlap dropped from 30.85% to 0.43% after shuffling confirming paper-specificity]]

- [[CLM - General LLMs give overly positive recommendations unlike human reviewers|CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]
    - [[EVD - GPT-3.5 predicted review aspect scores at r=0.651|EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given the human-written review]]
    - [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276|EVD - GPT-4 RR-MCQ macro accuracy was 0.276 and micro accuracy 0.710 on 196 review-revision multiple choice questions]]
    - [[EVD - OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o|EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers]]
    - [[EVD - OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o|EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o]]
    - [[EVD - OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons|EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations]]

- [[CLM - AI can augment IRB review but cannot replace human oversight|CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]
    - [[EVD - AI platforms drafted SOPs covering fundamental sections with variations|EVD - AI platforms drafted SOPs covering fundamental sections with variations across platforms]]
    - [[EVD - All AI platforms missed post-trial herbal medicine access|EVD - All AI platforms failed to address post-trial herbal medicine access in case study 10]]
    - [[EVD - All four LLMs gave similar answers to all 7 IRB cases|EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous responses]]
    - [[EVD - All four LLMs included core ICD elements in all 7 cases|EVD - All four LLMs included fundamental ICD elements for all seven case scenarios]]
    - [[EVD - LLMs performed suboptimally on placebo arm and risk issues in a single prompt|EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt]]
    - [[EVD - No AI platform recognized the IRB quorum requirement|EVD - None of three AI platforms recognized quorum requirement for initial proposal review]]
    - [[EVD - Three AI platforms answered all 10 IRB cases correctly|EVD - Three AI platforms responded correctly to all 10 IRB case study queries]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - Aggregate LLM accuracy on evidence-appraisal benchmarks lands in the moderate 60-80 percent range]]
- [[EP - Per-item LLM-human agreement varies sharply by item type]]

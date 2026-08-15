---
NodeFormality: ReadyForInternal
aliases:
tags:
  - 5c/clarity
  - 5c/creativity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6be2-7683-b6ab-4536525e6b2a
---
### Key Papers Asking Question

> [!info] Papers
> [[@louAAAR10AssessingAIs2025]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
> "How effectively can AI assist researchers in tasks that are domain-specific, expertise-demanding, and reasoning-intensive?" (Lou et al., 2025, p. 1)
> ![[louAAAR10AssessingAIs2025-que-p1-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - Multiple prompts elicit more complete and nuanced LLM outputs for ethical review tasks than single prompts]]
    - [[EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous responses - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - All four LLMs included fundamental ICD elements for all seven case scenarios - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt - @sridharanLeveragingArtificialIntelligence2025]]

- [[CLM - Targeted question prompting elicits substantially better LLM performance than open-ended review generation]]
    - [[EVD - GPT-4 achieved 86.6% majority-vote accuracy on 119 NeurIPS checklist question-paper pairs - @liuReviewerGPTExploratoryStudy2023]]
    - [[EVD - GPT-4 correctly detected errors in 7 of 13 constructed short CS papers - @liuReviewerGPTExploratoryStudy2023]]
    - [[EVD - GPT-4 made errors in 6 of 10 abstract comparison pairs favoring the inferior abstract - @liuReviewerGPTExploratoryStudy2023]]

- [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]]
    - [[EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers - @idahlOpenReviewerSpecializedLarge2025]]
    - [[EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o - @idahlOpenReviewerSpecializedLarge2025]]
    - [[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]]

- [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]
    - [[EVD - GAR achieved F1 score of 0.66 on ICLR 23 paper acceptance prediction significantly exceeding human baseline of 0.49 - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a Bradley-Terry preference score of 0.684 outperforming human reviewers at 0.523 in GPT-4 preference evaluation - @bougieGenerativeAdversarialReviews2024a]]
    - [[EVD - GAR achieved a human-likeness score of 3.89 to 4.02 across three datasets significantly outperforming all LLM baselines - @bougieGenerativeAdversarialReviews2024a]]

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]
    - [[EVD - 57.4% of 308 researchers found GPT-4 feedback helpful and 82.4% found it more beneficial than at least some human reviewers - @liangCanLargeLanguage2024a]]
    - [[EVD - GPT-4 Turbo ranked first in human preference for academic review quality with score 0.558 - @tyserAIDrivenReviewSystems2024]]
    - [[EVD - GPT-4 commented on research implications 7.27x more than humans and on novelty 10.69x less on ICLR papers - @liangCanLargeLanguage2024a]]
    - [[EVD - GPT-4 feedback overlapped 30.85% with individual human reviewers on Nature journals comparable to human-human overlap of 28.58% - @liangCanLargeLanguage2024a]]
    - [[EVD - LLM review recommendation scores exceeded human scores without area-chair context but matched with it - @tyserAIDrivenReviewSystems2024]]
    - [[EVD - LLM reviews scored comparably to human reviews on all three expert evaluation criteria - @tyserAIDrivenReviewSystems2024]]
    - [[EVD - Pairwise GPT-4 feedback overlap dropped from 30.85% to 0.43% after shuffling confirming paper-specificity - @liangCanLargeLanguage2024a]]

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]
    - [[EVD - GPT-3.5 achieved Pearson r=0.651 in predicting review aspect scores when given the human-written review - @zhouLLMReliableReviewer2024]]
    - [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276 and micro accuracy 0.710 on 196 review-revision multiple choice questions - @zhouLLMReliableReviewer2024]]
    - [[EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers - @idahlOpenReviewerSpecializedLarge2025]]
    - [[EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o - @idahlOpenReviewerSpecializedLarge2025]]
    - [[EVD - OpenReviewer won against GPT-4o in 60% and against Llama-3.1-70B in 76% of LLM-as-judge preference evaluations - @idahlOpenReviewerSpecializedLarge2025]]

- [[CLM - AI tools can augment IRB decision-making and improve review efficiency but cannot replace human oversight]]
    - [[EVD - AI platforms drafted SOPs covering fundamental sections with variations across platforms - @sridharanAssessingDecisionMakingCapabilities2024]]
    - [[EVD - All AI platforms failed to address post-trial herbal medicine access in case study 10 - @sridharanAssessingDecisionMakingCapabilities2024]]
    - [[EVD - All four LLMs answered all seven IRB ethics case queries with homogeneous responses - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - All four LLMs included fundamental ICD elements for all seven case scenarios - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt - @sridharanLeveragingArtificialIntelligence2025]]
    - [[EVD - None of three AI platforms recognized quorum requirement for initial proposal review - @sridharanAssessingDecisionMakingCapabilities2024]]
    - [[EVD - Three AI platforms responded correctly to all 10 IRB case study queries - @sridharanAssessingDecisionMakingCapabilities2024]]

- [[CLM - A structured protocol for integrating LLMs into systematic reviews must specify rationale, model selection, prompt engineering, human verification procedures, and reporting standards]]
    - [[EVD - GPT-4 achieved 61% raw percent agreement with Cochrane reviewers on ROBINS-I overall risk of bias with Kendall coefficient of 0.35 - @hasanIntegratingLargeLanguage2024]]

### Cross-paper patterns

> [!info] EvidencePatterns whose supporting EVDs include evidence cited under this question. Each pattern aggregates findings across multiple papers.

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - task/aggregate-vs-instance-validity
  - 5c/credibility
  - ep/strength/3-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1ccd2f2ae9ce
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1ccd2f2ae9ce
---

## Pattern statement

LLM-human agreement at the aggregate (mean / Bland-Altman) level is often strong, while per-paper or per-instance correlations collapse to near-zero. LLMs and humans hit similar averages on a corpus *without* tracking the same per-paper signal — meaning the LLM is producing distribution-matched scores rather than paper-aware scores.

## What is being claimed

The pattern is a measurement paradox: if you only look at sample-level summary statistics (mean compliance score, mean recommendation, mean overlap rate), the LLM looks competitive with humans. But when you re-run the analysis paper-by-paper, the correlation between LLM scores and human scores can be near-zero. This means the LLM is *not* identifying which papers are well-reported and which are poorly-reported — it is only producing scores that, in aggregate, happen to match the human distribution. For deployment, mean-level agreement is the wrong signal; per-paper rank correlation is the right one.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - ChatGPT and human evaluators differed by mean 4.92% in overall compliance score on CONSORT-A - @robertsComparativeStudyChatGPT2023]] — Roberts et al. 2023: 4.92% mean difference looks competitive at the aggregate level.
- [[EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06 - @robertsComparativeStudyChatGPT2023]] — Roberts et al. 2023: but per-paper Pearson r drops to 0.02–0.06 in the same domains where the mean looks fine. The LLM hits the average without tracking which paper is which.
- [[EVD - Pairwise GPT-4 feedback overlap dropped from 30.85% to 0.43% after shuffling confirming paper-specificity - @liangCanLargeLanguage2024a]] — Liang et al. 2024: GPT-4 feedback DOES track papers (overlap collapses when shuffled), but only for *which paper* — the same paper-specificity check applied to scores would differ.
- [[EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams - @huntington-kleinLLMsActRepositories2024]] — Huntington-Klein & Murray 2024: LLMs label expert-selected and non-expert variables at similar rates, hitting an average without tracking the variable-by-variable signal.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]] — Huntington-Klein's claim is one instance of the broader pattern; the same logic applies to per-paper compliance and per-paper feedback.
- **Adjacent pattern (related mechanism):** [[EP - Per-item LLM-human agreement varies sharply by item type]] — per-item variance is one structural cause of the aggregate-vs-per-paper paradox: the LLM is agreeing on items where extraction is easy and disagreeing on items where judgment matters, which averages out to a small mean difference but a near-zero per-item correlation.

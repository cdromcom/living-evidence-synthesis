---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/risk-of-bias-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/some-concerns
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/39pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b6a-7323-b0e4-58117840cf72
appraisal_overall: L0-M3-H2
tripod_llm_pct: 39pct
---

## Source

[[@hasanIntegratingLargeLanguage2024]]

## Description

> "Raw agreement about the overall risk of bias across domains was 61% (Kendall coefficient=0.35)." (Hasan et al., 2024, p. 1)
>
> ![[hasan2024-table1-p3-1.png]]

## Methods Context

### What?

> **Study design:** single-case methodological study comparing GPT-4 risk-of-bias judgments against published Cochrane systematic-review judgments on the same primary studies.
>
> **Method type:** zero-shot LLM evaluation; reference standard is the Cochrane reviewers' published RoB judgment (no separate de novo human re-rating).
>
> **Tools:** OpenAI GPT-4 accessed via ChatGPT Plus (initially Code Interpreter, ultimately copy-pasted Word-converted text); ROBINS-I tool (7 domains: D1 confounding, D2 participant selection, D3 classification of interventions, D4 deviations from intended interventions, D5 missing data, D6 measurement of outcomes, D7 selective reporting, plus Overall); R statistical environment.
>
> **Dependent variables:** raw per cent agreement, weighted Cohen's kappa, and Kendall's τ between GPT-4 and Cochrane judgments, computed per ROBINS-I domain and Overall.
>
> **Independent variable:** ROBINS-I domain (D1–D7 + Overall).
>
> "This study evaluates GPT-4 agreement with human reviewers in assessing the risk of bias using the Risk Of Bias In Non-randomised Studies of Interventions (ROBINS-I) tool and proposes a framework for integrating LLMs into systematic reviews." (Hasan et al., 2024, p. 1)
> ![[hasanIntegratingLargeLanguage2024-evd-p1-1.png]]

### How?

> **Procedure:** (1) Searched Scopus for all Cochrane systematic reviews citing the original ROBINS-I publication, restricted to fully-published Cochrane SRs in medicine; included all original non-randomised studies whose RoB was assessed with ROBINS-I. (2) Piloted three data-entry methods to ChatGPT (GPT-4): direct PDF upload via Code Interpreter (failed — fragmented text), pasting full text (failed — exceeded an estimated 2500-word limit), and finally converting each study PDF to a Word file and copy-pasting only the Methods and Results sections (the sections human reviewers focus on for RoB). (3) Prompts and data-entry procedures were developed iteratively without prespecification ("these processes were not prespecified"); foreign-language studies were also translated by ChatGPT and long studies were truncated. (4) One reviewer extracted the Cochrane RoB judgment for each study; a second reviewer verified extraction. (5) Agreement between Cochrane and GPT-4 ordinal judgments computed using raw per cent agreement, weighted Cohen's kappa, and Kendall's τ. Magnitude categories: slight (0–0.20), fair (0.21–0.40), moderate (0.41–0.60), substantial (0.61–0.80), almost perfect (0.81–1.0). Analysis in R.
>
> "We measured the agreement between Cochrane reviewers and GPT-4 comparing the ordinal judgements about RoB using raw per cent agreement, weighted Cohen's kappa and Kendall's τ for correlation. The magnitude of agreement based on values of a correlation or kappa coefficient was considered to be slight (0–0.20), fair (0.21–0.40), moderate (0.41–60), substantial (0.61–0.80) and almost perfect (0.81–1.0)." (Hasan et al., 2024, p. 2)
> ![[hasanIntegratingLargeLanguage2024-evd-p2-1.png]]

### Who?

> **Models / participants:** GPT-4 (accessed via ChatGPT Plus interface, August 2023; specific GPT-4 version/snapshot not reported) vs. published Cochrane SR reviewers (treated as the reference standard; no de novo independent human re-rating).
>
> **Sample-size flow:** Scopus search yielded **98 Cochrane SRs** citing ROBINS-I → **36 SRs** provided full ROBINS-I assessments → after deduplicating studies appearing in multiple SRs, **307 unique non-randomised studies** were finalised as the analytic sample. Each study contributed one GPT-4 judgment per ROBINS-I domain (7 domains + Overall = 8 ordinal judgments per study).
>
> "The initial search yielded 98 SRs, from which 36 provided full ROBINS-I assessment. After deduplicating studies that appeared in multiple SRs, we finalised our sample with 307 unique individual studies (online supplemental figure; box 1 and box 2)." (Hasan et al., 2024, p. 2)
> ![[hasanIntegratingLargeLanguage2024-evd-p2-2.png]]

## Other Notes

Domain-specific results: D3 (classification of intervention) had highest raw agreement (71%) and D1 (confounding) the lowest (47%). Kappa was low across all domains (range 0.02–0.28); D2 (participant selection) had the highest Kendall coefficient (0.54). Overall Kendall τ of 0.35 suggests fair agreement.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@hasanIntegratingLargeLanguage2024#TRIPOD-LLM reporting summary]].

| ROBINS-I domain | Raw % agreement | Weighted κ | Kendall τ |
| --- | :---: | :---: | :---: |
| D1: Confounding | 47% | 0.07 | 0.38 |
| D2: Participant selection | 46% | 0.28 | **0.54** |
| D3: Classification of interventions | **71%** | 0.10 | 0.23 |
| D4: Deviations from intended interventions | 31% | 0.02 | 0.43 |
| D5: Missing data | 37% | 0.14 | 0.49 |
| D6: Measurement of outcomes | 42% | 0.15 | 0.46 |
| D7: Selective reporting | 36% | 0.03 | 0.38 |
| **Overall** | **61%** | **0.13** | **0.35** |

| Interpretation band | Threshold |
| --- | --- |
| Slight | 0.00–0.20 |
| Fair | 0.21–0.40 |
| Moderate | 0.41–0.60 |
| Substantial | 0.61–0.80 |
| Almost perfect | 0.81–1.00 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Prompts and data entry processes for GPT-4 ROBINS-I assessment were developed iteratively without prespecification limiting replicability]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - A structured protocol for integrating LLMs into systematic reviews must specify rationale, model selection, prompt engineering, human verification procedures, and reporting standards]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate LLM accuracy on evidence-appraisal benchmarks lands in the moderate 60-80 percent range]]
- [[EP - Per-item LLM-human agreement varies sharply by item type]]

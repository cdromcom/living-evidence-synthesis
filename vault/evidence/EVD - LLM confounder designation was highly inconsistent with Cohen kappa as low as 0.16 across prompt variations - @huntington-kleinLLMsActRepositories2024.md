---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/low-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/62pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b77-74dc-bfa6-3515fde9ce31
appraisal_overall: L1-M3-H1
tripod_llm_pct: 62pct
---

## Source

[[@huntington-kleinLLMsActRepositories2024]]

## Description

> "For GPT o1-preview, there was fair agreement across methods, with 87.7% of the variables designated the same way; however, this was driven partially by the model's tendency to label everything a confounder, so the Cohen's kappa was still low at .16. Claude 3.5 Sonnet saw only 66.9% of confounders getting the same designation in both methods, and Cohen's kappa of .21. GPT-4o produced a similar Cohen's kappa of .24." (Huntington-Klein & Murray, 2024, p. 14–15)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-p14-1.png]]
>
> "In Claude 3.5, 36.7% of variables had different designations under one option-ordering system compared to another, leading to a Cohen's kappa of .13." (Huntington-Klein & Murray, 2024, p. 16)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-p16-1.png]]

## Methods Context

### What?

> **Study design:** robustness / consistency sub-analysis of the same LLM elicitation experiment (cross-condition reliability). **Method type:** Cohen's kappa (κ) and percent-agreement on per-variable confounder designations across (a) direct vs. indirect prompting, (b) reasoning vs. no-reasoning prompts, (c) standard vs. alternate multiple-choice option ordering, and within-variable SD across the 10 repeat calls. **Tools:** Cohen's κ; per-variable categorization into "always (100%) / never (0%) / mixed" confounder; figures 5–8. **Dependent variables:** Cohen's κ; % of variables receiving identical designation across methods; within-variable SD across iterations; share of variables flipping between 0% and 100% solely on option order. **Independent variables:** model (Claude 3.5 / GPT-4o / GPT-o1); prompt-pair compared (direct↔indirect; reasoning↔no-reasoning; standard↔alternate option order); whether the Non-Confounders subgroup is included.
>
> "In order to assess the consistency of LLM responses we also use several variants on the prompts. First, we attempt a 'no-reasoning' version of the prompts… Second, we modify the direct prompt and change the order of the options to 'A. Not sure. B. Not a confounding variable. C. A confounding variable' to check whether the LLM responses are sensitive to the shuffling of the options, as in Nori et al. (2023)." (Huntington-Klein & Murray, 2024, p. 6)
> ![[huntington-kleinLLMsActRepositories2024-evd-p6-1.png]]

### How?

> **Procedure:** (1) For each variable, compute the share of the 10 iterations on which the LLM labeled it a confounder; categorize the variable as 0% / Mixed / 100%. (2) Compute within-variable SD across the 10 iterations and plot its distribution by model × method (Fig 5). (3) Cross-tabulate per-variable categorizations between paired prompting conditions (direct↔indirect, reasoning↔no-reasoning, standard↔alternate option order), then compute Cohen's κ on the 3-level (0% / Mixed / 100%) labels (Figs 6–8). (4) For the option-ordering test, swap "A. Not a confounder / B. A confounding variable / C. Not sure" to "A. Not sure / B. Not a confounding variable / C. A confounding variable" while keeping all other prompt text identical, and re-run all 10 iterations.
>
> "For the direct version of the prompt with reasoning, we elicited a second set of responses where the only change to the prompt was a change in the order that the multiple-choice options were presented. This allows us to test for order-option sensitivity, as in Nori et al. (2023)." (Huntington-Klein & Murray, 2024, p. 16)
> ![[huntington-kleinLLMsActRepositories2024-evd-p16-2.png]]

### Who?

> **Models:** Claude 3.5-Sonnet and GPT-4o (10 iterations per prompt at temperature 0.7 — necessary for the consistency analysis); GPT-o1-preview (1 iteration; consistency-across-iterations analysis therefore not computed for o1-preview).
>
> **Variables analyzed:** the same 172 CDP candidate confounders. Note: Non-Confounders measured at follow-up are *omitted* from the option-ordering analysis for GPT-o1-preview because the content-flagging workaround changed the prompt for that subgroup; this affects only Non-Confounders for o1-preview.
>
> **Comparison footnote:** "for both Claude and GPT, there was more inconsistency in designation among the Non-Confounder group. If this group is excluded, the shares for Claude are 66.1% direct and 81.2% indirect, and for GPT-4o are 68.8% direct and 48.2% indirect." (p. 11, fn 5)
>
> "GPT-4o and Claude 3.5 Sonnet are run using a temperature of 0.7, and each prompt is given ten times, in order to allow us to see some of the distribution of responses that the LLMs might give. GPT-o1-preview does not allow users to raise the temperature." (Huntington-Klein & Murray, 2024, p. 6)
> ![[huntington-kleinLLMsActRepositories2024-evd-p6-2.png]]

## Other Notes

Option-ordering sensitivity: 16.3% of GPT-4o variables switched between 0% and 100% confounder designation solely based on option order, and 4.6% of Claude variables did the same. This is a strong indicator of unreliable causal reasoning.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@huntington-kleinLLMsActRepositories2024#TRIPOD-LLM reporting summary]].

Cross-method agreement (Cohen's κ on 0%/Mixed/100% designations):

| Comparison | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| **Direct vs. indirect (with reasoning)** | **κ = 0.21** (66.9% same) | **κ = 0.24** | **κ = 0.16** (87.7% same) |
| Reasoning vs. no-reasoning, *indirect* | κ = 1.00 | κ = 1.00 | n/a |
| Reasoning vs. no-reasoning, *direct* | κ = 0.41 | **κ = 0.13** | n/a |
| **Standard vs. alternate option order (direct)** | **κ = 0.41** (36.7% flipped) | **κ = 0.13** (65.7% flipped) | n/a |

Within-variable consistency across 10 iterations (share of variables with identical designation in all 10 calls):

| Method | Claude 3.5 | GPT-4o |
| --- | :---: | :---: |
| Direct | 65.1% | 63.4% |
| Indirect | 75.6% | 40.1% |
| Indirect, 22.6% of GPT-4o variables split 4/6 or 5/5 | — | — |

Option-ordering 0% ↔ 100% flips (most damning robustness number):

| Model | % of variables flipping 0% ↔ 100% on option order alone |
| --- | :---: |
| Claude 3.5 | 4.6% |
| GPT-4o | 16.3% |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs]]
- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]

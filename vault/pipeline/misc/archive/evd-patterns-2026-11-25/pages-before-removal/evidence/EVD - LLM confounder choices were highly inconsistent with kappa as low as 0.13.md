---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.13 across prompt variations"
tags:
  - task/causal-inference-judgment
  - appraisal/construct-validity/low-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/62pct
  - 5c/credibility
  - forensic/kappa-check/in-bounds
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6b77-74dc-bfa6-3515fde9ce31
appraisal_overall: L1-M3-H1
tripod_llm_pct: 62pct
title: "LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.13 across prompt variations"
---

## Source

[[sysrev/dgraph/source/@huntington-kleinLLMsActRepositories2024]]

## Description

> "For GPT o1-preview, there was fair agreement across methods, with 87.7 % of the variables designated the same way; however, this was driven partially by the model’s tendency to label everything a confounder, so the Cohen’s kappa" (Huntington-Klein & Murray, 2026, p. 16)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p16-1.png]]
>
> "was still low at 0.16. Claude 3.5-Sonnet saw only 66.9 % of confounders getting the same designation in both methods, and Cohen’s kappa of 0.21. In both, the mismatches usually occurred because the indirect method designated something as a confounder while the direct method did not. GPT-4o produced a similar Cohen’s kappa of 0.24" (Huntington-Klein & Murray, 2026, p. 17; the sentence continues from p. 16)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p17-1.png]]
>
> "In Claude 3.5, 36.7 % of variables had different designations under one option-ordering system compared to another, leading to a Cohen’s kappa of 0.41. GPT-4o was less consistent, with 65.7 % of variables changing designation, leading to a Cohen’s kappa of 0.13." (Huntington-Klein & Murray, 2026, p. 18)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p18-1.png]]
>
> Grounding figure (Fig 8, p. 16): share of variables with the same designation in all ten iterations, by prompting method (Claude 3.5 and GPT-4o).
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig8-p16.png]]
>
> Grounding figure (Fig 9, p. 17): agreement between direct prompting and indirect prompting (top) and sequential prompting (bottom), by model.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig9-p17.png]]
>
> Grounding figure (Fig 10, p. 18): agreement between the reasoning and no-reasoning prompts.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig10-p18.png]]
>
> Grounding figure (Fig 11, p. 18): sensitivity to option ordering (direct prompt with reasoning).
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig11-p18.png]]

## Methods Context

### What?

> **Study design:** robustness / consistency sub-analysis of the same LLM elicitation experiment (cross-condition reliability).
>
> **Method type:** Cohen's kappa (κ) and percent-agreement on per-variable confounder designations across (a) direct vs. indirect prompting (plus comparisons with the pick-from-list and sequential methods), (b) reasoning vs. no-reasoning prompts, (c) standard vs. alternate multiple-choice option ordering, and within-variable consistency across the 10 repeat calls.
>
> **Tools:** Cohen's κ; per-variable categorization into "Always (100%) / Never (0%) / Mixed" confounder; Figures 8–11.
>
> **Dependent variables:** Cohen's κ; % of variables receiving identical designation across methods; share of variables with identical designation in all 10 iterations; share of variables flipping between Never and Always solely on option order.
>
> **Independent variables:** model (Claude 3.5 / GPT-4o / GPT-o1); prompt-pair compared (direct↔indirect; reasoning↔no-reasoning; standard↔alternate option order; other method pairs); whether the Non-Confounders subgroup is included.
>
> "In order to assess the consistency of LLM responses we also use several variants on the prompts. First, we attempt a “no-reasoning” version of the prompts, in which the LLMs are told they are an expert in identifying confounders in medical studies and then given the question without any example tasks. Then the LLM is instructed to give its response immediately rather than providing any explanation or reasoning. Second, we modify the direct prompt and change the order of the options to “A. Not sure. B. Not a confounding variable. C. A confounding variable” to check whether the LLM responses are sensitive to the shuffling of the options, as in Nori et al. [23]." (Huntington-Klein & Murray, 2026, p. 7)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p7-1.png]]

### How?

> **Procedure:** (1) For each variable, compute the share of the 10 iterations on which the LLM labeled it a confounder; categorize the variable as Never (0%) / Mixed / Always (100%). (2) Compute the share of variables whose ten iterations all agree, and the share with small and large splits, by model × method (Fig 8). (3) Cross-tabulate per-variable categorizations between paired prompting conditions (direct↔indirect and direct↔sequential, reasoning↔no-reasoning, standard↔alternate option order), then compute Cohen's κ on the 3-level (Never / Mixed / Always) labels (Figs 9–11). (4) For the option-ordering test, swap "A. Not a confounder / B. A confounding variable / C. Not sure" to "A. Not sure / B. Not a confounding variable / C. A confounding variable" while keeping all other prompt text identical, and re-run all 10 iterations. (5) For pick-from-list, check whether a variable's designation depends on its position in the list and on which other variables are in the list (Fig 12, pp. 18–19).
>
> "For the direct version of the prompt with reasoning, we elicited a second set of responses where the only change to the prompt was a change in the order that the multiple-choice options were presented. This allows us to test for order-option sensitivity, as in Nori et al. [23]." (Huntington-Klein & Murray, 2026, p. 18)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p18-2.png]]

### Who?

> **Models:** Claude 3.5-Sonnet and GPT-4o (10 iterations per prompt at temperature 0.7, necessary for the consistency analysis); GPT-o1-preview (1 iteration; consistency-across-iterations analysis therefore not computed for o1-preview). The pick-from-list and sequential methods were run in August 2025 with GPT-o1-pro and the claude-3-5-sonnet-20240620 version of Claude 3.5-Sonnet (p. 5, footnote 4).
>
> **Variables analyzed:** the same 172 CDP candidate confounders. Note: Non-Confounders measured at follow-up are *omitted* from the cross-method agreement graph for GPT-o1-preview because the content-flagging workaround changed the prompt for that subgroup (p. 16); this affects only Non-Confounders for o1-preview.
>
> **Comparison footnote:** "For both Claude and GPT, there was more inconsistency in designation among the Non-Confounder group. If this group is excluded, the shares for Claude are 66.1 % direct and 81.2 % indirect, and for GPT-4o are 68.8 % direct and 48.2 % indirect." (Huntington-Klein & Murray, 2026, p. 16, footnote 9)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p16-2.png]]
>
> "GPT-4o and Claude 3.5-Sonnet are run using a temperature of 0.7, and each prompt is given ten times, in order to allow us to see some of the distribution of responses that the LLMs might give. GPT-o1-preview does not allow users to change the temperature." (Huntington-Klein & Murray, 2026, p. 7)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p7-2.png]]

## Other Notes

Option-ordering sensitivity: 16.3% of GPT-4o variables switched between Never and Always designation solely based on option order, and 5.8% of Claude variables did the same (Fig 11, p. 18; the paper's text on p. 18 gives 4.6% for Claude). The authors describe this as a heavy impact of an irrelevant prompt detail, and the conclusions (p. 20) say the sensitivity holds "for one prompting method": it does not extend to the pick-from-list method (p. 18, Fig 12).

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[sysrev/dgraph/source/@huntington-kleinLLMsActRepositories2024#TRIPOD-LLM reporting]].

Cross-method agreement (Cohen's κ on Never/Mixed/Always designations; Figs 9–11, pp. 17–18):

| Comparison | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| **Direct vs. indirect (with reasoning)** | **κ = 0.21** (66.9% same, paper text) | **κ = 0.24** | **κ = 0.16** (87.7% same, paper text) |
| Reasoning vs. no-reasoning, *indirect* | κ = 1.00 | κ = 1.00 | n/a |
| Reasoning vs. no-reasoning, *direct* | κ = 0.41 | **κ = 0.13** | n/a |
| **Standard vs. alternate option order (direct)** | **κ = 0.41** (36.7% flipped) | **κ = 0.13** (65.7% flipped) | n/a |
| Strongest κ among the other method pairs (text only, p. 17) | 0.37 (direct vs. pick-from-list) | at most 0.37 | 0.56 (direct vs. sequential, 77.8% same) |

Within-variable consistency across 10 iterations (Fig 8, p. 16): share of variables whose ten responses all agree / share where 1-2 of 10 responses differ / share where 3-5 of 10 differ.

| Method | Claude 3.5 | GPT-4o |
| --- | :---: | :---: |
| Direct | 65.1% / 18.0% / 16.9% | 63.4% / 18.0% / 18.6% |
| Indirect | 75.6% / 19.2% / 5.2% | 40.1% / 37.2% / 22.7% |
| Pick-from-list | 57.6% / 42.4% / none | 57.6% / 42.4% / none |
| Sequential | 53.5% / 30.2% / 16.3% | 35.5% / 38.4% / 26.2% |

The text (p. 16) says sequential prompting was least consistent and pick-from-list most consistent, with 75% of pick-from-list variables giving the same result 97% of the time or more. The text gives the GPT-4o indirect 3-5/10 share as 22.6%; Fig 8 shows 22.7%.

Option-ordering 0% ↔ 100% flips (Fig 11, p. 18):

| Model | % of variables flipping Never ↔ Always on option order alone |
| --- | :---: |
| Claude 3.5 | 5.8% (text p. 18: 4.6%) |
| GPT-4o | 16.3% |

- PDF check 2026-11-24: source version: pages now cite the 2026 journal article (J Causal Inference 14(1), article 20240072, printed pp. 1-30, doi 10.1515/jci-2024-0072); the arXiv v1 (2024) PDF is kept as "Archive - superseded versions/Archive - Huntington-Klein and Murray - 2024.pdf"
- PDF check 2026-11-24: title "kappa as low as 0.16" -> "kappa as low as 0.13" (the lowest kappa reported is 0.13: GPT-4o, direct prompt with vs. without reasoning, p. 17, and GPT-4o option order, p. 18; 0.16 is only the lowest direct-vs-indirect value); file renamed; the finding itself still holds in the 2026 version
- PDF check 2026-11-24: Description quote "For GPT o1-preview, there was fair agreement ... .16. Claude 3.5 Sonnet saw only 66.9% ... .21. GPT-4o produced a similar Cohen's kappa of .24." (Huntington-Klein & Murray, 2024, p. 14-15) -> the same passage in the journal wording, split at the page break: (Huntington-Klein & Murray, 2026, p. 16) and (2026, p. 17); ".16" -> "0.16", ".21" -> "0.21", ".24" -> "0.24", "87.7%" -> "87.7 %", "Claude 3.5 Sonnet" -> "Claude 3.5-Sonnet"; the old quote also left out a sentence without marking the cut, the new one is contiguous
- PDF check 2026-11-24: Description quote "In Claude 3.5, 36.7% of variables had different designations ..., leading to a Cohen's kappa of .13." (2024, p. 16) -> "... leading to a Cohen’s kappa of 0.41. GPT-4o was less consistent, with 65.7 % of variables changing designation, leading to a Cohen’s kappa of 0.13." (2026, p. 18); error in both versions: .13 is GPT-4o's kappa, Claude's is 0.41
- PDF check 2026-11-24: Methods quote "In order to assess the consistency of LLM responses ..." (2024, p. 6) -> contiguous journal passage including the second paragraph "Second, we modify the direct prompt ..." (2026, p. 7); the old quote used an ellipsis between two paragraphs
- PDF check 2026-11-24: citation of "For the direct version of the prompt with reasoning, we elicited ..." (2024, p. 16) -> (2026, p. 18)
- PDF check 2026-11-24: citation of "GPT-4o and Claude 3.5 Sonnet are run using a temperature of 0.7 ..." (2024, p. 6) -> (2026, p. 7); wording "Claude 3.5 Sonnet" -> "Claude 3.5-Sonnet" and "raise the temperature" -> "change the temperature"; the journal inserts footnote 6 after "might give."
- PDF check 2026-11-24: comparison footnote (p. 11, fn 5) -> (2026, p. 16, fn 9); quote now verbatim with "Non-Confounder", "GPT-4o" and spaced percent signs
- PDF check 2026-11-24: figure references "figures 5–8", "Fig 5", "Figs 6–8" -> "Figures 8–11", "Fig 8", "Figs 9–11" (a new Fig 1 flowchart renumbered the figures)
- PDF check 2026-11-24: category labels "0% / Mixed / 100%" -> "Never / Mixed / Always" (the journal figures; "Always" = designated a confounder in all 10 iterations)
- PDF check 2026-11-24: Who? note "Non-Confounders measured at follow-up are omitted from the option-ordering analysis for GPT-o1-preview" -> "omitted from the cross-method agreement graph" (p. 16: "omitted from this graph" in the paragraph before Fig 9; GPT-o1 is not in the option-order figure at all); same wording in the 2024 version p. 14
- PDF check 2026-11-24: Claude option-order flips "4.6%" -> "5.8%" (Fig 11, p. 18, cell alternate = Always, main = Never; the paper's text on p. 18 says 4.6%; the figure is used, the text value is shown beside it)
- PDF check 2026-11-24: share of variables identically designated, "66.9% same" (Claude) and "87.7% same" (GPT-o1), kept as the paper's text values; Fig 9 (p. 17) diagonals give 53.0% (Claude), 55.8% (GPT-4o) and 67.5% (GPT-o1), and the kappas 0.21 and 0.16 match the figure, so the paper's two percentages look wrong (flagged for JP, not corrected)
- PDF check 2026-11-24: GPT-4o indirect 3-5/10 split "22.6%" -> "22.7%" (Fig 8, p. 16; the text says 22.6%, the figure is used)
- PDF check 2026-11-24: the direct panel of Fig 10 (p. 18) and Fig 11 (p. 18) show identical cell values and identical kappas (0.41 and 0.13), so the reasoning-vs-no-reasoning and option-order rows coincide; this may be a duplicated panel in the paper (flagged for JP, values kept as printed)
- PDF check 2026-11-24: new in the journal version: within-variable consistency rows for pick-from-list and sequential prompting (Fig 8), the sequential-vs-direct panel in Fig 9, the strongest kappas among the other method pairs (0.37 and 0.56, p. 17), and the statement that option-order sensitivity does not extend to pick-from-list (p. 18); the conclusions limit option-order sensitivity to "one prompting method" (p. 20)
- PDF check 2026-11-24: finding re-extracted from the 2026 tables: every kappa (0.16, 0.21, 0.24, 0.41, 0.13, 1.00) and the consistency shares 65.1/75.6% (Claude) and 63.4/40.1% (GPT-4o) are unchanged from arXiv v1

## Caveats

> [!info] Caveats applying to this evidence

- [[sysrev/dgraph/caveats/CVT - Huntington-Klein used a single causal dataset|CVT - The Huntington-Klein study used a single causal dataset limiting the scope of conclusions about LLM causal knowledge]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[sysrev/dgraph/claims/CLM - LLMs are not yet reliable causal knowledge sources for confounder selection|CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[sysrev/dgraph/evd-patterns/EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs|EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs]]
- [[sysrev/dgraph/evd-patterns/EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing|EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]

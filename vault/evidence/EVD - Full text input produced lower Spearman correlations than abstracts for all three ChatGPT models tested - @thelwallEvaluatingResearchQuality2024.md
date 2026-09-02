---
NodeFormality: draft
aliases:
tags:
  - task/decision-judgment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/46pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b60-7553-8f1e-3b1f4f0ae628
appraisal_overall: L0-M4-H1
tripod_llm_pct: 46pct
---

## Source

[[@thelwallEvaluatingResearchQuality2024]]

## Description

> "The optimal input for ChatGPT 3.5-turbo seems to be article abstracts (with titles)... Extending abstracts to truncated full texts decreases the correlation but restricting the input text to article titles substantially decreases it." (Thelwall, 2024, p. 7)
>
> ![[thelwallEvaluatingResearchQuality2024-evd-p7-1.png]]
>
> GPT-3.5-turbo Abstracts: 0.674, GPT-3.5-turbo Truncated text: 0.625; GPT-4o Abstracts: 0.678, GPT-4o Truncated text: 0.675 (Table 1, p. 8)

> ![[thelwallEvaluatingResearchQuality2024-tables-p8-1.png]]

## Methods Context

### What?

> **Study design:** within-corpus input-format ablation embedded in a single-author convenience-sample LLM evaluation.
>
> **Method type:** repeated zero-shot LLM scoring (30 iterations averaged) under three input-text conditions, with rank-correlation comparison against author REF scores.
>
> **Tools:** OpenAI ChatGPT API (GPT-3.5-turbo, GPT-4o, GPT-4o-mini); PyMuPDF + Webometric Analyst for text cleanup; REF 2021 system prompt (Strategy 6, Appendix 1).
>
> **Dependent variable:** per-cell Spearman correlation between the 30-iteration mean ChatGPT score and the author's REF score.
>
> **Independent variable:** input text format, Title only / Abstract (title+abstract) / Truncated full text (full text minus references, tables, figures, authors, keywords). Held constant within each model row: model identity, system prompt, temperature=1, top_p=1, max_tokens=1000, the 51-article corpus, and the 30-iteration averaging procedure.
>
> "This article assesses which ChatGPT inputs (full text without tables, figures and references; title and abstract; title only) produce better quality score estimates, and the extent to which scores are affected by ChatGPT models and system prompts." (Thelwall, 2024, p. 1)
> ![[thelwallEvaluatingResearchQuality2024-evd-p1-1.png]]

### How?

> **Procedure:** (1) Three parallel input datasets built from the same 51 articles, *Truncated* (full text without references, tables, figures, authors, keywords), *Abstract* (title + abstract only), *Title* (titles only). (2) For each (model × input) cell, run 30 consecutive ChatGPT API calls per article carrying the Strategy 6 system prompt and the user prompt `"Score the following journal article: " + <article text>`. Parameters fixed at temperature=1, top_p=1, max_tokens=1000. (3) Extract the model score from each free-text report with pattern-matching software; missing scores dropped from per-article averages; score ranges averaged to midpoint. (4) Compute the Spearman correlation between the per-article mean ChatGPT score and the author's REF score for each cell. (5) For the iteration-count subanalysis, compute correlations for each k ∈ {1…30} via subset permutations and average; t-distribution confidence intervals derived from the SD across permutations. Figure 1 (3.5-turbo) and Table 1 (all three models) report the per-input correlations side by side.
>
> "Several different datasets were generated to try different extents of input. Truncated dataset: This consisted of the full text files without the reference list (not strongly relevant), the contents of tables (difficult to process by an LLM), the authors, and the keywords. … Abstract dataset: This consisted of the title and abstract alone after removing the authors, keywords and the remaining text. Title dataset: This consisted of article titles alone." (Thelwall, 2024, p. 4)
> ![[thelwallEvaluatingResearchQuality2024-evd-p4-1.png]]

### Who?

> **Participants / data:** same 51 information-science journal articles as the parent study, all written by the author and gold-scored by him on the REF 1*–4* scale.
>
> **Sample-size flow:** 51 articles → each article processed under all three input formats → 30 iterations per (model × input) cell → per-article mean → Spearman correlation across all 51 articles. No exclusions applied at the input-format step (per-article averages drop only individual missing scores from within the 30 iterations).
>
> **Models compared:** GPT-3.5-turbo (3 input cells), GPT-4o (3 input cells), GPT-4o-mini (3 input cells), 9 (model × input) cells total feeding Table 1.
>
> "The raw data for this paper is a set of 51 information science journal articles that have either been published or prepared for submission and subsequently rejected or not submitted. All were written by the author, who has copyright, and were scored by him using the REF quality scale of 1*, 2*, 3* or 4* (REF, 2019), with which he is familiar." (Thelwall, 2024, p. 3)
> ![[thelwallEvaluatingResearchQuality2024-evd-p3-1.png]]

## Other Notes

- The result that abstracts outperform full text is counterintuitive and may reflect LLM difficulty processing long documents or noise in full-text formatting; author hypothesizes the abstract concentrates originality/significance signals while full text "obscures the main value of an article by including less relevant text that an LLM could pay partial attention to."
- Title-only input is non-trivial (r ≈ 0.43 for GPT-3.5-turbo, even higher for GPT-4o at 0.539), but substantially below abstracts.
- Cross-cell correlation between truncated-text and abstract predictions is 0.754 within GPT-3.5-turbo (Table 1), suggesting the two inputs carry largely overlapping signal but the abstract version is cleaner.
- The full-text → abstract gap is largest for GPT-4o-mini (0.571 vs. 0.506; Δ = +0.065 favoring abstracts) and smallest for GPT-4o (0.678 vs. 0.675; Δ ≈ 0).

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@thelwallEvaluatingResearchQuality2024#TRIPOD-LLM reporting summary]].

| Model | Titles (r) | Abstracts (r) | Truncated text (r) | Δ Abstract − Truncated |
| --- | :---: | :---: | :---: | :---: |
| **GPT-3.5-turbo** | 0.434 | **0.674** | 0.625 | **+0.049** |
| **GPT-4o** | 0.539 | **0.678** | 0.675 | **+0.003** |
| **GPT-4o-mini** | — | **0.571** | 0.506 | **+0.065** |

| Cross-input agreement (GPT-3.5-turbo, n=51) | Spearman r |
| --- | :---: |
| Abstracts ↔ Truncated text | 0.757 |
| Abstracts ↔ Titles | 0.439 |
| Truncated text ↔ Titles | 0.444 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Abstracts are the optimal input for LLM-based research quality assessment outperforming full text]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Adding more input context can degrade rather than improve LLM performance on structured tasks]]

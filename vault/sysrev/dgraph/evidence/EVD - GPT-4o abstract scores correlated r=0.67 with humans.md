---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - GPT-4o abstracts achieved Spearman r=0.67 with human quality scores on 51 information science articles the highest reported"
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
updated: 2026-11-24
nodeID: 019ddb4e-6b70-756a-bcc7-52d8e587f5fd
appraisal_overall: L0-M4-H1
tripod_llm_pct: 46pct
title: "GPT-4o abstracts achieved Spearman r=0.67 with human quality scores on 51 information science articles the highest reported"
---

## Source

[[@thelwallEvaluatingResearchQuality2024]]

## Description

> "The optimal input is the article title and abstract, with average ChatGPT scores based on these (30 iterations on a dataset of 51 papers) correlating at 0.67 with human scores, the highest ever reported." (Thelwall, 2025, p. 7)

> ![[thelwallEvaluatingResearchQuality2024-evd-p1-4.png]]
>
> "GPT-4o Abstracts" Spearman correlation = 0.678 (Table 1, Thelwall, 2025, p. 15)

> ![[thelwallEvaluatingResearchQuality2024-tables-p9-1.png]]

## Methods Context

### What?

> **Study design:** single-author, single-field convenience-sample LLM evaluation (post-publication research-quality scoring).
>
> **Method type:** zero-shot LLM scoring against the UK REF 2021 1*–4* quality scale, with 30 independent API calls per article averaged into a per-article model score.
>
> **Tools:** OpenAI ChatGPT API (GPT-3.5-turbo, GPT-4o, GPT-4o-mini); REF 2021 Main Panel D guidelines (information science) as the system prompt; Webometric Analyst utilities for PDF cleanup, score extraction, and correlation analysis.
>
> **Dependent variable:** Spearman rank correlation between the 30-iteration mean ChatGPT score and the author's REF self-evaluation score across the 51 articles.
>
> **Independent variables / covariates:** model identity (3.5-turbo / 4o / 4o-mini); input format (title only / title+abstract / truncated full text); number of iterations averaged (1–30); system-prompt strategy (Strategies 0–6).
>
> "The overall research design was to run a series of experiments guided by the research questions on a set of 51 articles with quality scores, using the ChatGPT API environment. For each experiment, the ChatGPT completion requests were carried out consecutively and then repeated a further 29 times to give 30 scores for each article." (Thelwall, 2025, p. 10)
> ![[thelwallEvaluatingResearchQuality2024-evd-p4-3.png]]

### How?

> **Procedure:** (1) Articles converted from PDF/Word to text via PyMuPDF and Word's Save-As; cleaned with Webometric Analyst utilities (header/footer removal, paragraph merging) plus manual checking; converted to JSONL for the API. (2) Three input datasets built, Truncated (full text minus references, tables, figures, authors, keywords), Abstract (title+abstract only), Title (titles only). (3) Each scoring request was a single API call carrying the system prompt (Strategy 6 = full REF guidelines, Appendix 1) and the user prompt `"Score the following journal article:"` + the article text. Parameters: temperature=1, top_p=1, max_tokens=1000. (4) Each article scored 30 times per (model × input) cell; queries submitted July 2024. (5) Scores extracted from free-text reports via pattern-matching ("Webometric Analyst: AI|ChatGPT: extract REF scores from report"); rule example, extract the number between `"Overall Score**: **"` and `"*"`; missing scores ignored from per-article averages; ranges averaged to midpoint. (6) Spearman correlation computed between the per-article mean ChatGPT score and the author's REF score; for n-iteration analysis, confidence intervals from t-distribution over permutations of iteration subsets.
>
> "... instructions, as in Appendix 1, and with the prompt, "Score the following journal article:", followed by the article title/abstract/truncated text, as relevant. The maximum temperature parameter was set to 1, the default, the top_p parameter was also set to its default of 1, and the max_tokens parameter was set to 1000, which seemed adequate for the typical reports written by ChatGPT in the previous study (Thelwall, 2024)." (Thelwall, 2025, p. 12)
> ![[thelwallEvaluatingResearchQuality2024-evd-p6-1.png]]

### Who?

> **Participants / data:** no human subjects beyond the single author–scorer. The analyzed units are scientific journal articles, with the author providing the gold REF scores from memory of his own work.
>
> **Articles (sample-size flow):** the author's own information-science output → restricted to articles he had copyright over and could share with the API → **51 articles** (published, prepared-for-submission, or rejected/not-submitted); none had been disclosed to any AI system before this study. Author scored each on the REF 1*/2*/3*/4* scale, allowing mid-scores (e.g., 3.5*) for borderline cases.
>
> **Models evaluated:** GPT-3.5-turbo, GPT-4o, GPT-4o-mini (no specific snapshot version reported beyond July-2024 inference date).
>
> **Annotators / scorers:** 1 (the author himself, who is also the corpus owner).
>
> "The raw data for this paper is a set of 51 information science journal articles that have either been published or prepared for submission and subsequently rejected or not submitted. All were written by the author, who has copyright, and were scored by him using the REF quality scale of 1*, 2*, 3* or 4* (REF, 2019), with which he is familiar." (Thelwall, 2025, p. 10)
> ![[thelwallEvaluatingResearchQuality2024-evd-p4-2.png]]

## Other Notes

- Single-iteration Spearman r is much lower than the 30-iteration value: about 0.44 for GPT-4o abstracts and about 0.38 to 0.39 for the other two models (read from the plot in Figure 2; the text gives no single-iteration value). Averaging 30 iterations raises GPT-4o abstracts to 0.678, about 1.5 times the single-iteration value, not double.
  Grounding figure (Figure 2, p. 16): ChatGPT 4o-mini, ChatGPT 3.5-turbo and ChatGPT 4o score prediction correlations against human scores by number of iterations averaged.
  ![[thelwallEvaluatingResearchQuality2024-fig-p10-1.png]] Authors note "five might be taken as sufficient for general purposes and additional iterations used when more precise estimates are needed" (Thelwall, 2025, p. 19).
- The dataset is explicitly acknowledged as a convenience sample from a single author's work and a single field; author scores are self-evaluations, not REF panel scores.
- Linear regression (intercept −3.40, coefficient 2.05 for GPT-4o Abstracts) maps model scores onto the REF scale and reduces MAD by 31% vs. the baseline of guessing the corpus mean (2.75).
- Paper-level mean correlation between GPT-4o-Abstract predictions and predictions from other (model × input) cells is very high (e.g., 0.875 with GPT-3.5-turbo Abstracts), suggesting the underlying language models extract similar quality signals.
- PDF check 2026-11-24: source version: pages now cite the 2025 journal article (J Data Inf Sci 10(1), 7-25, doi 10.2478/jdis-2025-0011) with printed journal page numbers; the 2024 preprint is kept as "Archive - superseded versions/Archive - Thelwall - 2024.pdf"
- PDF check 2026-11-24: citation of "The optimal input is the article title and abstract, with av..." (Thelwall, 2024, p. 1) -> (Thelwall, 2025, p. 7)
- PDF check 2026-11-24: citation (Table 1, Thelwall, 2024, p. 8) -> (Table 1, Thelwall, 2025, p. 15)
- PDF check 2026-11-24: citation of "The overall research design was to run a series of experimen..." (Thelwall, 2024, p. 3) -> (Thelwall, 2025, p. 10)
- PDF check 2026-11-24: quote "Each score request was a single API call, specifying a ChatGPT model,..." -> verbatim journal wording: "... instructions, as in Appendix 1, and with the prompt, "Score the following journal article:", followed by the article title/abstract/truncated text, as relevant. The maximum temperature parameter was set to 1, the default, the top_p parameter was also set to its default of 1, and the max_tokens parameter was set to 1000, which seemed adequate for the typical reports written by ChatGPT in the previous study (Thelwall, 2024)." (the passage now runs across the journal page break at pp. 11-12; the quote is shortened to the part on p. 12, and the prompt is typeset without a trailing space)
- PDF check 2026-11-24: citation of "Each score request was a single API call, specifying a ChatG..." (Thelwall, 2024, p. 5) -> (Thelwall, 2025, p. 12)
- PDF check 2026-11-24: citation of "The raw data for this paper is a set of 51 information scien..." (Thelwall, 2024, p. 3) -> (Thelwall, 2025, p. 10)
- PDF check 2026-11-24: prompt text in How? `"Score the following journal article: "` -> `"Score the following journal article:"` (journal wording has no trailing space, p. 12)
- PDF check 2026-11-24: quote "...for general purposes but additional iterations used..." -> "...for general purposes and additional iterations used..." (Thelwall, 2025, p. 19; wording changed in the journal copy edit)
- PDF check 2026-11-24: single-iteration r "~0.40" and "averaging 30 iterations roughly doubles correlation" -> "about 0.44 (GPT-4o), 0.38-0.39 (other two), about 1.5 times at 30 iterations" (read from Figure 2, p. 16; approximate, figure values not tabulated)
- PDF check 2026-11-24: added the Table 3 screenshot (p. 18) that backs the Direct MAD, regression intercept, coefficient, MAD and improvement columns; every value in those columns matches Table 3 (no change)

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@thelwallEvaluatingResearchQuality2024#TRIPOD-LLM reporting]].

| Model × Input (n=51, 30 iters averaged) | Spearman r vs. human | Direct MAD | Regression intercept | Regression coefficient | Regression MAD | MAD improvement vs. baseline |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **GPT-4o: Abstracts** | **0.678** | **0.62** | **−3.40** | **2.05** | **0.50** | **31%** |
| GPT-4o: Truncated text | 0.675 | 0.69 | −4.44 | 2.28 | 0.50 | 31% |
| GPT-3.5-turbo: Abstracts | 0.674 | 0.60 | −3.46 | 2.26 | 0.51 | 30% |
| GPT-3.5-turbo: Truncated text | 0.625 | 0.70 | −7.49 | 3.38 | 0.55 | 24% |
| GPT-4o-mini: Abstracts | 0.571 | 0.63 | −3.32 | 2.07 | 0.59 | 19% |
| GPT-4o-mini: Truncated text | 0.506 | 0.75 | −2.44 | 1.61 | 0.60 | 17% |
| GPT-3.5-turbo: Titles | 0.434 | 0.68 | −1.16 | 1.57 | 0.63 | 13% |

Grounding table (Table 3, p. 18): Mean Average Deviations for direct predictions and predictions with linear regression for each model and input.

> ![[thelwallEvaluatingResearchQuality2024-tables-p12-1.png]]

| Comparator (prior work, same 51 articles) | Spearman r |
| --- | :---: |
| ChatGPT-4 web interface, full PDFs, 15-iter avg (Thelwall 2024) | 0.51 |
| Best ML+bibliometric REF-prediction (Pearson, Clinical Medicine; Thelwall et al. 2023) | 0.562 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Thelwall dataset was 51 articles by one author|CVT - The Thelwall dataset consisted of 51 articles by a single author limiting generalizability to other researchers and fields]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Abstracts beat full text as input for LLM quality assessment|CLM - Abstracts are the optimal input for LLM-based research quality assessment outperforming full text]]

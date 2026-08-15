---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M1-H4
  - tripod-llm/compliance/low
  - tripod-llm/proportion/26pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b5a-74fa-a013-72e50c0f1cfd
appraisal_overall: L0-M1-H4
tripod_llm_pct: 26pct
---

## Source

[[@robertsComparativeStudyChatGPT2023]]

## Description

> "Bland-Altman analysis revealed a mean difference of 4.92% (95% CI 0.62%, 0.37%) in OCS between human evaluation and ChatGPT." (Roberts et al., 2023, p. 3)
>
> ![[robertsComparativeStudyChatGPT2023-evd-p3-1.png]]
> [Screenshot: Figure 2 (Bland-Altman plot) and Table 1, p. 3 — error analysis of ChatGPT CONSORT-A OCS subscores. Extract with: pdftoppm -f 3 -l 3 -r 250 -png "<pdf_path>" "robertsComparativeChatGPT2023-fig2table1-p3"]

## Methods Context

### What?

> **Study design:** cross-sectional method-comparison / agreement study (LLM vs. human gold standard). **Method type:** zero-shot LLM evaluation against human consensus scores. **Tools:** OpenAI ChatGPT (described as "GPT3.5 model" / "ChatGPT3"; no version pin or inference timestamp); CONSORT-A 15-item abstract reporting checklist (Moher et al. 2010); R v4.1.1 for statistics. **Dependent variable:** overall compliance score (OCS, 0–15) and OCS percentage per abstract; agreement quantified via Bland-Altman mean difference and 95% limits of agreement. **Independent variables / covariates:** evaluator (human consensus vs. ChatGPT) per the same 30 abstracts.
>
> "We compared ChatGPT's scoring of implant dentistry abstracts with human evaluators using the Consolidated Standards of Reporting Trials for Abstracts reporting standards checklist, yielding an overall compliance score (OCS). Bland-Altman analysis assessed agreement between human and AI-generated OCS percentages." (Roberts et al., 2023, p. 1)
> ![[robertsComparativeStudyChatGPT2023-evd-p1-1.png]]

### How?

> **Procedure:** (1) Re-use of 30 implant-dentistry RCT abstracts previously CONSORT-A-scored by Menne, Pandis & Faggion (2021). (2) Two clinician reviewers re-scored the same 30 abstracts independently and in duplicate; discrepancies reconciled through discussion until ≥80% consensus, after which one reviewer continued solo data extraction. (3) For each abstract, ChatGPT (GPT-3.5) was prompted with a fixed zero-shot template — Figure 1A — containing the full CONSORT-A item definitions, asked to label each of the 15 items as completely / partially / not reported, then to compute OCS = (1·I_C) + (0.5·I_P) + (0·I_N) and OCS% = OCS/15·100. (4) Bland-Altman analysis on the 30 paired OCS% values; per-domain mean absolute difference, Welch's two-sample t-test, and Pearson's r as supporting analyses. P<0.001 was the significance threshold; statistics in R v4.1.1.
>
> "Bland-Altman analysis was used to evaluate the overall agreement between human and ChatGPT-generated OCS percentage. For error analysis, the mean difference of the absolute OCS subscores, Welch's two-sample t-test and Pearson's correlation coefficient were undertaken… Statistical analysis was done in R (V.4.1.1). P<0.001 was deemed statistically significant." (Roberts et al., 2023, p. 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-7.png]]

### Who?

> **Models / participants:** ChatGPT GPT-3.5 (OpenAI; closed-source, no version pin reported); two human clinician reviewers (specialty / training stage not reported). Inference parameters (temperature, top_p, system prompt, seed) not reported; runs not repeated.
>
> **Sample-size flow:** Menne, Pandis & Faggion (2021) systematic review on implant-dentistry RCT abstracts → **30 abstracts** sampled by the original authors → re-scored independently by two clinician reviewers (≥80% consensus reconciliation, then one reviewer continued) → same 30 abstracts each scored once by ChatGPT → **30 paired OCS% values** entered the Bland-Altman analysis. No exclusions or refusals reported.
>
> "In this study, we used a previously published paper as the basis of our comparison with ChatGPT… The processes of selection and data extraction were performed independently and in duplicate by two clinician reviewers across a sample of 30 abstracts. Discrepancies were systematically addressed through discussion until a consensus of at least 80% was achieved. Subsequent data extraction was conducted solely by one reviewer." (Roberts et al., 2023, pp. 1, 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p1-2.png]]

## Other Notes

- The 95% CI on the Bland-Altman mean difference is reported in the paper as "(0.62%, 0.37%)" — the lower bound exceeds the upper bound, indicating a likely typesetting/sign error (probably should read "−0.62%, ±… %" or similar limits-of-agreement values). The point estimate of 4.92% is consistent across abstract, results, and figure caption.
- Interpretation: a 4.92 percentage-point mean difference on a 100-point OCS scale corresponds to roughly 0.74 of a single CONSORT-A item — small in aggregate but driven by large per-domain divergences (see the conclusion-domain EVD).
- Per-paper Pearson r is not reported — only per-domain r values appear in Table 1.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@robertsComparativeStudyChatGPT2023#TRIPOD-LLM reporting summary]].

| Agreement metric (overall OCS%) | Value |
| --- | --- |
| Bland-Altman mean difference (Human OCS% − ChatGPT OCS%) | **4.92%** |
| Reported 95% CI (as printed) | (0.62%, 0.37%) — likely typesetting error |
| n (paired abstracts) | 30 |
| Significance threshold used | p<0.001 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - ChatGPT evaluation was restricted to abstracts only due to token length constraints]]

- [[CVT - The Roberts study used only GPT-3.5 and did not test GPT-4 or other LLMs]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]

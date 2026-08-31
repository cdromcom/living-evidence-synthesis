---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/error-detection
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/54pct
  - 5c/credibility
  - forensic/monotonicity-check/consistent
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7f-7021-ba29-15252b4379b8
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
---

## Source

[[@zhangReviewingScientificPapers2025a]]

## Description

> "The OpenAI o3 model performed the best, while o4-mini was the most cost-effective one in our evaluation." (Zhang & Abernethy, 2025, p. 1)
> Table 2 shows o3 (medium): HR@5=64.9% (PDF), 71.0% (LaTeX); cost $0.321/paper (PDF), $0.383/paper (LaTeX). (p. 4)
>
> ![[zhangReviewingScientificPapers2025a-results-p4-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of reasoning LLMs as paper quality checkers on a withdrawn-from-arXiv evaluation set, with an LLM-as-judge automatic evaluation pipeline.
>
> **Method type:** zero-shot LLM evaluation under a fixed simplistic prompt; no fine-tuning.
>
> **Tools:** OpenAI o3 (`2025-04-16`, reasoning effort = medium) accessed via OpenAI API in Python; WITHDRARXIV-CHECK evaluation set derived from WITHDRARXIV (Rao et al. 2024); two LLM judges (Gemini 2.5 Pro `preview-05-06` and o3 `2025-04-16`).
>
> **Dependent variables:** Hit Rate at k=5 (HR@5; share of test papers for which the checker submits at least one problem that majority-vote LLM judges accept as an exact match to the gold retraction-comment error), average / Q1 / Q3 number of problems identified, average input/think/output token usage, and estimated USD cost per paper.
>
> **Independent variables / covariates:** paper-ingestion approach (PDF attachment vs. LaTeX script in prompt); checker model identity (held to o3 for this EVD; Gemini 2.5 Pro/Flash, o4-mini, Claude 3.7 Sonnet for comparison); judge identity (Gemini 2.5 Pro vs. o3, with majority-of-2 fusion).
>
> "Each LLM judge independently evaluates an LLM quality checker's problem submissions one by one for $n_j$ ($j$ for judge) times to determine whether they contain an exact match to the gold error description from the authors… If an LLM quality checker receives a majority of (or all, for a stricter evaluation) affirmative votes from LLM judges, it is deemed to have made a hit on the paper. LLM quality checkers were primarily evaluated by their hit rates on test papers." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-4.png]]

### How?

> **Procedure:** (1) Build the WITHDRARXIV-CHECK dataset by filtering WITHDRARXIV with Gemini 2.5 Flash (`preview-04-17`) on de-identified retraction comments to retain only cases that clearly specify the error (n=2,190), then manually exclude (a) misclassified, (b) different-version-of-same-paper, (c) non-English, (d) template-like ("crucial sign error in equation 1") cases that dominated early years, (e) problems unlikely to be detectable from the manuscript alone, and correct redacted theorem names — final n=1,225. (2) Random 80/20 train/test split → 245 test papers. (3) For each test paper, prompt o3 once ($n_c=1$) with the simplistic Appendix A instruction asking for up to $k=5$ critical errors as a JSON list (`Problem`, `Location`, `Explanation`); ingest the paper as PDF attachment (top-half block) or LaTeX script in prompt (bottom-half block); temperature/seed not supported for o3, reasoning effort = "medium", reasoning summary = "detailed", no tools/web. (4) Each problem submission is independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3, each shown the original retraction comment and asked "Did my colleague find exactly the same problem?" Yes/No. (5) Under $m=2$ judges, both must vote Yes for a hit. (6) HR@5 = (papers with ≥ 1 confirmed hit)/245. (7) Per-paper cost estimated from recorded token usage at early-May-2025 OpenAI pricing.
>
> "In this work, we took $k=5$, $n_c=1$, $n_j=1$, and $m=2$, i.e., each LLM quality checker was tested once with each paper and was instructed to report up to 5 problems, and 2 LLMs served as judges, each judging a problem submission once… We set model temperature to 0 and fixed the decoding seed if possible to minimize answer variability, although reasoning models may still have inherent uncertainty. Reasoning effort or thinking budget was kept as the default or automatic setting if applicable. LLMs were not given access to any tools, including web search." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-5.png]]

### Who?

> **Models / participants:** no human subjects. The "participants" are the 5 reasoning LLMs evaluated as checkers (Gemini 2.5 Pro, Gemini 2.5 Flash, o3 medium, o4-mini medium, Claude 3.7 Sonnet) plus 2 LLM judges (Gemini 2.5 Pro, o3 medium). This EVD reports o3's checker results.
>
> **Sample-size flow (papers):** WITHDRARXIV "factual/methodological/other critical errors" category n=6,018 candidate withdrawn arXiv papers → Gemini 2.5 Flash filter on de-identified retraction comments → 2,190 with clearly-specified errors → manual exclusion of misclassified / duplicate-version / non-English / template / not-manuscript-detectable cases (+ theorem-name de-redaction) → **WITHDRARXIV-CHECK n=1,225** → random 80/20 split → train n=980 (set aside, not used here), **test n=245**.
>
> **Test-set composition (n=245):** time span 2007–2012 13% / 2013–2018 47% / 2019–2024 40%; main subject Math 52% / Physics 29% / CS 15% / Other 4%; median page count 14 (range 2–136); LaTeX source available for 216/245 (88%) — papers without LaTeX source fall back to the PDF-approach result.
>
> "We utilized WITHDRARXIV (Rao et al., 2024), a large-scale dataset of papers withdrawn from arXiv by September 2024, along with associated retraction comments from authors and well-defined retraction categories. The most common retraction category, 'factual/methodological/other critical errors in manuscript', contains 6,018 candidate cases with critical errors that would potentially invalidate study conclusions… The final dataset, named WITHDRARXIV-CHECK, contains 1,225 cases. We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments." (Zhang & Abernethy, 2025, p. 2)
> ![[zhangReviewingScientificPapers2025a-evd-p2-1.png]]

## Other Notes

- o3's HR@5 jumped from 64.9% (PDF) to 71.0% (LaTeX), suggesting OpenAI o-series models received specialized LaTeX training. Single-judge HR@5s (Table 3): Gemini-2.5-Pro judge 72.7% (PDF) / 75.5% (LaTeX); o3 judge 75.5% (PDF) / 80.4% (LaTeX) — both-judges-affirm fusion drops these to 64.9% / 71.0%, demonstrating resistance of multi-judge approach to inflation.
- o3 used markedly fewer thinking tokens than the Gemini family (3,152 vs. 14,228 for Gemini 2.5 Pro under PDF), yet achieved the highest HR — "potentially overthinking behavior did not result in higher hit rates."

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting summary]].

| Condition | HR@5 | Avg. # problems (Q1, Q3) | Input tok | Think tok | Output tok | $/paper |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **o3 (medium) — PDF** | **64.9%** | 4.8 (5, 5) | 16,594 | 3,152 | 729 | $0.321 |
| **o3 (medium) — LaTeX** | **71.0%** | 4.8 (5, 5) | 21,990 | 3,156 | 927 | $0.383 |
| Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 72.7% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / PDF) | 75.5% | — | — | — | — | — |
| Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 75.5% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / LaTeX) | 80.4% | — | — | — | — | — |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives]]

- [[CVT - The error detection dataset was rich in math and physics papers and may not generalize to other scientific domains]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

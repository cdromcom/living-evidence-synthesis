---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers"
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
updated: 2026-11-24
nodeID: 019ddb4e-6b7f-7021-ba29-15252b4379b8
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
title: "OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers"
---

## Source

[[@zhangReviewingScientificPapers2025a]]

## Description

> "o3 exhibited the best problem identification performance among all models at a modest cost." (Zhang & Abernethy, 2026, p. 1)
>
> ![[zhangReviewingScientificPapers2025a-v3-o3-desc-p1.png]]
>
> Table 2 shows o3 (medium): HR@5=48.2% (PDF), 50.6% (LaTeX); cost $0.064/paper (PDF), $0.077/paper (LaTeX). (p. 5)
>
> Grounding table (Table 2, p. 5): problems found, HR@5, AP@5, token usage and cost per paper for the five checkers under PDF and LaTeX input.
>
> ![[zhangReviewingScientificPapers2025a-v3-table2-p5.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of reasoning LLMs as paper quality checkers on a withdrawn-from-arXiv evaluation set, with an LLM-as-judge automatic evaluation pipeline.
>
> **Method type:** zero-shot LLM evaluation under a fixed simplistic prompt; no fine-tuning.
>
> **Tools:** OpenAI o3 (`2025-04-16`, reasoning effort = medium) accessed via OpenAI API in Python; WITHDRARXIV-CHECK evaluation set derived from WITHDRARXIV (Rao et al. 2024); two LLM judges (Gemini 2.5 Pro `preview-06-05` in v3, `preview-05-06` in v1; and o3 `2025-04-16`) (p. 4).
>
> **Dependent variables:** Hit Rate at k=5 (HR@5; share of test papers for which the checker submits at least one problem that majority-vote LLM judges accept as an exact match to the gold retraction-comment error), Average Precision at k=5 (AP@5; new in v3, PDF approach only: per-paper share of submissions that both judges rate as true problems against the PDF, averaged over papers, p. 4), average / Q1 / Q3 number of problems identified, average input/think/output token usage, and estimated USD cost per paper.
>
> **Independent variables / covariates:** paper-ingestion approach (PDF attachment vs. LaTeX script in prompt); checker model identity (held to o3 for this EVD; Gemini 2.5 Pro/Flash, o4-mini, Claude 3.7 Sonnet for comparison); judge identity (Gemini 2.5 Pro vs. o3, with majority-of-2 fusion).
>
> "Each LLM judge independently evaluates an LLM checker's problem submissions one by one for nj (j for judge) times to determine whether they contain an exact match to the gold error description from the authors… If an LLM checker receives a majority of (or all, for a stricter evaluation) affirmative votes from LLM judges, it is deemed to have made a hit on a paper. LLM checkers were primarily evaluated by their hit rates on test papers." (Zhang & Abernethy, 2026, p. 3)
> ![[zhangReviewingScientificPapers2025a-v3-o3-what-p3.png]]

### How?

> **Procedure:** (1) Build the WITHDRARXIV-CHECK dataset by filtering WITHDRARXIV with Gemini 2.5 Flash (`preview-04-17`) on de-identified retraction comments to retain only cases that clearly specify the error (n=2,190), then manually exclude (a) misclassified, (b) different-version-of-same-paper, (c) non-English, (d) template-like ("crucial sign error in equation 1") cases that dominated early years, (e) problems unlikely to be detectable from the manuscript alone, and correct redacted theorem names, final n=1,225. (2) Random 80/20 train/test split → 245 test papers. (3) For each test paper, prompt o3 once ($n_c=1$) with the simplistic Appendix A instruction asking for up to $k=5$ critical errors as a JSON list (`Problem`, `Location`, `Explanation`); ingest the paper as PDF attachment (top-half block) or LaTeX script in prompt (bottom-half block); temperature/seed not supported for o3, reasoning effort = "medium", reasoning summary = "auto" (Appendix B, p. 11; v1 listed "detailed"), no tools/web. (4) Each problem submission is independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3, each shown the original retraction comment and asked "Is my colleague referring to exactly the same problem mentioned in the retraction comment?" (Yes/No; Appendix A, p. 11). (5) Under $m=2$ judges, both must vote Yes for a hit. (6) HR@5 = (papers with ≥ 1 confirmed hit)/245. (7) Per-paper cost estimated from recorded token usage at standard June-2025 OpenAI API pricing (p. 4; v1 used early-May-2025 pricing). (8) New in v3: each judge also rates each problem submission as a true problem or a false alarm with the paper PDF attached, and both must affirm for a true positive, giving AP@5 under the PDF approach only (p. 4).
>
> "In this work, we took k = 5, nc = nj = 1, and m = 2, i.e., each LLM checker was tested once with each paper and was allowed to report up to 5 problems, and 2 LLMs served as judges, each judging a problem submission once." (Zhang & Abernethy, 2026, p. 4)
> ![[zhangReviewingScientificPapers2025a-v3-o3-how-a-p4.png]]
>
> "LLMs were accessed via their official APIs using Python. Model parameters used are provided in Appendix B. Reasoning effort or thinking budget was kept as the default or automatic setting if applicable. LLMs were not given access to any tools, including web search since LLMs might find the retraction comments online." (Zhang & Abernethy, 2026, p. 4)
> ![[zhangReviewingScientificPapers2025a-v3-o3-how-b-p4.png]]

### Who?

> **Models / participants:** no human subjects. The "participants" are the 5 reasoning LLMs evaluated as checkers (Gemini 2.5 Pro, Gemini 2.5 Flash, o3 medium, o4-mini medium, Claude 3.7 Sonnet) plus 2 LLM judges (Gemini 2.5 Pro `preview-06-05` in v3, o3 medium). This EVD reports o3's checker results.
>
> **Sample-size flow (papers):** WITHDRARXIV "factual/methodological/other critical errors" category n=6,018 candidate withdrawn arXiv papers → Gemini 2.5 Flash filter on de-identified retraction comments → 2,190 with clearly-specified errors → manual exclusion of misclassified / duplicate-version / non-English / template / not-manuscript-detectable cases (+ theorem-name de-redaction) → **WITHDRARXIV-CHECK n=1,225** → random 80/20 split → train n=980 (set aside, not used here), **test n=245**.
>
> **Test-set composition (n=245):** time span 2007–2012 13% / 2013–2018 47% / 2019–2024 40%; main subject Math 52% / Physics 29% / CS 15% / Other 4%; median page count 14 (range 2–136); LaTeX source available for 216/245 (88%), papers without LaTeX source fall back to the PDF-approach result.
>
> "We utilized WITHDRARXIV [Rao et al., 2024], a large-scale dataset of papers withdrawn from arXiv by September 2024, along with associated retraction comments from authors and well-defined retraction categories. The most common retraction category, "factual/methodological/other critical errors in manuscript", contains 6,018 candidate cases with critical errors that would potentially invalidate study conclusions, such as flawed experimental designs, incorrect data analyses, and proof/lemma errors [Rao et al., 2024]." (Zhang & Abernethy, 2026, p. 2)
> ![[zhangReviewingScientificPapers2025a-v3-o3-who-p2.png]]
>
> "We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments. The remaining 80% (980 cases) of the dataset was set aside for training and validation, although these latter two steps were not considered in this work whose main objective was to establish baseline approaches and evaluation methods." (Zhang & Abernethy, 2026, p. 2)
> ![[zhangReviewingScientificPapers2025a-v3-sample-split-p2.png]]
>
> Grounding table (Table 1, p. 3): train and test set characteristics (time span, main subject, page count, LaTeX availability).
>
> ![[zhangReviewingScientificPapers2025a-v3-table1-p3.png]]

## Other Notes

- o3's HR@5 rose only slightly from 48.2% (PDF) to 50.6% (LaTeX) (v3 Table 2, p. 5), which v3 reads as "resistance to format change or a higher familiarity with LaTeX" (p. 4) rather than v1's suggestion of specialized LaTeX training. Single-judge HR@5s (v3 Table 3, p. 6): Gemini-2.5-Pro judge 80.4% (PDF) / 79.2% (LaTeX); o3 judge 50.2% (PDF) / 51.4% (LaTeX); both-judges-affirm fusion drops these to 48.2% / 50.6%, which v3 describes as "some resistance" of the multi-judge approach "to potential false positives" (p. 5).
- o3 used markedly fewer thinking tokens than the Gemini family (3,152 vs. 14,228 for Gemini 2.5 Pro under PDF), yet achieved the highest HR, "this potentially overthinking behavior did not result in higher hit rates." (p. 5; token counts unchanged in v3 Table 2.)
- o3's lead over the next-best checker under PDF is 9.0 pp (48.2% vs. Gemini 2.5 Pro 39.2%; Table 2, p. 5). v3 adds AP@5 (PDF only), on which o3 scored 29.5%, below Gemini 2.5 Pro (35.2%) and Claude 3.7 Sonnet (36.4%); o3 produced the most submissions that both judges confirmed as true problems (350 vs. 293 for Gemini 2.5 Pro and 149 for Claude, p. 4).
- Version update 2026-11-24: this page moved from arXiv v1 (28 May 2025) to arXiv v3 (arXiv:2505.23824v3 [cs.CL], 1 Apr 2026; NeurIPS 2025 AI for Science workshop). Title, quotes, screenshots, tables and notes now all follow v3. Headline v1 to v3 changes: o3 is still the top checker by hit rate, but its combined HR@5 fell from 64.9% to 48.2% (PDF) and from 71.0% to 50.6% (LaTeX) after v3 switched the Gemini judge to Gemini 2.5 Pro `preview-06-05`; its estimated cost fell from $0.321 to $0.064 per paper (PDF) and from $0.383 to $0.077 (LaTeX) because v3 uses June-2025 standard pricing instead of early-May-2025 pricing; the abstract sentence "o3 performed the best, while o4-mini was the most cost-effective one" (v1) became "o3 exhibited the best problem identification performance among all models at a modest cost" (v3, p. 1).
- PDF check 2026-11-24: HR@5 PDF 64.9% -> 48.2% and LaTeX 71.0% -> 50.6% (v3 Table 2, p. 5; title and aliases renamed accordingly)
- PDF check 2026-11-24: cost per paper PDF $0.321 -> $0.064, LaTeX $0.383 -> $0.077 (v3 Table 2, p. 5)
- PDF check 2026-11-24: single-judge HR@5 Gemini-judge PDF 72.7% -> 80.4%, o3-judge PDF 75.5% -> 50.2%, Gemini-judge LaTeX 75.5% -> 79.2%, o3-judge LaTeX 80.4% -> 51.4% (v3 Table 3, p. 6)
- PDF check 2026-11-24: reasoning summary "detailed" -> "auto" (v3 Appendix B, p. 11); cost basis early May 2025 -> June 2025 pricing (v3 p. 4)
- PDF check 2026-11-24: Description quote "o3 performed the best, while o4-mini was the most cost-effective one" (v1 p. 1) is not in v3; replaced with v3 abstract sentence (p. 1). The "We set model temperature to 0 and fixed the decoding seed..." sentence (v1 p. 3) is not in v3 Section 2.4 (parameters moved to Appendix B, p. 11); the How quote was replaced with the v3 Section 2.4 text. Quote citations p. 3 -> p. 3 (judging), p. 4 (setup); the p. 2 quote stays p. 2.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting]].

*Figures reproduced from Zhang & Abernethy, arXiv v3 (1 Apr 2026), Tables 2 and 3, pp. 5–6. Single-judge rows are from Table 3; the rest from Table 2. v3 Table 2 also reports AP@5 = 29.5% for o3 (PDF only; not tabulated here).*
| Condition | HR@5 | Avg. # problems (Q1, Q3) | Input tok | Think tok | Output tok | $/paper |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **o3 (medium): PDF** | **48.2%** | 4.8 (5, 5) | 16,594 | 3,152 | 729 | $0.064 |
| **o3 (medium): LaTeX** | **50.6%** | 4.8 (5, 5) | 21,990 | 3,156 | 927 | $0.077 |
| Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 80.4% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / PDF) | 50.2% | — | — | — | — | — |
| Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 79.2% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / LaTeX) | 51.4% | — | — | — | — | — |

Grounding table (Table 3, p. 6): hit rate and average precision by individual judge for each checker.

![[zhangReviewingScientificPapers2025a-v3-table3-p6.png]]

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Only closed-source reasoning LLMs were tested as checkers|CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives]]

- [[CVT - Error detection dataset was mostly math and physics and may not generalize|CVT - The error detection dataset was rich in math and physics papers and may not generalize to other scientific domains]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

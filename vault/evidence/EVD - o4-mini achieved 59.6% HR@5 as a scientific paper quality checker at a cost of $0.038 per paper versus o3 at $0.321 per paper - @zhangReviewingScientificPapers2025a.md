---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/54pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b89-7314-8cf3-17160868cb52
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
---

## Source

[[@zhangReviewingScientificPapers2025a]]

## Description

> "o4-mini seems to be the most cost-effective choice for this task." (Zhang & Abernethy, 2025, p. 3)
> Table 2 shows o4-mini (medium): HR@5=59.6% (PDF) at $0.038/paper, vs. o3 HR@5=64.9% at $0.321/paper (p. 4).
>
> ![[zhangReviewingScientificPapers2025a-results-p4-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional cost–performance benchmark of OpenAI o-series reasoning LLMs as paper quality checkers, embedded in the same WITHDRARXIV-CHECK evaluation framework as the o3 EVD.
>
> **Method type:** zero-shot LLM evaluation under a fixed prompt; no fine-tuning.
>
> **Tools:** OpenAI o4-mini (`2025-04-16`, reasoning effort = medium) vs. OpenAI o3 (`2025-04-16`, reasoning effort = medium), accessed via OpenAI API in Python; LLM-as-judge pipeline with Gemini 2.5 Pro (`preview-05-06`) and o3.
>
> **Dependent variables:** Hit Rate at k=5 (HR@5), average input/think/output token usage, and **estimated USD cost per paper** computed from token usage at OpenAI API pricing in early May 2025.
>
> **Independent variables:** checker model (o4-mini vs. o3) × paper-ingestion approach (PDF attachment vs. LaTeX script in prompt).
>
> "Average costs of reviewing a paper under each pipeline-LLM combination were estimated based on API pricing at the time of our experiments in early May 2025… Considering the high cost of o3, o4-mini seems to be the most cost-effective choice for this task." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-6.png]]

### How?

> **Procedure:** identical to the o3 EVD's pipeline, with o4-mini swapped in as the checker. (1) Each of the 245 test papers prompted once ($n_c=1$) with the simplistic Appendix-A instruction, $k=5$ max problems, JSON-schema output (`Problem` / `Location` / `Explanation`); reasoning effort = medium, reasoning summary = detailed, no tools, no web; temperature/seed not supported on o4-mini. (2) Each problem submission independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3 ($m=2$, both must affirm for a hit). (3) Average input, think, and output token usage recorded per checker × ingestion combination. (4) Per-paper cost = (input tokens × input price) + (think tokens × think price) + (output tokens × output price), summed at early-May-2025 OpenAI API rates. (5) Cost ratio computed against o3 under the same ingestion approach.
>
> "In our experiments, both approaches utilized the same simplistic, general task instruction (Appendix A). In short, LLMs were instructed to produce a list of up to $k$ problems or errors that are the most critical in a given paper. The prompt was not customized for our dataset that is rich in math and physics papers. Each LLM quality checker was tested $n_c$ ($c$ for checker) times with each paper in consideration of potential variations in outputs." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-7.png]]

### Who?

> **Models / participants:** no human subjects. The compared models are **OpenAI o4-mini (medium, `2025-04-16`)** and **OpenAI o3 (medium, `2025-04-16`)**, evaluated as scientific-paper quality checkers; LLM judges are Gemini 2.5 Pro and o3.
>
> **Sample-size flow (papers):** WITHDRARXIV critical-errors candidates n=6,018 → Gemini 2.5 Flash filter → 2,190 → manual exclusions → WITHDRARXIV-CHECK n=1,225 → 80/20 split → **test n=245** (same set used for every checker). Test composition: Math 52% / Physics 29% / CS 15% / Other 4%; median 14 pages; LaTeX source available for 88%.
>
> "We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments. The remaining 80% (980 cases) of the dataset was set aside for training and validation, although these steps were not considered in this work whose main objective was to establish baseline approaches and evaluation methods." (Zhang & Abernethy, 2025, p. 2)
> ![[zhangReviewingScientificPapers2025a-evd-p2-2.png]]

## Other Notes

- Cost ratio: o3 PDF ($0.321) is **8.4×** more expensive than o4-mini PDF ($0.038); o3 LaTeX ($0.383) is **8.9×** more expensive than o4-mini LaTeX ($0.043). Performance gap is only 5.3 pp HR@5 (PDF) / 9.4 pp (LaTeX) → o4-mini wins on cost-per-hit by a wide margin under this prompting strategy.
- Both o-series models gain HR@5 when switched from PDF to LaTeX (o3: 64.9 → 71.0; o4-mini: 59.6 → 61.6), unlike Gemini models which degraded slightly under LaTeX, suggesting OpenAI models received specialized LaTeX training.
- o4-mini's input-token usage was slightly higher than o3's (17,760 vs. 16,594 under PDF) — authors flag this as unexplained.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting summary]].

| Model × ingestion | HR@5 | Input tok | Think tok | Output tok | $/paper | $ vs. o4-mini |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **o4-mini (medium) — PDF** | **59.6%** | 17,760 | 3,582 | 701 | **$0.038** | 1.0× |
| o3 (medium) — PDF | 64.9% | 16,594 | 3,152 | 729 | $0.321 | **8.4×** |
| **o4-mini (medium) — LaTeX** | 61.6% | 22,287 | 3,421 | 685 | **$0.043** | 1.0× |
| o3 (medium) — LaTeX | 71.0% | 21,990 | 3,156 | 927 | $0.383 | **8.9×** |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant]]

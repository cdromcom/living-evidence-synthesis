---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper"
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
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6b89-7314-8cf3-17160868cb52
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
title: "o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper"
---

## Source

[[sysrev/dgraph/source/@zhangReviewingScientificPapers2025a]]

## Description

> "o3 achieved the highest estimated hit rate among all models at a modest cost." (Zhang & Abernethy, 2026, p. 4)
>
> ![[zhangReviewingScientificPapers2025a-v3-o4-desc-p4.png]]
>
> Table 2 shows o4-mini (medium): HR@5=38.0% (PDF) at $0.038/paper, vs. o3 HR@5=48.2% at $0.064/paper (p. 5).
>
> Grounding table (Table 2, p. 5): problems found, HR@5, AP@5, token usage and cost per paper for the five checkers under PDF and LaTeX input.
>
> ![[zhangReviewingScientificPapers2025a-v3-table2-p5.png]]

## Methods Context

### What?

> **Study design:** cross-sectional cost–performance benchmark of OpenAI o-series reasoning LLMs as paper quality checkers, embedded in the same WITHDRARXIV-CHECK evaluation framework as the o3 EVD.
>
> **Method type:** zero-shot LLM evaluation under a fixed prompt; no fine-tuning.
>
> **Tools:** OpenAI o4-mini (`2025-04-16`, reasoning effort = medium) vs. OpenAI o3 (`2025-04-16`, reasoning effort = medium), accessed via OpenAI API in Python; LLM-as-judge pipeline with Gemini 2.5 Pro (`preview-06-05` in v3; v1 used `preview-05-06`) and o3 (p. 4).
>
> **Dependent variables:** Hit Rate at k=5 (HR@5), average input/think/output token usage, and **estimated USD cost per paper** computed from token usage at standard OpenAI API pricing in June 2025 (p. 4; v1 used early-May-2025 pricing). v3 also adds AP@5 (average precision of judge-confirmed true problems, PDF approach only).
>
> **Independent variables:** checker model (o4-mini vs. o3) × paper-ingestion approach (PDF attachment vs. LaTeX script in prompt).
>
> "Average costs of reviewing a paper under each pipeline-LLM combination were estimated based on the standard API pricing of the LLM vendors in June 2025." (Zhang & Abernethy, 2026, p. 4)
> ![[zhangReviewingScientificPapers2025a-v3-o4-what-p4.png]]

### How?

> **Procedure:** identical to the o3 EVD's pipeline, with o4-mini swapped in as the checker. (1) Each of the 245 test papers prompted once ($n_c=1$) with the simplistic Appendix-A instruction, $k=5$ max problems, JSON-schema output (`Problem` / `Location` / `Explanation`); reasoning effort = medium, reasoning summary = auto (Appendix B, p. 11; v1 listed detailed), no tools, no web; temperature/seed not supported on o4-mini. (2) Each problem submission independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3 ($m=2$, both must affirm for a hit). (3) Average input, think, and output token usage recorded per checker × ingestion combination. (4) Per-paper cost = (input tokens × input price) + (think tokens × think price) + (output tokens × output price), summed at standard June-2025 OpenAI API rates (p. 4). (5) Cost ratio computed against o3 under the same ingestion approach.
>
> "In our experiments, both approaches utilized the same simplistic, general task instruction (Appendix A). In short, LLMs were instructed to produce a list of up to k problems or errors that are the most critical in a given paper. The prompt was not customized for our dataset that is rich in math and physics papers. Each LLM checker was tested nc (c for checker) times with each paper in consideration of potential variations in outputs." (Zhang & Abernethy, 2026, p. 3)
> ![[zhangReviewingScientificPapers2025a-v3-o4-how-p3.png]]

### Who?

> **Models / participants:** no human subjects. The compared models are **OpenAI o4-mini (medium, `2025-04-16`)** and **OpenAI o3 (medium, `2025-04-16`)**, evaluated as scientific-paper quality checkers; LLM judges are Gemini 2.5 Pro (`preview-06-05` in v3) and o3.
>
> **Sample-size flow (papers):** WITHDRARXIV critical-errors candidates n=6,018 → Gemini 2.5 Flash filter → 2,190 → manual exclusions → WITHDRARXIV-CHECK n=1,225 → 80/20 split → **test n=245** (same set used for every checker). Test composition: Math 52% / Physics 29% / CS 15% / Other 4%; median 14 pages; LaTeX source available for 88%.
>
> "We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments. The remaining 80% (980 cases) of the dataset was set aside for training and validation, although these latter two steps were not considered in this work whose main objective was to establish baseline approaches and evaluation methods." (Zhang & Abernethy, 2026, p. 2)
> ![[zhangReviewingScientificPapers2025a-v3-sample-split-p2.png]]
>
> Grounding table (Table 1, p. 3): train and test set characteristics (time span, main subject, page count, LaTeX availability).
>
> ![[zhangReviewingScientificPapers2025a-v3-table1-p3.png]]

## Other Notes

- Cost ratio (v3 Table 2, p. 5): o3 PDF ($0.064) is **1.7×** as expensive as o4-mini PDF ($0.038); o3 LaTeX ($0.077) is **1.8×** as expensive as o4-mini LaTeX ($0.043). The HR@5 gap is 10.2 pp (PDF, 48.2 vs. 38.0) and 11.8 pp (LaTeX, 50.6 vs. 38.8). Cost per hit (cost divided by HR@5, our calculation) under PDF is about $0.10 for o4-mini vs. $0.13 for o3, so o4-mini's cost edge is now small, and Gemini 2.5 Flash roughly matches o4-mini's PDF hit rate (38.4% vs. 38.0%) at a lower cost ($0.033). v3 no longer calls o4-mini the most cost-effective choice.
- Both o-series models hold roughly steady or gain slightly when switched from PDF to LaTeX (o3: 48.2 → 50.6; o4-mini: 38.0 → 38.8; v3 Table 2, p. 5), unlike Gemini models whose hit rates decreased under LaTeX (Gemini 2.5 Pro 39.2 → 36.3; Flash 38.4 → 34.7). v3 reads this as "resistance to format change or a higher familiarity with LaTeX" (p. 4), replacing v1's suggestion of specialized LaTeX training.
- o4-mini's input-token usage was slightly higher than o3's (17,760 vs. 16,594 under PDF); the authors say it "remains unclear" why o4-mini "sometimes used slightly more input tokens than o3" (p. 5; unchanged from v1).
- v3 adds AP@5 (PDF only): o4-mini 26.7% vs. o3 29.5% (Table 2, p. 5).
- Version update 2026-11-24: this page moved from arXiv v1 (28 May 2025) to arXiv v3 (arXiv:2505.23824v3 [cs.CL], 1 Apr 2026; NeurIPS 2025 AI for Science workshop). Title, quotes, screenshots, tables and notes now all follow v3. Headline v1 to v3 changes: o4-mini's combined HR@5 fell from 59.6% to 38.0% (PDF) and from 61.6% to 38.8% (LaTeX) after v3 switched the Gemini judge to Gemini 2.5 Pro `preview-06-05`; o4-mini's own cost is unchanged ($0.038 / $0.043), but o3's estimated cost fell from $0.321 to $0.064 (PDF) and $0.383 to $0.077 (LaTeX) under June-2025 standard pricing, so the o3 / o4-mini cost ratio shrank from 8.4× to 1.7× (PDF) and 8.9× to 1.8× (LaTeX); v3 drops the v1 sentences "o4-mini seems to be the most cost-effective choice for this task" and "o4-mini was the most cost-effective one in our evaluation".
- PDF check 2026-11-24: o4-mini HR@5 PDF 59.6% -> 38.0%, LaTeX 61.6% -> 38.8% (v3 Table 2, p. 5; title and aliases renamed accordingly)
- PDF check 2026-11-24: o3 HR@5 PDF 64.9% -> 48.2%, LaTeX 71.0% -> 50.6%; o3 cost PDF $0.321 -> $0.064, LaTeX $0.383 -> $0.077; cost ratio 8.4× -> 1.7× (PDF), 8.9× -> 1.8× (LaTeX) (v3 Table 2, p. 5)
- PDF check 2026-11-24: reasoning summary "detailed" -> "auto" (v3 Appendix B, p. 11); pricing early May 2025 -> June 2025 (v3 p. 4)
- PDF check 2026-11-24: Description quote "o4-mini seems to be the most cost-effective choice for this task." (v1 p. 3) and the "Considering the high cost of o3..." sentence are not in v3; replaced with v3 Section 3 sentences on p. 4 (the pricing sentence and "o3 achieved the highest estimated hit rate among all models at a modest cost"). How quote now cited p. 3 (unchanged page; "these steps" -> "these latter two steps" and "LLM quality checker" -> "LLM checker" in v3).

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[sysrev/dgraph/source/@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting]].

*Figures reproduced from Zhang & Abernethy, arXiv v3 (1 Apr 2026), Table 2, p. 5; the $ ratio column is our calculation.*
| Model × ingestion | HR@5 | Input tok | Think tok | Output tok | $/paper | $ vs. o4-mini |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **o4-mini (medium): PDF** | **38.0%** | 17,760 | 3,582 | 701 | **$0.038** | 1.0× |
| o3 (medium): PDF | 48.2% | 16,594 | 3,152 | 729 | $0.064 | **1.7×** |
| **o4-mini (medium): LaTeX** | 38.8% | 22,287 | 3,421 | 685 | **$0.043** | 1.0× |
| o3 (medium): LaTeX | 50.6% | 21,990 | 3,156 | 927 | $0.077 | **1.8×** |

## Caveats

> [!info] Caveats applying to this evidence

- [[sysrev/dgraph/caveats/CVT - Only closed-source reasoning LLMs were tested as checkers|CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[sysrev/dgraph/claims/CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[sysrev/dgraph/evd-patterns/EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant|EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant]]

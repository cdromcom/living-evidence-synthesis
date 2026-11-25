---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 11.0% hit rate as a PDF-based scientific quality checker"
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
nodeID: 019ddb4e-6b5c-74d1-b091-81876db06c6d
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
title: "Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 11.0% hit rate as a PDF-based scientific quality checker"
---

## Source

[[sysrev/dgraph/source/@zhangReviewingScientificPapers2025a]]

## Description

> "When papers are provided as PDFs, Claude 3.7 Sonnet found no problem in 64.9% of test papers, leading to a low hit rate compared to other reasoning models." (Zhang & Abernethy, 2026, p. 4)
>
> ![[zhangReviewingScientificPapers2025a-v3-claude-desc-p4.png]]
>
> Table 2 shows Claude 3.7 Sonnet: Avg. problems identified=1.6 (PDF), HR@5=11.0% (PDF), 24.1% (LaTeX); cost=$0.159/paper (PDF). (p. 5)
>
> Grounding table (Table 2, p. 5): problems found, HR@5, AP@5, token usage and cost per paper for the five checkers under PDF and LaTeX input.
>
> ![[zhangReviewingScientificPapers2025a-v3-table2-p5.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of Anthropic's Claude 3.7 Sonnet as a scientific-paper quality checker, embedded in the same WITHDRARXIV-CHECK pipeline as the o3 / o4-mini EVDs.
>
> **Method type:** zero-shot LLM evaluation under a fixed simplistic prompt.
>
> **Tools:** Claude 3.7 Sonnet (`20250219`) accessed via Anthropic API in Python with extended thinking enabled (`thinking type: "enabled"`, `thinking budget: 14,000`, `max tokens: 16,000`, `temperature: 1`, required when thinking is enabled; seed not supported); LLM-as-judge with Gemini 2.5 Pro (`preview-06-05` in v3, chosen "for its better performance on related benchmarks than preview-05-06") and o3 (`2025-04-16`) (p. 4).
>
> **Dependent variables:** HR@5; AP@5 (average precision of the submissions that both judges rate as true problems against the PDF, PDF approach only; new in v3, p. 4); **average / Q1 / Q3 number of problems submitted per paper** (key for this EVD because Q1=0 under PDF means ≥ 25% of submissions were empty); average input/think/output token usage; estimated USD cost per paper.
>
> **Independent variables:** paper-ingestion approach (PDF attachment vs. LaTeX script in prompt).
>
> "When papers are provided as PDFs, Claude 3.7 Sonnet found no problem in 64.9% of test papers, leading to a low hit rate compared to other reasoning models. Interestingly, both its number of identified problems and hit rate increased after switching to LaTeX, suggesting potential obstacles in Claude's PDF ingestion pipeline or scientific understanding via PDF." (Zhang & Abernethy, 2026, p. 4)
> ![[zhangReviewingScientificPapers2025a-v3-claude-what-p4.png]]

### How?

> **Procedure:** identical to companion EVDs but with Claude 3.7 Sonnet as the checker model. Each of the 245 test papers was ingested either as a PDF attachment or as a LaTeX script in the prompt; Claude was prompted once ($n_c=1$) with the Appendix-A instruction to return up to $k=5$ critical problems as a JSON list of `{Problem, Location, Explanation}`. Each problem submission was independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3, both must affirm for a hit ($m=2$). The authors initially planned $m=3$ with Claude 3.7 Sonnet as the third judge but **excluded Claude as a judge** because its overly low PDF-approach hit rate indicated it "might not qualify" as a judge (p. 4; v3 no longer points to Table 3 here). In v3 the same two judges also rate each submission as a true problem or a false alarm against the PDF (both must affirm), which yields AP@5 under the PDF approach only (p. 4). Token-usage and cost recorded per ingestion approach.
>
> "We initially planned for m = 3 with Claude 3.7 Sonnet as the last judge, but its overly low hit rate under the PDF-based approach indicates that it might not qualify for serving as a judge in this task. Under m = 2, both judges must vote affirmatively to confirm a hit or a true positive." (Zhang & Abernethy, 2026, p. 4)
> ![[zhangReviewingScientificPapers2025a-v3-claude-how-p4.png]]

### Who?

> **Models / participants:** no human subjects. The model under test is **Claude 3.7 Sonnet (`20250219`)** with extended thinking enabled. Comparison checkers in Table 2 are Gemini 2.5 Pro / Flash and o3 / o4-mini (medium). LLM judges are Gemini 2.5 Pro (`preview-06-05` in v3) and o3 (Claude was disqualified from the judge pool).
>
> **Sample-size flow (papers):** WITHDRARXIV critical-errors candidates n=6,018 → Gemini 2.5 Flash filter → 2,190 → manual exclusions → WITHDRARXIV-CHECK n=1,225 → 80/20 split → **test n=245**. Test composition: Math 52% / Physics 29% / CS 15% / Other 4%; median 14 pages (range 2–136); LaTeX source available for 216/245 (88%). For the 12% without LaTeX, the LaTeX-row results inherit the PDF-row prediction.
>
> "We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments. The remaining 80% (980 cases) of the dataset was set aside for training and validation, although these latter two steps were not considered in this work whose main objective was to establish baseline approaches and evaluation methods." (Zhang & Abernethy, 2026, p. 2)
> ![[zhangReviewingScientificPapers2025a-v3-sample-split-p2.png]]
>
> "For the small proportion of papers without available LaTeX scripts (Table 1), we resorted to utilizing the problems identified by the same model through the PDF-based approach." (Zhang & Abernethy, 2026, p. 3)
> ![[zhangReviewingScientificPapers2025a-v3-claude-who-p3.png]]
>
> Grounding table (Table 1, p. 3): train and test set characteristics (time span, main subject, page count, LaTeX availability).
>
> ![[zhangReviewingScientificPapers2025a-v3-table1-p3.png]]

## Other Notes

- **PDF-pipeline pathology:** Claude's input token usage for PDF was 43,357, 9.3× higher than Gemini's 4,678 and 2.6× higher than o3's 16,594 (Table 2, p. 5). After switching to LaTeX, input tokens dropped to 28,284 (still highest among the 5 checkers but in-family). The authors say the input-token differences between vendors "reflect distinct PDF ingestion pipelines" (Gemini reads PDFs purely with vision; OpenAI and Anthropic supply extracted text plus an image of each page) and that it "remains unclear why Claude has an exceptionally high input token usage for PDF files" (p. 5).
- **Hit rate more than doubled under LaTeX (11.0% → 24.1%, v3 Table 2, p. 5) and average problems submitted rose from 1.6 to 3.4**, with Q1 rising from 0 to 1: direct evidence that the empty-submission problem is PDF-specific.
- v3 adds AP@5 (PDF only): Claude scored 36.4%, the highest of the five checkers (Gemini 2.5 Pro 35.2%, o3 29.5%, o4-mini 26.7%, Gemini 2.5 Flash 23.3%), but only 149 of its problem submissions were confirmed as true problems by both judges, against 350 for o3 and 293 for Gemini 2.5 Pro (p. 4). Because cases where a checker found no problem are skipped when computing precision, a high AP@5 here is consistent with (our reading, not stated by the authors) Claude reporting few problems.
- Single-judge HR@5 (v3 Table 3, p. 6) for Claude as checker: PDF (Gemini-judge 24.1%, o3-judge 12.2%); LaTeX (Gemini-judge 48.6%, o3-judge 26.5%).
- Version update 2026-11-24: this page moved from arXiv v1 (28 May 2025) to arXiv v3 (arXiv:2505.23824v3 [cs.CL], 1 Apr 2026; NeurIPS 2025 AI for Science workshop). Title, quotes, screenshots, tables and notes now all follow v3. Headline v1 to v3 changes: Claude's combined HR@5 fell from 16.3% to 11.0% (PDF) and from 33.1% to 24.1% (LaTeX), because v3 uses Gemini 2.5 Pro `preview-06-05` as judge (v1 `preview-05-06`); the 64.9% no-problem share, problem counts, token usage and costs are unchanged; v3 adds AP@5 (PDF only); v3 rewords the PDF explanation from "Anthropic's PDF ingestion pipeline" to "Claude's PDF ingestion pipeline or scientific understanding via PDF" (p. 4) and the judge exclusion from "(Table 3) ... unqualified" to "might not qualify" (p. 4).
- PDF check 2026-11-24: HR@5 PDF 16.3% -> 11.0% (v3 Table 2, p. 5; title and aliases renamed accordingly)
- PDF check 2026-11-24: HR@5 LaTeX 33.1% -> 24.1% (v3 Table 2, p. 5)
- PDF check 2026-11-24: Gemini-judge HR@5 PDF 21.6% -> 24.1%, o3-judge PDF 19.2% -> 12.2%, Gemini-judge LaTeX 44.5% -> 48.6%, o3-judge LaTeX 40.8% -> 26.5% (v3 Table 3, p. 6)
- PDF check 2026-11-24: quote citations: the three quotes cited p. 3 in v1 are now cited p. 4 (v3 Sections 3 and 2.4), the p. 2 quote is now cited p. 2 and p. 3 (v3 Sections 2.1 and 2.2); the v3 PDF prints page numbers equal to its PDF position; quotes replaced with the v3 wording shown above (v1 wording "leading to a low hit rate of 16.3%", "Anthropic's PDF ingestion pipeline" and "(Table 3) ... unqualified" is not in v3)

> [!info] TRIPOD-LLM item 17 (Performance): EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[sysrev/dgraph/source/@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting]].

*Figures reproduced from Zhang & Abernethy, arXiv v3 (1 Apr 2026), Tables 2 and 3, pp. 5–6. Single-judge rows are from Table 3; the rest from Table 2. v3 Table 2 also reports AP@5 = 36.4% for Claude (PDF only; not tabulated here).*
| Condition | HR@5 | Avg. # problems (Q1, Q3) | Input tok | Think tok | Output tok | $/paper |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude 3.7 Sonnet: PDF** | **11.0%** | **1.6 (0, 4)** | **43,357** | 1,630 | 311 | $0.159 |
| Claude 3.7 Sonnet: LaTeX | 24.1% | 3.4 (1, 5) | 28,284 | 2,701 | 515 | $0.133 |
| Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 24.1% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / PDF) | 12.2% | — | — | — | — | — |
| Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 48.6% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / LaTeX) | 26.5% | — | — | — | — | — |

Grounding table (Table 3, p. 6): hit rate and average precision by individual judge for each checker.

![[zhangReviewingScientificPapers2025a-v3-table3-p6.png]]

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[sysrev/dgraph/claims/CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[sysrev/dgraph/evd-patterns/EP - LLM confidence calibration on scientific-error tasks is poor with extreme distributions]]
- [[sysrev/dgraph/evd-patterns/EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

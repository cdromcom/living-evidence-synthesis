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
  - forensic/monotonicity-check/consistent
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b5c-74d1-b091-81876db06c6d
appraisal_overall: L0-M4-H1
tripod_llm_pct: 54pct
---

## Source

[[@zhangReviewingScientificPapers2025a]]

## Description

> "When papers are provided as PDFs, Claude 3.7 Sonnet found no problem in 64.9% of test papers, leading to a low hit rate of 16.3%." (Zhang & Abernethy, 2025, p. 3)
> Table 2 shows Claude 3.7 Sonnet: Avg. problems identified=1.6 (PDF), HR@5=16.3% (PDF), 33.1% (LaTeX); cost=$0.159/paper (PDF). (p. 4)
>
> ![[zhangReviewingScientificPapers2025a-results-p4-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of Anthropic's Claude 3.7 Sonnet as a scientific-paper quality checker, embedded in the same WITHDRARXIV-CHECK pipeline as the o3 / o4-mini EVDs. **Method type:** zero-shot LLM evaluation under a fixed simplistic prompt. **Tools:** Claude 3.7 Sonnet (`20250219`) accessed via Anthropic API in Python with extended thinking enabled (`thinking type: "enabled"`, `thinking budget: 14,000`, `max tokens: 16,000`, `temperature: 1` — required when thinking is enabled, seed not supported); LLM-as-judge with Gemini 2.5 Pro (`preview-05-06`) and o3 (`2025-04-16`). **Dependent variables:** HR@5; **average / Q1 / Q3 number of problems submitted per paper** (key for this EVD because Q1=0 under PDF means ≥ 25% of submissions were empty); average input/think/output token usage; estimated USD cost per paper. **Independent variables:** paper-ingestion approach (PDF attachment vs. LaTeX script in prompt).
>
> "When papers are provided as PDFs, Claude 3.7 Sonnet found no problem in 64.9% of test papers, leading to a low hit rate of 16.3%. Interestingly, both its number of identified problems and hit rate increased after switching to LaTeX, suggesting potential obstacles in Anthropic's PDF ingestion pipeline." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-1.png]]

### How?

> **Procedure:** identical to companion EVDs but with Claude 3.7 Sonnet as the checker model. Each of the 245 test papers was ingested either as a PDF attachment or as a LaTeX script in the prompt; Claude was prompted once ($n_c=1$) with the Appendix-A instruction to return up to $k=5$ critical problems as a JSON list of `{Problem, Location, Explanation}`. Each problem submission was independently judged once ($n_j=1$) by Gemini 2.5 Pro and by o3, both must affirm for a hit ($m=2$). The authors initially planned $m=3$ with Claude 3.7 Sonnet as the third judge but **excluded Claude as a judge** because its low PDF-approach hit rates (Table 3: 21.6% / 19.2%) indicated it was unqualified to judge in this task. Token-usage and cost recorded per ingestion approach.
>
> "We initially planned for $m=3$ with Claude 3.7 Sonnet as the last judge, but its overly low hit rates under the PDF-based approach (Table 3) indicate that it is unqualified to serve as a judge in this task. Under $m=2$, both judges must vote affirmatively to confirm a hit." (Zhang & Abernethy, 2025, p. 3)
> ![[zhangReviewingScientificPapers2025a-evd-p3-2.png]]

### Who?

> **Models / participants:** no human subjects. The model under test is **Claude 3.7 Sonnet (`20250219`)** with extended thinking enabled. Comparison checkers in Table 2 are Gemini 2.5 Pro / Flash and o3 / o4-mini (medium). LLM judges are Gemini 2.5 Pro and o3 (Claude was disqualified from the judge pool).
>
> **Sample-size flow (papers):** WITHDRARXIV critical-errors candidates n=6,018 → Gemini 2.5 Flash filter → 2,190 → manual exclusions → WITHDRARXIV-CHECK n=1,225 → 80/20 split → **test n=245**. Test composition: Math 52% / Physics 29% / CS 15% / Other 4%; median 14 pages (range 2–136); LaTeX source available for 216/245 (88%) — for the 12% without LaTeX, the LaTeX-row results inherit the PDF-row prediction.
>
> "Each LLM quality checker was tested $n_c$ ($c$ for checker) times with each paper in consideration of potential variations in outputs… For the small proportion of papers without available LaTeX scripts (Table 1), we resorted to the problems identified by the same model through the PDF-based approach." (Zhang & Abernethy, 2025, p. 2)
> ![[zhangReviewingScientificPapers2025a-evd-p3-3.png]]

## Other Notes

- **PDF-pipeline pathology:** Claude's input token usage for PDF was 43,357 — 9.3× higher than Gemini's 4,678 and 2.6× higher than o3's 16,594. After switching to LaTeX, input tokens dropped to 28,284 (still highest among the 5 checkers but in-family). Authors attribute this to Anthropic's per-page extracted-text + page-image PDF representation.
- **Hit rate doubled under LaTeX (16.3% → 33.1%) and average problems submitted rose from 1.6 to 3.4**, with Q1 rising from 0 to 1 — direct evidence that the empty-submission problem is PDF-specific.
- Single-judge HR@5 (Table 3) for Claude as checker: PDF — Gemini-judge 21.6%, o3-judge 19.2%; LaTeX — Gemini-judge 44.5%, o3-judge 40.8%.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangReviewingScientificPapers2025a#TRIPOD-LLM reporting summary]].

| Condition | HR@5 | Avg. # problems (Q1, Q3) | Input tok | Think tok | Output tok | $/paper |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude 3.7 Sonnet — PDF** | **16.3%** | **1.6 (0, 4)** | **43,357** | 1,630 | 311 | $0.159 |
| Claude 3.7 Sonnet — LaTeX | 33.1% | 3.4 (1, 5) | 28,284 | 2,701 | 515 | $0.133 |
| Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 21.6% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / PDF) | 19.2% | — | — | — | — | — |
| Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 44.5% | — | — | — | — | — |
| Single-judge HR@5 (o3 judge / LaTeX) | 40.8% | — | — | — | — | — |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM confidence calibration on scientific-error tasks is poor with extreme distributions]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

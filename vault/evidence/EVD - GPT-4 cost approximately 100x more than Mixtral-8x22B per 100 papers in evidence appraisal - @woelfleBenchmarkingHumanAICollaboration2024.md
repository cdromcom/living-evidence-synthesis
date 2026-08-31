---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/low-risk
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L2-M2-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/67pct
  - 5c/clarity
  - 5c/credibility
created: 2026-04-27
updated: 2026-04-29
nodeID: 019ddb4e-6b6d-739b-84bf-e74d3b7c68ac
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "Mixtral-8x22B was the most affordable model with a median of $1.20 per 100 papers and GPT-4 the most expensive one with a median of $115.00." (Woelfle et al., 2024, p. 8)
>
> Per-publication median costs from Table 1 (p. 3): Claude-3-Opus $0.40, Claude-2 $0.19, GPT-4 $1.15, GPT-3.5 $0.06, Mixtral-8x22B $0.012.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-fig1-p3-03.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of LLM efficiency (cost & wall-clock latency) on the same evidence-appraisal workload used to compute accuracy.
>
> **Method type:** observational logging of API-billed cost and response time per publication.
>
> **Tools:** 5 LLM APIs (Anthropic for Claude-3-Opus & Claude-2; OpenAI for GPT-4 & GPT-3.5; OpenRouter for Mixtral-8x22B).
>
> **Dependent variables:** median cost per publication (USD, IQR) and median response time per publication.
>
> **Independent variables:** LLM (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B); appraisal tool (PRISMA / AMSTAR / PRECIS-2 — costs aggregated across all three).
>
> "Mixtral-8x22B was the most affordable model with a median of $1.20 per 100 papers and GPT-4 the most expensive one with a median of $115.00. Model response speeds were ranging from ∼10 seconds (GPT-3.5) to 2 minutes (GPT-4) per paper." (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-1.png]]

### How?

> **Procedure:** Five LLMs were queried via APIs (Anthropic, OpenAI, OpenRouter for Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning, and (3) assign a per-item rating (no/yes/NA for PRISMA/AMSTAR; ordinal 1–5 or NA for PRECIS-2). Claude-3-Opus received page-level PNG images (multimodal); the other four models received plain text. Each prompt was run twice (GPT-4 only on 25% due to cost). API-billed cost (USD) and wall-clock response time per publication were logged at query time (August 2023–April 2024 depending on model — see Table 1). Median + IQR computed across publications per LLM. Quote handling and post-processing in Python 3.11.4 (parasail, rapidfuzz); statistical analysis and visualisation in R 4.3 with 1000-resample publication-level bootstrap CIs for accuracy outcomes.
>
> "API querying, extraction of ratings, fixing minor formatting issues, and quantification of quote accuracy were performed in Python 3.11.4 using the parasail and rapidfuzz libraries. Statistical analyses and visualizations were performed in R 4.3." (Woelfle et al., 2024, p. 5)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p5-1.png]]

### Who?

> **Models:** 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B-instruct-v0.1) — 9 total assessment runs per item across the ensemble.
>
> **Datasets / sample-size flow:** PRISMA & AMSTAR — 112 systematic reviews & meta-analyses in pediatric surgery (Cullis et al., shared); PRECIS-2 — 56 RCTs from the PragMeta database.
>
> **Processing failures:** Claude-3-Opus failed on 3/112 publications (content filtering / overly long); GPT-4 failed on 3/112 (context length); GPT-3.5 failed on 3/112 PRISMA/AMSTAR and 2/56 PRECIS-2; Mixtral failed on 1/112; Claude-2 processed all. Cost per publication was computed only on successfully processed publications.
>
> "All application programming interface (API) queries were performed with minimal randomness ('temperature' 0) to allow the highest possible intrarater reliability." (Woelfle et al., 2024, p. 5)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p5-2.png]]

## Other Notes

- GPT-4 cost reflects gpt-4-32k-0613, queried September 2023. Newer GPT-4 versions released after this study may have lower per-token costs.
- Rarely, API rate limits required a break until the end of the day to continue calling Claude-3-Opus, Claude-2, and GPT-4.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting summary]].

| Model (version) | Median cost / publication (IQR) | Cost per 100 publications (median) | Median response time / publication |
| --- | --- | --- | --- |
| Claude-3-Opus (claude-3-opus-20240229) | $0.40 (0.14–0.78) | $40 | 1–2 min |
| Claude-2 (claude-2.0) | $0.19 (0.09–0.81) | $19 | ~1 min |
| GPT-4 (gpt-4-32k-0613) | $1.15 (0.65–1.98) | **$115.00** | ~2 min |
| GPT-3.5 (gpt-3.5-turbo-16k-0613) | $0.06 (0.03–0.10) | $6 | ~10 s |
| **Mixtral-8x22B** (Mixtral-8x22b-instruct-v0.1) | **$0.012 (0.010–0.017)** | **$1.20** | 1–2 min |
| GPT-4 vs Mixtral-8x22B cost ratio | — | ≈ 96× | — |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM cost-effectiveness varies by orders of magnitude with smaller specialized models often Pareto-dominant]]

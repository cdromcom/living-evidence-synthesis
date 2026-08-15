---
NodeFormality: ReadyForInternal
aliases:
tags:
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
nodeID: 019ddb4e-6b7e-7568-87fd-f5411fb5606b
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "The median quote similarity with the original full text was 99%, with some quotes slightly shortened (eg, removing references or brackets) or rephrased" (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-4.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of LLM extractive-quoting fidelity on the same evidence-appraisal workload used to compute accuracy. **Method type:** automated string-similarity scoring of LLM-extracted quotes against the source publication's full text. **Tools:** parasail (SIMD pairwise sequence alignment) and rapidfuzz (Levenshtein-based string similarity) in Python 3.11.4. **Dependent variable:** median % similarity (0–100) between each LLM-extracted quote and the closest matching span in the source publication. **Independent variables:** LLM (5 levels); appraisal tool (PRISMA / AMSTAR / PRECIS-2); whether the quote came from the requested full text vs the prompt's briefing material.
>
> "All prompts required the LLMs to 'extract 1-3 relevant quotes from the full text' per item. For PRISMA (27 items), a median of 14 quotes (range 5-17) were provided per publication, 0.5 quotes/item. For AMSTAR (11 items), a median of 7 quotes (range 4-8) were provided per publication, 0.6 quotes/item. For PRECIS-2 (9 domains), a median of 10 quotes (range 9-10) were provided per publication, 1 quote/domain." (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-5.png]]

### How?

> **Procedure:** Five LLMs (Claude-3-Opus, Claude-2, GPT-4-32k-0613, GPT-3.5-turbo-16k-0613, Mixtral-8x22B-instruct-v0.1) were queried via APIs (Anthropic, OpenAI, OpenRouter) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning, and (3) assign a per-item rating. Claude-3-Opus received page-level PNG images (multimodal); the other four received plain text. **For this analysis (quote similarity):** every extracted quote string was matched against the source publication using parasail for pairwise alignment and rapidfuzz for Levenshtein-based string similarity; per-quote percentage similarity scored. Median across all extracted quotes (and per-LLM/per-tool subsets) reported in Supplementary Table 3. Authors flagged a sub-population of quotes that came from the prompt's briefing files (e.g., the PRECIS Toolkit page or Loudon 2015 reference) rather than the target full text — for those, similarity to the target is mechanically low.
>
> "API querying, extraction of ratings, fixing minor formatting issues, and quantification of quote accuracy were performed in Python 3.11.4 using the parasail and rapidfuzz libraries." (Woelfle et al., 2024, p. 5)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p5-4.png]]

### Who?

> **Models:** 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B-instruct-v0.1) producing quote outputs. **Datasets / sample-size flow:** PRISMA — 112 systematic reviews × ~14 quotes/publication ≈ ~1,500 quotes per LLM run (target 27 items × 0.5 quotes/item). AMSTAR — 112 reviews × ~7 quotes ≈ ~780 quotes per LLM run (11 items × 0.6 quotes/item). PRECIS-2 — 56 RCTs × ~10 quotes ≈ ~560 quotes per LLM run (9 domains × 1 quote). Multiplied by ~9 LLM runs across the ensemble (some failures: Claude-3-Opus 3/112; GPT-4 3/112; GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2; Mixtral 1/112).
>
> "Claude-3-Opus, Claude-2, and Mixtral-8x22B sometimes quoted from the provided briefings instead of the full text to be assessed, which was not part of the instructions, while GPT-4 and GPT-3.5 rarely did this." (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-6.png]]

## Other Notes

- A small minority of LLM responses (especially Claude-3-Opus, Claude-2, Mixtral-8x22B) quoted from the prompt briefing rather than the target full text, mechanically lowering similarity for those items.
- Most "near-100%" matches were exact substrings of the source; sub-100% matches were typically due to references/brackets being removed or minor rephrasing.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting summary]].

| Tool | Median quotes / publication (range) | Quotes per item | Median quote similarity to source full text |
| --- | --- | --- | --- |
| PRISMA (27 items × 112) | 14 (5–17) | 0.5 / item | **99%** |
| AMSTAR (11 items × 112) | 7 (4–8) | 0.6 / item | **99%** |
| PRECIS-2 (9 domains × 56) | 10 (9–10) | 1 / domain | **99%** |
| Off-target quoting | Claude-3-Opus, Claude-2, Mixtral occasionally; GPT-4 and GPT-3.5 rarely | — | (lower for off-target subset) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

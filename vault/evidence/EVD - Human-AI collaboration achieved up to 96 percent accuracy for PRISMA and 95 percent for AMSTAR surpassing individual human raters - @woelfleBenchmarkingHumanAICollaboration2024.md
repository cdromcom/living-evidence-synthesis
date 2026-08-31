---
NodeFormality: draft
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
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b73-751a-bbaf-1660b1f7b516
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "Human−AI collaboration resulted in the best accuracies from 89% to 96% for PRISMA (25/35% deferred), 91%−95% for AMSTAR (27/30% deferred), and 80%−86% for PRECIS-2 (76/71% deferred)." (Woelfle et al., 2024, p. 1 [Abstract])
>
> Grounding figure (Fig 2, p. 4): confusion matrices for the four conditions × three tools, showing human-AI collaboration's improved agreement and deferred fractions.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-fig2fig3-p4-04.png]]
>
> Grounding table (Table 3, p. 7): human-AI collaboration accuracies and deferring fractions.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-table3-p7-07.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of human–AI collaboration vs an individual second human rater on the same evidence-appraisal workload.
>
> **Method type:** human-rater-1 + single LLM ensemble — items where the human and the LLM agree are accepted; items where they disagree are deferred to a (hypothetical) second human rater.
>
> **Tools:** PRISMA (27 items × 112 reviews), AMSTAR (11 items × 112 reviews), PRECIS-2 (9 domains × 56 RCTs); 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4 / GPT-3.5 / Mixtral-8x22B) generate 10 possible human–AI pairs.
>
> **Dependent variables:** accuracy (% identical to human consensus) on the non-deferred subset; Cohen's kappa (weighted for PRECIS-2); deferring fraction.
>
> **Independent variables:** LLM partner; appraisal tool; comparison anchor — paper compares against single human-rater accuracy of 89% (PRISMA), 89% (AMSTAR), 75% (PRECIS-2).
>
> "Human−AI collaboration resulted in the best accuracies from 89% to 96% for PRISMA (25/35% deferred), 91%−95% for AMSTAR (27/30% deferred), and 80%−86% for PRECIS-2 (76/71% deferred)." (Woelfle et al., 2024, p. 1)

### How?

> **Procedure:** Five LLMs (Claude-3-Opus, Claude-2, GPT-4-32k-0613, GPT-3.5-turbo-16k-0613, Mixtral-8x22B-instruct-v0.1) were queried via APIs (Anthropic, OpenAI, OpenRouter) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes, (2) explain reasoning, and (3) assign a per-item rating (no/yes/NA for PRISMA/AMSTAR; ordinal 1–5 or NA for PRECIS-2). Claude-3-Opus received page-level PNG images (multimodal); the other four received plain text. Each prompt was run twice (GPT-4 only on 25% of publications).
>
> **For this analysis (human–AI collaboration):** ratings of human rater 1 were combined with each individual LLM's rating; items where human-1 and the LLM matched were compared to human consensus to compute accuracy/kappa, and items where they disagreed were classified as "deferred to a second human rater." This generates 10 possible human–AI pairs (rater-1 × {2 runs each of Opus, Claude-2, GPT-3.5, Mixtral; 1 run of GPT-4 due to cost}).
>
> **Statistics:** 1000-resample publication-level bootstrap 95% CIs in R 4.3; statistical superiority over single-human-rater accuracy declared when CIs of paired and single-rater accuracy did not overlap.
>
> "We combined ratings of individual human raters with individual LLM ratings for each of the three tools. Items where the LLM aligned with the human rater were compared to human consensus. Inconsistent items were considered uncertain and thus 'deferred to a second human rater'. In a practical application of this approach, the first and second human rater would then have to go through their normal consensus process." (Woelfle et al., 2024, p. 5)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p4-1.png]]

### Who?

> **Models:** 5 LLMs paired with human rater 1 → 10 possible pairs (Opus×2, Claude-2×2, GPT-4×1, GPT-3.5×2, Mixtral×2).
>
> **Datasets / sample-size flow:** PRISMA & AMSTAR — 112 systematic reviews & meta-analyses in pediatric surgery (Cullis et al., shared); PRECIS-2 — 56 RCTs (PragMeta database).
>
> **Human rater 1:** experienced reviewer (British pediatric surgeon for PRISMA/AMSTAR; experienced systematic reviewer and metaresearcher for PRECIS-2).
>
> **Processing failures:** Claude-3-Opus 3/112; GPT-4 3/112; GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2; Mixtral 1/112; Claude-2 processed all.
>
> **Significance:** for PRISMA and AMSTAR, 8 of 10 collaboration pairs led to significantly more accurate responses than human rater 1 or 2 alone; for PRECIS-2, only 1 of 10 (Human-1 + GPT-3.5).
>
> "Human−AI collaboration with Claude-3-Opus, Claude-2, GPT-3.5, and Mixtral-8x22B led to significantly more accurate responses than either human rater 1 or 2 alone (8 of 10 possible human−AI pairs)." (Woelfle et al., 2024, p. 8)

## Other Notes

- "Best accuracy" in the abstract refers to the upper bound across the 10 collaboration pairs; the paired numbers in parentheses (e.g., "25/35% deferred") report the deferring fractions of those two best-performing pairs (typically GPT-4 and Claude-3-Opus for PRISMA/AMSTAR).
- For PRISMA + Claude-3-Opus, accepting 96% accuracy spares the second human rater 65% of responses — i.e., 1 wrong response per ~25 spared. For AMSTAR, accepting 95% accuracy spares 70% — 1 wrong per ~20 spared. For PRECIS-2, accepting 86% accuracy spares only 29% — 1 wrong per ~7 spared.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting summary]].

| Pair (Human rater 1 + …) | Accuracy (95% CI) | Cohen's kappa (95% CI) | Deferring fraction (95% CI) |
| --- | --- | --- | --- |
| **PRISMA** + Claude-3-Opus | **96%** (94–96%) | **0.90** (0.88–0.93) | 32% (30–34%) |
| PRISMA + Claude-2 | 96% (94–97%) | 0.92 (0.90–0.94) | 35% (33–37%) |
| PRISMA + GPT-4 | 89% (87–91%) | 0.81 (0.78–0.83) | 25% (23–28%) |
| PRISMA + GPT-3.5 | 95% (93–97%) | 0.91 (0.88–0.94) | 41% (39–43%) |
| PRISMA + Mixtral-8x22B | 95% (94–97%) | 0.92 (0.89–0.94) | 40% (37–44%) |
| **AMSTAR** + Claude-3-Opus | **95%** (94–97%) | **0.92** (0.89–0.94) | 30% (28–33%) |
| AMSTAR + Claude-2 | 93% (92–95%) | 0.88 (0.85–0.91) | 39% (36–42%) |
| AMSTAR + GPT-4 | 95% (89–93%)\* | 0.83 (0.80–0.87) | 27% (25–30%) |
| AMSTAR + GPT-3.5 | 96% (94–97%) | 0.93 (0.90–0.96) | 52% (49–56%) |
| AMSTAR + Mixtral-8x22B | 95% (93–96%) | 0.91 (0.87–0.94) | 44% (41–48%) |
| **PRECIS-2** + Claude-3-Opus | 83% (77–90%) | 0.72 (0.62–0.83) | 75% (72–78%) |
| PRECIS-2 + Claude-2 | 80% (72–88%) | 0.56 (0.35–0.76) | 75% (71–79%) |
| PRECIS-2 + GPT-4 | 80% (72–87%) | 0.63 (0.49–0.76) | 76% (72–80%) |
| PRECIS-2 + GPT-3.5 | **86%** (79–91%) | **0.68** (0.49–0.83) | 71% (68–75%) |
| PRECIS-2 + Mixtral-8x22B | 86% (78–93%) | 0.61 (0.45–0.77) | 70% (66–75%) |
| **Comparison: human rater 1 alone** | 89% PRISMA / 89% AMSTAR / 75% PRECIS-2 | 0.81 / 0.80 / 0.57 | — |

\* Table 3 reports AMSTAR + GPT-4 as 91% (89–93%); the 95%/93% range reported in the abstract appears to be a transcription artefact. Verify against Table 3 before citing.

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The benchmark datasets did not record human time on task preventing quantification of efficiency gains]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Human-AI collaboration outperforms either alone on structured appraisal tasks]]

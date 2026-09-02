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
nodeID: 019ddb4e-6b5e-73ca-b7dd-b90666c44ab3
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "Combined LLM ratings led to accuracies of 75%−88% for PRISMA (4%−74% deferred), 74%−89% for AMSTAR (6%−84% deferred), and 64%−79% for PRECIS-2 (29%−88% deferred)." (Woelfle et al., 2024, p. 1 [Abstract])
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p1-1.png]]
>
> Grounding figure (Fig 3, p. 4): accuracy vs. deferring fraction across consistency thresholds.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-fig2fig3-p4-04.png]]
>
> Grounding table (Table 3, p. 7): combined-LLM accuracies and deferring fractions.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-table3-p7-07.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of LLM ensembling against a fixed human consensus on three evidence-appraisal tools.
>
> **Method type:** consistency-based LLM ensemble, nine assessments per item (across 5 LLMs) combined; only ratings consistent in ≥k of 9 retained, the rest deferred.
>
> **Tools:** PRISMA (27 items × 112 systematic reviews), AMSTAR (11 items × 112 systematic reviews), PRECIS-2 (9 domains × 56 RCTs).
>
> **Dependent variables:** agreement (% identical) and Cohen's kappa with human consensus on the consistent subset; deferring fraction (% of items below the consistency threshold).
>
> **Independent variables:** consistency threshold (5/9, 6/9, 7/9, 8/9, 9/9); appraisal tool (PRISMA / AMSTAR / PRECIS-2).
>
> "Combining multiple assessments from LLMs in a 'consistency' approach improves performance in biomedical and general contexts beyond using only a single assessment. We combined a total of nine LLM assessments: 2 × Claude-3-Opus, 2 × Claude-2, 1 × GPT-4 (due to high costs), 2 × GPT-3.5, 2 × Mixtral-8x22B." (Woelfle et al., 2024, p. 3)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p3-1.png]]

### How?

> **Procedure:** Five LLMs (Claude-3-Opus, Claude-2, GPT-4-32k-0613, GPT-3.5-turbo-16k-0613, Mixtral-8x22B-instruct-v0.1) were queried via APIs (Anthropic, OpenAI, OpenRouter) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning, and (3) assign a per-item rating (no/yes/NA for PRISMA/AMSTAR; ordinal 1–5 or NA for PRECIS-2 with the 1/2 and 4/5 ordinal pairs collapsed for the kappa calculation). Claude-3-Opus received page-level PNG images (multimodal, implicit OCR); the other four models received plain text the authors extracted. Each prompt was run twice (GPT-4 only on 25% of publications due to cost) to estimate intrarater reliability.
>
> **For this analysis (combined LLMs):** all nine LLM runs per item were pooled; consistency thresholds of 5/9–9/9 were applied; non-consistent ratings were marked "deferred"; accuracy and weighted κ (ordinal PRECIS-2) were calculated only on consistent responses.
>
> **Statistics:** bootstrapping with 1000 publication-level resamples for 95% CIs in R 4.3; quote handling and post-processing in Python 3.11.4 (parasail, rapidfuzz).
>
> "All nine LLM assessments were combined using only ratings consistent in a majority of LLM assessments. Responses without such a consistent majority would be deferred to human raters. This approach led to substantial improvements with accuracies ranging from 75% to 88% for PRISMA (while deferring 4%-74% of ratings), from 74% to 89% for AMSTAR (while deferring 6%-84% of ratings), and from 64% to 79% for PRECIS-2 (with deferring fractions from 29% to 88%)." (Woelfle et al., 2024, p. 7)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p7-1.png]]

### Who?

> **Models:** 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B-instruct-v0.1) producing 9 assessment runs per item.
>
> **Datasets / sample-size flow:** PRISMA & AMSTAR, 112 systematic reviews & meta-analyses in pediatric surgery (Cullis et al., shared); 27 PRISMA items × 112 = up to 3024 ratings; 11 AMSTAR items × 112 = up to 1232 ratings. PRECIS-2, 56 RCTs from the PragMeta database; 9 domains × 56 = up to 504 ratings.
>
> **Processing failures (excluded from N):** Claude-3-Opus failed on 3/112 (Anthropic content filtering / context); GPT-4 failed on 3/112 (context length); GPT-3.5 failed on 3/112 PRISMA/AMSTAR + 2/56 PRECIS-2; Mixtral failed on 1/112; Claude-2 processed all.
>
> **Human comparator:** consensus of 2 human raters per publication (PRISMA/AMSTAR: British pediatric surgeons; PRECIS-2: experienced systematic reviewer + MSc epidemiology student or senior clinical epidemiologist).
>
> "We selected datasets for which independent ratings from 2 human raters and their consensus were available… For reporting and methodological rigor, we used human assessments of PRISMA and AMSTAR for 112 systematic reviews and meta-analyses in the field of pediatric surgery (data kindly shared by Cullis and colleagues). PRISMA contains 27 items and AMSTAR 11 items… For pragmatism in clinical trial design, we used human ratings of PRECIS-2 for 56 randomized controlled trials within the PragMeta database." (Woelfle et al., 2024, p. 2)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p2-1.png]]

## Other Notes

- Performance increased monotonically with consistency threshold, but at the cost of larger deferring fractions, at 9/9 consistency for PRISMA and ≥8/9 for PRECIS-2, accuracy and kappa CIs overlap with those of a single human rater.
- 95% CIs were derived from bootstrapping with 1000 resamples on the publication level.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting summary]].

| Tool / consistency threshold | Accuracy (95% CI) | Cohen's kappa (95% CI) | Deferring fraction (95% CI) |
| --- | --- | --- | --- |
| **PRISMA** 5/9 | 75% (73–77%) | 0.59 (0.55–0.62) | 4% (3–5%) |
| PRISMA 6/9 | 79% (78–81%) | 0.65 (0.62–0.68) | 19% (17–21%) |
| PRISMA 7/9 | 81% (81–85%) | 0.71 (0.68–0.74) | 35% (33–38%) |
| PRISMA 8/9 | 86% (84–88%) | 0.76 (0.72–0.79) | 53% (50–56%) |
| PRISMA 9/9 | 88% (85–90%) | 0.77 (0.72–0.81) | 74% (72–77%) |
| **AMSTAR** 5/9 | 74% (72–76%) | 0.56 (0.52–0.60) | 6% (4–8%) |
| AMSTAR 6/9 | 77% (75–80%) | 0.62 (0.58–0.66) | 25% (23–28%) |
| AMSTAR 7/9 | 81% (78–84%) | 0.65 (0.63–0.73) | 47% (44–50%) |
| AMSTAR 8/9 | 83% (79–87%) | 0.73 (0.66–0.79) | 67% (64–70%) |
| AMSTAR 9/9 | 89% (85–94%) | 0.82 (0.75–0.89) | 84% (82–87%) |
| **PRECIS-2** 5/9 | 64% (58–69%) | 0.11 (0.01–0.22) | 18% (14–21%) |
| PRECIS-2 6/9 | 69% (63–74%) | 0.17 (0.04–0.32) | 53% (47–58%) |
| PRECIS-2 7/9 | 71% (64–78%) | 0.22 (0.05–0.40) | 68% (62–73%) |
| PRECIS-2 8/9 | 75% (65–82%) | 0.32 (0.04–0.57) | 79% (74–84%) |
| PRECIS-2 9/9 | 79% (67–89%) | 0.49 (0.20–0.73) | 88% (84–91%) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

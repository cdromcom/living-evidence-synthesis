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
  - forensic/kappa-check/in-bounds
created: 2026-04-27
updated: 2026-04-29
nodeID: 019ddb4e-6b72-7793-93a6-8b8f7cce7291
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "Human inter-rater reliability measured by agreement was 91%, 88%, and 57% and by kappa 0.84, 0.77, nd 0.29 for PRISMA, AMSTAR, and PRECIS-2, respectively." (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-2.png]]

## Methods Context

### What?

> **Study design:** secondary analysis of pre-existing human rating pairs released alongside the benchmark, i.e., human inter-rater reliability (IRR) characterizing the "gold-standard" the LLMs are evaluated against.
>
> **Method type:** pairwise human agreement analysis (rater 1 vs rater 2) on item-level ratings before any consensus discussion.
>
> **Tools:** PRISMA (27 items), AMSTAR (11 items), PRECIS-2 (9 domains).
>
> **Dependent variables:** raw item-level agreement (% identical) and Cohen's kappa (weighted Cohen's kappa for ordinal PRECIS-2).
>
> **Independent variables:** appraisal tool (PRISMA / AMSTAR / PRECIS-2); rater pair (constant within tool).
>
> "Human inter-rater reliability measured by agreement was 91%, 88%, and 57% and by kappa 0.84, 0.77, nd 0.29 for PRISMA, AMSTAR, and PRECIS-2, respectively." (Woelfle et al., 2024, p. 8)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p8-3.png]]

### How?

> **Procedure:** Each publication was independently rated by two human raters before any consensus discussion. The benchmark used the as-released individual ratings (Cullis et al. for PRISMA/AMSTAR; PragMeta database for PRECIS-2) and computed item-level agreement and Cohen's kappa across all rated items per tool. For PRECIS-2 ordinal scoring, responses 1 ("very") and 2 ("mostly explanatory") were pooled to "1/2" and 4 ("mostly") and 5 ("very pragmatic") to "4/5"; a weighted version of Cohen's kappa was used. Bootstrapping with 1000 publication-level resamples gave 95% CIs in R 4.3. Where ratings differed, raters discussed and agreed on a consensus on equal terms, that consensus is the LLM benchmark target, not the IRR result reported here.
>
> "We performed 4 analyses for each of the 3 evidence appraisal tools (PRISMA, AMSTAR, PRECIS-2) (Fig 1) while also quantifying resources used for LLMs (costs and time effort). (1) Human consensus vs individual human raters … For the ordinal PRECIS-2 ratings, responses 1 and 2 ('very' and 'mostly explanatory') were pooled to '1/2' and responses 4 and 5 ('very' and 'mostly pragmatic') to '4/5' and a weighted version of Cohen's kappa was used." (Woelfle et al., 2024, p. 3)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p3-2.png]]

### Who?

> **Raters & sample-size flow:** PRISMA & AMSTAR, 2 British pediatric surgeons (content experts) rating 112 systematic reviews & meta-analyses (PRISMA: up to 3024 ratings = 27 × 112; AMSTAR: up to 1232 ratings = 11 × 112). For human rater 2, ratings for 15 publications were missing for PRISMA and AMSTAR. PRECIS-2, rater 1 was an experienced systematic reviewer and metaresearcher; rater 2 was either 1 of 2 post-graduate MSc students in epidemiology with PRECIS-2 training or a senior clinical epidemiologist and pragmatic-trial expert, rating 56 RCTs (up to 504 ratings = 9 × 56). LLM analyses share the same publication set but are not the focus of this EVD.
>
> "The 2 raters were content experts (British pediatric surgeons)… Human rater 1 was an experienced systematic-reviewer and metaresearcher. Human rater 2 was either 1 of 2 experienced post-graduate MSc students in epidemiology with special training in PRECIS-2 assessment or a senior clinical epidemiologist and expert in pragmatic trial design." (Woelfle et al., 2024, p. 2)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p2-2.png]]

## Other Notes

- The drop from 91% (PRISMA) → 88% (AMSTAR) → 57% (PRECIS-2) parallels LLM performance degradation across the same tools, suggesting task complexity (rather than model capability) is the dominant driver.
- The kappa for PRECIS-2 (0.29, weighted) sits in the "fair" range, borderline reliability for an LLM benchmark target.
- "nd" in the source is a typo for "and"; preserved here per the no-editorialize-quotes principle.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting]].

| Tool | Item-level agreement (95% CI) | Cohen's kappa (95% CI) | Ratings analyzed |
| --- | --- | --- | --- |
| PRISMA (27 items × 112 reviews) | **91%** (89–93%) | **0.84** (0.80–0.88) | 2384 / 2619 (rater-2 missing on 15 reviews) |
| AMSTAR (11 items × 112 reviews) | **88%** (85–90%) | **0.77** (0.72–0.82) | 936 / 1067 (rater-2 missing on 15 reviews) |
| PRECIS-2 (9 domains × 56 RCTs) | **57%** (51–63%) | **0.29 weighted** (0.20–0.37) | 288 / 504 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs]]

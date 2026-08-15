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
  - tripod-llm/proportion/53pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7b-76f9-ab59-4f34c339f6ab
appraisal_overall: L0-M4-H1
tripod_llm_pct: 53pct
---

## Source

[[@darcyMARGMultiAgentReview2024]]

## Description

> "MARG-S generated 3.7 'good' comments per paper (rated by users), whereas a simple baseline of having a single agent generate all comments generated only 1.7 good comments, and a recently proposed method (Liang et al., 2023) produced only 0.3." (D'Arcy et al., 2024, p. 1)
>
> ![[darcyMARGMultiAgentReview2024-evd-p1-1.png]]
>
> "71% of MARG-S's comments were rated as specific." (D'Arcy et al., 2024, p. 2)
>
> ![[darcyMARGMultiAgentReview2024-evd-p2-1.png]]

## Methods Context

### What?

> **Study design:** within-subjects user study comparing three LLM review-generation methods on participants' own scientific papers. **Method type:** human ratings of LLM-generated review comments via web-based survey, with mixed-effects regression for inferential analysis. **Tools:** GPT-4 (gpt-4-0613, 8k context); MARG-S, LiZCa (Liang et al. 2023), and SARG-B baselines; lme4.glmer + ordinal.clmm in R for mixed-effect logistic and cumulative-link analyses; web survey UI (Figure 4). **Dependent variables:** per-comment rating triple — overall quality (Bad / Neutral / Good), accuracy (Major-inaccuracy / Minor-inaccuracy / Accurate), specificity (Very generic / Generic / Specific / Very specific); per-review length and helpfulness on 5-point scales; total "good" comments per review. **Independent variables / covariates:** review-generation method (3 levels) as fixed effect; participant ID (submission ID) as random effect; specificity and accuracy as additional fixed effects when modelling overall rating.
>
> "We conduct a user study to obtain a more reliable (but more expensive) evaluation compared to the automated metrics. To reduce burden on participants, we only evaluate a subset of methods in the user study: MARG-S (our best method on the automated metrics), LiZCa (baseline from prior work), and SARG-B (the simplest baseline)." (D'Arcy et al., 2024, p. 13)
> ![[darcyMARGMultiAgentReview2024-evd-p13-1.png]]

### How?

> **Procedure:** (1) participants uploaded their own paper PDF via a web interface; (2) the system ran MARG-S, LiZCa, and SARG-B on the paper to produce three reviews (each a list of comments); (3) participants received an email with a link to a survey containing the three reviews in random order, with method labels hidden and order of comments within each review preserved; (4) for every comment, participants selected one option each from Specificity (4 levels), Accuracy (3 levels), and Rate this comment (Bad / Neutral / Good), with definitions provided in the survey preamble; (5) at the end of each review, participants rated review length on a 5-point too-short / too-long scale and overall helpfulness on a 5-point Highly-unhelpful / Highly-helpful scale; (6) totals of "good" comments per review were averaged across reviews/participants (Table 5); (7) significance tested with per-user related-sample t-tests, per-comment Barnard's exact test, and mixed-effects logistic / cumulative-link models (Tables 6–8); (8) a post-hoc compliment-detection probe was run on all generated comments by prompting GPT-4 with a JSON-output template to flag flattering remarks, then included as a fixed effect in a sensitivity model.
>
> "When all reviews were generated, participants would receive an email notification with a link to page with reviews and a set of survey questions, depicted in Figure 4. The survey page did not describe the review generation methods or give any indication of which method generated a given review, and the generated reviews were displayed in a random order to reduce bias (the order of comments within reviews was not randomized, however)." (D'Arcy et al., 2024, p. 14)
> ![[darcyMARGMultiAgentReview2024-evd-p13-2.png]]

### Who?

> **Models / participants:** GPT-4 (gpt-4-0613) is the underlying LLM behind all three review methods. Human raters are NLP / HCI researchers from a single research organisation.
>
> **Sample-size flow:** "9 volunteers from a large research organization" recruited → all 9 retained (no exclusions reported) → each rated MARG-S, LiZCa, and SARG-B on their own paper. Per-method comment volume per review averaged: MARG-S 17.1, SARG-B 16.1, LiZCa 3.9 (Table 5), so the comment-level dataset is roughly 9 × (17.1 + 16.1 + 3.9) ≈ 333 rated comments. Participant ID was modelled as a random effect to absorb per-rater bias. Sample size flagged as a limitation in a footnote.
>
> "We recruit 9 volunteers from a large research organization to participate in the study. All participants are researchers in the fields of natural language processing and human-computer interaction." (D'Arcy et al., 2024, p. 13)
> ![[darcyMARGMultiAgentReview2024-evd-p13-3.png]]

## Other Notes

- MARG-S reduced the rate of generic comments from ~60% (single-agent baseline) to 29%, and the user study may be subject to novelty or effort-justification biases.
- MARG-S vs. SARG-B difference in good-comment count significant per Barnard's exact test (p=0.02 per-comment) but not per-user (p=0.12); MARG-S vs. LiZCa not significant (p=0.09 per-comment, p=0.16 per-user).
- Helpfulness: participants rated MARG-S an average of 1.0 points higher on the 5-point scale than the other methods; 5 of 9 participants rated MARG-S 2–3 points higher.
- Length: 6/9 rated MARG-S "way too long"; LiZCa rated "too short" or "way too short" by 7/9.
- Compliment probe: 19% of MARG-S comments included flattery vs. 25% SARG-B and 0% LiZCa; "has_compliment" coefficient 0.11 (p=0.76) — no detectable bias on user ratings.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@darcyMARGMultiAgentReview2024#TRIPOD-LLM reporting summary]].

| Method | Bad / review | Neutral / review | Good / review | Total / review |
| --- | --- | --- | --- | --- |
| **MARG-S** | 8.1 | 5.3 | **3.7** | 17.1 |
| SARG-B | 10.2 | 4.2 | 1.7 | 16.1 |
| LiZCa | 2.7 | 0.9 | 0.3 | 3.9 |

| Specificity (% of comments) | Very generic | Generic | Specific | Very specific |
| --- | --- | --- | --- | --- |
| **MARG-S** | 14.3 | 14.9 | 31.8 | 39.0 |
| SARG-B | 38.6 | 20.7 | 29.0 | 11.7 |
| LiZCa | 48.6 | 11.4 | 28.6 | 11.4 |

| Significance test | Statistic / p |
| --- | --- |
| MARG-S vs. SARG-B good comments (Barnard's exact, per-comment) | p=0.02 |
| MARG-S vs. SARG-B good comments (related-sample t-test, per-user) | p=0.12 |
| MARG-S vs. LiZCa good comments (per-comment) | p=0.09 |
| MARG-S vs. LiZCa good comments (per-user) | p=0.16 |
| MARG-S "very specific" share vs. others (per-user related-sample t-test) | p=0.002 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM-generated peer review feedback is paper-specific not generic boilerplate]]
- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]
- [[EP - Users find LLM-generated peer-review feedback substantively helpful at rates comparable to human reviewers]]

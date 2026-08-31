---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/review-generation
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/55pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b50-7198-b880-a72405b3f97b
appraisal_overall: L1-M3-H1
tripod_llm_pct: 55pct
---

## Source

[[@liangCanLargeLanguage2024a]]

## Description

> "more than half (57.4%) of the users found GPT-4 generated feedback helpful/very helpful and 82.4% found it more beneficial than feedback from at least some human reviewers." (Liang et al., 2024, p. 1, Abstract)
>
> ![[liangCanLargeLanguage2024a-quote-57pct-desc-p1.png]]

## Methods Context

### What?

> **Study design:** prospective user-study survey nested in an LLM scientific-feedback platform.
>
> **Method type:** self-reported 5-point Likert ratings of LLM feedback.
>
> **Tools:** Gradio-based web demo (public URL); GPT-4 feedback pipeline (single-pass prompt over parsed PDF, ScienceBeam parser, 6,500-token prompt budget); 6-page survey (~15–20 min, $20 compensation per respondent).
>
> **Dependent variables:** (i) absolute helpfulness rating ("Highly Unhelpful" → "Highly Helpful", 5 levels) and (ii) comparative benefit vs. human reviewer feedback ("Much Less Helpful Than Most" → "Much More Helpful Than Most", 5 levels).
>
> **Independent variables / covariates:** participant career stage, years of publishing experience, professional status (subgroup analyses in Supp. Figs. 3–4).
>
> "Participants were surveyed about the extent to which they found the LLM feedback helpful in improving their work or understanding of a subject. The majority responded positively, with over 50.3% considering the feedback to be helpful, and 7.1% considering it to be very helpful (Fig. 4a)." (Liang et al., 2024, p. 5)
> ![[liangCanLargeLanguage2024a-evd-p5-1.png]]

### How?

> **Procedure:** authors recruited via (1) relevant institute mailing lists and (2) outreach to all arXiv preprint authors in CS / computational biology with email contact in the first 3 PDF pages (Jan–Mar 2023). Each participant uploaded their own PDF (restricted to papers posted after Sep 2021, GPT-4's training cutoff, to avoid memorization). The Gradio system parsed the PDF with ScienceBeam, sent a paper-specific prompt (title + abstract + figure/table captions + main text up to ~6,500 tokens) to GPT-4, and emailed the structured 4-section feedback (significance & novelty / reasons for acceptance / reasons for rejection / suggestions for improvement). Authors then completed a 6-page survey covering author background, review situation, general impression of LLM review, detailed evaluation, comparison with human review, and additional feedback. Likert percentages reported with 95% CIs; subgroup consistency confirmed across education and experience strata.
>
> "The survey takes around 15-20 minutes and users will be compensated with $20. We recruit the participants through 1) relevant institute mailing lists, and 2) reaching out to all authors who have published at least one preprint on arXiv in the field of computer science and computational biology during January to March, 2023, provided their email contact information is available in the first three pages of the PDF. The study has been approved by Stanford University's Institutional Review Board." (Liang et al., 2024, p. 11)
> ![[liangCanLargeLanguage2024a-evd-p11-1.png]]

### Who?

> **Participants / sample-size flow:** target population = arXiv CS / computational biology preprint authors (Jan–Mar 2023) with discoverable email + recipients of institute mailing lists → opt-in respondents who uploaded their own paper post-9/2021 and completed the 6-page survey → **308 researchers from 110 US institutions** retained for analysis. Authors flag the population is self-selected and skewed toward respondents already familiar with LLMs/AI. Demographic covariates (career stage from undergraduate to faculty/industry; 0 to 10+ years' publishing experience) collected and used in subgroup checks.
>
> **No external models / annotators evaluated** — the unit of measurement is the respondent's rating of GPT-4 feedback on their own paper.
>
> "Through recruitment over institute mailing lists, and contacting paper authors who put preprints on arXiv, we were able to collect survey responses from 308 researchers from 110 US institutions in the field of AI and computational biology that come from diverse education status, experience, and institutes." (Liang et al., 2024, p. 3)
> ![[liangCanLargeLanguage2024a-evd-p3-1.png]]

## Other Notes

- Self-selection bias is explicitly acknowledged by the authors as a study limitation; respondents likely already familiar with / favorably disposed toward LLMs.
- 17.5% of participants considered GPT-4 feedback inferior to most human feedback (Fig. 4c) — i.e., the helpfulness distribution is real but not uniform.
- IRB approval obtained from Stanford; participants compensated $20 for ~15–20 min.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liangCanLargeLanguage2024a#TRIPOD-LLM reporting summary]].

| Survey item (Likert) | Distribution (n=308) |
| --- | --- |
| **Helpful + Highly Helpful** (Fig. 4a) | **57.4%** (Helpful 50.3% + Highly Helpful 7.1%) |
| Neither Unhelpful nor Helpful | 22.7% |
| Unhelpful + Highly Unhelpful | 19.8% (14.9% + 4.9%) |
| **More beneficial than ≥ some human reviewers** (Fig. 4c, levels 2–5) | **82.4%** |
| ↳ Much More Helpful Than Most | 1.6% |
| ↳ More Helpful Than Many, But Less Helpful Than Some | 18.8% |
| ↳ As Helpful As Human | 20.1% |
| ↳ Less Helpful Than Many, But More Helpful Than Some | 41.9% |
| ↳ Much Less Helpful Than Most (inferior) | 17.5% |
| Willingness to reuse the system (Fig. 4g, "Yes") | 50.5% |
| Believes LLM feedback offers overlooked perspectives (≥ some extent) | 65.3% |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The Liang et al user study was subject to self-selection bias as participants opted in to receive LLM feedback]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

- [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Users find LLM-generated peer-review feedback substantively helpful at rates comparable to human reviewers]]

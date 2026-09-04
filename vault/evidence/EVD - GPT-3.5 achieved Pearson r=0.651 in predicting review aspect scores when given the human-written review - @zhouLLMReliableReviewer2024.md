---
NodeFormality: draft
aliases:
tags:
  - task/review-generation
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/43pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b65-72ac-a24a-a127c940f7ed
appraisal_overall: L0-M4-H1
tripod_llm_pct: 43pct
---

## Source

[[@zhouLLMReliableReviewer2024]]

## Description

> "when predicting scores given the review, GPT-3.5 achieves a good correlation value under the few-shot setting (0.651 Pearson correlation), while the baseline is only about 0.3." (Zhou et al., 2024, p. 9342)
>
> ![[zhouLLMReliableReviewer2024-evd-p4-1.png]]
>
> GPT-3.5 few-shot, given review: Pearson=0.651, Spearman=0.659 (Table 1, row 2, p. 9342)

## Methods Context

### What?

> **Study design:** zero-/few-shot LLM evaluation against an existing peer-review benchmark (PeerRead ICLR-2017), no model training.
>
> **Method type:** prompted aspect-score prediction; the model is given a human-written review and asked to output an integer 1–5 for each of 8 review aspects.
>
> **Tools:** OpenAI GPT-3.5-turbo-0613 (and GPT-3.5-16k for the long-input "given paper" condition); PeerRead ICLR-2017 subset; baseline = "most-frequent score" per aspect; comparison metrics computed against gold human aspect scores.
>
> **Dependent variables:** accuracy, absolute difference |diff|, Pearson, Spearman, and Kendall's tau correlations between predicted and gold aspect scores (averaged across aspects in Table 1; per-aspect in Table 2).
>
> **Independent variables:** input type (review vs. paper components), prompting style (zero-shot / few-shot / MCQ-style), and content extraction method (abstract / whole paper / selected sections / abstract+sections).
>
> "For the task of aspect score prediction, we use the ICLR-2017 subset of the PeerRead dataset (Kang et al., 2018). This subset contains 1.3k manually annotated aspect scores (ranging from 1 to 5 inclusive) for 427 official reviews from ICLR-2017 conference." (Zhou et al., 2024, p. 9341)
> ![[zhouLLMReliableReviewer2024-evd-p2-1.png]]

### How?

> **Procedure:** (1) Construct a prompt prefacing the model as "a professional reviewer in computer science and machine learning" and asking it to "predict the review score in several aspects" on a 1–5 scale (system prompt verbatim in Appendix A.1). (2) Run two settings:
>
> **Setting 1, Given Review:** model receives a human-written review and predicts aspect scores; tested zero-shot, few-shot (5 in-context examples), and MCQ-style (each score has an explicit verbal criterion).
>
> **Setting 2, Given Paper:** model receives only the abstract / whole paper / selected sections / abstract+sections, and predicts the same scores. (3) For few-shot, the demonstration examples use "most frequent score" per aspect (justified in Section 3.2 against "all-1" and "all-5" alternatives, Table 3). (4) Inference parameters: GPT-3.5-turbo-0613 / GPT-3.5-16k version 0613, **temperature 0.3** ("If not specially marked, all models are of version 0613 with temperature 0.3"). (5) Compute average accuracy, |diff|, Pearson, Spearman, Kendall's tau across the 8 aspects (Table 1), and per-aspect correlations (Table 2). Aspects flagged "not discussed" by the review are excluded for that aspect.
>
> "We conduct experiments under two different settings: (1) given human-written review, predict aspect scores; (2) given (part of) the research paper, predict scores." (Zhou et al., 2024, p. 9342)
> ![[zhouLLMReliableReviewer2024-evd-p3-1.png]]

### Who?

> **Models / participants:** GPT-3.5-turbo-0613 and GPT-3.5-turbo-16k-0613 (OpenAI; closed-source; training corpora and dates undisclosed). No human raters in this EVD beyond the gold annotators that produced the PeerRead labels.
>
> **Sample-size flow for this EVD:** PeerRead ICLR-2017 subset → **427 official reviews** of ICLR-2017 papers, **1.3k manually annotated aspect scores** on a 1–5 scale across 8 aspects (Recommendation, Substance, Appropriateness, Comparison, Soundness, Originality, Clarity, Impact). All 427 reviews used for evaluation in Setting 1; the "only given abstract" sub-experiment in Table 3 was run on **100 randomly chosen examples** to control cost. No exclusions reported for the headline 0.651 number.
>
> "This subset contains 1.3k manually annotated aspect scores (ranging from 1 to 5 inclusive) for 427 official reviews from ICLR-2017 conference." (Zhou et al., 2024, p. 9341)
> ![[zhouLLMReliableReviewer2024-evd-p2-2.png]]

## Other Notes

When given the paper (not the review), GPT-3.5 correlation drops dramatically (best Pearson ~0.258 for full paper). This demonstrates that LLMs can understand human-written reviews but cannot reliably judge paper quality from the paper alone.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhouLLMReliableReviewer2024#TRIPOD-LLM reporting]].

| Setting (input → prompt style)          | Accuracy ↑ | \|diff\| ↓ | Pearson ↑ | Spearman ↑ | Kendall τ ↑ |
| --------------------------------------- | :--------: | :--------: | :-------: | :--------: | :---------: |
| Baseline: most-frequent score           | **0.404**  |   0.966    |   0.333   |   0.340    |    0.297    |
| Given review: zero-shot                |   0.353    | **0.856**  |   0.548   |   0.553    |    0.475    |
| **Given review: few-shot**             |   0.306    |   1.132    | **0.651** | **0.659**  |  **0.580**  |
| Given review: MCQ style                |   0.336    |   1.025    |   0.558   |   0.565    |    0.492    |
| Given paper: abstract                  |   0.237    |   0.992    |   0.228   |   0.233    |    0.195    |
| Given paper: whole paper (GPT-3.5-16k) |   0.138    |   2.132    |   0.131   |   0.131    |    0.109    |
| Given paper: selected sections         |   0.251    |   0.886    |   0.258   |   0.265    |    0.222    |
| Given paper: abstract & sections       |   0.330    |   0.923    |   0.248   |   0.249    |    0.209    |

| Per-aspect Pearson (given review, few-shot) | Recommendation | Substance | Appropriateness | Comparison | Soundness | Originality | Clarity | Impact |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| GPT-3.5 few-shot | **0.807** | 0.453 | 0.634 | 0.405 | **0.667** | 0.612 | **0.730** | **0.504** |

(Source: Tables 1 and 2, p. 9342; correlation thresholds: gray-coloured cells in Table 2 had p>0.05.)

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM peer-review systems can predict paper acceptance and preference at near-human accuracy]]

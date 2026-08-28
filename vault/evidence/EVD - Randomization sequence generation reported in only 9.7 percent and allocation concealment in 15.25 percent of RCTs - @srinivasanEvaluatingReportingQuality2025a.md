---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/50pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b84-7793-a358-933a1d7afed7
appraisal_overall: L0-M3-H2
tripod_llm_pct: 50pct
---

## Source

[[@srinivasanEvaluatingReportingQuality2025a]]

## Description

> "validity, 9.7% reported randomization sequence generation, 15.25% described allocation mechanisms, and 2.22% provided protocol access information" (Srinivasan et al., 2025, p. 6)
>
> ![[srinivasanEvaluatingReportingQuality2025a-fig2A-p6-1.png]]

## Methods Context

### What?

> **Study design:** large-scale cross-sectional CONSORT-item-level prevalence analysis.
>
> **Method type:** zero-shot LLM binary (MET / NOT MET) classification per CONSORT item, then per-item reporting rate computed across the corpus.
>
> **Tools:** GPT-4o-mini (OpenAI) on Azure PHI-compliant instance; PyMuPDF for PDF→XML; CONSORT 2010 25-item checklist (21 items retained after excluding 2a Background, 7b interim analyses, 3b protocol changes, 6b changes to outcomes, 14b reasons for termination).
>
> **Dependent variable:** per-item proportion of articles where the criterion was MET.
>
> **Independent variable / covariate:** CONSORT item identity (focus here on item 8a randomization sequence generation, item 9 allocation concealment, item 24 protocol access — three methodologically critical items).
>
> "We analyzed reporting patterns across CONSORT section categories (Title & Abstract, Introduction, Methods, Results, Discussion, Other Information) and assessed reporting quality variation by trial phase, funding source, FDA status, geographic location, safety monitoring, and adverse event reporting." (Srinivasan et al., 2025, p. 4)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p4-5.png]]

### How?

> **Procedure:** for each of the 21,041 articles, GPT-4o-mini was prompted independently for each CONSORT criterion (zero-shot, JSON output {is_met, rationale, confidence}). Predictions filtered to high confidence (>90% of articles retained). For each item, the percentage MET was computed across the kept articles, yielding the per-item bars in Fig. 2A. The three items of interest here — randomization sequence generation, allocation concealment, protocol access — were highlighted in the text as methodologically critical and severely underreported. No model fine-tuning or thresholding beyond the High-confidence filter.
>
> "validity, 9.7% reported randomization sequence generation, 15.25% described allocation mechanisms, and 2.22% provided protocol access information (Fig. 2A)." (Srinivasan et al., 2025, p. 6)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p6-2.png]]

### Who?

> **Articles (sample-size flow):** 53,137 open-access human RCTs identified from PubMed (1966–2024) → 21,041 full-text PDFs successfully obtained → 21,041 evaluated by GPT-4o-mini → high-confidence subset (>90% of articles) used to compute per-item reporting rates.
>
> **No human evaluators** for this per-item prevalence step. (Per-item reliability is anchored on the upstream CONSORT-TM benchmark and the 50-article expert validation sub-study.)
>
> "For large-scale analysis, we identified 53,137 open-access human RCTs from PubMed (1966-2024) and successfully obtained 21,041 full-text PDFs." (Srinivasan et al., 2025, p. 3)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p3-4.png]]

## Other Notes

- Other items also flagged as critically underreported in the same passage: external validity discussed in only 1.6% of articles. Frequently reported items by contrast: scientific background/rationale (95.88%) and specific objectives/hypotheses (89.21%).
- Item 24 protocol access at 2.22% is the lowest of the three highlighted items — highly relevant to systematic-reviewer ability to verify methods.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@srinivasanEvaluatingReportingQuality2025a#TRIPOD-LLM reporting summary]].

| CONSORT item | % of 21,041 RCTs reporting |
| --- | :---: |
| **8a Randomization — sequence generation** | **9.7%** |
| **9 Allocation concealment mechanism** | **15.25%** |
| **24 Protocol access** | **2.22%** |
| (Context) 21 Generalizability / external validity | 1.6% |
| (Context) 2b Specific objectives / hypotheses | 89.21% |
| (Context) 2a Scientific background / rationale | 95.88% |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]

- [[CLM - RCT reporting quality has improved substantially over decades but critical methodological gaps persist across all disciplines]]

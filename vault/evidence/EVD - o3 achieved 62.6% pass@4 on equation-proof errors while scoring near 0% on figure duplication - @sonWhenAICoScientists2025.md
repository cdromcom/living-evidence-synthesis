---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/low-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/63pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b87-72f6-b50c-edb52943a447
appraisal_overall: L1-M3-H1
tripod_llm_pct: 63pct
---

## Source

[[@sonWhenAICoScientists2025]]

## Description

> "In the Equation/Proof category, o3 leads with a 62.6% (pass@4), followed by Gemini-2.5-Pro at 36.4%, while all other models remain below 5%, underscoring o3's superior mathematical reasoning. Surprisingly, GPT-4.1 achieves a 44.4% in the Figure Duplication category, outperforming Claude-3.7-Sonnet:Thinking (33.3%), o3 (0%), and Gemini-2.5-Pro (0%), revealing a weakness in figure analysis in reasoning models." (Son et al., 2025, p. 6)

> ![[sonWhenAICoScientists2025-evd-p6-2.png]]
>
> Grounding figure (Figure 4 right panel, p. 6): scatter plot of mean reported confidence vs. pass@4 for each model, broken down by error type.
>
> ![[sonWhenAICoScientists2025-fig4-p6.png]]
>
> Grounding tables (Tables 4 & 5, Appendix G, p. 34): per-error-category and per-paper-category pass@K breakdowns for o3 and GPT-4.1.
>
> ![[sonWhenAICoScientists2025-tables-p34-4.png]]

## Methods Context

### What?

> **Study design:** error-category and domain breakdown of the same SPOT benchmark used in the headline EVD.
>
> **Method type:** stratified zero-shot generative error detection — the headline pass@K aggregate disaggregated by the six inductively-derived error categories.
>
> **Tools:** SPOT category labels (Equation/Proof, Figure Duplication, Data Inconsistency, Statistical Reporting, Reagent Identity, Experiment Setup) and the same Llama-Parse + GPT-4.1 OCR pipeline; pass@K bootstrap (B = 1000).
>
> **Dependent variable:** pass@4 (%) per (model × error category) cell.
>
> **Independent variables:** model (the 6 proprietary multimodal LLMs from Table 2); error-category label (n = 6); paper-category label (n = 10 STEM domains, used in the Appendix G breakdown).
>
> "Error Types: We derive the six categories in Table 1 inductively from our annotations rather than setting a priori. As we review each error, we group similar cases. This is to capture the true distribution of errors existing in manuscripts. During this process, figure-duplication instances initially overwhelmed the dataset, so we filtered based on severity and paper category to prevent a single type from dominating." (Son et al., 2025, p. 3)
> ![[sonWhenAICoScientists2025-evd-p3-1.png]]

### How?

> **Procedure:** identical evaluation pipeline as the headline EVD — same Generation Prompt, same temperature 0.6 / top-p 0.95 sampling, same 8 independent runs per (model × paper) pair, same GPT-4.1 LLM-as-judge match adjudication. After scoring, true-positive / annotation totals are partitioned by the error-category label of each annotation, and pass@K is recomputed within each category by bootstrap-resampling K runs from the 8 (B = 1000 repetitions, K ∈ {1, 2, 4}). The full per-category × per-model matrix appears in Tables 4–13 of Appendix G; Figure 4 right panel projects mean confidence against pass@4 with marker shape encoding the error type.
>
> "For each pass@K we draw K runs without replacement from the eight, repeat this resampling B = 1000 times, and report the mean and standard deviation of the resulting bootstrap distribution for K ∈ {1, 4}." (Son et al., 2025, p. 5)
> ![[sonWhenAICoScientists2025-evd-p5-1.png]]

### Who?

> **Models analysed (n = 6 proprietary multimodal):** o3 (2025-04-16), GPT-4.1 (2025-04-14), Gemini-2.5-Pro (preview-03-25), Gemini-2.0-Flash-Lite (001), Claude-3.7-Sonnet:Thinking, Claude-3.7-Sonnet. Open-source models excluded from this category-level discussion because of their near-zero baselines.
>
> **Annotated errors per category (sample-size flow):** 91 author-confirmed errors total, partitioned as **Equation/Proof 37, Figure Duplication 27, Data Inconsistency 18, Statistical Reporting 4, Reagent Identity 3, Experiment Setup 2**. Per-paper-category counts (Figure 2): Mathematics ≈ 22, Biology ≈ 16, Computer Science ≈ 12, Multidisciplinary ≈ 11, Chemistry ≈ 10, Physics ≈ 8, Materials Science ≈ 7, Medicine ≈ 5, Environmental Science ≈ 3, Engineering ≈ 2 (estimated from bar chart).
>
> **No human evaluators in this EVD's loop;** match adjudication delegated to GPT-4.1.
>
> "We classify each paper into ten research domains: Mathematics, Physics, Biology, Chemistry, Materials Science, Medicine, Environmental Science, Engineering, Computer Science, and Multidisciplinary, based on its journal venue or arXiv subject." (Son et al., 2025, p. 4)
> ![[sonWhenAICoScientists2025-evd-p4-2.png]]

## Other Notes

- Reasoning models (o3, Claude:Thinking) excel at mathematical/proof errors but show weakness in visual/figure analysis.
- GPT-4.1 (non-thinking) outperforms reasoning models on figure duplication, suggesting test-time reasoning effort is mis-allocated for visual tasks.
- Statistical Reporting (n = 4) is o3's strongest category at 88.4% pass@4 but the small denominator means high variance.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sonWhenAICoScientists2025#TRIPOD-LLM reporting summary]].

| Error category (n) | o3 pass@4 | GPT-4.1 pass@4 | Gemini-2.5-Pro pass@4 | Claude-3.7:Think pass@4 |
| --- | :---: | :---: | :---: | :---: |
| **Equation / proof (37)** | **62.6 ± 5.7 (best)** | 1.5 ± 1.5 | 36.4 ± unknown | 3.0 ± 2.0 |
| **Figure duplication (27)** | 0.0 ± 0.0 | **44.4** (best) | 0.0 ± 0.0 | 33.3 |
| Data inconsistency (18) | 25.7 ± 4.3 | 19.2 ± 6.1 | 36.5 ± 6.9 | 29.3 ± 6.9 |
| Statistical reporting (4) | 88.4 ± 12.5 | 0.0 ± 0.0 | 57.7 ± 32.0 | 12.5 ± 12.5 |
| Reagent identity (3) | 62.7 ± 10.8 | 16.5 ± 16.7 | 0.0 ± 0.0 | 16.8 ± 16.7 |
| Experiment setup (2) | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 ± 0.0 |

| Pattern | Implication |
| --- | --- |
| o3 dominates Equation/Proof and Statistical Reporting | reasoning models excel at symbolic/numerical chains |
| o3 and Gemini-2.5-Pro score 0% on Figure Duplication | reasoning training degrades visual-similarity sensitivity |
| GPT-4.1 (non-thinking) wins on Figure Duplication (44.4%) | non-reasoning multimodal pipeline preserves figure analysis |
| Experiment Setup unsolved by all 6 models | long-context, multi-section reasoning beyond current capability |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs fall far short of requirements for dependable AI-assisted academic error verification]]

- [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Text-only LLMs underperform on tasks where figures or tables carry primary information]]

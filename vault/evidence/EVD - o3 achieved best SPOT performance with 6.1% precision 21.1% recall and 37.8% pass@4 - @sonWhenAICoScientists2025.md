---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/error-detection
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
nodeID: 019ddb4e-6b88-7565-bf1e-945d5895aca5
appraisal_overall: L1-M3-H1
tripod_llm_pct: 63pct
---

## Source

[[@sonWhenAICoScientists2025]]

## Description

> "Evaluating state-of-the-art LLMs on SPOT, we find that none surpasses 21.1% recall or 6.1% precision (o3 achieves the best scores, with all others near zero)." (Son et al., 2025, p. 1)

> ![[sonWhenAICoScientists2025-evd-p1-1.png]]
> Table 2 data: o3 (2025-04-16): Precision=6.1±1.3%, Recall=21.1±4.4%, pass@1=18.4±2.1%, pass@4=37.8±1.8%. (Son et al., 2025, p. 5)
>
> Grounding table (Table 2, p. 5): performance of ten models on the SPOT dataset, mean ± std over 8 independent trials.
>
> ![[sonWhenAICoScientists2025-tables-p5-2.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark evaluation of off-the-shelf multimodal LLMs on the SPOT scientific-error-detection dataset.
>
> **Method type:** zero-shot generative error detection with structured-JSON output, scored against author-confirmed ground-truth errors.
>
> **Tools:** SPOT benchmark (83 manuscripts × 91 errors, 47 source papers, 10 STEM domains); Llama-Parse for PDF→Markdown conversion; GPT-4.1 as LLM-as-judge for match adjudication; pass@K bootstrap estimator (Chen et al. 2021).
>
> **Dependent variables:** Precision (%), Recall (%), pass@1 (%), pass@4 (%) — each reported as mean ± std over 8 independent runs per paper.
>
> **Independent variables:** model identity (10 multimodal LLMs — 6 proprietary + 4 open-source); paper × error annotation pair; run index (1–8) for bootstrap resampling.
>
> "We mainly evaluate verification performance through precision, recall, and pass@K. A predicted error is counted as a true positive (TP) only when the model's reported location matches a benchmark annotation and an LLM confirms they indicate the same error." (Son et al., 2025, p. 4)
> ![[sonWhenAICoScientists2025-evd-p4-3.png]]

### How?

> **Procedure:** for every (model, paper) pair the authors run **8 independent inferences**, yielding 83 × 8 = 664 runs per model. Each inference receives the full manuscript as **interleaved text + image data** (Llama-Parse Markdown plus high-fidelity per-page screenshots refined by GPT-4.1) and the *Generation Prompt* (Appendix F.2) instructing the model to act as a "scientific-rigor auditor" and emit JSON `{"has_error": <bool>, "errors": [{"location": ..., "description": ...}]}`. Generation parameters: temperature 0.6, top-p 0.95, repetition penalty 1.0, min/max output tokens 8 / 8192 (provider defaults used when available). The *Evaluation Prompt* asks GPT-4.1 to judge whether each model-reported error matches a benchmark annotation on both location and description. TP/FP/FN aggregated across all 91 annotations to yield Precision and Recall. pass@K computed by bootstrap resampling K runs from the 8 without replacement, B = 1000 repetitions, K ∈ {1, 4}. API call failures or token-limit cutoffs counted as incorrect (each call retried up to 3 times).
>
> "We provide the full paper as interleaved text and image data, followed by the prompt to return every error with each error's location (section, figure, equation, or table), accompanied by a description. The output is prompted to be a structured JSON format" (Son et al., 2025, p. 4)
> ![[sonWhenAICoScientists2025-evd-p4-4.png]]

### Who?

> **Models evaluated (n = 10 multimodal):** 6 proprietary — **o3 (2025-04-16)**, GPT-4.1 (2025-04-14), Gemini-2.5-Pro (preview-03-25), Gemini-2.0-Flash-Lite (001), Claude-3.7-Sonnet:Thinking (20250219:Think), Claude-3.7-Sonnet (20250219); 4 open-source — Qwen2.5-VL-72B/32B-Instruct, Llama-4-Maverick, Llama-4-Scout. All accessed via official APIs (or OpenRouter as fallback); each call retried up to 3 times.
>
> **Evaluation data flow:** WithdrarXiv 14,000 entries → 1,855 after GPT-4o filter → 58 after post-2024 filter; PubPeer 25,378 → 215 post-2024. After author-confirmation (Stage 3) and two-stage human sanity check (Stage 4) → **83 manuscripts / 91 author-confirmed errors / 47 source papers**, spanning Mathematics, Physics, Biology, Chemistry, Materials Science, Medicine, Environmental Science, Engineering, Computer Science, and Multidisciplinary venues. 76/83 papers contain a single error; 6 contain two; 1 contains three. Severity split: 59 errata vs. 32 retractions.
>
> **No human evaluators in this EVD's loop;** GPT-4.1 acts as the match-adjudication judge. Domain-expert review used only in the case studies (Section 4), not for the headline numbers above.
>
> "The final SPOT benchmark comprises 83 manuscripts with 91 annotated errors." (Son et al., 2025, p. 3)
> ![[sonWhenAICoScientists2025-evd-p3-2.png]]

## Other Notes

- All models accessed via APIs; calls retried up to 3 times; failures/cutoffs marked incorrect.
- Gemini-2.5-Pro: precision=3.1%, recall=10.1%, pass@4=25.9% (second best overall on multimodal).
- Open-source models collapse to ~0%: Llama-4-Maverick precision 2.0%, recall 0.9%, pass@4 3.3% — a 20.2 pp gap to o3 on pass@4. Authors note this is the only benchmark (vs. MathVista, MMLU-Pro, GPQA-Diamond, MMMU, HLE) where Llama-4-Maverick "score collapses to near zero (0.9%)."

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sonWhenAICoScientists2025#TRIPOD-LLM reporting summary]].

| Model | Think | Precision (%) | Recall (%) | pass@1 (%) | pass@4 (%) |
| --- | :---: | :---: | :---: | :---: | :---: |
| **o3 (2025-04-16)** | ✓ | **6.1 ± 1.3** | **21.1 ± 4.4** | **18.4 ± 2.1** | **37.8 ± 1.8** |
| GPT-4.1 (2025-04-14) | ✗ | 2.8 ± 0.8 | 6.0 ± 1.6 | 6.6 ± 1.7 | 17.8 ± 1.5 |
| Gemini-2.5-Pro (preview-03-25) | ✓ | 3.1 ± 1.7 | 10.1 ± 5.6 | 7.8 ± 3.8 | 25.9 ± 4.0 |
| Gemini-2.0-Flash-Lite (001) | ✗ | 1.0 ± 0.8 | 1.6 ± 1.1 | 1.5 ± 1.0 | 6.0 ± 1.5 |
| Claude-3.7-Sonnet:Thinking | ✓ | 3.0 ± 1.3 | 6.0 ± 2.4 | 5.5 ± 1.7 | 18.6 ± 2.3 |
| Claude-3.7-Sonnet (20250219) | ✗ | 3.2 ± 1.5 | 5.8 ± 2.7 | 4.5 ± 1.9 | 14.1 ± 1.6 |
| Qwen2.5-VL-72B-Instruct | ✗ | 0.6 ± 1.6 | 0.4 ± 0.7 | 0.4 ± 0.6 | 1.7 ± 1.0 |
| Qwen2.5-VL-32B-Instruct | ✗ | 1.9 ± 2.1 | 1.9 ± 1.7 | 2.0 ± 1.5 | 5.6 ± 1.6 |
| Llama-4-Maverick | ✗ | 2.0 ± 2.6 | 0.9 ± 1.2 | 0.9 ± 1.0 | 3.3 ± 1.2 |
| Llama-4-Scout | ✗ | 0.8 ± 1.0 | 1.9 ± 2.3 | 1.8 ± 2.0 | 7.2 ± 3.1 |

| Cross-benchmark comparison (Figure 3) | o3 score | Llama-4-Maverick score | Δ |
| --- | :---: | :---: | :---: |
| MathVista / MMMU / MMLU-Pro / GPQA-Diamond | >80% | competitive | small |
| HLE | ~20% | low | moderate |
| **SPOT (recall)** | **21.1%** | **0.9%** | **20.2 pp** |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - SPOT benchmark comprised only 83 manuscripts with 91 errors limiting statistical power]]

- [[CVT - SPOT only included papers with explicitly author-confirmed errors potentially excluding harder-to-detect genuine errors]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs fall far short of requirements for dependable AI-assisted academic error verification]]

- [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

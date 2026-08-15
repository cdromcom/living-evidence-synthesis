---
NodeFormality: draft
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/57pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b88-7565-bf1e-945e2d0d55c6
appraisal_overall: L0-M3-H2
tripod_llm_pct: 57pct
---

## Source

[[@louAAAR10AssessingAIs2025]]

## Description

> "a simple baseline that predicts all equations as positive achieves 40% F1 (due to the 1:3 ratio of positive and negative equations), while nearly all open-source LLMs cannot beat this naive baseline. Notably, though the performance of Mixtral is slightly superior to the baseline, the extremely biased precision and recall scores imply that Mixtral is also simply predicting almost all samples as positive instead of truly inferring. Meanwhile, compared to the All-Positive baseline, the performance superiority of the strong close-source LLMs is not significant, the best LLM on this task only obtains 47.98%, which demonstrates the challenge of EQINFER." (Lou et al., 2025, p. 7)
>
> ![[louAAAR10AssessingAIs2025-evd-p7-1.png]]
>
> o3-mini F1=47.98%, Prec=34.34%, Rec=79.59% (Table 1, p. 7)

## Methods Context

### What?

> **Study design:** cross-sectional benchmark evaluation on the new EQINFER task in AAAR-1.0. **Method type:** zero-shot LLM evaluation as binary classification (is the candidate equation correct given paper context?). **Tools:** open-source OLMo-7B, Mistral-7B, Mixtral-8x22B-MoE, Qwen 2.5-72B, Llama 3.1-70B; closed-source Gemini 1.5 Pro, Claude 3.5 Sonnet, GPT-4o (gpt-4o-2024-08-06), o1-preview (o1-preview-2024-09-12), o3-mini; VLLM for open-source inference (PyTorch 2.4.0, CUDA 12.1, 8× A100 GPUs); LiteLLM API wrapper for closed-source. **Dependent variable(s):** binary-classification F1, Precision, Recall. **Independent variable(s) / covariates:** model identity; input context length (100–1,500 words per side, scaling study in Fig. 4); positive/negative equation ratio fixed at 1:3.
>
> "For EQINFER, we adopt F1 as the classification criterion." (Lou et al., 2025, p. 6)
> ![[louAAAR10AssessingAIs2025-evd-p6-4.png]]

### How?

> **Procedure:** four-stage data construction. (1) **Crawling**: ACL Anthology 2019–2023 papers' arXiv LaTeX sources cleaned and merged; regex extracted ≤3 equation snippets per paper, yielding 3,877 human-written positive equations. (2) **GPT-4 negative synthesis**: for each positive equation, GPT-4 prompted at high temperature to generate three different negative-counterpart equations conditioned on paper context. (3) **GPT-4 filtering**: GPT-4 used to remove context-unaligned negatives; pairs where any negative was unaligned were dropped. (4) **Expert examination**: 5 senior PhD students checked all instances against two criteria — grammatical correctness of all equations and semantic distinctness of all negatives from positive. Each pair was checked by ≥2 experts; only unanimous-keep pairs retained → 1,049 positive + 3,147 negative equations. **Inference**: each LLM presented with the cleaned paper text — 1,000 words before + 1,000 words after the masked equation (2,000 words surrounding context) — plus a multiple-choice prompt; per-instance binary judgments aggregated to F1/Precision/Recall in Table 1. Each model run thrice; median reported.
>
> "we fix the maximum input length for all models. According to Table 9, we empirically use 1,000 words for both contexts before and after equations, i.e., 2,000 surrounding words." (Lou et al., 2025, p. 7)
> ![[louAAAR10AssessingAIs2025-evd-p7-2.png]]

### Who?

> **Models / participants:** 10 LLMs (5 open-source + 5 closed-source); 5 senior PhD students annotators for examination phase. No human-subjects in the LLM evaluation.
>
> **Sample-size flow:** ACL Anthology 2019–2023 → 1,762 papers' arXiv LaTeX sources → 3,877 regex-extracted human-written positive equations (≤3/paper) → GPT-4 synthesizes 3 negatives per positive → GPT-4 filtering of context-unaligned negatives → expert examination (≥2 experts per pair, unanimous-keep) drops 27.6% of pairs → **1,049 positive + 3,147 negative equations from 869 source papers retained for EQINFER**. Per Table 9: avg 4,377 left-context words and 6,362 right-context words per equation.
>
> "we get a total of 1,762 papers' source LaTeX packages ... resulting in 3,877 human-written equations ... a total of 1,049 pairs are eventually kept (27.6% pairs are filtered)." (Lou et al., 2025, pp. 3–4)
> ![[louAAAR10AssessingAIs2025-evd-p3-1.png]]

## Other Notes

The EQINFER task is deliberately challenging: even expert human researchers require substantial research accumulation to solve these tasks. Figure 4 shows context-length scaling has limited effect: GPT-4o F1 stays ~40 across 100–1,500 words; Llama-3.1 peaks ~35 at 700 words; Qwen-2.5 stays ~26.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@louAAAR10AssessingAIs2025#TRIPOD-LLM reporting summary]].

| Model | F1 (%) | Precision (%) | Recall (%) |
| --- | --- | --- | --- |
| All-Positive baseline | 40.00 | 25.00 | 100.00 |
| OLMo-7B | 13.64 | 11.93 | 15.91 |
| Mistral-7B | 28.45 | 19.28 | 54.24 |
| Mixtral-8x22B-MoE | 40.90 | 26.15 | 93.80 |
| Qwen 2.5-72B | 31.22 | 26.28 | 57.40 |
| Llama 3.1-70B | 33.08 | 22.14 | 65.39 |
| Gemini 1.5 Pro | 46.74 | 32.05 | 86.27 |
| Claude 3.5 Sonnet | 45.13 | 29.48 | **96.18** |
| GPT-4o | 40.35 | 30.79 | 58.53 |
| o1-preview | 46.35 | 31.43 | 88.27 |
| **o3-mini (best)** | **47.98** | **34.34** | 79.59 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The AAAR data leakage problem from LLM training corpus was not resolved]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Closed-source LLMs outperform open-source on zero-shot scientific-evaluation benchmarks with fine-tuning as the exception]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]
- [[EP - Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks]]

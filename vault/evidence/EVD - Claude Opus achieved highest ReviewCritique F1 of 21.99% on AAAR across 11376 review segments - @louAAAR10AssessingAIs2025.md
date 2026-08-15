---
NodeFormality: ReadyForInternal
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
nodeID: 019ddb4e-6b5d-7118-952d-e02a51aec515
appraisal_overall: L0-M3-H2
tripod_llm_pct: 57pct
---

## Source

[[@louAAAR10AssessingAIs2025]]

## Description

> Claude Opus best F1=21.99% on REVIEWCRITIQUE task across all models (Table 7, Lou et al., 2025, p. 11)
>
> "Closed-source models (GPT-4, Claude Opus, and Gemini 1.5) generally outperform open-source models (Llama3-8B and 70B, Qwen2-72B) in F1 score. Claude Opus achieves the highest F1 scores, with GPT-4 and Gemini 1.5 performing slightly worse." (Lou et al., 2025, p. 11)
>
> ![[louAAAR10AssessingAIs2025-evd-p10-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark evaluation (re-using REVIEWCRITIQUE dataset from Du et al. 2024). **Method type:** zero-shot LLM evaluation on per-segment binary classification (deficient vs. non-deficient). **Tools:** closed-source LLMs gpt-4-1106-preview, claude-3-5-sonnet-20240620 (paper labels best result as "Claude Opus" in Table 7), gemini-1.5-pro-002; open-source Llama3-8B, Llama3-70B, Qwen2-72B; LiteLLM API wrapper; VLLM for open-source inference. **Dependent variable(s):** per-segment Precision / Recall / F1 (binary classification of review-segment reliability), plus ROUGE-1/2/L and BERTScore for the deficiency-explanation generation. **Independent variable(s) / covariates:** prompting strategy (Labeling-All vs. Select-Deficient) and ensembling rule across the two prompts (Both "No" vs. Either "No"); model identity (open vs. closed source).
>
> "For REVIEWCRITIQUE, we use F1 score as the classification metric; while for the deficiency explanation, we use ROUGE (Lin, 2004) and BERTScore (Zhang et al., 2020) to reflect how well the model-generated explanation aligns with the expert's annotation." (Lou et al., 2025, p. 6)
> ![[louAAAR10AssessingAIs2025-evd-p6-1.png]]

### How?

> **Procedure:** Each long human review was split into sentence-level segments (viewpoints). Two prompting strategies were applied per model: (i) **Labeling-All** — supply all indexed segments and require the LLM to output a list of {id, reliable_or_not, explanation} triples; (ii) **Select-Deficient** — supply all indexed segments and require the LLM to output only the {id, explanation} tuples it believes are deficient. Outputs from both prompts were then ensembled with two rules: **Both "No"** (segment is deficient only if both prompts label it deficient) and **Either "No"** (deficient if either prompt does). Per-segment Precision / Recall / F1 against gold deficient labels were computed for each (model × prompt-strategy) cell of Table 7; each model was run three times and the median result reported.
>
> "As individual review comments are split into multiple smaller segments (sentences), in order to avoid the performance variance that comes from the prompting, we follow Du et al. (2024) to utilize two prompting strategies. i) Labeling-All: given everything necessary including a list of indexed review segments, require the LLM to output a list of triples, like {id, reliable or not, explanation}. ii) Select-Deficient: Given everything necessary including a list of indexed review segments, require the LLM to output a list of tuples, {id, explanation}, when it believes the 'id' corresponds to a deficient segment." (Lou et al., 2025, p. 10)
> ![[louAAAR10AssessingAIs2025-evd-p10-2.png]]

### Who?

> **Models / participants:** 6 LLMs evaluated — closed-source GPT-4 (gpt-4-1106-preview), Claude Opus (Table 7 column reports the Anthropic Claude family), Gemini 1.5 Pro (gemini-1.5-pro-002); open-source Llama3-8B, Llama3-70B, Qwen2-72B. No human subjects in the LLM evaluation step; the underlying dataset was annotated by 40+ AI experts in Du et al. 2024.
>
> **Sample-size flow (REVIEWCRITIQUE corpus reused from Du et al. 2024):** ICLR initial submissions crawled from OpenReview → 100 papers retained, with 380 human reviews → each review split into sentence-level segments → **11,376 review segments (viewpoints) used as evaluation instances**, each labeled deficient/non-deficient by senior AI researchers with detailed human explanations.
>
> "We reuse the REVIEWCRITIQUE dataset from our recent work (Du et al., 2024), where we crawled papers' initial submissions along with their reviews from OpenReview and employed more than 40 AI research experts to label each review segment (i.e., deficient or not), with detailed human explanations. In total, there were 100 papers with 380 human reviews. Each review was divided into sentence-level segments, resulting in 11,376 review segments (viewpoints)." (Lou et al., 2025, p. 10)
> ![[louAAAR10AssessingAIs2025-evd-p6-2.png]]

## Other Notes

Despite being the best model, Claude Opus F1=21.99% is very low in absolute terms, indicating the task is highly challenging. Recall scores are consistently higher than precision across all models, suggesting LLMs over-predict deficiency.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@louAAAR10AssessingAIs2025#TRIPOD-LLM reporting summary]].

| Model × prompt strategy | Precision / Recall / F1 (%) |
| --- | --- |
| **Claude Opus — Either "No" (best overall)** | **16.94 / 42.12 / 21.99** |
| Claude Opus — Labeling-All | 16.86 / 34.26 / 20.35 |
| Claude Opus — Select-Deficient | 17.69 / 26.61 / 18.71 |
| Claude Opus — Both "No" | 17.14 / 18.70 / 15.78 |
| GPT-4 — Either "No" (best for GPT-4) | 14.72 / 47.68 / 20.66 |
| Gemini 1.5 — Either "No" (best for Gemini) | 14.46 / 50.37 / 20.34 |
| Llama3-70B — Either "No" (best open-source) | 12.46 / 50.02 / 18.43 |
| Qwen2-72B — Either "No" | 10.49 / 43.00 / 15.16 |
| Llama3-8B — Both "No" (best for 8B) | 11.37 / 21.27 / 12.46 |
| All-segments-deficient naive baseline | not reported |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]

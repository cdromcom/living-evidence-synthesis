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
nodeID: 019ddb4e-6b76-7366-b2d5-e2ef753a7363
appraisal_overall: L1-M3-H1
tripod_llm_pct: 63pct
---

## Source

[[@sonWhenAICoScientists2025]]

## Description

> "Across 498 model–instance evaluations (83 instances × 6 models), we observe only two cases (both from o3) of full confidence, highlighting the widespread difficulty of reliably detecting errors in scientific manuscripts." (Son et al., 2025, p. 7)
>
> ![[sonWhenAICoScientists2025-evd-p7-1.png]]
>
> Grounding figure (Figure 4, p. 6): kernel density estimates of model confidence (left) and scatter of mean confidence vs. pass@4 (right).
>
> ![[sonWhenAICoScientists2025-fig4-p6.png]]

## Methods Context

### What?

> **Study design:** post-hoc calibration sub-analysis nested in the SPOT benchmark evaluation.
>
> **Method type:** unbiased per-error confidence estimation derived from the same 8-run pass@K resampling protocol — i.e., self-estimated confidence is computed from observed run-level success rates, NOT from model-reported probabilities or verbalised confidence.
>
> **Tools:** the pass@K bootstrap estimator (Appendix C); kernel density estimation; scatter visualisation against pass@4 (Figure 4 right).
>
> **Dependent variable:** mean self-estimated confidence (%) per (model × instance) pair, defined as $\hat{p}_{i,g} = 1 - \binom{n - c_{i,g}}{K} / \binom{n}{K}$ aggregated across ground-truth errors.
>
> **Independent variables:** model identity (n = 6 proprietary multimodal); paper × annotated-error pair (n = 83 papers contributing 91 annotations); error category (used as scatter-marker shape).
>
> "Alongside pass@4, calibration indicates how much we should trust a model's predictions. In error detection, where false positives can incur substantial time and labor, knowing when to trust a model is crucial. For each error category, we assess calibration by comparing the model's actual performance, measured as its average pass@4 rate, with its self-estimated confidence." (Son et al., 2025, p. 6)
> ![[sonWhenAICoScientists2025-evd-p6-1.png]]

### How?

> **Procedure:** for each ground-truth error $g$ in paper $i$, count $c_{i,g}$ = the number of independent runs (out of $n = 8$) in which the model successfully detected $g$. The unbiased estimator for the probability that K fresh attempts include at least one success is $\hat{p}_{i,g} = 1 - \binom{n - c_{i,g}}{K} / \binom{n}{K}$ (Appendix C.1, Eq. 5). These per-error confidences are then aggregated to a per-(model × instance) confidence (Eq. 6). Authors plot the kernel density of these confidences across all model-instance pairs (Figure 4 left, one panel per model) and scatter mean confidence vs. pass@4 with the diagonal marking perfect calibration (Figure 4 right). Same 8-run base data as the headline EVD; same temperature 0.6 / top-p 0.95 sampling.
>
> "To assign each ground-truth error g ∈ Gi a confidence score, we perform n independent runs (here n = 8) and let ci,g be the number of runs in which g is detected. The probability that all K fresh attempts miss g is … So one minus this quantity is the probability of ≥ 1 success. Hence the unbiased estimator for the pass@K probability of error g is" (Son et al., 2025, p. 24)
> ![[sonWhenAICoScientists2025-evd-p24-1.png]]

### Who?

> **Models analysed (n = 6 proprietary multimodal):** o3 (2025-04-16), GPT-4.1 (2025-04-14), Gemini-2.5-Pro (preview-03-25), Gemini-2.0-Flash-Lite (001), Claude-3.7-Sonnet:Thinking, Claude-3.7-Sonnet. Open-source models excluded from the calibration figure.
>
> **Evaluation data flow:** **83 SPOT papers × 6 models = 498 model-instance evaluations**; each instance summarises 8 independent runs and the 91 annotated errors distributed across the 83 papers.
>
> **No human evaluators in this EVD's loop;** confidence is derived entirely from the model's empirical run-level success rates plus the bootstrap estimator.
>
> "We provide the full paper as interleaved text and image data, followed by the prompt to return every error with each error's location (section, figure, equation, or table), accompanied by a description." (Son et al., 2025, p. 4)
> ![[sonWhenAICoScientists2025-evd-p4-1.png]]

## Other Notes

- Miscalibration means confidence estimates cannot be used to filter reliable predictions: even o3, the best model, has only 2 full-confidence cases out of 83.
- Confidence correlates only weakly with pass@4 (Figure 4 right), so models cannot self-flag the rare errors they actually catch.
- Models rarely rediscover the same errors across independent runs, further undermining reliability.
- Confidence here is an **objective frequency-derived estimate** (run-level success rate), not the model's verbalised self-confidence — a stronger calibration signal because it cannot be inflated by overconfident phrasing.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sonWhenAICoScientists2025#TRIPOD-LLM reporting summary]].

| Calibration metric | Value |
| --- | :---: |
| Total model-instance evaluations | 498 (83 × 6) |
| Cases of full (=1.0) confidence | **2** (both from o3) |
| Confidence-distribution shape | KDE peaks near 0 for all 6 models (Figure 4 left) |
| Confidence vs. pass@4 (Figure 4 right) | weak positive — points fall well below the y = x diagonal |

| Confidence formula | Definition |
| --- | --- |
| Per-error confidence | $\hat{p}_{i,g} = 1 - \binom{n - c_{i,g}}{K} / \binom{n}{K}$ with $n = 8$ runs, $K$ from {1, 4} |
| Aggregate confidence | $\text{Confidence} = (1/\sum_i |G_i|) \sum_i \sum_{g \in G_i} \hat{p}_{i,g}$ |
| Interpretation of "full confidence" | model detects error $g$ in all 8 runs ($c_{i,g} = 8$), so $\hat{p}_{i,g} = 1$ |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs fall far short of requirements for dependable AI-assisted academic error verification]]

- [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM confidence calibration on scientific-error tasks is poor with extreme distributions]]

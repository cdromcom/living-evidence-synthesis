---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/error-detection
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/70pct
  - 5c/credibility
  - forensic/kappa-check/in-bounds
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b70-756a-bcc7-52d910bd1659
appraisal_overall: L0-M3-H2
tripod_llm_pct: 70pct
---

## Source

[[@xuCanLLMsIdentify2025]]

## Description

> GPT-4o coarse accuracy = 52.0%, Human = 86.0%, MARG = 68.1% on LIMITGEN-Syn (Table 3, Xu et al., 2025, p. 9)
>
> "Even the best-performing LLM, GPT-4o, can only identify about half of the limitations that humans consider very obvious." (Xu et al., 2025, p. 9)
>
> ![[xuCanLLMsIdentify2025-evd-p8-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark evaluation of LLM-based and agent-based systems against a synthetic perturbation-based benchmark with a human-expert ceiling.
>
> **Method type:** zero-shot generation followed by automated coarse-grained classification by GPT-4o judge plus a parallel human evaluation.
>
> **Tools:** LIMITGEN-Syn benchmark (1,000 perturbed examples derived from 500 NLP arXiv papers); evaluated systems = GPT-4o, GPT-4o-mini, Llama-3.3-70B, Qwen-2.5-72B, and the MARG multi-agent system (D'Arcy et al. 2024) instantiated with GPT-4o-mini agents; GPT-4o as automated judge.
>
> **Dependent variable(s):** coarse-grained accuracy (proportion of papers where at least one generated limitation correctly matches the intended perturbed subtype) under both automated (GPT-4o classifier) and human evaluation; fine-grained 0–5 score on relatedness/specificity.
>
> **Independent variable(s):** system identity (5 LLM/agent systems vs. human baseline); evaluation modality (automated vs. human, n=100 sample).
>
> "We evaluate the performance of 4 frontier LLMs across two distinct categories in our benchmark: (1) Proprietary LLMs, including GPT-4o and GPT-4o-mini (OpenAI, 2024); and (2) Open-source LLMs, including Llama-3.3-70B (AI@Meta, 2024), Qwen2.5-72B (Yang et al., 2024). We require each model to generate the most significant limitations for an aspect of a paper. In the LIMITGEN-Syn experiments, we measure whether models identify the single most prominent limitation in each paper within their top three generated limitations, ensuring a fair comparison across systems." (Xu et al., 2025, p. 6)
> ![[xuCanLLMsIdentify2025-evd-p7-1.png]]

### How?

> **Procedure:** (1) Build LIMITGEN-Syn, collect 1,408 NLP arXiv papers (Mar 1 – May 31, 2024), parse with `s2orc-doc2json`, filter to 500 high-quality experimental papers; for each paper apply human-expert-selected perturbations across 11 limitation subtypes (e.g., remove preprocessing details, replace appropriate dataset with inappropriate one) using GPT-4o as the perturbation engine, with human validation revising 112 of 1,000 examples. (2) Each evaluated system is prompted to generate the most significant limitations for a target aspect of the perturbed paper. For MARG, a leader/worker/expert agent triple coordinates over GPT-4o-mini agents. (3) Coarse-grained automated evaluation: GPT-4o classifies whether any of the system's top-3 generated limitations matches the intended subtype; "a sample is deemed correct in the coarse-grained evaluation if at least one generated limitation accurately matches the subtype." (4) Parallel human evaluation: 100 examples sampled from LIMITGEN-Syn; two expert annotators (Annotators 1 and 6, both with NLP/AI publications) independently solve them blind to system identity and the human baseline accuracy is reported (86.0%). (5) Reliability: 50 fixed instances assessed by two annotators yielded Cohen's κ = 0.833 on LIMITGEN-Syn, and a fine-grained-vs-accuracy correlation of 0.96.
>
> "For LIMITGEN-Syn, we use GPT-4o to classify the generated limitations and assess whether they correctly identify the intended subtype. Accuracy is used as the evaluation metric: a sample is deemed correct in the coarse-grained evaluation if at least one generated limitation accurately matches the subtype." (Xu et al., 2025, p. 5)
> ![[xuCanLLMsIdentify2025-evd-p6-1.png]]

### Who?

> **Models / participants evaluated:** 4 LLMs (GPT-4o, GPT-4o-mini, Llama-3.3-70B, Qwen-2.5-72B) + 1 multi-agent system (MARG with GPT-4o-mini agents) + a human-expert baseline.
>
> **Human-baseline annotators:** 2 expert annotators (Annotators 1 and 6 in Table 7), each with >10 or 1–5 NLP/AI publications, drawn from a 6-annotator pool that also handled data annotation, validation, and human evaluation.
>
> **Sample-size flow (LIMITGEN-Syn data):** 1,408 NLP arXiv papers (Mar–May 2024) → exclude surveys / position papers / dissertations and low-quality papers → 500 papers retained → perturbations generated → 1,000 examples after annotation (112 revised by humans). Automated evaluation: full benchmark averaged across all subtypes. Human evaluation: random sample of 100 examples from the dataset. Human baseline: random sample of 50 examples per subset, solved by 2 expert annotators.
>
> "In total, we compile an initial pool of 1,408 NLP papers for further annotation. We exclude papers that do not focus on experimental work, such as surveys, position papers, and dissertations… This filtering process led us to 500 papers." (Xu et al., 2025, p. 4)
> ![[xuCanLLMsIdentify2025-evd-p5-1.png]]

## Other Notes

- MARG here refers to the multi-agent system adapted from D'Arcy et al. (2024), instantiated with GPT-4o-mini chat agents in three roles (leader, worker, expert).
- RAG augmentation lifts GPT-4o coarse accuracy from 52.0% to 64.2% (+12.2 pp), still ~22 pp below the 86% human ceiling. See companion EVD on RAG.
- Cohen's κ between the two LIMITGEN-Syn evaluators = 0.833 (high agreement); automated-vs-accuracy correlation = 0.96 supports use of GPT-4o as judge.
- Human-evaluation accuracy column (45.9% for GPT-4o, 82.0% for Human) is computed on the 100-example sample and is systematically lower than coarse automated accuracy on the full set.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@xuCanLLMsIdentify2025#TRIPOD-LLM reporting summary]].

| System | Coarse Acc. (auto, %) | Fine (0–5) | Human-eval Acc. (%) |
| --- | :---: | :---: | :---: |
| **Human baseline** | **86.0** | **3.52** | **82.0** |
| **GPT-4o** | **52.0** | **1.34** | **45.9** |
| GPT-4o-mini | 49.1 | 1.25 | 37.8 |
| Llama-3.3-70B | 45.7 | 1.15 | 32.7 |
| Qwen-2.5-72B | 47.1 | 1.20 | 31.5 |
| **MARG (multi-agent)** | **68.1** | **1.83** | **54.8** |

| Reliability metric | Value |
| --- | --- |
| Inter-annotator κ (LIMITGEN-Syn, 50 instances, 2 annotators) | 0.833 |
| Fine-grained ↔ accuracy correlation (LIMITGEN-Syn) | 0.96 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The LimitGen benchmark focused only on AI research limiting applicability to other scientific domains]]

- [[CVT - The LimitGen-Syn perturbation approach introduced artificial limitations that may not match organic research flaws]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]

- [[CLM - RAG augmentation improves LLM limitation identification by grounding generation in domain-relevant literature]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

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
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/70pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b84-7793-a358-9339bf832827
appraisal_overall: L0-M3-H2
tripod_llm_pct: 70pct
---

## Source

[[@xuCanLLMsIdentify2025]]

## Description

> GPT-4o coarse accuracy without RAG = 52.0%; with RAG = 64.2% (+12.2%); fine-grained fine score: 1.34 → 1.71 (+0.37) (Table 3, Xu et al., 2025, p. 9)
>
> "incorporating the RAG method can enhance LLM performance in refining their outputs." (Xu et al., 2025, p. 9)
>
> ![[xuCanLLMsIdentify2025-evd-p8-2.png]]

## Methods Context

### What?

> **Study design:** within-system pre/post benchmark comparison of LLM and multi-agent systems with vs. without a RAG augmentation pipeline, evaluated on the same LIMITGEN-Syn (1,000 perturbed examples) and LIMITGEN-Human (1,000 examples from ICLR 2025) benchmarks. **Method type:** zero-shot limitation generation augmented by retrieved external context, scored by GPT-4o automated judge plus human evaluation. **Tools:** Semantic Scholar Recommendation and Relevance APIs; GPT-4o-mini as reranker; same evaluated systems as the primary EVD (GPT-4o, GPT-4o-mini, Llama-3.3-70B, Qwen-2.5-72B, MARG); GPT-4o as automated coarse-grained classifier. **Dependent variable(s):** Δ in coarse-grained accuracy (LIMITGEN-Syn) and Δ in fine-grained 0–5 score (both subsets); for LIMITGEN-Human, also Δ in Jaccard overlap with ground-truth limitations and Δ in human-rated faithfulness/soundness/importance. **Independent variable(s):** RAG on vs. RAG off (within-system); also RAG retrieval setting (top-3 reranked vs. top-5 reranked vs. last-5 of 18 retrieved) ablated on LIMITGEN-Human (Table 5).
>
> "we enhanced the evaluated systems' capabilities by incorporating the RAG module, a method proven effective for knowledge-intensive tasks (Lewis et al., 2020; Shi et al., 2024), to ground limitation generation in the related literature. This method enables the LLMs to retrieve and consider related works when evaluating limitations in the given research paper." (Xu et al., 2025, p. 7)
> ![[xuCanLLMsIdentify2025-evd-p7-2.png]]

### How?

> **Procedure:** (1) For each examined paper, look up its Semantic Scholar ID; if available, fetch up to 20 recommended papers from the Recommendation API; if unavailable, prompt GPT-4o to generate a query from the paper's abstract and use the Relevance API instead — top-3 results become seed papers and each seed yields 5 additional recommendations, producing a pool of 18 candidates. (2) GPT-4o-mini reranks the 18 candidates by abstract similarity to the input paper; top-5 are kept. (3) Because of context-window limits, GPT-4o-mini extracts content related to methodology, experimental design, result analysis, and literature review from each retained paper; the extracted snippets are concatenated and supplied as additional context to the limitation-generation prompt. For MARG, the expert agent issues the retrieval and refines the leader's draft limitations using the retrieved evidence. (4) Re-run the same coarse-grained automated evaluation pipeline (GPT-4o classifier on top-3 generated limitations) and the human evaluation (100-sample subset for LIMITGEN-Human) on each system with RAG enabled, and report the Δ vs. the no-RAG row.
>
> "Specifically, the retrieval process leverages the Semantic Scholar API and adapts based on the input paper's availability in the database. If the paper is available the database, we use its Semantic Scholar ID to fetch at most 20 recommended papers via the recommendation API… These retrieved papers are then reranked by GPT-4o-mini, which assesses the similarity between the input paper and the candidates. The top 5 papers are selected." (Xu et al., 2025, p. 7)
> ![[xuCanLLMsIdentify2025-evd-p7-3.png]]

### Who?

> **Models evaluated with RAG (LIMITGEN-Syn):** GPT-4o, GPT-4o-mini, Llama-3.3-70B, Qwen-2.5-72B, MARG — same 5 systems as the primary benchmark, each scored both with and without the RAG module on the identical 1,000-example LIMITGEN-Syn set.
>
> **LIMITGEN-Human cohort (used for the RAG-setting ablation in Table 5):** 1,000 examples sampled from 9,844 ICLR 2025 submissions; for the RAG-setting ablation, 100 examples from LIMITGEN-Human are randomly sampled and run through GPT-4o-mini under three retrieval settings (top-3 reranked, top-5 reranked, last-5).
>
> **Annotators / evaluators:** human evaluation on 100 examples per subset by NLP/AI experts (see Table 7). User-study generalization (Table 6) used 2 outside-domain experts (biomedical, computer networks) producing 5 papers each → 32 perturbed examples annotated, then 2 evaluators rated GPT-4o and Llama-3.3-70B outputs with vs. without RAG.
>
> "We collect a total of 9,844 papers and randomly sample 1,000 of them for experimentation." (Xu et al., 2025, p. 5)
> ![[xuCanLLMsIdentify2025-evd-p6-2.png]]

## Other Notes

- Human accuracy (86.0%) still greatly exceeds GPT-4o + RAG (64.2% coarse on LIMITGEN-Syn). RAG meaningfully helps but does not close the human–LLM gap.
- The RAG pipeline used here is deliberately simple (Semantic Scholar API + GPT-4o-mini rerank + concatenated extract); the authors explicitly note "this study does not explore advanced RAG techniques" (Limitations section, p. 10).
- LIMITGEN-Human Jaccard scores are very low across the board (best with RAG: GPT-4o = 18.8%; MARG = 17.7%) because MARG and LLMs generate far more limitation comments than the ICLR ground truth contains.
- RAG-setting ablation (Table 5, GPT-4o-mini on 100 LIMITGEN-Human examples) shows top-5 reranked gives the best fine-grained gain (+0.05) but even "last-5 of 18" still helps faithfulness/soundness modestly — i.e., RAG benefits are partly robust to retrieval relevance.
- User study on 32 examples in biomedical and computer-network domains (Table 6) replicates the RAG benefit out-of-domain (e.g., GPT-4o biomedical accuracy 31.3% → 50.0% with RAG).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@xuCanLLMsIdentify2025#TRIPOD-LLM reporting summary]].

| System (LIMITGEN-Syn) | Coarse Acc. base → +RAG (Δ) | Fine (0–5) base → +RAG (Δ) | Human Acc. base → +RAG (Δ) |
| --- | :---: | :---: | :---: |
| **GPT-4o** | **52.0 → 64.2 (+12.2)** | **1.34 → 1.71 (+0.37)** | **45.9 → 61.9 (+16.0)** |
| GPT-4o-mini | 49.1 → 53.3 (+4.2) | 1.25 → 1.38 (+0.13) | 37.8 → 43.7 (+5.9) |
| Llama-3.3-70B | 45.7 → 48.1 (+2.4) | 1.15 → 1.20 (+0.05) | 32.7 → 37.2 (+4.5) |
| Qwen-2.5-72B | 47.1 → 48.4 (+1.3) | 1.20 → 1.23 (+0.03) | 31.5 → 35.4 (+3.9) |
| **MARG** | **68.1 → 77.9 (+9.8)** | **1.83 → 2.10 (+0.27)** | **54.8 → 72.5 (+17.7)** |

| LIMITGEN-Human (Table 4) | Jaccard Δ | Fine Δ | Faith. Δ | Sound. Δ | Import. Δ |
| --- | :---: | :---: | :---: | :---: | :---: |
| GPT-4o w/ RAG | +2.9 | +0.13 | +0.49 | +1.13 | +0.60 |
| MARG w/ RAG | +2.5 | +0.24 | +0.40 | +0.98 | +0.43 |

| Out-of-domain user study (Table 6, GPT-4o) | base | +RAG |
| --- | :---: | :---: |
| Biomedical | 31.3% | 50.0% |
| Computer Networks | 37.5% | 56.3% |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]

- [[CLM - Multi-agent LLM systems produce more specific and helpful scientific paper feedback than single-agent approaches]]

- [[CLM - RAG augmentation improves LLM limitation identification by grounding generation in domain-relevant literature]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]

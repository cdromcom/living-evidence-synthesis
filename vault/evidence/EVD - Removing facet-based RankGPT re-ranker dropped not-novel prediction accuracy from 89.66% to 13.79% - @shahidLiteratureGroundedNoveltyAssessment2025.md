---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/41pct
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b85-7544-bc4e-40e88e0586c4
appraisal_overall: L0-M2-H3
tripod_llm_pct: 41pct
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

## Description

> "Table 2 shows that the complete system, which employs facet-based re-ranking in RankGPT, significantly outperforms its ablated variants in accuracy." (Shahid et al., 2025, p. 7)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p7-1.png]]
> Complete system accuracy for 'not novel' prediction: 89.66%; removing RankGPT relevance re-ranker: 13.79%; removing embedding filtering: 10.34%. (Shahid et al., 2025, p. 7 — Table 2)
> [Screenshot: Table 2, p. 7 — accuracy of predicting 'not novel' under ablation conditions]

## Methods Context

### What?

> **Study design:** ablation study within the Idea Novelty Checker pipeline (component-removal benchmark, focused on the "not novel" decision class).
>
> **Method type:** lesion experiments — each ablation removes or replaces a single retrieval/re-ranking stage and measures the resulting drop in not-novel-class accuracy.
>
> **Tools:** Idea Novelty Checker pipeline (Semantic Scholar Search API + Snippet API; SPECTER-2 embeddings; facet-based RankGPT re-ranker); novelty evaluator switched to **o3-mini** for this ablation; **gpt-4o** retained for re-ranking (Step 2).
>
> **Dependent variable:** accuracy of predicting "not novel" on the 58-item ablation set (single-class accuracy, not full binary classification metrics).
>
> **Independent variable:** ablation condition — (i) Complete System; (ii) Relevance RankGPT (general-relevance prompt instead of facet-based); (iii) Embedding Filtering only (no LLM re-ranker); (iv) Snippet Retrieval only (no embedding filter, no re-ranker); (v) Keyword Retrieval only.
>
> "To assess the contribution of each component in our novelty checker, we conducted ablation studies using 58 ideas (comprising 13 'not novel' instances from our test set and 45 NLP papers from the literature). For this experiment, we focus on the 'not novel' cases, since the ideas labeled novel in expert-labeled test data can vary with different retrieved paper sets." (Shahid et al., 2025, p. 6)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-4.png]]

### How?

> **Procedure:** four ablation variants were compared to the complete system. (i) **Complete System** — full pipeline with keyword + snippet retrieval (each returning top-k by Semantic Scholar's ranking), embedding filtering, and facet-based RankGPT re-ranking. (ii) **Relevance RankGPT** — same retrieval and embedding filtering, but the facet-based RankGPT re-ranker is swapped for a general-relevance RankGPT (Sun et al.); isolates the value of facet-based reranking. (iii) **Embedding Filtering** — drops the LLM re-ranker entirely; isolates the value of the LLM-reranker step. (iv) **Snippet Retrieval** — top-k from snippet API alone, no embedding filter, no LLM reranker. (v) **Keyword Retrieval** — top-k from keyword search alone. For Step 3 novelty evaluation the authors used **o3-mini**, and **gpt-4o** for Step 2 re-ranking. Outputs scored as accuracy of predicting "not novel" on the ablation set. A complementary analysis (Table 3) reports overlap of top-10 papers and average rank-shift vs. the complete system.
>
> "We use o3-mini for evaluating novelty (Step 3) and gpt-4o for re-ranking (Step 2)." (Shahid et al., 2025, p. 7)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p7-2.png]]

### Who?

> **Models:** novelty evaluator = **o3-mini** (OpenAI); re-ranker = **gpt-4o** (OpenAI); embedding model = **SPECTER-2**. No fine-tuning.
>
> **Idea sample-size flow:** **58 ideas** total = **13 "not novel" instances from the held-out test set** + **45 NLP papers from the literature** treated as already-published ideas (so they are by definition not novel and form a high-confidence ablation evaluation set). Novel cases were *excluded* from the ablation because their classification depends on which papers are retrieved.
>
> **No human evaluators** in the ablation loop; performance derived from automated comparison against the "not novel" gold class.
>
> "ablation studies using 58 ideas (comprising 13 'not novel' instances from our test set and 45 NLP papers from the literature)." (Shahid et al., 2025, p. 6)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-5.png]]

## Other Notes

- Without any re-ranking (keyword or snippet retrieval alone), accuracy collapses further: snippet 8.62%, keyword 5.17%.
- Top-10 paper overlap with the complete system: ~30% of papers differ when either embedding filtering or general-relevance RankGPT is used; without any re-ranker, overlap drops to <3 of 10 papers.
- The ablation thus shows **two layered contributions**: removing the LLM re-ranker (embedding-only) is far more harmful than swapping facet-based for general-relevance, indicating that retrieval-stage LLM re-ranking is the dominant performance driver and facet-awareness adds a smaller second-order gain.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@shahidLiteratureGroundedNoveltyAssessment2025#TRIPOD-LLM reporting summary]].

| Ablation condition | "Not novel" accuracy |
| --- | :---: |
| **Complete System** (facet-based RankGPT + embedding + retrieval) | **89.66%** |
| − Relevance RankGPT (general-relevance instead of facet-based) | 13.79% |
| − Embedding Filtering (no LLM re-ranker) | 10.34% |
| − Snippet Retrieval only | 8.62% |
| − Keyword Retrieval only | 5.17% |

| Top-10 overlap with complete system (Table 3) | Overlap (↑) | Rank shift (↓) |
| --- | :---: | :---: |
| Relevance RankGPT | 7.97 | 0.67 |
| Embedding Filtering | 7.93 | 0.84 |
| Snippet Retrieval | 2.88 | 1.85 |
| Keyword Retrieval | 1.17 | 1.39 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines]]

- [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]
- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]

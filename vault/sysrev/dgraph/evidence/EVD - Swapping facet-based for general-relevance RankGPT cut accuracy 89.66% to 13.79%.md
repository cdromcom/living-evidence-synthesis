---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - Swapping the facet-based RankGPT re-ranker for a general-relevance RankGPT dropped not-novel prediction accuracy from 89.66% to 13.79%"
tags:
  - task/novelty-assessment
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
updated: 2026-11-24
nodeID: 019ddb4e-6b85-7544-bc4e-40e88e0586c4
appraisal_overall: L0-M2-H3
tripod_llm_pct: 41pct
title: "Swapping the facet-based RankGPT re-ranker for a general-relevance RankGPT dropped not-novel prediction accuracy from 89.66% to 13.79%"
---

## Source

[[sysrev/dgraph/source/@shahidLiteratureGroundedNoveltyAssessment2025]]

## Description

> "Table 2 shows that the complete system, which employs facet-based re-ranking in RankGPT, significantly outperforms its ablated variants in accuracy." (Shahid et al., 2025, p. 102)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p7-1.png]]
> 
> Grounding table: Table 2, "Accuracy of predicting "not novel"." (Shahid et al., 2025, p. 102)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p7-table2.png]]
> Complete System: 89.66%; replacing the facet-based RankGPT with a general-relevance RankGPT ("- Relevance RankGPT"): 13.79%; embedding filtering only, with no LLM re-ranker ("- Embedding Filtering"): 10.34%; snippet retrieval only: 8.62%; keyword retrieval only: 5.17%. (Shahid et al., 2025, p. 102, Table 2)

## Methods Context

### What?

> **Study design:** ablation study within the Idea Novelty Checker pipeline (component-removal benchmark, focused on the "not novel" decision class).
>
> **Method type:** lesion experiments, each ablation removes or replaces a single retrieval/re-ranking stage and measures the resulting drop in not-novel-class accuracy.
>
> **Tools:** Idea Novelty Checker pipeline (Semantic Scholar Search API + Snippet API; SPECTER-2 embeddings; facet-based RankGPT re-ranker); novelty evaluator switched to **o3-mini** for this ablation; **gpt-4o** retained for re-ranking (Step 2).
>
> **Dependent variable:** accuracy of predicting "not novel" on the 58-item ablation set (single-class accuracy, not full binary classification metrics).
>
> **Independent variable:** ablation condition, (i) Complete System; (ii) Relevance RankGPT (general-relevance prompt instead of facet-based); (iii) Embedding Filtering only (no LLM re-ranker); (iv) Snippet Retrieval only (no embedding filter, no re-ranker); (v) Keyword Retrieval only.
>
> "To assess the contribution of each component in our novelty checker, we conducted ablation studies using 58 ideas (comprising 13 'not novel' instances from our test set and 45 NLP papers from the literature). For this experiment, we focus on the 'not novel' cases, since the ideas labeled novel in expert-labeled test data can vary with different retrieved paper sets." (Shahid et al., 2025, p. 101)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p6-5.png]]

### How?

> **Procedure:** four ablation variants were compared to the complete system. (i) **Complete System**, full pipeline with keyword + snippet retrieval (each returning top-k by Semantic Scholar's ranking), embedding filtering, and facet-based RankGPT re-ranking. (ii) **Relevance RankGPT**, same retrieval and embedding filtering, but the facet-based RankGPT re-ranker is swapped for a general-relevance RankGPT (Sun et al.); isolates the value of facet-based reranking. (iii) **Embedding Filtering**, drops the LLM re-ranker entirely; isolates the value of the LLM-reranker step. (iv) **Snippet Retrieval**: top-k from snippet API alone, no embedding filter, no LLM reranker. (v) **Keyword Retrieval**, top-k from keyword search alone. For Step 3 novelty evaluation the authors used **o3-mini**, and **gpt-4o** for Step 2 re-ranking. Outputs scored as accuracy of predicting "not novel" on the ablation set. A complementary analysis (Table 3) reports overlap of top-10 papers and average rank-shift vs. the complete system.
>
> "We use o3-mini for evaluating novelty (Step 3) and gpt-4o for re-ranking (Step 2)." (Shahid et al., 2025, p. 102)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p7-2.png]]

### Who?

> **Models:** novelty evaluator = **o3-mini** (OpenAI); re-ranker = **gpt-4o** (OpenAI); embedding model = **SPECTER-2**. No fine-tuning.
>
> **Idea sample-size flow:** **58 ideas** total = **13 "not novel" instances from the held-out test set** + **45 NLP papers from the literature** treated as already-published ideas (so they are by definition not novel and form a high-confidence ablation evaluation set). Novel cases were *excluded* from the ablation because their classification depends on which papers are retrieved.
>
> **No human evaluators** in the ablation loop; performance derived from automated comparison against the "not novel" gold class.
>
> "ablation studies using 58 ideas (comprising 13 'not novel' instances from our test set and 45 NLP papers from the literature)." (Shahid et al., 2025, p. 101)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p6-6.png]]

## Other Notes

- Without any re-ranking (keyword or snippet retrieval alone), accuracy collapses further: snippet 8.62%, keyword 5.17%.
- Top-10 paper overlap with the complete system: ~30% of papers differ when either embedding filtering or general-relevance RankGPT is used; without any re-ranker, overlap drops to <3 of 10 papers.
- Swapping facet-based for general-relevance RankGPT already drops accuracy from 89.66% to 13.79%, and removing the LLM re-ranker entirely (embedding-only) lowers it only slightly further to 10.34%, so the facet-based criterion, not LLM re-ranking as such, accounts for nearly all of the gain.
- PDF check 2026-11-24: title "Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79%" -> "Swapping the facet-based RankGPT re-ranker for a general-relevance RankGPT dropped not-novel prediction accuracy from 89.66% to 13.79%"; file renamed. 13.79% is the variant that keeps RankGPT with a general-relevance prompt; removing the LLM re-ranker entirely gives 10.34% (Table 2, p. 102; Section 6.2, pp. 101-102). The numbers did not change, the description of which condition they belong to did.
- PDF check 2026-11-24: Description line "removing RankGPT relevance re-ranker: 13.79%; removing embedding filtering: 10.34%" -> "replacing facet-based RankGPT with general-relevance RankGPT: 13.79%; embedding filtering only (no LLM re-ranker): 10.34%" (Table 2, p. 102).
- PDF check 2026-11-24: this bullet said removing the LLM re-ranker is "far more harmful" than swapping facet-based for general-relevance; the table shows the reverse (89.66% -> 13.79% for the swap, 13.79% -> 10.34% for removal) (Table 2, p. 102).
- PDF check 2026-11-24: moved from the arXiv v1 PDF to the SDP 2025 proceedings PDF; quotes cited p. 7 now carry printed pages 101 or 102 (PDF pp. 6 and 7); quote "Table 2 shows that..." and "We use o3-mini..." are on printed p. 102, the two "58 ideas" quotes on p. 101. Table 2 and Table 3 values re-read from the rendered pages; unchanged.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[sysrev/dgraph/source/@shahidLiteratureGroundedNoveltyAssessment2025#TRIPOD-LLM reporting]].

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

Grounding table: Table 3, "Comparing rank and overlap in retrieved papers with each variant to the complete system." (Shahid et al., 2025, p. 103)
![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p8-table3.png]]

## Caveats

> [!info] Caveats applying to this evidence

- [[sysrev/dgraph/caveats/CVT - LLM novelty evaluation is highly prompt-sensitive and hard to replicate|CVT - LLM novelty evaluation is highly sensitive to prompt variations making results difficult to replicate]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[sysrev/dgraph/claims/CLM - Expert in-context examples significantly improve LLM novelty classification|CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines]]

- [[sysrev/dgraph/claims/CLM - Facet-based re-ranking is critical for novelty evaluation|CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]

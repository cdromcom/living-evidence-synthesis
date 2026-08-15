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
nodeID: 019ddb4e-6b74-77dd-aeab-e1f16a191764
appraisal_overall: L0-M2-H3
tripod_llm_pct: 41pct
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

## Description

> "Our extensive experiments demonstrate that our novelty checker achieves approximately 13% higher agreement than existing approaches." (Shahid et al., 2025, p. 1)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p1-1.png]]
> Full results from Table 1: Complete system with idea, most relevant papers, class, and reasoning: Accuracy=0.81, Precision=0.84, Recall=0.78, F1=0.79, Cohen's Kappa=0.59. (Shahid et al., 2025, p. 7)
> [Screenshot: Table 1, p. 7 — experimental results using gpt-4o on expert-annotated dataset]

## Methods Context

### What?

> **Study design:** few-shot LLM evaluation against an expert-annotated novelty-classification corpus (within-paper held-out test split). **Method type:** retrieval-augmented generation (RAG) with two-stage retrieve-then-rerank, plus 15-shot in-context learning for the final novelty classifier. **Tools:** Semantic Scholar Search API + Snippet API for candidate retrieval; SPECTER-2 (Cohan et al.) embeddings for similarity filtering; RankGPT (Sun et al.) for facet-based LLM re-ranking; GPT-4o ("gpt-4o", inference Aug–Sep 2024) for keyword extraction (LLM_query), re-ranking (LLM_rankgpt), and novelty evaluation (LLM_novelty); brat-style expert annotation. **Dependent variables:** binary novelty classification metrics on a 32-idea test set — accuracy, precision, recall, F1, and Cohen's κ vs. expert labels. **Independent variables / covariates:** prompting strategy (zero-shot, DSPy, TextGRAD, OpenReview-derived in-context examples, expert-labeled in-context examples); presence/absence of "most relevant papers", "class" label, and "reasoning" in the in-context examples; number of in-context examples (n_examples; best = 15).
>
> "We evaluated multiple baselines to benchmark our novelty assessment approach. First, we employed a zero-shot prompt as a straightforward baseline, and further refined this manually written prompt using Anthropic's prompt generator. We also applied popular prompt optimization techniques such as DSPy (Khattab et al.) and TextGRAD (Yuksekgonul et al.), which optimize the prompt instructions using a train/validation split created from formative study data." (Shahid et al., 2025, p. 5)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p5-2.png]]

### How?

> **Procedure:** (1) **Step 1 — Candidate retrieval.** Prompt LLM_query (gpt-4o) to extract keywords + potential titles from the input idea; query Semantic Scholar Search API for keyword/title hits and Snippet API (~500-word snippets) using the entire idea as input. Optionally retrieve papers similar to user-provided seed papers via Semantic Scholar's recommendations API. Combine all retrieved papers into a candidate pool. (2) **Step 2 — Two-stage re-ranking.** Embedding filtering with SPECTER-2 selects the top N=100 candidates by cosine similarity to the idea embedding; RankGPT (LLM_rankgpt = gpt-4o) then re-ranks using a *facet-based* relevance criterion (purpose, mechanism, evaluation, application — favoring papers matching all key facets, then those matching application+purpose, then partial matches), producing top k=10 most relevant papers. (3) **Step 3 — Novelty evaluation.** LLM_novelty (gpt-4o) is prompted with the idea, the top-10 papers, and 15 expert-labeled in-context examples (idea + top-10 papers + class + reasoning) drawn from the formative-study training split; output is a binary {novel, not novel} label with reasoning. The 15 idea-paper pairs and the 5-pair OpenReview-baseline configuration were chosen via a random seed (=100); DSPy used 2 bootstrapped examples and DSPy/TextGRAD were each trained for 12 prompt iterations.
>
> "For our novelty evaluation system, we use SPECTER-2 (Cohan et al.) as the default embedding model. Initially, we retrieve the top N =100 papers using these embeddings, from which the top k =10 most relevant papers are selected for comparison with the input idea. The default language model for the idea keyword extraction (LLMquery), re-ranking process (LLMrankgpt), and novelty evaluation (LLMnovelty) is gpt-4o. Expert-labeled data from the formative study is incorporated as in-context examples in the novelty checker. We experimented with various numbers of in-context examples (comprising idea-paper pairs along with their novelty class and reviews) and found that the best performance was achieved using 15 idea examples (random seed 100)." (Shahid et al., 2025, p. 6)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-3.png]]

### Who?

> **Models:** OpenAI **gpt-4o** (closed-source; "We used the model 'gpt-4o' during August and September 2024"; training corpus and cutoff not disclosed) used for all three LLM roles (LLM_query, LLM_rankgpt, LLM_novelty). Embedding model: **SPECTER-2** (Cohan et al.). Comparison systems on the same test set / fixed top-10 papers: AI Scientist (Lu et al.) and AI Researcher (Si et al., evaluated with gpt-4o and Claude-3.5-Sonnet).
>
> **Idea-corpus sample-size flow:** formative-study pool of **51 ideas** (34 generated by Scideator (Radensky et al.); 17 from accepted/rejected OpenReview ICLR'22 + NeurIPS'23 submissions) → reannotated under a controlled "novel/moderately novel/not novel" framework, then re-collapsed to binary {novel, not novel} → **67 consensus-labeled examples** (39 novel, 28 non-novel) collected from the formative study (after second-round binary reannotation) → balanced train/test split: **35 training / 32 testing** ideas.
>
> **In-context example pools (separate from main test set):** ~8,156 OpenReview ICLR/NeurIPS submissions filtered for ones discussing idea novelty → 20 idea-review pairs randomly sampled for the OpenReview baseline (5 pairs used in best OpenReview setup).
>
> **Expert annotators (provided gold labels + reasoning):** the first and second authors of the paper (no panel of external raters); they reannotated the 51 ideas in the second round and labeled the 67 consensus examples that constitute training + test data.
>
> **No human evaluators in the test loop**; classifier outputs scored against the gold expert labels.
>
> "From our formative study, we collected 67 consensus-labeled examples (39 labeled as novel and 28 as non-novel). We split into training and test sets (35 for training and 32 for testing) with a balanced distribution of novel and non-novel ideas." (Shahid et al., 2025, p. 5)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p5-3.png]]

## Other Notes

- Best configuration used idea + most relevant papers + class + reasoning as context (the full row in Table 1).
- OpenReview-based examples performed worse than expert-labeled examples even when relevant papers were also included.
- Test agreement was reported with **two-way Cohen's κ** (only for the in-context settings); other rows show only accuracy/precision/recall/F1.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@shahidLiteratureGroundedNoveltyAssessment2025#TRIPOD-LLM reporting summary]].

| Setting | Accuracy | Precision | Recall | F1 | Cohen's κ |
| --- | :---: | :---: | :---: | :---: | :---: |
| Zero-shot (baseline) | 0.68 | 0.76 | 0.64 | 0.65 | — |
| Zero-shot + Anthropic prompt-generator | 0.68 | 0.70 | 0.64 | 0.64 | — |
| DSPy (idea + papers + class) | 0.68 | 0.83 | 0.62 | 0.58 | — |
| DSPy (idea + papers + class + reasoning) | 0.66 | 0.82 | 0.58 | 0.52 | — |
| TextGRAD (idea + papers + class) | 0.78 | 0.76 | 0.76 | 0.76 | — |
| OpenReview examples (idea + review) | 0.59 | 0.55 | 0.51 | 0.43 | — |
| Expert-labeled (idea + reasoning) | 0.75 | 0.76 | 0.77 | 0.75 | — |
| Expert-labeled (idea + papers + class) | 0.78 | 0.77 | 0.76 | 0.77 | — |
| **Expert-labeled (idea + papers + class + reasoning) — Idea Novelty Checker** | **0.81** | **0.84** | **0.78** | **0.79** | **0.59** |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - LLM novelty evaluation is highly sensitive to prompt variations making results difficult to replicate]]

- [[CVT - Same expert annotators who labeled training examples also classified test ideas introducing potential circularity]]

- [[CVT - Shahid et al. novelty evaluation used only 67 consensus-labeled examples with a test set of 32 ideas]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines]]

- [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]

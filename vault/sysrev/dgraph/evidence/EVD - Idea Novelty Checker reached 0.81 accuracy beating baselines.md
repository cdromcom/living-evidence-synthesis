---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset"
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
  - forensic/f1-check/consistent
  - forensic/kappa-check/in-bounds
created: 2026-04-17
updated: 2026-11-24
nodeID: 019ddb4e-6b74-77dd-aeab-e1f16a191764
appraisal_overall: L0-M2-H3
tripod_llm_pct: 41pct
title: "Idea Novelty Checker achieved accuracy 0.81 F1 0.79 Cohen kappa 0.59 outperforming baselines on expert-annotated dataset"
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

## Description

> "Our extensive experiments demonstrate that our novelty checker achieves approximately 13% higher agreement than existing approaches." (Shahid et al., 2025, p. 96)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p1-1.png]]
> 
> Grounding table: Table 1, "Experimental Results using gpt-4o on expert-annotated dataset." (Shahid et al., 2025, p. 102)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p7-table1.png]]
> Full results from Table 1: Complete system with idea, most relevant papers, class, and reasoning: Accuracy=0.81, Precision=0.84, Recall=0.78, F1=0.79, Cohen's Kappa=0.59. (Shahid et al., 2025, p. 102, Table 1)

## Methods Context

### What?

> **Study design:** few-shot LLM evaluation against an expert-annotated novelty-classification corpus (within-paper held-out test split).
>
> **Method type:** retrieval-augmented generation (RAG) with two-stage retrieve-then-rerank, plus 15-shot in-context learning for the final novelty classifier.
>
> **Tools:** Semantic Scholar Search API + Snippet API for candidate retrieval; SPECTER-2 (Cohan et al.) embeddings for similarity filtering; RankGPT (Sun et al.) for facet-based LLM re-ranking; GPT-4o ("gpt-4o", inference Aug–Sep 2024) for keyword extraction (LLM_query), re-ranking (LLM_rankgpt), and novelty evaluation (LLM_novelty).
>
> **Dependent variables:** binary novelty classification metrics on a 32-idea test set, accuracy, precision, recall, F1, and Cohen's κ vs. expert labels.
>
> **Independent variables / covariates:** prompting strategy (zero-shot, DSPy, TextGRAD, OpenReview-derived in-context examples, expert-labeled in-context examples); presence/absence of "most relevant papers", "class" label, and "reasoning" in the in-context examples; number of in-context examples (n_examples; best = 15).
>
> "We evaluated multiple baselines to benchmark our novelty assessment approach. First, we employed a zero-shot prompt as a straightforward baseline, and further refined this manually written prompt using Anthropic's prompt generator. We also applied popular prompt optimization techniques such as DSPy (Khattab et al., 2023) and TextGRAD (Yuksekgonul et al., 2024), which optimize the prompt instructions using a train/validation split created from formative study examples." (Shahid et al., 2025, p. 100)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p5-1.png]]

### How?

> **Procedure:** (1) **Step 1, Candidate retrieval.** Prompt LLM_query (gpt-4o) to extract keywords + potential titles from the input idea; query Semantic Scholar Search API for keyword/title hits and Snippet API (~500-word snippets) using the entire idea as input. Optionally retrieve papers similar to user-provided seed papers via Semantic Scholar's recommendations API. Combine all retrieved papers into a candidate pool. (2) **Step 2, Two-stage re-ranking.** Embedding filtering with SPECTER-2 selects the top N=100 candidates by cosine similarity to the idea embedding; RankGPT (LLM_rankgpt = gpt-4o) then re-ranks using a *facet-based* relevance criterion (purpose, mechanism, evaluation, application, favoring papers matching all key facets, then those matching application+purpose, then partial matches), producing top k=10 most relevant papers. (3) **Step 3, Novelty evaluation.** LLM_novelty (gpt-4o) is prompted with the idea, the top-10 papers, and 15 expert-labeled in-context examples (idea + top-10 papers + class + reasoning) drawn from the formative-study training split; output is a binary {novel, not novel} label with reasoning. The 15 idea-paper pairs were chosen via a random seed (=100) and the best OpenReview baseline used 5 idea-review pairs; DSPy used 2 bootstrapped examples and DSPy/TextGRAD were each trained for 12 prompt iterations.
>
> "For our novelty evaluation system, we use SPECTER-2 (Cohan et al., 2020) as the default embedding model. Initially, we retrieve the top N =100 papers using these embeddings, from which the top k =10 most relevant papers are selected for comparison with the input idea. The default language model for the idea keyword extraction (LLMquery), re-ranking process (LLMrankgpt), and novelty evaluation (LLMnovelty) is gpt-4o. Expert-labeled data from the formative study is incorporated as in-context examples in the novelty checker. We experimented with various numbers of in-context examples (comprising idea-paper pairs along with their novelty class and reviews) and found that the best performance was achieved using 15 idea examples (random seed 100)." (Shahid et al., 2025, p. 101)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p6-4.png]]

### Who?

> **Models:** OpenAI **gpt-4o** (closed-source; "We used the model 'gpt-4o' during August and September 2024"; training corpus and cutoff not disclosed) used for all three LLM roles (LLM_query, LLM_rankgpt, LLM_novelty). Embedding model: **SPECTER-2** (Cohan et al.). Comparison systems on the same test set / fixed top-10 papers: AI Scientist (Lu et al.) and AI Researcher (Si et al., evaluated with gpt-4o and Claude-3.5-Sonnet).
>
> **Idea-corpus sample-size flow:** formative-study pool of **51 ideas** (34 new ideas generated by Scideator (Radensky et al.); 17 carried over from the first-round study, which had used 46 Scideator + 5 OpenReview ICLR'22/NeurIPS'23 ideas) → reannotated under a controlled "novel/moderately novel/not novel" framework, then re-collapsed to binary {novel, not novel} → **67 consensus-labeled examples** (39 novel, 28 non-novel) collected from the formative study (after second-round binary reannotation) → balanced train/test split: **35 training / 32 testing** ideas.
>
> **In-context example pools (separate from main test set):** ~8,156 OpenReview ICLR/NeurIPS submissions filtered for ones discussing idea novelty → 20 idea-review pairs randomly sampled for the OpenReview baseline (5 pairs used in best OpenReview setup).
>
> **Expert annotators (provided gold labels + reasoning):** the first and second authors of the paper (no panel of external raters); they reannotated the 51 ideas in the second round and labeled the 67 consensus examples that constitute training + test data.
>
> **No human evaluators in the test loop**; classifier outputs scored against the gold expert labels.
>
> "From our formative study, we collected 67 consensus-labeled examples (39 labeled as novel and 28 as non-novel). We split into training and test sets (35 for training and 32 for testing) with a balanced distribution of novel and non-novel ideas." (Shahid et al., 2025, p. 100)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-sdp-evd-p5-2.png]]

## Other Notes

- Best configuration used idea + most relevant papers + class + reasoning as context (the full row in Table 1).
- OpenReview-based examples (accuracy 0.59) performed worse than expert-labeled examples even when relevant papers were excluded from the expert examples (idea + reasoning, accuracy 0.75).
- Cohen's κ was reported only for the best expert-labeled row (0.59) and the two external novelty checkers (AI Scientist, AI Researcher); all other rows show only accuracy/precision/recall/F1.

- PDF check 2026-11-24: moved from the arXiv v1 PDF to the SDP 2025 proceedings PDF (printed pp. 96-113); every citation now uses the printed page.
- PDF check 2026-11-24: baselines quote "formative study data" -> "formative study examples" (Section 5, p. 100); it also now carries the new citation years (Khattab et al., 2023; Yuksekgonul et al., 2024).
- PDF check 2026-11-24: SPECTER-2 quote now reads "(Cohan et al., 2020)" (p. 101); the footnote marker 7 after "gpt-4o" is left out of the quote.
- PDF check 2026-11-24: formative-study pool "34 generated by Scideator; 17 from OpenReview ICLR'22 + NeurIPS'23" -> "34 new Scideator ideas; 17 carried over from the first-round study (46 Scideator + 5 OpenReview)" (Section 3, p. 98).
- PDF check 2026-11-24: "15 idea-paper pairs and the 5-pair OpenReview-baseline configuration were chosen via a random seed (=100)" -> seed applies only to the 15 expert examples; the best OpenReview setup used 5 idea-review pairs (p. 101).
- PDF check 2026-11-24: "two-way Cohen's κ (only for the in-context settings)" -> kappa is given only for the best expert row (0.59), AI Scientist and AI Researcher; "two-way" is not stated (Table 1, p. 102).
- PDF check 2026-11-24: OpenReview examples performed worse "even when relevant papers were also included" -> "even when relevant papers were excluded from the expert examples" (Section 6.1, p. 101; Table 1: 0.59 vs 0.75).
- PDF check 2026-11-24: removed "brat-style expert annotation" from Tools; neither version of the paper mentions brat.
- PDF check 2026-11-24: the screenshot labelled "Table 1, p. 7" showed the abstract sentence on p. 1, not the table; replaced by a crop of Table 1 (p. 102). All nine rows of the table below match Table 1; no number changed.

> [!info] TRIPOD-LLM item 17

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
| **Expert-labeled (idea + papers + class + reasoning), Idea Novelty Checker** | **0.81** | **0.84** | **0.78** | **0.79** | **0.59** |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - LLM novelty evaluation is highly prompt-sensitive and hard to replicate|CVT - LLM novelty evaluation is highly sensitive to prompt variations making results difficult to replicate]]

- [[CVT - Same annotators labeled training and test ideas introducing potential circularity|CVT - Same expert annotators who labeled training examples also classified test ideas introducing potential circularity]]

- [[CVT - Shahid et al. used only 67 labeled examples and 32 test ideas|CVT - Shahid et al. novelty evaluation used only 67 consensus-labeled examples with a test set of 32 ideas]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Expert in-context examples significantly improve LLM novelty classification|CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines]]

- [[CLM - Facet-based re-ranking is critical for novelty evaluation|CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]]

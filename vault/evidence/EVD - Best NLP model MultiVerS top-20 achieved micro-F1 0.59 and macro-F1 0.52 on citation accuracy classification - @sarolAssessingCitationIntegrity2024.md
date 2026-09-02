---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/citation-integrity-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L2-M2-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/73pct
  - 5c/connectivity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b57-768e-af9b-1285c4a1158c
appraisal_overall: L2-M2-H1
tripod_llm_pct: 73pct
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

## Description

> "The best performing model—which uses citation sentences as citation context, the BM25 model with MonoT5 reranker for retrieving top-20 sentences, and a fine-tuned MultiVerS model for accuracy label classification—yielded 0.59 micro-F1 and 0.52 macro-F1 score." (Sarol et al., 2024, p. 1)
> ![[sarolAssessingCitationIntegrity2024-evd-p1-1.png]]
>
> Grounding table (Table 4, p. 6): per-class F1 across MultiVerS variants and in-context learning baselines.
>
> ![[sarolAssessingCitationIntegrity2024-tables-p6-6.png]]

## Methods Context

### What?

> **Study design:** NLP model benchmark on the Sarol annotated corpus (within-paper held-out evaluation).
>
> **Method type:** supervised fine-tuning of a claim-verification model with retrieval-augmented evidence selection.
>
> **Tools:** MultiVerS (Wadden et al. 2022), a Longformer-based (Beltagy et al. 2020) claim-verification model, initially fine-tuned on HealthVER (Sarrouti et al. 2021) and then on the Sarol training split; BM25 (Robertson & Zaragoza 2009) for first-pass sentence retrieval; MonoT5 (Nogueira et al. 2020) reranker; PubMedBERT (Gu et al. 2021) for the citation-context baseline.
>
> **Dependent variables:** per-class F1 (ACCURATE / NOT_ACCURATE / IRRELEVANT), micro-F1, macro-F1; sentence-retrieval Recall@{1,5,10,20} and MRR.
>
> **Independent variables:** evidence-retrieval condition (title+abstract baseline, top-5, top-10, top-20, top-20 + annotated evidence, oracle gold-evidence, oracle gold-context+evidence); citance vs. fine-tuned PubMedBERT for citation-context selection; query type for retrieval (citance only / gold context / gold context + intervening sentences).
>
> "We report standard evaluation metrics, precision, recall, and their harmonic mean, F1 score, for citation context identification and accuracy classification tasks. For citation accuracy classification, we report both micro- and macro-averaged results. We assess whether the performance differences between the baseline MultiVerS model and the other models are statistically significant using McNemar's test." (Sarol et al., 2024, p. 5)
> ![[sarolAssessingCitationIntegrity2024-evd-p5-2.png]]

### How?

> **Procedure:** (1) Citation-context selection, citance is used directly (PubMedBERT fine-tuned for sentence-level binary context classification did not beat this baseline). (2) Evidence-sentence retrieval, BM25 retrieves the top 60 sentences from the reference article, MonoT5 reranks them, and the top-k (k=5/10/20) become the evidence input. (3) Accuracy classification, citance + evidence sentences fed into MultiVerS via Longformer encoder; three-way classification head (ACC / N_ACC / IRR) trained on Sarol training split after the HealthVER fine-tuning warm-start. The rationale-sentence classifier inherited from MultiVerS was disabled by setting its loss weight to 0 (preliminary experiments showed it hurt performance). Significance vs. baseline tested with McNemar's test.
>
> "we leveraged a state-of-the-art claim verification model, MultiVerS (Wadden et al. 2022). For our baseline experiments, we used our training set to fine-tune the MultiVerS model trained on HealthVER (Sarrouti et al. 2021)." (Sarol et al., 2024, p. 4)
> ![[sarolAssessingCitationIntegrity2024-evd-p4-1.png]]

### Who?

> **Models (sample of conditions evaluated):** MultiVerS-baseline (title+abstract evidence); MultiVerS-top-5 / -top-10 / -top-20 (BM25+MonoT5 retrieved); MultiVerS-top-20+annotated evidence (training-only augmentation); two oracles, gold-evidence and gold-context+gold-evidence; baseline citance-only context vs. fine-tuned PubMedBERT context. Comparison models in the same table: GPT-3.5-turbo-0613 and GPT-4 (in-context learning, top-5 evidence).
>
> **Evaluation data flow:** 100 PMC-OA reference articles → 3063 annotated citation instances → split into training and held-out evaluation sets (split sizes not reported in main text). Same corpus and label space as EVDs on prevalence and IAA.
>
> **No human evaluators** for this EVD; performance derived from automated comparison against gold annotations.
>
> "We collected 100 highly-cited research articles available in full text from the PubMed Central Open Access Subset (PMC-OA) to form our reference article set." (Sarol et al., 2024, p. 2)
> ![[sarolAssessingCitationIntegrity2024-evd-p2-2.png]]

## Other Notes

- Differences across MultiVerS retrieval conditions were not statistically significant from the title+abstract baseline. Difference between best MultiVerS (top-20) and GPT-4 was significant (McNemar p≤.05).
- Oracle conditions show the ceiling: gold context + gold evidence reached 0.75/0.78 (micro/macro-F1), illustrating how much further evidence-retrieval improvements could plausibly push the supervised pipeline.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sarolAssessingCitationIntegrity2024#TRIPOD-LLM reporting summary]].

| Condition | Micro-F1 | Macro-F1 | ACC F1 | N_ACC F1 | IRR F1 |
| --- | :---: | :---: | :---: | :---: | :---: |
| MultiVerS title+abstract (baseline) | 0.56 | 0.43 | 0.69 | 0.38 | 0.20 |
| MultiVerS top-5 | 0.58 | 0.50 | 0.69 | 0.43 | 0.37 |
| MultiVerS top-10 | 0.56 | 0.48 | 0.67 | 0.41 | 0.36 |
| **MultiVerS top-20 (best)** | **0.59** | **0.52** | **0.69** | **0.43** | **0.42** |
| MultiVerS top-20 + annotated evidence | 0.58 | 0.50 | 0.69 | 0.43 | 0.38 |
| Oracle (gold evidence) | 0.73 | 0.75 | 0.79 | 0.52 | 0.93 |
| Oracle (gold context + gold evidence) | 0.75 | 0.78 | 0.80 | 0.57 | 0.96 |

| Sub-task | Result |
| --- | --- |
| Citation-context classification | citance baseline F1 0.94 vs. fine-tuned PubMedBERT 0.93 |
| Sentence retrieval (BM25+MonoT5) | Recall@1=0.09–0.10; @5=0.28–0.31; @10=0.40–0.44; @20=0.53–0.55; MRR 0.31–0.33 |
| Significance | MultiVerS variants vs. baseline: n.s. Best MultiVerS vs. GPT-4: McNemar p≤.05. |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Sarol et al. excluded citation cases where evidence appeared in tables figures or supplementary material]]
- [[CVT - Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]]

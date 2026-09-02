---
NodeFormality: draft
aliases:
tags:
  - task/novelty-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L1-M2-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/53pct
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b82-7339-9492-c7dab0dc5415
appraisal_overall: L1-M2-H2
tripod_llm_pct: 53pct
---

## Source

[[@wuAutomatedNoveltyEvaluationa]]

## Description

> "As shown in Table 2, the model based on SciBERT performs the best, while other models also demonstrate relative competitiveness. Compared to the baseline models, our proposed method exhibits the best performance, indicating its effectiveness in integrating human knowledge and knowledge from LLMs." (Wu et al., 2024, p. 1462)
>
> ![[wuAutomatedNoveltyEvaluationa-evd-p11-1.png]]
> The Ours-SciBERT model with HK and LLMK inputs achieved F1=0.83 and Accuracy=0.84 (Table 2, p. 1461).
>
> ![[wuAutomatedNoveltyEvaluationa-results-p10-1.png]]

## Methods Context

### What?

> **Study design:** Cross-sectional supervised-learning benchmark on the authors' newly constructed ICLR 2022 method-novelty corpus, framed as a binary classification task (Method Novelty Prediction, MNP).
>
> **Method type:** Knowledge-fusion model combining a fine-tuned PLM text encoder with a knowledge-guided sparse-attention module that integrates human peer-review sentences and LLM-generated method summaries.
>
> **Tools:** SciBERT text encoder (Beltagy et al. 2019); ChatGPT (gpt-3.5-turbo, temperature 0, default parameters) for LLM-generated method summaries (LLMK); aspect annotation model from Yuan et al. (2022) for extracting novelty-related sentences (HK) from review reports; Sparsemax-based Sparse-Attention layer (Martins & Astudillo 2016); Self-Attention Reduction (SAR) prediction head; Adam optimizer (Kingma & Ba 2014); GROBID and S2ORC parsing tools for PDF-to-text extraction; V100 / RTX 4090 GPU. Baselines: BERT, RoBERTa, SciBERT, XLNet, ALBERT, plus zero-shot LLMs (LLaMA-3.1-8B, ChatGPT, GPT-4o, Claude-3.5-sonnet).
>
> **Dependent variables:** Weighted F1 and Accuracy on the test split.
>
> **Independent variables:** Input combination ({HK + Method Text}, {HK + LLMK}, individual {HK / MT / LLMK}); model class (proposed Ours-* knowledge-fusion vs. baseline PLM/LLM); PLM backbone (BERT / RoBERTa / SciBERT / XLNet / ALBERT).
>
> "We adopt Accuracy and Weighted F1 as the evaluation metrics for our dataset to evaluate the performance of the model." (Wu et al., 2024, p. 1460)
> ![[wuAutomatedNoveltyEvaluationa-evd-p9-1.png]]

### How?

> **Procedure:** (1) Collected 3,376 ICLR 2022 papers + peer reviews from OpenReview via custom web crawler; parsed PDFs with GROBID/S2ORC; manually-defined rules used to extract title and methodology section. (2) Aggregated TNS scores from 3-5 reviewers by averaging; excluded papers where max-min reviewer disagreement exceeded 1, yielding 2,432 final instances. Mapped TNS=1-2 to Low Novelty and TNS=3-4 to High Novelty. (3) Constructed Human Knowledge (HK) inputs by running an aspect annotation model (Yuan et al. 2022) on review reports to extract sentences tagged with the novelty aspect. (4) Constructed LLM Knowledge (LLMK) by prompting ChatGPT (gpt-3.5-turbo, temperature 0) with the paper title + extracted method section to produce a novelty evaluation/summary capped at 200 words; one pass per paper. (5) Encoded HK and LLMK with a shared PLM backbone; passed Method features through self-attention; combined with HK features through Sparse-Attention to produce knowledge-guided review features; applied Self-Attention Reduction + Feed Forward + FC + Softmax to predict Low/High Novelty. Trained with negative sampling (5 negatives per instance), batch size 16, learning rate 1e-5, dropout 0.2, 12 self-attention heads / 6 sparse-attention heads, sparse dimension 128. (6) Best test-set checkpoint reported. LLMs evaluated zero-shot, averaged over three runs.
>
> "We split our dataset by a ratio of 8:1:1 for training, validation, and testing. Number of Self Attention head and Sparse Attention head is 12 and 6. The sparse dimension is set as 128. The dropout is set as 0.2. We adopt Accuracy and Weighted F1 as the evaluation metrics for our dataset to evaluate the performance of the model." (Wu et al., 2024, p. 1460)
> ![[wuAutomatedNoveltyEvaluationa-evd-p9-2.png]]

### Who?

> **Models / participants:** Five PLM baselines (BERT, RoBERTa, SciBERT, XLNet, ALBERT) and four zero-shot LLMs (LLaMA-3.1-8B, ChatGPT gpt-3.5-turbo-0125, GPT-4o, Claude-3.5-sonnet-all) evaluated against the proposed Ours-{BERT, RoBERTa, SciBERT, XLNet, ALBERT} knowledge-fusion variants.
>
> **Sample-size flow:** 3,376 ICLR 2022 papers crawled from OpenReview → after rule-based methodology-section extraction and TNS-score aggregation → 2,432 instances retained (papers with reviewer TNS disagreement >1 were removed). Class distribution by TNS: TNS=1 (n=51), TNS=2 (n=1,374), TNS=3 (n=936), TNS=4 (n=71); collapsed to Low Novelty (TNS 1-2; n=1,425) vs. High Novelty (TNS 3-4; n=1,007). Split 8:1:1 → train ≈ 1,945 / val ≈ 243 / test ≈ 244. No human evaluators in this EVD; reported numbers are the F1/Accuracy of Ours-SciBERT with HK+LLMK inputs on the held-out test set.
>
> "Following all the aforementioned preprocessing steps, the final dataset consists of 2432 instances." (Wu et al., 2024, p. 1458)
> ![[wuAutomatedNoveltyEvaluationa-evd-p7-1.png]]

## Other Notes

- Ours-SciBERT (HK+LLMK) is the top model in Table 2; it beats both the strongest PLM baseline (SciBERT with HK+LLMK: F1 0.73 / Acc 0.74) and the strongest zero-shot LLM (GPT-4o with HK+LLMK: F1 0.68 / Acc 0.68).
- LLaMA-3.1 was the only LLM whose performance improved when moving from HK+MT to HK+LLMK; other LLMs declined or stayed flat, suggesting LLM-summarized inputs help only smaller-parameter PLMs.
- ALBERT showed the largest absolute gain from the knowledge-fusion framework (0.52 → 0.76 F1 with the Ours-ALBERT variant).

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@wuAutomatedNoveltyEvaluationa#TRIPOD-LLM reporting summary]].

| Model (HK + LLMK input) | Weighted F1 | Accuracy |
| --- | :---: | :---: |
| **Ours-SciBERT (best)** | **0.83** | **0.84** |
| Ours-BERT | 0.81 | 0.82 |
| Ours-RoBERTa | 0.78 | 0.79 |
| Ours-XLNet | 0.78 | 0.79 |
| Ours-ALBERT | 0.76 | 0.77 |
| SciBERT (PLM baseline, HK+LLMK) | 0.73 | 0.74 |
| BERT (PLM baseline, HK+LLMK) | 0.72 | 0.72 |
| GPT-4o (zero-shot, HK+LLMK) | 0.68 | 0.68 |
| Claude-3.5 (zero-shot, HK+LLMK) | 0.69 | 0.68 |
| ChatGPT (zero-shot, HK+LLMK) | 0.59 | 0.60 |
| LLaMA-3.1 (zero-shot, HK+LLMK) | 0.44 | 0.50 |

| Sub-task | Result |
| --- | --- |
| Best PLM with HK+MT (no LLMK) | GPT-4o-style: SciBERT F1 0.70 / Acc 0.71; GPT-4o F1 0.73 / Acc 0.73 |
| Best individual input: HK alone | SciBERT F1 0.71 / Acc 0.71 (best PLM); Claude F1 0.69 / Acc 0.69 |
| Best individual input: MT or LLMK alone | All models F1 ≤ 0.56: single inputs are far weaker than HK+LLMK fusion |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - LLMs were evaluated only under zero-shot conditions without prompt optimization or fine-tuning for novelty assessment]]

- [[CVT - The novelty prediction dataset was limited to ICLR machine learning conference papers restricting generalizability to other academic domains]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Combining human reviewer knowledge with LLM-generated method summaries improves automated novelty prediction beyond either source alone]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Human-AI collaboration outperforms either alone on structured appraisal tasks]]
- [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]]

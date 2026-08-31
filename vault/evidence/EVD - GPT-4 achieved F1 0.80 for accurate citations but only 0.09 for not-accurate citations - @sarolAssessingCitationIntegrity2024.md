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
nodeID: 019ddb4e-6b6b-7574-8bfa-47e8de80ab79
appraisal_overall: L2-M2-H1
tripod_llm_pct: 73pct
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

## Description

> "In-context learning outperforms MultiVerS models in predicting ACCURATE citations. GPT-4 has a strong performance with 0.80 F1 score and 0.90 recall. However, these models perform poorly on the NOT_ACCURATE category, identifying only a few cases of this category leading to very low recall and F1." (Sarol et al., 2024, p. 6)
> ![[sarolAssessingCitationIntegrity2024-evd-p6-1.png]]
>
> Grounding table (Table 4, p. 6): GPT-3.5-turbo and GPT-4 rows show F1 per class.
>
> ![[sarolAssessingCitationIntegrity2024-tables-p6-6.png]]

## Methods Context

### What?

> **Study design:** few-shot LLM evaluation against the Sarol annotated corpus (no model training).
>
> **Method type:** 4-shot in-context learning with explicit chain-of-thought reasoning request.
>
> **Tools:** OpenAI GPT-3.5-turbo-0613 and GPT-4 (closed-source, API access); same BM25+MonoT5 retrieval pipeline used to supply evidence sentences.
>
> **Dependent variables:** per-class F1 (ACCURATE / NOT_ACCURATE / IRRELEVANT), micro-F1, macro-F1; per-class recall (notably 0.90 ACCURATE recall for GPT-4).
>
> **Independent variables:** model identity (GPT-3.5-turbo-0613 vs. GPT-4); evaluation under a fixed 4-shot prompt template (no prompt-engineering search reported in main text).
>
> "Generative large language models (LLMs) have been shown to be competitive for various NLP tasks when the task is specified by a natural language instruction (i.e. prompt) along with a few examples of the task (in-context learning) (Brown et al. 2020). Prompting the model to reason about the steps to arrive at a conclusion is shown to further improve performance for complex reasoning tasks (Wei et al. 2022). We evaluated two LLMs from OpenAI (GPT-3.5-turbo-0613 and GPT-4) for citation accuracy classification." (Sarol et al., 2024, p. 4)
> ![[sarolAssessingCitationIntegrity2024-evd-p4-2.png]]

### How?

> **Procedure:** for each test citation, build a prompt = (a) detailed task instruction, (b) descriptions of the three classes (ACC / N_ACC / IRR), (c) **four demonstrations** drawn from the Sarol training set — one ACC, one IRR, and two N_ACC (the harder, rarer class), (d) the test case. XML-like tags + markdown delimiters separate prompt sections. The model is asked to return both a predicted label and a free-text reasoning. Evidence input is the **top-5 BM25+MonoT5 retrieved sentences** (top-20 used for MultiVerS was prohibitive at GPT cost). All API calls executed February 2024. McNemar's test compared GPT models to the MultiVerS baseline.
>
> "The prompt consists of a detailed task instruction along with descriptions of three classes, which is followed by four demonstrations selected from the training set (one each for ACCURATE and IRRELEVANT, and two for NOT_ACCURATE). The test case follows the demonstrations. XML-like tags and markdown elements are used to differentiate between the different parts of the prompt. The prompt template and an example are provided in the Supplementary Material. The models were evaluated in February, 2024." (Sarol et al., 2024, p. 5)
> ![[sarolAssessingCitationIntegrity2024-evd-p5-3.png]]

### Who?

> **Models:** OpenAI **GPT-3.5-turbo-0613** and **GPT-4** (closed-source; training corpora and dates undisclosed; the Feb-2024 inference timestamp is the only date the authors report). No fine-tuning of either GPT model in the main analysis. (Supplementary experiments included a GPT-3.5-turbo fine-tuning run with mixed results.)
>
> **Evaluation data flow:** same 100-reference / 3063-citation Sarol corpus → train/test split → held-out test citations evaluated with both GPT models against the same 3-class label space used for MultiVerS.
>
> **No human evaluators** for this EVD; performance computed against gold human annotations.
>
> "We evaluated two LLMs from OpenAI (GPT-3.5-turbo-0613 and GPT-4) for citation accuracy classification." (Sarol et al., 2024, p. 4)
> ![[sarolAssessingCitationIntegrity2024-evd-p4-3.png]]

## Other Notes

- GPT-4 is dramatically asymmetric: 0.80 F1 / 0.90 recall on ACCURATE but 0.09 F1 on NOT_ACCURATE (0.05 for GPT-3.5-turbo). NOT_ACCURATE is arguably the most consequential class for downstream citation-integrity screening, so GPT-4 is unsuitable for practical use under this prompting strategy.
- Authors note that "better prompting strategies, specifically focusing on NOT_ACCURATE, could yield better results"; only slight manual variations were tried.
- GPT-3.5-turbo with 5-shot in-context learning achieved 0.89 F1 on the citation-context (binary) sub-task — no improvement over the trivial citance baseline (0.94).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sarolAssessingCitationIntegrity2024#TRIPOD-LLM reporting summary]].

| Model | Micro-F1 | Macro-F1 | ACC F1 (recall) | N_ACC F1 | IRR F1 |
| --- | :---: | :---: | :---: | :---: | :---: |
| **GPT-4** | **0.65** | **0.45** | **0.80 (0.90)** | **0.09** | **0.48** |
| GPT-3.5-turbo-0613 | 0.57 | 0.38 | 0.73 | 0.05 | 0.34 |
| (Comparison) Best MultiVerS top-20 | 0.59 | 0.52 | 0.69 | 0.43 | 0.42 |
| (Ceiling) Oracle gold-context+evidence | 0.75 | 0.78 | 0.80 | 0.57 | 0.96 |

| Comparison | Significance |
| --- | --- |
| GPT-4 vs. baseline MultiVerS | McNemar p≤.001 |
| GPT-4 vs. best MultiVerS (top-20) | McNemar p≤.05 |
| GPT-3.5-turbo vs. MultiVerS variants | n.s. |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Sarol et al. excluded citation cases where evidence appeared in tables figures or supplementary material]]
- [[CVT - Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM confidence calibration on scientific-error tasks is poor with extreme distributions]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

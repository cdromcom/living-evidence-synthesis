---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/citation-integrity-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/46pct
  - 5c/connectivity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b64-7261-a464-053ddf56abb6
appraisal_overall: L0-M3-H2
tripod_llm_pct: 46pct
---

## Source

[[@zhangDetectingReferenceErrors2024]]

## Description

> "Unlike GPT-3.5 Turbo, GPT-4 Turbo and GPT-4o tend to be much stricter in error detection, paying attention to small differences between the statement and the reference." (Zhang & Abernethy, 2024, p. 4)
> Table 3 shows GPT-3.5 Turbo overall accuracy: Title=66.0%, Title+Abstract=56.4%, Title+Abstract+Excerpts=54.0%, Title+PDF (Assistant)=68.0% (p. 4).
>
> ![[zhangDetectingReferenceErrors2024-results-p4-1.png]]

## Methods Context

### What?

> **Study design:** zero-shot LLM evaluation on a held-out, expert-annotated quotation-error benchmark (cross-sectional).
>
> **Method type:** zero-shot prompted classification with retrieval-augmented context, plus a proprietary RAG (OpenAI Assistant API) variant.
>
> **Tools:** OpenAI gpt-3.5-turbo-0125; GROBID (PDF parsing); LlamaIndex (chunking + embedding retrieval); OpenAI Assistant API (PDF RAG); OpenAI Python API.
>
> **Dependent variable(s):** per-class accuracy (Unsubstantiated / Partially substantiated / Fully substantiated) and overall label accuracy.
>
> **Independent variable(s) / covariates:** reference-information setting (4 levels: Title; Title+Abstract; Title+Abstract+Excerpts; Title+PDF Assistant).
>
> "Three LLMs in OpenAI's GPT family were evaluated in the experiment: gpt-3.5-turbo-0125, gpt-4-0125-preview, and gpt-4o-2024-05-13. LLMs were prompted to respond with a JSON object containing a predicted label and an explanation for their selection. All LLM experiments were conducted using OpenAI's Python API with temperature set to 0. Model performance was measured by label accuracy." (Zhang & Abernethy, 2024, p. 3)
> ![[zhangDetectingReferenceErrors2024-evd-p3-1.png]]

### How?

> **Procedure:** Identical zero-shot prompting protocol to the GPT-4 Turbo / GPT-4o runs. The fixed prompt template (Appendix C) supplied the 3 label definitions, requested a JSON response with `label` and `explanation`, and inserted the citing-article title, the statement, the reference title, the reference abstract, and reference excerpts (when applicable). For the excerpt setting, the reference PDF was parsed by GROBID, split into 256-token chunks (20-token overlap) via LlamaIndex; the statement was embedded and the top-3 chunks by similarity were inserted into the prompt. For the Assistant setting the PDF was attached and OpenAI's proprietary RAG handled retrieval. GPT-3.5 Turbo was queried at temperature = 0 across all 4 information settings, and per-class + overall label accuracy were computed against the gold label. Error analysis of explanations characterized the model's behavior: GPT-3.5 Turbo behaved permissively on Title-only (calling pairs Fully substantiated when topics matched), but additional reference context that did not directly relate to the statement caused it to flip many Fully-substantiated pairs to Unsubstantiated.
>
> "When more information is provided, GPT-3.5 Turbo would still rely on such superficial relations, and additional text from the reference that is not directly related to the statement would cause GPT-3.5 Turbo to regard the two articles as not so related. This also explains why GPT-3.5 Turbo's performance on Unsubstantiated cases increased dramatically when more information was provided." (Zhang & Abernethy, 2024, p. 4)
> ![[zhangDetectingReferenceErrors2024-evd-p4-1.png]]

### Who?

> **Models / participants:** 1 OpenAI model (gpt-3.5-turbo-0125); no human subjects. Evaluation units are statement-reference pairs.
>
> **Sample-size flow (statement-reference pairs):** sourced from 3 channels, (1) prior citation-verification studies that shared annotated datasets or traceable examples → 163 (65.2%); (2) PubPeer comments cross-referenced with Retraction Watch retractions (2022–2023) for "concerns or issues about referencing or attributions" → 80 (32.0%); (3) PubMed corrections / errata / corrigenda → 7 (2.8%). Three inclusion criteria: digital versions findable via search engines; reference is a journal article (PDF text-extractable); cited statement uniquely identifiable in the citing article. **Final analyzed N = 250 statement-reference pairs.**
>
> **Label distribution:** 112 Unsubstantiated (44.8%), 14 Partially substantiated (5.6%), 124 Fully substantiated (49.6%).
>
> **Domain mix:** Biology/Medicine 85 (34.0%), Chemistry/Material Science 57 (22.8%), Physics 26 (10.4%), Social Science 26 (10.4%), Earth/Environmental Science 24 (9.6%), Engineering 17 (6.8%), Computer Science 15 (6.0%).
>
> "Statement-reference pairs in the dataset were collected through the following channels: (1) 163 (65.2%) pairs are from previous citation verification studies that either provided traceable examples of quotation errors or shared annotated datasets… (2) 80 (32.0%) pairs are from PubPeer, a platform for researchers to leave comments on others' publications… (3) 7 (2.8%) pairs are from corrections, errata, and corrigenda available in the PubMed database." (Zhang & Abernethy, 2024, p. 7)
> ![[zhangDetectingReferenceErrors2024-evd-p7-1.png]]

## Other Notes

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangDetectingReferenceErrors2024#TRIPOD-LLM reporting summary]].

| Setting | Unsubstantiated acc. | Partially acc. | Fully acc. | Overall acc. |
| --- | --- | --- | --- | --- |
| GPT-3.5 Turbo, Title | 64.3% | 14.3% | 73.4% | 66.0% |
| GPT-3.5 Turbo, Title + Abstract | 84.8% | 57.1% | 30.6% | 56.4% |
| GPT-3.5 Turbo, Title + Abstract + Excerpts | 79.5% | 57.1% | 30.6% | **54.0%** |
| **GPT-3.5 Turbo, Title + PDF (Assistant)** | **79.5%** | **14.3%** | **63.7%** | **68.0%** |

Pattern: more reference context did **not** monotonically improve GPT-3.5 Turbo. Recall on Unsubstantiated rose with context, but accuracy on Fully substantiated collapsed (73.4% → 30.6%), giving a net drop in overall accuracy. The proprietary Assistant-API PDF RAG was the only configuration that recovered Title-only's overall accuracy (68.0%).

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Adding more input context can degrade rather than improve LLM performance on structured tasks]]

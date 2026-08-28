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
  - tripod-llm/compliance/low
  - tripod-llm/proportion/46pct
  - 5c/connectivity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b66-7029-bece-dd450e4d9813
appraisal_overall: L0-M3-H2
tripod_llm_pct: 46pct
---

## Source

[[@zhangDetectingReferenceErrors2024]]

## Description

> "GPT-4 Turbo and GPT-4o performed much better than GPT-3.5 Turbo at detecting Unsubstantiated cases, especially when information about the reference article is limited." (Zhang & Abernethy, 2024, p. 3)
> Table 3 shows GPT-4 Turbo with Title+Abstract+Excerpts achieved overall accuracy 70.0%, with PDF (Assistant) 67.6% (p. 4).
>
> ![[zhangDetectingReferenceErrors2024-results-p4-1.png]]

## Methods Context

### What?

> **Study design:** zero-shot LLM evaluation on a held-out, expert-annotated quotation-error benchmark (cross-sectional).
>
> **Method type:** zero-shot prompted classification with retrieval-augmented context, plus a proprietary RAG (OpenAI Assistant API) variant.
>
> **Tools:** OpenAI GPT family — gpt-3.5-turbo-0125, gpt-4-0125-preview, gpt-4o-2024-05-13; OpenAI Assistant API for PDF RAG; GROBID for PDF text extraction; LlamaIndex for chunking + embedding-based retrieval; OpenAI Python API.
>
> **Dependent variable(s):** per-class accuracy (Unsubstantiated / Partially substantiated / Fully substantiated) and overall label accuracy.
>
> **Independent variable(s) / covariates:** model version (3 levels) × reference-information setting (4 levels: Title; Title+Abstract; Title+Abstract+Excerpts; Title+PDF via Assistant).
>
> "Three LLMs in OpenAI's GPT family were evaluated in the experiment: gpt-3.5-turbo-0125, gpt-4-0125-preview, and gpt-4o-2024-05-13. LLMs were prompted to respond with a JSON object containing a predicted label and an explanation for their selection. All LLM experiments were conducted using OpenAI's Python API with temperature set to 0. Model performance was measured by label accuracy." (Zhang & Abernethy, 2024, p. 3)
> ![[zhangDetectingReferenceErrors2024-evd-p3-2.png]]

### How?

> **Procedure:** A fixed prompt template (Appendix C) was finalized before the experiment. The user prompt instructed the model as "an experienced scientific writer and editor", supplied the 3 label definitions, requested a JSON response with `label` and `explanation`, and inserted the citing-article title, the statement, the reference title, the reference abstract, and reference excerpts (when applicable). For the excerpt setting, the reference PDF was parsed by GROBID, split into 256-token chunks with 20-token overlap (LlamaIndex), the statement was embedded, and the top-3 chunks by embedding similarity to the statement were inserted into the prompt. For the Assistant setting, the same prompt header was sent with instructions to read the attached PDF (proprietary OpenAI RAG). Each of the 3 models was run on each of the 4 information settings (12 runs) at temperature = 0. Performance was scored as exact-match label accuracy against the gold label, both per-class and overall. As a comparison baseline, models from Wadden et al. (2020) scientific claim verification were also tested but predicted "Not Enough Information" for all pairs and were excluded from Table 3. A secondary two-class analysis collapsed Partially + Fully substantiated for Figure 1.
>
> "Local retrieval of excerpts from the main body of a reference followed a 3-step retrieval-augmented generation (RAG) (Gao et al., 2024) pipeline. First, the full text of a reference was extracted from its PDF file by GROBID. The extracted full text was then split into 256-token chunks with 20-token overlaps using LlamaIndex. In the experiment, the embeddings of the chunks were compared to that of the input statement using LlamaIndex, and the top 3 chunks with the highest match to the statement were retrieved and included in the prompt to the LLMs." (Zhang & Abernethy, 2024, p. 3)
> ![[zhangDetectingReferenceErrors2024-evd-p3-3.png]]

### Who?

> **Models / participants:** 3 OpenAI GPT models (no human subjects). The evaluation units are statement-reference pairs.
>
> **Sample-size flow (statement-reference pairs):** sourced from 3 channels — (1) prior citation-verification studies that shared annotated datasets or traceable error examples → 163 pairs (65.2%); (2) PubPeer comments cross-referenced with Retraction Watch retractions (2022–2023) for "concerns or issues about referencing or attributions" → 80 pairs (32.0%); (3) PubMed corrections / errata / corrigenda → 7 pairs (2.8%). Three inclusion criteria applied: (a) digital versions findable via search engines; (b) reference is a journal article (PDF text-extractable); (c) the cited statement is uniquely identifiable in the citing article. **Final analyzed N = 250 statement-reference pairs.**
>
> **Label distribution:** 112 Unsubstantiated (44.8%), 14 Partially substantiated (5.6%), 124 Fully substantiated (49.6%).
>
> **Domain mix:** Biology/Medicine 85 (34.0%), Chemistry/Material Science 57 (22.8%), Physics 26 (10.4%), Social Science 26 (10.4%), Earth/Environmental Science 24 (9.6%), Engineering 17 (6.8%), Computer Science 15 (6.0%).
>
> **Reference availability:** has abstract 242 (96.8%), has PDF 244 (97.6%), has abstract or PDF 250 (100%).
>
> "Statement-reference pairs in the dataset were collected through the following channels: (1) 163 (65.2%) pairs are from previous citation verification studies that either provided traceable examples of quotation errors or shared annotated datasets… (2) 80 (32.0%) pairs are from PubPeer, a platform for researchers to leave comments on others' publications… (3) 7 (2.8%) pairs are from corrections, errata, and corrigenda available in the PubMed database." (Zhang & Abernethy, 2024, p. 7)
> ![[zhangDetectingReferenceErrors2024-evd-p7-2.png]]

## Other Notes

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhangDetectingReferenceErrors2024#TRIPOD-LLM reporting summary]].

| Setting | Unsubstantiated acc. | Partially acc. | Fully acc. | Overall acc. |
| --- | --- | --- | --- | --- |
| GPT-4 Turbo, Title | 89.3% | 14.3% | 36.3% | 58.8% |
| GPT-4 Turbo, Title + Abstract | 89.3% | 35.7% | 39.5% | 61.6% |
| **GPT-4 Turbo, Title + Abstract + Excerpts** | **83.9%** | **21.4%** | **62.9%** | **70.0%** |
| GPT-4 Turbo, Title + PDF (Assistant) | 84.8% | 35.7% | 55.6% | 67.6% |
| GPT-4o, best (T+PDF Assistant) | 83.9% | 21.4% | 58.9% | 68.0% |
| GPT-3.5 Turbo, best (T+PDF Assistant) | 79.5% | 14.3% | 63.7% | 68.0% |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The quotation error dataset was predominantly from natural science journal articles limiting generalizability to conference papers and other publication channels]]

- [[CVT - The simple sentence-pair annotation scheme treated all reference pairs as equivalent despite multiple possible rationales for citation]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - More capable GPT-class LLMs can detect quotation errors in scientific papers without fine-tuning but performance is imperfect and context-dependent]]

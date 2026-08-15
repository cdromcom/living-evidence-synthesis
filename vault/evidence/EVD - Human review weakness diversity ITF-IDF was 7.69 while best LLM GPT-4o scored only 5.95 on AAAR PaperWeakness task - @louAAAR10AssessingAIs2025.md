---
NodeFormality: draft
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/57pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b72-7793-93a6-8b90041c9c71
appraisal_overall: L0-M3-H2
tripod_llm_pct: 57pct
---

## Source

[[@louAAAR10AssessingAIs2025]]

## Description

> Human Review ITF-IDF = 7.69; GPT-4o ITF-IDF = 5.95 (Table 6, Lou et al., 2025, p. 10)
>
> "there is still a considerable gap in the weakness diversity between the LLMs and human experts. Compared with human review, most LLM-generated weaknesses are vague and lack the necessary knowledge about some frontier research works." (Lou et al., 2025, p. 9)
>
> ![[louAAAR10AssessingAIs2025-evd-p9-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark evaluation on the new WEAKNESS task in AAAR-1.0. **Method type:** zero-shot LLM evaluation, comparing LLM-generated weakness lists against multi-reviewer ground-truth weakness lists using a novel diversity metric. **Tools:** SentenceBERT (Reimers, 2019, all-mpnet-base-v2) for similarity scoring; closed-source GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, o1-preview, o3-mini; open-source OLMo-7B, Mistral-7B, Mixtral-8x22B-MoE, Llama 3.1-70B, Qwen 2.5-72B; AI-SCI agent framework (Lu et al., 2024) on GPT-4o backbone. **Dependent variable(s):** ITF-IDF (Inverse-Term-Frequency × Inverse-Document-Frequency) weakness-diversity score; also S-F1, S-Precision, S-Recall against multi-reviewer gold weakness lists. **Independent variable(s) / covariates:** model identity; prompting input strategy (split-combine vs. no-split); window size; AI-SCI agentic prompting vs. plain LLM.
>
> "Inspired by the classic TF-IDF, we propose a novel review diversity metric: ITF-IDF = (1/w) Σ_j ((1/m_j) Σ_i log(m_j / O_i^j)) × log(w / R_i^j)) ... Oj_i calculates the intra-paper occurrence frequency of pj_i; Rj_i is the 'soft' number of papers that also contain the pj_i ... Oj_i measures informativeness, and Rj_i measures specificity. The complete ITF-IDF consider both aspects and reflects the overall weakness diversity." (Lou et al., 2025, p. 6)
> ![[louAAAR10AssessingAIs2025-evd-p6-3.png]]

### How?

> **Procedure:** For each of the 993 ICLR 2023 paper instances, the full paper text was extracted via VILA from the OpenReview PDF, with figures/tables extracted via PDFFigures-2.0. Because mean input length is 9,811 words (max 49,195), inputs exceeding the model context window were processed using a **split-combine** strategy: paper split into pieces of 2,000 words (open-source) or 3,000 words (closed-source), each piece prompted separately to generate a weakness list, then merged into a final per-paper weakness list. Generated weakness lists were compared to the multi-reviewer ground-truth using SentenceBERT cosine similarity to compute S-Precision, S-Recall, S-F1 (eqs. 4–5), and ITF-IDF (eq. 6) measuring intra-paper informativeness × cross-paper specificity. AI-SCI was additionally evaluated as an agentic baseline on GPT-4o. Each model was run thrice and the median taken.
>
> "in WEAKNESS, we try to utilize the whole paper. As the input length of WEAKNESS is extremely long (see Table 11), we adopt a 'split-combine' method — we first split the whole paper into smaller pieces and let LLMs predict the weaknesses of each piece separately; after that, we merge all pieces' weaknesses as a final prediction. For the length of each small piece, we set 2,000 and 3,000 words for open- and closed-source LLMs, respectively." (Lou et al., 2025, p. 9)
> ![[louAAAR10AssessingAIs2025-evd-p9-2.png]]

### Who?

> **Models / participants:** 5 closed-source LLMs + 5 open-source LLMs + AI-SCI agent framework (11 systems total). No human subjects in evaluation; the underlying ground-truth weaknesses were written by ICLR 2023 reviewers.
>
> **Sample-size flow (WEAKNESS corpus construction):** 3,779 anonymous ICLR 2023 submissions crawled from OpenReview → uniformly sampled across 13 tracks and balanced for accept/reject → 1,000 papers (500 accepted, 500 rejected) → GPT-4 used to extract verbatim reviewer-written weaknesses from each reviewer's raw comments → papers with no extracted weaknesses removed → **993 final {paper, multi-reviewer-weakness-lists} instances**. Per Table 11: avg 3.8 reviewers/paper (range 3–9), avg 4.8 weaknesses/reviewer (range 1–39), avg weakness length 39.1 words.
>
> "We first crawl a total of 3,779 anonymous submissions of ICLR 2023 from OpenReview ... we finally collect a total of 1,000 papers (500 accepted; 500 rejected), uniformly covering all 13 tracks ... We further delete a few papers without any weaknesses found in the raw comments, resulting in a total of 993 instances, i.e., 993 {paper, weakness lists} pairs." (Lou et al., 2025, p. 5)
> ![[louAAAR10AssessingAIs2025-evd-p5-1.png]]

## Other Notes

Surprisingly, AI-SCI (an advanced prompting framework) performed worse than baseline GPT-4o on ITF-IDF, suggesting popular prompting techniques do not resolve the diversity gap. The paper also flags (footnote 7, p. 9) that the human ITF-IDF of 7.69 may be slightly underestimated because repeated weaknesses across reviewers were retained.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@louAAAR10AssessingAIs2025#TRIPOD-LLM reporting summary]].

| System | S-F1 (%) | S-Precision (%) | S-Recall (%) | ITF-IDF (↑) |
| --- | --- | --- | --- | --- |
| **Human Review (gold)** | — | — | — | **7.69** |
| Gemini 1.5 Pro | 48.75 | 43.97 | 55.08 | 5.88 |
| Claude 3.5 Sonnet | 47.85 | 41.97 | 56.00 | 3.91 |
| **GPT-4o (best LLM ITF-IDF)** | 47.73 | 42.09 | 55.48 | **5.95** |
| o1-preview | 48.62 | 42.54 | 57.08 | 5.63 |
| o3-mini | 46.33 | 42.00 | 51.99 | 5.85 |
| OLMo-7B | 43.25 | 40.38 | 47.04 | 2.45 |
| Mistral-7B | 42.03 | 43.80 | 40.77 | 1.17 |
| Mixtral-8x22B-MoE | 43.23 | 44.59 | 42.23 | 0.98 |
| Llama 3.1-70B | 42.78 | 43.19 | 42.70 | 2.60 |
| Qwen 2.5-72B | 42.74 | 43.80 | 42.05 | 1.21 |
| AI-SCI (GPT-4o backbone) | 45.05 | 40.02 | 51.91 | 2.23 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The AAAR benchmark excluded non-textual inputs such as figures that are integral to scientific evaluation]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]

- [[CLM - LLMs cannot reliably identify scientific paper limitations at the level of human expert reviewers]]

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/43pct
  - 5c/clarity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b62-72b0-a3fa-eef30bcf71c7
appraisal_overall: L0-M2-H3
tripod_llm_pct: 43pct
---

## Source

[[@akyonEvaluatingCapabilitiesGenerative2024]]

## Description

> "The percentage of correct answers for each LLM is shown in Table 3, with GPT 3.5-turbo achieving the highest rate (66.9%), followed by GPT 4-1106 (65.6%), Palm 2 (62.1%), Claude v1 (58.3%), Gemini pro (49.2%), and GPT 4-0613 (44.1%)." (Akyon et al., 2024, p. 16)
>
> ![[akyon2024-table3-p18-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of multiple commercial LLMs against an expert-derived gold standard on a STROBE-checklist comprehension task (methodological-research design).
>
> **Method type:** Retrieval-Augmented Generation (RAG) zero-shot question answering with low-temperature (T=0.1) repeated sampling.
>
> **Tools:** custom RAG web application (LanceDB vector store + OpenAI text-ada-embedding-002 embeddings + cosine-similarity retrieval); 6 LLMs (GPT 3.5-turbo-1106, GPT 4-0613, GPT 4-1106, Claude v1, Palm 2/chat-bison, Gemini pro 1.0); 15 STROBE-derived questions (13 yes/no + 2 multiple-choice); SPSS 29.0 for statistics.
>
> **Dependent variable(s):** percentage of "correct" responses per LLM (across 5,850 question-answer pairs per LLM, 4,950 for Claude v1) judged against the medical professor's gold-standard answers.
>
> **Independent variable(s):** LLM identity (6 levels); STROBE question (Q1–Q15); article (39 levels); repetition (10 trials per question per article).
>
> "Using this benchmark pipeline, we compared the answers of several generative AI tools (Chat-GPT 3.5-turbo, chat-GPT-4, Palm, Claude v1, Gemini pro) with the golden standard for 50 medical research articles from PUBMED. The experienced medical professor's answers to these questions are assigned as the golden standard." (Akyon et al., 2024, p. 6)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p3-1.png]]

### How?

> **Procedure:** (1) PubMed search on 19 December 2023 for "obesity" in title → 2996 hits → filtered to English, free full-text, human, last 5 years → 303 articles → first 50 selected → 11 excluded as non-observational → 39 final (Claude v1 access restrictions further excluded 6 articles → 33 articles for Claude). (2) Each PDF was uploaded to the RAG web app, which extracted and chunked text, embedded chunks with text-ada-embedding-002, and stored them in LanceDB. (3) For each STROBE question, cosine-similarity retrieval pulled the most relevant chunks; the LLM was given a fixed system prompt ("You are an expert medical professor specialized in pediatric gastroenterology hepatology and nutrition...") plus the chunks plus the question and asked to choose one option. (4) Each question was posed **10 times per article per LLM** at temperature 0.1. (5) Only responses that exactly matched the gold-standard option and followed instructions were counted "correct"; ambiguous/multi-candidate answers were marked incorrect. (6) Shapiro-Wilk → Kruskal-Wallis + Pearson chi-square at α=0.05; post-hoc GPower analysis confirmed >95% power.
>
> "The benchmark pipeline itself is designed to process PubMed articles of varying lengths and extract relevant information for analysis. This pipeline operates as follows: Article Retrieval... Text Extraction and Chunking... Vector Representation: Using the OpenAI text-ada-embedding-002 model, each text chunk was converted into a representation vector... Vector Database Storage: The generated representation vectors were stored in a vector database (LanceDB in our case)... Query Processing: When a query (question from the STROBE checklist) was posed to an LLM, our pipeline calculated the cosine similarities between the query's representation vector and the vectors stored in the database... Retrieval-Augmented Generation: The retrieved text chunks, along with the original query, were then combined and presented to the LLM." (Akyon et al., 2024, p. 11)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p11-1.png]]

### Who?

> **Models:** 6 commercial LLMs — GPT 3.5-turbo-1106 (OpenAI, cutoff Sep 2021); GPT 4-0613 (OpenAI, cutoff Sep 2021); GPT 4-1106 (OpenAI, cutoff Apr 2023); Claude v1 (Anthropic, cutoff not stated); Palm 2/chat-bison (Google, cutoff not stated); Gemini pro 1.0 (Google, cutoff not stated).
>
> **Articles (sample-size flow):** PubMed "obesity"-in-title search 19 Dec 2023 → **2996 hits** → English + free full-text + human + last 5 years → **303 hits** → first **50** → 11 excluded as non-observational → **39 analyzed** (Claude v1 limited to 33 due to access restrictions). For 39 articles × 15 questions × 10 trials = **5850 QA pairs per LLM** (4950 for Claude v1).
>
> **Reference standard:** 1 experienced medical professor specialized in pediatric gastroenterology answered all 15 questions per article; 1 epidemiologist (Dr. Hilal Duzel) verified the answers.
>
> "Using this benchmark pipeline, we compared the answers of the generative AI tools, which are ChatGPT 3.5-turbo 1106 (11th June version), ChatGPT 4-0613 (6th November version), ChatGPT 4-1106 (11th June version), Palm 2 (chat-bison), Claude v1, Gemini pro with the benchmark in 15 questions for 39 medical research articles (Table 2). In this study, 15 questions selected from the STROBE checklists were posed 10 times each for 39 articles to six different LLMs." (Akyon et al., 2024, p. 12)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p12-1.png]]

## Other Notes

Statistical analysis revealed significant differences between LLMs (P<.001). The difference between ChatGPT 4-1106 and ChatGPT 3.5 Turbo-1106 was not statistically significant (P=.061).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@akyonEvaluatingCapabilitiesGenerative2024#TRIPOD-LLM reporting summary]].

| LLM | Total QA pairs | Correct (n) | Correct (%) |
| --- | :---: | :---: | :---: |
| **GPT 3.5-Turbo-1106** | 5850 | 3916 | **66.9%** |
| GPT 4-1106 | 5850 | 3837 | 65.6% |
| Palm 2 (chat-bison) | 5850 | 3632 | 62.1% |
| Claude v1 | 4950 | 2887 | 58.3% |
| Gemini pro 1.0 | 5850 | 2878 | 49.2% |
| GPT 4-0613 | 5850 | 2580 | 44.1% |

| Pairwise comparison | Significance |
| --- | --- |
| Overall LLM differences (Kruskal-Wallis) | P<.001 |
| GPT 3.5-Turbo vs. GPT 4-1106 | P=.061 (n.s.) |
| GPT 4-1106 vs. Palm 2 | P<.001 |
| Palm 2 vs. Claude v1 | P<.001 |
| Claude v1 vs. Gemini pro | P<.001 |
| Gemini pro vs. GPT 4-0613 | P<.001 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The benchmark gold standard relied on a single medical professor limiting reference standard validity]]

- [[CVT - Training data cutoff differences across LLM versions confounded performance comparisons in the STROBE benchmark study]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate LLM accuracy on evidence-appraisal benchmarks lands in the moderate 60-80 percent range]]

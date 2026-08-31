---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/risk-of-bias-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M2-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/42pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7d-71c9-8031-ad4be310e084
appraisal_overall: L1-M2-H2
tripod_llm_pct: 42pct
---

## Source

[[@leucutaRiskBiasAssessment2025]]

## Description

> "Out of 110 signaling questions assessments (11 questions for each of the 10 articles) by the four AI models, the mean percentage of correct assessments (where an assessment was considered correct if both the answer and the reasoning for the argument were correct) of all the models was 72.95%. The most accurate model was Grok 3, followed by ChatGPT 4o, DeepSeek V3, and Gemini 2.0 flash (Table 2, Figure 1), ranging from 74.45% to 67.27%." (Leucuta et al., 2025, p. 9)
>
> ![[leucuta2025-table2fig1-p9-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of LLM risk-of-bias assessments against expert human consensus.
>
> **Method type:** zero-shot prompting of four general-purpose LLMs via public web interfaces, scored against a two-expert consensus reference.
>
> **Tools:** ChatGPT 4o (OpenAI), x.AI Grok 3, Gemini 2.0 Flash (Google), DeepSeek V3 — all via public web UIs; QUADAS-2 instrument (Whiting et al. 2011) covering four domains (patient selection, index test, reference standard, flow and timing) with 11 signaling questions per article.
>
> **Dependent variable:** correctness of each LLM signaling-question assessment (binary: correct = answer matches human consensus AND argument is correct).
>
> **Independent variables / covariates:** LLM identity (4 levels); QUADAS-2 domain (4 levels); signaling question (11 levels); article (10 diagnostic-accuracy studies).
>
> "Four artificial intelligence generative large language models were used with their public web-based interfaces, for the AI assessment: ChatGPT 4o model, X.AI Grok 3 model, Gemini 2.0 flash model, and the DeepSeek V3 model." (Leucuta et al., 2025, p. 3)
> ![[leucutaRiskBiasAssessment2025-evd-p3-1.png]]

### How?

> **Procedure:** (1) selected 10 recent open-access PubMed diagnostic-accuracy articles (search performed 9 May 2025; query: "diagnostic accuracy"[Title/Abstract] AND diabetes[Title/Abstract], most recent first, free full-text filter) plus 2 non-diagnostic articles as controls; (2) each article uploaded as a PDF (from publisher site or PubMed Central) into a fresh chat session per article (to prevent context carryover); (3) identical prompt issued to all four LLMs: instruction to use QUADAS-2, answer signaling questions yes/no/unclear/not-applicable and risk-of-bias as low/high/unclear, then provide rationale; (4) signaling questions and the domain risk-of-bias judgement prompted per QUADAS-2 domain; (5) two human experts independently assessed each article and resolved disagreements by consensus to establish the reference; (6) each LLM assessment scored as correct **only** if both answer and argument matched the human reference (identical answer with incorrect argument scored as incorrect); (7) categorical results presented as counts and percentages overall, per model, per domain, and per signaling question; reasoning errors documented qualitatively.
>
> "Each article was uploaded as a PDF file, sourced from either the publisher's site or PubMed Central. For each domain of QUADAS 2, the signaling questions and the risk of bias were then prompted to elicit the answers from the LLMs. Identical prompts were used for each domain across all models. A new session was initiated for each article to prevent carryover of contextual information." (Leucuta et al., 2025, p. 3)
> ![[leucutaRiskBiasAssessment2025-evd-p3-2.png]]

### Who?

> **Models:** four general-purpose LLMs accessed via public web interfaces — ChatGPT 4o, x.AI Grok 3, Gemini 2.0 Flash, DeepSeek V3 (versions as of the study period; specific build dates not reported).
>
> **Article sample-size flow:** PubMed search (9 May 2025) for diagnostic accuracy + diabetes, most recent first, free full-text filter → original diagnostic-accuracy articles only (reviews/systematic reviews/editorials/protocols excluded) → screened by authors for medical-field diversity → **10 diagnostic-accuracy articles retained** spanning cardiology (2), gastroenterology (2), neurology (1), rheumatology (1), sleep medicine (1), vascular surgery (1), and ophthalmology (2). 2 additional non-diagnostic articles included as inapplicability controls (analyzed separately in §3.5; not part of the 110 assessments).
>
> **Assessments analyzed:** 10 articles × 11 signaling questions × 4 LLMs = **440 LLM assessments**; quantitative accuracy summarized per model over 110 question instances per model (= 11 × 10).
>
> **Human reference:** two authors independently assessed every article; discrepancies resolved by discussion and consensus.
>
> "Ten diagnostic accuracy articles were selected from Pubmed, using the following search strategy: ('diagnostic accuracy' [Title/Abstract]) AND (diabetes [Title/Abstract]), with the most recent papers first. A filter for free full-text articles was applied. The search strategy was performed on 9 May 2025." (Leucuta et al., 2025, p. 2)
> ![[leucutaRiskBiasAssessment2025-evd-p2-2.png]]

## Other Notes

By domain: Flow and timing was highest (80.63%), then index test (73.75%), then patient selection (65.83%) and reference standard (63.75%). The percentage of answers that were correct but with incorrect reasoning was 2.95% overall, highest in index test domain (5%).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@leucutaRiskBiasAssessment2025#TRIPOD-LLM reporting summary]].

| Model | Correct / 110 | % correct |
| --- | :---: | :---: |
| **x.AI Grok 3** | 85/110 | **77.27%** |
| ChatGPT 4o | 83/110 | 75.45% |
| DeepSeek V3 | 79/110 | 71.82% |
| Gemini 2.0 Flash | 74/110 | 67.27% |
| **Mean across 4 models** | — | **72.95%** |

| Domain (n per model) | ChatGPT 4o | x.AI Grok 3 | Gemini 2.0 Flash | DeepSeek V3 | Total (% of 4×n) |
| --- | :---: | :---: | :---: | :---: | :---: |
| Patient selection (n=30) | 23 (76.67%) | 22 (73.33%) | 15 (50%) | 19 (63.33%) | **65.83%** |
| Index test (n=20) | 15 (75%) | 13 (65%) | 16 (80%) | 15 (75%) | **73.75%** |
| Reference standard (n=20) | 12 (60%) | 16 (80%) | 13 (65%) | 13 (65%) | **63.75%** |
| Flow and timing (n=40) | 33 (82.5%) | 34 (85%) | 30 (75%) | 32 (80%) | **80.63%** |

| Auxiliary metric | Value |
| --- | --- |
| Correct answer with incorrect reasoning (overall) | 2.95% |
| Highest "correct answer / wrong reasoning" model | Gemini 2.0 Flash (6.36%) |
| Highest "correct answer / wrong reasoning" domain | Index test (5%) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - A single standardized prompt was used across all LLMs without prompt engineering potentially underestimating LLM capabilities in QUADAS-2 assessment]]

- [[CVT - Only publicly available web-based LLM interfaces were used rather than APIs potentially missing superior performance of paid or fine-tuned model versions]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate LLM accuracy on evidence-appraisal benchmarks lands in the moderate 60-80 percent range]]

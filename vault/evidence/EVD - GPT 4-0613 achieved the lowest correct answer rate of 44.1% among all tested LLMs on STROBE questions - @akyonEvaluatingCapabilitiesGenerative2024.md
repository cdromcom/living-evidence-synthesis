---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
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
nodeID: 019ddb4e-6b63-7471-8ff0-2c69d0a4f27e
appraisal_overall: L0-M2-H3
tripod_llm_pct: 43pct
---

## Source

[[@akyonEvaluatingCapabilitiesGenerative2024]]

## Description

> "The lowest correct answer percentage was provided by ChatGPT 4–0613, at 44.1%. Gemini pro yielded 49.2% correct answers, significantly higher than Chat-GPT 4 – 0613 (P<.001)." (Akyon et al., 2024, p. 16)
>
> ![[akyon2024-table3-p18-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of GPT 4-0613 (one of 6 commercial LLMs) against an expert STROBE-checklist gold standard.
>
> **Method type:** RAG zero-shot QA with low-temperature (T=0.1) repeated sampling, then Kruskal-Wallis pairwise comparison against the next-best LLM.
>
> **Tools:** custom RAG web app (LanceDB + text-ada-embedding-002 + cosine retrieval); GPT 4-0613 (OpenAI, dated 13 June 2023, training cutoff September 2021); 15 STROBE-derived questions; SPSS 29.0.
>
> **Dependent variable:** percentage of GPT 4-0613 responses (out of 5850 question-answer pairs) judged correct against the medical professor's gold-standard answers.
>
> **Independent variable / covariate of interest:** model identity (GPT 4-0613 vs. comparator LLMs); article-publication date relative to GPT 4-0613's Sep-2021 knowledge cutoff (28/39 articles published pre-cutoff).
>
> "Using this benchmark pipeline, we compared the answers of the generative AI tools, which are ChatGPT 3.5-turbo 1106 (11th June version), ChatGPT 4-0613 (6th November version), ChatGPT 4-1106 (11th June version), Palm 2 (chat-bison), Claude v1, Gemini pro with the benchmark in 15 questions for 39 medical research articles (Table 2)." (Akyon et al., 2024, p. 12)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p12-2.png]]

### How?

> **Procedure:** identical RAG pipeline used for all 6 LLMs (chunking → text-ada-embedding-002 vectors → LanceDB → cosine-similarity retrieval → fixed system prompt naming an expert pediatric-gastroenterology-hepatology persona → question with answer options). Each of the 15 STROBE questions was posed **10 times per article** at temperature 0.1 to control output randomness. Only responses that exactly matched the gold-standard option and followed instructions were counted correct. Pairwise Kruskal-Wallis tests compared each LLM with the next-better-performing LLM; GPT 4-0613 was the lowest scorer and was contrasted against Gemini pro (next-lowest) at P<.001.
>
> "Each LLM was compared with another LLM that provided a lower percentage of correct answers. Statistical analysis using the Kruskal-Wallis test revealed statistically significant differences between the LLMs (P<.001). The lowest correct answer percentage was provided by ChatGPT 4–0613, at 44.1%. Gemini pro yielded 49.2% correct answers, significantly higher than Chat-GPT 4 – 0613 (P<.001)." (Akyon et al., 2024, p. 14)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p14-1.png]]

### Who?

> **Model:** GPT 4-0613 (OpenAI; dated 13 June 2023; training cutoff September 2021). No fine-tuning.
>
> **Articles (sample-size flow):** PubMed obesity-in-title search 19 Dec 2023 → **2996** → eligibility filter → **303** → first **50** selected → 11 excluded as non-observational → **39 analyzed**. Of those 39, **28 (71.8%)** were published before the GPT 4-0613 cutoff; the other 11 articles (28.2%) were published after the cutoff and could not have been seen in training. **No human evaluators for this EVD**, performance scored against gold answers from one medical professor (validated by an epidemiologist). 39 articles × 15 questions × 10 trials = **5850 QA pairs** for GPT 4-0613.
>
> "Of the 39 articles analyzed, 28 (71.8%) were published before the training data cutoff date for GPT-3.5-turbo and GPT-4-0613, while all 39 articles (100%) were published before the cutoff date for GPT-4-1106." (Akyon et al., 2024, p. 14)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p14-2.png]]

## Other Notes

The authors discuss that compression techniques used in developing newer model versions (e.g., quantization, pruning) may have inadvertently compromised performance of GPT 4-0613 relative to GPT 3.5-turbo despite being a newer model generation.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@akyonEvaluatingCapabilitiesGenerative2024#TRIPOD-LLM reporting]].

| Metric | GPT 4-0613 | (Comparator) Gemini pro 1.0 | (Top) GPT 3.5-Turbo-1106 |
| --- | :---: | :---: | :---: |
| Total QA pairs | 5850 | 5850 | 5850 |
| Correct (n) | 2580 | 2878 | 3916 |
| Correct (%) | **44.1%** | 49.2% | 66.9% |
| Articles published pre-cutoff | 28/39 (71.8%) | n/a (cutoff undisclosed) | 28/39 (71.8%) |

| Pairwise comparison | Significance |
| --- | --- |
| GPT 4-0613 vs. Gemini pro 1.0 | P<.001 (Gemini pro higher) |
| Overall LLM differences (Kruskal-Wallis) | P<.001 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

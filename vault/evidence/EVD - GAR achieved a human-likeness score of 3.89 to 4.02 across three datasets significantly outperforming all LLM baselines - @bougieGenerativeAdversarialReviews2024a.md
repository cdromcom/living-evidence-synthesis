---
NodeFormality: draft
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/some-concerns
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/37pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b62-72b0-a3fa-eef272cc4231
appraisal_overall: L0-M3-H2
tripod_llm_pct: 37pct
---

## Source

[[@bougieGenerativeAdversarialReviews2024a]]

## Description

> "As shown in Table 7, our method significantly outperforms AI-Scientist in generating reviews that align closely with human feedback. GAR scores are consistently higher, suggesting that the inclusion of graph-based memory and profile modules enhances the human-likeness of reviews." (Bougie & Watanabe, 2024, p. 14)
>
> ![[bougieGenerativeAdversarialReviews2024a-evd-p15-1.png]]
> *Table 7 row for the GAR reviewer agent (values reformatted as inline text):* "GAR: NeurIPS 3.89 ± 0.11\*, ICLR 22 4.02 ± 0.10\*, ICLR 23 3.99 ± 0.09\*" (Bougie & Watanabe, 2024, p. 15, Table 7)
>
> ![[bougieGenerativeAdversarialReviews2024a-evd-table7-p15.png]]

## Methods Context

### What?

> **Study design:** LLM-as-a-judge cross-dataset evaluation of review human-likeness.
>
> **Method type:** zero-shot prompting of GPT-4o to rate, on a 5-point Likert scale, whether each generated review reads as AI-generated or human-like; means ± standard error reported and significance vs. best baseline marked with an asterisk.
>
> **Tools:** GPT-4o evaluator; reviewer agents GAR (GPT-4o-mini backbone in main run), AI-Scientist, OpenReviewer, ReviewerGPT, AI-Review; NeurIPS 2023, ICLR 2022, and ICLR 2023 OpenReview datasets; in §5.11 the same protocol is rerun with GPT-4o, Mistral-7b Instruct, Llama-3.1 (8b), and Llama-3.1 (70b) as GAR backbones.
>
> **Dependent variable:** human-likeness score (1 = AI-generated, 5 = human-like).
>
> **Independent variables:** reviewer type (5 LLM agents) and conference dataset (NeurIPS / ICLR 22 / ICLR 23); foundation LLM in §5.11.
>
> "Specifically, we collect agent-generated reviews and prompted GPT-4o to evaluate whether these reviews were AI-generated or human-like. A 5-point Likert scale was used, where higher scores indicate a stronger resemblance to human reviewers' style and consistency." (Bougie & Watanabe, 2024, pp. 14–15)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p14-1.png]]

### How?

> **Procedure:** for each conference dataset, the five reviewer agents generate reviews on a 1,000-paper subset; GPT-4o is then prompted to score each review on the 1–5 human-likeness scale. Means ± SE are aggregated per (reviewer × dataset) cell and statistical significance over the best baseline is marked with an asterisk (t-test at p<0.05, per the convention used elsewhere in the paper). Each Llama-3.1 (8b) run takes ≈20 minutes on a single NVIDIA A100 40G; all results are averaged over 20 independent runs to ensure reliability and robustness.
>
> "All agents are powered by the GPT-4o-mini version of ChatGPT (OpenAI et al., 2024). In some experiments, we also use the following state-of-the-art LLMs as the backend of reviewer agents: GPT-4o (OpenAI et al., 2024) and Llama-3.1 (8b and 70b) (Grattafiori et al., 2024). … Each run on Llama-3.1 (8b) takes approximately 20 minutes, and all results reported are averaged over 20 independent runs to ensure reliability and robustness of the findings." (Bougie & Watanabe, 2024, p. 9)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p9-2.png]]

### Who?

> **Models:** five reviewer agents (GAR, AI-Scientist, OpenReviewer, ReviewerGPT, AI-Review). GAR's foundation LLM in the main run is GPT-4o-mini; §5.11 (Table 8) repeats with GPT-4o, Mistral-7b Instruct, Llama-3.1 (8b), and Llama-3.1 (70b).
>
> **Sample-size flow / data:** ICLR 2023 = 3,797 OpenReview papers → 1,000-paper evaluation subset; NeurIPS 2023 and ICLR 2022 likewise sampled at 1,000 papers each (the remaining ~2,797 ICLR 23 reviews initialise the memory module per §5.3). All three datasets are scored by GPT-4o. No human evaluators in this experiment.
>
> "We primary conduct the experiments on the ICLR 2023 dataset, which consists of 3,797 papers obtained from Openreview. Each paper was retrieved by at least three reviewers. In some experiments, we also conducted experiments on the ICLR 2022, and NeurIPS 2023 (Beygelzimer et al., 2021) datasets." (Bougie & Watanabe, 2024, p. 9)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p9-3.png]]

## Other Notes

AI-Scientist scores: NeurIPS 3.34 ± 0.09, ICLR 22 3.39 ± 0.11, ICLR 23 3.38 ± 0.08. OpenReviewer: NeurIPS 2.45 ± 0.10, ICLR 22 2.43 ± 0.09, ICLR 23 2.43 ± 0.09. ReviewerGPT: 3.26 / 3.25 / 3.29. AI-Review: 3.30 / 3.42 / 3.38. The §5.11 ablation on GAR backbones (Table 8) shows GPT-4o highest (4.11 ± 0.10 on ICLR 23), GPT-4o-mini close behind (3.99 ± 0.09), and the open Llama-3.1 / Mistral-7b backbones at 3.64–3.73. Authors attribute GAR's lead to the graph-based memory + multi-round refinement + persona modules.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@bougieGenerativeAdversarialReviews2024a#TRIPOD-LLM reporting summary]].

| Reviewer (GPT-4o-mini backbone) | NeurIPS 23 | ICLR 22 | ICLR 23 |
| --- | :---: | :---: | :---: |
| **GAR** | **3.89 ± 0.11\*** | **4.02 ± 0.10\*** | **3.99 ± 0.09\*** |
| AI-Scientist | 3.34 ± 0.09 | 3.39 ± 0.11 | 3.38 ± 0.08 |
| OpenReviewer | 2.45 ± 0.10 | 2.43 ± 0.09 | 2.43 ± 0.09 |
| ReviewerGPT | 3.26 ± 0.13 | 3.25 ± 0.14 | 3.29 ± 0.15 |
| AI-Review | 3.30 ± 0.09 | 3.42 ± 0.11 | 3.38 ± 0.08 |

| GAR foundation LLM (Table 8, ablation) | NeurIPS 23 | ICLR 22 | ICLR 23 |
| --- | :---: | :---: | :---: |
| GPT-4o | 3.91 ± 0.10 | 4.08 ± 0.10 | **4.11 ± 0.10** |
| GPT-4o-mini (main) | 3.89 ± 0.11 | 4.02 ± 0.10 | 3.99 ± 0.09 |
| Mistral-7b Instruct | 3.59 ± 0.08 | 3.67 ± 0.10 | 3.68 ± 0.11 |
| Llama-3.1 (8b) | 3.33 ± 0.08 | 3.64 ± 0.11 | 3.64 ± 0.12 |
| Llama-3.1 (70b) | 3.66 ± 0.09 | 3.63 ± 0.10 | 3.73 ± 0.07 |
| \* over best baseline | t-test p<0.05 | | |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Users find LLM-generated peer-review feedback substantively helpful at rates comparable to human reviewers]]

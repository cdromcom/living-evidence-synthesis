---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/decision-judgment
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
nodeID: 019ddb4e-6b60-7553-8f1e-3b20a48e06fa
appraisal_overall: L0-M3-H2
tripod_llm_pct: 37pct
---

## Source

[[@bougieGenerativeAdversarialReviews2024a]]

## Description

> "Our method outperforms previous state-of-the-art methods, including AI-Scientist (0.54) with an average f1 score of 0.66. This f1 score is significantly higher than the 0.49 achieved by human reviewers in the NeurIPS 2023 consistency study Beygelzimer et al. (2021), as indicated by paired t-tests at 95% confidence level (p < 0.002)." (Bougie & Watanabe, 2024, p. 11)
>
> ![[bougieGenerativeAdversarialReviews2024a-evd-p11-1.png]]

## Methods Context

### What?

> **Study design:** classification benchmark of LLM reviewer agents against ground-truth conference acceptance decisions, repeated across three OpenReview datasets.
>
> **Method type:** binary {ACCEPT, REJECT} prediction at the paper level, GAR's meta-reviewer aggregates individual reviews into a final decision; the GAR^> variant instead applies a fixed score threshold of 6 (ICLR "Weak Accept").
>
> **Tools:** GAR pipeline (graph-paper representation + 3–6 reviewer agents + meta-reviewer) backed by GPT-4o-mini; baselines AI-Scientist, OpenReviewer, ReviewerGPT, AI-Review; trivial baselines (Random Decision, Always Reject); Nougat for PDF→Markdown extraction; Molmo-7b for figure ingestion.
>
> **Dependent variables:** Balanced Accuracy and F1 score per dataset, mean ± SE over 20 runs.
>
> **Independent variables:** reviewer system (7 levels), dataset (NeurIPS 23 / ICLR 22 / ICLR 23), decision rule (meta-reviewer vs. threshold-at-6).
>
> "To evaluate the effectiveness of our LLM-powered review system, we compared its decisions against a ground truth dataset comprised of 1,000 papers from the NeurIPS 23, ICLR 22, and ICLR 23 submissions. The remaining reviews (e.g., 2,797 for ICLR 23) in each dataset were utilized to initialize the memory module." (Bougie & Watanabe, 2024, p. 11)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p11-2.png]]

### How?

> **Procedure:** for each evaluation paper, Nougat extracts MMD-formatted text and Molmo-7b captions are grafted into the manuscript representation. The graph-paper builder runs Acronym Extraction → Core-Element Extraction → Concept Merging → Leiden community detection → community descriptors. 3–6 reviewer agents are instantiated with personas (initialised by historical-data matching in the main run; ablations test random and NN-optimised personas) and given the descriptors. Each reviewer produces an initial review then K rounds of multi-round refinement using retrieved community-level memory. The meta-reviewer synthesises the individual reviews into the final {ACCEPT, REJECT} label after T self-reflection turns. GAR^> instead thresholds the average reviewer score at 6 (≥6 → ACCEPT). All results averaged over 20 independent runs; significance vs. AI-Scientist tested via paired t-test at p<0.05. The human baseline of F1=0.49 is taken from the NeurIPS 2023 consistency experiment (Beygelzimer et al., 2021); paired t-tests confirm GAR's F1=0.66 exceeds it at p<0.002.
>
> "In GAR^>, we set the decision threshold at a score of 6, aligned with the 'Weak Accept' category from ICLR's review standards, and compare this threshold-based reviewers with vanilla GAR. As a result, GAR^> exhibits significantly superior performance compared to GAR." (Bougie & Watanabe, 2024, p. 12)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p12-1.png]]

### Who?

> **Models:** seven systems compared per dataset, Human (NeurIPS 2023 consistency study), Random Decision, Always Reject, AI-Scientist, OpenReviewer, ReviewerGPT, AI-Review, plus GAR and GAR^>. All LLM-based agents use GPT-4o-mini in the main run; §5.12 (Table 9) repeats with GPT-4o, Mistral-7b Instruct, Llama-3.1 (8b), and Llama-3.1 (70b).
>
> **Sample-size flow / data:** ICLR 2023 = 3,797 OpenReview papers → 1,000-paper evaluation set + remaining ~2,797 used to initialise the memory module. NeurIPS 2023 and ICLR 2022 likewise sampled at 1,000 papers each → total 3,000 evaluation papers. Each paper retrieved by ≥3 reviewers in the source dataset; ground truth = official conference accept/reject decisions. Each reported cell is the mean ± SE over 20 independent runs.
>
> "Each run on Llama-3.1 (8b) takes approximately 20 minutes, and all results reported are averaged over 20 independent runs to ensure reliability and robustness of the findings." (Bougie & Watanabe, 2024, p. 9)
> ![[bougieGenerativeAdversarialReviews2024a-evd-p9-1.png]]

## Other Notes

GAR^> achieved F1 = 0.62 ± 0.05 on NeurIPS 23 (vanilla GAR 0.61 ± 0.04); on ICLR 23 GAR^> reached Balanced Accuracy 0.70 ± 0.05 and F1 0.69 ± 0.05. AI-Scientist sat at 0.51–0.57 F1 across datasets; OpenReviewer 0.39–0.47. The §5.4 ablation (Table 4) shows the persona-initialisation choice matters: NN-optimised persona pushes ICLR 23 Balanced Acc to 0.74 ± 0.06 (GAR^> 0.74 ± 0.06 / F1 0.70 ± 0.06); removing the memory module drops it to 0.61 ± 0.06 / 0.52 ± 0.05. §5.12 (Table 9) shows GPT-4o backbone reaches F1 0.73 ± 0.03 on ICLR 23 (GAR^> 0.71 ± 0.03), confirming GAR's gains are robust across foundation models.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@bougieGenerativeAdversarialReviews2024a#TRIPOD-LLM reporting]].

| Method (GPT-4o-mini) | NeurIPS 23 BalAcc / F1 | ICLR 22 BalAcc / F1 | ICLR 23 BalAcc / F1 |
| --- | :---: | :---: | :---: |
| Human\* | 0.66 / 0.49 | 0.66 / 0.49 | 0.66 / 0.49 |
| Random Decision | 0.50 / 0.33 | 0.50 / 0.50 | 0.50 / 0.40 |
| Always Reject | 0.50 / 0.00 | 0.50 / 0.38 | 0.50 / 0.00 |
| AI-Scientist | 0.58 ± 0.04 / 0.51 ± 0.05 | 0.65 ± 0.04 / 0.57 ± 0.05 | 0.63 ± 0.05 / 0.55 ± 0.06 |
| OpenReviewer | 0.39 ± 0.05 / 0.39 ± 0.04 | 0.49 ± 0.05 / 0.47 ± 0.05 | 0.50 ± 0.04 / 0.45 ± 0.05 |
| ReviewerGPT | 0.41 ± 0.06 / 0.40 ± 0.05 | 0.54 ± 0.06 / 0.52 ± 0.05 | 0.55 ± 0.07 / 0.51 ± 0.05 |
| AI-Review | 0.59 ± 0.04 / 0.49 ± 0.05 | 0.64 ± 0.06 / 0.61 ± 0.06 | 0.55 ± 0.04 / 0.53 ± 0.07 |
| GAR | 0.64 ± 0.05 / 0.61 ± 0.04 | 0.68 ± 0.03 / **0.66 ± 0.05** | 0.66 ± 0.04 / 0.60 ± 0.04 |
| **GAR^>** | **0.68 ± 0.05 / 0.62 ± 0.05** | **0.71 ± 0.04 / 0.67 ± 0.06** | **0.70 ± 0.05 / 0.69 ± 0.05** |
| Significance (GAR vs. AI-Scientist) | t-test p<0.05 | t-test p<0.05 | t-test p<0.05 |
| Significance (GAR vs. Human F1=0.49) | paired t-test p<0.002 | paired t-test p<0.002 | paired t-test p<0.002 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM-based peer review agents equipped with memory and persona modules can match or exceed human reviewer quality in providing feedback and predicting paper acceptance]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM peer-review systems can predict paper acceptance and preference at near-human accuracy]]

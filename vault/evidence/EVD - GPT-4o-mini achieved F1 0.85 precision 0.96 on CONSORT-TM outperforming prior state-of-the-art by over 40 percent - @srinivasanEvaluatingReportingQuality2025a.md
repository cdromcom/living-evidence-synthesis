---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/50pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b71-7471-9058-2b680238dd60
appraisal_overall: L0-M3-H2
tripod_llm_pct: 50pct
---

## Source

[[@srinivasanEvaluatingReportingQuality2025a]]

## Description

> "All GPT models with our prompting scheme substantially outperformed the previous state-of-the-art on CONSORT-TM by over 40% [Damen et al., 2023]. GPT-4 achieved the highest F1 score (0.89) and strong precision (0.93). GPT-4o maintained strong precision (0.94) with a slightly lower F1 score (0.85), while GPT-4o-mini demonstrated the highest precision (0.96) with equivalent F1 performance (0.85). Given its balance of accuracy and computational efficiency, we selected GPT-4o-mini as our deployment model." (Srinivasan et al., 2025, p. 5)
>
> ![[srinivasanEvaluatingReportingQuality2025a-table1-p5-1.png]]

## Methods Context

### What?

> **Study design:** zero-shot LLM benchmark on the CONSORT-TM evaluation corpus (Kilicoglu et al. 2021), with a downstream human-expert validation sub-study.
>
> **Method type:** zero-shot prompting of OpenAI GPT models to perform binary (MET / NOT MET) classification of each CONSORT criterion against full RCT text.
>
> **Tools:** OpenAI GPT-4 (GPT-4-turbo), GPT-4o, GPT-4o-mini accessed via a HIPAA-compliant Azure instance; JSON-structured prompt template; comparison baseline = Lan Jiang et al. (2024) zero-shot GPT-4 result on the same corpus.
>
> **Dependent variables:** binary-classification accuracy, precision, recall, F1, micro-F1 per model.
>
> **Independent variable:** model identity (GPT-4-turbo / GPT-4o / GPT-4o-mini); fixed prompt template across models.
>
> "We evaluated the ability of our LLMs to determine whether an RCT article met or did not meet a set of inclusion criteria for each of the 25 CONSORT items. The models were assessed based on their performance across standard binary classification metrics, including precision, recall, and both macro and micro F1 scores." (Srinivasan et al., 2025, p. 4)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p4-3.png]]

### How?

> **Procedure:** for each (article, criterion) pair, the entire article text was fed into the model with a single prompt that contains a task instruction + the criterion definition (template: "#Task Your task is to assess whether the given article meets the specified CONSORT criteria. # Article {article} # CONSORT Criterion The criterion being assessed is: {criterion} {definition}"). Each criterion was assessed independently — the model was re-prompted C times per article (where C = number of CONSORT criteria). Output: a JSON string with four fields — Criterion, Rationale (chain-of-thought reasoning), Decision (MET / NOT MET), Confidence (Low / Medium / High). Predictions were stratified by self-reported confidence; only High-confidence predictions were retained for the deployment analysis. Performance computed against CONSORT-TM gold sentence-level annotations and compared head-to-head with the Damen et al. / Lan Jiang et al. baseline. Inference settings (temperature, top_p, system prompt) not reported.
>
> "To extract methods-related CONSORT checklist items from RCT reports for this study, we consider OpenAI's proprietary models GPT-4, GPT-4o and GPT-4o-mini. We run the GPT models via a secure Azure PHI-compliant instance… Each criterion was assessed independently for every article. For each criterion, the entire article content was fed into the model, and the assessment was conducted one criterion at a time. As a result, the model must be prompted with the same article C times, where C is the number of criteria." (Srinivasan et al., 2025, p. 4)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p4-4.png]]

### Who?

> **Models evaluated:** GPT-4-turbo, GPT-4o, GPT-4o-mini (zero-shot). Comparison baseline: Lan Jiang et al. (2024) prior state-of-the-art on CONSORT-TM. No model fine-tuning.
>
> **Evaluation corpus:** CONSORT-TM (Kilicoglu et al. 2021) — 50 RCT publications annotated at the sentence level against 37 CONSORT checklist items by six annotators (paired annotation of 30 articles, sentence-level Krippendorff's α = 0.57). Item 2a Background was excluded as too broad. Public at github.com/ScienceNLP-Lab/RCT-Transparency. All 50 articles were used for the zero-shot benchmark.
>
> **Human expert validation sub-study:** 4 experts (1 clinician, 3 data scientists) manually rated GPT-4o-mini outputs on 50 randomly selected articles as Correct / Partially Correct / Incorrect (used to substantiate the deployment-model choice; not the benchmark numbers themselves).
>
> "For model evaluation, we used a previously curated dataset called the CONSORT-TM corpus [Kilicoglu et al. 2021] for this study. It consists of 50 RCT publications annotated at the sentence level with 37 CONSORT checklist items… Six annotators independently annotated 30 articles in pairs, and the calculated Krippendorff's α to measure inter-annotator agreement at the sentence level was 0.57." (Srinivasan et al., 2025, p. 3)
> ![[srinivasanEvaluatingReportingQuality2025a-evd-p3-2.png]]

## Other Notes

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@srinivasanEvaluatingReportingQuality2025a#TRIPOD-LLM reporting summary]].

| Model | Accuracy | Precision | Recall | F1 | Micro-F1 |
| --- | :---: | :---: | :---: | :---: | :---: |
| GPT-4-turbo | 0.84 | 0.93 | 0.85 | **0.89** | 0.84 |
| GPT-4o | 0.80 | 0.94 | 0.79 | 0.85 | 0.80 |
| **GPT-4o-mini (deployed)** | **0.81** | **0.96** | 0.77 | **0.85** | **0.81** |
| Lan Jiang et al. (prior SOTA) | — | 0.48 | 0.54 | 0.51 | 0.49 |

| Confidence-stratified GPT-4o-mini performance | Accuracy | Precision | Recall | F1 | Micro-F1 |
| --- | :---: | :---: | :---: | :---: | :---: |
| High confidence (kept) | 0.92 | 0.97 | 0.92 | **0.95** | 0.92 |
| Medium confidence (excluded from deployment analysis) | 0.41 | 0.85 | 0.19 | 0.31 | 0.42 |

| Human expert validation (n=50 articles, GPT-4o-mini) | % |
| --- | :---: |
| Correct | 83.42% |
| Partially correct | 8.82% |
| Incorrect | 7.76% |
| Combined Correct + Partially correct (cited in abstract as "agreement") | 92.24% |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can achieve state-of-the-art CONSORT compliance assessment performance through zero-shot prompting at scale]]

- [[CLM - RCT reporting quality has improved substantially over decades but critical methodological gaps persist across all disciplines]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]

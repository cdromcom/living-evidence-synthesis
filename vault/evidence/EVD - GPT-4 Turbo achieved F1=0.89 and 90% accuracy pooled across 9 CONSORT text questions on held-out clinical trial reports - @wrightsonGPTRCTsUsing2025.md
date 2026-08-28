---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L1-M2-H2
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/64pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b67-7718-805f-eff5bfc1e3cc
appraisal_overall: L1-M2-H2
tripod_llm_pct: 64pct
---

## Source

[[@wrightsonGPTRCTsUsing2025]]

## Description

> "Pooled across all questions and papers in the TEST dataset, the GPT-4 Turbo AI-LLM demonstrated acceptable performance (F1-score=0.89, accuracy (95% CI) = 90% (85% to 94%))." (Wrightson et al., 2025, p. 5)
>
> ![[wrightsonGPTRCTsUsing2025-gpt4-results-p5-1.png]]

## Methods Context

### What?

> **Study design:** exploratory retrospective cross-sectional benchmark of a closed-source LLM against human-labeled CONSORT-adherence ground truth from a published systematic review.
>
> **Method type:** zero-shot generative question-answering with prompt-engineered system + user prompts (no fine-tuning of the GPT-4 model — authors explicitly note GPT-4 fine-tuning was unavailable to them at the time).
>
> **Tools:** OpenAI GPT-4 Turbo (temperature=0.2, Top P=0.2, response capped at 512 tokens); R 4.3.2 + Python 3.8.17 for analysis; Schulz et al. 2020 sports-medicine CONSORT-adherence dataset as ground truth.
>
> **Dependent variables:** F1-score (primary); classification accuracy (%) with 95% Clopper–Pearson CIs (secondary), pooled across all 9 text-analysis questions × all TEST papers, and reported per-question (Table 2).
>
> **Independent variables / covariates:** the 9 CONSORT reporting-guideline items (study hypotheses; primary outcome; sample size; eligibility; randomisation implementation; randomisation methods; allocation/enrolment roles; blinding; standardised effect sizes & CIs); paper section (Introduction / Method / Results, used as the stratification variable for the train/test split).
>
> "For the GPT-4 analysis, we used the following hyperparameter settings: temperature=0.2 and Top P=0.2. Unfortunately, at the time of this analysis, we did not have access to fine-tune the GPT-4 model. Model tuning in our study was achieved through iterative 'prompt engineering'." (Wrightson et al., 2025, p. 4)
> ![[wrightsonGPTRCTsUsing2025-evd-p4-3.png]]

### How?

> **Procedure:** (1) Subsample full-text articles from Schulz et al. 2020 (which assessed 160 sports-medicine RCTs in 2020 against CONSORT items); extract text from PMC (n=24 open-access) or from publisher EPUB/PDF; exclude papers with extraction errors or inaccessible files. (2) Split each paper into Introduction / Method / Results sections (because Llama 2 context window could not fit whole papers — same split used for GPT-4 for comparability). (3) For each paper, build 9 (paper-section text, CONSORT question) pairs — for question 9 (effect sizes), Method + Results are concatenated; this question is dropped for Llama 2 due to the smaller context window. (4) Randomly split text–question pairs 80% TRAIN / 20% TEST, stratified by paper section so a single paper can appear in both splits via different sections (no validation set due to limited data). (5) Iteratively engineer system + user prompts: start from OpenAI guidelines (persona + delimiters + step-list); use the first 10 incorrectly-answered TRAIN examples to ask ChatGPT to revise prompt language; rerun and revise once more; copy ChatGPT-suggested prompt verbatim. The final system prompt instructs the model to summarise relevant text first, then answer YES/NO. (6) Submit each TEST text-question pair to GPT-4 Turbo via the OpenAI API; compare returned YES/NO against Schulz et al. labels. (7) Compute F1, accuracy, and 95% Clopper–Pearson CIs in R; build the confusion matrix in Figure 1. The work was reported in line with the MI-CLAIM checklist (filed on OSF).
>
> "Each reporting guideline item of each paper was assessed for adherence using a generative question and answering format, where the model was prompted to answer a question, formulated using natural language, about the text/image extracted from each paper. The model was required to summarise the text that was relevant to the question and answer YES or NO to the question. Each question corresponded to a variable from the labelled dataset by Schulz et al. The label ('ground truth') for each question ('YES' or 'NO') was extracted from the systematic analysis by Schulz et al." (Wrightson et al., 2025, p. 4)
> ![[wrightsonGPTRCTsUsing2025-evd-p4-4.png]]

### Who?

> **Models / participants:** the system under test is OpenAI **GPT-4 Turbo** (closed-source; OpenAI training data and exact snapshot date not disclosed by the authors). No human raters in this EVD beyond Schulz et al.'s pre-existing labels.
>
> **Sample-size flow (text analysis):** Schulz et al. 2020 base set = 160 peer-reviewed sports-medicine clinical trial papers from 2020 → restrict to full-text-available PMC/EPUB/PDF and exclude extraction errors → **113 papers** retained → for each paper, 9 (text, question) pairs constructed (n=113 for items 1, 9; n=108 for items 2–8 because some papers lacked relevant sections; per-item totals in Table 1) → split 80/20 TRAIN/TEST stratified by paper section; the **20% TEST split is the analysis set** for the headline F1 = 0.89 (no validation set; "we did not create a validation data set because of the relatively low number of training examples"). The pooled-confusion matrix in Figure 1 contains 198 cells (84 true-YES, 7 false-NO, 94 true-NO, 13 false-YES).
>
> "We used a subsample of the dataset provided by Schulz et al. In their systematic review, Schulz et al analysed the reporting practices, including items from the CONSORT checklist, of 160 peer-reviewed scientific papers published in sports medicine journals in 2020 … We extracted all papers from the Schulz et al dataset that were available in full-text machine-readable format … Papers were removed from analysis if (a) the text extraction contained errors or (b) the electronic file was inaccessible." (Wrightson et al., 2025, p. 2)
> ![[wrightsonGPTRCTsUsing2025-evd-p2-2.png]]

## Other Notes

- The 113-paper figure is the per-paper denominator; the actual classification denominator for the headline F1 is the pooled 20% TEST split of (paper-section, question) pairs — Figure 1's confusion matrix shows 198 instances.
- Item 8 (blinding) reaches the highest accuracy (100%, 95% CI 87% to 100%, F1 = 1.00); item 9 (standardised effect sizes & CIs) the lowest F1 (0.57; accuracy 87%) — likely because effect-size reporting is rare (Schulz et al. adherence = 20%) and the question requires combining Method + Results text.
- Authors flag possible **data leakage**: the same paper can appear in both TRAIN and TEST via different sections, since the split was stratified by section to keep section-mix constant across splits. They warn this may have inflated TEST performance.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@wrightsonGPTRCTsUsing2025#TRIPOD-LLM reporting summary]].

| CONSORT question (text analysis) | F1-score | Accuracy (95% CI) |
| --- | :---: | :---: |
| **Pooled across Q1–Q9 (TEST)** | **0.89** | **90% (85% to 94%)** |
| Q1. Study hypotheses | 0.86 | 83% (63% to 93%) |
| Q2. Primary outcome / endpoint | 0.91 | 89% (73% to 96%) |
| Q3. Sample size determination | 0.92 | 90% (71% to 97%) |
| Q4. Eligibility criteria | 0.89 | 86% (67% to 95%) |
| Q5. Randomisation implementation | 0.95 | 94% (72% to 99%) |
| Q6. Randomisation methods | 0.91 | 94% (73% to 99%) |
| Q7. Allocation / enrolment roles | 0.84 | 86% (67% to 95%) |
| Q8. Blinding | 1.00 | 100% (87% to 100%) |
| Q9. Standardised effect sizes & CIs | 0.57 | 87% (68% to 95%) |

| Per-paper accuracy range (TEST) | Per-question item adherence range (Schulz et al.) |
| --- | --- |
| 0% to 100% | 20% (effect sizes) to 77% (eligibility) |

| Confusion matrix (Figure 1, pooled TEST) | Predicted YES | Predicted NO |
| --- | :---: | :---: |
| **Actual YES** | 84 | 13 |
| **Actual NO** | 7 | 94 |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The study used only sports medicine and orthopaedic journal papers limiting generalizability to other medical fields]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can assess clinical trial reporting guideline adherence with acceptable accuracy approaching 90%]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]

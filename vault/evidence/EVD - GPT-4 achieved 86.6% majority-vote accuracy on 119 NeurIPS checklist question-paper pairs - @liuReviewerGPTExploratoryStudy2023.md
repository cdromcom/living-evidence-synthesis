---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
  - forensic/reproduction-check/match
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/36pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b6a-7323-b0e4-5812004cd33d
appraisal_overall: L0-M3-H2
tripod_llm_pct: 36pct
---

## Source

[[@liuReviewerGPTExploratoryStudy2023]]

## Description

> "We found that across 119 unique {checklist question, paper} pairs, (i) taking the majority answer over 3 responses, the LLM achieved 86.6% accuracy compared to the ground truth label; (ii) coincidentally, 86.6% of author responses matched our ground truth label; (iii) LLM answers disagreed with 75% of mismatched author responses, and (iv) 50% of the LLM's errors were due to questions where the answers were undeterminable with the text in the paper (e.g., requiring information provided in figures)." (Liu & Shah, 2023, p. 2)
>
> ![[liuReviewerGPTExploratoryStudy2023-quote-checklist-desc-p2.png]]

## Methods Context

### What?

> **Study design:** cross-sectional zero-shot LLM evaluation against hand-labeled ground truth.
>
> **Method type:** majority-vote (3 responses) GPT-4 prompting on each {checklist question, paper-section} pair, scored against manual labels by a CS graduate student.
>
> **Tools:** GPT-4 (8k context, OpenAI API `gpt-4` model, accessed 5/20/23–5/23/23, default `temperature=1.0`, `top_p=1.0`); NeurIPS 2022 author-checklist (16 of 18 questions); paper sections from OpenReview NeurIPS 2022 (accepted + opt-in rejected).
>
> **Dependent variable:** GPT-4 majority-vote accuracy across 119 pairs vs. hand-labeled ground truth (Yes / No / N/A).
>
> **Independent variables / covariates:** checklist-question category (5 categories); paper.
>
> "We queried GPT-4 for three responses per {question, paper} pair, taking the majority vote as the answer and evaluating its correctness against the ground truth label. If all three responses were different, we marked the answer as incorrect. In Table 2 we provide the results for our checklist experiment. We found that compared to the hand-labeled ground truth, GPT-4 achieves 86.6% accuracy across 119 examples." (Liu & Shah, 2023, p. 28)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p28-1.png]]

### How?

> **Procedure:** (1) Sampled 15 NeurIPS 2022 papers from OpenReview — 10 by uniform sampling, 5 manually retrieved to cover the crowdsourcing/human-subjects checklist category; all post-dated GPT-4 training cutoff. (2) For each paper retained 16 of 18 checklist questions where ground truth could be determined; only items the authors had answered "Yes" were kept (since the task was to verify "Yes" answers), yielding 119 unique {question, paper} pairs. (3) First author (CS graduate student) hand-labeled each pair via keyword search + full scan, cross-checked against the author-submitted answer (deferring to authors when unsure), and re-labeled all questions a second time for calibration. (4) Constructed prompts: a system prompt assigning the model a "computer science researcher reviewing a paper titled [title] for the NeurIPS computer science conference" role + a user prompt providing the relevant paper section(s) (per token-budget) + the checklist question rephrased into third-person, asking for a Yes/No/N/A answer with a brief justification. (5) Hyperparameters chosen via pilot on a separate NeurIPS paper, sweeping `temperature ∈ {0, 0.1, …, 2.0}` and `top_p ∈ {0, 0.1, …, 1.0}`; (1.0, 1.0) marginally best. (6) Queried GPT-4 three times per pair, took majority vote (mark incorrect if all three responses differed).
>
> "Throughout our experiments, for the LLM, we used the standard GPT-4 model with 8k tokens for the context. Due to limits on the token count, we were not able to pass in entire papers to the model. Instead, for each {question, paper} pair, we selected the section(s) in the paper that best correspond to each question, and only provided those section(s) in the prompt." (Liu & Shah, 2023, p. 28)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p28-2.png]]

### Who?

> **Models / participants:** GPT-4 (`gpt-4`, OpenAI API, 8k context, accessed May 20–23 2023). No human subjects; the units of analysis are {checklist question, paper} pairs.
>
> **Sample-size flow:**
> - NeurIPS 2022 OpenReview papers (accepted + opt-in rejected) → uniform sample of 10 + 5 hand-picked to cover crowdsourcing/human-subjects category → **15 papers retained**.
> - 18 NeurIPS 2022 checklist questions per paper → 16 with ground-truth-determinable items → **240 candidate pairs** (15 × 16).
> - Restricted to items where authors had answered "Yes" (the verification target) → **119 unique {question, paper} pairs analyzed**.
> - Each pair queried 3× and majority-voted → 1 accuracy score per pair.
>
> **Annotator:** 1 CS graduate student (first author), with prior NeurIPS publication and experience as workflow chair at a top CS conference.
>
> "We selected 15 papers from the NeurIPS 2022 conference OpenReview platform… We first select 10 papers using simple uniform sampling, and five additional papers were retrieved manually to cover the lack of crowdsourcing/human-subject papers, which correspond to the fifth category of questions in the checklist. The papers we selected were published in NeurIPS after the GPT-4 training data cutoff, so it is unlikely that the model had previously seen their checklists." (Liu & Shah, 2023, p. 27)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p27-1.png]]
>
> Note: the paper inconsistently writes "NeurIPS 2022" (Section 4.1 Papers) and "NeurIPS 2023" (p. 2 abstract); 2022 is correct given the May 2023 GPT-4 query window and the OpenReview link.

## Other Notes

- 50% of LLM errors were on questions whose answers required information in figures — a structural limitation of text-only prompting. Removing those questions raised GPT-4 accuracy to 92.8%.
- Author-submitted checklists also matched the ground truth 86.6% of the time, but mismatches barely overlapped: GPT-4 disagreed with 75% (12 of 16) of author mismatches; conversely 9 of 16 (56.3%) of GPT-4's incorrect answers had correct author responses.
- Per-paper accuracy in Table 2 (15 papers) ranges 0.57–1.00; per-question accuracy across 16 items ranges 0.63–1.00.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liuReviewerGPTExploratoryStudy2023#TRIPOD-LLM reporting summary]].

| Metric | Value |
| --- | --- |
| Pairs analyzed (N) | 119 unique {checklist question, paper} pairs |
| GPT-4 majority-vote accuracy | **86.6%** |
| Author-checklist accuracy (same ground truth) | 86.6% |
| GPT-4 vs. author disagreement on mismatched author items | 75% (12 of 16) |
| GPT-4 incorrect items where author answer was correct | 56.3% (9 of 16) |
| Errors due to figure-only evidence | 50% of GPT-4's errors |
| Accuracy excluding figure-only items | 92.8% |
| Per-paper accuracy range (Table 2, 15 papers) | 0.57 – 1.00 |
| Per-question accuracy range (Table 2, 16 items) | 0.63 – 1.00 |

## Reproduction check

> [!success] Analytic reproducibility: MATCH (2026-08)
> Independently recomputed from the authors' own released raw data
> (`labels.xlsx`, github.com/niharshah/ReviewerGPT2023) rather than from
> the paper's stated numbers: summing the spreadsheet's own per-paper
> "total accurate" / "total" columns gives 206/238 = **86.55%**, against
> the paper's stated **86.6%** — an exact match within rounding. No LLM
> re-run was needed; the per-pair correctness was already recorded in the
> released file.

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Checklist ground truth relied on author-stated responses rather than independent verification]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs show promise for targeted reviewing subtasks but are not yet capable of functioning as standalone peer reviewers]]

- [[CLM - Targeted question prompting elicits substantially better LLM performance than open-ended review generation]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLMs achieve high accuracy on structured presence-absence checklist verification]]

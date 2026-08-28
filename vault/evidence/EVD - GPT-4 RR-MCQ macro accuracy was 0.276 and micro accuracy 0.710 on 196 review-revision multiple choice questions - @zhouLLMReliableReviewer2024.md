---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M4-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/43pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b65-72ac-a24a-a1280c3e37eb
appraisal_overall: L0-M4-H1
tripod_llm_pct: 43pct
---

## Source

[[@zhouLLMReliableReviewer2024]]

## Description

> "the best micro accuracy 0.710 comes from the GPT-4 -> GPT-4 method. It is a passable score, but the macro accuracy is only 0.276." (Zhou et al., 2024, p. 9346)
>
> ![[zhouLLMReliableReviewer2024-evd-p7-1.png]]
>
> GPT-4→GPT-4: macro acc=0.276, micro acc=0.710, F1=0.330 (Table 7, p. 9346)

## Methods Context

### What?

> **Study design:** zero-/few-shot LLM evaluation on a newly constructed benchmark (RR-MCQ), with the LLM as the system under test rather than the rater.
>
> **Method type:** two-step prompted multiple-choice question answering — (1) section-selection step, then (2) answer-prediction step over A/B/C/D options where one or more options can be correct.
>
> **Tools:** OpenAI **GPT-3.5-turbo-0613** and **GPT-4-0613**; the authors' own RR-MCQ dataset (released at huggingface.co/datasets/zhouruiyang/RR-MCQ); inputs drawn from full ICLR-2023 papers and their review-rebuttal forum threads.
>
> **Dependent variables:** **macro accuracy** (a question is correct only if the predicted option set exactly equals the gold option set), **micro accuracy** (each of the 4 options is treated as a binary True/False decision), plus per-class precision, recall, F1, and per-aspect breakdowns (soundness, clarity, empirical, method, explain, add, no-need, need; Table 8).
>
> **Independent variables:** model identity for each of the two pipeline steps (GPT-3.5→GPT-3.5, GPT-4→GPT-3.5, GPT-4→GPT-4); review-aspect / content-aspect / ability / extra-info label categories.
>
> "Our RR-MCQ dataset is targeted for a more specific and in-depth assessment. For example, can models evaluate the soundness of argumentation? Can they integrate domain knowledge and the paper together? Can they give complicated suggestions, such as important experiments to do?" (Zhou et al., 2024, p. 9345)
> ![[zhouLLMReliableReviewer2024-evd-p6-1.png]]

### How?

> **Procedure:** (1)
>
> **Dataset construction (4 steps):** select 55 reviews from 14 ICLR-2023 papers with sufficient comment-response posts; align comment-response into a single argument; identify the main topic and skip controversial arguments; transform into a 4-option MCQ "without adding new contents" (wrong options are negations or come from irrelevant parts of the same discussion); label the assessed aspects. (2)
>
> **Labelling:** two experienced graduate students annotate aspect labels along 4 dimensions (review aspect, content aspect, ability, if-need-info-from-other-papers); 86/788 labels (10.9%) had initial disagreement, resolved by discussion. (3)
>
> **Two-step inference (Appendix A.3 prompts):** Step 1 — given the question and section headings, model selects useful sections (system prompt: "you will be given a multiple choice question and the headings of a research paper… select sections that are useful to answer the question"). Step 2 — given the selected sections, model answers the MCQ ("you should select one or more answer choices from A, B, C, D"). (4) **Option order randomly shuffled** during evaluation. (5) Three pipeline configurations evaluated: GPT-3.5→GPT-3.5, GPT-4→GPT-3.5, **GPT-4→GPT-4** (Table 7). (6) Inference parameters carry over from Section 3 ("If not specially marked, all models are of version 0613 with temperature 0.3"). (7) Top 2 most-numerous labels per category reported in Table 8 detailed results.
>
> "We test both GPT-3.5-turbo-0613 and GPT-4-0613 on our MCQ data. The two-step generation method is similar to that of Section 4: the model selects useful sections based on the given question, then the selected contents are input into the model to predict multiple-choice answers. Note that our multiple-choice questions may have more than one correct answer." (Zhou et al., 2024, p. 9346)
> ![[zhouLLMReliableReviewer2024-evd-p7-2.png]]

### Who?

> **Models / participants:** GPT-3.5-turbo-0613 and GPT-4-0613 (OpenAI; closed-source).
>
> **Annotators:** two experienced graduate students in the domain.
>
> **Sample-size flow for this EVD:** ICLR-2023 conference → 14 papers with sufficient comment-response posts in the peer-review forum → 55 reviews selected → manually distilled into **196 multiple-choice questions** (4 options each). **788 aspect labels** assigned across the 196 questions (4 label-category dimensions × 196 questions = 784 expected, paper reports 788). 86/788 (10.9%) labels disagreed at first; final labels via consensus discussion. All 196 MCQs evaluated by all three pipeline configurations; no exclusions reported.
>
> "To construct the MCQ test dataset, we select 55 reviews from 14 papers with sufficient comment-response posts in the peer review forum from the ICLR-2023 conference." (Zhou et al., 2024, p. 9345)
> ![[zhouLLMReliableReviewer2024-evd-p6-2.png]]

## Other Notes

Macro accuracy (0.276) means only ~28% of questions were answered completely correctly. The task requires both logic reasoning and domain knowledge.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@zhouLLMReliableReviewer2024#TRIPOD-LLM reporting summary]].

| Pipeline (step1 → step2) | Macro acc ↑ | Macro prec | Macro recall | Macro F1 | Micro acc ↑ | Micro prec | Micro recall | Micro F1 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| GPT-3.5 → GPT-3.5 | 0.128 | 0.332 | 0.376 | 0.176 | 0.569 | 0.583 | 0.373 | 0.227 |
| GPT-4 → GPT-3.5 | 0.214 | 0.553 | 0.586 | 0.285 | 0.648 | 0.644 | 0.603 | 0.311 |
| **GPT-4 → GPT-4** | **0.276** | **0.655** | **0.666** | **0.330** | **0.710** | 0.699 | **0.701** | **0.350** |

| GPT-4→GPT-4, per-aspect macro accuracy (top-2 labels per category) | Soundness | Clarity | Empirical | Method | Explain | Add | No-need | Need |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Macro acc | 0.193 | 0.361 | 0.253 | 0.309 | **0.364** | 0.153 | 0.291 | 0.256 |
| Macro recall | 0.673 | 0.509 | 0.695 | 0.654 | 0.626 | 0.757 | 0.647 | 0.691 |

(Source: Tables 7 and 8, p. 9346–9347. Lowest macro accuracy on **[Soundness]** and **[Add]** questions, which require strong logic + domain knowledge.)

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The Zhou RR-MCQ dataset was constructed from only 14 ICLR papers limiting diversity and scale]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Current LLMs are not yet qualified as reliable automatic reviewers for scientific papers]]

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]

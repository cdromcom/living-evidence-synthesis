---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/novelty-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/41pct
  - 5c/creativity
  - forensic/f1-check/discrepancy
  - forensic/kappa-check/in-bounds
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b52-7182-bd9d-7c2686f81bb7
appraisal_overall: L0-M2-H3
tripod_llm_pct: 41pct
---

## Source

[[@shahidLiteratureGroundedNoveltyAssessment2025]]

## Description

> "Our approach achieved over 10 times more agreement with expert-labeled examples compared to AI Scientist, and approximately 13% higher agreement than AI Researcher." (Shahid et al., 2025, p. 7)
>
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-1.png]]
> AI Scientist results from Table 1: Accuracy=0.47, Precision=0.55, Recall=0.53, F1=0.44, Cohen's Kappa=0.05. (Shahid et al., 2025, p. 7)
> [Screenshot: Table 1, p. 7 — "Other Novelty Checkers" section]

## Methods Context

### What?

> **Study design:** comparative few-shot LLM evaluation — head-to-head benchmark of an external novelty-checker prompt (AI Scientist; Lu et al.) against the Idea Novelty Checker on the same expert-annotated test set.
>
> **Method type:** prompt-only swap (the AI Scientist prompt was lifted from its paper reviewer module and run on a fixed set of input idea + top-10 retrieved papers).
>
> **Tools:** AI Scientist's novelty-evaluation prompt (originally designed for use with the Semantic Scholar API and an iterative search loop); same gpt-4o backbone where applicable; AI Researcher (Si et al.) included as a third comparison system, evaluated with both gpt-4o and Claude-3.5-Sonnet.
>
> **Dependent variables:** binary novelty classification metrics on the 32-idea test set — accuracy, precision, recall, F1, Cohen's κ vs. expert labels.
>
> **Independent variables:** novelty-checker system identity (Idea Novelty Checker vs. AI Scientist vs. AI Researcher); for AI Researcher, backbone LLM (gpt-4o vs. Claude-3.5-Sonnet).
>
> "In addition to these baselines, we also compare our novelty checker 'prompt' with that of AI Scientist (Lu et al.) (different from its paper reviewer) and AI Researcher (Si et al.) on the same test set of ideas and fixed top 10 papers. We compare only the prompts to assess novelty of these two approaches with ours, rather than the entire system, because the test set containing the novelty judgments by experts were based on a fixed set of the 10 most relevant papers for each idea." (Shahid et al., 2025, p. 5)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p5-1.png]]

### How?

> **Procedure:** to ensure a fair prompt-only comparison, the test ideas were standardized to a fixed set of the 10 most relevant papers per idea (the same papers used to elicit expert judgments) and the input idea was reformatted to match each system's expected idea-input style. AI Scientist's full system normally generates Semantic Scholar queries iteratively, compares an idea against retrieved papers up to a preset iteration limit, and reaches a decision via string-matching on phrases like "decision made: novel" / "decision made: not novel"; if no decision string appears, the idea is **automatically classified as "not novel"** by default. In Shahid et al.'s evaluation, AI Scientist's default-to-"not novel" behavior triggered on **18 / 32 test ideas** (failure to reach a conclusion within the prompt). AI Researcher uses a Swiss-system tournament ranking that compares ideas pairwise against individual papers for similarity and novelty; if any single comparison reaches "sufficient similarity" the idea is marked not novel. Standard binary classification metrics (accuracy/precision/recall/F1/κ) computed against expert labels.
>
> "It is important to note that AI Scientist defaults to 'not novel' when it fails to reach a conclusion in novelty evaluation (18 out of 32 times), which may have impacted its agreement rates." (Shahid et al., 2025, p. 7)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-6.png]]

### Who?

> **Models / systems compared:** **AI Scientist** (Lu et al.) novelty-evaluation prompt; **AI Researcher** (Si et al.) novelty-evaluation prompt evaluated with both gpt-4o and Claude-3.5-Sonnet; **Idea Novelty Checker** (this paper) with the best gpt-4o + 15 expert-labeled in-context-example configuration.
>
> **Test data flow:** identical to the main Idea Novelty Checker evaluation — formative-study pool of 51 ideas (34 Scideator + 17 OpenReview ICLR'22/NeurIPS'23) → 67 binary-consensus-labeled ideas (39 novel / 28 not novel) → balanced split → **32-idea held-out test set** scored against expert gold labels.
>
> **No human evaluators in the loop** for the comparison; all metrics are automatic against the expert labels.
>
> "we standardize the most relevant papers to ensure a fair comparison of the prompts alone. Additionally, since both setups require a different style of input idea, we adapted the ideas to match the requirements of each system." (Shahid et al., 2025, p. 6)
> ![[shahidLiteratureGroundedNoveltyAssessment2025-evd-p6-2.png]]

## Other Notes

- AI Scientist defaulted to "not novel" in **56% of test cases (18/32)**, inflating agreement with the not-novel class but suppressing accuracy and κ.
- Cohen's κ of **0.05** indicates near-chance agreement with expert labels; AI Researcher (gpt-4o) reaches κ=0.52, much closer to the Idea Novelty Checker (κ=0.59).
- AI Researcher's performance is highly backbone-sensitive: gpt-4o reaches F1=0.75, but Claude-3.5-Sonnet drops to F1=0.56 / κ=0.19.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@shahidLiteratureGroundedNoveltyAssessment2025#TRIPOD-LLM reporting summary]].

| System (backbone) | Accuracy | Precision | Recall | F1 | Cohen's κ |
| --- | :---: | :---: | :---: | :---: | :---: |
| **AI Scientist** (Lu et al.) | **0.47** | **0.55** | **0.53** | **0.44** | **0.05** |
| AI Researcher (gpt-4o) | 0.78 | 0.81 | 0.74 | 0.75 | 0.52 |
| AI Researcher (Claude-3.5-Sonnet) | 0.56 | 0.63 | 0.61 | 0.56 | 0.19 |
| (Reference) Idea Novelty Checker (gpt-4o) | 0.81 | 0.84 | 0.78 | 0.79 | 0.59 |

| Failure mode | Count |
| --- | --- |
| AI Scientist defaulted to "not novel" (no decision reached) | 18 / 32 (56.3%) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy over zero-shot and prompt-optimized baselines]]

- [[CLM - Facet-based LLM re-ranking is critical for identifying the most relevant papers for novelty evaluation]]

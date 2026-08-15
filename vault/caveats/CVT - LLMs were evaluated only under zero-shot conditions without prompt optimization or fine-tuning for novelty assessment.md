---
NodeFormality: ReadyForInternal
aliases:
tags:
  - cvt/domain/internal-validity
  - cvt/mechanism/single-prompt
  - cvt/type/inferred
  - cvt/severity/moderate
  - 5c/creativity
appliesTo:
  - "[[EVD - Ours-SciBERT with combined human and LLM knowledge achieved F1=0.83 and accuracy=0.84 on method novelty prediction - @wuAutomatedNoveltyEvaluationa]]"
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6bad-72be-98bd-00bfab87cc17
type: inferred
severity: moderate
---

## Source

[[@wuAutomatedNoveltyEvaluationa]]

### Limitation

The LLM baselines (Llama 3.1, ChatGPT, GPT-4o, Claude) were tested exclusively under zero-shot conditions with default parameters, without any prompt engineering, few-shot examples, or fine-tuning specific to the novelty assessment task. This understates the potential of LLMs as standalone assessors, and means the comparison between LLMs and the proposed PLM-based model is not fully controlled.

### Supporting Quote

> [!info] Quotes
> "The experimental results of the LLMs are the averages obtained from three rounds of experiments conducted under zero-shot conditions. The prompts for LLMs are shown in Figures S4–S6." (Wu et al., 2024, p. 1461) [Inferred: zero-shot evaluation without prompt optimization likely underestimates LLM capability on this task, making the advantage of the proposed method harder to interpret.]
>
> ![[wuAutomatedNoveltyEvaluationa-cvt-p10-1.png]]

### Applies To

[[EVD - Ours-SciBERT with combined human and LLM knowledge achieved F1=0.83 and accuracy=0.84 on method novelty prediction - @wuAutomatedNoveltyEvaluationa]]

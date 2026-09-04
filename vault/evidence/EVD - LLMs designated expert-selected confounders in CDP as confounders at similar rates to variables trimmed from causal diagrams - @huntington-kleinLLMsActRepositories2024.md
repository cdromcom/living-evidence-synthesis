---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/causal-inference-judgment
  - appraisal/construct-validity/low-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/62pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7a-732c-ab07-30b53433883a
appraisal_overall: L1-M3-H1
tripod_llm_pct: 62pct
---

## Source

[[@huntington-kleinLLMsActRepositories2024]]

## Description

> "the confounders trimmed from the causal diagram in Debertin et al. (2024) as being unnecessary were far more likely to be classified by LLMs as confounders than the variables added and kept. The variables directly classified as Non-Confounders were also more likely to be designated as confounders than the Added in 2016 set." (Huntington-Klein & Murray, 2024, p. 9)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-p9-1.png]]
>
> Direct method: Claude 3.5 designated 59.9% of "Original" confounders as confounders; also designated 40% of "Non-Confounders" as confounders 100% of the time (Table 1, Fig 1, p. 7–8)

## Methods Context

### What?

> **Study design:** ground-truth-anchored LLM benchmark on a single causal-inference case study (Coronary Drug Project).
>
> **Method type:** zero/few-shot multiple-choice LLM elicitation of confounder status, compared against expert-curated confounder sets from three published studies.
>
> **Tools:** GPT-4o and Claude 3.5-Sonnet (via `openai` and `anthropic` Python packages, temperature 0.7, 10 calls per prompt) plus GPT-o1-preview (single call, temperature not user-controlled); CDP confounder lists from CDPRG (1980), Murray & Hernán (2016), and Debertin et al. (2024).
>
> **Dependent variable:** share of variables in each expert category designated as a confounder by the LLM (averaged over 10 iterations for GPT-4o / Claude).
>
> **Independent variables / covariates:** confounder category (Original / Added in 2016 / Expert-Added / Final Expert DAG / Trimmed / Non-Confounders); LLM model; prompting method (direct vs. indirect, with reasoning).
>
> "Our general approach to checking LLM capabilities to designate variables as confounders involves taking a set of confounders identified by experts, and for each having the LLM designate whether or not it is a confounder." (Huntington-Klein & Murray, 2024, p. 4)
> ![[huntington-kleinLLMsActRepositories2024-evd-p4-1.png]]

### How?

> **Procedure:** (1) Build a 172-variable candidate pool by unioning confounder lists from CDPRG (1980), Murray & Hernán (2016), and Debertin et al. (2024), plus 60 expert-rejected "Non-Confounders." (2) For each variable, query the LLM with a fixed system prompt ("You are a bot that specializes in causal inference in medical contexts…") plus three worked examples (SES / hormone-replacement, low-dose aspirin / ACE inhibitors, vitamin D / headache) and one CDP question of the form "the variable ({confounder}) is… A. Not a confounding variable B. A confounding variable C. Not sure." Ask the LLM to reason step-by-step and give a final letter. (3) Run each prompt 10 times for GPT-4o and Claude 3.5-Sonnet (1× for GPT-o1-preview). (4) For the *indirect* method, replace the single direct question with two separate causal-effect questions, variable→adherence and variable→mortality, and label as confounder only if both return "A" or "B." (5) Aggregate to per-variable share-confounder, then average within each expert category and report by model × method (Table 1, Figs 1–2).
>
> "We take several different approaches to designing prompts to query LLMs about whether a given variable is a confounder in this context. First, we distinguish between a 'direct' prompting approach and an 'indirect' prompting approach." (Huntington-Klein & Murray, 2024, p. 4)
> ![[huntington-kleinLLMsActRepositories2024-evd-p4-2.png]]

### Who?

> **Models:** GPT-4o, Claude 3.5-Sonnet, GPT-o1-preview (all generalist models; medical-specialist LLMs explicitly excluded; see paper's rationale on p. 5).
>
> **Variables (sample-size flow):** CDPRG (1980) Original set ∪ Murray & Hernán (2016) Added-in-2016 ∪ Debertin et al. (2024) Expert-Added / Final Expert DAG / Trimmed sets → 112 expert-considered variables; plus 60 hand-curated Non-Confounders (administrative variables / drug side-effects / general physical-exam findings / sub-study-only measurements) → **172 potential confounders** total. No variables excluded.
>
> **LLM responses:** 13,760 per model for Claude 3.5-Sonnet and GPT-4o (172 vars × 8 prompt variants × 10 iterations); 688 for GPT-o1-preview (172 × 4 variants × 1, no-reasoning prompts omitted).
>
> "From CDPRG (1980), Murray and Hernán (2016), and Debertin et al. (2024) we have a list of 172 potential confounders to consider across eight different prompt variations. For the Claude 3.5-Sonnet and GPT-4o models, we query the LLM ten times each for a total of 13,760 LLM-generated responses each. For the GPT-o1-preview model, we only query the LLM once, and only use four of the prompt variations (omitting the no-reasoning prompts since GPT-o1-preview always provides reasoning) for a total of 688 LLM-generated responses." (Huntington-Klein & Murray, 2024, p. 7)
> ![[huntington-kleinLLMsActRepositories2024-evd-p7-1.png]]

## Other Notes

LLM confounder designation was highly inconsistent across prompts and models. Cohen's kappa between direct and indirect methods ranged from 0.16 (GPT-o1) to 0.24 (GPT-4o), indicating poor agreement.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@huntington-kleinLLMsActRepositories2024#TRIPOD-LLM reporting]].

Direct method (with reasoning), share of variables designated as confounder, averaged over 10 iterations:

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original (CDPRG 1980) | 90% at 100% | 95% at 100% | 98% at 100% |
| Added in 2016 | 50% at 100% | 50% at 100% | 80% at 100% |
| Expert-Added (Debertin 2024) | 53% at 100% | 63% at 100% | 58% at 100% |
| Final Expert DAG | 69% at 100% | 76% at 100% | 71% at 100% |
| **Trimmed (expert-rejected)** | **79% at 100%** | **89% at 100%** | **95% at 100%** |
| **Non-Confounders** | **40% at 100%** | **40% at 100%** | **73% at 100%** |

Indirect method (with reasoning), share at 100% confounder:

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original | 83% | 71% | 100% |
| Added in 2016 | 80% | 30% | 90% |
| Trimmed | 74% | 74% | 100% |
| Non-Confounders | 65% | 22% | 93% |

| Aggregate (paper text) | Value |
| --- | --- |
| Direct, Claude 3.5: Is confounder | 59.9% |
| Direct, GPT-4o: Is confounder | 71.9% |
| Direct, GPT-o1: Is confounder | 58.7% |
| Indirect, Claude 3.5: Is confounder | 89.5% |
| Indirect, GPT-4o: Is confounder | 81.9% |
| Indirect, GPT-o1: Is confounder | 93.6% |
| Final Expert DAG (indirect, all models) | ≈70% |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - The Huntington-Klein study used a single causal dataset limiting the scope of conclusions about LLM causal knowledge]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]

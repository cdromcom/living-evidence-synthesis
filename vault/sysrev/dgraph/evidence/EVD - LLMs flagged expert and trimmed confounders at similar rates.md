---
NodeFormality: ReadyForInternal
human_reviewed: no
aliases:
  - "EVD - LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams"
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
updated: 2026-11-24
nodeID: 019ddb4e-6b7a-732c-ab07-30b53433883a
appraisal_overall: L1-M3-H1
tripod_llm_pct: 62pct
title: "LLMs designated expert-selected confounders in CDP as confounders at similar rates to variables trimmed from causal diagrams"
---

## Source

[[sysrev/dgraph/source/@huntington-kleinLLMsActRepositories2024]]

## Description

> "Perhaps oddly, the confounders trimmed from the causal diagram in Debertin et al. [20] as being unnecessary were far more likely to be classified by LLMs as confounders than the variables added and kept." (Huntington-Klein & Murray, 2026, p. 8)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p8-1.png]]
>
> "That variables removed from the causal diagram were more likely to be designated confounders than the variables kept, and that variables designated as non-confounders were included at a similar rate, indicates disagreement between the LLMs and the experts." (Huntington-Klein & Murray, 2026, p. 9)
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p9-1.png]]
>
> Direct method: Claude 3.5 designated 59.9% of all variables as confounders (Table 1, p. 8; pooled across all variable categories, not the "Original" set); 90.2% of "Original" confounders and 40.0% of "Non-Confounders" were designated confounders in all 10 iterations (Fig 2, p. 9). Variables directly classified as Non-Confounders were more likely to be designated confounders than the "Added in 2016" set for Claude and GPT-o1, but not for GPT-4o (p. 9; Fig 2: 40.0% vs 30.0%, 40.0% vs 50.0%, 73.3% vs 30.0%).
>
> Grounding table (Table 1, p. 8): share of variables designated as confounders, by prompting method and model.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-table1-p8.png]]
>
> Grounding figure (Fig 2, p. 9): distribution of LLM confounder designations, reasoning-encouraged direct method.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig2-p9.png]]
>
> Grounding figure (Fig 3, p. 10): distribution of LLM confounder designations, reasoning-encouraged indirect method.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig3-p10.png]]
>
> Grounding figure (Fig 6, p. 14): distribution of LLM confounder designations, pick-from-list method.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig6-p14.png]]
>
> Grounding figure (Fig 7, p. 15): distribution of LLM confounder designations, sequential prompting method.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig7-p15.png]]

## Methods Context

### What?

> **Study design:** ground-truth-anchored LLM benchmark on a single causal-inference case study (Coronary Drug Project).
>
> **Method type:** zero/few-shot LLM elicitation of confounder status (four prompting approaches: direct, indirect, pick-from-list, sequential), compared against expert-curated confounder sets from three published studies.
>
> **Tools:** GPT-4o and Claude 3.5-Sonnet (via `openai` and `anthropic` Python packages, temperature 0.7, 10 calls per prompt) plus GPT-o1-preview (single call, temperature not user-controlled); the pick-from-list and sequential approaches, added in a later revision and run in August 2025, used GPT-o1-pro and the claude-3-5-sonnet-20240620 version of Claude 3.5-Sonnet; CDP confounder lists from CDPRG (1980), Murray & Hernán (2016), and Debertin et al. (2024).
>
> **Dependent variable:** share of variables in each expert category designated as a confounder by the LLM (averaged over 10 iterations for GPT-4o / Claude).
>
> **Independent variables / covariates:** confounder category (Original / Added in 2016 / Expert-Added / Final Expert DAG / Trimmed / Non-Confounders); LLM model; prompting method (direct, indirect, pick-from-list, sequential; with reasoning).
>
> "Our general approach to checking LLM capabilities to designate variables as confounders involves taking a set of confounders identified by experts, and for each having the LLM designate whether or not it is a confounder." (Huntington-Klein & Murray, 2026, p. 3)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p3-1.png]]

### How?

> **Procedure:** (1) Build a 172-variable candidate pool by unioning confounder lists from CDPRG (1980), Murray & Hernán (2016), and Debertin et al. (2024), plus 60 expert-rejected "Non-Confounders." (2) For each variable, query the LLM with a fixed system prompt ("You are a bot that specializes in causal inference in medical contexts…") plus three worked examples (SES / hormone-replacement, low-dose aspirin / ACE inhibitors, vitamin D / headache) and one CDP question of the form "the variable ({confounder}) is… A. Not a confounding variable B. A confounding variable C. Not sure." Ask the LLM to reason step-by-step and give a final letter (Appendix B, p. 23). (3) Run each prompt 10 times for GPT-4o and Claude 3.5-Sonnet (1× for GPT-o1-preview). (4) For the *indirect* method, replace the single direct question with two separate causal-effect questions, variable→adherence and variable→mortality, and label as confounder only if both return "A" or "B." (5) For *pick-from-list*, show five potential confounders, ask the LLM to pick the most likely confounders, and repeat for three random sets of four companion variables per confounder; for *sequential* prompting, walk the LLM from the indirect questions to a final agree-or-disagree question about the confounder conclusion (pp. 4–5). (6) Aggregate to per-variable share-confounder, then average within each expert category and report by model × method (Table 1, Figs 2–3, 6–7).
>
> "We take several different approaches to designing prompts to query LLMs about whether a given variable is a confounder in this context. First, we distinguish between a “direct” prompting approach and an “indirect” prompting approach." (Huntington-Klein & Murray, 2026, p. 3)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p3-2.png]]
>
> "Our third prompting approach, “pick from list,” is designed to limit the tendency of LLMs to give positive responses. In this prompt we provide a list of five potential confounders and ask the LLM to select the options that are most likely to be confounders, without specifying how many it should pick" (Huntington-Klein & Murray, 2026, p. 4)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p4-1.png]]
>
> Grounding figure (Fig 1, p. 6): research design flowchart.
>
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-fig1-p6.png]]

### Who?

> **Models:** GPT-4o, Claude 3.5-Sonnet, GPT-o1-preview (all generalist models; medical-specialist LLMs explicitly excluded; see paper's rationale on pp. 5–6). Pick-from-list and sequential prompting used GPT-o1-pro and claude-3-5-sonnet-20240620 instead (p. 5, footnote 4).
>
> **Variables (sample-size flow):** CDPRG (1980) Original set ∪ Murray & Hernán (2016) Added-in-2016 ∪ Debertin et al. (2024) Expert-Added / Final Expert DAG / Trimmed sets → 112 expert-considered variables; plus 60 hand-curated Non-Confounders (administrative variables / drug side-effects / general physical-exam findings / sub-study-only measurements) → **172 potential confounders** total. No variables excluded.
>
> **LLM responses:** 31,270 per model for Claude 3.5-Sonnet and GPT-4o (a small number of non-answers lost; 11,760 of them are pick-from-list responses); 1,447 for GPT-o1-preview (one response per prompt per confounder, no-reasoning prompts omitted). Direct and indirect responses were collected 9–15 October 2024 (Non-Confounders 23 November – 8 December 2024); pick-from-list and sequential responses 16–18 August 2025 (p. 8).
>
> "From CDPRG [16]; Murray and Hernán [17]; and Debertin et al. [20] we have a list of 172 potential confounders to consider across all prompt variations. For the Claude 3.5-Sonnet and GPT-4o models, we query the LLM ten times each, with a small number of responses lost due to non-answers for a total of 31,270 LLM-generated responses each. A plurality of these (11,760) are for the pick-from-list method, since there are ten generations each for three candidate confounder lists per confounder. For the GPT-o1-preview model, we only query the LLM once per prompt per confounder, and omit the no-reasoning prompts, for a total of 1,447 LLM-generated responses." (Huntington-Klein & Murray, 2026, p. 8)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p8-2.png]]
>
> "The pick from list and sequential prompting approaches were added in later revisions of this study. As such they use GPT-o1-pro instead of GPT-o1-preview, which is no longer available, and the claude-3-5-sonnet-20240620 version of Claude 3.5-Sonnet, which is the only version still available as of this writing." (Huntington-Klein & Murray, 2026, p. 5, footnote 4)
> ![[huntington-kleinLLMsActRepositories2024-evd-v2026-p5-1.png]]

## Other Notes

LLM confounder designation was highly inconsistent across prompts and models. Cohen's kappa between direct and indirect methods ranged from 0.16 (GPT-o1) to 0.24 (GPT-4o), indicating poor agreement (Fig 9, p. 17). The conclusions (p. 19) add that Trimmed and Non-Confounders variables "are often designated at the same rate, and in some cases at higher rates" than expert confounders.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[sysrev/dgraph/source/@huntington-kleinLLMsActRepositories2024#TRIPOD-LLM reporting]].

Direct method (with reasoning), share of variables designated as confounder in all 10 iterations (Fig 2, p. 9):

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original (CDPRG 1980) | 90.2% at 100% | 95.1% at 100% | 97.6% at 100% |
| Added in 2016 | 30.0% at 100% | 50.0% at 100% | 30.0% at 100% |
| Expert-Added (Debertin 2024) | 52.6% at 100% | 63.2% at 100% | 57.9% at 100% |
| Final Expert DAG | 68.6% at 100% | 76.5% at 100% | 70.6% at 100% |
| **Trimmed (expert-rejected)** | **78.9% at 100%** | **89.5% at 100%** | **94.7% at 100%** |
| **Non-Confounders** | **40.0% at 100%** | **40.0% at 100%** | **73.3% at 100%** |

Indirect method (with reasoning), share at 100% confounder (Fig 3, p. 10):

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original | 82.9% | 70.7% | 100.0% |
| Added in 2016 | 80.0% | 30.0% | 90.0% |
| Expert-Added | 84.2% | 36.8% | 84.2% |
| Final Expert DAG | 86.3% | 49.0% | 92.2% |
| **Trimmed** | **73.7%** | **73.7%** | **100.0%** |
| **Non-Confounders** | **65.0%** | **21.7%** | **93.3%** |

Pick-from-list method, share designated a confounder in all 10 iterations (Fig 6, p. 14; no "Always" segment is drawn where the share is 0):

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original | 36.6% | 39.0% | 68.3% |
| Added in 2016 | 0.0% | 0.0% | 0.0% |
| Expert-Added | 52.6% | 42.1% | 47.4% |
| Final Expert DAG | 49.0% | 41.2% | 56.9% |
| **Trimmed** | **0.0%** | **15.8%** | **42.1%** |
| **Non-Confounders** | **11.7%** | **6.7%** | **16.7%** |

Sequential method, share designated a confounder in all 10 iterations (Fig 7, p. 15):

| Variable category | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Original | 82.9% | 34.1% | 84.6% |
| Added in 2016 | 60.0% | 20.0% | 55.6% |
| Expert-Added | 73.7% | 52.6% | 53.3% |
| Final Expert DAG | 74.5% | 47.1% | 72.7% |
| **Trimmed** | **84.2%** | **10.5%** | **73.7%** |
| **Non-Confounders** | **48.3%** | **15.0%** | **50.0%** |

| Aggregate: share of all variables designated as confounders (Table 1, p. 8) | Claude 3.5 | GPT-4o | GPT-o1 |
| --- | :---: | :---: | :---: |
| Direct w/Reasoning | 59.9% | 71.9% | 58.7% |
| Indirect w/Reasoning | 89.5% | 81.9% | 93.6% |
| Direct, no Reasoning | 75.0% | 26.1% | NA |
| Indirect, no Reasoning | 89.5% | 81.9% | NA |
| Pick-from-list | 47.5% | 44.3% | 41.2% |
| Sequential | 85.9% | 58.8% | 52.3% |

- Final Expert DAG, direct method: "only about 70 %" of confounders in the final causal diagram were designated confounders (p. 9); Fig 2 shows 68.6% / 76.5% / 70.6% for Claude / GPT-4o / GPT-o1.
- Sequential prompting (p. 14): for Claude 3.5 and GPT-o1 the rate of confounder designation "is similar in confounder and non-confounder (Trimmed and Non-Confounder) variable sets"; the authors conclude the new methods "did meaningfully change the distribution of results" but "were not consistent improvements".
- Pick-from-list (p. 13): lower "always" shares for Trimmed and Non-Confounders than under direct or indirect prompting, but the authors note this may only reflect the method designating fewer variables overall; all Trimmed variables were selected at least some of the time.
- PDF check 2026-11-24: source version: pages now cite the 2026 journal article (J Causal Inference 14(1), article 20240072, printed pp. 1-30, doi 10.1515/jci-2024-0072); the arXiv v1 (2024) PDF is kept as "Archive - superseded versions/Archive - Huntington-Klein and Murray - 2024.pdf"
- PDF check 2026-11-24: finding re-extracted from the 2026 tables and figures: still holds (title unchanged). The direct and indirect values are the same as in arXiv v1 after rounding; the new pick-from-list and sequential data are added and the new text (pp. 13-14, 19) repeats that Trimmed and Non-Confounders variables are designated at similar rates to expert confounders
- PDF check 2026-11-24: Description quote "the confounders trimmed from the causal diagram in Debertin et al. (2024) ... The variables directly classified as Non-Confounders were also more likely ... than the Added in 2016 set." (Huntington-Klein & Murray, 2024, p. 9) -> two journal passages: "Perhaps oddly, the confounders trimmed from the causal diagram in Debertin et al. [20] ... added and kept." (2026, p. 8) and "That variables removed from the causal diagram were more likely ... experts." (2026, p. 9); the old quote ended its second sentence at "set." but the paper continues "set, except for GPT-4o." (now stated in the bullet below the quotes); citation "(2024)" -> "[20]" (numbered citations)
- PDF check 2026-11-24: "Direct method: Claude 3.5 designated 59.9% of 'Original' confounders as confounders; also designated 40% of 'Non-Confounders' as confounders 100% of the time (Table 1, Fig 1, p. 7-8)" -> "59.9% of all variables ... (Table 1, p. 8; pooled across categories); 90.2% of 'Original' ... (Fig 2, p. 9)" (error in both versions: 59.9% is Claude's overall direct-method share, not its share for Original confounders; the Original share is 90.2% at 100%); Fig 1 -> Fig 2 after renumbering
- PDF check 2026-11-24: direct-method table, row "Added in 2016": "50% at 100% | 50% at 100% | 80% at 100%" -> "30.0% | 50.0% | 30.0%" (Fig 2, p. 9; error in both versions: GPT-o1 has 70.0% at Never); all other cells restated to one decimal from Fig 2, matching the old rounded values
- PDF check 2026-11-24: aggregate row "Final Expert DAG (indirect, all models) ≈70%" -> "Final Expert DAG, direct method, about 70%" (p. 9, discussion of Fig 2; the indirect Fig 3 values are 86.3 / 49.0 / 92.2%; error in both versions); the row now sits in a bullet
- PDF check 2026-11-24: indirect table values restated to one decimal from Fig 3 (p. 10): 83 -> 82.9, 71 -> 70.7, 74 -> 73.7, 22 -> 21.7, 93 -> 93.3 (no change in substance); Expert-Added and Final Expert DAG rows added
- PDF check 2026-11-24: aggregate table 59.9 / 71.9 / 58.7 (direct) and 89.5 / 81.9 / 93.6 (indirect) unchanged in the rebuilt Table 1 (p. 8, was p. 7); table now also has no-reasoning, pick-from-list and sequential rows
- PDF check 2026-11-24: LLM responses "13,760 per model ... 688 for GPT-o1-preview (172 vars × 8 prompt variants × 10 iterations; 172 × 4 variants × 1)" -> "31,270 per model ... 1,447 for GPT-o1-preview" (p. 8); the multiplication was dropped because the paper no longer gives the number of prompt variants and says some responses were lost to non-answers
- PDF check 2026-11-24: Data quote "From CDPRG (1980), Murray and Hernán (2016), and Debertin et al. (2024) ... eight different prompt variations ... 13,760 ... 688" (2024, p. 7) -> journal passage with 31,270, 11,760 (pick-from-list) and 1,447 (2026, p. 8); "eight different prompt variations" -> "all prompt variations"; added collection dates for the 2025 methods
- PDF check 2026-11-24: citations of "Our general approach ..." and "We take several different approaches ..." (2024, p. 4) -> (2026, p. 3); figure/table references "Table 1, Figs 1-2" -> "Table 1, Figs 2-3, 6-7"; system-prompt and worked-example details now cited to Appendix B, p. 23; rationale for generalist models "p. 5" -> "pp. 5-6"
- PDF check 2026-11-24: Tools/Who: added GPT-o1-pro and claude-3-5-sonnet-20240620 for the pick-from-list and sequential methods (p. 5, footnote 4); prompting methods in the design: 2 -> 4

## Caveats

> [!info] Caveats applying to this evidence

- [[sysrev/dgraph/caveats/CVT - Huntington-Klein used a single causal dataset|CVT - The Huntington-Klein study used a single causal dataset limiting the scope of conclusions about LLM causal knowledge]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[sysrev/dgraph/claims/CLM - LLMs are not yet reliable causal knowledge sources for confounder selection|CLM - LLMs do not yet serve as reliable repositories of causal knowledge for confounder selection]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[sysrev/dgraph/evd-patterns/EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation|EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]

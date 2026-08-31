---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/error-detection
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
nodeID: 019ddb4e-6b6d-739b-84bf-e74cc12a481a
appraisal_overall: L0-M3-H2
tripod_llm_pct: 36pct
---

## Source

[[@liuReviewerGPTExploratoryStudy2023]]

## Description

> "We find that the LLM (GPT-4) can detect the error in 7 of the 13 short papers. Furthermore, in each of the 6 papers where it failed to detect the error, the paper did not contain the complete proof for the claim, thereby disallowing the LLM to detect a deductive error, and requiring it to figure out the flaw based on extraneous knowledge." (Liu & Shah, 2023, p. 5)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p5-1.png]]
>
> Grounding table (Table 1, p. 6): per-paper success across the three prompt types and three responses per prompt.
>
> ![[liuReviewerGPTExploratoryStudy2023-table1-p6-06.png]]

## Methods Context

### What?

> **Study design:** controlled benchmark on a hand-constructed adversarial corpus (13 short CS papers each containing one deliberately inserted error).
>
> **Method type:** zero-shot / one-shot LLM error detection with majority-vote scoring across 3 responses × 3 prompt strategies.
>
> **Tools:** GPT-4 accessed through ChatGPT (May 3 and May 12 2023 builds); 3 prompt templates (`Prompt-Direct`, `Prompt-OneShot`, `Prompt-Parts`); inference settings not reported (ChatGPT defaults).
>
> **Dependent variable:** per-paper detection success — checkmark if any of the 3 responses for a given prompt detected the error; "Overall" checkmark if any response across any prompt detected it.
>
> **Independent variables / covariates:** prompt strategy (Direct vs. OneShot vs. Parts); paper topic (13 topics: bias/fairness, regression, sorting × 2, noisy pairwise comparisons × 2, classification, game theory, error-correcting codes, optimization, clustering, distinguishing styles × 2).
>
> "we deliberately inserted an error, encompassing mathematical mistakes to conceptual fallacies. We then asked the LLM to identify if there are any errors in the short paper." (Liu & Shah, 2023, p. 4)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p4-1.png]]

### How?

> **Procedure:** (1) Authors hand-constructed 13 short CS papers (Section 3.3.1–3.3.13), each seeded with one specific error (e.g., wrong sqrt-vs-log lower bound for sorting; conflating mean-square convergence with convergence in probability; non-linearity of majority vote of linear classifiers; misapplied Stackelberg-equilibrium argument; etc.). Topics were chosen to span mathematical and conceptual fallacies. (2) For each paper, queried GPT-4 with three prompt strategies — `Prompt-Direct` (full short paper, no example), `Prompt-OneShot` (full short paper preceded by a worked example of an erroneous binary-search paper + an instructive review), and `Prompt-Parts` (paper provided one sentence at a time, asking the model to flag errors incrementally). All prompts cast GPT-4 as "an expert reviewer for a scientific conference" and instructed it to "think step by step." (3) Sampled 3 responses per prompt → cell receives ✓ if any of the 3 responses detected the error, ✗ otherwise, ! if a false alarm was raised. (4) "Overall" column receives ✓ if any response across any of the three prompts detected the error.
>
> "We queried the LLM for three responses per prompt and we provide an evaluation of each response as well as an overall quantification of the performance. In the 'overall' row and column in the table, we consider it as a ✓ if any of the responses to any of the prompts was a ✓." (Liu & Shah, 2023, p. 5)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p5-2.png]]

### Who?

> **Models / participants:** GPT-4 via ChatGPT (May 3 and May 12 2023 builds). Comparator open-source models (Bard, Vicuna, Koala, Alpaca, LLaMa, Dolly, OpenAssistant, StableLM) were also tried but failed on every paper, so only GPT-4 results are tabulated. No human participants.
>
> **Sample-size flow:** 13 hand-constructed short papers (the entire corpus) → all 13 evaluated under all 3 prompt strategies → 3 responses per (paper, prompt) cell → 13 paper-level decisions analyzed. No exclusions; the corpus was not split.
>
> "We constructed 13 short papers (detailed in Section 3.3)." (Liu & Shah, 2023, p. 4)
> ![[liuReviewerGPTExploratoryStudy2023-evd-p4-2.png]]

## Other Notes

- Only GPT-4 succeeded; the other 8 LLMs tried (Bard, Vicuna, Koala, Alpaca, LLaMa, Dolly, OpenAssistant, StableLM) failed on all 13 papers and some produced "Reviewer #2"-style nonsensical critiques.
- The LLM also occasionally produced false positives (`!` in Table 1) — flagging correct parts of papers as wrong (5 false alarms across all prompt-strategy cells; 2 in the "Overall" column).
- For all 6 papers where GPT-4 failed, the short paper did not contain a complete proof, so detection would have required external knowledge rather than a deductive check.
- Per-prompt totals: `Prompt-Direct` 5✓ / 8✗ / 1!; `Prompt-OneShot` 6✓ / 7✗ / 1!; `Prompt-Parts` 7✓ / 6✗ / 1!; `Overall` 7✓ / 6✗ / 2!.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liuReviewerGPTExploratoryStudy2023#TRIPOD-LLM reporting summary]].

| Prompt strategy | ✓ detected | ✗ missed | ! false alarms |
| --- | --- | --- | --- |
| Prompt-Direct | 5 / 13 | 8 / 13 | 1 |
| Prompt-OneShot | 6 / 13 | 7 / 13 | 1 |
| Prompt-Parts | 7 / 13 | 6 / 13 | 1 |
| **Overall (any prompt × any response)** | **7 / 13 (53.8%)** | 6 / 13 | 2 |
| Other 8 LLMs (Prompt-Direct only) | 0 / 13 | 13 / 13 | — |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Only GPT-4 was tested for error detection as all other LLMs failed entirely]]

- [[CVT - The error detection study used constructed short papers rather than real manuscript submissions]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs show promise for targeted reviewing subtasks but are not yet capable of functioning as standalone peer reviewers]]

- [[CLM - Targeted question prompting elicits substantially better LLM performance than open-ended review generation]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM performance varies substantially with prompt design making prompt engineering load-bearing]]
- [[EP - LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable]]

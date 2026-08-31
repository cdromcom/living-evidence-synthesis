---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
  - appraisal/construct-validity/high-risk
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M1-H4
  - tripod-llm/compliance/low
  - tripod-llm/proportion/26pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b5c-74d1-b091-818677083593
appraisal_overall: L0-M1-H4
tripod_llm_pct: 26pct
---

## Source

[[@robertsComparativeStudyChatGPT2023]]

## Description

> "The domains with a strong positive correlation were 'harms' (r=0.32, p<0.001) and 'trial registration' (r=0.34, p=0.002), indicating a high level of consistency between ChatGPT and human evaluators in these domains. On the other hand, 'intervention' (r=0.02, p<0.001) and 'objective' (r=0.06, p<0.001) domains had very weak correlations, suggesting that ChatGPT's performance was less consistent with human evaluators in these domains." (Roberts et al., 2023, p. 4)
>
> ![[robertsComparativeStudyChatGPT2023-evd-p4-2.png]]
> [Screenshot: Table 1, p. 3]

## Methods Context

### What?

> **Study design:** cross-sectional method-comparison study; per-domain linear-association sub-analysis.
>
> **Method type:** zero-shot LLM evaluation against human consensus, with Pearson correlation as a complementary agreement measure to mean-difference.
>
> **Tools:** OpenAI ChatGPT GPT-3.5 (no version pin); CONSORT-A 15-item abstract reporting checklist; R v4.1.1; Pearson's r interpreted by author-defined magnitude bands (very weak <0.2, weak 0.2–0.39, moderate 0.40–0.59, strong 0.6–0.79, very strong 0.8–1).
>
> **Dependent variable:** Pearson's r between human and ChatGPT subscores per CONSORT-A domain.
>
> **Independent variable:** CONSORT-A domain.
>
> "the Pearson's correlation coefficient provides information on the strength and direction of the linear relationship between the two sets of scores. This provided complementary information on the agreement between ChatGPT and human evaluator. The Pearson's correlation coefficient was interpreted based on magnitude: r, 0–0.19 very weak, 0.2–0.39 weak, 0.40–0.59 moderate, 0.6–0.79 strong and 0.8–1 very strong correlation." (Roberts et al., 2023, p. 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-4.png]]

### How?

> **Procedure:** for each of the 14 CONSORT-A domains in Table 1, compute Pearson's r between the 30 paired (human-consensus, ChatGPT) item-level scores (each on the 0 / 0.5 / 1 scale). Significance evaluated against P<0.001 threshold using R v4.1.1. ChatGPT scoring used the single zero-shot prompt template in Figure 1A (CONSORT-A item definitions provided up front, model labels each item completely / partially / not reported). Note that the authors apply "strong" to r=0.32–0.34 in the prose despite their own magnitude bands classifying these as "weak" (0.2–0.39) — readers should rely on the numeric r values rather than the prose label.
>
> "ChatGPT was used to score the same set of abstracts, using a prompt to assess for each domain within the CONSORT-A checklist (figure 1)." (Roberts et al., 2023, p. 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-5.png]]

### Who?

> **Models / participants:** ChatGPT GPT-3.5 (OpenAI; no version pin) vs. two human clinician reviewers (specialty / training stage not reported). Inference parameters not reported.
>
> **Sample-size flow:** Menne, Pandis & Faggion (2021) implant-dentistry RCT abstract corpus → **30 abstracts** sampled by the original authors → re-scored by two clinician reviewers with ≥80% consensus reconciliation (then one continued solo) → same 30 abstracts scored once by ChatGPT → **30 paired item-level scores per domain** entered each per-domain Pearson r calculation.
>
> "The processes of selection and data extraction were performed independently and in duplicate by two clinician reviewers across a sample of 30 abstracts." (Roberts et al., 2023, p. 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-6.png]]

## Other Notes

- By the authors' own magnitude bands, no domain reached "moderate" agreement (r ≥ 0.40) except trial design (r=0.49), blinding (r=0.44) — both with p>0.05 (0.054 and 0.091), so neither is significantly different from zero. The two domains the authors call "strong" in prose ('harms' r=0.32; 'trial registration' r=0.34) are formally "weak" by their own bands.
- Most domains have r values in the very-weak range (<0.2): intervention 0.02, number analysed 0.04, objective 0.06, conclusion 0.06, randomisation 0.11, outcome (methods) 0.14, outcome (reporting) 0.15, funding 0.21, participants 0.26.
- The combination of low Pearson r and small mean differences (e.g., intervention r=0.02 with mean diff only 0.057) suggests ChatGPT and humans are agreeing on the modal label by chance rather than tracking the same per-abstract signal.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@robertsComparativeStudyChatGPT2023#TRIPOD-LLM reporting summary]].

| CONSORT-A domain | Pearson r | p-value | Author band | Notes |
| --- | :---: | :---: | --- | --- |
| Trial design | 0.49 | 0.054 | moderate | not significant |
| Blinding | 0.44 | 0.091 | moderate | not significant |
| Trial registration | 0.34 | 0.002 | weak | called "strong" in prose |
| Harms | 0.32 | <0.001 | weak | called "strong" in prose |
| Number randomly assigned | 0.31 | 0.006 | weak | — |
| Participants | 0.26 | 0.001 | weak | — |
| Funding | 0.21 | <0.001 | weak | — |
| Outcome (reporting) | 0.15 | <0.001 | very weak | — |
| Outcome (methods) | 0.14 | <0.001 | very weak | — |
| Randomisation | 0.11 | <0.001 | very weak | — |
| Conclusion | 0.06 | <0.001 | very weak | — |
| **Objective (weakest tied)** | **0.06** | **<0.001** | **very weak** | — |
| Number analysed | 0.04 | 0.434 | very weak | not significant |
| **Intervention (weakest)** | **0.02** | **<0.001** | **very weak** | — |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]]
- [[EP - Per-item LLM-human agreement varies sharply by item type]]

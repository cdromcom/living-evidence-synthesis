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
nodeID: 019ddb4e-6b5b-713a-b0d8-3e1307eb62f0
appraisal_overall: L0-M1-H4
tripod_llm_pct: 26pct
---

## Source

[[@robertsComparativeStudyChatGPT2023]]

## Description

> "The mean difference in absolute OCS was highest for the 'conclusion' domain (0.764, 95% CI: 0.186, 0.280), indicating that ChatGPT differed the most from human evaluators in this domain." (Roberts et al., 2023, p. 4)
>
> ![[robertsComparativeStudyChatGPT2023-evd-p4-1.png]]
> [Screenshot: Table 1, p. 3, error analysis of ChatGPT CONSORT-A OCS subscores by domain]

## Methods Context

### What?

> **Study design:** cross-sectional method-comparison study, per-domain breakdown of LLM vs. human gold-standard scores.
>
> **Method type:** zero-shot LLM evaluation against human consensus on each of 14 CONSORT-A domains.
>
> **Tools:** OpenAI ChatGPT GPT-3.5 (no version pin); CONSORT-A 15-item abstract reporting checklist (Moher et al. 2010); R v4.1.1.
>
> **Dependent variable:** mean absolute difference in per-domain OCS subscore (each item scored 0 / 0.5 / 1 by both human and ChatGPT) plus per-domain Welch's two-sample t-test p-value and Pearson's r.
>
> **Independent variable:** CONSORT-A domain (14 rows: trial design, participants, intervention, objective, outcome [methods], randomisation, blinding, number randomly assigned, number analysed, outcome [reporting], harms, conclusion, trial registration, funding).
>
> "Error analysis revealed small mean differences between human evaluation and ChatGPT in most domains (table 1). The mean difference in absolute OCS was highest for the 'conclusion' domain (0.764, 95% CI: 0.186, 0.280), indicating that ChatGPT differed the most from human evaluators in this domain." (Roberts et al., 2023, pp. 3–4)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-2.png]]

### How?

> **Procedure:** for each of the 14 CONSORT-A domains in Table 1, the 30 paired (human, ChatGPT) item-level scores (0 / 0.5 / 1) were used to compute (i) mean absolute difference with 95% CI, (ii) Welch's two-sample t-test p-value (P<0.001 deemed significant), and (iii) Pearson's r between the two raters' subscores. ChatGPT scoring used the single zero-shot prompt template in Figure 1A, definitions for all 15 CONSORT-A items provided up front, with the model asked to label each item completely / partially / not reported and then compute OCS = (1·I_C) + (0.5·I_P) + (0·I_N). The "conclusion" domain in CONSORT-A is binary in practice (a conclusion is either stated or not), so disagreement reflects the model's interpretation of "conclusion was stated" vs. the human reviewers'.
>
> "ChatGPT was used to score the same set of abstracts, using a prompt to assess for each domain within the CONSORT-A checklist (figure 1)… An overall compliance score (OCS) was given out of 15, along with an OCS percentage (figure 1B). This was performed using the GPT3.5 model." (Roberts et al., 2023, p. 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p3-3.png]]

### Who?

> **Models / participants:** ChatGPT GPT-3.5 (OpenAI; no version pin) vs. two human clinician reviewers (specialty / training stage not reported). Inference parameters not reported.
>
> **Sample-size flow:** Menne, Pandis & Faggion (2021) implant-dentistry RCT abstract corpus → **30 abstracts** sampled by the original authors → re-scored by two clinician reviewers with ≥80% consensus reconciliation (then one continued solo) → same 30 abstracts scored once by ChatGPT → **30 paired (human, ChatGPT) item-level scores per domain × 14 domains** entered Table 1's per-domain analyses.
>
> "In this study, we used a previously published paper as the basis of our comparison with ChatGPT. In their study, abstracts from a systematic review on implant dentistry were scored using the Consolidated Standards of Reporting Trials for Abstracts (CONSORT-A) statement by the human authors of the study." (Roberts et al., 2023, pp. 1, 3)
> ![[robertsComparativeStudyChatGPT2023-evd-p1-3.png]]

## Other Notes

- Lowest mean difference was 'blinding' (0.034, 95% CI 0.818, 0.895), indicating ChatGPT was most accurate there. Note the wide CI (0.818, 0.895) and high p-value (0.091) suggest the result is not significantly different from zero, i.e., agreement, not divergence.
- The CIs in Table 1 are inconsistent with the point estimates throughout (e.g., the 'conclusion' point estimate 0.764 falls outside its reported 95% CI 0.186, 0.280). These appear to be either typesetting errors or a different statistic mislabelled as a CI; the per-domain p-values and r values are internally consistent.
- Authors hypothesise prompt quality and ChatGPT's known instruction-following weaknesses as causes of the conclusion-domain divergence; no follow-up prompt-engineering experiments performed.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@robertsComparativeStudyChatGPT2023#TRIPOD-LLM reporting]].

| CONSORT-A domain | Mean abs. OCS diff | Welch p | Pearson r |
| --- | :---: | :---: | :---: |
| **Conclusion (highest divergence)** | **0.764** | **<0.001** | **0.06** |
| Randomisation | 0.633 | <0.001 | 0.11 |
| Outcome (methods) | 0.553 | <0.001 | 0.14 |
| Funding | 0.411 | <0.001 | 0.21 |
| Objective | 0.316 | <0.001 | 0.06 |
| Participants | 0.228 | 0.001 | 0.26 |
| Outcome (reporting) | 0.170 | <0.001 | 0.15 |
| Harms | 0.133 | <0.001 | 0.32 |
| Number randomly assigned | 0.105 | 0.006 | 0.31 |
| Trial design | 0.065 | 0.054 | 0.49 |
| Intervention | 0.057 | <0.001 | 0.02 |
| Trial registration | 0.045 | 0.002 | 0.34 |
| Blinding (lowest divergence) | 0.034 | 0.091 | 0.44 |
| Number analysed | 0.028 | 0.434 | 0.04 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can help automate appraisal of medical literature for reporting standard compliance]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]

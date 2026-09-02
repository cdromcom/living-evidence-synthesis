---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/risk-of-bias-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M2-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/42pct
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b79-776c-99b6-c4f4fe3f567d
appraisal_overall: L1-M2-H2
tripod_llm_pct: 42pct
---

## Source

[[@leucutaRiskBiasAssessment2025]]

## Description

> "In the patient selection domain, common issues included misinterpretation of consecutive sampling, particularly in the context of case-control designs, incorrect assumptions about sampling methods, and a failure to distinguish between exclusions made at the selection and analysis stages. LLMs also misclassified justified clinical exclusions as inappropriate." (Leucuta et al., 2025, p. 15)
> ![[leucutaRiskBiasAssessment2025-evd-p14-1.png]]

## Methods Context

### What?

> **Study design:** qualitative reasoning-error analysis nested within the Leucuta et al. cross-sectional QUADAS-2 LLM benchmark.
>
> **Method type:** investigator-driven thematic categorization of LLM rationales judged incorrect (either wrong answer, or correct answer with wrong reasoning) against a two-expert consensus reference; errors grouped by QUADAS-2 domain and signaling question.
>
> **Tools:** QUADAS-2 instrument (4 domains, 11 signaling questions); responses from ChatGPT 4o, x.AI Grok 3, Gemini 2.0 Flash, DeepSeek V3 collected via public web UIs; Supplementary Table S1 (per-article reasoning errors).
>
> **Dependent variable:** qualitative error type / theme per signaling question.
>
> **Independent variables / covariates:** QUADAS-2 domain; signaling question; LLM identity (errors aggregated across the four models rather than disaggregated).
>
> "For each article and each signaling question, we qualitatively evaluated the reasoning errors made by the LLMs. We then synthesized these errors by QUADAS-2 domain." (Leucuta et al., 2025, p. 10)
> ![[leucutaRiskBiasAssessment2025-evd-p10-1.png]]

### How?

> **Procedure:** (1) for each of the 10 diagnostic-accuracy articles and each of the 11 signaling questions, the team inspected every LLM response whose answer was incorrect, or whose answer was correct but whose argument was wrong, against the human-consensus reference; (2) errors were documented per article and question, then synthesized into themes within each QUADAS-2 domain (patient selection / index test / reference standard / flow and timing); (3) within the patient-selection domain, themes were organized by signaling question, "Was a consecutive or random sample of patients enrolled?", "Was a case-control design avoided?", and "Did the study avoid inappropriate exclusions?", and each theme illustrated with concrete examples drawn from the LLM rationales; (4) all responses and errors are presented in Supplementary Table S1; (5) the patient-selection domain yielded four major systematic error categories around consecutive sampling, inference about reporting, ambiguity handling, and representativeness, plus exclusion-handling errors.
>
> "Concerning the patient selection domain of QUADAS-2, the reasoning errors were observed by the following signaling question: Was a consecutive or random sample of patients enrolled? 1. Misunderstanding of consecutive sampling in case-control or subgroup design… 2. Inference errors concerning consecutive sampling based on the author's explicit reporting… 3. Ambiguity in authors' descriptions of sampling methods… 4. Misinterpreting representativeness." (Leucuta et al., 2025, pp. 10–11)
> ![[leucutaRiskBiasAssessment2025-evd-p10-2.png]]

### Who?

> **Models analyzed:** four general-purpose LLMs, ChatGPT 4o, x.AI Grok 3, Gemini 2.0 Flash, DeepSeek V3, accessed via public web interfaces during the study period. Errors aggregated across all four (not disaggregated per model in the qualitative synthesis).
>
> **Article sample-size flow:** PubMed search 9 May 2025 ("diagnostic accuracy"[TI/AB] AND diabetes[TI/AB], free full-text, most recent first) → original diagnostic-accuracy articles only → screened for medical-field diversity → **10 articles retained** (cardiology ×2, gastroenterology ×2, neurology ×1, rheumatology ×1, sleep medicine ×1, vascular surgery ×1, ophthalmology ×2).
>
> **Assessments inspected for errors:** all 4 models × 10 articles × 11 signaling questions = 440 assessments; the qualitative analysis covered the subset where the answer was incorrect or where a correct answer was paired with incorrect reasoning. Within patient selection alone (3 signaling questions × 10 articles × 4 models = 120 assessments), 79 were correct and 41 incorrect by the paper's tables → roughly 41 patient-selection assessments fed the patient-selection error themes.
>
> **Human reference:** two authors (medical informatics / biostatistics) independently assessed each article using QUADAS-2 and resolved disagreements by consensus.
>
> "The human assessment was performed by two authors who independently assessed the quality of the articles and resolved their discrepancies by discussion and consensus." (Leucuta et al., 2025, p. 2)
> ![[leucutaRiskBiasAssessment2025-evd-p2-1.png]]

## Other Notes

Four major error categories in patient selection: (1) misunderstanding consecutive sampling in case-control/subgroup designs; (2) inference errors about consecutive sampling based on author reporting; (3) ambiguity handling in contradictory author descriptions; (4) misinterpreting representativeness of diagnostic populations. These errors were systematic, not random.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@leucutaRiskBiasAssessment2025#TRIPOD-LLM reporting summary]].

| Patient-selection signaling question | Error theme(s) observed |
| --- | --- |
| Was a consecutive or random sample of patients enrolled? | (1) Misunderstanding consecutive sampling in case-control / subgroup designs (e.g., concluding consecutive sampling is impossible under case-control, or that having a target enrollment percentage per group precludes it; treating inclusion/exclusion criteria as invalidating consecutive sampling). (2) Inference errors from author reporting (asserting consecutive sampling occurred when not stated; treating absence of an explicit method as proof of non-use; missing clearly reported consecutive sampling). (3) Ambiguity handling (picking one of two contradictory author statements, "convenience" vs. "consecutive", instead of judging the design uninterpretable). (4) Misinterpreting representativeness (treating "patients with suspicion of a diagnosis" as non-representative even though it is the canonical diagnostic-test population). |
| Was a case-control design avoided? | Incorrectly classifying a single-sample design as case-control by anchoring on the authors' label rather than on how participants were actually recruited (e.g., one cohort assessed for disease and post-hoc split into cases/controls). |
| Did the study avoid inappropriate exclusions? | Misclassifying justified clinical exclusions as inappropriate without a medical argument; treating absence of an exclusion statement as proof of no exclusions; conflating exclusions at selection with exclusions at the analysis stage (which belong in flow and timing); failing to recognize that excluding "unclear" / poor-quality cases can itself induce bias. |

| Quantitative anchor (from Table 3, p. 9) | Value |
| --- | --- |
| Patient-selection correct rate (overall, 4 models × 10 articles × 3 Qs, n=120) | **65.83%** (79/120): the **second-lowest** of the four QUADAS-2 domains |
| Best models for patient selection | ChatGPT 4o (76.67%) and Grok 3 (73.33%); Gemini 2.0 Flash worst (50%) |

For the Methods/Results compliance items (5a–15, 16a–16d, 18) and the headline accuracy numbers, see the companion EVD and the source-file table linked above. Source-file `## TRIPOD-LLM reporting summary` is at [[@leucutaRiskBiasAssessment2025#TRIPOD-LLM reporting summary]] and includes Supplementary Table S1 as the full per-article error catalogue.

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]

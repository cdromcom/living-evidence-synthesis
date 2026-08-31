---
NodeFormality: draft
TruthValue: 0.75
aliases:
tags:
  - task/reporting-compliance-checking
  - 5c/credibility
  - 5c/clarity
  - ep/strength/5-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cca81355c38
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cca81355c38
---

## Pattern statement

Across at least five independent papers evaluating LLMs against human raters using structured reporting checklists or methodological scoring rubrics (CONSORT, PRISMA, ROBINS-I, QUADAS-2, STROBE), agreement varies dramatically by item type. LLMs match humans well on simple/structured/extractable items (presence-of-section checks, factual extraction, flow-diagram identification) but diverge sharply on items requiring methodological judgment (randomization adequacy, study-design assessment, eligibility-criteria evaluation, statistical-software detail).

## What is being claimed

The pattern is not "LLMs are bad at scoring papers." It is more specific: **headline aggregate accuracy hides item-level structure**. Where LLMs fail is exactly where reviewer expertise actually matters — the methodologically loaded items that require judgment about whether what the paper *did* was appropriate, not just whether what the paper *says* is present. Anyone deploying an LLM as a reporting-compliance scorer should expect strong agreement on superficial items and weak agreement on the items that drive overall paper quality.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]] — Alharbi & Asiri 2024: perfect agreement on simple items, significant discrepancy on randomization.
- [[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]] — Alharbi & Asiri 2024 (PRISMA twin): same pattern in the systematic-review domain.
- [[EVD - LLMs showed lowest accuracy on questions about statistical software used and study funding across all models - @akyonEvaluatingCapabilitiesGenerative2024]] — Akyon et al. 2024: LLMs lowest accuracy on items requiring detail extraction (stats software, funding).
- [[EVD - ChatGPT-human correlation was weakest in intervention and objective CONSORT-A domains r equals 0.02 and 0.06 - @robertsComparativeStudyChatGPT2023]] — Roberts et al. 2023: per-item Pearson r drops to 0.02–0.06 on methodologically loaded domains.
- [[EVD - ChatGPT diverged most from humans in the conclusion domain with mean difference 0.764 on CONSORT-A - @robertsComparativeStudyChatGPT2023]] — Roberts et al. 2023: largest divergence on the most subjective domain (conclusions).
- [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]] — Leucuta et al. 2025: systematic errors on the patient-selection domain (study-design judgment).
- [[EVD - GPT-4 achieved 61% raw percent agreement with Cochrane reviewers on ROBINS-I overall risk of bias with Kendall coefficient of 0.35 - @hasanIntegratingLargeLanguage2024]] — Hasan et al. 2024: 61% raw agreement varies sharply by ROBINS-I domain (47% confounding vs 71% intervention classification).
- [[EVD - GPT-4 Vision identified CONSORT flow diagrams with 100% accuracy but detected missing participant details at only 57% accuracy - @wrightsonGPTRCTsUsing2025]] — Wrightson et al. 2025: 100% on flow-diagram identification, only 57% on missing-detail detection.

## Connected discourse-graph nodes

- **Within-paper claims this pattern generalizes:** [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]], [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]].
- **Adjacent pattern (related):** [[EP - Aggregate-level LLM-human agreement masks near-zero per-paper correlation]] — overlap with this pattern via Roberts; per-item variance is *one mechanism* by which aggregate scores can match while per-paper correlations collapse.

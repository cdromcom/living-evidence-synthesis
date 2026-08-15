---
NodeFormality: draft
TruthValue: 0.8
aliases:
tags:
  - 5c/credibility
  - 5c/clarity
  - ep/strength/4-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec70653d5f69
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec70653d5f69
---

## Pattern statement

When zero-shot frontier LLMs are evaluated against human-rater consensus on standard evidence-appraisal tools (ROBINS-I, QUADAS-2, STROBE, PRISMA, AMSTAR), aggregate accuracy converges in a remarkably tight 60–80% band — across four independent papers, four different tools, four different LLM line-ups. Not a one-paper finding; a corpus-wide convergence.

## What is being claimed

The pattern is the practical-headline number for "how good are LLMs at evidence appraisal right now?" The answer is: **moderately good — too consistently good to dismiss, too consistently sub-human to deploy unsupervised.** Aggregate accuracy in this band is consistent with the within-paper finding that LLMs hit human level on simple items and miss on judgment-heavy items: the average over all items lands in the middle. For deployment, this band tells you that "LLM as a second reader, human-supervised" is the realistic frame, not "LLM replaces the rater."

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - GPT-4 achieved 61% raw percent agreement with Cochrane reviewers on ROBINS-I overall risk of bias with Kendall coefficient of 0.35 - @hasanIntegratingLargeLanguage2024]] — Hasan et al. 2024: GPT-4 reaches 61% raw agreement with Cochrane ROBINS-I judgments.
- [[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]] — Leucuta et al. 2025: mean across 4 LLMs hits 72.95% on QUADAS-2 (range 67–77%).
- [[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]] — Akyon et al. 2024: best LLM hits 66.9% on STROBE; range across 6 LLMs is 44–67%.
- [[EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans - @woelfleBenchmarkingHumanAICollaboration2024]] — Woelfle et al. 2024: individual LLMs hit 63–70% PRISMA / 53–74% AMSTAR vs. 89% humans.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]] — exact one-line statement of the pattern.
- **Mechanism behind the moderate-accuracy band:** [[EP - Per-item LLM-human agreement varies sharply by item type]] — the average comes from a mix of high-agreement items (extractable) and low-agreement items (methodologically loaded).
- **Path to higher accuracy:** [[EP - Human-AI collaboration outperforms either alone on structured appraisal tasks]], [[EP - Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks]] — both EPs identify approaches that move beyond the moderate-accuracy band.

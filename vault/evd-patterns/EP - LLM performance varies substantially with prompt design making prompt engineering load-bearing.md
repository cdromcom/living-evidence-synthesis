---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - 5c/credibility
  - ep/strength/4-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc81-bad6-76e4-b874-ec77b19ef454
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc81-bad6-76e4-b874-ec77b19ef454
---

## Pattern statement

LLM performance on scientific-evaluation tasks varies *substantially* with prompt design — large enough that prompt engineering is a load-bearing experimental variable, not a tuning detail. Across at least four independent papers, varying the prompt for the same task produces accuracy or output-completeness differences that are larger than typical model-vs-model differences on the same benchmark.

## What is being claimed

The pattern is methodological: any single-prompt evaluation of an LLM is reporting a *lower bound* on what that LLM can do, and the true ceiling is unknown without prompt-engineering search. Within-LLM variance across prompt variations matches or exceeds across-LLM variance under a single prompt. The pattern has two implications: (1) for benchmark interpretation, single-prompt results understate model capability; (2) for deployment, prompt engineering is a real engineering surface that materially shapes accuracy and should be invested in.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - LLM confounder designation was highly inconsistent with Cohen kappa as low as 0.16 across prompt variations - @huntington-kleinLLMsActRepositories2024]] — Huntington-Klein & Murray 2024: same LLM, different prompts → Cohen κ as low as 0.16 across prompt variations on the same questions.
- [[EVD - LLMs performed suboptimally identifying placebo arm suitability and risk mitigation in single prompt - @sridharanLeveragingArtificialIntelligence2025]] — Sridharan & Sivaramakrishnan 2025: single-prompt strategy missed substantive items that a multi-prompt strategy recovered.
- [[EVD - GPT-4 correctly detected errors in 7 of 13 constructed short CS papers - @liuReviewerGPTExploratoryStudy2023]] — Liu & Shah 2023: chain-of-thought-style prompting (Liu's prompt) achieves 7/13; the Liu paper notes that other prompts tested in pilot did not work at all.
- [[EVD - Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% to 13.79% - @shahidLiteratureGroundedNoveltyAssessment2025]] — Shahid et al. 2025: removing one prompt-and-retrieval scaffold step (facet-based RankGPT) drops accuracy from 89.66% to 13.79% — a 76-percentage-point gap from a prompt-architecture choice.

## Connected discourse-graph nodes

- **Within-paper claim this pattern generalizes:** [[CLM - LLM novelty evaluation is highly sensitive to prompt variations making results difficult to replicate]] (Shahid's framing of the same finding).
- **Methodological caveat this pattern motivates:** [[CVT - A single standardized prompt was used across all LLMs without prompt engineering potentially underestimating LLM capabilities in QUADAS-2 assessment]] — single-prompt evaluations under-report capability; this pattern is the cross-paper evidence that the CVT's concern is real.
- **Compatible pattern:** [[EP - RAG and few-shot prompting improve LLM performance but rarely close the human gap]] — prompt design changes both *whether* scaffolding is applied and *how* — both axes matter.

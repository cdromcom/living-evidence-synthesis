# Pipeline phases and models: best set, cross-checked, swappable

Status: plan by Claude on JP's instruction (2026-11-24). It follows JP's v2 toolchain in `vault/pipeline/skills/Tools-and-Models.md` (hosted APIs, US developers only) and does not add new model decisions; rows marked "to confirm" need JP. Benchmark numbers come from `benchmarking-validation/` and were tuned on the same 66 to 68 rows, so they are encouraging, not a clean test.

## Rules for every phase

1. **Best available model for the job**, chosen from the model registry, not from memory or a leaderboard.
2. **A validator from a different model family** (or a deterministic check) for every model output that reaches the vault. Two models from one family do not count as independent.
3. **Swappable.** A phase talks to its model only through the registry and a fixed input and output format, so replacing a model is a one-line change plus a re-run of the fixed test set.
4. **US developers only** (JP, 2026-11-20). Record each model's developer, base model and licence.

## Phases, from PDF to web app

| # | Phase | Primary | Independent check | Human gate |
|---|---|---|---|---|
| 0 | Intake: pick the paper version, DOI, licence | scripts (Crossref, Unpaywall) | Opus 5.5 only on ambiguous versions | JP |
| 1 | Parse the PDF to page markdown and tables | GPT-6.2 Sol (PDF input, High) | PyMuPDF text layer as second vote; where they disagree the page image decides; scanned pages get the two-OCR agreement rule (Chandra OCR 2 + OXR-1.0, to confirm) | none unless images decide |
| 2 | PICOST extraction (paper level) | GPT-6.2 Sol (High) | Opus 5.5 on parser disagreements plus a 10% sample; Liquid d1-ultra check is on hold (JP) | JP spot check |
| 3 | Find and write nodes (QUE, EVD, CLM, CVT) | Sonnet drafts; GPT-6.2 Sol (Medium) and Inkling 2 Small vote; Opus 5.5 checks and edits | three different families already in the loop | JP reviews EVDs |
| 4 | Quotes, screenshots, page numbers | PyMuPDF word coordinates and `pdftoppm` (deterministic) | verbatim audit script; decision-model grounding check in shadow mode: the average of Perplexity, Liquid and Jev reached 97% on 66 quote rows | JP on disagreements |
| 5 | Number and page checks | audit scripts | a second model family reads the page image | JP |
| 6 | Relevancy and fidelity judging | relevancy: average of Perplexity Decider 1.3, Liquid d1-ultra and Opus 5.5 (97 to 98.5% on 68 rows against 92.6% for always "Relevant") | disagreements logged and sent to JP | JP; **fidelity stays human for now**: no rater beat always-Met (93.9%) and kappa was near zero |
| 7 | Synthesis: claims and evidence patterns | Opus 5.5 | GPT-6.2 Sol writes an independent critique; contradictions listed | JP |
| 8 | Build the graph and the data files | `scripts/build-graph.mjs` (deterministic) | graph counts and snapshot tests in CI | none |
| 9 | Build and publish the web app | Claude Opus 5.5 in this repository; Muse Wonder Max and GPT-6.2 Sol are bake-off candidates (see `redesign/decisions.md`) | a different model family reviews each change; axe, Playwright keyboard tests and Lighthouse in CI | JP approves each release |

## Making it modular

- **Model registry** (`config/models.json`, to create): one entry per model with id, developer, base model, licence, version string, role, price, and where it runs. Phases read it; no phase hard-codes a model name.
- **Fixed contract per phase**: a JSON input and output schema, and one **run record** per call (model id and version, prompt hash, tokens, time, cost, output hash). `benchmarking-validation/` already records this for the decision models.
- **Fixed test set per phase**: JP's validated judgments, the 147 PDF-audit corrections and the version comparisons. Any change to a model or prompt re-runs it first; the change ships only if it clears the phase's pass bar (for example every quote verbatim, every number correct, kappa 0.6 or higher with JP).
- **Shadow mode**: a new model runs next to the current one and its output is logged but not used until it matches or beats the current one on the test set.
- **Fallbacks**: each phase names its fallback model in the registry so an API outage or price change does not stop the pipeline.

## Open items for JP

- Confirm Chandra OCR 2, OXR-1.0, Ripple-65B Preview and Inkling 2 Small origins and licences (the base-model check).
- Decide when to switch Liquid d1-ultra back on for PICOST QA.
- Decide whether the bake-off in phase 9 is worth the day it takes.

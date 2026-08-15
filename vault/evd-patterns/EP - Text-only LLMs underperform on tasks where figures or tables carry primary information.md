---
NodeFormality: draft
TruthValue: 0.7
aliases:
tags:
  - 5c/credibility
  - ep/strength/2-papers
  - ep/scope/cross-paper
created: 2026-04-29
updated: 2026-04-29
nodeID: 019ddc10-aada-707e-ac01-1cd0508396ea
nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh
nodeInstanceId: 019ddc10-aada-707e-ac01-1cd0508396ea
---

## Pattern statement

LLMs that process only text (text-only frontier models, or multimodal models when fed text-only inputs) underperform on scientific-evaluation tasks where figures, flow diagrams, image-rendered tables, or visual layout carry primary content. The gap is task-specific: figure-heavy verifications (figure duplication, flow-diagram validation, panel-content checks) suffer the most, while equation-style verifications via LaTeX source can recover.

## What is being claimed

The pattern says text/non-text input has a substantive effect on accuracy that researchers and tool builders need to plan for. A scientific-error-detection system fed only PDF-extracted text will systematically miss errors localized in figures (image manipulation, panel duplication, mismatched legends). Even reasoning models that excel at equation-proof verification on LaTeX source collapse near zero on figure-duplication detection. Multimodal models (Vision-style) close some but not all of the gap — they can identify a flow diagram, but still struggle with fine-grained content within it.

## Supporting Evidence

> [!info] EVDs from independent papers that instantiate this pattern.

- [[EVD - GPT-4 Vision identified CONSORT flow diagrams with 100% accuracy but detected missing participant details at only 57% accuracy - @wrightsonGPTRCTsUsing2025]] — Wrightson et al. 2025: multimodal GPT-4 Vision correctly identifies *whether* a flow diagram exists (100%) but only catches missing participant details inside the diagram 57% of the time.
- [[EVD - o3 achieved 62.6% pass@4 on equation-proof errors while scoring near 0% on figure duplication - @sonWhenAICoScientists2025]] — Son et al. 2025: o3 reaches 62.6% on equation-proof errors (text/LaTeX-encodable) but near-zero on figure-duplication errors (figure-only) — a 60-percentage-point gap driven by input modality.

## Connected discourse-graph nodes

- **Caveats that flag this gap structurally:** [[CVT - Most LLMs were text-only and blind to figures and image-rendered tables relevant for evidence appraisal]], [[CVT - The AAAR benchmark excluded non-textual inputs such as figures that are integral to scientific evaluation]] — these CVTs document the gap from the *evaluation* side; this EP documents it from the *finding* side.
- **Adjacent pattern (per-item variance, related):** [[EP - Per-item LLM-human agreement varies sharply by item type]] — visual-content items are one specific kind of item where LLMs struggle.

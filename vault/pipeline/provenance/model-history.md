---
title: Model history by date
type: provenance
---
# Which model wrote what, by date

A node's footer says exactly which model made it when a call log exists. Pages from before the call log are placed in an era below. Recorded means a file in this vault or the GitHub history says so. "Per JP" means the owner remembers it, but no file records it.

| Era | Dates | Model | What it made | How we know |
|---|---|---|---|---|
| 1 | 2026-04-17 (first extraction) to spring and summer 2026 | Claude Sonnet 4.6 (Claude Code) | First SRC, QUE, CLM, EVD, CVT pages; links between them | `Tools-and-Models.md` (Sonnet 4.6); spring/summer use per JP |
| 1b | 2026-04-28 | Batch subagents, model not recorded | First TRIPOD-LLM tables (Phase 18, 26 agents) and Quality appraisal prose (Phase 19) | Phase logs record the phase, not the model |
| 2 | 2026-08-25 | Claude Sonnet 5 | SRC page curation, quotes and quality tables re-curated | `curatedWithModel`, `curatedWithModelDate` in all 26 SRC pages |
| 3 | 2026-11-23 on | Perplexity Decider 1.3, Liquid d1-ultra, Jev 1.14.0, Claude Opus 5.5 | Decision-model benchmarks against JP's ratings (77 EVDs) | `pipeline/misc/evd-validation/` |
| 5 | 2026-11-26 on | Claude Sonnet 5.5 (quote and verification screenshots), Perplexity Decider 1.3, Liquid d1.2-ultra (text and screenshots), Claude Opus 5.5 (failure analysis, EVD rework) | Verification of every extracted item, quote checks, numbers check, EVD redrafts under the new rules | `pipeline/runs/<run>/verification.json`, review sheet tabs, `misc/evd-validation/LOG.md` |
| 4 | 2026-11-25 on | Logged per call | New runs; design consult (Fable 5.2, GPT-6.2 Sol, Opus 5.5, Sonnet 5.5); batch runner extraction (Gemini 4 Neon), rechecks (GPT-6.2 Sol) and adjudication (Opus 5.5); planned: drafting by debate (Sonnet 5.5, Sol, Neon) and quality-signal rating (Opus 5.5, Sol, Neon) | `pipeline/runs/<run>/calls.jsonl` and `manifest.json` |

## History of one page
A page can have several authors over time. To list them, take the page's commit dates from GitHub (`git log --format='%h %ad' --date=short -- <path>`) and place each date in the table. `scripts/file_model_history.py <path>` does that.

Open items: confirm the model of the April 28 batch agents if any log turns up; confirm which pages were rewritten in the summer.

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

## Update 2026-11-27 (lean model plan, local aim, tables, verification)

**Lean model plan (JP, 2026-11-27; pending validation, not built).** Target at most $2.49 per paper for extraction, quality signals, TRIPOD-LLM and the quality appraisal table. Quality signals and TRIPOD-LLM rows: Gemini 4 Neon (high) rates every row; low-confidence rows go to GPT-6.2 Sol (high); if Sol is also unsure the row goes to JP; Opus 5.5 is not used. Verification: when the two decision models disagree, Neon (medium) judges instead of Sonnet 5.5. Quote reading from screenshots: Neon replaces Sonnet. Drafting: first drafts by GPT-6.2 Sol only, critique by Neon only, tiebreaker Sonnet 5.5. EVD rework below 0.60: Sol (medium). Classifying sampled problems: a small local model to try (Neon low as the hosted fallback). Grouping questions, claims, evidence and caveats: EmbeddingGemma 2 (local) finds candidates, Neon (medium) decides. The estimate from pilot logs is about $3.0 to $3.5, above the target (see `misc/evd-validation/TODO.md`). Until JP validates it, the three-rater maximum-accuracy setting remains the default in `config/models.json`.

**Verification and decision models (2026-11-27).** `decision_models.resolve_preferred()` tries `d1.3-ultra` first and keeps `d1.2-ultra` while the API returns 404 (it did on 2026-11-27). Baseten bison-1 (31B, $0.10 per million tokens) runs as a text-only shadow verifier and is not in any vote: on 226 Woelfle items it agrees with d1.2-ultra 79%, Perplexity 81%, Sonnet 86%, passes PICOST slots almost always (1% below 0.5), and its image test was unreliable. Each stage now records elapsed seconds and request count in `stage_log`.

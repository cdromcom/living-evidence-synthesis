---
type: prompt
id: draft-nodes-v2
used_by: pipeline/scripts/lives_stages.py (draft, round 0; Sonnet 5.5, GPT-6.2 Sol, Gemini 4 Neon Medium; Inkling 2 Small as a benchmark-only shadow)
written: 2026-11-25
---

You write discourse-graph nodes for a living evidence synthesis about LLMs in scientific research and peer review. You are given the extraction of one paper: the paper's own questions (original wording and a reframed question), PICOST findings with tiers, locators, numbers and verbatim spans, and claims and caveats with verbatim spans. Every finding, claim and caveat is linked to the questions and findings it belongs to. Work ONLY from this extraction: use no outside knowledge and invent nothing. Return one JSON object and nothing else.

## Node types and rules
**EVD (evidence), one per finding you are given (all tiers).**
- `statement`: one finding, at most 247 characters (count them), in this pattern: [named model(s)] [prompting, only if the paper states it] [verb] [N + field + "research reports"] [task or instrument], [result against a comparator] ([metric = value, ...]). Name every model ("GPT 3.5-turbo", not "ChatGPT"); call custom systems "bespoke"; give N, the field and the data source; always give a comparator (humans, other models, a baseline), including a row that contradicts the headline; put statistics in parentheses with spelled-out metric names ("Cohen's kappa", "F1 score", "Fisher's exact test p > 0.05"); prefer kappa and F1 to accuracy; round sensibly.
- Every number in the statement must appear in the finding's numbers or spans. Never add a number, a model, a comparator or a direction that the extraction does not contain.
- A secondary EVD's statement says what it qualifies (for example the human raters' agreement behind a primary kappa). Write plain sentences (a high-school graduate should follow them): active voice, short, jargon explained, no arrows or slashes.
- `quote`: the finding's best verbatim span, copied exactly. `page`: its printed page.
**QUE (question), one per question you are given.** `title` is the question in everyday words, clear and granular (one capability per question; the extraction's `reframed` is a starting point you may improve): start from the canonical phrasings if one fits ("How well can LLMs identify errors in research reports?", "How accurately can LLMs evaluate research reports' alignment with reporting guidelines?", "How well can LLMs review research reports?", "How accurately can LLMs evaluate research reports' methodological rigor using critical appraisal tools?", "How well can LLMs evaluate the novelty of research reports?", "How do LLM-generated peer reviews compare to human-generated peer reviews in quality?", and similar); strip implementation detail ("without fine-tuning", "automatically", "using PRISMA"); name the capability, not the method. `original_wording`: the verbatim span.
**CLM (claim), one per claim you are given.** `statement`: one generalization the paper's evidence supports, in one sentence, no stronger than the quote; `quote`: the verbatim span; `supports`: the ids of the EVD nodes it rests on.
**CVT (caveat), one per caveat you are given.** `limitation`: one limitation in one sentence; `quote`: the verbatim span; `applies_to`: the ids of the EVD nodes it qualifies.

## Style (JP, 2026-11-25)
Write like a person: plain words, concrete, no filler. Use no em dashes (use commas, periods, colons or parentheses). Say each thing once; cut repeated or padded wording. Keep every statement skimmable.

## Output (JSON only)
{"nodes": [
 {"id": "E-F1", "type": "EVD", "source_id": "F1", "tier": "primary", "answers_QUE": ["Q-Q1"], "supports_EVD": [], "statement": "", "quote": "", "page": ""},
 {"id": "Q-Q1", "type": "QUE", "source_id": "Q1", "title": "", "original_wording": ""},
 {"id": "C-C1", "type": "CLM", "source_id": "C1", "answers_QUE": ["Q-Q1"], "statement": "", "quote": "", "supports": ["E-F1"]},
 {"id": "V-V1", "type": "CVT", "source_id": "V1", "limitation": "", "quote": "", "applies_to": ["E-F1"]}]}
Use the ids "E-", "Q-", "C-", "V-" followed by the source id. Write one node for every item you were given. Keep every link: an EVD names the questions it answers (`answers_QUE`, using the "Q-" ids) and, for secondary and tertiary EVDs, the primary EVDs it supports (`supports_EVD`); a CLM names the questions it answers and the EVDs it rests on; a CVT names the EVDs it qualifies.

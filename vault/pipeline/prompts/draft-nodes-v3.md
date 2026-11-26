---
type: prompt
id: draft-nodes-v3
used_by: pipeline/scripts/lives_stages.py (draft, round 0; Sonnet 5.5, GPT-6.2 Sol, Gemini 4 Neon Medium; Inkling 2 Small as a benchmark-only shadow)
written: 2026-11-26
changes: v3 rewrites the EVD rules from JP's own EVDs in the sheet LIVES - AAA Benchmarking (HAI), tabs LIVES - EVD and LIVES-EVD-Benchmarking (Woelfle examples EVD 16, 32, 43, 45, 47), and allows at most one set of parentheses per EVD (JP, 2026-11-26).
---

You write discourse-graph nodes for a living evidence synthesis about LLMs in scientific research and peer review. You are given the extraction of one paper: the paper's own questions (original wording and a reframed question), PICOST findings with tiers, locators, numbers and verbatim spans, and claims and caveats with verbatim spans. Every finding, claim and caveat is linked to the questions and findings it belongs to. Work ONLY from this extraction: use no outside knowledge and invent nothing. Return one JSON object and nothing else.

## Node types and rules
**EVD (evidence), one per finding you are given (all tiers).** Write the way JP writes his own EVDs.
- `statement`: one finding in one sentence, at most 247 characters (count them). Order: [named model or models, each with its exact name: "Claude 3 Opus", "GPT 3.5", "Mixtral-8x22B"; "bespoke" for a custom system] [prompting, only if the paper states it: zero-shot, few-shot] [past-tense verb: appraising, evaluating, checking, reviewing] [N + field + "research reports" or the paper's own object, such as "112 systematic reviews in pediatric surgery"] [the task or tool, such as "for alignment with the reporting guideline PRISMA"], [the result against a comparator: "losing to human experts", "agreed less", "was 100X more expensive than Mixtral-8x22B"] ([the numbers]).
- **One set of parentheses at most.** Put all statistics in that one set, at the end, separated by semicolons or "vs.", for example (Cohen's kappa = 0.40-0.51 vs. 0.81). Use no other parentheses, and no brackets. Anything else that would go in parentheses goes into the sentence in words, or is left out.
- Always give a comparator (humans, another model, a baseline), including a result that contradicts the headline. Spell out metric names ("Cohen's kappa", "F1 score", "accuracy"); prefer kappa and F1 to accuracy; write ranges with a hyphen (63-70%); write multiples as 100X; round sensibly.
- Call papers "research reports". Give N and the field (and the data source when the paper names one). Do not use Greek letters or symbols: write kappa, not κ.
- Every number in the statement must appear in the finding's numbers or spans. Never add a number, a model, a comparator or a direction that the extraction does not contain.
- A secondary EVD's statement says what it qualifies (for example the human raters' agreement that serves as the reference standard). Plain sentences (a high-school graduate should follow them): active voice, short, no arrows or slashes.
- Examples written by JP (study the structure, do not copy the content):
  1. Unifying Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B reached 75-88 percent accuracy when applying PRISMA, deferring 4-74 percent.
  2. GPT-4 appraising medical research reports was 100X more expensive than Mixtral-8x22B (medians: 115.00 USD vs. 1.20 USD).
  3. LLMs Claude-3-Opus, GPT-3.5, and GPT-4 zero-shot evaluated 112 systematic reviews and meta-analyses in pediatric surgery for alignment with the reporting guideline PRISMA, losing to human experts (LLM accuracy: 63-70% vs. human accuracy: 89%).
  4. Human raters, the reference standard for LLMs appraising medical research reports, agreed less as the tools got harder (Cohen's kappa: PRISMA = 0.84, AMSTAR = 0.77, PRECIS-2 = 0.29 weighted).
  5. Compared to a human rater, Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B zero-shot appraising 112 pediatric surgery systematic reviews with the reporting guideline PRISMA agreed less (Cohen's kappa = 0.40-0.51 vs. 0.81). (This is JP's example 47 with its two parenthetical groups merged into one.)
- `quote`: the finding's best verbatim span, copied exactly. `page`: its PDF page.
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

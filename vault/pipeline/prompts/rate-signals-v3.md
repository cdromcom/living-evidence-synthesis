---
type: prompt
id: rate-signals-v3
used_by: pipeline/scripts/lives_stages.py (quality-signal and TRIPOD-LLM rating; the raters and the fallback rater named in pipeline/config/models.json, roles.raters and roles.qs_fallback)
written: 2026-11-27
changes: v3 (JP, 2026-11-27) adds a `confidence` field (high, medium or low) to every rating. A rating given with low confidence goes to a fallback rater; if the fallback rater is also low, a person decides. Everything else is unchanged from v2 (anchors instead of a whole quote, JP, 2026-11-26).
---

You rate one research paper (the attached PDF, or its text) on the quality signals below, independently and without seeing anyone else's ratings. For every signal give one rating from its allowed values, and point to the passage in the paper that justifies it with three things: `page` (the PDF page, position in the file, first page = 1: never the printed page number), `quote_start` (the first 6 to 10 words of the passage, copied character for character from the paper) and `quote_end` (the last 6 to 10 words of the same passage, copied the same way). Choose the shortest passage that justifies the rating: one sentence or one table row, never more than 3 sentences. If the paper is silent (which usually means not addressed or not disclosed), write `none` in `quote_start` and leave `quote_end` empty. Add `locator` as the section and any table or figure, for example `Methods, Table 2` (no page number: code adds it). Add `confidence`: `high` when the passage settles the rating, `medium` when it is a judgment call between two neighbouring ratings, `low` when the paper is unclear, contradicts itself, or you could not find the passage with certainty. Use `low` whenever you are unsure; a person or a second model will then check the row, which costs little, while a confident wrong rating is not checked. Do not guess: the absence of something is itself the rating. Return one JSON object and nothing else.

## Signals and allowed values
{SIGNALS}

## Output (JSON only)
{"ratings": [{"signal": "baseline-adequacy", "rating": "partial", "page": 5, "quote_start": "first six to ten words", "quote_end": "last six to ten words", "locator": "Methods, Table 2", "confidence": "high"}]}
Write one entry for every signal listed.

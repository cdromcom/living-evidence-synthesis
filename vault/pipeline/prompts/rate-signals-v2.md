---
type: prompt
id: rate-signals-v2
used_by: pipeline/scripts/lives_stages.py (quality-signal rating; Opus 5.5, GPT-6.2 Sol and Gemini 4 Neon Medium count; Inkling 2 Small is benchmark-only)
written: 2026-11-26
changes: v2 asks for anchors instead of a whole quote: the first and the last words of the passage, copied exactly, plus the PDF page. Code takes the exact PDF text between them (JP, 2026-11-26).
---

You rate one research paper (the attached PDF, or its text) on the quality signals below, independently and without seeing anyone else's ratings. For every signal give one rating from its allowed values, and point to the passage in the paper that justifies it with three things: `page` (the PDF page, position in the file, first page = 1: never the printed page number), `quote_start` (the first 6 to 10 words of the passage, copied character for character from the paper) and `quote_end` (the last 6 to 10 words of the same passage, copied the same way). Choose the shortest passage that justifies the rating: one sentence or one table row, never more than 3 sentences. If the paper is silent (which usually means not addressed or not disclosed), write `none` in `quote_start` and leave `quote_end` empty. Add `locator` as the section and any table or figure, for example `Methods, Table 2` (no page number: code adds it). Do not guess: the absence of something is itself the rating. Return one JSON object and nothing else.

## Signals and allowed values
{SIGNALS}

## Output (JSON only)
{"ratings": [{"signal": "baseline-adequacy", "rating": "partial", "page": 5, "quote_start": "first six to ten words", "quote_end": "last six to ten words", "locator": "Methods, Table 2"}]}
Write one entry for every signal listed.

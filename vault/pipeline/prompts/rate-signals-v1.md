---
type: prompt
id: rate-signals-v1
used_by: pipeline/scripts/lives_stages.py (quality-signal rating; Opus 5.5, GPT-6.2 Sol and Gemini 4 Neon Medium count; Inkling 2 Small is benchmark-only)
written: 2026-11-25
---

You rate one research paper (the attached PDF, or its text) on the quality signals below, independently and without seeing anyone else's ratings. For every signal give one rating from its allowed values, a verbatim quote from the paper that justifies it (or `none` if the paper is silent, which usually means not addressed or not disclosed), and a locator in the form `Section, p.<printed page>[, Table n | Fig n]` (use `PDF p. N` when the file prints no page numbers). Quotes must be copied exactly from the paper. Do not guess: the absence of something is itself the rating. Return one JSON object and nothing else.

## Signals and allowed values
{SIGNALS}

## Output (JSON only)
{"ratings": [{"signal": "baseline-adequacy", "rating": "partial", "quote": "verbatim or none", "locator": "Methods, p.5"}]}
Write one entry for every signal listed.

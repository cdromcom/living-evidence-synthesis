---
type: prompt
id: adjudicate-signals-v2
used_by: pipeline/scripts/lives_stages.py (quality signals; GPT-6.2 Sol decides only the signals where the two raters, Neon (High) and Opus 5.5, disagreed)
written: 2026-11-25
---

You are the third rater of a research paper (the attached PDF). Two raters disagreed on the quality signals listed below. For each one you are shown both raters' ratings, quotes and locators, with their names hidden (Rater 1 and Rater 2). Read the paper yourself and decide the rating that the paper itself supports, from the allowed values. You may agree with either rater or give a third rating. Check each quote against the paper; a quote that is not in the paper counts against that rater. Give your own passage as anchors: `page` (PDF page, position in the file), `quote_start` and `quote_end` (the first and last 6 to 10 words of the passage, copied exactly; one sentence or table row, at most 3 sentences). Do not guess: the absence of something is itself the rating. Return one JSON object and nothing else.

## Signals in dispute, with allowed values
{SIGNALS}

## Output (JSON only)
{"ratings": [{"signal": "baseline-adequacy", "rating": "partial", "page": 5, "quote_start": "first six to ten words, or none", "quote_end": "last six to ten words", "locator": "Methods, Table 2", "reason": "one sentence"}]}
Write one entry for every signal listed.

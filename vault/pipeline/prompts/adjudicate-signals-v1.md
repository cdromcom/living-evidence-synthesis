---
type: prompt
id: adjudicate-signals-v1
used_by: pipeline/scripts/lives_stages.py (quality signals; GPT-6.2 Sol decides only the signals where the two raters, Neon (High) and Opus 5.5, disagreed)
written: 2026-11-25
---

You are the third rater of a research paper (the attached PDF). Two raters disagreed on the quality signals listed below. For each one you are shown both raters' ratings, quotes and locators, with their names hidden (Rater 1 and Rater 2). Read the paper yourself and decide the rating that the paper itself supports, from the allowed values. You may agree with either rater or give a third rating. Check each quote against the paper; a quote that is not in the paper counts against that rater. Do not guess: the absence of something is itself the rating. Return one JSON object and nothing else.

## Signals in dispute, with allowed values
{SIGNALS}

## Output (JSON only)
{"ratings": [{"signal": "baseline-adequacy", "rating": "partial", "quote": "verbatim or none", "locator": "Methods, p.5", "reason": "one sentence"}]}
Write one entry for every signal listed.

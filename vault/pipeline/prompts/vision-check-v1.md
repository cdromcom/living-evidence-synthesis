---
type: prompt
id: vision-check-v1
used_by: pipeline/scripts/lives_stages.py (checks; GPT-6.2 Sol vision on flagged crops, low-confidence checks and a 10% sample; Opus 5.5 on rare disputes)
written: 2026-11-25
---

You are given a cropped screenshot from a research paper (with the quoted text highlighted) and the finding it is supposed to support. Look at the image and answer for each item: (1) does the crop show the whole quote, with nothing cut off at the top or bottom; (2) is the highlighted text exactly the quote given; (3) do the table row, column or figure caption visible in the crop support the stated value (say `not applicable` if the finding does not rest on a table or figure); (4) does the crop support the statement, with the right model, condition and direction. Be strict. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"id": "F1", "whole_quote": true, "quote_matches": true, "table_or_figure_supports": true, "supports_statement": true, "overall": "pass", "reason": "one sentence"}]}

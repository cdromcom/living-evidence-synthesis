---
type: prompt
id: vision-check-v2
used_by: pipeline/scripts/lives_stages.py (checks; GPT-6.2 Sol vision on every finding's crop; Opus 5.5 on rare disputes)
written: 2026-11-25
changes: v2 adds the outcome cannot_verify (JP, 2026-11-25)
---

You are given a cropped screenshot from a research paper (with the quoted text highlighted) and the finding it is supposed to support. Look at the image and answer for each item: (1) does the crop show the whole quote, with nothing cut off at the top or bottom; (2) is the highlighted text exactly the quote given; (3) do the table row, column or figure caption visible in the crop support the stated value (say `not applicable` if the finding does not rest on a table or figure); (4) does the crop support the statement, with the right model, condition and direction. Be strict, but do not guess. If the crop does not show enough to decide (the quote is cut off, the table or figure is not in the crop, the text is unreadable, or the statement rests on something outside the crop such as the methods), the overall result is `cannot_verify`, and the reason says what is missing so a person can look. Use `fail` only when the crop shows the finding is wrong. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"id": "F1", "whole_quote": true, "quote_matches": true, "table_or_figure_supports": true, "supports_statement": true, "overall": "pass | fail | cannot_verify", "reason": "one sentence"}]}

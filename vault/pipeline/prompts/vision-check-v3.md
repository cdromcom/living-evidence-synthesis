---
type: prompt
id: vision-check-v3
used_by: pipeline/scripts/lives_stages.py (checks; GPT-6.2 Sol vision on every finding's crop; Opus 5.5 on rare disputes)
written: 2026-11-25
changes: v2 added the outcome cannot_verify (JP, 2026-11-25). v3 narrows it: in the first reruns 80% of findings came back cannot_verify because the crop does not show the study's sample size, model settings or comparator, which sit elsewhere in the paper. v3 judges only what the crop is supposed to show: the quote, the numbers and the direction.
---

You are given a cropped screenshot from a research paper (with the quoted text highlighted) and the finding it is supposed to support. The crop is only the region around the evidence; it will not show everything in the statement (the sample size, the study design or a comparator may be stated elsewhere in the paper). Judge only what the crop is meant to show. Answer for each item: (1) `whole_quote`: does the crop show the whole quote, with nothing cut off at the top or bottom; (2) `quote_matches`: is the highlighted text the quote given (ignore differences in dashes, spacing and symbols); (3) `numbers_match`: does every number in the statement that is meant to come from this crop appear in it with the same value, row, column or caption (`not applicable` if the finding has no numbers); (4) `direction_right`: does the crop support the direction and the comparison the statement draws from these numbers (higher or lower, better or worse, significant or not).

Overall result:
- `pass`: the quote is shown and matches, the numbers match, and the direction is right. Details of the statement that the crop is not meant to show do not stop a pass; list them in `unseen`.
- `fail`: the crop shows the finding is wrong: a number differs, the direction is reversed, or the quote says something else.
- `cannot_verify`: only when the crop itself prevents the judgment: the quote or table is cut off, the evidence is not in the crop, or the text is unreadable. Say what is missing in `reason`.
Do not guess, and do not use `cannot_verify` just because the statement mentions things outside the crop. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"id": "F1", "whole_quote": true, "quote_matches": true, "numbers_match": true, "direction_right": true, "overall": "pass | fail | cannot_verify", "unseen": "parts of the statement the crop does not show, or empty", "reason": "one sentence"}]}

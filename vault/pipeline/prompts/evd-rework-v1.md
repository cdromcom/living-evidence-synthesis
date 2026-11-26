---
type: prompt
id: evd-rework-v1
used_by: pipeline/scripts/lives_stages.py (draft, rework of EVD statements whose decision-model score is below 0.60; Claude Opus 5.5, a different model from the three drafting authors)
written: 2026-11-26
---

Two decision models scored a drafted EVD statement below 0.60 on fidelity, on numbers-in-source, or on both. You decide whether the statement has a real problem and, if it does, rewrite it. You are given the statement, the finding it was drafted from (statement, PICOST, the Numbers list with each number's table or figure, row, column and printed page, and the source span or spans), the two decision-model scores with the lowest question named, and a screenshot of the source with the quoted text highlighted. Work ONLY from these. Do not use outside knowledge. Return one JSON object and nothing else.

## Steps
1. **Numbers.** For every number in the EVD statement, say where you found it: `span` (in the source span), `numbers_list` (in the Numbers list), `screenshot` (visible in the screenshot only) or `nowhere`. A number that is in none of the three is a problem.
2. **Fidelity.** Check the named models, prompting method, data, comparator, direction (higher, lower, better, worse, significant or not) and scope against the same material. List each mismatch in one short phrase.
3. **Verdict.**
   - `ok`: every number is found and nothing in the statement goes beyond the material. The decision models were wrong. Leave `revised_statement` empty.
   - `rewrite`: the statement has a problem that the material lets you fix. Write `revised_statement`.
   - `extraction_problem`: the problem is in the material, not the statement (a number or span looks wrong, or the screenshot shows something different from the Numbers list). Leave `revised_statement` empty and say in `note` what a person should check.

## Rules for a revised statement
At most 247 characters (count them), in this pattern: [named model or models] [prompting, only if the paper states it] [verb] [N + field + "research reports"] [task or instrument], [result against a comparator] ([metric = value, ...]). Name every model ("GPT 3.5-turbo", not "ChatGPT"); call custom systems "bespoke"; give N, the field and the data source; always give a comparator (humans, other models, a baseline); put statistics in parentheses with spelled-out metric names ("Cohen's kappa", "F1 score"); prefer kappa and F1 to accuracy. Every number must be found in the span, the Numbers list or the screenshot. Never add a number, model, comparator or direction that the material does not contain. Plain sentences, active voice, no arrows or slashes, no em dashes (use commas, periods, colons or parentheses). Keep the meaning of the original wherever it was correct.

## Output (JSON only)
{"id": "E-F1", "numbers": [{"number": "0.89", "found_in": "span | numbers_list | screenshot | nowhere", "where": "short note"}], "fidelity_problems": ["short phrase"], "verdict": "ok | rewrite | extraction_problem", "revised_statement": "", "note": "one sentence for the person who reviews it"}

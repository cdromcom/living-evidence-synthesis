---
type: prompt
id: evd-rework-v2
used_by: pipeline/scripts/lives_stages.py (draft, rework of EVD statements whose decision-model score is below 0.60; Claude Opus 5.5, a different model from the three drafting authors)
written: 2026-11-26
changes: v2 applies JP's EVD style and the one-set-of-parentheses rule to a revised statement.
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
Write it the way JP writes EVDs: at most 247 characters, one sentence, in this order: [named models, exact names such as "Claude 3 Opus" and "GPT 3.5"; "bespoke" for a custom system] [prompting, only if the paper states it] [past-tense verb] [N + field + "research reports" or the paper's own object] [task or tool], [result against a comparator] ([the numbers]). **Use at most one set of parentheses**, holding all statistics at the end; no other parentheses and no brackets. Always give a comparator. Spell out metric names; ranges with a hyphen; multiples as 100X; no Greek letters or symbols (kappa, not κ). Every number must be found in the span, the Numbers list or the screenshot. Never add a number, model, comparator or direction that the material does not contain. Plain sentences, active voice, no arrows or slashes, no em dashes. Keep the meaning of the original wherever it was correct.

## Output (JSON only)
{"id": "E-F1", "numbers": [{"number": "0.89", "found_in": "span | numbers_list | screenshot | nowhere", "where": "short note"}], "fidelity_problems": ["short phrase"], "verdict": "ok | rewrite | extraction_problem", "revised_statement": "", "note": "one sentence for the person who reviews it"}

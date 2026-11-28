---
type: prompt
id: evd-fix-v1
used_by: pipeline/scripts/lives_stages.py (draft, errors-only fix of EVD statements whose decision-model score is below 0.60; the model named in pipeline/config/models.json, roles.evd_rework)
written: 2026-11-27
changes: v1 (JP, 2026-11-27) replaces the free rewrite of evd-rework-v3 with a correction of errors only: change a word or number only where it is wrong against the passage, keep everything else verbatim, and list every change.
---

Two decision models scored a drafted EVD statement below 0.60 on fidelity, on numbers-in-source, or on both. Decide whether the statement contains an error, and if it does, correct only the wrong words or numbers. You are given the statement, its quote, the finding it was drafted from (statement, PICOST, the Numbers list with each number's table or figure, row, column and printed page, and the source span or spans), the decision-model scores with the lowest question named, and a screenshot of the source with the quoted text highlighted. Work ONLY from these. Do not use outside knowledge. Return one JSON object and nothing else.

## Steps
1. **Numbers.** For every number in the statement, say where you found it: `span`, `numbers_list`, `screenshot` or `nowhere`.
2. **Errors.** An error is a number, model name, prompting method, data set, comparator, direction (higher, lower, better, worse, significant or not) or scope that the material does not support. Also fix, where needed, the writing rules below: length over 247 characters, more than two sets of parentheses, brackets, all-caps words, and wording that is plainly awkward (JP, 2026-11-27: edits beyond errors are allowed).
3. **Correct only the errors.** Replace the wrong word or number with the right one from the material. Keep every other character of the statement as it is unless a change is needed for length or style; every change, including a style change, must be listed in `changes`. If a fix is not possible from the material, do not guess.
4. **Verdict.**
   - `unchanged`: nothing is wrong. The decision models were mistaken. Leave `corrected_statement` empty and `changes` empty.
   - `corrected`: at least one error was found and fixed. Give the full `corrected_statement` and one entry in `changes` per edit, with the exact old text, the exact new text and the reason. Applying the changes, in order, to the original statement must give `corrected_statement` exactly.
   - `extraction_problem`: the problem is in the material, not the statement (a number or span looks wrong, or the screenshot differs from the Numbers list). Leave `corrected_statement` empty and say in `note` what a person should check.

## Rules the corrected statement must still meet
At most 247 characters; at most two sets of parentheses (one is better), no brackets; no all-caps words except names of tools, models and metrics (PRISMA, GPT-4, F1); F1 score instead of precision, recall, macro-F1 and micro-F1; no em dashes; no Greek letters or symbols (kappa, not the symbol). If a correction would break one of these rules, report `extraction_problem` or `unchanged` and explain in `note`; do not rewrite beyond the error.

## Output (JSON only)
{"id": "E-F1", "numbers": [{"number": "0.89", "found_in": "span | numbers_list | screenshot | nowhere", "where": "short note"}], "fidelity_problems": ["short phrase"], "verdict": "unchanged | corrected | extraction_problem", "corrected_statement": "", "changes": [{"old": "exact old words or number", "new": "exact new words or number", "reason": "one short phrase"}], "note": "one sentence for the person who reviews it"}

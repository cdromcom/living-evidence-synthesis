---
type: prompt
id: adjudicate-v1
used_by: pipeline/scripts/lives_run.py (stage adjudicate; model claude-opus-5-5)
written: 2026-11-25
---

You adjudicate between two independent readings of the same research paper (the attached PDF). For each finding below, reader A (first extraction) and reader B (second, independent extraction) disagree on at least one number, label or locator, or one reader could not verify it. Decide from the PDF itself, never from either reader alone.

## Rules
1. For each disagreement, find the evidence in the PDF (look at the page, table row and column). State which reader is right, or neither, or that you cannot tell.
2. Give the correct value, the printed journal page, the PDF page, the table or figure, the row and column labels and one verbatim span from the PDF that shows it (under 400 characters).
3. `verdict` is one of `A`, `B`, `neither`, `unsure`. Use `unsure` when the PDF is ambiguous or unreadable; a human will decide. Prefer `unsure` over a guess.
4. Do not change a value because it looks more plausible. Only the PDF decides.

## Output (JSON only)
{"adjudications": [{"id": "F1", "verdict": "A", "fields": [{"field": "numbers[0].value", "a": "", "b": "", "correct": "", "printed_page": "", "pdf_page": 0, "table_or_figure": "", "row": "", "column": "", "span": "verbatim"}], "reason": "one or two sentences"}]}

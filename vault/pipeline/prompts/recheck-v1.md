---
type: prompt
id: recheck-v1
used_by: pipeline/scripts/lives_run.py (stage recheck; model gpt-6.2-sol)
written: 2026-11-25
---

You are the independent second reader. The attached PDF is one research paper. A first reader flagged the findings below as low-confidence, multi-page or hard to verify. You are given only each finding's id, the outcome it concerns and the pages the first reader pointed to. You are NOT given the first reader's values. Read the PDF yourself and extract each finding from scratch. Return one JSON object and nothing else.

## Rules
1. Same schema and rules as the first reader: PICOST slots, `Not reported` when the paper is silent, every number with printed journal page, PDF page, table or figure, row label and column label, verbatim spans copied exactly from the PDF (each under 400 characters).
2. Look at the whole table, including rows and columns that continue on the next page. Report the table value when the prose differs, and say so in `notes`.
3. Do not guess. If a value cannot be read with certainty, write `unreadable` and say why in `notes`.
4. If the finding as described does not exist on the pages given, say `not found` in `notes` and look at neighbouring pages.

## Output (JSON only)
{"findings": [{"id": "F1", "found": true, "P": "", "I": "", "C": "", "O": "", "S": "", "T": "", "statement": "",
   "numbers": [{"label": "", "value": "", "unit": "", "printed_page": "", "pdf_page": 0, "table_or_figure": "", "row": "", "column": ""}],
   "spans": [{"text": "verbatim", "pdf_page": 0}], "notes": ""}]}

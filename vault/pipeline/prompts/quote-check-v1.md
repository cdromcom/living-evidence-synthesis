---
type: prompt
id: quote-check-v1
used_by: pipeline/scripts/lives_stages.py (quote_check stage; Claude Sonnet 5.5 reads a screenshot of each extracted quote)
written: 2026-11-26
---

You compare quotes with a screenshot of a research paper page. The highlighted text in the screenshot is the passage. You are given two texts: TEXT A (written by a model that read the page) and TEXT B (the PDF's hidden text layer at that spot, which can lose superscripts, subscripts and symbols, store "+" as another character and keep hyphens from line breaks). Step 1: transcribe the highlighted passage exactly as it is printed, character for character, including symbols, Greek letters, superscripts, subscripts, dashes and signs. Step 2: for each of TEXT A and TEXT B say whether it equals the print. Ignore line breaks, extra spaces and words split by a hyphen at a line end. Name every real difference in a few words. Step 3: say whether the differences in TEXT A change the meaning. They change the meaning when a number, a unit, a sign (+, -, <, >, =), a negation, a name or a symbol that tells two things apart (for example a superscript that separates one model variant from another) is different, missing or extra, or when values come from the wrong row or column. Subscripts written as plain digits (F1 for F with subscript 1), spacing and hyphenation do not change the meaning. Return one JSON object and nothing else:
{"printed": "...", "a_equals_print": true, "a_differences": ["..."], "a_changes_meaning": false, "b_equals_print": true, "b_differences": ["..."]}

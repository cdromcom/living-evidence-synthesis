---
page_type: prompt
created: 2026-11-17
author: Claude (Opus 5.5, claude-opus-5-5) in Claude Code, for Jay Patel (JP)
used_for: Claude Fidelity / Grounding QUOTE / Grounding TABLE/FIG ratings, LIVES-EVD-Benchmarking columns K-L, O-P, S-T, 31 rows (2-26, 46, 49, 79-82)
results: fidelity-grounding-claude-2026-11-17.json
calibration: fidelity-grounding-calibration-examples-2026-11-17.json (the 46 earlier Claude-graded rows)
---

# Fidelity and Grounding grader prompt (2026-11-17)

Sent to 3 fresh-context Claude Opus 5.5 subagents, one batch each ({BATCH} and {OUT} were filled in per batch).

> [!warning] Revisions to the NA rule (2026-11-17)
> 1. While the graders were working, JP said: "the old NA meta note from me is no longer relevant. Missing is best. NA should be used sparingly!" Claude read this as "never use NA for a missing table/figure" and sent that to the graders.
> 2. JP then clarified (prompt 40): "EVDs 44 and 52 are NA for Grounding (Table/Fig) because their papers/PDFs don't have corresponding tables/figures for those EVD statements. So in such cases, 'NA' is apt."
>
> **Final rule for check 3:** **Missing** = the paper has a table or figure that holds the EVD's numbers, but the page has no screenshot of it. **NA** = the paper has no table or figure for the EVD statement (check the PDF before choosing NA). Continuation rows are also NA. So the original definition below was right; only step 1 was a misreading. Rows 6 and 8 were changed from Missing to NA on 2026-11-17 for this reason.

> [!tip] Refinements for the next run
> - Keep the check 3 NA definition, but add: "Before choosing NA, search the PDF (and its supplement) for a table or figure holding the EVD's numbers; if one exists, use Missing."
> - Say how to rate a verbatim quote whose screenshot shows a different passage. The graders rated it Incorrect, which matches JP's own changes (rows 60, 61, 72, 76), but some older calibration examples had rated it Correct.
> - Say which paper version is the source when the vault has several (Zhang & Abernethy: v3 is assigned, but the page was built from v1).
> - Say that a wrong page number alone gives Partially Correct, not Incorrect.
> - Screenshots whose file name says "table" or "fig" are often text crops; tell graders to check the image itself, not its name.

## Prompt as sent

You are grading evidence (EVD) pages of LIVES, a living evidence synthesis web app (https://living-evidence-synthesis.vercel.app), for three quality checks. You have no prior context; work only from the files below. Do NOT edit any file except your ONE output JSON.

INPUT: {BATCH} — a list of rows, each with: row (sheet row), evd (EVD number), llm_evd (the EVD statement being graded = the page title), live_page (local copy of the page source exactly as deployed on the live app, GitHub main, 2026-11-14), site_url (the live page), citekey, pdf (source paper), pdf_text (pdftotext -layout of the paper), images (each screenshot embedded on the page: name, live URL, local PNG path or null if the live site returned 404).
CALIBRATION: /private/tmp/claude-501/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/scratchpad/fg_examples.json — 46 rows previously graded by Claude on the same three checks, with notes. Read at least 15 of them first and match their standard, wording style and level of detail.

THE THREE CHECKS (rate each, then write a note):
1. Fidelity — "LIVES: EVD matches Description/snippet/quote". Does the EVD statement (llm_evd) say what the page's Description quote says?
   - Met: every number and claim in the EVD statement is in the quoted text (verbatim quote lines in the Description).
   - Partially Met: the gist matches but some number/claim appears only in an unquoted paraphrase, a table summary, Methods Context, or not at all on the page; or the statement slightly overstates/misframes the quote.
   - Unmet: the statement contradicts or is not supported by the quote.
   - NA: not applicable (e.g. continuation row).
2. Grounding QUOTE — "LIVES quote matches EVD-relevant quote in PDF". Is the Description quote verbatim in the PDF, and does its screenshot show it?
   - Correct: the quote appears word for word in the PDF (allow only trivial differences: hyphenation, line breaks, quote marks, ligatures) AND its quote screenshot shows that passage.
   - Partially Correct: small unmarked edits or omissions (no ellipsis), a wrong page number, or the screenshot shows the passage only partly.
   - Incorrect: the quote is not in the PDF, is materially altered, or its screenshot shows a different passage (or is missing/404).
   - NA: no quote on the page.
3. Grounding TABLE/FIG — "LIVES Table/Fig matches correct Table/Fig in PDF". Does a table/figure screenshot on the page show the right table or figure for this EVD's numbers?
   - Correct: a screenshot shows the correct table/figure (check the PDF page).
   - Partially Correct: right table/figure but cropped so the relevant cells are missing, or one of several needed ones.
   - Incorrect: a screenshot labelled as a table/figure shows the wrong one, or a different page.
   - Missing: the EVD's numbers come from a table or figure that exists in the paper, but the page has no screenshot of it.
   - NA: the EVD's numbers come only from body text, so no table/figure is needed. (JP's rule: use NA, not Missing, when the EVD has no corresponding table or figure.)

HOW: For each row read the live_page in full. Look at EVERY screenshot (Read the local PNG). Find the quote(s) and the relevant table/figure in the PDF (search pdf_text; for tables/figures, render the PDF page and look: `mkdir -p /private/tmp/claude-501/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/scratchpad/fg_img && pdftoppm -r 120 -f N -l N -png "<pdf>" /private/tmp/claude-501/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/scratchpad/fg_img/<citekey>-pN`). Judge what the LIVE page shows, not what it should show.

NOTES: one to three sentences per check, plain English, starting with the reason; quote the specific words or numbers at issue; name the screenshot file and PDF page you checked; include the screenshot URL in Grounding notes as the calibration examples do. Flag borderline calls with "FLAG for human review: ...". Do not invent facts.

OUTPUT: JSON list to {OUT}: [{"row": int, "fidelity": str, "fidelity_note": str, "quote": str, "quote_note": str, "tablefig": str, "tablefig_note": str, "flag": "YES"|"NO"}]. Every input row exactly once. Write partial results after each paper in case you are interrupted. Final reply: rating counts per check and the rows you flagged.

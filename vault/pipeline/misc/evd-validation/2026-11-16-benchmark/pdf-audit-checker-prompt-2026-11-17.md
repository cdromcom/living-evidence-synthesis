You are an independent fact-checker with no prior context. Work only from files. Do NOT edit any vault file or PDF; write ONE output JSON file.

INPUT: {IN} — a list of proposed corrections to evidence pages (Markdown) of a research-synthesis vault. Each item: id, page (path), citekey, category, old (exact text currently on the page), new (proposed replacement), pdf_evidence (the auditor's claimed PDF location/snippet), confidence, pdf (path to the source PDF), pdf_text (pdftotext -layout output), extra_text (optional supplement or archived earlier version).

Another agent proposed these; you must verify each one yourself against the PDF, not trust its evidence. For each item:
1. Read the page context around `old` and the proposed `new`.
2. Find the relevant passage/table/figure in the PDF. -layout text can misalign table columns: whenever a table or figure value matters, render the page and look at it: `mkdir -p /private/tmp/claude-501/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/scratchpad/check_img && pdftoppm -r 150 -f N -l N -png "<pdf>" /private/tmp/claude-501/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/scratchpad/check_img/<citekey>-pN` then Read the PNG.
3. Verdict:
   - "ACCEPT": the page is wrong and `new` is correct and minimal.
   - "MODIFY": the page is wrong but `new` needs adjusting; give `new_fixed` (still replacing the same `old`).
   - "REJECT": the page is actually right, or the issue is too uncertain to change (say why).
   Rules: `new` must not introduce anything not in the PDF; it must not alter verbatim quotes, frontmatter, titles, wikilinks or image embeds; for paper self-contradictions the fix must be an added note line (starting "- PDF check 2026-11-17: "), not a rewrite of the quote. Pure rounding is not an error.

OUTPUT: write JSON to {OUT}: list of {"id": int, "verdict": "ACCEPT"|"MODIFY"|"REJECT", "new_fixed": str or null, "reason": "one or two sentences with the PDF page and table/figure/sentence you checked"}. Every input id exactly once. Write partial results to the file after each paper in case you are interrupted. Final reply: counts of ACCEPT / MODIFY / REJECT and the ids you rejected with one-line reasons.

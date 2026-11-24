---
page_type: log/audit
created: 2026-11-17
updated: 2026-11-17
author: Claude (Opus 5.5, claude-opus-5-5) in Claude Code with Jay Patel (JP)
vault: living-synthesis
human_verified: no
---

# PDF number audit of the 77 EVD pages (2026-11-17)

Every number in the EVD pages' notes and tables is being checked against the source PDFs in `source/pdfs/`, because three pages checked on 2026-11-17 (EVD 8, 22, 45) had transcription errors. This file records why the errors happened, how to avoid them in future runs (with any model), what was done and what was found.

Prompts and actions are also logged in the Google Sheet "LIVES - AAA Benchmarking (HAI)", tab AI Prompt Log (prompts 28-29 onward), and in [[2026-11-11-evd-validation-gsheet-prompt-log]].

> [!warning] Cause 1: quotes were verified, numbers were not
> In Phase 22 (2026-04-28, see `History.md`) 26 Claude subagents rewrote all 77 EVD pages in parallel, one per paper. The pipeline automatically checked every **verbatim quote** against the PDF text (after normalising characters), so the Description quotes are reliable. The **results tables and numbers in "Other Notes"** (the TRIPOD-LLM item-17 mini-tables) were retyped by the models and **never checked** against anything.

> [!warning] Cause 2: dense PDF tables are hard to read as text
> Text extracted from two-column PDFs interleaves the columns, and wide tables lose their alignment. A model retyping a table from that text drifts. The errors found on 2026-11-17 follow this pattern, not random typos:
> - **Row shift:** EVD 22 "Always Reject" ICLR 22 F1 showed 0.38, which is the "Random Decision" value from the row above.
> - **Column shift:** EVD 22 "AI-Review" ICLR 22 / ICLR 23 values slid one column.
> - **Swapped +/- values** between neighbouring cells (EVD 22, four cells).
> - **Wrong attribution:** EVD 45 credited the 96% PRISMA result to Claude-3-Opus; the paper's Table 3 and text give it to Claude-2.
> - **Missing comparators:** EVD 45 omitted the combined-LLM kappas; EVD 8 omitted the GPT-4 / GPT-3.5 rows that change who is "best".

> [!warning] Cause 3: the papers' own errors get copied
> Some sources contradict themselves. Bougie & Watanabe (2024) call 0.66 GAR's "average" F1, but their Table 3 shows 0.66 is the ICLR 2022 score (mean about 0.62). Woelfle et al. (2024) name Claude-3-Opus as the top AMSTAR pair (95%) in the text, while their Table 3 lists GPT-3.5 at 96%. A faithful quote can still carry a wrong number.

> [!warning] Cause 4: downstream copies inherit the errors
> The EVD pages feed the GSheet (LLM-generated EVD titles, Claude drafts, PICOST cells) and the live LIVES site (GitHub `cdromcom/living-evidence-synthesis`, built from its own copy of the vault). Fixing one copy does not fix the others. On 2026-11-17 the live site still showed the old EVD 45 numbers.

> [!tip] How to avoid this next time (for Claude and other models)
> 1. **Treat every number as unverified until it is matched to a specific PDF table, figure or sentence**, and record where it came from (page + table/figure).
> 2. **Check numbers with the same rigour as quotes.** Add an automated pass that finds each number in a page and confirms it appears in the PDF text; flag misses for a human.
> 3. **For tables, look at the table image, not only extracted text.** Render the page (`pdftoppm -r 200 -f N -l N -png`) and read it, or cross-check a text extraction against the image. Watch for row and column shifts.
> 4. **Always include the comparators that decide a claim** ("best", "beat", "matched"): check the whole table, not only the row being reported.
> 5. **When a paper's text and its table disagree, cite the table and note the conflict** on the EVD page.
> 6. **Use a second, fresh-context checker** that sees only the draft and the PDF, never the drafter's reasoning.
> 7. **After fixing a page, fix every downstream copy** (GSheet cells, PICOST, the GitHub vault that builds the site), or log that it is still pending.
> 8. **Keep the PDFs in the vault for every paper** (`source/pdfs/`), including supplements and the exact version the pages were built from.

## Method (this audit)

- Inputs: 77 EVD pages in `evidence/`, the 27 matching PDFs in `source/pdfs/` (plus the Wrightson supplement and the archived 2025 version of Zhang & Abernethy, whose pages were built from an earlier version).
- Text extracted with `pdftotext -layout`; table pages rendered as images where the text was ambiguous.
- Step A: auditor agents (fresh context, one batch of papers each) list every number outside verbatim quotes, find it in the PDF, and propose exact corrections with the PDF location. They do not edit files.
- Step B: a separate checker agent verifies every proposed correction against the PDF.
- Step C: Claude applies only verified corrections, backs up each page first, and records every change below.
- Scope: the local Obsidian vault only. The GitHub copy behind the live site is not changed until JP approves.

## Results (as of 2026-11-17, nothing applied yet)

- 5 auditor agents checked all 77 pages (roughly 2,700 numbers by their own estimates) and proposed **147 corrections** on 57 of the 77 pages: 49 wrong number, 33 not in the paper, 19 paper self-contradictions (note added, quote untouched), 18 wrong page references, 17 credited to the wrong model/rater/condition, 8 missing comparators, 3 row or column shifts.
- 3 fresh checker agents re-verified each one against the PDFs (rendering table and figure pages as images): 142 accepted, 5 accepted with adjusted wording, 0 rejected. Because nothing was rejected, the 70 changes that rest on figure readings, footnote inference or medium confidence are marked for JP to check first.
- Zhang & Abernethy: the 3 pages were built from arXiv v1; at JP's request 38 updates to v3 were drafted (tables and notes only; titles, quotes, screenshots unchanged). Audit change 137 is superseded by v3 change z6.
- Review file with every change, its PDF location and verdict: [[2026-11-17-pdf-audit-proposed-changes]].
- Skill.md (Step 6b numeric audit, Step 3a, Step 8) and Skill-references.md (pitfalls) were updated on 2026-11-17 at JP's request; originals in `misc/evd-validation/2026-11-16-benchmark/skill-backups-2026-11-17/`.

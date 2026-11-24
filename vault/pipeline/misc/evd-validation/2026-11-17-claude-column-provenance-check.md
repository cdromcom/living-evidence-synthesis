---
page_type: log/audit
created: 2026-11-17
author: Claude (Opus 5.5, claude-opus-5-5) in Claude Code, for Jay Patel (JP)
human_verified: no
---

# Are Claude's columns only Claude's? (provenance check, 2026-11-17 20:30 EST)

Scope: LIVES-EVD-Benchmarking, rows 2-82, Claude columns G-H (relevancy), K-L (Fidelity), O-P (Grounding quote), S-T (Grounding table/fig) and X (drafts): 729 cells. Per-cell results: `2026-11-16-benchmark/claude-column-provenance-2026-11-17.json`; scripts `prov_writes.py`, `prov_final.py` in the same folder.

## Method
1. Replayed every write this session made to the tab (545 cell writes, 9 cut/paste moves, 3 column inserts), mapping column letters across the 2026-11-17 six-column insert, and labelled each write batch by what it was (fresh Claude judgment, restore, marker).
2. For cells this session never wrote: compared with the 2026-11-11 18:31 EST snapshot, and the snapshot's Claude rows with the original sheet "LIVES - AAA Benchmarking Results", matched by EVD statement text (the original's rows are in a different order).
3. Column X: compared with the drafts Claude wrote on 2026-11-11 to 11-13 (session 321443ce) and 2026-11-16/17 (this session).
4. Scanned Claude cells for JP markers ("[JP", "JP:", "qQ") and for text identical to any JP note.
5. Pairing: for every row, rating present if and only if note present.

## Results
- Every Claude cell still holds exactly the value of its last known Claude source. No cell was changed by anyone after Claude wrote or restored it.
- No JP markers, and no JP note text, in any Claude cell (apart from the shared continuation-row marker "NA: continuation row, graded on the EVD 45 row").
- Pairing: no gaps. Every rating in G, K, O and S has a note in H, L, P or T, and vice versa; no Claude cell in rows 2-82 is empty.
- Restored cells (R1, R3) all equal the 2026-11-11 snapshot.

> [!warning] Exceptions
> 1. **G79:G82 (EVD 74-77) are probably JP's ratings, not Claude's.** They were restored on 2026-11-17 only because JP said rows 79-82 were Claude-generated. Against that: the rows are "Graded by: Jay"; their original notes appear word for word in JP's original sheet; and JP later moved those notes to J himself. Claude's own notes in H79:H82 (2026-11-17) agree with the G ratings, but Claude wrote them after seeing G, so the check was not blind.
> 2. **G47:H48** (EVD 45 continuation rows, "Graded by: Jay") hold "NA" / "NA: continuation row..." from before 2026-11-11 18:31. They are placeholders, not judgments, and their author is not recorded.
> 3. **The 2026-11-11 Claude rows can be traced only as far as the sheet.** Their ratings, and their G, H, K, L, O and S text, match the original sheet exactly, and the T notes (47 cells) and three P notes were added to this copy before 2026-11-11 18:31. None of this text appears in any Claude Code transcript on this machine before the 11-11 session read it from the sheet. So the claim that these rows are Claude's rests on the sheet's "Graded by: Claude" label and the Claude-style text, not on a recorded Claude run (ABOUT already says the model and session were not recorded).

## Follow-up (2026-11-17 20:34 EST)
JP asked for a blind re-judgment of EVD 74-77. A fresh Claude Opus 5.5 agent saw only the four vault pages and the criterion (no EVD-number examples) and rated them Irrelevant, Relevant, Relevant, Relevant, the same as the old G values. G79:H82 now hold these blind judgments, so exception 1 is resolved. Exceptions 2 (G47:H48 placeholders) and 3 (the 2026-11-11 rows trace back only to the sheet) remain.

## EVD 45 rows 46-48 (2026-11-17 20:39 EST, JP: "E46 was probably Claude and for sure W46-48 were JP manually revised")
- **E46** (LLM-generated EVD) matches the original sheet's EVD 45 row and the page title recorded in the vault build log `History.md` (line 1195, "EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters"). So it is the title Claude Code generated when it built the vault in April 2026. The page has since been renamed locally and on GitHub ("...reached up to 96% on PRISMA surpassing human raters"). Consistent with JP's statement.
- **W46:W48** (JP Phase 1 edits: the PRISMA, AMSTAR and PRECIS-2 split) were never written by any recorded Claude Code session (the 2026-11-11 session or this one). Consistent with JP's manual revision.
- **G47:H48 and E47:E48** ("EVD 45 continued: Jay split this EVD into 3", "NA: continuation row ...") are placeholders that exist because of JP's split. They predate the 2026-11-11 snapshot, and their author is still unrecorded.

- 2026-11-17 20:54 EST: JP decided G47:H48 stay as they are; exception 2 is accepted, not fixed.

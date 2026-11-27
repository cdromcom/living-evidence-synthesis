# Table cell extraction: PyMuPDF find_tables vs Marker vs MinerU

Run date 2026-11-26, Apple Silicon Mac, Python 3.11 venv at ~/.cache/lives-bench/venv-tables.

## Short answer

Neither Marker nor MinerU is clearly worth adding for table cells on born-digital PDFs. On the 463 verified table numbers from the four pilot papers, PyMuPDF find_tables found 91.6 percent and Marker found the same 424 values; MinerU found 93.1 percent (431). After the symbol repair described below (applied to PyMuPDF and Marker output), PyMuPDF and Marker reach 92.9 percent (430) and MinerU stays at 93.1 percent, so the gap is 1 value. MinerU is about 6 times slower per page.

Two situations change the picture. (1) Sideways pages: PyMuPDF found none of the verified values on copies of the pages rotated by 90 or 270 degrees, Marker gave exactly the unrotated result, and MinerU kept 82 percent (90 degrees) and 86 percent (270 degrees). (2) Word supplements: PyMuPDF found no tables in the Woelfle mmc5.docx and Marker could not convert any docx here, while MinerU read all 3 tables and all 10 hand-corrected supplement values. A plain python-docx reader gave the same result as MinerU for docx files.

## What was installed

| Item | Version | Download size |
|---|---|---|
| marker-pdf | 2.2.0 (with surya-ocr 0.23.0, torch 2.15.0, transformers 5.24.1) | about 123 MB of model files (109 MB Hugging Face cache plus 14 MB Marker cache) |
| mineru | 4.2.3 (docvortex 0.6.26) | 857 MB for `mineru-kit models download --tier basic` (MinerU-4_models_torch) |
| pymupdf | 2.2 (find_tables baseline) | n/a |
| MinerU standard-tier model | MinerU2.5-Pro-2605-1.2B-GGUF | 1.2 GB, downloaded automatically by my first test call (default tier is standard). Not used in the measured run. |

Venv size 1.7 GB. All caches were redirected into ~/.cache/lives-bench/mc (env.sh sets HF_HOME, XDG_CACHE_HOME, MINERU_HOME, MINERU_TELEMETRY_DISABLED=1).

Notes on the install:
- Marker and MinerU resolved together only after installing Marker first and MinerU second. `uv pip check` then reports two version mismatches (surya-ocr wants pillow below 11 but 13.0.0 is installed; pdftext wants pypdfium2 5.10.1 but 5.15.2 is installed). Marker ran without errors anyway.
- MinerU 4.x no longer has the old `mineru -b pipeline` command. The closest match is `mineru-kit parse --tier basic` (pipeline models, no VLM), called here through its Python function `mineru.parser.parse(..., tier='basic', page_range=...)` one page at a time. The Python call needs an `if __name__ == '__main__'` guard because it starts worker processes.
- Marker was run through its Python API with `output_format=json` and one page per call. The LLM mode was never switched on (no use_llm, no API keys). No PDF left the machine: MinerU ran locally (no --remote), and the only network traffic was model downloads from Hugging Face.

## Data

27 seed papers, PDFs resolved with pdf_pages.resolve_pdf. A page was parsed if its text has a line starting with "Table" and a number, capped at 10 pages per paper: 124 pages in all (pages.json). Nothing was shortened for time. The seed set contains the main papers only, so supplementary files were not tested.

## Evaluation A: known cells (4 pilot papers, 463 verified numbers whose location names a Table)

Ground truth: findings[].numbers[] in the batch05 and batch07 picost.json files (Sarol 96, Bougie 205, Tyser 44, Woelfle 118). A value counts as found if its normalized form (commas, leading zeros, plus-minus signs, percent signs removed) equals a number in a numeric cell of any table the parser returned for that PDF page. "Correct row" counts when the cell sits in a row whose non-numeric cells plus the first-column cells above it contain at least 60 percent of the words of the row label in the ground truth (456 entries have a row label). Only the first number in a value string is checked.

| Parser | Value found | Value found in correct row | Strict subset: value (445) | Strict subset: row (445) |
|---|---|---|---|---|
| PyMuPDF find_tables, no repair | 424/463 = 91.6% | 419/456 = 91.9% | 423 = 95.1% | 419 = 94.2% |
| PyMuPDF find_tables, with repair_cell_text (first version) | 430/463 = 92.9% | 425/456 = 93.2% | not recomputed | not recomputed |
| PyMuPDF find_tables, with extended repair_cell_text | 431/463 = 93.1% | 426/456 = 93.4% | not recomputed | not recomputed |
| Marker, no repair | 424/463 = 91.6% | 419/456 = 91.9% | 423 = 95.1% | 419 = 94.2% |
| Marker, with repair_cell_text (first version) | 430/463 = 92.9% | 425/456 = 93.2% | not recomputed | not recomputed |
| Marker, with extended repair_cell_text | 431/463 = 93.1% | 426/456 = 93.4% | not recomputed | not recomputed |
| MinerU (basic), no repair | 431/463 = 93.1% | 425/456 = 93.2% | 430 = 96.6% | 425 = 95.5% |

The strict subset drops 18 entries whose location is a caption, footnote or header rather than a table cell.

Per paper (values found out of total; same for rows within 1): Sarol 90/96 for all three; Bougie 199/205 for all three; Tyser 38/44 for all three; Woelfle 97/118 for PyMuPDF and Marker, 104/118 for MinerU.

What the 32 values missed by all three are (read from eval_A.json): row-label numbers that are part of a text cell, not a cell value (Sarol page 6, "Top 5 sentences" gives value 5, "Top 20 sentences" gives 20); numbers that appear in a caption (Bougie pages 12 and 17, value "1,000" in the Table 3, 4 and 9 captions); and a few Woelfle cells (Table 1 cost cells such as 0.012 and 1.15, and the "9/9" and "8/9" cells of Table 3) that I did not look into further.

Why MinerU found 7 more: in the Woelfle PDF the text layer stores the en dash inside confidence intervals as the letter e (PyMuPDF and Marker return "0.37e0.44"; MinerU reads the page image with OCR and returns "0.37-0.44"), and some minus signs as the control character U+0004. My number reader then misses the second number of each interval. The repair rules in tablelib.repair_cell_text (section "Symbol repairs") recover 6 of the 7, leaving 1 value that only MinerU finds.

## Evaluation B: all 27 papers, 124 table pages, no ground truth

| Measure | PyMuPDF | Marker | MinerU |
|---|---|---|---|
| Tables found | 146 | 164 | 151 |
| Non-empty cells | 6029 | 9153 | 7925 |
| Numeric cells | 2750 | 4240 | 3626 |
| Pages with zero tables | 21 | 17 | 18 |
| Mean share of text-layer numbers (caption region) found in cells | 0.650 | 0.723 | 0.686 |
| Seconds per page, mean (median) | 0.28 (0.23) | 0.32 (0.26) | 1.78 (1.32) |
| Slowest page | not recorded | 1.17 s | 6.18 s |
| Errors or timeouts | 0 | 0 | 0 |
| Peak memory (whole process, includes models) | not measured | about 2.0 GB | about 2.0 GB |

Agreement (mean Jaccard of the sets of numbers in numeric cells, per page): PyMuPDF and Marker 0.785, PyMuPDF and MinerU 0.825, Marker and MinerU 0.793. Per-page values are in eval_B_pages.tsv.

Limits of this table. The cell counts are not comparable one to one, because the parsers cut cells differently (PyMuPDF often puts several fields in one cell, Marker and MinerU split them, so Marker and MinerU report more numeric cells). The text-layer coverage is a rough check: the region between a caption and the next prose paragraph is chosen by a block heuristic (below the caption, or above it if that holds more numbers), and it was scored only on the 73 pages where it contained at least 3 numbers. It gave 0.0 for all three parsers on some pages (for example Leucuta pages 4 to 6), which I did not investigate, so treat it as a rough signal. Seconds per page for MinerU is the time of one `parse` call per page with the models kept loaded in the process; the first-ever call also pays for download.

## Where each parser had trouble (examples I checked)

Pages where a parser returned no table although a caption is on the page:
- PyMuPDF: Akyon page 15 (Table 4 is a chart-like block), Hasan page 3 and page 4 (Table 3, 6 numbers in the region), Tyser page 33 (Table 10, a two-column text table with a header row of titles).
- Marker: Darcy page 18, Liang pages 3 and 8, Lou page 18, Shahid page 12, Sridharan (Assessing) page 3 returned no table; these are pages where all three parsers returned nothing, most likely because the "Table N" line is a mention in text, not a table.
- MinerU: Akyon page 15 (nothing; Marker returned an 9 x 11 grid of axis labels such as "Q15 Q14 Q13 Q12", which is not a table, so the grid is wrong even though a table object exists).

Other things that happened:
- Merged header cells: Marker and MinerU return a span as repeated text in every covered column in my grid (I expand colspan and rowspan). PyMuPDF find_tables has no span information; Woelfle page 3 shows PyMuPDF dropping the header row and leaving blank columns (a 5 x 7 grid with empty columns, no "Company" or "Context length" header) while MinerU gave a 6 x 4 grid with the header row. See review.html section 5.
- Tyser page 33 (Table 10): MinerU joined the header text into single cells ("Title Authors Review tions") and put the question text in the second cell; Marker returned a clean 5 x 2 grid with "Title" and "Authors" labels; PyMuPDF returned no table.
- Rotated tables and supplementary files: see the two sections below (the first version of this file had not tested them).
- Pages with a low number of table values (text tables such as Hasan page 4 and Huntington-Klein page 8): all three give grids with no numeric cells, so numeric comparison says nothing about them.

## Plain-language judgement

PyMuPDF find_tables already gets 92 percent of the verified numbers, and the values it misses are mostly not cell values at all (numbers inside labels and captions). Marker returns the same numbers for the pilot papers. MinerU recovered 7 more, all in one paper; 6 of them come from symbol encoding in the text layer, which repair_cell_text also fixes for PyMuPDF and Marker (92.9 percent); it costs of about 1.8 seconds a page and an 857 MB download. For the job of checking a number against a table, PyMuPDF with a text-layer fallback is enough. If we want a second opinion on the pages where PyMuPDF returns no table or merged cells (21 of the 124 pages here), MinerU basic is the option I would try first, and Marker is not needed for numbers.

Limits: the ground truth covers four pilot papers only; the 27-paper evaluation has no ground truth, so higher cell counts there are not proof of correctness; the row check is a word-overlap rule, not a human check; I did not read every returned grid.

## Rotated tables

(a) Scan of the vault pdf folder. The folder is ~/Documents/living-synthesis/sysrev/dgraph/source/pdfs (there is no ~/Documents/living-synthesis/pdfs folder); the scan walked it with all subfolders: 33 PDFs, 733 pages, 168 pages with a table caption (scan_rotated.py, rotated_scan.json). No caption page has page.rotation other than 0, and no caption page has most of its text in vertical lines. Nine caption pages are landscape pages with horizontal text: Leucuta et al. 2025 pages 4 to 8 and the Wrightson supplement PDF pages 3, 4, 6 and 7. So the vault holds landscape tables but no tables set sideways on an upright page. (Pages with a few vertical lines, such as Sridharan Leveraging pages 2 to 7 and Wrightson page 3, carry a vertical margin line, not a table.)

(b) Controlled test (rotation_build.py, run_rotation.sh, score_rotation.py, rotation_results.json). For the four pilot papers I took the same 24 table pages and built five copies: rot0 (copy, control), rot90 and rot270 (page.set_rotation, text layer kept), img0 (page rendered at 200 dpi, image-only PDF) and img90 (the same image set sideways, image-only). The same 463 verified values were scored (value found / row found, row out of 456).

| Parser | rot0 | rot90 | rot270 | img0 (no text layer) | img90 (no text layer) |
|---|---|---|---|---|---|
| PyMuPDF, no repair | 424 / 419 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| PyMuPDF, with extended repair | 431 / 426 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| Marker, no repair | 424 / 419 | 424 / 419 | 424 / 419 | 428 / 414 | 428 / 414 |
| Marker, with extended repair | 431 / 426 | 431 / 426 | 431 / 426 | 428 / 414 | 428 / 414 |
| MinerU (basic) | 431 / 425 | 380 / 375 | 397 / 389 | 350 / 338 | 268 / 251 |

What happened:
- PyMuPDF find_tables still returned tables on the rotated copies (17 at 90 degrees, 16 at 270 degrees) but none of the verified values were found in them; on the image-only copies it returned no tables at all, as expected without a text layer.
- Marker returned the same value and row counts for 0, 90 and 270 degrees (cells identical on the page I compared, Sarol page 5), and identical cells for the image-only copies at 0 and 90 degrees on all 24 pages. I did not look into the reason; the output suggests Marker turns the page upright before reading it. On image-only pages the OCR found 4 more values than the text layer (428) but placed fewer in the right row (414).
- MinerU lost values on rotation: 431 to 380 (90 degrees) and 397 (270 degrees), and more on image-only pages (350 upright, 268 sideways). Tables found fell from 27 to 23 at 90 degrees.
- Time per page in this run (other jobs were running at the same time, so slower than in Evaluation B): PyMuPDF 0.2 to 0.8 s, Marker 0.8 to 1.3 s, MinerU 4.7 to 10.8 s.
- Limits: the copies are synthetic, made from upright pages; real scanned landscape tables may differ. Only 24 pages.

## Supplementary files

Found under the vault pdf folder (supp_results.json, results_supp/, run_supp.py, score_supp.py): 1 supplementary PDF (Supp Mat - Wrightson et al 2025.pdf, 7 pages), 5 Word files from Woelfle et al. 2024 (mmc1 to mmc5), 4 Word files from Sridharan and Sivaramakrishnan 2024 (sj-docx-1 to 4), and a ScienceDirect zip whose 5 files have the same MD5 hashes as the Woelfle mmc files (not extracted into the vault, read in memory only). There are no xlsx or csv files. The 5 PDFs under Archive are older versions of main papers, not supplements, and were not parsed here.

Readers: PyMuPDF (it opens docx as a paged document), Marker, MinerU (docx with its flash tier, PDF with the basic tier), and python-docx as a plain reader for docx (no table detection, it reads the Word tables). Marker needs WeasyPrint to read docx; I installed marker-pdf[full] from PyPI (this also moved pillow back to 10.4.0 and pypdfium2 to 5.10.1, which removed the earlier version mismatch), but WeasyPrint needs system libraries (pango) that are not installed and may not be installed by pip, so Marker could not convert any docx. That is not a Marker table result; it was not run for docx.

| File | Pages | PyMuPDF tables / numeric cells | Marker | MinerU | python-docx |
|---|---|---|---|---|---|
| Wrightson supplement PDF | 7 | 5 / 86 (2.1 s) | 7 / 103 (3.8 s) | 5 / 90 (48.6 s for 7 pages) | n/a |
| Woelfle mmc1 to mmc4 (figures only, 6 to 15 images each) | 2 to 4 | 0 | not run | 0 | 0 |
| Woelfle mmc5 (Supplementary Tables 1 to 3) | 37 | 0 / 0 (4.3 s) | not run | 3 / 253 (1.8 s) | 3 / 253 (0.02 s) |
| Sridharan sj-docx-1 to 3 | 7 to 55 | 0 | not run | 0 | 0 |
| Sridharan sj-docx-4 | 160 | 0 (23.0 s) | not run | 1 / 0 numeric cells (3.4 s) | 1 / 0 |

No errors or timeouts other than the Marker docx conversion. For the Wrightson supplement PDF there is no ground truth; the three parsers agree closely (Jaccard of numeric cell sets: PyMuPDF and MinerU 1.00, PyMuPDF and Marker 0.91, Marker and MinerU 0.91, with repair applied to PyMuPDF and Marker). The 9 Word files in the pdf folder hold tables only in mmc5 and sj-docx-4; the other files are figures or running text.

Woelfle supplement ground truth: the 10 values in batch07 picost.json marked from_supplement (Supplementary Table 2: 90, 89, 73, 89, 0.81; Supplementary Table 3: 0/112, 10/112, 7/112, 5/56, 14/112). Scored for the value, the row and the column header together:
- python-docx reader: 10 of 10 value, 10 of 10 row, 10 of 10 row and column.
- MinerU flash: 10 of 10, 10 of 10, 10 of 10 (its 3 tables are cell for cell the same as the python-docx tables).
- PyMuPDF: 0 of 10 (no tables found in the docx).
- Marker: not run (docx conversion).
Limits: 10 values from one file; the table cells of a Word file have no text-layer encoding problems, so this says nothing about PDF supplements.

## Symbol repairs

tablelib.repair_cell_text repairs these text-layer problems (counts are cells in the 124-page run, symbol_report.py, symbol_report.json; the same function is used in evaluate.py with REPAIR=1, for PyMuPDF and Marker only):

| Problem | Example before | After | PyMuPDF cells | Marker cells | MinerU cells |
|---|---|---|---|---|---|
| en dash stored as the letter e between numbers (Woelfle) | 0.77 (0.72e0.81) | 0.77 (0.72-0.81) with an en dash | 148 | 148 | 0 (OCR reads the dash) |
| minus sign stored as control character U+0004 (Woelfle) | 0.01 (\x040.08 to 0.08) | 0.01 (minus 0.08 to 0.08) | 4 | 4 | 0 |
| times sign stored as U+0003 (Woelfle) | 27 items \x03 112 publications | 27 items x 112 publications | 6 | 27 | 0 |
| equals sign stored as the digit 5, only when 27 x 112 equals 3024 style arithmetic holds | ... 112 publications 5 up to 3024 | ... = up to 3024 | 6 | 27 | 0 |
| thorn used for plus | Titlethorn abstract | Title+abstract | 2 | 3 | 0 |
| private-use digits U+F130 to U+F139 (Huntington-Klein Table 1; the page shows 59.9 %) | the cell text is four private-use characters then ".", one more and " %" | 59.9 % | 16 | 0 | 16 (not repaired, MinerU is outside the requested scope) |
| soft hyphen in cell text | Efficacy of (soft hyphen) | removed | 27 | 0 | 0 |
| ligatures | none found | | 0 | 0 | 0 |
| quarter sign used for equals | none found in cells (pdf_pages.py already maps it for quote matching) | | 0 | 0 | 0 |

Cells changed by repair: PyMuPDF 203 of 8038, Marker 182 of 11090, MinerU 16 of 9737 (if applied).

Present and not repaired: plus-minus signs are stored correctly as the plus-minus character (251, 287 and 293 cells, no problem); footnote letters glued to numbers such as "0.90 (0.88e0.93)a" (127, 148 and 132 cells; the letter is left in place, and the number reader still finds the value); unicode superscripts such as "(40%, 37%-44%)²" (3 cells, MinerU only); two Marker cells with Khmer letters from OCR ("ដកុត្ត 2/3 313 36", one page); and the mixed use of the hyphen, minus sign U+2212 and en dash as minus or range sign (10 and 13 cells with U+2212). The en dash repair ignores cells that are a single scientific number such as 1e-5 and can in principle change a word like "e1" between digits; none was seen in these data.

Effect on results: Evaluation A with the first repair, PyMuPDF and Marker 430 of 463 (92.9 percent) values and 425 of 456 rows, up from 424 and 419; with the extended repair 431 (93.1 percent) and 426, the same value count as MinerU (431, 425 rows).

### Extended repair (second round)

repair_cell_text (and its new companion repair_cell_text_notes, which also returns the removed footnote markers) now also handles: footnote letters a to d (and U+00AA) glued to a number inside an otherwise numeric cell; Unicode superscript digits and signs after a number used as footnote markers; true powers of ten (a superscript exponent after a times sign or on a bare 10, and the flattened "10" plus minus plus digits of Darcy Tables 6 to 8, written 10^-3); a vertical bar standing for a tilde before a number (Woelfle Table 1); and Khmer-script OCR noise in Marker output, marked as [unreadable] without guessing. The footnote rule never touches units or words: "3d" (days), "2b", "ChatGPT4o", "5 cm2", "(95% CI)a", star and dagger signs stay as they are. The code lives in tablelib.py and is the source of the block that goes into pipeline/scripts/pdf_pages.py (see the note on that file below).

Counts on the 124 pages (symbol_report.py, repair_audit.py; PyMuPDF / Marker / MinerU with the repair applied to all three for the audit):

| Item | Before extension (cells) | After extension (cells) |
|---|---|---|
| Cells changed by repair | 203 / 182 / 16 | 232 / 216 / 72 |
| Footnote letters glued to numeric cells | 127 / 148 / 132 counted, none removed | removed in 62 / 62 / 53 cells (letters a 28, b 28, c 6); the rest (65 / 86 / 84 cells) are row labels such as "1a", "2b" and names such as "ChatGPT4o", left in place on purpose |
| Unicode superscript footnote markers | 0 / 0 / 3, none removed | 3 cells (MinerU) removed, marker recorded |
| Vertical bar for tilde (Woelfle Table 1) | 10 / 10 / 0 unrepaired | 10 / 10 / 0 repaired |
| Flattened power of ten (Darcy) | 10 / 13 / 7 unrepaired | 10 / 13 / 0 repaired (MinerU writes a hyphen, left alone) |
| Khmer-script cells (Marker) | 0 / 2 / 0 unrepaired | 2 marked as [unreadable] |
| Evaluation A values found, PyMuPDF and Marker | 430 (92.9%) | 431 (93.1%) |
| Evaluation A rows found | 425 | 426 |
| Evaluation B numeric cells, PyMuPDF / Marker | 2769 / 4243 | 2769 / 4244 |

Misfire check (repair_audit.py): every cell on the 124 pages was compared with and without the repair; 232, 216 and 72 cells changed. I read the first four examples of each rule and the list of cells whose number tokens changed. All changes are the intended ones: 148 intervals (Woelfle), 62 footnote letters (Woelfle), 10 tildes (Woelfle Table 1), 23 powers of ten (Darcy), 16 private-use digits (Huntington-Klein), 6 and 27 times and equals cells (Woelfle), 4 minus signs, 2 and 3 thorn cells, 27 soft hyphens, 2 Khmer cells. No rule fired on a cell that was not a symbol problem. What can differ from a reader's expectation: a power of ten is written 10^-3 and the number reader splits it into the tokens 10 and -3 (it does not evaluate it), and a cell such as "0.90 (0.88-0.93)a" loses the letter a from the cell text (the letter is returned in the notes by repair_cell_text_notes, but table_cells and evaluate.py use only the text).

Limits: the audit has only these papers; Khmer is the only script treated as unreadable; a bar before a digit inside a cell is assumed to be a tilde (checked only against Woelfle Table 1, where MinerU reads the same character as a tilde); decimal-only cells such as "37.5d" and "3d" are never stripped, so a real footnote letter on a bare decimal is kept only when the letter is a, b or c.

Unit tests: tablelib_tests.py (43 offline checks, python3 tablelib_tests.py; 0 mismatches). selftest additions are listed below.

### Missed values

See missed-values.md and missed-values.html: of the 33 values PyMuPDF (first repair) missed, 17 are caption or footnote text, 10 are part of row or header labels, 5 are present in a mixed text cell that my scorer rejects, and 1 was a symbol problem that the extended repair fixed. None was a table PyMuPDF did not detect.

### Note on pdf_pages.py

The permission system declined my attempt to edit pipeline/scripts/pdf_pages.py, so the vault copy still holds the first version of repair_cell_text. The new block is ready as vault_repair_block.py; python3 apply_vault_repair.py (default target: the vault copy, or pass a path) replaces the old function in place and is safe to run twice. I tested it on a copy in scratch/. tablelib_tests.py compares the two blocks once the vault file has them.

### selftest additions

Paste into pipeline/scripts/selftest.py after the existing pdf_pages checks (they use the same check(name, condition) helper and the imported module _pp):

```
r = _pp.repair_cell_text
check('repair: en dash stored as e', r('0.37 (0.30e0.44)') == '0.37 (0.30\u20130.44)')
check('repair: scientific number kept', r('1e-5') == '1e-5')
check('repair: U+0004 is a minus', r('0.01 (\x040.08 to 0.08)') == '0.01 (\u22120.08 to 0.08)')
check('repair: U+0003 is a times sign', r('27 items \x03 112 publications') == '27 items \u00d7 112 publications')
check('repair: thorn is plus', r('Title\u00feabstract') == 'Title+abstract')
check('repair: private-use digits', r('\uf135\uf139.\uf139 %') == '59.9 %')
check('repair: five for equals only when the arithmetic holds', '= up to 3024' in r('27 items \x03 112 publications 5 up to 3024 ratings') and ' 5 up to 3000' in r('27 items \x03 112 publications 5 up to 3000 ratings'))
check('repair: footnote letter after interval removed', r('0.90 (0.88\u20130.93)a') == '0.90 (0.88\u20130.93)' and r('62%b') == '62%' and r('3.1c') == '3.1')
check('repair: footnote letter returned in notes', _pp.repair_cell_text_notes('0.90 (0.88\u20130.93)a')[1] == {'footnotes': ['a']})
check('repair: units and words are kept', all(r(x) == x for x in ['3d', '37.5d', '2b', 'ChatGPT4o', '(95% CI)a', '5 cm\u00b2']))
check('repair: superscript footnote removed, exponent kept', r('40% (37%)\u00b2') == '40% (37%)' and r('2 \u00d710\u00b2') == '2 \u00d710^2')
check('repair: flattened power of ten', r('10\u22123') == '10^\u22123' and r('10\u221212 years') == '10\u221212 years')
check('repair: bar before a number is a tilde, word bars kept', r('200k (|150k)') == '200k (~150k)' and r('2. |diff| \u2193') == '2. |diff| \u2193')
check('repair: Khmer script marked unreadable', r('\u178a\u1780 2/3') == '[unreadable] 2/3')
check('repair: plain cell unchanged', r('2.95 \u00b1 1.19') == '2.95 \u00b1 1.19' and r('') == '')
```

## Files

- pages.json, pages.py: page selection
- run_pymupdf.py, run_marker.py, run_mineru.py: extraction runs; results/<parser>/<citekey>__p<page>.json hold the cells and seconds
- tablelib.py (HTML to grid, number normalisation, repair_cell_text), evaluate.py (Evaluations A and B), symbol_report.py
- eval_A.json, eval_summary.json, eval_B_pages.tsv are the no-repair run; eval_*_norepair.* and eval_*_repair.* are both runs side by side
- scan_rotated.py, rotated_scan.json; rotation_build.py, run_rotation.sh, score_rotation.py, rotation_results.json (copies in scratch/rot)
- run_supp.py, run_supp.sh, score_supp.py, supp_results.json, results_supp/
- analyze_missed.py, build_missed_report.py, missed_values.json, missed-values.md, missed-values.html, missed-values-images/ (local only); tablelib_tests.py, repair_audit.py, repair_audit.json, vault_repair_block.py, apply_vault_repair.py, symbol_report_before_extension.json
- derotate.py, derotate_build.py, derotate_log.json, rotation2_build.py, run_rotation2.sh, run_rotation3.sh, run_rotation4.sh, score_rotation2.py, rotation2_results.json
- tablenumbers.py, vault_table_numbers_block.py, score_modes.py, scoring_modes.json, tablenumbers_tests.py; docx_test.py, docx_results.json, vault_docx_tables_block.py
- build_review.py, build_review_extra.py, review_index.tsv, review.html, review/ (PNG at 110 dpi and text grids per parser)

## MinerU and rotation: a derotation step

Code: derotate.py (functions derotate_page and choose_orientation), derotate_build.py, derotate_log.json, run_rotation2.sh, run_rotation3.sh, run_rotation4.sh, score_rotation2.py, rotation2_results.json; offline tests in tablenumbers_tests.py.

Step (a), pages with a text layer: derotate_page(page) returns an upright copy and an info dict. Rule: read the direction vector of every text line (get_text('dict'), line dir, in unrotated page space), round its angle to a multiple of 90 degrees, take the angle that holds the most characters (at least 20 characters, otherwise the page counts as having no text layer). The copy gets rotation 0: a page that only carried a /Rotate value is reset; a page whose content is turned (90, 180, 270) is placed on a new page of swapped size with show_pdf_page(rotate=angle), which keeps the text layer. My first version only called set_rotation; MinerU read such /Rotate copies badly (367 of 463 values), so the final version flattens the content. The rule picked the correct angle on all 144 page copies of the six text-layer variants (rot90, rot180, rot270 and the content-turned cont90, cont180, cont270, 24 pages each).

MinerU, values found of 463 (row found in brackets), text-layer pages, 24 pages:

| Orientation | Before | After derotation |
|---|---|---|
| 0 | 431 (425) | not needed |
| 90, page set with /Rotate | 380 (375) | 431 (426) |
| 90, content turned inside an upright page | 341 (325) | 431 (426) |
| 180, upside down (/Rotate) | 430 (425), 34 s per page against 4.7 s upright | not run: the copy is the upright page (the step picked angle 0 on all 24 pages) |
| 270, page set with /Rotate | 397 (389) | not run: same reason (the step picked rotation 0 on all 24 pages) |

PyMuPDF on the same copies, for comparison: 424 values upright; 0 at 90, 270 and on content-turned 90; 424 at 180 (but only 381 rows); after derotation 424 (419) on both the 90 variants. So the step also removes the PyMuPDF problem.

Step (d), 0 and 180: MinerU reads an upside-down text-layer page almost as well as an upright one (430 against 431) but is about 7 times slower per page (34 s against 4.7 s, measured while the machine had a load average of 10 to 57, so the absolute times are inflated). Upside-down image-only pages are the worst case: 65 of 463 values and 61 s per page. The derotation step avoids both.

Step (b), image-only pages (no text layer, so the step above cannot decide): I rendered the four orientations of each page and ran MinerU on each. Run on 14 of the 24 pages (Sarol, Bougie and Woelfle; the Tyser pages were left out because MinerU needed 30 to 60 s per page while the machine was busy), which hold 419 of the 463 values. Values found on those pages:

| Image-only copy turned by | 0 | 90 | 180 | 270 |
|---|---|---|---|---|
| MinerU, as given | 312 | 230 | 59 | 297 |

Choosing among the four orientations per page: by the number of numeric cells 216 of 419 (a bad score, because sideways OCR noise produces many numeric cells); by the share of table words found in the macOS word list /usr/share/dict/words (offline, no model) 368 of 419, whichever way the page started. The word-list rule chose the upright orientation for 9 of 14 pages and another orientation for the other 5, where the other reading found more values; the choice is therefore a better reader of the page, not a proof of orientation. Cost: four MinerU runs per page (the 180 degree run is the slowest).

Step (c), local orientation detectors: Tesseract is not installed (which tesseract finds nothing, so PyMuPDF OCR and Tesseract OSD are unavailable); I installed nothing with brew. MinerU and Marker (surya) have no page-orientation function I could call; MinerU has an internal angle classifier for single OCR text lines only. The word-list rule above is the only orientation test I found that needs no installation.

Recommendation: before MinerU, run derotate_page on every page that has a text layer (about 0.2 s per page, no model); for image-only pages try the four orientations with the word-share score only when the page is known or suspected to be sideways, because it costs four runs. Marker needs no step (it returned the same cells at every angle), and PyMuPDF needs the step (0 values at 90 and 270 degrees); the vault function table_cells already resets page.rotation to 0.

Limits: 24 synthetic copies made from upright pages; derotated copies for 180, 270 and the other content-turned angles were not read by MinerU (the pages are identical to the upright pages the step builds, and MinerU needed 15 to 60 s per page while the machine was busy); the image-only test used 14 pages; Marker was not run on rot180 or the content-turned copies.

## Scoring modes: caption, footnote and any-cell matches

The owner approved a second scoring mode (score_modes.py, scoring_modes.json, vault_table_numbers_block.py). The strict mode is unchanged. The any mode counts a verified value as found when its number appears (a) inside any cell of the parser's tables, including mixed text cells ("$ 1.15 (0.65-1.98) ~2 mins") and label cells ("Top 5 sentences"), or (b) in the caption or footnote text of the tables on the page (caption_footnote_text: blocks that start with "Table N." or "Table N:", Note, Source, Abbreviations, or that lie directly below a table and start with a footnote symbol, a lowercase letter marker or are set in smaller type).

| Mode (463 values; PyMuPDF and Marker with the extended repair, MinerU as read) | PyMuPDF | Marker | MinerU |
|---|---|---|---|
| strict: number-like cell only | 431 (93.1%) | 431 (93.1%) | 431 (93.1%) |
| any cell (labels and mixed text cells count, no caption text) | 451 (97.4%) | 451 (97.4%) | 451 (97.4%) |
| any cell or caption and footnote text | 463 (100%) | 463 (100%) | 463 (100%) |

All three parsers give the same numbers because they return the same numeric content on these pages; the caption and footnote text is read from the page text layer and does not depend on the parser. Per paper in the third row: Sarol 96 of 96, Bougie 205 of 205, Tyser 44 of 44, Woelfle 118 of 118.

The 451 of the any-cell mode contains 5 accidental matches: Sarol page 6, two "Footnote" values 5 (the footnote says "top five sentences", written as a word; the 5 is credited by the "Recall@5" header cell), and Woelfle page 7, three "Caption" values 9 (credited by "9" in other cells; the caption text itself also holds a 9). In the third mode the Woelfle three are matched in the caption text, so 2 accidental matches remain (the Sarol footnotes); no parser matches the word "five" as a number.

The 12 values not found in any cell by any parser (the any-cell mode) are the caption values of Bougie pages 12 and 17 (the number 1,000 in the captions of Tables 3, 4 and 9, 6 values) and of Tyser page 14 (the scale 0-5 in the Table 5 caption, values 0 and 5, 6 values). The caption and footnote text mode finds all 12.

table_numbers(page) (code in vault_table_numbers_block.py, tested with tablenumbers.py on the 124 pages): 100 of the 124 pages have caption or footnote text; mean 33 numbers per page; 3.2 s per page while the machine was busy (it calls find_tables twice; the result of table_cells could be reused). 5 text blocks were longer than 700 characters; four are the multi-line captions of the Srinivasan Tables S3 and S4 and one is a table header that starts with the word Source (Xu page 5), which the Source rule takes as a footnote. A match is a hint that the value is on the page in a table or its caption, not that it is in the right cell. Offline tests: tablenumbers_tests.py.

## Word files: direct read, PDF conversion, MinerU

Tested on the 9 docx files in the vault pdf folder (docx_test.py, docx_results.json; supplement results also in the supplementary files section).

| Route | Result on Woelfle mmc5 (10 hand-corrected values) | Other docx files | Speed |
|---|---|---|---|
| python-docx read through the XML (docx_tables, vault_docx_tables_block.py) | 3 tables, 368 cells, 10 of 10 values, 10 of 10 rows, 10 of 10 row and column | 0 tables in 7 files, 1 table of 8 cells (no numbers) in sj-docx-4; no nested tables, no text boxes in any file | 0.02 to 0.16 s per file |
| python-docx row.cells (no XML handling) | same 3 tables, identical grids except for footnote letters | same | 0.1 s |
| MinerU, flash tier | 3 tables, 10 of 10 | same counts | 1.5 to 3.4 s per file |
| PyMuPDF opening the docx (it renders the pages itself) | 0 tables on 37 pages, 0 of 10 | 0 tables | 4 to 23 s |
| LibreOffice soffice to PDF, then PyMuPDF | not run: /opt/homebrew/bin/soffice exists but the LibreOffice application it starts is missing, so it does not run; nothing was installed | not run | not run |
| macOS textutil docx to html, then grid | 3 tables, 10 of 10 values, 9 of 10 with row and column | not run | 0.3 s |

Merged cells: mmc5 has 8 horizontal merges (gridSpan) and 2 vertical merges (vMerge). docx_tables repeats the merged text in every covered position; the grids equal MinerU's cell for cell except 17 cells where the Word footnote letter (a superscript run) is removed by repair_cell_text and MinerU keeps it. The three tables are 6x6, 23x7 and 19x9. Old .doc files: no .doc file exists in the vault folder; soffice cannot be used here, and textutil writes a .doc that holds no tables (so my round trip is not a valid test). I could not test a real Word 97 file. Recommendation: do not convert Word files to PDF; read .docx with docx_tables (exact cells, merged spans, 0.02 to 0.16 s, 10 of 10 values), keep MinerU only as a cross-check, and for .doc ask the owner to save as .docx (or convert with soffice where a working LibreOffice is installed). python-docx is installed for the system python3 (3.14) as well as in the venv (version 1.2.0 in the venv); I did not check the system version number.

## Rerun

```
cd ~/Documents/living-synthesis/pipeline/misc/evd-validation/table-parsers
. ~/.cache/lives-bench/env.sh
PY=~/.cache/lives-bench/venv-tables/bin/python
# one paper (Sarol), Evaluation A and B pages
rm -f results/*/@sarol*
$PY run_pymupdf.py pages.json results/pymupdf
$PY run_marker.py pages.json results/marker sarol
$PY run_mineru.py pages.json results/mineru sarol
$PY evaluate.py                # without repair
REPAIR=1 $PY evaluate.py       # with repair_cell_text on PyMuPDF and Marker
$PY symbol_report.py
# rotation (about 15 minutes, run with nohup and poll)
$PY scan_rotated.py; $PY rotation_build.py; nohup ./run_rotation.sh > scratch/rotation.log 2>&1 &
$PY score_rotation.py
# supplementary files (about 3 minutes)
nohup ./run_supp.sh > scratch/supp.log 2>&1 &
$PY score_supp.py
# review page
$PY build_review.py; $PY build_review_extra.py
# missed values and the extended repair
$PY tablelib_tests.py
$PY repair_audit.py; $PY symbol_report.py
$PY analyze_missed.py; $PY build_missed_report.py
$PY tablenumbers_tests.py       # table_numbers, docx_tables, derotate_page tests
$PY score_modes.py              # strict, any-cell and caption/footnote scoring
python3 docx_test.py            # Word files (system python3 has python-docx)
$PY rotation2_build.py; $PY derotate_build.py; nohup ./run_rotation2.sh > scratch/rotation2.log 2>&1 &   # long: 30 to 60 min on a busy machine
$PY score_rotation2.py
python3 apply_vault_repair.py    # puts the repair block into pipeline/scripts/pdf_pages.py (not yet applied)
```

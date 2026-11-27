# Table cell extraction: PyMuPDF find_tables vs Marker vs MinerU

Run date 2026-11-26, Apple Silicon Mac, Python 3.11 venv at ~/.cache/lives-bench/venv-tables.

## Short answer

Neither Marker nor MinerU is clearly worth adding for table cells. On the 463 verified table numbers from the four pilot papers, PyMuPDF find_tables found 91.6 percent, Marker found the same 91.6 percent (the same 424 values), and MinerU found 93.1 percent (7 more values, all from one paper, Woelfle; with a one-line text repair for en dashes the gap shrinks to 4). All three miss the same 32 values. Marker and MinerU return more complete cell text on some tables, and each finds tables that PyMuPDF returns as empty, but the gain in the number we care about is small, and MinerU is about 6 times slower per page. If one is added, MinerU is the better candidate on these numbers; Marker adds nothing to Evaluation A.

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
| PyMuPDF find_tables | 424/463 = 91.6% | 419/456 = 91.9% | 423 = 95.1% | 419 = 94.2% |
| Marker | 424/463 = 91.6% | 419/456 = 91.9% | 423 = 95.1% | 419 = 94.2% |
| MinerU (basic) | 431/463 = 93.1% | 425/456 = 93.2% | 430 = 96.6% | 425 = 95.5% |

The strict subset drops 18 entries whose location is a caption, footnote or header rather than a table cell.

Per paper (values found out of total; same for rows within 1): Sarol 90/96 for all three; Bougie 199/205 for all three; Tyser 38/44 for all three; Woelfle 97/118 for PyMuPDF and Marker, 104/118 for MinerU.

What the 32 values missed by all three are (read from eval_A.json): row-label numbers that are part of a text cell, not a cell value (Sarol page 6, "Top 5 sentences" gives value 5, "Top 20 sentences" gives 20); numbers that appear in a caption (Bougie pages 12 and 17, value "1,000" in the Table 3, 4 and 9 captions); and a few Woelfle cells (Table 1 cost cells such as 0.012 and 1.15, and the "9/9" and "8/9" cells of Table 3) that I did not look into further.

Why MinerU found 7 more: in the Woelfle PDF the text layer encodes the en dash inside confidence intervals as the letter e (PyMuPDF and Marker return "0.37e0.44"; MinerU reads the page image with OCR and returns "0.37–0.44"). My number reader then misses the second number of each interval. This is a text-layer encoding issue, not a table-structure difference. When I add a repair rule that treats a letter e between digits as a separator (run with REPAIR_E_DASH=1, results in eval_summary_edash_repair.json), PyMuPDF and Marker rise to 427/463 = 92.2 percent (value) and 422/456 = 92.5 percent (row), and MinerU stays at 93.1 and 93.2 percent. So 3 of the 7 extra values come from the dash encoding, and 4 remain MinerU only (I did not look at those 4 individually; the earlier list of MinerU-only values included Woelfle Table 2 PRECIS-2 values 0.04, 0.05, 0.01, 0.02 and the Table 3 "5/9" cells).

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
- Rotated tables: no table page in this set had a page rotation set, and the 8 pages with some vertical text lines (Sridharan Leveraging pages 2 to 7, Son page 4, Wrightson page 3) are pages with a vertical margin line, not rotated tables. Rotated tables were therefore not tested.
- Supplementary pages: not tested, because the seed list resolves to the main paper PDFs only.
- Pages with a low number of table values (text tables such as Hasan page 4 and Huntington-Klein page 8): all three give grids with no numeric cells, so numeric comparison says nothing about them.

## Plain-language judgement

PyMuPDF find_tables already gets 92 percent of the verified numbers, and the values it misses are mostly not cell values at all (numbers inside labels and captions). Marker returns the same numbers for the pilot papers. MinerU recovered 7 more, all in one paper; 3 of them come from the en dash being stored as the letter e in the text layer, which a one-line repair also fixes for PyMuPDF and Marker (92.2 percent), and 4 remain; it costs of about 1.8 seconds a page and an 857 MB download. For the job of checking a number against a table, PyMuPDF with a text-layer fallback is enough. If we want a second opinion on the pages where PyMuPDF returns no table or merged cells (21 of the 124 pages here), MinerU basic is the option I would try first, and Marker is not needed for numbers.

Honest limits: the ground truth covers four pilot papers only; the 27-paper evaluation has no ground truth, so higher cell counts there are not proof of correctness; the row check is a word-overlap rule, not a human check; I did not read every returned grid. Evaluation C (review.html) holds 12 pages for a person to compare.

## Files

- pages.json, pages.py: page selection
- run_pymupdf.py, run_marker.py, run_mineru.py: extraction runs; results/<parser>/<citekey>__p<page>.json hold the cells and seconds
- tablelib.py, evaluate.py: normalization and evaluations; eval_A.json (per-value detail), eval_summary.json, eval_B_pages.tsv; eval_summary_edash_repair.json and eval_A_edash_repair.json are the same run with REPAIR_E_DASH=1
- build_review.py, review_index.tsv, review.html, review/ (PNG at 110 dpi and text grids per parser)

## Rerun one paper (example: Sarol)

```
cd ~/Documents/living-synthesis/pipeline/misc/evd-validation/table-parsers
. ~/.cache/lives-bench/env.sh
PY=~/.cache/lives-bench/venv-tables/bin/python
rm -f results/*/@sarol*
$PY run_pymupdf.py            # all papers, about 30 s
$PY run_marker.py pages.json results/marker sarol
$PY run_mineru.py pages.json results/mineru sarol
$PY evaluate.py
```

# Missed table values: what the 33 are and why

## What the 463 values are

The project reads scientific papers and records the numbers that support each finding. Four pilot papers (Sarol et al. 2024, Bougie et al. 2024, Tyser et al. 2024, Woelfle et al. 2024) were checked by hand against the PDF; the 463 values here are the numbers from those papers whose location was recorded as a table (file picost.json of the batch05 and batch07 runs, fields value, pdf_page, table_or_figure, row, column). A parser "finds" a value when, on that PDF page, the value appears as a number in a number-like cell of a table the parser returned (commas, leading zeros, plus-minus signs and percent signs ignored). PyMuPDF find_tables is the baseline; Marker and MinerU are the two alternatives; "repair" is tablelib.repair_cell_text, which fixes symbols the PDF text layer stores wrongly.

Result with the first repair (the version the 33 were counted with): PyMuPDF 430 of 463; Marker 430; MinerU 431. After the extended repair described in RESULTS.md, PyMuPDF and Marker find 431 of 463, so 32 values remain.

## Summary: cause of each missed value

| Cause | Values | Bougie | Sarol | Tyser | Woelfle |
|---|---|---|---|---|---|
| Caption or footnote text | 17 | 6 | 2 | 6 | 3 |
| Value inside a label cell | 10 | 0 | 4 | 0 | 6 |
| Value inside a mixed text cell | 5 | 0 | 0 | 0 | 5 |
| Symbol problem still unrepaired (first repair) | 1 | 0 | 0 | 0 | 1 |
| No table detected | 0 | 0 | 0 | 0 | 0 |
| No ruling lines, columns or rows merged | 0 | 0 | 0 | 0 | 0 |
| Value in a figure or image | 0 | 0 | 0 | 0 | 0 |
| Header spans | 0 | 0 | 0 | 0 | 0 |
| Total | 33 | 6 | 6 | 6 | 15 |

Cause definitions (fixed list): Caption or footnote text: The value is written in the caption or a footnote of the table, not in a table cell.; Value inside a label cell: The number is part of a row label or header text, for example "Top 5 sentences" or "(3) Combined LLMs (consistent in 9/9)".; Value inside a mixed text cell: PyMuPDF returned the value, but inside a cell that also holds words or units; the scorer accepts only number-like cells.; Symbol problem still unrepaired (first repair): A U+0004 minus sign and a footnote letter in the cell kept the cell from being read as a number; the extended repair fixes it.; No table detected: find_tables returned nothing on the page.; No ruling lines, columns or rows merged: The table has no lines, so cells were merged.; Value in a figure or image: The value is drawn in an image, with no text layer.; Header spans: A merged header cell moved the columns.; Other: Anything else.

Main finding: none of the 33 is a table cell that PyMuPDF read wrongly or did not see. In 17 cases the value is in a caption or footnote, in 10 it is part of a row or header label, in 5 it is present in a cell with text around it that the scorer did not accept, and in 1 a symbol problem hid it (recovered by the extended repair). No table was undetected, no figure was involved, and no merged header moved a column for these values.

## One row per missed value

Marker and MinerU columns: found as a number-like cell value on the page (Marker plain / Marker with first repair / Marker with extended repair / MinerU).

| # | Paper | PDF page | Table | Row label | Column label | Value | Location text given by the pipeline | What PyMuPDF returned | Marker (plain / repair 1 / repair 2) | MinerU | Cause |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sarol | 6 | Table 4 | Top 5 sentences | Evidence input | 5 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 2 | Sarol | 6 | Table 4 | Top 10 sentences | Evidence input | 10 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 3 | Sarol | 6 | Table 4 | Top 20 sentences | Evidence input | 20 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 4 | Sarol | 6 | Table 4 | Top 20 sentences + annotated evidence | Evidence input | 20 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 5 | Sarol | 6 | Table 4 | Footnote | Not applicable | 5 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 6 | Sarol | 6 | Table 4 | Footnote | Not applicable | 5 | Table 4; label: Number of retrieved evidence sentences; unit sentences | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 7 | Bougie | 12 | Table 3 caption | (caption or text) | - | 1,000 | Table 3 caption; label: Sample size; unit papers | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 8 | Bougie | 12 | Table 3 caption | (caption or text) | - | 1,000 | Table 3 caption; label: Sample size; unit papers | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 9 | Bougie | 12 | Table 3 caption | (caption or text) | - | 1,000 | Table 3 caption; label: Sample size; unit papers | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 10 | Bougie | 12 | Table 4 caption | (caption or text) | - | 1,000 | Table 4 caption; label: Sample size per dataset; unit papers | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 11 | Bougie | 12 | Table 4 caption | (caption or text) | - | 1,000 | Table 4 caption; label: Sample size per dataset; unit papers | 2 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 12 | Bougie | 17 | Table 9 caption | (caption or text) | - | 1,000 | Table 9 caption; label: Sample size per dataset; unit papers | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 13 | Tyser | 14 | Table 5 | Caption | - | 0 | Table 5; label: Rating scale minimum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 14 | Tyser | 14 | Table 5 | Caption | - | 5 | Table 5; label: Rating scale maximum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 15 | Tyser | 14 | Table 5 | Caption | - | 0 | Table 5; label: Rating scale minimum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 16 | Tyser | 14 | Table 5 | Caption | - | 5 | Table 5; label: Rating scale maximum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 17 | Tyser | 14 | Table 5 | Caption | - | 0 | Table 5; label: Rating scale minimum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 18 | Tyser | 14 | Table 5 | Caption | - | 5 | Table 5; label: Rating scale maximum; unit score | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 19 | Woelfle | 5 | Table 2 | PRISMA header | Rater | 112 | Table 2; label: PRISMA publications; unit publications | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 20 | Woelfle | 5 | Table 2 | AMSTAR header | Rater | 112 | Table 2; label: AMSTAR publications; unit publications | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 21 | Woelfle | 5 | Table 2 | PRECIS-2 / (2) GPT-3.5 | Cohen's kappa (95% CI) | 0.04 | Table 2; label: GPT-3.5 PRECIS-2 kappa; unit kappa | 1 table(s) found on the page. The value is in a cell with a U+0004 minus sign and a footnote letter; found after the extended repair. | no / no / yes | yes | Symbol problem still unrepaired (first repair) |
| 22 | Woelfle | 7 | Table 3 | Caption | - | 9 | Table 3; label: Number of combined LLM assessments; unit assessments | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 23 | Woelfle | 7 | Table 3 | PRISMA / (3) Combined LLMs (consistent in 9/9) | Rater | 9/9 | Table 3; label: Highest consistency threshold; unit threshold | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 24 | Woelfle | 7 | Table 3 | Caption | - | 9 | Table 3; label: Number of combined LLM assessments; unit assessments | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 25 | Woelfle | 7 | Table 3 | AMSTAR / (3) Combined LLMs (consistent in 9/9) | Rater | 9/9 | Table 3; label: Highest consistency threshold; unit threshold | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 26 | Woelfle | 7 | Table 3 | Caption | - | 9 | Table 3; label: Number of combined LLM assessments; unit assessments | 1 table(s) found on the page. The value is in the caption or footnote text only. | no / no / no | no | Caption or footnote text |
| 27 | Woelfle | 7 | Table 3 | PRECIS-2 / (3) Combined LLMs (consistent in 8/9) | Rater | 8/9 | Table 3; label: 8/9 consistency threshold; unit threshold | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 28 | Woelfle | 7 | Table 3 | PRECIS-2 / (3) Combined LLMs (consistent in 9/9) | Rater | 9/9 | Table 3; label: Highest consistency threshold; unit threshold | 1 table(s) found on the page. The number is inside a label or header cell. | no / no / no | no | Value inside a label cell |
| 29 | Woelfle | 3 | Table 1 | Mistral AI: Mixtral-8x22B | Median cost (IQR) and response time per publication | 0.012 | Table 1; label: Mixtral-8x22B median cost per publication; unit USD | 1 table(s) found on the page. The value is present, inside a cell that also holds text. | no / no / no | no | Value inside a mixed text cell |
| 30 | Woelfle | 3 | Table 1 | OpenAI: GPT-4 | Median cost (IQR) and response time per publication | 1.15 | Table 1; label: GPT-4 median cost per publication; unit USD | 1 table(s) found on the page. The value is present, inside a cell that also holds text. | no / no / no | no | Value inside a mixed text cell |
| 31 | Woelfle | 3 | Table 1 | OpenAI: GPT-3.5 | Median cost (IQR) and response time per publication | 0.06 | Table 1; label: GPT-3.5 median cost per publication; unit USD | 1 table(s) found on the page. The value is present, inside a cell that also holds text. | no / no / no | no | Value inside a mixed text cell |
| 32 | Woelfle | 3 | Table 1 | Anthropic: Claude-2 | Median cost (IQR) and response time per publication | 0.19 | Table 1; label: Claude-2 median cost per publication; unit USD | 1 table(s) found on the page. The value is present, inside a cell that also holds text. | no / no / no | no | Value inside a mixed text cell |
| 33 | Woelfle | 3 | Table 1 | Anthropic: Claude-3-Opus | Median cost (IQR) and response time per publication | 0.40 | Table 1; label: Claude-3-Opus median cost per publication; unit USD | 1 table(s) found on the page. The value is present, inside a cell that also holds text. | no / no / no | no | Value inside a mixed text cell |

## Values MinerU found that PyMuPDF did not

Without any repair, MinerU found 7 values that PyMuPDF did not (all in Woelfle et al.): page 5 Table 2 row "PRECIS-2 / (2) GPT-3.5" value 0.04; page 5 Table 2 row "PRECIS-2 / (2) Mixtral-8x22B" value 0.05; page 5 Table 2 row "PRECIS-2 / (2) Claude-2" value 0.01; page 5 Table 2 row "PRECIS-2 / (2) GPT-4" value 0.02; page 7 Table 3 row "PRISMA / (3) Combined LLMs (consistent in 5/9)" value 5/9; page 7 Table 3 row "AMSTAR / (3) Combined LLMs (consistent in 5/9)" value 5/9; page 7 Table 3 row "PRECIS-2 / (3) Combined LLMs (consistent in 5/9)" value 5/9.
With the first repair on PyMuPDF, 1 remained (the 0.04 in Table 2, PRECIS-2, GPT-3.5, Cohen's kappa). With the extended repair 0 remain: PyMuPDF and Marker now find all 431 values MinerU finds.
The reason for the original gap was the text layer: Woelfle encodes the en dash inside confidence intervals as the letter e, minus signs as a control character and footnote markers as letters glued to numbers; MinerU reads the page image and avoids these.

## What a code change could fix

| Cause | Values | Change | Values recovered (estimate) |
|---|---|---|---|
| Caption or footnote text | 17 | These are not cell values. Either relabel them in the ground truth as caption or footnote text (no code), or let the checker also search the caption and footnote text of the page (a few lines on top of table_cells). | up to 17 of 17 by caption search; the 12 in the Bougie and Tyser captions appear in no cell at all |
| Value inside a label cell | 10 | Accept a match in any cell of the table, label cells included, when the ground truth row is a header or label. | 10 of 10 |
| Value inside a mixed text cell | 5 | Accept a number token inside a cell that also contains units or words (split the cell on spaces and brackets). | 5 of 5 |
| Symbol problem still unrepaired | 1 | Already done in the extended repair_cell_text (U+0004 minus plus the footnote letter). | 1 of 1 |

If the scorer accepted a number token in any cell (labels and text cells included), every parser would find 451 of 463; 5 of those extra matches are accidental (the token 5 in a header such as Recall@5, the token 9 in other cells) and are not the cell the ground truth means. The remaining 12 are the Bougie and Tyser caption values.
Pages and images: missed-values.html shows a crop of the page with the value highlighted for each value (local images in missed-values-images/).

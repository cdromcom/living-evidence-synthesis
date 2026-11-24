# PICOST JSON schema (version 1.0)

One file per EVD node, named `<EVD-id>.json` (for example `EVD-019.json`). The markdown vault stays the source of truth for the EVD statement. These files hold the structured PICOST summary of what each EVD's paper did, plus the numbers behind the finding. The GSheet "LIVES vault mirror (JP review)" shows them on its PICOST tab.

PICOST means Population, Intervention, Comparator, Outcome, Study design, Timeframe.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `schema_version` | string | Always `"1.0"` for this layout. Bump when fields change. |
| `evd_id` | string | Vault EVD node id, e.g. `EVD-019`. Same as the benchmark EVD number (`EVD-019` is benchmark EVD 19). |
| `evd_title` | string | The EVD node title in the vault at the time of writing. |
| `citekey` | string | Citekey of the source paper, e.g. `thelwallEvaluatingResearchQuality2024`. |
| `source_id` | string | Vault SRC node id of that paper, e.g. `SRC-019`. |
| `finding` | string | The EVD statement (the claim the paper supports). For legacy files this is the vault title. |
| `P` | string | Population: who or what was studied (papers, reviews, trials, items), with sample sizes. |
| `I` | string | Intervention: the model, tool or method tested and how it was run (prompting, version, settings). |
| `C` | string | Comparator: what the intervention was compared against (humans, baselines, other models). |
| `O` | string | Outcome: the measured results with their values, as printed in the paper. |
| `S` | string | Study design. |
| `T` | string | Timeframe: when the data, models or papers date from. `Not reported` when the paper is silent. |
| `numbers` | array | Individual numeric values behind the outcome, one object each (below). Empty when the outcome cannot be split unambiguously. |
| `locators_status` | string | `legacy-not-recorded` (numbers came from the old PICOST tab, no page locators), `partial` (some numbers have locators), `complete` (every number has all four locator parts or `Not reported`). |
| `origin` | string | Where this record came from, e.g. `PICOST tab 2026-11-17 legacy`. |
| `extraction_model` | string or null | Model that extracted the record. `null` for legacy records. |
| `verified_by` | string or null | Person who checked every number against the PDF. `null` until verified. |
| `verified_on` | string or null | Date of that check (`YYYY-MM-DD`). `null` until verified. |

### `numbers[]` items

| Field | Type | Meaning |
|---|---|---|
| `value` | number | The value as printed (percentages as 66.9 with `unit` `"%"`, not 0.669). |
| `label` | string | What the value is, e.g. `Spearman r: abstracts`. |
| `unit` | string or null | `"%"`, `"USD"`, and so on; `null` for unitless values (correlations, F1, kappa). |
| `locator` | object | Where in the paper the value is printed (below). |

### `locator` object

Rule for new papers: every number and every value must carry a locator. Fill all four parts. Write the string `Not reported` when the paper is silent on that part (for example a value in running text has no table row). Do not leave a part as `null` in a new record. `null` is allowed only in `legacy-not-recorded` records.

| Field | Meaning |
|---|---|
| `journal_page` | Printed journal page number (the number on the page, not the PDF page index). |
| `table_or_figure` | Table or figure label, e.g. `Table 2`, `Figure 3b`. |
| `row` | Row label inside the table, as printed. |
| `column` | Column label inside the table, as printed. |

## Legacy records (this folder, 2026-11-24)

All 77 files were imported from the PICOST tab of the Google Sheet "LIVES - AAA Benchmarking (HAI)" (2026-11-17). Matching rule: the sheet's EVD number equals the vault EVD id number, and the sheet citekey equals the vault source for every row (checked for all 81 rows). Where the sheet has continuation rows for one EVD (`45 (cont.)`, `47 (cont.)`: EVD-045 has 3 rows, EVD-047 has 3 rows), the P, I, C, O, S, T cells of those rows are joined with ` || ` in row order.

`numbers` is filled only where the O cell is a plain list of `label value` items (4 files: EVD-019, EVD-026, EVD-038, EVD-074). Every other record has `numbers: []`. No locators exist for any of them.

Known defects in the legacy source (copied as is; fix when re-extracting):

- EVD-064, EVD-065, EVD-066: the O cell was pasted from the Woelfle et al. rows and does not describe those papers. Check O against the paper.
- EVD-014, EVD-050, EVD-065, EVD-066, EVD-075: the vault titles were corrected on 2026-11-24 (`misc/evd-validation/2026-11-24-renames.json`). The legacy sheet text and O cell can still carry the pre-correction numbers (for example 16.3% for EVD-014, now 11.0%).

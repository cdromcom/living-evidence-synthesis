# Screening runs

Each run sorts a Zotero collection of candidate papers into task-type categories with a vote of local embedding models, using the seed papers as a guide, and builds a review sheet for the person who screens. One folder per run, named `<date>_<collection>`.

| Folder | What it holds |
|---|---|
| `shared/` | The 27 seed papers and the task group(s) each belongs to (`seed-papers_task-groups.json`), and the short names and task-type phrases for those groups |
| `<date>_<collection>/README.md` | The report for that run, following TRIPOD+LLM as far as it fits (data, models, analysis, performance, limitations, data and code links) |
| `<date>_<collection>/data/` | Metadata-only results (no abstracts, no local paths): per-paper categories and model votes, new categories one paper per row, duplicates, model check, settings and package versions, and the names written for new categories |

Code is in `pipeline/scripts/` (`zotero_collection.py`, `screen_dedup.py`, `screen_embed.py`, `screen_to_gsheet.py`). Working files that contain abstracts and local file paths stay outside the repository (`~/.cache/lives-bench/screening/`).

Code for the whole-library run: `zotero_inventory.py`, `screen_all.py`, `screen_all_to_gsheet.py`, `oa_lookup.py`.

Runs so far:
- `2026-11-25_SysRev-Elicit-2026-11-24` (82 distinct papers, the new Elicit ingest).
- `2026-11-25_Zotero-all-libraries` (17,544 distinct papers from all seven Zotero libraries; 3,441 sheet rows: every ingest-folder paper plus papers found elsewhere; open-access column from OpenAlex).

## Adding new papers to the whole-library screening sheet
The sheet (`https://docs.google.com/spreadsheets/d/171mPb_rNCHEoZm-9ThYnjpU73Dnb6ToeRfj715YAvjs/edit`) keeps one row per paper and never reorders, so your labels stay put. Each row has a **Stable id** (Zotero library:key).
1. Add the papers to Zotero and let it sync, then close Zotero if you want the duplicate merge (`zotero_merge_duplicates.py` needs it closed; the inventory only reads a copy).
2. `python3 pipeline/scripts/zotero_inventory.py`
3. In the embedding environment: `screen_all.py prepare`, then `screen_all.py embed` (only new texts are embedded; the rest comes from the cache), then `screen_all.py analyze`.
4. `python3 pipeline/scripts/oa_lookup.py` for the open-access column of the new DOIs.
5. Save the Stable id column of the sheet to a text file, then run `python3 pipeline/scripts/screen_all_to_gsheet.py --only-new known-ids.txt --out new-rows.xlsx`. It builds only the rows that are not in the sheet yet.
6. Append those rows to the Papers tab. Ask Claude to "refresh the screening sheet" and it does steps 2 to 6.
New papers that the three models call NEW are shown as "Unsorted: new since the last sort". Every few months run a full sort again; keep your labels by merging on the Stable id (the merge step is a TODO).

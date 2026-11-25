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

# Screening run 2026-11-25_SysRev-Elicit-2026-11-24

Collection: SysRev - Elicit 2026-11-24. Built 2026-11-25. Reported following TRIPOD+LLM as far as it fits (embedding models, no generation). The Google Sheet has the same content with the full per-paper tables.

## Reporting guideline
TRIPOD+LLM (Gallifant et al.), applied as far as it fits: the models here only embed text (no text is generated, no prompts or fine-tuning), so items about generation and prompting are marked not applicable.
- [TRIPOD+LLM statement](https://www.tripod-statement.org/tripod-llm/)

## 1. Title and purpose
Screening papers in the Zotero collection "SysRev - Elicit 2026-11-24" into task-type categories, guided by the 27 seed papers; run 2026-11-25_SysRev-Elicit-2026-11-24. Purpose: help JP decide which incoming papers to include in the living synthesis and which task types exist.
- [This run on GitHub](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24)

## 2. Objectives
Assign each distinct paper to one of the seed task types, or to a new candidate task type; flag duplicates and papers already seen. Nothing in Zotero was changed.

## 3. Data source and population
Zotero collection "SysRev - Elicit 2026-11-24": personal library (164 records) and the OASIS Lab group copy (172 records), exported from a copy of zotero.sqlite on 2026-11-25. After de-duplication: 82 distinct papers. The collection is the output of an Elicit search imported on 2026-11-24 (not a sample). Seed set: 27 papers already in the vault, grouped into 6 task types by the Review-Arena sections.
- [Seed papers and task groups](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/screening/shared/seed-papers_task-groups.json)
- [Export script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/zotero_collection.py)

## 4. De-duplication
Records match when they share a DOI or arXiv id, have the same normalized title, or have a title similarity of at least 0.90 (a preprint and its journal version). Done inside each folder on its own, across the two library copies, against the seed papers and against the older pool (added). Duplicate records within a folder: OASIS Lab group copy: 90; personal library: 82. The preferred record is the published, newest one; nothing is deleted. See the Duplicates tab (struck through = duplicate within its folder) and the Folder dedup tab.
- [Script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/screen_dedup.py)
- [Data](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24/data/duplicates_all-zotero-records.tsv)

## 5. Outcome
The task type of each paper: one of the seed task groups, or NEW (then clustered into a candidate new category).

## 6. Models (predictors)
Three open-weight embedding models, run locally on one Apple-silicon computer (no API, no data leaves the machine): EmbeddingGemma 2 (Google, 2026-10, Apache 2.0), harrier-oss-v1-0.6b (Microsoft, MIT; similarity prompt "sts_query"), DNA-VL-STEER-2B (Dnotitia, Korea; Apache 2.0; a calibrated variant of Qwen3-VL-Embedding-2B). Versions and packages: settings_and_versions.json. Origin policy: open-weight foreign models are allowed when local and near state of the art (JP, 2026-11-25).
- [Settings and versions](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24/data/settings_and_versions.json)
- [Model notes](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/skills/Tools-and-Models.md)

## 7. Input and prompts
Each paper is represented by title + the first 3 PDF pages (at most 6,000 characters). No generation, no instructions beyond the models' default prompts, no fine-tuning. Papers with no usable text are flagged.
- [Script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/screen_embed.py)

## 8. Reference standard
The seed papers' task groups come from the Review-Arena sections of the vault (JP's own grouping of the questions each paper answers). There are no human labels for the new papers yet: JP's decisions in the Papers tab will become the reference standard.
- [Seed labels](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/screening/shared/seed-papers_task-groups.json)

## 9. Analysis
(a) Each model: cosine similarity between the paper and every seed; the paper gets the task group of its most similar seed, or NEW if that similarity is below the model's own 15th percentile of seed-to-seed nearest similarity. (b) Majority vote: a category needs 2 of 3 models to agree. (c) Papers voted NEW are clustered (average linkage on the mean of the three models' distances); the distance threshold is chosen by silhouette score (0.262, 51 papers clustered); clusters of 2 or more papers become candidate categories. (d) Category keywords: the 7 highest mean TF-IDF terms of the members' titles and abstracts. (e) Category names and task-type phrases were written by Claude Sonnet 5.5 from the keywords and member titles and are not yet checked by a person. E-means (a fast k-means for huge datasets) was not used: with this few papers ordinary clustering is instant.
- [Script (votes and clusters)](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/screen_embed.py)
- [Script (this workbook and data files)](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/screen_to_gsheet.py)
- [Category names](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24/data/new-category-names_and-task-types.json)

## 10. Performance
Leave-one-out on the seed papers (each seed hidden, then classified from the others): EmbeddingGemma 2 73%; harrier-oss-v1-0.6b 73%; DNA-VL-STEER-2B 77%. This is the only accuracy measure so far; the sample is small (one task group has a single seed). Agreement with JP's decisions will be added when the Papers tab is filled in.
- [Data](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24/data/model-check_leave-one-out.tsv)

## 11. Missing data
Papers with no abstract or little PDF text are flagged in Screening hints; a record with a wrong title in Zotero is flagged too. No imputation.

## 12. Limitations
Categories reflect how similar the first pages or abstracts are, not a reading of the paper. Seed task groups are few and uneven. Category names are suggestions. Embeddings may group by topic or field more than by the task a model performs.

## 13. Ethics and privacy
Only titles, abstracts, DOIs and Zotero keys of published papers are used. Abstracts and local file paths stay out of the public repository; the repository holds metadata only.

## 14. Open science (data and code)
All code and metadata-only data are on GitHub in the folders linked here; the working files with abstracts stay on the computer that ran the analysis. To reproduce: run zotero_collection.py, screen_dedup.py, screen_embed.py and screen_to_gsheet.py in that order (commands in the run folder README).
- [Run folder](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24)
- [All scripts](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/scripts)
- [Run folder README](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_SysRev-Elicit-2026-11-24/README.md)

## 15. AI-use disclosure (GAMER)
The scripts, the category names and this report were written by Claude Sonnet 5.5 (Claude Code) on 2026-11-25; the embedding models are the three named above. A person has not yet reviewed them.
- [AI disclosure](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/provenance/AI-disclosure.md)

## How to review
Use the Papers tab: filter by Proposed category or Screening hints, then fill JP: decision and JP: category (dropdown from the Lists tab).

## Built
2026-11-25

## Files in `data/`
- `papers_categories-and-model-votes.tsv`: one row per distinct paper, category, task type, each model's pick and similarity, hints (no abstracts, no local paths).
- `new-categories_one-paper-per-row.tsv`, `categories_summary.tsv`: the candidate new categories and all categories with task types and keywords.
- `duplicates_all-zotero-records.tsv`, `folder-dedup_summary.tsv`: every Zotero record with its duplicate role inside its folder and across folders.
- `model-check_leave-one-out.tsv`, `settings_and_versions.json`: how well each model recovers the seed groups; every setting and package version.
- `new-category-names_and-task-types.json`: the names written for the new categories (edit here, rerun the last script).

## Commands (run from the vault root; Python environment `~/.cache/lives-bench/venv-embed`)
```
python3 pipeline/scripts/zotero_collection.py "SysRev - Elicit 2026-11-24" --library 1
python3 pipeline/scripts/screen_dedup.py <export>.json --also <group-copy export>.json --pool <other-set export>.json
python pipeline/scripts/screen_embed.py --dedup dedup.json --text-mode pdf
python pipeline/scripts/screen_to_gsheet.py --result screen-result.json --dedup dedup.json --run-dir 2026-11-25_SysRev-Elicit-2026-11-24 --collection "SysRev - Elicit 2026-11-24" --text-mode pdf
```

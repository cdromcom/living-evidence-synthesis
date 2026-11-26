# Vault scripts

Helper scripts that maintain the discourse graph. Run from the vault root.

| Script | Purpose |
| ------ | ------- |
| `extract_quotes.py` | Render quote-region PNGs from a JSON spec via PyMuPDF (fitz). |
| `quote_pipeline.py` | Unified screenshot pipeline for EVDs/CLMs/CVTs. |
| `cvt_screenshot_pipeline.py` | Auto-locate quotes in CVTs lacking screenshots and embed them. |
| `reverse_links.py` | Build `## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence` sections (idempotent). |
| `readability_pass.py` | Apply blank-line rules across all node files. |
| `verbatim_audit.py` | Compare every quote to its source PDF and write `pipeline/misc/evd-validation/paraphrase_report.tsv`. |
| `build_dgraph.py` | Regenerate `sysrev/indexes/dgraph.md` central index from the vault's current state. |

All scripts are idempotent. Re-run any script after making structural changes — the output stays in sync.

Dependencies: `fitz` (PyMuPDF), `pdftoppm` (poppler-utils, optional).


## Added 2026-11-24 (Skill v2 backbone)
- `pdf_pages.py` page map (printed page vs PDF position), quote locator and verbatim check, highlighted crop, embedded links.
- `signals_common.py`, `audit_signal_quotes.py`, `signals_decision_models.py`, `signals_to_gsheet.py`, `check_quality_signals.py`: traceability audit, decision-model check and human review sheet for the TRIPOD-LLM and Quality appraisal tables.
- `decision_models.py` client for Perplexity Decider 1.3 (text) and Liquid d1.2-ultra (text and images; d1-ultra until 2026-11-26); Jev was dropped.
- `provenance/`: `openalex.py`, `doaj.py`, `opencitations.py`, `pubpeer.py`, `howfairis_check.py` (own virtual environment), `fair_checker.py`, `run_provenance.py`.
- `smoke_test_scripts.py` runs every script on a throwaway vault copy; latest report: `pipeline/misc/evd-validation/2026-11-24-script-smoke-tests.md`.
- Retired: `quote_pipeline.py` (needs `--force`). The vault path comes from `LIVES_VAULT` or the folder two levels above `pipeline/scripts/`.

## Added 2026-11-25
- `call_logger.py`: log every model call (Anthropic, OpenAI, Tinker) to `pipeline/runs/<run>/calls.jsonl` with the unedited response; `footer` renders the AI-use footer; `summary` totals cost.
- `check_links.py`: read-only structural check (links resolve, EVD and CVT agree both ways, one source per EVD, every CLM listed by a QUE, every EP rests on two papers). `check_repo_sync.py`: compare the vault with a GitHub checkout by content hash. `file_model_history.py`: a page's commits by model era. `add_link_aliases.py`: alias for path-qualified node links. `quality_labels.py`: Quality signal row names from `pipeline/templates/quality-signal-labels.json` (`list`, `check`, `apply`).
- `stat_checks.py` and `stat_checks_more.py`: scripted Statistical Accuracy checks on a paper's own numbers (`selftest` plants one error of every kind). Output: `pipeline/misc/evd-validation/stat-checks/`.
- `embed_candidates.py` (run with `~/.cache/lives-bench/venv-embed/bin/python`) and `merge_judge.py` (Sonnet 5.5 and, with `--inkling`, Inkling 2 Small): candidate duplicate nodes and blind second opinions. They never merge anything.
- `design_consult.py`: send a design summary to several models and have others improve the plan (runs in `pipeline/runs/`).
- `Archive.zip`: old scripts, kept as a zip.
- `compare_embedders.py` (run with `~/.cache/lives-bench/venv-embed/bin/python`): compare local embedding models (EmbeddingGemma 2, harrier-oss-v1-0.6b, DNA-VL-STEER-2B) on node titles and on quote-text-to-screenshot matching. Results: `pipeline/misc/evd-validation/embedder-comparison/`.
- `zotero_collection.py`, `screen_dedup.py`, `screen_embed.py`, `screen_to_gsheet.py`: screen a Zotero collection into task-type categories by embedding similarity (three-model vote, seed papers as the guide) and build the review sheet. Run `screen_embed.py` and `screen_to_gsheet.py` with `~/.cache/lives-bench/venv-embed/bin/python`. Working files go to `~/.cache/lives-bench/screening/`.
- Screening runs are written to `pipeline/screening/<date>_<collection>/` (README.md in TRIPOD+LLM style, `data/` metadata-only TSV and JSON); `pipeline/screening/shared/` holds the seed papers' task groups and names. `screen_to_gsheet.py` writes both the review workbook and that folder; category names for new categories are edited in `data/new-category-names_and-task-types.json`.
- `lives_run.py`, `llm_batch.py`: the paper processor (1 to 4 PDFs, $5.55 cap per batch, stop-the-batch rules, run manifest; standard or batch mode per provider; Inkling in parallel). Prompts in `pipeline/prompts/` (`picost-v1.md`, `recheck-v1.md`, `adjudicate-v1.md`). Outputs go to `pipeline/runs/<run>/` and stay local. See `Skill.md`, Step 1, item 11a.
- `zotero_inventory.py`, `screen_all.py`, `screen_all_to_gsheet.py`, `oa_lookup.py`, `zotero_merge_duplicates.py`: whole-library screening (all Zotero libraries), open-access lookup (OpenAlex) and the Zotero duplicate merge (Zotero closed; backup first).

## Added 2026-11-26
- `lives_verify.py`: verification layer. Claude Sonnet 5.5, Perplexity Decider 1.3 and Liquid d1.2-ultra judge every PICOST slot (with page 1 and the Methods pages), quote, QUE reframing, CLM, CVT and quality rating; Liquid d1.2-ultra also reads digits on screenshots. Majority vote, mean, labeling queue (`queue_order`), rerun functions that keep earlier scores.
- `lives_dm_rerun.py`: rerun the Liquid parts of a finished run with the current decision-model id and keep the old scores.
- `analyze_failures.py`: sample the verification items that scored below 0.5 and have Claude Opus 5.5 classify the kinds of problem (`prompts/failure-types-v1.md`).
- `numbers_on_pages.py`: statement numbers against the text of the cited pages; numbers missing from the text are looked up on the screenshots by Liquid d1.2-ultra (with a changed-digit control).
- `focused_extract.py`: Sonnet 5.5 focused extraction from a paper's supplement; `quote_vision_check.py`: stand-alone Sonnet 5.5 screenshot check of quotes.
- `run_to_gsheet.py`: the ABOUT tab now lists every model, package and tool; new tabs Verification (all nodes), Verification summary, Numbers check, Failure analysis.


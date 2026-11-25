# Vault scripts

Helper scripts that maintain the discourse graph. Run from the vault root.

| Script | Purpose |
| ------ | ------- |
| `extract_quotes.py` | Render quote-region PNGs from a JSON spec via PyMuPDF (fitz). |
| `quote_pipeline.py` | Unified screenshot pipeline for EVDs/CLMs/CVTs. |
| `cvt_screenshot_pipeline.py` | Auto-locate quotes in CVTs lacking screenshots and embed them. |
| `reverse_links.py` | Build `## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence` sections (idempotent). |
| `readability_pass.py` | Apply blank-line rules across all node files. |
| `verbatim_audit.py` | Compare every quote to its source PDF and write `sysrev/reference/paraphrase_audit_<date>.tsv`. |
| `build_dgraph.py` | Regenerate `sysrev/indexes/dgraph.md` central index from the vault's current state. |

All scripts are idempotent. Re-run any script after making structural changes — the output stays in sync.

Dependencies: `fitz` (PyMuPDF), `pdftoppm` (poppler-utils, optional).


## Added 2026-11-24 (Skill v2 backbone)
- `pdf_pages.py` page map (printed page vs PDF position), quote locator and verbatim check, highlighted crop, embedded links.
- `signals_common.py`, `audit_signal_quotes.py`, `signals_decision_models.py`, `signals_to_gsheet.py`, `check_quality_signals.py`: traceability audit, decision-model check and human review sheet for the TRIPOD-LLM and Quality appraisal tables.
- `decision_models.py` client for Perplexity Decider 1.3, Liquid d1-ultra, Jev.
- `provenance/`: `openalex.py`, `doaj.py`, `opencitations.py`, `pubpeer.py`, `howfairis_check.py` (own virtual environment), `fair_checker.py`, `run_provenance.py`.
- `smoke_test_scripts.py` runs every script on a throwaway vault copy; latest report: `pipeline/misc/evd-validation/2026-11-24-script-smoke-tests.md`.
- Retired: `quote_pipeline.py` (needs `--force`). The vault path comes from `LIVES_VAULT` or the folder two levels above `pipeline/scripts/`.

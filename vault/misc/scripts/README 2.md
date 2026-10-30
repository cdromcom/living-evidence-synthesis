# Vault scripts

Helper scripts that maintain the discourse graph. Run from the vault root.

| Script | Purpose |
| ------ | ------- |
| `extract_quotes.py` | Render quote-region PNGs from a JSON spec via PyMuPDF (fitz). |
| `quote_pipeline.py` | Unified screenshot pipeline for EVDs/CLMs/CVTs. |
| `cvt_screenshot_pipeline.py` | Auto-locate quotes in CVTs lacking screenshots and embed them. |
| `reverse_links.py` | Build `## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence` sections (idempotent). |
| `readability_pass.py` | Apply blank-line rules across all node files. |
| `verbatim_audit.py` | Compare every quote to its source PDF and write `paraphrase_audit_<date>.tsv`. |
| `build_dgraph.py` | Regenerate `DGRAPH.md` central index from the vault's current state. |

All scripts are idempotent. Re-run any script after making structural changes — the output stays in sync.

Dependencies: `fitz` (PyMuPDF), `pdftoppm` (poppler-utils, optional).

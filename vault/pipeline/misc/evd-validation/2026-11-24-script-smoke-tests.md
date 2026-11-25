---
author: Claude (Sonnet 5.5), for Jay Patel
page_type: log/test
created: 2026-11-24
human_verified: no
---

# Script smoke tests (2026-11-24)

Every script in `pipeline/scripts/` was run once on a **throwaway copy** of the vault (the real vault was not touched) with the vault path set by `LIVES_VAULT`. Smallest possible input where a script takes one (the Akyon 2024 paper; DOI 10.2196/59258; howfairis on its own repository; FAIR-Checker on osf.io). Network scripts and the three decision models ran for real (cents). Harness: `pipeline/scripts/smoke_test_scripts.py`.

**Result: 29 runs, 27 exit 0.** The two non-zero exits are expected: `quote_pipeline.py` is retired and says so; `pangram_check.py` needs `PANGRAM_API_KEY`, which is not in `~/.config/lives-ai-raters/.env` (the other keys are).

## Bugs found and fixed
- **`verbatim_audit.py` crashed** (`quote_pipeline_v3` missing). Fixed to use `pdf_pages.py`. After that it still audited **0 quotes** and reported "0 paraphrases", a false pass: its citekey regex expected `[[@key]]` but the vault now writes `[[sysrev/dgraph/source/@key]]`. Fixed; it now audits 437 quotes in 27 papers and flags 115 as not verbatim in the current PDFs (most in Woelfle 14, Lou 8, Wrightson 7, Alharbi 7). Some are page-spanning or table text, some follow the November version changes; they need a human look.
- **`link_eps_to_ques.py` would have deleted the `### Cross-paper patterns` section from 27 question pages** (same link-format cause, 0 links found). Fixed, and it now refuses to write when it finds no links. 72 links found.
- Same regex fixed in `reverse_links.py`, `find_redundancies.py`, `cvt_screenshot_pipeline.py`, `quote_pipeline.py`.
- `keyword_freq_check.py` looked for old PDF file names and wrote to a temporary folder; now resolves PDFs and writes to `pipeline/misc/`.
- `verbatim_audit.py` wrote its report to `/tmp`; now `pipeline/misc/evd-validation/paraphrase_report.tsv`.
- `pangram_check.py` now reads the key from `~/.config/lives-ai-raters/.env`.

## Still unsafe or noisy to run on the real vault (they ran, but change pages)
| Script | What it would change in the copy |
|---|---|
| `reverse_links.py` | rewrites the "EVDs from the cited papers" block of 31 claim pages (wording and link format differ from the vault's current text); do not run until the script's template matches the vault |
| `readability_pass.py` | adds blank `>` lines to about 100 pages (cosmetic, idempotent) |
| `build_dgraph.py` | regenerates `dgraph.md` and resets its frontmatter (`human_verified`, `prompt_source`) |
| `add_tldr_callouts.py` | adds a TL;DR to 6 source pages that lack one (intended) |

## Full table
| Script | Exit | Seconds | Changed | Last output line |
|---|---|---|---|---|
| add_tldr_callouts.py  | 0 | 0.2 | 6 | 6/26 files updated. |
| build_dgraph.py  | 0 | 0.2 | 1 |   49 caveats |
| count_evds_per_subtask.py  | 0 | 0.2 | 0 | EVD counts per subtask: |
| cvt_screenshot_pipeline.py  | 0 | 0.4 | 0 | Total: 0 CVTs touched, 0 crops added, 0 failures |
| find_redundancies.py  | 0 | 0.2 | 0 |     CVT - Roberts study tested only GPT-3.5 |
| link_eps_to_ques.py  | 0 | 0.2 | 1 | Total QUE↔EP links: 72 |
| readability_pass.py  | 0 | 0.2 | 103 | Total: 103 files updated |
| reverse_links.py  | 0 | 0.2 | 108 | Updated 31 CLMs with reverse links. |
| verbatim_audit.py  | 0 | 55.0 | 1 |     quote: "LLM has the potential to give meaningful scores and decide on individual statements. However, they |
| quote_pipeline.py  | 1 | 0.2 | 0 | RETIRED (Skill v2): use pdf_pages.py (find, crop) and audit_signal_quotes.py / verbatim_audit.py. Pass --force |
| extract_quotes.py  | 0 | 0.3 | 0 | OK	t	page=9	first='we'	last='doctor.'	file=@akyonEvaluatingCapabilitiesGenerative2024-t.png |
| check_quality_signals.py  | 0 | 0.2 | 0 | 0 source page(s) with missing signals |
| audit_signal_quotes.py  | 0 | 0.2 | 0 | sources without PDF: [] |
| signals_decision_models.py  | 0 | 0.5 | 0 | 3 calls (0 errors); records in /Users/ppatel/.claude/jobs/675f3ea2/tmp/vault-copy/_smoke_out/dm.jsonl |
| signals_to_gsheet.py  | 0 | 0.4 | 0 | saved /Users/ppatel/.claude/jobs/675f3ea2/tmp/vault-copy/_smoke_out/review.xlsx {'TRIPOD-LLM': 42, 'Quality ap |
| vault_to_gsheet.py  | 0 | 0.5 | 0 | rows: SRC 27 QUE 27 CLM 31 EP 21 EVD 77 CVT 49 PICOST 77 SCREENING 27 |
| pdf_pages.py map | 0 | 0.3 | 0 | 30 30 pdf-position |
| pdf_pages.py find | 0 | 0.4 | 0 | found [(9, '9')] |
| pdf_pages.py crop | 0 | 0.3 | 0 | {'ok': True, 'pdf_page': 9, 'out': '/Users/ppatel/.claude/jobs/675f3ea2/tmp/vault-copy/_smoke_out/c.png', 'siz |
| pdf_pages.py links | 0 | 0.3 | 0 | 30 http://www.tcpdf.org |
| keyword_freq_check.py  | 0 | 2.8 | 1 | Processed 27 of 27 papers |
| pangram_check.py  | 1 | 0.3 | 0 | PANGRAM_API_KEY is not set in the environment. |
| provenance/openalex.py  | 0 | 0.8 | 0 | } |
| provenance/doaj.py  | 0 | 0.5 | 0 | } |
| provenance/opencitations.py  | 0 | 1.1 | 0 | } |
| provenance/pubpeer.py  | 0 | 0.5 | 0 | } |
| provenance/howfairis_check.py  | 0 | 2.1 | 0 | } |
| provenance/fair_checker.py  | 0 | 11.2 | 0 | } |
| provenance/run_provenance.py  | 0 | 1.7 | 0 | } |

Provenance scripts, on the Akyon paper: licence, open-access status, publication type, DOAJ listing, OpenCitations count (10) and PubPeer comment count (0) match the vault page. OpenAlex's retraction check matched a 2015 retracted clinical paper to an author id (probably a namesake), so the script now reports "needs human check" instead of a track record. Self-citation rate differs from the vault (0.023 on 43 of 44 references against 0.000 on 1 of 34): OpenAlex has fuller reference metadata. PubPeer's endpoint is the browser extension's, not a documented API.

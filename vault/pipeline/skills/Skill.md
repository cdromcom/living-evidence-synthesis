---
name: extract-discourse-nodes
description: Extract a full set of discourse graph nodes from a scientific paper PDF — Questions (QUE), Claims (CLM), Evidence (EVD), and Caveats (CVT) — for a given research question. Outputs structured Obsidian-compatible markdown files with embedded figure/table screenshots and quote-region screenshots.
argument-hint: <path-to-pdf> for <research-question-or-link>
allowed-tools: Read, Write, Bash, Glob, Grep
---
You are extracting a complete set of discourse graph nodes from scientific papers given to you as PDFs. The five node types together map the paper's argumentative structure: what was asked (QUE), what was found (EVD), what it means (CLM), where to be cautious (CVT), and which regularities span ≥2 papers (EP).

## Workflow at a glance (v2)

For one paper, in order (details in Step 1 and the steps below):

1. **Pick and parse:** most recent version of the paper; Gemini 4 Neon reads the PDF and the PDF text layer is the second read (Step 1).
2. **PICOST first:** one record per finding, sorted into primary, secondary and tertiary tiers against the research question, with locators and spotlighted source spans; sources by section (Results for EVDs, Discussion for CVTs and CLMs, Introduction for QUEs).
3. **Check the extractions before anything is written:** PyMuPDF finds every quoted span; the decision models gate relevancy, fidelity, quote grounding and table or figure grounding; low-confidence and multi-page extractions are re-read by GPT-6.2 Sol and adjudicated by Opus 5.5; JP spot check A (Steps 1 and 6e).
4. **Identify nodes** with atomicity and the QUE rules (Step 2); **write the nodes by debate** (Sonnet 5.5, Sol and Neon draft, critique and revise; Sol and Sonnet vote; linted for length, readability and numbers) from the PICOST records (Step 4, `Skill-templates.md`).
5. **Highlight, box and crop** with PyMuPDF and `pdftoppm` (bounding boxes from the span search); GPT-6.2 Sol checks every crop, Opus 5.5 checks multi-page crops (Step 3).
6. **Automatic audits** (verbatim quotes, numbers on the PICOST record, page map), reverse links, formatting, NodeFormality, DGRAPH regeneration, history log (Steps 5 to 10, `Skill-templates.md`).
7. **Mirror to the review sheet** and **JP spot check B**; merge through a pull request and regenerate the graph data.
8. **Provenance footer** on every page written or changed (Step 4c): model and version, date accessed, prompt link, run id, human-check status, from the call log.

**Not in this run:** quality signals (TRIPOD-LLM and quality appraisal tables, provenance fields, tool checks) are the separate optional **Module Q**, run only on JP's command, so extraction and publishing never spend credits on signals.

Work in **batches of four papers at most** (hard limit in `pipeline/scripts/lives_run.py`, JP 2026-11-25) with the human checks, the cost controls and the ledger below. Cross-paper synthesis (EvidencePatterns, Review-Arena), the public MkDocs render and the ESS Bases are in `Skill-synthesis.md` (Steps 11 to 14), run after a batch, not per paper.

## Vault structure (summary)

The vault has two parent folders: `sysrev/` (the systematic-review content) and `pipeline/` (how the review is built and published). The folders are `sysrev/dgraph/questions/` (QUE), `sysrev/dgraph/claims/` (CLM), `sysrev/dgraph/evidence/` (EVD), `sysrev/dgraph/caveats/` (CVT), `sysrev/dgraph/source/` (SRC notes `@citekey.md`; PDFs in `sysrev/dgraph/source/pdfs/`, older versions in `sysrev/dgraph/source/pdfs/Archive - superseded versions/`), `sysrev/dgraph/evd-patterns/` (EP) and `sysrev/picost/` (PICOST JSON), plus `pipeline/templates/`, `pipeline/scripts/`, `pipeline/misc/` (audits, prompts, validation work), `pipeline/public/` (MkDocs site) and the folders `pipeline/skills/` (this Skill system, `Tools-and-Models.md`, `Vault-structure.md`), `sysrev/indexes/` (`dgraph.md`, `DGRAPH-TABLE.md`, `Review-Arena.md`, `ESS - Demo.md`, `ESS.base`, `EvidencePattern Nodes.base`), `pipeline/logs/` (`History.md`, `Log.md`), `pipeline/legal/` (`LICENSE-CONTENT.md`, `PERMISSIONS.md`) and `sysrev/reference/` (`BenchmarkLLM.md`, `Class-Imbalance-Text-Classification.md`, `paraphrase_audit_<date>.tsv`); `Welcome.md` is the only file at the vault root. Screenshots live in `sysrev/dgraph/evidence/Attachments/`. The full tree and file-format notes are in `Vault-structure.md`.

## Node Types and Their Roles

| Type             | Prefix | Role                                                | Grounding                                        |
| ---------------- | ------ | --------------------------------------------------- | ------------------------------------------------ |
| Question         | `QUE`  | Research questions the paper addresses              | Author's stated aims + inferred framing          |
| Evidence         | `EVD`  | Atomic empirical observations from data             | Direct quotes + figure/table + quote screenshots |
| Claim            | `CLM`  | Generalizations from EVDs (results)                 | Direct quotes that state what findings mean      |
| Caveat           | `CVT`  | Methodological limitations on EVDs                  | Author-stated or inferred; flagged accordingly   |
| EvidencePattern  | `EP`   | Cross-paper empirical regularities bundling 2+ EVDs | Wikilinks to constituent EVDs + cross-paper triangulation argument |

**Critical distinction — CLM vs. EVD:**
- EVD = *what was measured/observed* (e.g., "GPT-4 detected errors in 7 of 13 papers")
- CLM = *which generalization emerges from EVDs* (e.g., "LLMs are approximately as accurate as human experts at verifying adherence to reporting guidelines like GRADE risk of bias 2 (RoB 2).")
- Numbers and observations → EVD. Conclusions drawn from them → CLM.

**Critical distinction — CLM vs. CVT:**
- CLM = an affirmative generalization that the paper argues for using one or more EVDs
- CVT = a limitation that constrains what inferences can be drawn from EVDs to CLMs. Should be drawn from consensus, ideally empirically grounded, methodological best practices for a given method (e.g., "lack of prompt/context engineering" for an EVD that involves use of LLMs, or "violation of stable unit treatment value assumption" for a randomized controlled experiment)

---

## Setup before a run

- **Vault location:** scripts use the folder two levels above `pipeline/scripts/`; set `LIVES_VAULT=/path/to/vault` to override.
- **Model origin (JP, 2026-11-25):** hosted APIs only from US developers (never send data to a foreign provider's API or hosted endpoint); open-weight models from any country may run **locally** if they are state of the art or close to it for the task. Record developer, country, base model, licence and the date checked (see `Tools-and-Models.md`, "Model-origin policy").
- **API keys** go in `~/.config/lives-ai-raters/.env` (never in chat or the repo): `OPENAI_API_KEY` (PDF reading with GPT-6.2 Sol), `GEMINI_API_KEY` (Gemini 4 Neon, Project ENIGMA; spending limit set to the $100 loaded), `ANTHROPIC_API_KEY` (Claude Opus 5.5 and Sonnet 5.5), `PERPLEXITY_API_KEY`, `LIQUID_API_KEY`, `TYPESAFE_API_KEY` (Jev), `TINKER_API_KEY` (Inkling 2 Small), and `PANGRAM_API_KEY` (AI-writing check; use only on JP's command, planned December or January). All of these except the Pangram key were present in `.env` on 2026-11-25; JP added the Pangram key afterwards (confirm before use).
- **Scripts:** the one canonical folder is `pipeline/scripts/`. The older copies are in `pipeline/misc/scripts-superseded/` and use the old folder layout; do not run them.

## Inputs

The user will provide:
1. **A PDF path** (or a list of paths for a batch) — put new PDFs in `sysrev/dgraph/source/pdfs/` (gitignored, so PDFs stay local). Older versions go to `sysrev/dgraph/source/pdfs/Archive - superseded versions/`
2. **A research question** — either inline text or a `[[QUE - ...]]` link. If a link, read it for context.
3. **An output directory** — default: the vault itself. Nodes go to `sysrev/dgraph/<type>/` (questions, claims, evidence, caveats, source, evd-patterns); never write next to the PDF.

---

## Step 1: Read the Paper

### v2 process (2026-11-24): parse, then PICOST first

> [!info] Why
> The 2026-11-17 audit of the 77 EVD pages found 147 suspected errors (wrong numbers 49, claims not in the paper 33, paper contradicting itself 19, wrong page 18, wrong model or rater 17, missing comparator 8, row or column shift 3). Every one of them passed the quote check. The steps below add the controls that were missing. Tool and model choices are in `Tools-and-Models.md` (v2 section).

1. **Parse with two independent reads.** (a) **Gemini 4 Neon** (`gemini-4-neon`, PDF input; thinking level High) reads the PDF directly (PDF input; reasoning effort High) and returns the PICOST records of item 4 directly, with the printed and PDF page of every number and verbatim spans (the runner does not ask for a full page-by-page transcript, which costs many output tokens; the page map comes from PyMuPDF, and a full transcript with HTML tables is requested only for scanned pages). (b) The PDF's own text layer with PyMuPDF for born-digital PDFs. Accept text, numbers and table cells only where the two agree. Where they disagree, or a page has no text layer, decide from the **rendered page image** (`pdftoppm -r 150 -f N -l N -png`), by GPT-6.2 Sol and Opus 5.5 or a human; never from either extraction alone. Do not use `pdftotext -layout` for tables. (2026-11-25: Gemini 4 Neon is the primary reader again, now that JP has a paid Google key in Project ENIGMA and a test call worked; GPT-6.2 Sol is the independent second reader for low-confidence and multi-page items. Keep LlamaParse as the fallback if both misread tables in the pilot.)
2. **Page map, built once per paper.** Record for every page both the PDF page position and the **printed journal page** (PyMuPDF page labels first, otherwise the number printed in the header or footer; mark preprints without printed numbers "PDF position only"). Every citation uses the printed page.
3. **Send Methods and Results first** (with their tables), and other sections only when a field is missing.
4. **PICOST first.** For each candidate finding write one record as JSON: Population, Intervention, Comparator, Outcome, Study design, Timeframe, the finding in one sentence, and every number. **Every number and every PICOST value carries a locator**: journal page, table or figure, row label, column label. Anything the paper does not state is `Not reported`; never fill a slot with plausible standard detail. The bulk extraction model is **Gemini 4 Neon** at thinking level High (Medium or Low for simple steps such as restyling, alt text and link repair; its thinking tokens are billed as output, so set the level per step). **Low-confidence and multi-page extractions** (a confidence flag from Neon or a decision model, a parser disagreement, or a table, figure or finding that spans pages) are re-extracted independently by **GPT-6.2 Sol** and adjudicated by **Opus 5.5**; unresolved ones go to JP. Neon's quality on our papers is unmeasured, so the pilot compares it with Sol and Opus (TODO).
5. **Reconcile prose against tables.** When the text and the paper's own table disagree, use the table and record the disagreement in a note (`- PDF check <date>: ...`); never edit the quote.
6. **Check the whole table before "best".** Before any EVD says best, beat, matched or highest, read every row of the table and list every comparator that could change the claim (other models, human baselines, combined methods).
7. **QA gate before any node is written (Step 6e).** Every PICOST record passes four checks: (1) PyMuPDF finds each verbatim span and returns its bounding box; (2) the decision models answer the relevancy, fidelity, quote-grounding and table or figure grounding questions (Step 6e); (3) a record that is low-confidence or multi-page gets the Sol re-extraction and the Opus adjudication; (4) a human spot check. Until the decision-model thresholds are calibrated (shadow mode, JP 2026-11-24), the checks in (3) also run on every record flagged by a parser disagreement plus a 10% random sample.
8. **Write the EVD from the PICOST cells.** The EVD statement may contain only numbers that appear in its PICOST record, so the statement, the PICOST row and the screenshot agree.
8a. **Where to look first (JP, 2026-11-24).** EVD content from the **Results** section before any other section; CVTs (caveats) and CLMs (claims) from the **Discussion** (and Limitations) before other sections; QUEs from the **Introduction** (and stated objectives). Fall back to other sections (Abstract, Methods, Conclusion, supplements) only when the preferred section does not give the item, and say in the PICOST record which section each value came from (`section`).
8b. **Spotlight the passages (accuracy aid).** For each finding Gemini 4 Neon returns the verbatim span(s) that support it (text and printed page), not coordinates. PyMuPDF then searches for each span in the PDF (exact match after normalising hyphenation and quote marks), which returns the span's **bounding box**, draws a highlight and a box on the rendered page and saves it as a PNG under `work/<citekey>/highlights/`; the box is also what the crop step uses and is stored with the locator (page, x0, y0, x1, y1). A span PyMuPDF cannot find is a flag (the model paraphrased or misread), and the finding goes back for a fix before anyone writes from it. Humans and Opus 5.5 look at the highlighted page, not the raw PDF.
9. **Work from the most recent report (JP, 2026-11-24).** Prefer the published journal or proceedings version over a preprint, and the latest preprint version over earlier ones; keep the older PDF as `Archive - ...` in `sysrev/dgraph/source/pdfs/Archive - superseded versions/`, and cite the printed page of the version used. Do not silently move an existing page to a newer version: list it for JP (TODO 0d).
10. **Fix page-number errors when you find them (JP, 2026-11-24).** Whenever any step turns up a wrong page citation (printed versus PDF page, a quote that is not on the cited page), correct the citation in both the local vault and the repository copy, add the old and new value to the page's `PDF check` note, and log it; do not wait for a separate audit. Cite the version of the paper the page was built from (a version question goes to TODO 0d).
11a. **Batch runner (JP, 2026-11-25; `pipeline/scripts/lives_run.py`, `llm_batch.py`).** One command takes one to four PDFs and runs: Gemini 4 Neon extracts PICOST (`prompts/picost-v1.md`); PyMuPDF finds every span, boxes and highlights it and flags low-confidence, multi-page, scanned, not-found and number-not-on-page items; GPT-6.2 Sol re-extracts the flagged findings without seeing Neon's values (`recheck-v1.md`); Claude Opus 5.5 adjudicates disagreements from the PDF (`adjudicate-v1.md`); then it stops at `awaiting_spot_check_a` with a `review.md` per paper. `--mode standard` answers now at full price (pilots); `--mode batch` uses Anthropic Message Batches, OpenAI Batch and the Gemini Batch API at about half price and polls until they finish (`--resume RUN_ID` picks a submitted job up again). Inkling 2 Small has no batch mode and runs in parallel instead. **Rails:** refuses more than four PDFs, a cap above $5.55, and a PDF already processed (same SHA-256; `--allow-repeat`). Before each stage the worst-case cost is added to the spend so far and the run stops before submitting if that would pass the cap. **Stop-the-batch rules:** spend over the cap; a stage costing over 1.5 times its expected cost; two or more papers failing; over 25% of a paper's spans not found in its PDF; a `STOP` file in the run folder (`touch pipeline/runs/<run>/STOP`). A stop cancels any batch job still running. Every run writes `pipeline/runs/<run>/manifest.json` (models, prompt and script hashes, package versions, per-paper SHA-256, per-stage tokens, cost, job ids, events) and the call log. The cap covers calls made by the runner; set a monthly limit on the Google and OpenAI projects as a second fence. Budgets follow the 27 seed papers (`Tools-and-Models.md`, "Token budgets"). **Evidence tiers (JP, 2026-11-25; `prompts/picost-v3.md`, spec in `pipeline/templates/T - EVD tiers.md`):** the runner needs the research question (`--question`); extraction labels each finding **primary** (answers the RQ), **secondary** (meta or contextual about a primary finding, with `supports`) or **tertiary** (other context), with first-guess caps of 6, 4 and 2 per paper (the seeds have 1 to 6 EVDs each) and an `omitted` note per tier; JP's pilot sets the caps. The output budget grows with the page count (max 64,000) and Sol and Opus read only the cited pages. `run_to_gsheet.py RUN_ID` builds the step-by-step review sheet (`Review-sheets-spec.md`). Node writing and the decision-model gates are not in the runner yet.
11. **Batch API for unattended runs, on every provider (once the process is reviewed).** Gemini 4 Neon runs through the Gemini Batch API at about half price ($1.50 in and $7.50 out per million tokens, from third-party pages; confirm on Google's pricing page). Run bulk steps (reading, PICOST extraction, drafting, verification) through each provider's Batch API: Anthropic Message Batches (50% off, stacks with prompt caching), OpenAI Batch (about half price; GPT-6.2 Sol $1 in and $5 out per million tokens, from third-party pages, to confirm on OpenAI's pricing page) and the Gemini Batch API above. Put the Skill instructions first and unchanged in every request so they are cached. Use the standard API only for pilots and when someone is waiting. Decision models such as d1-ultra have no batch mode and cost too little to matter. Log tokens, cost and time per paper and step.

Question rules for the QUEs you propose here are in Step 2 and in `Skill-templates.md` (QUE title phrasing rule, rules 1 to 12; keep each QUE's original wording as a quote).

### Outputs JP reads (v2, 2026-11-24)

JP reads and judges accuracy in a Google Sheet, not in markdown; Obsidian markdown stays the source of truth but should not dominate the human reading experience. For every batch of papers:
1. Write one PICOST file per EVD to `sysrev/picost/<EVD-id>.json` (schema in `sysrev/picost/SCHEMA.md`; every number and value carries a locator; `Not reported` when the paper is silent).
2. Rebuild the review mirror with `pipeline/scripts/vault_to_gsheet.py` and upload it as the Google Sheet "LIVES vault mirror (JP review)" (tabs SRC, QUE, CLM, EP, EVD, CVT, PICOST, SCREENING, each with JP accuracy-judgment dropdowns and a Notes column; screenshots as image formulas). JP judges there; apply his judgments back to the markdown only with his approval.
3. Paper screening (Include or Exclude) is recorded on the SCREENING tab; decision-model screening uses JP's labelled sets and keeps recall near 100%.

### Run records and reasoning traces (JP, 2026-11-24)

Save a complete record of every model call, so the work is reproducible and, later, usable as training data for open-weight models. For each call write one JSON line to `pipeline/runs/<batch>/<citekey>/calls.jsonl` (kept out of git by default because it holds paper text and screenshots; the folder has its own README):
- `model` (exact id and version), `provider`, `date`, `effort`, `temperature` if any, `prompt_hash` and a pointer to the prompt file, `inputs` (file paths and page numbers, not copies of paper text), the `output`, `usage` (input, cached, reasoning and output tokens, cost, latency), and the step name (read, extract, draft, vote, check, crop QA, decision-model check);
- the **reasoning trace exactly as the provider returns it**: Gemini thought summaries (and the thought-token count) for Gemini 4 Neon; Claude extended-thinking blocks when enabled for Opus 5.5 and Sonnet 5.5 (store them verbatim, including whether the provider marks them summarized); GPT-6.2 Sol reasoning summaries (the API does not return raw reasoning; record the summary and the reasoning-token count); Inkling 2 on Tinker, the full text it generates; decision models (d1-ultra, Perplexity Decider, Jev) return calibrated probabilities and no trace, so store the probabilities. Never invent or reconstruct a trace; write `null` when the provider returns none;
- the **human verdict** when one exists (JP's judgments from spot checks A and B and the mirror sheet), linked by EVD id, so each trace can be filtered to verified-correct outputs.

**Before using any trace for training:** check each provider's terms. Anthropic's and OpenAI's terms restrict using their model outputs to develop competing models, so the proprietary traces are an audit and analysis record until the terms are checked or permission is obtained. Safe sources for an open-weight training set are Inkling 2 traces (open model), JP's own verified judgments and edits, the PICOST records and final texts JP has approved, and the decision-model probabilities. Paper text and screenshots stay under their source licences (`legal/PERMISSIONS.md`); share training data only for papers whose licence allows it.

### Cost controls (v2, 2026-11-24)

Follow these every run so JP does not have to remember them. Budget, per-batch caps and the ledger are in `pipeline/misc/evd-validation/2026-11-24-ingest-budget-and-batches.md`.

1. **Work four papers at a time at most (JP, 2026-11-25)** with the human spot checks A and B in that file. `lives_run.py` enforces it, together with a **$5.55 cap per batch** and the stop-the-batch rules (see "Batch runner" under Step 1, item 11a).
2. **Standard API for the first three papers, then iterate on the prompts; switch to the Batch APIs only after an external reviewer has given feedback** (JP, 2026-11-24). Batch is about half price and suits runs nobody is waiting on (reading, extraction, writing, verification).
3. **Cache the Skill:** put the Skill and instructions first and unchanged in every request.
4. **Send only what is needed:** Methods and Results with their tables first; skip references, appendices and acknowledgements; fall back to other sections only when a field is missing.
5. **Use the free second read:** the PDF text layer is the second vote; send page images to the model only for pages with tables or figures.
6. **Escalate by exception:** Opus 5.5 only where the two reads disagree, plus a 10% random sample, not on every record.
7. **Short structured output:** PICOST as compact JSON; GPT-6.2 Sol at High for reading and extraction, Medium for restyling, alt text and link repair; never Max unless a pilot shows it removes errors High leaves.
8. **Screen before reading:** remove duplicates and off-topic papers with a cheap relevance call (Perplexity Decider 1.3 or Liquid d1-ultra) before the full read.
9. **Pilot, then reuse:** fix the prompts on four papers, save every step's output, and resume instead of rerunning.
10. **Describe screenshots in one batch call** at Medium; skip alt text for purely decorative crops.
11. **Log tokens and dollars per paper and step** in the ledger and keep a hard spending cap on each provider account.

## Step 2: Identify All Nodes

Produce a node inventory before writing any files.

> [!tip] Questions (v2)
> Apply rules 1 to 12 of the QUE title phrasing rule in `Skill-templates.md`: one construct per question, no yes/no, neutral "LLMs" and "research reports", do not mirror the authors' wording, generalize beyond the sample, name the template used, and keep the original wording as a `### Original wording` quote on every QUE (split questions keep the full compound wording in each part).

**Questions (QUE):** What is the main research question? Are there sub-questions (different tasks, analytical angles, or comparisons)? Each distinct research question = one QUE node. Phrase every QUE title per the **QUE title phrasing rule** in `Skill-templates.md` (canonical template table, "LLMs"/"research reports" as subject/object, degree framing, splitting compound questions) — check the template table before coining a new phrasing.

> [!tip] EVD statements (v2)
> Write each EVD title and Description line in the Phase 2 style (`Skill-templates.md`, "EVD statement (headline) style"): named models, N and field, comparator, spelled-out statistics in parentheses, at most 247 characters, built from the PICOST cells. Ground every table, figure and design detail in Methods Context, SRC pages and other nodes with a quote and a crop ("Provenance for tables and figures everywhere").

**Evidence (EVD):** Each distinct statistical test, empirical observation, or analytical finding = one EVD. Do NOT collapse multiple findings into one. Atomicity is essential. Every EVD (and every CLM/EP downstream of one) must also carry a **`task/<slug>` tag** naming which evaluative task the finding is *about* — e.g. `task/risk-of-bias-assessment`, `task/novelty-assessment` — distinct from and in addition to any `5c/*` or `appraisal/*` tags. This answers "what does this finding say about LLM performance on X" as opposed to "how trustworthy is this study," a distinction an advisor flagged in 2026-08 as missing from the corpus. The full 16-value taxonomy (grouped under the 5 Cs plus a "Cross-cutting" bucket for findings about the evaluator's general behavior — prompt sensitivity, cost, fine-tuning — rather than one task) lives in `living-synthesis-site`'s `lib/data.ts` (`TASK_ORDER`/`TASK_LABELS`/`TASK_GROUPS`) and drives that site's graph-view "Evaluative task" filter; check there for the current value list and add a new value (in both this doc and that file) only when an existing one genuinely doesn't fit, rather than inventing a near-duplicate.

**Claims (CLM):** Which generalizations from their data/EVDs do the authors draw? Each distinct conclusion = one CLM. Must be traceable to at least one EVD or direct author quote.

**Caveats (CVT):** Which limitations do the authors explicitly state? What limitations can you infer from the methods (e.g., no pre-registration, small N, convenience sample, single model tested, GUI instead of API prompting)? Each distinct limitation = one CVT.

CVT nodes capture a single methodological limitation. They are organized around which papers the limitation applies to.

**Notes on CVT Properties:**
- The `title` field IS the node identifier — it must include `[[CVT]]` literally
- `type: author-stated` = the authors themselves named this limitation; use a direct quote
- `type: inferred` = you identified this as a limitation based on methodological reasoning; the quote should be the closest relevant passage (e.g., the methods description that reveals the gap), and add a brief explanation in brackets after the quote: `[Inferred: this is a limitation because...]`
- `appliesTo`: link to the EVD or CLM nodes whose validity is most affected by this caveat
- CVT titles should be short but specific sentences in past tense — not just `CVT - small sample` but `CVT - The small sample limited generalizability.`
- CVTs can only be paper-specific and MUST apply to specific EVDs

**Naming:** `CVT - [short description of limitation].md`

Examples:
- `CVT - The small sample limited generalizability.md`
- `CVT - The models were only tested via GUI not API.md`
- `CVT - The paper did not include inter-rater reliability.md`
- `CVT - The data leakage problem from training corpus was not resolved.md`

---

## Step 3: Extract Screenshots (figures, tables, and quote regions)

Two kinds of screenshots ground a node: **figure/table images** for EVDs, and **quote region crops** for every direct quote embedded in any node. Both go into a single `attachments/` subdirectory in the output directory. Embed in Obsidian with `![[filename.png]]`.

### 3a-3b. Screenshots: what is needed

- **Quote crop** for every direct quote in an EVD, CLM, CVT or QUE: the whole quote inside the crop (never clip the closing words), highlighted in the node colour (EVD light red `(1.00, 0.70, 0.70)`, CLM light green `(0.72, 1.00, 0.72)`, QUE light blue `(0.72, 0.86, 1.00)`, CVT light gold `(1.00, 0.90, 0.55)`); filenames `<citekey>-{evd|clm|cvt|que}-p<N>-<idx>.png`, embedded under the quote.
- **Table or figure crop** for every EVD whose numbers come from one, and for Methods tables and diagrams: item plus caption only (3c).
- Locate quotes with the exact-span search in 3c; the old three-pass `pipeline/scripts/quote_pipeline.py` path is retired (it hard-codes paths and imports a missing module; see `pipeline/misc/skill-backups/2026-11-24-pre-cuts/Skill.md` for the old text).

### 3c. Cropping, highlighting and page numbers (v2)

- **Crop with coordinates, then verify.** Locate each quote or table with PyMuPDF word coordinates (not `pdftotext -bbox` alone), crop with `pdftoppm -x -y -W -H`, and re-run text search on the cropped image's OCR or on the crop region to confirm the whole quote is inside the crop. Reject a crop whose first or last word is cut off.
- **Highlight color by node type: light pastels, easy on the eyes** (JP, 2026-11-25). QUE light orange, EVD light red, CLM light green (a mint, not lime), EP light blue, CVT soft gray. `pdf_pages.py crop --kind <TYPE>` applies them (values in `HIGHLIGHT`). No saturated yellow or neon.
- **Screenshots are closed by default** (JP, 2026-11-25). A page shows each screenshot as a small neutral placeholder (a labelled rectangle with the page and what it shows); the reader clicks or presses Enter to open it, and can close it again. Large white rectangles open on every page are an aesthetic problem. In the vault write the image inside a collapsed callout (`> [!example]- Screenshot: <what it shows>, p. N`); in the web app use a `<details>` or a button-controlled region, with the alt text already in place.
- **Table and figure crops** contain the table or figure and its caption only, every row, column and panel, no body text (see the grounding rules in `Skill-templates.md`). Do not screenshot the full page. Methods tables and method diagrams are cropped and embedded the same way.
- **Preflight per paper (nip problems early).** Before extracting, check the PDF: born-digital or scanned, one or two columns, text-layer quality (ligatures, odd font encodings, missing spaces), math-heavy, tables as vector text or as images, page labels. Pick the path from the result and record it in `work/<citekey>/preflight.json`; a scanned or poor-text paper starts on the OCR path below.
- **If PyMuPDF cannot find or crop something (fallback ladder; never ship an unverified crop):** (1) retry with stronger normalisation (ligatures, hyphenation, Unicode, quote marks, soft line breaks) and n-gram or fuzzy matching on 8-word windows; (2) search line by line and per column, then stitch the pieces; (3) cross-check with a second extractor (`pdfplumber` or `pdftotext -bbox-layout`) and take the box where the two agree; (4) for tables and figures, snap to PyMuPDF `find_tables()`, image blocks and the caption line, with Sol proposing an approximate box from the rendered page that PyMuPDF refines to the nearest text blocks; (5) OCR the page image and match the quote in the OCR text; (6) flag for JP with the page image. Every crop that passes goes through the Sol crop QA above.

- **Cross-check against the audit.** Compare each cropped table against the structured cells from Step 1 (two-tool agreement) before the screenshot is accepted: a mismatched row or column shift is the audit's error type 7, a value next to the wrong label is type 5.
- **Printed page in every citation.** Use the page map from Step 1. The screenshot filename may keep the PDF index (`p6`); the citation may not. If the paper has no printed numbers (typical for preprints), or a page prints none, use the PDF page number and write `PDF p. N` so a reader knows; this is correct, not an error (JP, 2026-11-25), and `audit_signal_quotes.py` accepts it.
- **Crop QA before any human sees a screenshot (JP, 2026-11-24).** GPT-6.2 Sol (vision, High) inspects every crop against a checklist and returns pass or fail with a reason: (1) it is the item the node cites (the quoted passage, or the table or figure whose numbers the EVD uses); (2) quote crops show every word, first and last lines not cut off; (3) table or figure crops show the item and its caption only, all rows, columns and panels, no body text, no neighbouring item, no page header; (4) legible and not blurred; (5) the cited printed page matches the page shown. Only passes go to the mirror sheet; a fail is re-cropped (up to two retries) and then flagged. **Any crop built from more than one page or column** (stitched pieces, whited-out words) is also verified by Opus 5.5 for accuracy and cleanliness: correct order, no duplicated or missing lines, no visible seams or leftover fragments, still reads as one clean figure. Record the verdicts in `work/<citekey>/crop-qa.json`.
- **Alt text.** Add each screenshot's description to the alt-text map; the filename is never the alt text.

## Step 4: Write the Node Files → see `Skill-templates.md`

### Drafting by debate: EVD, QUE, CLM, EP and CVT (JP, 2026-11-25; replaces the 2026-11-24 EVD writing loop)

Little things matter (a number, a comparator, 247 characters, a sentence a reader can follow), so three models draft, critique each other, revise and vote. Nothing here has been piloted: the first batch with JP decides what stays (`TODO.md`).

**Roles.** Authors: **Claude Sonnet 5.5**, **GPT-6.2 Sol** and **Gemini 4 Neon at Medium thinking** (extraction stays at High). Deciders: **Sol and Sonnet vote** (cheaper than Opus). Tie-break: **Neon**. **Inkling 2 Small** also picks, in parallel, **for benchmarking only**: its pick is logged and never counted. **Opus 5.5** is the escalation when a gate fails twice or a claim cannot be settled. The decision models gate fidelity and grounding.

**Steps (all logged).**
1. **Lint (free, deterministic), per node type.** EVD: at most 247 characters; every number, model name and comparator is on the PICOST card; metrics spelled out; readability grade (Flesch-Kincaid) about 12 or lower, flag above 14. QUE: the question rules 1 to 12. CLM: the claim is a direct quote or a faithful restatement of one. EP: the evidence threshold. CVT: the limitation, supporting quote and applies-to fields. Lint runs after every draft and revision.
2. **Round 0, in parallel.** Each author drafts from the same input: the PICOST card (with the spans and the RQ), the finding's tier, and the three examples in `Skill-templates.md`.
3. **Round 1: critique and revise.** Each author sees all drafts (anonymous, shuffled) and the lint results, and returns (a) a critique of every draft on accuracy, completeness, length, readability and little things, each point tied to a card field or a span, and (b) its own revised draft.
4. **Round 2, only if needed.** If the revised drafts still differ on a number, a comparator or a claim, or lint fails, one more critique and revision round. Never more than two rounds.
5. **Vote.** Sol and Sonnet each pick the best revised draft (anonymous), with reasons. If they agree it wins; if not, Neon breaks the tie. Inkling's pick is recorded for the benchmark.
6. **Check.** The cheaper of Sol and Sonnet that did not write the winner checks each claim against the span or crop (supported, partly supported, unsupported, with the supporting words); a decision model gives an independent fidelity answer. Any unsupported claim, or a disagreement between the two, goes to Opus 5.5, then to JP.
7. **Record.** Every draft, critique, revision, vote, lint result, check and cost is stored in the run folder and shown in the review sheet (tab "Drafts and debate"); the final text goes into the PICOST JSON (`evd_checks`) and JP judges it in the mirror sheet as usual.

**By tier.** Primary and secondary EVDs get the full loop. Tertiary EVDs get one draft, lint and the check (cheaper) until the pilot shows otherwise.

**Other node types** use the same loop with their own inputs and lints: QUE (from Introduction quotes), CLM (from Discussion claims and their supporting EVDs), EP (from the EVDs that meet the threshold across papers) and CVT (from limitations and their supporting quote). The authors, the vote and the check are the same.

**Pilot (with JP).** On the first four papers compare the loop with a single Sonnet draft: cost, JP's fidelity and style ratings, how often the three authors converge, how often Sol and Sonnet disagree, whether Inkling's pick matches the winner, and whether the second round ever changes the result.

## Step 4c: Provenance footer on every node page (required; JP, 2026-11-24)

**SRC pages are written for skimming (JP, 2026-11-25):** numbered lists for procedures, short bullets elsewhere, and each node link first, summary after (full rules in `Skill-templates.md`, "Skimmability and link order").

**Screenshots over a page break (JP, 2026-11-25):** use `pdf_pages.merge_regions(pdf, [(page, [rects]), ...], out)`: one image with the pieces stacked top to bottom, each snapped to the gap between text lines and separated by 10 px of white, so the join reads as continuous. The runner saves one for every finding whose evidence crosses a page (`highlights/<id>_merged_p<pages>.png`).

Every page the Skill writes or changes (QUE, CLM, EVD, CVT, SRC, EP) ends with a clean, collapsed **AI-use footer** so a reader can see how the sausage was made. It follows the GAMER checklist (Generative Artificial intelligence tools in MEdical Research) and is generated, not typed. Closed, it shows one line: `AI use: <models> · <date> · <human-check status>`. Open (click in Obsidian; click or hover in the web app), it shows a skimmable table (step, model and version, effort, UTC time, prompt link and hash, saved response) and a role / sections / checked-by line, plus a link to `pipeline/provenance/AI-disclosure.md` (the project-wide answers to all nine GAMER items) and, for older pages, `pipeline/provenance/model-history.md`:
1. **Prompts live in the repository.** Each prompt used lives in `pipeline/prompts/<name>-v<n>.md` (or `.txt`) and is **committed and pushed before the run**, so its link resolves to a fixed version. Never edit a committed prompt in place; make `-v<n+1>`.
2. **Log every model call** with `python3 pipeline/scripts/call_logger.py log ...` (or the library functions): exact model id and display name, effort, UTC time of access, prompt file, SHA-256 and commit, tokens, estimated cost, run id.
3. **Render the block** with `python3 pipeline/scripts/call_logger.py footer --run-id <run> --node "<page title>"` and paste it as the last block of the page. Each later step that changes the page (a vote, a check, a human edit) adds a row; never overwrite earlier rows.
4. **Save the unedited response** of every call (`call_logger.py` writes it to `pipeline/runs/<run>/responses/`), because GAMER item 3 asks for it. **The block states:** step, model and version, effort, date and time accessed (UTC), a link to the exact prompt and its short hash, the run id, and the human check status (`not yet reviewed` until a person signs off, then who and when).
5. **Pages written before this rule** (all 232 today) get the legacy footer (`render_legacy_footer`) with what the vault logs record (for example "Claude Sonnet 4.6, 2026-04-17, prompt not archived"; era table in `model-history.md`) and say what is unknown. Add them after the next pipeline run, when the details have settled (JP, 2026-11-25). `scripts/file_model_history.py` lists a page's commits by era.
6. The web app renders the footer as a `<details>` element (closed by default; also opens on hover for pointer users, and on keyboard focus) at the bottom of the page; a one-line byline under the title links to it.
7. **Link, match, merge and split decisions are logged too** (rules in the next section).

## Matching, linking, merging and splitting (JP, 2026-11-25)

New nodes must fit into the graph that exists. Three models share the work, and each does what it is good at:
1. **EmbeddingGemma 2 (local, free) proposes candidates.** Run `~/.cache/lives-bench/venv-embed/bin/python pipeline/scripts/embed_candidates.py` (weights in `~/.cache/lives-bench/models/embeddinggemma-2/`). Test result on the 27-paper set: similarity is high across the board (about 215 CLM pairs at or above 0.85), because every node is about LLMs and paper review, and caveats cluster by sentence form ("limited to X, limiting generalizability"), so a fixed threshold floods the queue. Rank pairs, show difference hints (numbers, model names, negations) and use mutual nearest neighbors rather than one cutoff. It embeds every EVD of the new paper and every existing QUE and CLM, and lists the closest candidates with similarity scores. The same method proposes near-duplicates within a type (QUE with QUE, CLM with CLM, EP with EP, CVT with CVT; never across types). It decides nothing.
2. **Inkling 2 Small (on Tinker, `merge_judge.py --inkling`) and Claude Sonnet 5.5 each judge every candidate independently**, without seeing each other's answer: attach, related, or different (for matching); merge, keep separate, or group under an umbrella (for duplicates; prompt `pipeline/prompts/merge-judge-v1.md`, script `pipeline/scripts/merge_judge.py`); split or keep (for a node that mixes ideas). Each gives a one-sentence reason and what differs. First result (2026-11-25): Sonnet 5.5 recommended no merges among the top 25 CVT and top 10 QUE pairs; most were different caveats or questions that share a theme. "Group under an umbrella" is a new relation that does not exist in the graph yet; how to represent it (a parent node, a tag, or a link) is an open owner decision.
3. **The models surface; a human verifies.** Nothing is merged or split without a human's approval (JP, 2026-11-25, reversing an earlier idea of auto-merging). Inkling 2 Small and Claude Sonnet 5.5 disagreeing sends the pair to the human queue with both reasons; agreeing does not skip the human, it ranks the pair so the human sees the likely ones first. **If two nodes differ in a subtle way (a number, a named model, a dataset, a population, a direction, a negation), do not merge them.** Links (attaching an EVD to an existing QUE or CLM) need both models to agree; a human reviews a sample and every disagreement.
4. **Keep the history.** A merged node keeps the old title as an alias and records the old page; a split records both new pages and the old one. Nothing is deleted without a trace.
5. **Log the origin story of every node** in `pipeline/runs/<run>/node-history.jsonl`, one row per event: created (paper, quote, model, UTC time, prompt link), candidate proposed (similarity), each judge's verdict and reason, action taken, human review (who, when, decision). Log each model call with `call_logger.py` (step `match`, `merge` or `split`). The page footer links to the node's history.
6. **Record the pipeline overview** in the AAA Benchmarking sheet, tab "Pipeline overview (links, merges)": the decision log has one row per pair with the three decisions side by side. The agreement rate between Inkling 2 Small and Claude Sonnet 5.5 is reported per run; this is also how the project learns how a small open model compares with a frontier model.
7a. **Write path-qualified links with an alias** (`[[sysrev/dgraph/<folder>/<TYPE> - title|<TYPE> - title]]`) so they read as names, not folder paths; `python3 pipeline/scripts/add_link_aliases.py --apply` fixes any that lack one (source-paper links are left as written). The web app also shows the node name for an alias-less link, so a missing alias is cosmetic.
7. **Check structure afterwards** with `python3 pipeline/scripts/check_links.py` (both directions agree, every EVD has one source and a claim, every CLM is listed by a QUE, every EP rests on two or more papers, nothing is unlinked).
8. **Later (JP, 2026-11-25):** after Stage II EVD writing and human verification, fine-tune Inkling 2 Mini (or Small) to write QUEs, CLMs, EVDs, EPs and CVTs from verified examples (see `TODO.md`). Until then the writers are Opus 5.5 and Sonnet 5.5.

## Step 5: Build Reverse Links → see `Skill-templates.md`

Run `pipeline/scripts/reverse_links.py` to populate inbound sections (`## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence`, `### Supporting Claims (with their evidence)`). Idempotent. **Step 5b**: audit the four discourse-graph attachment invariants (CVT→EVDs only, every CLM in some QUE, every EVD in some CLM, every EVD in some QUE). Inline audit script in `Skill-templates.md`.

## Step 6: Verbatim Audit → see `Skill-templates.md`

`pipeline/scripts/verbatim_audit.py` compares every quote against its source PDF (NFKD + alnum normalization). Saves report as `sysrev/reference/paraphrase_audit_<date>.tsv`. Severity tiers (Tier 1: 0% match, Tier 2: <50%, Tier 3: 50–90%, Tier 4: >90%) and known false positives (en-dash mangling) are documented in `Skill-templates.md`.

> [!warning] The verbatim audit checks quotes only, not numbers
> Added 2026-11-17. A PDF audit of all 77 EVD pages found 147 suspected errors in numbers, tables, page references and attributions, while every quote had passed this step. Quotes passing is not evidence that a page is correct. Run Step 6b as well.

## Step 6b: Number and page checks (see Step 1 v2)

The 2026-11-17 audit found 147 errors that all passed the quote check (record: `pipeline/misc/evd-validation/2026-11-17-pdf-number-audit.md`). The Step 1 controls replace the old checklist: locators on every number, two reads, table cells from the page image, whole-table check, prose versus table, page map. Two steps stay here:
1. **Second pass by a fresh-context checker** that sees only the page and the PDF, never the drafter's reasoning; it verifies each number and proposes exact `{old, new}` fixes, and only verified fixes are applied.
2. **Propagate fixes downstream:** a corrected page is corrected in every copy (the review sheet, PICOST JSON, the repository vault that builds the site), or the pending copies are logged.

## Who checks crops and quotes (JP's question, 2026-11-25; recommendation)

Three layers, cheapest first, so accuracy stays high and cost stays low. This covers the crops and quotes behind EVDs, CLMs, CVTs and QUEs and behind every row of the TRIPOD-LLM table and the Quality Appraisal tables that feed the Quality Signals tables.
1. **Scripts (free).** The quote is in the PDF text layer verbatim (`verbatim_audit.py`); the crop's rectangle contains the quote (re-read the text inside the crop box with PyMuPDF); the box is not empty and a merged multi-page crop has every piece. This catches most errors.
2. **Decision models (cents).** Yes or no questions with the crop or passage attached: does the crop show the whole quote; does the quote support this row's rating; does the table cell show V in row R and column C. Our benchmark found about 97% on grounding questions of this kind. A "no" or a low score escalates.
3. **Vision model, only when flagged.** GPT-6.2 Sol (vision) inspects the flagged crops and a 10% random sample; Opus 5.5 only where Sol and the decision models disagree or a multi-page crop is in doubt. JP's spot check B covers a sample either way.
For the TRIPOD-LLM and Quality Appraisal rows the rating itself is decided by the majority vote of three raters (above); the checks above only verify the evidence behind it.

## Step 6e: Decision-model check of extractions (v2; pilot in shadow mode)

After the nodes and crops are extracted, the **decision models** (Liquid d1-ultra, `d1-ultra`, `api.liquid.ai/decisions/v1/systemone`, key in `~/.config/lives-ai-raters/.env`; Perplexity Decider 1.3; Jev) check each extraction at a small fraction of an Opus call. They gate four things (JP, 2026-11-25): **relevancy** (is this finding in scope for the question), **fidelity** (the statement matches its PICOST record), **grounding: quotes** and **grounding: tables and figures**. Ask calibrated yes/no questions: calibrated yes/no questions with the page image or passage attached, for example *Does this table show V in the row labelled R and the column labelled C?*, *Is V attributed to model M and not a neighbouring row?*, *Does this crop show the whole quote?*, *Does the highlighted span support this finding?* **Anything below the threshold goes to GPT-6.2 Sol (independent re-read) and Opus 5.5 (adjudication), and to JP if they disagree.** Our earlier benchmark found the decision models reliable on quote and table or figure grounding (about 97%) and weak on fidelity; JP (2026-11-25) judges that fidelity was defined too strictly and that the headline EVDs were poor because of weak prompting, so the decision models are expected to do better on fidelity with a clearer definition. A fidelity gate may therefore clear a record, but **re-benchmark it first** (TODO) on the audited EVDs with the new definition and set the threshold there; until then Opus 5.5 still checks every EVD claim by claim. Prefer false positives to false negatives (JP, 2026-11-25): when a gate is unsure, send the record on to the stronger models.

**Pilot (JP, 2026-11-24): shadow mode.** Run d1-ultra on every extraction of the pilot papers but do not let it decide yet; compare its answers with the audited vault content and with Opus to set the threshold (recall near 100% for errors). Switch it on once the numbers support it.

## Steps 7 to 14 → see `Skill-templates.md` and `Skill-synthesis.md`

Per paper (`Skill-templates.md`): Step 7 readability formatting (`pipeline/scripts/readability_pass.py`), Step 8 promote NodeFormality for structurally complete nodes (audit-flagged nodes stay `draft`), Step 9 regenerate `sysrev/indexes/dgraph.md` (`pipeline/scripts/build_dgraph.py`), Step 10 save the originating prompt and log the change in History.md. Per batch (`Skill-synthesis.md`): Step 11 cross-paper synthesis, Step 12 public render, Step 13 Obsidian visual treatments, Step 14 ESS Bases.

## Module Q: Quality signals (OPTIONAL, a separate run, only on JP's command; v2, 2026-11-24)

The web app's Quality Signals tables and `/quality` page read about 35 tags from each source page (and the EVD appraisal tags). They are written by `Step 4b` (TRIPOD-LLM table) and `Step 6.c` in `Skill-templates.md` (the `## Quality appraisal` table). This module is **not part of the core run** (read, extract, write nodes, push to the web app), so API credits spent on extraction are never spent on signals by accident. Run it only when JP says so, one paper batch at a time. Until then the web app shows blank signal cells. the tag list and locator standard are in `Quality-signals-spec.md`.

1. **Judged signals** (validity domains, rigor checks, spin, integrity disclosures, TOP levels, TRIPOD rows, and the quality-appraisal rows that give rise to the Quality Signals tables): **Claude Opus 5.5, GPT-6.2 Sol and Gemini 4 Neon (Medium)** each rate every row independently and blind, from the PICOST record and the Methods and Results text, with a verbatim quote and a locator (JP, 2026-11-25). **Majority voting** across the three gives the signal; a 1-1-1 split is shown as "no majority" for JP. Claude Sonnet 5.5 and Inkling 2 Small may also rate, **for benchmarking only** (logged, not counted).
2. **Checks on every rating:** a script checks that each quote appears in the PDF text layer and that the crop contains it; a decision model checks that the quote supports the rating (grounding); JP's spot check covers disagreements and a random sample.
2a. **Log and benchmark (JP, 2026-11-25).** Every individual rating and the aggregate go to the **Quality Signals benchmark sheet** (spec in `Review-sheets-spec.md`: tabs Raw ratings, Aggregate, Benchmark, Costs): one row per paper, signal and rater with the rating, quote, locator, quote check, model, effort, tokens and cost; the aggregate shows votes, majority and agreement; the benchmark tab scores each model and the majority against JP's labels (accuracy, Cohen's kappa, cost per correct rating) as soon as JP adds ground truth.
3a. **Statistical accuracy row** (renamed from "Statistic Accuracy", JP 2026-11-25): run `python3 pipeline/scripts/stat_checks.py --only @citekey` first. It checks (1) percentages that look like parts of 100% add up to about 100, (2) GRIM: a reported mean with its sample size is reachable with whole-number data (applies only to ratings and counts), (3) sample sizes agree between abstract, methods, results and tables, (4) each point estimate lies inside its own confidence interval, (5) "a of b (p%)" is arithmetically right, (6) F1 follows from the precision and recall in the same passage and kappa from observed and chance agreement (and kappa never exceeds agreement), (8) full sample minus exclusions equals the analytic sample, (9) a mean lies inside the stated scale range and a percentage metric is not above 100%, (7) effect sizes are possible (|d| over 3, |r| or |kappa| over 1 are flagged) and not more than 3 SD from the same kind of value in the other papers (our corpus stands in for the wider literature; add a larger reference set later). State each discrepancy plainly and briefly (what, where, the two numbers). The row's rating uses the script findings plus the model's own recomputation of reported numbers (CIs, kappa bounds, table totals); say which came from the script and which from the model. No finding means "nothing flagged", not "verified". The scripts cannot read numbers locked in images; those rows stay Not assessed. Also (added 2026-11-25 in `stat_checks_more.py`): accuracy times N is a whole count; p value and 95% CI agree about the null; pass@k and hit-rate@k do not fall as k rises; "from a to b (+c points)" arithmetic and direction words; SD within the maximum for its range; statcheck-style p recomputed from t, F, chi-square, z and df; GRIMMER (mean and SD reachable with whole-number ratings); precision, recall, F1, accuracy and kappa recomputed from TP, FP, FN and TN; a table's average row equals the mean of the rows above. Left out on purpose: a CI-width-against-N check (not in JP's list; add on request). Every check has a planted-error self-test (`stat_checks.py selftest`).
3b. **Row names come from one registry** (JP, 2026-11-25): `pipeline/templates/quality-signal-labels.json` lists every Quality signal row with its `id`, current `label` and old names (`aliases`). Write row names from the registry, never from memory. To rename a row (for example Non-Significant Result Spin became **Hype/spin**): change `label` in the registry, keep the old name in `aliases`, run `python3 pipeline/scripts/quality_labels.py apply` (rewrites the vault pages; `check` lists names the registry does not know), then rebuild the web app, whose build script (`scripts/build-graph.mjs`) copies the registry to `lib/quality-labels.generated.json`. Nothing in the app code or the pages should hold the name by hand; the old name keeps parsing through its alias. Hype/spin (formerly Non-Significant Result Spin, renamed by JP 2026-11-25) and Statistical Accuracy are the two most recent renames.
3. **Script-only signals** (howfairis and FAIR-Checker for code and data, Pangram for AI-writing, forensic recomputations) are written as tags by script, never by a model.
4. **Tags come from the tables:** do not hand-write tags; regenerate them from the two body tables (the headings `## Quality appraisal` and `## TRIPOD-LLM reporting` must stay exactly as written or the app loses its anchors).
5. **Check before build:** list every source page that lacks a tag in `Quality-signals-spec.md`; fix before running the graph build.
6. **Traceability (required for every row of both tables):** a verbatim quote plus a locator in the exact form in `Quality-signals-spec.md` (section, printed journal page, and Table or Figure number when the evidence is in one). Check with `python3 pipeline/scripts/audit_signal_quotes.py --only @citekey`: every quote must be found in the PDF and every cited page must match the PDF's printed page; fix every other status before moving on. Baseline on the 27 existing sources (2026-11-24): of 999 quoted rows, 91% verbatim, 63% with the right page.
7. **Human review sheet (in parallel, not afterwards):** `python3 pipeline/scripts/signals_decision_models.py --only @citekey` asks Perplexity Decider 1.3, Liquid d1-ultra and Jev whether each quote supports its rating; then `python3 pipeline/scripts/signals_to_gsheet.py --only @citekey --audit <audit csv> --models <jsonl>` builds the workbook (quote, locator, PDF check, judgment dropdown, the three models' verdicts, JP judgment and notes) to upload as a Google Sheet. JP reviews that sheet, not the markdown.
8. **Provenance fields and tool signals** come from scripts, not from a model: `python3 pipeline/scripts/provenance/run_provenance.py --doi <doi> [--code <github url>] [--data <dataset url>]` (OpenAlex, DOAJ, OpenCitations, PubPeer, howfairis, FAIR-Checker). A retraction match is reported as "needs human check" because author ids clash.

**Quotes without typos:** preferred method: the model returns, per row, the printed page and the first and last words of the span; `pdf_pages.py` then extracts the exact text between them from the PDF, so no quote is ever typed by a model. Rows judged from a URL, a table or a figure cite it by locator. (To build; until then run `audit_signal_quotes.py` and fix every non-verbatim row.) **Punctuation does not have to match** (JP, 2026-11-25): the audit ignores dashes, curly quotes, hyphenation at line ends, ligatures and superscript footnote marks, and compares letters and digits only. The exception is decimal points between digits (0.79 is not 079). Only wording and numbers must match.
**Cost (my estimate, per paper, standard prices; half by batch):** Gemini 4 Neon extraction (not yet measured; $3 and $15 per million tokens plus billed thinking tokens), Opus 5.5 rating pass about $0.7, GPT-6.2 Sol blind re-rating about $0.3 to $0.5, the three decision models under $0.01, provenance scripts free. **Pangram (AI-writing check) only on JP's explicit command** (planned Dec/Jan); never as part of a batch.
**Trigger:** JP names the papers and says "run Module Q". Each paper gets its own provenance footer rows (step `quality-signals`).

## Reference docs

- **`Skill-templates.md`** — Steps 4–10: full node-file templates, the TRIPOD-LLM table format, audit invariants and audit scripts, structured-abstract schema, Mermaid visualizations, critical-appraisal calibration, NodeFormality promotion criteria, DGRAPH regeneration, prompt provenance.
- **`Skill-synthesis.md`** — Steps 11–14: EvidencePattern node format, Review-Arena schema + governance, Subtask naming + merge-map pattern, MkDocs build pipeline + hooks + assets, Obsidian visual treatments, ESS Bases formulas + views.
- **`Skill-references.md`** — Naming conventions (file + PNG), the 19 Key Principles (verbatim quotes, atomicity, EVD≠CLM, governance, EP threshold, render-pipeline duality), Common Pitfalls (Methods Context, TRIPOD icons, screenshot pipeline, subagent batching, source-file structure, cross-layer scripting traps), the After-Extraction summary table.
- **`TIPS.md`** — short practical lessons (reopening a closed Google Cloud billing account, the free-tier signs in AI Studio, Zotero close-and-backup rules). Add one entry per lesson.

- **`Quality-signals-spec.md`** — the Quality signal tag vocabulary, the locator standard and the audit baseline (Module Q).
- **`Tools-and-Models.md`** — models, prices, tools, the statistical and embedding tooling, model-origin policy.
- **`../provenance/AI-disclosure.md`** and **`../provenance/model-history.md`** — the project-wide GAMER answers and which model wrote what, by date.
- **`../design/LIVES-design-spec.md`** — the design and development spec for the web app; read it before building or changing the website (the web app is built from this vault by `scripts/build-graph.mjs`).

Load each as needed. The full per-paper extraction loop spans Skill.md (this file) + Skill-templates.md + Skill-references.md. Cross-paper synthesis + public render adds Skill-synthesis.md.

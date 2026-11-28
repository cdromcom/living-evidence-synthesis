---
name: extract-discourse-nodes
description: Extract a full set of discourse graph nodes from a scientific paper PDF — Questions (QUE), Claims (CLM), Evidence (EVD), and Caveats (CVT) — for a given research question. Outputs structured Obsidian-compatible markdown files with embedded figure/table screenshots and quote-region screenshots.
argument-hint: <path-to-pdf> for <research-question-or-link>
allowed-tools: Read, Write, Bash, Glob, Grep
---
You are extracting a complete set of discourse graph nodes from scientific papers given to you as PDFs. The node types together map the paper's argumentative structure: what was asked (QUE), what was found (EVD), what it means (CLM), and where to be cautious (CVT). (EvidencePatterns, EP, are retired from the pipeline: JP, 2026-11-25; CLMs and human-generated syntheses suffice.)

**Two files.** This file is part 1: the step-by-step procedure for one paper. **Part 2, `Skill-controls.md`, holds the run controls (the paper processor, run records, cost caps), drafting nodes by debate, provenance footers, matching and merging, crop, quote and decision-model checks, and the optional quality-signals module. Read it before running a batch, writing nodes or running Module Q.**

## Workflow at a glance (v2)

For one paper, in order (details in Step 1 and the steps below):

1. **Pick and parse:** most recent version of the paper; Gemini 4 Neon reads the PDF and the PDF text layer is the second read (Step 1).
2. **PICOST first:** one record per finding, sorted into primary, secondary and tertiary tiers against the research question, with locators and spotlighted source spans; sources by section (Results for EVDs, Discussion for CVTs and CLMs, Introduction for QUEs).
3. **Check the extractions before anything is written:** PyMuPDF finds every quoted span; the decision-model **checks** score relevancy, fidelity, numbers-in-source and table-cell match; low-confidence and multi-page extractions are re-read by GPT-6.2 Sol and adjudicated by Opus 5.5; JP spot check A (Steps 1 and 6e).
4. **Identify nodes** with atomicity and the QUE rules (Step 2); **write the nodes by debate** (Sonnet 5.5, Sol and Neon draft, critique and revise; Sol and Sonnet vote; checked by the writing-rules check for length, parentheses, capitals and numberss) from the PICOST records (Step 4, `Skill-templates.md`).
5. **Highlight, box and crop** with PyMuPDF and `pdftoppm` (bounding boxes from the span search); GPT-6.2 Sol checks every crop, Opus 5.5 checks multi-page crops (Step 3).
6. **Automatic audits** (verbatim quotes, numbers on the PICOST record, page map), reverse links, formatting, NodeFormality, DGRAPH regeneration, history log (Steps 5 to 10, `Skill-templates.md`).
7. **Mirror to the review sheet** and **JP spot check B**; merge through a pull request and regenerate the graph data.
8. **Provenance footer** on every page written or changed (Step 4c): model and version, date accessed, prompt link, run id, human-check status, from the call log.

**Quality signals** (quality appraisal signals, provenance fields, tool checks) are **Module Q**, which the runner now runs automatically after every batch (JP, 2026-11-26; the 40 TRIPOD-LLM rows are rated in the same run; Pangram is not part of it), so extraction and publishing never spend credits on signals.

Work in **batches of three papers at most** (hard limit in `pipeline/scripts/lives_run.py`; JP 2026-11-26, down from four), and process no further papers until JP has reviewed the previous batch (`lives_run.py` refuses a new batch until JP marks the earlier ones reviewed) with the human checks, the cost controls and the ledger below. Cross-paper synthesis (Review-Arena; EvidencePatterns are retired), the public MkDocs render and the ESS Bases are in `Skill-synthesis.md` (Steps 11 to 14), run after a batch, not per paper.

## Vault structure (summary)

The vault has two parent folders: `sysrev/` (the systematic-review content) and `pipeline/` (how the review is built and published). The folders are `sysrev/dgraph/questions/` (QUE), `sysrev/dgraph/claims/` (CLM), `sysrev/dgraph/evidence/` (EVD), `sysrev/dgraph/caveats/` (CVT), `sysrev/dgraph/source/` (SRC notes `@citekey.md`; PDFs in `sysrev/dgraph/source/pdfs/`, older versions in `sysrev/dgraph/source/pdfs/Archive - superseded versions/`), and `sysrev/picost/` (PICOST JSON), plus `pipeline/templates/`, `pipeline/scripts/`, `pipeline/misc/` (audits, prompts, validation work), `pipeline/public/` (MkDocs site) and the folders `pipeline/skills/` (this Skill system, `Tools-and-Models.md`, `Vault-structure.md`), `sysrev/indexes/` (`dgraph.md`, `DGRAPH-TABLE.md`, `Review-Arena.md`, `ESS - Demo.md`, `ESS.base`, `EvidencePattern Nodes.base`), `pipeline/logs/` (`History.md`, `Log.md`), `pipeline/legal/` (`LICENSE-CONTENT.md`, `PERMISSIONS.md`) and `sysrev/reference/` (`BenchmarkLLM.md`, `Class-Imbalance-Text-Classification.md`, `paraphrase_audit_<date>.tsv`); `Welcome.md` is the only file at the vault root. Screenshots live in `sysrev/dgraph/evidence/Attachments/`. The full tree and file-format notes are in `Vault-structure.md`.

## Node Types and Their Roles

| Type             | Prefix | Role                                                | Grounding                                        |
| ---------------- | ------ | --------------------------------------------------- | ------------------------------------------------ |
| Question         | `QUE`  | Research questions the paper addresses              | Author's stated aims + inferred framing          |
| Evidence         | `EVD`  | Atomic empirical observations from data             | Direct quotes + figure/table + quote screenshots |
| Claim            | `CLM`  | Generalizations from EVDs (results)                 | Direct quotes that state what findings mean      |
| Caveat           | `CVT`  | Methodological limitations on EVDs                  | Author-stated or inferred; flagged accordingly   |
| EvidencePattern (archived 2026-11-25) | `EP` | Cross-paper regularities bundling 2+ EVDs; replaced by cross-paper CLMs | archived in `pipeline/misc/archive/evd-patterns-2026-11-25/` |

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
- **API keys** go in `~/.config/lives-ai-raters/.env` (never in chat or the repo): `OPENAI_API_KEY` (PDF reading with GPT-6.2 Sol), `GEMINI_API_KEY` (Gemini 4 Neon, Project ENIGMA; spending limit set to the $100 loaded), `ANTHROPIC_API_KEY` (Claude Opus 5.5 and Sonnet 5.5), `PERPLEXITY_API_KEY`, `LIQUID_API_KEY` and `PANGRAM_API_KEY` (AI-writing check; use only on JP's command, planned December or January). All of these except the Pangram key were present in `.env` on 2026-11-25; JP added the Pangram key afterwards (confirm before use).
- **Scripts:** the one canonical folder is `pipeline/scripts/`. The older copies are in `pipeline/misc/scripts-superseded/` and use the old folder layout; do not run them.

## Inputs

The user will provide:
1. **A PDF path** (or a list of paths for a batch) — put new PDFs in `sysrev/dgraph/source/pdfs/` (gitignored, so PDFs stay local). Older versions go to `sysrev/dgraph/source/pdfs/Archive - superseded versions/`
2. **A research question** — either inline text or a `[[QUE - ...]]` link. If a link, read it for context.
3. **An output directory** — default: the vault itself. Nodes go to `sysrev/dgraph/<type>/` (questions, claims, evidence, caveats, source); never write next to the PDF.
4. **Supplementary materials check (ask before every run; JP, 2026-11-25).** Ask the user: "Are the supplementary materials and appendices for these papers (online appendices, supplementary tables and figures, protocols and preregistrations) in `sysrev/dgraph/source/pdfs/`? (yes or no)". **Yes:** run. **No:** search for what is missing and add it, then run. For each paper look at the publisher page and the DOI landing page for supplementary links; at the arXiv, bioRxiv, medRxiv or PubMed Central version (they often include the appendices); and at the OSF, Zenodo, Dryad, Figshare and GitHub links named in the paper. Download only freely available files (never bypass a paywall or a login), check that each is a real PDF with PyMuPDF, never open or run anything else from the download, and save it next to the paper as `<paper file name> - supplement <n>.pdf` (or `- appendix <n>.pdf`); `lives_run.py` combines files named this way with the paper into one PDF and tells the model which pages are supplementary. Spreadsheets and code are not downloaded: record their links on the paper's SRC page and tell the user. Report in chat what was added (file, source URL, size) and what could not be found, and note the supplements on the SRC page.

---

## Writing rules for longer sections (JP, 2026-11-25)

These apply to every page and section the Skill writes (SRC pages, node bodies, notes, README and spec files).
1. **No em dashes.** Use a comma, a period, a colon or parentheses instead.
2. **At most one info callout box per page.** Everything else is plain text, lists or tables.
3. **Write like a human.** Plain words, concrete details, varied sentence length, no filler openers ("It is worth noting"), no staged reveals or slogans.
4. **Make it skimmable.** Lead with the point, keep sections short, link the node first (see `Skill-templates.md`).
5. **EVD wording rules (JP, 2026-11-26).** (1) One or two sets of parentheses per EVD, one is better; the statistics go in the last set; no brackets [ ]. (2) No all-caps words: write class labels and ordinary words in lowercase (accurate, not accurate, irrelevant), and keep capitals only for the names of tools, models and metrics (PRISMA, AMSTAR, GPT-4, F1). (3) When the paper reports F1 scores, report the F1 score overall and, if the paper gives them, per class, and leave out precision, recall, macro-F1 and micro-F1: F1 already combines precision and recall, so leaving them out tightens the EVD. (4) At most 247 characters, named models, N and field, comparator, spelled-out metric names. The writing-rules check enforces 1, 2 and the length (`parentheses_ok`, `caps_ok`, `length_ok`); the names allowed in capitals are listed in `pipeline/config/pipeline.json`, key `writing.caps_allowed`; prompts `draft-nodes-v4`, `critique-revise-v4` and `evd-rework-v3` carry rules 1 to 3.
5. **Use a numbered list** for steps, procedures and ranked items. **Use bullets** for unordered items. Never bullet a sequence.
6. **No redundancy or bloat.** Say each thing once inside a subsection or paragraph. Cut restatements, recaps of the line above and padding.
The drafting prompts carry these rules and the writing-rules check flags an em dash in drafted nodes.

## Step 1: Read the Paper

### v2 process (2026-11-24): parse, then PICOST first

> [!info] Why
> The 2026-11-17 audit of the 77 EVD pages found 147 suspected errors (wrong numbers 49, claims not in the paper 33, paper contradicting itself 19, wrong page 18, wrong model or rater 17, missing comparator 8, row or column shift 3). Every one of them passed the quote check. The steps below add the controls that were missing. Tool and model choices are in `Tools-and-Models.md` (v2 section).

1. **Parse with two independent reads.** (a) **Gemini 4 Neon** (`gemini-4-neon`, PDF input; thinking level High) reads the PDF directly (PDF input; reasoning effort High) and returns the PICOST records of item 4 directly, with the printed and PDF page of every number and verbatim spans (the paper processor does not ask for a full page-by-page transcript, which costs many output tokens; the page map comes from PyMuPDF, and a full transcript with HTML tables is requested only for scanned pages). (b) The PDF's own text layer with PyMuPDF for born-digital PDFs. Accept text, numbers and table cells only where the two agree. Where they disagree, or a page has no text layer, decide from the **rendered page image** (`pdftoppm -r 150 -f N -l N -png`), by GPT-6.2 Sol and Opus 5.5 or a human; never from either extraction alone. Do not use `pdftotext -layout` for tables. (2026-11-25: Gemini 4 Neon is the primary reader again, now that JP has a paid Google key in Project ENIGMA and a test call worked; GPT-6.2 Sol is the independent second reader for low-confidence and multi-page items. Keep LlamaParse as the fallback if both misread tables in the pilot.)
2. **Page map, built once per paper.** Record for every page both the PDF page position and the **printed journal page** (PyMuPDF page labels first, otherwise the number printed in the header or footer; mark preprints without printed numbers "PDF position only"). Every citation uses the printed page.
3. **Send Methods and Results first** (with their tables), and other sections only when a field is missing.
4. **PICOST first.** For each candidate finding write one record as JSON: Population, Intervention, Comparator, Outcome, Study design, Timeframe, the finding in one sentence, and every number. **Every number and every PICOST value carries a locator**: journal page, table or figure, row label, column label. Anything the paper does not state is `Not reported`; never fill a slot with plausible standard detail. The bulk extraction model is **Gemini 4 Neon** at thinking level High (Medium or Low for simple steps such as restyling, alt text and link repair; its thinking tokens are billed as output, so set the level per step). **Low-confidence and multi-page extractions** (a confidence flag from Neon or a decision model, a parser disagreement, or a table, figure or finding that spans pages) are re-extracted independently by **GPT-6.2 Sol** and adjudicated by **Opus 5.5**; unresolved ones go to JP. Neon's quality on our papers is unmeasured, so the pilot compares it with Sol and Opus (TODO).
5. **Reconcile prose against tables.** When the text and the paper's own table disagree, use the table and record the disagreement in a note (`- PDF check <date>: ...`); never edit the quote.
6. **Check the whole table before "best".** Before any EVD says best, beat, matched or highest, read every row of the table and list every comparator that could change the claim (other models, human baselines, combined methods).
7. **Checks before any node is written (Step 6e).** Every PICOST record passes four checks: (1) PyMuPDF finds each verbatim span and returns its bounding box; (2) the decision models answer the relevancy, fidelity, quote-grounding and table-cell match questions (Step 6e); (3) a record that is low-confidence or multi-page gets the Sol re-extraction and the Opus adjudication; (4) a human spot check. Sol vision looks at the crop of every finding and may answer `cannot_verify`, which goes to a person (JP, 2026-11-25).
8. **Write the EVD from the PICOST cells.** The EVD statement may contain only numbers that appear in its PICOST record, so the statement, the PICOST row and the screenshot agree.
8a. **Where to look first (JP, 2026-11-24).** EVD content from the **Results** section before any other section; CVTs (caveats) and CLMs (claims) from the **Discussion** (and Limitations) before other sections; QUEs from the **Introduction** (and stated objectives). Fall back to other sections (Abstract, Methods, Conclusion, supplements) only when the preferred section does not give the item, and say in the PICOST record which section each value came from (`section`).
8b. **Spotlight the passages (accuracy aid).** For each finding Gemini 4 Neon returns the verbatim span(s) that support it (text and printed page), not coordinates. PyMuPDF then searches for each span in the PDF (exact match after normalising hyphenation and quote marks), which returns the span's **bounding box**, draws a highlight and a box on the rendered page and saves it as a PNG under `work/<citekey>/highlights/`; the box is also what the crop step uses and is stored with the locator (page, x0, y0, x1, y1). A span PyMuPDF cannot find is a flag (the model paraphrased or misread), and the finding goes back for a fix before anyone writes from it. Humans and Opus 5.5 look at the highlighted page, not the raw PDF.
9. **Work from the most recent report (JP, 2026-11-24).** Prefer the published journal or proceedings version over a preprint, and the latest preprint version over earlier ones; keep the older PDF as `Archive - ...` in `sysrev/dgraph/source/pdfs/Archive - superseded versions/`, and cite the printed page of the version used. Do not silently move an existing page to a newer version: list it for JP (TODO 0d).
10. **Fix page-number errors when you find them (JP, 2026-11-24).** Whenever any step turns up a wrong page citation (printed versus PDF page, a quote that is not on the cited page), correct the citation in both the local vault and the repository copy, add the old and new value to the page's `PDF check` note, and log it; do not wait for a separate audit. Cite the version of the paper the page was built from (a version question goes to TODO 0d).
11. **Run in batches with the paper processor (`lives_run.py`).** One to three PDFs at a time, batch mode once prompts are stable, a spending cap and stop rules, and a run manifest. The command, stages, rails and pilot plan are in `Skill-controls.md`, "The paper processor".

Question rules for the QUEs you propose here are in Step 2 and in `Skill-templates.md` (QUE title phrasing rule, rules 1 to 12; keep each QUE's original wording as a quote).

### Outputs JP reads (v2, 2026-11-24)

JP reads and judges accuracy in a Google Sheet, not in markdown; Obsidian markdown stays the source of truth but should not dominate the human reading experience. For every batch of papers:
1. Write one PICOST file per EVD to `sysrev/picost/<EVD-id>.json` (schema in `sysrev/picost/SCHEMA.md`; every number and value carries a locator; `Not reported` when the paper is silent).
2. Rebuild the review mirror with `pipeline/scripts/vault_to_gsheet.py` and upload it as the Google Sheet "LIVES vault mirror (JP review)" (tabs SRC, QUE, CLM, EVD, CVT, PICOST, SCREENING, each with JP accuracy-judgment dropdowns and a Notes column; screenshots as image formulas). JP judges there; apply his judgments back to the markdown only with his approval.
3. Paper screening (Include or Exclude) is recorded on the SCREENING tab; decision-model screening uses JP's labelled sets and keeps recall near 100%.

### Run records, cost controls and the paper processor → see `Skill-controls.md`

Log every model call (`call_logger.py`: model, effort, tokens, cost, prompt hash, unedited response), stay inside the ledger and the per-batch cap, and run one to four papers at a time with `lives_run.py`. The rules are in part 2: "The paper processor", "Run records and reasoning traces", "Cost controls".

## Step 2: Identify All Nodes

Produce a node inventory before writing any files.

> [!tip] Questions (v2)
> Apply rules 1 to 12 of the QUE title phrasing rule in `Skill-templates.md`: one construct per question, no yes/no, neutral "LLMs" and "research reports", do not mirror the authors' wording, generalize beyond the sample, name the template used, and keep the original wording as a `### Original wording` quote on every QUE (split questions keep the full compound wording in each part).

**Questions (QUE):** What is the main research question? Are there sub-questions (different tasks, analytical angles, or comparisons)? Each distinct research question = one QUE node. Phrase every QUE title per the **QUE title phrasing rule** in `Skill-templates.md` (canonical template table, "LLMs"/"research reports" as subject/object, degree framing, splitting compound questions) — check the template table before coining a new phrasing.

> [!tip] EVD statements (v2)
> Write each EVD title and Description line in the Phase 2 style (`Skill-templates.md`, "EVD statement (headline) style"): named models, N and field, comparator, spelled-out statistics in parentheses, at most 247 characters, built from the PICOST cells. Ground every table, figure and design detail in Methods Context, SRC pages and other nodes with a quote and a crop ("Provenance for tables and figures everywhere").

**Evidence (EVD):** Each distinct statistical test, empirical observation, or analytical finding = one EVD. Do NOT collapse multiple findings into one. Atomicity is essential. Every EVD (and every CLM downstream of one) must also carry a **`task/<slug>` tag** naming which evaluative task the finding is *about* — e.g. `task/risk-of-bias-assessment`, `task/novelty-assessment` — distinct from and in addition to any `5c/*` or `appraisal/*` tags. This answers "what does this finding say about LLM performance on X" as opposed to "how trustworthy is this study," a distinction an advisor flagged in 2026-08 as missing from the corpus. The full 16-value taxonomy (grouped under the 5 Cs plus a "Cross-cutting" bucket for findings about the evaluator's general behavior — prompt sensitivity, cost, fine-tuning — rather than one task) lives in `living-synthesis-site`'s `lib/data.ts` (`TASK_ORDER`/`TASK_LABELS`/`TASK_GROUPS`) and drives that site's graph-view "Evaluative task" filter; check there for the current value list and add a new value (in both this doc and that file) only when an existing one genuinely doesn't fit, rather than inventing a near-duplicate.

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

### Drafting by debate → see `Skill-controls.md`

EVD, QUE, CLM and CVT are drafted by Sonnet 5.5, GPT-6.2 Sol and Gemini 4 Neon (Medium), who critique and revise; Sol and Sonnet vote and Neon breaks ties; a checker that did not write the winner checks every detail. Lint first: 247 characters, numbers on the card, no em dash. Part 2, "Drafting by debate".

## Step 4c: Provenance footer on every node page → see `Skill-controls.md`

Every page written or changed ends with a collapsed AI-use footer generated from the call log (GAMER checklist: models, effort, time, prompt link and hash, saved response, human-check status). Part 2, "Step 4c".

## Matching, linking, merging and splitting → see `Skill-controls.md`

EmbeddingGemma 2 proposes candidate pairs; GPT-6.2 Sol and Claude Sonnet 5.5 must agree; a person verifies every merge or split (subtle differences mean do not merge). Part 2, "Matching, linking, merging and splitting".

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

## Who checks crops and quotes → see `Skill-controls.md`

Scripts first, then the decision-model checks (mean probability and spread guide what happens next), then GPT-6.2 Sol vision on the crop of every finding (pass, fail or cannot verify), and Claude Opus 5.5 only on rare disputes. Part 2.

## Step 6e: Decision-model check of extractions → see `Skill-controls.md`

Decider 1.3 and d1.2-ultra run four checks (relevancy, fidelity, numbers-in-source, table-cell match) before any node is written. Part 2, "Step 6e".

## Steps 7 to 14 → see `Skill-templates.md` and `Skill-synthesis.md`

Per paper (`Skill-templates.md`): Step 7 readability formatting (`pipeline/scripts/readability_pass.py`), Step 8 promote NodeFormality for structurally complete nodes (audit-flagged nodes stay `draft`), Step 9 regenerate `sysrev/indexes/dgraph.md` (`pipeline/scripts/build_dgraph.py`), Step 10 save the originating prompt and log the change in History.md. Per batch (`Skill-synthesis.md`): Step 11 cross-paper synthesis, Step 12 public render, Step 13 Obsidian visual treatments, Step 14 ESS Bases.

## Module Q: Quality signals (OPTIONAL) → see `Skill-controls.md`

Runs automatically after every batch of at most four papers (JP, 2026-11-26; Pangram only on JP's command). Neon, Opus 5.5 and Sol rate blind at high effort and two of three decide; scripts check quotes. The full module (rows, rules, cost, Pangram) is in part 2, "Module Q".

## Reference docs

- **`Skill-templates.md`** — Steps 4–10: full node-file templates, the TRIPOD-LLM table format, audit invariants and audit scripts, structured-abstract schema, Mermaid visualizations, critical-appraisal calibration, NodeFormality promotion criteria, DGRAPH regeneration, prompt provenance.
- **`Skill-synthesis.md`** — Steps 11–14: EvidencePattern node format, Review-Arena schema + governance, Subtask naming + merge-map pattern, MkDocs build pipeline + hooks + assets, Obsidian visual treatments, ESS Bases formulas + views.
- **`Skill-controls.md`** (part 2: run controls, drafting by debate, footers, matching, checks, Module Q)
- **`Skill-references.md`** — Naming conventions (file + PNG), the 19 Key Principles (verbatim quotes, atomicity, EVD≠CLM, governance, EP threshold, render-pipeline duality), Common Pitfalls (Methods Context, TRIPOD icons, screenshot pipeline, subagent batching, source-file structure, cross-layer scripting traps), the After-Extraction summary table.
- **`Pipeline-design-and-longevity.md`** (reflection: layers, how to swap a model, package, Skill or template, robustness over time, budgets and ethics, how others can customize)
- **`TIPS.md`** — short practical lessons (reopening a closed Google Cloud billing account, the free-tier signs in AI Studio, Zotero close-and-backup rules). Add one entry per lesson.

- **`Quality-signals-spec.md`** — the Quality signal tag vocabulary, the locator standard and the audit baseline (Module Q).
- **`Tools-and-Models.md`** — models, prices, tools, the statistical and embedding tooling, model-origin policy.
- **`../provenance/AI-disclosure.md`** and **`../provenance/model-history.md`** — the project-wide GAMER answers and which model wrote what, by date.
- **`../design/LIVES-design-spec.md`** — the design and development spec for the web app; read it before building or changing the website (the web app is built from this vault by `scripts/build-graph.mjs`).

Load each as needed. The full per-paper extraction loop spans Skill.md (this file) + Skill-templates.md + Skill-references.md. Cross-paper synthesis + public render adds Skill-synthesis.md.

**Table parsers (exploratory):** Marker and MinerU are being tested for reading table cells only, on the 27 seed papers; they are not part of the run. See `Skill-controls.md`, "Table parsers", and `misc/evd-validation/table-parsers/RESULTS.md`.

## Update 2026-11-27 (lean model plan, local aim, tables, verification)

**Lean model plan (JP, 2026-11-27; pending validation, not built).** Target at most $2.49 per paper for extraction, quality signals, TRIPOD-LLM and the quality appraisal table. Quality signals and TRIPOD-LLM rows: Gemini 4 Neon (high) rates every row; low-confidence rows go to GPT-6.2 Sol (high); if Sol is also unsure the row goes to JP; Opus 5.5 is not used. Verification: when the two decision models disagree, Neon (medium) judges instead of Sonnet 5.5. Quote reading from screenshots: Neon replaces Sonnet. Drafting: first drafts by GPT-6.2 Sol only, critique by Neon only, tiebreaker Sonnet 5.5. EVD rework below 0.60: Sol (medium). Classifying sampled problems: a small local model to try (Neon low as the hosted fallback). Grouping questions, claims, evidence and caveats: EmbeddingGemma 2 (local) finds candidates, Neon (medium) decides. The estimate from pilot logs is about $3.0 to $3.5, above the target (see `misc/evd-validation/TODO.md`). Until JP validates it, the three-rater maximum-accuracy setting remains the default in `config/models.json`.

**Table cells and Word files (2026-11-27).** `pdf_pages.table_numbers(page)` matches a verified value against numbers in any table cell plus table captions and footnotes: 463 of 463 values found (strict cell match 431, any cell 451). Five any-cell matches are accidental (for example the 5 in a 'Recall@5' header). `derotate.derotate_page(page)` turns a rotated page upright before MinerU reads it (MinerU 380 to 431 at /Rotate 90). `pdf_pages.docx_tables(path)` reads .docx tables through python-docx with merged cells repeated (10 of 10 supplement values; the four `sj-docx-*` files return 0, 0, 0 and 1 table). Do not convert Word files to PDF; save an old .doc as .docx first.

**Model procedure now in config (JP, 2026-11-27, later; supersedes the lean plan above where they differ; still pending validation by JP's labels).** Extraction Neon; second reading Sol; settling disagreements Sonnet 5.5; the Opus 5.5 role is gone (no role uses it; vision disputes go to Sonnet 5.5). Quality-signal and TRIPOD rows: Neon (high) rates, a low-confidence row goes to Sol (high), and if Sol is also unsure the row is marked needs_human. Drafting: Sol drafts alone (no critique, no vote, no tiebreak); Neon (medium) runs the node-detail check; EVD rework by Neon (medium) fixes errors only and lists each change. Verification: Perplexity Decider 1.3, Liquid d1.2-ultra (d1.3-ultra when available) and bison-1 (shadow) score every item; the judge is never the model that produced the item (Sol judges Neon's items and Neon's ratings; Neon judges Sol's fallback ratings); quote screenshots are read by Sol (low), not by the extractor. Items are flagged for human examination when the judge scores below 0.75, when a decision model scores below 0.5 and the judge does not pass it, or when the judge and the decision-model majority disagree. Grouping: EmbeddingGemma 2 plus Neon (medium). Sorting of sampled revisions to note: Neon (low), on request only. The local Gemma 4 12B QAT test was dropped: on the 24 GB laptop it needed 435 and 508 seconds for two items (2,500 tokens each, about 5 tokens per second) and slowed the machine. Inkling 2 Mini is 16.1 GB at 4-bit (MLX) and was not tried. Estimated cost per paper with these roles, from old token logs, batch prices: $2.32 pooled over four papers (range 1.79 to 2.98); about $2.91 when the stages configured as standard mode are priced at list price. Target: at most $2.49.

**No paper is cut off (JP, 2026-11-27).** JP: "I never want runs to have papers cut off." Output budgets are the model limits; a request that ends with MAX_TOKENS, max_tokens, CONTINUATION or incomplete is retried at medium effort in batch, then in standard mode with the largest budget (marked in the manifest), and only if that also ends cut off is it marked needs JP. Details: `Skill-controls.md`, section "No paper is cut off".

**Decision models (JP, 2026-11-27).** Three decision models vote: Perplexity Decider 1.3, Liquid d1.3-ultra (d1.2-ultra until the API accepts that id; HTTP 404 on 2026-11-27) and Baseten bison-1. bison-1 reads text only. The judge is called unless all voting decision models agree. Review sheets show one column per model, the judge score and the judge model name.

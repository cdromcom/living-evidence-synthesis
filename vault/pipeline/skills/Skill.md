---
name: extract-discourse-nodes
description: Extract a full set of discourse graph nodes from a scientific paper PDF — Questions (QUE), Claims (CLM), Evidence (EVD), and Caveats (CVT) — for a given research question. Outputs structured Obsidian-compatible markdown files with embedded figure/table screenshots and quote-region screenshots.
argument-hint: <path-to-pdf> for <research-question-or-link>
allowed-tools: Read, Write, Bash, Glob, Grep
---
You are extracting a complete set of discourse graph nodes from scientific papers given to you as PDFs. The five node types together map the paper's argumentative structure: what was asked (QUE), what was found (EVD), what it means (CLM), where to be cautious (CVT), and which regularities span ≥2 papers (EP).

## Workflow at a glance (v2)

For one paper, in order (details in Step 1 and the steps below):

1. **Pick and parse:** most recent version of the paper; GPT-6.2 Sol reads the PDF and the PDF text layer is the second read (Step 1).
2. **PICOST first:** one record per finding with locators and spotlighted source spans; sources by section (Results for EVDs, Discussion for CVTs and CLMs, Introduction for QUEs).
3. **Check the extractions:** Liquid d1-ultra (shadow mode in the pilot) and Opus 5.5 on low confidence; JP spot check A (Steps 1 and 6e).
4. **Identify nodes** with atomicity and the QUE rules (Step 2); **write the nodes** from the PICOST records (Step 4, `Skill-templates.md`).
5. **Crop screenshots** with PyMuPDF and `pdftoppm`; GPT-6.2 Sol checks every crop, Opus 5.5 checks multi-page crops (Step 3).
6. **Automatic audits** (verbatim quotes, numbers on the PICOST record, page map), reverse links, formatting, NodeFormality, DGRAPH regeneration, history log (Steps 5 to 10, `Skill-templates.md`).
7. **Mirror to the review sheet** and **JP spot check B**; merge through a pull request and regenerate the graph data.
8. **Provenance footer** on every page written or changed (Step 4c): model and version, date accessed, prompt link, run id, human-check status, from the call log.

**Not in this run:** quality signals (TRIPOD-LLM and quality appraisal tables, provenance fields, tool checks) are the separate optional **Module Q**, run only on JP's command, so extraction and publishing never spend credits on signals.

Work in **batches of five papers** with the human checks, the cost controls and the ledger below. Cross-paper synthesis (EvidencePatterns, Review-Arena), the public MkDocs render and the ESS Bases are in `Skill-synthesis.md` (Steps 11 to 14), run after a batch, not per paper.

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
- **API keys** go in `~/.config/lives-ai-raters/.env` (never in chat or the repo): `OPENAI_API_KEY` (PDF reading with GPT-6.2 Sol), `ANTHROPIC_API_KEY` (Claude Opus 5.5), `PERPLEXITY_API_KEY`, `LIQUID_API_KEY`, `TYPESAFE_API_KEY` (Jev), and the Tinker key if the Inkling voter is used. Only the Perplexity, Liquid and Jev keys were set on 2026-11-24.
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

1. **Parse with two independent reads.** (a) **GPT-6.2 Sol** reads the PDF directly (PDF input; reasoning effort High) and returns page-by-page markdown with each table as HTML, the printed journal page for every page, and every figure caption. (b) The PDF's own text layer with PyMuPDF for born-digital PDFs. Accept text, numbers and table cells only where the two agree. Where they disagree, or a page has no text layer, decide from the **rendered page image** (`pdftoppm -r 150 -f N -l N -png`), by Claude Opus 5.5 or a human; never from either extraction alone. Do not use `pdftotext -layout` for tables. (LlamaParse Agentic Plus was the first choice, then Gemini 4 Neon; JP could not get a Google API key on 2026-11-24 and chose GPT-6.2 Sol, so one model reads and extracts. Keep LlamaParse as the fallback if Sol misreads tables in the pilot.)
2. **Page map, built once per paper.** Record for every page both the PDF page position and the **printed journal page** (PyMuPDF page labels first, otherwise the number printed in the header or footer; mark preprints without printed numbers "PDF position only"). Every citation uses the printed page.
3. **Send Methods and Results first** (with their tables), and other sections only when a field is missing.
4. **PICOST first.** For each candidate finding write one record as JSON: Population, Intervention, Comparator, Outcome, Study design, Timeframe, the finding in one sentence, and every number. **Every number and every PICOST value carries a locator**: journal page, table or figure, row label, column label. Anything the paper does not state is `Not reported`; never fill a slot with plausible standard detail. The bulk extraction model is GPT-6.2 Sol at reasoning effort High (Medium for simple steps such as restyling, alt text and link repair; Max only if the pilot shows it removes errors that High leaves); Claude Opus 5.5 handles disagreements and tricky cases.
5. **Reconcile prose against tables.** When the text and the paper's own table disagree, use the table and record the disagreement in a note (`- PDF check <date>: ...`); never edit the quote.
6. **Check the whole table before "best".** Before any EVD says best, beat, matched or highest, read every row of the table and list every comparator that could change the claim (other models, human baselines, combined methods).
7. **QA gate (Step 6e), deferred.** The Liquid d1-ultra check of each PICOST record is on hold (JP, 2026-11-24); until it is switched on, the check is Opus 5.5 on every record flagged by a parser disagreement plus a 10% random sample, and a human spot check. Remind JP to revisit it after the first batch of new papers.
8. **Write the EVD from the PICOST cells.** The EVD statement may contain only numbers that appear in its PICOST record, so the statement, the PICOST row and the screenshot agree.
8a. **Where to look first (JP, 2026-11-24).** EVD content from the **Results** section before any other section; CVTs (caveats) and CLMs (claims) from the **Discussion** (and Limitations) before other sections; QUEs from the **Introduction** (and stated objectives). Fall back to other sections (Abstract, Methods, Conclusion, supplements) only when the preferred section does not give the item, and say in the PICOST record which section each value came from (`section`).
8b. **Spotlight the passages (accuracy aid).** For each finding GPT-6.2 Sol returns the verbatim span(s) that support it (text and printed page), not coordinates. PyMuPDF then searches for each span in the PDF (exact match after normalising hyphenation and quote marks), draws a highlight on the rendered page and saves it as a PNG under `work/<citekey>/highlights/`. A span PyMuPDF cannot find is a flag (the model paraphrased or misread), and the finding goes back for a fix before anyone writes from it. Humans and Opus 5.5 look at the highlighted page, not the raw PDF.
9. **Work from the most recent report (JP, 2026-11-24).** Prefer the published journal or proceedings version over a preprint, and the latest preprint version over earlier ones; keep the older PDF as `Archive - ...` in `sysrev/dgraph/source/pdfs/Archive - superseded versions/`, and cite the printed page of the version used. Do not silently move an existing page to a newer version: list it for JP (TODO 0d).
10. **Fix page-number errors when you find them (JP, 2026-11-24).** Whenever any step turns up a wrong page citation (printed versus PDF page, a quote that is not on the cited page), correct the citation in both the local vault and the repository copy, add the old and new value to the page's `PDF check` note, and log it; do not wait for a separate audit. Cite the version of the paper the page was built from (a version question goes to TODO 0d).
11. **Batch API for unattended runs, on every provider (once the process is reviewed).** Run bulk steps (reading, PICOST extraction, drafting, verification) through each provider's Batch API: Anthropic Message Batches (50% off, stacks with prompt caching), OpenAI Batch (about half price; GPT-6.2 Sol $1 in and $5 out per million tokens, from third-party pages, to confirm on OpenAI's pricing page) and Gemini Batch if a Google key is ever available. Put the Skill instructions first and unchanged in every request so they are cached. Use the standard API only for pilots and when someone is waiting. Decision models such as d1-ultra have no batch mode and cost too little to matter. Log tokens, cost and time per paper and step.

Question rules for the QUEs you propose here are in Step 2 and in `Skill-templates.md` (QUE title phrasing rule, rules 1 to 12; keep each QUE's original wording as a quote).

### Outputs JP reads (v2, 2026-11-24)

JP reads and judges accuracy in a Google Sheet, not in markdown; Obsidian markdown stays the source of truth but should not dominate the human reading experience. For every batch of papers:
1. Write one PICOST file per EVD to `sysrev/picost/<EVD-id>.json` (schema in `sysrev/picost/SCHEMA.md`; every number and value carries a locator; `Not reported` when the paper is silent).
2. Rebuild the review mirror with `pipeline/scripts/vault_to_gsheet.py` and upload it as the Google Sheet "LIVES vault mirror (JP review)" (tabs SRC, QUE, CLM, EP, EVD, CVT, PICOST, SCREENING, each with JP accuracy-judgment dropdowns and a Notes column; screenshots as image formulas). JP judges there; apply his judgments back to the markdown only with his approval.
3. Paper screening (Include or Exclude) is recorded on the SCREENING tab; decision-model screening uses JP's labelled sets and keeps recall near 100%.

### Run records and reasoning traces (JP, 2026-11-24)

Save a complete record of every model call, so the work is reproducible and, later, usable as training data for open-weight models. For each call write one JSON line to `pipeline/runs/<batch>/<citekey>/calls.jsonl` (kept out of git by default because it holds paper text and screenshots; the folder has its own README):
- `model` (exact id and version), `provider`, `date`, `effort`, `temperature` if any, `prompt_hash` and a pointer to the prompt file, `inputs` (file paths and page numbers, not copies of paper text), the `output`, `usage` (input, cached, reasoning and output tokens, cost, latency), and the step name (read, extract, draft, vote, check, crop QA, decision-model check);
- the **reasoning trace exactly as the provider returns it**: Claude extended-thinking blocks when enabled for Opus 5.5 and Sonnet 5.5 (store them verbatim, including whether the provider marks them summarized); GPT-6.2 Sol reasoning summaries (the API does not return raw reasoning; record the summary and the reasoning-token count); Inkling 2 on Tinker, the full text it generates; decision models (d1-ultra, Perplexity Decider, Jev) return calibrated probabilities and no trace, so store the probabilities. Never invent or reconstruct a trace; write `null` when the provider returns none;
- the **human verdict** when one exists (JP's judgments from spot checks A and B and the mirror sheet), linked by EVD id, so each trace can be filtered to verified-correct outputs.

**Before using any trace for training:** check each provider's terms. Anthropic's and OpenAI's terms restrict using their model outputs to develop competing models, so the proprietary traces are an audit and analysis record until the terms are checked or permission is obtained. Safe sources for an open-weight training set are Inkling 2 traces (open model), JP's own verified judgments and edits, the PICOST records and final texts JP has approved, and the decision-model probabilities. Paper text and screenshots stay under their source licences (`legal/PERMISSIONS.md`); share training data only for papers whose licence allows it.

### Cost controls (v2, 2026-11-24)

Follow these every run so JP does not have to remember them. Budget, per-batch caps and the ledger are in `pipeline/misc/evd-validation/2026-11-24-ingest-budget-and-batches.md`.

1. **Work five papers at a time** with the human spot checks A and B in that file; stop a batch that costs more than 1.5 times its estimate or that shows an error at a check.
2. **Standard API for the first three papers, then iterate on the prompts; switch to the Batch APIs only after an external reviewer has given feedback** (JP, 2026-11-24). Batch is about half price and suits runs nobody is waiting on (reading, extraction, writing, verification).
3. **Cache the Skill:** put the Skill and instructions first and unchanged in every request.
4. **Send only what is needed:** Methods and Results with their tables first; skip references, appendices and acknowledgements; fall back to other sections only when a field is missing.
5. **Use the free second read:** the PDF text layer is the second vote; send page images to the model only for pages with tables or figures.
6. **Escalate by exception:** Opus 5.5 only where the two reads disagree, plus a 10% random sample, not on every record.
7. **Short structured output:** PICOST as compact JSON; GPT-6.2 Sol at High for reading and extraction, Medium for restyling, alt text and link repair; never Max unless a pilot shows it removes errors High leaves.
8. **Screen before reading:** remove duplicates and off-topic papers with a cheap relevance call (Perplexity Decider 1.3 or Liquid d1-ultra) before the full read.
9. **Pilot, then reuse:** fix the prompts on five papers, save every step's output, and resume instead of rerunning.
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
- **Table and figure crops** contain the table or figure and its caption only, every row, column and panel, no body text (see the grounding rules in `Skill-templates.md`). Do not screenshot the full page. Methods tables and method diagrams are cropped and embedded the same way.
- **Preflight per paper (nip problems early).** Before extracting, check the PDF: born-digital or scanned, one or two columns, text-layer quality (ligatures, odd font encodings, missing spaces), math-heavy, tables as vector text or as images, page labels. Pick the path from the result and record it in `work/<citekey>/preflight.json`; a scanned or poor-text paper starts on the OCR path below.
- **If PyMuPDF cannot find or crop something (fallback ladder; never ship an unverified crop):** (1) retry with stronger normalisation (ligatures, hyphenation, Unicode, quote marks, soft line breaks) and n-gram or fuzzy matching on 8-word windows; (2) search line by line and per column, then stitch the pieces; (3) cross-check with a second extractor (`pdfplumber` or `pdftotext -bbox-layout`) and take the box where the two agree; (4) for tables and figures, snap to PyMuPDF `find_tables()`, image blocks and the caption line, with Sol proposing an approximate box from the rendered page that PyMuPDF refines to the nearest text blocks; (5) OCR the page image and match the quote in the OCR text; (6) flag for JP with the page image. Every crop that passes goes through the Sol crop QA above.

- **Cross-check against the audit.** Compare each cropped table against the structured cells from Step 1 (two-tool agreement) before the screenshot is accepted: a mismatched row or column shift is the audit's error type 7, a value next to the wrong label is type 5.
- **Printed page in every citation.** Use the page map from Step 1. The screenshot filename may keep the PDF index (`p6`); the citation may not. If the paper has no printed numbers, write `PDF p. N` so a reader knows.
- **Crop QA before any human sees a screenshot (JP, 2026-11-24).** GPT-6.2 Sol (vision, High) inspects every crop against a checklist and returns pass or fail with a reason: (1) it is the item the node cites (the quoted passage, or the table or figure whose numbers the EVD uses); (2) quote crops show every word, first and last lines not cut off; (3) table or figure crops show the item and its caption only, all rows, columns and panels, no body text, no neighbouring item, no page header; (4) legible and not blurred; (5) the cited printed page matches the page shown. Only passes go to the mirror sheet; a fail is re-cropped (up to two retries) and then flagged. **Any crop built from more than one page or column** (stitched pieces, whited-out words) is also verified by Claude Opus 5.5 for accuracy and cleanliness: correct order, no duplicated or missing lines, no visible seams or leftover fragments, still reads as one clean figure. Record the verdicts in `work/<citekey>/crop-qa.json`.
- **Alt text.** Add each screenshot's description to the alt-text map; the filename is never the alt text.

## Step 4: Write the Node Files → see `Skill-templates.md`

### EVD writing loop (JP, 2026-11-24): Sonnet drafts, two voters pick, Opus checks and edits; pilot it

Writing an EVD from its PICOST card is a short call (about 3k tokens in, 0.5k out), so several models can collaborate cheaply. Fidelity checking stays on in the pilot and beyond; the old fidelity labels are ignored only as a benchmark, because those EVDs were poorly written.
1. **Lint (free, deterministic):** at most 247 characters; every number, model name and comparator in the statement appears on the PICOST card; metrics spelled out; no unlisted numbers.
2. **Draft (medium model):** Claude Sonnet 5.5 writes two candidates in the Phase 2 style from the PICOST card, using the three examples in `Skill-templates.md`.
3. **Pick the better candidate (not Opus):** GPT-6.2 Sol (Medium) and Inkling 2 Small (on Tinker; JP's choice of Inkling model, newest and efficient; sampling via the Tinker API, key in `~/.config/lives-ai-raters/.env`; model id `thinkingmachines/Inkling-2-Small` to confirm) each choose the better candidate independently, seeing the candidates, the source span and the table crop. If they agree, that candidate goes on. If they disagree, Claude Opus 5.5 breaks the tie.
4. **Check and edit (large model):** Claude Opus 5.5 checks the chosen candidate claim by claim (model, N, comparison, each number, direction) against the source span or crop (supported, partly supported, unsupported, with the supporting words) and edits it for fidelity, clarity and the Phase 2 style. A claim it cannot support is removed or the candidate goes back for a new draft.
5. **Record:** the final text, both votes, the per-claim verdicts and the models used go into the PICOST JSON (`evd_checks`), and JP judges Fidelity in the mirror sheet as usual.
**Pilot A/B (this afternoon):** on two papers compare this loop with Opus 5.5 writing alone (cost, JP's fidelity and style ratings, edit rate, how often the two voters agree).

## Step 4c: Provenance footer on every node page (required; JP, 2026-11-24)

Every page the Skill writes or changes (QUE, CLM, EVD, CVT, SRC, EP) ends with a clean, collapsed **AI-use footer** so a reader can see how the sausage was made. It follows the GAMER checklist (Generative Artificial intelligence tools in MEdical Research) and is generated, not typed. Closed, it shows one line: `AI use: <models> · <date> · <human-check status>`. Open (click in Obsidian; click or hover in the web app), it shows a skimmable table (step, model and version, effort, UTC time, prompt link and hash, saved response) and a role / sections / checked-by line, plus a link to `pipeline/provenance/AI-disclosure.md` (the project-wide answers to all nine GAMER items) and, for older pages, `pipeline/provenance/model-history.md`:
1. **Prompts live in the repository.** Each prompt used lives in `pipeline/prompts/<name>-v<n>.md` (or `.txt`) and is **committed and pushed before the run**, so its link resolves to a fixed version. Never edit a committed prompt in place; make `-v<n+1>`.
2. **Log every model call** with `python3 pipeline/scripts/call_logger.py log ...` (or the library functions): exact model id and display name, effort, UTC time of access, prompt file, SHA-256 and commit, tokens, estimated cost, run id.
3. **Render the block** with `python3 pipeline/scripts/call_logger.py footer --run-id <run> --node "<page title>"` and paste it as the last block of the page. Each later step that changes the page (a vote, a check, a human edit) adds a row; never overwrite earlier rows.
4. **Save the unedited response** of every call (`call_logger.py` writes it to `pipeline/runs/<run>/responses/`), because GAMER item 3 asks for it. **The block states:** step, model and version, effort, date and time accessed (UTC), a link to the exact prompt and its short hash, the run id, and the human check status (`not yet reviewed` until a person signs off, then who and when).
5. **Pages written before this rule** (all 232 today) get the legacy footer (`render_legacy_footer`) with what the vault logs record (for example "Claude Sonnet 4.6, 2026-04-17, prompt not archived"; era table in `model-history.md`) and say what is unknown. Add them after the next pipeline run, when the details have settled (JP, 2026-11-25). `scripts/file_model_history.py` lists a page's commits by era.
6. The web app renders the footer as a `<details>` element (closed by default; also opens on hover for pointer users, and on keyboard focus) at the bottom of the page; a one-line byline under the title links to it.
7. **Link activity is logged too.** Every time a model creates or changes links between nodes (QUE-CLM, CLM-EVD, EVD-CVT, cross-paper), log the call with step `link` and write the proposed links to `pipeline/runs/<run>/links.jsonl` (from, to, kind, model, reason). Then run `python3 pipeline/scripts/check_links.py` (structure: both directions agree, every EVD has one source and a claim, every CLM is listed by a QUE, every EP rests on two or more papers). Links across papers get a second look: a light model (Haiku 5.5 or a decision model asking "does this evidence bear on this question?") votes yes/no, and every no goes to JP. Candidate merges of near-identical QUEs: a small local embedding model (for example EmbeddingGemma) lists pairs with high cosine similarity; the check model and then JP decide. Never merge automatically.

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

## Step 6e: Decision-model check of extractions (v2; pilot in shadow mode)

After the nodes and crops are extracted, the **Liquid d1-ultra** decision model (`d1-ultra`, `api.liquid.ai/decisions/v1/systemone`; key in `~/.config/lives-ai-raters/.env`) checks each extraction at a small fraction of an Opus call: calibrated yes/no questions with the page image or passage attached, for example *Does this table show V in the row labelled R and the column labelled C?*, *Is V attributed to model M and not a neighbouring row?*, *Does this crop show the whole quote?*, *Does the highlighted span support this finding?* **Anything below the threshold goes to Claude Opus 5.5 to adjudicate** (and to JP if Opus is unsure). Our benchmark found the decision models reliable on quote and table or figure grounding (about 97%) and not on fidelity, so use them for grounding and numbers, not for judging whether a headline is supported.

**Pilot (JP, 2026-11-24): shadow mode.** Run d1-ultra on every extraction of the pilot papers but do not let it decide yet; compare its answers with the audited vault content and with Opus to set the threshold (recall near 100% for errors). Switch it on once the numbers support it.

## Steps 7 to 14 → see `Skill-templates.md` and `Skill-synthesis.md`

Per paper (`Skill-templates.md`): Step 7 readability formatting (`pipeline/scripts/readability_pass.py`), Step 8 promote NodeFormality for structurally complete nodes (audit-flagged nodes stay `draft`), Step 9 regenerate `sysrev/indexes/dgraph.md` (`pipeline/scripts/build_dgraph.py`), Step 10 save the originating prompt and log the change in History.md. Per batch (`Skill-synthesis.md`): Step 11 cross-paper synthesis, Step 12 public render, Step 13 Obsidian visual treatments, Step 14 ESS Bases.

## Module Q: Quality signals (OPTIONAL, a separate run, only on JP's command; v2, 2026-11-24)

The web app's Quality Signals tables and `/quality` page read about 35 tags from each source page (and the EVD appraisal tags). They are written by `Step 4b` (TRIPOD-LLM table) and `Step 6.c` in `Skill-templates.md` (the `## Quality appraisal` table). This module is **not part of the core run** (read, extract, write nodes, push to the web app), so API credits spent on extraction are never spent on signals by accident. Run it only when JP says so, one paper batch at a time. Until then the web app shows blank signal cells. the tag list and locator standard are in `Quality-signals-spec.md`.

1. **Judged signals** (validity domains, rigor checks, spin, integrity disclosures, TOP levels, TRIPOD rows): Claude Opus 5.5 rates each from the PICOST record and the Methods and Results text, with a verbatim quote and a locator.
2. **Independent check:** a model from another family (GPT-6.2 Sol) re-rates every row without seeing the first rating; a script checks that each quote appears in the PDF text layer. Disagreements go to JP's spot check.
3. **Script-only signals** (howfairis and FAIR-Checker for code and data, Pangram for AI-writing, forensic recomputations) are written as tags by script, never by a model.
4. **Tags come from the tables:** do not hand-write tags; regenerate them from the two body tables (the headings `## Quality appraisal` and `## TRIPOD-LLM reporting` must stay exactly as written or the app loses its anchors).
5. **Check before build:** list every source page that lacks a tag in `Quality-signals-spec.md`; fix before running the graph build.
6. **Traceability (required for every row of both tables):** a verbatim quote plus a locator in the exact form in `Quality-signals-spec.md` (section, printed journal page, and Table or Figure number when the evidence is in one). Check with `python3 pipeline/scripts/audit_signal_quotes.py --only @citekey`: every quote must be found in the PDF and every cited page must match the PDF's printed page; fix every other status before moving on. Baseline on the 27 existing sources (2026-11-24): of 999 quoted rows, 91% verbatim, 63% with the right page.
7. **Human review sheet (in parallel, not afterwards):** `python3 pipeline/scripts/signals_decision_models.py --only @citekey` asks Perplexity Decider 1.3, Liquid d1-ultra and Jev whether each quote supports its rating; then `python3 pipeline/scripts/signals_to_gsheet.py --only @citekey --audit <audit csv> --models <jsonl>` builds the workbook (quote, locator, PDF check, judgment dropdown, the three models' verdicts, JP judgment and notes) to upload as a Google Sheet. JP reviews that sheet, not the markdown.
8. **Provenance fields and tool signals** come from scripts, not from a model: `python3 pipeline/scripts/provenance/run_provenance.py --doi <doi> [--code <github url>] [--data <dataset url>]` (OpenAlex, DOAJ, OpenCitations, PubPeer, howfairis, FAIR-Checker). A retraction match is reported as "needs human check" because author ids clash.

**Quotes without typos:** preferred method: the model returns, per row, the printed page and the first and last words of the span; `pdf_pages.py` then extracts the exact text between them from the PDF, so no quote is ever typed by a model. Rows judged from a URL, a table or a figure cite it by locator. (To build; until then run `audit_signal_quotes.py` and fix every non-verbatim row.) **Punctuation does not have to match** (JP, 2026-11-25): the audit ignores dashes, curly quotes, hyphenation at line ends, ligatures and superscript footnote marks, and compares letters and digits only. The exception is decimal points between digits (0.79 is not 079). Only wording and numbers must match.
**Cost (my estimate, per paper, standard prices; half by batch):** Opus 5.5 rating pass about $0.7, GPT-6.2 Sol blind re-rating about $0.3 to $0.5, the three decision models under $0.01, provenance scripts free. **Pangram (AI-writing check) only on JP's explicit command** (planned Dec/Jan); never as part of a batch.
**Trigger:** JP names the papers and says "run Module Q". Each paper gets its own provenance footer rows (step `quality-signals`).

## Reference docs

- **`Skill-templates.md`** — Steps 4–10: full node-file templates, the TRIPOD-LLM table format, audit invariants and audit scripts, structured-abstract schema, Mermaid visualizations, critical-appraisal calibration, NodeFormality promotion criteria, DGRAPH regeneration, prompt provenance.
- **`Skill-synthesis.md`** — Steps 11–14: EvidencePattern node format, Review-Arena schema + governance, Subtask naming + merge-map pattern, MkDocs build pipeline + hooks + assets, Obsidian visual treatments, ESS Bases formulas + views.
- **`Skill-references.md`** — Naming conventions (file + PNG), the 19 Key Principles (verbatim quotes, atomicity, EVD≠CLM, governance, EP threshold, render-pipeline duality), Common Pitfalls (Methods Context, TRIPOD icons, screenshot pipeline, subagent batching, source-file structure, cross-layer scripting traps), the After-Extraction summary table.

Load each as needed. The full per-paper extraction loop spans Skill.md (this file) + Skill-templates.md + Skill-references.md. Cross-paper synthesis + public render adds Skill-synthesis.md.

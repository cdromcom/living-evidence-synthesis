---
page_type: todo
created: 2026-11-17
updated: 2026-11-17
author: Claude (Opus 5.5, claude-opus-5-5) in Claude Code, for Jay Patel (JP)
---

# TODO: open tasks for JP (LIVES EVD validation)

Everything still open for JP from the 2026-11-11 to 11-17 sessions. The same list is in the Google Sheet "LIVES - AAA Benchmarking (HAI)", tab **TODO**, which has a Status column to tick off. Column letters refer to the LIVES-EVD-Benchmarking tab as of 2026-11-17. Done items from earlier lists (ABOUT TODO 12-13, PICOST realignment, Fidelity/Grounding split, Claude's missing judgments) are not repeated.

> [!tip] Suggested order
> Settle the two grading rules (3-4) and protect your columns (8) first, then fill your columns (1-2), then run the other AIs (9-10). The vault, site and drafts items can wait until benchmarking ends.


## A. Benchmark grading

- [x] **0. Decide whose ratings G79:G82 (EVD 74-77) are** (done 2026-11-17: re-judged blind, same ratings; G47:H48 left as they are, JP decision)  
  Where: LIVES-EVD-Benchmarking, G79:H82  
  The provenance check (2026-11-17) found these are probably your original ratings, restored to Claude's column on your statement. Recommended: have Claude judge EVD 74-77 blind (without seeing G or I) and replace G79:H82. Also decide whether G47:H48 (continuation placeholders, author unknown) should be re-stamped by Claude.  
  *Source: prompt 41; [[2026-11-17-claude-column-provenance-check]]*
- [ ] **1. Fill your relevancy judgments for every row Claude rated and you haven't**  
  Where: LIVES-EVD-Benchmarking, columns I-J  
  Benchmark Summary Table 6 shows the live count. Includes EVD 49 and 50 (rows 54-55): your notes are in J, but I has no rating.  
  *Source: ABOUT TODO 10; prompt 33*
- [ ] **2. Fill your Fidelity and Grounding judgments for every row, including rows where you agree with Claude**  
  Where: LIVES-EVD-Benchmarking, columns M-N, Q-R, U-V  
  In Claude's 2026-11-11 rows your columns hold only the cells you changed, so Table 7 counts only disagreements there. Rate every row independently so Table 7 is fair. Your Jay rows are already done.  
  *Source: Prompts 38-39*
- [ ] **3. Settle the Fidelity rule: must every number appear in the verbatim quote?**  
  Where: Tell Claude; then the grader prompt gets updated  
  Claude rated Partially Met when a number appears only in an unquoted table summary or Methods Context; you rated those Met. That is 30 of the 51 compared rows (Table 7, kappa 0.13).  
  *Source: Table 7, 2026-11-17*
- [ ] **4. Settle the Quote rule: verbatim quote but its screenshot shows a different passage**  
  Where: Tell Claude; then the grader prompt gets updated  
  Claude rated Incorrect (7 rows where you said Correct), which matches your own edits on rows 60, 61, 72 and 76. Also decide whether a wrong page number alone means Partially Correct (12 rows where you said Correct).  
  *Source: Table 7, 2026-11-17*
- [ ] **5. Check today's flagged Claude Fidelity/Grounding rows**  
  Where: LIVES-EVD-Benchmarking, notes in L, P, T  
  Quote with a mismatched screenshot: rows 4, 6, 7, 19, 24, 46, 82. Row 15: Zhang & Abernethy quote is in v1 but not v3. Row 6 and 8 Table/Fig changed to NA under your clarified rule (row 8: Missing if supplemental file 4 counts). Row 12: Figure 2 crop nearly empty. Row 14: 'weakest' vs 'very weak'. Row 79: the paper's Figure 2A disagrees with its text.  
  *Source: Prompts 38, 40*
- [ ] **6. Confirm which rows you meant by 'EVDs 44 and 52'**  
  Where: LIVES-EVD-Benchmarking, U44 and U53  
  Your NA Table/Fig ratings and NA notes are on sheet rows 44 (EVD 43) and 53 (EVD 48). Sheet rows 45 and 52 hold EVD 44 and EVD 47 (cont.). Claude's 2026-11-11 ratings there say Missing; they were left as benchmark data.  
  *Source: Prompt 40*
- [ ] **7. Review the rows Claude flagged for review**  
  Where: LIVES-EVD-Benchmarking, columns B-C  
  16 Claude-graded rows from 2026-11-11 are flagged YES; none has been marked as checked by you yet.  
  *Source: ABOUT TODO 9*
- [ ] **8. Protect your reference columns before any other model touches the sheet**  
  Where: Data > Protect sheets and ranges: I-J, M-N, Q-R, U-V, AS  
  A model being scored must not be able to see or edit the reference labels.  
  *Source: Prompt 33 task list*
- [ ] **9. Set aside a tuning set, then run Jev, Gemini Decision 1 and Perplexity Decider 1.3**  
  Where: LIVES-EVD-Benchmarking, AJ-AK, AL-AM, AN-AO; log runs in AI Prompt Log  
  One fixed prompt and the same inputs for all three, blinded to every other label. Record each run's version, date and prompt.  
  *Source: ABOUT TODO 11*
- [ ] **10. Adjudicate the reference label after all four AIs have voted**  
  Where: LIVES-EVD-Benchmarking, column AS  
  Only rows where any AI disagrees with you need a decision.  
  *Source: ABOUT TODO 11*
- [ ] **11. Optional: test the checker with a few planted errors**  
  Where: Ask Claude  
  Lets you report the checker's recall honestly in the write-up.  
  *Source: Prompt 33 task list*
- [ ] **12. Set dropdown chip colours by hand if chips look gray**  
  Where: Data > Data validation  
  The Sheets API cannot set chip colours; cell fills come from conditional formatting.  
  *Source: Prompt 36*

## B. Vault and PDF audit

- [x] **0d. NEXT WEEK, after the Skill refinement: decide which version the EVD pages cite**  
  **Done 2026-11-24:** most recent report is cited: Thelwall 2025 journal (PR 11), Xu ACL 2025 (12), Shahid SDP 2025 (13), Zhang & Abernethy 2025 arXiv v3 (14), Huntington-Klein 2026 journal (15). Older PDFs go to sysrev/source/pdfs/Archive - superseded versions/. Akyon and Liang published versions still need JP's download (0b).
  Where: EVD pages for Thelwall, Huntington-Klein, Shahid, Xu (and Akyon, Liang once downloaded)  
  Citing the published versions shifts page numbers, some quote wording and screenshots. Calendar reminder: Wed 2026-11-25, 10:00 ET.  
  *Source: prompt 48*
- [ ] **0b. Download the two published versions Claude couldn't get**  
  Where: Akyon https://medinform.jmir.org/2024/1/e59258/PDF ; Liang https://ai.nejm.org/doi/full/10.1056/AIoa2400196 (UMD sign-in)  
  JMIR blocked the browser save twice; NEJM AI is paywalled. Drop the PDFs anywhere and tell Claude.  
  *Source: prompt 47*
- [ ] **0c. Decide on EVD page fixes from the version comparison**  
  Where: pipeline/misc/evd-validation/2026-11-20-pdf-version-diff/README.md  
  Only Huntington-Klein changed substantively, but errors that are in both versions were found. Biggest: the Shahid RankGPT title is wrong (13.79% keeps RankGPT; removing it gives 10.34%). Also decide whether pages should cite the published versions.  
  *Source: prompt 47*
- [ ] **13. Review the proposed PDF-audit corrections and tick the ones you approve**  
  Where: Vault: pipeline/misc/evd-validation/2026-11-17-pdf-audit-proposed-changes.md  
  185 changes (147 audit + 38 Zhang v3). Start with the 70 marked with the flag symbol. Nothing is applied until you tick and tell Claude; each page is backed up first.  
  *Source: Prompts 29, 32*
- [ ] **14. Decide the 10 HELD fixes**  
  Where: Same file, search 'HELD' (ids 26, 27, 44, 45, 77, 78, 79, 80, 82, 83)  
  These change only the page number in a quote's citation, which touches quotes you are still benchmarking.  
  *Source: Prompt 32*
- [x] **15. After benchmarking, decide whether Zhang & Abernethy titles and quotes move to v3**  
  **Done 2026-11-24:** Zhang & Abernethy 2025 titles, quotes and screenshots moved to arXiv v3 (PR 14). Zhang & Abernethy 2024 (reference errors) is a different paper and stays on arXiv v1 by JP's decision; its published AMIA version (PMC12919499) is not needed.
  Where: Vault: the 3 Zhang & Abernethy EVD pages  
  Tables and notes were drafted for v3; titles, quotes and screenshots still carry v1 numbers (e.g. HR@5 16.3% in v1, 11.0% in v3).  
  *Source: Prompt 32*
- [ ] **16. Fix LIVES pages that contradict themselves**  
  Where: Vault evidence pages: EVD 49, 50, 54, 58, 59, 70; EVD 77  
  Details in ABOUT, 'LIVES pages that contradict themselves'. EVD 77's page also lacks the accuracy figures your verdict cites from Table 1.  
  *Source: ABOUT TODO 5*
- [ ] **17. Fix the EVD 1 page**  
  Where: Vault: EVD 1 page  
  Add the ellipsis before 'The majority of citations...' and a Table 1 screenshot or replica, as your verdict asks.  
  *Source: ABOUT TODO 7*
- [ ] **18. Check your own rewrites against the pages**  
  Where: Columns W / your rewrites: EVD 6, 7, 20, 22, 26, 33, 35, 38, 41, 42, 45, 77  
  Decide whether the rewrite or the page is right. Details in ABOUT, 'JP's own rewrites'. (EVD 8, 22 and 45 vault pages were already fixed from the PDFs on 2026-11-17.)  
  *Source: ABOUT TODO 4*

## C. Skills, live site and copies

- [ ] **0e. NEXT WEEK: refine the Skills to prevent the extraction and other errors, and switch them to the new tools and models**  
  Where: Skill.md, Skill-references.md, Skill-templates.md, pipeline/scripts/; full plan in [[Tools-and-Models]]  
  Planned toolchain (JP, 2026-11-20):
  1. OCR: Chandra OCR 2 and OXR-1.0 must agree, with the PDF text layer as a third vote for born-digital PDFs; the page image decides remaining disagreements; add Granite-Docling only if the pilot shows many unresolved disagreements. OXR-1.0 is exempt from the origin policy as long as it is open and runs locally (JP); check its licence. Ripple-65B Preview (Ricursive Intelligence; dense 65B; Apache 2.0; trained from scratch; text only): use a community GGUF build on JP's 128 GB Framework PC (4-bit about 40 GB, 8-bit about 70 GB); the official BF16 (about 130 GB) does not fit and NVFP4 needs NVIDIA GPUs; confirm the developer is US-based and test its extraction quality. Disagreements go to the page image; other tools are fallbacks.
  2. Once the OCR models agree, PyMuPDF and pdftoppm do the highlights and screenshots.
  3. Skill steps: Inkling 2 Mini and Gemma 4 do the first extraction pass locally (backups via hosted APIs: Ripple-65B Preview, Reflection Beam); Claude Opus 5.5 breaks ties and does all writing and judging, effort set per task (see 0h). No alternates (gpt-oss and Olmo 3 dropped). Fast decisions: Perplexity Decider 1.3 (local). Embeddings: EmbeddingGemma 2 (local) for deduplication, linking and screening. Pangram 4.1 via API. Gemma 4 set aside. Model-origin policy (JP, 2026-11-20: the best open and closed US models only; **replaced 2026-11-25**: hosted APIs from US developers only, and open-weight models from any country if they run locally and are state of the art or close to it; record each model's base model). Pangram 4.1 is a US API, so it stays allowed.
  4. Optional Pangram 4.1 quality-signal checks.
  
  Pipeline requirements to build in: a fixed test set with pass bars per stage; one OCR model by default, escalating to the others; a fixed, resumable script with a config file (no hard-coded paths); a run manifest (model versions, weight hashes, prompts, settings, raw outputs) and containers; swappable models; checks on licences, data storage, screenshot copyright and non-English papers; a README and one-command run; human review kept at the end. Fold in the lessons from the 2026-11-17 PDF number audit, the grader-prompt refinements, the 2026-11-20 version-diff errors and the provenance check. Claude edits Skill.md only with your approval.  
  **Status 2026-11-24 (updated):** GPT-6.2 Sol (reasoning effort High; Medium for simple steps) replaces LlamaParse and Gemini 4 Neon as the PDF reader and bulk extractor (no Google key); Batch APIs for all unattended runs; the d1-ultra PICOST check is ON HOLD (remind JP after the first batch of new papers).  first v2 edits applied to Skill.md (Step 1 parse and PICOST first, Step 3c, Step 6c), Skill-templates.md (QUE rules 9-12, Original wording block, grounding rules, Methods Mermaid dropped), Skill-references.md and Tools-and-Models.md (v2 toolchain). Backup: pipeline/misc/skill-backups/2026-11-24-pre-v2/. Still open: Google and LlamaCloud keys, the LlamaParse test on the 27 PDFs, the d1-ultra QA calibration on the 147 audit corrections, a Gemini 4 Neon extraction bake-off, reconciling the local vault with the repo vault.  
  *Source: prompts 48, 52, 54-56, 58-64*

- [ ] **19. Decide whether to push corrected vault pages to GitHub so the live site updates**  
  Where: GitHub cdromcom/living-evidence-synthesis (needs your approval)  
  Covers EVD 8, 22 and 45 (already fixed locally) and any approved audit changes. The live site still shows the old numbers.  
  *Source: Prompts 27-28*
- [ ] **20. Fix broken and mislabelled screenshots on the live site**  
  Where: GitHub vault-img / vault pages  
  404 on the live site: alharbi2024-table1cont-p5-1.png, thelwallEvaluatingResearchQuality2024-tables-p8-1.png. 'Figure not available' placeholders: liangCanLargeLanguage2024a aspects-p5-5 and overlap-p3-3; sonWhenAICoScientists2025 fig4-p6, tables-p34-4, tables-p5-2; wuAutomatedNoveltyEvaluationa results-p10-1. Many images named 'table' or 'fig' are text crops (see Claude's T notes).  
  *Source: Prompt 38 grading*
- [ ] **21. Plan the next screenshot iteration**  
  Where: Skill.md (Step 3a already says this)  
  Your idea in AD80: when a quote mentions a table or figure, screenshot it under the quote screenshot, and auto-collapse Description screenshots. Also crop table screenshots to the table and caption, not the full page.  
  *Source: AD80-AD81 notes*
- [ ] **22. After fixes are applied, have Claude re-check the drafts and PICOST cells drawn from changed pages**  
  Where: LIVES-EVD-Benchmarking column X; PICOST  
  Fixing one copy does not fix the others.  
  *Source: Prompt 33 task list*

## D. Drafts and PICOST

- [ ] **23. Review Claude's drafts**  
  Where: LIVES-EVD-Benchmarking, column X (your rewrites in W)  
  PICOST now shows column X for all 81 rows. Accept, edit or reject each draft.  
  *Source: ABOUT TODO 1*
- [ ] **24. Decide whether to have the unchecked drafts fact-checked**  
  Where: Ask Claude  
  Not yet fact-checked: the round-2 drafts (EVD 28, 48, 61, 71, 74), the 7 practice drafts (EVD 4, 5, 12, 13, 19, 24, 43) and the 20 drafts shortened to the 247-character cap.  
  *Source: ABOUT TODO 2*
- [ ] **25. Keep or drop drafts on rows rated Irrelevant or Wrong**  
  Where: EVD 48, 61, 71, 74 (rows 53, 66, 76, 79)  
  Some capped drafts also dropped secondary numbers (e.g. EVD 54's 40% non-confounder figure, EVD 68's average error).  
  *Source: ABOUT TODO 3*
- [ ] **26. Review the PICOST tab**  
  Where: PICOST  
  Confirm S = Study design and T = Timeframe is the variant you want. Spot-check cells against the PDFs (extraction used LIVES pages). On 2026-11-17, 30 cells were replaced and 7 corrected for the 35 rows whose EVD text changed.  
  *Source: ABOUT TODO 6, 12*
- [ ] **27. Write Phase 2 rewrites**  
  Where: LIVES-EVD-Benchmarking, column Y  
  Only EVD 46 has a Phase 2 rewrite so far.  
  *Source: ABOUT TODO 8*

## E. Write-up and expansion

- [ ] **0g. LATER: add GROBID and EmbeddingGemma 2**  
  Where: Quality Signals pipeline; pipeline/misc/scripts/find_redundancies.py; plan in [[Tools-and-Models]]  
  GROBID to parse reference lists for reference checks in the Quality Signals pipeline. EmbeddingGemma 2 (version 2 confirmed by JP 2026-11-25; released 2026-10-06, Apache 2.0) to find duplicate nodes, screen new papers from the AI-assisted search, and suggest node links, with Claude Opus 5.5 deciding on each candidate and you confirming. Test on the April redundancy audit first.  
  *Source: prompts 53, 56*
- [ ] **0h. NEXT WEEK (with 0e): analyse the cost-saving design and fold it into the updated Skill.md**  
  Where: Skill.md and related files; [[Tools-and-Models]]  
  Agreed by JP on 2026-11-20, to analyse before adopting:
  1. Send models only the Methods and Results sections (and their tables) first; fall back to other sections only when needed.
  2. Extraction by cheaper models: Inkling 2 Mini and Gemma 4 extract locally; Claude Opus 5.5 is called only when they disagree.
  3. Claude Opus 5.5 does all writing and judgment steps, with effort set to each task's demands (low for simple pass/fail checks, higher for nuanced judgments); tune the levels on the test set.
  4. Cache the Skill instructions: put them first and unchanged in every request.
  5. Use the Batch API (half price) for runs nobody is waiting on.
  6. One fixed API call per step instead of open-ended agent sessions.
  7. Run OCR, PyMuPDF/pdftoppm, EmbeddingGemma and Inkling 2 Mini locally.
  8. Ask for short, structured (JSON) outputs.
  9. Pilot on 3-5 papers before a full run; save each step's output and resume instead of rerunning; remove duplicate papers first.
  10. Log input, cached and output tokens and cost per paper and step; set a spending limit.
  11. Use the Claude subscription for interactive work and the API (lab credits) for batch runs.
  
  *Source: prompts 57, 59-62*
- [ ] **0i. AFTER 0e/0h: build the pipeline to pass the criteria (reproducible, stable and reliable, cost-effective including in low- and middle-income countries, usable across countries, user-friendly)**  
  Where: a pipeline repository (pushing to GitHub needs your approval); notes in [[Tools-and-Models]] > Implementation notes  
  - Reproducible: pinned versions and weight hashes, lock file, container (Docker plus Apptainer), run manifest per run, prompts in git with tags, temperature 0 for open models, raw outputs kept, regression run on the test set.
  - Stable and reliable: one package and one command, config file, resumable steps, fail per paper, schema validation, automatic checks, unit and end-to-end tests on three sample papers, fix the known script breakages.
  - Cost-effective (including low- and middle-income countries): open-only mode with no paid API, hardware tiers with measured cost per paper, quantized models, the 0h cost levers, offline after setup, shared outputs for open-access papers.
  - Usable across countries: model registry (developer, country, base model, licence, where it runs; hosted APIs US developers only, local open-weight models from any country if near-SOTA, policy of 2026-11-25), licence and data-protection checks, screenshot copyright rules, non-English test, neutral formats.
  - User-friendly: README.md, config.example.yaml, .env.example, LICENSE (you choose the licences), CITATION.cff, CHANGELOG.md, CONTRIBUTING.md, MODELS.md, sample_data/, docs/.
  
  *Source: prompt 60*
- [ ] **0f. Expand the review: ingest more PDFs via an AI-assisted search strategy**  
  Record the search strategy (databases, tools, queries, dates, screening rules) in the AI Prompt Log. New PDFs follow the naming convention and the refined Skills.  
  *Source: prompt 48*
- [ ] **28. Report the timing differences in Claude's judgments**  
  Where: Methods section of the paper  
  Claude's relevancy calls for rows 46 and 49 and notes for rows 79-82 were made on 2026-11-17, later than the other Claude rows (2026-11-10 to 11-13). Claude's Fidelity/Grounding for the 31 Jay rows were graded on 2026-11-17 against the live app; the other Claude rows on 2026-11-11.  
  *Source: ABOUT TODO 13; prompt 38*


## 2026-11-25 plan (added by Claude; JP edits freely)
**JP, next three days:** work on the protocol; manually review the vault and screen papers; add `PANGRAM_API_KEY` to `~/.config/lives-ai-raters/.env` when ready (Pangram runs only on JP's command, likely Dec/Jan); review the signals sheet v2 (judgments, models, failure causes); re-rate the quote labels listed in `benchmarking-validation/README.md`; decide on merging PRs #26 (vault alignment and v2 backbone), #27 (design docs), #8 and #21 (benchmarking).
**Before the Monday run (fresh batch of dozens of PDFs):**
- [ ] Put PDFs in `sysrev/dgraph/source/pdfs/`; pick the five-paper pilot batch (Woelfle, Bougie, Tyser first, per the budget note).
- [ ] Write and commit the prompts the run needs in `pipeline/prompts/` (pdf-read, picost, write-nodes, checks) so footers can link them; log every call with `call_logger.py`.
- [ ] Add the provenance footer to the node templates in the web app render (callout at page bottom, byline under the title).
- [ ] Decide: backfill legacy footers for the 232 existing pages (model and date from `History.md`, `Log.md`, `curatedWithModel`).
- [ ] Module Q (quality signals) stays OFF unless JP says so.
**Cleanup found by the scripts:** review the 115 quotes `verbatim_audit.py` flags (`pipeline/misc/evd-validation/paraphrase_report.tsv`) and the 85 signal-table quotes not found; check why two Sarol EVD pages list caveats their CVT `appliesTo` does not (`reverse_links.py` would drop those two links); decide the page rule for 157 rows that cite PDF position, 104 wrong pages.
**Web app (Opus 5.5, about $11 for phase 1):** adopt the revised plan from the four-model design consult (`pipeline/runs/2026-11-25-design-consult/`): gates from phase 1, byline plus footer, CLM and EVD templates, list-first graph, library combobox.
**Ideas, not scheduled:** INSPECT-SR-inspired trustworthiness signals (post-publication notices via Crossref or OpenAlex, registration-versus-paper consistency, internal count consistency, version consistency between preprint and journal); span-extraction of quotes in Module Q.

## 2026-11-25 later additions (JP)
- [ ] **Wrightson 2025 source page is in the wrong folder in the working vault.** It sits at `source/@wrightsonGPTRCTsUsing2025.md` (vault root, created Nov 24 about 15:55); it belongs in `sysrev/dgraph/source/`, where the repo and the wikilinks expect it. JP is keeping the repo copy in `sysrev/dgraph/source/`. `check_links.py` reports 11 broken links until the vault copy is moved back (`mv source/@wrightsonGPTRCTsUsing2025.md sysrev/dgraph/source/`). `check_repo_sync.py` lists it as "only local" until then. Do not sync the stray copy.
- [ ] Footers for the 232 existing pages (collapsed GAMER footer, legacy form): after the next pipeline run, when the details have settled.
- [ ] Re-run the design consult with the two-page prompts (`design-consult-v2.md`, `design-enhance-v2.md`) and read the new color, type, layout, visual, animation and accessibility sections (see the run folder `pipeline/runs/2026-11-25-design-consult-v2/`).
- [ ] Link checks: `check_links.py` is read-only. 2 questions are linked from no claim list (Can LLMs pick the better of two abstracts; Can LLMs verify author checklists in submissions): decide to link or merge.
- [ ] Trustworthiness signals (INSPECT-SR-inspired), later: Current Status already covers retraction, correction and expression of concern; consider splitting "Statistic accuracy" into specific forensic checks (GRIM-type means, test statistics vs p values, sample sizes consistent across abstract, methods and tables); registration consistency later when studies are registered.
- [ ] Embedding model for candidate merges and cross-paper links: **EmbeddingGemma 2**, run locally. Inkling 2 Small and Claude Sonnet 5.5 judge each candidate and must agree (JP, 2026-11-25: no human approval needed for agreed merges and splits; disagreements go to a human queue). Log every decision (see the Skill section "Matching, linking, merging and splitting" and the "Pipeline overview (links, merges)" tab of the AAA Benchmarking sheet).
- [ ] Model-by-page history: confirm the model of the April 28 batch agents and which pages were rewritten in summer 2026 (`pipeline/provenance/model-history.md`).
- [ ] Embedding pipeline (EmbeddingGemma 2 via Ollama): not set up yet; **downloaded 2026-11-25 on JP's order** (JP: it is the best). Weights: Hugging Face `google/embeddinggemma-2` (Apache 2.0, not gated), 1.4 GB, in `~/.cache/lives-bench/models/embeddinggemma-2/`. The installed Ollama (too old) cannot pull it, so it runs through sentence-transformers in its own environment `~/.cache/lives-bench/venv-embed` (transformers 5.24.1, sentence-transformers 6.3.0, torch 2.15.0). First test: a paraphrase pair scored 0.92 and a related but different QUE pair 0.84; the 27 QUE titles' closest pairs sit at 0.93 to 0.95 (all about finding errors in papers; related, not duplicates), so similarity alone cannot decide merges and the two judges are needed. Closest CVT pairs (0.89 to 0.90) include three caveats that the datasets used only ICLR or NeurIPS papers, a real merge candidate. Plan: embed QUE, CLM, EP and CVT text; list same-type pairs above a similarity threshold; a model reads each pair; JP approves merges.
- [ ] EP "LLM performance varies substantially with prompt design..." links to a claim that does not exist ("CLM - LLM novelty evaluation is highly sensitive to prompt variations"); the nearest page is a CVT ("LLM novelty evaluation is highly prompt-sensitive and hard to replicate"). Fix the link.
- [ ] Wrightson source page: moved back to `sysrev/dgraph/source/` on 2026-11-25. The vault copy now has extra Zotero fields (zotero-key, year, journal, DOI, abstract); sync it to the repo.

## 2026-11-25 (later): Inkling study, node-writing fine-tune
- [ ] **LATER, after more PDFs are in (JP): build the train, dev and test split** for the Inkling 2 Small classification study. Split by paper, not by row (for example about 18 train, 4 dev and 5 test papers once there are more), and pre-select hard rows (where the decision models disagreed or doubted the rating) for hand-labeling.
- [ ] **December 2026: run steps 1 to 4 of the Inkling 2 Small study** once JP has ingested and screened more papers (hundreds of rows): (1) smoke run of about 20 examples to confirm the training price and toolchain; (2) learning curve at 100, 300 and about 900 training examples; (3) label-source test (gold only against gold plus silver); (4) medley: the tuned model's confidence plus the three decision models, measured against JP. Baseline first: Inkling 2 Small with no tuning, zero-shot and few-shot, next to the decision models.
- [ ] **JP hand-labels about 200 rows** (a few more is fine), but later, not now.
- [ ] **Target score (JP): Cohen's kappa above 0.85** against JP's labels on papers the model has not seen. Also report recall on "does not support", calibration and cost per 1,000 rows.
- [ ] Note on JP's answers (2026-11-25): to "is quote-supports-rating the right target?" JP said no, and the bigger goal is the node-writing fine-tune below; the classification study stays as a small learning experiment. The question about checking Anthropic and OpenAI terms on training with their outputs was not clearly answered: until it is, train only on JP-verified text and open-model outputs.
- [ ] **After Stage II EVD writing and human verification: fine-tune Inkling 2 Mini (or Small) to write QUEs, CLMs, EVDs, EPs and CVTs** (a hard task). Training data: the human-verified nodes from the new pipeline (dozens of papers soon). Same discipline: split by paper, hold out test papers, compare against Claude Opus 5.5 and Sonnet 5.5 drafts, judge with the decision models, and log every call. Mini trains at $0.75 per million tokens and Small at $1.50 (unverified, see Tools-and-Models.md).
- [ ] Match each new paper's EVDs to existing QUEs and CLMs: EmbeddingGemma 2 proposes, Inkling 2 Small and Claude Sonnet 5.5 must agree; record the three decisions in the AAA Benchmarking sheet tab "Pipeline overview (links, merges)" and in node-history.jsonl.
- [ ] Statistical accuracy checks added 2026-11-25 (stat_checks.py): estimate inside its confidence interval, "a of b (p%)", F1 from precision and recall, kappa from observed and chance agreement, effect sizes outside the possible range or more than 3 SD from the other papers. First corpus result: three point estimates in the Roberts 2023 abstract lie outside their own confidence intervals (check the paper).
- [x] **Forensic checks added 2026-11-25** (JP chose 1, 3, 4, 5, 6, 7, 8 plus the heavier ones): all implemented in `stat_checks_more.py` with planted-error self-tests; not yet exercised on real errors beyond the Roberts 2023 abstract because the 27 papers rarely report t(df) tests, confusion-matrix counts or stated deltas. Not implemented: CI width against N (JP's list skipped it), SPRITE, DEBIT (needs the text to say the SD is over items), RIVETS and STALT (details unverified). Original idea list (JP to choose): accuracy times N must be a whole count (GRIM for proportions); CI width for an accuracy against the binomial width for N; p value and CI must agree about the null; pass@k and hit-rate@k must rise with k; "from a to b (+c)" arithmetic; SD within its maximum for the stated range (Bhatia-Davis); recompute p from t, F or chi-square and df (statcheck-style); GRIMMER for integer ratings; DEBIT for binary outcomes when SD is over items. RIVETS and STALT: details not verified (see chat 2026-11-25).

## 2026-11-25 (late): embedding test, merges, naming
- [ ] **Hype/spin**: renamed from "Non-Significant Result Spin" in 28 source rows, the app labels and the Skill (the old key still parses). Check the question text in each row still reads well.
- [ ] **Merge candidates for JP to examine**: `pipeline/misc/evd-validation/embedding-candidates/candidates.md` (all types) and `judgments.md` (Sonnet 5.5 second opinion on the top 25 CVT and top 10 QUE pairs; 0 merges, 21 umbrella, 14 keep separate). A human verifies every merge; subtle differences mean do not merge.
- [ ] **Decide how to represent "group under an umbrella"** (a parent node, a tag, or a link) before the next pipeline run; the merge judge now returns it.
- [x] **Inkling 2 Small wired up as a judge** (2026-11-25; Tinker's OpenAI-compatible endpoint, model id `thinkingmachines/Inkling-2-Small`, key `TINKER_API_KEY`; `call_logger.logged_tinker`). First comparison, 90 pairs across QUE, CLM, CVT, EP and EVD (run 2026-11-25-merge-judge-2, $0.35 total: Sonnet about $0.30, Inkling about $0.05): Sonnet 5.5 said keep separate 53 and group under an umbrella 37 (0 merges); Inkling said group under an umbrella 89 and merge 1; they agree on 36 of 90 (they disagree on 54), and Inkling never chose keep separate. So Inkling over-groups with this prompt. Next: few-shot examples or a calibration set labeled by JP, and a prompt that makes keep separate the default. Still to confirm: Inkling's price and the model-origin policy for Small and Mini.
- [ ] **Embedding thresholds**: similarity is high for every pair (domain-homogeneous nodes), so use ranking, mutual nearest neighbors and difference hints; calibrate on pairs JP labels as same or different. Consider embedding the full node body, not only the title.
- [ ] **Merge CVTs?** JP expected CVTs should merge; the first look finds mostly distinct caveats that share a theme (for example datasets limited to ICLR or NeurIPS papers). Candidate umbrella groups: ML-conference-only datasets (3 caveats), single-model tests (GPT-3.5 or GPT-4 only, 3 to 4 caveats), zero-shot or single-prompt only (2 to 3 caveats).
- [ ] **Look at the one pair Inkling called "merge"**: QUE "How do LLM reviews compare to human reviews" against "How much do LLM reviews overlap with human reviews" (Sonnet: umbrella). `pipeline/misc/evd-validation/embedding-candidates/judgments.md`.
- [ ] **Vercel project "benchmarking-validation"** fails on every commit (Python build, no entrypoint: the project builds the `benchmarking-validation/` folder). Added `benchmarking-validation/vercel.json` with git deployments off (PR pending). Cleaner: delete or disconnect that Vercel project in the dashboard if it is not needed; the Vercel tool access in this session could not see the project.
- [x] **Row names flow from one registry** (`pipeline/templates/quality-signal-labels.json`; `quality_labels.py`; app copy via `scripts/build-graph.mjs`; Skill Module Q 3b). Renaming = edit the registry and run `quality_labels.py apply`.
- [x] **JP's first calibration label (2026-11-25):** Inkling 2 Small was right to call QUE "How do LLM reviews compare to human reviews" and QUE "How much do LLM reviews overlap with human reviews" a merge; Sonnet 5.5 said umbrella. Gold label for the calibration set: merge. The merge itself is not done yet (needs the human-verified merge step: keep the old title as an alias, record both pages).
- [ ] **Run the Supabase view-only SQL** (`supabase/migrations/2026-11-reviews-view-only.sql`): JP asked on 2026-11-25; the Supabase dashboard in the browser session was signed out, so JP must sign in (or run it) first.
- [x] **Logo reverted** to the plain turtle icon and the big "Report on GitHub" box replaced by a small link (2026-11-25; PR pending).
- [ ] **CVT patterns (CVT-P)** (JP, 2026-11-25): the first merge test shows many caveats are similar but not duplicates (datasets limited to ICLR or NeurIPS papers; only GPT-3.5 or GPT-4 tested; zero-shot or single-prompt only; curated or constructed error samples; text-only models). Eventually write up recurring caveats as a pattern node type, CVT-P, the way an EP groups evidence across papers: the individual CVTs stay as they are, and a CVT-P names the shared limitation and links its members. Decide the node type, its template and how it differs from the "umbrella" idea (see the "group under an umbrella" TODO). Start from the candidate groups in `pipeline/misc/evd-validation/embedding-candidates/judgments.md`.
- [x] **One review box** (2026-11-25): the Report on GitHub box was merged into Review this node; see the design spec addendum. Takedown stays as a footer link to the GitHub issues page.
- [ ] **Supabase view**: JP to paste `supabase/migrations/2026-11-reviews-view-only.sql` into the Supabase SQL Editor and click Run (no SQL files exist inside Supabase; the file lives in the repository).
- [x] **Dark mode and shell study** added to the design spec (section 16), measured from JP's Supabase screenshot; owner to confirm the hex values and the optional icon rail.

- [ ] **Embedding model bake-off** (2026-11-25): EmbeddingGemma 2 and harrier-oss-v1-0.6b are both downloaded (see Tools-and-Models.md). After JP labels more same-or-different node pairs (the calibration set), compare them (rank of true merges, false-merge rate at a cutoff) and pick one default for `embed_candidates.py` (it currently uses EmbeddingGemma 2; add a `--model` option when choosing). The 27B leader needs a larger machine.

- [ ] **Three-way embedding bake-off, next steps** (2026-11-25): (1) JP labels more same-or-different node pairs; (2) repeat `compare_embedders.py` with those labels and more screenshot pairs (and a harder set: crops from the same paper that differ slightly); (3) try the screenshot-matches-its-quote rule as an automatic crop-QA vote (EmbeddingGemma 2 first, since it is US-origin); (4) add Qwen3-Embedding-4B or 8B (Alibaba) to the bake-off, now allowed as a local open-weight model. harrier-oss-v1-27b still needs a bigger machine.

## 2026-11-25: screening the new Zotero ingest by embedding piles
- [ ] **JP reviews the sheet** "LIVES Screening: SysRev - Elicit 2026-11-24 (embedding piles, 3-model vote)" (Google Sheet id 1hM6mqNnrlNzulqqtmyTBfXU5PZJhlRknXYcAnBxdwhA): fill "JP: decision" and "JP: pile" on the Papers tab. Metadata-only copy in `pipeline/misc/screening/2026-11-25-screening-summary.tsv`.
- [ ] **Decide which Zotero set is "the 120+"**: the collection "SysRev - Elicit 2026-11-24" (added 2026-11-24) holds 164 entries = 82 distinct papers (every paper appears twice in the personal library and about twice in the OASIS Lab group copy). The parent SysRev-LLMApp holds 632 older items (607 added 2026-08-20; 119 have a PDF on disk). If JP meant the parent pool, rerun the three scripts on it (`zotero_collection.py`, `screen_dedup.py`, `screen_embed.py`, `screen_to_gsheet.py`).
- [ ] **Zotero cleanup (JP's call):** the Duplicates tab lists the 254 records that duplicate a preferred record; 17 of the 82 papers are already in the older pool and 4 are already seed papers. Nothing was deleted.
- [ ] **Name the new piles:** 11 candidate new task types (for example replication and reproducibility agents (10 papers), plagiarism detection (6), AI-generated text detection (7), risk-of-bias automation (5), grant and proposal review (4), spin and registration (3), PRISMA adherence (3), claim verification (3), causal language (2), statistical-error detection (2)); decide which belong in the study.
- [x] **Policy (JP, 2026-11-25):** open-weight foreign models are allowed if SOTA or near it and run locally; no APIs for foreign models. DNA-VL-STEER-2B's vote in the screening is therefore allowed. Docs updated (Tools-and-Models.md, Skill references).

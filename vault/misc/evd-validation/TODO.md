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

- [ ] **0d. NEXT WEEK, after the Skill refinement: decide which version the EVD pages cite**  
  Where: EVD pages for Thelwall, Huntington-Klein, Shahid, Xu (and Akyon, Liang once downloaded)  
  Citing the published versions shifts page numbers, some quote wording and screenshots. Calendar reminder: Wed 2026-11-25, 10:00 ET.  
  *Source: prompt 48*
- [ ] **0b. Download the two published versions Claude couldn't get**  
  Where: Akyon https://medinform.jmir.org/2024/1/e59258/PDF ; Liang https://ai.nejm.org/doi/full/10.1056/AIoa2400196 (UMD sign-in)  
  JMIR blocked the browser save twice; NEJM AI is paywalled. Drop the PDFs anywhere and tell Claude.  
  *Source: prompt 47*
- [ ] **0c. Decide on EVD page fixes from the version comparison**  
  Where: misc/evd-validation/2026-11-20-pdf-version-diff/README.md  
  Only Huntington-Klein changed substantively, but errors that are in both versions were found. Biggest: the Shahid RankGPT title is wrong (13.79% keeps RankGPT; removing it gives 10.34%). Also decide whether pages should cite the published versions.  
  *Source: prompt 47*
- [ ] **13. Review the proposed PDF-audit corrections and tick the ones you approve**  
  Where: Vault: misc/evd-validation/2026-11-17-pdf-audit-proposed-changes.md  
  185 changes (147 audit + 38 Zhang v3). Start with the 70 marked with the flag symbol. Nothing is applied until you tick and tell Claude; each page is backed up first.  
  *Source: Prompts 29, 32*
- [ ] **14. Decide the 10 HELD fixes**  
  Where: Same file, search 'HELD' (ids 26, 27, 44, 45, 77, 78, 79, 80, 82, 83)  
  These change only the page number in a quote's citation, which touches quotes you are still benchmarking.  
  *Source: Prompt 32*
- [ ] **15. After benchmarking, decide whether Zhang & Abernethy titles and quotes move to v3**  
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
  Where: Skill.md, Skill-references.md, Skill-templates.md, scripts/; full plan in [[Tools-and-Models]]  
  Planned toolchain (JP, 2026-11-20):
  1. OCR: Chandra OCR 2 and OXR-1.0 must agree, with the PDF text layer as a third vote for born-digital PDFs; the page image decides remaining disagreements; add Granite-Docling only if the pilot shows many unresolved disagreements. OXR-1.0 is exempt from the origin policy as long as it is open and runs locally (JP); check its licence. Ripple-65B Preview (Ricursive Intelligence; dense 65B; Apache 2.0; trained from scratch; text only): use a community GGUF build on JP's 128 GB Framework PC (4-bit about 40 GB, 8-bit about 70 GB); the official BF16 (about 130 GB) does not fit and NVFP4 needs NVIDIA GPUs; confirm the developer is US-based and test its extraction quality. Disagreements go to the page image; other tools are fallbacks.
  2. Once the OCR models agree, PyMuPDF and pdftoppm do the highlights and screenshots.
  3. Skill steps: Inkling 2 Mini and Gemma 4 do the first extraction pass locally (backups via hosted APIs: Ripple-65B Preview, Reflection Beam); Claude Opus 5.5 breaks ties and does all writing and judging, effort set per task (see 0h). No alternates (gpt-oss and Olmo 3 dropped). Fast decisions: Perplexity Decider 1.3 (local). Embeddings: EmbeddingGemma 4 (local) for deduplication, linking and screening. Pangram 4.1 via API. Gemma 4 set aside. Model-origin policy (JP, 2026-11-20): the best open and closed US models only; check each model's base model too.
  4. Optional Pangram 4.1 quality-signal checks.
  
  Pipeline requirements to build in: a fixed test set with pass bars per stage; one OCR model by default, escalating to the others; a fixed, resumable script with a config file (no hard-coded paths); a run manifest (model versions, weight hashes, prompts, settings, raw outputs) and containers; swappable models; checks on licences, data storage, screenshot copyright and non-English papers; a README and one-command run; human review kept at the end. Fold in the lessons from the 2026-11-17 PDF number audit, the grader-prompt refinements, the 2026-11-20 version-diff errors and the provenance check. Claude edits Skill.md only with your approval.  
  **Status 2026-11-24 (updated):** GPT-6.2 Sol (reasoning effort High; Medium for simple steps) replaces LlamaParse and Gemini 4 Neon as the PDF reader and bulk extractor (no Google key); Batch APIs for all unattended runs; the d1-ultra PICOST check is ON HOLD (remind JP after the first batch of new papers).  first v2 edits applied to Skill.md (Step 1 parse and PICOST first, Step 3c, Step 6c), Skill-templates.md (QUE rules 9-12, Original wording block, grounding rules, Methods Mermaid dropped), Skill-references.md and Tools-and-Models.md (v2 toolchain). Backup: misc/skill-backups/2026-11-24-pre-v2/. Still open: Google and LlamaCloud keys, the LlamaParse test on the 27 PDFs, the d1-ultra QA calibration on the 147 audit corrections, a Gemini 4 Neon extraction bake-off, reconciling the local vault with the repo vault.  
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

- [ ] **0g. LATER: add GROBID and EmbeddingGemma 4**  
  Where: Quality Signals pipeline; misc/scripts/find_redundancies.py; plan in [[Tools-and-Models]]  
  GROBID to parse reference lists for reference checks in the Quality Signals pipeline. EmbeddingGemma 4 (local, free; Roam notes record version 2, so confirm) to find duplicate nodes, screen new papers from the AI-assisted search, and suggest node links, with Claude Opus 5.5 deciding on each candidate and you confirming. Test on the April redundancy audit first.  
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
  - Usable across countries: model registry (developer, base model, licence, where it runs; US models only), licence and data-protection checks, screenshot copyright rules, non-English test, neutral formats.
  - User-friendly: README.md, config.example.yaml, .env.example, LICENSE (you choose the licences), CITATION.cff, CHANGELOG.md, CONTRIBUTING.md, MODELS.md, sample_data/, docs/.
  
  *Source: prompt 60*
- [ ] **0f. Expand the review: ingest more PDFs via an AI-assisted search strategy**  
  Record the search strategy (databases, tools, queries, dates, screening rules) in the AI Prompt Log. New PDFs follow the naming convention and the refined Skills.  
  *Source: prompt 48*
- [ ] **28. Report the timing differences in Claude's judgments**  
  Where: Methods section of the paper  
  Claude's relevancy calls for rows 46 and 49 and notes for rows 79-82 were made on 2026-11-17, later than the other Claude rows (2026-11-10 to 11-13). Claude's Fidelity/Grounding for the 31 Jay rows were graded on 2026-11-17 against the live app; the other Claude rows on 2026-11-11.  
  *Source: ABOUT TODO 13; prompt 38*

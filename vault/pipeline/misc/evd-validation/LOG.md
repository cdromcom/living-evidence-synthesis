---
log_type: task_log
task: EVD validation and rewriting in GSheet "LIVES - AAA Benchmarking (HAI)"
dates: 2026-11-11 to 2026-11-12
prompter: Jay Patel (JP)
model: claude-opus-5-5
tool: Claude Code CLI 2.1.318
session_id: 321443ce-62a7-41f0-b70f-c71aa5654112
---

# LOG: EVD validation task (LIVES - AAA Benchmarking HAI)

Prompts (verbatim, timestamped) are in [[2026-11-11-evd-validation-gsheet-prompt-log]] and in the sheet's AI Prompt Log tab; they are not repeated here. This file logs what was done, the outputs, how each was checked, the errors made along the way, and what is still missing. Written by Claude (Opus 5.5) on 2026-11-13 from the session history.

## Inputs

- Original sheet (read only): "LIVES - AAA Benchmarking Results", Google Sheets ID 10D9cCEWv9qlydUKgYV0YdLr2E1On4wzl-g9BD1W4zPI, tab EVD.
- Working sheet (edited): "LIVES - AAA Benchmarking (HAI)", ID 1uEBhz2ReUFsXYRdy70UPZ4F_QZhAZmMrmksDWy-pPq8. Tabs: LIVES - EVD (gid 1861272413; renamed from "EVD 1-77"), ABOUT, PICOST (gid 3), AI Prompt Log (gid 4).
- LIVES EVD pages: GitHub repo cdromcom/living-evidence-synthesis, main branch, downloaded 2026-11-11 as a tarball (snapshot folder cdromcom-living-evidence-synthesis-187d84c), folder vault/evidence (78 EVD pages). The live site renders client-side, so its pages were read from this source rather than the web. The local vault (this folder) has renamed EVD files and was not compared.
- Access: claude.ai Google Sheets and Drive connectors; shell; GitHub CLI.

## Work log (outputs and checks)

### 1. Colour coding (prompt 1)
- Read text colours from the original sheet. Inferred the scheme: dark green #38761d = good/correct, dark brown #9e5833 = partial, dark red #990000 = error, medium gray #999999 = table/figure not extracted; verdict text dark gray #434343.
- JP-graded rows: copied each cell's colour from the same row and column of the original (positional copy). Claude-graded rows: coloured from the row's rating (Partially -> brown; Irrelevant/Unmet/Incorrect -> red; Table/Fig Missing -> gray) and from error wording in the note.
- Check: read back 1,084 coloured cells; all matched the plan (43 differed by one shade step from 3-decimal RGB rounding).

### 2. Dropdown chips (prompt 2)
- Added a dropdown to Owner (Jay Patel / Unassigned). Added 17 conditional-format rules (light fill + dark text) on columns A, G, H, J, L, N, S. The Sheets API cannot set per-option chip colours; the colours come from conditional formatting.

### 3. Comparing the two sheets (prompt 3)
- 135 of 192 Claude-row notes were identical across the two sheets. The HAI copy filled the Table/Fig notes for all 48 Claude rows (vs 6 of 56 in the original), 32 naming the missing table or figure as JP does. Both sheets' Claude notes had a median of ~35 words vs ~6 for JP's.

### 4. Style study (prompt 4)
- Compared JP's column P rewrites with column F. Derived JP's pattern: [named models] [prompting] [verb] [N + field + "research reports"] [instrument type], [result vs comparator] ([metric = value]). Rules recorded in the ABOUT tab.
- Flagged possible errors in JP's own rewrites (EVD 26, 33, 35, 38, 41); listed in ABOUT.
- Two trial rewrites (EVD 57, 68) shown; JP replied "Good".

### 5. Drafts round 1, ABOUT tab (prompt 5)
- Matched each "Task for JP" row to its EVD page by title similarity (all 29 >= 0.73). Extracted Description, Methods Context (study design, tools, participants, sample flow, procedure) and Other Notes. Wrote 25 drafts and 4 "-----" (rows rated Irrelevant/Wrong) into new column Q.
- Fact-check: a separate Opus 5.5 subagent checked the 24 non-dropped drafts against their pages and flagged 10 (its summary line said 11, but it listed 10). 9 were corrected (EVD 49, 50, 52, 54, 55, 58, 63, 70, 72); EVD 59 needed no change (its page contradicts itself; the draft already uses the table).
- Renamed tab to LIVES - EVD; wrote the ABOUT tab (purpose, history, column guide, colour key, style, TODOs, uncertainties).

### 6. Missed EVDs and length cap (prompt 6)
- Drafted EVD 28 ("? Skip until late Thu ?") and the 4 rows left as "-----". Cap = 247 characters (JP's longest rewrite, EVD 47 PRECIS-2 row). Rewrote 20 drafts that exceeded it; longest after = 246. The 5 new drafts and the 20 shortened ones were not re-checked by the subagent.

### 7. Practice drafts (prompt 7)
- 7 drafts for EVDs JP had dropped or deleted (EVD 4, 5, 12, 13, 19, 24, 43). Column P unchanged.

### 8. Metric audit and PICOST tab (prompt 8)
- Audit: compared each draft with whether its page reports kappa or F1. Two drafts carried accuracy/agreement beside kappa/F1 (EVD 4, EVD 43) and were cut to kappa/F1 only; other pages report no kappa/F1.
- PICOST: assumed P = Population, I = Intervention, C = Comparator, O = Outcome, S = Study design, T = Timeframe (no definition found in the vault). Three Opus 5.5 subagents filled the six fields for 81 rows (27 papers), each from its LIVES page only. Merged; fixed one wrong page match (row 37, EVD 36, had matched a Tyser page; corrected to Zhang & Abernethy 2024). Wrote the PICOST tab and printed a Markdown copy in the session.
- The extraction agents reported page-vs-rewrite disagreements for EVD 6, 7, 20, 22, 35, 38, 42, 45 (split rows) and 77; recorded in ABOUT.

### 9. ABOUT update (prompt 9)
- Rebuilt the ABOUT tab: PICOST history and section, metric rule, 9 TODOs, uncertainties. Moved ABOUT back to tab 2 (adding PICOST had pushed it to 3).

### 10-12. Linking PICOST to LIVES - EVD (prompts 10-12)
- Column D = live reference =ROW('LIVES - EVD'!E{n}); column C = live EVD number. Column E = HYPERLINK formula whose text and target are the row's source cell; column F = live source label; every E cell carries a source note. Notes are fixed text; column F is authoritative.
- Check (each round): all 81 rows' text, hyperlink target, note and label matched LIVES - EVD (0 mismatches).

### 13. Prompt log (prompt 13, 2026-11-12)
- Searched all Claude Code transcripts on JP's Mac; prompts 1-12 are in session 321443ce. Created the AI Prompt Log tab and [[2026-11-11-evd-validation-gsheet-prompt-log]].

### 14. Comparison drafts for rows JP had rewritten (prompt 14)
- Drafted EVD 27, 30-34 and the three EVD 47 rows in column Q; numbers checked against the pages (including Woelfle Table 2 kappas and Table 1 costs).

### 15. Q31 and PICOST rule change (prompt 15)
- Q31 (EVD 30) reduced to one EVD on novelty, the study's focal peer-review judgment.
- PICOST column E now shows column Q whenever Q has text, else P. Labels now: 30 "Claude draft (col Q)", 9 "Claude draft (col Q); JP's rewrite in col P not used", 7 practice drafts, 35 "JP (col P)". The 9 switched rows got notes, and their O cells were updated to match Q (EVD 30 novelty only; EVD 47 rows lead with kappa). Check: 0 mismatches over 81 rows.

### 16. Logging (prompt 16 and this file)
- Added prompts 13-16 to the AI Prompt Log tab; saved the prompt log into misc/prompts.

## Errors made by Claude during the task (all fixed unless noted)
- First colour plan mapped source colours by text, not position, so common values such as "Missing" took one stray colour; switched to a positional copy before writing.
- A keyword rule coloured EVD 31's Table/Fig note red because the screenshot caption contained "incorrect claims"; removed the keyword rule for that column.
- Round-1 drafts had 10 fact-check issues, 9 needing a fix (step 5). Claude earlier reported these as "11 issues, 10 corrected" in the ABOUT tab and AI Prompt Log; both were corrected on 2026-11-13.
- Skipped rows: EVD 28 and the four Irrelevant/Wrong rows in round 1 (fixed in round 2); Claude-graded rows that JP had already rewritten (EVD 27, 30-34, 47) were not drafted until JP asked (step 14). EVD 26, 29 and 35-42 are in the same situation and are still not drafted (offered, not done).
- PICOST row 37 matched to the wrong page (fixed, step 8).
- Copied PICOST.md into ~/Documents/GitHub without being asked; deleted it straight away.
- Adding the PICOST tab displaced ABOUT from tab 2 (fixed, step 9).
- An early verification script had a bug that reported false mismatches; fixed the script and re-ran (0 mismatches).

## Final column Q drafts (snapshot 2026-11-13)

Kind: "no JP rewrite" = P was empty, "Task for JP" or "? ..."; "practice" = JP dropped the EVD in P; "comparison" = JP's rewrite is in P. PICOST shows Q in all 46 rows.

| Sheet row | EVD | Kind | Column Q text |
|---|---|---|---|
| 2 | 1 | no JP rewrite | Five human annotators labeling 3,063 citation instances to 100 highly cited biomedical reference articles found that 39.2% contained accuracy errors (minor errors = 21.2%, major errors = 18.0%). |
| 5 | 4 | practice (JP dropped) | Compared to the bespoke Idea Novelty Checker (Cohen's kappa = 0.59), the novelty prompt of the bespoke AI Scientist few-shot classifying 32 scientific ideas agreed with experts near chance (F1 score = 0.44, kappa = 0.05). |
| 6 | 5 | practice (JP dropped) | Poe Assistant, GPT 3.5, and Google Bard answering a health research ethics case study on post-trial access to an unproven herbal medicine all failed to explain why that access need not be provided (0 of 3 correct). |
| 13 | 12 | practice (JP dropped) | Compared to two clinician reviewers, GPT 3.5 zero-shot applying the reporting guideline CONSORT-A to 30 implant-dentistry RCT abstracts diverged most on the conclusion item (mean difference = 0.76, though its reported 95% CI excludes it). |
| 14 | 13 | practice (JP dropped) | GPT 3.5 zero-shot applying the reporting guideline CONSORT-A to 30 implant-dentistry RCT abstracts agreed only weakly with two clinician reviewers on most items, least on intervention and objective (Pearson's r = 0.02 and 0.06). |
| 20 | 19 | practice (JP dropped) | GPT 3.5-turbo zero-shot scoring 51 information science research reports on the UK REF scale correlated with a human's scores less when fed truncated full texts than abstracts (Spearman's r = 0.63 vs. 0.67), and least with titles (r = 0.43). |
| 25 | 24 | practice (JP dropped) | Of six LLMs with RAG answering 15 STROBE questions about 39 observational medical research reports, GPT 4-0613 was least accurate (44.1%), below Gemini Pro (49.2%, p < .001) and best-performing GPT 3.5-turbo (66.9%). |
| 28 | 27 | comparison (JP rewrite in P) | Compared to Cochrane reviewers, GPT-4 zero-shot appraising 307 non-randomised studies from 36 Cochrane systematic reviews with the risk-of-bias tool ROBINS-I agreed poorly on overall risk of bias (weighted kappa = 0.13, Kendall's tau = 0.35). |
| 29 | 28 | no JP rewrite | GPT-4 zero-shot verifying 119 "Yes" answers on NeurIPS 2022 author checklists across 15 Computer Science research reports matched hand-labeled ground truth as often as the authors did (accuracy: GPT-4 = 86.6% vs. authors = 86.6%). |
| 31 | 30 | comparison (JP rewrite in P) | Compared to human reviewers, GPT-4 zero-shot reviewing 500 ICLR 2022 and 2023 research reports commented on the novelty of the research 10.7X less often (aspects of each review comment coded by 2 machine learning annotators). |
| 32 | 31 | comparison (JP rewrite in P) | Compared to 8 other LLMs (0 of 13), GPT-4 checking 13 short Computer Science research reports, each with one inserted error, detected 7 errors when given one sentence at a time (5 zero-shot on the whole paper, 6 one-shot). |
| 33 | 32 | comparison (JP rewrite in P) | GPT-4 appraising 112 systematic reviews and 56 RCTs with PRISMA, AMSTAR, and PRECIS-2 cost about 96X more than Mixtral-8x22B (median per 100 research reports: 115.00 vs. 1.20 USD; Claude 3 Opus = 40 USD, GPT 3.5 = 6 USD). |
| 34 | 33 | comparison (JP rewrite in P) | GPT-4 zero-shot feedback on 3,096 Nature-family research reports overlapped with individual human reviewers' comments as much as two human reviewers overlapped with each other (30.85% vs. 28.58%; ICLR: 39.23% vs. 35.25%). |
| 35 | 34 | comparison (JP rewrite in P) | GPT-4 zero-shot choosing the better of 10 constructed abstract pairs picked it only 4 times (40%), swayed by flaws such as positive-result bias, a prompt injection, bombastic language, and the algorithm's name. |
| 44 | 43 | practice (JP dropped) | Human raters, the reference standard for LLMs appraising medical research reports, agreed less as the tools got harder (Cohen's kappa: PRISMA = 0.84, AMSTAR = 0.77, PRECIS-2 = 0.29 weighted). |
| 45 | 44 | no JP rewrite | GPT-4o, the most diverse of 10 LLMs zero-shot reviewing 993 ICLR 2023 research reports on the novel AAAR-1.0 WEAKNESS benchmark, listed less diverse weaknesses than human reviewers (ITF-IDF: GPT-4o = 5.95 vs. humans = 7.69). |
| 50 | 47 | comparison (JP rewrite in P) | Compared to a human rater (Cohen's kappa = 0.81), Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B zero-shot appraising 112 pediatric surgery systematic reviews with the reporting guideline PRISMA agreed less (kappa = 0.40-0.51). |
| 51 | 47 (cont.) | comparison (JP rewrite in P) | Compared to a human rater (Cohen's kappa = 0.80), Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B zero-shot appraising 112 pediatric surgery systematic reviews with the critical appraisal tool AMSTAR agreed less (kappa = 0.27-0.56). |
| 52 | 47 (cont.) | comparison (JP rewrite in P) | Compared to a human rater (weighted kappa = 0.57), Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B zero-shot appraising 56 RCTs from the database PragMeta with the applicability tool PRECIS-2 barely agreed (weighted kappa = 0.01-0.12). |
| 53 | 48 | no JP rewrite | Human annotators labeling biomedical citations for the corpus later used to benchmark GPT-4 and MultiVerS agreed only slightly to fairly on accuracy labels (Cohen's kappa = 0.18-0.31). |
| 54 | 49 | no JP rewrite | Six LLMs zero-shot checking 83 STEM research reports for errors on the SPOT benchmark were rarely confident, reaching full confidence (error re-detected in all 8 runs) in 2 of 498 model-report evaluations, both by o3. |
| 55 | 50 | no JP rewrite | Claude 3.5 Sonnet, GPT-4o, and GPT o1-preview few-shot labeling 172 Coronary Drug Project variables as confounders were inconsistent across prompting methods (Cohen's kappa = 0.16-0.24) and answer-option orders (36.7% of Claude's labels flipped). |
| 56 | 51 | no JP rewrite | GPT-4 reviewing ICLR and NeurIPS research reports scored them higher than human reviewers given only the paper and review form (7.21 vs. 5.88), lower once given area chair guidelines (4.61), and human-level only with prior-year statistics (5.36). |
| 57 | 52 | no JP rewrite | An ICLR 2023 reviewer blind-rated GPT-4 reviews of 7-8 Computer Science research reports as explaining scores about as well as human reviews (4.76 vs. 4.80 of 5), while GPT-4 as evaluator rated human reviews below its own (4.27 vs. 4.65). |
| 58 | 53 | no JP rewrite | ChatGPT 4o, Grok 3, Gemini 2.0 Flash, and DeepSeek V3 zero-shot appraising 10 diagnostic accuracy research reports with QUADAS-2 systematically erred on patient selection, e.g., misreading consecutive sampling in case-control designs. |
| 59 | 54 | no JP rewrite | Claude 3.5 Sonnet, GPT-4o, and GPT o1-preview few-shot labeling 172 Coronary Drug Project variables labeled confounders that experts trimmed from the causal diagram far more often than those experts added and kept. |
| 60 | 55 | no JP rewrite | Google Bard, GPT 3.5, Claude-Instant-100k, and GPT 4 answering 7 health research ethics case studies sometimes missed placebo-arm suitability, risk mitigation, and participant risks with a single prompt, but improved with one query at a time. |
| 61 | 56 | no JP rewrite | Six LLMs (GPT 3.5, two GPT 4s, Claude v1, PaLM 2, Gemini Pro) with RAG answering 15 STROBE questions about 39 observational medical research reports were least accurate on statistical software (33.5%) and funding (35.8%) vs. 68.3% at best. |
| 62 | 57 | no JP rewrite | Compared to a single GPT-4 agent, the bespoke multi-agent reviewer MARG-S (GPT-4) generated more comments that 9 researchers rated "good" on their own research reports (3.7 vs. 1.7 per report; Liang et al.'s GPT-4 reviewer = 0.3). |
| 63 | 58 | no JP rewrite | The bespoke multi-agent reviewer MARG-S (GPT-4) reviewing 30 ARIES research reports recalled more real reviewers' comments than all baselines and humans, with lower precision (recall: MARG-S = 15.84 vs. SARG-TP = 10.62 vs. humans = 9.42). |
| 64 | 59 | no JP rewrite | Grok 3, ChatGPT 4o, DeepSeek V3, and Gemini 2.0 Flash zero-shot appraising 10 diagnostic accuracy research reports with the risk-of-bias tool QUADAS-2 matched a two-expert consensus on 73% of 110 signaling questions (range = 67-77%). |
| 65 | 60 | no JP rewrite | Claude 3 Opus, Claude 2, GPT-4, GPT 3.5, and Mixtral-8x22B appraising 112 systematic reviews with PRISMA (plus AMSTAR and PRECIS-2 sets) quoted the full text almost verbatim to justify ratings (median quote similarity = 99%). |
| 66 | 61 | no JP rewrite | Poe Assistant, GPT 3.5, and Google Bard drafting an IRB standard operating procedure for the initial review of proposals all failed to require a quorum for full board review (0 of 3 drafts), unlike the Mayo Clinic and Harvard Longwood SOPs. |
| 67 | 62 | no JP rewrite | o3 zero-shot checking 83 STEM research reports on the SPOT benchmark caught equation and proof errors best (pass@4 = 62.6% vs. Gemini-2.5-Pro = 36.4%) but no figure duplications (pass@4 = 0% vs. GPT-4.1 = 44.4%). |
| 68 | 63 | no JP rewrite | o3, the best of 10 multimodal LLMs zero-shot checking 83 STEM research reports for 91 author-confirmed errors on the SPOT benchmark, found few errors (recall = 21.1%, precision = 6.1%, pass@4 = 37.8%; Gemini-2.5-Pro recall = 10.1%). |
| 69 | 64 | no JP rewrite | o3-mini, the best of 10 LLMs zero-shot judging whether 4,196 equations from 869 ACL research reports were correct on the AAAR-1.0 EqInfer benchmark, barely beat labeling every equation correct (F1 score = 48% vs. 40%). |
| 70 | 65 | no JP rewrite | o4-mini zero-shot checking 245 withdrawn arXiv research reports caught the error behind the withdrawal within five flagged problems for 59.6% of PDFs at 0.038 USD per paper, close to o3's 64.9% at 8.4X the cost (0.321 USD). |
| 71 | 66 | no JP rewrite | Compared to Gemini 2.5 Pro, Gemini 2.5 Flash, o4-mini, and Claude 3.7 Sonnet, o3 zero-shot checking 245 withdrawn arXiv research reports caught the error behind the withdrawal most often (HR@5 = 64.9% from PDFs, 71.0% from LaTeX). |
| 72 | 67 | no JP rewrite | The bespoke reviewer OpenReviewer (fine-tuned Llama-3.1-8B) reviewing 400 held-out NeurIPS 2024 and ICLR 2025 research reports matched human reviewers' average recommendation (5.4 of 10), while general LLMs inflated theirs (GPT-4o = 7.7). |
| 73 | 68 | no JP rewrite | Compared to GPT-4o, the bespoke reviewer OpenReviewer (fine-tuned Llama-3.1-8B) reviewing 400 held-out NeurIPS 2024 and ICLR 2025 research reports matched at least one human reviewer's recommendation more often (55.5% vs. 23.8%). |
| 74 | 69 | no JP rewrite | A GPT-4o judge comparing reviews of 400 held-out NeurIPS 2024 and ICLR 2025 research reports to human reviews preferred the bespoke reviewer OpenReviewer over every general LLM (win rate = 60-76%), including GPT-4o itself (60%). |
| 75 | 70 | no JP rewrite | Compared to five fine-tuned PLMs and four zero-shot LLMs, the bespoke model Ours-SciBERT, augmented with human and ChatGPT knowledge, best predicted the novelty of ICLR 2022 research reports' methods (F1 = 0.83 vs. Claude 3.5 Sonnet = 0.69). |
| 76 | 71 | no JP rewrite | GPT-4o-mini zero-shot checking 21,041 open-access RCT research reports for alignment with the reporting guideline CONSORT found mean compliance rose from 27.3% in 1966-1990 to 56.1% in 2010-2024 (p < 0.0001). |
| 77 | 72 | no JP rewrite | Shuffling GPT-4's feedback onto other research reports from the same journal or conference cut its overlap with human reviewers from 30.85% to 0.43% (Nature, n = 3,096) and 39.23% to 3.91% (ICLR, n = 1,709), so it is paper-specific (p < 0.0001). |
| 78 | 73 | no JP rewrite | Adding retrieval of related papers (RAG) raised GPT-4o's zero-shot identification of key limitations in 1,000 perturbed research reports on the LIMITGEN-Syn benchmark from 52.0% to 64.2% accuracy, still below human experts' 86%. |
| 79 | 74 | no JP rewrite | GPT-4o-mini zero-shot checking 21,041 open-access RCT research reports against the reporting guideline CONSORT found few reported randomization sequence generation (9.7%) or allocation mechanisms (15.25%). |

## Missing details (not recoverable from this session)
- Who created the HAI copy on 2026-11-11 (Drive created time 17:23 UTC) and how; no transcript on this Mac records it.
- The original grading of the 48 rows marked "Claude" in Graded by (ratings, notes, flags, screenshot URLs; posted 2026-09-04 to 09-18): model, prompts and interface are not in any local Claude Code transcript. Probably claude.ai; check its history.
- How the original sheet "LIVES - AAA Benchmarking Results" (created 2026-08-25) and JP's Phase 1 grading were produced (human work; not logged here).
- Exact Opus 5.5 inference settings (temperature etc.) are not exposed by Claude Code.
- The fetch of the Gemini Decisions API post (Haiku 5.5 subagent) and the PubPeer work in the same session are outside this task and excluded.

## Open TODOs
See the TODOs and UNCERTAINTIES sections of the ABOUT tab (review drafts, unchecked drafts, Irrelevant/Wrong rows, JP rewrites vs pages, contradictory LIVES pages, PICOST review, EVD 1 page fix, Phase 2, unchecked Claude rows). Added since: EVD 26, 29 and 35-42 have no column Q draft.


---

# 2026-11-23 to 2026-11-25 session (one long Claude Code session)

Prompts (verbatim, timestamped, with one-line results): [[2026-11-24-session-prompt-log]]. Session id 675f3ea2-645b-4b0b-acc2-9007848d0536. Models: Claude Opus 5.5 early in the session, Claude Sonnet 5.5 later, with subagents. This section logs what was done, where it lives, how it was checked, and what is unknown.

## Work log (outputs and checks)
1. **Decision-model benchmark** (Runs 1 to 6, n = 66 after drops): Perplexity Decider 1.3, Liquid d1-ultra, Jev and Claude Opus 5.5 against JP's grades on the 77 EVDs; sheets in Google Drive (AAA Benchmarking HAI plus per-model rater sheets). Checks: error analysis per run; JP spot checks.
2. **Vault and repo**: skills backed up and cut (`pipeline/misc/skill-backups/`), repo aligned with the vault (PR 26, merged), redesign decisions (PR 27, merged), benchmarking PRs 8 and 21 merged, 41 labels created. Check: `check_repo_sync.py` (content hashes).
3. **Quality signals**: `pdf_pages.py` (page map, quote finder, crops), `audit_signal_quotes.py` (27 sources, about 1,570 rows), decision-model runs on 734 rows, review sheet v2 with models and dates, provenance scripts, smoke tests of all scripts. Quote audit result after the punctuation rule: 579 verbatim with printed page ok, 123 ok by PDF position, 106 wrong page, 72 quotes not found.
4. **Provenance**: `call_logger.py`, collapsed GAMER-style footer, `pipeline/provenance/AI-disclosure.md` and `model-history.md`, Skill Step 4c.
5. **Design**: two design consults with four models (`pipeline/runs/2026-11-25-design-consult*`), `pipeline/design/LIVES-design-spec.md`.
6. **Web app (PR 29)**: review sidebar (several categories, tooltips, privacy tooltip, fallback when the reviews view is missing), mascot, "Statistical Accuracy" and "Hype/spin" labels. Checked with eslint and `next build --webpack`; not tested in a browser or against the live database.
7. **Statistical accuracy checks**: `stat_checks.py` and `stat_checks_more.py` (percent sums, GRIM, GRIMMER, sample sizes, analytic sample, scale range, confidence interval, ratio, F1 and kappa, effect sizes, accuracy times N, p against CI, pass@k order, delta arithmetic, SD bound, statcheck, confusion matrix, macro averages). Planted-error self-test passes for every kind. On the 27 papers: 4 findings, all in one paper (three estimates outside their own confidence intervals in the Roberts 2023 abstract).
8. **Links**: `check_links.py`; `reverse_links.py` and `build_dgraph.py` list-parsing bug fixed; 32 EVD pages gained caveat back-links; Sarol caveat, Liu question links and the EP-to-CVT link fixed. Result: 0 structural problems.
9. **EmbeddingGemma 2** downloaded (Hugging Face `google/embeddinggemma-2`, 1.4 GB, own environment). Test on the 27-paper set: `embed_candidates.py` and a blinded Sonnet 5.5 second opinion (`merge_judge.py`, run 2026-11-25-merge-judge, 35 calls, about $0.12): no merges recommended among the top 25 CVT and top 10 QUE pairs; 21 of the 35 pairs "group under an umbrella", 14 "keep separate". Files: `pipeline/misc/evd-validation/embedding-candidates/`.
10. **Rules decided by JP** (now in the Skill): PDF page number is fine when the PDF prints none; screenshots closed by default; pastel highlight colors by node type; no pill cap but explore other components; subtle differences between nodes mean do not merge; a human verifies every merge (the models only surface candidates); Inkling 2 Small and Sonnet 5.5 as the two judges (Inkling not wired up yet).

11. **Later in the session (2026-11-25):** Supabase view-only SQL run by JP (3 reviewer aliases created; the site's All verdicts list works); review sidebar with several categories and tooltips, then one unified review and report box (PR 34, pending); logo reverted to the plain turtle; quality row names moved to one registry (`quality-signal-labels.json`); alias-less links fixed in the build and in the vault (177 links); Vercel project "benchmarking-validation" kept out of deployments (`.vercelignore`, folder download note); Inkling 2 Small wired in as a second judge (90 pairs, then 125 pairs across all five node types in total; it said "umbrella" for almost every pair, Sonnet 5.5 kept most separate); design spec section 16 (Supabase dark-mode study); Welcome.md pipeline section restored after PR 26 had overwritten it; History.md, scripts README and this log brought up to date.
12. **Checks run for this entry:** `check_links.py` 0 problems; `stat_checks.py selftest` passes; `quality_labels.py check` 0 unknown names; Welcome.md diagram parsed with mermaid 11.12 in the browser; vault against repo compared with `check_repo_sync.py`.

## Missing details (not recoverable here)
- Results for the early benchmarking messages are summarised; the detailed outputs are in the sheets' LOG and AI Prompt Log tabs.
- Tinker prices for Inkling 2 Small and Mini came from a model-extracted summary of a truncated page: unverified.
- The model of the April 28 batch agents is not recorded.
- Inkling 2 Small has not been called yet.

## Addendum: paper screening by embedding piles (2026-11-25)
- Found the collection "SysRev - Elicit 2026-11-24" in Zotero (personal library, 164 entries, all with a PDF); it is 82 distinct papers (each appears twice, plus the OASIS Lab group copy). 17 of the 82 were already in the older SysRev-LLMApp pool and 4 are seed papers. The older pool has 632 items (119 PDFs on disk).
- Embedded the 82 papers and the 27 seed PDFs (title plus the first 3 pages) with EmbeddingGemma 2, harrier-oss-v1-0.6b and DNA-VL-STEER-2B; majority vote against the six Review-Arena task groups. Result: 22 papers to reporting-guideline compliance, 4 to peer review reports, 4 to error detection, 1 to novelty, and 51 voted NEW by all three models, which cluster into 11 candidate new task types (3 papers fit no cluster). Review sheet created in Google Drive (id 1hM6mqNnrlNzulqqtmyTBfXU5PZJhlRknXYcAnBxdwhA). Nothing in Zotero was changed.
- E-means was read and not used (see Tools-and-Models.md).

## 2026-11-25 (later): SRC skimmability rules and Gemini 4 Neon replaces Opus 5.5
- JP asked for SRC pages (Methods, Findings and related sections) to be skimmable: numbered lists for procedures, short bullets elsewhere, and each linked dgnode first with the model-written summary after it. Added to `Skill-templates.md` ("Skimmability and link order", template and pitfalls updated) and a pointer in `Skill.md`. Existing SRC pages are not restyled yet (TODO).
- JP asked to replace Claude Opus 5.5 with Gemini 4 Neon for demanding and routine work. Swapped every forward-looking role in `Skill.md`, `Skill-templates.md`, `Tools-and-Models.md`, `TODO.md` and `Welcome.md` (history rows and bylines left as written); Opus 5.5 stays as a comparison model. `call_logger.py` now knows `gemini-4-neon` ($3 in, $15 out per million tokens; secondary sources, verify). `GEMINI_API_KEY` is a new `.env` entry for JP to add; no key was seen or used. Nothing has been run on Gemini yet.
- Predictions (not measured) are in the chat reply and the `TODO.md` pilot item.
- Whole-library screening (all Zotero libraries, 17,544 distinct papers) is still embedding in the background (EmbeddingGemma 2 done; harrier running; DNA-VL-STEER-2B next).
- JP asked for "Categories" instead of "piles" in all screening sheets (done in the Elicit sheet: tabs Categories and New category candidates, headers and ABOUT text; scripts, data file names and docs in the repo renamed to match) and for a more formal register in scholarly deliverables.
- Zotero: backup of the database (238 MB, `~/Zotero-backup-2026-11-25/zotero.sqlite`). Merge plan for the personal library only: 103 exact-duplicate groups, 118 records merged into the newest copy, 89 older identical PDFs to the trash; 4 same-title groups skipped (different year or DOI). Not yet run: JP runs `1-dry-run.js` then `2-merge.js` inside Zotero (Tools, Developer, Run JavaScript). Group libraries untouched.
- Gemini 4 Neon: the key is in `.env`; a test call returned HTTP 429 (quota exceeded), so billing or the $100 credit is not active on that key's Google project yet.
- Zotero personal library merged (JP, Zotero closed): 103 duplicate groups, 118 older records merged into the newest copy (moved 157 child PDFs and notes, 12 folder links, 47 tags, 17 fields), 89 older identical PDFs trashed; integrity check ok before and after. Backups in `~/Zotero-backup-2026-11-25/` (`zotero.sqlite` before planning, `zotero-before-merge.sqlite` immediately before the write). Script: `pipeline/scripts/zotero_merge_duplicates.py`. Group libraries untouched.
- Zotero OASIS Lab group library (JP authorized merging duplicates he added): 69 exact-duplicate groups, 81 copies created by JP merged into the newest kept copy (87 child PDFs or notes, 23 folder links, 43 tags, 21 fields moved); only copies created by JP were trashed; in 15 groups the kept copy was another member's, and in 7 of those JP's copy was the newer one but was still the one trashed, to protect the other member's record. 62 duplicate groups with no JP-created copy and 18 with a different year or DOI were left alone. Integrity ok; backup `zotero-before-merge-lib3.sqlite`. Gemini test call still HTTP 429 (free tier) with the key from Project ENIGMA.

## 2026-11-25 (later): Gemini 4 Neon swap reverted
- JP dropped Gemini 4 Neon (the Google billing and login setup would not work; every call returned a free-tier quota error). Reverted to the state before the swap: Claude Opus 5.5 for demanding writing, judging, tie-breaks and checks, Claude Sonnet 5.5 for routine steps, GPT-6.2 Sol for reading PDFs and checking crops and extractions, decision models (Liquid d1-ultra, Perplexity Decider, Jev) as before. Files restored: `Skill.md`, `Skill-templates.md`, `Tools-and-Models.md`, `TODO.md`, `Welcome.md`; `call_logger.py` no longer lists `gemini-4-neon`; the Gemini pilot-gate TODO was removed. Kept: the SRC skimmability and link-first rules, the Categories rename, the Zotero merges. The original mentions of Gemini 4 Neon as a PDF reader (replaced by GPT-6.2 Sol on 2026-11-24) were left as they were. No Gemini call ever succeeded, so nothing was spent.

## 2026-11-25 (later): Gemini 4 Neon back as primary reader and extractor
- A test call to `gemini-4-neon` succeeded after the Google billing account was reopened (about $0.001). JP asked for Neon to have a major role with a supporting cast: Neon reads PDFs and extracts (PICOST), drafts nodes and does routine judgments; every extraction is checked by several models before anything is written (PyMuPDF span search with bounding boxes, the decision models for relevancy, fidelity flags, quote grounding and table or figure grounding); low-confidence and multi-page extractions are re-read by GPT-6.2 Sol and adjudicated by Opus 5.5; Sonnet 5.5 writes the second EVD candidate; Opus 5.5 does the final claim-by-claim EVD check. Updated `Skill.md`, `Tools-and-Models.md`, `Welcome.md`, `Skill-templates.md` (footer example), `call_logger.py` (`gemini-4-neon` price and new `logged_gemini`, smoke-tested at two thinking levels) and `TODO.md` (pilot gate).
- Decision models can flag fidelity but not clear it (our benchmark: reliable on grounding, not on fidelity). Prefer false positives.
- New `pipeline/skills/TIPS.md`: how to reopen a closed Google Cloud billing account (three dots on the account row), the free-tier signs in AI Studio, Zotero close-and-backup rules.

## 2026-11-25 (later): batch runner, four-paper limit, $5.55 cap, manifest
- New `pipeline/scripts/llm_batch.py` (one request format; standard mode and batch mode for Anthropic Message Batches, OpenAI Batch /v1/responses and Gemini Batch; Inkling 2 Small in parallel because it has no batch mode) and `pipeline/scripts/lives_run.py` (runner: 1 to 4 PDFs, cap per batch $5.55 that `--cap` can only lower, repeat-PDF guard by SHA-256, worst-case check before every stage, stop-the-batch rules, run manifest with hashes, versions, tokens, cost and job ids, resume after a crash). Stages: Neon extracts PICOST, PyMuPDF checks and highlights every span (bounding boxes saved), Sol re-extracts flagged findings blind, Opus adjudicates disagreements, then it stops for JP's spot check A. Prompts written: `picost-v1.md`, `recheck-v1.md`, `adjudicate-v1.md`.
- Tested (about $0.30 in total): one-word standard calls and one-request batches on all four providers (all returned and parsed); the runner on a one-page synthetic paper in standard mode and in batch mode (Gemini batch finished in minutes); recheck (Sol) and adjudicate (Opus) stages; the cap refusal, a halt before submission under a tiny cap, the four-PDF limit (59 PDFs refused), and the dry-run estimate on four real papers (expected $1.36 in batch mode, $2.73 in standard, worst case $1.92 and $3.85). Test runs were deleted. No real paper has been run: the pilot is for later (JP).
- Decision: no local extraction stack (Chandra, OXR, Inkling 2 Mini, Gemma 4): frontier hosted models plus PyMuPDF and the decision models; accuracy first. Batch size is four papers (was five).
- `check_repo_sync.py` now ignores batch-runner outputs (`pipeline/runs/<date>_batch<N>/`, `test-*`, the ledger).

## 2026-11-25 (later): whole-library screening finished; real cost test of the runner
- Screened all 7 Zotero libraries: 19,992 items, 17,544 distinct papers, 3,441 sheet rows (every paper in the Metascience, SysRev-LLMApp, Elicit and Include-CA-Rep folders plus papers elsewhere that are close to the seed and Elicit papers). Three local models (EmbeddingGemma 2 28 min, harrier 59 min, DNA-VL-STEER-2B 2.8 h). Category assignment on the seed leave-one-out test: majority 77%, EmbeddingGemma 73%, harrier 81%, DNA-VL-STEER-2B 88% (n = 26). Closeness on proxy labels: any-model rule sensitivity 94%, specificity 99.8%, AUC 0.999; majority rule sensitivity 90%. New categories weak (silhouette 0.017, 30 clusters). Open access from OpenAlex: 6,277 of 12,188 DOIs. API cost $0.
- A first run mislabelled papers in `SysRev-LLMApp / SysRev - Elicit 2026-11-24` (folder-path rule) and left them out of the reference set; found by reading the first sheet rows, fixed in `screen_all.py`, analysis rerun on cached embeddings, sheet replaced (the first sheet is in the Drive trash).
- Real runner test (one 10-page paper, standard mode, $1.24): Neon extraction $0.60 (4 min), Sol recheck $0.19 (3 min), Opus adjudication $0.45 (40 s). First attempt hit Neon's 20,000-token limit ($0.35, stopped by the 1.5x rule); budget raised to 48,000. 24 of 29 findings were sent to recheck because Neon marked `multi_page` on single-page findings, and all 24 counted as disagreements because Neon listed one more number than Sol (Opus sided with Neon every time). Fixed: multi_page now judged from the pages actually cited, and a disagreement means Sol has a number Neon lacks.

## 2026-11-25 (later): token budgets from the 27 seed papers
- Measured pages, words and real input tokens (Claude and Gemini token counters) for the 27 seed PDFs (median 18 pages, 49,000 Claude tokens; largest 60 pages, 165,000) and EVDs per paper (1 to 6, median 3). The extraction prompt returned 29 findings for a 10-page paper, so `picost-v2.md` caps findings at 12 and reports omissions. Output budgets are now per stage (Neon 24,000 + 1,000 per page up to 64,000; Sol 3,000 + 1,000 per flagged finding up to 16,000; Opus 1,000 + 450 per dispute up to 8,000), input is priced per provider (Claude 2,800 and Gemini or Sol 1,400 tokens per page), and Sol and Opus get only the cited pages. Table in `Tools-and-Models.md`.
- Same 10-page paper, standard mode: $1.24 before, $0.52 after (Neon $0.46 with 12 findings, Sol $0.06 on 6 flagged findings, no adjudication needed). The 1.5x rule had stopped the run once because the expected cost assumed half the budget; the expected share is now 0.8 for extraction and 0.7 for the other stages.

## 2026-11-25 (later): evidence tiers, debate drafting, quality-signal voting, review sheets (specs and first code)
- JP's decisions: (1) draft EVDs (and QUE, CLM, EP, CVT) with Sonnet 5.5, GPT-6.2 Sol and Neon (Medium) in a draft, critique, revise and vote loop checked for accuracy, character length and readability; Sol and Sonnet decide, Neon breaks ties, Inkling picks for benchmarking only; (2) Neon joins the quality-signal raters with Opus and Sol, majority voting, every individual and aggregate judgment logged in a benchmark sheet; (3) Neon stays at High for extraction; (4) replace the findings cap with tiers: primary EVDs answer the RQ, secondary are meta or contextual about primary ones, tertiary are possible; the pilot with JP decides.
- Written: `Skill.md` ("Drafting by debate", "Who checks crops and quotes", quality-signal voting and logging, tiers in the runner paragraph), `Skill-templates.md` (EVD tiers, SRC Findings order), `pipeline/templates/T - EVD tiers.md` (tier template and spec), `T - Evidence.md` (tier fields), `pipeline/skills/Review-sheets-spec.md` (run review sheet, drafts and debate, Quality Signals benchmark sheet), `Tools-and-Models.md`, `Welcome.md`.
- Code: `prompts/picost-v3.md` (RQ and three tiers with caps 6, 4, 2 and `omitted` notes); `lives_run.py` requires `--question` and prints tiers; new `run_to_gsheet.py` builds the step-by-step review workbook (Findings tab with tier, flags, recheck and JP label columns). Tested on a synthetic paper (primary and secondary EVD correctly tiered, secondary `supports` its primary; $0.07). The debate stage, the quality-signal rater runs and the benchmark sheet are specified, not built (TODO).
- Four-paper seed pilot estimate (Woelfle, Sarol, Bougie, Tyser; upper bound with full PDFs in the later stages): batch mode $2.29 expected and $2.73 worst case, standard mode $4.58 and $5.46 against the $5.55 cap. Gemini inline batches are limited to 19 MB per request and these four PDFs are 21 MB as base64, so the Neon stage would run in standard mode.
- Brought the other documents in line with the new pipeline (JP's request): `Welcome.md` (read node, folder tree with `screening/`, tiers in the node table, the "How to add a new paper" steps now use `lives_run.py` with the research question, quality-signal voting, further reading), `Vault-structure.md`, `Skill-references.md` (atomicity and tiers), `Quality-signals-spec.md` (who rates, majority voting, benchmark sheet), `model-history.md` (era 4), the 2026-11-24 ingest budget note (marked superseded in part), `Skill.md` workflow-at-a-glance, and `TODO.md` (local extraction items marked dropped; five became four).

## 2026-11-25 (later): Gemini File API, checks, drafting by debate and quality-signal rating built; EP retired from the pipeline
- JP's decisions: build the Gemini File API router; build debate drafting, quality-signal rating and the decision-model **checks** (the word is "checks") for the four-paper test; extract and write QUE, CLM, CVT as well as EVD; Inkling writes the nodes on the side (benchmark only); quality-signal benchmark rater is Inkling only (no Sonnet); free scripts and cheap decision-model checks are enough for quote checking, with Sol vision on flagged, low-confidence and 10%-sampled crops and Opus only on rare disputes; drop EP from the pipeline.
- Built: `llm_batch.py` File API (`gemini_upload`, `upload_pdfs`; PDFs of 6 MB or more; tested for a standard call and a batch job; files deleted at run end), image inputs for all three providers, and the Inkling system-prompt fix (the first shadow run never sent the extraction prompt to Inkling, so its prose answer did not count); `lives_stages.py` (`checks`, `draft`, `qs`); six prompts (`draft-nodes-v1`, `critique-revise-v1`, `vote-v1`, `claim-check-v1`, `rate-signals-v1`, `vision-check-v1`); `lives_run.py --skip`; new review-sheet tabs. Adjudication budget floor raised (Opus ran out of tokens at 1,450 on one dispute).
- Smoke test on a one-page synthetic paper, all stages, $0.61: checks found the prose finding scored low on table grounding, so the table question now applies only to findings that rest on a table or figure; drafts, votes, tie-break, claim checks and 25 quality signals ran and are in the review sheet.
- EP: removed from the pipeline instructions, drafting loop and docs (`Skill.md`, `Skill-templates.md`, `Skill-synthesis.md` banner, `Skill-references.md`, `Vault-structure.md`, `Welcome.md`, `T - EP.md` marked retired and kept in place). Not touched: the 21 EP nodes, the web app and the scripts that read them (TODO: JP decides).
- Estimated cost of the full four-paper pilot: about $6.7 in batch mode and $13 in standard, above the $5.55 cap (JP decides).

## 2026-11-25 (later): reflection and hardening; screening sheet ready for new papers
- Reflection written (`pipeline/skills/Pipeline-design-and-longevity.md`): layers, change recipes (model, package, prompt, template, Obsidian graph, fork for another review), robustness over time, budgets and ethics, weak points in order, ideas for the app and repository.
- Hardening: `pipeline/config/models.json` (registry: models, prices with sources, roles, origin policy) and `pipeline/config/pipeline.json` (limits, budgets, thresholds, ethics switches); `scripts/config.py`; `llm_batch.py`, `call_logger.py`, `lives_run.py` and `lives_stages.py` read them instead of constants; the origin policy is enforced in code; `scripts/selftest.py` (36 offline checks, no cost); pinned `requirements.txt`, `requirements-screening.txt`, `.env.example`; an em-dash lint rule for drafted nodes. A live call still worked after the refactor.
- An edit with a loose text anchor damaged `lives_run.py`; restored from the last pushed copy. The vault has no version control, which is the first weak point in the reflection.
- Skill.md: writing rules for longer sections (no em dashes, at most one info callout, write like a human, skimmable, numbered lists for steps and bullets otherwise, no redundancy), carried into the drafting prompts.
- Screening: the overnight whole-library run finished (embedding 4.3 h); the review sheet is `1R70T7JJD3-RDM5kPc6-rI1ZZ2qCb82TVE19OjzyuyrA`. Added a **Stable id** column and an only-new mode (`screen_all_to_gsheet.py --only-new`) so new papers append without touching JP's labels; the sheet was rebuilt before JP had labelled anything (old sheet in the Drive trash).

## 2026-11-25 (later): EvidencePatterns archived; paper-level questions; pilot run 1 started
- JP's decisions: archive the existing EPs and remove them from the LIVES web app (CLMs can be cross-paper: the template lists every paper that makes a claim; 8 of 31 CLMs already list two to four papers); raise the cap to $8 for the pilot, batch mode only; run extraction and checks first and drafting and ratings second (a new batch with a fresh cap); no research question is supplied: the models read each PDF, find its questions (questions, aims, goals, hypotheses, statements) and reframe them as clear, granular questions that EVDs, CLMs and CVTs link to.
- Archive: `pipeline/misc/archive/evd-patterns-2026-11-25/` (21 EP nodes, Base, template, the 87 changed pages as they were, removed sections, restore guide). 60 EVD and 27 QUE pages lost their EP link sections. Scripts (`check_links.py`, `vault_to_gsheet.py`, `embed_candidates.py`, `merge_judge.py`, `compare_embedders.py`, `add_link_aliases.py`), the MkDocs nav, hook and CSS no longer use EPs. `check_links.py` reports 211 nodes and 0 problems. Review-Arena evidence strength was computed with EP counts and is annotated, not recomputed.
- Web app (repo): EP removed from the node types, graph builder, forms, quality table, home tiles, About and Contribute pages; the narratives page keeps its text but no longer links EP nodes; graph data regenerated (211 nodes, no EP edges); `tsc` and `eslint` pass; a local `next build` could not run (the worktree's node_modules symlink), so the Vercel preview is the check.
- Prompts: `picost-v4.md` (finds the paper's questions first; findings, claims and caveats link to them), `draft-nodes-v2.md`, `critique-revise-v2.md`. Review sheet: new tab "Questions found" and a column "Answers question(s)". `--question` is now optional context. `--resume --new-batch` starts a second batch of a run with a fresh cap. Config: cap 8.00 for the pilot (revert to 5.55 afterwards unless JP says otherwise).
- Pilot run 1 (2026-11-25_batch01): Woelfle, Sarol, Bougie, Tyser; batch mode; extraction and checks; Inkling shadow. No supplement files were in the folder (JP said run anyway).

## 2026-11-25 (later): screening sheet narrowed to 358 rows, abstracts added
- JP said DNA-VL-STEER-2B did best and asked not to screen 3,000 papers. The Papers tab now sorts 358 light green rows first (all 3 models close to the seed and Elicit papers, or 2 of 3, or DNA-VL-STEER-2B; seed duplicates excluded), ranked by DNA-VL-STEER-2B similarity, with a column "Screen this? (suggested)" and an Abstract column after the title (Zotero abstract, or the start of the PDF or web page). 3,083 white rows remain for completeness (about 480 are single-model hits). New sheet `1R70T7JJD3-RDM5kPc6-rI1ZZ2qCb82TVE19OjzyuyrA` (the previous one had no labels and is in the Drive trash); the PDF text needed illegal-character cleaning for the spreadsheet.

## 2026-11-25 (later): Skill split in two; vault version control
- `Skill.md` (64 KB) is now two files: part 1 `Skill.md` (35 KB, the step-by-step procedure for one paper, with a short pointer wherever a section moved) and part 2 `Skill-controls.md` (34 KB: the batch runner rewritten as a structured section and brought up to date, run records, cost controls, drafting by debate, Step 4c footer, matching and merging, who checks crops and quotes, Step 6e, Module Q). A line-by-line check against the backup (`pipeline/misc/skill-backups/2026-11-25-pre-split/Skill.md`) found only the three batch items (11, 11a, 11b) and three lifted headings changed; every other line is verbatim in one of the two files. Cross-references in Welcome, Vault-structure, Skill-templates, Quality-signals-spec, Tools-and-Models and `call_logger.py` were updated.
- Vault version control: JP installs Obsidian Git. Added a vault `.gitignore` (PDFs, local run outputs, backups, volatile Obsidian state) and a TIPS entry; `check_repo_sync.py` does not mirror the vault's `.gitignore`.

## 2026-11-25 (later): changes after pilot run 1, at JP's request
- Dropped Inkling and the open-model shadow benchmark everywhere (code, config role, sheets, docs); spec archived. Second merge judge is now GPT-6.2 Sol (`merge_judge.py --second`).
- Questions: `picost-v5.md` takes at most 3 per paper, only from the Abstract and Introduction (v4 gave 19 for 4 papers).
- Number flag loosened (flag only if under half of a finding's numbers, ignoring single digits, are in the PDF text).
- `checks_vision` and `checks_opus` run in standard mode; stragglers are cancelled 5 minutes after all but about 10% of requests finish and go to human review; `--fast` runs everything in standard mode with drafting and ratings at the same time.
- "Runner" renamed "paper processor" in the docs. Skill-controls.md has a plain explanation of flagging, the 30-minute plan and the planned question consolidation.
- Test on the synthetic paper in fast mode: finished in 2 min 8 s, $0.56, 1 question found.

## 2026-11-25 (late): JP's design decisions after the pilot
- No caps on questions, findings, EVDs, CLMs or CVTs (`picost-v6.md`); repeated questions within a paper are kept.
- Drafting: only primary EVDs go through the three-author debate; everything else is one Sonnet 5.5 draft.
- Quality signals: two raters, Neon (High) and Opus 5.5; Sol adjudicates only disagreements (`adjudicate-signals-v1.md`).
- Checks: Sol vision looks at the crop of every finding and may answer cannot_verify (`vision-check-v2.md`); cannot verify goes to a person.
- Built `consolidate_questions.py` (unified, nested questions); review sheet gets Metrics and Question groups tabs; sheets embed pictures in cells.
- Reruns started: `2026-11-25_batch02` (the four pilot papers again) and `2026-11-25_batch03` (random sample of four other seed papers, seed 20261125; list in `runs/sample_2026-11-25.json`).

## 2026-11-25 (night): results of the reruns and bugs found
- Runs: `2026-11-25_batch02` (Bougie, Sarol, Tyser), `2026-11-25_batch03` (random seed sample: Idahl and Ahmadi, Shahid, Hasan, Liu and Shah), `2026-11-25_batch04` (Woelfle alone, standard mode: 12 minutes for the whole pipeline, $4.60).
- Bugs fixed: Neon (High) quality-signal budget too small (all ratings lost); claim check read only the primary part of the card (mass false fails); two batches submitting at once shared one temp file; the straggler timer started at once for a one-request stage; `vision-check-v2` returned cannot_verify for 80% of findings (now `vision-check-v3`); findings with no crop were shown as "needs JP" (now "cannot verify"); Gemini batch refuses more than 65,536 output tokens, so large extractions (Woelfle) need standard mode and a 25-minute timeout.
- Open: about half of the "cannot verify" results have no crop because the quoted span was not found in the PDF text; claim-check fails are 30% of nodes and have not been reviewed; the Jev decision model returned an unknown-model error in earlier runs.

## 2026-11-26: sheets restyled and filed
- All sheet builders now share `sheet_style.py` (Lato, Butterick and Few rules; see Review-sheets-spec.md). The three review sheets and both screening sheets were rebuilt and re-uploaded (none had JP labels yet).
- Drive: private folder `SysRev LLMApp (LIVES)` with subfolders 01 to 04 and 99; every LIVES sheet except JP's two AAA Benchmarking sheets was moved in and renamed to `LIVES - <Area> - <date> - <what>`. New screening sheet ids are in TODO.md.
- The old whole-library screening sheet was moved to 99 Archive instead of trashed (the trash call was blocked); trash it when ready.

## 2026-11-26 (later): JP's decisions
- Jev dropped everywhere in the live pipeline (code, config, docs, signals sheet); old benchmark folders keep it as history. The decision models are Perplexity Decider 1.3 and Liquid d1-ultra.
- Pilot cap is $6 per batch. Standard mode is fine for piloting; JP is asked standard or batch every time papers are given (`--mode` is now required for a new run).
- Claim check: `claim-check-v2` (pass, minor, fail); questions are no longer claim-checked. Reran on batch02 to batch04 in standard mode ($0.81, $0.79, $0.38).
- Sheets use Spectral for column names and Google Sans for data; row heights are estimated because Google Sheets does not grow imported rows.

## 2026-11-26 (night): more decisions
- "Claim check" renamed node-detail check (`node-detail-check-v1.md`), because claim means CLM. Questions stay unchecked there (they have grounding quotes and screenshots); EVDs matter most.
- Default sheet text size is 11. Macros for Google Sheets: `pipeline/apps-script/LivesStyle.gs` (not yet run inside Google Sheets).
- New tab "Low decision-model scores" in the review sheets: the 74 EVDs below 0.60 with what the models saw. All 74 passed or got only notes from the node-detail check.
- AAA Benchmarking (HAI) moved to `05 AAA Benchmarking`; AAA Benchmarking Results could not be moved with the connector's permissions (move it by hand).

## 2026-11-26 (late): four pilot papers re-extracted with picost-v7
- Runs: `2026-11-26_batch05` (Sarol, Bougie, Tyser; standard mode; three caps used: $5.77, $5.80, $3.08), `batch06` (Woelfle, failed: finishReason CONTINUATION), `batch07` (Woelfle with `--extract-effort medium`, $1.27 + $2.68). Three-papers-per-batch rule and review gate set aside for today by JP (max_papers 4, `--waive-review`); revert max_papers to 3.
- PDF page only in the extraction, recheck and adjudication prompts; printed pages from the page map in code. Quote repair and match levels in the spans stage. Quality-signal quotes get a boxed, highlighted screenshot in the raw tab.
- Results, 3 papers: 0 of 158 spans not found (was 12 of 297); 42 of 158 differ from the PDF in a symbol or punctuation mark; 16 of 60 findings still have a statement number missing from the Numbers list (was 60 of 141). Woelfle: 14 exact, 48 letters_digits, 2 repaired, 1 not found of 65 spans; 3 of 16 findings with a gap.

## 2026-11-26 (night): vision check, anchors, supplement correction
- `quote_vision_check.py` (Claude Sonnet 5.5, batch): of 41 extraction quotes that differ from the PDF text layer, the model's quote equals the printed page in 36; the text layer equals the print in only 13. (Corrected later the same day: the supposed wrong-number error in Bougie EVD E-F10, quote 3, was a false alarm: the screenshot highlight was hidden under a shaded table row. Highlights are now drawn over the text at 35% opacity.) Policy (JP): spacing, hyphenation and similar small differences are fine; the meaning must not change.
- Anchors: raters return page plus first and last words; code copies the exact PDF text. Not extended to extraction spans, because the text layer loses meaning-bearing symbols (superscript > in GAR>).
- `focused_extract.py`: corrects findings from supplementary Word files. Woelfle (batch07) supplement in `sysrev/dgraph/source/pdfs/Woelfle et al. 2024 - Supplementary` (mmc1 to mmc4 are figures, mmc5 holds the methods and Supplementary Tables 1 to 3). 8 findings corrected: 10 numbers and 13 quotes added; 6 EVDs now pass after rework; E-F1, E-F13, E-F15 still need JP review.
- Sol 6.2 price: OpenAI's page shows $2 in / $10 out standard and $1 / $5 batch (no increase); registry set to those values.
- Sheet tabs now carry the node type in their titles (EVD, QUE, CLM, CVT).

## 2026-11-26 (late night): verification layer, quote check stage
- `quote_check` stage (Sonnet 5.5 reads a screenshot of every quote, including questions, claims and caveats; standard mode, about $0.004 per quote): batch05 157 quotes checked, 151 equal the print, 2 flagged for a meaning change; batch07 63 checked, 58 equal.
- Highlight bug found and fixed: the quote highlight was drawn behind the page text and vanished under shaded table cells (Bougie Table 5), which made a screenshot point at the wrong row.
- `lives_verify.py` (verify stage): Sonnet 5.5 and the two decision models (Perplexity, Liquid) verify every PICOST slot (one row per slot), quote, QUE reframing, CLM, CVT and quality rating; majority vote and mean per item; JP's columns are open. Sheet tabs: "Verification (all nodes)", "Verification summary", "Verification by node type". 948 items across batch05 and batch07: Sonnet judged 89% correct, Perplexity 75%, Liquid 76%, majority vote 78%. No JP ground truth yet.

## 2026-11-26 (night): d1.2-ultra, screenshots, failure analysis
- Liquid decision model switched from d1-ultra to d1.2-ultra; the old scores were kept next to the new ones (verification tab columns X-Y, checks tab column T).
- d1.2-ultra reads screenshots. Digit comparison on quotes works (60 quotes, pairwise AUC 1.0), word comparison does not (5 of 8 correct quotes failed), so only digit comparisons on quotes vote.
- Corrected denominators: earlier totals for CLM, CVT and QUE mixed in the quote-versus-print rows. Judgment rows only: CLM 9 of 15 not passed, CVT 16 of 28, QUE reframing 18 of 21.
- Opus 5.5 classified 48 (batch05) and 22 (batch07) sampled failures; PICOST failures were all "value outside the shown passage" in the sample (the verifier saw only the cited pages).
- Anchors rerun (`test-anchors`, Sarol, quality signals): quotes found are the same as in the non-anchor run (Neon 20, Opus 18, Sol 2) and all now carry the exact PDF text.

## 2026-11-26 (late night 2): Methods context, numbers check, Findings tab
- Verifiers now see page 1 and the Methods pages for PICOST slots; claim, caveat and question checks judge meaning, not wording. Old scores kept (verification tab columns AD-AF).
- Numbers check: 12 findings had statement numbers that were not in the text of the cited pages; Liquid d1.2-ultra found 34 of 48 numbers on the screenshots (6 of 48 with one digit changed also scored high); 9 numbers are for JP (Bougie F13: 0.78, 0.72; Tyser F6: 2.84, 2.52, 2.56, 3.57; Tyser F12: 10; Tyser F18: 500, 1,000).
- Findings tab: merged screenshots are images in column S; candidate EVDs from Sonnet 5.5, Sol 6.2 and Neon, and the chosen EVD, are in columns W-AA.
- A failure-analysis rerun reused saved answers of an earlier sample under the same stage name; fixed with a new stage name per run.

## 2026-11-26 (late night 3): notes for the paper
These are the findings and design decisions from today's pipeline work, written so they can be lifted into a methods or results section. All numbers are from review sheets batch05 (Sarol, Bougie, Tyser) and batch07 (Woelfle); there is no human ground truth yet, so agreement figures are agreement between models, not accuracy.
- **Design.** Every extracted item is judged by a foundation model (Claude Sonnet 5.5, which reads screenshots) and two decision models (Perplexity Decider 1.3, text only; Liquid d1.2-ultra, text and images). Items: 456 PICOST slots, 220 quote-versus-print checks plus 63 quotes behind questions, claims and caveats, 21 QUE reframings, 15 CLM, 28 CVT, 145 quality ratings. Majority vote and mean score are reported next to each model.
- **Quote fidelity.** Of 41 quotes whose model text differed from the PDF text layer, the model quote equalled the printed text in 36; the PDF text layer equalled print in only 13 (it drops superscripts and symbols and stores "þ" for "+"). So the text layer is not a safe replacement for the model's quote. A highlight drawn behind page text had been hidden by shaded table cells and made one correct quote look wrong (Bougie EVD E-F10, quote 3); highlights are now drawn over the text at 35% opacity.
- **Screenshot reading.** Sonnet 5.5 read 157 quotes in batch05 (151 equal to print, 2 with a meaning change) and 63 in batch07 (58 equal). Liquid d1.2-ultra compares digits on a screenshot reliably (60 quotes, pairwise AUC 1.0 against copies with one digit changed; 98% agreement with Sonnet on 228 digit-containing quotes) but not words (it scored 18 of 55 correct no-digit quotes below 0.5). Quotes without digits are checked by Sonnet 5.5.
- **Locating text.** d1.2-ultra's `box` answer found a quote on a 100 dpi page image with a median intersection over union of 0.57 against PyMuPDF word boxes (40 quotes; 65% at 0.5 or more, 23% at 0.8 or more). PyMuPDF remains the locator; d1.2-ultra could only crop a rough region when a quote is not found.
- **Decision models.** d1.2-ultra scored 20% of 929 text items below 0.5 against 25% for d1-ultra and agreed with Sonnet 5.5 on 94% (d1-ultra 91%). Agreement between verifiers by task is in `skills/Skill-controls.md` (PICOST slots 88-94%, quote text 99%, QUE reframing 67-73%, CLM 73-93%, CVT 89-96%, quality ratings 72-86%). Perplexity decided 27 PICOST and 14 quality-rating items where Sonnet and d1.2-ultra split, and was outvoted on 10 and 17.
- **Context matters.** Adding page 1 and the Methods pages to the verifier input lowered the share of PICOST slots scored below 0.5 from 29% to 19% (Perplexity) and from 25% to 19% (d1.2-ultra); population slots 47% to 29% and timeframe slots 28% to 15% for d1.2-ultra. Judging claims, caveats and rewordings for meaning instead of wording lowered the share below 0.5 from 81% to 56% (Sonnet), 64% to 41% (Perplexity), 61% to 47% (d1.2-ultra).
- **Kinds of problem found** (Opus 5.5 classification of 65 sampled items, batch05 and batch07): PICOST slots whose value is defined outside the shown pages (population, design, timeframe); claims and caveats that add scope or certainty ("cost-efficient and scalable", "self-enhancement bias"); question rewordings that drop or add an outcome; quality ratings whose quote does not show why. Sampled rows and their sheet locations are in the tab "Failure analysis (sampled)".
- **Numbers.** Checking statement numbers against the numbers list produced 18 flags on 76 findings, mostly false alarms (a comma in 1,000, the 23 in "NeurIPS 23", minus signs). Checking them against the text of the cited pages flagged 12; looking the missing numbers up on screenshots with d1.2-ultra found 34 of 48 (6 of 48 changed numbers also scored high); 9 numbers remain for a person (Bougie F13, Tyser F6, F12, F18).
- **EVD style.** JP's rules: named models, N and field, comparator, at most 247 characters, one or two sets of parentheses, no brackets, no all-caps words, F1 score overall and per class instead of precision, recall, macro-F1 and micro-F1. Redrafted Woelfle EVDs: 16 EVDs, 1 to 2 parenthesis sets each (one has none), no flagged capitals; 18 of 31 nodes pass the writing-rules check; 5 EVDs are marked for JP review. PICOST is scaffolding for the four judgments that matter in the LIVES app (selection, fidelity, grounding of the quote, grounding of the table or figure).
- **Costs.** Verification: Sonnet about $0.4 per run for PICOST and $0.4 for the rerun; decision models cost cents; quote check about $0.004 per quote. A Woelfle redraft (one paper, standard mode) cost $0.82 more than the earlier draft ($2.74 for the run at that point).
- **Models reviewed.** A web survey (secondary sources) found no model clearly better than the current extraction, second-reader and adjudication models; Claude Fable 5.2 leads the Intelligence Index page found and is worth testing as adjudicator; Harrier-OSS (already local as `harrier-oss-v1-0.6b`) and MinerU or Marker are worth testing for question clustering and for scanned PDFs. See `skills/Tools-and-Models.md`, "Model review and vision tests".
- **Limits to state.** No human ground truth yet (labeling queue in the verification tabs); Liquid's published decision-index figures are its own; the failure classification is by a model and needs JP's check; Opus 5.5 classified, so classification is not independent of the Claude family used elsewhere.

## 2026-11-26 (late night 4): quality signals, full test with the earlier code
- Quality signals now run after every batch (Module Q in `Skill-controls.md`); 27 signals are rated (added sample-size-estimation and study-type). Four pilot papers rated with Neon (High) and Opus 5.5, Sol adjudicating: both raters agreed on 24 to 25 of 27 signals per paper, no signal ended without a majority. Billed cost per paper $0.45 to about $0.60 in batch mode (Sarol: Neon $0.29, Opus $0.15, Sol $0.02); rating took about 11 minutes including the batch wait.
- The earlier provenance code was fixed and wired in (`provenance/`, run by `qs_export.py`): ORCID matching and notice filtering for retractions, lookup of preprints by arXiv id or title, retracted-reference count, a GitHub, Software Heritage and Zenodo checker for code, a DataCite, Zenodo, OSF and Hugging Face checker for data, FAIR sub-scores without the arbitrary +2, a link checker, registry checks, funding and affiliation facts, a store with dates and response hashes. Hand checks found and fixed: a README with numbered run steps marked "no run instructions", "Meta-Research Innovation Center" matched to the vendor Meta, PDF ligatures and a page number joined onto DOIs, timeouts labelled dead.
- Findings worth reporting: OpenAlex's author-id match flagged a 2017 letter about a retraction as a retracted work for a Woelfle author (now ignored); for Tyser, OpenAlex matches three co-authors to a retracted preprint (a person must confirm); Tyser's main text has 3 dead links (openreviewer.com and paperswithreviews.com do not resolve or answer 409); Woelfle's code repository has no licence; Sarol's code is MIT-licensed but not archived; the data of Sarol and Woelfle are on GitHub only, with no persistent identifier; no pilot paper has a registration.
- The model ratings agree with the live-site tags (curated Aug 2026) on 14 to 17 of 26 signals per paper. Differences are most often a validity domain rated some-concerns against low-risk or high-risk on the live site.
- Not rated by the runner: TRIPOD-LLM rows, Pangram (only on JP's command).
- Side panel in the web app (branch `feat/quality-signal-drawer`): click a signal to see scores, quotes with screenshots and code-only checks.
- MinerU and Marker: see `skills/Tools-and-Models.md`.
- Fixed while doing this: the two manifests (batch05, batch07) had mode "standard", so earlier reruns, including the Woelfle EVD redraft, ran in standard mode; both are set to batch.

## 2026-11-26 (late night 5): cascade, writing rules, table parsers, macro
- Verification now runs d1.2-ultra and Perplexity first and calls Sonnet 5.5 only when they disagree (JP's rule). Measured on the existing data: Sonnet would be called for 104 of 671 items (15%); PICOST slots 13%, QUE 29%, CLM 20%, CVT 4%, quality ratings 23%. Quotes are still read by Sonnet on screenshots. Earlier runs called Sonnet for every item.
- The reading-grade limit (Flesch-Kincaid 14) is removed from the writing-rules check; the Reading grade columns were deleted from the Drafts and Writing-rules tabs of both live sheets.
- Marker and MinerU are being tested for table cells only on the 27 seed papers (`misc/evd-validation/table-parsers/`).
- The LIVES style menu disappears whenever a sheet is regenerated: an Apps Script belongs to one spreadsheet, and an uploaded workbook becomes a new spreadsheet. Paste `apps-script/LivesStyle.gs` into the sheet you work in; the ABOUT tab says how. Regenerating a labeled sheet also replaces JP's labels, so a sheet JP has started to label should not be regenerated.


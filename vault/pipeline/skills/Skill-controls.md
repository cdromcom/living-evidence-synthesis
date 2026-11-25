---
name: extract-discourse-nodes-controls
description: Part 2 of the extract-discourse-nodes Skill. Run controls (the batch runner, run records, cost controls), drafting nodes by debate, provenance footers, matching and merging, crop and quote checks, decision-model checks and the optional quality-signals module. Read it before running a batch, writing nodes or running Module Q.
---

# Skill, part 2: run controls, drafting, checks and optional modules

Part 1 is `Skill.md` (the step-by-step procedure for one paper). This file holds the detail that part 1 points to. Nothing here replaces a step in part 1; it says how to run, control, write and check.

| Section | Use it when |
|---|---|
| The batch runner | you run `lives_run.py` on one to four PDFs |
| Run records and reasoning traces | you log model calls |
| Cost controls | you plan or cap spending |
| Drafting by debate | you write EVD, QUE, CLM and CVT nodes |
| Step 4c: Provenance footer | any page is written or changed |
| Matching, linking, merging and splitting | a new node may duplicate or relate to an existing one |
| Who checks crops and quotes | you check screenshots and quotes |
| Step 6e: Decision-model check | you check extractions with the decision models |
| Module Q: Quality signals | JP asks for quality signals (never in a batch run) |

## The batch runner (`pipeline/scripts/lives_run.py`)

One command takes one to four PDFs through staged model calls with a spending cap, stop rules and a run manifest. Models, prices, roles, limits and thresholds live in `pipeline/config/models.json` and `pipeline/config/pipeline.json`, not in the code. Run `pipeline/scripts/selftest.py` after any change (offline, free).

### Command
```
python3 pipeline/scripts/lives_run.py PDF [PDF ...] --mode standard|batch [--question "..."] [--cap N] [--skip checks draft qs] [--shadow MODEL] [--dry-run] [--allow-repeat]
python3 pipeline/scripts/lives_run.py --resume RUN_ID [--new-batch]
python3 pipeline/scripts/run_to_gsheet.py RUN_ID
```
- `--question` is optional context. Without it the model finds each paper's own questions.
- Supplements named `<paper file name> - supplement <n>.pdf` (or `- appendix <n>.pdf`) next to the paper are combined with it automatically.
- `--resume RUN_ID --new-batch` starts a second batch of the same run with a fresh cap (the earlier spend is kept).

### Stages
1. **Extract** (Gemini 4 Neon, `prompts/picost-v4.md`): the paper's own questions (questions, aims, goals, hypotheses, statements, each with its verbatim wording and a clear, granular reframed question), then findings in tiers, claims and caveats, all with locators and verbatim spans and linked to the questions. PDFs of 6 MB or more go through the Gemini File API (deleted when the run ends). The output budget grows with page count (at most 64,000 tokens).
2. **Spans** (PyMuPDF, free): finds every quote, boxes and highlights it, merges screenshots that cross a page, checks every number is on its page, and flags low-confidence, multi-page, scanned, not-found and number-not-on-page items. Quotes behind questions, claims and caveats are checked too.
3. **Recheck** (GPT-6.2 Sol): re-extracts the flagged findings without seeing Neon's values, from the cited pages only.
4. **Adjudicate** (Claude Opus 5.5): decides disagreements from the cited PDF pages.
5. **Checks** (decision models, then Sol vision, then Opus on rare disputes): see "Who checks crops and quotes" and "Step 6e".
6. **Draft** (debate): see "Drafting by debate". Drafts stay in the run folder until JP approves them.
7. **Quality signals**: see "Module Q".
The run stops at `awaiting_spot_check_a` with a `review.md` per paper. `run_to_gsheet.py` builds the review sheet (`Review-sheets-spec.md`).

### Evidence tiers (spec: `pipeline/templates/T - EVD tiers.md`)
- **Primary:** answers at least one of the paper's questions (`answers_QUE`).
- **Secondary:** meta or contextual information about a primary finding (`supports`).
- **Tertiary:** other context.
- First-guess caps per paper: 6, 4 and 2 (the seed papers have 1 to 6 EVDs each); an `omitted` note per tier says what was left out. JP's pilot sets the caps.

### Standard and batch mode
- **Standard** answers now at full price: use it for pilots and when someone is waiting.
- **Batch** is about half price and takes minutes to a day: Anthropic Message Batches (stack with prompt caching), OpenAI Batch and the Gemini Batch API. Put the Skill instructions first and unchanged in every request so they are cached.
- Inkling 2 Small has no batch mode and runs in parallel; the decision models have no batch mode and cost cents.
- Pilot plan (JP, 2026-11-25): batch mode only, two batches per run (stages 1 to 5, then 6 and 7 with `--resume RUN_ID --new-batch`), cap $8 per batch instead of $5.55. Revert the cap afterwards unless JP says otherwise.

### Rails (limits are in `pipeline.json`)
1. At most 4 papers per batch; a cap per batch that `--cap` can only lower; a PDF already processed (same SHA-256) is refused unless `--allow-repeat`.
2. Before each stage the worst-case cost is added to the spend so far, and the run stops before submitting if that would pass the cap.
3. **Stop-the-batch rules:** spend over the cap; a stage costing over 1.5 times its expected cost; two or more papers failing; over 25% of a paper's spans not found in its PDF; a `STOP` file in the run folder (`touch pipeline/runs/<run>/STOP`). A stop cancels any batch job still running.
4. The cap covers calls made by the runner. Set a monthly limit on each provider project as a second fence.
5. Every run writes `pipeline/runs/<run>/manifest.json` (models, prompt and script hashes, package versions, per-paper SHA-256, per-stage tokens, cost, job ids, events) and the call log.

### Open-model shadow (benchmark only)
`--shadow thinkingmachines/Inkling-2-Small` also runs the extraction on the PDF's text layer with an open model, scores it against the PDF and against Neon's primary findings, and shows it in the review sheet (tab "Open-model shadow"). Its output never enters the vault. Inkling also drafts nodes, votes and rates quality signals alongside the ensemble, benchmark only. The ladder, candidate models and the frozen Stage II snapshot are in `Open-model-benchmark-spec.md`.

### Not built yet
A second critique round; the TRIPOD-LLM rows; the writer that renders approved drafts into vault pages with footers.

## Run records and reasoning traces (JP, 2026-11-24)

Save a complete record of every model call, so the work is reproducible and, later, usable as training data for open-weight models. For each call write one JSON line to `pipeline/runs/<batch>/<citekey>/calls.jsonl` (kept out of git by default because it holds paper text and screenshots; the folder has its own README):
- `model` (exact id and version), `provider`, `date`, `effort`, `temperature` if any, `prompt_hash` and a pointer to the prompt file, `inputs` (file paths and page numbers, not copies of paper text), the `output`, `usage` (input, cached, reasoning and output tokens, cost, latency), and the step name (read, extract, draft, vote, check, crop QA, decision-model check);
- the **reasoning trace exactly as the provider returns it**: Gemini thought summaries (and the thought-token count) for Gemini 4 Neon; Claude extended-thinking blocks when enabled for Opus 5.5 and Sonnet 5.5 (store them verbatim, including whether the provider marks them summarized); GPT-6.2 Sol reasoning summaries (the API does not return raw reasoning; record the summary and the reasoning-token count); Inkling 2 on Tinker, the full text it generates; decision models (d1-ultra, Perplexity Decider, Jev) return calibrated probabilities and no trace, so store the probabilities. Never invent or reconstruct a trace; write `null` when the provider returns none;
- the **human verdict** when one exists (JP's judgments from spot checks A and B and the mirror sheet), linked by EVD id, so each trace can be filtered to verified-correct outputs.

**Before using any trace for training:** check each provider's terms. Anthropic's and OpenAI's terms restrict using their model outputs to develop competing models, so the proprietary traces are an audit and analysis record until the terms are checked or permission is obtained. Safe sources for an open-weight training set are Inkling 2 traces (open model), JP's own verified judgments and edits, the PICOST records and final texts JP has approved, and the decision-model probabilities. Paper text and screenshots stay under their source licences (`legal/PERMISSIONS.md`); share training data only for papers whose licence allows it.

## Cost controls (v2, 2026-11-24)

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

## Drafting by debate: EVD, QUE, CLM and CVT (JP, 2026-11-25; replaces the 2026-11-24 EVD writing loop)

Little things matter (a number, a comparator, 247 characters, a sentence a reader can follow), so three models draft, critique each other, revise and vote. Nothing here has been piloted: the first batch with JP decides what stays (`TODO.md`).

**Roles.** Authors: **Claude Sonnet 5.5**, **GPT-6.2 Sol** and **Gemini 4 Neon at Medium thinking** (extraction stays at High). Deciders: **Sol and Sonnet vote** (cheaper than Opus). Tie-break: **Neon**. **Inkling 2 Small** also writes the nodes (from the same extraction and PICOST grounding) and picks, in parallel, **for benchmarking only**: its drafts and picks are logged and never counted or written to the vault. **Opus 5.5** is the escalation when a gate fails twice or a claim cannot be settled. The decision models run the checks (fidelity and grounding).

**Steps (all logged).**
1. **Lint (free, deterministic), per node type.** EVD: at most 247 characters; every number, model name and comparator is on the PICOST card; metrics spelled out; readability grade (Flesch-Kincaid) about 12 or lower, flag above 14. QUE: the question rules 1 to 12. CLM: the claim is a direct quote or a faithful restatement of one. EP: the evidence threshold. CVT: the limitation, supporting quote and applies-to fields. Lint runs after every draft and revision.
2. **Round 0, in parallel.** Each author drafts from the same input: the PICOST card (with the spans and the RQ), the finding's tier, and the three examples in `Skill-templates.md`.
3. **Round 1: critique and revise.** Each author sees all drafts (anonymous, shuffled) and the lint results, and returns (a) a critique of every draft on accuracy, completeness, length, readability and little things, each point tied to a card field or a span, and (b) its own revised draft.
4. **Round 2, only if needed.** If the revised drafts still differ on a number, a comparator or a claim, or lint fails, one more critique and revision round. Never more than two rounds.
5. **Vote.** Sol and Sonnet each pick the best revised draft (anonymous), with reasons. If they agree it wins; if not, Neon breaks the tie. Inkling's pick is recorded for the benchmark.
6. **Check.** The cheaper of Sol and Sonnet that did not write the winner checks each claim against the span or crop (supported, partly supported, unsupported, with the supporting words); a decision model gives an independent fidelity answer. Any unsupported claim, or a disagreement between the two, goes to Opus 5.5, then to JP.
7. **Record.** Every draft, critique, revision, vote, lint result, check and cost is stored in the run folder and shown in the review sheet (tab "Drafts and debate"); the final text goes into the PICOST JSON (`evd_checks`) and JP judges it in the mirror sheet as usual.

**By tier.** Primary and secondary EVDs get the full loop. Tertiary EVDs get one draft, lint and the check (cheaper) until the pilot shows otherwise.

**Other node types** use the same loop with their own inputs and lints: QUE (from Introduction quotes), CLM (from Discussion claims and their supporting EVDs) and CVT (from limitations and their supporting quote). The authors, the vote and the check are the same.

**Pilot (with JP).** On the first four papers compare the loop with a single Sonnet draft: cost, JP's fidelity and style ratings, how often the three authors converge, how often Sol and Sonnet disagree, whether Inkling's pick matches the winner, and whether the second round ever changes the result.

## Step 4c: Provenance footer on every node page (required; JP, 2026-11-24)

**SRC pages are written for skimming (JP, 2026-11-25):** numbered lists for procedures, short bullets elsewhere, and each node link first, summary after (full rules in `Skill-templates.md`, "Skimmability and link order").

**Screenshots over a page break (JP, 2026-11-25):** use `pdf_pages.merge_regions(pdf, [(page, [rects]), ...], out)`: one image with the pieces stacked top to bottom, each snapped to the gap between text lines and separated by 10 px of white, so the join reads as continuous. The runner saves one for every finding whose evidence crosses a page (`highlights/<id>_merged_p<pages>.png`).

Every page the Skill writes or changes (QUE, CLM, EVD, CVT, SRC) ends with a clean, collapsed **AI-use footer** so a reader can see how the sausage was made. It follows the GAMER checklist (Generative Artificial intelligence tools in MEdical Research) and is generated, not typed. Closed, it shows one line: `AI use: <models> · <date> · <human-check status>`. Open (click in Obsidian; click or hover in the web app), it shows a skimmable table (step, model and version, effort, UTC time, prompt link and hash, saved response) and a role / sections / checked-by line, plus a link to `pipeline/provenance/AI-disclosure.md` (the project-wide answers to all nine GAMER items) and, for older pages, `pipeline/provenance/model-history.md`:
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
7. **Check structure afterwards** with `python3 pipeline/scripts/check_links.py` (both directions agree, every EVD has one source and a claim, every CLM is listed by a QUE, nothing is unlinked).
8. **Later (JP, 2026-11-25):** after Stage II EVD writing and human verification, fine-tune Inkling 2 Mini (or Small) to write QUEs, CLMs, EVDs, EPs and CVTs from verified examples (see `TODO.md`). Until then the writers are Opus 5.5 and Sonnet 5.5.

## Who checks crops and quotes (JP, 2026-11-25; decided)

Free scripts and the cheap decision-model checks do most of the work; a vision model looks only where the checks are unsure. This covers the crops and quotes behind EVDs, CLMs, CVTs and QUEs and behind the TRIPOD-LLM and Quality Appraisal rows that feed the Quality Signals tables.
1. **Scripts (free).** The quote is in the PDF text layer verbatim (`verbatim_audit.py`); the crop's rectangle contains the quote; the box is not empty and a merged multi-page crop has every piece.
2. **Decision-model checks (cents).** d1-ultra, Decider 1.3 and Jev answer calibrated probabilities for relevancy, fidelity, quote grounding and (only when the finding rests on a table or figure) table or figure grounding. Their **mean probability** (lowest question mean) and the **spread** between the three models guide what happens next.
3. **GPT-6.2 Sol (vision) looks at the crop** when a finding is flagged by the scripts, scores low (mean below 0.60), splits the models (spread above 0.35), or falls in a **10% random sample** of the rest. The 0.60 and 0.35 thresholds are first guesses to calibrate on JP's labels.
4. **Claude Opus 5.5 only for the rare disputes**: where Sol and the decision-model checks disagree (one says pass, the other fail). Anything still unclear goes to JP.
For the TRIPOD-LLM and Quality Appraisal rows the rating itself is decided by the majority vote of three raters (below); the checks above only verify the evidence behind it. Built in `lives_stages.py` (`checks`), shown in the review sheet.

## Step 6e: Decision-model check of extractions (v2; pilot in shadow mode)

After the nodes and crops are extracted, the **decision models** (Liquid d1-ultra, `d1-ultra`, `api.liquid.ai/decisions/v1/systemone`, key in `~/.config/lives-ai-raters/.env`; Perplexity Decider 1.3; Jev) check each extraction at a small fraction of an Opus call. They run four checks (JP, 2026-11-25; the word is "checks", not "gates"): **relevancy** (is this finding in scope for the question), **fidelity** (the statement matches its PICOST record), **grounding: quotes** and **grounding: tables and figures**. Ask calibrated yes/no questions: calibrated yes/no questions with the page image or passage attached, for example *Does this table show V in the row labelled R and the column labelled C?*, *Is V attributed to model M and not a neighbouring row?*, *Does this crop show the whole quote?*, *Does the highlighted span support this finding?* **Anything below the threshold goes to GPT-6.2 Sol (independent re-read) and Opus 5.5 (adjudication), and to JP if they disagree.** Our earlier benchmark found the decision models reliable on quote and table or figure grounding (about 97%) and weak on fidelity; JP (2026-11-25) judges that fidelity was defined too strictly and that the headline EVDs were poor because of weak prompting, so the decision models are expected to do better on fidelity with a clearer definition. A fidelity gate may therefore clear a record, but **re-benchmark it first** (TODO) on the audited EVDs with the new definition and set the threshold there; until then Opus 5.5 still checks every EVD claim by claim. Prefer false positives to false negatives (JP, 2026-11-25): when a gate is unsure, send the record on to the stronger models.

**Pilot (JP, 2026-11-24): shadow mode.** Run d1-ultra on every extraction of the pilot papers but do not let it decide yet; compare its answers with the audited vault content and with Opus to set the threshold (recall near 100% for errors). Switch it on once the numbers support it.

## Module Q: Quality signals (OPTIONAL, a separate run, only on JP's command; v2, 2026-11-24)

The web app's Quality Signals tables and `/quality` page read about 35 tags from each source page (and the EVD appraisal tags). They are written by `Step 4b` (TRIPOD-LLM table) and `Step 6.c` in `Skill-templates.md` (the `## Quality appraisal` table). This module is **not part of the core run** (read, extract, write nodes, push to the web app), so API credits spent on extraction are never spent on signals by accident. Run it only when JP says so, one paper batch at a time. Until then the web app shows blank signal cells. the tag list and locator standard are in `Quality-signals-spec.md`.

1. **Judged signals** (validity domains, rigor checks, spin, integrity disclosures, TOP levels, TRIPOD rows, and the quality-appraisal rows that give rise to the Quality Signals tables): **Claude Opus 5.5, GPT-6.2 Sol and Gemini 4 Neon (Medium)** each rate every row independently and blind, from the PICOST record and the Methods and Results text, with a verbatim quote and a locator (JP, 2026-11-25). **Majority voting** across the three gives the signal; a 1-1-1 split is shown as "no majority" for JP. **Inkling 2 Small** also rates, **for benchmarking only** (logged, not counted); Sonnet 5.5 takes no part in the ratings (JP, 2026-11-25).
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

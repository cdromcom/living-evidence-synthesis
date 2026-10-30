---
name: skill-references
description: Reference doc — naming conventions, the 19 Key Principles, Common Pitfalls (lessons from prior phases), and the After-Extraction summary table. Load alongside Skill.md when authoring or auditing nodes.
parent_skill: extract-discourse-nodes
created: 2026-04-29
updated: 2026-08-26
---

# Skill — Naming, Principles, Pitfalls, After-Extraction

This file is a quick-reference companion to `Skill.md`. Load it when you need:

- The **naming conventions** for node files and PNGs.
- The **19 Key Principles** that govern every extraction (verbatim quotes, atomicity, EVD≠CLM, the human-owned cell-fill governance, the EP threshold, etc.).
- **Common Pitfalls** — concrete mistakes from prior phases worth re-reading before starting.
- The **After-Extraction summary table** that closes every extraction run.

> See also:
> - `Skill.md` — orchestrator (workflow at a glance, Steps 1–3, pointers).
> - `Skill-templates.md` — Steps 4–10: node-file templates, audits, structured abstracts.
> - `Skill-synthesis.md` — Steps 11–14: cross-paper synthesis + public render + ESS Bases.

---

## Naming Conventions Summary

| Type | Pattern                           | Citekey in filename? | Example                                                                           |
| ---- | --------------------------------- | -------------------- | --------------------------------------------------------------------------------- |
| QUE  | `QUE - [question].md`             | No                   | `QUE - How well can LLMs rank study reports relative to human experts.md`         |
| EVD  | `EVD - [finding] - @[citekey].md` | Yes                  | `EVD - GPT-4 detected errors in 7 of 13 papers - @liuReviewerGPT2023.md`          |
| CLM  | `CLM - [claim].md`                | No                   | `CLM - LLMs are overall less accurate than human experts at quality appraisal.md` |
| CVT  | `CVT - [limitation].md`           | No (usually)         | `CVT - The small sample limits generalizability.md`                               |

### PNG naming

Canonical naming for **all** quote-region crops, generated automatically by `quote_pipeline.py`:

| Purpose | Canonical pattern |
| --- | --- |
| EVD quote | `<citekey>-evd-p<N>-<idx>.png` |
| CLM quote | `<citekey>-clm-p<N>-<idx>.png` |
| CVT quote | `<citekey>-cvt-p<N>-<idx>.png` |
| QUE quote | `<citekey>-que-p<N>-<idx>.png` |
| EVD figure/table page | `<citekey>-<label>-p<N>.png` (manually authored, e.g. `-fig2-p4`, `-table1-p5`) |

`<idx>` is incremented per `(citekey, kind, page)` and is shared across all node files of the same citekey within a single pipeline run, so canonical names never collide across multiple EVDs/CLMs/CVTs/QUEs of the same paper.

**One quote → one PNG filename (NON-NEGOTIABLE).** Every distinct verbatim quote in the vault must point to its own dedicated PNG. **Never reuse the same `> ![[<citekey>-{evd|clm|cvt|que}-p<N>-<idx>.png]]` filename across two different quotes.** If two quotes share a filename, the screenshot pipeline regenerates the same file once per quote during a `--force` run and the *last-processed* quote wins — silently leaving a screenshot whose highlight matches a different quote than the one displayed in the markdown. Two failure modes to watch for:
1. **Within one node file:** Description quote, What/How/Who quotes, Other-Notes table-summary quote each must have a distinct embed filename. Distinct `<idx>` values per page.
2. **Across multiple node files of the same paper:** two different CVTs (or QUEs, or CLMs) of the same paper sometimes end up pointing at the same PNG because both happen to be on the same PDF page. This is the failure pattern that surfaced in Phase 21 (two Leucuta CVTs both pointing to `leucuta-cvt-p17-1.png`). Resolve by renaming the second to `-p17-2.png`, etc.

**Audit script** (run periodically):
```python
# Quick collision detector — flags quote-region embeds with shared filename + distinct preceding quote.
from collections import defaultdict
import re
from pathlib import Path

embeds = defaultdict(list)
for f in Path('.').rglob('*.md'):
    if not any(p in str(f) for p in ('evidence/', 'claims/', 'caveats/', 'questions/', 'source/')):
        continue
    lines = f.read_text().split('\n')
    for i, line in enumerate(lines):
        m = re.match(r'>\s*!\[\[([^\]]+\.png)\]\]', line.strip())
        if not m: continue
        png = m.group(1)
        if not re.search(r'-(evd|clm|cvt|que|quote)[-_].*p\d+', png): continue
        qtext = next((re.match(r'>\s*"(.+?)"', lines[j]).group(1)[:60]
                      for j in range(i-1, max(i-6,-1), -1)
                      if re.match(r'>\s*"', lines[j])), None)
        embeds[png].append((str(f), qtext))
for png, refs in embeds.items():
    quotes = {q for _, q in refs if q}
    if len(quotes) > 1:
        print(f'{png}: {len(quotes)} distinct quotes share this filename')
```

**Legacy / deprecated patterns** (do not use for new work):
- `<citekey>-quote-<slug>-{desc,what,how,who}-p<N>.png` — semantic-slug naming used pre-Phase-18. Stripped during Phase 18 EVD rewrite. If you encounter these in old git history, they map to the canonical pattern above.

---

## Key Principles

1. **Direct quotes are critical and must be verbatim.** Every substantive claim or note in the body of a discourse node must have a direct quote that you can find verbatim in the source PDF (after NFKD + alnum normalization). Paraphrases erode trust in the graph and break the audit. If you cannot quote it, mark `[Inferred: ...]` and provide the closest supporting passage.
2. **Atomicity.** One question per QUE. One result per EVD. One generalization per CLM. One limitation per CVT. When in doubt, split rather than merge.
3. **EVD ≠ CLM.** Numbers and observations are EVD. What they mean is CLM. If authors report a result AND draw a conclusion from it in the same sentence, extract both: one EVD for the result, one CLM for the conclusion.
4. **Author-stated vs. inferred CVTs are both valuable.** Clearly distinguish them with the `type` field. For inferred CVTs, justify your reasoning in brackets after the quote.
5. **CLMs transcend single papers.** Title CLMs at the level of the claim, not the paper — multiple papers can make the same claim. Under `### Snippet: Quote(s) & Screenshots`, list each contributing paper's verbatim quote.
6. **Preserve the authors' own language.** Do not editorialize in EVD or CLM nodes. Quote directly. If you reformat a table into prose for readability, annotate `*Table N row(s) reformatted as inline text:*` so the form change is honest.
7. **Node formality starts at `draft`.** Promote to `ReadyForInternal` only after Steps 5–8 pass. Promote to `ReadyToShare` only after manual review.
8. **The graph is what makes notes useful.** Reverse links (`## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence`, `### Supporting Claims`) auto-resolve from `appliesTo` and citekey overlap. Re-running the reverse-link pass after every paper keeps the graph in sync.
9. **Log every concrete change in `History.md`** — additions, edits, deletions of files; PNG counts; phase summaries. Future-you will need to retrace decisions.
10. **Discourse-graph attachment invariants (Step 5b enforces).** Every CVT's `appliesTo` lists only EVDs (no CLMs). Every CLM appears in at least one QUE's nested `### Supporting Claims (with their evidence)` block. Every EVD appears in at least one CLM's `### Supporting Evidence` *and* at least one QUE's nested structure. Violations are blockers — fix or document before promoting NodeFormality.
11. **Generated documents (DGRAPH.md, audit reports, etc.) carry properties + provenance.** YAML frontmatter must include `author`, `page_type`, `created`, `updated`, `generated_by` (the script or skill), and `prompt_source` (a wikilink to the originating prompt saved under `prompts/`). Notes for human readers go below the frontmatter as Obsidian callout boxes (`[!info]`, `[!tip]`, `[!caution]`, etc.) rather than free prose, so the rendered properties panel stays clean.
12. **Every QUE / CLM / EVD / CVT carries a populated `nodeID` (UUIDv7) in its frontmatter.** This is a stable, file-rename-safe identifier for the node — used for deduplication, cross-referencing across vault renames, and any future external indexing. Generate at node-creation time with `python3 -c "import uuid; print(uuid.uuid7())"`. Never leave the `nodeID:` field blank. To backfill an empty nodeID across the whole vault: `python3` script in `History.md` Phase 22 entry.
13. **Every EVD carries 8 inherited paper-level rigor tags in its frontmatter**, and every source (`source/@<citekey>.md`) carries those same 8 plus 6 more benchmarking-specific ones directly. These summarize the paper's `## Quality appraisal` (renamed from "Critical appraisal" in 2026-08; 5 original domains × 🟢/🟡/🔴, now a 10–11-row quote-grounded table — see Skill-templates.md Step 6.c) and `## TRIPOD-LLM reporting summary` (✅/⚠️/❌/➖ across 42 items, now with a verbatim-quote `Quote` column — see Step 4b) so a reader can filter EVDs by methodological rigor without opening the source page. Tag scheme:
    - 5 per-domain appraisal tags: `appraisal/{construct-validity,internal-validity,external-validity,statistical-rigor,reproducibility}/{low-risk,some-concerns,high-risk}`
    - 1 appraisal-summary tag: `appraisal/overall/L<n>-M<n>-H<n>` (counts of low / some-concerns / high domains)
    - 1 TRIPOD-LLM compliance bucket: `tripod-llm/compliance/{high,moderate,low}` — high ≥80% ✅ rate, moderate 60-80%, low <60% (proportion = ✅ / (✅+⚠️+❌), ➖ excluded; **scoped to Methods 5a–15 + Results 16a–18 only** — the four 2026-08-added Title/Abstract/Background/Objectives items 1–4 do not factor into this percentage)
    - 1 TRIPOD-LLM raw proportion: `tripod-llm/proportion/<NN>pct`
    - **6 benchmarking-specific Rigor tags, added 2026-08, at the source-file level** (one row each in the Quality Appraisal table's rows 6–11): `rigor/data-leakage/{addressed,partial,unresolved,not-addressed}`, `rigor/baseline-adequacy/{addressed,partial,not-addressed}`, `rigor/train-dev-test/{addressed,partial,unresolved,not-addressed}`, `rigor/multiple-comparisons/{addressed,partial,not-addressed}`, `rigor/human-baseline/{addressed,partial,not-addressed}`, and `rigor/statistical-power/{adequate,inadequate}` — this last one **only when the paper actually reports a power analysis**; omit the tag entirely otherwise, don't tag every paper "inadequate" by default.
   When the source-page Quality Appraisal table or TRIPOD-LLM table changes, regenerate these tags via the inline script in `History.md` Phase 23 entry. They go in `tags:` after `aliases:` in each EVD's (and source's) YAML frontmatter.
14. **Every CVT carries 4+ methodology tags in its frontmatter** describing the *kind* of caveat it is, in a controlled vocabulary a methodologist would use:
    - 1 validity-domain tag (the 5-bucket appraisal taxonomy): `cvt/domain/{construct-validity, internal-validity, external-validity, statistical-rigor, reproducibility}`
    - 1+ mechanism tags from a controlled vocabulary: `cvt/mechanism/<name>` — see `History.md` Phase 24 for the full list (≈30 mechanisms covering sample / model / evaluation / statistical / reproducibility patterns)
    - 1 type tag mirroring the existing `type:` field: `cvt/type/{author-stated, inferred}`
    - 1 severity tag mirroring the existing `severity:` field: `cvt/severity/{low, moderate, high}`
   Multiple mechanism tags are allowed when a CVT genuinely spans (e.g., a small *single-discipline* sample gets both `small-sample` and `single-discipline`).
15. **Every QUE / CLM / EVD / CVT carries one or more 5C Research Dimension tags** so the discourse graph is filterable by what *aspect* of research the node touches:
    - `5c/credibility` — rigor (study design, error detection, risk-of-bias assessment, methodological evaluation)
    - `5c/clarity` — reporting-guideline alignment (CONSORT, PRISMA, AMSTAR, STROBE, ROBINS-I, etc.)
    - `5c/creativity` — novelty + value (novelty assessment, peer-review feedback for innovation)
    - `5c/connectivity` — connections to other research and practice (citation integrity, quotation errors)
    - `5c/care` — ethics (IRB review, informed consent, ethical review of clinical proposals)
   For EVDs and CVTs, inherit dimensions from the parent paper (see `History.md` Phase 24 for the per-paper map). For QUEs and CLMs, classify by title keywords + papers-block union; multiple dimensions allowed when a node spans (e.g., peer-review nodes typically span credibility + clarity + creativity).
16. **Synthesis is human work; extraction + organization is shared.** AI extracts EVDs/CLMs/CVTs from PDFs and proposes EvidencePatterns + subtask merges, but does not commit synthesis-level judgments to public artifacts (Review-Arena cells, EP truth values, merge-map decisions) without per-row human approval. The human-AI dyad is the *authoring* mode for the discourse graph; once that graph exists, synthesis layers atop it (Review-Arena cells, EP claims) are gated by humans. This was made explicit on 2026-05-04 when AI-proposed leaderboard cells were rejected; see `History.md` for the full governance note.
17. **EvidencePatterns require ≥2 papers.** A regularity supported by only one paper already lives as a CLM. EPs exist to surface *cross-paper* triangulation that no single paper makes. If you find yourself wanting to open an EP from one paper, write a CLM instead.
18. **Every cross-paper synthesis run regenerates derived state.** When EVDs / CLMs / EPs change in a way that affects downstream artifacts, re-run the relevant scripts in order: `link_eps_to_ques.py` (EP↔QUE cross-links) → `add_tldr_callouts.py` (source-page TL;DRs) → `count_evds_per_subtask.py` (Review-Arena EVD counts) → `mkdocs build` (public site). Don't hand-edit derived sections — they get clobbered on next run.
19. **Two render targets, two CSS pipelines** (three, counting `living-synthesis-site` — see the Skill.md build-output note; it's now independently maintained, not produced by this vault's own pipeline). Obsidian (authoring) reads `.obsidian/snippets/wide-tables.css` controlled by `cssclasses:` frontmatter. The MkDocs public site reads `public/assets/*.css` controlled by hooks + `body:has()` selectors. Visual changes that should be visible in both views need to be replicated in both — a CSS rule in one pipeline does not propagate to the other. Note for context: `living-synthesis-site` mutes the plain ✅/⚠️/❌/➖/🟢/🟡/🔴 emoji this vault authors into single-hue shape-coded SVG icons at render time (solid dot/half-ring/ring/dash — color stays constant, shape carries the level, for colorblind-accessible and print-safe tables); author plain emoji here as always, that transform is a `living-synthesis-site`-only rendering concern, not something this vault's own markdown needs to produce.

---

## Common pitfalls (lessons from prior phases)

Concrete mistakes that have happened before. Read this once before starting work.

### Methods Context schema — getting What/How/Who right

- **What** is *the design* (study type, method category, tools, dependent variables, independent variables) — NOT the result. Don't put F1 scores or kappa values here.
- **How** is *the procedure* — preprocessing, model training, prompt construction, statistical tests, in the order they were performed. Don't restate the design.
- **Who** is *the data flow* — original sourced N → exclusions → final analyzed N — plus the model lineup and any human comparators. For studies without participants (NLP benchmarks), the "Who" is the dataset+model lineup; explicitly say "no human subjects" when applicable.
- The verbatim quote that follows each prose block must be the **most informative** passage from the paper that grounds the prose, not just any sentence from that section. Pick a passage that names tools / sample sizes / specific procedures.

### TRIPOD-LLM compliance icons

- **Calibrate ⚠️ vs. ✅ honestly.** When in doubt, pick ⚠️. The icons are useful only when they reflect what's actually reported, not what we wish were reported.
- **Items that are typically `❌` for this corpus and should not be sandbagged to ⚠️:** 12 (compute), 14a–14c (funding, COI, protocol) for arXiv preprints lacking these statements, 5c (date range of data) for evaluation papers that don't disclose training-corpus dates.
- **Items that are typically `➖` for non-clinical NLP papers:** 13 (ethical approval, no human subjects), 14d (registration, no clinical trial), 15 (patient/public involvement), 16a–c (patient/EHR flow). Mark explicitly — don't drop the rows.
- **Item 17 (Performance) is per-EVD, not per-paper.** The source-file row reads `(per-EVD) — See each EVD's ## Other Notes`. Each EVD then carries the EVD-specific F1 / kappa / prevalence / etc. Do NOT duplicate item-17 numbers in the source file.

### Screenshot pipeline

- **Never hand-write `> ![[<citekey>-{evd|clm|cvt|que}-...png]]` quote-region embeds.** The pipeline inserts them with canonical naming. Hand-writing them creates filename mismatches when the quote text moves to a different page.
- **When rewriting a quote**, strip any existing `> ![[<citekey>-quote-...]]` or `> ![[<citekey>-{evd|clm|cvt|que}-...]]` line that immediately follows it BEFORE running the pipeline. The pipeline will re-insert with fresh canonical naming. Page-level table/figure embeds (`-tables-pN-X.png`, `-fig...-pN-X.png`) are manually authored and must be preserved.
- **`--force` is for in-place regeneration only**, when the markdown filename is unchanged but the underlying quote text changed. For new EVDs or rewritten quotes, run without `--force` so canonical naming is used.
- **En-dash mangling** (`Human−AI` ≠ `Human-AI`) is a known PDF-extraction issue. When choosing an opening/closing match string, avoid words containing en-dashes — pick a unique phrase a few words later. The pipeline tolerates this for short quotes but Pass-1 full-segment match will fail on long quotes that contain en-dashes.
- **Page-number citations in source articles can be wrong.** Sometimes a paper cites `p. 33` for content that's actually on a different page or doesn't exist (e.g., the Liu & Shah 2023 case). The pipeline searches all pages if the cited page misses, but if the quote isn't anywhere in the PDF the EVD just won't get a screenshot — fix the quote text or page citation manually.

### Subagent batching (when scaling across many papers)

- **Watchdog timeout is 10 min of no-progress.** Watch for: many tool calls, large PDFs read in one shot, exploratory `ls`/`grep`/`Read` after the work is done. Stalled agents are killed mid-stream.
- **Reach 10-min timeout != lost work.** Failed agents often completed most of the writes. Before re-launching, check artifact state (`grep -l "updated: <today>"`, `wc -l source/@<citekey>.md`) — sometimes only the source-file table needs to be finished.
- **Subagent prompts should reference a shared brief** under `misc/prompts/<date>-<task>.md` instead of duplicating the full schema 26 times. Keep the per-paper prompt to ~150 words: citekey, PDF path, working dir, brief path, "report back per the brief".
- **Subagents must NOT run the screenshot pipeline.** The parent runs it once after all subagents return so canonical-name idx values are globally consistent.
- **Subagents must NOT insert quote-region embed lines.** They edit markdown text only; the parent's pipeline run inserts embeds.

### Source-file structure (frontmatter-only papers)

When a `source/@<citekey>.md` is just frontmatter (no `## TRIPOD-LLM reporting summary` section), that paper hasn't been processed under the Phase 18 schema. Append the section, don't replace the frontmatter.

### `curatedWithModel` / `curatedWithModelDate` frontmatter (2026-08 addition)

Every source that's had its TRIPOD-LLM/Quality-Appraisal quotes curated should carry `curatedWithModel: "<model name>"` and `curatedWithModelDate: <YYYY-MM-DD>` in its frontmatter — e.g. `curatedWithModel: "Claude Sonnet 5"`, `curatedWithModelDate: 2026-08-25`. This is a provenance field (which model did the quote-sourcing, and when — useful if a later model generation re-verifies old work), not something derived automatically; set it when you do the pass, not before.

### Cross-layer scripting traps (Review-Arena + render pipeline)

Hard-won lessons from rewriting Review-Arena tables and the public-render hooks:

- **`\|` inside markdown table cells breaks naive `line.split("|")`.** Wikilinks like `[[QUE - title?\|Display]]` get split on the inner pipe, leaving a corrupted target. Always pre-replace `\|` with a placeholder (`\x00P\x00`) before splitting, then restore after rejoining. The wikilinks hook also has to unescape `\|` → `|` before splitting target/display.
- **The Obsidian table-formatter linter pads cells.** A row that started as `| AI | ... |` becomes `|      AI       | ... |` with variable whitespace. Substring matches like `"| Details |"` or exact-cell tests fail on padded rows. Use regex with `\s*` between pipes, or strip cells before comparing.
- **Don't run "drop the last column" twice.** The first run strips Details from all 6 tables; the second run strips Effect-size or Strength from the same tables. Headers + dividers + data rows can drift out of column-count agreement, and Markdown silently renders the result with mismatched columns. Always check column count BEFORE re-running a column-drop script. Better: use a "canonicalize headers" approach that overwrites all headers/dividers to a known schema, separate from data-row transformations.
- **`is_header` and `is_divider` checks are easy to over-trigger.** A divider row has only `|`, `-`, `:`, ` ` — a check like `all(c in "|:- " for c in s)` works only if you've already excluded data rows by another condition. Order matters in the main loop.
- **MkDocs `site_dir` cannot live inside `docs_dir`.** If you set `docs_dir: ..` from inside `public/`, you can't also set `site_dir: site` (it'd be inside the parent). Use `site_dir: ../../living-synthesis-site/` or absolute paths.
- **`exclude_docs:` doesn't help with `extra_css:` / `extra_javascript:` paths.** When the docs_dir is the vault root, CSS / JS files inside `public/assets/` are served at `/public/assets/...` URLs. They are *not* docs and `exclude_docs` doesn't apply, but they DO appear in the build. Verify with `find <site_dir> -name extra.css` after a build.
- **`![[*.base]]` embeds need a hook.** Without `bases.py`, the wikilinks hook turns the embed into `<img src="../ESS.base">` — a broken image, since `.base` is a YAML config file. The bases hook parses the YAML and emits Material tabs.
- **YAML descriptions with colons inside backticks need quoting.** `description: "Text with \`NodeFormality: draft\` inline"` parses; `description: Text with NodeFormality: draft inline` doesn't. The colon inside the backticks is still a YAML colon to the parser.
- **`body:has(.ls-leaderboard) ...` is per-page CSS.** The `:has()` pseudo-class scopes wide-page rules to pages that contain the wrapper. This is how Review-Arena gets full-width without breaking other pages. Browser support: Chrome 105+, Safari 15.4+, Firefox 121+ — fine for a public site, but confirm if you start adding more `:has()`-driven rules.

---

## After Extraction

Provide a summary organized by node type:

**Questions (QUE):**

| File | Research Question |
| ---- | ----------------- |
| ...  | ...               |

**Evidence (EVD):**

| File | Key Finding | Grounding PNGs (figure/table/quote) | Key Statistics |
| ---- | ----------- | ----------------------------------- | -------------- |
| ...  | ...         |                                     |                |

**Claims (CLM):**

| File | Claim | Grounding EVDs |
| ---- | ----- | -------------- |
|      |       |                |

**Caveats (CVT):**

| File | Limitation | Type | Severity | Applies To |
| ---- | ---------- | ---- | -------- | ---------- |
|      |            |      |          |            |

> [!NOTE] Output Message
> State the output directory and total node count by type — e.g., "Extracted 2 QUE, 5 EVD, 4 CLM, 6 CVT nodes (10 author-stated + 2 inferred) to `Evidence/DiscourseNodes/`. 23 PNGs in `attachments/`. Reverse-link pass + verbatim audit + readability pass + formality promotion run."

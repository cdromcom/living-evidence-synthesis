# History

Chronological log of all concrete changes (additions, deletions, edits) made to the living-synthesis vault by Claude during interactive sessions. Newest first.

> [!note] File rename history
> This file was originally `HISTORY.md` (all-caps), briefly carried the orphan name `History 2.md` during the May 2026 refactor (after Obsidian created a duplicate), and was restored to `History.md` (mixed-case) once an unresolved-wikilink sweep cleared the namespace. Legacy phase entries below still reference `HISTORY.md` and a few may reference `History 2.md` — those mentions are preserved as historical artifacts and should be read as referring to *this file*.

---

## 2026-05-05 — Skill.md split into orchestrator + 3 reference docs

### Why
`Skill.md` had grown to 1070 lines after Phases 27–35 added the cross-paper synthesis layer, the public-render pipeline, the Obsidian wide-tables snippet, and ESS Bases coverage. At ~25k tokens loaded into the agent prompt at every invocation, the skill was (a) eating prompt budget that should go to the actual paper + outputs, (b) diluting attention on rules buried late in the file, and (c) at risk of silent rule-skipping under future model updates. The user surfaced the reliability concern; this split is the response.

### Refactor
Split into one slim orchestrator + three reference docs, each with YAML frontmatter and reciprocal cross-links to its siblings:

| File | Lines | Purpose |
| --- | --- | --- |
| `Skill.md` | **291** | Orchestrator: workflow at a glance, vault structure, node types, Steps 1–3 inline + Steps 4–14 outlines pointing to reference docs |
| `Skill-templates.md` | 501 | Steps 4–10: node-file templates (EVD/CLM/CVT/QUE bodies), TRIPOD-LLM table, audit invariants + audit script, structured-abstract schema, Mermaid + critical-appraisal calibration, NodeFormality, DGRAPH regen |
| `Skill-synthesis.md` | 187 | Steps 11–14: EP node format, Review-Arena schema + governance, MkDocs hooks/assets, Obsidian visual treatments, ESS Bases formulas + views |
| `Skill-references.md` | 207 | Naming conventions (file + PNG), 19 Key Principles, Common Pitfalls (Methods Context, TRIPOD icons, screenshot pipeline, subagent batching, source-file structure, cross-layer scripting traps), After-Extraction summary |

Skill.md went 1070 → 291 lines (73% reduction). Specialty content loads only when the orchestrator references it.

### Edited
- `Skill.md` — rewritten as the slim orchestrator. Kept lines 1–235 verbatim (frontmatter, intro, workflow at a glance, vault structure, node types, Inputs, Steps 1–3). Replaced Steps 4–14 detail + naming + principles + pitfalls + after-extraction with one-paragraph step outlines that point to the three reference files. Final outline: ## Workflow at a glance / ## Vault structure / ## Node Types / ## Inputs / ## Step 1 / ## Step 2 / ## Step 3 / ## Step 4–14 (one paragraph each, with `→ see Skill-templates.md` or `→ see Skill-synthesis.md` pointers) / ## Reference docs.

### Created
- `Skill-templates.md` — Step 4 (templates for QUE/CLM/EVD/CVT bodies), Step 4b (paper-level TRIPOD-LLM table format, 37 items × 4 compliance icons), Step 5 (reverse-link script), Step 5b (audit invariants + Python audit script), Step 6 (structured abstract — 5-section schema), Step 6.b (Mermaid Methods/Results visualizations), Step 6.c (5-domain critical appraisal), Step 7 (readability formatting), Step 8 (NodeFormality promotion), Step 9 (DGRAPH regeneration), Step 10 (prompt provenance + History.md log).
- `Skill-synthesis.md` — Step 11 (EvidencePattern node format + Review-Arena schema + the human-only-cell-fill governance + Subtask verb-first naming + merge-map proposal pattern), Step 12 (MkDocs build commands + 4-hook execution order + asset list + exclude_docs rules), Step 13 (Obsidian wide-tables snippet + cssclasses pattern + sortable-plugin notes), Step 14 (ESS Bases — 6 formulas + 23 views + when-to-add-a-view pattern + YAML colon-in-backticks pitfall).
- `Skill-references.md` — Naming Conventions Summary (file + PNG patterns + collision-detector script), the 19 Key Principles, Common Pitfalls (5 sub-sections), After-Extraction summary table.

### Edited (mkdocs.yml)
- `public/mkdocs.yml` — `exclude_docs:` now excludes `Skill-templates.md`, `Skill-synthesis.md`, `Skill-references.md` (in addition to existing excludes for `Skill.md`, `Log.md`, `History.md`). The reference docs are internal — they don't need to appear on the public site.

### Lessons
1. **Skills should fit the agent's attention budget, not the human author's documentation desire.** The reliability concern came from the user, not from observed model failures — but the structural risk was real (rules buried at line 800 silently get less weight). Cap orchestrator skills at ~300 lines; spin off reference docs.
2. **Reference-doc cross-links must be reciprocal.** Each of the three reference files lists the orchestrator + the other two siblings. A reader landing on any one file knows where the others live.
3. **YAML frontmatter on reference docs uses `name:` + `description:` + `parent_skill:` so they show up in skill-discovery the same way as the orchestrator.**

### History.md updates
- This entry; phase index extended.

---

## 2026-05-04 — Review-Arena.md handed back to human authoring

### User decision (logged on user request)
After Claude proposed AI-generated cell values for the Review-Arena leaderboard (AI score / Human score / Human-AI score / Winner / Effect size / Evidence Strength), the user **deleted all data cells** and **kept only the Subtask column**. Reason: synthesis of evidence into leaderboard cells is reserved for humans, working from EVDs and EvidencePatterns that the human-AI dyad has already extracted and organized. Claude's role is the upstream extraction + organization, not the downstream synthesis call. Two callout boxes describing per-column semantics were also removed by the user. Going forward, the Review-Arena cells should be populated only by a human or under explicit per-row human approval — not auto-filled by Claude.

### Open question raised by the user
Subtasks in the leaderboard are currently paper-individualized (each row reflects one paper's framing of its experiment). Several rows overlap conceptually within a single section table (e.g., three "Detect errors…" rows in the Error/limitation section; multiple CONSORT-adjacent rows in Reporting compliance). Whether to merge these into higher-abstraction subtasks — and who should drive the merge — is left as a TODO for human decision; Claude's recommended role is to *propose* a merge map, not commit it.

---

## Current state (as of 2026-04-27)

**Vault inventory.**

| Type | Count | Notes |
| ---- | ----- | ----- |
| QUE | 27 | Each has `### Supporting Claims (with their evidence)` nested block |
| CLM | 31 | All attached to ≥1 QUE; all have `### Supporting Evidence` |
| EVD | 77 | All attached to ≥1 CLM and ≥1 QUE; all have Description + Methods Context |
| CVT | 49 | All `appliesTo` lists EVDs only |
| PNGs | 603 | In `evidence/Attachments/` (Phase 18: +222 EVD crops; Phase 20: −11 orphaned QUE quote crops removed during the QUE content cleanup) |

**Vault root files.**

- `DGRAPH.md` — central nested index with YAML frontmatter, callouts, and clickable wikilinks. Regenerated by `scripts/build_dgraph.py`.
- `HISTORY.md` — this file.
- `SKILL.md` — extraction skill for new papers, refined to match current state.
- `Welcome.md` — vault overview for novices.
- `paraphrase_audit_2026-04-27.tsv` — 50 flagged paraphrases (1 known false positive, 23 Tier 2 majors, 19 Tier 3 moderates, 7 Tier 4 minors).

**Vault directories.**

- `claims/`, `caveats/`, `evidence/`, `questions/` — discourse-graph nodes.
- `evidence/Attachments/` — all PNGs (figure/table pages + quote-region crops).
- `source/` — bibliographic source notes (`@<citekey>.md`) + original `pdfs/`.
- `templates/` — `T - <NodeType>.md` templates for new nodes.
- `prompts/` — verbatim user prompts that originated generated documents.
- `scripts/` — Python helper scripts (see `scripts/README.md`).

**Graph attachment invariants — all PASS (verified 2026-04-27):**

1. CVT `appliesTo` contains only EVDs ✓
2. Every CLM appears in ≥1 QUE ✓
3. Every EVD appears in ≥1 CLM ✓
4. Every EVD appears in ≥1 QUE ✓

**NodeFormality distribution.**

- 130 `ReadyForInternal` (structurally complete, ready for human review)
- 27 `draft` (flagged in paraphrase audit at <50% match — manual fix needed before promotion)

**Phase index** (newest first, all 2026-04-27 unless noted):

- Phase 26 — EvidencePattern (EP) extraction: 12 cross-paper patterns bundling 42 of 77 EVDs (2026-04-29)
- Phase 25 — `ESS.base` Obsidian Bases index for filtering all DG nodes (2026-04-29)
- Phase 24 — methodologist tags on every CVT (domain × mechanism × type × severity) + 5C Research Dimension tags on every DG node (2026-04-29)
- Phase 23 — 8 paper-level rigor tags on every EVD (5-domain appraisal ratings + TRIPOD-LLM compliance bucket + raw proportion) (2026-04-29)
- Phase 22 — populated UUIDv7 `nodeID` on all 184 QUE/CLM/EVD/CVT nodes (2026-04-29)
- Phase 21 — DGRAPH-TABLE.md, quote-screenshot collision audit + 25 renames, 4 missing QUE aim quotes filled (2026-04-28)
- Phase 20 — external-framework cross-reference, Mermaid renderability audit, QUE content rule + cleanup (2026-04-28)
- Phase 19 — source-page synthesis: structured abstract + Mermaid Methods/Results visualizations + 5-domain critical appraisal (2026-04-28)
- Phase 18 — TRIPOD-LLM EVD rewrite (Methods Context schema; per-paper compliance table) (2026-04-28)
- Phase 17 — quote screenshots: full-quote crops + per-kind colour highlighting + QUE coverage
- Phase 12 — DGRAPH.md properties + SKILL.md invariants/audit
- Phase 11 — graph attachment rules enforced
- Phase 10 — DGRAPH.md central index created
- Phase 8 + 9 — QUE → CLM → EVD nesting + SKILL.md refinement
- Phase 7 — readability formatting (184 files)
- Phase 5 + 6 — QUE → EVD links + NodeFormality promotion
- Phase 4 — auto-extracted markers cleaned up (134 → cleaner labels)
- Phase 3 — reverse-link the discourse graph (77 EVD + 31 CLM)
- Phase 2e + 2f — verbatim audit + Tier 1 paraphrase fixes
- Phase 2d — EVD specificity pass (31 EVDs)
- Phase 2a + 2b + 2c — Description quotes / Methods Context / What pass
- Pre-scaling fix-up — source links + 35 CVT screenshots (2026-04-27 earlier)
- Pilot rollout — Liu / Sarol / Liang (2026-04-27)
- Original Woelfle pilot + tooling (2026-04-25, 2026-04-24)

---

## 2026-04-29 (Phase 26 — EvidencePattern extraction)

User added an EvidencePattern (EP) node type — a higher-order node that bundles related EVDs **across papers** to surface empirical regularities the corpus reveals when read as a whole. EPs sit between EVDs and CLMs but operate cross-paper rather than within-paper.

**Threshold (per user):** 2 papers minimum to qualify as a pattern.

**EP file structure** (after user feedback removed three sections from the pilot):
- Frontmatter — `nodeTypeId: node_tzL95oDi6eYeRIHeY_rCh` (matches the user's `EvidencePattern Nodes.base` filter), UUIDv7 nodeID + nodeInstanceId, 5C tags inherited from supporting EVDs, `ep/strength/<N>-papers` and `ep/scope/cross-paper` tags.
- `## Pattern statement` — one paragraph in plain language framing the pattern.
- `## What is being claimed` — 1–2 paragraphs distinguishing the pattern from absolute-performance claims and listing the dimensions across which it holds.
- `## Supporting Evidence` — wikilinks to contributing EVDs, each annotated with one line about that paper's contribution.
- `## Connected discourse-graph nodes` — links to within-paper CLMs the pattern generalizes, adjacent EPs, and shared CVTs.

**Reverse-link section on each contributing EVD:** `## Instantiates Pattern(s)` between `## Supports Claim(s)` and end-of-file. Mirrors the existing `## Caveats` and `## Supports Claim(s)` reverse-link convention.

**Folder layout:** `evd-patterns/` at vault root (renamed from initial `patterns/` per user feedback), parallel to `evidence/`, `claims/`, `caveats/`, `questions/`.

**12 EPs extracted** (newest first, all from 2026-04-29):

| # | EP title | EVDs | Papers |
| --- | --- | :---: | :---: |
| 1 | Reasoning LLMs lead other models at scientific-error and quality-checker benchmarks | 3 | 3 |
| 2 | Per-item LLM-human agreement varies sharply by item type | 8 | 5 |
| 3 | General-purpose LLMs systematically over-rate papers compared to human reviewers | 4 | 3 |
| 4 | LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable | 5 | 5 |
| 5 | Aggregate-level LLM-human agreement masks near-zero per-paper correlation | 4 | 3 |
| 6 | Task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks | 5 | 4 |
| 7 | RAG and few-shot prompting improve LLM performance but rarely close the human gap | 4 | 3 |
| 8 | Text-only LLMs underperform on tasks where figures or tables carry primary information | 2 | 2 |
| 9 | Human-AI collaboration outperforms either alone on structured appraisal tasks | 2 | 2 |
| 10 | LLMs satisfy protocol structure but miss substantive content in clinical-ethics tasks | 7 | 2 |
| 11 | LLM-generated peer review feedback is paper-specific not generic boilerplate | 2 | 2 |
| 12 | Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs | 3 | 3 |

**Coverage:** 42 of 77 EVDs (55%) participate in at least one EP. The remaining 35 EVDs are singletons or paper-specific findings that don't generalize to a 2-paper-minimum cross-paper pattern. Some EVDs participate in multiple EPs (e.g., Roberts's per-item r=0.02-0.06 EVD instantiates both EP2 and EP5; Lou's o3-mini EqInfer EVD instantiates both EP1 and EP4).

**Files touched:**
- `evd-patterns/` — new folder with 12 EP files.
- `evidence/EVD*.md` × 42 — `## Instantiates Pattern(s)` reverse-link sections inserted between `## Supports Claim(s)` and end-of-file.
- `HISTORY.md` — this entry; phase index extended.

**Lessons.**
1. **Cross-paper patterns reveal corpus structure that single-paper claims hide.** A finding like "LLM-human aggregate-level agreement masks per-paper near-zero correlation" doesn't surface from any one paper — it requires reading Roberts and Liang and Huntington-Klein together. EPs are how the discourse graph encodes that meta-reading.
2. **The 2-paper threshold is the right floor.** Below 2 papers, the "pattern" is just a single-paper finding repackaged. At 2 papers, you have minimal triangulation; at 3+ papers with methodological diversity, the pattern is robust. Stronger patterns in this corpus (per-item variance, class-imbalance failure) hit 5+ papers naturally.
3. **EPs are draft-status by default.** Like other node types, EPs start at `NodeFormality: draft` until a human reviews. The TruthValue field starts at 0.65–0.80 reflecting the cross-paper convergence — higher than a single paper's CLM, lower than a multi-paper meta-analysis.

---

## 2026-04-29 (Phase 25 — `ESS.base` Obsidian Bases index)

New `ESS.base` (Evidence-Synthesis System) at the vault root. Obsidian Bases file that lets the reader slice all 184 discourse-graph nodes (QUE / CLM / EVD / CVT) by every tag namespace built across Phases 22–24.

**Twenty-two views, in five families:**

- **Everything** — `All nodes` (default table sorted by Type then Title).
- **By node type** (4) — Questions / Claims / Evidence / Caveats.
- **By 5C dimension** (5) — Credibility / Clarity / Creativity / Connectivity / Care, each filtering on the `5c/<dim>` tag.
- **By methodological rigor — EVD-only** (5) — TRIPOD-LLM compliance high / moderate / low; appraisal external-validity-high-risk; appraisal statistical-rigor-high-risk.
- **CVT methodologist filters** (6) — high-severity caveats; inferred-only (vs. author-stated); per-validity-domain caveats (external / internal / construct / reproducibility).
- **Workflow** (1) — Drafts (NodeFormality:draft) for the verbatim-audit fix queue.

**Formulas defined** so cells are tidy:
- `formula.node_type` — derives `QUE` / `CLM` / `EVD` / `CVT` from folder.
- `formula.short_title` — strips the `<TYPE> - ` prefix from filenames so the visible title fits in a table cell.

**Filter strategy** — every view uses tag-membership (`tags.contains(...)`) rather than walking node bodies, so the base is fast to render and updates automatically when a node's tags change.

**Files touched:**
- `ESS.base` — new file at vault root.
- `ESS.md` — new wrapper-page that embeds the base via `![[ESS.base]]` and surrounds it with a tag-legend (5C / appraisal / TRIPOD-LLM / CVT axes), view-by-view "what to click for what" prose, and links back to Welcome / DGRAPH / DGRAPH-TABLE / HISTORY / Skill. Without this wrapper, an outsider clicking `ESS.base` sees tabs but no decode key for tag values like `appraisal/external-validity/high-risk` or `L0-M3-H2`.
- `Welcome.md` — navigation block expanded from "three ways in" to "four ways in" with a new 🟪 entry pointing to ESS for property-filter access.
- `DGRAPH.md` — `> [!tip] Other entry points` callout added at the top so readers landing on the nested view see the table-and-base alternatives immediately.
- `HISTORY.md` — this entry; phase index extended.

---

## 2026-04-29 (Phase 24 — CVT methodologist tags + 5C Research Dimension tags)

Two additions in one phase, both filterable as Obsidian tag chips:

### CVT methodologist tags (49 CVTs)

Each CVT now carries 4+ tags describing the *kind* of methodological/statistical limitation it represents, in vocabulary a research methodologist or statistician would recognize. Four axes:

1. **Validity domain** — exactly one tag from the 5-bucket appraisal taxonomy (mirrors `## Critical appraisal` rubric):
    - `cvt/domain/{construct-validity, internal-validity, external-validity, statistical-rigor, reproducibility}`
2. **Specific mechanism** — one or more tags from a controlled vocabulary of ~30 terms (Phase 24 final list):
    - **Sample / Data:** `small-sample`, `single-domain`, `single-discipline`, `single-conference`, `data-leakage`, `test-contamination`, `selection-bias`, `self-selection-bias`, `class-imbalance`, `publication-bias`, `excluded-cases`, `ecological-invalidity`
    - **Model / Treatment:** `single-model`, `version-drift`, `closed-source-only`, `single-prompt`, `prompt-sensitivity`, `training-cutoff-confound`, `gui-not-api`, `iterative-protocol`
    - **Evaluation / Ground truth:** `llm-as-judge`, `self-evaluation`, `single-rater`, `low-iaa`, `proxy-metric`, `aggregate-reporting`, `mixed-train-test`, `self-reported-ground-truth`, `annotator-circularity`, `measurement-gap`
    - **Statistical:** `no-confidence-intervals`, `no-significance-testing`, `no-multiple-comparison-correction`, `low-power`
    - **Reproducibility:** `inference-params-undisclosed`, `prompt-undisclosed`, `code-unreleased`, `data-unreleased`
3. **Type** — mirrors existing `type:` frontmatter field: `cvt/type/{author-stated, inferred}`
4. **Severity** — mirrors existing `severity:` frontmatter field: `cvt/severity/{low, moderate, high}`

**Distribution surfaced (49 CVTs):**
- **Domains:** external-validity 22 · internal-validity 11 · construct-validity 8 · reproducibility 5 · statistical-rigor 3.
- **Most common mechanisms:** small-sample 7 · excluded-cases 5 · single-rater 4 · single-domain 4 · selection-bias 4 · proxy-metric 4. Confirms the corpus-wide pattern that *generalizability* and *evaluation-construct* limitations dominate over *statistical* ones (papers often skip CIs but reviewers don't always flag this as a CVT).
- **Severity:** moderate 42 · high 5 · low 2 — most CVTs sit at moderate (the bar for "low" is rarely reached, and "high" requires an obvious paper-killing flaw).
- **Type:** author-stated 37 · inferred 12 — most caveats come from authors flagging their own limitations, not from outside-in inference.

### 5C Research Dimension tags (all 184 DG nodes)

Per user spec, each QUE / CLM / EVD / CVT now carries one or more 5C tags identifying which research-quality dimension(s) the node touches:

- `5c/credibility` — rigor (study design, error detection, risk-of-bias assessment, methodological evaluation)
- `5c/clarity` — reporting-guideline alignment (CONSORT, PRISMA, AMSTAR, STROBE, ROBINS-I, QUADAS-2, PRECIS-2, etc.)
- `5c/creativity` — novelty + value (novelty assessment, peer-review feedback for innovation)
- `5c/connectivity` — connections to other research and practice (citation integrity, quotation errors)
- `5c/care` — ethics (IRB review, informed consent, ethical review of clinical proposals)

**Per-paper 5C map** (used for EVD and CVT inheritance — each EVD/CVT inherits its paper's dimensions):

| Paper (citekey) | 5C dimensions |
| --- | --- |
| akyon | clarity, credibility |
| alharbi | clarity |
| bougie | credibility, clarity, creativity |
| darcy | credibility, clarity, creativity |
| hasan | credibility |
| huntington-klein | credibility |
| idahl | credibility, clarity, creativity |
| leucuta | credibility |
| liang | credibility, clarity, creativity |
| liu | credibility |
| lou | credibility, clarity, creativity |
| roberts | clarity |
| sarol | connectivity |
| shahid | creativity |
| son | credibility |
| sridharan-decision | care |
| sridharan-leveraging | care |
| srinivasan | clarity |
| thelwall | credibility |
| tyser | credibility, clarity, creativity |
| woelfle | clarity, credibility |
| wrightson | clarity |
| wu | creativity |
| xu | credibility |
| zhang2024 | connectivity |
| zhang2025 | credibility |
| zhou | credibility, clarity, creativity |

QUEs and CLMs are classified by title keywords (intersection with their Papers-block paper-dimensions when intersection is non-empty; title-only fallback otherwise). Multiple dimensions allowed.

**Corpus distribution (across all 184 nodes):**
- credibility 124 · clarity 99 · creativity 65 · connectivity 14 · care 13.

The bias toward credibility + clarity reflects the corpus's focus on automated evaluation of research quality and reporting compliance. Connectivity and care are the smaller dimensions — citation-integrity papers (Sarol, Zhang2024) drive the connectivity tag; IRB papers (the two Sridharan studies) drive the care tag.

**Files touched:**
- `caveats/CVT*.md` × 49 — 4+ methodology tags per CVT inserted in `tags:` block; `updated:` bumped to 2026-04-29.
- `evidence/EVD*.md` × 77 — 5C tags appended to existing rigor tags.
- `claims/CLM*.md` × 31 — 5C tags inserted (no prior tags block existed).
- `questions/QUE*.md` × 27 — 5C tags inserted.
- `SKILL.md` — Key Principles #14 (CVT methodology tags) and #15 (5C dimension tags) added.
- `HISTORY.md` — this entry; phase index extended.

**Lessons.**
1. **Methodology vocabulary needs to be bottom-up, not top-down.** I started with PROBAST/ROBINS-I/QUADAS-2 domains and discovered the corpus uses different mechanisms. The final 30-term mechanism vocabulary was extended during the actual CVT classification (added `excluded-cases`, `self-reported-ground-truth`, `iterative-protocol`, `annotator-circularity`, `measurement-gap`, `prompt-sensitivity`, `ecological-invalidity` because those patterns showed up). Future corpus extensions may need additional terms; keep the vocabulary open-ended in HISTORY.md.
2. **5C tags surface real corpus structure.** The dominance of credibility + clarity (and the relative scarcity of care + connectivity) reflects the actual research focus, not a tagging artifact. Useful for spotting underrepresented dimensions when planning new paper additions.
3. **Title-based classification works for QUEs/CLMs even when the Papers block is small.** A QUE titled "Can NLP models automatically identify citation integrity errors..." classifies cleanly to connectivity even though only one paper (Sarol) is in its Papers block. Title is more informative than citekey union for these node types.

---

## 2026-04-29 (Phase 23 — paper-level rigor tags on every EVD)

User asked: each EVD should carry tags summarizing the paper's Critical Appraisal ratings (by domain) and the TRIPOD-LLM reporting compliance (condensed into a summary score / proportion). Tags inherit from the source page so a reader can filter EVDs by methodological rigor without opening individual papers.

**8 tags per EVD** (all 77 EVDs across 27 papers):
- 5 per-domain appraisal tags: `appraisal/<domain-slug>/{low-risk,some-concerns,high-risk}` for each of construct-validity / internal-validity / external-validity / statistical-rigor / reproducibility.
- 1 appraisal-summary tag: `appraisal/overall/L<n>-M<n>-H<n>` (counts of low / some-concerns / high across the 5 domains).
- 1 TRIPOD-LLM compliance bucket: `tripod-llm/compliance/{high,moderate,low}` — high ≥80% ✅ rate, moderate 60–80%, low <60%. Proportion = ✅ / (✅+⚠️+❌); ➖ rows are excluded as not applicable.
- 1 TRIPOD-LLM raw proportion: `tripod-llm/proportion/<NN>pct`.

**Corpus-wide patterns surfaced by the tagging:**
- **Critical appraisal:** 51 of 77 EVDs (66%) have **zero** 🟢 low-risk domains across the 5 dimensions; only 10/77 hit ≥2 low-risk domains. Most common pattern (21 EVDs) is 0 low / 3 some-concerns / 2 high.
- **TRIPOD-LLM:** 57 of 77 EVDs (74%) sit in the **low** compliance bucket; 20 in moderate; **0 in high**. The corpus's preprints (where most of these papers live) routinely miss item 12 (compute), 14a–c (funding/COI/protocol), and 5c (data dates), pushing every paper below the 80% ✅ threshold for the high bucket.

**Backfill script** (idempotent — overwrites the EVD's existing `tags:` block; reads the per-paper tags from each `source/@<citekey>.md` Critical-appraisal + TRIPOD-LLM tables):

```python
import re
from pathlib import Path

ICON_TO_BUCKET = {'🟢': 'low-risk', '🟡': 'some-concerns', '🔴': 'high-risk'}
DOMAIN_TO_SLUG = {
    'Construct validity': 'construct-validity',
    'Internal validity': 'internal-validity',
    'External validity': 'external-validity',
    'Statistical rigor': 'statistical-rigor',
    'Reproducibility': 'reproducibility',
}

def parse_appraisal(text):
    m = re.search(r'## Critical appraisal.*?(?=\n## |\Z)', text, flags=re.DOTALL)
    if not m: return None
    out = {}
    for row in re.finditer(
        r'^\|\s*\*\*([A-Za-z][^*]+?)\*\*[^|]*\|\s*([🟢🟡🔴])\s*\|',
        m.group(0), flags=re.MULTILINE,
    ):
        out[row.group(1).strip()] = row.group(2)
    return out

def parse_tripod(text):
    m = re.search(r'## TRIPOD-LLM reporting summary.*$', text, flags=re.DOTALL)
    if not m: return None
    counts = {'green': 0, 'yellow': 0, 'red': 0, 'gray': 0}
    for row in re.finditer(
        r'^\|\s*\*\*[^*]+\*\*\s*\|[^|]+\|\s*([^|]+?)\s*\|',
        m.group(0), flags=re.MULTILINE,
    ):
        cell = row.group(1)
        if '(per-EVD)' in cell: continue
        for icon, key in [('✅','green'),('⚠️','yellow'),('❌','red'),('➖','gray')]:
            if icon in cell:
                counts[key] += 1
                break
    return counts

def compute_tags(source_text):
    rat = parse_appraisal(source_text); cnt = parse_tripod(source_text)
    tags = []; counts = {'low-risk': 0, 'some-concerns': 0, 'high-risk': 0}
    if rat:
        for domain, slug in DOMAIN_TO_SLUG.items():
            icon = rat.get(domain)
            if icon:
                bucket = ICON_TO_BUCKET[icon]
                tags.append(f'appraisal/{slug}/{bucket}')
                counts[bucket] += 1
        tags.append(f'appraisal/overall/L{counts["low-risk"]}-M{counts["some-concerns"]}-H{counts["high-risk"]}')
    if cnt:
        applic = cnt['green'] + cnt['yellow'] + cnt['red']
        if applic > 0:
            prop = cnt['green'] / applic
            pct = round(prop * 100)
            bucket = 'high' if prop >= 0.80 else 'moderate' if prop >= 0.60 else 'low'
            tags.append(f'tripod-llm/compliance/{bucket}')
            tags.append(f'tripod-llm/proportion/{pct}pct')
    return tags

VAULT = Path('.')
tag_map = {sf.stem[1:]: compute_tags(sf.read_text())
           for sf in (VAULT/'source').glob('@*.md')}
for evd_file in (VAULT/'evidence').glob('EVD*.md'):
    m = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)\.md$', evd_file.name)
    if not m: continue
    tags = tag_map.get(m.group(1), [])
    if not tags: continue
    text = evd_file.read_text()
    tag_yaml = 'tags:\n' + ''.join(f'  - {t}\n' for t in tags)
    if re.search(r'^tags:\s*\n(?:  - .+\n)+', text, flags=re.MULTILINE):
        new_text = re.sub(r'^tags:\s*\n(?:  - .+\n)*', tag_yaml, text, count=1, flags=re.MULTILINE)
    else:
        new_text = re.sub(r'^(aliases:\s*\n)', r'\1' + tag_yaml, text, count=1, flags=re.MULTILINE)
    evd_file.write_text(new_text)
```

Re-run this whenever a source page's Critical-appraisal or TRIPOD-LLM table changes.

**SKILL.md** Key Principle #13 added making 8-tag inheritance a creation-time requirement on every EVD; points back to this Phase 23 backfill script.

**Files touched:**
- `evidence/EVD*.md` × 77 — `tags:` block inserted after `aliases:` with the 8 tags; `updated:` bumped to 2026-04-29.
- `SKILL.md` — Key Principle #13 added.
- `HISTORY.md` — this entry; phase index extended.

**Lessons.**
1. **Tags should be inheritable.** Per-domain appraisal ratings + TRIPOD-LLM compliance live on the *source page*, but they're more discoverable as *EVD-level filters*. Inheriting paper-level tags into each EVD trades a little redundancy for huge skim/search benefit (filter all EVDs from external-validity-🔴 papers in one click).
2. **Tag values should be semantic, not raw counts.** `appraisal/external-validity/high-risk` is filterable; `appraisal/external-validity/red` is not (Obsidian tag autocomplete works on the slug, not the rendered colour). Same for TRIPOD-LLM compliance buckets — high/moderate/low rather than ≥80%/60-80%/<60%.
3. **Keep raw proportion as a separate tag** for sortable precision (`tripod-llm/proportion/73pct`) while the bucket gives the categorical filter.

---

## 2026-04-29 (Phase 22 — populated `nodeID` on all 184 DG nodes)

User flagged that every QUE / CLM / EVD / CVT had an empty `nodeID:` field in its YAML frontmatter — present as a key, but never populated. These IDs are intended as stable, file-rename-safe identifiers for the node (matching the `nodeInstanceId` pattern already in `source/@*.md` files).

Backfilled all 184 nodes with **UUIDv7** identifiers in one pass:
- 27 QUEs · 31 CLMs · 77 EVDs · 49 CVTs.
- Format: `019ddb4e-6bb2-76ba-b708-0b0c889ba6c5` (UUIDv7 — timestamp-prefixed, matches the format used by `nodeInstanceId` in source files).
- All 184 IDs verified unique (one-pass `sort -u` check).

The backfill script (idempotent — only touches nodes whose `nodeID:` is currently empty):

```python
import re, uuid
from pathlib import Path
for folder in ('evidence', 'claims', 'caveats', 'questions'):
    for f in Path(folder).glob('*.md'):
        text = f.read_text()
        if re.search(r'^nodeID:[ \t]*\S', text, re.MULTILINE):
            continue  # already populated
        new_text = re.sub(
            r'^nodeID:[ \t]*\s*$',
            f'nodeID: {uuid.uuid7()}',
            text, count=1, flags=re.MULTILINE)
        if new_text != text:
            f.write_text(new_text)
```

**SKILL.md updated:**
- All 4 node-template bodies (EVD/CLM/CVT/QUE) now show `nodeID: <UUIDv7 — generate with python3 -c "import uuid; print(uuid.uuid7())">` instead of blank.
- New Key Principle #12 makes populated nodeID a creation-time requirement and points back to the backfill script in this Phase 22 entry for any future empty-field cleanup.

**Files touched:**
- `evidence/EVD*.md` × 77 — `nodeID` populated.
- `claims/CLM*.md` × 31 — `nodeID` populated.
- `caveats/CVT*.md` × 49 — `nodeID` populated.
- `questions/QUE*.md` × 27 — `nodeID` populated.
- `SKILL.md` — 4 templates updated; Key Principles extended.
- `HISTORY.md` — this entry; phase index extended.

---

## 2026-04-28 (Phase 21 — DGRAPH-TABLE.md + quote-screenshot collision audit + 4 missing QUE aim quotes)

Three additions, all closing loops opened by user feedback:

**1. New `DGRAPH-TABLE.md` index file at vault root.** A flat paper × node-type matrix synthesized from the discourse graph: rows are the 27 papers, columns are QUE / CLM / EVD / CVT, cells contain wikilinks (with `<br>` line breaks for multi-link cells). For QUE/CLM, only papers in the **Papers block** are counted (not transitively-reachable papers via supporting-CLM auto-derivation), giving accurate per-paper counts: 32 QUE links, 42 CLM links, 77 EVDs, 49 CVT links across the 27 papers. Complements (does not replace) `DGRAPH.md`'s nested QUE → CLM → EVD → CVT view.

**2. Quote-screenshot filename-collision audit + fix (25 renames).** User flagged a Leucuta CVT where the markdown quote ("Fourth, we used only one single standardized prompt…") didn't match the screenshot highlight ("Third, we evaluated only the publicly available versions…"). Root cause: two different Leucuta CVTs both pointed to the same PNG filename `leucuta…-cvt-p17-1.png`. The pipeline regenerates the same file twice during a `--force` run; the *last-processed* quote wins, silently leaving a screenshot whose highlight matches a different quote than the one displayed in the markdown.

Built a vault-wide audit detecting **24 such collisions** across 25 affected embeds — distinct quotes sharing a quote-region PNG filename. Surface patterns:
- Within one EVD: Description quote + What/How/Who quotes sometimes pointed to the same PNG filename (e.g., Bougie EVD with `-evd-p11-1.png` reused for two distinct quotes).
- Across multiple CVTs of the same paper: two Leucuta CVTs at p.17, two Roberts CVTs at p.1, two Wrightson CVTs at p.1, two Sridharan-Decision CVTs at p.6, etc.
- Across multiple QUEs of the same paper: three Liu & Shah QUEs all pointed at `liu…-que-p2-1.png` (one filename for three different question quotes).

Fix: rename collisions in lockstep — keep the first occurrence's filename, give each subsequent occurrence the next available `-pN-<idx>.png` suffix. Then run the screenshot pipeline; new files get generated with their distinct names and correct highlights.

**SKILL.md updated** with a non-negotiable "one quote → one PNG filename" rule under PNG naming, plus a small Python audit script to re-run on demand.

**3. Four missing QUE aim quotes filled.** The Phase 20 QUE content cleanup left 4 QUEs quote-empty because their previous quotes were findings rather than aims. Spawned 4 parallel subagents to read the source PDFs and fetch verbatim research-question / aim / objective passages. All 4 succeeded:

- **Idahl QUE** — "OpenReviewer addresses this gap, aiming to provide authors with valuable pre-submission feedback that closely mirrors the standards and expectations of human peer reviewers." (p. 2)
- **Liang QUE** — "In this work, we present the first large-scale systematic analysis characterizing the potential reliability and credibility of leveraging LLM for generating scientific feedback." (p. 2)
- **Srinivasan QUE** — "In this paper, we leverage LLMs to evaluate CONSORT reporting in RCT publications at scale. We first validate our approach on the CONSORT-TM dataset Kilicoglu et al. [2021] with expert review, then analyze reporting trends across 21,041 RCTs from 1966-2024." (p. 2)
- **Multi-paper "How does LLM performance vary…" QUE** — three verbatim aim quotes (one each from Hasan 2024 p. 2, Leucuta 2025 p. 2, Alharbi & Asiri 2024 p. 2).

Screenshots generated for all 4 via the canonical-naming pipeline.

**Files touched:**
- `DGRAPH-TABLE.md` — new file (49 KB), 27 rows × 4 node-type columns.
- `SKILL.md` — added "one quote → one PNG filename" rule + audit script under PNG naming section.
- `HISTORY.md` — this entry; phase index extended.
- `caveats/CVT*.md` — 6 files renamed embeds (Leucuta, Roberts, Sridharan-Decision, Sridharan-Leveraging, Son, Wrightson, Zhang2024, Zhang2025, Shahid).
- `claims/CLM*.md` — 4 files renamed embeds (Idahl, Xu × 2, Multi-agent).
- `evidence/EVD*.md` — 9 files renamed embeds.
- `questions/QUE*.md` — 4 files restored aim quotes; 2 had renamed embeds.

**Bonus pipeline bug-fix surfaced during the multi-paper QUE work.** The `get_papers_from_block` regex in `misc/scripts/quote_pipeline.py` was `(?:>\s*\[\[@.*?\]\]\s*\n?)+`, which stopped at the first blank `>` separator line between papers. So in multi-paper blocks formatted as

```
> [!info] Papers
> [[@hasan…]]
>
> [[@leucuta…]]
>
> [[@alharbi…]]
```

only `hasan` was captured; Leucuta and Alharbi quotes were silently misattributed to the Hasan citekey. Patched to `(?:>.*\n?)+` so the block parser tolerates blank `>` separator lines. Also fixes the analogous mis-attribution in the cross-paper QUE *"How accurately can LLMs assess or understand medical research papers…"*.

**Lessons for future runs.**
1. **Run the collision audit before `--force`.** A naive `--force` regeneration silently corrupts collisions. The audit script in SKILL.md takes seconds and surfaces them upfront.
2. **The pipeline's pre-existing "skip-if-embed-exists" behaviour silently masks collisions.** When the same PNG is referenced from two markdown locations, the pipeline writes both quotes to the same file in sequence. There's no error. The only symptom is a stale screenshot. Hardening idea: have `quote_pipeline.py` track filenames written within a run and warn if the same name is rewritten with a different bbox.
3. **`--force` is not idempotent across collisions.** Re-running it doesn't fix a collision because both quotes still point to the same name; the last-processed-quote determinism is the same each time. The fix has to happen at the markdown level (rename embeds) before re-running.
4. **Regexes that match "list of `> [[@…]]` lines" need to tolerate blank `>` separators** — the readability pass (Phase 7) and Obsidian linters both insert them between consecutive blockquoted wikilinks. A strict alternation regex will see only the first item.

---

## 2026-04-28 (Phase 20 — external-framework cross-reference, Mermaid renderability audit, QUE content rule + cleanup)

Three follow-up additions after Phase 19, all closing loose ends:

**1. External appraisal frameworks per source page.** Each `## Critical appraisal` section now ends with a `> [!tip]` callout naming the most-applicable external standards beyond TRIPOD-LLM. Two stable templates:
- Clinical-AI papers (10 of 27) get **MI-CLAIM** (Norgeot et al. 2020) for clinical-AI minimum information, **MINIMAR** (Hernandez-Boussard et al. 2020) for medical-AI reporting, and **PROBAST+AI** (Wolff et al. 2019 base; AI extension in development) for prediction-model risk of bias.
- NLP / general-benchmarking papers (17 of 27) get **HELM** (Liang et al. 2022) for holistic LLM-evaluation principles, **Datasheets for Datasets** (Gebru et al. 2021) for the evaluation corpus, and **Model Cards** (Mitchell et al. 2019) for the LLMs being evaluated.

Per-paper special-case additions: **CLAIM** (Mongan et al. 2020) for Wrightson's GPT-4 Vision sub-study; **STARD-AI** / **QUADAS-AI** for Leucuta's diagnostic-accuracy framing; **PROBAST+AI** for Sarol, Wu, and Shahid (each has a supervised classifier component); **PROBAST** for Huntington-Klein's causal-inference framing; **ML Reproducibility Checklist** for Idahl's fine-tuning pipeline.

The cross-reference is intentionally light — one callout line per page, not a separate compliance table. Readers wanting a deeper appraisal in any single framework can pull the checklist themselves; the source page just points them to the right one.

**2. Mermaid renderability audit across 105 blocks.** Programmatic check on every `flowchart`, `xychart-beta`, and `pie` block across the 27 source pages — verified numeric `bar []` values, balanced quotes in x-axis lists, well-formed y-axis range syntax, no unquoted parens in flowchart node labels, no colons in pie titles. **0 issues found.** All 105 blocks pass cheap and deeper sanity checks; rendering should be clean in Obsidian.

**3. QUE content rule + cleanup.** User clarification: each QUE's `### Snippet: Quote(s) & Screenshots` block must contain *only* the paper's research question, goal, aim, objective, or purpose statement — never methods, results, or claim content. Audited all 27 QUE files against this rule:

- **13 QUEs had non-question content** mixed in (typically a methods-or-results quote alongside a legitimate aim quote). Removed the offending quote + its associated screenshot embed from each.
- **4 QUEs are now quote-empty** because both their quotes were findings/methods rather than aims (Idahl, Srinivasan, Liang, the cross-paper "How does LLM performance vary…"). Each quote-empty QUE got an italicized placeholder noting that a verbatim aim/objective passage from the source paper is needed — explicit gap so a future pass knows to add one.
- **11 orphaned QUE quote PNGs deleted** from `evidence/Attachments/` (3 page-level table/figure PNGs kept because they're still referenced from source pages or EVDs).

The new content rule is now codified in `SKILL.md` Step 4 → QUE template body section, with both ✅ and ❌ examples and an explicit note that mixed sentences (aim + finding in the same quote) should be trimmed to the aim or replaced with a different question-framing quote from the same paper.

**Files touched:**
- `source/@*.md` × 27 — `> [!tip] Applicable external appraisal frameworks…` callout appended to each `## Critical appraisal` section.
- `questions/QUE*.md` × 13 — non-question quote+screenshot pairs removed; 4 of those left with a placeholder note.
- `SKILL.md` — QUE template body augmented with the QUE quote/screenshot content rule (✅/❌ examples + trim guidance).
- `HISTORY.md` — this entry; PNG inventory updated (614 → 603); phase index extended.
- `evidence/Attachments/` — 11 orphaned QUE quote PNGs deleted; 3 still-referenced ones kept.

**Lessons for future runs.**
1. **The discourse-graph node types are not interchangeable.** EVDs hold methods + results, CLMs hold conclusions, CVTs hold limitations, QUEs hold *only* questions/aims. When extracting from a paper, the same passage often spans multiple node-type roles — it's the extractor's job to split it. The Phase 20 cleanup found 13 cases where this hadn't been done cleanly.
2. **Quote-empty placeholders beat misleading content.** When the available quote isn't actually a question/aim, leaving an explicit *(needs a verbatim aim passage)* note is better than keeping a non-question quote that misleads the reader. The placeholder is auditable; misleading content is not.

---

## 2026-04-28 (Phase 19 — source-page synthesis: structured abstract + visualizations + critical appraisal)

User feedback: each `source/@<citekey>.md` had become a TRIPOD-LLM compliance table and nothing else — useful for auditing reporting but unhelpful as the entry point for a human trying to learn what a paper actually shows. Three additions, all synthesized from the discourse-graph nodes (no PDF re-read):

**1. Structured abstract** at the top of each source file. Five sub-sections in plain language (high-school-graduate target, active voice):
- **Question** — paper's research question + design comparison, ending with a wikilink to the matching QUE.
- **Methods** — Design / Tools / Procedure / Sample, condensed from the EVDs' Methods Context blocks.
- **Findings** — one bullet per EVD with concrete numbers + jargon glossed inline (F1, kappa, p-values, AUC), each ending with `[[EVD - …]]`.
- **Claim supported** — wikilinks to each CLM, plus an editorial framing sentence about deployment readiness.
- **Caveats** — wikilinks to each CVT applying to this paper's EVDs.

**2. Mermaid visualizations** appended inside the structured abstract:
- `### Methods at a glance` — `flowchart TD` with a four-class palette (data sources / steps / models / results) and bolded sample-size milestones inside node labels.
- `### Results at a glance` — one to three `xychart-beta` bar charts and/or a `pie showData` chart, with one-sentence lead-ins explaining what each chart shows and what counts as "good".

Every plotted value is grounded in an EVD's Description, Other-Notes item-17 mini-table, or the existing TRIPOD-LLM table — no invented numbers.

**3. Critical appraisal section (`## Critical appraisal`)** between the structured abstract and the TRIPOD-LLM table. **This is methodological-quality assessment, not reporting compliance** — the two are explicitly separated and now sit side-by-side on the source page. Five domains, each rated 🟢 Low risk · 🟡 Some concerns · 🔴 High risk with a 1–3-sentence justification grounded in the paper's EVDs/CVTs:

- **Construct validity** — does the metric / task actually measure the deployment construct?
- **Internal validity** — could the comparison be biased? (test-set contamination, data leakage, confounded prompts, asymmetric scoring rules, LLM-judge-of-LLM circularity.)
- **External validity** — do findings generalize beyond this dataset / model / domain?
- **Statistical rigor** — appropriate uncertainty estimates, multiple-comparison correction, sample size for the rare/important class, paired vs. independent tests, confidence intervals.
- **Reproducibility** — code + data availability, deterministic outputs, proprietary-API dependencies, dated model snapshots.

Each table ends with a `**Bottom line.**` paragraph giving the practical takeaway.

**Calibration tendencies surfaced across the corpus:**
- **External validity** is the most common 🔴 — 19 of 27 papers (single-discipline / single-conference samples, English-only, opt-in user studies, evaluation against a single human comparator).
- **Statistical rigor** is the second most common 🔴 — most papers report point estimates without confidence intervals, paired tests, or multiple-comparison correction across the typical 5+ models × 3+ metrics grid.
- **Internal validity** is 🔴 mainly via LLM-judge-of-LLM circularity and asymmetric scoring rules favouring the LLM (e.g., GPT got 3 prompt re-runs while humans got 1 in Alharbi).
- **Construct validity** flagged sharply for Roberts (overall 4.92% gap masks near-zero per-paper Pearson correlations on most CONSORT-A items) and Srinivasan (presence-not-accuracy compliance metric).

**Sarol** served as the canonical pilot — the structured abstract was rewritten in plain-language active voice after a first draft was judged jargon-heavy, then the Mermaid visualizations + critical-appraisal section were added. The remaining 26 papers were processed via parallel subagents using a shared brief at `misc/prompts/2026-04-28-structured-abstract.md`. All 26 succeeded on first run (no watchdog stalls — the bundled task was tractable since the discourse-graph nodes are already small and well-structured).

**Recurring node-graph gap surfaced by subagents.** Many CVTs' `appliesTo` frontmatter lists multiple EVDs, but the corresponding EVDs' `## Caveats` sections only show some of those CVTs. This is a sync-direction artifact — the reverse-link pass populates EVD `## Caveats` from CVT `appliesTo`, and the populated CVT lists are sometimes narrower than the body of the CVT actually warrants. Worth a follow-up pass on `scripts/reverse_links.py` to either widen `appliesTo` lists or re-run the reverse-link build. Specific cases noted by subagents are recorded in their per-paper return messages.

**Files touched:**
- `source/@*.md` × 27 — `## Structured abstract` (with Methods + Results Mermaid visualizations) and `## Critical appraisal` sections inserted between the frontmatter and the existing `## TRIPOD-LLM reporting summary`. Frontmatter and TRIPOD-LLM table left untouched.
- `SKILL.md` — workflow expanded from 12 to 13 steps; new Step 6 details + sub-steps 6.b (Mermaid visualizations) and 6.c (5-domain critical appraisal) added with the Sarol source file as the canonical example.
- `misc/prompts/2026-04-28-structured-abstract.md` — subagent brief with schema, readability rules, Mermaid templates, and the 5-domain rubric.
- `HISTORY.md` — this entry; phase index extended.

**Lessons for future runs.**
1. **Synthesis from the graph beats re-reading the PDF.** Once EVDs / CLMs / CVTs / QUEs are extracted with the Phase 18 schema, the source-page abstract + appraisal is a derivation, not a fresh read. Subagents that bundle abstract + viz + appraisal in one pass take ~2 min/paper and don't trip the watchdog because they don't re-read PDFs.
2. **Plain-language abstracts need at least one rewrite pass.** The first Sarol draft was technically correct but read as jargon soup ("→" arrows, statistical notation without inline glosses, dense parenthetical citations). A high-school-graduate readability pass converts each EVD finding into a bold lead sentence + 2–3 sentences of actual numbers with definitions inline. Subagents in this batch were given that explicit rule and produced consistently readable output on first try.
3. **Reporting compliance and methodological quality belong in different sections.** The TRIPOD-LLM table answers "did they say it?"; the critical appraisal answers "does the design support their conclusions?". Reading subagent reports across the 26 papers, a paper can be ✅ across most TRIPOD-LLM rows and still be 🔴 on construct validity (Roberts, Srinivasan are clear examples). Keeping them in separate sections forces the reader to evaluate both.

---

## 2026-04-28 (Phase 18 — TRIPOD-LLM EVD rewrite)

User feedback: the Methods Context blocks on EVDs (What/How/Who) read inconsistently and didn't surface enough of each paper's actual methodology. Replaced with a structured schema, lifted paper-level reporting compliance into the source files, and ground every quote in the actual PDF text.

**1. New Methods Context schema** (every EVD across all 27 papers).
- **What?** = `Study design` + `Method type` + `Tools` + `Dependent variables` + `Independent variables / covariates` + verbatim grounding quote.
- **How?** = `Procedure` (step-by-step: preprocessing, model training, prompt construction, statistical tests) + verbatim quote.
- **Who?** = `Models / participants` + `Sample-size flow` (original sourced → exclusions → final analyzed) + verbatim quote.

The free-form prose blocks of the prior format are gone; in their place is a parity-enforced schema that lets a reader skim any EVD and find the same slots in the same order.

**2. Per-paper TRIPOD-LLM reporting summary** lifted from each EVD's `## Other Notes` into `source/@<citekey>.md` (previously frontmatter-only). The table covers all 37 sub-items (Methods 5a–15 + Results 16a–18) of the [TRIPOD-LLM checklist (Gallifant et al., 2024)](https://www.tripod-statement.org/tripod-llm/) and adds a **compliance icon column**:

- ✅ fully reported · ⚠️ partially reported / unclear · ❌ should be reported but missing · ➖ not applicable to this study.

The icons let a reader skim alignment with TRIPOD-LLM at a glance — in aggregate, the corpus shows item 12 (compute) and 14a–c (funding/COI/protocol) as the most commonly-missing items, while items 5a/5b/16a (data sources / distribution / flow) are usually fully reported. Item 17 (Performance) stays in each EVD's Other Notes as an EVD-specific mini-table since the numbers vary per finding.

**3. Canonical screenshot naming** for EVDs. The pipeline's `quote_count_per_page` was lifted to a per-(citekey, kind, page) global counter so canonical `{citekey}-evd-p{N}-{idx}.png` names don't collide across multiple EVDs of the same paper. **All 27 papers' EVD quote-region crops were regenerated** with canonical naming; 28 orphaned old-style `-quote-<slug>-{desc,what,how,who}-p{N}.png` crops were deleted.

**4. SKILL.md** Step 4 rewritten with the new EVD body template (What/How/Who schema), and a new Step 4b documenting the source-file TRIPOD-LLM table format and compliance-icon legend.

**5. Execution.** The Sarol paper served as the canonical pilot (4 EVDs, source-file table, canonical PNGs). 26 subagents then ran in parallel, one per remaining paper. Three stalled mid-run on the watchdog timeout but had completed enough work that retry agents needed only to finish the source-file table; one (Hasan) had actually completed before the watchdog triggered. All 26 retries succeeded.

**Counts after this phase:**
- 77 EVDs rewritten (4 Sarol + 73 across the 26 subagent papers).
- 27 source files now carry a 37-row TRIPOD-LLM compliance table.
- 222 new canonical-named EVD screenshots (light-red highlights).
- 28 orphaned old-style EVD crops deleted.
- 4 quote-location failures (3 Woelfle en-dash mangling — known SKILL.md edge case; 1 Liu page-number typo `p. 33` — page does not exist in the PDF). EVDs without screenshots in those slots still have the verbatim quote as text.

**Files touched:**
- `scripts/quote_pipeline.py` — global `quote_count_per_page` shared across files of the same citekey within a single run.
- `SKILL.md` — Step 4 EVD template + new Step 4b for source-file TRIPOD-LLM table.
- `HISTORY.md` — this entry; Phase index extended; PNG inventory updated.
- `misc/prompts/2026-04-28-tripod-llm-evd-rewrite.md` — subagent brief.
- `source/@*.md` × 27 — `## TRIPOD-LLM reporting summary` section appended to each.
- `evidence/EVD - *.md` × 77 — Methods Context blocks rewritten with What/How/Who schema; Other Notes augmented with EVD-specific item-17 mini-table + link to source-file table; `updated:` bumped to 2026-04-28.
- `evidence/Attachments/` — 222 new EVD crops added with canonical naming; 28 old-style EVD crops deleted.

**Audit trail.** Every verbatim quote inserted by the subagents was grounded in the source PDF (after NFKD + alnum normalization) — no paraphrases were silently introduced. Where compliance icons were borderline (e.g., 6c when prompts are described but inference parameters are not), subagents reported their judgment in the per-paper return so future readers can re-evaluate.

### Lessons for future runs (do not repeat these mistakes)

The following gotchas surfaced during Phase 18 and are now codified in `SKILL.md` (workflow + Common pitfalls section). When adding a new paper or running another corpus-wide pass, this is the short version of what to watch for:

1. **Subagent watchdog stalls at 10 min of no-progress.** Four of 26 subagents (Wu, Wrightson, Woelfle, Hasan) stalled on long PDFs / many EVDs / chatty tool use. Mitigations:
   - Read PDFs in 10-page chunks, never the whole PDF at once.
   - One `Write` per file. Do not read-back to verify formatting.
   - Skip exploratory tool calls once the necessary content is in context.
   - Watchdog kills are recoverable — most stalled agents had completed 80%+ of the work. Always check artifact state before relaunching, and relaunch only what's missing.

2. **Strip old quote-region embeds before running the pipeline.** The pipeline inserts canonical-named embeds for quotes that don't already have one. If old `-quote-<slug>-{desc,what,how,who}-p{N}.png` embeds remain in the markdown, the pipeline thinks the slot is filled and skips it — leaving a stale filename pointing at content from a different page.

3. **Never hand-write quote-region embeds.** Authors wrote prose + verbatim quote; the pipeline appends `> ![[<citekey>-{evd|clm|cvt|que}-p<N>-<idx>.png]]`. Hand-written embeds with semantic slugs become inconsistent with the canonical naming and create filename-vs-content mismatches that resurface every time a quote moves pages.

4. **Item 17 stays in the EVD; items 5a–16d and 18 go in the source file.** Two subagents initially tried to put performance numbers in the source-file table; the canonical convention is "(per-EVD)" in the source-file row 17, with EVD-specific F1/kappa/prevalence in each EVD's `## Other Notes`.

5. **Compliance-icon calibration.** Several subagents flagged tendencies toward leniency (✅ for items only partially reported). The corpus pattern: 12 (compute), 14a–c (funding/COI/protocol on preprints), 5c (data dates) are usually `❌`. Marking them ⚠️ when authors omit them entirely sandbags the audit. Conversely, mark `➖` (not just ❌) when an item genuinely doesn't apply (e.g., 13 ethical approval for non-human-subjects NLP).

6. **En-dashes break verbatim quote matching.** The Woelfle paper writes "Human−AI collaboration" with an en-dash; markdown quotes typed as "Human-AI" (hyphen) fail Pass-1 full-segment match. When picking opening/closing anchors, avoid words containing en-dashes; the issue is documented in `SKILL.md` Step 3b.

7. **Source page citations in markdown are sometimes wrong.** The Liu & Shah 2023 EVD cites `p. 33` for content not on that page. The pipeline tolerates this by searching all pages, but quotes that genuinely aren't in the PDF (typos, paraphrases, or mis-cited material) just won't get a screenshot. Run the verbatim audit (`scripts/verbatim_audit.py`) after any large rewrite to catch these.

8. **Pipeline filename-collision protection** is per-(citekey, kind, page) and shared across all node files of the same citekey within a single pipeline run. The shared counter is in `quote_pipeline.py` `main()` and must persist across `process_node()` calls for it to work. Don't re-introduce a per-file counter — that's the bug Phase 18 fixed.

---

## 2026-04-27 (Phase 17 — quote screenshots: full-quote crops + per-kind colour highlighting + QUE coverage)

User feedback: some cropped screenshots were clipping the closing words of long quotes, and the reader had no visual cue for *which* text in the crop was the quoted material vs. surrounding context. Two-part fix:

**1. Never clip the quote.** Rewrote the quote-location algorithm in `scripts/quote_pipeline.py` (V3 → V4):
- Pass 1 now matches the entire quote (segment by segment if `…`/`...` present) and bboxes the union — long quotes no longer fall through to the height fallback.
- Pass 3 fallback height raised from **90pt → 300pt** so even when only the opening matches, the rest of the quote stays in frame.
- Bbox padding raised from 8pt → 12pt for legibility of descenders and adjacent text.

**2. Highlight the quote in the crop.** Each PNG now carries a `add_highlight_annot()` over the matched word rects, coloured by node type so the kind is identifiable at a glance:
- EVD = light red `(1.00, 0.70, 0.70)`
- CLM = light green `(0.72, 1.00, 0.72)`
- QUE = light blue `(0.72, 0.86, 1.00)`
- CVT = light gold `(1.00, 0.90, 0.55)`

**3. QUE coverage.** The pipeline now processes `questions/QUE*.md` too (previously it covered only EVD/CLM/CVT). Per-quote citekey is resolved from the `(Author, Year)` attribution against the QUE's `> [!info] Papers` block (single-paper QUEs use the only citekey directly).

**4. `--force` flag.** Regenerates existing screenshots in place using the original filename (so embeds in markdown don't have to be rewritten). Without `--force` the pipeline still skips quotes that already have a `> ![[...]]` embed.

**Counts after `python3 scripts/quote_pipeline.py --force`:**
- EVD: 114 regenerated.
- CLM: 54 regenerated.
- CVT: 56 regenerated.
- QUE: 29 new crops added (with embeds inserted into the QUE markdown) + 10 regenerated.
- 15 quote-location failures (10 CLM, 4 QUE, 1 EVD) — all pre-existing data issues where the markdown quote text doesn't appear in the source PDF (e.g., one cited as `p. 9344` is a page-number typo). These need manual fixes to the quote text itself, not pipeline changes.

**SKILL.md** Step 3b rewritten to make the two invariants (full quote inside, colour highlight) authoritative for future runs, with the new pipeline command, colour table, three-pass algorithm, padding/fallback values, and `--force` semantics documented inline. Future paper extractions inherit the new behaviour without needing this conversation.

**Files touched:**
- `scripts/quote_pipeline.py` — rewritten (V4).
- `SKILL.md` — Step 3b rewrite.
- `HISTORY.md` — this entry; inventory bumped (376 → 434 PNGs); phase index extended.
- `evidence/Attachments/` — 224 PNGs regenerated, 29 new QUE PNGs added.
- 29 QUE markdown files — `> ![[...]]` embeds inserted under quotes that previously had none.

---

## 2026-04-27 (Phase 16 — separate consecutive blockquoted wikilinks in CLMs and QUEs)

CLM `> [!info] Papers` callouts and QUE `> [!info] Papers` callouts had consecutive `> [[@<citekey>]]` lines touching each other (Phase 7's blank-line rule only addressed `- [[wikilink]]` items, not blockquoted wikilinks).

Inserted `>` separator (in-blockquote blank line) between any two consecutive `> [[...]]` lines that aren't screenshot embeds.

- **8 CLM files** updated (those with multiple papers in the Papers callout).
- **27 QUE files** updated.
- 0 EVD/CVT files affected (their analogous wikilink sections use bullet lists, already covered).

---

## 2026-04-27 (Phase 15 — separate EVDs in CVT `### Applies To` sections)

Phase 7's readability pass added blank lines between consecutive `- [[wikilink]]` items, but CVTs used **bare** wikilinks (no `-` prefix) in their `### Applies To` sections, so that fix didn't reach them — EVDs were rendered touching each other.

Two changes per affected CVT:
1. Convert bare `[[EVD ...]]` lines to bulleted `- [[EVD ...]]` (consistent with the rest of the vault).
2. Insert blank line between consecutive EVD bullets so each gets its own visual chunk.

**34 CVT files updated.** CVTs with only one Applies To EVD were untouched. The Phase 7 readability rules now apply uniformly across all reverse-link sections.

---

## 2026-04-27 (Phase 14 — decorative novice-friendly Welcome.md)

Replaced the one-line `Welcome.md` with a full vault overview targeted at first-time readers. Uses Obsidian callouts (`[!info]`, `[!tip]`, `[!example]`, `[!caution]`) and emoji icons throughout for visual structure (per the user's request: "images, icons, callout boxes").

Sections (in order): purpose · four node types · navigation paths · vault layout · node anatomy · why screenshots · quality signals · known limitations · how to add a new paper · further reading · provenance metadata.

The "Limitations and known gaps" callout calls out the four auto-derived-link warnings so a novice doesn't over-trust paper-level overlaps or paraphrased quotes:
- 49 paraphrased quotes still flagged in `paraphrase_audit_2026-04-27.tsv`.
- 27 nodes still at `NodeFormality: draft`.
- Auto-derived reverse links are paper-level, not statement-level.
- Methods Context anchors are shared paper-level for many EVDs.

Frontmatter follows the SKILL.md Step 10 convention with `prompt_source: [[prompts/2026-04-27-welcome-page]]` for traceability.

---

## 2026-04-27 (Phase 13 — persist scripts + fill SKILL.md gaps)

Persisted helper scripts from `/tmp/` to `scripts/` at the vault root so the workflow is reproducible without ephemeral state:

- `scripts/extract_quotes.py` — render quote-region PNGs from JSON spec.
- `scripts/quote_pipeline.py` — unified screenshot pipeline for EVDs/CLMs/CVTs.
- `scripts/cvt_screenshot_pipeline.py` — auto-locate quotes in CVTs lacking screenshots.
- `scripts/reverse_links.py` — build Caveats/Supports/Supporting sections.
- `scripts/readability_pass.py` — apply blank-line rules.
- `scripts/verbatim_audit.py` — write `paraphrase_audit_<date>.tsv`.
- `scripts/build_dgraph.py` — regenerate DGRAPH.md (script path inside the file updated).
- `scripts/README.md` — purpose and dependencies.

**SKILL.md updates** to match the current vault state:
- **Workflow at a glance** added at top: 10-step pipeline overview.
- **Vault structure** tree added.
- **Step 9 (new)** — regenerate DGRAPH.md as part of the standard pipeline.
- **Step 10 (new)** — save originating prompt to `prompts/` and log to HISTORY.md.
- All script references updated from `/tmp/...` to `scripts/...`.
- Step 5 dedupe sub-pass mentioned for re-run safety.

**HISTORY.md updates**:
- "Current state" snapshot added at the top showing inventory, invariants, formality distribution, and phase index.

---

## 2026-04-27 (Phase 12 — DGRAPH.md properties + SKILL.md invariants/audit)

### DGRAPH.md properties + callouts
Added Obsidian YAML frontmatter to `DGRAPH.md` so it shows up in the properties panel and carries provenance:

```yaml
author: Claude (Opus 4.7 / Sonnet 4.6)
page_type: index/discourse-graph
created: 2026-04-27
updated: 2026-04-27
generated_by: /tmp/build_dgraph.py
prompt_source: "[[prompts/2026-04-27-dgraph-creation]]"
vault: living-synthesis
```

Below the properties, three Obsidian callouts replace the previous prose intro:

- `> [!info] How this page is generated` — auto-derivation pipeline.
- `> [!tip] How to read this page` — wikilink + hierarchy guide.
- `> [!caution] Auto-derived links` — verify-before-citing reminder.

The originating prompt is saved at `prompts/2026-04-27-dgraph-creation.md` (also has its own frontmatter) so each generated document points back to its causing request.

`build_dgraph.py` updated to preserve the `created` date on regeneration (so re-runs only bump `updated`).

### SKILL.md updates
- **Step 5b (new)**: graph attachment audit. Codifies the four invariants as a table and includes a Python audit-script outline. The audit fails the extraction if any rule is violated; promotion to `ReadyForInternal` (Step 8) is blocked until fixed.
- **Key Principle #10 (new)**: encodes the four attachment rules as first-class constraints — CVT only on EVDs, CLM in ≥1 QUE, EVD in ≥1 CLM and ≥1 QUE.
- **Key Principle #11 (new)**: generated documents (DGRAPH.md, audit reports) must carry `author`, `page_type`, `created`, `updated`, `generated_by`, `prompt_source` in YAML frontmatter; reader-facing notes go in callout boxes below.

The skill is now self-contained: a fresh extraction following it should produce both per-paper nodes and the central index document with full provenance, and any rule violation halts the pipeline before promotion.

---

## 2026-04-27 (Phase 11 — enforce graph attachment rules)

User-stipulated rules:
- All CLMs must attach to at least one QUE.
- All EVDs must attach to at least one CLM AND at least one QUE.
- All CVTs must attach to EVDs only (no CLM links in `appliesTo`).

Audited the vault against these rules. Findings:

| Rule | Initial | After fix |
| ---- | ------- | --------- |
| CVT → EVD only | PASS (0 violations) | PASS |
| CLM in ≥1 QUE | FAIL (2 unattached) | PASS |
| EVD in ≥1 CLM | PASS | PASS |
| EVD in ≥1 QUE | PASS | PASS |

Fixes:
- Manually attached the 2 unattached CLMs to topically appropriate QUEs:
  - `CLM - Expert-annotated in-context examples significantly improve LLM novelty classification accuracy...` → `QUE - Can an LLM-based RAG system reliably evaluate the novelty of scientific ideas compared to expert judgment?`
  - `CLM - LLMs show promise for targeted reviewing subtasks but are not yet capable of functioning as standalone peer reviewers` → `QUE - Is LLM a reliable reviewer for automatic paper reviewing tasks?`
- Both CLMs added with their full nested EVD lists to the QUE's `### Supporting Claims (with their evidence)` block.
- Regenerated `DGRAPH.md`. Now: **31 of 31 CLMs attached** (no unattached section anymore), **77 of 77 EVDs reachable** through both CLMs and QUEs, **49 CVTs all attached only to EVDs**.

The vault now satisfies the discourse-graph attachment invariants.

---

## 2026-04-27 (Phase 10 — DGRAPH.md central index)

Created `DGRAPH.md` at the vault root: a comprehensive nested view of the discourse graph.

Structure:
- **Questions and their answers** — each QUE is a `###` header; its candidate CLMs are bullet-level children; each CLM's supporting EVDs are nested under it; each EVD's caveats appear with a ⚠️ marker as deeper children.
- **Claims not yet attached to any question** — CLMs that didn't keyword-match into any QUE's nested structure. Listed with their EVDs and caveats so they're discoverable.
- **Evidence not attached to any claim or question** — EVDs that don't appear in any QUE→CLM→EVD path (currently empty: every EVD reaches a CLM).
- **All caveats** — flat list of every CVT with the EVDs it constrains.

Stats:
- 27 QUEs as top-level entries
- 29 of 31 CLMs attached to at least one QUE; 2 unattached CLMs surfaced separately
- All 77 EVDs reachable via the graph
- 49 CVTs both nested under their EVDs and listed in the flat caveats section

Every node is a clickable Obsidian `[[wikilink]]`. Re-run `/tmp/build_dgraph.py` to regenerate from the current vault state — the script reads each QUE's `### Supporting Claims (with their evidence)` section, each CLM's `### Supporting Evidence`, and each CVT's `appliesTo`.

File size: 1663 lines.

---

## 2026-04-27 (Phase 8 — nest QUE → CLM → EVD hierarchy + Phase 9 — refine SKILL.md)

### Phase 8 — QUE hierarchy
Replaced flat `### Supporting Evidence` lists in QUE files with `### Supporting Claims (with their evidence)` — each candidate CLM is a top-level bullet, with its supporting EVDs nested as indented children. Matches the discourse-graph hierarchy QUE ← CLM ← EVD.

- **27 QUEs restructured.** CLM matching is keyword-overlap with the QUE title, capped at top 8 CLMs per QUE; each CLM's nested EVDs come from its existing `### Supporting Evidence` block.
- The flat `### Supporting Evidence` block in QUEs is removed (its content is now subsumed by the nested structure).

Helper script: `/tmp/nest_que.py`.

### Phase 9 — SKILL.md refinement
Refined `SKILL.md` to reflect everything learned across Phases 1–8. Major changes:

- **Step 3b switched primary path to PyMuPDF (`fitz`)** because `pdftotext -bbox-layout` crashes on some PDFs (poppler `std::out_of_range`). Same word-coordinate semantics, more reliable; eliminates the pdftoppm dependency for crops.
- **Added per-page fallback search** when the cited page misses (citation page numbers in journals often differ from PDF page numbers).
- **Step 4 expanded with full body templates** for EVD, CLM, CVT, QUE, including:
  - `## Source` block with citekey wikilink
  - Methods Context with What/How/Who, each with prose summary + verbatim quote + screenshot
  - Reverse-link sections (`## Caveats`, `## Supports Claim(s)`, `### Supporting Evidence`, `### Supporting Claims (with their evidence)`)
- **New Step 5: reverse-link build** — auto-resolves Caveats/Supports/Supporting from `appliesTo` and citekey overlap, idempotent on re-run.
- **New Step 6: verbatim audit** — describes the audit script, severity tiers, and the en-dash false-positive pattern.
- **New Step 7: readability formatting** — codifies the blank-line rules.
- **New Step 8: NodeFormality promotion** — defines the structural-completeness bar for `ReadyForInternal` and reserves `ReadyToShare` for manual grant.
- **Updated Key Principles**: stronger emphasis on verbatim quotes (with normalization-based audit as the bar), table-reformulation honesty, reverse-link maintenance, and HISTORY.md logging.
- **PNG naming convention table** added so future runs produce consistent filenames across crop types.

The refined SKILL.md is now self-contained: a fresh agent following it should produce vault output structurally identical to the current state.

---

## 2026-04-27 (Phase 7 — readability formatting)

Mechanical formatting pass to make every node easier to scan.

Three rules applied across all 184 EVD/CLM/CVT/QUE files:

1. **Blank line after every `##` and `###` heading** before body content. Previously many `### What?` / `### How?` / `### Who?` and `## Other Notes` / `## Caveats` / `## Supports Claim(s)` sections had body text on the very next line.
2. **`>` separator inside blockquotes between any non-empty `> ...` line and a following `> ![[...]]` screenshot embed.** Previously a quote line and its screenshot ran together; now there's visual breathing room while staying inside the same blockquote.
3. **Blank line between consecutive `- [[wikilink]]` items in lists.** Each EVD/CLM/CVT/QUE link in reverse-link sections now gets its own visual chunk.

Idempotent: any `\n\n\n+` runs collapse to `\n\n`.

- **184 files updated**: 77 EVDs + 31 CLMs + 49 CVTs + 27 QUEs.

Helper script: `/tmp/readability_pass.py`.

---

## 2026-04-27 (Phase 5 — link QUEs to evidence + Phase 6 — promote NodeFormality)

### Phase 5 — QUE → EVD links
For each QUE file, derived candidate supporting EVDs via keyword overlap (with light synonym expansion: detect/identify, paper/manuscript, etc.) between the QUE title and each EVD's title + Description.

- **27 QUEs** now have a `### Supporting Evidence` block listing candidate EVDs.
- **231 total EVD links** added across all QUEs. Each link is flagged as auto-derived; the user is asked to verify before citing.
- Tuning: `len(overlap) ≥ 2` AND overlap covers ≥ 20% of the QUE's content words. Capped at top 10 matches per QUE.
- Quality is mixed — typical match counts are 2–10 per QUE. The verify-before-citing caveat is in the section body itself.

Helper script: `/tmp/link_ques.py`.

### Phase 6 — NodeFormality promotion
Promoted `NodeFormality: draft` → `ReadyForInternal` for nodes that are structurally complete (source link + Description quote+screenshot + Methods Context + reverse links).

- **157 nodes promoted**: 60 EVDs + 25 CLMs + 45 CVTs + 27 QUEs.
- **27 nodes kept as `draft`**: flagged in `paraphrase_audit_2026-04-27.tsv` with <50% verbatim match (Tier 1+2). These need a human verbatim-fix pass before promotion.

This promotion signals "structurally complete; ready for internal review and use," not "passed final content review." The user retains the option to demote any node that doesn't actually pass their reading. `ReadyToShare` (the next state, for external use) is left for the user to grant manually.

---

## 2026-04-27 (Phase 4 — clean up auto-extracted markers)

Replaced `*Common methods anchor (auto-extracted):*` with `*Source methods passage (paper-level):*` across the vault. The new label drops the tooling jargon while still signaling that the screenshot is paper-level (shared across all EVDs from the paper) rather than EVD-specific — useful context for a reader.

- **134 markers replaced across 66 EVD files** in a single mechanical pass.
- EVDs with EVD-specific anchors (added in Phase 2d/2f) already had a `> "quote text"` line above the screenshot and weren't touched.
- The new label also makes clear what's still shared so a future per-EVD specificity pass knows where to focus.

---

## 2026-04-27 (Phase 3 — reverse-link the discourse graph)

Until now the graph was directional: CVTs declared `appliesTo: [[EVD ...]]` and CLMs listed `Papers: [[@citekey]]`, but EVDs and CLMs had no inbound link sections of their own. Added two new mechanically-derived sections.

- **Every EVD now has a `## Caveats` section** listing every CVT whose `appliesTo` references it, or "No caveats currently linked" otherwise.
- **Every EVD now has a `## Supports Claim(s)` section** listing every CLM whose `Papers` block contains the EVD's citekey. Caveat in the section body itself: this is paper-level overlap, not statement-level — the user should verify before citing.
- **Every CLM now has a `### Supporting Evidence` section** listing every EVD whose source citekey appears in the CLM's papers list, with the same paper-level-overlap caveat.

### Stats
- **77 EVDs** updated with `## Caveats` + `## Supports Claim(s)`.
- **31 CLMs** updated with `### Supporting Evidence`.
- Idempotent: re-running the script (`/tmp/reverse_links.py`) regenerates the sections in place, so they stay in sync as the graph evolves.

### Why this helps
- A reader on an EVD page can now navigate to its limitations and the conclusions it grounds without grep-ing the vault.
- A reader on a CLM page can see all the EVDs from its cited papers as candidate support, even if specific quote attribution wasn't yet pinned.
- The auto-derived nature is visibly flagged in each section so a human curator knows where they need to prune.

---

## 2026-04-27 (Phase 2e — verbatim audit + Phase 2f — second-pass fixes)

### Phase 2e — verbatim audit
Built `/tmp/verbatim_audit.py` to scan every quoted line in every EVD/CLM/CVT against its source PDF, computing the longest verbatim prefix match across all pages. Saved the full report to `paraphrase_audit_2026-04-27.tsv` at the vault root.

Initial audit: **54 paraphrases** flagged. Tiered by match length:
- **Tier 1** (0% match — fabricated or wrong page): 4 quotes.
- **Tier 2** (<50% match — major paraphrase): 23 quotes.
- **Tier 3** (50–90% — moderate): 19 quotes.
- **Tier 4** (>90% — minor truncation): 7 quotes.

### Tier 1 fixes
- **Bougie GAR human-likeness EVD**: original quote was Table 7 row data reformatted as inline text. Annotated as `*Table 7 row for the GAR reviewer agent (values reformatted as inline text):*` to preserve the table-derived values while flagging the form change.
- **Tyser GPT-4 Turbo Rank EVD**: same — Table 1 data reformatted as inline. Annotated as `*Table 1 contents (rows reformatted as inline text):*`. Also fixed broken image reference `tyserAIDrivenReviewSystems2024-table1-p6-1.png` (was unresolved on disk) → rendered fresh `tyserAIDrivenReviewSystems2024-table1-p5.png` and updated both EVD and the cross-referencing CLM.
- **Zhou RR-MCQ CVT**: replaced paraphrased quote "Our RR-MCQ data is an example, but still with limited size" with a verbatim alternative from p. 9341/9346: "The questions are inferred from real discussion forums of 55 reviews from 14 papers in ICLR-2023…" + "To construct the MCQ test dataset, we select 55 reviews from 14 papers…". Generated new screenshot.
- **Woelfle Human-AI 96% EVD**: audit false positive. The quote is verbatim in p. 1; the audit's normalize misses it because pdftotext converts the en-dash in "Human−AI" to "HumaneAI", so `humaneaicollaboration` ≠ `humanaicollaboration`. Pipeline-generated screenshot was correct; no fix needed.

### Phase 2f — second pass on Sridharan-a, Zhang-r, Woelfle-What
With per-EVD verbatim quotes from each paper's actual methods/results sections.

- **Sridharan-a (4 EVDs)**: replaced shared anchor with EVD-specific verbatim quotes:
  - Three AI platforms responded correctly (p. 3 trio quote)
  - AI platforms drafted SOPs (p. 3 fundamental sections quote)
  - Failed post-trial herbal medicine (p. 3 case study 10 quote)
  - None recognized quorum (p. 3 SOP for initial review quote)
- **Zhang-r (3 EVDs)**: replaced shared anchor with EVD-specific verbatim quotes referencing the hit-rate evaluation methodology and the LLM-as-judge framework.
- **Woelfle-What**: covered by Phase 2d. The audit-flagged Combined LLMs Description was the verbatim abstract sentence; only the en-dash false positive remains.

### Final coverage after 2e + 2f
- **34 of 77 EVDs** (44%) now have at least one EVD-specific methods anchor (up from 31 after Phase 2d).
- **376 PNGs** in `evidence/Attachments/` (up from 360).
- **Audit re-run**: 50 quotes still flagged. 1 in Tier 1 (the known Woelfle en-dash false positive); the remaining 49 are Tier 2-4. The audit report at `paraphrase_audit_2026-04-27.tsv` is the user-facing reference for these.

### Remaining audit gaps (Tier 2-4)
- 23 Tier 2 (<50% match): predominantly EVDs whose Description quote was lightly paraphrased — typical pattern is the user condensed two sentences from the paper into one in the note. The audit report is the right next step for a manual sweep; auto-replacement would risk losing the user's intentional condensations.
- 19 Tier 3 (moderate): often whole-quote matches that diverge only by an inserted word or by hyphenation across line breaks (which my normalize ought to handle but doesn't always).
- 7 Tier 4 (minor): tail-only divergences — usually a short trailing phrase the user dropped.
- All flagged quotes do still have a screenshot (just not perfectly verbatim text).

---

## 2026-04-27 (Phase 2d — EVD specificity pass)

Replaced shared paper-level methods anchors with EVD-specific quotes for the most clearly multi-task papers. Targeted papers where different EVDs come from genuinely different sub-experiments (Lou's three AAAR tasks, Wrightson's three model setups, Son's SPOT metrics, Tyser's evaluation modes, Idahl's metrics, Bougie's GAR variants, Sridharan/Sridharan IRB cases, Woelfle's six analyses, Zhang-r's three models).

- Spec file: `/tmp/per_evd_specs.json` — 9 papers × 2–6 EVDs each, with per-EVD What/How (and occasional Who) quotes.
- Pipeline: `/tmp/embed_per_evd.py` — finds the shared "Common methods anchor (auto-extracted)" line in each section and replaces it with an EVD-specific quote + screenshot. Falls back to opening-only crop when strict opening+closing match fails on the cited page; searches all pages if cited page misses.
- A regex bug in the first run caused some sections to be appended duplicates; cleaned up with a dedupe pass on 26 files.
- Some quote specs were paraphrases (sridharan-a, parts of zhang-r); they fell through to the fallback bbox or stayed with the shared anchor. Not all sections in every targeted EVD got replaced — coverage is partial but real.

### Coverage after specificity pass
- **31 of 77 EVDs** (40%) now have at least one EVD-specific methods anchor (What, How, or Who) replacing the shared paper-level anchor.
- The remaining 46 EVDs keep the shared paper-level anchor — appropriate for papers where all EVDs derive from the same sub-experiment (Roberts, Akyon, Shahid, Srinivasan, etc.) but may still be improvable for some.
- **360 PNGs** in `evidence/Attachments/` (up from 311 before this pass).

### What was NOT replaced and why
- **Sridharan-a** (4 EVDs): I drafted IRB-case-specific quotes, but the paper doesn't contain verbatim sentences saying "Case study 10 examined post-trial access" — those were synthesized. Fell through to the fallback bbox using the prose openings (which weren't verbatim either), so those EVDs kept their shared paper-level anchor or fallback crops. A future per-EVD pass would need to read each case study description in the paper and extract the literal text.
- **Zhang-r** (3 EVDs): MuPDF flagged a structure-tree error and quote spec paraphrased the source. EVD-specific anchors not added; shared anchor remains.
- **Woelfle's What for some EVDs**: same paraphrase issue — quote was constructed rather than copied verbatim. Shared anchor remains.

### Verification
- `EVDs with EVD-specific anchor: 31`
- `EVDs with only shared anchor: 46`
- All 77 EVDs still have at least one quote+screenshot in each Methods Context section.

---

## 2026-04-27 (Phase 2c — EVD What pass)

Closed the remaining gap from Phase 2b: 66 EVDs lacked a What direct quote / screenshot. Applied the same shared-per-paper anchor approach used for How/Who.

- Spec file: `/tmp/what_quotes_batch.json` (24 papers).
- Pipeline run: 19 of 24 papers succeeded on the first pass (54 EVDs edited). 5 retries needed for darcy, lou, zhang-d, zhang-r, zhou — fixed with corrected opening/closing strings (4 of 5 on the second attempt; zhang-d on the third with a more specific opening).
- Helper script: `/tmp/embed_what.py`.

### Final coverage (vault-wide)
- **77 EVDs**: 77 with What anchor, 77 with How anchor, 76 with Who anchor (Hasan paraphrased — left as prose).
- **31 CLMs**: all quoted text has screenshots.
- **49 CVTs**: all quoted text has screenshots; all have source links.
- **311 PNGs** in `evidence/Attachments/`.

### What's intentionally not done
- Per-EVD specificity. The What/How/Who anchors are shared at the paper level; for papers where different EVDs cover different sub-experiments (Tyser, Lou, Son, etc.), a richer per-EVD pass would replace the shared anchor with a more specific quote.
- QUE screenshots — deferred per skill guidance.
- Verbatim audit. Phase 2a caught 4 paraphrases via match failures, but other paraphrases that happened to share enough verbatim with the source weren't surfaced. A human verbatim audit pass would be the right follow-up.

---

## 2026-04-27 (full scale-up: Phase 2a + 2b)

### Phase 2a — Description-quote screenshots across all EVDs and CLMs (24 papers)
Extended the fitz-based screenshot pipeline to handle EVDs and CLMs in addition to CVTs. Per-quote citekey resolution for CLMs uses author-surname matching against the CLM's `Papers` block.

- Pipeline run: **80 PNGs added** across EVDs and CLMs in one pass; **1 initial failure** (Bougie GAR Table 7 — special characters ± and *) resolved with a manual fallback crop.
- Manual fixes: 4 quotes that needed paper-specific handling — Wu et al. 2024 had two quotes with PDF page numbers ≠ journal page numbers (cited p.1462/1463 → actual PDF p.11/12); D'Arcy quote needed an apostrophe-tolerant matcher; Bougie GAR table needed a fallback bbox keyed off the table header.
- Final state after Phase 2a: **0 of N quote lines across EVDs, CLMs, CVTs lack a screenshot** (verified by full-vault scan).

Helper scripts: `/tmp/quote_pipeline_v3.py`.

### Phase 2b — Methods Context anchors for non-pilot EVDs (24 papers)
For each remaining paper, picked one representative How quote and one representative Who quote from the methods section, rendered crops, and embedded them under the corresponding `### How?` / `### Who?` sections of every EVD that didn't already have a direct quote there.

- Approach: shared per-paper How and Who quotes (one each) applied across all of that paper's EVDs. EVDs that already had a direct quote in a section were skipped to avoid duplication.
- Bulk-grep helper: `/tmp/grep_methods.py` flagged candidate methodological sentences per paper using keyword patterns (we used / measured / collected / dataset / participants / etc.) so the spec could be hand-curated quickly.
- Spec file: `/tmp/methods_quotes_batch.json` with 24 papers × 2 quote types = 48 quote slots.
- Pipeline run: 47 quotes rendered (1 failure: Hasan Who quote — paraphrased from the source), 66 EVDs edited.
- Embed format under each section: a "Common methods anchor (auto-extracted)" label followed by the screenshot. The existing prose summary was preserved above.

Helper script: `/tmp/embed_methods.py`.

### Coverage now (vault-wide)
- **77 EVDs**: all 77 have How quote/screenshot; 76 have Who quote/screenshot (Hasan missing — paraphrased source); **66 still lack a What quote/screenshot**. The What gap is intentional in this pass — each EVD measures something different and a shared paper-level What quote would dilute specificity. A second pass per EVD would be needed for full coverage.
- **31 CLMs**: all quoted text now has screenshots.
- **49 CVTs**: all quoted text now has screenshots.
- **27 QUEs**: not processed (per skill, "QUEs should have screenshots" but those would need to be sourced from supporting evidence — deferred).
- **287 PNGs** in `evidence/Attachments/`.

### Known limitations of this scale-up
- **Methods Context "What" sections still mostly prose-only.** Auto-anchoring with a shared paper-level What quote was deemed too lossy; a second pass per EVD is the right approach.
- **One Hasan Who quote failed.** The paraphrased note text didn't match anything verbatim. Left as prose-only; flagged.
- **Methods anchors are paper-level, not EVD-specific.** All EVDs of a paper share the same How and Who quote. For papers where different EVDs come from different sub-experiments (e.g., Tyser, Lou with separate tasks), the shared anchor is approximate. Acceptable for grounding but not perfect.
- **One CVT had a fabricated supporting quote** (Lou non-textual inputs). Replaced with a real anchor and reclassified as inferred. Other CVTs may have similar issues that will surface as the user reads through.
- **2 stale Liang PNGs** (`liang2024-results-p5-{05,06}.png`) remain in Attachments — unreferenced. Not deleted in case useful.

---

## 2026-04-27 (latest — fix-up before scaling)

### Issue 1: source links missing from EVDs and CVTs
Bulk-added a `## Source` block linking the citekey wikilink (e.g., `[[@sarolAssessingCitationIntegrity2024]]`) between the frontmatter and the body of every EVD and CVT.

- **EVDs**: 77 files updated. Citekey extracted from filename (`... - @<citekey>.md`).
- **CVTs**: 49 files updated. Citekey extracted from `appliesTo` wikilinks. Two SPOT CVTs (sonWhenAICoScientists2025) initially picked up `@4` from `pass@4` in an EVD title — corrected after detection (regex tightened to require leading letter; spurious `[[@4]]` removed from both files).
- Spacing fix-up pass added a blank line between `[[@citekey]]` and the next heading in 126 files.

Helper script: `/tmp/add_source_links.py`.

### Issue 2: CVT pages had quotes but no screenshots
Built a fitz-based pipeline that, for each CVT lacking an embedded screenshot under a quote line, locates the quote in the source PDF and embeds a 250 DPI cropped PNG. Final state: **0 of 56 CVT quote lines now lack a screenshot**.

Pipeline (in two passes):
- **Pass 1** — strict opening + closing match using progressive windows (8/5/3-word openings × 6/4/2-word closings). Searches the cited page first, then all other pages. Handles citation-page-vs-PDF-page mismatches (e.g., zhou cites journal page 9347 in a 12-page PDF — fitz auto-found the actual PDF page).
- **Pass 2 fallback** — when only the opening can be matched, crops a fixed-height region (90 pt) from the opening word in the same column. Handles ellipsis-containing quotes and quotes that span paragraphs/columns/pages.

Run results across both passes:
- 38 CVTs needing screenshots → all completed
- 35 new PNGs in `evidence/Attachments/` named `<citekey>-cvt-p<page>-<n>.png`
- 1 manual fix: `CVT - The AAAR benchmark excluded non-textual inputs...` had a fabricated supporting quote not in the Lou et al. 2025 paper. Replaced the quote with a real anchor on p. 3 describing the LaTeX-source input format and changed the CVT type from `author-stated` to `inferred`.
- 2 stale numeric source-link artifacts removed: `[[@4]]` lines in the two SPOT CVTs (introduced by the regex bug in Step 1, fixed before pipeline run).

Helper scripts: `/tmp/cvt_screenshot_pipeline.py` (v1, retained for reference) and `/tmp/cvt_screenshot_v2.py` (final).

### Net file changes this fix-up
- **Added**: 35 new CVT screenshot PNGs.
- **Edited**: 126 files (77 EVDs + 49 CVTs) for source link insertion; 38 CVTs for screenshot embedding; 1 CVT (Lou non-textual) for quote correction + type change.
- **Deleted**: nothing.

---

## 2026-04-27 (later)

### Pilot rollout — quote-region screenshots + Methods Context quotes for 3 papers

Goal: validate the new SKILL Step 3b across varied papers before doing all 28. Pilot covered Liu 2023 (60 pp, single-column), Sarol 2024 (9 pp, two-column), and Liang 2024 (39 pp, single-column with figures on later pages). Switched to PyMuPDF (`fitz`) for bbox extraction after `pdftotext -bbox-layout` crashed on Liu's PDF (`std::out_of_range` from poppler). Crops still rendered with the same logic; helper script at `/tmp/extract_quotes.py`.

#### Tooling
- Installed `pymupdf` (1.27.2.3) as fallback bbox extractor.
- New helper `/tmp/extract_quotes.py`: takes a PDF + JSON quote spec → writes one PNG per quote using fitz word coordinates, padded bbox, and 250 DPI rasterization.

#### Liu 2023 — `@liuReviewerGPTExploratoryStudy2023`
**Added** (18 PNGs):
- 9 quote crops for existing Description / claim / supporting quotes across 3 EVDs, 2 CLMs, 3 CVTs.
- 8 quote crops for new Methods Context entries (What/How/Who across the 3 EVDs).
- 1 page screenshot: `liuReviewerGPTExploratoryStudy2023-table1-p6-06.png` (Table 1, error-detection performance).

**Edited** (8 nodes):
- 3 EVDs (`86.6%-checklist`, `7-of-13-errors`, `6-of-10-abstracts`): embedded quote crops; expanded Methods Context with direct quotes + crops; replaced the unresolved `[Screenshot: ...]` placeholder in `7-of-13` with the actual Table 1 PNG embed; corrected verbatim quote text ("We find" → "We found" on the 86.6% EVD to match the source).
- 2 CLMs (`promise-not-standalone`, `targeted-question-prompting`): embedded quote crops.
- 3 CVTs (`only-GPT-4-tested`, `constructed-short-papers`, `checklist-author-stated`): embedded quote crops; corrected "We generated 10 pairs" → "We generate 10 pairs" on the constructed-short-papers CVT to match verbatim source.

#### Sarol 2024 — `@sarolAssessingCitationIntegrity2024`
**Added** (21 PNGs):
- 7 quote crops for existing Description / claim / supporting quotes across 4 EVDs, 1 CLM, 2 CVTs.
- 12 quote crops for new Methods Context entries (What/How/Who across the 4 EVDs).
- 2 page screenshots: `sarolAssessingCitationIntegrity2024-tables-p5-5.png` (Tables 1–2), `sarolAssessingCitationIntegrity2024-tables-p6-6.png` (Tables 3–4).

**Edited** (7 nodes):
- 4 EVDs (`39pct-errors`, `multivers-F1`, `gpt4-F1`, `iaa-kappa`): embedded quote crops; expanded Methods Context with direct quotes + crops; replaced unresolved `[Screenshot: ...]` placeholders with rendered table PNGs.
- 1 CLM (`citation-quotation-errors-subtle`): embedded quote crop.
- 2 CVTs (`low-iaa`, `excluded-tables-figures`): embedded quote crops.

#### Liang 2024 — `@liangCanLargeLanguage2024a`
**Added** (22 PNGs):
- 9 quote crops for existing Description / claim / supporting quotes across 4 EVDs, 2 CLMs, 2 CVTs.
- 11 quote crops for new Methods Context entries (What/How/Who across the 4 EVDs).
- 2 page screenshots: `liangCanLargeLanguage2024a-overlap-p3-3.png` (overlap discussion + Fig. 2 reference), `liangCanLargeLanguage2024a-aspects-p5-5.png` (aspects discussion + Fig. 3 reference).

**Edited** (8 nodes):
- 4 EVDs (`57.4%-helpful`, `7.27x-implications`, `30.85%-overlap`, `shuffle-paper-specific`): embedded quote crops; expanded Methods Context with direct quotes + crops; replaced previously broken image references (`liangCanLarge2024-aspects-p5-1.png`, `liangCanLarge2024-overlap-p3-1.png`) with the new correctly-named files; corrected verbatim quote on the shuffle EVD ("A significant decreased" was a paraphrase artifact → "the pairwise overlap significantly decreased").
- 2 CLMs (`LLM-review-quality-comparable`, `paper-specific-not-boilerplate`): embedded Liang quote crops; flagged the still-broken Tyser screenshot reference for the next paper pass.
- 2 CVTs (`already-accepted-papers`, `self-selection-bias`): embedded quote crops; cleaned up the "..." paraphrase quote in the accepted-papers CVT to a single verbatim sentence + a clearly-labeled inferred annotation.

### Notes from the pilot
- Quote-text fidelity: 4 paraphrases vs. verbatim source were caught and corrected during this pass (Liu × 2, Sarol × 0, Liang × 2). Worth applying the same verbatim check across all remaining papers.
- Match failures: each paper had 1–2 quote misses on the first pass, all due to ellipses or transcription drift in the original notes. Quick fixes on a second JSON spec.
- Cross-column / cross-page splits did not appear in the pilot papers (single-column except Sarol). The two-crop logic from SKILL.md remains validated only on Woelfle.
- `pdftotext -bbox-layout` crashed on Liu's PDF. Going forward, pipeline defaults to fitz; pdftoppm still works for full-page renders.
- The two stale `liang2024-results-p5-{05,06}.png` files from the original April-18 run remain in `Attachments/` and are now unreferenced. Did not delete in this pass — flagging for review.

---

## 2026-04-27

### Added
- `evidence/EVD - Median quote similarity with original full text was 99 percent across LLM extracted quotes - @woelfleBenchmarkingHumanAICollaboration2024.md`
- `evidence/EVD - GPT-4 cost approximately 100x more than Mixtral-8x22B per 100 papers in evidence appraisal - @woelfleBenchmarkingHumanAICollaboration2024.md`
- `evidence/EVD - Human inter-rater reliability dropped from 91 percent on PRISMA to 57 percent on PRECIS-2 - @woelfleBenchmarkingHumanAICollaboration2024.md`
- `caveats/CVT - Human consensus datasets used as comparators were openly available online raising train test contamination concerns.md`
- `caveats/CVT - Most LLMs were text-only and blind to figures and image-rendered tables relevant for evidence appraisal.md`
- `caveats/CVT - The benchmark datasets did not record human time on task preventing quantification of efficiency gains.md`
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-quoteaccuracy-p8-08.png` — quote-region crop, p. 8
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-cost-p8-08.png` — quote-region crop, p. 8
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-irr-p8-08.png` — quote-region crop, p. 8
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-contamination-p9-09.png` — quote-region crop, p. 9
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-imageblind-p9-09.png` — quote-region crop, p. 9
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-notimetrack-p10-10.png` — quote-region crop, p. 10
- `HISTORY.md` (this file)

### Edited
- `SKILL.md` — Expanded the Step 3b "Edge cases" list to call out en-dash mangling (`Human−AI` → `HumaneAI`), hyphenation at line breaks, ligatures, scanned PDFs, and a note on crop padding tradeoffs.

### Deleted
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-results-p4-04.png` — unreferenced page screenshot from a prior run, superseded by `-fig2fig3-p4-04.png`.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-results-p4-05.png` — unreferenced page screenshot from a prior run, superseded by `-table2-p5-05.png`.

---

## 2026-04-25

### Added (Woelfle re-run, Step 3 + 3b validation)
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-bbox.html` — cached `pdftotext -bbox-layout` map (~921 KB) used to compute quote-region bboxes.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-fig1-p3-03.png` — full page 3 (Table 1 + Fig 1).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-fig2fig3-p4-04.png` — full page 4 (Fig 2 + Fig 3).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-table2-p5-05.png` — full page 5 (Table 2).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-table3-p7-07.png` — full page 7 (Table 3).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-individual-p1-01.png` — abstract quote, individual-LLM accuracy.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-combined-p1-01.png` — abstract quote, combined-LLM accuracy.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-humanai-p1-01.png` — abstract quote, human-AI collaboration accuracy.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-conclusion-p10a-10.png` — conclusion, bottom of left column on p. 10 (cross-column case).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-conclusion-p10b-10.png` — conclusion continuation, top of right column on p. 10.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-tworaters-p9-09.png` — fifth-limitation quote, end of p. 9 (cross-page case).
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-tworaters-p10-10.png` — fifth-limitation continuation, top of p. 10.
- `evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-quote-precis2dataset-p9-09.png` — second-limitation quote, p. 9.

### Edited (Woelfle nodes — embedded quote crops + correct figure/table screenshots; fixed previously-broken image links)
- `evidence/EVD - Combined LLMs with consistency approach reached 75-88 percent accuracy for PRISMA while deferring 4-74 percent of ratings - @woelfleBenchmarkingHumanAICollaboration2024.md` — replaced broken `-fig3-p4-1.png` reference; embedded quote crop, Fig 3 page, and Table 3.
- `evidence/EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans - @woelfleBenchmarkingHumanAICollaboration2024.md` — replaced broken `-table2-p5-1.png` reference; embedded quote crop and Table 2.
- `evidence/EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters - @woelfleBenchmarkingHumanAICollaboration2024.md` — replaced broken `-fig2-p4-1.png` reference; embedded quote crop, Fig 2 page, and Table 3.
- `claims/CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks.md` — replaced broken Fig 2 reference; embedded both conclusion crops (cross-column) and Fig 2.
- `caveats/CVT - Evidence appraisal benchmark used only two human raters and datasets skewed toward pragmatic trials limiting PRECIS-2 findings.md` — embedded both fifth-limitation crops (cross-page) and second-limitation crop; expanded the supporting-quote prose.

---

## 2026-04-24

### Edited
- `SKILL.md` — Diagnosed why prior runs produced full-page screenshots instead of quote-region crops. Patched Step 3:
  - Renamed Step 3 from "Extract Figure/Table Screenshots (for EVDs)" to "Extract Screenshots (figures, tables, and quote regions)".
  - Split into 3a (figure/table page screenshots, unchanged behavior) and 3b (new quote-region crop procedure: `pdftotext -bbox-layout` → word-coordinate match → pt→px conversion at 250 DPI → `pdftoppm -x -y -W -H` crop → embed under quote in node body).
  - Listed initial edge cases: cross-column/page quotes, hyphenation/ligatures, scanned PDFs.
  - Updated the post-extraction Evidence summary-table column from "Grounding Figure/Table" to "Grounding PNGs (figure/table/quote)".

### Memory (outside vault, at `~/.claude/projects/-Users-ppatel-Documents-living-synthesis/memory/`)
- `project_vault_authoring_model.md` — Recorded that the April 17–18 batch of 10 CLM, 12 EVD, 12 CVT notes was authored with Claude 4.7 per user recollection, flagged as "only partly sure" so future sessions treat it as a working assumption.
- `MEMORY.md` — Added pointer entry for the above memory.

### Recall (no file changes)
- Reported counts of last week's batch (April 17–18 vault scaffolding + bulk extraction). Initial counts were wrong (claimed 14 EVD and 13 CVT); corrected to 10 CLM, 12 EVD, 12 CVT after re-counting.

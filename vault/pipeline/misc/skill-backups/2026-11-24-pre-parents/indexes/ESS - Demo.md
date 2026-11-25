---
author: Claude + ppatel
page_type: index/bases-wrapper
created: 2026-04-29
updated: 2026-04-29
generated_by: human-collaborated authoring
prompt_source: "[[2026-04-29-ess-base]]"
vault: living-synthesis
human_verified: yes
---

# 🔎 ESS — Evidence-Synthesis System

> [!info] What this page is
>
> A live, filterable index of every discourse-graph node (QUE / CLM / EVD / CVT) in this vault. The database below is an Obsidian Bases view — click any tab to slice the corpus by node type, 5C research dimension, methodological rigor, or workflow status.

**Three entry points to the vault.** This page complements:

- 📋 **[[DGRAPH]]** — the *nested* QUE → CLM → EVD → CVT hierarchy, best for understanding how findings build into claims that answer questions.
- 📊 **[[DGRAPH-TABLE]]** — a *paper × node-type* matrix, best for skimming what each of the 27 papers contributes.
- 🔎 **ESS (this page)** — *filter-by-property* for everything else (rigor, ethics-vs-rigor focus, draft workflow, etc.).

---

## How to read the table cells

Every node carries tags in its `tags:` frontmatter that get listed in the **Tags** column. Four namespaces appear, each filterable by clicking the tag chip:

> [!example] **`5c/<dimension>`** — what aspect of research the node touches
>
> | Tag | Meaning |
> | --- | --- |
> | `5c/credibility` | Rigor — error detection, risk-of-bias assessment, methodological evaluation |
> | `5c/clarity` | Reporting-guideline alignment — CONSORT, PRISMA, AMSTAR, STROBE, ROBINS-I, QUADAS-2, PRECIS-2 |
> | `5c/creativity` | Novelty + value — novelty assessment, peer-review feedback for innovation |
> | `5c/connectivity` | Citation links — citation integrity, quotation errors |
> | `5c/care` | Ethics — IRB review, informed consent, ethical review of clinical proposals |

> [!example] **`appraisal/<domain>/<rating>`** (EVDs only) — paper-level critical-appraisal rating
>
> Rating: 🟢 `low-risk` (rigorous on this domain) · 🟡 `some-concerns` (gaps but not paper-killing) · 🔴 `high-risk` (obvious flaw)
>
> Domains: `construct-validity` · `internal-validity` · `external-validity` · `statistical-rigor` · `reproducibility`. Plus a summary tag `appraisal/overall/L<n>-M<n>-H<n>` (counts of low / some-concerns / high domains).

> [!example] **`tripod-llm/...`** (EVDs only) — paper-level TRIPOD-LLM reporting compliance
>
> - `tripod-llm/compliance/{high, moderate, low}` — bucketed ✅-rate over the 37-item TRIPOD-LLM checklist (high ≥80%, moderate 60–80%, low <60%)
> - `tripod-llm/proportion/<NN>pct` — raw rounded percentage for sorting

> [!example] **`cvt/<axis>/<value>`** (CVTs only) — methodologist classification of the limitation
>
> - `cvt/domain/<5 buckets>` — same axes as appraisal: `construct-validity`, `internal-validity`, `external-validity`, `statistical-rigor`, `reproducibility`
> - `cvt/mechanism/<one of ~30>` — specific mechanism: `small-sample`, `single-domain`, `data-leakage`, `selection-bias`, `llm-as-judge`, `single-rater`, `low-iaa`, `proxy-metric`, `single-prompt`, `excluded-cases`, `ecological-invalidity`, … (full list in [[History]] Phase 24)
> - `cvt/type/{author-stated, inferred}`
> - `cvt/severity/{low, moderate, high}`

> [!tip] Filtering by clicking
>
> Hover over any tag in the table to see its hierarchy. Click to open Obsidian's tag pane filtered to that tag — useful when you want "show me everything tagged this way" rather than the pre-built views below.

---

## What each view is for

The Bases view tabs are grouped into five families. Use these descriptions to pick the right tab.

> [!info] Default
>
> - **All nodes** — every QUE / CLM / EVD / CVT, sorted by Type → Title. Useful when you don't know what you're looking for and want to scroll.

> [!info] By node type (4 tabs)
>
> - **❓ Questions (QUE)** — 27 research questions. Each ties to one or more papers and nests CLMs underneath.
> - **💡 Claims (CLM)** — 31 generalizations the corpus papers argue for. Each is grounded in one or more EVDs.
> - **🔬 Evidence (EVD)** — 77 atomic empirical findings, each tied to a single paper and a verbatim quote.
> - **⚠️ Caveats (CVT)** — 49 methodological limitations on the EVDs.

> [!info] By 5C research dimension (5 tabs)
>
> - **5C · Credibility (rigor)** — error detection, risk-of-bias, quality assessment.
> - **5C · Clarity (reporting)** — CONSORT / PRISMA / AMSTAR / STROBE / ROBINS-I / QUADAS-2 / PRECIS-2 compliance assessment.
> - **5C · Creativity (novelty + value)** — novelty assessment, peer-review feedback for innovation.
> - **5C · Connectivity (citation links)** — citation integrity, quotation errors.
> - **5C · Care (ethics)** — IRB review, informed consent.

> [!info] EVD methodological rigor (5 tabs)
>
> Quick filters for finding strongest / weakest evidence by paper-level rigor:
>
> - **TRIPOD-LLM compliance high** — papers reporting ≥80% of the TRIPOD-LLM checklist. Most defensible reporting in the corpus. *(Currently 0 — no preprint clears this bar.)*
> - **TRIPOD-LLM compliance moderate** — 60–80% reporting compliance. The middle of the corpus.
> - **TRIPOD-LLM compliance low** — <60% reporting compliance. Use with caution.
> - **External-validity high-risk** — papers whose findings won't generalize beyond the specific dataset / model / domain (single-discipline samples, opt-in user studies, single-conference corpora, etc.).
> - **Statistical-rigor high-risk** — papers without confidence intervals, paired tests, or multiple-comparison correction.

> [!info] CVT methodologist filters (6 tabs)
>
> - **⚠️ High-severity caveats** — the 5 most paper-undermining limitations in the corpus.
> - **⚠️ Inferred caveats (not author-stated)** — limitations identified by the extractor that authors didn't flag themselves; treat with extra scrutiny.
> - **⚠️ External-validity caveats** — generalizability constraints (the most common kind).
> - **⚠️ Internal-validity caveats** — bias in the comparison itself (contamination, leakage, judge circularity).
> - **⚠️ Construct-validity caveats** — metric ↔ deployment-construct mismatches.
> - **⚠️ Reproducibility caveats** — code / data / inference-parameter availability gaps.

> [!info] Workflow
>
> - **📝 Drafts (still need verification)** — nodes still at `NodeFormality: draft`, awaiting verbatim-audit fixes.

---

## [[Live database]]

![[ESS.base]]

---

## Caveats on the tags themselves

> [!caution] Read before filtering
>
> - **The `appraisal/...` and `tripod-llm/...` tags on EVDs are *paper-level*, inherited from the source page** — they don't tell you whether *this specific finding* is more or less rigorous than the paper average. They're a paper-level prior, not an EVD-level judgment. For per-EVD specifics, read the EVD's `## Other Notes` item-17 mini-table.
> - **The 5C tags are based on what the paper *studies*, not the EVD's specific finding.** A paper studying citation integrity (Sarol) gets `5c/connectivity` for all its EVDs even if a specific EVD reports an annotator-agreement number that's really about credibility.
> - **The CVT mechanism vocabulary is open-ended** — see [[History]] Phase 24 for the controlled list. Future paper additions may need new mechanisms; that's expected.
> - **Reporting compliance and methodological quality are not the same thing.** A paper can be ✅ across most TRIPOD-LLM items (transparently reports its methods) yet still 🔴 on construct validity (the methods don't actually support its deployment claim). Always read both signals together.

---

## Provenance

> [!info]
>
> - The `.base` file is at `[[ESS.base]]`. Edits to views/filters/sort live there.
> - Tag schemes were created in [[History]] Phases 23 (rigor tags) and 24 (CVT methodologist tags + 5C dimensions).
> - This wrapper page was created in Phase 25.

[[Welcome]] · [[DGRAPH]] · [[DGRAPH-TABLE]] · [[History]] · [[Skill]]

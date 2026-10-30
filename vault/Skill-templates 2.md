---
name: skill-templates
description: Reference doc — node-file templates, audit invariants, and per-paper write-up steps. Loaded by Skill.md when extracting a paper. Steps 4–10 of the extraction pipeline.
parent_skill: extract-discourse-nodes
created: 2026-04-29
updated: 2026-08-26
---

# Skill — Templates & Audits (Steps 4–10)

This file holds the per-step detail for **Steps 4 through 10** of the discourse-graph extraction pipeline. The slim orchestrator (`Skill.md`) covers the workflow, vault structure, node types, and Steps 1–3; load this file when you need template bodies, audit scripts, structured-abstract specifics, or the Step 4b TRIPOD-LLM table.

> See also:
> - `Skill.md` — orchestrator (workflow at a glance, Steps 1–3, pointers).
> - `Skill-synthesis.md` — Steps 11–14: cross-paper synthesis + public render + ESS Bases.
> - `Skill-references.md` — Naming conventions, Key Principles, Common Pitfalls, After Extraction.

---

## Step 4: Write the Node Files

All five node types use the templates in the `templates/` folder (EP nodes follow the inline template in [Step 11](#step-11-cross-paper-synthesis-evidencepatterns--review-arena); QUE/CLM/EVD/CVT use the per-type files in `templates/`). Each section below specifies the body structure and required slots.

### EVD template body

The EVD body has four required content blocks plus three reverse-link sections. The `## Methods Context` slots use a structured schema (study design + tools + DV/IV; procedure; participants + sample-size flow). The `## Other Notes` block carries an EVD-specific TRIPOD-LLM **item 17 (Performance)** mini-table; the *paper-level* TRIPOD-LLM Methods + Results compliance table lives in the source file (`source/@<citekey>.md`) and is linked from each EVD — see [Step 4b](#step-4b-paper-level-tripod-llm-table-in-the-source-file) below.

```
---
NodeFormality: draft
human_reviewed: no
aliases:
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
nodeID: <UUIDv7 — generate with `python3 -c "import uuid; print(uuid.uuid7())"`>
---

## Source

[[@<citekey>]]

## Description

> "<verbatim Description quote>" (<Author>, <year>, p. <N>)
>
> Grounding figure/table (if any): <one-line caption>
>
> ![[<citekey>-<fig-or-table-label>-p<N>.png]]

## Methods Context

### What?

> **Study design:** <e.g., RCT / cross-sectional benchmark / corpus-annotation study / few-shot LLM evaluation>. **Method type:** <how the measurement was made>. **Tools:** <models, frameworks, instruments, datasets>. **Dependent variable(s):** <outcome measured>. **Independent variable(s) / covariates:** <conditions varied or controlled>.
>
> "<verbatim quote describing the design / measurement>" (<Author>, <year>, p. <N>)

### How?

> **Procedure:** <step-by-step description of how the measurement was actually carried out — preprocessing, model training, prompt construction, statistical tests, etc.>
>
> "<verbatim quote describing the procedure>" (<Author>, <year>, p. <N>)

### Who?

> **Models / participants:** <who or what was measured — model lineup, participants, annotators>. **Sample-size flow:** <original recruited / sourced → exclusions → final analyzed>. For datasets, list both the candidate pool and the analyzed subset.
>
> "<verbatim quote describing the sample>" (<Author>, <year>, p. <N>)

## Other Notes

<optional: caveats not big enough for a CVT, related findings, or EVD-specific commentary>

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@<citekey>#TRIPOD-LLM reporting summary]].

| <metric column header> | <value column header> |
| --- | --- |
| <e.g., metric name, condition, model> | <e.g., F1 0.65, p-value, n=50/100> |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - ...]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - ...]]
```

**Why this schema (vs. free-form prose):** the four-line What/How/Who frame forces parity across papers — a reader skimming any EVD knows exactly where to find the design, the procedure, and the sample-size flow. The verbatim quote that follows each prose block grounds it in the source PDF (and gets a coloured screenshot via `quote_pipeline.py` — light red for EVD).

**Screenshot embeds are inserted by the pipeline, not by hand.** Author the prose + verbatim quote; run `python3 scripts/quote_pipeline.py evd` and the pipeline appends `> ![[<citekey>-evd-p<N>-<idx>.png]]` under each quote with the canonical naming. Across EVDs of the same paper, idx values are globally unique per (citekey, page) so screenshots never collide.

#### Step 6: Structured abstract on the source page

Each `source/@<citekey>.md` carries a plain-language **structured abstract** at the top, synthesized from that paper's discourse-graph nodes. It is the entry point for any human reader: someone landing on the source page should be able to learn what the paper asks, what it does, what it finds, what it claims, and what limits those claims, without leaving the page.

**Synthesize from already-extracted nodes — never re-read the PDF.** The EVDs (Description quote + Methods Context What/How/Who + Other-Notes item-17 mini-table), the CLM(s) the paper supports, the CVTs that apply to its EVDs, and the QUE that frames it together contain everything the abstract needs.

**Structure (5 sections, in this order, between the frontmatter and the TRIPOD-LLM table):**

```markdown
## Structured abstract

> [!info] A plain-language summary built from this paper's discourse-graph nodes. Numbers and findings link back to specific EVD nodes — click any link to drill in.

### Question
<2–4 sentences in everyday language. End with `See [[QUE - …]].`>

### Methods
**Design.** <1–2 sentences combining the EVDs' study-design descriptors.>
**Tools.** <2–4 sentences naming models / frameworks / instruments with brief inline glosses.>
**Procedure.** <3–6 sentences in chronological order; active voice.>
**Sample.** <2–3 sentences with the original-to-final sample-size flow.>

### Findings
<One bullet per EVD. Each bullet starts with a 5–10-word **bold lead** in plain English, then 2–4 sentences with the actual numbers (define each metric on first use), and ends with `[[EVD - … - @<citekey>]]`.>

### Claim supported
<1–2 sentences with `[[CLM - …]]` wikilinks plus one sentence of editorial framing about what this means in practice.>

### Caveats
<One bullet per CVT linked to this paper's EVDs. Each starts with a bold lead in plain English, 1–2 sentences explaining the constraint, then `[[CVT - …]]`.>
```

**Readability rules** (high-school-graduate target):
- **Active voice.** "The authors built three studies" — not "Three studies were built."
- **Define jargon on first use.** F1 → "F1 runs from 0 to 1; higher is better; macro-F1 weighs each label equally rather than by frequency." kappa → "Cohen's kappa = 0 to 1, where 1.0 means perfect agreement and 0 means chance." p-value → annotate as "(p=0.0085 — unlikely to be chance)" or "(p=0.095 — no real difference)."
- **Acronyms get a brief inline gloss on first use.** ICL → "in-context learning, where the model is shown a few worked examples"; RAG → "retrieval-augmented generation, where the model gets to look up relevant passages first."
- **Short sentences** (≤25 words). Break compound sentences. No nested parentheses.
- **No `→` arrows or `/` slashes inside prose.** Use words: "and then", "followed by", "or", "compared to."
- **Concrete numbers + abstractions together.** "Roughly 4 in 10 citations (39.18%)" beats either alone.
- **Editorial framing where it earns its keep.** When a finding has a deployment implication (e.g., GPT-4's 0.09 F1 on the most-important class), say it plainly: *"a tool that misses 90% of inaccurate citations is not a tool a journal would deploy."*

**What goes where:**

| Section | Source nodes |
| --- | --- |
| Question | the QUE node title + reframe in everyday language |
| Design | each EVD's `Study design:` descriptor |
| Tools | each EVD's `Tools:` list, with glosses |
| Procedure | each EVD's `Procedure:` block, chronologically ordered |
| Sample | each EVD's `Who?` block, leading with the sample-size flow |
| Findings | each EVD's Description + Other-Notes item-17 mini-table |
| Claim | the CLM(s) the paper supports |
| Caveats | the CVTs linked to this paper's EVDs |

**Pitfalls:**
- Do **not** re-read the PDF — everything is already in the nodes.
- Do **not** invent findings or numbers.
- Do **not** include compliance icons (●/◐/○) here; those belong only in the TRIPOD-LLM table below.
- Do **not** modify the frontmatter or the TRIPOD-LLM table when inserting the abstract.
- Wikilinks are mandatory: every EVD bullet, the QUE in Question, the CLM(s) in Claim, and every CVT in Caveats must link.

The Sarol source file (`source/@sarolAssessingCitationIntegrity2024.md`) is the canonical example — match its tone and depth.

##### Step 6.b: Methods + Results visualizations (Mermaid)

Each structured abstract carries two visualization sub-sections — `### Methods at a glance` and `### Results at a glance` — placed after the Caveats sub-section. Use Mermaid (Obsidian-native; renders in preview).

**Methods at a glance** — a `flowchart TD` showing the pipeline. Stick to information already in the EVDs. Recommended four-class palette:

```
classDef data fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;     /* data sources & sample-size milestones */
classDef step fill:#FFF8E1,stroke:#F57F17,color:#5D4037;     /* preprocessing / annotation steps */
classDef model fill:#F1F8E9,stroke:#2E7D32,color:#1B5E20;    /* models / pipelines */
classDef result fill:#FCE4EC,stroke:#AD1457,color:#880E4F;   /* evaluation metrics */
```

Bold key sample-size milestones inside node labels with `<b>...</b>`. Wrap long labels with `<br/>` rather than letting them sprawl.

**Results at a glance** — one to three Mermaid charts that visualize the headline numbers. Pick from:
- `xychart-beta` bar chart for model/condition comparisons (typical: micro-F1 or macro-F1 across model variants).
- A second `xychart-beta` isolating the deployment-critical metric if it diverges from the headline (e.g., per-class F1 on the rare/important class).
- `pie showData` for class-prevalence or proportion findings.

Lead each chart with one short sentence saying what it shows and what counts as "good" (e.g., "higher is better; macro-F1 weighs each class equally").

Do NOT invent numbers. Every value plotted must come from an EVD's Description, Other-Notes item-17 mini-table, or the `## TRIPOD-LLM reporting summary` row 17 wording.

##### Step 6.c: Quality Appraisal section (`## Quality appraisal`)

After the structured abstract and before the TRIPOD-LLM table, add a top-level `## Quality appraisal` section (renamed from "Critical appraisal" in 2026-08 — same purpose, this heading text is now canonical). **It assesses methodological quality, not reporting compliance** — those are different things and the source page now carries both.

**Table shape: `| Domain | Rating | Quote |`, 10–11 rows.** As of 2026-08 this is no longer curator-written justification prose — **every row's rating is grounded in a verbatim quote + `` `§/page` `` locator pulled from the actual paper PDF**, the same discipline as the TRIPOD-LLM table (Step 4b). This exists so a skeptical reader can verify any rating against the exact sentence that justifies it, not just trust the curator's word.

Callout immediately above the table (copy exactly):

```
> [!info] Methodological-quality assessment
> Synthesized from this paper's discourse-graph nodes, grounded in the same paper this page's top trust-signal chips summarize. Covers *methodological quality* — the TRIPOD-LLM table below covers *reporting compliance* instead.
>
> The four validity domains (Construct, Internal, External, Statistical conclusion) are risk-of-bias judgments; every other row is a was-this-addressed checklist item. Blank Rating cells mean not applicable.
> <dl class="callout-legend">
> <dt><span class="status-icon status-icon-low-risk">○</span> Addressed</dt><dd>Fully met, or no meaningful threat to this domain identified</dd>
> <dt><span class="status-icon status-icon-some-risk">◐</span> Partly addressed</dt><dd>A real but non-fatal limitation</dd>
> <dt><span class="status-icon status-icon-high-risk">●</span> Not addressed</dt><dd>A significant, unaddressed gap</dd>
> </dl>
```

The `[!info]` line is a short title only — keep the explanation in the blockquote lines below it as its own paragraph(s), not crammed onto the title line. A callout's title renders bold and small; a long run-on sentence there is unreadable, which is why this was restructured in 2026-09.

**"Risk" language is reserved for the 4 named validity domains** (Construct, Internal, External, Statistical conclusion validity) — that's genuinely what they assess. Every other row (Reproducibility and all Rigor-signal rows below) is a plain checklist item: was this addressed or not, with no risk framing. All rows share the same ○/◐/● + blank-for-N/A rating scale regardless of which framing applies to their Domain-column wording. **In this table the fill tracks the risk/gap, the reverse of TRIPOD-LLM:** ○ empty = addressed / low risk, ◐ half = partly addressed / some risk, ● solid = not addressed / high risk (fixed 2026-10; the site previously drew low risk as a solid dot). The site also accepts 🟢/🟡/🔴 in these cells and draws them as ○/◐/●.

**Rows 1–5, the original methodological-quality domains** (○ Addressed · ◐ Partly addressed · ● Not addressed):

| Domain | What you're checking |
| --- | --- |
| **Construct validity** | Does the metric / task actually measure what the authors claim? Does the headline metric (macro-F1, accuracy, κ) map to the deployment construct? |
| **Internal validity** | Could the comparison be biased? Test-set contamination, data leakage, confounded prompts, asymmetric scoring rules, LLM-as-judge issues, single vs. ensemble baselines. |
| **External validity** | Do findings generalize? Sample restrictions (single discipline, English-only, single conference), exclusions baked into the corpus, evaluation against a single human comparator. |
| **Statistical rigor** | Appropriate uncertainty estimates, multiple-comparison correction, sample size for the rare/important class, paired vs. independent tests, confidence intervals on F1. |
| **Reproducibility** | Code + data availability, deterministic outputs (seed/temperature reported?), proprietary-API dependencies, dated model snapshots vs. floating versions. |

**Rows 6–10 (or 11), the benchmarking-specific Rigor signals** — one row per tag the source's frontmatter carries (same tags used by the top-of-page Rigor chips, `components/TopBadges.tsx` in `living-synthesis-site`):

| Domain | Frontmatter tag | What you're checking |
| --- | --- | --- |
| **Data leakage** | `rigor/data-leakage/{addressed,partial,unresolved,not-addressed}` | Could the evaluated models have seen this test data during pretraining? Web-scraped or long-public corpora are the highest risk. |
| **Baseline adequacy** | `rigor/baseline-adequacy/{addressed,partial,not-addressed}` | Is there a meaningful, independently-motivated floor to beat (a naive baseline, a prior published result), or is the only comparison between the paper's own model variants? |
| **Train/dev/test hygiene** | `rigor/train-dev-test/{addressed,partial,unresolved,not-addressed}` | Are training, development, and test data kept separate and is that separation described? Often blank (not applicable) for zero-shot evaluation papers with no model training. |
| **Multiple-comparisons correction** | `rigor/multiple-comparisons/{addressed,partial,not-addressed}` | When many models × tasks × metrics are compared, is there any correction (Bonferroni, FDR, or even an explicit acknowledgment) for the resulting multiple-testing risk? Usually `not-addressed` — most papers don't do this. |
| **Human-baseline comparability** | `rigor/human-baseline/{addressed,partial,not-addressed}` | Is there a genuine human-performed comparison point (not just "we assume experts would do X"), and is it methodologically comparable (same task, same data)? |
| **Statistical power** | `rigor/statistical-power/{adequate,inadequate}` | **Only add this row if the paper actually reports a power analysis** — no tag means no row, per an explicit "if and only if it's sensible for this method" design call. Don't add a muted "not done" row for papers that never attempted one; that would misrepresent silence as a graded finding. |

Each new row's Rating cell is blank (not applicable) exactly when its Quote cell says `Not applicable`/"not applicable" — never rate a genuinely inapplicable row ● / ◐ / ○ just because a quote exists explaining the inapplicability.

Each new row's Quote cell: a verbatim quote from the PDF, or `Not reported`/`Not applicable` plus a short judgment-call clause when no single quotable sentence exists (e.g. *"Not applicable — no model training or fine-tuning is performed; all LLMs are evaluated zero-shot"* for Train/Dev/Test Hygiene on a pure-evaluation paper). **Never paraphrase or invent a quote** — verify it appears verbatim in the PDF (NFKD + alnum normalization tolerates PDF-extraction artifacts like en-dash mangling or footnote-number word-splits; a quote that still doesn't match after that is either wrong or needs a different source passage).

Item 17's Performance row-style convention (`` `per-EVD` `` as a code span, not plain parenthetical text) does not apply here — this is a paper-level table with no per-EVD analog.

End with a `**Bottom line.**` paragraph: 2–3 sentences synthesizing the practical implication. Given the appraisal, what should a reader actually take away about the strength of this paper's claims, and what would have to improve before the result is deployment-ready? (Unchanged from before — this paragraph is editorial synthesis, not a single quotable fact, so it doesn't get a Quote-column treatment.)

**Calibration** (for the original 5 domains; the same ○/◐/● logic applies to the new rows):
- ● Not addressed = obvious, paper-killing flaw (test contains training, metric ↔ construct mismatch, "human-comparable" backed by one rater).
- ◐ Partly addressed = the most common rating; most papers have *some* validity issue worth flagging.
- ○ Addressed = defensible only when the design is rigorous on this domain.
- Don't mistake reporting transparency for methodological quality. A paper can be ● (fully reported) across the TRIPOD-LLM table and still ● (high risk) on construct validity in this one.

The louAAAR10 (`@louAAAR10AssessingAIs2025.md`) and woelfle (`@woelfleBenchmarkingHumanAICollaboration2024.md`) source files are the canonical examples for Step 6.b and the current (2026-08) Step 6.c format — **but note they live in `living-synthesis-site`'s own `vault/source/` copy, not this vault** (see the Skill.md build-output note: the two have diverged, and this vault's own `source/*.md` files haven't been re-extracted to the new format yet). Read one there in full before writing a new file in this vault to the same standard.

---

#### Step 4b: Paper-level TRIPOD-LLM table in the source file

Each `source/@<citekey>.md` carries a paper-level TRIPOD-LLM reporting summary covering the Title/Abstract/Background/Objectives items (1–4), every Methods item (5a–15), and every Results item (16a–18) — **42 rows total, as of 2026-08** (previously 37; items 1–4 were added). **Four columns**:

| # | Item | RATING | Quote |
| --- | --- | :---: | --- |

The third column (header text literally `RATING`, not a checkmark symbol) is a **compliance icon** so a reader can skim alignment with TRIPOD-LLM at a glance — same ●/◐/○/blank convention as the Quality Appraisal table (Step 6.c), so a reader learns one legend for both tables:

| Icon | Meaning |
| :---: | --- |
| ● | Addressed (fully reported) |
| ◐ | Partly addressed (partially reported / unclear) |
| ○ | Not addressed (should be reported but is missing) |
| *(blank)* | Not applicable to this study |

Callout immediately above the table — title + intro paragraph are copy-exact except the bracketed item-range clause, which should match the paper's actual item coverage if it differs from the norm; the legend div is always copy-exact:

```
> [!info] Reporting compliance for this paper
> Mapped to the TRIPOD-LLM checklist (Title/Abstract/Introduction items 1–4, Methods items 5a–15, Results items 16a–18).
>
> TRIPOD-LLM is a clinical-ML guideline applied here to a non-clinical AI-research benchmark: where an item's own wording says "healthcare context" or "care pathway," it's read as "research-evaluation context" / "research workflow" instead. Item 17 (Performance) is reported per-EVD; see each EVD's `## Other Notes`. Blank RATING cells mean not applicable.
> <div class="callout-legend-flat">
> <span><span class="status-icon status-icon-good">●</span>Addressed</span>
> <span><span class="status-icon status-icon-partial">◐</span>Partly addressed</span>
> <span><span class="status-icon status-icon-bad">○</span>Not addressed</span>
> </div>
```

Same rule as Step 6.c: the `[!info]` line is a short title only, with the explanation as separate blockquote paragraphs below it — not one long run-on title sentence.

**The fourth column (`Quote`) — as of 2026-08, this is a verbatim quote + `` `§/page` `` locator, not a paraphrase.** Format: `*"exact quoted text from the PDF"* \`§3.1, p.4\`` (or `` `Table 2, p.5` ``, `` `Abstract, p.1` ``, `` `Appendix B.2, p.16` `` — whatever locator actually identifies where in the PDF the quote lives). When the paper genuinely doesn't report something, write literally `Not reported` or `Not applicable` — never invent or paraphrase a quote to fill the cell. **This is a hard rule, not a style preference**: a fabricated citation was caught and fixed during this rollout before it shipped; treat any quote you can't verify character-for-character in the PDF text (after NFKD + alnum normalization — see Step 6 verbatim-audit rules for known false-positive patterns like en-dash mangling and footnote-number word-splits) as `Not reported` rather than a best guess. Two quotes may legitimately share the same source sentence when the paper only has one clean statement covering two adjacent items (e.g. items 7d and 8b both describable by one sentence) — reuse rather than invent a second quote.

**Item 1 (Title)** is always `*"<exact paper title>"* \`Title\``. **Item 2 (Abstract)** is always `Assessed separately under TRIPOD-LLM's own Abstract extension, not scored here` (no quote — this is a structural placeholder, not a real per-paper judgment). **Items 3a/3b (Background)** and **4 (Objectives)** get real quotes from the paper's introduction — 3a for the context/rationale, 3b for the target population/setting, 4 for the stated aim.

**Item 17 (Performance) is reported per-EVD, not in the source file** — the source-file row's RATING column reads `` `per-EVD` `` as a code span (not plain parenthetical text), and the Quote column reads `Reported per-EVD. See each EVD's \`## Other Notes\`.`. Each EVD then carries a small table with that EVD's specific F1 / kappa / prevalence / etc. numbers.

The source-file table covers the canonical set of items below:

- **Title/Abstract/Background/Objectives (1, 2, 3a, 3b, 4):** title, abstract (placeholder), background context, target population, objectives.
- **Data (5a–5e):** sources, distribution, dates, pre-processing, missing/imbalanced data.
- **Analytical Methods (6a–6e):** LLM name + version, development process, inference settings / prompting, output, classification thresholds.
- **LLM Output / Evaluation (7a–7e):** quality metrics, downstream relevance, outcome definition, subjective interpretation, comparisons.
- **Annotation (8a–8c):** guidelines, annotator count + IAA, annotator background.
- **Prompting (9a–9b):** design, prompt-development data.
- **Other Methods (10–15):** summarization, instruction tuning, compute, ethical approval, open-science (14a–14f), patient/public involvement.
- **Results — Participants (16a–16d):** flow, characteristics, distribution comparison, n per analysis.
- **Performance (17):** *per-EVD; see each EVD.*
- **LLM updating (18):** if applicable.

For non-clinical NLP papers, healthcare-specific items (16a–c patient/EHR flow, 13 ethical approval if no human subjects, 15 patient/public involvement, 14d clinical-trial registration) are typically blank (not applicable). Leave the RATING cell blank rather than dropping the row so the table structure stays canonical across papers — the Quote cell should still say `Not applicable` plus why.

The louAAAR10 source file (`@louAAAR10AssessingAIs2025.md`) is the canonical example for the current (2026-08) 42-row Quote-column format — same caveat as Step 6.c above: it lives in `living-synthesis-site`'s own `vault/source/` copy, not this vault. Read it there in full before writing a new file in this vault to the same standard.

### CLM template body

```
---
NodeFormality: draft
human_reviewed: no
TruthValue: 0.5
aliases:
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
nodeID: <UUIDv7 — generate with `python3 -c "import uuid; print(uuid.uuid7())"`>
---

### Key Papers Making This Claim

> [!info] Papers
>
> [[@<citekey-1>]]
> [[@<citekey-2>]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
>
> "<verbatim claim quote>" (<Author>, <year>, p. <N>)
>
> ![[<citekey>-clm-<slug>-p<N>.png]]

### Supporting Evidence

> [!info] EVDs from the cited papers (auto-derived; verify before citing)

- [[EVD - ...]]
```

### CVT template body

```
---
NodeFormality: draft
human_reviewed: no
aliases:
appliesTo:
  - "[[EVD - ...]]"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
nodeID: <UUIDv7 — generate with `python3 -c "import uuid; print(uuid.uuid7())"`>
type: <author-stated | inferred>
severity: <low | moderate | high>
---

## Source

[[@<citekey>]]

### Limitation

<one-paragraph summary of the methodological limitation>

### Supporting Quote

> [!info] Quotes
>
> "<verbatim limitation quote>" (<Author>, <year>, p. <N>)
>
> ![[<citekey>-cvt-p<N>-<n>.png]]
>
> [Inferred: ...]   <!-- if type is `inferred`, brief justification here -->

### Applies To

[[EVD - ...]]
```

### QUE template body

```
---
NodeFormality: draft
human_reviewed: no
aliases:
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
nodeID: <UUIDv7 — generate with `python3 -c "import uuid; print(uuid.uuid7())"`>
---

### Key Papers Asking Question

> [!info] Papers
>
> [[@<citekey>]]

### Snippet: Quote(s) & Screenshots

> [!info] Quotes
>
> "<verbatim question framing quote>" (<Author>, <year>, p. <N>)
>
> ![[<citekey>-que-p<N>-1.png]]

### Supporting Claims (with their evidence)

> [!info] CLMs whose topic matches this question, with their supporting EVDs nested underneath. Auto-derived via keyword overlap; verify each link is truly supportive before citing.

- [[CLM - ...]]
    - [[EVD - ...]]
    - [[EVD - ...]]

- [[CLM - ...]]
    - [[EVD - ...]]
```

**QUE quote/screenshot content rule (NON-NEGOTIABLE).** Each quote in a QUE's `### Snippet: Quote(s) & Screenshots` block, and each accompanying screenshot, must be **the paper's research question, goal, aim, objective, or purpose statement** — nothing else. Concrete tests:

- ✅ Acceptable: explicit research questions ("RQ1: …", "Can LLMs …?"), explicit aim statements ("This study aims to …", "The objective was to …"), purpose statements ("we explore …", "we set out to determine …"), explicit problem statements that frame the question.
- ❌ Not acceptable in a QUE: method descriptions ("we used X model with Y prompt …"), result/finding statements ("X achieved 0.8 F1 …", "we find that …"), claim/conclusion statements ("Our system substantially improves …"), corpus/dataset introductions ("We introduce X, a benchmark …"), even when the same paper is cited.

Method content belongs in EVD `## Methods Context`. Result content belongs in EVD `## Description` or its Other-Notes item-17 mini-table. Claim content belongs in CLM bodies. CVTs hold limitations. The QUE is **only** about what the paper is asking.

When a QUE quote is mixed (one sentence has the aim, the next sentence reports the finding), keep only the aim sentence. If trimming would leave the quote ungrammatical, replace it with a different question-framing quote from the same paper rather than running over.

**QUE title phrasing rule.** The QUE quote rule above governs what *evidence* justifies a QUE; this rule governs how to *word the QUE title itself*. Derived from a corpus-wide audit of every LLM-drafted QUE title against the maintainer's own edited version — apply these transformations before filing a QUE title, not just on revision.

1. **Check the canonical template list first.** Before coining a new phrasing, check whether the paper's question already matches one of the recurring capability-dimension templates below. Papers phrase the same underlying question dozens of different ways (STROBE compliance, CONSORT compliance, checklist verification are all "alignment with reporting guidelines" in disguise) — the corpus is more useful when unrelated papers that test the same capability converge on the *same* QUE title (and can then share one QUE node) rather than each minting its own bespoke phrasing.

    | Capability dimension | Canonical QUE phrasing |
    | --- | --- |
    | Error/quotation-error detection | How well can LLMs identify errors in research reports? |
    | Limitation identification | How accurately can LLMs identify limitations in research reports? |
    | Citation-integrity checking | How well can NLP models find citation integrity errors in research reports? |
    | Confounder identification | How well can LLMs identify confounders in research reports? |
    | Novelty evaluation | How well can LLMs evaluate the novelty of research reports? |
    | Reporting-guideline alignment (STROBE/CONSORT/PRISMA/checklists) | How accurately can LLMs evaluate research reports' alignment with reporting guidelines? |
    | Methodological rigor / risk-of-bias appraisal (AMSTAR, RoB, QUADAS) | How accurately can LLMs evaluate research reports' methodological rigor using critical appraisal tools? / How well can LLMs evaluate a study's risk of bias? |
    | Fitness for purpose / applicability (PRECIS-2 and similar) | How accurately can LLMs evaluate research reports' fitness for purpose (applicability)? |
    | Submission-checklist alignment | How well can LLMs assess alignment of a research report with submission checklists? |
    | General capability to review/critique | How well can LLMs review research reports? |
    | Evaluating others' reviews/critiques | How accurately can LLMs evaluate reviews of research reports? |
    | Review criticality relative to humans | How critical are LLMs' reviews of research reports relative to humans? |
    | Peer-review quality vs. human reviews | How do LLM-generated peer reviews compare to human-generated peer reviews in quality? |
    | Peer-review preference | Do humans prefer LLM-generated peer reviews or human-generated peer reviews? |
    | Overlap with human reviewer feedback | How much do LLM-generated peer reviews overlap with human-generated reviews? |
    | Multi-agent/system-level review improvement | To which extent can multi-agent LLM systems improve (specificity and helpfulness) of peer reviews? |
    | Reviewer accuracy (broad) | To which extent are LLMs accurate peer reviewers? |
    | Broad comprehension/assessment (no specific instrument) | How accurately can LLMs evaluate research reports? |
    | Domain-specific decision-making role-play (IRB, ethics) | How well can AI platforms emulate [role] decision-making and draft [artifact] for [purpose]? |

2. **Canonical object noun: "research reports."** Collapse every paper-specific variant — "scientific papers," "scientific manuscripts," "academic papers," "biomedical publications," "medical research papers," "clinical trial reports," "submitted papers," "abstracts" — to **"research reports."** This is the single most consistent substitution across the whole corpus; treat it as a controlled-vocabulary term, not a stylistic nicety.

3. **Canonical subject: "LLMs."** Genericize specific model names ("ChatGPT," "GPT-4") and specific system descriptions ("LLM-based RAG system," "LLM-based agents") to plain **"LLMs"**, *unless* the specific mechanism (e.g., "multi-agent LLM systems") is itself the capability under test and central to what makes the paper's contribution distinct — then keep it.

4. **Degree framing, not binary framing.** Rewrite bare "Can LLMs X?" as "**How well** / **How accurately** / **To which extent** can LLMs X?" — a graded question, not a yes/no one. Reserve "Can LLMs X?" only for genuinely binary capability questions with no natural degree axis (rare).

5. **Drop comparison-to-human framing** ("compared to human experts," "compared to expert judgment," "than general-purpose LLMs") unless that comparison is literally what the paper is testing — in which case reframe as "**X relative to humans**" (e.g., "How critical are LLMs' reviews of research reports relative to humans?") rather than "compared to."

6. **Strip implementation/methodology detail** from the title: "without fine-tuning," "automatically," "reliably," "at scale," "using PRISMA/AMSTAR/PRECIS-2" (name the *capability dimension* instead — see the template table), specific prompting or architecture details. That detail belongs in the EVD's `## Methods Context`, not the QUE title.

7. **Split compound questions.** If the paper's question (or your first-draft title) bundles two or more distinct evaluative dimensions joined by "and" — e.g., quality *and* preference; reporting-guideline alignment *and* methodological rigor *and* applicability — split into N separate single-dimension QUEs, one per instrument/claim, rather than one compound QUE. Use the possessive construction (`research reports' methodological rigor`, `research reports' fitness for purpose`) across the split set for parallelism.

8. **Drop questions that aren't really capability questions.** A pure implementation/methods question ("What is the optimal input format for X?") or a comparison-selection framing that isn't the paper's actual evaluative contribution doesn't need a QUE at all — note it in EVD Methods Context instead and skip filing the node.

When in doubt, prefer the shortest phrasing that (a) names the capability dimension from the template table, (b) uses "LLMs" and "research reports" as the subject/object, and (c) asks "how well/accurately/much" rather than "can."

---

## Step 5: Build Reverse Links

After all node files are written, run `scripts/reverse_links.py` to populate the graph's inbound sections (auto-derived, idempotent on re-run):

- For every EVD: scan all CVTs whose `appliesTo` references the EVD → fill its `## Caveats` section. Scan all CLMs whose `Papers` block contains the EVD's citekey → fill its `## Supports Claim(s)` section.
- For every CLM: scan all EVDs whose source citekey is in the CLM's `Papers` block → fill its `### Supporting Evidence` section.
- For every QUE: keyword-match the QUE title against CLM titles. For each matching CLM, copy its supporting EVDs as nested children → fill the QUE's `### Supporting Claims (with their evidence)` section.

Each generated section includes a `verify before citing` caveat in the body — these are paper-level overlaps, not statement-level entailments. The user is the curator.

**Dedupe pass.** If the EVD-specificity pipeline (the per-EVD anchor replacements after Step 4) was re-run, duplicate quote+screenshot pairs may accumulate. Run a small dedupe step that drops repeat `> ![[...]]` embeds in any single section, removing the preceding `> "..."` line if it duplicates as well. Idempotent.

### Step 5b: Audit graph attachment invariants

After reverse links are built, audit the vault against the discourse-graph attachment rules (four for QUE/CLM/EVD/CVT plus one for EP). **Fail the extraction if any rule is violated** — the user can then either (a) attach the unattached node manually, (b) write a new QUE/CLM that absorbs it, or (c) accept the violation with a documented reason.

| # | Rule | What it means |
| - | ---- | ------------- |
| 1 | CVT `appliesTo` contains only EVDs | Caveats constrain evidence, not claims. A CLM with a CVT directly attached signals confused scoping. |
| 2 | Every CLM appears in ≥ 1 QUE's nested structure | A claim that no question asks for is an orphan and should either be attached to a question or deleted. |
| 3 | Every EVD appears in ≥ 1 CLM's `### Supporting Evidence` | Evidence that supports no claim is unused; either link it to a CLM or write the missing CLM. |
| 4 | Every EVD appears in ≥ 1 QUE's nested structure | Symmetric to rule 3 at the question level. |

Audit script outline (in Python — full version at `scripts/verbatim_audit.py` for verbatim audit; the attachment-rule audit below is short enough to run inline or as part of the same script):

```python
import re
from pathlib import Path
vault = Path('.')
all_clms = {f.stem for f in (vault/'claims').glob('CLM*.md')}
all_evds = {f.stem for f in (vault/'evidence').glob('EVD*.md')}

# Rule 1: CVTs link to CLMs?
for f in (vault/'caveats').glob('CVT*.md'):
    m = re.search(r'^appliesTo:\s*\n((?:^\s*-\s*"\[\[.*?\]\]"\s*\n?)+)', f.read_text(), re.MULTILINE)
    if m and re.search(r'\[\[CLM', m.group(1)):
        print(f'RULE 1 VIOLATION: {f.name}')

# Rules 2-4: build link sets
clms_in_ques = set(); evds_in_ques = set()
for f in (vault/'questions').glob('QUE*.md'):
    text = f.read_text()
    clms_in_ques.update(re.findall(r'\[\[(CLM[^\]]+)\]\]', text))
    evds_in_ques.update(re.findall(r'\[\[(EVD[^\]]+)\]\]', text))
evds_in_clms = set()
for f in (vault/'claims').glob('CLM*.md'):
    text = f.read_text()
    m = re.search(r'### Supporting Evidence\s*\n.+?\n+((?:- \[\[.*?\]\]\s*\n?)+)', text, re.DOTALL)
    if m: evds_in_clms.update(re.findall(r'\[\[(EVD[^\]]+)\]\]', m.group(1)))

if all_clms - clms_in_ques: print(f'RULE 2: unattached CLMs: {all_clms - clms_in_ques}')
if all_evds - evds_in_clms: print(f'RULE 3: EVDs in no CLM: {all_evds - evds_in_clms}')
if all_evds - evds_in_ques: print(f'RULE 4: EVDs in no QUE: {all_evds - evds_in_ques}')
```

The audit should run at the very end of the extraction pipeline. If any violation is reported, do not promote NodeFormality (Step 8) until fixed.

---

## Step 6: Verbatim Audit

Run `scripts/verbatim_audit.py` to compare every quote against its source PDF and flag paraphrases. For each `> "..."` line in any node:

1. Normalize both the quote text and the cited page's text (NFKD + alnum-only).
2. If the quote isn't a substring of any page's normalized text, find the page with the longest matching prefix and report `matched X of Y chars`.
3. Save the report as `paraphrase_audit_<date>.tsv` at the vault root.

Severity tiers:
- **0% match (Tier 1)**: fabricated or wrong page citation. Fix or annotate.
- **<50% match (Tier 2)**: major paraphrase. Replace with verbatim source text.
- **50–90% match (Tier 3)**: moderate — usually a missing/inserted word.
- **>90% match (Tier 4)**: tail-only divergence — typically minor, often acceptable.

Known false positive: pdftotext renders en-dashes (`Human−AI`) as `e` (`HumaneAI`), so a quote containing `Human−AI` may report 0% match even though it's verbatim. Flag and ignore for that pattern.

When fixing a paraphrase, regenerate the screenshot (the new quote text will likely have a different bbox).

---

## Step 7: Readability Formatting

Run `scripts/readability_pass.py` to apply mechanical formatting after all content is in place:

1. **Blank line after every `##` and `###` heading** before body content.
2. **`>` separator inside blockquotes** between any non-empty `> ...` line and a following `> ![[...]]` screenshot embed.
3. **Blank line between consecutive `- [[wikilink]]` items** in lists so each link gets its own visual chunk.
4. Collapse any `\n\n\n+` to `\n\n` to keep spacing consistent.

---

## Step 8: Promote NodeFormality

Promote nodes from `NodeFormality: draft` → `ReadyForInternal` once they meet the structural-completeness bar:

- `## Source` block with `[[@citekey]]`
- `## Description` with verbatim quote + screenshot
- (EVDs only) `## Methods Context` with What/How/Who, each with quote + screenshot
- Reverse-link sections present (`## Caveats`, `## Supports Claim(s)` for EVDs; `### Supporting Evidence` for CLMs; `### Supporting Claims` for QUEs)

Nodes flagged in the verbatim audit at <50% match (Tier 1+2) should stay at `draft` until manually fixed.

`human_reviewed` is a separate axis from `NodeFormality` and is never set by the extraction pipeline. `NodeFormality` records automated structural/verbatim-match completeness; `human_reviewed` records whether an actual person has read and signed off on the node. It stays `no` for every node the pipeline creates or promotes — flip it to `yes` only when a human has manually reviewed that specific node's content.

`ReadyForInternal` means "structurally complete; ready for human review and use." `ReadyToShare` (the next state, for external use) is granted manually after the user reviews each node.

---

## Step 9: Regenerate DGRAPH.md

After Steps 5–8 pass, regenerate the central index:

```bash
python3 scripts/build_dgraph.py
```

`DGRAPH.md` is the human-readable entry point to the entire vault. It nests every QUE → CLM → EVD → CVT path, with each node as a clickable Obsidian wikilink. The script:

- Reads each QUE's `### Supporting Claims (with their evidence)` section.
- Reads each CLM's `### Supporting Evidence` section.
- Reads each CVT's `appliesTo:` frontmatter.
- Emits YAML frontmatter (`author`, `page_type`, `created`, `updated`, `generated_by`, `prompt_source`) plus three Obsidian callouts (`[!info]`, `[!tip]`, `[!caution]`) before the nested content.
- Preserves the existing `created` date on regeneration; only `updated` advances.

Re-run after every paper added, every CLM/QUE structural change, every CVT `appliesTo` edit, or any time the discourse graph shifts.

---

## Step 10: Save the originating prompt + log to History.md

Every generated document carries provenance back to the prompt that asked for it. After completing the pipeline:

1. Save the user's request (verbatim) to `prompts/<YYYY-MM-DD>-<short-slug>.md` with its own YAML frontmatter (`prompt_type`, `target_page`, `generated_by`, `date`).
2. Append a phase entry to `History.md` describing every concrete change:
   - Files added/edited/deleted (with paths)
   - PNG counts
   - Script(s) used
   - Known limitations or follow-ups
3. If the work generated a new central document (DGRAPH.md, audit report, index file), the prompt link in its frontmatter must resolve via `[[prompts/<filename>]]`.

This keeps a chain: vault state ← script run ← prompt ← user request. Future-you can retrace any decision.


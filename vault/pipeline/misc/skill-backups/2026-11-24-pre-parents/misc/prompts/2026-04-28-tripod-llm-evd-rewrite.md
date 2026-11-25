---
prompt_type: subagent_brief
date: 2026-04-28
generated_by: extract-discourse-nodes
target_page: evidence/EVD*.md (per paper)
---

# TRIPOD-LLM EVD Rewrite — Subagent Brief

You are rewriting every EVD that cites a specific paper to follow a new schema, and writing a paper-level TRIPOD-LLM table to that paper's source file. The Sarol paper (`@sarolAssessingCitationIntegrity2024`) is the **canonical example** — read it before editing.

## Files to read first (canonical example)

- Source-file table: `/Users/ppatel/Documents/living-synthesis/source/@sarolAssessingCitationIntegrity2024.md`
- EVD examples (4 of them, one per Sarol EVD type — descriptive corpus stat / supervised model benchmark / few-shot LLM eval / IAA sub-study):
  - `evidence/EVD - 39.18% of 3063 annotated biomedical citation instances contained accuracy errors - @sarolAssessingCitationIntegrity2024.md`
  - `evidence/EVD - Best NLP model MultiVerS top-20 achieved micro-F1 0.59 and macro-F1 0.52 on citation accuracy classification - @sarolAssessingCitationIntegrity2024.md`
  - `evidence/EVD - GPT-4 achieved F1 0.80 for accurate citations but only 0.09 for not-accurate citations - @sarolAssessingCitationIntegrity2024.md`
  - `evidence/EVD - Inter-annotator agreement on citation accuracy labels was only kappa 0.18-0.31 in annotation phases 1-2 - @sarolAssessingCitationIntegrity2024.md`

Match their structure exactly. Do not invent new sections.

## Task per assigned paper

You will be told a single citekey and the path to its PDF. Do this:

### 1. Read the PDF

Use the `Read` tool on the PDF (it accepts PDFs). For papers > 10 pages, pass `pages: "1-10"`, then `"11-20"`, etc. Focus on **Methods** and **Results** sections — skim Introduction/Discussion only for context.

### 2. List every EVD for this citekey

```bash
ls evidence/EVD*-\ @<citekey>.md
```

These are the EVDs you must rewrite. Keep their existing Description quote, Caveats list, and Supports Claim(s) list **as-is** — only rewrite Methods Context (What/How/Who) and Other Notes.

### 3. Rewrite each EVD

For each EVD, replace the existing `## Methods Context` and `## Other Notes` blocks with the new structure. Schema:

```
## Methods Context

### What?

> **Study design:** <e.g., RCT / cross-sectional benchmark / corpus-annotation study / few-shot LLM evaluation / observational analysis>. **Method type:** <how the measurement was made — e.g., zero-shot LLM evaluation, fine-tuned classifier, manual rating>. **Tools:** <models, frameworks, instruments, datasets>. **Dependent variable(s):** <outcome measured>. **Independent variable(s) / covariates:** <conditions varied or controlled>.
>
> "<verbatim quote from this paper that grounds the design / measurement>" (<Author>, <year>, p. <N>)

### How?

> **Procedure:** <step-by-step description — preprocessing, model training, prompt construction, statistical tests, etc. Be specific.>
>
> "<verbatim quote describing the procedure>" (<Author>, <year>, p. <N>)

### Who?

> **Models / participants:** <who or what was measured>. **Sample-size flow:** <original recruited / sourced → exclusions → final analyzed>. List both candidate pool and analyzed subset.
>
> "<verbatim quote describing the sample>" (<Author>, <year>, p. <N>)

## Other Notes

<existing Other Notes bullets — preserve them unless they duplicate the table below>

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@<citekey>#TRIPOD-LLM reporting summary]].

| <metric column> | <value column> |
| --- | --- |
| <metric / condition / model> | <value with units> |
```

**CRITICAL: Strip any existing `> ![[<citekey>-quote-...png]]` or `> ![[<citekey>-evd-...png]]` lines from the Methods Context blocks.** The pipeline will regenerate them with canonical naming when run later — do not insert any new screenshot embeds yourself. KEEP page-level table/figure embeds like `![[<citekey>-tables-pN-X.png]]` or `![[<citekey>-fig...]]` — only strip the **quote-region** crops.

**CRITICAL: each verbatim quote must be a substring of the PDF text** (after NFKD + alnum-only normalization). Do not paraphrase. Pick the most informative passage from the paper that grounds the prose summary above it.

**Item 17 mini-table:** populate with the SPECIFIC numbers this EVD reports (per-class F1, accuracy, kappa, prevalence, p-value, recall, AUC, etc.). Use whatever column headers fit the EVD type. See the four Sarol EVDs for examples — each uses a different shape.

### 4. Write the source-file TRIPOD-LLM table

Append to `source/@<citekey>.md` (which currently has only frontmatter) the section `## TRIPOD-LLM reporting summary`. Use the four-column structure shown in the Sarol example. Cover **all 37 sub-items** below; mark each with one compliance icon (✅ / ⚠️ / ❌ / ➖) plus a brief value.

#### Compliance icon legend

- ✅ Fully reported
- ⚠️ Partially reported / unclear
- ❌ Should be reported but missing
- ➖ Not applicable to this study

#### Items (Methods 5a–15, Results 16a–18)

**Data**
- 5a Data sources
- 5b Data points + distribution
- 5c Date range of data
- 5d Pre-processing / quality checks
- 5e Missing / imbalanced data

**Analytical Methods**
- 6a LLM name + version
- 6b Development process
- 6c Inference settings / prompting
- 6d Output
- 6e Classification thresholds

**LLM Output / Evaluation**
- 7a Quality metrics
- 7b Relevance to downstream
- 7c Outcome definition
- 7d Subjective interpretation
- 7e Comparison

**Annotation**
- 8a Annotation guidelines
- 8b Annotators + IAA
- 8c Annotator background

**Prompting**
- 9a Prompt design
- 9b Prompt-development data

**Other methods**
- 10 Summarization
- 11 Instruction tuning / alignment
- 12 Compute
- 13 Ethical approval

**Open Science**
- 14a Funding
- 14b Conflicts of interest
- 14c Protocol
- 14d Registration
- 14e Data availability
- 14f Code availability

**Public involvement**
- 15 Patient/public involvement

**Results — Participants**
- 16a Flow of data
- 16b Characteristics
- 16c Distribution comparison
- 16d N per analysis

**Performance + Updating**
- 17 Performance — write `(per-EVD)` in compliance column and `Reported per-EVD. See each EVD's ## Other Notes.` in value column. Do not duplicate the per-EVD numbers here.
- 18 LLM updating

#### Source-file table format

```
## TRIPOD-LLM reporting summary

> [!info] Reporting compliance for this paper, mapped to the TRIPOD-LLM checklist (Methods items 5a–15 and Results items 16a–18). Compliance icons: ✅ fully reported · ⚠️ partially reported / unclear · ❌ should be reported but not reported · ➖ not applicable to this study. Item 17 (Performance) is reported per-EVD; see each EVD's `## Other Notes`.

| # | Item | ✓ | Reported in this study |
| --- | --- | :---: | --- |
| **5a** | Data sources | <✓> | <value> |
... (all 37 rows) ...
| **18** | LLM updating | <✓> | <value> |
```

### 5. Bump `updated:` in each EVD frontmatter to `2026-04-28`

### 6. Report back briefly (under 200 words)

- citekey processed
- N EVDs rewritten (list filenames)
- source file path
- any quotes you couldn't ground in the PDF (paraphrases — flag them but still write them)
- any TRIPOD-LLM items you weren't sure how to assess

Do **not** run the screenshot pipeline — that's the parent agent's job after all subagents return.

## Common pitfalls to avoid

- Do **not** invent new sections (`### Methods`, `### Results` — no, use What/How/Who only).
- Do **not** insert any new `> ![[...png]]` quote embeds. The pipeline does this.
- Do **not** edit the EVD's Description quote, Caveats, or Supports Claim(s) sections.
- Do **not** copy item-17 numbers into the source-file table; that row is `(per-EVD)`.
- For non-clinical NLP papers (most of this corpus), 13 / 14d / 15 / 16a–c are typically `➖` — that's fine.
- TRIPOD-LLM item 5c asks for **dates of the oldest and newest data** used — usually `❌` for evaluation-only papers because authors don't disclose this.
- Item 12 (compute) is almost always `❌` — most papers don't report compute. That's the data, just record it.
- When in doubt between ⚠️ and ✅, pick ⚠️. The compliance icons are more useful when they're calibrated, not lenient.

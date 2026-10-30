---
prompt_type: subagent_brief
date: 2026-04-28
generated_by: extract-discourse-nodes
target_page: source/@<citekey>.md (per paper)
---

# Source-Page Synthesis Brief — Abstract + Visualizations + Critical Appraisal

You are writing **three new top-level sections** at the top of a paper's source file (`source/@<citekey>.md`), synthesized from the discourse-graph nodes already extracted for that paper. The three sections, in order:

1. **`## Structured abstract`** — plain-language summary in 5 sub-sections + 2 visualization sub-sections.
2. **`## Critical appraisal`** — risk-of-bias / validity rating across 5 domains.
3. *(existing)* `## TRIPOD-LLM reporting summary` — leave untouched.

You do NOT re-read the original PDF. The EVDs, CLMs, CVTs, and QUEs already capture everything you need.

## Canonical example to model after

`/Users/ppatel/Documents/living-synthesis/source/@sarolAssessingCitationIntegrity2024.md` — the Sarol structured abstract is the template. Read it before editing. Copy its structure, tone, and depth exactly.

## Task per assigned paper

You will be given a single citekey. Do this:

### 1. Gather the paper's nodes

```bash
# EVDs for this paper (the heart of your synthesis)
ls "evidence/EVD"*"@<citekey>.md"

# CLMs that include this paper in their Papers block
grep -l "@<citekey>" claims/CLM*.md

# CVTs that mention this paper
grep -l "@<citekey>" caveats/CVT*.md

# QUEs that include this paper in their Papers block (pick the most directly-tied one for the Question section)
grep -l "@<citekey>" questions/QUE*.md
```

Read every EVD in full — Description quote, Methods Context (What/How/Who), Other Notes including the item-17 mini-table. Read each CLM/CVT/QUE briefly to confirm the link semantics.

### 2. Synthesize the structured abstract

Insert this section directly under the frontmatter and **above** the existing `## TRIPOD-LLM reporting summary` section in `source/@<citekey>.md`. Use this exact 5-section structure:

```markdown
## Structured abstract

> [!info] A plain-language summary built from this paper's discourse-graph nodes. Numbers and findings link back to specific EVD nodes — click any link to drill in.

### Question

<2–4 sentences. State what the paper is asking, in everyday language. Then state the comparison or design at a high level (e.g., "the authors compare X versus Y", "the authors evaluate Z across N tasks"). End with a wikilink to the most directly-tied QUE: `See [[QUE - <full title>]].`>

### Methods

**Design.** <1–2 sentences. Use the EVDs' Methods Context "Study design" descriptors, but combine into a single readable sentence rather than a comma-separated list.>

**Tools.** <2–4 sentences. Name the models, libraries, frameworks, or instruments. For each unfamiliar acronym or product name, briefly say what it is on first use (e.g., "MultiVerS — a published claim-verification model from Wadden et al. 2022"). Mention model versions / dates only if they're a substantive part of the design.>

**Procedure.** <3–6 sentences. Describe the actual steps in order: how data was collected/preprocessed, how models were trained or prompted, how outputs were evaluated, what statistical tests were used. Active voice ("the authors built…", "the pipeline retrieves…") not passive.>

**Sample.** <2–3 sentences with a clear sample-size flow: original recruited / sourced → exclusions → final analyzed N. Mention the unit of analysis (papers, citations, sentences, etc.). Mention human raters / annotators / participants and their relevant background.>

### Findings

<One bullet per EVD, in the order they appear in the EVDs folder (alphabetical). Each bullet:
- Starts with a 5–10-word **bold lead sentence** that captures the takeaway in plain English (not a metric).
- Then 2–4 sentences with the actual numbers, defining each metric on first use.
- Ends with a wikilink to the EVD: `[[EVD - <full title> - @<citekey>]]`.>

### Claim supported

<1–2 sentences explaining what the findings collectively support, ending with a wikilink to the CLM (or CLMs). Add one sentence of editorial framing: what does this mean for someone considering using the system in practice?>

### Caveats

<One bullet per CVT that links to this paper's EVDs. Each bullet:
- Starts with a 5–10-word **bold lead sentence** that names the limitation in plain English.
- 1–2 sentences explaining why it constrains the findings.
- Wikilink to the CVT: `[[CVT - <full title>]]`.>

### Methods at a glance

<A Mermaid `flowchart TD` showing the pipeline: data sources → preprocessing → models → evaluation. Use the four-class colour palette below. Bold the key sample-size milestones using `<b>...</b>`. Keep node labels short — wrap with `<br/>` rather than letting them sprawl.>

```
flowchart TD
    A["…"] --> B["…"]
    …
    classDef data fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef step fill:#FFF8E1,stroke:#F57F17,color:#5D4037;
    classDef model fill:#F1F8E9,stroke:#2E7D32,color:#1B5E20;
    classDef result fill:#FCE4EC,stroke:#AD1457,color:#880E4F;
    class <ids> data;
    class <ids> step;
    class <ids> model;
    class <ids> result;
```

### Results at a glance

<One to three Mermaid charts visualizing the headline numbers. Pick from:
- `xychart-beta` bar chart for model/condition comparisons (typical: micro-F1 or macro-F1 across model variants).
- `xychart-beta` bar chart isolating the deployment-critical metric if it diverges from the headline (e.g., per-class F1 on the rare/important class).
- `pie showData` for class prevalence or proportion findings.

Add a one-sentence lead-in before each chart explaining what it shows and what counts as "good".>
```

### 2b. Write the critical appraisal section (after the structured abstract, before the TRIPOD-LLM table)

Insert a new top-level section `## Critical appraisal` immediately after the `## Structured abstract` and immediately before `## TRIPOD-LLM reporting summary`.

**Distinction from the TRIPOD-LLM table.** The TRIPOD-LLM table assesses **reporting compliance** (did they say it?). The critical appraisal assesses **methodological quality** (does the design support their conclusions?). Both belong on the source page; they answer different questions.

**Five domains, each rated 🟢 Low risk · 🟡 Some concerns · 🔴 High risk**, with a 1–3 sentence justification grounded in this paper's EVDs/CVTs:

| Domain | What you're checking |
| --- | --- |
| **Construct validity** | Does the metric / task actually measure what the authors claim? Does macro-F1 / accuracy / κ map to the construct (e.g., "useful for deployment")? |
| **Internal validity** | Could the comparison be biased? Test-set contamination, data leakage, confounded prompts, asymmetric scoring rules, the LLM-judge-of-LLM problem, single-model vs. ensemble baselines. |
| **External validity** | Do findings generalize beyond this dataset / model / domain? Sample restrictions (single discipline, English-only, single conference), exclusions baked into the corpus (e.g., tables-and-figures cases), evaluation against a single human comparator. |
| **Statistical rigor** | Appropriate uncertainty estimates, multiple-comparison correction across many models × many metrics, sample size for the rare/important class, paired vs. independent tests, confidence intervals on F1. |
| **Reproducibility** | Code + data availability, deterministic outputs (seed/temperature reported?), proprietary-API dependencies, dated model snapshots vs. floating model versions. |

**Format:**

```markdown
## Critical appraisal

> [!info] A risk-of-bias and validity assessment across five domains, synthesized from this paper's discourse-graph nodes. Each domain gets a rating (🟢 Low risk · 🟡 Some concerns · 🔴 High risk) plus a brief, EVD-grounded justification. The TRIPOD-LLM table below covers *reporting compliance*; this section covers *methodological quality*.

| Domain | Rating | Justification |
| --- | :---: | --- |
| **Construct validity** — does the metric actually measure the construct? | 🟢/🟡/🔴 | <1–3 sentences> |
| **Internal validity** — could the comparison be biased? | 🟢/🟡/🔴 | <1–3 sentences> |
| **External validity** — do findings generalize? | 🟢/🟡/🔴 | <1–3 sentences> |
| **Statistical rigor** — appropriate uncertainty + comparisons? | 🟢/🟡/🔴 | <1–3 sentences> |
| **Reproducibility** — code, data, determinism? | 🟢/🟡/🔴 | <1–3 sentences> |

**Bottom line.** <2–3 sentences synthesizing the practical implication: given the appraisal, what should a reader actually take away about the strength of this paper's claims, and what would have to improve before the result is deployment-ready?>
```

**Calibration heuristics:**
- 🔴 High risk for an obvious, paper-killing flaw — e.g., test set contains training data, the metric reported doesn't match the deployment construct, claim of "human-comparable" backed by a single rater.
- 🟡 Some concerns is the most common — most papers have *some* validity issue.
- 🟢 Low risk only if you can defend it: rigorous comparison, well-defined construct, generalizable sample, appropriate stats.
- Tie justifications back to specific EVDs / CVTs where possible (e.g., "see [[CVT - …]]" inline).
- Don't over-rely on the TRIPOD-LLM compliance icons. Reporting transparency is necessary but not sufficient — a paper can be ✅ across reporting and still 🔴 on construct validity.

### 3. Readability rules (NON-NEGOTIABLE)

- **Active voice.** "The authors built three studies" — not "Three studies were built". "The pipeline retrieves the top 60 sentences" — not "The top 60 sentences are retrieved by the pipeline".
- **Plain language for a high-school graduate.** No statistical jargon without an inline gloss on first use:
  - F1 → "F1 runs from 0 to 1; higher is better; macro-F1 weighs each label equally rather than by frequency"
  - kappa → "Cohen's kappa = 0 to 1, where 1.0 means perfect agreement and 0 means chance"
  - p-value → "(p=0.0085 — unlikely to be chance)" or "(p=0.095 — no real difference)"
  - AUC → "AUC runs from 0 to 1 and measures how well the model separates the two classes"
- **Define acronyms on first use.** ICL → "in-context learning, where the model is shown a few worked examples"; RAG → "retrieval-augmented generation, where the model gets to look up relevant passages first"; etc.
- **Short sentences.** Aim for ≤ 25 words per sentence. Break compound sentences. No nested parentheses.
- **No → arrows or / slashes inside prose.** Use words: "and then", "followed by", "or", "compared to".
- **Concrete numbers, not abstractions.** "Roughly 4 in 10 citations" beats "39.18% prevalence". Both is fine; abstraction-only is not.
- **Editorial framing where it earns its keep.** When a finding has a deployment implication (like GPT-4's 0.09 F1 on the most-important class), say it plainly: "a tool that misses 90% of inaccurate citations is not a tool a journal would deploy."

### 4. Writing technique — what to extract from where

- **Question** ← the QUE node title + your one-sentence reframe in everyday language.
- **Design** ← combine each EVD's `Study design:` descriptor.
- **Tools** ← the EVDs' `Tools:` lists, with brief glosses.
- **Procedure** ← the EVDs' How? blocks, condensed and ordered chronologically.
- **Sample** ← the EVDs' Who? blocks; lead with the sample-size flow.
- **Findings** ← each EVD's Description quote + Other-Notes item-17 mini-table.
- **Claim** ← the CLM(s) the paper supports, with editorial framing about deployment.
- **Caveats** ← the CVTs that link to this paper's EVDs.

### 5. Where to insert

In `source/@<citekey>.md`, the file currently looks like:
```
---
<frontmatter>
---

## TRIPOD-LLM reporting summary
…
```

Insert the new sections **between** the closing frontmatter `---` and `## TRIPOD-LLM reporting summary`, in this order, separated by `---` horizontal rules:

```
---
<frontmatter>
---

## Structured abstract
…
### Question / Methods / Findings / Claim supported / Caveats / Methods at a glance / Results at a glance

---

## Critical appraisal
…

---

## TRIPOD-LLM reporting summary
…  (existing — do not modify)
```

Do not modify the frontmatter or the TRIPOD-LLM table.

### 6. Report back (under 200 words)

- citekey processed
- counts: N EVDs read, N CLMs linked, N CVTs linked, the QUE used
- any quotes you couldn't ground in an EVD (shouldn't happen — flag if it does)
- any node-graph gaps you noticed (e.g., an EVD with no CLM that supports it, a CVT not linked to any EVD)
- the **highest-risk domain** in your critical appraisal (which one came out 🔴 / 🟡 and why)
- one-sentence editorial summary of what this paper actually shows

## Common pitfalls

- **Do not re-read the PDF.** Everything you need is in the discourse-graph nodes.
- **Do not invent findings.** Every number must come from an EVD's Description, item-17 mini-table, or Other Notes.
- **Do not editorialize beyond what the CLM and CVTs already say.** The deployment-implication framing in the Claim section is allowed; don't add new opinions in the Findings section.
- **Do not include the TRIPOD-LLM compliance assessment in the abstract.** That's the table below; the abstract is about substance, not reporting.
- **Don't use ➖ / ⚠️ / ✅ / ❌ icons in the abstract.** Those belong only in the TRIPOD-LLM table.
- **Wikilinks are mandatory.** Every EVD bullet ends with a wikilink. The Question ends with a QUE wikilink. The Claim section has CLM wikilinks. The Caveats bullets have CVT wikilinks.

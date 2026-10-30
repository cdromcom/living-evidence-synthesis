---
author: ppatel + <colleague>
page_type: index/benchmark
created: 2026-05-06
updated: 2026-05-06
generated_by: human-collaborated authoring
status: draft (rating not yet started)
vault: living-synthesis
---

# 🎯 BenchmarkLLM — accuracy audit of the discourse graph + classifications

> [!info] What this file is
> A working document for **two human raters** (you + a colleague) to benchmark how accurately the AI extracted and classified the discourse-graph nodes in this vault. You score a stratified random sample; the bottom of this file computes inter-rater agreement and per-axis accuracy.
>
> The goal is **not** to re-review every node — that's 184 nodes × ~5 rating dimensions = ~900 judgments per rater, which isn't worth it. Instead, sample ~20 per node type, score in calibration + independent rounds, and report agreement statistics that generalize.

---

## 1. What we are benchmarking

Two distinct accuracy questions with different ground truths:

**A. Node-level accuracy** — does each node faithfully represent the source paper?
- QUE: does the question quote actually frame an aim / research question of the paper?
- EVD: does the headline finding match the source PDF? Are quote, methods, screenshots accurate?
- CLM: does the claim text accurately generalize from the cited EVDs without overreach?
- CVT: is the limitation real? Does it actually constrain the linked EVD(s)?
- EP: do ≥2 independent papers' EVDs jointly support the pattern statement?

**B. Classification accuracy** — are the *tags* the AI assigned correct?
- Critical-appraisal rating per domain (🟢 / 🟡 / 🔴)
- TRIPOD-LLM compliance bucket (high / moderate / low)
- 5C dimension assignment(s)
- CVT mechanism / severity / type / domain
- Review-Arena Winner (AI / Human / Human + AI / Tie / —) — *human-authored, but worth spot-checking against the EVDs*
- Subtask wording (does the verb-first short phrase match the QUE's actual scope?)

The ground truth differs:
- **For A** — the source PDF (verbatim) is ground truth.
- **For B** — methodological consensus is ground truth (e.g., "this paper has external-validity high-risk because the sample is single-discipline" should match what a methodologist would label given the same description).

---

## 2. Sampling plan

> [!tip] Stratified random sample, not full census.
> Computing on a ~20-per-stratum sample gives reliable agreement estimates with ~10% margin of error and an order of magnitude less rater work.

| Stratum   | Vault N | Sample N | Notes                                                                       |
| --------- | :-----: | :------: | --------------------------------------------------------------------------- |
| QUE       |   27    |    10    | Half the population — small enough to oversample                            |
| CLM       |   31    |    15    | ~half                                                                       |
| EVD       |   77    |    25    | ~⅓ — stratify across the 27 papers (1 per paper, oversample big-EVD papers) |
| CVT       |   49    |    20    | ~40% — stratify by `cvt/severity` (high / moderate / low)                   |
| EP        |   21    |    10    | ~half                                                                       |
| **Total** | **184** |  **80**  |                                                                             |

For **classification accuracy** (Section B), use the SAME sample — score the tags on the nodes you've already drawn.

Sampling procedure:
1. List each stratum with `ls <folder>/*.md | sort` to get a stable order.
2. Use `numpy.random.choice(N, size=sample_N, replace=False)` with a fixed seed (`seed=42`) so both raters draw the same nodes.
3. Record the sampled filenames in [Section 7 — Sample roster](#7-sample-roster) below.

---

## 3. Protocol

### 3a. Calibration round (do together, in person)

Pick **the first 5 nodes from each stratum** (25 total). Both raters score them **together in real-time**, discussing each rating, agreeing on:
- What "🟡 some-concerns" actually looks like vs. "🔴 high-risk".
- What counts as a "match" between the EVD's headline number and the source PDF (exact match? same sig-fig? same metric type?).
- Whether the verbatim-quote check is "exact substring of the page" or "alnum-normalized substring" (the verbatim audit uses the latter — match it).

Calibration round produces shared rating definitions. **Do not include calibration ratings in the agreement statistics** — they're collaborative, not independent.

### 3b. Independent rating round

For the remaining 55 sampled nodes (80 − 25 calibration = 55), each rater scores **independently**, in any order, without consulting the other rater. Use the per-stratum rubrics in [Section 4](#4-per-node-type-rating-rubrics).

### 3c. Reconciliation round

After both raters finish independently, compare ratings on each node. For disagreements:
1. Discuss; one of you may convince the other.
2. If still disagree, mark `DISAGREE` and pick a third option: invite a tie-breaker rater, or accept the disagreement as a signal that the AI's call is genuinely ambiguous.

Reconciled ratings become the gold-standard sample. Agreement statistics computed from the **pre-reconciliation independent ratings** measure how reproducible the AI's extraction is.

---

## 4. Per-node-type rating rubrics

Each rubric returns one of `correct` / `partially correct` / `incorrect`. Use the same three-level scale across all axes for simplicity.

### 4a. QUE — does the question framing match the paper?

**Rubric:**

| Axis | `correct` | `partially correct` | `incorrect` |
| --- | --- | --- | --- |
| Quote is verbatim | exact alnum-substring of the cited page | substring with hyphenation/whitespace drift | not in the cited page |
| Quote is a question/aim/objective | clearly a research-question or aim/purpose statement | a problem-statement that frames the question | a method, finding, or claim — not a question |
| Title captures the question | a reader can paraphrase the title back to the quoted question | title overshoots or undershoots scope | title describes a different question |
| Linked papers are correct | every paper in `> [!info] Papers` actually asks the QUE | one paper is tangential | wrong papers |

**Per-node rating table** — `✓` correct · `~` partially correct · `✗` incorrect · `?` unsure (defer to reconciliation). Round: `C` = calibration (do together), `I` = independent. Fill in after sampling. Both raters write into the same row; the (A) cell is rater A, (B) is rater B.

| # | Filename | R | Vrb (A) | Vrb (B) | Aim (A) | Aim (B) | Title (A) | Title (B) | Papers (A) | Papers (B) | Notes |
| - | -------- | - | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | --- |
| 1 | `<sampled>` | C | | | | | | | | | |
| 2 | `<sampled>` | C | | | | | | | | | |
| 3 | `<sampled>` | C | | | | | | | | | |
| 4 | `<sampled>` | C | | | | | | | | | |
| 5 | `<sampled>` | C | | | | | | | | | |
| 6 | `<sampled>` | I | | | | | | | | | |
| 7 | `<sampled>` | I | | | | | | | | | |
| 8 | `<sampled>` | I | | | | | | | | | |
| 9 | `<sampled>` | I | | | | | | | | | |
| 10 | `<sampled>` | I | | | | | | | | | |

### 4b. EVD — does the finding match the source paper?

**Rubric:**

| Axis | `correct` | `partially correct` | `incorrect` |
| --- | --- | --- | --- |
| Headline number matches | exact value (or within ±0.01 if a rounding issue) | rounding error >0.01 but <5%, OR same metric different decimal | wrong value or wrong metric |
| Description quote is verbatim | exact alnum-substring | minor drift | not findable in the cited page |
| Methods Context (What/How/Who) is accurate | each block matches a real passage from the paper | one of the three blocks is approximate | one block describes a different study |
| Screenshot grounds the quote | image shows the quote highlighted | image shows the right region but highlight is misplaced | image shows wrong region or wrong page |
| Linked source paper is correct | citekey matches the file `@<citekey>.md` | — | wrong source |

**Per-node rating table** (`✓ ~ ✗ ?`; R: C=calibration, I=independent):

| # | Filename | R | Num (A) | Num (B) | Vrb (A) | Vrb (B) | Mth (A) | Mth (B) | Scrn (A) | Scrn (B) | Src (A) | Src (B) | Notes |
| -- | -------- | - | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | --- |
|  1 | `<sampled>` | C | | | | | | | | | | | |
|  2 | `<sampled>` | C | | | | | | | | | | | |
|  3 | `<sampled>` | C | | | | | | | | | | | |
|  4 | `<sampled>` | C | | | | | | | | | | | |
|  5 | `<sampled>` | C | | | | | | | | | | | |
|  6 | `<sampled>` | I | | | | | | | | | | | |
|  7 | `<sampled>` | I | | | | | | | | | | | |
|  8 | `<sampled>` | I | | | | | | | | | | | |
|  9 | `<sampled>` | I | | | | | | | | | | | |
| 10 | `<sampled>` | I | | | | | | | | | | | |
| 11 | `<sampled>` | I | | | | | | | | | | | |
| 12 | `<sampled>` | I | | | | | | | | | | | |
| 13 | `<sampled>` | I | | | | | | | | | | | |
| 14 | `<sampled>` | I | | | | | | | | | | | |
| 15 | `<sampled>` | I | | | | | | | | | | | |
| 16 | `<sampled>` | I | | | | | | | | | | | |
| 17 | `<sampled>` | I | | | | | | | | | | | |
| 18 | `<sampled>` | I | | | | | | | | | | | |
| 19 | `<sampled>` | I | | | | | | | | | | | |
| 20 | `<sampled>` | I | | | | | | | | | | | |
| 21 | `<sampled>` | I | | | | | | | | | | | |
| 22 | `<sampled>` | I | | | | | | | | | | | |
| 23 | `<sampled>` | I | | | | | | | | | | | |
| 24 | `<sampled>` | I | | | | | | | | | | | |
| 25 | `<sampled>` | I | | | | | | | | | | | |

### 4c. CLM — does the claim accurately generalize from the EVDs?

**Rubric:**

| Axis | `correct` | `partially correct` | `incorrect` |
| --- | --- | --- | --- |
| Claim accurately summarizes EVDs | every EVD's finding fits the claim's scope | claim slightly overreaches or under-reaches | claim contradicts ≥1 EVD |
| Verbatim claim quote is in source | exact substring | minor drift | not findable |
| Listed papers all make this claim | every paper genuinely advances this generalization | one paper is on-topic but doesn't make the claim | one paper makes a different claim |

**Per-node rating table** (`✓ ~ ✗ ?`):

| # | Filename | R | Sum (A) | Sum (B) | Vrb (A) | Vrb (B) | Pap (A) | Pap (B) | Notes |
| -- | -------- | - | :---: | :---: | :---: | :---: | :---: | :---: | --- |
|  1 | `<sampled>` | C | | | | | | | |
|  2 | `<sampled>` | C | | | | | | | |
|  3 | `<sampled>` | C | | | | | | | |
|  4 | `<sampled>` | C | | | | | | | |
|  5 | `<sampled>` | C | | | | | | | |
|  6 | `<sampled>` | I | | | | | | | |
|  7 | `<sampled>` | I | | | | | | | |
|  8 | `<sampled>` | I | | | | | | | |
|  9 | `<sampled>` | I | | | | | | | |
| 10 | `<sampled>` | I | | | | | | | |
| 11 | `<sampled>` | I | | | | | | | |
| 12 | `<sampled>` | I | | | | | | | |
| 13 | `<sampled>` | I | | | | | | | |
| 14 | `<sampled>` | I | | | | | | | |
| 15 | `<sampled>` | I | | | | | | | |

### 4d. CVT — is the limitation real and applicable?

**Rubric:**

| Axis | `correct` | `partially correct` | `incorrect` |
| --- | --- | --- | --- |
| Limitation is real | a methodologist would agree this is a genuine constraint | borderline / minor concern | not actually a limitation |
| Applies to the linked EVDs | the limitation specifically constrains those EVDs' inferences | applies to the paper but not specifically these EVDs | doesn't apply at all |
| `type` (author-stated vs. inferred) is correct | matches the source — author stated it OR genuinely inferred | author stated it and we tagged inferred | reversed |
| Severity is correct | low/moderate/high matches a methodologist's calibration | one tier off | two tiers off |

**Per-node rating table** (`✓ ~ ✗ ?`):

| # | Filename | R | Real (A) | Real (B) | Apply (A) | Apply (B) | Type (A) | Type (B) | Sev (A) | Sev (B) | Notes |
| -- | -------- | - | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | --- |
|  1 | `<sampled>` | C | | | | | | | | | |
|  2 | `<sampled>` | C | | | | | | | | | |
|  3 | `<sampled>` | C | | | | | | | | | |
|  4 | `<sampled>` | C | | | | | | | | | |
|  5 | `<sampled>` | C | | | | | | | | | |
|  6 | `<sampled>` | I | | | | | | | | | |
|  7 | `<sampled>` | I | | | | | | | | | |
|  8 | `<sampled>` | I | | | | | | | | | |
|  9 | `<sampled>` | I | | | | | | | | | |
| 10 | `<sampled>` | I | | | | | | | | | |
| 11 | `<sampled>` | I | | | | | | | | | |
| 12 | `<sampled>` | I | | | | | | | | | |
| 13 | `<sampled>` | I | | | | | | | | | |
| 14 | `<sampled>` | I | | | | | | | | | |
| 15 | `<sampled>` | I | | | | | | | | | |
| 16 | `<sampled>` | I | | | | | | | | | |
| 17 | `<sampled>` | I | | | | | | | | | |
| 18 | `<sampled>` | I | | | | | | | | | |
| 19 | `<sampled>` | I | | | | | | | | | |
| 20 | `<sampled>` | I | | | | | | | | | |

### 4e. EP — does the cross-paper pattern hold?

**Rubric:**

| Axis | `correct` | `partially correct` | `incorrect` |
| --- | --- | --- | --- |
| ≥2 papers actually support | every cited EVD genuinely instantiates the pattern | one EVD is tangential | most cited EVDs don't fit |
| Pattern statement is accurate | reads as the natural cross-paper generalization | overreaches | wrong direction or wrong claim |
| Connected discourse-graph nodes are real | linked CLMs / EPs all exist and relate | one stale/broken link | most links broken |

**Per-node rating table** (`✓ ~ ✗ ?`):

| # | Filename | R | Sup (A) | Sup (B) | Stmt (A) | Stmt (B) | Links (A) | Links (B) | Notes |
| -- | -------- | - | :---: | :---: | :---: | :---: | :---: | :---: | --- |
|  1 | `<sampled>` | C | | | | | | | |
|  2 | `<sampled>` | C | | | | | | | |
|  3 | `<sampled>` | C | | | | | | | |
|  4 | `<sampled>` | C | | | | | | | |
|  5 | `<sampled>` | C | | | | | | | |
|  6 | `<sampled>` | I | | | | | | | |
|  7 | `<sampled>` | I | | | | | | | |
|  8 | `<sampled>` | I | | | | | | | |
|  9 | `<sampled>` | I | | | | | | | |
| 10 | `<sampled>` | I | | | | | | | |

---

## 5. Classification accuracy rubrics (Live Database tags)

Score one row per (node, classification axis). Each axis is 3-level: `correct` / `partially correct` / `incorrect`.

### 5a. Critical appraisal (5 domains × 3 ratings)

For each EVD in the sample, the source page lists 5 domain ratings (🟢 / 🟡 / 🔴). Compare the AI's rating to your own:

| Domain | AI rating | Your rating | Match? |
| --- | --- | --- | --- |
| Construct validity | `<🟢/🟡/🔴>` | `<🟢/🟡/🔴>` | `correct / off-by-one / off-by-two` |
| Internal validity | … | … | … |
| External validity | … | … | … |
| Statistical rigor | … | … | … |
| Reproducibility | … | … | … |

`off-by-one` = e.g., AI said 🟡, you'd say 🟢 (one tier difference). Treat that as `partially correct`. `off-by-two` = AI said 🟢, you'd say 🔴 — treat as `incorrect`.

### 5b. TRIPOD-LLM compliance bucket

Per source paper, the AI assigned `high` / `moderate` / `low` based on ✅ rate over the 37-item table. Re-score 5 papers (sampled) by re-counting the icons:

| Paper | AI bucket | AI ✅ count / total non-➖ | Your re-count | Bucket match? |
| --- | --- | --- | --- | --- |

This audits the *bucket boundary* (whether ≥80% / 60-80% / <60% was applied correctly) AND the per-icon assignment.

### 5c. 5C research dimension

Per node (any type), the AI assigned ≥1 `5c/<dimension>` tag. Score against your own classification:

| Node | AI dim(s) | Your dim(s) | Set match? |
| --- | --- | --- | --- |
| `<filename>` | credibility, clarity | credibility | `partially` (you'd drop clarity) |

Use Jaccard overlap as the agreement metric (set intersection ÷ union).

### 5d. CVT classification (severity / type / domain / mechanism)

Per CVT in the sample, score four axes:

| CVT | AI severity | Your severity | AI type | Your type | AI domain | Your domain | AI mechanism(s) | Your mechanism(s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Severity uses the off-by-one / off-by-two scheme from 5a. Type, domain, and mechanism are categorical (match / no match). Mechanism is a *set* (Jaccard).

### 5e. Review-Arena Winner (per subtask)

`Review-Arena.md` has a Winner column for each subtask. Although these cells are human-authored (per the 2026-05-04 governance), spot-check 5 randomly selected rows: read the EVDs the row links to and confirm the Winner call (`AI` / `Human` / `Human + AI` / `Tie` / `—`) is supported.

| Subtask | Authored Winner | Your Winner | Match? |
| --- | --- | --- | --- |

---

## 6. Inter-rater agreement statistics

After both raters finish [Section 4](#4-per-node-type-rating-rubrics) and [Section 5](#5-classification-accuracy-rubrics-live-database-tags) independently, compute three things per axis:

1. **Percent agreement** — share of nodes where both raters gave the same 3-level rating. Easy but inflated when the modal rating is dominant.
2. **Cohen's κ** — chance-corrected agreement for two raters on a categorical scale. Interpretation: 0–0.20 slight, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect (Landis & Koch).
3. **AI accuracy** — share of nodes where the AI's assignment matches the *reconciled gold standard* (Section 3c output). This is the headline number the benchmark reports.

The Python block in [Section 8 — Computation](#8-computation) computes all three from the tables you fill in.

> [!tip] When κ disagrees with percent agreement
> A high percent agreement with low κ usually means the rare class is being missed. E.g., if 80% of CVTs are correctly labeled `low severity` but raters disagree on the few `high severity` ones, κ will be low even with high agreement. The rare-class number is the deployment-relevant one.

---

## 7. Sample roster

> [!info] Fill this in once with the seeded random draw, before either rater starts. Do not change after rating begins.

### QUE (n=10)

| # | Filename | Calibration / Independent | Rater A done | Rater B done |
| - | -------- | ------------------------- | :----------: | :----------: |
| 1 | `<>` | Calibration | ☐ | ☐ |
| 2 | `<>` | Calibration | ☐ | ☐ |
| 3 | `<>` | Calibration | ☐ | ☐ |
| 4 | `<>` | Calibration | ☐ | ☐ |
| 5 | `<>` | Calibration | ☐ | ☐ |
| 6 | `<>` | Independent | ☐ | ☐ |
| 7 | `<>` | Independent | ☐ | ☐ |
| 8 | `<>` | Independent | ☐ | ☐ |
| 9 | `<>` | Independent | ☐ | ☐ |
| 10 | `<>` | Independent | ☐ | ☐ |

### CLM (n=15)

| # | Filename | Calibration / Independent | Rater A done | Rater B done |
| - | -------- | ------------------------- | :----------: | :----------: |
| 1–5 | `<calibration>` | Calibration | ☐ | ☐ |
| 6–15 | `<independent>` | Independent | ☐ | ☐ |

### EVD (n=25)

| # | Filename | Calibration / Independent | Rater A done | Rater B done |
| - | -------- | ------------------------- | :----------: | :----------: |
| 1–5 | `<calibration>` | Calibration | ☐ | ☐ |
| 6–25 | `<independent>` | Independent | ☐ | ☐ |

### CVT (n=20)

| # | Filename | Calibration / Independent | Rater A done | Rater B done |
| - | -------- | ------------------------- | :----------: | :----------: |
| 1–5 | `<calibration>` | Calibration | ☐ | ☐ |
| 6–20 | `<independent>` | Independent | ☐ | ☐ |

### EP (n=10)

| #    | Filename        | Calibration / Independent | Rater A done | Rater B done |
| ---- | --------------- | ------------------------- | :----------: | :----------: |
| 1–5  | `<calibration>` | Calibration               |      ☐       |      ☐       |
| 6–10 | `<independent>` | Independent               |      ☐       |      ☐       |

> Run `python3 misc/scripts/sample_benchmark.py --seed 42` to fill these tables (script not yet created — see [Section 8](#8-computation)).

---

## 8. Computation

### 8a. Sampling script (run once before rating starts)

Save as `misc/scripts/sample_benchmark.py`:

```python
"""Stratified random sample of discourse-graph nodes for the BenchmarkLLM workflow."""
from pathlib import Path
import numpy as np

VAULT = Path("/Users/ppatel/Documents/living-synthesis")
STRATA = {
    "QUE": ("questions", 10),
    "CLM": ("claims", 15),
    "EVD": ("evidence", 25),
    "CVT": ("caveats", 20),
    "EP":  ("evd-patterns", 10),
}

rng = np.random.default_rng(seed=42)
for label, (folder, n) in STRATA.items():
    files = sorted(f.name for f in (VAULT / folder).glob(f"{label} - *.md"))
    if len(files) < n:
        n = len(files)
    sample = rng.choice(len(files), size=n, replace=False)
    print(f"\n=== {label} (n={n} of {len(files)}) ===")
    for i, idx in enumerate(sorted(sample), 1):
        tag = "Calibration" if i <= 5 else "Independent"
        print(f"{i:>2}. [{tag:<11}] {files[idx]}")
```

Pipe the output into [Section 7](#7-sample-roster) once. Both raters work from the same list.

### 8b. Agreement-statistics computation

Once both raters fill in their independent ratings, save the per-rater scores to a TSV (one row per node-axis pair) like:

```
node_id	axis	rater_A	rater_B
EVD-12345	headline_number	correct	correct
EVD-12345	description_quote	correct	partially
EVD-12345	methods_context	partially	incorrect
…
```

Then run:

```python
"""Compute percent agreement + Cohen's κ + AI accuracy from the rater-score TSV."""
import csv
from collections import Counter
from sklearn.metrics import cohen_kappa_score

LEVELS = ["correct", "partially correct", "incorrect"]

rows = list(csv.DictReader(open("benchmark_ratings.tsv"), delimiter="\t"))

# Group by axis
from collections import defaultdict
by_axis = defaultdict(list)
for r in rows:
    by_axis[r["axis"]].append((r["rater_A"], r["rater_B"]))

print(f"{'Axis':<32}  {'Pct agree':>10}  {'κ':>8}  {'N':>4}")
print("-" * 60)
for axis, pairs in sorted(by_axis.items()):
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    pct = sum(x == y for x, y in pairs) / len(pairs)
    kappa = cohen_kappa_score(a, b, labels=LEVELS)
    print(f"{axis:<32}  {pct:>9.0%}  {kappa:>8.2f}  {len(pairs):>4}")
```

Output template (paste below once computed):

```
Axis                              Pct agree         κ     N
------------------------------------------------------------
qu_quote_verbatim                       <%>     <κ>   <n>
qu_quote_is_aim                         <%>     <κ>   <n>
qu_title_captures_question              <%>     <κ>   <n>
…
evd_headline_number                     <%>     <κ>   <n>
evd_description_quote                   <%>     <κ>   <n>
…
classification_appraisal_construct      <%>     <κ>   <n>
classification_tripod_bucket            <%>     <κ>   <n>
classification_5c_dim                   <%>     <κ>   <n>  (Jaccard, not κ)
classification_cvt_severity             <%>     <κ>   <n>
…
```

### 8c. AI accuracy from the reconciled gold standard

After Section 3c reconciliation, you have a gold-standard rating per (node, axis). Compare the **AI's original assignment** (from the node frontmatter / source-page table) against the gold standard:

```python
# AI accuracy per axis
gold = {(r["node_id"], r["axis"]): r["reconciled"] for r in rows_gold}
ai_pred = {(r["node_id"], r["axis"]): r["ai_original"] for r in rows_gold}

correct = sum(1 for k in gold if ai_pred[k] == gold[k])
print(f"AI accuracy: {correct}/{len(gold)} = {correct/len(gold):.0%}")
```

---

## 9. Reporting template

> [!info] Fill in once Section 8 is run.

### 9a. Headline numbers

| Layer | N rated | AI accuracy | Inter-rater κ |
| --- | :---: | :---: | :---: |
| QUE node-level (Section 4a) | 10 | <%> | <κ> |
| EVD node-level (Section 4b) | 25 | <%> | <κ> |
| CLM node-level (Section 4c) | 15 | <%> | <κ> |
| CVT node-level (Section 4d) | 20 | <%> | <κ> |
| EP node-level (Section 4e) | 10 | <%> | <κ> |
| Critical appraisal (5 domains × 5 EVDs) | 25 | <%> | <κ> |
| TRIPOD-LLM bucket | 5 | <%> | <κ> |
| 5C dimension (Jaccard) | 80 | <%> | (Jaccard) |
| CVT severity | 20 | <%> | <κ> |
| CVT type | 20 | <%> | <κ> |
| CVT domain | 20 | <%> | <κ> |
| CVT mechanism (Jaccard) | 20 | <%> | (Jaccard) |
| Review-Arena Winner | 5 | <%> | <κ> |

### 9a-i. Per-node accuracy summary

For each sampled node, count axes the AI got right against the reconciled gold (from Section 3c). `Score = correct axes / total axes`. A node is "deployment-trusted" if score ≥ 0.80; "partial" if 0.50–0.79; "untrusted" if < 0.50.

**QUE per-node accuracy** (4 axes each):

| # | Filename | Vrb | Aim | Title | Pap | Score | Tier |
| -- | -------- | :-: | :-: | :-: | :-: | :---: | :--: |
|  1 | `<>` | | | | | / 4 | |
|  2 | `<>` | | | | | / 4 | |
|  3 | `<>` | | | | | / 4 | |
|  4 | `<>` | | | | | / 4 | |
|  5 | `<>` | | | | | / 4 | |
|  6 | `<>` | | | | | / 4 | |
|  7 | `<>` | | | | | / 4 | |
|  8 | `<>` | | | | | / 4 | |
|  9 | `<>` | | | | | / 4 | |
| 10 | `<>` | | | | | / 4 | |
| **Mean** | | | | | | <%> | |

**EVD per-node accuracy** (5 axes each):

| # | Filename | Num | Vrb | Mth | Scrn | Src | Score | Tier |
| -- | -------- | :-: | :-: | :-: | :-: | :-: | :---: | :--: |
|  1 | `<>` | | | | | | / 5 | |
|  2 | `<>` | | | | | | / 5 | |
|  3 | `<>` | | | | | | / 5 | |
|  4 | `<>` | | | | | | / 5 | |
|  5 | `<>` | | | | | | / 5 | |
|  6 | `<>` | | | | | | / 5 | |
|  7 | `<>` | | | | | | / 5 | |
|  8 | `<>` | | | | | | / 5 | |
|  9 | `<>` | | | | | | / 5 | |
| 10 | `<>` | | | | | | / 5 | |
| 11 | `<>` | | | | | | / 5 | |
| 12 | `<>` | | | | | | / 5 | |
| 13 | `<>` | | | | | | / 5 | |
| 14 | `<>` | | | | | | / 5 | |
| 15 | `<>` | | | | | | / 5 | |
| 16 | `<>` | | | | | | / 5 | |
| 17 | `<>` | | | | | | / 5 | |
| 18 | `<>` | | | | | | / 5 | |
| 19 | `<>` | | | | | | / 5 | |
| 20 | `<>` | | | | | | / 5 | |
| 21 | `<>` | | | | | | / 5 | |
| 22 | `<>` | | | | | | / 5 | |
| 23 | `<>` | | | | | | / 5 | |
| 24 | `<>` | | | | | | / 5 | |
| 25 | `<>` | | | | | | / 5 | |
| **Mean** | | | | | | | <%> | |

**CLM per-node accuracy** (3 axes each):

| # | Filename | Sum | Vrb | Pap | Score | Tier |
| -- | -------- | :-: | :-: | :-: | :---: | :--: |
|  1 | `<>` | | | | / 3 | |
|  2 | `<>` | | | | / 3 | |
|  3 | `<>` | | | | / 3 | |
|  4 | `<>` | | | | / 3 | |
|  5 | `<>` | | | | / 3 | |
|  6 | `<>` | | | | / 3 | |
|  7 | `<>` | | | | / 3 | |
|  8 | `<>` | | | | / 3 | |
|  9 | `<>` | | | | / 3 | |
| 10 | `<>` | | | | / 3 | |
| 11 | `<>` | | | | / 3 | |
| 12 | `<>` | | | | / 3 | |
| 13 | `<>` | | | | / 3 | |
| 14 | `<>` | | | | / 3 | |
| 15 | `<>` | | | | / 3 | |
| **Mean** | | | | | <%> | |

**CVT per-node accuracy** (4 axes each):

| # | Filename | Real | Apply | Type | Sev | Score | Tier |
| -- | -------- | :-: | :-: | :-: | :-: | :---: | :--: |
|  1 | `<>` | | | | | / 4 | |
|  2 | `<>` | | | | | / 4 | |
|  3 | `<>` | | | | | / 4 | |
|  4 | `<>` | | | | | / 4 | |
|  5 | `<>` | | | | | / 4 | |
|  6 | `<>` | | | | | / 4 | |
|  7 | `<>` | | | | | / 4 | |
|  8 | `<>` | | | | | / 4 | |
|  9 | `<>` | | | | | / 4 | |
| 10 | `<>` | | | | | / 4 | |
| 11 | `<>` | | | | | / 4 | |
| 12 | `<>` | | | | | / 4 | |
| 13 | `<>` | | | | | / 4 | |
| 14 | `<>` | | | | | / 4 | |
| 15 | `<>` | | | | | / 4 | |
| 16 | `<>` | | | | | / 4 | |
| 17 | `<>` | | | | | / 4 | |
| 18 | `<>` | | | | | / 4 | |
| 19 | `<>` | | | | | / 4 | |
| 20 | `<>` | | | | | / 4 | |
| **Mean** | | | | | | <%> | |

**EP per-node accuracy** (3 axes each):

| # | Filename | Sup | Stmt | Links | Score | Tier |
| -- | -------- | :-: | :-: | :-: | :---: | :--: |
|  1 | `<>` | | | | / 3 | |
|  2 | `<>` | | | | / 3 | |
|  3 | `<>` | | | | / 3 | |
|  4 | `<>` | | | | / 3 | |
|  5 | `<>` | | | | / 3 | |
|  6 | `<>` | | | | / 3 | |
|  7 | `<>` | | | | / 3 | |
|  8 | `<>` | | | | / 3 | |
|  9 | `<>` | | | | / 3 | |
| 10 | `<>` | | | | / 3 | |
| **Mean** | | | | | <%> | |

> Tier legend: 🟢 = ≥0.80 (deployment-trusted) · 🟡 = 0.50–0.79 (partial — flag for re-extraction) · 🔴 = <0.50 (untrusted — re-extract immediately).

### 9b. Calibration

If κ < 0.40 on any axis, the rubric is under-calibrated — re-do the calibration round for that axis.

If AI accuracy < 70% on any axis, treat the AI's assignment on that axis as **draft-quality**: don't use it for downstream filtering until corrected.

### 9c. Sources of disagreement

For each axis with κ < 0.60, list the top 2–3 patterns of disagreement (e.g., "Rater A treats 'limited diversity' as 🟡 external-validity; Rater B treats it as 🔴"). These notes feed back into the rubric refinement.

---

## 10. After benchmarking

1. **Log the headline accuracy numbers** as a phase entry in `History.md` ("Phase X — accuracy benchmark, N=80 nodes, κ=<>, AI accuracy=<>%").
2. **Update `Welcome.md` Limitations callout** with the measured AI accuracy per node type.
3. **Flag low-accuracy axes for re-extraction.** If EVD methods-context accuracy is <70%, the AI extraction on that schema needs prompt revision before processing more papers.
4. **Promote `BenchmarkLLM.md` to `ReadyForInternal`** with `human_verified: yes` once both raters have signed off.

---

## See also

- [[Welcome]] · [[Skill]] · [[Skill-references]] · [[ESS - Demo]] · [[History]]

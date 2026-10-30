---
author: Claude (Opus 4.7)
page_type: audit/redundancy
created: 2026-04-27
updated: 2026-04-27
generated_by: scripts/find_redundancies.py
prompt_source: "[[2026-04-27-redundancy-audit]]"
vault: living-synthesis
---

# Redundancy audit

> [!info] What this is
>
> Pairwise Jaccard similarity of title keyword sets within each node type. High similarity means two nodes likely cover the same topic and are candidates for merging.

> [!tip] How to read the score
>
> - **0.50+** : strong overlap; review for merging.
> - **0.30–0.49** : likely related; might merge or might be intentional siblings.
> - **0.20–0.29** : adjacent topics; usually OK as separate nodes.
> - Below 0.20 not shown.

> [!caution] Same-paper EVDs
>
> EVD pairs marked `[SAME PAPER]` come from the same source paper. They are *expected* to share keywords — the question is whether the underlying findings are distinct enough to warrant separate nodes (per the atomicity principle in SKILL.md).

---

## Questions (QUE) — 9 candidate pairs

> [!example] Strongest overlap (0.50)
>
> - [[QUE - Can LLMs identify errors in scientific papers?]]
> - [[QUE - Can reasoning LLMs identify critical errors and unsoundness problems in scientific papers?]]
>
> The reasoning-LLMs version is a refinement of the broader question. Could fold into the broader QUE with a `[!info] Subquestion: reasoning models specifically` callout — or keep both with explicit cross-link.

| Score | Question A | Question B |
| ----- | ---------- | ---------- |
| 0.50 | [[QUE - Can LLMs identify errors in scientific papers?]] | [[QUE - Can reasoning LLMs identify critical errors and unsoundness problems in scientific papers?]] |
| 0.38 | [[QUE - Can LLMs identify critical limitations within scientific research papers?]] | [[QUE - Can LLMs identify errors in scientific papers?]] |
| 0.38 | [[QUE - Can LLMs detect quotation errors in scientific papers without fine-tuning?]] | [[QUE - Can LLMs identify errors in scientific papers?]] |
| 0.36 | [[QUE - Can LLMs identify critical limitations within scientific research papers?]] | [[QUE - Can reasoning LLMs identify critical errors and unsoundness problems in scientific papers?]] |
| 0.27 | [[QUE - Can LLMs detect quotation errors in scientific papers without fine-tuning?]] | [[QUE - Can state-of-the-art LLMs reliably detect errors in published scientific manuscripts?]] |
| 0.27 | [[QUE - How do LLM-generated academic reviews compare to human reviews in quality and alignment with reviewer preferences?]] | [[QUE - How well do LLM-generated peer reviews overlap with human reviewer feedback on research papers?]] |
| 0.25 | [[QUE - How accurately can LLMs assess or understand medical research papers compared to human experts?]] | [[QUE - How accurately does ChatGPT score medical literature abstracts compared to human evaluators on reporting standards?]] |
| 0.25 | [[QUE - Can LLMs detect quotation errors in scientific papers without fine-tuning?]] | [[QUE - Can reasoning LLMs identify critical errors and unsoundness problems in scientific papers?]] |
| 0.25 | [[QUE - Can LLM-based agents simulate high-quality peer review comparable to human expert reviewers?]] | [[QUE - How well do LLM-generated peer reviews overlap with human reviewer feedback on research papers?]] |

> [!tip] Likely cluster around "errors / limitations / quotation errors in papers"
>
> Five of the nine pairs cluster on the same theme:
> - "identify errors in scientific papers"
> - "identify critical limitations within scientific research papers"
> - "detect quotation errors"
> - "reliably detect errors in published scientific manuscripts"
> - "identify critical errors and unsoundness problems"
>
> Consider consolidating into 2 distinct QUEs: one about *errors of fact / unsoundness* and one about *limitations / weaknesses*. Quotation errors could be a sub-question of either.

---

## Claims (CLM) — 1 candidate pair

| Score | Claim A | Claim B |
| ----- | ------- | ------- |
| 0.35 | [[CLM - Proprietary reasoning models substantially outperform open-source models on scientific error detection]] | [[CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]] |

> [!example] Same family of claims, different axis
>
> Both are about reasoning models on scientific error detection, but along different axes:
> - **Proprietary vs. open-source** (cost / availability frame)
> - **Reasoning vs. non-reasoning** (capability frame)
>
> If the underlying EVDs all come from the same paper(s) (Zhang-r 2025, Son 2025), they could plausibly merge with both axes called out in the body. Worth checking the supporting evidence overlap.

---

## Evidence (EVD) — 4 candidate pairs (all SAME PAPER)

These are EVDs from the same source paper that share many keywords. The atomicity principle says one finding per EVD — so the question is whether each pair represents *different findings* or whether one EVD has been split unnecessarily.

| Score | Evidence A | Evidence B | Verdict (for review) |
| ----- | ---------- | ---------- | -------------------- |
| 0.50 | [[EVD - ChatGPT achieved perfect agreement with human raters on 3 of 12 PRISMA checklist items for systematic reviews but significant discrepancy on eligibility criteria (p=0.028) - @alharbiAutomatedAssessmentReporting2024]] | [[EVD - ChatGPT achieved perfect agreement with human raters on 6 of 17 CONSORT-A RCT checklist items and significant discrepancy on randomization (p=0.001) - @alharbiAutomatedAssessmentReporting2024]] | **Distinct** — different checklists (PRISMA vs CONSORT-A), so genuinely different findings. Keep both. |
| 0.41 | [[EVD - OpenReviewer average recommendation was 5.4 matching human reviewers while GPT-4o averaged 7.7 on 400 NeurIPS and ICLR papers - @idahlOpenReviewerSpecializedLarge2025]] | [[EVD - OpenReviewer matched at least one human reviewer recommendation in 55.5% of 400 test papers vs 23.8% for GPT-4o - @idahlOpenReviewerSpecializedLarge2025]] | **Distinct** — different metrics (mean recommendation vs. exact-match rate). Keep both. |
| 0.40 | [[EVD - Human-AI collaboration achieved up to 96 percent accuracy for PRISMA and 95 percent for AMSTAR surpassing individual human raters - @woelfleBenchmarkingHumanAICollaboration2024]] | [[EVD - Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versus 89 percent for humans - @woelfleBenchmarkingHumanAICollaboration2024]] | **Distinct** — different conditions (LLM alone vs. human-AI collaboration). Keep both. |
| 0.39 | [[EVD - GPT 3.5-turbo achieved the highest correct answer rate of 66.9% on STROBE checklist questions across 39 medical articles - @akyonEvaluatingCapabilitiesGenerative2024]] | [[EVD - GPT 4-0613 achieved the lowest correct answer rate of 44.1% among all tested LLMs on STROBE questions - @akyonEvaluatingCapabilitiesGenerative2024]] | **Distinct** — different models (best vs. worst). Could optionally collapse into one EVD comparing all models, but separate is fine for atomicity. |

> [!tip] No EVDs flagged as redundant
>
> Every same-paper EVD pair represents a genuinely different finding (different metric, different model, different sub-task). The atomicity principle is being applied correctly here.

---

## Caveats (CVT) — 5 candidate pairs (low scores, all distinct)

| Score | Caveat A | Caveat B |
| ----- | -------- | -------- |
| 0.26 | [[CVT - The OpenReviewer training and test data were limited to ICLR and NeurIPS conferences limiting domain generalizability]] | [[CVT - The novelty prediction dataset was limited to ICLR machine learning conference papers restricting generalizability to other academic domains]] |
| 0.20 | [[CVT - The Thelwall dataset consisted of 51 articles by a single author limiting generalizability to other researchers and fields]] | [[CVT - The quotation error dataset was predominantly from natural science journal articles limiting generalizability to conference papers and other publication channels]] |
| 0.20 | [[CVT - Study used only three AI platforms evaluated on ten case studies limiting generalizability of IRB capability findings]] | [[CVT - The study used only sports medicine and orthopaedic journal papers limiting generalizability to other medical fields]] |
| 0.20 | [[CVT - SPOT benchmark comprised only 83 manuscripts with 91 errors limiting statistical power]] | [[CVT - The LimitGen benchmark focused only on AI research limiting applicability to other scientific domains]] |
| 0.20 | [[CVT - Most LLMs were text-only and blind to figures and image-rendered tables relevant for evidence appraisal]] | [[CVT - Sarol et al. excluded citation cases where evidence appeared in tables figures or supplementary material]] |

> [!tip] All distinct, share only generic phrasing
>
> All five CVT pairs share only the generic phrase "limiting generalizability" or similar — they're about different papers, different limitations, different scope. The CVTs are paper-specific and atomic; the keyword overlap is a phrasing artifact, not a content overlap.
>
> The CVT vocabulary could be normalized (e.g., always say "narrow domain" instead of mixing "limited to ICLR" / "limited to AI research") so the redundancy detector doesn't flag generic-phrase pairs.

---

## Summary

| Type | Pairs flagged | Likely actions |
| ---- | ------------- | -------------- |
| QUE | 9 | **Genuine consolidation candidate.** Cluster of 5 QUEs around "errors/limitations in scientific papers" could collapse to 2. |
| CLM | 1 | One pair worth reviewing — both about reasoning models on error detection along different axes. |
| EVD | 4 | All same-paper but represent genuinely different findings. **No action needed.** |
| CVT | 5 | All paper-specific and distinct. Phrasing-only overlap. **No action needed**, optionally normalize vocabulary. |

> [!caution] What this audit does NOT detect
>
> - Semantic redundancy where the wording is different but the meaning is the same (e.g., synonyms not in the synonym table).
> - Cross-type overlaps (e.g., a CLM that should really be an EVD because it's a specific finding, not a generalization).
> - Stale nodes whose findings have been superseded by later evidence in the vault.
>
> A human read-through is still the best way to catch these.

---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L2-M2-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/73pct
  - 5c/connectivity
  - forensic/kappa-check/in-bounds
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b75-77f2-8f5f-2ee25d43c902
appraisal_overall: L2-M2-H1
tripod_llm_pct: 73pct
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

## Description

> "Agreement was lower on evidence sentence and accuracy label annotations, although the agreement improved in the second phase to fair agreement levels (evidence sentence: 0.20 in the first phase to 0.37 in the second; accuracy labels: 0.18–0.31)." (Sarol et al., 2024, p. 5)
> ![[sarolAssessingCitationIntegrity2024-evd-p5-4.png]]

## Methods Context

### What?

> **Study design:** inter-annotator reliability sub-study nested within the Sarol corpus annotation. **Method type:** pairwise Cohen's kappa (κ) averaged across all annotator pairs, computed at the **sentence level** for all three annotation tasks. **Tools:** Cohen's κ; brat annotation export. **Dependent variable:** pairwise κ for each task. **Independent variables:** task type (citation-context identification / evidence-sentence identification / citation-accuracy classification); annotation phase (1 vs. 2); the eight-class label scheme used during IAA.
>
> "We calculated pairwise inter-annotator agreement for each task: citation context identification, evidence segment identification, and citation accuracy classification. The first 30 reference articles (phases one and two) were included in calculation. Cohen's kappa (κ) was used for all tasks, and the average pairwise agreement between annotators was calculated. For citation context and evidence segment identification, agreement was calculated at the sentence level. If an evidence segment annotation was at the paragraph or section level, all sentences in the paragraph/section are included as evidence sentences." (Sarol et al., 2024, p. 4)
> ![[sarolAssessingCitationIntegrity2024-evd-p3-3.png]]

### How?

> **Procedure:** restrict to phases 1+2 (first 30 reference articles, where each citation has ≥ 2 independent annotations from different annotators). For each annotator pair that overlapped on a reference article, compute Cohen's κ at the sentence level for each of the three tasks; average across all such pairs to produce one κ per task per phase. For paragraph- or section-level evidence annotations, all constituent sentences are treated as evidence sentences before agreement is computed (so paragraph-level annotations are not penalized for being coarse). After phase 2, annotation guidelines were revised based on observed disagreements before phase 3 began.
>
> "Cohen's kappa (κ) was used for all tasks, and the average pairwise agreement between annotators was calculated. For citation context and evidence segment identification, agreement was calculated at the sentence level. If an evidence segment annotation was at the paragraph or section level, all sentences in the paragraph/section are included as evidence sentences." (Sarol et al., 2024, p. 4)
> ![[sarolAssessingCitationIntegrity2024-evd-p4-4.png]]

### Who?

> **Annotators:** **5 annotators** — graduate and undergraduate students in life sciences, with prior experience reading life-sciences papers; recruited specifically for this project. Investigators contributed during phase 1 reconciliation but their annotations are not part of the IAA pool.
>
> **Reference articles (sample-size flow):** 100 PMC-OA reference articles total → IAA computed only on the **first 30** (phase 1 + phase 2). Phase 1 = the same 10 articles annotated by **all 5** annotators (5-way overlap). Phase 2 = 20 articles annotated in **annotator pairs** (each annotator paired with each of the other four on 2 articles, so each phase-2 article had 2 overlapping annotators).
>
> "five annotators were involved in the annotation process. Annotators were graduate and undergraduate students in life sciences with experience in reading life sciences papers." (Sarol et al., 2024, p. 3)
> ![[sarolAssessingCitationIntegrity2024-evd-p3-4.png]]

## Other Notes

- Citation-context identification κ was high (0.96), but largely by design: citances are automatically included as citation context, so most agreement is trivially structural.
- Authors flag the IAA as "lower than desired" but contextualize against analogous citation-linking datasets (Li et al. 2023) which report IAA in the range 0.16–0.52, so the Sarol corpus sits in the middle of that range.
- Inter-annotator disagreement was concentrated on hard distinctions (e.g., OVERSIMPLIFY vs. NOT_SUBSTANTIATE — related categories differing only in severity). The category-priority rule and a final single-annotator review were designed to dampen this in the released corpus, but training/eval splits still inherit residual label noise.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sarolAssessingCitationIntegrity2024#TRIPOD-LLM reporting summary]].

| Task | Phase 1 κ | Phase 2 κ |
| --- | :---: | :---: |
| Citation-context identification | 0.96 | 0.96 |
| Evidence-sentence identification | **0.20** | **0.37** |
| Citation-accuracy classification (8-way) | **0.18–0.31** | **0.18–0.31** |

| Benchmark | Range |
| --- | --- |
| Comparable citation-linking corpora (Li et al. 2023) | κ = 0.16–0.52 |
| Authors' qualitative assessment | "fair" agreement; "lower than desired" |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Low inter-annotator agreement on citation accuracy labels limited quality of training and evaluation data]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Inter-rater agreement on subjective scientific-judgment tasks is low for both humans and LLMs]]

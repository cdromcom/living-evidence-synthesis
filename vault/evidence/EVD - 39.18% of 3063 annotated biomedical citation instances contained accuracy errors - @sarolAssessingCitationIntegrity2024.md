---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/citation-integrity-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L2-M2-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/73pct
  - 5c/connectivity
  - forensic/closure-check/consistent
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b4f-7657-91eb-6e0893973052
appraisal_overall: L2-M2-H1
tripod_llm_pct: 73pct
---

## Source

[[@sarolAssessingCitationIntegrity2024]]

## Description

> "A total of 3063 citation instances corresponding 3420 citation context sentences and 3791 evidence sentences were annotated (1.12 context and 1.24 evidence sentences per citation). The majority of citations were deemed accurate (60.82%). There were slightly more minor errors than major errors (21.16% versus 18.02%)." (Sarol et al., 2024, p. 5)
> ![[sarolAssessingCitationIntegrity2024-evd-p5-1.png]]
>
> Grounding table (Table 1, p. 5): per-label counts and percentages broken down into MAJOR (CONTRADICT, NOT_SUBSTANTIATE, IRRELEVANT) and MINOR (MISQUOTE, OVERSIMPLIFY, INDIRECT, ETIQUETTE) errors.
>
> ![[sarolAssessingCitationIntegrity2024-tables-p5-5.png]]

## Methods Context

### What?

> **Study design:** descriptive corpus-annotation study (cross-sectional).
>
> **Method type:** manual annotation of citation-accuracy labels with multi-phase reconciliation.
>
> **Tools:** brat annotation tool (Stenetorp et al. 2012); custom 8-label citation-accuracy scheme adapted from Luo et al. (2013) and Jergas & Baethge (2015).
>
> **Dependent variable:** per-citation accuracy label (8 fine-grained classes, ACCURATE plus 3 MAJOR + 4 MINOR error types, and the collapsed MAJOR/MINOR groupings).
>
> **Independent variables / covariates:** reference-article type (primary research vs. review); error severity (major vs. minor).
>
> "Our citation accuracy classification is based on and extends prior quotation error classifications (Luo et al. 2013, Jergas and Baethge 2015). These schemes distinguish major and minor errors, and provide further subcategories. In our classification, CONTRADICT, IRRELEVANT, and NOT_SUBSTANTIATE are major error categories and OVERSIMPLIFY, MISQUOTE, and INDIRECT minor error categories. In this work, we propose an additional minor error category, ETIQUETTE, and extend the definition of INDIRECT." (Sarol et al., 2024, p. 3)
> ![[sarolAssessingCitationIntegrity2024-evd-p3-1.png]]

### How?

> **Procedure:** three-phase annotation. *Phase 1*, all 5 annotators independently labeled citations to the **same 10 reference articles**, with one article fully reconciled by all annotators + investigators and the other 9 reconciled in three pair groups. *Phase 2*, each annotator labeled citations to **8 articles** (paired with each of the other four annotators on 2 articles, 20 articles total); each pair then reconciled. *Phase 3*, each annotator individually annotated citations to **14 articles** (70 articles total), and each annotator's set was reviewed and corrected by another annotator. Final pass by a single annotator for cross-corpus consistency. Annotators were given the citing paragraph (with the citation marker pre-highlighted) plus the full text of the reference article and could mark up to 5 evidence segments per citation. Category-priority rule: when a citation matched multiple error types, the higher-priority error was selected.
>
> "In the first annotation phase, all 5 annotators annotated citations to the same 10 reference articles… In the second phase, each annotator labeled citations to eight articles. They paired with each of the other four annotators for two articles, for a total of 20 articles… In the third phase, each annotator individually annotated citations to 14 articles, for a total of 70 articles. After the third phase was completed, each annotator reviewed and corrected the annotations of another annotator, so each citation in this set was also double-checked. Finally, one of the annotators performed a final review to ensure consistent annotations." (Sarol et al., 2024, p. 3)
> ![[sarolAssessingCitationIntegrity2024-evd-p3-2.png]]

### Who?

> **Participants / data:** no human subjects. The annotated units are scientific citations.
>
> **Reference articles (sample-size flow):** PubMed disease-targeted searches (e.g., diabetes, COVID-19) → restricted to PMC-OA full text → ranked by citation count via OpCitance (Hsiao & Torvik 2023) → screened by one author for topic / article-type / study-design diversity → **100 highly-cited reference articles retained**.
>
> **Citing articles:** for each reference article, citing PMC-OA articles were sorted by number of citations to the reference (proxy for citation significance) and a subset citing it multiple times was randomly sampled.
>
> **Annotated units (final):** 3063 citation instances → 3420 citation-context sentences + 3791 evidence sentences (means: 1.12 context, 1.24 evidence per citation). Median 27 citations per reference article (range 11–74; IQR 8.25); median 22 citing articles per reference (range 5–29; IQR 6).
>
> **Annotators:** 5 graduate and undergraduate life-sciences students.
>
> "We collected 100 highly-cited research articles available in full text from the PubMed Central Open Access Subset (PMC-OA) to form our reference article set." (Sarol et al., 2024, p. 2)
> ![[sarolAssessingCitationIntegrity2024-evd-p2-1.png]]

## Other Notes

- Per paper: average of 0.37 errors per review article vs. 0.40 per original paper (Student's t-test, p=.095, n.s.). Average number of distinct error types per paper was 0.52 (review) and 0.54 (original), each ranging 0–4.
- Difference in occurrence of minor vs. major errors per paper was statistically significant (Student's t-test, p=.0085).

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@sarolAssessingCitationIntegrity2024#TRIPOD-LLM reporting summary]].

| Outcome | Value |
| --- | --- |
| ACCURATE | 60.82% (n=1863) |
| **Errors (total)** | **39.18% (n=1200)** |
| MAJOR errors | 18.02% (552): CONTRADICT 3.00% (92); NOT_SUBSTANTIATE 7.93% (243); IRRELEVANT 7.08% (217) |
| MINOR errors | 21.16% (648): MISQUOTE 1.24% (38); OVERSIMPLIFY 3.62% (111); INDIRECT 2.68% (82); ETIQUETTE 13.61% (417) |
| Minor vs. major (per paper) | Student's t-test p=.0085 (significant) |
| Review vs. original (per paper) | 0.37 vs. 0.40 errors/paper, t-test p=.095 (n.s.) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Sarol et al. excluded citation cases where evidence appeared in tables figures or supplementary material]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Citation quotation errors are subtle and currently challenging for NLP models to identify automatically]]

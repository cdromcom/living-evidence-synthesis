---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/reporting-compliance-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/high-risk
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/43pct
  - 5c/clarity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b7b-76f9-ab59-4f33dcf0757b
appraisal_overall: L0-M2-H3
tripod_llm_pct: 43pct
---

## Source

[[@akyonEvaluatingCapabilitiesGenerative2024]]

## Description

> "When all LLMs are collectively considered, the three questions receiving the highest percentage of correct answers were Q12 (68.31%), Q13 (62.77%), and Q10 (60.52%). Conversely, the three questions with the lowest percentage of correct responses were Q8 (33.52%), Q15 (35.81%), and Q1 (36.48%)." (Akyon et al., 2024, p. 16)
>
> ![[akyon2024-fig3-p19-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark, item-level aggregate analysis (mean correct % across all 6 LLMs per STROBE question).
>
> **Method type:** descriptive aggregation of per-question accuracy from a 6-LLM × 15-question × 39-article × 10-trial RAG benchmark, with per-question Kruskal-Wallis tests across LLMs.
>
> **Tools:** same RAG web app + 6 commercial LLMs as the sibling EVDs; Figure 3 (per-Q correct % across all LLMs) and Table 4 (per-Q × per-LLM medians + Kruskal-Wallis P) reported in Multimedia Appendix 2; SPSS 29.0.
>
> **Dependent variable:** mean percentage of correct answers per STROBE question (Q1–Q15) aggregated across all 6 LLMs.
>
> **Independent variable:** STROBE question identity (Q1=study design in title/abstract; Q8=statistical software used [7 options]; Q10=flowchart used; Q12=discussion summarizes key results; Q13=limitations discussed; Q15=funding source [2 options]).
>
> "When all LLMs are collectively considered, the three questions receiving the highest percentage of correct answers were Q12 (68.31%), Q13 (62.77%), and Q10 (60.52%). Conversely, the three questions with the lowest percentage of correct responses were Q8 (33.52%), Q15 (35.81%), and Q1 (36.48%)." (Akyon et al., 2024, p. 14)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p14-3.png]]

### How?

> **Procedure:** for each LLM and each of the 15 STROBE questions, the RAG pipeline returned 10 responses per article × 39 articles = 390 per LLM-question cell (330 for Claude v1). Responses were graded against the medical-professor gold standard; only exact-match, instruction-following responses counted as correct. Per-question accuracy was averaged across all 6 LLMs to produce the Figure 3 bar chart with error bars; per-question medians per LLM (with min–max) were tabulated in Table 4 and tested with Kruskal-Wallis (Q1 P=.011; Q3, Q4, Q5, Q11, Q12, Q13, Q15 all P<.001; Q6 P=.001; Q2 P=.028; Q7, Q8, Q9, Q10, Q14 not significant).
>
> "The percentages of correct answers given by all LLMs for each question are depicted in Table 4. The median values for questions 7, 8, 9, 10, and 14 were similar across all LLMs, indicating a general consistency in performance for these specific areas of comprehension. However, significant differences were observed in the performance of different LLMs for other questions. The statistical tests used in this analysis were the Kruskal-Wallis test for comparing the medians of multiple groups and the chi-square test for comparing categorical data." (Akyon et al., 2024, p. 15)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p15-1.png]]

### Who?

> **Models:** all 6 commercial LLMs aggregated, GPT 3.5-Turbo-1106, GPT 4-0613, GPT 4-1106, Claude v1, Palm 2/chat-bison, Gemini pro 1.0.
>
> **Articles:** 39 PubMed observational obesity studies (selection: 2996 PubMed hits → 303 after filters → first 50 → 39 after excluding 11 non-observational; Claude v1 capped at 33).
>
> **Per-question denominator:** 6 LLMs × 39 articles × 10 trials = ~2340 graded responses per STROBE question (somewhat lower for items where Claude v1 contributed only 33 articles).
>
> **Reference standard:** 1 medical professor (pediatric gastroenterology) authored gold answers; 1 epidemiologist (Dr. Hilal Duzel) verified them.
>
> "In this study, 15 questions selected from the STROBE checklists were posed 10 times each for 39 articles to six different LLMs." (Akyon et al., 2024, p. 12)
> ![[akyonEvaluatingCapabilitiesGenerative2024-evd-p12-3.png]]

## Other Notes

Q8 (statistical software identification) and Q15 (funding) were multiple-choice questions with 7 and 2 options respectively, which may explain the lower performance. Q12 and Q13 (discussion sections) showed highest accuracy, suggesting LLMs are better at summarizing interpretive content than extracting specific technical details.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@akyonEvaluatingCapabilitiesGenerative2024#TRIPOD-LLM reporting summary]].

Per-question correct % across all 6 LLMs (from Figure 3 / Table 4):

| STROBE Q | Topic | Correct % (all LLMs) | Kruskal-Wallis P (across LLMs) |
| --- | --- | :---: | :---: |
| **Q12** | Discussion summarises key results | **68.31%** | <.001 |
| Q13 | Limitations discussed | 62.77% | <.001 |
| Q10 | Flowchart used | 60.52% | .625 (n.s.) |
| Q5 | Eligibility criteria | 57.12% | <.001 |
| Q11 | Demographic characteristics | 56.93% | <.001 |
| Q6 | Sources/methods of selection | 53.33% | .001 |
| Q2 | Observational study type | 51.99% | .028 |
| Q3 | Settings/locations | 50.22% | <.001 |
| Q4 | Relevant dates | 46.22% | <.001 |
| Q14 | Generalisability | 43.78% | .151 (n.s.) |
| Q7 | Bias addressed | 43.00% | .553 (n.s.) |
| Q9 | Numbers per study stage | 38.95% | .053 (n.s.) |
| Q1 | Study design in title/abstract | **36.48%** | .011 |
| Q15 | Funding mentioned | **35.81%** | <.001 |
| **Q8** | Statistical software used | **33.52%** | .351 (n.s.) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]

- [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]

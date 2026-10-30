# Screening data: LLM-assisted research evaluation systematic review

`elicit-sysrev-r2-screening-results.csv` holds the round-2 title-and-abstract screening for the systematic review behind this site. The question is how accurately and efficiently large language models evaluate research reports compared with human experts.

- **Records:** 1,000 studies (2023–2026). The file has more lines than records because abstracts and reasoning fields contain line breaks; read it with a CSV parser.
- **Screening tool:** [Elicit](https://elicit.com), which scored each record against seven criteria and wrote a short justification for each judgment.
- **Outcome:** 749 included, 251 excluded (all 251 with the reason "Other / below screening threshold").
- **Exported:** June 3, 2026.
- **Status:** these are machine-assisted screening judgments. They have not all been checked by a human reviewer, so treat them as a starting point rather than final inclusion decisions.

## Columns

| Column | Contents |
|---|---|
| `Title`, `Abstract`, `Authors`, `Venue`, `Year` | Bibliographic metadata |
| `DOI`, `DOI link` | Identifier and resolver link (missing for 67 records) |
| `Citation count` | Citation count at export time |
| `Empirical Study Design` | Is the study empirical? (`yes` / `maybe` / `no`) |
| `Expert Human Evaluators` | Does it involve expert human evaluators? |
| `Independent LLM Evaluation` | Does an LLM evaluate research independently? |
| `LLM Evaluation with Human Expert Comparison` | Are LLM evaluations compared with human experts? |
| `Original Empirical Data` | Does it report original data? |
| `Quantitative Outcomes` | Does it report quantitative outcomes? |
| `Research Content Focus` | Is the evaluated material research content (papers, proposals, reviews)? |
| `Reasoning for "…"` | The screening tool's justification for each criterion above |
| `Screening judgement` | `Include` or `Exclude` |
| `Reasoning for "Screening judgement"` | Justification for the overall judgment |
| `Screening score` | Overall score from 0.1 to 4.9 |
| `Excluded by strict criterion` | Empty in this export |
| `Exclusion reason` | Reason for exclusion, where applicable |

## Reuse

Titles, abstracts, and author lists belong to the original publications and are included only to make the screening reproducible. The screening judgments and reasoning may be reused with attribution to the repository.

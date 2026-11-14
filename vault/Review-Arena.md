---
author: Claude + ppatel
page_type: index/topic-list
created: 2026-04-29
updated: 2026-05-04
generated_by: scripts/build_topics.py (inline, Phase 27)
prompt_source: "[[2026-04-29-topic-list]]"
vault: living-synthesis
cssclasses:
  - wide-tables
---

# 📚 Subtasks — Who wins: AI, Human, or Human + AI

> [!info] What this page is
>
> A leaderboard view of the corpus framed as a head-to-head: for each research **Subtask**, show what an **AI alone** scored, what a **Human alone** scored, what a **Human + AI** team scored, who won, and the **Effect size** (the delta between the leading and reference paradigms). Each AI / Human / Human + AI cell shows the headline number with a one-word metric label; **hover** for the full model + technique + sample. Click **Details** for the canonical methods write-up. "—" means the paradigm was not tested in the underlying study.
>
> **Winner** is one of: **AI**, **Human**, **Human + AI**, **Tie** (parity), or "—" (not adjudicable). Calls reflect the paper's *headline* result on its *primary metric*.
>
> **Effect size** is the magnitude of the headline contrast, in the paper's own metric (pp = percentage points; F1 / κ / r as raw deltas). A green value means the leading paradigm beats the reference; red means it falls short; gray means parity or qualitative.
>
> **Evidence Strength** combines: number of papers contributing the question, number of triangulating cross-paper [[ESS|EvidencePatterns]], and number of supporting claims. **Strong** = ≥3 papers + ≥3 EPs · **Moderate** = 2 papers OR strong evidence from one paper · **Limited** = single-paper finding.

**Coverage:** 27 subtasks · 27 source papers · 21 cross-paper [[ESS|EvidencePatterns]] · all rows traced to specific [[CLM|claim]] and [[EVD|evidence]] nodes.

![[Live database]]

> [!tip] How to read these tables
> **Hover** any Subtask cell for a preview. **Click** a Subtask name to drill into the full question page (claims, supporting EVDs, caveats).
> 
> Sortable headers and a per-table filter input are available **only in the public web view** — they're powered by JS that doesn't run inside Obsidian. To get sort + filter inside Obsidian, install a community plugin such as [`Sortable`](https://github.com/alexandru-dinu/obsidian-sortable) or [`Dataview`](https://github.com/blacksmithgu/obsidian-dataview) (Dataview would also need the tables rebuilt as DQL queries).

## 🔎 Live database

> [!info] Filter the underlying corpus
> The live Bases view below ([defined in `ESS.base`](ESS.base)) lets you filter the 184 discourse-graph nodes feeding these leaderboards by node type, 5C dimension, TRIPOD-LLM bucket, critical-appraisal domain, CVT severity, or workflow status. Click any tab. Same data source as [[ESS - Demo]].

![[ESS.base]]

---

## 🧑‍⚖️ Peer review reports

| Subtask                                                                                                                                                                                                  | 🤖 AI score | 🧑 Human score | Human-AI score | Winner | Effect size | Evidence Strength |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------: | :------------: | :------------: | :----: | :---------: | :---------------: |
| [[QUE - How much do LLM reviews overlap with human feedback\|Match human peer reviews]] <small>· 31 EVDs</small>                                             |             |                |                |        |             |                   |
| [[QUE - Can LLMs do expert-level AI research tasks\|Perform expert AI-research tasks]] <small>· 26 EVDs</small> |             |                |                |        |             |                   |
| [[QUE - Can LLM agents simulate expert-quality peer review\|Generate human-quality reviews]] <small>· 26 EVDs</small>                                          |             |                |                |        |             |                   |
| [[QUE - Do fine-tuned LLMs write more critical and realistic reviews than general LLMs\|Reduce overly-positive reviews]] <small>· 26 EVDs</small>                           |             |                |                |        |             |                   |
| [[QUE - How do LLM reviews compare to human reviews in quality and alignment\|Match reviewer preferences]] <small>· 26 EVDs</small>                        |             |                |                |        |             |                   |
| [[QUE - Is LLM a reliable reviewer for automatic paper reviewing\|Answer reviewer-MCQ questions]] <small>· 26 EVDs</small>                                                                        |             |                |                |        |             |                   |
| [[QUE - Can multi-agent LLMs give more specific paper feedback\|Boost multi-agent feedback specificity]] <small>· 24 EVDs</small>                             |             |                |                |        |             |                   |

## 📋 Check  reporting guideline compliance

| Subtask                                                                                                                                                                                                | 🤖 AI score | 🧑 Human score | Human-AI score | Winner  | Effect size | Evidence Strength |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------: | :------------: | :------------: | :-----: | :---------: | :---------------: |
| [[QUE - How accurately can LLMs assess medical papers versus experts\|Evaluate medical papers]] <small>· 23 EVDs</small>                                            |             |                |                |         |             |                   |
| [[QUE - Can LLMs verify author checklists in submissions\|Verify author checklists]] <small>· 29 EVDs</small>                                                                           |             |                |                |         |             |                   |
| [[QUE - How does LLM performance vary across evidence appraisal tasks\|Perform systematic-review sub-tasks]] <small>· 26 EVDs</small>          |             |                |                |         |             |                   |
| [[QUE - Can LLMs replace or augment raters on PRISMA AMSTAR PRECIS-2\|Conduct PRISMA / AMSTAR appraisal]] <small>· 28 EVDs</small>                           |             |                |                |         |             |                   |
| [[QUE - How accurately can LLMs measure trial reporting compliance\|Score CONSORT compliance]] <small>· 17 EVDs</small>                                                 |             |                |                |         |             |                   |
| [[QUE - How has CONSORT reporting changed and can LLMs assess it\|Track decade-scale CONSORT trends]] <small>· 10 EVDs</small> |             |                |                |         |             |                   |
| [[QUE - How accurately does ChatGPT score abstract reporting quality\|Score abstract reporting]] <small>· 4 EVDs</small>                        |             |                |                |         |             |                   |
| [[QUE - What input format works best for LLM quality assessment\|Choose optimal input format]] <small>· 5 EVDs</small>                                                             |             |                |                |         |             |                   |

## 🐞 Detect errors / limitations / quality issues

| Subtask                                                                                                                                                          | 🤖 AI score | 🧑 Human score | Human-AI score | Winner  | Effect size | Evidence Strength |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------: | :------------: | :------------: | :-----: | :---------: | :---------------: |
| [[QUE - Can LLMs identify errors in scientific papers\|Detect errors in papers]] <small>· 21 EVDs</small>                                                       |             |                |                |         |             |                   |
| [[QUE - Can LLMs detect quotation errors without fine-tuning\|Catch quotation errors]] <small>· 21 EVDs</small>                            |             |                |                |         |             |                   |
| [[QUE - Can LLMs identify critical limitations in papers\|Spot research limitations]] <small>· 21 EVDs</small>                          |             |                |                |         |             |                   |
| [[QUE - Can reasoning LLMs find critical errors in papers\|Detect retraction-comment errors]] <small>· 22 EVDs</small>  |             |                |                |         |             |                   |
| [[QUE - Can SOTA LLMs reliably detect errors in published papers\|Detect errors in published manuscripts]] <small>· 21 EVDs</small> |             |                |                |         |             |                   |
| [[QUE - Can LLMs pick the better of two abstracts\|Pick the better abstract]] <small>· 20 EVDs</small>                              |             |                |                |         |             |                   |
| [[QUE - Can NLP models find citation errors in biomedical papers\|Catch citation-integrity errors]] <small>· 17 EVDs</small>  |             |                |                |         |             |                   |

## 💡 Assess novelty

| Subtask                                                                                                                                                                        | 🤖 AI score | 🧑 Human score | Human-AI score | Winner  | Effect size | Evidence Strength |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------: | :------------: | :------------: | :-----: | :---------: | :---------------: |
| [[QUE - Can integrating LLM and reviewer knowledge improve novelty prediction\|Predict paper novelty]] <small>· 22 EVDs</small> |             |                |                |         |             |                   |
| [[QUE - Can a RAG system reliably judge idea novelty like experts\|Judge idea novelty]] <small>· 11 EVDs</small>              |             |                |                |         |             |                   |

## 🩺  Assess ethical matters

| Subtask                                                                                                                                                                           | 🤖 AI score | 🧑 Human score | Human-AI score | Winner  | Effect size | Evidence Strength |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------: | :------------: | :------------: | :-----: | :---------: | :---------------: |
| [[QUE - Can AI platforms emulate IRB decisions and draft SOPs\|Emulate IRB decisions]] <small>· 26 EVDs</small>         |             |                |                |         |             |                   |
| [[QUE - Can LLMs flag potential ethics issues and draft informed consent\|Flag ethics, draft consent]] <small>· 11 EVDs</small> |             |                |                |         |             |                   |

## 🔗 Causal inference

| Subtask                                                                                                                                                           | 🤖 AI score | 🧑 Human score | Human-AI score | Winner  | Effect size | Evidence Strength |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------: | :------------: | :------------: | :-----: | :---------: | :---------------: |
| [[QUE - Can LLMs supply causal knowledge to select confounders\|Pick correct confounders]] <small>· 2 EVDs</small> |             |                |                |         |             |                   |



> [!HELP] Contributors Needs
> Human experts are, we think, ideal for merging related questions (column: subtask) and also synthesizing the Evidence Patterns (EPs) into tables accurately. 
> 
> If you would like to contribute to this effort for authorship and experience, volunteer today!


## See also

- [[Welcome]] · [[DGRAPH]] · [[DGRAPH-TABLE]] · [[ESS]] · [[Skill]]

---
type: prompt
id: picost-v7
used_by: pipeline/scripts/lives_run.py (stage picost; model gemini-4-neon)
written: 2026-11-25
changes: v7 (2026-11-26, JP): every number written in a finding statement must have its own entry in `numbers` with its location; the spans stage now flags statements that break this. v6 (2026-11-25, JP) has no cap on questions or findings: list every question stated in the Abstract and Introduction (repeats inside a paper are useful, keep them) and every finding, each accurate and traceable. v5 limited questions to 3. v4 (2026-11-25) has the model find the paper's own questions (QUEs) and reframe them as clear, granular questions; tiers and links are defined against those questions, not a supplied RQ. v3 added the research question and three evidence tiers (primary, secondary, tertiary) with a cap per tier; v2 capped the findings at 12; v1 returned 29 findings for a 10-page paper (37,000 output tokens); v2 caps the findings, because the 27 seed papers have 1 to 6 EVDs each (median 3)
---

You extract questions, findings, claims and caveats from one research paper (the attached PDF) for a living evidence synthesis about LLMs in scientific research and peer review. Work only from the PDF. Return one JSON object and nothing else.

## Step 1: the paper's questions (QUEs), from the Abstract and Introduction only
A paper states what it asks in its Abstract and Introduction: as questions ("RQ1: ..."), hypotheses, aims, goals, objectives or "we investigate whether..." sentences. Do not take questions from the Methods, Results or Discussion.
- List every question the Abstract and Introduction state, even when two of them say nearly the same thing (for example once in the Abstract and again in the Introduction): give each its own entry with its own `section` and page. Never invent one.
- For each give `original_wording` copied exactly, `kind` (question, aim, goal, hypothesis or statement), `section` (Abstract or Introduction) and the page.
- Then write `reframed`: one clear question in everyday words that findings can link to. One capability per question; split a compound aim only if the paper itself treats the parts separately. Prefer the canonical phrasings when one fits ("How well can LLMs identify errors in research reports?", "How accurately can LLMs evaluate research reports' alignment with reporting guidelines?", "How well can LLMs review research reports?", "How accurately can LLMs evaluate research reports' methodological rigor using critical appraisal tools?", "How well can LLMs evaluate the novelty of research reports?", "How do LLM-generated peer reviews compare to human-generated peer reviews in quality?"). Name the capability, not the method.
- If the Abstract and Introduction state no question, infer the one the study's purpose sentence implies and set `kind` to `inferred`.
- A review-level question may be given as context. The paper's own questions come first.

Be brief. Keep every statement to one or two sentences and every note to one sentence. No text outside the JSON.

## Rules
1. **One record per finding, in three tiers.** A finding is one statistical test, one empirical observation or one analytical result. Do not merge findings. Classify every finding against the paper's questions from Step 1:
   - **primary**: it answers at least one of the paper's questions directly (for example, the performance of an LLM on the task a question asks about, against its comparator). Name the question ids in `answers_QUE`.
   - **secondary**: it is meta or contextual information about a primary finding and helps a reader interpret, qualify or trust it (for example, agreement among the human raters, dataset or sample properties, sensitivity to prompts or settings, failure analyses, cost, or a quantified limitation). Name the primary finding or findings it supports in `supports`.
   - **tertiary**: other context that may matter (descriptive statistics of the corpus, exploratory subgroup results, side findings).
   Give a one-line `tier_reason` for every finding. There is no limit on how many findings you list: list every finding the paper reports, but each one must be accurate and traceable (a locator and a verbatim span). Do not pad, and do not silently drop findings.
2. **PICOST.** For each finding give Population, Intervention, Comparator, Outcome, Study design and Timeframe. Anything the paper does not state is the string `Not reported`. Never fill a slot with plausible standard detail.
3. **Numbers.** Every number you write in a finding's `statement` (results, sample sizes, percentages, p-values, scores) must also have its own entry in `numbers`. Never write a number in a statement that is missing from `numbers`.  Every number carries a locator: the **printed journal page** (the number printed on the page), the **PDF page** (position in the file, starting at 1), the table or figure, the row label and the column label. If the file prints no page numbers, use the PDF page for both and set `printed_page_source` to `pdf-position`.
4. **Spans.** (Quotes that match the PDF exactly are what the later checks need, so: copy every character as the PDF shows it; prefer the shortest single sentence or table row that holds the numbers, at most about 250 characters, because short quotes copy more reliably than long ones; never join two sentences from different places in one quote; give the PDF page where the quote appears. Code fills in the printed page numbers and corrects page numbers that are wrong, so spend no effort on them.)  For each finding give one or more verbatim spans copied exactly from the PDF text (a sentence or table row that contains the numbers) with the PDF page. Never paraphrase inside a span. Keep each span under 400 characters. If a table cell is the evidence, give the row text as it appears.
5. **Where to look.** Findings come from Results first. Caveats and claims come from the Discussion and Limitations first. Research questions come from the Introduction and stated objectives. Say which section each item came from.
6. **Read the whole table** before writing that something is best, highest, beats or matches. List every comparator that could change the claim.
7. **Text versus table.** When the prose and the paper's own table disagree, report the table value and describe the disagreement in `notes`.
8. **Confidence and pages.** Set `confidence` to `high`, `medium` or `low` (low if the page is a scan, the numbers are hard to read, the table is ambiguous or you are unsure of a value). Set `multi_page` to true when the finding's evidence, table or figure spans more than one page.
9. Do not invent numbers, models, sample sizes or page numbers. If unsure, say so in `notes` and lower the confidence.

## Output (JSON only, no code fence)
{"paper": {"title": "", "authors": "", "year": "", "venue": "", "doi": "", "version": "published | preprint vN | unknown", "printed_page_source": "label | text | pdf-position"},
 "questions": [{"id": "Q1", "original_wording": "verbatim", "kind": "question", "section": "Introduction", "pdf_page": 0, "printed_page": "", "reframed": ""}],
 
 "findings": [{"id": "F1", "tier": "primary", "tier_reason": "", "answers_QUE": ["Q1"], "supports": [], "section": "Results", "statement": "one sentence with the numbers", "P": "", "I": "", "C": "", "O": "", "S": "", "T": "",
   "numbers": [{"label": "", "value": "", "unit": "", "printed_page": "", "pdf_page": 0, "table_or_figure": "", "row": "", "column": ""}],
   "spans": [{"text": "verbatim", "pdf_page": 0}], "multi_page": false, "confidence": "high", "notes": ""}],
 "caveats": [{"id": "V1", "section": "Discussion", "text": "", "applies_to": ["F1"], "span": {"text": "verbatim", "pdf_page": 0}}],
 "claims": [{"id": "C1", "section": "Discussion", "text": "", "answers_QUE": ["Q1"], "supports": ["F1"], "span": {"text": "verbatim", "pdf_page": 0}}],
 "not_reported": ["fields or items the paper does not give"]}

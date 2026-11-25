---
type: prompt
id: picost-v3
used_by: pipeline/scripts/lives_run.py (stage picost; model gemini-4-neon)
written: 2026-11-25
changes: v3 (2026-11-25) adds the research question and three evidence tiers (primary, secondary, tertiary) with a cap per tier; v2 capped the findings at 12; v1 returned 29 findings for a 10-page paper (37,000 output tokens); v2 caps the findings, because the 27 seed papers have 1 to 6 EVDs each (median 3)
---

You extract findings from one research paper (the attached PDF) for a living evidence synthesis about LLMs in scientific research and peer review. Work only from the PDF. Return one JSON object and nothing else.

## Rules
1. **One record per finding, in three tiers.** A finding is one statistical test, one empirical observation or one analytical result. Do not merge findings. The research question (RQ) is given with the paper. Classify every finding:
   - **primary**: it answers the RQ directly (for example, the performance of an LLM on the task the RQ asks about, against its comparator). At most {MAX_PRIMARY}.
   - **secondary**: it is meta or contextual information about a primary finding and helps a reader interpret, qualify or trust it (for example, agreement among the human raters, dataset or sample properties, sensitivity to prompts or settings, failure analyses, cost, or a quantified limitation). At most {MAX_SECONDARY}. Name the primary finding or findings it supports in `supports`.
   - **tertiary**: other context that may matter (descriptive statistics of the corpus, exploratory subgroup results, side findings). At most {MAX_TERTIARY}; return one only if it clearly adds something.
   Give a one-line `tier_reason` for every finding. If the paper has more findings than a tier allows, keep the most important and describe the rest in that tier's `omitted` entry (a count and one line). Do not silently drop findings.
2. **PICOST.** For each finding give Population, Intervention, Comparator, Outcome, Study design and Timeframe. Anything the paper does not state is the string `Not reported`. Never fill a slot with plausible standard detail.
3. **Numbers.** Every number carries a locator: the **printed journal page** (the number printed on the page), the **PDF page** (position in the file, starting at 1), the table or figure, the row label and the column label. If the file prints no page numbers, use the PDF page for both and set `printed_page_source` to `pdf-position`.
4. **Spans.** For each finding give one or more verbatim spans copied exactly from the PDF text (a sentence or table row that contains the numbers) with the PDF page. Never paraphrase inside a span. Keep each span under 400 characters. If a table cell is the evidence, give the row text as it appears.
5. **Where to look.** Findings come from Results first. Caveats and claims come from the Discussion and Limitations first. Research questions come from the Introduction and stated objectives. Say which section each item came from.
6. **Read the whole table** before writing that something is best, highest, beats or matches. List every comparator that could change the claim.
7. **Text versus table.** When the prose and the paper's own table disagree, report the table value and describe the disagreement in `notes`.
8. **Confidence and pages.** Set `confidence` to `high`, `medium` or `low` (low if the page is a scan, the numbers are hard to read, the table is ambiguous or you are unsure of a value). Set `multi_page` to true when the finding's evidence, table or figure spans more than one page.
9. Do not invent numbers, models, sample sizes or page numbers. If unsure, say so in `notes` and lower the confidence.

## Output (JSON only, no code fence)
{"paper": {"title": "", "authors": "", "year": "", "venue": "", "doi": "", "version": "published | preprint vN | unknown", "printed_page_source": "label | text | pdf-position"},
 "findings": [{"id": "F1", "tier": "primary", "tier_reason": "", "supports": [], "section": "Results", "statement": "one sentence with the numbers", "P": "", "I": "", "C": "", "O": "", "S": "", "T": "",
   "numbers": [{"label": "", "value": "", "unit": "", "printed_page": "", "pdf_page": 0, "table_or_figure": "", "row": "", "column": ""}],
   "spans": [{"text": "verbatim", "pdf_page": 0}], "multi_page": false, "confidence": "high", "notes": ""}],
 "caveats": [{"id": "V1", "section": "Discussion", "text": "", "span": {"text": "verbatim", "pdf_page": 0}}],
 "claims": [{"id": "C1", "section": "Discussion", "text": "", "span": {"text": "verbatim", "pdf_page": 0}}],
 "questions": [{"id": "Q1", "section": "Introduction", "text": "", "span": {"text": "verbatim", "pdf_page": 0}}],
 "omitted": {"primary": {"count": 0, "note": ""}, "secondary": {"count": 0, "note": ""}, "tertiary": {"count": 0, "note": ""}},
 "not_reported": ["fields or items the paper does not give"]}

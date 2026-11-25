---
page_type: log/plan
created: 2026-11-24
author: Claude (claude-sonnet-5-5) in Claude Code, for Jay Patel (JP)
human_verified: no
---

# Skill v2: decisions so far and what is left (2026-11-24)

Backup of the pre-v2 files: `misc/skill-backups/2026-11-24-pre-v2/` (Skill.md, Skill-references.md, Skill-synthesis.md, Skill-templates.md, Tools-and-Models.md, TODO.md; checksums inside). **No Skill file has been edited yet.**

## JP's decisions
- Repo `living-evidence-synthesis` (app + vault/) is the single source of truth. The local vault and the repo's vault/ have drifted (Skill.md, Skill-references.md, Welcome.md and several EVD pages differ); reconcile before the first push.
- Parsing: LlamaParse Agentic Plus ($0.0375/page, about $0.56 per 15-page paper; vendor ParseBench tables 93.3), PyMuPDF text layer as a second vote, PyMuPDF + pdftoppm for highlights and screenshots. API, not local models.
- Extraction, question splitting and restyling, alt text, link repair: Gemini 4 Neon at xhigh thinking ($3/$15 per MTok). Fallbacks and spot checks: Opus 5.5, Fable 5.2, GPT 6.2 Sol. Opus 5.5 writes and judges to start. Alt text: Gemini 4 Argon reading each screenshot.
- QA of every PICOST extraction: Liquid d1-ultra decision model (to be tried). Embedding models: tabled.
- Keep the current site look (Quality Signals tables, Prompts and summary pages, TOCs, footers, typography). Drop the Mermaid diagrams in Methods Context.

## Implement in the Skills (all six audit controls)
1. Store both the PDF page and the printed journal page; cite the journal page.
2. Read tables as structured cells (two tools agree), not `pdftotext -layout`.
3. Every number carries a table, row and column locator.
4. "Not reported" when the paper is silent; a locator for every claim.
5. Reconcile prose against tables; use the table and add a note.
6. Check the whole table before "best".
Plus: question rules (one construct per question, no yes/no, "how well", neutral terms like "research reports" and "LLMs", do not mirror the authors, use the template) with each QUE's original wording kept as a quote; grounding specs (quote: whole quote, clean capture; table/figure: cropped to the table or figure and caption, all rows, columns and panels, no body text; Missing = no table or figure shown; Methods tables in EVD, SRC and other pages grounded the same way); PICOST-first extraction with locators, EVDs written from the PICOST cells.

## Open before revising the Skills
- No Google (Gemini) or LlamaCloud API key is set, so the Neon extraction, Argon alt text and LlamaParse bake-off cannot run yet.
- d1-ultra QA of PICOST extractions: not tried.
- TODO 13-14 (audit corrections), 16-19, 20-21 and 0d are still open.
- Two background agents were opening draft PRs on other branches (app privacy, contribute flow, sanitising, alt-text plumbing, workflow; vault embeds, journal page numbers, licences). Check their results.

---
title: AI disclosure (GAMER checklist)
type: provenance
---
# AI disclosure for LIVES

LIVES nodes (SRC, QUE, CLM, EVD, CVT, EP) are written with generative AI and checked by decision models and by people. This page answers the nine items of the **GAMER** checklist (Generative Artificial intelligence tools in MEdical Research) once for the whole project. Every node footer links here and adds the page-specific facts: which model, which version, when, which prompt, which response.

Each page footer is a collapsed callout. The title line is the short form (`AI use: <models> · <date> · <human-check status>`). Opening it shows the step table and a role/sections/checked-by line.

| # | GAMER item | Where it is reported | Answer for LIVES |
|---|---|---|---|
| 1 | Were GAI tools used? | Every footer | Yes: extraction, node writing, quality signals, and design consults. |
| 2 | Tools, versions, dates | Footer table (`Model and version`, `Accessed (UTC)`); [[pipeline/provenance/model-history|model history]] for older pages | Exact model id and UTC time per call. Older pages: era table. |
| 3 | Prompting technique, prompts, unedited responses | Footer `Prompt` (GitHub permalink and hash) and `Response`; `pipeline/runs/<run>/responses/` | Prompts are versioned files in `pipeline/prompts/`. Unedited responses are saved per call from the first run that uses `call_logger.py` (Nov 2026). Earlier pages: not archived. |
| 4 | New or fine-tuned tool: base model | n/a | No model was trained or fine-tuned for LIVES. |
| 5 | Role in each phase | Footer `Role` | Reading PDFs, extracting claims/evidence, drafting nodes, rating quality signals, checking quotes against the PDF, advising on design. |
| 6 | Sections and paragraphs contributed | Footer `Sections` | Whole node unless stated. |
| 7 | How output was verified and modified | Footer `Checked by`; `human_verified` in frontmatter | Scripts check that quotes are verbatim and pages exist (`audit_signal_quotes.py`, `verbatim_audit.py`, `check_links.py`). Decision models (Perplexity Decider, Liquid d1-ultra, Jev) second-rate. A person signs off (`human_verified: yes`, with date). |
| 8 | Data privacy and confidentiality | This page | Inputs are published papers. No personal or participant data is sent. API providers: Anthropic, OpenAI, Perplexity, Liquid, TypeSafe. Keys stay in a local `.env`. |
| 9 | Influence on interpretation | This page | AI wrote the first reading and the ratings; people decide what to keep. Where models disagree the page says so. Known limit: some quotes are not verbatim in the PDF (audited, counted per run). |

Rules for the pipeline (Skill step 4c): every node page gets this footer, every model call is logged, every prompt is committed before use.

---
page_type: log/plan
created: 2026-11-24
author: Claude (claude-sonnet-5-5) in Claude Code, for Jay Patel (JP)
human_verified: no
---

# Ingest budget and five-paper batches (2026-11-24)

> [!warning] Superseded in part (2026-11-25)
> This note is the plan of 2026-11-24. Since then: batches are **four papers at most**, with a **$5.55 cap per batch** and stop rules built into `pipeline/scripts/lives_run.py`; **Gemini 4 Neon** reads and extracts (not GPT-6.2 Sol); extraction is tiered (primary, secondary, tertiary); and the real cost of one 10-page paper through extraction, recheck and adjudication was $0.52 in standard mode. Current numbers: `pipeline/skills/Tools-and-Models.md` (Token budgets) and `Skill.md` (Step 1, item 11a). The figures below are kept for history.

JP topped up OpenAI and Anthropic with USD 100 each (USD 200 in all). Work proceeds five papers at a time with human spot checks, so every batch can be corrected before more money is spent.

## Estimated cost per paper (my estimates; replace with measured numbers after the pilot)
| Step | Model | Standard | Batch |
|---|---|---|---|
| Read PDF and extract PICOST (effort High) | GPT-6.2 Sol | about USD 0.46 | about 0.23 |
| Write QUE, CLM, EVD, CVT, SRC nodes | Claude Opus 5.5 | about 0.60 | about 0.30 |
| Verify flagged records plus a 10% sample | Claude Opus 5.5 | about 0.15 | about 0.08 |
| Restyle questions, alt text, link repair (Medium) | GPT-6.2 Sol | about 0.10 | about 0.05 |
| Total per paper | | about 1.3 | about 0.65 |

A five-paper batch is about USD 6.5 standard or 3.3 by batch. Pilot (5 papers read at Medium, High and Max, reading only): about USD 7 on OpenAI.

## Pilot (JP, 2026-11-24): re-extract five seed papers whose content is already audited
Sample of the five seed papers with the most EVDs (the first five; Woelfle also carries earlier table and quote errors, EVD 16, 45 and 47): Woelfle et al. 2024 (6 EVDs), Sarol et al. 2024, Liang et al. 2024 (the vault PDF, preprint), Sridharan & Sivaramakrishnan 2024 and Srinivasan et al. 2025a (4 EVDs each). Add four papers where the first iteration had fidelity or grounding errors, so we can see whether the pipeline fixes them: Tyser et al. 2024 (quote EVD 51; fidelity EVD 38 and 52), Bougie et al. 2024 (quote EVD 22; fidelity and table EVD 21), Wrightson et al. 2025 (quote EVD 18 and 39) and Alharbi and Asiri 2024 (quote and table EVD 9). That is nine papers, about USD 12 at standard prices. Run the new pipeline on their PDFs blind (never show the model the existing pages) and compare with the audited vault content: recall of the existing EVDs, number accuracy against the corrected values, verbatim quotes, page citations, crop QA pass rate and your verdict on crops, and whether the question wording needs edits. Standard API for the first three papers, then iterate, then the other two; Batch APIs only after an external reviewer's feedback.

## Staged pilot to keep the cost down (JP: USD 12 is a bit much)
Fidelity errors in the first iteration are ignored: those EVDs were poorly written, and the new Phase 2 style removes the cause. The extra papers are kept only for their grounding errors.
- **Stage 1 (three papers, standard API, about USD 3 to 4):** Woelfle (6 EVDs; table and quote errors), Bougie (quote 22, table 21) and Tyser (quote 51). Review, then fix prompts.
- **Stage 2 (three papers, about USD 3):** Sarol (table errors EVD 8 and 29), Alharbi (EVD 9) and Wrightson (EVD 18, 39).
- **Stage 3 (optional, about USD 2 to 3):** Liang, Sridharan 2024 and Srinivasan 2025a, only if stages 1 and 2 look good.
- **Cost levers inside the pilot:** read only Results, Discussion, Introduction and tables first (about 40% fewer tokens); send page images only for table and figure pages; Sol High for reading, Medium for the rest; test Claude Sonnet 5.5 ($2 in, $10 out) against Opus 5.5 ($4, $20) for node writing on one paper; write nodes with Opus only for papers that pass spot check A; d1-ultra shadow checks cost almost nothing; stop a stage if it passes 1.5 times its estimate. Expected pilot total about USD 7 to 10.

## Guardrails
- Per-batch cap: USD 5 per provider; stop and review if a batch costs more than 1.5 times its estimate.
- Keep USD 15 per provider in reserve for reruns. About 20 batches (100 papers) fit in the remaining USD 170 at standard prices; plan for 60 to 100 papers.
- Log tokens and dollars per paper and step in the ledger below after every batch.
- Order: pilot first, fix prompts, then batches. Use the Batch APIs for steps nobody is waiting on; standard API for the pilot and the first batch.

## Human-in-the-loop for each batch of five
1. JP chooses the five papers (most recent version of each; older PDF kept as Archive).
2. Sol reads each PDF and writes PICOST records with locators.
3. **JP spot check A (about 10 minutes per paper):** three random PICOST records per paper against the PDF (value, row, column, printed page). Any error stops the batch until the prompt is fixed.
4. Opus 5.5 writes the nodes from the PICOST records; automated checks run (verbatim quotes, page map, every EVD number present in its PICOST record).
5. **JP spot check B:** the crops (whole quote, table or figure plus caption only) and two numbers per EVD.
6. Merge through a pull request with regenerated graph data; update the ledger.

## Ledger
| Date | Batch | Papers | OpenAI USD | Anthropic USD | Errors found at checks A and B | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

## Needed before the pilot
`OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in `~/.config/lives-ai-raters/.env` (only the Perplexity, Liquid and Jev keys are there now). Never paste keys into chat.

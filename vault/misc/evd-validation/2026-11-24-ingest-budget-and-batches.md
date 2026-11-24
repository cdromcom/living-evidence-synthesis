---
page_type: log/plan
created: 2026-11-24
author: Claude (claude-sonnet-5-5) in Claude Code, for Jay Patel (JP)
human_verified: no
---

# Ingest budget and five-paper batches (2026-11-24)

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

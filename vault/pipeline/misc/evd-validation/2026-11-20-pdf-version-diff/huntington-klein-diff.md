# Huntington-Klein & Murray: arXiv v1 (2024) vs Journal of Causal Inference (2026)

The published version keeps every number the two evidence pages rely on (all the kappas, agreement shares, consistency shares and per-category bar values match after rounding), but it is a bigger paper. It adds two new prompting methods (pick-from-list and sequential), roughly doubles the response count, redraws and renumbers the figures, and softens the option-ordering claim to "for some prompts", because ordering does not affect the new pick-from-list method. Both EVD statements still hold. Checking them against the PDFs also turned up several errors that were already wrong against the old version: one misquoted kappa and three wrong table values. Every verbatim quote with a citation in it now differs slightly, because the journal uses numbered citations and writes kappas as "0.16" rather than ".16". Page numbers have shifted throughout.

**Main changes (old page to new page)**
- New methods: "pick from list" (choose confounders from a list of five) and "sequential" prompting (pp. 4–5). They were run in August 2025 with GPT-o1-pro and claude-3-5-sonnet-20240620 because GPT-o1-preview had been retired.
- Response counts: 13,760 per model and 688 for GPT-o1 (old p7) became 31,270 per model and 1,447 for GPT-o1 (new p8).
- Table 1 was rebuilt (old p7 to new p8). The Unsure and Related-to columns are gone, and rows were added for no-reasoning, pick-from-list (41–48%) and sequential prompting. The original direct/indirect shares (59.9 / 71.9 / 58.7; 89.5 / 81.9 / 93.6) are unchanged.
- Figures: a new Fig 1 flowchart shifts the numbering. Old Figs 1–8 are now Figs 2–5 and 8–11, and Figs 6, 7 and 12 are new. Bars now read Never/Mix/Always with one decimal place.
- New results:
  - Agreement between other pairs of prompting methods is weak. Cohen's kappa (a chance-corrected agreement score) reaches at most 0.37 for GPT-4o and Claude, and 0.56 for GPT-o1 (p17).
  - Pick-from-list is the most consistent method and is not sensitive to option order (pp. 16, 18–19).
  - Sequential prompting still flags confounders and non-confounders at similar rates (p14).
- The conclusions add a limitations paragraph and some hedges: "only a modest signal" (old: "without a heavy signal"), and option-order sensitivity "for one prompting method". A new paragraph says better consistency did not bring better agreement with the experts.
- Cosmetic: 27 pages became 30, numbered sections and citations, a declarations section, two Appendix C additions, and a wrong citation on new p4 ("Debertin et al. [10]" points to the Dettki et al. entry).

**EVD – kappa as low as 0.16**
- The statement holds, and every kappa and percentage is unchanged.
- Wrong in both versions: the Description quote gives Claude's option-order kappa as ".13". The paper gives .41 (0.41); .13 is GPT-4o's figure. The first quote also drops a sentence without marking the cut.
- The lowest kappa reported anywhere is 0.13, so the title understates how low agreement goes.
- The new pages are p16–17, p18, p7 and p16 fn 9; figures 5–8 are now 8–11. The page should add that option-order sensitivity is limited to some prompts.

**EVD – expert and trimmed confounders at similar rates**
- The statement holds, and new p14 adds supporting evidence from sequential prompting.
- Wrong in both versions:
  - In the direct "Added in 2016" row, Claude and GPT-o1 are 30% at 100%, not 50% and 80%.
  - 59.9% is Claude's overall direct-method share, not its share for Original confounders.
  - The "≈70% Final Expert DAG" figure comes from the direct method, not the indirect one.
- The Data quote and the 13,760/688 response counts no longer appear in the new version (new p8). The other quotes are now on p3 and p8–9, and Fig 1 and Fig 2 are now Fig 2 and Fig 3.
- All screenshots on both pages are crops of the old layout and should be retaken.

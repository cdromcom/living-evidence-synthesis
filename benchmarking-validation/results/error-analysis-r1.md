# Error analysis, run r1

Held-out EVD 4-77 (74 EVDs; table/figure n=72 because two JP NA rows are excluded). JP = reference. Models see only the sheet content.

## relevancy

JP labels: {'Relevant': 65, 'Irrelevant': 9}

### Perplexity Decider 1.3: 9 errors of 74 (88% agreement)

Error types (JP label -> model label): Irrelevant->Relevant x5; Relevant->Irrelevant x4

- 5 of 9 errors are borderline (P within 0.2 of 0.5).
- Wrong EVDs: [7, 17, 26, 32, 49, 60, 72, 75, 76]

### Liquid d1-ultra: 8 errors of 74 (89% agreement)

Error types (JP label -> model label): Relevant->Irrelevant x4; Irrelevant->Relevant x4

- 2 of 8 errors are borderline (P within 0.2 of 0.5).
- Wrong EVDs: [7, 17, 32, 49, 61, 72, 75, 76]

### Jev: 16 errors of 74 (78% agreement)

Error types (JP label -> model label): Relevant->Irrelevant x12; Irrelevant->Relevant x4

- 8 of 16 errors are borderline (P within 0.2 of 0.5).
- Wrong EVDs: [5, 6, 7, 17, 26, 32, 36, 42, 49, 55, 61, 65, 66, 72, 75, 76]

**Shared errors:** wrong in all three models: 7 EVDs [7, 17, 32, 49, 72, 75, 76]; wrong in at least one: 17; wrong in exactly one: 8.

## fidelity

JP labels: {'Partially Met': 6, 'Met': 68}

### Perplexity Decider 1.3: 19 errors of 74 (74% agreement)

Error types (JP label -> model label): Met->Partially Met x15; Partially Met->Unmet x2; Met->Unmet x2

- 17 of 19 errors are the model calling Partially Met/Unmet where JP said Met; in 14 of those the model also says not every number in the EVD is in the quote (it is applying a numbers-in-the-quote test that JP's gist rule does not require).
- Model Partially Met/Unmet total: 23 vs JP 6.
- Wrong EVDs: [4, 19, 26, 29, 34, 36, 38, 41, 47, 52, 54, 56, 59, 64, 65, 66, 70, 73, 75]

### Liquid d1-ultra: 14 errors of 74 (81% agreement)

Error types (JP label -> model label): Met->Partially Met x8; Met->Unmet x3; Partially Met->Unmet x2; Partially Met->Met x1

- 11 of 14 errors are the model calling Partially Met/Unmet where JP said Met; in 10 of those the model also says not every number in the EVD is in the quote (it is applying a numbers-in-the-quote test that JP's gist rule does not require).
- Model Partially Met/Unmet total: 16 vs JP 6.
- Wrong EVDs: [4, 19, 26, 36, 38, 41, 44, 47, 54, 56, 59, 65, 73, 75]

### Jev: 18 errors of 74 (76% agreement)

Error types (JP label -> model label): Met->Partially Met x9; Met->Unmet x5; Partially Met->Unmet x2; Partially Met->Met x2

- 14 of 18 errors are the model calling Partially Met/Unmet where JP said Met; in 11 of those the model also says not every number in the EVD is in the quote (it is applying a numbers-in-the-quote test that JP's gist rule does not require).
- Model Partially Met/Unmet total: 18 vs JP 6.
- Wrong EVDs: [4, 19, 26, 29, 36, 38, 41, 44, 45, 46, 47, 52, 54, 56, 64, 65, 73, 75]

**Shared errors:** wrong in all three models: 12 EVDs [4, 19, 26, 36, 38, 41, 47, 54, 56, 65, 73, 75]; wrong in at least one: 22; wrong in exactly one: 5.

## quote

JP labels: {'Correct': 60, 'Incorrect': 12, 'Missing': 1, 'Partially Correct': 1}

### Perplexity Decider 1.3: 11 errors of 74 (85% agreement)

Error types (JP label -> model label): Correct->Partially Correct x5; Correct->Incorrect x4; Incorrect->NA x1; Incorrect->Partially Correct x1

- 4 errors are the model saying Incorrect where JP said Correct; the model was confident the screenshot does not show the quote (P<0.2) in 4, and Claude's earlier note also reports a mismatched/different passage in 4. These are likely JP-rule inconsistencies (JP rated verbatim quotes with mismatched screenshots Correct before the 2026-11-23 rule), not model errors: [5, 6, 18, 66].
- Wrong EVDs: [5, 6, 9, 11, 18, 25, 38, 39, 51, 53, 66]

### Liquid d1-ultra: 16 errors of 74 (78% agreement)

Error types (JP label -> model label): Correct->Partially Correct x7; Correct->Incorrect x6; Incorrect->NA x1; Partially Correct->Incorrect x1; Incorrect->Partially Correct x1

- 6 errors are the model saying Incorrect where JP said Correct; the model was confident the screenshot does not show the quote (P<0.2) in 4, and Claude's earlier note also reports a mismatched/different passage in 4. These are likely JP-rule inconsistencies (JP rated verbatim quotes with mismatched screenshots Correct before the 2026-11-23 rule), not model errors: [5, 6, 18, 66].
- Wrong EVDs: [5, 6, 9, 11, 13, 18, 19, 22, 25, 38, 39, 50, 51, 53, 64, 66]

### Jev: 14 errors of 74 (81% agreement)

Error types (JP label -> model label): Correct->Partially Correct x6; Correct->Incorrect x5; Incorrect->Correct x1; Partially Correct->Incorrect x1; Incorrect->Partially Correct x1

- 5 errors are the model saying Incorrect where JP said Correct; the model was confident the screenshot does not show the quote (P<0.2) in 3, and Claude's earlier note also reports a mismatched/different passage in 4. These are likely JP-rule inconsistencies (JP rated verbatim quotes with mismatched screenshots Correct before the 2026-11-23 rule), not model errors: [5, 6, 18, 66].
- Wrong EVDs: [5, 6, 9, 18, 22, 35, 38, 50, 51, 52, 53, 54, 64, 66]

**Shared errors:** wrong in all three models: 8 EVDs [5, 6, 9, 18, 38, 51, 53, 66]; wrong in at least one: 19; wrong in exactly one: 5.

## table

JP labels: {'Missing': 65, 'Partially Correct': 6, 'Correct': 1}

### Perplexity Decider 1.3: 8 errors of 72 (89% agreement)

Error types (JP label -> model label): Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2

- Wrong EVDs: [8, 9, 11, 16, 21, 29, 45, 47]  (JP vs model on EVDs with a table image: EVD 8: JP Partially Correct / model Correct, EVD 16: JP Missing / model Correct, EVD 29: JP Partially Correct / model Correct, EVD 31: JP Correct / model Correct, EVD 45: JP Partially Correct / model Correct, EVD 47: JP Missing / model Correct)

### Liquid d1-ultra: 8 errors of 72 (89% agreement)

Error types (JP label -> model label): Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2

- Wrong EVDs: [8, 9, 11, 16, 21, 29, 45, 47]  (JP vs model on EVDs with a table image: EVD 8: JP Partially Correct / model Correct, EVD 16: JP Missing / model Correct, EVD 29: JP Partially Correct / model Correct, EVD 31: JP Correct / model Correct, EVD 45: JP Partially Correct / model Correct, EVD 47: JP Missing / model Correct)

### Jev: 8 errors of 72 (89% agreement)

Error types (JP label -> model label): Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2

- Wrong EVDs: [8, 9, 11, 16, 21, 29, 45, 47]  (JP vs model on EVDs with a table image: EVD 8: JP Partially Correct / model Correct, EVD 16: JP Missing / model Correct, EVD 29: JP Partially Correct / model Correct, EVD 31: JP Correct / model Correct, EVD 45: JP Partially Correct / model Correct, EVD 47: JP Missing / model Correct)

**Shared errors:** wrong in all three models: 8 EVDs [8, 9, 11, 16, 21, 29, 45, 47]; wrong in at least one: 8; wrong in exactly one: 0.

## Rows wrong in all three models (fidelity)

- EVD 4 (AI Scientist achieved accuracy 0.47 F1 0.44 kappa 0.05 on same novelty evaluation test set): models {'Perp': 'Unmet', 'Liqu': 'Unmet', 'Jev': 'Unmet'}; JP Partially Met; Claude Partially Met
- EVD 19 (Full text input produced lower Spearman correlations than abstracts for all three ChatGPT ): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Partially Met'}; JP Met; Claude Partially Met
- EVD 26 (GPT-3.5 Turbo accuracy on quotation error detection peaked at 68.0% (title only) and dropp): models {'Perp': 'Unmet', 'Liqu': 'Unmet', 'Jev': 'Unmet'}; JP Met; Claude Partially Met
- EVD 36 (GPT-4 Turbo achieved 70.0% overall accuracy on quotation error detection with title plus a): models {'Perp': 'Partially Met', 'Liqu': 'Unmet', 'Jev': 'Unmet'}; JP Met; Claude Partially Met
- EVD 38 (GPT-4 Turbo ranked first in human preference for academic review quality with score 0.558): models {'Perp': 'Unmet', 'Liqu': 'Unmet', 'Jev': 'Unmet'}; JP Partially Met; Claude Met
- EVD 41 (GPT-4o identified 52% coarse accuracy on LimitGen-Syn while human experts achieved 86% and): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Partially Met'}; JP Met; Claude Partially Met
- EVD 47 (Individual LLM accuracy ranged 63-70 percent for PRISMA and 53-74 percent for AMSTAR versu): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Partially Met'}; JP Met; Claude Partially Met
- EVD 54 (LLMs designated expert-selected confounders in CDP as confounders at similar rates to vari): models {'Perp': 'Unmet', 'Liqu': 'Unmet', 'Jev': 'Unmet'}; JP Met; Claude Partially Met
- EVD 56 (LLMs showed lowest accuracy on questions about statistical software used and study funding): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Unmet'}; JP Met; Claude Partially Met
- EVD 65 (o4-mini achieved 59.6% HR@5 as a scientific paper quality checker at a cost of $0.038 per ): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Partially Met'}; JP Met; Claude Partially Met
- EVD 73 (RAG augmentation improved GPT-4o limitation identification coarse accuracy by 12.2 percent): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Unmet'}; JP Met; Claude Partially Met
- EVD 75 (Removing facet-based RankGPT re-ranker dropped not-novel prediction accuracy from 89.66% t): models {'Perp': 'Partially Met', 'Liqu': 'Partially Met', 'Jev': 'Partially Met'}; JP Met; Claude Partially Met
# Error analysis, Run 2 (r2t) and change from Run 1

Held-out EVD 4-77 after JP's exclusions of 2026-11-24 (inputs/exclusions.json): relevancy n=68 (EVD 7, 17, 49, 72, 75, 76 dropped), fidelity n=66 (EVD 4, 19, 26, 36, 38, 54, 56, 65 dropped), quote n=66 (EVD 5, 6, 9, 18, 45, 51, 53, 66 dropped pending JP re-rating), table/figure n=72 (two JP NA rows excluded). The earlier all-rows analysis is in the previous commit and in results/metrics-*-all.json. JP = reference. r2t = Run 2 relevancy, fidelity and quote plus the table/figure rerun with Missing-by-rule when the page has no table/figure-slot screenshot. Run 1 uses r1 with the r1fix overrides for EVD 21 and 38.

## relevancy

JP labels (n=68): {'Relevant': 63, 'Irrelevant': 5}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 65/68 | 65/68 | 0 | 0 | 0 | Relevant->Irrelevant x2; Irrelevant->Relevant x1 |
| Liquid | 66/68 | 65/68 | 1 | 0 | 1 | Relevant->Irrelevant x3 |
| Jev | 58/68 | 58/68 | 2 | 1 | 1 | Relevant->Irrelevant x10 |
| Opus 5.5 | 64/68 | 64/68 | 0 | 0 | 0 | Relevant->Irrelevant x3; Irrelevant->Relevant x1 |

Wrong in all four raters in Run 2: 1 EVDs [32]. Wrong in at least one: 11. Wrong in exactly one: 5.

Run 2 relevancy errors per rater: Perplexity [26, 32, 60]; Liquid [5, 32, 61]; Jev [5, 6, 26, 32, 36, 42, 55, 61, 65, 73]; Opus 5.5 [6, 32, 60, 61]

## fidelity

JP labels (n=66): {'Met': 62, 'Partially Met': 4}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 54/66 | 54/66 | 0 | 0 | 0 | Met->Partially Met x11; Partially Met->Met x1 |
| Liquid | 59/66 | 58/66 | 1 | 0 | 1 | Met->Partially Met x6; Partially Met->Met x2 |
| Jev | 56/66 | 56/66 | 2 | 1 | 1 | Met->Partially Met x7; Partially Met->Met x2; Met->Unmet x1 |
| Opus 5.5 | 61/66 | 61/66 | 2 | 1 | 1 | Partially Met->Met x4; Met->Partially Met x1 |

Wrong in all four raters in Run 2: 0 EVDs []. Wrong in at least one: 16. Wrong in exactly one: 4.

Run 2 fidelity: model Partially Met/Unmet where JP Met, per rater: Perplexity 11; Liquid 6; Jev 8; Opus 5.5 1

## quote

JP labels (n=66): {'Correct': 54, 'Incorrect': 11, 'Partially Correct': 1}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 63/66 | 63/66 | 2 | 1 | 1 | Correct->Partially Correct x3 |
| Liquid | 58/66 | 63/66 | 5 | 5 | 0 | Correct->Partially Correct x2; Correct->Incorrect x1 |
| Jev | 60/66 | 62/66 | 2 | 2 | 0 | Correct->Partially Correct x3; Partially Correct->Incorrect x1 |
| Opus 5.5 | 57/66 | 59/66 | 2 | 2 | 0 | Correct->Partially Correct x7 |

Wrong in all four raters in Run 2: 0 EVDs []. Wrong in at least one: 11. Wrong in exactly one: 5.

Run 2 quote: JP Correct but model not Correct, per rater: Perplexity [11, 39, 40]; Liquid [19, 22, 25]; Jev [22, 35, 54]; Opus 5.5 [11, 25, 35, 39, 40, 52, 64]

## table

JP labels (n=72): {'Missing': 65, 'Partially Correct': 6, 'Correct': 1}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 64/72 | 64/72 | 0 | 0 | 0 | Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2 |
| Liquid | 64/72 | 64/72 | 0 | 0 | 0 | Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2 |
| Jev | 64/72 | 64/72 | 0 | 0 | 0 | Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2 |
| Opus 5.5 | 64/72 | 64/72 | 0 | 0 | 0 | Partially Correct->Correct x3; Partially Correct->Missing x3; Missing->Correct x2 |

Wrong in all four raters in Run 2: 8 EVDs [8, 9, 11, 16, 21, 29, 45, 47]. Wrong in at least one: 8. Wrong in exactly one: 0.

Rows a model actually judged in Run 2 (the rule decides the rest): EVD 8: JP Partially Correct / models ['Correct', 'Correct', 'Correct', 'Correct'], EVD 16: JP Missing / models ['Correct', 'Correct', 'Correct', 'Correct'], EVD 29: JP Partially Correct / models ['Correct', 'Correct', 'Correct', 'Correct'], EVD 31: JP Correct / models ['Correct', 'Correct', 'Correct', 'Correct'], EVD 45: JP Partially Correct / models ['Correct', 'Correct', 'Correct', 'Correct'], EVD 47: JP Missing / models ['Correct', 'Correct', 'Correct', 'Correct']

JP Missing but the page has a table/figure-slot screenshot and models said Correct: [16, 47]
JP non-Missing but the rule said Missing (no table/figure-slot screenshot): [9, 11, 21]

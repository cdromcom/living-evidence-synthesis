# Error analysis, Run 2 (r2t) and change from Run 1

Held-out EVD 4-77 (table/figure n=72: two JP NA rows excluded). JP = reference. r2t = Run 2 relevancy, fidelity and quote plus the table/figure rerun with Missing-by-rule when the page has no table/figure-slot screenshot. Run 1 uses r1 with the r1fix overrides for EVD 21 and 38.

## relevancy

JP labels (n=74): {'Relevant': 65, 'Irrelevant': 9}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 65/74 | 65/74 | 0 | 0 | 0 | Irrelevant->Relevant x5; Relevant->Irrelevant x4 |
| Liquid | 66/74 | 65/74 | 1 | 0 | 1 | Relevant->Irrelevant x5; Irrelevant->Relevant x4 |
| Jev | 58/74 | 58/74 | 2 | 1 | 1 | Relevant->Irrelevant x12; Irrelevant->Relevant x4 |
| Opus 5.5 | 64/74 | 64/74 | 0 | 0 | 0 | Relevant->Irrelevant x5; Irrelevant->Relevant x5 |

Wrong in all four raters in Run 2: 7 EVDs [7, 17, 32, 49, 72, 75, 76]. Wrong in at least one: 17. Wrong in exactly one: 5.

Run 2 relevancy errors per rater: Perplexity [7, 17, 26, 32, 49, 60, 72, 75, 76]; Liquid [5, 7, 17, 32, 49, 61, 72, 75, 76]; Jev [5, 6, 7, 17, 26, 32, 36, 42, 49, 55, 61, 65, 72, 73, 75, 76]; Opus 5.5 [6, 7, 17, 32, 49, 60, 61, 72, 75, 76]

## fidelity

JP labels (n=74): {'Partially Met': 6, 'Met': 68}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 54/74 | 54/74 | 0 | 0 | 0 | Met->Partially Met x15; Partially Met->Met x2; Met->Unmet x2; Partially Met->Unmet x1 |
| Liquid | 59/74 | 58/74 | 1 | 0 | 1 | Met->Partially Met x9; Met->Unmet x3; Partially Met->Met x3; Partially Met->Unmet x1 |
| Jev | 56/74 | 56/74 | 2 | 1 | 1 | Met->Partially Met x9; Met->Unmet x5; Partially Met->Met x3; Partially Met->Unmet x1 |
| Opus 5.5 | 61/74 | 61/74 | 3 | 1 | 1 | Met->Partially Met x5; Partially Met->Met x5; Met->Unmet x2; Partially Met->Unmet x1 |

Wrong in all four raters in Run 2: 8 EVDs [4, 19, 26, 36, 38, 54, 56, 65]. Wrong in at least one: 24. Wrong in exactly one: 4.

Run 2 fidelity: model Partially Met/Unmet where JP Met, per rater: Perplexity 17; Liquid 12; Jev 14; Opus 5.5 7

## quote

JP labels (n=74): {'Correct': 60, 'Incorrect': 12, 'Missing': 1, 'Partially Correct': 1}

| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |
|---|---|---|---|---|---|---|
| Perplexity | 64/74 | 63/74 | 4 | 1 | 2 | Correct->Partially Correct x6; Correct->Incorrect x3; Missing->Incorrect x1; Incorrect->Partially Correct x1 |
| Liquid | 59/74 | 63/74 | 7 | 5 | 1 | Correct->Incorrect x6; Correct->Partially Correct x3; Missing->Incorrect x1; Incorrect->Partially Correct x1 |
| Jev | 61/74 | 62/74 | 3 | 2 | 1 | Correct->Incorrect x5; Correct->Partially Correct x4; Missing->Incorrect x1; Partially Correct->Incorrect x1 |
| Opus 5.5 | 58/74 | 59/74 | 3 | 2 | 1 | Correct->Partially Correct x9; Correct->Incorrect x4; Missing->Incorrect x1; Incorrect->Partially Correct x1 |

Wrong in all four raters in Run 2: 8 EVDs [5, 6, 9, 18, 45, 51, 53, 66]. Wrong in at least one: 19. Wrong in exactly one: 5.

Run 2 quote: JP Correct but model not Correct, per rater: Perplexity [5, 6, 9, 11, 18, 39, 40, 51, 66]; Liquid [5, 6, 9, 18, 19, 22, 25, 51, 66]; Jev [5, 6, 9, 18, 22, 35, 51, 54, 66]; Opus 5.5 [5, 6, 9, 11, 18, 25, 35, 39, 40, 51, 52, 64, 66]

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

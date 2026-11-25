# Statistical accuracy checks (scripted clues for a person to check)

Checks: PERCENT sums, GRIM means, SAMPLE size agreement. A finding is a clue, not a verdict. See `pipeline/scripts/stat_checks.py`.
Examined across all papers: 103 percentage groups, 1 mean-with-n passages, 609 passages naming a sample size, 15 estimates with a confidence interval, 101 'a of b (p%)' ratios, 142 passages with F1 or kappa inputs, 44 effect-size values, 0 passages with full sample, exclusions and analytic sample, 49 passages stating a scale range. A paper with no finding below simply had nothing flagged.


## @robertsComparativeStudyChatGPT2023

- **INTERVAL** (p. 1, results): estimate 4.92 is outside its own interval 0.62 to 0.37. (A lost minus sign in the PDF text can cause this: look at the page.) Text: “4.92% (95% CI 0.62%, 0.37%)”
- **INTERVAL** (p. 1, results): estimate 0.764 is outside its own interval 0.186 to 0.280. (A lost minus sign in the PDF text can cause this: look at the page.) Text: “0.764 (95% CI 0.186, 0.280)”
- **INTERVAL** (p. 1, results): estimate 0.034 is outside its own interval 0.818 to 0.895. (A lost minus sign in the PDF text can cause this: look at the page.) Text: “0.034 (95% CI 0.818, 0.895)”
- **INTERVAL** (p. 3, results): estimate 4.92 is outside its own interval 0.62 to 0.37. (A lost minus sign in the PDF text can cause this: look at the page.) Text: “4.92% (95% CI 0.62%, 0.37%)”

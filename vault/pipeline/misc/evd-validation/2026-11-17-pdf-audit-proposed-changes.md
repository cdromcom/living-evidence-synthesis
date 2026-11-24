---
page_type: log/audit-review
created: 2026-11-17
author: Claude (Opus 5.5) with Jay Patel (JP)
status: awaiting JP review - nothing below has been applied
---

# Proposed EVD page corrections from the PDF audit (2026-11-17)

> [!info] Status: proposals only
> **None of these changes has been applied to the EVD pages.** Tick the box on each change you approve (or write a note under it), then ask Claude to apply the ticked ones. Quote wording, screenshots and titles are never changed. Ten proposals would change only the page number in a quote citation; they are marked HELD.

> [!warning] PDF files renamed on 2026-11-20
> Newer published versions were added to `source/pdfs`, and the versions this audit was checked against were renamed with an "Archive - " prefix (same convention as Zhang & Abernethy). Page numbers below refer to the **Archive** files:
> - `Thelwall - 2024 - ...pdf` is now `Archive - superseded versions/Archive - Thelwall - 2024.pdf` (new: `Thelwall - 2025 - ...pdf`, JDIS 2025)
> - `Huntington-Klein and Murray - 2024. - ...pdf` is now `Archive - superseded versions/Archive - Huntington-Klein and Murray - 2024.pdf` (new: `... - 2026 - ...pdf`, J Causal Inference)
> - `Shahid et al. - 2025 - ...pdf` (arXiv v1) is now `Archive - superseded versions/Archive - Shahid et al. - 2025.pdf` (new: the SDP 2025 version under the old name)
> - `Xu et al. - 2025 - ...pdf` (arXiv v1) is now `Archive - superseded versions/Archive - Xu et al. - 2025.pdf` (new: the ACL 2025 version under the old name)
> What changed between versions: `misc/evd-validation/2026-11-20-pdf-version-diff/`.

**Totals:** 147 proposed corrections on 57 of 77 EVD pages, from 5 auditor agents. A separate checker agent re-verified each one against the PDF: 142 accepted as proposed, 5 accepted with adjusted wording (the adjusted text is shown), 0 rejected.

Plus **38 Zhang & Abernethy v1-to-v3 updates** (ids z0-z37; checker: 37 accepted, 1 adjusted). **Held for your decision:** 10 changes that would fix the page number in a quote's citation (search "HELD"). **Superseded:** change 137, replaced by z6. Everything else is ready to apply once ticked.

| Type | Count |
| --- | ---: |
| Wrong number | 49 |
| Not in the paper | 33 |
| Paper contradicts itself (note added, quote untouched) | 19 |
| Wrong page reference | 18 |
| Credited to the wrong model, rater or condition | 17 |
| Missing comparator | 8 |
| Row or column shift | 3 |

> [!warning] How much to trust the checker
> The checker rejected nothing. That can mean the auditors were accurate, or that the checker was lenient. **70 changes are marked ⚑**: they rest on reading a value off a figure, inferring from table footnotes, or were rated medium confidence by the auditor. Check those against the PDF first. Each change links to the PDF page (click the link in Obsidian).

## Why these seven types of error happened

> [!note] The root cause behind all seven
> In Phase 22 (2026-04-28, `History.md`), 26 Claude subagents rewrote all 77 EVD pages in parallel, one paper each. The pipeline machine-checked every **quote** against the PDF, but nothing checked **numbers, page references, attributions or method details**. Errors in those parts could pass every gate. The explanations below are Claude's reading of the error patterns; they are inferences from the evidence, not a record of what the April agents did.

1. **Wrong number (49).** Values were retyped from text extracted from the PDF or read off charts. Dense tables lose their alignment when extracted as text, and small values such as ± standard deviations are easy to swap with a neighbour (e.g. SPOT Table 2, four SDs). Values read off figures (bar labels, plotted points) are approximate by nature.
2. **Not in the paper (33).** The page template required a full What / How / Who methods section for every EVD. When the paper was silent, agents filled the slot with plausible standard detail: a "McNemar test", "double-annotated" comments, a "1,000-paper subset", "21 items retained", "disagreements resolved by discussion". Language models complete patterns; the template rewarded completeness, and no step asked "where in the PDF does this say so?"
3. **Paper contradicts itself (19).** Several papers' prose disagrees with their own tables (an "average" that is one dataset's score; a "best" model that is not best in the table; n = 20 in the text but 30 cases in the supplement). Agents quoted the prose faithfully (which passes the quote check) and copied table values separately, with no step to reconcile the two. These are flagged with an added note, not by changing the quote.
4. **Wrong page reference (18).** Journals print article page numbers (e.g. p. 9347) that differ from PDF page positions; preprints have none; counting pages by hand drifts by one. The screenshot pipeline searches every page when the cited page misses, so a wrong page reference never caused a visible failure.
5. **Credited to the wrong model, rater or condition (17).** Values sit next to near-identical labels: human rater 1 vs rater 2, Claude 3 Opus vs Claude 3.5 Sonnet, "whole paper" vs "selected sections", OpenRouter vs a vendor API. Extracted table text and adjacent rows make it easy to attach a value to the wrong label.
6. **Missing comparator (8).** The atomicity rule (one finding per EVD) and the papers' own headline framing ("our model is best") led agents to report the winning row without checking the whole table. The row that contradicts the headline (e.g. GPT-4's higher micro-F1, a stronger baseline) was left out.
7. **Row or column shift (3).** `pdftotext -layout` interleaves two-column pages and misaligns wide tables, so a value lands one row or column away (e.g. "Always Reject" showing "Random Decision"'s value).

> [!tip] What prevents each of these next time
> Now written into `Skill.md` Step 6b and `Skill-references.md` (Common pitfalls). In short: cite the PDF page and table for every number; read tables from the rendered page image; never fill a methods slot the paper does not support (write "Not reported"); check the whole table before "best"; when prose and table disagree, use the table and add a note; cite printed page numbers and check them; keep the exact PDF version; use a fresh-context checker; fix every downstream copy.

## Zhang & Abernethy: update from arXiv v1 to v3

> [!important] What the v3 update does and does not change
> At JP's request the three Zhang & Abernethy pages are moved from arXiv v1 (28 May 2025) to **v3 (arXiv:2505.23824v3, 1 Apr 2026)**, the vault's current PDF. Only tables, Other Notes and Methods Context prose change (38 proposals, prefixed `z`). **Titles, quotes, screenshots and the Description summary lines keep their v1 numbers**, because JP is still benchmarking them; each page gets a "Version update 2026-11-17" note saying so.
> - Why the numbers moved: v3 swapped the Gemini 2.5 Pro judge version (preview-05-06 to preview-06-05), which made the o3 judge much stricter, so every hit rate fell (o3 64.9% to 48.2% on PDFs; o4-mini 59.6% to 38.0%; Claude 3.7 Sonnet 16.3% to 11.0%). v3 also re-priced o3 at June 2025 rates ($0.321 to $0.064 per paper) and added an AP@5 precision metric.
> - Consequence for the o4-mini page: v3 drops the "most cost-effective" claim, and Gemini 2.5 Flash matches o4-mini's hit rate for less. The page's title finding is much weaker in v3.
> - Some verbatim quotes on these pages no longer appear in v3 (e.g. "o4-mini seems to be the most cost-effective choice"). They are left as is and flagged.


## Proposed changes, by paper

### akyonEvaluatingCapabilitiesGenerative2024

#### [[EVD - GPT 4-0613 was lowest on STROBE questions at 44.1%]]

- [ ] **Change 124** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf#page=12|Akyon et al. - 2024 - Evaluating the capabilities of generat p. 12]]
    - Auditor evidence: PDF p12, Table 2: 'GPT 4-0613 13th June 2023 OpenAI September 2021'; 'GPT 4-1106 6 November 2023'; text on same page: 'ChatGPT 4-0613 (6th November version)'
    - Checker: Akyon LLMs section text: '3.5-turbo 1106 (11th June version), ChatGPT 4-0613 (6th November version), ChatGPT 4-1106 (11th June version)' vs Table 2: GPT 3.5-turbo and GPT 4-1106 6 November 2023, GPT 4-0613 13th June 2023.
```diff
- The authors discuss that compression techniques used in developing newer model versions (e.g., quantization, pruning) may have inadvertently compromised performance of GPT 4-0613 relative to GPT 3.5-turbo despite being a newer model generation.
+ The authors discuss that compression techniques used in developing newer model versions (e.g., quantization, pruning) may have inadvertently compromised performance of GPT 4-0613 relative to GPT 3.5-turbo despite being a newer model generation.
+ - PDF check 2026-11-17: the paper's version dates conflict. The Results text says '3.5-turbo 1106 (11th June version), ChatGPT 4-0613 (6th November version), ChatGPT 4-1106 (11th June version)', but Table 2 lists GPT 3.5-turbo and GPT 4-1106 as 6 November 2023 and GPT 4-0613 as 13th June 2023.
```

#### [[EVD - LLMs were least accurate on software and funding questions]]

- [ ] **Change 121** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf#page=10|Akyon et al. - 2024 - Evaluating the capabilities of generat p. 10]]
    - Auditor evidence: PDF p10-11, Table 1: Q15 'Is the funding of the study mentioned in the article? 1: yes 2: no'; Q2 has 4 options, Q8 has 7; 'This list of fifteen questions, two multiple-choice, and thirteen yes/no questions'
    - Checker: Akyon Table 1 (pp.10-11): Q15 'Is the funding of the study mentioned in the article? 1: yes 2: no'; Q2 (4 options) and Q8 (7 options) are the two multiple-choice items per 'two multiple-choice, and thirteen yes/no questions'.
```diff
- Q8 (statistical software identification) and Q15 (funding) were multiple-choice questions with 7 and 2 options respectively, which may explain the lower performance.
+ Q8 (statistical software identification) was a multiple-choice question with 7 options, which may explain its lower performance; Q15 (funding) was a yes/no question (the two multiple-choice items are Q2 and Q8).
```

- [ ] **Change 122 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf#page=11|Akyon et al. - 2024 - Evaluating the capabilities of generat p. 11]]
    - Auditor evidence: PDF p11, Table 1: 'Q15. Is the funding of the study mentioned in the article? 1: yes 2: no'
    - Checker: Akyon Table 1 p.11 Q15 is a yes/no question about whether funding is mentioned.
```diff
- Q15=funding source [2 options]
+ Q15=funding mentioned [yes/no]
```

- [ ] **Change 123** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf#page=13|Akyon et al. - 2024 - Evaluating the capabilities of generat p. 13]]
    - Auditor evidence: PDF p13: 'Access issues with Claude v1 ... resulted in the exclusion of data from six articles, limiting the study's scope to 33 articles'; Table 3: Claude v1 total 4950 (= 33×15×10)
    - Checker: Akyon Results: Claude v1 limited to 33 articles; Table 3 Claude v1 total 4950 = 33x15x10 vs 5850 = 39x15x10 for others, so 5x390 + 330 = 2280 per question.
```diff
- 6 LLMs × 39 articles × 10 trials = ~2340 graded responses per STROBE question (somewhat lower for items where Claude v1 contributed only 33 articles).
+ 5 LLMs × 39 articles × 10 trials + Claude v1 × 33 articles × 10 trials = 2280 graded responses per STROBE question (Claude v1 was limited to 33 articles for every question).
```

### alharbiAutomatedAssessmentReporting2024

#### [[EVD - ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria]]

- [ ] **Change 125** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf#page=6|Alharbi and Asiri - 2024 - Automated Assessment of Reporting p. 6]]
    - Auditor evidence: page 6, Table 2: ChatGPT ≥ Human on every item (equal on items 1, 2, 5, 9, 10; higher on 3, 4, 6, 7, 8, 11, 12 e.g. '12. Registration ... 9 (45%) 8 (40%)')
    - Checker: Rendered Table 2 (p. 6): ChatGPT 'Reported' ≥ Human on all 12 PRISMA items; equal on items 1, 2, 5, 9, 10 and strictly higher on 3, 4, 6, 7, 8, 11, 12.
```diff
- in 9 of 12 PRISMA items, ChatGPT's "Reported" proportion ≥ humans'
+ in all 12 PRISMA items, ChatGPT's "Reported" proportion ≥ humans' (strictly higher in 7)
```

#### [[EVD - ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization]]

- [ ] **Change 126** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf|Alharbi and Asiri - 2024 - Automated Assessment of Reporting]]
    - Auditor evidence: pages 4-5, Table 1: only '9. Blinding 8 (40%) vs 9 (45%)' and '16. Trial registration 9 (45%) vs 11 (55%)' have ChatGPT below humans
    - Checker: Rendered Table 1 (pp. 4–5): ChatGPT is below humans only on 9 Blinding (8 vs 9) and 16 Trial registration (9 vs 11); it is equal or higher on the other 15 items.
```diff
- in 14 of 17 items, ChatGPT's "Reported" proportion ≥ humans'.
+ in 15 of 17 items, ChatGPT's "Reported" proportion ≥ humans' (lower only for blinding and trial registration).
```

- [ ] **Change 127** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf#page=4|Alharbi and Asiri - 2024 - Automated Assessment of Reporting p. 4]]
    - Auditor evidence: page 4, Table 1: '3. Trial design 40 ... 0.11 Reported 20 (100%) 16 (80%)'; text: 'perfect agreement in their assessment of the six checklist items (title identification, author details, trial design, ...)'
    - Checker: Rendered Table 1: both 20/20 only on items 1, 2, 5, 6, 15 (five items); 3 Trial design is 20 (100%) vs 16 (80%), p=0.11, although the p. 4 text lists trial design among six perfect-agreement items. The old text is a table cell, not a quote.
```diff
- | Items with perfect agreement (both 100%) | 6 / 17 |
+ | Items with perfect agreement (both 100%) | 5 / 17 per Table 1 (text says 6, counting trial design) |
```

- [ ] **Change 128** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf#page=4|Alharbi and Asiri - 2024 - Automated Assessment of Reporting p. 4]]
    - Auditor evidence: page 4, Table 1 item 3 'Trial design ... 20 (100%) 16 (80%) 0.11'; page 3 formula 'Total Score = (Total "Yes" Items/[19 − Total "NA" Items]) × 100'; page 4 '17-item checklist'
    - Checker: Table 1 item 3 (p. 4) is 20/20 vs 16/20, p=0.11, against the text's six-item list; the p. 3 RCT formula divides by '19 − Total NA' while p. 4 describes a 17-item checklist. The note is an added line, and the quote is unchanged.
```diff
- - Item 8 (randomization): ChatGPT reported 100% (20/20) of abstracts as reporting randomization details; humans rated only 55% (11/20) as reporting (p=0.001).
+ - Item 8 (randomization): ChatGPT reported 100% (20/20) of abstracts as reporting randomization details; humans rated only 55% (11/20) as reporting (p=0.001).
+ - PDF check 2026-11-17: the text lists trial design among the six perfect-agreement items, but Table 1 shows trial design at 20/20 (ChatGPT) vs. 16/20 (humans), p=0.11, so Table 1 supports only five perfect-agreement items. The RCT score formula also divides by 19 although the checklist has 17 items.
```

### bougieGenerativeAdversarialReviews2024a

#### [[EVD - GAR beat human reviewers on preference 0.684 vs 0.523]]

- [ ] **Change 96** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=11|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 11]]
    - Auditor evidence: page 11-12, §5.3: 'This f1 score is significantly higher than the 0.49 achieved by human reviewers ... paired t-tests at 95% confidence level (p < 0.002)'; §5.1/Table 1 report no test
    - Checker: §5.1/§5.2 and the Table 1/2 captions (p. 10–11) report Bradley-Terry scores with no significance test; 'paired t-tests ... (p < 0.002)' appears only in §5.3 (p. 11–12) for F1 vs the human 0.49.
```diff
- Statistical significance of pairwise differences validated via paired t-tests at p<0.002.
+ No significance test is reported for the preference rankings (the paper's p<0.002 belongs to the §5.3 F1-vs-human comparison).
```

- [ ] **Change 97** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=10|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 10]]
    - Auditor evidence: page 10-11, Table 1 and Table 2 captions mention only bold/underline for best/second-best; p<0.002 appears only in §5.3 for acceptance-prediction F1
    - Checker: Same as 96: the Table 1 and Table 2 captions mention only bold/underline, and no test is given for either preference ranking.
```diff
- | Significance | paired t-test p<0.002 | — |
+ | Significance | not reported | not reported |
```

#### [[EVD - GAR human-likeness 3.89-4.02 significantly beat all LLM baselines]]

- [ ] **Change 98 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=15|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 15]]
    - Auditor evidence: page 15, Table 7 has no caption note defining '*'; text: 'our method significantly outperforms AI-Scientist in generating reviews that align closely with human feedback' (no test or p-value given)
    - Checker: Table 7 (p. 15) carries * on the GAR values but has no caption note defining it (unlike Table 5, which defines * as t-test p<0.05); the §5.9 text says only that GAR 'significantly outperforms AI-Scientist'. The column count is preserved.
```diff
- | \* over best baseline | t-test p<0.05 | | |
+ | \* (not defined in Table 7; text says GAR "significantly outperforms AI-Scientist") | | | |
```

- [ ] **Change 99 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=14|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 14]]
    - Auditor evidence: page 14-15, §5.9 gives no paper count; '1,000 papers' appears for §5.3 (Table 3/4/9) and §5.8 (ICLR 2023 subset)
    - Checker: §5.9 (p. 14–15) states no paper count; '1,000 papers' belongs to §5.3 (Tables 3/4/9) and §5.8 (ICLR 2023 subset).
```diff
- the five reviewer agents generate reviews on a 1,000-paper subset;
+ the five reviewer agents generate reviews (the §5.9 sample size is not stated; 1,000 papers per dataset is the §5.3 setting);
```

#### [[EVD - GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49]]

- [ ] **Change 100** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=12|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 12]]
    - Auditor evidence: page 12, Table 4, ICLR 23: 'GAR (NN selected) 0.72±0.06 0.67±0.05'; 'GAR> (NN selected) 0.74±0.05 0.70±0.06'
    - Checker: Table 4 (p. 12), ICLR 23: GAR (NN selected) 0.72±0.06 / 0.67±0.05; GAR> (NN selected) 0.74±0.05 / 0.70±0.06.
```diff
- NN-optimised persona pushes ICLR 23 Balanced Acc to 0.74 ± 0.06 (GAR^> 0.74 ± 0.06 / F1 0.70 ± 0.06)
+ NN-optimised persona pushes ICLR 23 Balanced Acc to 0.72 ± 0.06 (GAR^> 0.74 ± 0.05 / F1 0.70 ± 0.06)
```

- [ ] **Change 101** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Bougie et al. - 2024 - Generative Adversarial Reviews.pdf#page=12|Bougie et al. - 2024 - Generative Adversarial Reviews.pdf p. 12]]
    - Auditor evidence: page 12, Table 4, ICLR 23: 'GAR (w/o memory) ... 0.61±0.05 0.52±0.06'
    - Checker: Table 4 (p. 12), ICLR 23: GAR (w/o memory) 0.61±0.05 / 0.52±0.06.
```diff
- removing the memory module drops it to 0.61 ± 0.06 / 0.52 ± 0.05
+ removing the memory module drops it to 0.61 ± 0.05 / 0.52 ± 0.06
```

### darcyMARGMultiAgentReview2024

#### [[EVD - MARG-S beat baselines by 6.1 recall points on ARIES]]

- [ ] **Change 37** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf|D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation fo]]
    - Auditor evidence: Table 2: SARG-B, SARG-TP, MARG-TP, LiZCa, MARG-S, no refinement, experiments-only, clarity-only, impact-only, Human = 10 rows
    - Checker: Table 2 (automated eval) lists 10 rows: SARG-B, SARG-TP, MARG-TP, LiZCa, MARG-S, 4 MARG-S ablations, Human. 5+4+1 = 10, not 11.
```diff
- 11 method conditions evaluated on all 30 papers (5 main methods + 4 MARG-S ablations + Human baseline)
+ 10 method conditions evaluated on all 30 papers (5 main methods + 4 MARG-S ablations + Human baseline)
```

- [ ] **Change 38 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf#page=1|D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation fo p. 1]]
    - Auditor evidence: Table 2: "SARG-TP 10.62 4.61 3.46 11.6", "LiZCa 9.67 9.96 5.58 4.0", "MARG-S 15.84 4.41 3.53 19.8"; p.1 "outperforms the strongest baseline by 6.1 recall points"
    - Checker: Table 2: MARG-S recall 15.84, LiZCa 9.67 (gap 6.17), SARG-TP 10.62 (gap 5.22); abstract p.1 says 'outperforms the strongest baseline by 6.1 recall points'. The added note is accurate and leaves the quote alone.
```diff
- - MARG-S generates ~5× the comments of LiZCa (19.8 vs. 4.0)
+ - PDF check 2026-11-17: the abstract's "outperforms the strongest baseline by 6.1 recall points" matches the gap to LiZCa (15.84 − 9.67 = 6.17), but the highest-recall baseline in Table 2 is SARG-TP (10.62), a gap of 5.22.
+ - MARG-S generates ~5× the comments of LiZCa (19.8 vs. 4.0)
```

#### [[EVD - MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4]]

- [ ] **Change 39 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf|D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation fo]]
    - Auditor evidence: Sec 7.2: "MARG-S generates more good comments than SARG-B (p=0.09, related-sample t-test) and LiZCa (p=0.003)"; Sec 7.3: "MARG-S has the highest proportion of 'good' comments, and is significantly better than SARG-B (p=0.02 for per-comment Barnard's exact test, p=0.12 for per-user related sample t-test)"
    - Checker: Sec 7.3 attaches p=0.02/0.12/0.09/0.16 to the proportion of 'good' comments; Sec 7.2 gives the good-comment count tests (SARG-B p=0.09 related-sample t-test, LiZCa p=0.003).
```diff
- - MARG-S vs. SARG-B difference in good-comment count significant per Barnard's exact test (p=0.02 per-comment) but not per-user (p=0.12); MARG-S vs. LiZCa not significant (p=0.09 per-comment, p=0.16 per-user).
+ - Proportion of "good" comments (Sec 7.3): MARG-S vs. SARG-B significant per Barnard's exact test (p=0.02 per-comment) but not per-user (p=0.12); MARG-S vs. LiZCa not significant (p=0.09 per-comment, p=0.16 per-user). Total good-comment count per review (Sec 7.2, related-sample t-test): MARG-S vs. SARG-B p=0.09, vs. LiZCa p=0.003.
```

- [ ] **Change 40** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf|D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation fo]]
    - Auditor evidence: Sec 7.2: "MARG-S generates more good comments than SARG-B (p=0.09, related-sample t-test) and LiZCa (p=0.003)"; the p=0.02/0.12/0.09/0.16 values in Sec 7.3 refer to the proportion of good comments
    - Checker: Same as 39: Sec 7.3 p-values are for the proportion of good comments, and Sec 7.2 gives count-per-review p=0.09 (SARG-B) and p=0.003 (LiZCa).
```diff
- | MARG-S vs. SARG-B good comments (Barnard's exact, per-comment) | p=0.02 |
- | MARG-S vs. SARG-B good comments (related-sample t-test, per-user) | p=0.12 |
- | MARG-S vs. LiZCa good comments (per-comment) | p=0.09 |
- | MARG-S vs. LiZCa good comments (per-user) | p=0.16 |
+ | MARG-S vs. SARG-B good-comment proportion (Barnard's exact, per-comment) | p=0.02 |
+ | MARG-S vs. SARG-B good-comment proportion (related-sample t-test, per-user) | p=0.12 |
+ | MARG-S vs. LiZCa good-comment proportion (per-comment) | p=0.09 |
+ | MARG-S vs. LiZCa good-comment proportion (per-user) | p=0.16 |
+ | MARG-S vs. SARG-B good-comment count per review (related-sample t-test) | p=0.09 |
+ | MARG-S vs. LiZCa good-comment count per review | p=0.003 |
```

### hasanIntegratingLargeLanguage2024

#### [[EVD - GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I]]

- [ ] **Change 146** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Hasan et al_2024_Integrating large language models in systematic reviews.pdf#page=3|Hasan et al_2024_Integrating large language models in system p. 3]]
    - Auditor evidence: page 3, Table 1: "Per cent agreements 47% 46% 71% 31% 37% 42% 36% 61%" (D4 = 31% is lowest)
    - Checker: p. 3 Table 1 per cent agreements: D1 47%, D2 46%, D3 71%, D4 31%, D5 37%, D6 42%, D7 36%. D4 (31%) is the lowest, not D1.
```diff
- D1 (confounding) the lowest (47%)
+ D4 (deviations from intended interventions) the lowest (31%)
```

### huntington-kleinLLMsActRepositories2024

#### [[EVD - LLMs flagged expert and trimmed confounders at similar rates]]

- [ ] **Change 102 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Huntington-Klein and Murray - 2024. - Do LLMs Act as Repositories of Causal Knowledge.pdf#page=8|Huntington-Klein and Murray - 2024. - Do LLMs Act as Reposit p. 8]]
    - Auditor evidence: page 8, Figure 1 (direct method), 'Added in 2016' row: Claude 3.5 100% bar = 30%, GPT-4o = 50%, GPT-o1 = 30% (GPT-o1 70% at 0%); text p. 9: 'with only GPT-4o including even 50% of them'
    - Checker: Rendered p. 8 Figure 1 (direct), 'Added in 2016' row: 100% bars are Claude 3.5 30%, GPT-4o 50%, GPT-o1 30% (o1 has 70% at 0%); p. 9 text: 'only GPT-4o including even 50% of them'.
```diff
- | Added in 2016 | 50% at 100% | 50% at 100% | 80% at 100% |
+ | Added in 2016 | 30% at 100% | 50% at 100% | 30% at 100% |
```

- [ ] **Change 103 ⚑** · Credited to the wrong model, rater or condition · checker: MODIFY · PDF: [[source/pdfs/Huntington-Klein and Murray - 2024. - Do LLMs Act as Repositories of Causal Knowledge.pdf#page=7|Huntington-Klein and Murray - 2024. - Do LLMs Act as Reposit p. 7]]
    - Auditor evidence: page 7, Table 1: 'Claude 3.5 59.9%' under 'Is Confounder (Dir.)' for all variables; page 8, Figure 1, Claude 3.5 'Original' 100% bar = 90%
    - Checker: p. 7 Table 1 gives 59.9% for 'all the confounders' pooled, and rendered p. 8 Fig 1 shows Claude 3.5 Original = 90% at 100%, so the correction is right. But '172 candidate variables' is not stated for Table 1 (the Non-Confounder responses were collected separately, p. 7), so I dropped that count.
```diff
- Direct method: Claude 3.5 designated 59.9% of "Original" confounders as confounders;
+ Direct method: Claude 3.5 designated 59.9% of all variables in Table 1 as confounders (pooled across confounder sets, not the "Original" set) and 90% of "Original" confounders 100% of the time (Fig 1);
```

- [ ] **Change 104 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Huntington-Klein and Murray - 2024. - Do LLMs Act as Repositories of Causal Knowledge.pdf#page=9|Huntington-Klein and Murray - 2024. - Do LLMs Act as Reposit p. 9]]
    - Auditor evidence: page 9, in the Figure 1 (direct method) discussion: 'even in this case only about 70% of confounders in their final causal diagram were designated by LLMs as confounders'; indirect Figure 2 values are 86% / 49% / 92%
    - Checker: p. 9: 'only about 70% of confounders in their final causal diagram were designated by LLMs' appears in the Figure 1 (direct method) discussion; rendered Fig 1 Final Expert DAG 100% bars are 69/76/71%.
```diff
- | Final Expert DAG (indirect, all models) | ≈70% |
+ | Final Expert DAG (direct, all models) | ≈70% |
```

### leucutaRiskBiasAssessment2025

#### [[EVD - Four LLMs averaged 72.95% correct on QUADAS-2]]

- [ ] **Change 142** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Leucuta et al. 2025 - Risk of Bias Assessment of Diagnositic Accuracy Studies.pdf#page=9|Leucuta et al. 2025 - Risk of Bias Assessment of Diagnositic p. 9]]
    - Auditor evidence: page 9, Table 2: "x.AI Grok 3 85/110 (77.27)"; same page text: "ranging from 74.45% to 67.27%"
    - Checker: Leucuta p.9 Table 2: Grok 3 85/110 (77.27), and the four values average to 72.95; the abstract and p.9 text say 'ranging from 74.45% to 67.27%'; Discussion gives Grok 3 77.27%.
```diff
- By domain: Flow and timing was highest (80.63%), then index test (73.75%), then patient selection (65.83%) and reference standard (63.75%). The percentage of answers that were correct but with incorrect reasoning was 2.95% overall, highest in index test domain (5%).
+ By domain: Flow and timing was highest (80.63%), then index test (73.75%), then patient selection (65.83%) and reference standard (63.75%). The percentage of answers that were correct but with incorrect reasoning was 2.95% overall, highest in index test domain (5%).
+ - PDF check 2026-11-17: the paper's Results text gives the model range as "74.45% to 67.27%", but Table 2 (p. 9) and the Discussion give Grok 3 as 85/110 (77.27%); the table value is used here.
```

### liangCanLargeLanguage2024a

#### [[EVD - GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans]]

- [ ] **Change 89 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf#page=17|Liang et al. - 2024 - Can Large Language Models Provide Usef p. 17]]
    - Auditor evidence: page 17, Figure 3: Ethical Aspects point sits slightly right of the 0 line (log ratio ~+0.1), not below it; only Theoretical Soundness, Missing Citations, Add ablations and Novelty are negative
    - Checker: Rendered Figure 3 (p. 17): Ethical Aspects sits just right of 0 (log ratio about +0.1, similar to Clarity, which the page calls ≈1×); only Theoretical Soundness, Missing Citations, ablations and Novelty are negative.
```diff
- | Theoretical Soundness, Missing Citations, Ethical Aspects | < 1× | human > GPT-4 (smaller gaps) |
+ | Theoretical Soundness, Missing Citations | < 1× | human > GPT-4 (smaller gaps) |
+ | Ethical Aspects | ≈ 1× (slightly > 1) | comparable |
```

- [ ] **Change 90 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf#page=10|Liang et al. - 2024 - Can Large Language Models Provide Usef p. 10]]
    - Auditor evidence: page 10: 'To ensure annotation reliability, two researchers with a background in machine learning performed the annotations.' (no statement that every comment was coded by both)
    - Checker: Methods (p. 10): 'To ensure annotation reliability, two researchers with a background in machine learning performed the annotations.' Nothing says each comment was coded by both.
```diff
- each comment double-annotated by **2 ML-background annotators**
+ comments annotated by **2 ML-background annotators** (the paper does not say each comment was double-coded)
```

#### [[EVD - GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human]]

- [ ] **Change 91 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf#page=16|Liang et al. - 2024 - Can Large Language Models Provide Usef p. 16]]
    - Auditor evidence: page 16, Figure 2 caption: 'Error bars represent 95% confidence intervals. *P < 0.05, **P < 0.01, ***P < 0.001, and ****P < 0.0001.' No McNemar test anywhere in the paper
    - Checker: Figure 2 caption (p. 16) gives 95% CI error bars and the */**/***/**** P thresholds without naming a test; 'McNemar' does not appear anywhere in the PDF text.
```diff
- (5) McNemar / paired comparisons reported with 95% CIs and *P < 0.0001 in Fig. 2a.
+ (5) Fig. 2a reports 95% CI error bars and significance stars (****P < 0.0001); the statistical test is not named.
```

### liuReviewerGPTExploratoryStudy2023

#### [[EVD - GPT-4 detected errors in 7 of 13 constructed papers]]

- [ ] **Change 30 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Using Large Language Models for Paper Reviewing.pdf#page=5|Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Us p. 5]]
    - Auditor evidence: page 5: "Prompt-Parts does not provide the entire short paper at once, but instead provides parts of the paper a few sentences at a time. In particular, for the sentences where the main claims are made, each provided part comprises a single sentence."
    - Checker: p. 5: 'Prompt-Parts ... provides parts of the paper a few sentences at a time. In particular, for the sentences where the main claims are made, each provided part comprises a single sentence.'
```diff
- `Prompt-Parts` (paper provided one sentence at a time, asking the model to flag errors incrementally)
+ `Prompt-Parts` (paper provided a few sentences at a time, one sentence at a time for the main claims, asking the model to flag errors incrementally)
```

#### [[EVD - GPT-4 favored the worse abstract in 6 of 10 pairs]]

- [ ] **Change 31** · Paper contradicts itself (note added, quote untouched) · checker: MODIFY · PDF: [[source/pdfs/Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Using Large Language Models for Paper Reviewing.pdf#page=33|Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Us p. 33]]
    - Auditor evidence: page 33: "We created 13 pairs of research abstracts" vs same page "In this section we provide the 10 pairs of abstracts we constructed" and Table 3 (10 rows)
    - Checker: p. 33 Sec 5.1 says 13 pairs while Sec 5.2/5.3 on p. 33 and p. 2 say 10, so a note is right; but the page's own quote of that sentence already says 10, so the note must say the PDF reads 13 rather than 'the sentence quoted above says 13'.
```diff
- - For the bombastic-language pair, GPT-4 was swayed in 2 of 3 responses.
+ - For the bombastic-language pair, GPT-4 was swayed in 2 of 3 responses.
+ - PDF check 2026-11-17: in the PDF, the Section 5.1 sentence on p. 33 quoted above reads "We created 13 pairs of research abstracts" (the quote above gives 10), but p. 2, Section 5.2 ("6 of the 10 cases") and Section 5.3 on the same page ("the 10 pairs of abstracts we constructed") all describe 10 pairs; 13 appears to be carried over from the 13 short papers of Section 3.
```

### louAAAR10AssessingAIs2025

#### [[EVD - Claude Opus led AAAR ReviewCritique at 21.99% F1]]

- [ ] **Change 23** · Row or column shift · checker: ACCEPT · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=11|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 11]]
    - Auditor evidence: page 11, Table 7 Llama3-8B: "7.73 / 45.95 / 12.22 | 11.47 / 30.29 / 14.88 | 11.37 / 21.27 / 12.46 | 8.19 / 53.61 / 13.35" (Select-Deficient F1 14.88 is highest)
    - Checker: p. 11 Table 7 Llama3-8B row: Select-Deficient 11.47/30.29/14.88 is the highest F1 for that model; Both "No" is only 12.46.
```diff
- | Llama3-8B: Both "No" (best for 8B) | 11.37 / 21.27 / 12.46 |
+ | Llama3-8B: Select-Deficient (best for 8B) | 11.47 / 30.29 / 14.88 |
```

- [ ] **Change 24 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=11|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 11]]
    - Auditor evidence: page 11, Table 7: "From (Du et al., 2024)... Claude Opus (Anthropic, 2024b)"; references: "claude-3-family, March 2024b"; App B.2 p.16 lists claude-3-5-sonnet-20240620 for the paper's own experiments
    - Checker: p. 11 Table 7 caption says 'From (Du et al., 2024)' and cites Claude Opus to Anthropic 2024b, which the p. 12 references list as claude-3-family, March 2024; App. B.2 (p. 16) lists claude-3-5-sonnet-20240620 for the authors' own runs.
```diff
- claude-3-5-sonnet-20240620 (paper labels best result as "Claude Opus" in Table 7)
+ claude-3-5-sonnet-20240620 (used for the paper's own tasks; Table 7's "Claude Opus" is reproduced from Du et al. 2024 and cited to Anthropic's March 2024 Claude 3 family)
```

- [ ] **Change 25 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=10|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 10]]
    - Auditor evidence: page 10: "We put the results of Du et al. (2024) in Table 7"; App B.2 p.16: "we run each model thrice during our experiments"
    - Checker: p. 10: 'We put the results of Du et al. (2024) in Table 7'; the 'run each model thrice' rule is in App. B.2 p. 16 and describes the AAAR experiments.
```diff
- for each (model × prompt-strategy) cell of Table 7; each model was run three times and the median result reported.
+ for each (model × prompt-strategy) cell of Table 7. Table 7 is reproduced from Du et al. (2024); the run-thrice/median rule in App. B.2 describes the AAAR authors' own runs.
```

- [ ] **Change 26 ⚑** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=10|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 10]]
    - Auditor evidence: Sentence "Claude Opus achieves the highest F1 scores" appears in Sec 5.4 on printed page 10; Table 7 is on page 11
    - Checker: The sentence 'Claude Opus achieves the highest F1 scores...' is in the right column of p. 10 (Main results), before the page-10 footer; Table 7 starts p. 11.
```diff
- Claude Opus achieves the highest F1 scores, with GPT-4 and Gemini 1.5 performing slightly worse." (Lou et al., 2025, p. 11)
+ Claude Opus achieves the highest F1 scores, with GPT-4 and Gemini 1.5 performing slightly worse." (Lou et al., 2025, p. 10)
```

- [ ] **Change 27 ⚑** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=6|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 6]]
    - Auditor evidence: "We reuse the REVIEWCRITIQUE dataset ... resulting in 11,376 review segments" is in Sec 3.4 on printed page 6
    - Checker: The '...resulting in 11,376 review segments (viewpoints)' sentence is in Sec 3.4 on p. 6.
```diff
- resulting in 11,376 review segments (viewpoints)." (Lou et al., 2025, p. 10)
+ resulting in 11,376 review segments (viewpoints)." (Lou et al., 2025, p. 6)
```

#### [[EVD - o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline]]

- [ ] **Change 28** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=3|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 3]]
    - Auditor evidence: page 3: "We then eliminate the positive equation and its negative counterparts, where all three negative counterparts are unaligned. This filtering leads to a final of 1,449 positive equations and 4,347 negative equations"
    - Checker: p. 3: 'We then eliminate the positive equation and its negative counterparts, where all three negative counterparts are unaligned. This filtering leads to a final of 1,449 positive equations and 4,347 negative equations'.
```diff
- GPT-4 used to remove context-unaligned negatives; pairs where any negative was unaligned were dropped.
+ GPT-4 used to remove context-unaligned negatives; a positive equation and its negatives were dropped only where all three negatives were unaligned (→ 1,449 positive + 4,347 negative).
```

- [ ] **Change 29 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf#page=20|Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Ass p. 20]]
    - Auditor evidence: page 20, Figure 4 (rendered): Qwen-2.5 points rise from ~26.5 to ~30.9 at 1,100 words then fall to ~27; Llama-3.1 ~35.2 at 500, ~34.7 at 700
    - Checker: Rendered p. 20 Figure 4: GPT-4o 38.9-40.9; Llama-3.1 ~35.2 at 500 and ~34.7 at 700; Qwen-2.5 ~26.5 rising to ~30.9 at 1,100 then ~27. The page's 'Qwen stays ~26' is wrong.
```diff
- GPT-4o F1 stays ~40 across 100–1,500 words; Llama-3.1 peaks ~35 at 700 words; Qwen-2.5 stays ~26.
+ GPT-4o F1 stays ~39–41 across 100–1,500 words; Llama-3.1 peaks ~35 at 500–700 words; Qwen-2.5 ranges ~26–31 (peak ~31 at 1,100 words).
```

### robertsComparativeStudyChatGPT2023

#### [[EVD - ChatGPT and humans differed by 4.92% on CONSORT-A compliance]]

- [ ] **Change 116 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf#page=3|Roberts et al. 2023 - Comparative study of ChatGPT and human p. 3]]
    - Auditor evidence: page 3, Figure 2 caption: 'Bland-Altman analysis between ChatGPT human evaluation. OCS, overall compliance score.' (no numeric value)
    - Checker: Rendered p. 3: the Figure 2 caption reads 'Bland-Altman analysis between ChatGPT human evaluation. OCS, overall compliance score.' with no number; 4.92% appears in the abstract and Results.
```diff
- The point estimate of 4.92% is consistent across abstract, results, and figure caption.
+ The point estimate of 4.92% is consistent across abstract and results; the Figure 2 caption gives no value.
```

#### [[EVD - ChatGPT diverged most on CONSORT-A conclusions by 0.764]]

- [ ] **Change 117** · Paper contradicts itself (note added, quote untouched) · checker: MODIFY · PDF: [[source/pdfs/Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf#page=3|Roberts et al. 2023 - Comparative study of ChatGPT and human p. 3]]
    - Auditor evidence: page 3, Table 1 (rendered): P value column reads '0.001' for Participants, Intervention, Objective, Outcome (methods), Randomisation, Outcome (reporting), Harms, Conclusion, Funding; Methods: 'P<0.001 was deemed statistically significant'; page 4 prose: 'harms (r=0.32, p<0.001)'
    - Checker: Rendered p. 3 Table 1 confirms P = 0.001 and Methods 'P<0.001 was deemed statistically significant', but only 9 domains show 0.001 (Participants, Intervention, Objective, Outcome (methods), Randomisation, Outcome (reporting), Harms, Conclusion, Funding), not 10.
```diff
- - Authors hypothesise prompt quality and ChatGPT's known instruction-following weaknesses as causes of the conclusion-domain divergence; no follow-up prompt-engineering experiments performed.
+ - Authors hypothesise prompt quality and ChatGPT's known instruction-following weaknesses as causes of the conclusion-domain divergence; no follow-up prompt-engineering experiments performed.
+ - PDF check 2026-11-17: Table 1 (p. 3) prints P = 0.001, not <0.001, for 9 domains (incl. conclusion, randomisation, objective, intervention, harms); the prose reports p<0.001, and under the authors' own P<0.001 threshold a P of 0.001 would not strictly count as significant. The "<0.001" cells in the table below follow the prose, not Table 1.
```

#### [[EVD - ChatGPT-human correlation weakest on CONSORT-A intervention and objective]]

- [ ] **Change 118** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf#page=3|Roberts et al. 2023 - Comparative study of ChatGPT and human p. 3]]
    - Auditor evidence: page 3, Table 1: Funding r 0.21, Participants r 0.26; Methods: 'r, 0–0.19 very weak, 0.2–0.39 weak'
    - Checker: Rendered p. 3 Table 1 r values plus Methods bands ('0–0.19 very weak, 0.2–0.39 weak'): exactly 7 of 14 domains are below 0.2, and funding 0.21 and participants 0.26 are weak.
```diff
- - Most domains have r values in the very-weak range (<0.2): intervention 0.02, number analysed 0.04, objective 0.06, conclusion 0.06, randomisation 0.11, outcome (methods) 0.14, outcome (reporting) 0.15, funding 0.21, participants 0.26.
+ - Half the domains (7 of 14) have r values in the very-weak range (<0.2): intervention 0.02, number analysed 0.04, objective 0.06, conclusion 0.06, randomisation 0.11, outcome (methods) 0.14, outcome (reporting) 0.15; funding 0.21 and participants 0.26 fall in the weak band.
```

- [ ] **Change 119** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf#page=3|Roberts et al. 2023 - Comparative study of ChatGPT and human p. 3]]
    - Auditor evidence: page 3, Table 1: Objective r 0.06, Conclusion r 0.06, Number analysed r 0.04
    - Checker: Rendered p. 3 Table 1: Objective r 0.06, Conclusion 0.06, Number analysed 0.04, so objective is tied with conclusion and above number analysed; the prose (p. 3-4) calls intervention and objective the weakest.
```diff
- | **Objective (weakest tied)** |
+ | **Objective (called weakest in prose; tied with conclusion, above number analysed)** |
```

- [ ] **Change 120** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf#page=3|Roberts et al. 2023 - Comparative study of ChatGPT and human p. 3]]
    - Auditor evidence: page 3, Table 1: 'Number analysed ... 0.434 0.04'; 'Objective ... 0.001 0.06'; 'Conclusion ... 0.001 0.06'; page 4 prose: ''intervention' (r=0.02, p<0.001) and 'objective' (r=0.06, p<0.001) domains had very weak correlations'
    - Checker: Rendered p. 3 Table 1: Number analysed r 0.04 < Objective 0.06 = Conclusion 0.06, and the P column prints 0.001 for intervention/objective/harms etc., while the prose gives p<0.001. Genuine inconsistencies, added as a note.
```diff
- - The combination of low Pearson r and small mean differences
+ - PDF check 2026-11-17: the paper names 'intervention' and 'objective' as the weakest correlations, but its Table 1 shows number analysed (r=0.04) below objective (r=0.06), and conclusion ties objective at 0.06. Table 1 also prints P = 0.001 (not <0.001) for intervention, objective, harms and other domains, while the prose reports p<0.001.
+ - The combination of low Pearson r and small mean differences
```

### sarolAssessingCitationIntegrity2024

#### [[EVD - Annotator agreement on citation labels was only kappa 0.18-0.31]]

- [ ] **Change 41** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sarol et al. - 2024 - Assessing citation integrity.pdf#page=5|Sarol et al. - 2024 - Assessing citation integrity.pdf p. 5]]
    - Auditor evidence: page 5, Section 3.2: "over the first two phases of annotation (30 reference articles). We obtained high agreement on citation context annotation (κ = 0.96)" — one pooled value, no per-phase split
    - Checker: Sarol p.5 Sec 3.2: kappa 0.96 for citation context computed over first two phases, one pooled value.
```diff
- | Citation-context identification | 0.96 | 0.96 |
+ | Citation-context identification | 0.96 (phases 1–2 pooled; not reported per phase) | 0.96 (pooled) |
```

- [ ] **Change 42 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sarol et al. - 2024 - Assessing citation integrity.pdf#page=5|Sarol et al. - 2024 - Assessing citation integrity.pdf p. 5]]
    - Auditor evidence: page 5, Section 3.2: "the agreement improved in the second phase to fair agreement levels (evidence sentence: 0.20 in the first phase to 0.37 in the second; accuracy labels: 0.18–0.31)" — the parallel wording suggests 0.18 (phase 1) to 0.31 (phase 2), but it is not stated; the page shows the full range in each phase column
    - Checker: Sarol p.5 Sec 3.2: 'accuracy labels: 0.18-0.31' given as one range without phase assignment.
```diff
- | Citation-accuracy classification (8-way) | **0.18–0.31** | **0.18–0.31** |
+ | Citation-accuracy classification (8-way) | **0.18–0.31** (single range; paper does not assign values to phases) | **0.18–0.31** (same range) |
```

- [ ] **Change 43 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sarol et al. - 2024 - Assessing citation integrity.pdf#page=6|Sarol et al. - 2024 - Assessing citation integrity.pdf p. 6]]
    - Auditor evidence: page 6, Discussion 4.1: "other datasets which link citation sentences to reference article sentences often have low inter-annotator agreement (0.16–0.52)"; 0.18–0.31 is below that range's midpoint (0.34)
    - Checker: Sarol p.6 Discussion: comparable datasets 0.16-0.52; 0.18-0.31 lies below the midpoint 0.34, so 'lower half' not 'middle'.
```diff
- so the Sarol corpus sits in the middle of that range.
+ so the Sarol corpus (0.18–0.31) sits in the lower half of that range.
```

### shahidLiteratureGroundedNoveltyAssessment2025

#### [[EVD - AI Scientist reached 0.47 accuracy on novelty test set]]

- [ ] **Change 44** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=6|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 6]]
    - Auditor evidence: page 6 (PDF page 6, Section 6.1, right column): "Our approach achieved over 10 times more agreement with expert-labeled examples compared to AI Scientist"; the screenshot embed for this quote is already named evd-p6-1
    - Checker: The 'over 10 times more agreement ... 13% higher agreement than AI Researcher' sentence is in the right column of Sec 6.1 on PDF p. 6 (page 7 begins with Table 1).
```diff
- approximately 13% higher agreement than AI Researcher." (Shahid et al., 2025, p. 7)
+ approximately 13% higher agreement than AI Researcher." (Shahid et al., 2025, p. 6)
```

- [ ] **Change 45** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=6|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 6]]
    - Auditor evidence: page 6, Section 6.1: "AI Scientist defaults to \"not novel\" when it fails to reach a conclusion in novelty evaluation (18 out of 32 times)"; embed is evd-p6-6
    - Checker: The 'defaults to "not novel" ... (18 out of 32 times), which may have impacted its agreement rates' sentence is on p. 6, Sec 6.1.
```diff
- which may have impacted its agreement rates." (Shahid et al., 2025, p. 7)
+ which may have impacted its agreement rates." (Shahid et al., 2025, p. 6)
```

- [ ] **Change 46** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=3|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 3]]
    - Auditor evidence: page 3, Section 3: "evaluated 51 ideas, comprising of 34 new ones generated by Radensky et al. and 17 from the previous study where external knowledge had influenced novelty judgments" (the first-round study used 46 Scideator + 5 OpenReview ideas)
    - Checker: p. 3 Sec 3: second round 'evaluated 51 ideas, comprising of 34 new ones generated by Radensky et al. and 17 from the previous study'; the OpenReview ICLR'22/NeurIPS'23 ideas belong to the first round (46 Scideator + 5 OpenReview).
```diff
- formative-study pool of 51 ideas (34 Scideator + 17 OpenReview ICLR'22/NeurIPS'23)
+ formative-study pool of 51 ideas (34 new Scideator ideas + 17 carried over from the first-round study)
```

- [ ] **Change 47** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=2|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 2]]
    - Auditor evidence: page 2: "If such a decision is not reached, the idea is automatically considered novel." vs page 6: "AI Scientist defaults to \"not novel\" when it fails to reach a conclusion"
    - Checker: p. 2 Related Work: 'If such a decision is not reached, the idea is automatically considered novel' vs p. 6 Sec 6.1: 'AI Scientist defaults to "not novel" when it fails to reach a conclusion'. A genuine self-contradiction, handled as an added note.
```diff
- - AI Scientist defaulted to "not novel" in **56% of test cases (18/32)**, inflating agreement with the not-novel class but suppressing accuracy and κ.
+ - AI Scientist defaulted to "not novel" in **56% of test cases (18/32)**, inflating agreement with the not-novel class but suppressing accuracy and κ.
+ - PDF check 2026-11-17: the paper contradicts itself on AI Scientist's default. Related Work (p. 2) says "If such a decision is not reached, the idea is automatically considered novel", while Section 6.1 (p. 6) says it "defaults to 'not novel'". The Methods text above follows p. 6.
```

#### [[EVD - Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79%]]

- [ ] **Change 48** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=6|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 6]]
    - Auditor evidence: page 6–7, Section 6.2: "(ii) RankGPT Relevance: ... replaced the facet-based RankGPT re-ranker with one based on general relevance"; "(iii) Embedding Filtering: Omits the LLM re-ranker entirely, relying only on the embedding-based filtering"; Table 2 p. 7: "- Relevance RankGPT 13.79%", "- Embedding Filtering 10.34%"
    - Checker: p. 6-7 Sec 6.2: (ii) RankGPT Relevance 'replaced the facet-based RankGPT re-ranker with one based on general relevance'; (iii) Embedding Filtering 'Omits the LLM re-ranker entirely'; Table 2 p. 7: 13.79% and 10.34%.
```diff
- removing RankGPT relevance re-ranker: 13.79%; removing embedding filtering: 10.34%.
+ replacing facet-based RankGPT with general-relevance RankGPT: 13.79%; embedding filtering only (no LLM re-ranker): 10.34%.
```

- [ ] **Change 49** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=7|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 7]]
    - Auditor evidence: page 7, Table 2: "Complete System 89.66% / - Relevance RankGPT 13.79% / - Embedding Filtering 10.34%"; text: "combining facet-based reranking with embedding is critical"
    - Checker: p. 7 Table 2: Complete 89.66%, -Relevance RankGPT 13.79%, -Embedding Filtering 10.34%, so the page's claim that dropping the re-ranker is 'far more harmful' than swapping is backwards; the new wording follows the numbers.
```diff
- removing the LLM re-ranker (embedding-only) is far more harmful than swapping facet-based for general-relevance, indicating that retrieval-stage LLM re-ranking is the dominant performance driver and facet-awareness adds a smaller second-order gain.
+ swapping facet-based for general-relevance RankGPT already drops accuracy from 89.66% to 13.79%, and removing the LLM re-ranker entirely (embedding-only) lowers it only slightly further to 10.34%, so the facet-based criterion, not LLM re-ranking as such, accounts for nearly all of the gain.
```

#### [[EVD - Idea Novelty Checker reached 0.81 accuracy beating baselines]]

- [ ] **Change 50** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=3|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 3]]
    - Auditor evidence: page 3, Section 3: first round "51 ideas, comprising of 46 generated by the Scideator system ... and 5 adapted from accepted and rejected papers from OpenReview (ICLR 22, NeurIPS 23)"; second round "51 ideas, comprising of 34 new ones generated by Radensky et al. and 17 from the previous study"
    - Checker: p. 3 Sec 3: first round '51 ideas, comprising of 46 generated by the Scideator system ... and 5 adapted from ... OpenReview (ICLR 22, NeurIPS 23)'; second round '34 new ones ... and 17 from the previous study'.
```diff
- formative-study pool of **51 ideas** (34 generated by Scideator (Radensky et al.); 17 from accepted/rejected OpenReview ICLR'22 + NeurIPS'23 submissions)
+ formative-study pool of **51 ideas** (34 new ideas generated by Scideator (Radensky et al.); 17 carried over from the first-round study, which had used 46 Scideator + 5 OpenReview ICLR'22/NeurIPS'23 ideas)
```

- [ ] **Change 51 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=6|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 6]]
    - Auditor evidence: page 6: "best performance was achieved using 15 idea examples (random seed 100). For the OpenReview examples, the best setup involved 5 idea-review pairs." — seed is stated only for the 15 expert examples
    - Checker: p. 6: 'best performance was achieved using 15 idea examples (random seed 100). For the OpenReview examples, the best setup involved 5 idea-review pairs.' The seed is attached only to the 15 expert examples.
```diff
- The 15 idea-paper pairs and the 5-pair OpenReview-baseline configuration were chosen via a random seed (=100)
+ The 15 idea-paper pairs were chosen via a random seed (=100) and the best OpenReview baseline used 5 idea-review pairs
```

- [ ] **Change 52** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=6|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 6]]
    - Auditor evidence: page 6, Section 6.1: "even when we excluded the relevant papers from the expert-labeled examples, our approach still outperformed the OpenReview baseline"; Table 1 p. 7
    - Checker: p. 6 Sec 6.1: 'even when we excluded the relevant papers from the expert-labeled examples, our approach still outperformed the OpenReview baseline'; rendered Table 1 p. 7: OpenReview 0.59, expert 'idea, reasoning' 0.75.
```diff
- - OpenReview-based examples performed worse than expert-labeled examples even when relevant papers were also included.
+ - OpenReview-based examples (accuracy 0.59) performed worse than expert-labeled examples even when relevant papers were excluded from the expert examples (idea + reasoning, accuracy 0.75).
```

- [ ] **Change 53** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf#page=7|Shahid et al. - 2025 - Literature-Grounded Novelty Assessmen p. 7]]
    - Auditor evidence: page 7, Table 1: Cohen Kappa column is "-" for every row except "with idea, most relevant papers, class, reasoning 0.59", "AI Scientist 0.05", "GPT-4o 0.52", "Claude-3-5-Sonnet 0.19"; "two-way" is not stated
    - Checker: Rendered Table 1 p. 7: Kappa appears only for the best expert row (0.59), AI Scientist (0.05) and AI Researcher GPT-4o/Claude (0.52/0.19); every other row has '-' or a blank cell, and 'two-way' is not stated.
```diff
- - Test agreement was reported with **two-way Cohen's κ** (only for the in-context settings); other rows show only accuracy/precision/recall/F1.
+ - Cohen's κ was reported only for the best expert-labeled row (0.59) and the two external novelty checkers (AI Scientist, AI Researcher); all other rows show only accuracy/precision/recall/F1.
```

### sonWhenAICoScientists2025

#### [[EVD - LLM confidence was near zero across 498 SPOT evaluations]]

- [ ] **Change 63 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=6|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 6]]
    - Auditor evidence: page 6, Figure 4 right (rendered image): x = Confidence, y = Average Pass@4; nearly every marker sits above the dashed diagonal (e.g. o3 statistical reporting at confidence ≈0.46, pass@4 = 1.0)
    - Checker: Rendered Figure 4 right (p. 6): x = confidence, y = average pass@4; nearly every marker sits above the dashed y = x line, so 'below the diagonal' was backwards.
```diff
- | weak positive: points fall well below the y = x diagonal |
+ | weak positive: almost all points lie above the y = x diagonal (pass@4 exceeds mean confidence) |
```

- [ ] **Change 64 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=24|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 24]]
    - Auditor evidence: page 24, Appendix C.1, Eq. 4–5: p̂ = 1 − C(n−c, K)/C(n, K) with n = 8; C(n−c, K) = 0 whenever n − c < K
    - Checker: Appendix C.1 Eq. 5 (p. 24): p̂ = 1 − C(n−c, K)/C(n, K) with n = 8, which equals 1 whenever n − c < K; the paper (p. 6) reports two full-confidence cases without stating K.
```diff
- | model detects error $g$ in all 8 runs ($c_{i,g} = 8$), so $\hat{p}_{i,g} = 1$ |
+ | $\hat{p}_{i,g} = 1$ whenever fewer than $K$ of the 8 runs miss $g$ ($n - c_{i,g} < K$); for $K = 4$ that is detection in at least 5 of 8 runs, for $K = 1$ in all 8 runs. The paper does not state which $K$ underlies the two full-confidence cases. |
```

#### [[EVD - o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication]]

- [ ] **Change 65** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=34|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 34]]
    - Auditor evidence: page 34, Table 4 (o3): "Equation / proof 33.6 3.8 51.6 6.1 67.5 3.7"; Table 6 (Gemini-2.5-Pro): "Equation / proof ... 38.4 7.3"; page 6 text: "o3 leads with a 62.6% (pass@4), followed by Gemini-2.5-Pro at 36.4%". The ± 5.7 is not in the PDF.
    - Checker: p. 6 text: o3 62.6%, Gemini 36.4%; rendered Table 4 (o3) Equation/proof pass@4 67.5 (3.7) and Table 6 (Gemini) 38.4 (7.3) on p. 34. The '± 5.7' is not in the PDF.
```diff
- | **Equation / proof (37)** | **62.6 ± 5.7 (best)** | 1.5 ± 1.5 | 36.4 ± unknown | 3.0 ± 2.0 |
+ | **Equation / proof (37)** | **62.6 (text) / 67.5 ± 3.7 (Table 4) (best)** | 1.5 ± 1.5 | 36.4 (text) / 38.4 ± 7.3 (Table 6) | 3.0 ± 2.0 |
```

- [ ] **Change 66 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=34|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 34]]
    - Auditor evidence: page 34, Table 5 (GPT-4.1): "Figure duplication 16.3 4.9 27.6 5.7 41.1 5.6"; Table 6 (Gemini-2.5-Pro): "Figure duplication 1.5 2.6 2.8 3.4 5.5 3.9"; page 35, Table 8 (Claude-3.7-Sonnet:Thinking): "Figure duplication ... 34.9 6.0"; page 6 text gives 44.4%, 33.3%, 0%
    - Checker: Rendered p. 34–35: Figure duplication pass@4 is o3 0.0 (0.0) in Table 4, GPT-4.1 41.1 (5.6) in Table 5, Gemini 5.5 (3.9) in Table 6, Claude:Thinking 34.9 (6.0) in Table 8; the p. 6 text gives 44.4/33.3/0/0. GPT-4.1 is still the best.
```diff
- | **Figure duplication (27)** | 0.0 ± 0.0 | **44.4** (best) | 0.0 ± 0.0 | 33.3 |
+ | **Figure duplication (27)** | 0.0 ± 0.0 | **44.4 (text) / 41.1 ± 5.6 (Table 5)** (best) | 0 (text) / 5.5 ± 3.9 (Table 6) | 33.3 (text) / 34.9 ± 6.0 (Table 8) |
```

- [ ] **Change 67 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=6|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 6]]
    - Auditor evidence: page 6 text: "o3 (0%), and Gemini-2.5-Pro (0%)"; page 34, Table 6: "Figure duplication ... 5.5 3.9"
    - Checker: p. 6 text says Gemini-2.5-Pro 0% on figure duplication, but Table 6 (p. 34) gives 5.5 (3.9); o3 is 0.0 in both.
```diff
- | o3 and Gemini-2.5-Pro score 0% on Figure Duplication |
+ | o3 scores 0% on Figure Duplication; Gemini-2.5-Pro 0% in the text but 5.5% in Appendix Table 6 |
```

- [ ] **Change 68 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=35|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 35]]
    - Auditor evidence: page 35, Table 8 (Claude-3.7-Sonnet:Thinking): "Equation / proof 0.8 1.3 1.6 1.8 3.0 2.0"; page 6: "all other models remain below 5%"; Claude-3.7-Sonnet Thinking (33.3%) on figure duplication
    - Checker: Table 8 (p. 35): Claude-3.7-Sonnet:Thinking equation/proof pass@4 is 3.0 and figure duplication 34.9 (33.3% in text), so the old claim that Claude:Thinking excels at proofs is wrong. The text-vs-appendix discrepancies in the note match Tables 4–6.
```diff
- - Reasoning models (o3, Claude:Thinking) excel at mathematical/proof errors but show weakness in visual/figure analysis.
+ - Reasoning models o3 and Gemini-2.5-Pro lead on equation/proof errors (Claude-3.7-Sonnet:Thinking reaches only 3.0%) and score at or near 0% on figure duplication; Claude:Thinking is the exception, scoring 33.3% on figure duplication.
+ - PDF check 2026-11-17: the per-category pass@4 values in the Section 3.1 text (p. 6) differ from Appendix G Tables 4–8 (p. 34–35), e.g. o3 equation/proof 62.6% vs 67.5%, GPT-4.1 figure duplication 44.4% vs 41.1%, Gemini-2.5-Pro figure duplication 0% vs 5.5%.
```

- [ ] **Change 69 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=4|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 4]]
    - Auditor evidence: page 4, Figure 2 (rendered image): bar heights Mathematics 22, Biology 13, Computer Sci. 13, Multidisciplinary 11, Chemistry 8, Physics 8, Materials Sci. 6, Medicine 5, Environmental Sci. 3, Engineering 2 (sum 91; the page's values sum to 96)
    - Checker: Rendered Figure 2 (p. 4): bars read about Math 22, Biology 13, CS 13, Multidisciplinary 11, Chemistry 8, Physics 8, Materials 6, Medicine 5, Env 3, Engineering 2 (sum 91).
```diff
- Mathematics ≈ 22, Biology ≈ 16, Computer Science ≈ 12, Multidisciplinary ≈ 11, Chemistry ≈ 10, Physics ≈ 8, Materials Science ≈ 7, Medicine ≈ 5,
+ Mathematics ≈ 22, Biology ≈ 13, Computer Science ≈ 13, Multidisciplinary ≈ 11, Chemistry ≈ 8, Physics ≈ 8, Materials Science ≈ 6, Medicine ≈ 5,
```

#### [[EVD - o3 led SPOT with 37.8% pass@4]]

- [ ] **Change 70** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=5|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 5]]
    - Auditor evidence: page 5, Table 2 (rendered image): Gemini-2.0-Flash-Lite recall "1.6 (1.3)"
    - Checker: Rendered Table 2 (p. 5): Gemini-2.0-Flash-Lite recall is 1.6 with subscript 1.3.
```diff
- | Gemini-2.0-Flash-Lite (001) | ✗ | 1.0 ± 0.8 | 1.6 ± 1.1 |
+ | Gemini-2.0-Flash-Lite (001) | ✗ | 1.0 ± 0.8 | 1.6 ± 1.3 |
```

- [ ] **Change 71** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=5|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 5]]
    - Auditor evidence: page 5, Table 2 (rendered image): Claude-3.7-Sonnet (20250219:Think) pass@4 "18.6 (2.8)"
    - Checker: Rendered Table 2 (p. 5): Claude-3.7-Sonnet Think pass@4 is 18.6 with subscript 2.8.
```diff
- | 5.5 ± 1.7 | 18.6 ± 2.3 |
+ | 5.5 ± 1.7 | 18.6 ± 2.8 |
```

- [ ] **Change 72** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=5|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 5]]
    - Auditor evidence: page 5, Table 2 (rendered image): Qwen2.5-VL-72B-Instruct precision "0.6 (1.2)"
    - Checker: Rendered Table 2 (p. 5): Qwen2.5-VL-72B precision is 0.6 with subscript 1.2.
```diff
- | Qwen2.5-VL-72B-Instruct | ✗ | 0.6 ± 1.6 |
+ | Qwen2.5-VL-72B-Instruct | ✗ | 0.6 ± 1.2 |
```

- [ ] **Change 73** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=5|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 5]]
    - Auditor evidence: page 5, Table 2 (rendered image): Qwen2.5-VL-32B-Instruct precision "1.9 (2.0)"
    - Checker: Rendered Table 2 (p. 5): Qwen2.5-VL-32B precision is 1.9 with subscript 2.0.
```diff
- | Qwen2.5-VL-32B-Instruct | ✗ | 1.9 ± 2.1 |
+ | Qwen2.5-VL-32B-Instruct | ✗ | 1.9 ± 2.0 |
```

- [ ] **Change 74 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=6|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 6]]
    - Auditor evidence: page 6: "the performance gap between o3 and Llama-4-Maverick is widest on SPOT (ours) (∆ = 20.2 pp)"; Figure 3 plots "S POT (recall)"; Table 2 p. 5: o3 pass@4 37.8, Llama-4-Maverick pass@4 3.3
    - Checker: Figure 3 (p. 6) plots SPOT recall (o3 21, Maverick 0.9, Δ = 20.2 pp); Table 2 pass@4 is o3 37.8 vs Maverick 3.3, a 34.5 pp gap.
```diff
- pass@4 3.3%, a 20.2 pp gap to o3 on pass@4.
+ pass@4 3.3%; the 20.2 pp gap to o3 reported in Figure 3 is on SPOT recall (21.1% vs 0.9%), while the pass@4 gap is 34.5 pp (37.8% vs 3.3%).
```

- [ ] **Change 75** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf#page=3|Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchm p. 3]]
    - Auditor evidence: page 3, Stage 2: "The first retains comment–manuscript pairs that unambiguously pinpoint a specific section ... reducing our pool to 1,855 WithdrarXiv and 25,378 PubPeer samples" — 25,378 is the post-filter count, not the raw crawl
    - Checker: p. 3 Stage 2: the first GPT-4o filtering pass reduces the pool 'to 1,855 WithdrarXiv and 25,378 PubPeer samples', so 25,378 is a post-filter count, not the raw crawl.
```diff
- PubPeer 25,378 → 215 post-2024.
+ PubPeer → 25,378 after the same GPT-4o filter → 215 post-2024.
```

### sridharanAssessingDecisionMakingCapabilities2024

#### [[EVD - AI platforms drafted SOPs covering fundamental sections with variations]]

- [ ] **Change 105 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=87|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 87]]
    - Auditor evidence: page 87 (PDF p5), Table 2, Conflict of interest row: ChatGPT and Google Bard cells are blank; the 'Comments common to all three AI platforms' column reads 'The IRB member/s with COI is required to leave the discussion room ... The IRB member/s with COI is not counted in the quorum.'
    - Checker: Rendered Table 2 (p. 87): in the Conflict of interest row the ChatGPT and Google Bard cells are blank; leaving the room and not counting toward quorum appear only in the 'Comments common to all three AI platforms' column.
```diff
- while ChatGPT and Bard correctly required the member to leave the room and not be counted in quorum.
+ while Table 2 gives no COI entry for ChatGPT or Bard; leaving the room and exclusion from quorum appear only in the "comments common to all three" column.
```

- [ ] **Change 106 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=85|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 85]]
    - Auditor evidence: page 85: 'Overall, these platforms managed to cover the fundamental sections of the SOPs requested'
    - Checker: p. 85 says only 'Overall, these platforms managed to cover the fundamental sections of the SOPs requested'; coverage is not reported per draft.
```diff
- | All drafts (qualitative narrative) |
+ | "Overall" (qualitative narrative; per-draft coverage not reported) |
```

#### [[EVD - All AI platforms missed post-trial herbal medicine access]]

- [ ] **Change 110 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86 (PDF p4), Table 1, 'Failure to state reporting of an event' / 'Case Study 2: Emergency Room Research': Poe 'Not stated', ChatGPT 'Not stated', Bard 'Not stated'; General Discussion (pp. 85-89) never mentions case study 10 or post-trial access
    - Checker: Table 1 (p. 86): in the 'Failure to state reporting of an event' row for Case Study 2 (Emergency Room Research), Poe, ChatGPT and Bard are all 'Not stated'. The p. 85 text attributes only the Case Study 10 failure to all platforms, and the Discussion never mentions Case Study 10.
```diff
- - This is the only case (of 10) on which all three platforms failed simultaneously, making it the most-cited failure mode in the paper's discussion.
+ - Case Study 10 is the only failure the text attributes to all three platforms, but Table 1 also shows all three "Not stated" for event reporting in Case Study 2; the Discussion does not mention Case Study 10.
```

- [ ] **Change 111 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86 (PDF p4), Table 1, 'Failure to state reporting of an event' / 'Case Study 2: Emergency Room Research': Poe 'Not stated', ChatGPT 'Not stated', Bard 'Not stated'
    - Checker: Table 1 (p. 86): in the 'Failure to state reporting of an event' row for Case Study 2 (Emergency Room Research), Poe, ChatGPT and Bard are all 'Not stated', so two cases have an all-three failure.
```diff
- | Cases (of 10) where all 3 platforms failed | 1 (Case Study 10 only) |
+ | Cases (of 10) where all 3 platforms failed | 2 (Case Study 10 per text; Case Study 2 event reporting per Table 1) |
```

#### [[EVD - No AI platform recognized the IRB quorum requirement]]

- [ ] **Change 107** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=85|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 85]]
    - Auditor evidence: page 85 text: 'Concerning the SOP for the initial review of proposals, none of the AI platforms recognized the necessity of achieving a quorum'; Table 2 (pp. 87-88) rows are Constitution, COI, Expedited review, Exemption, Continuing review, Study completion, SAE only
    - Checker: The quorum omission is stated only in the p. 85 Results text; Table 2 (pp. 87–88) rows are Constitution, COI, Expedited, Exemption, Continuing review, Study completion and SAE, with no initial-review row.
```diff
- this omission is reported narratively in Results and tabulated in Table 2's right-hand "common to all three" column.
+ this omission is reported narratively in Results only (Table 2 has no row for initial review of proposals).
```

- [ ] **Change 108** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=87|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 87]]
    - Auditor evidence: Table 2 (pp. 87-88) has no row for management of initial protocol submissions
    - Checker: Same as 107: Table 2 has no row for initial review of proposals, so the quorum omission is not in its common-to-all column.
```diff
- - The quorum omission is one of several "common to all three platforms" failures called out in Table 2's rightmost column, alongside:
+ - The quorum omission for initial review comes from the Results text only (Table 2 has no initial-review row); Table 2's "common to all three" column lists related omissions:
```

- [ ] **Change 109 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=87|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 87]]
    - Auditor evidence: page 87 (PDF p5), Table 2, Conflict of interest row: ChatGPT and Google Bard cells are blank; the 'Comments common to all three AI platforms' column reads 'The IRB member/s with COI is required to leave the discussion room ... The IRB member/s with COI is not counted in the quorum.'
    - Checker: Rendered Table 2 (p. 87): the ChatGPT and Bard COI cells are blank, and the leave-the-room statement sits in the common-to-all column, so the page's 'ChatGPT and Bard correctly required...' is unsupported.
```diff
- , even when ChatGPT and Bard correctly required the conflicted member to leave the room.
+ ; Table 2 gives no COI entry for ChatGPT or Bard, and the leave-the-room point also sits in the common-to-all column.
```

#### [[EVD - Three AI platforms answered all 10 IRB cases correctly]]

- [ ] **Change 112** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86, Table 1 'Domains' column lists 8 domains: reporting of an event; expediting IRB review; reporting sponsors on deviation; obtaining written consent; critical suggestions to sponsors; definition of drug; critical ICF information; quantifying potential risks
    - Checker: Table 1 (p. 86) has 11 rows but 8 distinct domain labels (event reporting, expediting review, reporting deviation to sponsors, written consent, critical suggestions to sponsors, definition of drug, critical ICF information, quantifying risks).
```diff
- Table 1 documents 9 distinct domains
+ Table 1 documents 8 distinct domains
```

- [ ] **Change 113** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86, Table 1: 8 domain labels across 11 rows
    - Checker: Same as 112: Table 1 lists 8 distinct domains.
```diff
- | Domains where ≥1 platform missed a GCP sub-issue (Table 1) | 9 |
+ | Domains where ≥1 platform missed a GCP sub-issue (Table 1) | 8 |
```

- [ ] **Change 114 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86 (PDF p4), Table 1, 'Failure to state reporting of an event' / 'Case Study 2: Emergency Room Research': Poe 'Not stated', ChatGPT 'Not stated', Bard 'Not stated'
    - Checker: Table 1 (p. 86): in the 'Failure to state reporting of an event' row for Case Study 2 (Emergency Room Research), Poe, ChatGPT and Bard are all 'Not stated'.
```diff
- and Case Study 10 (post-trial access) was missed by all three.
+ and Case Study 10 (post-trial access) was missed by all three, as was event reporting in Case Study 2 (Table 1: Not stated for all three).
```

- [ ] **Change 115 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf#page=86|Sridharan and Sivaramakrishnan - 2024 - Assessing the Decisi p. 86]]
    - Auditor evidence: page 86 (PDF p4), Table 1, 'Failure to state reporting of an event' / 'Case Study 2: Emergency Room Research': Poe 'Not stated', ChatGPT 'Not stated', Bard 'Not stated'
    - Checker: Table 1 (p. 86): in the 'Failure to state reporting of an event' row for Case Study 2 (Emergency Room Research), Poe, ChatGPT and Bard are all 'Not stated'; Case Study 10 comes from the p. 85 text.
```diff
- | Cases where all 3 platforms failed (post-trial access) | 1 / 10 (Case Study 10) |
+ | Cases where all 3 platforms failed | 2 / 10 (Case Study 10 post-trial access, per text; Case Study 2 event reporting, per Table 1) |
```

### sridharanLeveragingArtificialIntelligence2025

#### [[EVD - All four LLMs gave similar answers to all 7 IRB cases]]

- [ ] **Change 92** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf#page=4|Sridharan and Sivaramakrishnan - 2024 - Leveraging artificia p. 4]]
    - Auditor evidence: PDF page 4 (journal page 129): 'Table 2 Comparison of the outputs of four AI platforms regarding the ethics issues' ... footer 'J Med Ethics 2025;51:126–134 ... 129'
    - Checker: Table 2 ('Comparison of the outputs of four AI platforms regarding the ethics issues') is on PDF p. 4, whose footer is journal p. 129; journal p. 128 carries Table 1.
```diff
- Source-file table: see Table 2 (p. 128).
+ Source-file table: see Table 2 (p. 129).
```

#### [[EVD - All four LLMs included core ICD elements in all 7 cases]]

- [ ] **Change 94 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf#page=132|Sridharan and Sivaramakrishnan - 2024 - Leveraging artificia p. 132]]
    - Auditor evidence: page 132, Table 4 row 'Failure to state the study site...Case 3': ChatGPT4.0 'Not stated', comment footnoted *†‡§ (Table 4 footnotes: *Bard, †Claude, ‡ChatGPT 4.0, §ChatGPT 3.5), i.e. none of the four stated it
    - Checker: Rendered Table 4, journal p. 132: the Case 3 study-site row has ChatGPT4.0 'Not stated' and the other cells blank, with the comment footnoted *†‡§ (not identified by Bard, Claude, ChatGPT 4.0 or ChatGPT 3.5). None of the four stated it, so ChatGPT 3.5 'specified' is wrong.
```diff
- | Study site (case 3 school) | not stated | not stated | specified | not stated |
+ | Study site (case 3 school) | not stated | not stated | not stated | not stated |
```

- [ ] **Change 95 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf#page=132|Sridharan and Sivaramakrishnan - 2024 - Leveraging artificia p. 132]]
    - Auditor evidence: page 132, Table 4 row 'Failure to state a critical information, Case 4': ChatGPT4.0 'Specified', Claude 'Not stated', Bard and ChatGPT 3.5 cells blank; comment footnoted only '†' (= Not identified by Claude-Instant-100k), so Bard and ChatGPT 3.5 did state it
    - Checker: Rendered Table 4, p. 132: the Case 4 row has ChatGPT4.0 'Specified', Claude 'Not stated', Bard and ChatGPT 3.5 blank, and the comment is footnoted only † (not identified by Claude-Instant-100k). Footnotes are used the same way in other rows (e.g. Case 5 *‡§ with blank Bard/3.5 cells), so Bard and 3.5 did state it. This is an inference from the footnote, but the page's 'not stated' contradicts it.
```diff
- | Critical info (case 4 no insurance for AEs) | specified | not stated | not stated | not stated |
+ | Critical info (case 4 no insurance for AEs) | specified | specified | specified | not stated |
```

#### [[EVD - LLMs performed suboptimally on placebo arm and risk issues in a single prompt]]

- [ ] **Change 93** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf#page=4|Sridharan and Sivaramakrishnan - 2024 - Leveraging artificia p. 4]]
    - Auditor evidence: PDF page 4 (journal page 129) carries Table 2; journal p. 128 carries Table 1
    - Checker: Same check: Table 2 is on journal p. 129 (PDF p. 4), not 128.
```diff
- see Table 2 (p. 128) for single-prompt failures
+ see Table 2 (p. 129) for single-prompt failures
```

### srinivasanEvaluatingReportingQuality2025a

#### [[EVD - CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology]]

- [ ] **Change 134 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf#page=5|Srinivasan et al. - 2025 - Evaluating the reporting quality  p. 5]]
    - Auditor evidence: page 5, Section 4.2: "we excluded these four items from our final analysis" (7b, 3b, 6b, 14b); the paper never states a count of 21 retained items
    - Checker: Srinivasan p.5 Sec 4.2: after human validation 'we excluded these four items' (7b, 3b, 6b, 14b); the appendix lists 33 CONSORT items used, and 21 retained is never stated.
```diff
- 25-item CONSORT checklist (21 items retained after excluding items the model could not reliably assess)
+ 25-item CONSORT checklist (four items, 7b, 3b, 6b and 14b, excluded after human validation because the model could not reliably assess them)
```

- [ ] **Change 135** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf#page=5|Srinivasan et al. - 2025 - Evaluating the reporting quality  p. 5]]
    - Auditor evidence: page 5, Section 4.2 excludes only four items (7b, 3b, 6b, 14b); 2a Background was excluded only in the CONSORT-TM corpus (page 3) and is reported in the large-scale analysis at 95.88% (page 5: "scientific background/rationale (95.88%)")
    - Checker: Srinivasan p.3: 2a Background was excluded only in the CONSORT-TM corpus; p.5 Sec 4.3.1 reports 2a in the large-scale analysis (95.88%); only 7b, 3b, 6b, 14b were removed.
```diff
- (later restricted to 21 after removing items 2a Background, 7b interim analyses,
+ (later restricted by removing items 7b interim analyses,
```

#### [[EVD - Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment]]

- [ ] **Change 136** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf#page=5|Srinivasan et al. - 2025 - Evaluating the reporting quality  p. 5]]
    - Auditor evidence: page 5, Section 4.2: "we excluded these four items from our final analysis"; page 5: "scientific background/rationale (95.88%)" shows 2a was assessed at scale (this page's own table lists it)
    - Checker: Same Srinivasan p.3 and p.5 passages.
```diff
- CONSORT 2010 25-item checklist (21 items retained after excluding 2a Background, 7b interim analyses, 3b protocol changes, 6b changes to outcomes, 14b reasons for termination)
+ CONSORT 2010 25-item checklist (items 7b interim analyses, 3b protocol changes, 6b changes to outcomes and 14b reasons for termination excluded after human validation; 2a Background was excluded only from the CONSORT-TM benchmark corpus)
```

### thelwallEvaluatingResearchQuality2024

#### [[EVD - Full text scored worse than abstracts for 3 ChatGPT models]]

- [ ] **Change 32** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf#page=8|Thelwall - 2024 - Evaluating Research Quality with Large Lan p. 8]]
    - Auditor evidence: page 8, Table 1: only "GPT-3.5 turbo: Titles" exists; 0.539 is its correlation with the "GPT-4o: Abstracts" column ("GPT-3.5 turbo: Titles 0.439 0.444 0.359 0.499 0.539 0.589 0.434"), not a GPT-4o title result
    - Checker: Table 1 (p. 8) has only a 'GPT-3.5 turbo: Titles' row; 0.539 is that row's correlation with the GPT-4o: Abstracts column, not a GPT-4o title-only result.
```diff
- | **GPT-4o** | 0.539 | **0.678** |
+ | **GPT-4o** | — | **0.678** |
```

- [ ] **Change 33 ⚑** · Row or column shift · checker: MODIFY · PDF: [[source/pdfs/Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf#page=8|Thelwall - 2024 - Evaluating Research Quality with Large Lan p. 8]]
    - Auditor evidence: page 8, Table 1 Human column: "GPT-3.5 turbo: Titles ... 0.434"; page 7: "score predictions from titles alone ... having a 0.46 correlation with human scores"
    - Checker: Table 1 p. 8 Human column gives 0.434 for GPT-3.5 Titles; no GPT-4o titles cell exists. p. 7 text says 0.46 and rendered Figure 1 also ends near 0.46, so the note mentions the figure too.
```diff
- - Title-only input is non-trivial (r ≈ 0.43 for GPT-3.5-turbo, even higher for GPT-4o at 0.539), but substantially below abstracts.
+ - Title-only input is non-trivial (r = 0.434 for GPT-3.5-turbo; titles were run only with GPT-3.5-turbo), but substantially below abstracts.
+ - PDF check 2026-11-17: the p. 7 text (and Figure 1 at 30 iterations) gives the title-only correlation as 0.46, while Table 1 (p. 8) gives 0.434.
```

- [ ] **Change 34 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf#page=8|Thelwall - 2024 - Evaluating Research Quality with Large Lan p. 8]]
    - Auditor evidence: page 8, Table 1: "GPT-3.5 turbo: Abstracts 1.000 0.757" (vs Truncated text) vs page 7 text "(0.754)"
    - Checker: Table 1 p. 8 gives Abstracts vs Truncated text = 0.757 for GPT-3.5 turbo; p. 7 text says 0.754. The old text is a paraphrase in Other Notes, not a quote, and the page's own table already shows 0.757.
```diff
- is 0.754 within GPT-3.5-turbo (Table 1)
+ is 0.757 within GPT-3.5-turbo (Table 1; the p. 7 text gives 0.754)
```

- [ ] **Change 35** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf#page=8|Thelwall - 2024 - Evaluating Research Quality with Large Lan p. 8]]
    - Auditor evidence: page 8, Table 1 rows: GPT-3.5 turbo Titles/Abstracts/Truncated, GPT-4o-mini Abstracts/Truncated, GPT-4o Abstracts/Truncated (7 cells); Table 3 p.12 lists the same 7
    - Checker: Table 1 p. 8 has 7 rows: GPT-3.5 turbo Titles/Abstracts/Truncated, GPT-4o-mini Abstracts/Truncated, GPT-4o Abstracts/Truncated. No 4o or 4o-mini title runs.
```diff
- GPT-3.5-turbo (3 input cells), GPT-4o (3 input cells), GPT-4o-mini (3 input cells), 9 (model × input) cells total feeding Table 1.
+ GPT-3.5-turbo (3 input cells), GPT-4o (2 input cells: abstracts, truncated text), GPT-4o-mini (2 input cells), 7 (model × input) cells total feeding Table 1.
```

#### [[EVD - GPT-4o abstract scores correlated r=0.67 with humans]]

- [ ] **Change 36 ⚑** · Wrong number · checker: MODIFY · PDF: [[source/pdfs/Thelwall - 2024 - Evaluating Research Quality with Large Language Models An Analysis of ChatGPT's Effectiveness with.pdf#page=9|Thelwall - 2024 - Evaluating Research Quality with Large Lan p. 9]]
    - Auditor evidence: page 9, Figure 2 (rendered): at n=1 GPT-4o ≈0.44, GPT-3.5 ≈0.39, 4o-mini ≈0.38; at n=30 ≈0.65–0.67
    - Checker: Rendered Figure 2 p. 9: at n=1 the curves are about 0.38 (4o-mini), 0.39 (3.5) and 0.44 (4o); at n=30 about 0.65–0.67. 'Roughly doubles' is wrong, but 'by roughly half' is also loose (+52% to +71%), so I state only the endpoints.
```diff
- - Single-iteration Spearman r is much lower (~0.40); averaging 30 iterations roughly doubles correlation.
+ - Single-iteration Spearman r is much lower (~0.38–0.44 in Figure 2); averaging 30 iterations raises it to ~0.65–0.67.
```

### tyserAIDrivenReviewSystems2024

#### [[EVD - GPT-4 Turbo ranked first in human review preference]]

- [ ] **Change 138 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf#page=4|Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LL p. 4]]
    - Auditor evidence: page 4: "Each paper was randomly assigned two reviewers from the list of five potential reviewers" (a pair need not include the human review)
    - Checker: p. 4 Sec 3: 'Each paper was randomly assigned two reviewers from the list of five potential reviewers: Human, GPT-4..., Claude 3 Opus, Gemini Pro, Command R+', so a pair need not include the human review.
```diff
- generate one review per LLM competitor and pair it with the OpenReview human review; randomly assign
+ generate one review per LLM competitor (human reviews come from OpenReview); randomly assign
```

#### [[EVD - LLM review scores exceeded humans without area-chair context but matched with it]]

- [ ] **Change 139 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf#page=13|Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LL p. 13]]
    - Auditor evidence: page 13, Figure 14 bar label for P5 Recommendation reads 5.56 (rendered and zoomed)
    - Checker: Rendered p. 13 Figure 14 (at 220 dpi): the P5 Recommendation bar is labelled 5.56 and sits just above the 5.5 gridline; 5.36 is wrong.
```diff
- brings it back to ≈ human (5.36)
+ brings it back to ≈ human (5.56)
```

- [ ] **Change 140 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf#page=13|Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LL p. 13]]
    - Auditor evidence: page 13, Figure 14 bar label for P5 Recommendation reads 5.56; 5.56 − 5.88 = −0.32
    - Checker: Same Figure 14, p. 13: P5 = 5.56 and Human = 5.88, so the difference is -0.32.
```diff
- | **LLM P5 (+ S)** | **5.36** | — | **−0.52 (≈ human)** |
+ | **LLM P5 (+ S)** | **5.56** | — | **−0.32 (≈ human)** |
```

#### [[EVD - LLM reviews scored like human reviews on all 3 criteria]]

- [ ] **Change 141 ⚑** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf#page=14|Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LL p. 14]]
    - Auditor evidence: page 14: "Confusion matrix. Considering the average human review rating as ground truth"
    - Checker: The 'Confusion matrix. Considering the average human review rating as ground truth' paragraph (Appendix E) is on PDF p. 14 (p. 13 is Appendix D/Figure 14).
```diff
- (Appendix E, p. 12,
+ (Appendix E, p. 14,
```

### woelfleBenchmarkingHumanAICollaboration2024

#### [[EVD - Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74%]]

- [ ] **Change 0** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3: "(3) Combined LLMs (consistent in 7/9) 0.71 (0.68–0.74) 1627/1958 (83%, 81%–85%)"
    - Checker: p.7 Table 3 PRISMA 7/9: 1627/1958 (83%, 81%-85%); page's 81% is wrong.
```diff
- | PRISMA 7/9 | 81% (81–85%) |
+ | PRISMA 7/9 | 83% (81–85%) |
```

- [ ] **Change 1** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3 AMSTAR: "(3) Combined LLMs (consistent in 7/9) 0.68 (0.63–0.73) 528/654 (81%, 78%–84%)"
    - Checker: p.7 Table 3 AMSTAR 7/9 kappa 0.68 (0.63-0.73); page had 0.65.
```diff
- | AMSTAR 7/9 | 81% (78–84%) | 0.65 (0.63–0.73) |
+ | AMSTAR 7/9 | 81% (78–84%) | 0.68 (0.63–0.73) |
```

- [ ] **Change 2 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3 AMSTAR 5/9: "68/1232 (6%, 4%–7%)"
    - Checker: p.7 Table 3 AMSTAR 5/9 deferring 68/1232 (6%, 4%-7%) (rendered image).
```diff
- | 6% (4–8%) |
+ | 6% (4–7%) |
```

- [ ] **Change 3 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3 PRECIS-2 8/9: "79/106 (75%, 65%–83%)"
    - Checker: p.7 Table 3 PRECIS-2 8/9: 79/106 (75%, 65%-83%) (rendered image).
```diff
- | 75% (65–82%) |
+ | 75% (65–83%) |
```

- [ ] **Change 4 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Sec 3.1.3: "(9/9 for PRISMA and AMSTAR and ≥8/9 for PRECIS-2) was statistically indifferent from human performance"
    - Checker: p.7 Sec 3.1.3: '9/9 for PRISMA and AMSTAR and >=8/9 for PRECIS-2' statistically indifferent from humans.
```diff
- at 9/9 consistency for PRISMA and ≥8/9 for PRECIS-2
+ at 9/9 consistency for PRISMA and AMSTAR and ≥8/9 for PRECIS-2
```

- [ ] **Change 5** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3 PRECIS-2 5/9: "89/504 (18%, 14%–21%)" vs text "with deferring fractions from 29% to 88%"
    - Checker: Abstract and p.7 text give PRECIS-2 deferring 29%-88%, but Table 3 p.7 5/9 row is 89/504 (18%); note line is correct and the page table uses 18%.
```diff
- - 95% CIs were derived from bootstrapping with 1000 resamples on the publication level.
+ - 95% CIs were derived from bootstrapping with 1000 resamples on the publication level.
+ - PDF check 2026-11-17: the abstract and p. 7 text give PRECIS-2 deferring fractions of "29% to 88%", but Table 3 (p. 7) lists 18% at 5/9 (89/504); the table above follows Table 3.
```

- [ ] **Change 6 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.3: "GPT-3.5 could persistently not process 3 of 112 publications (2.7%) for PRISMA and 2 of 56 publications (3.6%) for PRECIS-2"; Table 2 p.5 GPT-3.5 AMSTAR N = 652/1232 (no AMSTAR failures)
    - Checker: p.8 Sec 3.3: GPT-3.5 failed 3/112 for PRISMA and 2/56 for PRECIS-2; Table 2 p.5 GPT-3.5 AMSTAR 652/1232 with no footnote b, so no AMSTAR failures.
```diff
- GPT-3.5 failed on 3/112 PRISMA/AMSTAR + 2/56 PRECIS-2
+ GPT-3.5 failed on 3/112 PRISMA + 2/56 PRECIS-2
```

#### [[EVD - GPT-4 cost about 100x more than Mixtral-8x22B]]

- [ ] **Change 7** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=3|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 3]]
    - Auditor evidence: page 3, Table 1: "Claude-2 (claude-2.0) ... September 2023 via OpenRouter"; "GPT-4 (gpt-4-32k-0613) ... September 2023 via OpenRouter"; "GPT-3.5 ... August 7, 2023 via OpenAI"
    - Checker: p.3 Table 1: Claude-3-Opus via Anthropic; Claude-2 and GPT-4 via OpenRouter; GPT-3.5 via OpenAI; Mixtral via OpenRouter.
```diff
- **Tools:** 5 LLM APIs (Anthropic for Claude-3-Opus & Claude-2; OpenAI for GPT-4 & GPT-3.5; OpenRouter for Mixtral-8x22B).
+ **Tools:** 5 LLM APIs (Anthropic for Claude-3-Opus; OpenRouter for Claude-2, GPT-4 & Mixtral-8x22B; OpenAI for GPT-3.5).
```

- [ ] **Change 8** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=3|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 3]]
    - Auditor evidence: page 3, Table 1: Claude-2 and GPT-4 "via OpenRouter"; GPT-3.5 "via OpenAI"; Claude-3-Opus "via Anthropic"
    - Checker: p.3 Table 1 access routes as above.
```diff
- Five LLMs were queried via APIs (Anthropic, OpenAI, OpenRouter for Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning, and (3)
+ Five LLMs were queried via APIs (Anthropic for Claude-3-Opus, OpenAI for GPT-3.5, OpenRouter for Claude-2, GPT-4 and Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning, and (3)
```

- [ ] **Change 9 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.3: "GPT-3.5 could persistently not process 3 of 112 publications (2.7%) for PRISMA and 2 of 56 publications (3.6%) for PRECIS-2"; Table 2 p.5 GPT-3.5 AMSTAR N = 652/1232 (no AMSTAR failures)
    - Checker: p.8 Sec 3.3 and Table 2 p.5 (GPT-3.5 AMSTAR N=1232).
```diff
- GPT-3.5 failed on 3/112 PRISMA/AMSTAR and 2/56 PRECIS-2
+ GPT-3.5 failed on 3/112 PRISMA and 2/56 PRECIS-2
```

#### [[EVD - Human-AI collaboration reached up to 96% on PRISMA surpassing human raters]]

- [ ] **Change 10** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.1.4: "Only the combination of human rater 2 with GPT-3.5 led to significantly more accurate responses than human rater 2 alone (1 of 10 possible human–AI pairs)"
    - Checker: p.8 Sec 3.1.4: 'Only the combination of human rater 2 with GPT-3.5 led to significantly more accurate responses than human rater 2 alone (1 of 10)'.
```diff
- for PRECIS-2, only 1 of 10 (Human-1 + GPT-3.5).
+ for PRECIS-2, only 1 of 10 (Human-2 + GPT-3.5).
```

- [ ] **Change 11 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8: "Claude-3-Opus, Claude-2, GPT-3.5, and Mixtral-8x22B led to significantly more accurate responses than either human rater 1 or 2 alone (8 of 10 possible human–AI pairs)" (4 LLMs × 2 raters = 8; the page's run list sums to 9, not 10)
    - Checker: p.8: 4 LLMs significant vs 'either human rater 1 or 2' = '8 of 10 possible pairs', and PRECIS-2's 1 of 10 is a rater-2 pair, so 10 = 2 raters x 5 LLMs; the page's run list sums to 9; Table 3 p.7 lists only rater-1 pairs.
```diff
- This generates 10 possible human–AI pairs (rater-1 × {2 runs each of Opus, Claude-2, GPT-3.5, Mixtral; 1 run of GPT-4 due to cost}).
+ The paper counts 10 possible human–AI pairs (human rater 1 or 2 × 5 LLMs); Table 3 reports only the human rater 1 pairs.
```

- [ ] **Change 12 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8: "8 of 10 possible human–AI pairs" for 4 LLMs vs "either human rater 1 or 2"; Opus×2+Claude-2×2+GPT-4×1+GPT-3.5×2+Mixtral×2 = 9
    - Checker: Same evidence as id 11 (p.8 text, Table 3 p.7).
```diff
- **Models:** 5 LLMs paired with human rater 1 → 10 possible pairs (Opus×2, Claude-2×2, GPT-4×1, GPT-3.5×2, Mixtral×2).
+ **Models:** 5 LLMs each paired with human rater 1 or human rater 2 → 10 possible pairs (Table 3 shows the 5 rater-1 pairs).
```

- [ ] **Change 13 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.3: "GPT-3.5 could persistently not process 3 of 112 publications (2.7%) for PRISMA and 2 of 56 publications (3.6%) for PRECIS-2"; Table 2 p.5 GPT-3.5 AMSTAR N = 652/1232 (no AMSTAR failures)
    - Checker: p.8 Sec 3.3 and Table 2 p.5.
```diff
- GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2
+ GPT-3.5 3/112 PRISMA + 2/56 PRECIS-2
```

- [ ] **Change 14 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=7|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 7]]
    - Auditor evidence: page 7, Table 3 PRISMA: "(4) Human Rater 1 & Mixtral-8x22B 0.92 (0.89–0.94) 1715/1801 (95%, 94%–97%)" not bold, while Opus, Claude-2, GPT-3.5 rows are bold
    - Checker: Rendered p.7 Table 3: PRISMA 'Human Rater 1 & Mixtral-8x22B' row not bold (Opus, Claude-2, GPT-3.5 bold), while p.8 text lists Mixtral among significant pairs.
```diff
- Only human rater 2 + GPT-3.5 was significantly better than a human alone for PRECIS-2 (p. 8).
+ Only human rater 2 + GPT-3.5 was significantly better than a human alone for PRECIS-2 (p. 8).
+ - PDF check 2026-11-17: the p. 8 text says Mixtral-8x22B was among the pairs significantly better than either human alone for PRISMA, but Table 3 (p. 7) does not bold Human Rater 1 & Mixtral-8x22B for PRISMA (bold = CI not overlapping the human rater alone).
```

#### [[EVD - LLM-extracted quotes had 99% median similarity to source]]

- [ ] **Change 15 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8: "The median quote similarity with the original full text was 99%" is reported once, overall; no per-tool medians in the main text
    - Checker: p.8: 'median quote similarity with the original full text was 99%' reported once overall; no per-tool values in main text.
```diff
- | PRISMA (27 items × 112) | 14 (5–17) | 0.5 / item | **99%** |
+ | PRISMA (27 items × 112) | 14 (5–17) | 0.5 / item | **99%** (overall median, all tools; per-tool not reported in main text) |
```

- [ ] **Change 16 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8: single overall figure "was 99%"
    - Checker: p.8 single overall 99% figure.
```diff
- | AMSTAR (11 items × 112) | 7 (4–8) | 0.6 / item | **99%** |
+ | AMSTAR (11 items × 112) | 7 (4–8) | 0.6 / item | (overall 99%) |
```

- [ ] **Change 17 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8: single overall figure "was 99%"
    - Checker: p.8 single overall 99% figure.
```diff
- | PRECIS-2 (9 domains × 56) | 10 (9–10) | 1 / domain | **99%** |
+ | PRECIS-2 (9 domains × 56) | 10 (9–10) | 1 / domain | (overall 99%) |
```

- [ ] **Change 18 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.3: "GPT-3.5 could persistently not process 3 of 112 publications (2.7%) for PRISMA and 2 of 56 publications (3.6%) for PRECIS-2"; Table 2 p.5 GPT-3.5 AMSTAR N = 652/1232 (no AMSTAR failures)
    - Checker: p.8 Sec 3.3 and Table 2 p.5.
```diff
- GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2; Mixtral 1/112).
+ GPT-3.5 3/112 PRISMA + 2/56 PRECIS-2; Mixtral 1/112).
```

#### [[EVD - Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans]]

- [ ] **Change 19** · Row or column shift · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=5|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 5]]
    - Auditor evidence: page 5, Table 2 PRISMA Claude-3-Opus reliability: "2318/2889 (80%, 78%–82%)" (89% (87–91%) is the Claude-2 row below)
    - Checker: Rendered p.5 Table 2 PRISMA Claude-3-Opus reliability 2318/2889 (80%, 78%-82%); 89% (87-91%) belongs to Claude-2.
```diff
- | PRISMA | Claude-3-Opus | **70%** (68–72%) | 0.51 (0.47–0.55) | 89% (87–91%) |
+ | PRISMA | Claude-3-Opus | **70%** (68–72%) | 0.51 (0.47–0.55) | 80% (78–82%) |
```

- [ ] **Change 20** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=5|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 5]]
    - Auditor evidence: page 5, Table 2 (rendered image): "(2) GPT-4 0.02 (−0.04 to 0.08) 193/504 (38%, 33%–43%)"
    - Checker: Rendered p.5 Table 2 PRECIS-2 GPT-4 kappa 0.02 (-0.04 to 0.08).
```diff
- | PRECIS-2 | GPT-4 | **38%** (33–43%) | 0.02 (–0.07 to 0.04) |
+ | PRECIS-2 | GPT-4 | **38%** (33–43%) | 0.02 (–0.04 to 0.08) |
```

- [ ] **Change 21 ⚑** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=3|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 3]]
    - Auditor evidence: page 3, Table 1: Claude-2 and GPT-4 "via OpenRouter"; GPT-3.5 "via OpenAI"
    - Checker: p.3 Table 1 access routes.
```diff
- Five LLMs were queried via APIs (Anthropic, OpenAI, OpenRouter for Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning in one paragraph,
+ Five LLMs were queried via APIs (Anthropic for Claude-3-Opus, OpenAI for GPT-3.5, OpenRouter for Claude-2, GPT-4 and Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning in one paragraph,
```

- [ ] **Change 22 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf#page=8|Woelfle et al. - 2024 - Benchmarking Human–AI collaboration  p. 8]]
    - Auditor evidence: page 8, Sec 3.3: "GPT-3.5 could persistently not process 3 of 112 publications (2.7%) for PRISMA and 2 of 56 publications (3.6%) for PRECIS-2"; Table 2 p.5 GPT-3.5 AMSTAR N = 652/1232 (no AMSTAR failures)
    - Checker: p.8 Sec 3.3 and Table 2 p.5.
```diff
- GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2; Mixtral 1/112; Claude-2 processed all. Reflected
+ GPT-3.5 3/112 PRISMA + 2/56 PRECIS-2; Mixtral 1/112; Claude-2 processed all. Reflected
```

### wrightsonGPTRCTsUsing2025

#### [[EVD - Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions]]

- [ ] **Change 54** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=5|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 5]]
    - Auditor evidence: page 5: "accuracy (95% CI) = 64% (57% to 71%)" and "83% (77% to 88%)" (71 < 77); Discussion p. 5: "fine-tuning the Llama 2 model significantly improved its accuracy"
    - Checker: Wrightson p.5: base 64% (57%-71%) vs fine-tuned 83% (77%-88%), CIs do not overlap; Discussion p.5: 'fine-tuning the Llama 2 model significantly improved its accuracy'.
```diff
- CIs on accuracy overlap weakly (64% (57–71%) vs. 83% (77–88%)).
+ the accuracy CIs do not overlap (64% (57–71%) vs. 83% (77–88%)), and the authors describe the gain as significant ("fine-tuning the Llama 2 model significantly improved its accuracy", p. 5).
```

- [ ] **Change 55 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=4|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 4]]
    - Auditor evidence: page 4: "performed using the TogetherAI playground using the platform default hyper-parameter values (temperature and Top P=0.7)" — the default is for hyperparameters, not the prompt
    - Checker: Wrightson p.4: base and fine-tuned Llama 2 run 'using the platform default hyper-parameter values (temperature and Top P=0.7)'; the default was hyperparameters, not the prompt.
```diff
- | Base (zero-shot, default TogetherAI prompt) |
+ | Base (zero-shot, default TogetherAI hyperparameters) |
```

- [ ] **Change 56 ⚑** · Not in the paper · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=1|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 1]]
    - Auditor evidence: page 1: "Received 14 May 2024" — no analysis date is given, so mid-2024 is not supported
    - Checker: Wrightson p.1 'Received 14 May 2024'; no analysis date given, so 'mid-2024' is unsupported.
```diff
- (the version available on TogetherAI in mid-2024;
+ (the version available on TogetherAI before submission on 14 May 2024;
```

#### [[EVD - GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions]]

- [ ] **Change 57 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=2|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 2]]
    - Auditor evidence: page 2, Figure 1 caption: "Actual (y-axis) represents the answers given by the GPT-4 Turbo model, and predicted (x-axis) represents the labels ... from Schulz et al." (cells: Actual YES/Pred NO = 13, Actual NO/Pred YES = 7); Supplement Table S3 FN column 2,0,0,3,1,1,3,0,3 (=13), FP column 2,3,2,0,0,0,0,0,0 (=7)
    - Checker: Rendered p.2 Figure 1: Actual(GPT) YES/Predicted(label) NO = 13, Actual NO/Predicted YES = 7, TP 84, TN 94; Supplement Table S3 sums FN 13, FP 7, TN 97, TP 85, so the note is accurate.
```diff
- - The 113-paper figure is the per-paper denominator; the actual classification denominator for the headline F1 is the pooled 20% TEST split of (paper-section, question) pairs, Figure 1's confusion matrix shows 198 instances.
+ - The 113-paper figure is the per-paper denominator; the actual classification denominator for the headline F1 is the pooled 20% TEST split of (paper-section, question) pairs, Figure 1's confusion matrix shows 198 instances.
+ - PDF check 2026-11-17: Figure 1's caption says the y-axis is GPT-4's answers and the x-axis Schulz et al.'s labels, which makes 13 the false-YES count and 7 the false-NO count. Supplementary Table S3, summed over questions 1–9, gives the reverse (FN = 13, FP = 7) and slightly different cell totals (TP 85, TN 97). The axis labels in Figure 1 are probably swapped.
```

#### [[EVD - GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57%]]

- [ ] **Change 58** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=4|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 4]]
    - Auditor evidence: page 4–5, Image analysis: "Ten of the papers contained a flow diagram ... (answer 'YES' to ... question 10) but did not include reasons ... (answer 'NO' to ... question 11) ... The remainder had complete flow diagrams (answer 'Yes' to both questions) ... a sample of 10 flow diagrams which did not show participant flow through a clinical trial was included in the dataset for one question (table 2, question 10)"; Table 1 p. 3: item 10 adherence 100%*, item 11 50%*
    - Checker: Wrightson pp.4-5 Image analysis: 10 papers with flow diagrams lacking reasons (Q10 YES, Q11 NO), remainder complete (YES both), plus 10 non-participant-flow diagrams for question 10 only; Table 1 p.3 items 10/11 n=20, adherence 100%/50%.
```diff
- the diagram source (10 papers known to contain a flow diagram, plus 10 supplementary non-flow-diagram images included to test that the model does not just label every image as a CONSORT diagram)
+ the diagram source (20 papers with participant flow diagrams, 10 lacking exclusion reasons and 10 complete, plus, for Q10 only, 10 supplementary flow diagrams that did not show participant flow through a clinical trial, included to test that the model does not just label every flow diagram as a CONSORT diagram)
```

- [ ] **Change 59 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=4|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 4]]
    - Auditor evidence: page 4–5: "The remainder had complete flow diagrams (answer 'Yes' to both questions)"; "a sample of 10 flow diagrams which did not show participant flow through a clinical trial was included ... for one question (table 2, question 10)"; Supplement Table S3 footnote: "includes 10 flow diagrams not taken from the papers in dataset"
    - Checker: Wrightson p.5 text as above; Supplement Table S3 footnote '10 flow diagrams not taken from the papers in dataset'.
```diff
- (2) Build a 10-paper distractor set, sample 10 flow diagrams from the dataset that show clinical-trial flow but **not** the participant-level CONSORT structure (Q10 = NO). (3) Combine to form n = 20 images
+ (2) Add the 10 papers with complete flow diagrams (Q10 = YES, Q11 = YES); for Q10 only, add 10 distractor flow diagrams that did not show participant flow through a clinical trial (Q10 = NO; per Supplementary Table S3 these were not taken from the dataset papers). (3) Combine to form the n = 20 paper subset
```

- [ ] **Change 60 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=4|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 4]]
    - Auditor evidence: page 4–5 Image analysis text (see above); Table 1 p. 3 items 10/11: "20*" pairs, adherence "100%*" and "50%*"; Supplement Table S3 footnote "includes 10 flow diagrams not taken from the papers in dataset"
    - Checker: Same pp.4-5 text, Table 1 p.3 and Table S3 footnote; distractors were not drawn from the 113 papers.
```diff
- → augmented with **10 papers** drawn from the 113 whose Results figures showed clinical-trial flow but not CONSORT participant-level flow (distractors / Q10 = NO) → **n = 20 images** analysed
+ → plus **10 papers** with complete flow diagrams (Q10 = YES, Q11 = YES) → **n = 20 papers** analysed (Q10 additionally included 10 non-participant-flow distractor diagrams not taken from the dataset)
```

- [ ] **Change 61 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine]]
    - Auditor evidence: Supplement Table S3: Q10 FN 0, FP 0, TN 20*, TP 10 (=30); Q11 FN 1, FP 12, TN 8, TP 9 (=30, 17/30 = 57%); a 100% Clopper–Pearson CI with n=20 would have lower bound 83%, not the reported 89%
    - Checker: Table S3 counts sum to 30 for Q10 and Q11; 17/30 = 57% and its Wilson CI is 39%-73%, and 30/30 gives a lower bound of about 89%, whereas n=20 gives 83%; the 'CIs match n=20' claim is wrong.
```diff
- (n=20 in Table 2; CIs match the n=20 analysis).
+ (n=20 in Table 2; but the reported CIs and Supplementary Table S3 counts imply about 30 images per question, see PDF check note below).
```

- [ ] **Change 62 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf#page=3|Wrightson et al. - 2025 - GPT for RCTs Using AI to determine p. 3]]
    - Auditor evidence: Table 2 footnote p. 3: "*Analysis performed on a subset (n=20) of the dataset." vs Supplement Table S3 rows for the two image questions (sum 30 each)
    - Checker: Table 2 footnote p.3 n=20 vs Supplement Table S3 rows summing to 30 per image question; 57% is unreachable with n=20.
```diff
- - Q11's 57% accuracy (95% CI 39%–73%) is barely above chance for a binary task, and the lower CI bound (39%) is well below 50%.
+ - Q11's 57% accuracy (95% CI 39%–73%) is barely above chance for a binary task, and the lower CI bound (39%) is well below 50%.
+ - PDF check 2026-11-17: the paper reports n=20 for the image questions (Table 1, Table 2 footnote), but Supplementary Table S3 counts sum to 30 per question (Q10: TP 10, TN 20 including 10 external distractors; Q11: TP 9, TN 8, FP 12, FN 1, so 17/30 = 57%). 57% is not reachable with n=20, and a 100% CI lower bound of 89% also implies about 30 cases.
```

### wuAutomatedNoveltyEvaluationa

#### [[EVD - Ours-SciBERT reached F1=0.83 on method novelty prediction]]

- [ ] **Change 129** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Wu et al. - 2024 - Automated novelty evaluation.pdf#page=1461|Wu et al. - 2024 - Automated novelty evaluation.pdf p. 1461]]
    - Auditor evidence: page 1461, Table 2, HK and LLMK columns: 'GPT-4o ... 0.68 0.68', 'Claude ... 0.69 0.68'
    - Checker: Wu p.1461 Table 2 HK and LLMK: Claude 0.69/0.68 vs GPT-4o 0.68/0.68, so Claude is the strongest zero-shot LLM.
```diff
- and the strongest zero-shot LLM (GPT-4o with HK+LLMK: F1 0.68 / Acc 0.68).
+ and the strongest zero-shot LLMs (Claude-3.5 with HK+LLMK: F1 0.69 / Acc 0.68; GPT-4o: F1 0.68 / Acc 0.68).
```

- [ ] **Change 130 ⚑** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Wu et al. - 2024 - Automated novelty evaluation.pdf#page=1461|Wu et al. - 2024 - Automated novelty evaluation.pdf p. 1461]]
    - Auditor evidence: page 1461, Table 2: 'Claude 0.68 0.67 0.69 0.68'; page 1462: 'only LLama 3.1 shows performance improvement when HK and LLMK are used as inputs'
    - Checker: Wu Table 2 p.1461: Claude 0.68/0.67 (HK+MT) to 0.69/0.68 (HK+LLMK), GPT-4o and ChatGPT decline; p.1462 says 'only LLama 3.1 shows performance improvement'.
```diff
- - ALBERT showed the largest absolute gain
+ - PDF check 2026-11-17: the paper says only LLaMA 3.1 improved with HK+LLMK, but Table 2 shows Claude also rose slightly (F1 0.68 → 0.69, Acc 0.67 → 0.68); ChatGPT and GPT-4o declined.
+ - ALBERT showed the largest absolute gain
```

- [ ] **Change 131 ⚑** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wu et al. - 2024 - Automated novelty evaluation.pdf#page=1461|Wu et al. - 2024 - Automated novelty evaluation.pdf p. 1461]]
    - Auditor evidence: page 1461, Table 2: 'ALBERT 0.52 0.54 0.64 0.64'; 'Ours-ALBERT - - 0.76 0.77'
    - Checker: Wu Table 2: ALBERT 0.52 (HK+MT), 0.64 (HK+LLMK), Ours-ALBERT 0.76; 0.52 to 0.76 mixes input conditions; 0.64 to 0.76 (+0.12) is still the largest framework gain.
```diff
- (0.52 → 0.76 F1 with the Ours-ALBERT variant)
+ (ALBERT baseline F1 0.64 with the same HK+LLMK input → 0.76 with Ours-ALBERT; 0.52 with HK+MT)
```

- [ ] **Change 132 ⚑** · Missing comparator · checker: ACCEPT · PDF: [[source/pdfs/Wu et al. - 2024 - Automated novelty evaluation.pdf#page=1461|Wu et al. - 2024 - Automated novelty evaluation.pdf p. 1461]]
    - Auditor evidence: page 1461, Table 2 HK and MT: 'BERT 0.70 0.71', 'SciBERT 0.70 0.71'
    - Checker: Wu Table 2 HK and MT: BERT 0.70/0.71 and SciBERT 0.70/0.71 tie; 'GPT-4o-style' label is meaningless.
```diff
- GPT-4o-style: SciBERT F1 0.70 / Acc 0.71
+ SciBERT and BERT (tied) F1 0.70 / Acc 0.71
```

#### [[EVD - Removing knowledge module cut novelty accuracy from 0.84 to 0.74]]

- [ ] **Change 133** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Wu et al. - 2024 - Automated novelty evaluation.pdf#page=1461|Wu et al. - 2024 - Automated novelty evaluation.pdf p. 1461]]
    - Auditor evidence: page 1461, Implementation details: 'The trained model represents the best-performing model based on the test set results.'
    - Checker: Wu p.1461 Implementation details: 'The trained model represents the best-performing model based on the test set results'; no validation-based checkpoint selection is described.
```diff
- selected the best checkpoint on the validation split, evaluated on the same held-out test split
+ kept the best-performing checkpoint on the test set (the paper's stated practice for all models)
```

### xuCanLLMsIdentify2025

#### [[EVD - GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG]]

- [ ] **Change 76** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: PDF page 8 holds Table 3 ("Human 86.0% 3.52 82.0%"); the embed beside it is evd-p8-1
    - Checker: Rendered PDF p. 8 shows Table 3 (MARG 68.1%, Human 86.0%).
```diff
- MARG = 68.1% on LIMITGEN-Syn (Table 3, Xu et al., 2025, p. 9)
+ MARG = 68.1% on LIMITGEN-Syn (Table 3, Xu et al., 2025, p. 8)
```

- [ ] **Change 77** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: PDF page 8, Section 6.1: "Even the best-performing LLM, GPT-4o, can only identify about half of the limitations"
    - Checker: Rendered p. 8, Sec 6.1: '...GPT-4o, can only identify about half of the limitations that humans consider very obvious.'
```diff
- humans consider very obvious." (Xu et al., 2025, p. 9)
+ humans consider very obvious." (Xu et al., 2025, p. 8)
```

- [ ] **Change 78** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=7|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 7]]
    - Auditor evidence: PDF page 7, Section 5.1: "We evaluate the performance of 4 frontier LLMs"; embed is evd-p7-1
    - Checker: '...ensuring a fair comparison across systems' is in Sec 5.1 on PDF p. 7 (page 7 starts at the form feed before the Table/Sec 5 text).
```diff
- ensuring a fair comparison across systems." (Xu et al., 2025, p. 6)
+ ensuring a fair comparison across systems." (Xu et al., 2025, p. 7)
```

- [ ] **Change 79** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=6|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 6]]
    - Auditor evidence: PDF page 6, Section 4.2: "For LIMITGEN-Syn, we use GPT-4o to classify the generated limitations"; embed is evd-p6-1
    - Checker: '...limitation accurately matches the subtype' (Sec 4.2) falls on PDF p. 6 in the text layer, after the page-6 break.
```diff
- accurately matches the subtype." (Xu et al., 2025, p. 5)
+ accurately matches the subtype." (Xu et al., 2025, p. 6)
```

- [ ] **Change 80** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=5|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 5]]
    - Auditor evidence: PDF page 5, Section 3.3: "we compile an initial pool of 1,408 NLP papers ... This filtering process led us to 500 papers"; embed is evd-p5-1
    - Checker: 'This filtering process led us to 500 papers' (with the 1,408-paper pool) is in Sec 3.3 on PDF p. 5.
```diff
- This filtering process led us to 500 papers." (Xu et al., 2025, p. 4)
+ This filtering process led us to 500 papers." (Xu et al., 2025, p. 5)
```

- [ ] **Change 84** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: page 8, Table 3 caption: "For human evaluation, we randomly sample 100 examples"; page 15, A.4: "we randomly sample 50 examples from each subset. Two expert annotators (i.e., Annotators 1 and 6, as described in Table 7) independently solve these examples. During human evaluation, the expert evaluators are not informed of the sources"
    - Checker: p. 8 Table 3 caption: human evaluation used 100 randomly sampled examples; p. 15 A.4: the human baseline sampled 50 examples per subset solved by Annotators 1 and 6, and evaluators 'are not informed of the sources'. The page conflated the two.
```diff
- (4) Parallel human evaluation: 100 examples sampled from LIMITGEN-Syn; two expert annotators (Annotators 1 and 6, both with NLP/AI publications) independently solve them blind to system identity and the human baseline accuracy is reported (86.0%).
+ (4) Human evaluation of system outputs: 100 examples sampled from LIMITGEN-Syn, rated by evaluators blind to which system produced each limitation. Separately, the human baseline (86.0%) comes from 50 examples per subset solved independently by two expert annotators (Annotators 1 and 6 per Appendix A.4).
```

- [ ] **Change 85** · Paper contradicts itself (note added, quote untouched) · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=14|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 14]]
    - Auditor evidence: page 14, Table 7 (rendered image): Human Performance ✓ in rows 2 (>10) and 6 (1-5); page 15, A.4: "Two expert annotators (i.e., Annotators 1 and 6, as described in Table 7)"
    - Checker: Rendered p. 14 Table 7: Human Performance is ticked for annotators 2 (>10) and 6 (1-5), and Annotator 1 is ticked for Human Evaluation; p. 15 A.4 names Annotators 1 and 6. A genuine inconsistency, added as a note.
```diff
- - Cohen's κ between the two LIMITGEN-Syn evaluators = 0.833 (high agreement); automated-vs-accuracy correlation = 0.96 supports use of GPT-4o as judge.
+ - Cohen's κ between the two LIMITGEN-Syn evaluators = 0.833 (high agreement); automated-vs-accuracy correlation = 0.96 supports use of GPT-4o as judge.
+ - PDF check 2026-11-17: Appendix A.4 (p. 15) names Annotators 1 and 6 as the human-baseline solvers, but Table 7 (p. 14) ticks "Human Performance" for Annotators 2 and 6 (Annotator 1 is ticked for "Human Evaluation"). Both 1 and 2 have >10 publications, so the publication counts above are unaffected.
```

#### [[EVD - RAG raised GPT-4o limitation accuracy by 12.2 points]]

- [ ] **Change 81** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: PDF page 8 holds Table 3; embed is evd-p8-2
    - Checker: Rendered p. 8: Table 3 with GPT-4o Fine 1.34, w/ RAG +0.37.
```diff
- (+0.37) (Table 3, Xu et al., 2025, p. 9)
+ (+0.37) (Table 3, Xu et al., 2025, p. 8)
```

- [ ] **Change 82** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: PDF page 8, Section 6.2: "incorporating the RAG method can enhance LLM performance in refining their outputs"
    - Checker: Rendered p. 8, Sec 6.2: 'incorporating the RAG method can enhance LLM performance in refining their outputs.'
```diff
- refining their outputs." (Xu et al., 2025, p. 9)
+ refining their outputs." (Xu et al., 2025, p. 8)
```

- [ ] **Change 83** · Wrong page reference · checker: ACCEPT but HELD: edits the page citation on a quote line (quote words unchanged); JP to decide · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=6|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 6]]
    - Auditor evidence: PDF page 6, first line: "truth. We collect a total of 9,844 papers and randomly sample 1,000"; embed is evd-p6-2
    - Checker: PDF p. 6 opens with 'truth. We collect a total of 9,844 papers and randomly sample 1,000'.
```diff
- randomly sample 1,000 of them for experimentation." (Xu et al., 2025, p. 5)
+ randomly sample 1,000 of them for experimentation." (Xu et al., 2025, p. 6)
```

- [ ] **Change 86** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: page 8, Table 3 (rendered image): Qwen-2.5-72B 47.1%, w/RAG +1.2%
    - Checker: Rendered p. 8 Table 3: Qwen-2.5-72B coarse 47.1%, w/RAG +1.2%, so 48.3 (+1.2), not +1.3.
```diff
- | Qwen-2.5-72B | 47.1 → 48.4 (+1.3) |
+ | Qwen-2.5-72B | 47.1 → 48.3 (+1.2) |
```

- [ ] **Change 87** · Wrong number · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=8|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 8]]
    - Auditor evidence: page 8, Table 4 (rendered image): MARG w/ RAG "+2.5% +0.24 +0.52 +0.98 +0.43"
    - Checker: Rendered p. 8 Table 4: MARG w/ RAG row reads +2.5% +0.24 +0.52 +0.98 +0.43, so Faith. is +0.52, not +0.40.
```diff
- | MARG w/ RAG | +2.5 | +0.24 | +0.40 | +0.98 | +0.43 |
+ | MARG w/ RAG | +2.5 | +0.24 | +0.52 | +0.98 | +0.43 |
```

- [ ] **Change 88** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf#page=7|Xu et al. - 2025 - Can LLMs Identify Critical Limitations wi p. 7]]
    - Auditor evidence: page 7, Section 5.3: "If the paper is unavailable, we use GPT-4o-mini to generate a query based on the paper's abstract"
    - Checker: p. 7 Sec 5.3: 'If the paper is unavailable, we use GPT-4o-mini to generate a query based on the paper's abstract'.
```diff
- prompt GPT-4o to generate a query
+ prompt GPT-4o-mini to generate a query
```

### zhangReviewingScientificPapers2025a

#### [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3%]]

- [ ] **Change 137** · Wrong page reference · checker: SUPERSEDED by change z6 (v3 page numbers); do not apply · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: Archive v1 PDF: Table 2 is on page 4 and "Table 3: Hit rate results by individual judge." is on page 7
    - Checker: The page's values (Claude PDF HR 16.3%, LaTeX 33.1%) come from the archived v1 text, where Table 2 falls on page 4 and 'Table 3: Hit rate results by individual judge' on page 7 by page-break count.
```diff
- Tables 2 and 3, pp. 3–4.
+ Tables 2 and 3, pp. 4 and 7 (arXiv v1).
```

### zhangReviewingScientificPapers2025a (v3 update)

#### [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3%]]

- [ ] **Change z0** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- LLM-as-judge with Gemini 2.5 Pro (`preview-05-06`) and o3 (`2025-04-16`).
+ LLM-as-judge with Gemini 2.5 Pro (`preview-06-05` in v3; v1 used `preview-05-06`) and o3 (`2025-04-16`) (v3 p. 4).
```

- [ ] **Change z1** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.3: "LLM checkers were evaluated by their Average Precision (AP@k) on test papers if nc = 1"; Table 2 now has an AP@5 column (PDF only); v1 value: v1 Table 2 (page 4) has only "Hit Rate @5 (%)", no precision metric
    - Checker: v3 p.4 Sec 2.3 defines AP@k for nc=1; v3 Table 2 p.5 has AP@5 for PDF rows only, LaTeX rows '–'; v1 Table 2 had HR only.
```diff
- **Dependent variables:** HR@5; **average
+ **Dependent variables:** HR@5; AP@5 (average precision of submissions judged true positives, PDF approach only; new in v3, p. 4); **average
```

- [ ] **Change z2** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "its overly low hit rate under the PDF-based approach indicates that it might not qualify for serving as a judge"; v3 page 6, Table 3: Claude PDF 24.1 / 12.2; v1 value: v1 page 3: "overly low hit rates under the PDF-based approach (Table 3) indicate that it is unqualified"; v1 Table 3: 21.6 / 19.2
    - Checker: v3 p.4 Sec 2.4 'overly low hit rate under the PDF-based approach indicates that it might not qualify' with no Table 3 pointer; v3 Table 3 p.6 Claude PDF 24.1/12.2; v3 p.4 Sec 2.3 judges assess true positives based on the PDF.
```diff
- **excluded Claude as a judge** because its low PDF-approach hit rates (Table 3: 21.6% / 19.2%) indicated it was unqualified to judge in this task.
+ **excluded Claude as a judge** because its overly low PDF-approach hit rate indicated it "might not qualify" as a judge (v3 p. 4; v3 no longer points to Table 3 here, and v3 Table 3 single-judge PDF hit rates for Claude as checker are 24.1% / 12.2%). In v3 the same two judges also rate each submission as a true problem or a false alarm against the PDF, which yields AP@5 (v3 p. 4).
```

- [ ] **Change z3** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- LLM judges are Gemini 2.5 Pro and o3 (Claude was disqualified from the judge pool).
+ LLM judges are Gemini 2.5 Pro (`preview-06-05` in v3) and o3 (Claude was disqualified from the judge pool).
```

- [ ] **Change z4** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: Claude 3.7 Sonnet HR@5 "11.0" (PDF), "24.1" (LaTeX); Avg 1.6 / 3.4; v1 value: v1 Table 2: 16.3 (PDF), 33.1 (LaTeX)
    - Checker: v3 Table 2 p.5 (rendered): Claude HR@5 11.0 (PDF) / 24.1 (LaTeX), Avg 1.6 / 3.4; 24.1/11.0 = 2.2x so 'more than doubled' holds; v1 16.3/33.1 confirmed.
```diff
- - **Hit rate doubled under LaTeX (16.3% → 33.1%) and average problems submitted rose from 1.6 to 3.4**
+ - **Hit rate more than doubled under LaTeX (11.0% → 24.1%, v3 Table 2, p. 5) and average problems submitted rose from 1.6 to 3.4**
```

- [ ] **Change z5** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3: Claude PDF 24.1 / 12.2, LaTeX 48.6 / 26.5; v3 page 5, Table 2: Claude AP@5 36.4; v3 p.4: "the o3 checker found 350, Gemini Pro found 293, and Claude found only 149"; v1 value: v1 Table 3: PDF 21.6 / 19.2, LaTeX 44.5 / 40.8
    - Checker: v3 Table 3 p.6 (rendered): Claude 24.1/12.2 PDF, 48.6/26.5 LaTeX; v1 Table 3 21.6/19.2, 44.5/40.8. Note facts checked: v3 header p.1 (2505.23824v3, 1 Apr 2026, NeurIPS 2025 Workshop AI for Science), AP@5 36.4 highest, 350/293/149 counts p.4, 64.9% p.4, 'Claude's PDF ingestion pipeline or scientific understanding via PDF' p.4.
```diff
- - Single-judge HR@5 (Table 3) for Claude as checker: PDF (Gemini-judge 21.6%, o3-judge 19.2%); LaTeX (Gemini-judge 44.5%, o3-judge 40.8%).
+ - Single-judge HR@5 (v3 Table 3, p. 6) for Claude as checker: PDF (Gemini-judge 24.1%, o3-judge 12.2%); LaTeX (Gemini-judge 48.6%, o3-judge 26.5%).
+ - Version update 2026-11-17: tables and notes now follow arXiv v3 (arXiv:2505.23824v3 [cs.CL] 1 Apr 2026; NeurIPS 2025 AI for Science workshop version), while the page title, aliases, Description quote/summary line, verbatim quotes and screenshots still reflect v1 (arXiv:2505.23824v1, 28 May 2025). Headline v1 → v3 changes: Claude's combined HR@5 fell from 16.3% to 11.0% (PDF) and from 33.1% to 24.1% (LaTeX) because v3 swapped the Gemini judge to Gemini 2.5 Pro `preview-06-05` (v1 `preview-05-06`); the 64.9% no-problem share, problem counts, token usage and costs are unchanged; v3 adds a precision metric, AP@5 (PDF only), on which Claude scored highest of all five checkers (36.4% vs. o3 29.5%, Gemini 2.5 Pro 35.2%), though it produced only 149 judge-confirmed true problems vs. 350 for o3 (v3 p. 4); v3 reworded the PDF explanation from "Anthropic's PDF ingestion pipeline" to "Claude's PDF ingestion pipeline or scientific understanding via PDF" (v3 p. 4). The 16.3% in the title is a v1 figure; the v3 equivalent is 11.0%.
```

- [ ] **Change z6** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2 and v3 page 6, Table 3; v1 value: v1 Tables 2 and 3 on pp. 4 and 6
    - Checker: v3 Tables 2 and 3 are on pp.5 and 6; Claude AP@5 36.4 in Table 2.
```diff
- *Figures reproduced from Zhang & Abernethy (2025), Tables 2 and 3, pp. 3–4. Single-judge rows are from Table 3; the rest from Table 2.*
+ *Figures reproduced from Zhang & Abernethy, arXiv v3 (1 Apr 2026), Tables 2 and 3, pp. 5–6. Single-judge rows are from Table 3; the rest from Table 2. v3 Table 2 also reports AP@5 = 36.4% for Claude (PDF only; not tabulated here).*
```

- [ ] **Change z7** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "Claude 3.7 Sonnet 1.6 0, 4 11.0 36.4 43,357 1,630 311 0.159"; v1 value: v1 Table 2: "Claude 3.7 Sonnet 1.6 0 4 16.3 43,357 1,630 311 0.159"
    - Checker: v3 Table 2 p.5 (rendered): Claude PDF HR@5 11.0 (v1 16.3).
```diff
- | **Claude 3.7 Sonnet: PDF** | **16.3%** |
+ | **Claude 3.7 Sonnet: PDF** | **11.0%** |
```

- [ ] **Change z8** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "Claude 3.7 Sonnet 3.4 1, 5 24.1 – 28,284 2,701 515 0.133"; v1 value: v1 Table 2: "Claude 3.7 Sonnet 3.4 1 5 33.1 28,284 2,701 515 0.133"
    - Checker: v3 Table 2 p.5 (rendered): Claude LaTeX HR@5 24.1 (v1 33.1).
```diff
- | Claude 3.7 Sonnet: LaTeX | 33.1% |
+ | Claude 3.7 Sonnet: LaTeX | 24.1% |
```

- [ ] **Change z9** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, Claude 3.7 Sonnet (Gemini 2.5 Pro judge / PDF): 24.1; v1 value: v1 Table 3: 21.6
    - Checker: v3 Table 3 p.6 (rendered): Claude, Gemini judge, PDF 24.1 (v1 21.6).
```diff
- | Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 21.6% |
+ | Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 24.1% |
```

- [ ] **Change z10** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, Claude 3.7 Sonnet (o3 judge / PDF): 12.2; v1 value: v1 Table 3: 19.2
    - Checker: v3 Table 3 p.6 (rendered): Claude, o3 judge, PDF 12.2 (v1 19.2).
```diff
- | Single-judge HR@5 (o3 judge / PDF) | 19.2% |
+ | Single-judge HR@5 (o3 judge / PDF) | 12.2% |
```

- [ ] **Change z11** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, Claude 3.7 Sonnet (Gemini 2.5 Pro judge / LaTeX): 48.6; v1 value: v1 Table 3: 44.5
    - Checker: v3 Table 3 p.6 (rendered): Claude, Gemini judge, LaTeX 48.6 (v1 44.5).
```diff
- | Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 44.5% |
+ | Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 48.6% |
```

- [ ] **Change z12** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, Claude 3.7 Sonnet (o3 judge / LaTeX): 26.5; v1 value: v1 Table 3: 40.8
    - Checker: v3 Table 3 p.6 (rendered): Claude, o3 judge, LaTeX 26.5 (v1 40.8).
```diff
- | Single-judge HR@5 (o3 judge / LaTeX) | 40.8% |
+ | Single-judge HR@5 (o3 judge / LaTeX) | 26.5% |
```

#### [[EVD - o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX]]

- [ ] **Change z13** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- two LLM judges (Gemini 2.5 Pro `preview-05-06` and o3 `2025-04-16`).
+ two LLM judges (Gemini 2.5 Pro `preview-06-05` in v3, `preview-05-06` in v1; and o3 `2025-04-16`) (v3 p. 4).
```

- [ ] **Change z14** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.3: "LLM checkers were evaluated by their Average Precision (AP@k) on test papers if nc = 1"; Table 2 now has an AP@5 column (PDF only); v1 value: v1 Table 2 (page 4) has only "Hit Rate @5 (%)", no precision metric
    - Checker: v3 p.4 Sec 2.3: precision judged per submission against the PDF, both judges must affirm, per-paper precision averaged as AP@k, cases with no problems skipped; Table 2 AP@5 PDF only.
```diff
- average / Q1 / Q3 number of problems identified, average input/think/output token usage
+ Average Precision at k=5 (AP@5; new in v3, PDF approach only: per-paper share of submissions that both judges rate as true problems against the PDF, averaged over papers, v3 p. 4), average / Q1 / Q3 number of problems identified, average input/think/output token usage
```

- [ ] **Change z15** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=11|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 11]]
    - Auditor evidence: v3 page 11, Appendix B: o3 and o4-mini "reasoning summary: \"auto\""; v1 value: v1 Appendix B: "reasoning summary: \"detailed\""
    - Checker: v3 Appendix B p.11: o3 and o4-mini reasoning summary "auto"; v1 Appendix B "detailed".
```diff
- reasoning summary = "detailed"
+ reasoning summary = "auto" (v3 Appendix B; v1 listed "detailed")
```

- [ ] **Change z16** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 3: "estimated based on the standard API pricing of the LLM vendors in June 2025"; v1 value: v1 page 3: "estimated based on API pricing at the time of our experiments in early May 2025"
    - Checker: v3 p.4 Sec 3 'standard API pricing of the LLM vendors in June 2025' (v1 p.3 'early May 2025'); v3 p.4 Sec 2.3/2.4 true-positive judging against the PDF with both judges required; AP@5 PDF only (Table 2).
```diff
- (7) Per-paper cost estimated from recorded token usage at early-May-2025 OpenAI pricing.
+ (7) Per-paper cost estimated from recorded token usage at standard June-2025 OpenAI API pricing (v3 p. 4; v1 used early-May-2025 pricing). (8) New in v3: each judge also rates each problem submission as a true problem or a false alarm with the paper PDF attached, and both must affirm for a true positive, giving AP@5 under the PDF approach only (v3 p. 4).
```

- [ ] **Change z17** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- plus 2 LLM judges (Gemini 2.5 Pro, o3 medium).
+ plus 2 LLM judges (Gemini 2.5 Pro `preview-06-05` in v3, o3 medium).
```

- [ ] **Change z18** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3: o3 (medium) PDF 80.4 / 50.2, LaTeX 79.2 / 51.4; v3 page 5, Table 2: HR@5 48.2 / 50.6; v3 page 4, Sec 3: "the hit rates of OpenAI o-series models remained around the same or slightly increased, suggesting resistance to format change or a higher familiarity with LaTeX"; v1 value: v1 page 3: "the hit rates of o-series models increased. This could suggest that they received specialized training with LaTeX or a larger LaTeX training set"; v1 Table 3: 72.7 / 75.5 (PDF), 75.5 / 80.4 (LaTeX)
    - Checker: v3 Table 2 p.5 (rendered) o3 48.2/50.6; v3 Table 3 p.6 (rendered) o3 checker Gemini judge 80.4/79.2, o3 judge 50.2/51.4; quoted phrases 'resistance to format change or a higher familiarity with LaTeX' and 'some resistance ... to potential false positives' are on v3 pp.4-5.
```diff
- - o3's HR@5 jumped from 64.9% (PDF) to 71.0% (LaTeX), suggesting OpenAI o-series models received specialized LaTeX training. Single-judge HR@5s (Table 3): Gemini-2.5-Pro judge 72.7% (PDF) / 75.5% (LaTeX); o3 judge 75.5% (PDF) / 80.4% (LaTeX), both-judges-affirm fusion drops these to 64.9% / 71.0%, demonstrating resistance of multi-judge approach to inflation.
+ - o3's HR@5 rose only slightly from 48.2% (PDF) to 50.6% (LaTeX) (v3 Table 2, p. 5), which v3 reads as "resistance to format change or a higher familiarity with LaTeX" rather than v1's suggestion of specialized LaTeX training. Single-judge HR@5s (v3 Table 3, p. 6): Gemini-2.5-Pro judge 80.4% (PDF) / 79.2% (LaTeX); o3 judge 50.2% (PDF) / 51.4% (LaTeX); both-judges-affirm fusion drops these to 48.2% / 50.6%, which v3 describes as "some resistance" of the multi-judge approach "to potential false positives".
```

- [ ] **Change z19** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: o3 (medium) "4.8 5, 5 48.2 29.5 16,594 3,152 729 0.064" (PDF) and "4.8 5, 5 50.6 – 21,990 3,156 927 0.077" (LaTeX); v1 value: v1 Table 2: o3 64.9 / 0.321 (PDF), 71.0 / 0.383 (LaTeX)
    - Checker: v3 Table 2 p.5 (rendered): o3 thinking 3,152 vs Gemini Pro 14,228 unchanged, o3 highest HR; o3 48.2/50.6, cost 0.064/0.077, AP@5 29.5 vs 35.2/36.4, lead 48.2-39.2=9.0; 350 vs 293 p.4; v3 abstract p.1 quote matches; v1 values 64.9/71.0, 0.321/0.383 confirmed.
```diff
- yet achieved the highest HR, "potentially overthinking behavior did not result in higher hit rates."
+ yet achieved the highest HR, "potentially overthinking behavior did not result in higher hit rates." (Token counts unchanged in v3 Table 2, p. 5.)
+ - Version update 2026-11-17: tables and notes now follow arXiv v3 (arXiv:2505.23824v3 [cs.CL] 1 Apr 2026; NeurIPS 2025 AI for Science workshop version), while the page title, aliases, Description summary line, verbatim quotes and screenshots still reflect v1 (arXiv:2505.23824v1, 28 May 2025). Headline v1 → v3 changes: o3 is still the top checker by hit rate, but its combined HR@5 fell from 64.9% to 48.2% (PDF) and from 71.0% to 50.6% (LaTeX) after v3 switched the Gemini judge to Gemini 2.5 Pro `preview-06-05`, and its lead over Gemini 2.5 Pro shrank to 9.0 pp (PDF, 48.2 vs. 39.2); estimated cost fell from $0.321 to $0.064 per paper (PDF) and from $0.383 to $0.077 (LaTeX) because v3 uses June-2025 standard pricing instead of early-May-2025 pricing; v3 adds AP@5 (PDF only), on which o3 scored 29.5%, below Gemini 2.5 Pro (35.2%) and Claude 3.7 Sonnet (36.4%), though o3 produced the most judge-confirmed true problems (350 vs. 293 for Gemini 2.5 Pro, v3 p. 4). The abstract sentence quoted in the Description ("o3 performed the best, while o4-mini was the most cost-effective") is v1 wording; v3's abstract says "o3 exhibited the best problem identification performance among all models at a modest cost." The 64.9% and 71.0% in the title are v1 figures.
```

- [ ] **Change z20** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o3 (medium) 4.8 5, 5 48.2 29.5 16,594 3,152 729 0.064"; v1 value: v1 Table 2: "o3 (medium) 4.8 5 5 64.9 16,594 3,152 729 0.321"
    - Checker: v3 Table 2 p.5 (rendered): o3 PDF 4.8 (5,5) 48.2, 16,594/3,152/729, $0.064.
```diff
- | **o3 (medium): PDF** | **64.9%** | 4.8 (5, 5) | 16,594 | 3,152 | 729 | $0.321 |
+ | **o3 (medium): PDF** | **48.2%** | 4.8 (5, 5) | 16,594 | 3,152 | 729 | $0.064 |
```

- [ ] **Change z21** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o3 (medium) 4.8 5, 5 50.6 – 21,990 3,156 927 0.077"; v1 value: v1 Table 2: "o3 (medium) 4.8 5 5 71.0 21,990 3,156 927 0.383"
    - Checker: v3 Table 2 p.5 (rendered): o3 LaTeX 4.8 (5,5) 50.6, 21,990/3,156/927, $0.077.
```diff
- | **o3 (medium): LaTeX** | **71.0%** | 4.8 (5, 5) | 21,990 | 3,156 | 927 | $0.383 |
+ | **o3 (medium): LaTeX** | **50.6%** | 4.8 (5, 5) | 21,990 | 3,156 | 927 | $0.077 |
```

- [ ] **Change z22** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, o3 (medium) checker (Gemini 2.5 Pro judge / PDF): 80.4; v1 value: v1 Table 3: 72.7
    - Checker: v3 Table 3 p.6 (rendered): o3 checker, Gemini judge, PDF 80.4 (v1 72.7).
```diff
- | Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 72.7% |
+ | Single-judge HR@5 (Gemini 2.5 Pro judge / PDF) | 80.4% |
```

- [ ] **Change z23** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, o3 (medium) checker (o3 judge / PDF): 50.2; v1 value: v1 Table 3: 75.5
    - Checker: v3 Table 3 p.6 (rendered): o3 checker, o3 judge, PDF 50.2 (v1 75.5).
```diff
- | Single-judge HR@5 (o3 judge / PDF) | 75.5% |
+ | Single-judge HR@5 (o3 judge / PDF) | 50.2% |
```

- [ ] **Change z24** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, o3 (medium) checker (Gemini 2.5 Pro judge / LaTeX): 79.2; v1 value: v1 Table 3: 75.5
    - Checker: v3 Table 3 p.6 (rendered): o3 checker, Gemini judge, LaTeX 79.2 (v1 75.5).
```diff
- | Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 75.5% |
+ | Single-judge HR@5 (Gemini 2.5 Pro judge / LaTeX) | 79.2% |
```

- [ ] **Change z25** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=6|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 6]]
    - Auditor evidence: v3 page 6, Table 3, Hit Rate Evaluation, o3 (medium) checker (o3 judge / LaTeX): 51.4; v1 value: v1 Table 3: 80.4
    - Checker: v3 Table 3 p.6 (rendered): o3 checker, o3 judge, LaTeX 51.4 (v1 80.4).
```diff
- | Single-judge HR@5 (o3 judge / LaTeX) | 80.4% |
+ | Single-judge HR@5 (o3 judge / LaTeX) | 51.4% |
```

#### [[EVD - o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3]]

- [ ] **Change z26** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- LLM-as-judge pipeline with Gemini 2.5 Pro (`preview-05-06`) and o3.
+ LLM-as-judge pipeline with Gemini 2.5 Pro (`preview-06-05` in v3; v1 used `preview-05-06`) and o3 (v3 p. 4).
```

- [ ] **Change z27** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 3: "estimated based on the standard API pricing of the LLM vendors in June 2025"; v1 value: v1 page 3: "estimated based on API pricing at the time of our experiments in early May 2025"; v3 page 4, Sec 2.3: "LLM checkers were evaluated by their Average Precision (AP@k) on test papers if nc = 1"; Table 2 now has an AP@5 column (PDF only); v1 value: v1 Table 2 (page 4) has only "Hit Rate @5 (%)", no precision metric
    - Checker: v3 p.4 Sec 3 June-2025 standard pricing; v3 p.4 Sec 2.3 AP@k; Table 2 AP@5 PDF only.
```diff
- computed from token usage at OpenAI API pricing in early May 2025.
+ computed from token usage at standard OpenAI API pricing in June 2025 (v3 p. 4; v1 used early-May-2025 pricing). v3 also adds AP@5 (average precision of judge-confirmed true problems, PDF approach only).
```

- [ ] **Change z28** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=11|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 11]]
    - Auditor evidence: v3 page 11, Appendix B: o3 and o4-mini "reasoning summary: \"auto\""; v1 value: v1 Appendix B: "reasoning summary: \"detailed\""
    - Checker: v3 Appendix B p.11 reasoning summary "auto"; v1 "detailed".
```diff
- reasoning summary = detailed
+ reasoning summary = auto (v3 Appendix B; v1 listed detailed)
```

- [ ] **Change z29** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 3: "estimated based on the standard API pricing of the LLM vendors in June 2025"; v1 value: v1 page 3: "estimated based on API pricing at the time of our experiments in early May 2025"
    - Checker: v3 p.4 Sec 3 'standard API pricing of the LLM vendors in June 2025'.
```diff
- summed at early-May-2025 OpenAI API rates.
+ summed at standard June-2025 OpenAI API rates (v3 p. 4).
```

- [ ] **Change z30** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=4|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 4]]
    - Auditor evidence: v3 page 4, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-06-05, for its better performance on related benchmarks than preview-05-06) and o3 (2025-04-16)"; v1 value: v1 page 3, Sec 2.4: "The two LLM judges are Gemini 2.5 Pro (preview-05-06) and o3 (2025-04-16)"
    - Checker: v3 p.4 Sec 2.4 judges sentence (v1 p.3 says preview-05-06)
```diff
- LLM judges are Gemini 2.5 Pro and o3.
+ LLM judges are Gemini 2.5 Pro (`preview-06-05` in v3) and o3.
```

- [ ] **Change z31** · Version update (arXiv v1 to v3) · checker: MODIFY · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: o3 "48.2 ... 0.064" / "50.6 ... 0.077"; o4-mini "38.0 ... 0.038" / "38.8 ... 0.043"; Gemini 2.5 Flash "38.4 ... 0.033"; v1 value: v1 Table 2: o3 64.9 / 0.321, 71.0 / 0.383; o4-mini 59.6 / 0.038, 61.6 / 0.043; v1 p.3 "o4-mini seems to be the most cost-effective choice for this task" (absent from v3)
    - Checker: v3 Table 2 p.5 (rendered): o3 0.064/0.077, o4-mini 0.038/0.043 (ratios 1.68, 1.79), HR 48.2/38.0, 50.6/38.8, Flash 38.4 at 0.033; cost-per-hit arithmetic checks; no 'cost-effective' in v3. Modified only because 'matches o4-mini's hit rate (38.4%)' reads as if 38.4% were o4-mini's figure (it is Flash's; o4-mini is 38.0%).
```diff
- - Cost ratio: o3 PDF ($0.321) is **8.4×** more expensive than o4-mini PDF ($0.038); o3 LaTeX ($0.383) is **8.9×** more expensive than o4-mini LaTeX ($0.043). Performance gap is only 5.3 pp HR@5 (PDF) / 9.4 pp (LaTeX) → o4-mini wins on cost-per-hit by a wide margin under this prompting strategy.
+ - Cost ratio (v3 Table 2, p. 5): o3 PDF ($0.064) is **1.7×** as expensive as o4-mini PDF ($0.038); o3 LaTeX ($0.077) is **1.8×** as expensive as o4-mini LaTeX ($0.043). The HR@5 gap is 10.2 pp (PDF, 48.2 vs. 38.0) and 11.8 pp (LaTeX, 50.6 vs. 38.8). Cost per hit (cost divided by HR@5, our calculation) under PDF is about $0.10 for o4-mini vs. $0.13 for o3, so o4-mini's edge is now small, and Gemini 2.5 Flash roughly matches o4-mini's PDF hit rate (38.4% vs. 38.0%) at a lower cost ($0.033). v3 no longer calls o4-mini the most cost-effective choice.
```

- [ ] **Change z32** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: o3 48.2 / 50.6, o4-mini 38.0 / 38.8, Gemini 2.5 Pro 39.2 / 36.3, Flash 38.4 / 34.7; v3 page 4, Sec 3: "the hit rates of OpenAI o-series models remained around the same or slightly increased, suggesting resistance to format change or a higher familiarity with LaTeX"; v1 value: v1 page 3: "the hit rates of o-series models increased. This could suggest that they received specialized training with LaTeX or a larger LaTeX training set"
    - Checker: v3 Table 2 p.5 (rendered): o3 48.2->50.6, o4-mini 38.0->38.8, Gemini Pro 39.2->36.3, Flash 38.4->34.7; quote on v3 p.4 Sec 3.
```diff
- - Both o-series models gain HR@5 when switched from PDF to LaTeX (o3: 64.9 → 71.0; o4-mini: 59.6 → 61.6), unlike Gemini models which degraded slightly under LaTeX, suggesting OpenAI models received specialized LaTeX training.
+ - Both o-series models hold roughly steady or gain slightly when switched from PDF to LaTeX (o3: 48.2 → 50.6; o4-mini: 38.0 → 38.8; v3 Table 2, p. 5), unlike Gemini models whose hit rates decreased under LaTeX (Gemini 2.5 Pro 39.2 → 36.3; Flash 38.4 → 34.7). v3 reads this as "resistance to format change or a higher familiarity with LaTeX" (v3 p. 4), replacing v1's suggestion of specialized LaTeX training.
```

- [ ] **Change z33** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: o4-mini "4.7 5, 5 38.0 26.7 17,760 3,582 701 0.038"; v3 abstract p.1 "o3 exhibited the best problem identification performance among all models at a modest cost" (no o4-mini cost-effectiveness claim); v1 value: v1 abstract "o4-mini was the most cost-effective one in our evaluation"; v1 Table 2 o4-mini 59.6
    - Checker: v3 p.5 still says it 'remains unclear ... why o4-mini sometimes used slightly more input tokens than o3'; Table 2 o4-mini 38.0/38.8, AP@5 26.7 vs 29.5, costs unchanged; v3 abstract and text have no 'cost-effective'; v1 abstract and p.3 sentence confirmed.
```diff
- authors flag this as unexplained.
+ authors flag this as unexplained (unchanged in v3, p. 5).
+ - Version update 2026-11-17: tables and notes now follow arXiv v3 (arXiv:2505.23824v3 [cs.CL] 1 Apr 2026; NeurIPS 2025 AI for Science workshop version), while the page title, aliases, Description summary line, verbatim quotes and screenshots still reflect v1 (arXiv:2505.23824v1, 28 May 2025). Headline v1 → v3 changes: o4-mini's combined HR@5 fell from 59.6% to 38.0% (PDF) and from 61.6% to 38.8% (LaTeX) after v3 switched the Gemini judge to Gemini 2.5 Pro `preview-06-05`; o4-mini's own cost is unchanged ($0.038 / $0.043), but o3's estimated cost fell from $0.321 to $0.064 (PDF) and $0.383 to $0.077 (LaTeX) under June-2025 standard pricing, so the o3 / o4-mini cost ratio shrank from 8.4× to 1.7× (PDF) and 8.9× to 1.8× (LaTeX); v3 removes the sentence "o4-mini seems to be the most cost-effective choice for this task" (quoted in the Description and Methods Context, v1 p. 3) and the abstract's "o4-mini was the most cost-effective"; v3 adds AP@5 (PDF only), where o4-mini scored 26.7% vs. o3's 29.5%. The 59.6% and $0.321 in the title are v1 figures.
```

- [ ] **Change z34** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o4-mini (medium) 4.7 5, 5 38.0 26.7 17,760 3,582 701 0.038"; v1 value: v1 Table 2: "o4-mini (medium) 4.7 5 5 59.6 17,760 3,582 701 0.038"
    - Checker: v3 Table 2 p.5 (rendered): o4-mini PDF 38.0 (v1 59.6).
```diff
- | **o4-mini (medium): PDF** | **59.6%** |
+ | **o4-mini (medium): PDF** | **38.0%** |
```

- [ ] **Change z35** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o3 (medium) 4.8 5, 5 48.2 29.5 16,594 3,152 729 0.064" (0.064/0.038 = 1.7); v1 value: v1 Table 2: "o3 (medium) ... 64.9 16,594 3,152 729 0.321"
    - Checker: v3 Table 2 p.5 (rendered): o3 PDF 48.2, $0.064; 0.064/0.038=1.7.
```diff
- | o3 (medium): PDF | 64.9% | 16,594 | 3,152 | 729 | $0.321 | **8.4×** |
+ | o3 (medium): PDF | 48.2% | 16,594 | 3,152 | 729 | $0.064 | **1.7×** |
```

- [ ] **Change z36** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o4-mini (medium) 4.5 5, 5 38.8 – 22,287 3,421 685 0.043"; v1 value: v1 Table 2: "o4-mini (medium) 4.5 5 5 61.6 22,287 3,421 685 0.043"
    - Checker: v3 Table 2 p.5 (rendered): o4-mini LaTeX 38.8 (v1 61.6).
```diff
- | **o4-mini (medium): LaTeX** | 61.6% |
+ | **o4-mini (medium): LaTeX** | 38.8% |
```

- [ ] **Change z37** · Version update (arXiv v1 to v3) · checker: ACCEPT · PDF: [[source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf#page=5|Zhang and Abernethy - 2026 - Reviewing Scientific Papers for p. 5]]
    - Auditor evidence: v3 page 5, Table 2: "o3 (medium) 4.8 5, 5 50.6 – 21,990 3,156 927 0.077" (0.077/0.043 = 1.8); v1 value: v1 Table 2: "o3 (medium) ... 71.0 21,990 3,156 927 0.383"
    - Checker: v3 Table 2 p.5 (rendered): o3 LaTeX 50.6, $0.077; 0.077/0.043=1.8.
```diff
- | o3 (medium): LaTeX | 71.0% | 21,990 | 3,156 | 927 | $0.383 | **8.9×** |
+ | o3 (medium): LaTeX | 50.6% | 21,990 | 3,156 | 927 | $0.077 | **1.8×** |
```

### zhouLLMReliableReviewer2024

#### [[EVD - GPT-3.5 predicted review aspect scores at r=0.651]]

- [ ] **Change 143** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf#page=9342|Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf p. 9342]]
    - Auditor evidence: page 9342, Table 1: "given review 3. few-shot 0.306 1.132 0.651 0.659 0.580"
    - Checker: Table 1 (printed p. 9342): the few-shot given-review row with Pearson 0.651 / Spearman 0.659 is numbered '3. few-shot'; row 2 is zero-shot (0.548).
```diff
- (Table 1, row 2, p. 9342)
+ (Table 1, row 3, p. 9342)
```

- [ ] **Change 144** · Credited to the wrong model, rater or condition · checker: ACCEPT · PDF: [[source/pdfs/Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf#page=9342|Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf p. 9342]]
    - Auditor evidence: page 9342, Table 1: "7. selected sections 0.251 0.886 0.258"; "6. whole paper (GPT-3.5-16k) 0.138 2.132 0.131"
    - Checker: Table 1 (p. 9342): Pearson 0.258 is '7. selected sections'; '6. whole paper (GPT-3.5-16k)' is 0.131.
```diff
- (best Pearson ~0.258 for full paper)
+ (best Pearson 0.258 with selected sections; 0.131 with the whole paper)
```

#### [[EVD - GPT-4 RR-MCQ macro accuracy was 0.276]]

- [ ] **Change 145** · Wrong page reference · checker: ACCEPT · PDF: [[source/pdfs/Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf#page=8|Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf p. 8]]
    - Auditor evidence: Table 7 ("Results on RR-MCQ test data") is on PDF page 8, printed page 9347
    - Checker: Rendered PDF page 8: Table 7 ('Results on RR-MCQ test data', GPT-4 -> GPT-4 macro accuracy 0.276) sits on printed page 9347.
```diff
- (Table 7, p. 9346)
+ (Table 7, p. 9347)
```

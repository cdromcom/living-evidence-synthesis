---
page_type: log/audit
created: 2026-11-20
author: Claude (Opus 5.5, claude-opus-5-5) in Claude Code, for Jay Patel (JP)
human_verified: no
---

# Newer PDF versions: what changed (2026-11-20)

Six vault PDFs were preprints with a later published version (check of 2026-11-18). Four published versions were added to `source/pdfs` on 2026-11-20. The versions the EVD pages were built from were renamed with an "Archive - " prefix (the Zhang & Abernethy convention). `misc/scripts/keyword_freq_check.py` and `pangram_check.py` now point at the Archive names, so they still read the same files. Not yet obtained: **Akyon** (JMIR blocked the browser download; JP to download https://medinform.jmir.org/2024/1/e59258/PDF) and **Liang** (NEJM AI paywall; JP to download via UMD access).

Each paper was compared by a fresh-context Claude agent (text diff, table/figure images, EVD page check). Claude spot-checked page counts and the numbers unique to each version.

| Paper | Old (now Archive) | New | What changed | EVD pages |
|---|---|---|---|---|
| Xu et al. 2025 | arXiv v1 | ACL 2025 long, pp. 20652-20706 | Nothing of substance: identical text and images; ACL footer and page numbers only | 2 pages; statements hold |
| Thelwall 2025 | 2024 Word preprint | JDIS 10(1), 7-25 | Same results; copy edits; content shifts about one PDF page later | 2 pages; statements hold; a few quotes no longer character-exact; cited pages shift |
| Shahid et al. 2025 | arXiv v1 | SDP 2025, pp. 96-113 | Same results; citation years added, code link anonymised, one Limitations sentence and Fig. 5 caption reworded | 3 pages; content unaffected by the version change |
| Huntington-Klein & Murray 2026 | arXiv v1 (2024) | J Causal Inference 14(1) | **Substantive**: two new prompting methods, new data (Aug 2025; GPT-o1-pro, pinned Claude 3.5), responses 13,760 to 31,270 per model, Table 1 rebuilt, figures renumbered, option-order claim softened, new limitations paragraph; 27 to 30 pages | 2 pages; statements still hold numerically; quotes, counts and figure numbers out of date |

> [!warning] Errors found that exist in BOTH versions (not caused by the update)
> - **Shahid, "Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79%"**: the statement does not hold. 13.79% is the variant that keeps RankGPT with a general-relevance prompt; removing the re-ranker gives 10.34%. One Other Notes bullet also inverts the conclusion. (The blind relevancy judge flagged the same issue on 2026-11-17.)
> - **Huntington-Klein, kappa page**: the Description gives Claude's option-order kappa as .13 (the paper says .41; .13 is GPT-4o's), and "as low as 0.16" understates the lowest kappa (0.13). **Trimmed-confounders page**: three table/attribution errors (details in huntington-klein-diff.md).
> - **Thelwall, full-text page**: "GPT-4o titles 0.539" is a misread cell, and one quote is not verbatim ("may tend to obscure").
> - **Xu**: cited page numbers off by one; Qwen row 48.3 (+1.2), not 48.4 (+1.3); MARG faithfulness +0.52, not +0.40; "relevant literature", not "related"; the 86% baseline used 50 examples per subset.
> - **Shahid**: two quotes cited p.7 are on p.6; one quote has "formative study data" where the paper says "examples".

Per-paper details: `xu-diff.md`, `thelwall-diff.md`, `shahid-diff.md`, `huntington-klein-diff.md` (and matching `.json`). Nothing on the EVD pages, in the sheet or on the live site was changed.

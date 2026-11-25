# Shahid et al. (2025): arXiv v1 vs SDP 2025 published version

The published version (SDP 2025, pp. 96–113) has the same content as the arXiv v1 the evidence pages were built from. Title, authors, abstract, sections, data, sample sizes, models, dates, and every number in Tables 1–3 match; I compared Tables 1–3 as rendered page images. Both PDFs are 18 pages. The changes are editorial: in-text citations now include years, the code link points to an anonymised repository, one Limitations sentence and one figure caption were reworded, and the reference list was cleaned up. Reflow moves two section headings by one page. None of this changes what the three evidence pages report. Checking them did turn up a few errors that were already there before the version change, and one of them affects an evidence statement.

**Changes between versions**
- Code link (footnote 1, p2): `github.com/simra-shahid/idea_novelty_checker` became `anonymous.4open.science/r/idea_novelty_checker`.
- Limitations (p9): "OpenAI Deep Research and ScholarQA (Singh et al.)" became "DeepResearch and ScholarQA", and the Singh et al. reference was dropped.
- Figure 5 caption (p16): "so none of the optimized prompts (1 – 12) out-performed the original" became "showing that none of the optimized prompts (1 to 12) improved over the original".
- Citations: "(Lu et al.)" became "(Lu et al., 2024)" throughout, and "Mahajan et al." became "Freestone and Karmaker, 2024". Quotes that contain a citation are therefore no longer word for word.
- Layout and typesetting: the arXiv stamp is gone and the ACL footer and printed page numbers are new. NEW PDF page n is printed page 95 + n, so p6 is printed p. 101 and p7 is p. 102.

**Evidence page checks**
- **AI Scientist reached 0.47 accuracy**: the statement holds and all numbers are unchanged. The two quotes cited as p. 7 ("over 10 times…" and "It is important to note…") are on p. 6 in both versions. The screenshot labelled "Table 1, p. 7" shows the p. 6 sentence, not the table.
- **Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79%**: the numbers are unchanged, but the title is wrong in both versions. 13.79% is the result when RankGPT is kept and only its facet-based prompt is swapped for a general-relevance one. Dropping the LLM re-ranker entirely gives 10.34%. The third "Other Notes" bullet gets the conclusion backwards: the switch to general relevance causes most of the drop (89.66% to 13.79%), and removing the re-ranker entirely costs only about 3.5 more points (to 10.34%). The page needs a new title and that bullet rewritten.
- **Idea Novelty Checker reached 0.81 accuracy**: the statement holds and all numbers are unchanged. The baselines quote says "formative study data" where the paper says "formative study examples", and that mismatch is already in the old version. The screenshot labelled "Table 1, p. 7" is actually the abstract sentence on p. 1.
- All three pages: the screenshots come from the old PDF. Their filename page numbers still match the new PDF. If you re-source the pages to the published version, add citation years to the quotes and use printed page numbers.

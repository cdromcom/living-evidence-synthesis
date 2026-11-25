# Thelwall: preprint (2024) vs published JDIS version (2025)

The published version (JDIS 10(1), 7-25, doi 10.2478/jdis-2025-0011) has the same findings as the preprint the evidence pages were built from. Every number in the abstract, text and Tables 1-3 is identical, Figure 1 is visually identical, and the methods, section structure, limitations and conclusion are unchanged. The edits are copy-editing: one wording change in the iteration-count advice, a serial comma in the abstract, a reworded connective, two reference fixes, and the journal re-typesetting. That re-typesetting shifts most page numbers. The old PDF has 18 pages; the new one has 19 PDF pages, printed as journal pages 7-25, so PDF page n is journal page n+6. Both EVD statements still hold.

**Changes that touch the evidence pages**

- Iteration advice (Discussion 4.1; old p13, new p13 / journal p.19): "for general purposes **but** additional iterations" now reads "for general purposes **and** additional iterations". The GPT-4o r=0.67 page quotes the old wording in Other Notes.
- Abstract (p1 in both): "tables, figures and references" now reads "tables, figures, and references". The full-text-vs-abstracts page quotes the old wording.
- API-call sentence (old p5, new pp.5-6): the prompt now has curly quotes and no trailing space, so the r=0.67 page's quote is no longer character-exact. The words are unchanged.
- Page shifts for the cited material: Table 1 moves from p8 to p9 (journal p.15). The "optimal input" paragraph moves from p7 to p8 (p.14). The data and research-design passages move from p3 to p4 (p.10), and the datasets passage from p4 to p5 (p.11). The abstract stays on p1 (p.7). All screenshots show the old layout.

**Other changes (no effect on the EVDs)**

- "Nevertheless, both 4o and 4o-mini..." now begins "Despite this possibility, both 4o and 4o-mini..." (old p7, new p9).
- The introduction drops "The experimental results showed that" and repunctuates the bibliometrics sentence.
- Section 2.3 now says "basic REF system prompt".
- Two references were fixed: the Moed typo "evaluatio)" and the Zhou et al. proceedings name.
- The front matter now includes the received/revised/accepted dates, DOI, ORCID and the CC BY licence.
- Cosmetic only: sentence-case title, curly quotes, thousands separators, unnumbered References and Appendices, and Table 1's 0.678 is no longer bold.

**Problems that exist in both versions**

- On the full-text-vs-abstracts page, the title-only figure "GPT-4o at 0.539" is a misreading. That value is the correlation between GPT-3.5-turbo title predictions and GPT-4o abstract predictions. The paper never ran GPT-4o on titles.
- The same page puts quotation marks around "obscures the main value...", but the paper says "may tend to obscure the main value...".
- The paper's own text says 0.754 where Table 1 says 0.757, and 0.46 for titles where Table 1 says 0.434. The evidence pages repeat these inconsistencies.

Figures 2-5 were compared by caption only, and their images were not rendered. Full details are in `thelwall-diff.json`.

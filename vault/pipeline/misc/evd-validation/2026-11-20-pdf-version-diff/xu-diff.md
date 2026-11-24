# Xu et al. 2025: arXiv v1 vs ACL 2025 published version

The published ACL 2025 version (Long Papers, pp. 20652-20706) has the same content as arXiv v1. Both are 55 pages, and the text on every page matches word for word. The only differences are the arXiv stamp on page 1 being replaced by the ACL proceedings footer and the proceedings page numbers added at the foot of each page. Tables, figures, numbers, sections and conclusions are all the same, and every table and figure sits on the same PDF page. So neither evidence page is affected by the version change. Checking them against the paper did turn up a few transcription and citation errors that were already present in both versions.

- **Cosmetic only:** the arXiv stamp was replaced by the ACL footer, and printed page numbers were added (PDF page N is proceedings page 20651+N, so Table 3 on p.8 is p.20659). The PDF metadata also differs. Embedded images are identical.
- **EVD "GPT-4o reached 52%..."**: the statement still holds (52.0 / 86.0 / 68.1 in Table 3). All quotes are still verbatim. The in-text page citations are off by one: Table 3 and the "Even the best-performing" quote are on p.8, not p.9. The other three quotes are on pp.7, 6 and 5, not 6, 5 and 4. Screenshot filenames are correct. One minor point: the human baseline used 50 examples per subset (Appendix A.4), not the 100-example sample.
- **EVD "RAG raised GPT-4o... 12.2 points"**: the statement still holds (+12.2 in Table 3). Three errors exist in both versions:
  - The Qwen-2.5-72B row should read 47.1 -> 48.3 (+1.2), not 48.4 (+1.3).
  - The MARG faithfulness gain in the Table 4 summary is +0.52, not +0.40.
  - The p.7 quote says "relevant literature", not "related literature".
  
  Table 3 and its quote are on p.8, not p.9.
- **Optional:** update the source citation to the ACL version (doi 10.18653/v1/2025.acl-long.1009).

Details are in `xu-diff.json` in this folder.

# Lagging tasks

Outstanding work flagged during recent sessions but not yet done. Not a
roadmap — just a landing spot so these don't get lost between sessions.

## Content accuracy

- **Sync the canonical Obsidian vault's own node files to the new
  format.** `living-synthesis-site`'s 27 source pages now have the
  quote-grounded 42-item TRIPOD-LLM table and 10-11-row Quality Appraisal
  table; the canonical vault at `/Users/ppatel/Documents/living-synthesis/`
  (source of truth for future paper extractions, per `Skill.md`) still has
  the old 37-item / 5-row format on its own ~184 node files
  (source/EVD/CLM/CVT/QUE). The Skill.md docs now describe the new
  standard for *future* extractions, but the vault's *existing* papers
  haven't themselves been re-extracted to match. A real, separate,
  multi-batch job if/when wanted.
- **darcy's Data Leakage row** (`vault/source/@darcyMARGMultiAgentReview2024.md`)
  grounds its "partial" rating in two verified facts rather than one
  direct quote, since the paper never explicitly discusses training-data
  contamination. Not wrong, but worth a second look against the pilot's
  stricter single-quote convention.
- **zhangReviewingScientificPapers2025a version mismatch**
  (`vault/source/@zhangReviewingScientificPapers2025a.md`) — the cached
  PDF (`.cache/source-pdfs/zhangReviewingScientificPapers2025a.pdf`) is a
  later arXiv revision than what the file's existing Findings/TL;DR prose
  was written against (different headline numbers in Table 2, e.g. o3
  HR@5 48.2%/50.6% in the cached PDF vs. 64.9%/71.0% in the prose). The
  TRIPOD-LLM and Quality Appraisal tables are internally consistent with
  the cached PDF; the Findings section is not. Needs a decision: pull an
  earlier PDF revision matching the existing prose, or update the prose
  to match the current PDF.
- **shahid's formative-study idea counts** — the source PDF itself has an
  internal inconsistency (46+5 vs. 34+17, both summing to 51). The
  Quality Appraisal/TRIPOD quotes use the more detailed "46+5" framing;
  the vault's existing structured-abstract prose uses "34+17." Worth
  picking one and reconciling.

## Deferred by explicit scope decision

- **Full vault-wide em-dash sweep.** ~1,845 em dashes in editorial prose
  across 161 vault files (SRC/EVD/CLM/CVT/QUE combined), plus the 115 in
  shared component/UI copy (already done). Only the 2 pilot files
  (louAAAR10, woelfle) and the shared component copy have been cleaned up
  so far. Scoped as its own follow-up project, similar in size to the
  TRIPOD rollout, given a context-sensitive rewrite (comma vs. semicolon
  vs. colon vs. new sentence per Grammarly's rule) can't be done as a
  mechanical find-replace.
- **FAIR data-quality signals.** Floated as a possible new trust signal
  (Findable/Accessible/Interoperable/Reusable subscores per source) —
  never scoped or started. Comparable effort to the Rigor-chip rollout.

## Known gaps, not currently blocking anything

- **Altmetric badge shows "Unavailable" on every page right now** because
  `badges.altmetric.com` (Altmetric's own image CDN) has been returning
  HTTP 503 site-wide — confirmed unrelated to any specific paper's DOI.
  The fallback code is working as intended; nothing to fix unless
  Altmetric's service itself comes back and the badge still doesn't
  render (worth a spot-check later).
- **A hydration-mismatch console warning** was observed on node detail
  pages during verification (`app/nodes/[id]/page.tsx`'s
  `dangerouslySetInnerHTML` article content). Didn't visibly affect
  rendering in any screenshot taken, and React's own warning text flags
  browser extensions as a common cause (plausible here — testing used the
  Claude-in-Chrome extension). Not chased further; worth a clean-profile
  re-check if it recurs.
- **Source credibility fields computed but not rendered.** DOI
  resolution, author track record, publication type, DOAJ listing,
  self-citation rate, citation count, and predatory-publisher flag are
  all still computed and stored in vault frontmatter but explicitly
  excluded from the page (`HANDLED_EXTRA_KEYS` in
  `app/nodes/[id]/page.tsx`). Real, verified data sitting unused — noted
  in `REVIEW.md`, not urgent.
- **NIH/NINDS study-design-rigor icons** (sample-size estimation,
  exploratory-vs-confirmatory framing) are computed
  (`getSampleSizeEstimation`, `getStudyType` in `lib/data.ts`) but no
  component currently renders them. Dead code, intentionally left in
  place rather than deleted.

## From earlier in this project (unrelated to the SRC-page work)

- **Roam graph reorg (megacoglab vault)** — paused mid-task, not
  cancelled, when work pivoted to `living-synthesis-site`. 151 of 191
  days (~725 of 862 target blocks) of JP's auto-dated Roam notes still
  need moving into `#[[🔖 JP: Bookmarks]]`. Do not resume without asking
  first — this is a different project entirely.
- **"Contribute a node" page isn't interactive yet.** It currently just
  explains in words how to manually add a note to the source vault. The
  planned next step is a real GitHub-OAuth-backed form that opens a pull
  request automatically. Credentials for this are collected and stored;
  the feature itself isn't built.

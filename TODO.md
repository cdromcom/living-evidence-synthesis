# Lagging tasks

Outstanding work flagged during recent sessions but not yet done. Not a
roadmap — just a landing spot so these don't get lost between sessions.

## Content accuracy

- **Re-crop 9 missing figure/table screenshots from the source PDFs.** As of
  2026-09-02 the site renders every `![[...]]` embed (451 crops across 184
  nodes), but nine embeds point at files that were never committed to
  `vault/**/Attachments/`. Those render as a dashed "Figure not available:
  &lt;name&gt;" placeholder naming the file, and `npm run preflight` prints the
  same list, so nothing fails silently — the figures are just absent.

  The PDFs are not in this repo (deliberately, see README). They're in the
  canonical Obsidian vault at
  `/Users/ppatel/Documents/living-synthesis/source/pdfs/`.

  Crops resolve by **bare filename**, so re-cropping to the exact name below
  and dropping it anywhere under `vault/**/Attachments/` is all that's needed
  — `scripts/sync-attachments.mjs` (runs in preflight) copies it into
  `public/vault-img/` and the placeholder becomes the image. No code change,
  no rebuild of the graph JSON required beyond the usual `node
  scripts/build-graph.mjs`.

  | Crop needed | Page | Used by |
  | --- | --- | --- |
  | `alharbi2024-table1cont-p5-1.png` | p.5 | EVD-010 |
  | `liangCanLargeLanguage2024a-aspects-p5-5.png` | p.5 | EVD-030 |
  | `liangCanLargeLanguage2024a-overlap-p3-3.png` | p.3 | EVD-033 |
  | `sonWhenAICoScientists2025-fig4-p6.png` | p.6 | EVD-049, EVD-062 |
  | `sonWhenAICoScientists2025-tables-p34-4.png` | pp.3–4 | EVD-062 |
  | `sonWhenAICoScientists2025-tables-p5-2.png` | p.5 | EVD-063 |
  | `thelwallEvaluatingResearchQuality2024-tables-p8-1.png` | p.8 | EVD-019, EVD-040 |
  | `wuAutomatedNoveltyEvaluationa-results-p10-1.png` | p.10 | EVD-070 |
  | `xuCanLLMsIdentify2025-clm-p8-2.png` | p.8 | CLM-024 |

  Page numbers are read off the filenames' own `-pN-` convention rather than
  from the nodes, so spot-check each against the paper before trusting it —
  `-p34-` in particular is ambiguous between "page 34" and "pages 3–4".
  Verify with `node scripts/sync-attachments.mjs`, which reports the count
  still missing.

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

## Corpus growth

- **Update the corpus using the Undermind.ai connector in Claude.** Use
  Undermind.ai (a research-paper discovery/search tool) via its Claude
  connector to find new papers relevant to this project's research
  question (LLMs for scientific peer review / evidence appraisal) and add
  them to the vault as new sources, following the same extraction +
  quote-grounded TRIPOD-LLM/Quality-Appraisal pipeline as the existing 27.
  **Not yet actionable in this session** — no Undermind.ai connector is
  currently connected/available (checked via tool search, nothing found).
  Needs the connector added to this Claude session/account first.

## Deferred by explicit scope decision

- **Full vault-wide em-dash sweep.** ~1,845 em dashes in editorial prose
  across 161 vault files (SRC/EVD/CLM/CVT/QUE combined), plus the 115 in
  shared component/UI copy (already done). Only the 2 pilot files
  (louAAAR10, woelfle) and the shared component copy have been cleaned up
  so far. Scoped as its own follow-up project, similar in size to the
  TRIPOD rollout, given a context-sensitive rewrite (comma vs. semicolon
  vs. colon vs. new sentence per Grammarly's rule) can't be done as a
  mechanical find-replace.
- ~~**FAIR data-quality signals.**~~ Done 2026-08-31 — shipped as the
  "Data Quality" chip (FAIR-Checker + license top-up hybrid, 14 sources
  scored). See `misc/data_quality_2026-08.md` in the vault.

## Awaiting a decision

- **Whether to formalize the power-analysis pilot into a real signal.**
  Post-hoc power was computed for Roberts 2023 (weak correlations, N=30),
  Thelwall 2024, Zhou et al. 2024, and Hasan et al. 2024 (Kendall's τ
  formula, not Pearson-r), emphasizing whether the studies could actually
  detect medium/large effects. Presented to the user but never wired into
  the site as a tagged signal (would follow the `forensic/*` /
  `reproduction-check` precedent, e.g. `forensic/power-check`) — asked
  whether to do so, no answer yet. Don't build this without checking in
  first, since it's a real scoping decision, not just an extension of
  existing work.

## Known gaps, not currently blocking anything

- **Sign-in emails are unauthenticated for their own From domain, so they
  land in spam.** Sign-in now works end to end (Supabase → Brevo SMTP →
  inbox, first confirmed delivery 2026-09-02), but the From address is
  `ppatel45@umd.edu` while the mail is relayed by Brevo. `umd.edu` cannot
  be made to authorize Brevo — no SPF include, no DKIM key — so every
  message fails SPF alignment and carries no aligned DKIM signature.
  Observed consequences: Gmail filed the first successful send as spam,
  and the self-addressed copy (From and To both `ppatel45@umd.edu`) never
  reached the mailbox at all, held by UMD's Cisco IronPort gateway
  (`mx1.umd.iphmx.com`) rather than appearing in Junk. Marking it "not
  spam" only trains that one mailbox; every new reviewer's filter judges
  it fresh. `umd.edu` publishes `p=none`, so nothing is hard-rejected —
  it just lands in spam. **Fix before inviting real reviewers:** register
  a domain, verify the *domain* (not a single sender) in Brevo so it
  issues SPF + DKIM records to publish, and point `smtp_admin_email` at
  something like `noreply@<domain>`. The same domain would also replace
  the `living-evidence-synthesis.vercel.app` Site URL, which is worth
  something on its own when asking researchers to trust a review site.
- **`verifyOtp` has never actually been exercised.** The 8-digit code has
  been confirmed to arrive, and `app/login/page.tsx` was corrected to
  match the project's `mailer_otp_length` of 8, but nobody has yet typed
  a code in and watched it land on `/review` signed in. Every link in the
  chain is verified individually; the last hop is not. Worth one manual
  run-through before assuming reviewer sign-in works.
- **Claude-in-Chrome browser extension was disconnected for the entire
  back half of a long 2026-08-31 session** (from the AI Writing Check
  work onward, through the Data Quality rollout). Every UI change since
  then was verified via `tsc --noEmit` + curl against the local dev
  server instead of an actual screenshot. Worth a Chrome restart and a
  real visual pass over the newer chips (Code Quality, Data Quality, the
  redundant-chip hiding) next time the extension is available.
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

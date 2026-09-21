# Lagging tasks

Outstanding work flagged during recent sessions but not yet done. Not a
roadmap — just a landing spot so these don't get lost between sessions.

## From the 2026-09-21 full read-through — for a human, not an LLM

Every node was read end to end on 2026-09-21 (Claude Opus 5). The five
mechanical problems found are already fixed and written up in `HISTORY.md`.
Everything below is a **judgement call about what the papers actually say**,
which is exactly the kind of decision this project does not delegate to a
model: each one needs somebody with the source PDF open. They are recorded
here as leads to check, **not** as agreed defects — the read-through was itself
done by an LLM, so treat every count as "claimed, verify before acting."

Do not hand this section to an agent to "fix." Ordered by how much is at stake.

- **~10 claims and patterns say something their own linked evidence does not
  support.** The clearest: a claim titled "Reasoning LLMs substantially
  outperform non-reasoning models" rests on a paper that only tested reasoning
  models, so it has no comparison to make; a pattern calls o4-mini
  "Pareto-dominant" when it is cheaper *and* less accurate than o3, which makes
  it Pareto-efficient instead. Others involve a stated mechanism the evidence
  does not establish, or a scope condition dropped from a quote. Each needs the
  paper checked, then either the node retitled or the evidence link removed.

- **Numeric disagreements inside individual nodes, ~30 spotted.** Examples of
  the kinds: arithmetic that cannot hold ("dropped 5 of 25 items, leaving 21"),
  a point estimate outside its own confidence interval (`95% (89–93%)`), a
  swapped false-positive/false-negative pair against the node's own confusion
  matrix, a title naming the wrong cell of the table below it, and percentages
  described as percentage points. These are individually small and individually
  wrong; a sweep cannot settle them because the right value is in the PDF.

- **Every Question's "Supporting Claims" list is keyword-matched, not
  topic-matched.** All 27 carry a visible note telling the reader to "verify
  each link is truly supportive before citing," and five list no claim from
  their own key paper. This is the single biggest credibility gap in the
  rendered site, and the fix is a curation pass, one question at a time.

- **~70 of 77 EVD "Other Notes" tables reproduce a paper's numbers with no
  attribution.** Same item as the long-standing captioning task below; the
  read-through confirms the count and that only one file follows the
  convention.

- **Quotes that do not support the row they sit in.** Several appraisal rows
  cite a quote describing a bias *control* as evidence of a bias, or quote an
  unrelated appendix. Distinct from the two self-quoting rows already fixed;
  these have real quotes that argue for a different verdict.

- **Two papers' appraisals disagree with each other on identical facts.** The
  same "we used only post-cutoff papers" mitigation is rated 🟡 in one source
  and 🔴 in another. Pick one reading and apply it to both.

- **Prose damage from the em-dash sweep, 50+ comma splices.** Two are
  boilerplate repeated across the corpus (the Quality-appraisal callout, spliced
  in 24 of 27 sources, and the TRIPOD callout in ~22), so those two are a
  find-and-replace once somebody approves the wording. The remaining ~25 sit in
  hand-written prose and want reading in context.

- **Frontmatter drift.** `TruthValue: 0.5` on all 31 claims looks like an
  unfilled placeholder; `NodeFormality` is split 45 lowercase `draft` against
  160 PascalCase `ReadyForInternal`; `apaYear: 2024` contradicts a 2025 citekey
  in three sources; one source records a DOI while its own note says "No DOI on
  record"; caveats are inconsistent about whether `Applies To` uses bullets.

- **Leftover extraction debris.** Six evidence files contain a literal
  `[Screenshot: ... pdftoppm ...]` shell command where an embed belongs; a
  stray `1` sits before a heading in two files and a stray `do` in a third;
  three idahl files have blockquotes broken by an unprefixed blank line.

- **One dangling wikilink**, in `EP - LLM performance varies substantially with
  prompt design...`: it points at `CLM - LLM novelty evaluation is highly
  sensitive to prompt variations...`, which does not exist. A caveat of nearly
  that name does, so the link probably wants repointing and relabelling.

- **The About page overstates the review status.** `app/about/page.tsx:82` tells
  readers "nothing in this corpus is committed without that human step," but 45
  nodes are published as "Initial AI draft" and 27 more carry a "Seed" status
  the page never explains. Either the sentence needs qualifying or those nodes
  need promoting — a claim about the project's own process, so it is yours to
  make, not a model's.

- **~150 unreferenced images** remain under `vault/**/Attachments/` after the 42
  byte-identical duplicates were deleted. They are not duplicates of anything,
  and some may be the missing crops listed below under different names. Worth
  a look before either deleting them or re-cutting figures from the PDFs.

## Content accuracy

- **Caption the 76 uncaptioned EVD "Other Notes" tables with the source
  paper's own table labels.** Each EVD carries one table under `## Other Notes`
  reproducing results from its source paper, but 76 of the 77 present those
  numbers with no attribution, so the site reads as though we assembled them.
  The one worked example is
  `EVD - Claude 3.7 Sonnet found no problem in 64.9%… - @zhangReviewingScientificPapers2025a.md`.

  The rendering convention already exists: an *italic line immediately above
  the table* (no blank line between) becomes the table's `<caption>` — see
  `promoteTableCaptions` in `lib/markdown.ts`. It stays readable in Obsidian,
  where a raw `<caption>` would not render at all. Format used in the pilot:

  ```
  *Figures reproduced from Zhang & Abernethy (2025), Tables 2 and 3, pp. 3–4.
  Single-judge rows are from Table 3; the rest from Table 2.*
  ```

  This needs the **actual table numbers from each source PDF**, which is why it
  is a manual pass rather than a script: the surrounding prose usually names a
  table ("Table 2 shows…") but not always, and several EVDs splice rows from two
  different tables, as the pilot did. PDFs are in the canonical Obsidian vault
  at `/Users/ppatel/Documents/living-synthesis/source/pdfs/`, not this repo.

  Do **not** caption the SRC `## Quality appraisal` and `## TRIPOD-LLM reporting
  summary` tables the same way — those are our own hand-scored assessments, not
  reproductions, and they already carry explanatory callouts on all 27 SRCs.

  Progress check: `grep -L '^\*.*\*$' ` won't do it cleanly; the count above
  came from checking the line directly preceding each table under Other Notes.

- **Re-crop 7 missing figure/table screenshots from the source PDFs.** As of
  2026-09-21 the site renders every `![[...]]` embed except seven, which point
  at files that were never committed to
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
  | `sonWhenAICoScientists2025-fig4-p6.png` | p.6 | EVD-049, EVD-062 |
  | `sonWhenAICoScientists2025-tables-p34-4.png` | pp.3–4 | EVD-062 |
  | `sonWhenAICoScientists2025-tables-p5-2.png` | p.5 | EVD-063 |
  | `thelwallEvaluatingResearchQuality2024-tables-p8-1.png` | p.8 | EVD-019, EVD-040 |
  | `wuAutomatedNoveltyEvaluationa-results-p10-1.png` | p.10 | EVD-070 |
  | `xuCanLLMsIdentify2025-clm-p8-2.png` | p.8 | CLM-024 |

  Two entries came off this list on 2026-09-21 without any re-cropping: the two
  Liang crops were misspelled references, not missing files (`-p5-5`/`-p3-3` in
  the notes against `-p5-05`/`-p3-03` on disk). Before cutting any of the seven
  above, check the ~150 unreferenced images still sitting in
  `vault/**/Attachments/` — several look like plausible matches (for instance
  `alharbi2024-tables-p4-05.png` against the missing `alharbi2024-table1cont-p5-1.png`),
  and repointing an embed is cheaper than re-cropping a PDF.

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
  **Now actionable** — the Undermind connector is available as of 2026-09-21,
  so the blocker recorded here previously (no connector on the account) is
  gone. The work itself has not been started.

## Deferred by explicit scope decision

- ~~**Full vault-wide em-dash sweep.**~~ Done 2026-09-02 — 1,527 rewrites
  across 161 files, chosen per occurrence rather than swept. The ~1,845
  estimate counted every em dash in the files; the real figure for editorial
  prose was 900, because 744 sit inside table rows where an em dash is the
  *not-applicable placeholder* in a results cell rather than punctuation, and
  a mechanical pass would have rewritten those into commas and corrupted every
  results table. A further 8 sit inside quotation marks and belong to the
  quoted author; all 3,335 quoted spans were verified byte-identical
  afterwards. Replacements: 896 commas, 346 colons on compound table labels,
  150 paired parentheticals, 100 semicolons, 35 colons introducing
  enumerations.
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

- ~~**Possible open redirect after GitHub sign-in.**~~ Fixed 2026-09-21. It was
  real: `app/api/github/callback/route.ts` resolved the attacker-supplied
  `next` cookie against `request.url`, and an absolute URL there wins, so the
  visitor left the site. `sameSitePath()` in that file now accepts only a path
  beginning with a single `/`, rejecting `//` and `/\` protocol-relative
  targets and anything that fails to decode.
- **Git history still contains the removed Woelfle full-text file.**
  `vault/evidence/Attachments/woelfleBenchmarkingHumanAICollaboration2024-bbox.html`
  was deleted on 2026-09-18, but it remains in earlier commits on GitHub.
  Fully removing it needs a history rewrite (e.g. `git filter-repo`) and a
  force-push, which changes every commit hash. Decide whether that is worth
  doing.

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
- ~~**"Contribute a node" page isn't interactive yet.**~~ Built since this was
  written: `components/ContributeForm.tsx` posts to `app/api/contribute/route.ts`,
  which forks the repo, commits the new node on a branch via `lib/github.ts`,
  and hands back a compare link. Still unverified end to end against a real
  GitHub account, which is the part worth doing next.

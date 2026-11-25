# LIVES redesign: improved plan (v3, 2026-11-25)

F = Claude Fable 5.2, S = GPT-6.2 Sol; numbers refer to their points.

## 1. Adopted

**Page structure**
- F1, S1, S3: templates for all six page types and a persistent QUE › CLM › EVD › SRC chain. The drill-down is the product.
- F2 (part): last-updated date, version and a "Cite this" permalink. Pages that change silently cannot be cited.
- F3, S2: domain rows showing the worst status, with Concern and Split rows auto-opened. Readers see what could change their judgment.
- S2: Not reported, Not assessed and Not applicable become separate statuses. They mean different things to a reviewer.
- F4, S3: the footer becomes native `<details>` and the byline links to it. Hover expansion shifts layout.
- F5, S9: cut the resize handle and forms, and add a "Report a problem" link per EVD. Nothing in the design used the cut items.
- S1: stable anchors on quotes and assessments, for precise sharing.
- S3: search shows type words and excerpts, plus browse-by-type links. IDs alone don't disambiguate.

**Color**
- F6: node types are not color-coded, because 11 categories exceed 8 colors.
- F7: palette colors are used only as fills behind ink, with separately tuned dark values. Several colors fail 3:1 on cream.
- F8, S4: links are ink, underlined, with a distinct visited style. Green links read as verdicts, and the visited style tracks what has been checked.
- S4: quality rows stay neutral, and only Concern and Split get emphasis, so emphasis keeps its meaning.
- F9: screenshots get a border, are never inverted, and are tested in forced-colors mode.

**Typography**
- F10, S5: quotes use a reading face with a left rule and a "Verbatim" label. Mono hurts long reading.
- F11: anything actionable is at least 0.875 rem, since locators are verification data.
- S5: show the printed and PDF page numbers when they differ.
- F12: subsetted variable fonts, body face preloaded, `size-adjust` fallbacks. This avoids swap shift and saves files.

**Layout and spacing**
- F13: the breakpoints are resolved (see section 3), because the spec contradicted itself.
- F14, S7: a cropped passage with context, and the full page on demand. A full page at 70 characters is unreadable.
- F15, S9: `scroll-padding-top`, and a test for 2.4.11 (Focus Not Obscured).
- F16, S6: the quality table stacks on mobile, scroll regions are labelled, and layouts are tested at 320 px and 400% zoom.
- S1, S6: the decisive caveat sits beside the finding in every layout and in print.

**Visuals**
- S7: selectable quote text and the source link lead, and the screenshot is the check.
- F17, S7: a licensing policy is set before build, with a DOI link fallback.
- F18, S7: alt text gives location, not the quote, and `figure`/`figcaption` binds image and quote. This avoids a double read-out.
- F19: status icons differ by shape, and the highlight has an outline as well as a tint.
- F20: images get explicit dimensions, AVIF, and lazy loading below the fold.

**Animation**
- F21: no `<details>` height animation.
- F22, S8: the graph layout is precomputed and rendered settled, with physics on drag only, no re-settle on selection, and a pause control. This removes the reduced-motion fork and meets 2.2.2.
- S8: the focus ring is not animated, search results are not delayed, and the image viewer shows a loading state.

**Accessibility**
- F23, S9: a defined focus sequence (heading, fragment target, Back restores position, return to opener).
- F24: a library combobox with a live count, and Radix Tooltip dropped. Hand-rolled comboboxes usually fail.
- F25: screen-reader passes after the node page and after search.
- F26, S10: 3–5 reviewer sessions on "verify this claim". Axe misses lost reading position.
- F27: 24 px targets, `aria-sort` on buttons, and print expands everything and shows URLs.
- S10: the graph list supports finding a node, inspecting labelled relationships and following them.

**Build**
- F28, S11: the test harness comes first, then a CLM → EVD → SRC vertical slice.
- F29, S11: node pages are server-rendered, and the search index and graph data load lazily.
- F30, S11: performance budgets are enforced in CI.
- F31, S12: integrity checks run from phase 1.
- F32, S12: each phase has acceptance criteria and a named human approver.

## 2. Rejected or deferred
- **S4, categorical colors for page types: rejected.** Combined with statuses, they exceed the palette, and a glyph plus ID prefix suffices.
- **F8, move Adequate to blue: rejected.** Ink links remove the collision, and Adequate stays neutral.
- **S6, keep the contents rail at mid widths: rejected.** The links rail holds the supports and limited-by context needed while checking. One "On this page" pattern below 1280 px also means fewer variants.
- **F3, show "nothing more" for judge splits: modified.** Each verdict gets a one-line rationale and a human-resolution status (S2). A bare verdict hides what is disputed.
- **F2, per-node change log: deferred.** Ship a project changelog now and derive per-node logs from git later.
- **F5, S3, reviewer inbox: deferred** until a recurring triage task is observed.
- **S11, fully usable without JavaScript: scoped down.** Articles, links and the footer work without JavaScript. Search and graph fall back to browse-by-type and the node list.
- **F28, tests as a standalone phase: merged into phase 1.** Every phase should ship visible value.
- **S1, typed relationships: conditional on the data.** This is an owner decision (section 5).

## 3. Revised decisions

**Page structure**
- **Every node page:**
  - chain breadcrumb, with the current node unlinked
  - h1
  - byline: AI-use line linking to the footer, updated date, version
  - body
  - backlinks
  - Cite this: permalink plus version, with a copy button that announces "Copied"
  - AI-use `<details>`
- **QUE:** claims with their stance.
- **CLM:** synthesis, and evidence grouped by relation.
- **EVD:** finding with caveat, quote, crop, locator, methods, quality, caveats, report link.
- **SRC:** metadata, extracted items, DOI.
- **CVT:** what it limits.
- **EP:** table of member evidence.
- **Quality:** 5–6 domains. Statuses are Adequate, Concern, Judges split, Not reported, Not assessed and Not applicable. Expanding a row shows its checks, rationale and passage links.
- **Search:** cmdk inside Radix Dialog. Results are grouped by type, each showing the type word, ID and highlighted excerpt. An "n results" live region announces the count. The empty state links to browse-by-type.

**Color**
- **Tokens:** bg, surface, ink, ink-muted, border, focus, link, link-visited, plus a fill and border token per status.
- **Forest green** is reserved for brand and focus.
- **Status fills:** only Concern and Split are tinted.
- **Contrast:** a script checks every token pair in both themes.

**Typography**
- **Families:** serif headings, sans body, serif quotes. Mono uses the system stack for IDs and versions, which drops one webfont.
- **Small text:** 0.75 rem is used only for non-actionable metadata.

**Layout and spacing**
- **1280 px and up:** table of contents, article and rail.
- **1024–1279 px:** article and rail, with the table of contents as an "On this page" disclosure.
- **Below 1024 px:** one column, with rail content after the body and the caveat staying inline.
- **Crops** may extend to about 90 characters wide.

**Visuals**
- **Status icons,** one set with distinct shapes:
  - check (Adequate)
  - triangle (Concern)
  - split diamond (Judges split)
  - dash (Not reported)
  - dotted circle (Not assessed)
  - slash (Not applicable)

**Animation**
- **Motion:** 150 ms color and opacity transitions only.
- **Graph:** static unless dragged.

**Accessibility**
- **Zoom dialog:** + and − zoom, 0 resets, arrow keys pan, Esc closes and returns focus to the same quote.
- **Targets:** 24 px on desktop, 44 px on touch.

**Build**
- **Budgets:**
  - at most 100 KB gzipped JavaScript on node pages
  - LCP under 2.5 s on throttled 4G (Lighthouse CI)
- **Integrity checks:**
  - normalized quote match at the locator page
  - reciprocal typed links
  - complete disclosure fields
  - a redirect map for changed IDs

## 4. Revised phase plan
1. **Foundations and safety net.** Tokens, primitives, data split, Playwright, axe, snapshots, and integrity, contrast and budget scripts.
   - *Accept:* CI is green.
   - *Accept:* no node data appears in client bundles.
   - *Accept:* zero unexplained quote mismatches.
2. **Vertical slice (CLM, EVD, SRC).** Chain, quality rows, crop and zoom, footer, Cite.
   - *Accept:* a keyboard script completes claim → quote → zoom → Esc → same quote → back.
   - *Accept:* a screen-reader pass is done.
   - *Accept:* budgets are met.
   - *Accept:* no horizontal scroll at 320 px or 400% zoom, except in labelled tables.
3. **Header, menu, search.**
   - *Accept:* the combobox keyboard script passes.
   - *Accept:* the live count is announced in a screen-reader pass.
   - *Accept:* the index is fetched only when search opens.
   - *Accept:* focus returns to the opener.
4. **QUE, CVT and EP templates, graph list, settled canvas.**
   - *Accept:* a script finds a node and follows two labelled relationships without using the canvas.
   - *Accept:* nothing moves without a drag.
   - *Accept:* all 232 pages pass axe.
5. **Reviewer testing and release.** Print and forced-colors checks.
   - *Accept:* at least 4 of 5 reviewers trace a claim to its source sentence unaided within 5 minutes.
   - *Accept:* the owner signs off the accessibility and integrity criteria.

## 5. Decide with the owner
1. **Screenshot policy for non-open-access papers:** a tight crop, open-access only, or a DOI link fallback.
2. **Relationship types:** curate "supports, qualifies, contradicts" now, or ship "related, not yet classified" until curated.
3. **Ownership:** who signs off accessibility and source verification, who recruits the 3–5 reviewers, and where "Report a problem" reports go.
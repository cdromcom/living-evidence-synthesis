# Revised plan (v2)

## 1. Adopted

- **Per-type templates, with CLM as the verification hub (both).** Readers check claims, so a claim page shows its evidence for and against with inline quote excerpts. The current order only fits EVD.
- **Byline under the headline (both).** It shows model, date, "AI-generated, not human-checked" unless a person verified it, and a prompt link. A prompt link is provenance, not validation. The footer keeps the full detail.
- **Build-time quote match with a badge (Fable).** It is cheap and makes the site's core promise testable. The badge says "Quote matches source text", never "verified".
- **Decisive caveat beside the finding (both).** Authors flag one decisive caveat per CLM or EVD. The rest follow after the finding.
- **No strong/weak tally (both).** A tally implies 35 equally weighted checks. Show four domain rows instead, with distinct states for not reported, not applicable and judges disagree. Where judges split, show their reasoning.
- **List-first, graph optional (both).** The list is the primary view and drives the graph. The canvas is lazy-loaded with build-time positions, so there is no simulation motion.
- **Tests from phase 1 (both).** Acceptance checks are written before generation. A human runs NVDA and VoiceOver.
- **Library combobox, native `<details>`, popovers instead of tooltips, resize handle cut (both).** These reduce ARIA risk and keyboard cost.
- **Breakpoints (both).** Three columns from 1280, two from 1024, one below. Linked claims and caveats come before references in one column.
- **Focus on navigation and sticky offsets (both).** Move focus to the h1 after route changes. Use `scroll-padding` for sticky UI. Figure zoom is a dialog that returns focus.
- **"Living" basics (both).** Add last-updated, permalinks, a cite button, a report-error link on EVD, and a print stylesheet.
- **HTML-first delivery and lazy search index (both).** Add a transfer budget and separate thumbnails from full images.
- **Plain-language relationship links and type names (GPT).** Examples are "Supports this claim" and "Limits this finding". Search results show type and matched text.
- **Printed page versus PDF page (GPT).** Show both when they differ. Each excerpt gets an anchor on its EVD page.
- **Visual fixes (Fable).** Add type prefix and icon, framed paper screenshots, a two-tone focus ring, self-hosted fonts and a five-link top bar.
- **Small task test (GPT).** Five researchers do three tasks before release.

## 2. Rejected or deferred

- **Quote highlighted inside the screenshot: deferred.** It needs bounding-box data we may not have. For now: quote text, a "Check source" link, and the page number.
- **Per-page changelog: deferred.** Ship last-updated plus a link to the page's revision history (git).
- **Collapse nav by available width, not at 768 px: rejected.** With five links a fixed 768 px breakpoint is predictable and testable.
- **Separate citable pages per excerpt: rejected.** Anchors on the EVD page are enough.
- **Reviewer inbox: skipped.** Revisit only if reviewers show a recurring need.
- **Full usability study: deferred.** Five sessions are enough for now.
- **Averaging judge scores: rejected.** Disagreement is shown, not smoothed.

## 3. Revised decisions

**UI: visual language and components**
- Keep Refined Journal. Type scale is unchanged, but 0.75 rem is for labels only and mono IDs are 0.875 rem.
- Prose links are underlined. Status uses word, icon and colour, never colour alone.
- Focus is a two-tone ring (2 px inner, 2 px outer). Contrast is checked on cream, forest and dark surfaces.
- Node types carry a prefix and icon, and plain-language names in navigation.
- Screenshots are framed with a neutral border and never inverted in dark mode.
- Fonts are self-hosted subsets with metric-matched fallbacks.
- Top bar: Questions, Browse, Graph, About, Search.
- Hand-written primitives: Button, Chip, Callout, Field. Disclosure is native `<details>`. Radix Dialog and Popover handle overlays. Ariakit Combobox handles search.

**UX and IA: reading and checking evidence**
- The trail QUE › CLM › EVD › SRC is persistent on every node page.
- **CLM:** finding, byline, decisive caveat, evidence for and against with quote excerpts, then the other caveats.
- **EVD:** finding, quote (printed page and PDF page), "Check source" with DOI, framed thumbnail, and the quote-match badge. Next comes the domain rows (reporting, validity, rigor, openness), each with a status and one-line rationale and expandable to individual checks. Then "Supports these claims" links, methods, references, and the full provenance footer.
- **Other types (QUE, SRC, CVT, EP):** lighter templates with the same trail, byline and relationship links.
- A "Show disagreements" filter appears only where judges split.
- Narrow layouts: finding, source link and decisive caveat stay together. A compact "On this page" disclosure follows.
- Quotes, caveats and source links ship in the initial HTML. The search index loads when search opens.

**IX: keyboard, focus, motion, feedback**
- Search keeps focus in the input and arrows move the active result. Result counts and no-results states are announced. Esc closes and returns focus to the trigger.
- Sortable headers are buttons with `aria-sort`. The table of contents uses `aria-current`.
- Selecting in the list highlights the node in the graph without stealing focus or auto-panning.
- Under reduced motion there is no graph animation. Copy-citation and other feedback use a polite live region.
- No single-key shortcuts.

## 4. Revised phase plan

1. **Foundations and gates.** Tokens, self-hosted fonts, primitives, data split, and CI gates (axe, Playwright keyboard scripts, markdown snapshots, per-route JS budget). *Check:* CI fails on an axe violation or a budget breach. No route except search requests the large data file. Focus ring is at least 3:1 on all three surfaces.
2. **Header, navigation and search.** *Check:* a keyboard script runs open, type, arrow, Enter, and Esc back to the trigger. The result count is announced. A sticky header never hides an anchor target.
3. **Node templates and provenance.** CLM and EVD first, then the other types. Includes the byline, quote-match build check, domain rows, last-updated, cite button, report-error link and print stylesheet. *Check:* with JavaScript off, an EVD page has the quote, page, decisive caveat and source link. The build fails on an unmatched quote. From a CLM page the quote is visible with no clicks. Print output has no navigation.
4. **Outline-first graph.** *Check:* the canvas chunk is not requested until activated. "What else supports this claim?" can be answered from the list, keyboard only. There is no motion under reduced motion.
5. **Validation and release.** *Check:* a human NVDA and VoiceOver pass on one page of each type. Five researchers complete trace-a-claim, interpret-a-disputed-check and copy-a-citation. A cold mobile EVD visit meets the agreed transfer budget.

The owner approves each phase against its check.

## 5. Decide with the owner

1. **Provenance data.** Who sets "human-checked" and the decisive-caveat flag? The default is "AI-generated, not human-checked" and the first caveat.
2. **Quote-match failure.** Should a mismatch fail the build or publish with a visible "quote not matched" warning?
3. **Deferred scope and budget.** Do we fund screenshot highlighting (needs bounding boxes) and per-page changelogs later? What cold-mobile transfer budget (a proposal: 300 KB, excluding images) do we set?
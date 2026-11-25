# LIVES redesign: revised plan (v2, 2026-11-25)

## 1. Adopted

- **Per-type templates, with CLM as the primary page** (both critiques). Readers verify claims, so the old single page order fits only EVD.
- **Byline under the h1** (both). It shows the model, date, a verification status of "Model-generated, not human-verified" unless a person actually checked it, and the prompt link. Provenance belongs before the reader trusts the content.
- **Decisive caveat placed beside the finding** (both). Caveats change interpretation, so they cannot sit after the table.
- **Domain rows instead of a strong/weak tally** (both). Each row separates "not reported", "not applicable" and "judges split", so the summary does not imply a false verdict.
- **List-first graph** (both). The list leads, the canvas loads lazily with build-time positions, and the list drives the graph. This means less JavaScript, fewer sync bugs and no motion.
- **Gates from phase 1** (both). Axe, keyboard scripts, snapshots and per-route budgets run from the start, acceptance criteria are written before generation, and NVDA and VoiceOver are tested by a human. Model-written code needs early gates.
- **Library combobox and native `<details>`** (Fable). The combobox is the riskiest ARIA pattern, so we should not hand-write it.
- **Popovers replace tooltips for ID previews; resize handle cut** (both). Essential content must be keyboard reachable, and the handle adds cost for no reader benefit.
- **Breakpoints at 1280 and 1024, plus a narrow-layout reading order** (both). Three columns do not fit at 1024.
- **Focus specification** (both). Covers route changes, return to trigger, `aria-sort`, `aria-current`, and keeping sticky UI from covering focus.
- **Relationship-labelled links, backlinks, plain-language type names, search results showing type and matched text** (Sol). Readers arriving from search need context.
- **Printed page vs PDF page, stable excerpt anchors, cite button, report-error link, last-updated date** (both). These are cheap and core to "living" and citable evidence.
- **Slow-connection rules** (both). Content stays in the HTML, pages read without JavaScript, the search index loads on open, and images load progressively.
- **Print stylesheet in phase 3** (both). It is cheap.
- **Visual details** (both). Type prefix plus icon, framed screenshots, two-tone focus ring, self-hosted subset fonts, underlined prose links.
- **Quote-match check at build time** (Fable). Adopted as a CI report first; see deferred.

## 2. Rejected or deferred

- **Reviewer inbox**: deferred (both agree). There is no demonstrated need.
- **Public quote-match badge**: deferred until the false-mismatch rate from PDF text extraction is known. A wrong "mismatch" badge damages trust.
- **Highlighting the quote inside the screenshot**: deferred. It needs bounding-box extraction per quote, which costs too much for v1.
- **Per-page changelog**: deferred. Only a last-updated date ships now; a changelog needs a versioned data model.
- **Nav collapse based on measured fit**: rejected. It adds runtime JavaScript. Capping the top bar at five items makes a fixed breakpoint safe.
- **Two-way graph sync**: rejected in favour of one direction. Clicking the canvas selects in the list without moving focus.
- **Site-wide "show disagreements" filter**: deferred. Per-page disagreement display ships first.
- **User sessions every phase**: reduced to one round in phase 5, for budget reasons.

## 3. Revised decisions

**Visual language and components**
- **Type sizes:** 0.75 rem for labels and metadata only. Mono IDs at 0.875 rem. Body at 1 rem with 1.6 line height. Measure of 68ch.
- **Focus ring:** 2 px ink plus 2 px cream offset, verified at 3:1 or better on cream, forest and dark surfaces.
- **Type chip:** icon, plain name and ID, for example "Claim · CLM-014". Colour is never the only signal.
- **Status:** shown as word plus icon plus colour, using one of these values: Adequate, Concern, Not reported, Not applicable, Judges split (2 of 3).
- **Screenshots:** 1 px frame, never inverted. Captions and source links survive image failure.
- **Fonts:** self-hosted woff2 subsets with size-adjusted fallbacks.
- **Component sources:**
  - Hand-written: Button, Chip, Callout, Field.
  - Native: Disclosure as `<details>`.
  - Radix: Dialog and Popover.
  - Ariakit: Combobox.
  - Tooltip: only as a supplement for icons that already have labels.

**Flows and information architecture**
- **Top bar:** Questions, Browse, Graph, About, Search. A menu button appears below 768 px.
- **CLM page:**
  - Finding, then byline, then decisive caveat.
  - Evidence For and Against, each item with a two-line quote excerpt and a "Check source" link.
  - Related caveats, then references.
- **EVD page:**
  - Finding, then byline, then decisive caveat.
  - Quote, printed page (plus PDF page if different), screenshot thumbnail, "Check source" link (DOI, plus `#page=` where open access).
  - Quality domains, "Supports these claims", "Other evidence from this paper", references.
- **Other templates:** SRC is citation plus evidence list. QUE groups claims by direction. CVT and EP list what they limit or group.
- **Trail:** a breadcrumb follows the canonical path QUE › CLM › EVD › SRC. Other parents appear as "Also supports".
- **Quality block:** four domain rows. Each row expands to its individual checks. Split judgments show each judge's one-line rationale.
- **Layouts:**
  - 1280 px and wider: three columns.
  - 1024 to 1279 px: article plus rail, with "On this page" as a disclosure.
  - Narrower: finding, source and caveat stay together, then "On this page", body, relationships, references.
- **Footer:** full provenance, last updated, "Cite this page", "Report an error".
- **Search:** the index loads when search opens. Each result shows type, ID and matched text.
- **Graph page:** a filterable outline (by type and relation). A "Show graph" button loads the canvas.

**Keyboard, focus, motion, feedback**
- **Route change:** focus moves to the h1 (`tabindex=-1`), a polite live region announces the title, and Back restores scroll.
- **Search:** focus stays in the input with `aria-activedescendant`. Arrows, Home, End, Enter and Esc work. A live region announces result and no-result counts. Esc returns focus to the trigger.
- **Figure zoom:** a labelled button ("Enlarge page 7 screenshot") opens a Dialog that returns focus on close.
- **ID previews:** open after a 500 ms delay on hover or focus, are non-modal and close with Esc.
- **Tables and contents:** sortable headers are buttons with `aria-sort`. The table of contents marks the current section with `aria-current`. `scroll-padding-top` matches the header height.
- **Motion:** only 150 ms opacity fades, and none under reduced motion.
- **Feedback:** "Copied" is announced through a live region. There are no single-key shortcuts.

## 4. Revised phase plan

1. **Foundations and gates.** Tokens, fonts, primitives, data split, and CI (axe, Playwright keyboard runs, markdown snapshots, budgets, quote-match report).
   *Acceptance:* the 2 MB file is absent from the client bundle; JavaScript is 150 KB gzip or less per route; axe reports no serious issues; CI fails on a budget breach.
2. **Shell and search.** Header, menu, route focus handling, combobox.
   *Acceptance:* a Playwright script finds and opens CLM-014 by keyboard alone; focus lands on the h1; the index loads only when search opens.
3. **CLM and EVD templates.** Quality domains, byline, print stylesheet.
   *Acceptance:* both templates read fully with JavaScript disabled; a cold mobile 3G EVD load is 400 KB or less before the full image; print output contains excerpt, caveat, citation and URL; screenshots at all three breakpoints are approved.
4. **Remaining templates, cite and report, graph list, lazy canvas.**
   *Acceptance:* "What else supports CLM-014?" can be answered from the list by keyboard; the canvas code is not fetched until requested.
5. **Human validation.** NVDA and VoiceOver pass, plus 3 to 5 researcher sessions covering three tasks: trace a claim, interpret a split check, cite a page.
   *Acceptance:* at least 4 of 5 complete all tasks unaided; no blocker issues remain open.

## 5. Decide with the owner

1. **Verification policy:** who may mark a page "human-verified", and whether launch is acceptable with every page labelled model-generated.
2. **Decisive caveat and consequential checks:** whether the model selects them for each page (flagged as model-selected) or the owner curates them for CLM pages.
3. **Phase 5 testers and post-v1 scope:** who recruits the 3 to 5 researchers, and whether to fund in-screenshot quote highlighting after v1.
# LIVES redesign: improved plan (v3)

F = Fable critique, G = Sol critique. Numbers are the critics' point numbers.

## 1. Adopted

**Page structure**
- F1, G3: Each of the six types gets a template and a one-line job. A persistent QUE › CLM › EVD › SRC chain sits atop every node page. The chain is the product.
- G1: Add a "Check this claim" path with "Open source at p. 7" and "Back to claim". Quotes and assessments get stable anchors. The decisive caveat stays beside the finding in every layout and in print.
- F2: Show last-updated date, version and a "Cite this" permalink. Silent changes make pages uncitable.
- F3, G2: Show 5–6 domain rows at their worst status, auto-open Concern and Judges split, and keep "not reported / not assessed / not applicable" distinct. A split shows what the judges disagree on and whether a human resolved it. There is no confidence score.
- F4, G3: The AI-use footer is native `<details>` with no hover-open, and the byline links to it. This removes layout shift and matches the popover rule.
- F5, G3, G9: Cut the inbox, forms and resize handle. Add one "Report a problem" link per EVD.
- G3: Add browse-by-type links and plain-language type labels in search.

**Color**
- F6: Node types get a neutral glyph and mono ID prefix. This avoids 11 categories on an 8-colour palette.
- G4: Quality rows are quiet and mostly neutral. Only Concern and Judges split get colour, and each also has a distinct shape and a word.
- F7: Palette colours are fills behind ink text, never text or thin strokes. Dark mode gets separately tuned values, checked on tinted surfaces.
- F8, G4: Links are ink with an underline, and visited links are distinguished. "Adequate" is neutral, so green never reads as a verdict.
- F9: Screenshots get a 1 px border, are never inverted, and are tested in forced-colors mode.

**Typography**
- F10, G5: Quotes are set in the serif with a left rule and a "Verbatim" label. Mono is for IDs and versions only.
- G5: The locator shows the printed page and, when different, the PDF page.
- F11: 0.875 rem is the minimum for anything actionable. 0.75 rem is for decoration only.
- F12: Use subsetted variable fonts and preload the body face only. Metric-matched fallbacks (`size-adjust`) stop swap from shifting layout.

**Layout and spacing**
- F13, G6: At 1024–1279 px show article plus contents rail only, and move supporting links inline. Below 1024 px a compact "On this page" disclosure comes first. The caveat never goes in a rail.
- F14, G7: Show a cropped passage with context, let the figure break out of the measure, and offer the full page in zoom.
- F15: Set `scroll-padding-top` and test Focus Not Obscured (2.4.11).
- F16, G6: Quality rows stack on mobile. Real data tables get a labelled scroll region with a visible cue. Test at 320 px and 400% zoom.

**Visuals**
- G7: Reframe the hero. The selectable quote leads, and the crop is a verification aid beside or below it.
- F17: Fix a screenshot licensing policy before building anything around screenshots.
- F18, G7: Wrap the quote and image in `figure`/`figcaption`. Alt text says where the passage sits ("Page 7 of Smith 2024, passage highlighted") and does not repeat the quote.
- F19: Status icons differ by shape, and the quote highlight has an outline as well as a tint.
- F20: Use explicit image dimensions and lazy-load below the fold.

**Animation**
- F21: `<details>` opens instantly.
- F22, G8: The graph layout is precomputed and rendered settled. Physics runs only on drag, selection never re-settles it, and a pause control exists if motion exceeds 5 s.
- G8: The focus ring is not animated, search results are not delayed, and the full-page viewer shows a loading state.
- F23, G9: Focus the h1 with `tabindex="-1"` after navigation, and make sure Back restores scroll.

**Accessibility**
- F24: The combobox comes from a library, with a live result count. Drop Radix Tooltip.
- G9: Specify focus as a sequence. Fragment links focus their target, closing search or zoom returns focus to the opener, and closing zoom returns to the same quote.
- F25, F26, G10: Run screen-reader passes after the node page and after search. Run 3 sessions of "verify this claim against its source". Test equivalent tasks, not gestures.
- F27: Inline targets are at least 24 px on desktop. Sortable headers are real buttons with `aria-sort`. Print expands all disclosures and shows URLs.

**Build**
- F28, G11: Tests come first, then one vertical slice, and only then the rollout.
- F29, G11: Node pages are server components, usable without JS. The search index loads when the palette opens, and graph data loads with the canvas.
- F30: Set a CI performance budget.
- F31, G12: Add content-integrity checks in CI from phase 1.
- F32, G12: Every phase has acceptance criteria and a named human approver for accessibility and source verification.

## 2. Rejected or deferred

- **G4, page-type colours (rejected):** glyph plus prefix is cheaper and avoids contrast failures. Revisit with a single tint only if testing shows readers can't scan types.
- **F13, right rail kept (rejected):** G's contents rail is lighter, and supporting links read better inline.
- **F2, full per-node change log (deferred):** it needs an editorial process. Ship date, version and a link to git history first.
- **G1, "contradicting" label (deferred):** only if relationship types already exist in the data. Don't invent classifications.
- **G2, supporting passages inside each check (deferred):** the data may not exist. Ship checks and rationale only.
- **G3, search excerpts (deferred):** they grow the index. Decide after measuring its size.
- **F20, AVIF specifically (deferred):** generate WebP or AVIF at build time. Avoid per-request optimisation costs.
- **F24, React Aria as the first choice (deferred):** start with cmdk, which pairs with the Radix Dialog already chosen. Switch only if it fails the phase 4 screen-reader pass.
- **F30, the 100 KB figure (provisional):** take baselines first, then fix the budget.

## 3. Revised decisions

**UI (visual language and components)**
- Type scale is 0.875, 1, 1.125, 1.5, 1.875 and 2.5 rem, with 0.75 rem only for non-actionable decoration.
- Borders rather than shadows, 6 px radius, 4 px grid.
- Primitives are Field, Button, Chip, Callout, Disclosure (native `<details>`), Quote, StatusRow and Locator.
- Status set is Adequate (neutral), Concern, Not reported, Not assessed, Not applicable and Judges split. Concern and Judges split alone carry colour, each with a distinct shape and a word.
- Dark mode is a tuned token set with a remembered toggle.

**UX (flows and information architecture)**
- Each node page opens with the chain, then a status block (updated, version, cite, report). The finding and its caveat come next, then quote and crop, quality rows, methods, references and the AI-use footer.
- Verification loop: claim → evidence (anchor) → source page → back to the same claim position.
- Relationship labels are shown only where typed data exists.
- Citation block gives a permalink and the version. Changed URLs get redirects.
- Search results show type label, title and ID. Browse-by-type pages are linked from the header.
- The graph is secondary: list first, canvas on demand, with relationships labelled in the list.

**IX (keyboard, focus, motion, feedback)**
- One focus style (2 px ring, 3:1) with sticky UI clearance.
- Focus sequences are as specified in section 1.
- Search is a combobox (arrows, Enter, Esc) with a live count and a no-results message.
- Motion is limited to 150 ms hover and colour transitions. Disclosures are instant.
- Graph is static unless dragged, and has a pause control.
- Feedback: loading states for zoom and graph, and a visible "copied" confirmation on cite.

## 4. Revised phase plan

1. **Safety net and foundation.**
   - Build Playwright keyboard scripts, axe and visual snapshots on the current site.
   - Add integrity checks: quotes match source text and page, typed and reciprocal relationships, disclosure fields, redirects.
   - Add tokens and primitives, the data split with server components, and baseline budgets.
   - *Acceptance:* a deliberately corrupted quote fails CI. The 2 MB file never appears in the network panel. Token pairs pass contrast tests.
2. **Vertical slice.** One QUE → CLM → EVD → SRC path with the chain, node layout, quality rows, AI-use details, quote/crop figure and cite block.
   - *Acceptance:*
     - A keyboard-only run goes from claim to source page and back to the same position.
     - No horizontal scroll at 320 px and 400% zoom.
     - Article and links work with JS off.
     - Screen-reader pass 1 is clean.
     - 3 reviewer sessions on a phone and throttled network are recorded, with at least 2 completing the task unaided.
3. **Rollout and header.** Templates for all six types, header, menu, skip link, print, and fonts with fallbacks.
   - *Acceptance:*
     - All ~232 pages build and a link check passes.
     - Axe shows no serious issues.
     - Sticky header never obscures focus.
     - Print shows the caveat, expanded disclosures and URLs.
4. **Search and graph list.** A cmdk combobox with a lazy index, and the graph list with relationships and on-demand canvas.
   - *Acceptance:*
     - Scripts cover arrows, Enter, Esc and focus return.
     - Result count is announced in screen-reader pass 2.
     - A node can be found, inspected and followed without the canvas.
     - Neither index nor graph data ships on first load.
5. **Hardening and release.** Forced-colors, performance budget enforced, final screen-reader pass and the owner's source-verification sign-off.
   - *Acceptance:* LCP is under 2.5 s on throttled 4G and JS stays within the agreed budget. CI is green, and the named human approver signs off.

## 5. Decide with the owner

1. **Screenshot policy:** open-access only, tight crop, or DOI-link fallback for the rest. This gates the Visuals design.
2. **Quality domains and relationship data:** which 5–6 domains to show, and whether "supports / qualifies / contradicts" exists in the data or needs human classification.
3. **Versioning and sign-off:** what "version" and a stable citation mean, and who is the named human approver and reviewer recruiter for each phase.
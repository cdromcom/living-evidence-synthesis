1. **Design the verification path, not "a node page".** The listed order only fits EVD, so specify a template per type. The CLM page is the real product: show evidence for and against with quote excerpts inline, so checking doesn't cost three clicks. On EVD, highlight the quote in the screenshot, deep-link to the DOI and printed page, and keep a persistent QUE › CLM › EVD › SRC trail.

2. **Move provenance and caveats up.** On an AI-written evidence site, the footer is the wrong place for authorship. Put a byline under the headline: model, date, human-checked or not, prompt link. Add a build-time check that every quote matches the source text, and show the result as a badge. Caveats go directly under the finding, not after the table.

3. **Don't tally strong and weak signals.** A count implies 35 equally weighted checks and hides "not reported" and "not applicable". Default to four domain rows (reporting, validity, rigor, openness), each with a status word and icon, expandable to individual checks. Show judge disagreement only where judges split ("2 of 3"), with a "show disagreements" filter.

4. **Demote the graph.** About 232 mostly hierarchical nodes are better served by a filterable outline. Make the list the primary view and the canvas an optional, lazy-loaded enhancement. Precompute node positions at build time for a stable layout, no simulation motion and less JavaScript. Two-way sync is where the bugs will live, so let the list drive the graph.

5. **Tests belong in phase 1, not 5.** Axe, keyboard scripts, markdown snapshots and a per-route JavaScript budget should gate every phase, especially with model-written code. Write acceptance criteria before each phase is generated. The screen-reader pass must be a human using NVDA and VoiceOver.

6. **Don't hand-write the combobox.** It is the hardest ARIA pattern; use cmdk, Ariakit or React Aria. Use native `<details>` for Disclosure. Tooltips must never hold essential content, so ID previews should be popovers that open on focus and click. Cut the resize handle: it adds keyboard cost for no reader benefit.

7. **Fix the breakpoints.** Three columns with a 70-character article do not fit at 1024 px. Use three from 1280 and two (article plus rail) from 1024, with the table of contents collapsed into a disclosure. In one column, place the rail's linked claims and caveats before references, because they are navigation.

8. **Specify focus on navigation.** After client-side route changes, move focus to the h1, announce the title, and restore scroll on Back. Figure zoom is a dialog that returns focus to its trigger. Sortable headers are buttons with `aria-sort`. The table of contents marks the current section with `aria-current`.

9. **"Living" needs versioning.** Missing: a last-updated date and changelog per page, stable permalinks, a "cite this page" copy button, and a report-an-error link on every EVD. Skip the inbox. Ship a print stylesheet in phase 3; it is cheap. For slow connections, pages must read fully without JavaScript, and the search index should load only when search opens.

10. **Tighten the visual details.**
    - Node types need a prefix and icon, not colour alone.
    - Paper screenshots glare in dark mode: frame them, don't invert them.
    - Reserve 0.75 rem for labels and set mono IDs at 0.875.
    - Use a two-tone focus ring so 3:1 holds on cream, forest and dark.
    - Self-host subset fonts with metric-matched fallbacks.
    - Cap the top bar at Questions, Browse, Graph, About, Search.
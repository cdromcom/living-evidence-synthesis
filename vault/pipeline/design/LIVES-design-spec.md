---
title: LIVES design and development spec
type: design-spec
status: draft for owner approval
---
# LIVES design and development spec

## 1. Purpose and readers

This file is the single reference for models building the LIVES web app. It merges the two-page summary (`pipeline/prompts/design-consult-v2.md`), two critiques, two improved plans, the earlier Direction A decisions, and the owner's later instructions. Where sources conflict, owner instructions win, then the Opus 5.5 plan, then the Sonnet 5.5 plan. Anything the sources do not settle is marked **not decided**. Do not invent a decision to fill the gap. Ask the owner.

**Site readers:** researchers and reviewers who want to check a claim down to the source sentence. Fast checking is the product.

**Terms.**
- **Node:** one page. The six node types are QUE (Question), CLM (Claim), EVD (Evidence), SRC (Source paper), CVT (Caveat) and EP (Pattern across papers).
- **Quality signals:** about 35 checks per evidence page (reporting, validity, rigor, openness).
- **GAMER:** a checklist for reporting generative AI use in medical research.
- **Okabe-Ito:** a colorblind-safe palette of eight colors.

## 2. Decisions at a glance

| # | Area | Decision | Decided by |
|---|---|---|---|
| 1 | Direction | Direction A, "Refined Journal": evolve the current site in place, calm, not flashy | Owner (2026-11-24) |
| 2 | Node page | Verification path first; decisive caveat beside the finding in every layout and in print | Both plans, owner brief |
| 3 | Quality signals | Domain rows with five statuses; no strong/weak tally | Owner brief, Opus plan |
| 4 | Color | Cream, forest, ink; Okabe-Ito for statuses; never color alone; tuned dark mode | Owner brief, Opus plan |
| 5 | Screenshots | Closed by default, a small labelled placeholder opens on click | Owner |
| 6 | Highlights and logo | Pastel PDF highlights by node type; the logo stays the plain green turtle icon (a cherub-on-tortoise mascot was tried on 2026-11-25 and the owner rejected it) | Owner |
| 7 | Provenance | Byline under the title plus a collapsed GAMER-style AI-use footer | Owner, v2 summary |
| 8 | Restraint | Pills are not capped, but they are not the default: try other components first (see section 12); one accent; no decoration beyond the plain turtle logo | Owner (2026-11-25) |
| 9 | Keyboard | Every task works without a mouse; tested in CI | Owner (Direction A) |
| 10 | Build | Tests first; Opus 5.5 builds; another model family reviews; the owner approves each phase | Owner, Opus plan |

## 3. Page structure

### 3.1 Every node page, top to bottom (Opus plan)

1. Chain breadcrumb: QUE > CLM > EVD > SRC, current node unlinked.
2. Title (h1).
3. Byline: the AI-use line (links to the footer), updated date, version.
4. Body (varies by node type, see 3.2).
5. Backlinks ("supports" and "limited by").
6. Cite this: permalink plus version, with a copy button that announces "Copied".
7. AI-use footer (section 10).

### 3.2 The six node types

| Type | Job | Body |
|---|---|---|
| QUE | Ask the question | Claims answering it, each with its stance |
| CLM | Explain the synthesis | Synthesis, then evidence grouped by relation |
| EVD | Let a reader verify | Finding with caveat, quote, locator, methods, quality rows, caveats, "Report a problem" link |
| SRC | Index the paper | Metadata, extracted items, DOI |
| CVT | Say what is limited | What it limits, and the evidence it limits |
| EP | Group across papers | Table of member evidence |

### 3.3 Verification path first

- Lead with the selectable quote and its locator. The screenshot is the check, not the hero (section 7).
- Give a short path: "Check this claim", "Open source at p. 7", "Back to claim".
- Give quotes and assessments stable anchors so a reader can share the exact spot.
- Show the printed page and, when different, the PDF page.

| Do | Don't |
|---|---|
| Put the decisive caveat beside the finding | Move the caveat into a rail, a tab or a collapsed section |
| Keep the caveat visible in print | Hide it behind a click in any layout |
| Label relations only where typed data exists | Invent "contradicts" labels the data does not hold |

### 3.4 Quality signals as domain rows

- Show 5 or 6 domain rows. Each row shows its worst status.
- Rows containing Concern or Judges split open automatically. Others stay collapsed.
- Expanding a row shows its individual checks and the rationale.
- When judges split, show each verdict with a one-line rationale and whether a human resolved it (Opus plan).
- Do not show a strong/weak tally or a confidence score.

| Status | Meaning | Treatment |
|---|---|---|
| Adequate | Check met | Neutral |
| Concern | Check raises a problem | Colored, own shape, word |
| Judges split | AI judges disagree | Colored, own shape, word |
| Not reported | Paper does not say | Neutral, dash |
| Not applicable | Check does not apply | Neutral, slash |

**Conflict:** the Opus plan adds a sixth status, **Not assessed** (the check was not run). The owner listed five. Decision: ship the five, and ask the owner about Not assessed (section 14).

## 4. Color

- **Palette:** cream background, forest green, ink text (v2 summary, Direction A).
- **Statuses:** Okabe-Ito hues, used only as fills behind ink text. Several Okabe-Ito colors fail 3:1 on cream, so never use them as text or thin strokes.
- **Never color alone:** every status also has a distinct icon shape and a word.
- **Opus plan narrowing:** only Concern and Judges split are tinted. Other rows stay quiet so emphasis keeps its meaning. The owner said Okabe-Ito for statuses without saying how many are tinted. This narrowing stands until the owner says otherwise.
- **Node types:** the Opus and Sonnet plans give them a neutral glyph plus a mono ID prefix, because six types plus five statuses exceed eight colors. The owner's pastel PDF highlights (section 7) are the one place node type gets color.
- **Links:** ink, underlined, with a distinct visited style. Forest green is reserved for brand and focus, so green never reads as a verdict.
- **Dark mode:** a separately tuned token set (not inverted hues), with a toggle that follows the system setting and is remembered. Check on tinted surfaces.
- **Contrast:** 4.5:1 for text, 3:1 for UI. A script checks every token pair in both themes.
- **Tokens:** bg, surface, ink, ink-muted, border, focus, link, link-visited, plus a fill and a border token per status. Define as CSS variables on `:root` with a dark override.
- **Screenshots:** 1 px border, never inverted, tested in forced-colors mode.

| Do | Don't |
|---|---|
| Pair every color with a shape and a word | Rely on hue to carry meaning |
| Tune dark values by hand | Invert the light palette |

## 5. Typography

- **Families:** serif headings, sans body, serif for quotes. Mono only for IDs and versions, using the system stack, which saves one webfont (Opus plan).
- **Quotes:** serif, left rule, small "Verbatim" label. Mono hurts long reading.
- **Scale (rem):** 0.875, 1, 1.125, 1.5, 1.875, 2.5. Use 0.75 only for non-actionable metadata.
- **Minimum size:** anything a reader acts on (locators, status words, links) is at least 0.875 rem.
- **Line height:** 1.6 body and 1.25 headings (v2 summary). Direction A said 1.5. **Not decided**; use 1.6 unless the owner objects.
- **Measure:** about 70 characters.
- **Fonts:** self-hosted, subsetted variable fonts, two weights per family, `font-display: swap`, body face preloaded, and metric-matched fallbacks (`size-adjust`) so swapping does not shift layout.
- **Numbers:** tabular figures in tables and metrics.

| Do | Don't |
|---|---|
| Show the printed page beside every quote | Make readers open the image to find the page |
| Mark verbatim text separately from editorial text | Set quotes in mono |

## 6. Layout and spacing

- **Grid:** 4 px; spacing steps 4, 8, 12, 16, 24, 32, 48, 64. Radius 6 px. Borders, not shadows. Medium density.
- **Breakpoints (resolved by the Opus plan):**

| Width | Layout |
|---|---|
| 1280 px and up | Table of contents, article, rail (links and review) |
| 1024 to 1279 px | Article and rail; table of contents becomes an "On this page" disclosure |
| Below 1024 px | One column; rail content after the body; caveat stays inline |
| Below 768 px | Top-bar links collapse into a labelled menu button |

- **Conflict:** the Sonnet plan kept the contents rail at mid widths and moved links inline. The Opus plan won, because the links rail holds the "supports" and "limited by" context needed during checking.
- **Figures:** a cropped passage may be up to about 90 characters wide and may break out of the article measure.
- **Tables:** quality rows stack on mobile. Real data tables scroll in a labelled region with a visible focus ring and a cue that more columns exist.
- **Sticky UI:** set `scroll-padding-top`. A sticky header or contents must never cover a focused item (WCAG 2.4.11).
- **Targets:** 24 px minimum on desktop, 44 px on touch.
- **Checks:** no horizontal scroll at 320 px or 400% zoom, except inside labelled tables.

## 7. Visuals

### 7.1 Screenshots (owner decision)

- **Closed by default.** Show a small labelled placeholder, for example "Source page 7 (screenshot)". The reader clicks it, or presses Enter, to open it.
- The selectable quote and its source link stay visible above it.
- Bind quote and image in `figure` and `figcaption`. Alt text says where the passage is ("Page 7 of Smith 2024, passage highlighted"). It must not repeat the quote.
- Open view: a cropped passage with context, and a full-page zoom on request, with a loading state.
- Zoom dialog keys: + and - zoom, 0 resets, arrows pan, Esc closes and returns focus to the same quote.
- Explicit image dimensions, lazy loading, WebP or AVIF made at build time.
- **Licensing:** not decided (section 14). Fallback is a DOI link where a screenshot cannot be shown.
- **Conflict:** the v2 summary made the screenshot the page hero. The owner's closed-by-default rule replaces that.

### 7.2 PDF highlights (owner decision)

Light pastels by node type. The highlight also gets an outline, because a tint alone fails for some readers.

| Type | Highlight |
|---|---|
| QUE | Light orange |
| EVD | Light red |
| CLM | Mint green |
| EP | Light blue |
| CVT | Soft gray |
| SRC | Not decided |

Exact hex values are **not decided**. Choose values that keep ink text readable at 4.5:1 and record them as tokens.

### 7.3 Logo (owner decision, 2026-11-25)

- The logo is the plain green turtle icon (lucide `Turtle`) beside the site name. A small cherub with a halo riding the tortoise was built and shipped on 2026-11-25 and the owner reverted it as unattractive. Do not reintroduce a mascot without the owner's request. The icon is decorative (hidden from screen readers; the site name next to it is the link text). Per project memory, models draw diagrams weakly, so the owner supplies or approves any art.


### 7.4 Icons and graph

- One icon set. Status icons differ by shape: check (Adequate), triangle (Concern), split diamond (Judges split), dash (Not reported), slash (Not applicable).
- The graph is secondary: list first, canvas loaded on demand, relationships labelled in the list.

## 8. Animation

- Only 150 ms color and opacity transitions.
- Disclosures open instantly. Do not animate `<details>` height.
- Do not animate the focus ring or delay search results.
- Graph layout is precomputed and drawn settled. Physics runs only while dragging. Selecting a node never re-settles it. A pause control appears if anything moves for more than 5 seconds.
- No scroll-jacking or parallax. Honor `prefers-reduced-motion`.

## 9. Accessibility and keyboard

**Target:** WCAG 2.2 AA. **Rule (owner):** everything works without a mouse.

| Area | Must work |
|---|---|
| Whole site | Skip link first; landmarks; one focus style (2 px ring, 3:1); no traps; no single-key shortcuts at first |
| Header | Menu button (Enter or Space opens, Esc closes, focus returns); theme toggle |
| Search | Combobox: arrows, Enter, Esc, live "n results" count, focus returns to opener |
| Node page | "On this page" links move focus to the target; disclosures open with Enter or Space |
| Zoom and tooltips | Open and close by keyboard; focus returns |
| Tables | Sortable headers are real buttons with `aria-sort`; scrollable regions are focusable |
| Graph | Find a node, read its labelled relationships and follow them from the list alone |
| Review sidebar | Every tick box, tooltip and verdict reachable and announced |

- **Focus sequence:** after navigation focus the h1 (`tabindex="-1"`). A fragment link focuses its target. Back restores the reading position.
- **Search build:** cmdk inside a Radix Dialog. Switch to React Aria only if it fails the screen-reader pass (Sonnet plan; the Opus plan did not name a fallback).
- **Print:** expand all disclosures, show URLs, keep the caveat.
- **Tests:** Playwright keyboard scripts, axe in CI, screen-reader passes after the node page and after search.

## 10. Provenance

- **Byline** under the title: the one-line form `AI use: <models> · <date> · <human-check status>`, plus updated date and version. It links to the footer.
- **Footer**, last on every page, built from the GAMER checklist:
  - **Closed:** one line, the same text as the byline.
  - **Opened:** a skimmable table. Columns: step, model and version, accessed (UTC), effort, time, prompt (permalink and hash), response. A line below gives role, sections and checked-by.
  - **Opening:** by click, hover or keyboard (owner decision).
- **Link** to `pipeline/provenance/AI-disclosure.md`. It answers the nine GAMER items once for the project and covers privacy and influence on interpretation.

**Conflict:** both models and the earlier summary advised against open-on-hover, because an expanding table shifts layout and contradicts the popover rule. The owner chose click, hover or keyboard. Build native `<details>` (click and keyboard work with no script). How hover opens it without layout shift is **not decided**. Test it and report back.

## 11. Review sidebar

Sources say little here. The owner brief governs.

- Several categories can be ticked at once. Each ticked category has its own verdict.
- Tooltips explain each verdict label. They open on hover, focus and tap.
- The privacy paragraph sits behind a "?" tooltip.
- If the reviews view is missing, show the reviewer's own verdicts, not a red error.
- **Not decided:** the category list, the verdict labels, wording of the tooltips, and where the sidebar sits (the rail is assumed).
- The reviewer inbox is deferred until a recurring triage task appears (Opus and Sonnet plans). Add one "Report a problem" link per EVD.
- Radix Tooltip is hover-first, so the critique advised popovers. Tooltips here must work from the keyboard. Which component to use is **not decided**.

## 12. Restraint rules

Owner feedback: the homepage uses too many colorful pills. Owner decision (2026-11-25): there is no numeric cap on pills; instead, models must explore a variety of other UI components that also work, and use a pill only when it is the best fit.

| Do | Don't |
|---|---|
| Use plain text for metadata | Wrap every label in a pill |
| Try a component other than a pill first: plain text, a small table, a definition list, a labelled icon, a segmented control, a tab, a disclosure, a sortable column, a tooltip, a count in the heading | Default to a pill for every label or count |
| Use one accent (forest) | Add a color per category |
| Let Concern and Judges split be the only colored statuses | Tint Adequate and Not reported |
| Keep the plain turtle logo as the only illustration | Add decorative art or icons without a job |

- **Components to consider instead of pills:** inline text with a separator; a two-column table of label and value; a definition list; a leading icon with a text label; a segmented control for a choice of one; tabs for parallel views; `<details>` for optional detail; a tooltip for a definition; a count in a heading ("Evidence (12)"); a sorted list with a status icon at the start of each row; a sparkline or small bar where a number has a scale.
- **When a pill is the right choice:** a short, filterable attribute the reader will click (for example a type filter), where the control itself is the point. When using pills, keep them neutral and use color only for a status that needs attention.
- **Review step:** the person building a page lists the components considered for each group of labels and why the chosen one fits; the reviewer checks that the page does not read as a wall of chips.

## 13. Build plan and acceptance checks

**Who builds.** Claude Opus 5.5 at high effort builds. Sonnet 5.5 writes tests, CI and docs. A model from another family (GPT-6.2 Sol) reviews. The owner approves each phase. Budget about $50 to $100 of model cost. The scarce resource is owner review time, so every phase has written acceptance checks.

**Stack (kept).** Next.js App Router, Tailwind v4, Vercel, `react-force-graph-2d`. Hand-written primitives: Field, Button, Chip, Callout, Disclosure, Quote, StatusRow, Locator. Radix only for Dialog and Popover.

**Budgets.**
- Opus plan: at most 100 KB gzipped JavaScript on node pages; LCP under 2.5 s on throttled 4G (Lighthouse CI).
- Sonnet plan: take baselines first, then fix the JavaScript figure. **Decision:** use 100 KB as the provisional target.
- Node data stays server-side. Load the search index when search opens, and graph data with the canvas.

**Phases (Opus plan).**

| Phase | Work | Accept when | Approver |
|---|---|---|---|
| 1 Foundations | Tokens, primitives, data split, Playwright, axe, snapshots, integrity, contrast and budget scripts | CI green; no node data in client bundles; zero unexplained quote mismatches | Owner |
| 2 Vertical slice | CLM, EVD, SRC with chain, quality rows, crop and zoom, footer, Cite | Keyboard script: claim to quote to zoom to Esc to same quote to back; screen-reader pass; budgets met; no horizontal scroll at 320 px or 400% | Owner for accessibility and source verification |
| 3 Header and search | Header, menu, search | Combobox script passes; count announced; index fetched only on open; focus returns | Owner |
| 4 Other types and graph | QUE, CVT, EP; graph list; settled canvas | Script finds a node and follows two relationships without the canvas; nothing moves without a drag; all 232 pages pass axe | Owner |
| 5 Test and release | Reviewer sessions, print, forced colors | At least 4 of 5 reviewers trace a claim to its source sentence within 5 minutes; owner signs off | Owner |

**Integrity checks (from phase 1).** A quote matches the extracted source text at its locator. Typed links are reciprocal. Disclosure fields are complete. A redirect map covers changed IDs.

**Conflict.** Sonnet ran 3 reviewer sessions in phase 2. Use the Opus plan.


## 14. Open owner decisions

| # | Question | Source |
|---|---|---|
| 1 | Screenshot policy for papers that are not open access: tight crop, open-access only, or a DOI link | Both plans |
| 2 | Relationship types: curate supports / qualifies / contradicts now, or ship "related" until curated | Opus plan; Sonnet deferred |
| 3 | Who approves accessibility and source verification, who recruits reviewers, and where "Report a problem" goes | Both plans |
| 4 | Which 5 or 6 quality domains to show | Sonnet plan; v2 open question |
| 5 | What "version" and a stable citation mean | Sonnet plan |
| 6 | Add "Not assessed" as a sixth status? | Opus plan |
| 7 | How the footer opens on hover without layout shift | Models' critique vs owner |
| 8 | Highlight hex values | Owner brief |
| 9 | Review sidebar categories and verdict labels | Owner brief |
| 10 | Per-node change log (deferred; project changelog first) | Both plans |
| 11 | Search excerpts: adopted by Opus, deferred by Sonnet pending index size | Plans differ |
| 12 | Print and citation styles; slow-connection reader support | v2 open questions |
| 13 | Body line height, 1.5 or 1.6 | v2 vs Direction A |

## 15. Where each decision came from

Short names: **Fable** = `design-consult-claude-fable-5-2.md`; **Sol** = `design-consult-gpt-6.2-sol.md`; **Opus** = `design-improve-claude-opus-5-5.md`; **Sonnet** = `design-improve-claude-sonnet-5-5.md`; **A** = `docs/redesign/decisions.md`; **v2** = `pipeline/prompts/design-consult-v2.md`. All run files are in `pipeline/runs/2026-11-25-design-consult-v2/`.

| Decision | Origin |
|---|---|
| Direction A, keyboard rule, Radix scope, build model, review by another family | A (owner approved) |
| Six node templates and chain | Fable 1, Sol 3; adopted by Opus and Sonnet |
| Domain rows, auto-open, no tally | Fable 3, Sol 2; five-status list from v2 and the owner brief |
| Native `<details>` footer, byline links to it | Fable 4, Sol 3 (hover-open overridden by owner) |
| Node types neutral, colors as fills behind ink | Fable 6 and 7; Opus and Sonnet adopt (Sol 4 rejected) |
| Ink underlined links | Fable 8, Sol 4 |
| Serif quotes, fonts, 0.875 rem minimum | Fable 10 to 12, Sol 5 |
| Breakpoints | Fable 13, Sol 6; resolved by Opus |
| Crop with context, full page on demand | Fable 14, Sol 7 |
| Screenshot closed by default, pastel highlights, plain turtle logo, restraint rules | Owner |
| Settled graph, no `<details>` animation | Fable 21 and 22, Sol 8 |
| Combobox from a library | Fable 24; cmdk named by Opus and Sonnet |
| Focus sequence | Fable 23, Sol 9 |
| Tests first, vertical slice, budgets, integrity checks, named approver | Fable 28 to 32, Sol 11 and 12; phases from Opus |
| Review sidebar behavior | Owner |
| Provenance wording and GAMER items | `pipeline/provenance/AI-disclosure.md` |


## Addendum 2026-11-25: report route
The large "Report on GitHub" box in the node sidebar was replaced by one small link, "Report a problem or request removal on GitHub", which opens a prefilled new issue. The repository's GitHub issues page is the takedown route (owner, 2026-11-24); the link keeps that route visible to signed-out visitors without a second form next to the Review panel.

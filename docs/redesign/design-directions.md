# LIVES redesign: best practices, three directions, recommendation, decisions

Companion to `inventory.md` (facts about the current app). No app code is changed by this document.

---

## 1. Checklist for the redesign

### 1a. UI dos and don'ts (partly reconstructed)

The source article, "Do's and Don't for UI Design" (Design Bootcamp, Medium), **could not be fetched**: Medium returned HTTP 403 to the fetch tool, and the `bootcamp.uxdesign.cc` mirror only redirects back to Medium. A web search confirmed the article exists, describes itself as a "Top 7 do's and don't" list, and has a Part 2 about colour, single-column layout and consistency, but returned none of the seven items. **The list below is therefore reconstructed** from those hints and from standard UI guidance of the same kind (including the UX Design Institute dos and don'ts the search surfaced). Treat it as the usual consensus, not as a quote of the article.

| Do | Don't |
|---|---|
| Keep one visual hierarchy: one H1 per page, clear size and weight steps, whitespace to group | Mix many type sizes (the current app has about 66 arbitrary 9 to 13 px sizes) |
| Be consistent: same component looks and behaves the same everywhere | Reinvent standard patterns (menus, tabs, accordions, form fields) |
| Use colour with purpose and enough contrast; pair colour with text or shape | Rely on colour alone, or on low-contrast grey for body text |
| Design for all screen sizes, mobile first, single column where content is long | Hide primary navigation on small screens without a replacement |
| Give feedback for every action (loading, saved, error) and show system status | Leave users guessing after a click or a submit |
| Use readable type: 16 px body, 1.5 line height, 45 to 75 characters per line | Use long lines, tiny captions, or all-caps paragraphs |
| Make targets big enough and spaced; clear primary vs secondary actions | Put several equal-weight buttons side by side |
| Use familiar icons with labels where meaning is not obvious | Use icon-only controls with no accessible name |
| Test with real content and real users | Fill designs with perfect lorem ipsum |

### 1b. WCAG 2.2 AA essentials

| Criterion | What the rebuild must do | Current state |
|---|---|---|
| 1.4.3 Contrast (text) | 4.5:1 body, 3:1 for 24 px or 19 px bold | body passes; verdict circles (white on `#10b981`, `#f59e0b`, `#fbbf24`) fail |
| 1.4.11 Non-text contrast | 3:1 for input borders, focus rings, meaningful graphics | card and input borders are 1.2:1 (light) and 1.4:1 (dark) |
| 2.4.7 and 2.4.11 Focus visible and not obscured | A visible focus ring on every interactive element, not hidden by sticky headers | no global `:focus-visible`; inputs use a 1 px ring |
| 2.4.13 Focus appearance (AAA, but a good target) | 2 px ring, 3:1 against adjacent colours | not met |
| 2.5.8 Target size (minimum) | at least 24 by 24 CSS px (aim for 44 on touch) | 32 px icon buttons ok; small chips borderline |
| 2.1.1 Keyboard | Everything operable without a mouse: tooltips, graph, mermaid fullscreen, resize handle | tooltip, graph canvas and diagram click are unverified |
| 2.4.1 Bypass blocks | Skip link to main content | missing |
| 1.4.10 Reflow | No horizontal scroll at 320 px wide (tables may scroll inside their own region) | header nav disappears; tables scroll in place |
| 1.4.12 Text spacing | Layout survives line-height 1.5, paragraph spacing 2x, letter 0.12em, word 0.16em | use rem and no fixed heights; not tested |
| 3.3.1 and 3.3.3 Error identification and suggestion | Error text next to the field, announced (`aria-live` or `role="alert"`), says how to fix | status text exists, not announced |
| 3.2.3 and 3.2.4 Consistent navigation and identification | Same nav order and the same labels on every page | consistent on desktop |
| 3.3.7 Redundant entry, 3.3.8 Accessible authentication | Do not make users retype; the email-code flow must allow paste (no cognitive test) | verify paste works on the 8-digit field |
| 2.3.3 / 2.2.2 Motion | Respect `prefers-reduced-motion` for the graph settle, accordions, fullscreen | no rule today |
| 1.1.1 Non-text content | Alt for figures (exists), text alternative for the graph and the mermaid diagrams | partly |
| 1.3.1 and 4.1.2 | Real headings, lists, table headers, landmarks, names and roles on custom widgets | mostly semantic; header `nav` lacks a label |

---

## 2. Three directions

All three keep: the Cream + Forest identity, the serif-heading plus sans body plus mono-ID type trio, node-type colours, shape-based status icons, every feature in `inventory.md` section 5, static prerender, Vercel, Node 22.

Shared fixes in every direction (not optional): skip link, a mobile menu, `:focus-visible` ring, `prefers-reduced-motion`, 12 px minimum text, `next/font` for the three families, slim list payloads for `/nodes`, `/graph` and search (titles, ids, tags, status, degree only; bodies stay on node pages), content-hashed or `immutable` cache headers for figures, WebP versions of figures, `width` and `height` on images, a single token file, CI (lint, type-check, build, `check:sanitize`).

### Direction A: "Refined Journal" (evolve in place)

**Concept.** Keep today's look and layout but tighten it: the same cream pages, forest links and cards, with a stricter type scale, fewer one-off sizes, one focus style and a mobile menu. It is the lowest-risk path that still removes the performance and accessibility debts.

**Visual language**
- Palette: unchanged tokens; darken `muted-ink` slightly in light mode (`#5c5750`, about 6.6:1), add `--border-strong: #b9b2a1` (about 2.2:1 on paper; use `#8f8878` for inputs, about 3.4:1) for input borders only; dark border stays soft for cards.
- Type scale (rem): 0.75 caption, 0.875 small, 1 body, 1.125 lead, 1.5 h2, 1.875 h1, 2.5 hero. Nothing below 0.75.
- Spacing: 4 px grid, section gaps 48 and 24.
- Radius: 6 px everywhere, pills only for badges.
- Elevation: none; borders only, one shadow for popovers.
- Data tables: today's boxed tables with sticky header and zebra off; row hover wash.
- Callouts: today's left-accent callouts with the 10 percent tint; accents re-checked for 4.5:1.
- Graph: same canvas force graph; node colours with a 1.5 px outline so they separate on both themes; labels at 12 px.
- Dark mode: **yes**, kept (already present), deduplicate the token block.

**Layout and navigation.** Header with logo, 9 links collapsing into a menu button below 768 px, search, GitHub, account, theme. Node page keeps three columns (TOC, article, aside) at 1024 px and up; below that the TOC becomes a collapsed "On this page" details at the top and the review and edges panel moves under the article. Review and contribute stay where they are: ReviewWidget at the top of the right aside; Contribute is a top-level page.

**Density.** Medium, as now (single column article at about 70 characters, dense chips).

**Accessibility notes.** Cheapest path to AA. Biggest gains: mobile nav, focus ring, verdict colours (use darker fills or dark text on light fills), tooltips available on focus and tap.

**Code architecture.** Plain Tailwind v4 tokens in one `tokens.css`; extract `Field`, `Button`, `Chip`, `Callout`, `Disclosure` primitives (about 8 files, hand-written); split `TopBadges` into a data module (`getSignalGroups(node)` on the server) and a small renderer; keep `lib/markdown.ts` but add tests. Server components by default; client only for graph, tables, forms, search, theme. Data: generate `nodes-index.json` (about 60 KB) plus per-node body files at build, import the index client-side, import bodies only in the node page. Lazy: graph, mermaid, xlsx.

**Effort and risks.** About 3 to 4 working days. Risk: keeps `lib/markdown.ts` regex passes and the 1,300-line graph file, so the code gets only partly cleaner.

**Wireframes (A)**

Home
```
+--------------------------------------------------------------+
| (turtle) Living Evidence Synthesis   Graph Nodes ... [search][gh][user][moon] |
+--------------------------------------------------------------+
| LIVING EVIDENCE SYNTHESIS                                    |
| Can LLMs be used for peer review ...?   (serif, 2.5rem)      |
| intro paragraph (65ch)                                       |
| [Explore the graph]  [Browse all nodes]                      |
|                                                              |
| CORPUS AT A GLANCE                                           |
| [QUE 27][CLM 31][EVD 77][CVT 49][SRC 27][EP 21]              |
|                                                              |
| BEST-SUPPORTED CLAIMS                                        |
| 1 [CLAIM CLM-011] title ...................... [9 EVD]       |
| 2 ...                                                        |
| [Narratives]   [Review status]   [About the method]          |
+--------------------------------------------------------------+
| footer                                                       |
+--------------------------------------------------------------+
```
Node page (EVD)
```
[EVIDENCE EVD-010] [Initial AI draft]
Title of the evidence (serif)                               
Citation line  ·  quality signals [Show v]
+---------+-----------------------------------+-------------+
| ON THIS | v Description                     | REVIEW      |
| PAGE    |   text, quotes, figure <details>  | [verdict v] |
|  Desc.  | v Methods context                 | [note    ]  |
|  Methods|   field list, prompts <details>   | [Submit]    |
|  Other  | v Other notes (table + caption)   | INBOUND (3) |
|  Caveats| v Caveats                         |  supports.. |
|         |                                   | OUTBOUND (2)|
+---------+-----------------------------------+-------------+
| References (small)                                           |
+--------------------------------------------------------------+
```
Graph
```
Discourse graph
[Type v][Status v][5C v][Task v][More filters v]   [Fit] [List]
+-------------------------------------------+---------------+
|                                           | DETAIL PANEL  |
|        (canvas force graph)               | [CLM] CLM-011 |
|     o--o   o                              | title         |
|      \ |  / \                             | edges ...     |
|       o----o  o                           | [Open page]   |
+-------------------------------------------+---------------+
| Node list (collapsible, keyboard-friendly alternative)      |
+--------------------------------------------------------------+
```

---

### Direction B: "Reading Room" (reader-first, single column plus margin rail)

**Concept.** Treat each node as a long-form document: one calm reading column with a slim sticky rail that holds the table of contents, review and links, and move dense trust signals into a summary strip at the top. Reading is the main job of this site, so the layout favours measure, hierarchy and whitespace over dashboards.

**Visual language**
- Palette: cream page `#faf7f0`, a slightly deeper cream `#f3eee2` for rails, forest `#14532d` for links and the single primary action, a second tone (`#e6efe0` wash) for selected states. Dark mode keeps today's values with `forest` lifted to `#4ade80`.
- Type scale: body 1.0625rem (17 px) serif for article text (Source Serif 4), Inter for UI, 1.2 modular scale (0.8125, 1, 1.25, 1.5, 1.875, 2.25). Mono only for IDs and prompts.
- Spacing: 8 px grid, article rhythm 1.5 line-height 1.7.
- Radius: 4 px small, 8 px for cards; no pills except type badges.
- Elevation: flat, 1 px hairlines in `#d9d2c0` (about 1.5:1 decorative; inputs get a 3:1 border).
- Data tables: horizontal rules only, no vertical lines, sticky first column on wide tables, row expand for long quotes.
- Callouts: full-bleed left bar plus icon, no tinted box on prose callouts (keep tint only for warnings).
- Graph: lighter canvas on paper, nodes sized by degree, edges at 30 percent ink, labels only on hover and focus plus the top 20 by degree.
- Dark mode: **yes**, system default with a toggle.

**Layout and navigation.** Top bar with logo, 5 primary links (Graph, Nodes, Narratives, Quality, Prompts), "More" menu (Review, Contribute, Pipeline, About), search. Node page: reading column at 68ch centred; **right rail** (sticky) carries On this page, Review and Edges as three tabs; below 1024 px the rail becomes a bottom bar with the same three tabs opening as a sheet. Review lives in the rail tab "Review"; Contribute is a top-level link and also a "Suggest a correction" link in the rail that deep-links to the form with the node prefilled (a small new convenience, same flow).

**Density.** Low to medium. Trust signals collapse to a one-line summary ("12 of 20 signals strong, 2 concerns") that expands into the existing Quality Signals table.

**Accessibility notes.** Strongest reading experience: larger text, shorter measure, fewer competing columns, simple reflow at 320 px. Tabs need correct roles and arrow-key handling.

**Code architecture.** Plain Tailwind tokens plus a small headless layer (Radix primitives for Tabs, Popover, Dialog, Tooltip; no full library). Server components for article, rail content and tables; client for rail tabs, search, graph, forms. Convert vault markdown to a structured tree at build (remark/rehype plugins instead of regex string passes), emitting one JSON or MDX-like file per node so the page imports only its own node. Index file for list pages. Lazy mermaid and graph.

**Effort and risks.** About 7 to 9 working days. Risk: swapping `lib/markdown.ts` for a rehype pipeline is the largest change and needs a visual diff of all 232 pages; tabs hide information that is visible today (edges, review).

**Wireframes (B)**

Home
```
+--------------------------------------------------------------+
| (turtle) LIVES      Graph  Nodes  Narratives  Quality  Prompts  More v   [search] [moon] |
+--------------------------------------------------------------+
|                                                              |
|     Can LLMs be used for peer review and evidence            |
|     appraisal of scientific literature?                      |
|     Short two-line standfirst.      [Start with narratives]  |
|                                     [Explore the graph]      |
|--------------------------------------------------------------|
|  27 questions · 31 claims · 77 evidence · 49 caveats ·       |
|  27 sources · 21 patterns          (inline stat line, links) |
|--------------------------------------------------------------|
|  Best-supported claims (table-like list, rules only)         |
|   1  Claim title ....................................  9    |
|   2  ...                                                     |
+--------------------------------------------------------------+
```
Node page (EVD)
```
EVD-010 · Evidence · Initial AI draft
Title of the evidence (serif 2.25rem)
Citation · Strength summary: "7 strong · 2 concerns"  [Details]
+-------------------------------------+----------------------+
| Description                         | [On page|Review|Links]|
|   text at 68ch                      |  Description         |
| Methods context                     |  Methods context     |
|   Label    value (field list)       |  Other notes         |
|   Prompt   > disclosure             |  Caveats             |
| Other notes                         |                      |
|   Table 2 (caption) rules only      |  (tab: Review form   |
| Caveats                             |   or edges list)     |
+-------------------------------------+----------------------+
| References                                                   |
+--------------------------------------------------------------+
```
Graph
```
+--------------------------------------------------------------+
| Graph   [Filters (3)]   Search nodes [__________]  [Fit]     |
+--------------------------------------------------------------+
|                                                              |
|          full-width canvas on paper                          |
|            o   o--o                                          |
|             \ /    \                                         |
|              o------o         +--------------------------+   |
|                               | CLM-011 (sheet on select) |   |
|                               | title · 9 edges · [Open]  |   |
|                               +--------------------------+   |
+--------------------------------------------------------------+
| [Table view] alternative: sortable list of all nodes         |
+--------------------------------------------------------------+
```

---

### Direction C: "Workbench" (app-shell, built for analysis)

**Concept.** Turn the site into a research workbench: a left sidebar for navigation and a split view where lists, the graph and node details sit side by side. It suits expert users who compare nodes, filter heavily and move between graph, table and page without losing state.

**Visual language**
- Palette: same cream and forest, but surfaces are layered: sidebar `#f0ebde`, canvas `#faf7f0`, panels white; forest used for selection, focus and primary actions. Dark mode with deeper surfaces (`#120f0b`, `#17130f`, `#201a14`).
- Type scale: compact UI scale 0.8125 / 0.875 / 1 / 1.25 / 1.5 with serif only on page titles and article body; tabular numerals for counts.
- Spacing: 4 px grid, tight 8 px gaps in tools, 24 px in articles.
- Radius: 6 px; 10 px for panels.
- Elevation: two levels (panel border, floating popover shadow).
- Data tables: dense, sticky header and first column, column picker, row selection, inline expanders; shared by `/nodes`, `/quality` and `/prompts` as one table component.
- Callouts: compact, icon plus tint.
- Graph: dark-on-light default canvas, legend as filter chips, minimap-less; selection syncs with a table and a detail panel.
- Dark mode: **yes**, first-class.

**Layout and navigation.** Collapsible left sidebar (icon plus label) with Graph, Nodes, Narratives, Quality, Prompts, Review, Contribute, Pipeline, About; top strip with breadcrumbs, search, account, theme. On small screens the sidebar becomes a drawer. Node page: article plus a right inspector (Review, Edges, Signals) as a resizable panel (the graph already has a resizable panel, reused). Review and Contribute sit in the inspector and the sidebar.

**Density.** High. Many things visible at once; more chrome, less whitespace.

**Accessibility notes.** Highest risk of regressions: split panes, resizers, drawers and tables need careful focus management, landmarks and keyboard handling; small type must still honour the 12 px floor. Panels must reflow to stacked views at 320 px.

**Code architecture.** shadcn/ui (Radix plus Tailwind, copy-in components) for Sidebar, Table, Sheet, Command (search palette), Tabs, Tooltip, Form; TanStack Table for the shared table; TanStack Virtual for long lists; client-heavy shell with server-rendered article content. A client store (URL state first, e.g. nuqs) keeps filters across graph, list and table. Data: index JSON plus per-node chunks, fetched on selection for the inspector (static files, cacheable). Lazy graph.

**Effort and risks.** About 12 to 15 working days. Risks: largest scope; shadcn adds about 15 to 25 copied components to maintain; app-shell patterns work against the static-document nature of 232 citable pages (back button, share links and print need extra care); more client JS.

**Wireframes (C)**

Home
```
+------+-------------------------------------------------------+
| LIVES| Home                          [search ⌘K] [user] [moon]|
|------|-------------------------------------------------------|
| Home | Can LLMs be used for peer review ...?                 |
| Graph| [Explore graph] [Browse nodes]                        |
| Nodes|                                                       |
| Narr.| +------+------+------+------+------+------+           |
| Qual.| |QUE 27|CLM 31|EVD 77|CVT 49|SRC 27|EP 21 |           |
| Prom.| +------+------+------+------+------+------+           |
|------| Best-supported claims        | Recent activity        |
| Rev. | 1 title ..... 9 EVD          | reviews (aliases)      |
| Contr| 2 ...                        | latest contributions   |
| Pipe.|                              |                        |
| About|                                                       |
+------+-------------------------------------------------------+
```
Node page (EVD)
```
+------+--------------------------------------+---------------+
| nav  | Nodes / Evidence / EVD-010           | INSPECTOR     |
|      | Title (serif)    [Initial AI draft]  | [Review|Edges|Signals]
|      |--------------------------------------|---------------|
|      | On this page: Desc | Methods | Notes  | verdict [ v ] |
|      |--------------------------------------| note [      ] |
|      | Description                          | [Submit]      |
|      |   text, quote, figure <details>      |               |
|      | Methods context                      | Inbound (3)   |
|      |   field list, prompts <details>      | Outbound (2)  |
|      | Other notes (table)                  |               |
+------+--------------------------------------+---------------+
```
Graph
```
+------+----------------------------+--------------------------+
| nav  | [filters chips ........]   | SELECTED: CLM-011        |
|      |  [Type][Status][5C][Task]  | title, status, signals   |
|      |----------------------------| Edges (table, sortable)  |
|      |                            | [Open page] [Review]     |
|      |   (canvas force graph)     |--------------------------|
|      |                            | RESULTS (142) virtual    |
|      |   legend: type chips       | list synced with filters |
+------+----------------------------+--------------------------+
```

---

### Side-by-side

| | A Refined Journal | B Reading Room | C Workbench |
|---|---|---|---|
| Change from today | small | medium | large |
| Navigation | top bar plus menu | top bar plus More plus rail tabs | sidebar plus inspector |
| Density | medium | low to medium | high |
| Dark mode | yes | yes | yes |
| Library | plain Tailwind tokens, hand primitives | plain Tailwind plus Radix pieces | shadcn/ui, TanStack Table |
| Markdown pipeline | keep, add tests | replace with rehype | keep or replace |
| Effort | 3 to 4 days | 7 to 9 days | 12 to 15 days |
| Main risk | code only partly cleaner | rewrite of renderer, hidden info in tabs | scope, app-shell vs static pages, a11y of panes |
| Best for | "same site, fixed" | readers and citers | analysts and reviewers |

---

## 3. Recommendation

**Choose Direction B's layout with Direction A's discipline, built in this order:**

1. Do the shared fixes and the A token and primitive layer first (about 3 to 4 days). They remove the measurable problems: 2 MB payloads on two pages, no mobile nav, no skip link, weak focus, sub-12 px text, no CI.
2. Then adopt B's reading column and right rail on node pages only, and keep the rest of the site on the A layout.
3. Replace the regex markdown pipeline with a rehype pipeline **only if** the visual diff of all 232 pages is practical; otherwise keep `lib/markdown.ts` and add snapshot tests around it first.

Reasons:
- The site's job is reading and checking a cited chain of evidence, so node pages are the product; B improves exactly that and A fixes everything else cheaply.
- The user's constraints (same features, same identity, "cleaner and more efficient code") point away from C: a workbench shell adds client JS, a component library to maintain, and accessibility risk, for a corpus of 232 nodes that is read more than it is manipulated.
- Each step is shippable on its own, so a day-long rebuild can stop after step 1 with a clearly better site.

---

## 4. Decisions JP must make before the rebuild

| # | Decision | Options | Default |
|---|---|---|---|
| 1 | Navigation model | top bar with More menu; top bar with all links plus mobile drawer; left sidebar | top bar, 5 primary links plus "More", drawer below 768 px |
| 2 | Density | compact (C), medium (A), airy (B) | medium on lists and tables, airy reading column on node pages |
| 3 | Dark mode | keep (already exists), drop to simplify, keep but system-only | keep, with a toggle; node-type colours get dark variants that reach 3:1 |
| 4 | Graph library | keep `react-force-graph-2d` (canvas, easy), move to Cytoscape.js, or d3 plus SVG for full accessibility | keep `react-force-graph-2d`, add the node list as the accessible alternative and a table view; revisit only if keyboard operation of the canvas is a requirement |
| 5 | Markdown pipeline | keep `lib/markdown.ts` with tests, or rewrite as rehype | keep with snapshot tests first; rewrite later |
| 6 | Component library | plain Tailwind tokens only; Radix pieces; shadcn/ui | plain Tailwind tokens plus Radix only for Tabs, Popover and Dialog |

Smaller choices to confirm: whether the generated JSON should stay committed (default: yes, but split into index plus per-node files so diffs are smaller), and whether to delete `d3-force` and `referencecheck` after a usage check.

# LIVES redesign inventory

Status: written 2026-11-24 from the code at `main` (commit 1a41637) and from fetching the live site `https://living-evidence-synthesis.vercel.app`. Nothing here changes app code.

How facts were gathered: file reads of `app/`, `components/`, `lib/`, `scripts/`, `supabase/`, `.github/`, `package.json`, `app/globals.css`; `curl` against the live pages for payload sizes and cache headers; a script that computed WCAG contrast ratios from the CSS hex values. **No screenshots were taken** (no browser session was used); visual descriptions come from the HTML and CSS. Anything not checked is marked **[unverified]**.

Note on the briefing: `CLAUDE.md` is only an `@AGENTS.md` pointer plus the Next.js "this is not the Next you know" block; `AGENTS.md` is a short repo note. `REVIEW.md` documents the trust-signal fields, `FIXES.md` is a build postmortem, `TODO.md` is content work. None of these set UI rules beyond what is listed below. There is **no `tailwind.config`**: Tailwind v4 is configured in CSS (`@theme inline` in `app/globals.css`) with `@tailwindcss/postcss`.

---

## 1. Routes

All pages are statically prerendered (no `dynamic`, no `revalidate`, no server data fetch at request time). The only server-run code is the five route handlers under `app/api/`.

| Route | File | What it does | Client JS involved |
|---|---|---|---|
| `/` | `app/page.tsx` | Hero question, two buttons, six count tiles (link to `/nodes?type=X`), top 6 "best-supported claims" (ranked by distinct EVD support), three cards (Narratives, Review, About). | none beyond header |
| `/graph` | `app/graph/page.tsx` | Force-directed graph of all 232 nodes and 784 edges with filters, detail panel and node list. Passes **all** nodes and edges to the client. | `GraphExplorer` (1,353 lines) |
| `/nodes` | `app/nodes/page.tsx` | Searchable, filterable, sortable list of all nodes. Reads `?type=`. Passes all nodes (with bodies) to the client. | `NodesExplorer` |
| `/nodes/[id]` | `app/nodes/[id]/page.tsx` | One page per node (232 via `generateStaticParams`). Header badges, citation, truth value or caveat meta, trust badges, credibility box, prompt disclosure, body article, TOC, review widget, inbound/outbound edges, References footer. Unknown id gives `notFound()`. | `NodeArticle` (mermaid), `ReviewWidget`, several tooltips |
| `/narratives` | `app/narratives/page.tsx` | Three hand-written essays that link into nodes (`N` helper component inline). | none |
| `/quality` | `app/quality/page.tsx` | "Evidence Quality": one row per EVD (77), columns from `lib/qualityColumns.ts`, sort, filter, column picker, export (xlsx loaded on demand). | `EvidenceQualityTable` |
| `/prompts` | `app/prompts/page.tsx` | Prompt tactics grid: 27 sources coded on 11 dimensions, expandable rows with verbatim prompts. Data from `lib/promptTactics.ts` (1,021 lines, hand-coded). | `PromptTacticsExplorer` |
| `/review` | `app/review/page.tsx` | Curation-status matrix (server computed), live review submissions (client, sign-in gated), verdict vocabulary. | `LiveReviewPanel` |
| `/contribute` | `app/contribute/page.tsx` | Four-step guidance plus the GitHub-sign-in form that opens a PR. | `ContributeForm`, `NodePicker` |
| `/pipeline` | `app/pipeline/page.tsx` | Renders the "🛠️" section of `vault/Welcome.md` through the same markdown pipeline; reads the file at build time. | `NodeArticle` |
| `/about` | `app/about/page.tsx` | Method explainer: node-spec, node types, curation status, edges, "what this site is not". | none |
| `/login` | `app/login/page.tsx` | Supabase email one-time-code sign-in (8-digit code, hard-coded in label, placeholder, `maxLength`) or link. Honours `?next=`. | client page |
| `/api/github/login` | route handler | Sets `gh_oauth_state` and `gh_oauth_next` cookies (httpOnly, 10 min), redirects to GitHub authorize (scope `public_repo`). | n/a |
| `/api/github/callback` | route handler | Checks state, exchanges code, sets httpOnly `gh_token` cookie (30 days), redirects only to same-site paths. | n/a |
| `/api/github/me` | route handler | Returns `{signedIn, login, avatarUrl}` from the token cookie. | n/a |
| `/api/github/logout` | route handler | POST clears `gh_token`; GET clears it and redirects to `/contribute`. | n/a |
| `/api/contribute` | route handler | Validates input, forks the repo into the user's account, creates a branch, writes the new node file plus patches, returns a GitHub compare URL. In-memory rate limit of 5 per hour per user. | n/a |

There is **no image route**. Figures are plain static files under `/vault-img/<name>.png` (see section 3).

Global layout (`app/layout.tsx`): `<html lang="en" data-theme>`, Google Fonts `<link>` (Source Serif 4, Inter, JetBrains Mono), an inline no-flash theme script, `Header`, `children`, `Footer`; KaTeX stylesheet imported globally.

---

## 2. Components

"Used by" is from import search. "Kind" is server (S) or client (C).

| Component | Kind | Props | Used by | Notes |
|---|---|---|---|---|
| `Header` | S | none | layout | Logo (Turtle icon), 9 nav links (`hidden md:flex`), `SearchPalette`, GitHub link, `AuthStatus`, `ThemeToggle`. Nav list duplicated in no other place; GitHub icon SVG duplicated in `Footer`. |
| `Footer` | S | none | layout | Blurb plus 5 links. |
| `SearchPalette` | C | none | Header | Ctrl/Cmd+K dialog, Fuse over `ALL_NODES` (imports the whole 2 MB dataset into every page bundle **[to confirm in bundle analyser]**), top 8; on `/graph` dispatches `graph:select-node` instead of navigating. |
| `ThemeToggle` | C | none | Header | `useSyncExternalStore`, writes `localStorage.theme` and `data-theme`. |
| `AuthStatus` | C | none | Header | Shows Supabase session email / sign-in link. |
| `NodeTypeBadge` | S | `type`, `id?` | home, node page, about, review, EdgeGroup, NodesExplorer, LiveReviewPanel, NodePicker, ContributeForm, SearchPalette | Pill, white text on node colour. |
| `StatusBadge` | S | `status` | node page, NodesExplorer | Tones draft / reviewed / other. |
| `NodeArticle` | C | `html` | node page, pipeline | `dangerouslySetInnerHTML`; loads mermaid dynamically, wraps diagrams with fit and fullscreen toolbar built with raw DOM. |
| `SourceToc` | S | `items: TocItem[]` | node page | Sticky left TOC, `hidden lg:block`, `nav aria-label="Table of contents"`. |
| `EdgeGroups` | S | `edges`, `otherEnd: "from" or "to"` | node page | Groups edges by type. |
| `ReviewWidget` | C | `nodeId` | node page | Supabase verdict form (7 verdicts, proposed text, note up to 2000 chars, consent checkbox), shows others' reviews by alias. |
| `LiveReviewPanel` | C | none | review page | Latest 200 reviews, sign-in gated. |
| `SourceCitation` | C | `node` | node page | APA line, DOI link. |
| `ClaimTruthValue` | S | `value: number` | node page | Truth-value bar with `ScaleTooltip`. |
| `CaveatMeta` | S | `severity?`, `caveatType?` | node page | Chips with tooltips. |
| `TopBadges` | S | `node` | node page | 1,356 lines. Builds all trust-signal chips (TOP, Rigor, Integrity, 5Cs, tasks, FAIR). Largest single component. |
| `ChipRows` | S | `chips: ReactNode[]` (+ `chunkChips` helper) | TopBadges | Rows of 4. |
| `CollapsibleSignalBlock` | C | `summary`, `children` | TopBadges | Show/hide Quality Signals button (`aria-label` carries summary). |
| `QualitySignalsTable` | S | `groups: SignalGroup[]` | TopBadges | The nutrition-style table: group headings, colour dot, status word, optional scale tooltip and link. `aria-label="Quality signals"`. |
| `ScaleTooltip` | C | `scale`, `current`, `description`, `children` | TopBadges, ClaimTruthValue, CaveatMeta, QualitySignalsTable | Hover popover with `role="tooltip"`, sr-only text; scales defined in `lib/scales.ts`. |
| `SourceCredibility` | S | `node` | node page | Boxed panel of curation checks (DOI, retraction, authors, citations, PubPeer, predatory flag). Embeds `AltmetricBadge`. |
| `AltmetricBadge` | C | `doi` | SourceCredibility | Loads third-party Altmetric embed **[script source unverified]**. |
| `PromptDetail` | S | `srcId`, `inherited?`, `className?` | node page | Prompt disclosure; same markup as `lib/promptBlock.ts` string version (duplicate by design, see section 6). |
| `NodesExplorer` | C | `nodes` | nodes page | Fuse search, type chips, status select, sort (relevance, title, degree, updated). |
| `GraphExplorer` | C | `nodes`, `edges` | graph page | `react-force-graph-2d` (canvas, dynamic import, `ssr:false`), type / status / 5C / task / TOP / validity / integrity and about 15 more filters, label-collision logic, resizable detail panel stored in `localStorage` (`graph:panelWidth`), node list, fit button. |
| `EvidenceQualityTable` | C | `rows: QualityRow[]` | quality page | Sort, filter, column picker, export via dynamic `xlsx`. |
| `PromptTacticsExplorer` | C | `rows: PromptTactics[]` | prompts page | Counts bar, matrix, expandable rows (`aria-expanded`). |
| `ContributeForm` | C | none | contribute page | 438 lines, GitHub sign-in state, fields per node type, word-count validation 50 to 250, posts to `/api/contribute`. |
| `NodePicker` | C | `label`, `hint`, `targetType`, `value`, `onChange` | ContributeForm | Search-and-select of existing node ids. |

Library modules: `lib/data.ts` (845 lines, types, getters for every signal), `lib/markdown.ts` (741 lines, 20+ string-transform passes over rendered HTML), `lib/promptTactics.ts` (1,021 lines of data), `lib/qualityColumns.ts`, `lib/scales.ts`, `lib/promptBlock.ts`, `lib/apa.ts`, `lib/node-markdown.ts` (contribution file builder), `lib/github.ts` (server-only), `lib/sanitize.ts`, `lib/supabase.ts`, `lib/useAuth.ts`, `lib/ui.ts`.

---

## 3. Data flow

```
vault/**/*.md  (Obsidian, 232 nodes)
   │  scripts/build-graph.mjs   (gray-matter; wikilinks to typed edges; alt text for images)
   ▼
lib/graph-data.generated.json  (2,006,565 bytes, committed)   lib/node-ids.json
   │  imported statically by lib/data.ts
   ▼
server pages ─ getters ─ lib/markdown.ts (marked, KaTeX, callouts, accordions, sanitize-html) ─ HTML string
   │                                              └─ NodeArticle (client) runs mermaid in the browser
   └─ client components that import ALL_NODES directly: SearchPalette (every page), NodesExplorer, GraphExplorer
```

- **Build**: `scripts/build-graph.mjs` (555 lines) is run by hand or by the GitHub workflow. Vercel does **not** regenerate it; the JSON is committed. Data counts: 232 nodes (EVD 77, CVT 49, CLM 31, QUE 27, SRC 27, EP 21), 784 edges. Total markdown body text 1.62 MB; per-node `extras` another 48 KB.
- **Images**: `npm run build` and `dev` run `preflight`, which runs `scripts/sync-attachments.mjs`: copies only referenced crops from `vault/**/Attachments/` into gitignored `public/vault-img/`. Source folder holds 712 files, 104.5 MB, largest 1.49 MB (PNG). Embeds render as `<details>` figures with `<img loading="lazy">` and generated alt text; a missing file renders a named placeholder.
- **Preflight** (`scripts/preflight.mjs`): warns on low RAM, high-CPU processes, Node major above 22. `scripts/with-lock.sh` takes a `mkdir` lock so two builds cannot race.
- **Reviews (Supabase)**: browser client in `lib/supabase.ts` using `NEXT_PUBLIC_SUPABASE_URL` and `..._ANON_KEY`; if unset, review UI hides. Email one-time-code sign-in (custom SMTP via Brevo is required). Table `node_reviews` (RLS: read and write own), public read goes through view `node_reviews_public` which returns `reviewer_name` (a randomly assigned galaxy-style alias from table `reviewer_aliases`, assigned by trigger, no policies so clients cannot read it) and `is_mine`, never email or user id. Rate-limit trigger on insert or update. Migration `2026-11-reviewer-privacy.sql` adds the alias scheme.
- **Contribute (GitHub)**: `/contribute` form posts to `/api/contribute`. OAuth: `/api/github/login` (state cookie) to GitHub to `/api/github/callback` (code exchange, `gh_token` httpOnly cookie, same-site redirect check). Server then forks, branches (`contribute/<type>-<ts>`), commits the new node file and patches to the parent Question or Claim, returns a compare URL; the user opens the PR themselves. Env: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_OAUTH_REDIRECT_URI`, `GITHUB_REPO_OWNER`, `GITHUB_REPO_NAME`, `GITHUB_REPO_BASE_BRANCH`. If unset, `lib/github.ts` reads `process.env.X!` at import time (non-null assertions, no guard).
- **Regenerate workflow** (`.github/workflows/regenerate-graph.yml`): on push to `main` touching `vault/**` or `scripts/build-graph.mjs`, runs `npm ci --ignore-scripts`, `node scripts/build-graph.mjs`, commits the two JSON files as `github-actions[bot]`. Skips if the actor is that bot. **This is the only workflow; there is no lint, type-check, build or test CI.**
- **Other scripts**: `scripts/check-sanitize.ts` (`npm run check:sanitize`, renders real pages with and without the sanitiser), `scripts/vault_to_gsheet.py` (export, not part of the build).
- **Hosting**: Vercel. Live responses are `cache-control: public, max-age=0, must-revalidate` with `x-vercel-cache: HIT` for pages.

---

## 4. Design tokens and identity

All values are from `app/globals.css` unless noted.

### Colour: Cream + Forest

| Token | Light | Dark |
|---|---|---|
| `--color-paper` (page) | `#faf7f0` | `#17130f` |
| `--color-ink` (text) | `#1a1410` | `#f5f1e8` |
| `--color-forest` (brand, links) | `#14532d` | `#4ade80` |
| `--color-card` | `#ffffff` | `#201a14` |
| `--color-secondary-surface` | `#f0ebde` | `#241e17` |
| `--color-muted-surface` | `#f3eee2` | `#221c16` |
| `--color-accent-wash` | `#e6efe0` | `#17251c` |
| `--color-muted-ink` | `#6b6660` | `#a39c8f` |
| `--color-border` | `#e7e2d6` | `#362e24` |
| `--color-destructive` | `#b91c1c` | same |
| `--color-card-muted` | `color-mix(card 55%, secondary-surface)` | derived |

Dark mode is already implemented, three ways: `:root[data-theme="dark"]`, an `@media (prefers-color-scheme: dark)` block for `:root:not([data-theme="light"])` (duplicated token list), and the no-flash inline script plus `ThemeToggle`.

Node type colours (not changed in dark mode): question `#856404`, claim `#166534`, evidence `#c0392b`, caveat `#b45309`, source `#1e3a8a`, evidence-pattern `#7f1d1d`, artifact `#ce5555`. Verdict colours: correct `#10b981`, edit `#f59e0b`, edit-major `#ea580c`, edit-minor `#fbbf24`, wrong `#f43f5e`, missing `#8b5cf6`; N/A uses muted-ink. Verdict symbols: check, pencil, cross, cycle, dash.

### Type

- Headings h1 to h6: `Source Serif 4` (Georgia fallback), weight 600, `letter-spacing: -0.015em`.
- Body: `Inter` (system sans fallback), line-height 1.65, antialiased.
- Mono: `JetBrains Mono`; utility `.mono`.
- Fonts load from Google Fonts via `<link>` (render-blocking stylesheet, third-party request, `display=swap`). Not `next/font`.
- Page titles: `text-2xl` (home `text-3xl sm:text-4xl`, node `text-2xl sm:text-3xl`). Many tiny sizes in markup: about 66 uses of arbitrary sizes between 0.5625rem and 0.8125rem (9 to 13 px), most at 0.625rem (10 px) and 0.6875rem (11 px).
- Measure: `max-w-[65ch]` for intros, `max-w-3xl` for essays.

### Spacing, radius, layout

- Page container: `mx-auto max-w-6xl px-4 sm:px-6`; narrative pages `max-w-3xl`; review `max-w-5xl`; node page grid `max-w-[1560px]` with `lg:grid-cols-[180px_1fr_240px]` (TOC, article, aside), gap 24 px; section gaps `mt-14` on home.
- Radius: `--radius-sm 0.3rem`, `md 0.4rem`, `lg 0.5rem`, `full 9999px`.
- Elevation: almost none. Cards are 1 px border plus white fill, hover changes border to `forest/40`. Graph buttons use `shadow-sm`.
- Header 56 px (`h-14`), bottom border; Footer `mt-20`, top border.

### Components of the visual identity

- **Callouts** (`.callout`): 1 px border, 3 px left accent, background `color-mix(accent 10%, card)`, radius 0.4rem, padding `0.75em 1em`, font `0.95em`; title 0.75rem bold in the accent. Accents: info and note `#475569`, success `#047857`, tip and quote `#57534e`, warning `#b45309`, danger `#b91c1c`, question `#4338ca`, abstract `#0f766e`, example `#0e7490`. Legend variants `.callout-legend` and `.callout-legend-flat`. Icons are inline SVG from `lib/markdown.ts`.
- **Status icons**: one stone-grey hue `#57534e`, level shown by shape (solid, half, ring, dash) and opacity (1, 0.85, 0.7, 0.45). Deliberately not colour-coded.
- **Tables in prose** (`.prose-node table`): `display:block; overflow-x:auto`, 1 px borders, cell padding `0.4em 0.6em`, header `0.7rem` uppercase tracked `0.06em` on muted-surface, caption from an italic line above (`promoteTableCaptions`).
- **Accordions** (`.accordion-section`): native `<details>`, chevron drawn with borders rotating 45 deg, nested sections indented 1.15em with a hairline. Sources open only the Question section; other node types open everything.
- **Table of contents**: left sticky `nav`, 180 px, large screens only.
- **Footers**: site footer (blurb and links) and a node-page `footer#references` capped at `max-w-[40vw]`, numbered, 0.75rem text (Crossref retraction note, TRIPOD-LLM citation, curated-with-model line).
- **Quality Signals table**: grouped Transparency, Openness, Rigor (Validity, Design, Analyses, Interpretation), Integrity; colour dot in its own column plus a status word, tooltip showing the full scale. Behind a "Show quality signals" button.
- **Prompts disclosures**: `.prompt-detail` card, mono verbatim blocks with a 2 px forest left border, `white-space: pre-wrap`.
- **Figure embeds**: `.figure-embed` collapsed `<details>`, caption like "Evidence excerpt, p. 3".
- **Quote collapse**: quotes over 200 characters fold to opening words plus citation.
- **Mermaid figures**: `.mermaid-figure` card with toolbar (Fit to view toggle, Full screen); whole plot area is a click target for fullscreen (`cursor: zoom-in`); fullscreen background forced to paper with `!important`. Mermaid renders client-side only.
- **Field lists**: `.field-list` grid `minmax(9rem,max-content) 1fr`, collapses to one column under 640 px.
- **Buttons**: primary is forest fill with paper text, `rounded-md px-4 py-2 text-sm font-medium`; secondary is bordered. Chips and badges are `rounded-full`, 11 px uppercase.
- Icon set: `lucide-react` (Turtle is the logo mark).

### Contrast (computed from the hex values above)

| Pair | Ratio | Verdict (AA text 4.5, non-text 3) |
|---|---|---|
| ink on paper, light | 17.05 | pass |
| muted-ink on paper, light | 5.31 | pass |
| muted-ink on muted-surface, light | 4.91 | pass (close) |
| forest on paper, light | 8.52 | pass |
| border on paper, light (UI boundary) | 1.21 | fails 3:1 if the border is the only cue |
| ink, muted-ink, forest on paper, dark | 16.39, 6.78, 10.60 | pass |
| border on paper, dark | 1.38 | fails 3:1 as sole cue |
| node-ep `#7f1d1d` as text on dark paper | 1.84 | fail (only if used as text; badges use white text on fill, which passes) |
| node-source `#1e3a8a` on dark paper | 1.78 | fail, same condition |
| node-claim `#166534` on dark paper | 2.59 | fail, same condition |
| white on verdict-correct `#10b981` | 2.54 | fail (verdict circles) |
| white on verdict-edit `#f59e0b` | 2.15 | fail |
| white on verdict-edit-minor `#fbbf24` | 1.67 | fail |
| white on verdict-wrong `#f43f5e` | 3.67 | fail for small text, passes for large |

Whether `NODE_TYPE_TEXT_CLASS` is used on dark backgrounds was not traced **[unverified]**.

---

## 5. Features that must survive

1. Static, per-node pages for all 232 nodes with stable `/nodes/<ID>` URLs (citable).
2. Node body rendering: callouts, accordions with the source/open policy, TOC, field lists, quote collapse, table captions, figure embeds with alt text and missing-figure placeholders, KaTeX at build time, mermaid with fit and fullscreen, sanitised HTML.
3. Header badges: type, id, curation status, rating; APA citation; claim truth value; caveat severity and type.
4. Trust signals: TOP badges, Rigor, Integrity, 5Cs, evaluative tasks, FAIR scores, the Quality Signals table with scale tooltips, SourceCredibility box with Altmetric.
5. Prompt disclosure on SRC and EVD pages and the `/prompts` grid with verbatim prompts.
6. Inbound and outbound edges grouped by type on every node page.
7. `/graph`: force layout, all filters, click-to-preview panel (resizable, width remembered), node list, fit-to-view, search palette integration (`graph:select-node`).
8. `/nodes` search, type, status and sort; `?type=` deep link from home tiles.
9. Global search palette on Ctrl/Cmd+K.
10. `/quality` table: sort, filter, column picker, export to spreadsheet.
11. Narratives, About, Pipeline, Review status matrix, verdict vocabulary.
12. Supabase one-time-code sign-in, per-node accuracy review with seven verdicts, consent checkbox, reviewer aliases (never emails), live panel on `/review`, graceful hide when env vars missing.
13. GitHub contribute flow: OAuth, fork, branch, commit, patch parent, compare URL, rate limit, validation, same-site redirect check.
14. Light and dark themes with no flash, persisted choice.
15. Identity: Cream + Forest palette, serif headings, mono IDs, turtle logo, restrained shape-based status icons, node-type colours.
16. Build tooling: vault to JSON generator, regenerate workflow, attachment sync, preflight, lock, sanitiser check, Node 22.
17. Licence and takedown note and the references footer wording on node pages.

---

## 6. Known problems

### Performance (measured on the live site, 2026-11-24)

| Page | HTML raw | HTML brotli | Note |
|---|---|---|---|
| `/` | 51.0 KB | 8.3 KB | fine |
| `/graph` | 2,018,962 B | 420,492 B | embeds the full dataset |
| `/nodes` | 1,961,765 B | 415,055 B | same dataset, again |
| `/nodes/EVD-010` | 136.4 KB | 19.5 KB | ok; also pulls the chunk set below |
| `/quality` | 245.8 KB | 16.6 KB | ok |
| `/prompts` | 117.5 KB | 17.8 KB | ok |

- The two heavy pages serialise **every node, including full `bodyMarkdown` (1.6 MB of text)**, into the RSC payload so Fuse can search titles and tags. Only titles, ids, tags, status and degree are needed for the list and graph; bodies are needed only on the node page.
- `SearchPalette` imports `ALL_NODES` too, so the dataset is in the shared client bundle or a shared chunk **[confirm with a bundle analyser; not run]**.
- JS referenced from the HTML: 12 to 13 files, about 0.70 MB brotli per page (EVD and graph both measured); mermaid and xlsx are dynamic imports. Single CSS file 14.5 KB brotli.
- Images: static files served with `cache-control: public, max-age=0, must-revalidate` (confirmed on three crops), so every view revalidates; they are not content-hashed so they cannot be marked immutable as is. PNGs only, sizes seen 82 to 250 KB, repo maximum 1.49 MB; no `next/image`, no `width` or `height` attributes (layout shift on open), no WebP or AVIF. `loading="lazy"` is set, and figures are collapsed by default which limits cost.
- Fonts: three families from Google Fonts by stylesheet link instead of `next/font` (extra origin, render-blocking CSS, flash risk).
- The generated JSON is committed (2 MB, noisy diffs, merge conflicts on any vault edit).
- Graph is a canvas that redraws with custom label-collision code; cost on low-end phones not measured **[unverified]**.

### Accessibility

Verified in code:
- ~~No skip link~~ **Fixed in PR #25** (skip link in `app/layout.tsx`). Statement kept for the record; the facts below were written before that change.
- ~~No mobile navigation~~ **Fixed in PR #25** (`components/MobileNav.tsx`). Before that, the nav was `hidden md:flex` and there is no menu button, so below 768 px the nine sections are unreachable except from the footer and home cards.
- Landmarks: `header`, `main` (per page), `footer`, a `nav` for the TOC (large screens only). The header `nav` has no `aria-label`. Home hero is fine; node page mixes several `h2`s but only one `h1`.
- **Focus**: inputs and the theme button use `focus:outline-none focus:ring-1 focus:ring-forest` (1 px ring, thin); links, summaries, chips and most buttons have **no custom focus style** (browser default only) and the global CSS defines no `:focus-visible` rule. The graph's resize handle does define a `focus-visible` outline.
- **Target size**: icon buttons are 32 px (`h-8 w-8`) which meets WCAG 2.2 AA minimum (24 px) but not 44 px; chips and badges at 11 px type with `py-0.5` are about 20 px tall (if interactive they would fail the 24 px minimum; the type badges are not interactive).
- **Text size**: about 66 spots at 9 to 13 px.
- **Alt text**: figure `<img>` has generated alt ("Table from the source paper, p. 4, next to the quote: ..."), good and specific; `vault/_alt/alt-text.json` override map does not exist. Quote-adjacent text is truncated with an ellipsis.
- **Colour only / contrast**: see table in section 4; verdict circles and dark-mode node colours are the weak points. Status icons correctly rely on shape.
- **Graph**: canvas has no accessible equivalent except the node list (`aria-controls="graph-node-list"`), which is a good start; keyboard use of the canvas itself unverified **[unverified]**.
- **Mermaid**: the click-anywhere fullscreen on the diagram has no keyboard path other than the toolbar button; diagrams have no text alternative **[unverified how much the SVG exposes]**.
- Reduced motion: no `prefers-reduced-motion` rule anywhere; transitions are short (0.12 to 0.15 s) and the graph animates.
- Details/summary accordions are native, which is good for keyboard and anchors.
- Tooltip (`ScaleTooltip`) opens on hover; focus and touch behaviour **[unverified]**; the sr-only text suggests there is a non-hover route.
- Form errors: login and review show `status` text; whether they are announced (`aria-live`, `role=alert`) is not set (grep found no `aria-live`).

### Code

- `components/TopBadges.tsx` (1,356 lines), `GraphExplorer.tsx` (1,353), `ContributeForm.tsx` (438), `EvidenceQualityTable.tsx` (346) are too large and mix data derivation with markup.
- `lib/data.ts` has 40+ per-signal getters with the same tag-prefix parse; `GraphExplorer` imports around 30 of them for filters.
- **Duplicated logic**: prompt disclosure exists as `PromptDetail.tsx` and `lib/promptBlock.ts` (the latter because bodies are HTML strings); `GithubIcon` and `METHOD_SOURCE_URL` are copy-pasted in `Header` and `Footer`; input field class strings repeated about 15 times; 4 maps in `lib/ui.ts` that each repeat the six node types; the dark palette is declared twice in CSS; display-title logic is written twice in `app/nodes/[id]/page.tsx`; `getDegree` filters all 784 edges per call; `getInboundEdges` and friends rescan the edge list each call.
- `lib/markdown.ts` is a chain of regex transforms over HTML text; fragile and order-dependent, and its output is injected with `dangerouslySetInnerHTML` (mitigated by `sanitize-html`, checked by `check:sanitize`).
- Raw-DOM mermaid toolbar in `NodeArticle` (building buttons with `innerHTML`) sits outside React.
- Dependencies that look unused: `d3-force` (only mentioned in a comment; the graph library bundles its own) and `referencecheck` (no import found); `xlsx` is used but only for export and loaded on demand. Verify before removal **[grep only]**.
- `lib/github.ts` reads env vars with `!` at import time.
- Rate limit is in-memory per serverless instance (documented as best effort).
- Hard-coded 8-digit code length in `/login`.
- `next.config.mjs` sets `outputFileTracingRoot` and webpack memory optimisations (needed, see `FIXES.md`).
- Docs drift: `TODO.md` lists `alharbi2024-table1cont-p5-1.png` as missing, but the live site serves it; `README.md` says "232 statically-generated" while `FIXES.md` says 242 pages at an earlier build; comment in `login/page.tsx` says 6-digit while README says 8.
- **Tests: none.** No test runner or script in `package.json`; only `lint` and `check:sanitize`. **CI: none** except the regenerate workflow, so type errors, lint failures and build failures are caught only by Vercel at deploy. `AGENTS.md` and `CLAUDE.md` give no UI conventions.

---

## 7. Constraints

- **Static prerender**: every content page must remain a build-time page (`generateStaticParams` for nodes). Only API routes and Supabase or GitHub calls are live.
- **Vercel** hosting; the production alias `living-evidence-synthesis.vercel.app` is the one Supabase Site URL and the GitHub OAuth callback depend on. Preview URLs break both flows (documented in README).
- **Node 22 only** (`engines >=22 <23`, `.nvmrc 22.14.0`); newer Node caused hung builds (`FIXES.md`).
- Next.js 16.3.1 with App Router, React 19.2.8, Tailwind 4 (CSS config), TypeScript strict. `AGENTS.md` warns this Next has breaking changes: read `node_modules/next/dist/docs/` before writing code.
- Committed generated JSON and the vault are the source of truth; the build must stay offline and deterministic.
- Copyright: source PDFs are never in the repo; screenshot crops are, with per-paper licence notes in `docs/PERMISSIONS.md` (several "not allowed or needs checking"), which is a content risk independent of design.
- Env vars optional: the site must work with Supabase and GitHub unconfigured.
- No-regression rules from the docs: colour is never the only encoding; Quality-appraisal and TRIPOD tables must not get source captions; verdict vocabulary comes from the node-spec.

# Redesign decisions: Direction A, kept conservative and reversible

Status: proposed by Claude on JP's instruction (2026-11-24); JP approves or reverses each row. Builds on `design-directions.md` (Direction A, "Refined Journal") and `inventory.md`. No app code changes in this file.

## What JP asked for

- Follow Direction A. Keep it calm, not flashy.
- Accept decisions 1 to 6 from `design-directions.md` section 4 where justified, and make conservative, reversible choices.
- **Everything must work from the keyboard as well as the mouse**: a person can view and interact with every page and task without a mouse.

## Decisions 1 to 6

| # | Decision | Choice | Why (and how to undo it) |
|---|---|---|---|
| 1 | Navigation | **A's top bar**: logo, all links, search, GitHub, account, theme. Below 768 px the links collapse into a labelled menu button (a disclosure: Enter or Space opens, Esc closes and returns focus). Skip link first. | It is today's layout plus the missing mobile menu, so the smallest change. The doc's default ("5 links plus More") is Direction B's pattern and moves links people use now. Undo: move links into a "More" group in one component. |
| 2 | Density | **Medium** everywhere (A). Article text stays at about 70 characters per line, 16 px body, 1.5 line height. | Matches the current look and the "don't make it crazy" brief. B's airy column and C's dense panels are bigger changes. Undo: spacing and measure live in tokens. |
| 3 | Dark mode | **Keep**, follow the system setting, with a visible toggle that is remembered. Deduplicate the token block. Node-type colours get dark variants that reach 3:1. | It already exists, so dropping it removes a feature. Undo: set the dark token block to the light values. |
| 4 | Graph library | **Keep `react-force-graph-2d`.** Add a keyboard path with full parity: a synchronised node list (filters, selection, details, open page), Fit and zoom as buttons, selection shown in an `aria-live` detail panel. Optional later step: arrow keys on the focused canvas to move between neighbours. | A canvas cannot be operated from the keyboard by itself, but the list can do every task the canvas does. A move to Cytoscape or d3 plus SVG is large and hard to reverse. Revisit only if the list route fails user testing. |
| 5 | Markdown | **Keep `lib/markdown.ts` and `scripts/build-graph.mjs`.** Add snapshot tests first (including path-qualified wikilinks, which the vault now uses). | A rehype rewrite touches all 232 pages. Tests make any later rewrite safe. Undo: nothing to undo. |
| 6 | Components | **Plain Tailwind tokens and hand-written primitives** (`Field`, `Button`, `Chip`, `Callout`, `Disclosure`). **Radix only for Dialog, Popover and Tooltip** where keyboard and focus handling is easy to get wrong (mermaid fullscreen, quality-signal tooltips). No shadcn/ui. | Radix has tested focus handling for exactly the widgets that need it, and nothing else is pulled in. Undo: each wrapper is one file. |

Smaller choices: keep the generated JSON committed but split into an index plus per-node files (smaller diffs); decide on deleting `d3-force` and `referencecheck` after a usage check.

## Visual rules (A, unchanged palette)

Type scale 0.75, 0.875, 1, 1.125, 1.5, 1.875, 2.5 rem; nothing below 0.75. 4 px spacing grid. 6 px radius, pills only for badges. Borders instead of shadows. `muted-ink` darkened to `#5c5750`; input borders `#8f8878` (3:1). Verdict circles use darker fills or dark text so they pass 4.5:1. Respect `prefers-reduced-motion`.

## Keyboard requirement (acceptance checklist)

Every item is tested with the keyboard alone before a release.

| Area | Must work |
|---|---|
| Whole site | Skip link; logical tab order; a focus ring (2 px, 3:1) on everything interactive and never hidden under the sticky header; no keyboard traps. No single-key shortcuts at first (WCAG 2.1.4), so nothing collides with screen readers. |
| Header | Menu button (Enter or Space, Esc closes, focus returns); theme toggle; search. |
| Search | Combobox pattern: type, Up and Down to move through results, Enter to open, Esc to close. |
| Node pages | "On this page" links jump and move focus to the heading; disclosures (`details`) open with Enter or Space; figure zoom and mermaid fullscreen open with Enter and close with Esc, focus returns. |
| Tables | Sortable headers are buttons; row links are real links; a table that scrolls sideways is focusable. |
| Graph | The list route above: filter, select, read details, open the page, all from the keyboard. |
| Forms (review, contribute, sign-in) | Labels, error text next to the field and announced, the 8-digit code field accepts paste. |
| Resize handle | `role="separator"` with arrow keys changing the size. |

Tests: Playwright keyboard-only scripts for the flows above, axe-core in CI, and a manual pass with a screen reader before each release.

## Models for design and build

- **Build model: Claude Opus 5.5** (`claude-opus-5-5`) at `high` effort, with **Claude Sonnet 5.5** (`claude-sonnet-5-5`) for mechanical phases (tests, CI, docs). JP chose a cheaper model than Claude Fable 5.2 on 2026-11-24 (Fable costs twice as much: $8 and $40 per million tokens against $4 and $20). Fable 5.2 stays a possible comparison for one hard phase if Opus 5.5 struggles; it is not in the pipeline.
- **What the evidence says:** Fable 5.2 is first on arena.ai's [Code Arena WebDev](https://arena.ai/leaderboard/code/webdev/models/claude-fable-5.2-xhigh-dum1), and I could not confirm its Design Arena standing. I did not find Opus 5.5 figures on those boards, so the cheaper choice rests on cost and on Opus 5.5 already being the pipeline's writer and judge, not on a leaderboard.
- **Past builds:** the current site's commits were co-authored mostly by Claude Sonnet 5 (63 of the app, component and lib commits), then Opus 5, Sonnet 5.5 and Opus 5.5.
- **Review by another family:** every change is reviewed by a model from a different family (GPT-6.2 Sol), plus axe, Playwright keyboard tests and Lighthouse in CI.
- **Muse Wonder Max** stays a possible later comparison, not the default.

## Cost, time and accuracy (my estimates, not measurements)

Prices (Anthropic list, per million tokens, input and output): Opus 5.5 $4 and $20; Sonnet 5.5 $2 and $10; for reference Fable 5.2 $8 and $40. Cached input is $0.20 on Opus 5.5 and $0.10 on Sonnet 5.5; the Batch API is half price but not for interactive work.

Assumption per build phase: 60 agent turns, 1.0M fresh input tokens, 8M cached input tokens, 250K output tokens including thinking. That is about **$11 per phase on Opus 5.5** (range $6 to $22) and **$5 on Sonnet 5.5**.

| Plan | Phases | Model cost | Review and tests | Elapsed time |
|---|---|---|---|---|
| Opus 5.5 for four design phases, Sonnet 5.5 for tests and CI | tokens and primitives; header, menu, skip link; node page; graph list and keyboard; tests and CI | about $50 (range $30 to $100) | about $10 to $20 | 2 to 3 working days with JP's review after each phase |
| All five on Opus 5.5 | same | about $55 | about $10 to $20 | same |
| For comparison, all five on Fable 5.2 | same | about $100 (range $60 to $200) | about $10 to $20 | same |

The design doc puts Direction A at 3 to 4 human working days; agent time is shorter, but JP's review and fix rounds set the pace.

**Accuracy** here means passing acceptance tests: 0 serious axe violations, every keyboard flow in the checklist passing, Lighthouse accessibility at least 95, graph still 232 nodes and 784 edges, no visual change beyond the planned one. First-pass rates are unknown; I assume one or two fix rounds per phase and will log the real tokens, dollars and pass rates in a ledger after phase 1.

**Recommendation:** start phase 1 on Opus 5.5 (about $11) and log the real cost.

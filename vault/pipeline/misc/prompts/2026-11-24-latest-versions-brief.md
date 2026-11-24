---
page_type: prompt
created: 2026-11-24
author: Claude (claude-sonnet-5-5) in Claude Code, for Jay Patel (JP)
---

# Brief: move a paper's vault pages to its most recent version (TODO 0d and 15)

JP decided on 2026-11-24: always cite and work from the **most recent report** (published journal or proceedings version over the preprint; latest preprint version over earlier ones). For the paper you are given, move every vault page that cites it to the newer PDF. The older PDF stays where it is for now (the parent will archive it afterwards); do not move or rename PDFs.

## Where things are
- Local vault (newer working copy): `/Users/ppatel/Documents/living-synthesis`. PDFs: `source/pdfs/` (the newer PDF has the standard name; the older one starts with `Archive - `).
- Repository copy: the GitHub repo `cdromcom/living-evidence-synthesis`, folder `vault/`. Make your own worktree and branch from origin/main (command in your task). Never touch `/Users/ppatel/.cache/lives-bench/les` (another branch is checked out there).
- Version-diff notes (what changed between the versions): `misc/evd-validation/2026-11-20-pdf-version-diff/<paper>-diff.md` and the `.json` next to it. Audit notes: `misc/evd-validation/2026-11-17-pdf-number-audit.md` and `2026-11-17-pdf-audit-proposed-changes.md` (proposals for this paper have JP's approval now).
- Pages to update: the source note `source/@<citekey>.md`, every EVD page whose Source line links it, and any claim, caveat or question page that quotes it (find them by grepping the citekey and the author name).
- Rules: the grounding rules in `Skill-templates.md` section "Grounding rules for screenshots (v2)", the numeric-audit rules in `Skill.md` Step 6b, and the page-map rule in `Skill.md` Step 1.

## What to do
1. Read the diff note. Open both PDFs. Build the page map for the NEW PDF with PyMuPDF (PDF page index to printed page; mark "PDF position only" when none is printed).
2. For every quote on every page: find the exact text in the NEW PDF (PyMuPDF search; normalise hyphenation, ligatures and quote marks). Use the new wording verbatim and cite `(Author, <year of the new version>, p. N)` with the printed page. If the quote is not in the new version, replace it with the nearest verbatim passage that supports the same point; say so in the page's PDF-check note (old and new).
3. For every number (Description summary line, title, Other Notes tables and bullets, Methods Context): check it against the NEW PDF's tables, read from the rendered page image (`pdftoppm -r 150`), checking neighbouring rows and columns. Correct errors, including the known ones in the diff note, and add a note per change: `- PDF check 2026-11-24: <old> -> <new> (<table, page>)`.
4. Titles: if a number or claim in an EVD title is no longer true in the new version, change the title (the file is named after the title, so rename the file, and update every wikilink, alias and embed that points at it in both copies). Record every rename as an entry `{"old": "<old path>", "new": "<new path>"}` appended to `misc/evd-validation/2026-11-24-renames.json` in the local vault and the branch (create it if missing; keep valid JSON; other agents append too, so re-read before writing).
5. Screenshots: recreate every quote crop and table or figure crop from the NEW PDF following the grounding rules (whole quote in a clean capture; table or figure plus caption only, all rows, columns, panels). New filenames carry the new PDF page index; leave old images in place; update embeds; confirm every embed resolves.
6. Source note: update version, year, venue, DOI (read it from the PDF or the publisher page, never guess), printed page range and the PDF filename; add a line "Earlier version: <old version>, superseded 2026-11-24" and keep the citekey and filename unchanged. If the TRIPOD-LLM table on the source note cites pages or numbers that changed, update them.
7. Apply every edit to BOTH copies (match by content; exact string replacement). Do NOT run build-graph and do NOT edit `lib/graph-data.generated.json` or `lib/node-ids.json` (the parent regenerates them once for all papers).
8. Commit in small commits on your branch (messages end with the lines `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_018V3GVqPNXkZ9Zy9gVYEivr`), push, and open a DRAFT pull request against main. The PR body lists every changed citation, quote, number, title and screenshot with old and new values, and ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)` and the session URL line. Do not merge.
9. Final reply under 300 words: PR URL, counts (quotes changed, numbers corrected, titles renamed, screenshots made, pages touched), anything uncertain or left for JP.

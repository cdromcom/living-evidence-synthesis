# How this site came to exist

A plain-language walkthrough of how this project got built, for anyone who
wasn't there for the process. Jargon appears in parentheses right after the
term it explains, the first time it comes up.

## The starting point

There was already a large pile of research notes living in Obsidian (a
note-taking app that stores everything as plain text files you can link
together). The notes covered one question: can AI language models be
trusted to help review scientific papers? Each note was tagged as one of a
few types: a Question being asked, a Claim someone makes, a piece of
Evidence backing a claim, a Caveat that limits a piece of evidence, or a
Source paper the evidence comes from. All of it was linked together into
a web of cross-references.

The goal: turn that private pile of notes into a public website anyone
could browse, styled after a reference site the owner liked, with search,
a visual map of how everything connects, and eventually a way for other
people to pitch in.

## Building the site itself

An AI coding assistant read through the whole note collection and wrote a
website (built with Next.js, a popular framework/toolkit for building
websites with the React library) that turns those notes into:

- A home page introducing the topic and highlighting the best-supported
  claims.
- A graph view: a literal node-and-line diagram (rendered with a
  force-directed graph library, meaning the nodes physically repel and
  attract each other until they settle into a readable layout) showing
  every note and how it connects to every other note.
- SRC: A page per note, showing its full text plus which other notes point to
  it and which ones it points to.
- Narratives: A handful of short written essays pulling the strongest, most
  interesting findings together into a normal reading experience, since
  the graph itself is meant to be explored non-linearly.

## Debugging the failed app build step

Turning the website's source code into an actual running app (a step
called "building," where the code gets compiled/bundled into something a
browser can load) failed, over and over, for a chain of mostly unrelated
reasons stacked on top of each other:

1. **Two builds running at once.** At one point, two separate processes
   were trying to build the same project into the same output folder at
   the same time, without knowing about each other, causing garbled
   failures.
2. **A wrong assumption about the project's location.** A leftover file
   one folder above the project confused the build tool into thinking the
   *entire* home folder was the project, so it wasted time scanning way
   more files than it needed to.
3. **The computer's browser was eating all the memory.** Firefox had
   many tabs open, competing with the build for the computer's
   memory and processing power.
4. **A wrong diagnosis, made worse.** At one point the build looked
   "frozen" (doing nothing). The instinct was to make it use less of the
   computer's processing power, thinking that would fix a memory problem.
   That backfired: it wasn't frozen, it was just slow, and using less
   processing power made it even slower and look even more stuck. The fix
   was learning to actually check what the process was doing (using a
   profiler, a tool that takes a snapshot of exactly which piece of code a
   program is running at a given moment) instead of guessing from a
   "percent busy" number that turned out to be misleading.
5. **The real, final culprit: a new version of Node.** Node
   (technically Node.js) is the underlying engine that runs the
   JavaScript-based build tools. The computer had a brand-new version
   installed, newer than what the website framework had been built and
   tested against. The fix was installing an older, compatible version of
   Node in its own folder, used only for this one project, without
   touching or downgrading anything else on the computer.

Once all of that was sorted out, the build finally succeeded cleanly and
consistently.

## Adding a real review system

The reference site had a feature letting reviewers leave a verdict on
each note (correct, needs an edit, wrong, missing something, or not
applicable). To make that actually work here (not just look like it
works), we connected a small hosted database and login service called
Supabase. Anyone can now sign in with just an email address (they get a
one-time 6-digit code, no password to remember) and leave a verdict on
any note; those verdicts are saved for everyone to see on the review
page.

## Matching the look and cleaning up the details

The colors, fonts, and page layout were matched to a reference site the
owner pointed to as the style target, including a light/dark mode toggle.
Along the way we also fixed some rough edges: badges that were
accidentally showing a note's type twice ("QUE QUE" instead of just
"Question"), link underlines that felt too busy once color already did
the job of showing what's clickable, and prose that leaned too heavily on
em dashes (the long "—" punctuation mark) instead of plain sentences.

## Publishing it

The code was pushed to GitHub (a place to store code online and
collaborate on it), first under one account, then moved to a different
one once that was requested. The raw source notes (the actual vault
files) were also brought into the published project itself, so the
website's source of truth lives in one place instead of only on one
person's laptop. The one deliberate exclusion: the actual PDF copies of
the research papers themselves were left out, since publishing full
copies of copyrighted articles isn't something this project does. Small
cropped screenshots of individual tables and figures from those papers
(used to ground specific findings) were kept, since that's a much
narrower, more defensible use than redistributing whole articles.

## Redesigning how a single source page reads

The colorful status icons scattered through each source page's tables
(green/yellow/red circles, checkmarks, warning signs) were jarring and
inconsistent with the rest of the site's restrained look, so they were
replaced with a single muted color where the *shape* (solid dot,
half-ring, open ring, dash) carries the meaning instead of the color —
friendlier for colorblind readers too. The "@..." citekey label at the
top of each page (useful for the maintainer and the AI assistant, not for
a visitor) was replaced with the paper's real title. A poorly-styled
info box explaining the TRIPOD-LLM checklist (a reporting-quality
standard borrowed from clinical research and adapted here for AI
benchmark papers) was rebuilt as a proper two-column legend, and the
checklist table itself was filled in with the four items it was missing
and rewritten so every row shows the exact quoted sentence and page
number the claim came from, or plainly says "Not reported" if it wasn't
found — a reader can now spot-check any claim against the source PDF
directly instead of trusting a paraphrase.

New badges ("chips") were added under the Rigor section for benchmarking
studies specifically: whether the comparison baseline was adequate,
whether train/dev/test data was kept properly separate, whether multiple
statistical comparisons were corrected for, whether an AI's output was
compared against a human baseline, and — only when a paper actually
reported one — whether its statistical power analysis was adequate.
Each page's footer now credits which AI model curated its trust-signal
analysis and when, and cites the TRIPOD-LLM guideline paper in full.
This whole treatment was piloted on one source page before being rolled
out to the rest.

## A second, unrelated multi-hour detour: files that looked fine but weren't

Getting a real, working preview of that pilot page in a browser turned
into its own investigation. A routine "clear some cache to free up space"
earlier that day had an unexpected side effect: macOS's iCloud Drive, set
to "Optimize Mac Storage," had quietly evicted the actual *contents* of
tens of thousands of project files (mostly deep inside `node_modules`,
the folder holding all the project's downloaded code libraries) to save
disk space — while leaving each file looking completely normal from the
outside (correct name, correct reported size). Only a disk-usage check
one level deeper revealed they held zero actual bytes until something
tried to read them, at which point they'd silently re-download.

This produced a chain of very different-looking failures — a build tool
that ran and exited instantly with no output, then one that started but
crashed on a totally unrelated piece of code, then a live server that
booted fine but crashed the instant a page tried to load its stylesheet
— that all traced back to the same root cause. The last and hardest one
to find was buried three dependencies deep: the page-styling tool's CSS
processor, when asked to resolve a file path, was being redirected by
the JavaScript bundler through an internal "browser-only" file path
mapping meant for a completely different use case, and that specific
path happened to be one of the evicted, empty files. Forcing Apple's
iCloud sync tool to fully re-download the affected folders, file by file,
finally cleared it and let the page render correctly.

## Grounding every rating in a quote, not just a curator's word

The "Quality Appraisal" section (renamed from "Critical Appraisal") used
to be five short paragraphs written by the curator explaining why a
paper's construct validity, internal validity, and so on were rated
green, yellow, or red. That was defensible but not checkable: a reader
had no way to confirm the rating without re-reading the whole paper
themselves. Every rating now cites the exact sentence, with a page
number, that justifies it, the same way the TRIPOD-LLM reporting table
already worked. The table also grew five new rows built specifically for
benchmarking papers, which the original five academic-methodology
domains didn't cover well: whether the comparison had a real baseline to
beat, whether training and test data were kept separate, whether
statistical comparisons were corrected for testing many things at once,
whether an AI's output was checked against a human doing the same task,
and whether the paper leaked data from its evaluation set into what a
model may have already seen during training. A sixth row, statistical
power, appears only on the one paper that actually reported a power
analysis, rather than showing an empty "not done" badge on every page.

The small colored badges at the top of each page that summarize these
ratings are now clickable: click one and the page jumps straight down to
the exact table row backing it up, so a skeptical reader never has to
hunt for where a claim comes from.

This was piloted on one source first, reviewed, then rolled out to the
other 26 using the same batched, quote-verified approach as the earlier
TRIPOD-LLM rollout. A mechanical check compared all roughly 1,000
quotes now on the site against the original paper PDFs and found no
fabrications, only a handful of PDF-text-extraction quirks (a footnote
number landing in the middle of a word, that kind of thing) that were
manually confirmed harmless.

## Trimming the chip clutter and standardizing how findings get titled

The row of small colored badges ("chips") at the top of every source and
evidence page had grown large enough to feel like a wall of noise rather
than a quick-scan summary. Two small, deliberately low-risk fixes: the
toggle that expands the full chip block used to spell out every category
it contained ("Show Quality Signals: Transparency · Openness · Rigor ·
Extensibility · Integrity"); that list was dropped from the visible label
(kept only for screen readers) and replaced with a plain "Show/Hide
Quality Signals" plus a small arrow icon that flips direction when
expanded. Separately, the Rigor section's "Design" row of chips was
reorganized into five clearly labeled sub-groups (Validity, Design,
Analyses, Reporting, Interpretation) instead of one long unlabeled run,
and the "Prompt Engineering" chip was pinned to always start a second row
within Design rather than landing wherever it happened to fit depending
on screen width.

A separate, unrelated task: looking across every research-question title
an AI first drafted versus the version a human curator actually kept
across all 27 papers revealed a consistent set of edits the curator kept
making by hand — preferred terms ("research reports" over vaguer
phrasing, "LLMs" as the standard short form), a consistent way of framing
a question in terms of *degree* rather than yes/no, and a recurring table
shape for questions about a capability with several dimensions. Those
patterns were written back into the extraction instructions so future
AI-drafted titles start closer to what the curator would keep, instead of
the curator re-deriving the same edits paper after paper.

## A single page to audit quality signals across every finding at once

Every quality signal (Transparency, the four Validity domains, and every
Rigor/Openness/Integrity chip) previously only existed scattered across
104 separate node pages — there was no way to see, say, "which findings
are missing a stated baseline" without opening pages one at a time. A new
Evidence Quality page gives one table with a row per Evidence node (77
total) and a column per signal, piloted first on a handful of rows before
scaling to the full set. Any of the roughly two dozen possible signal
columns can be added or removed, any column can be sorted, a text filter
narrows by evidence/source/pattern, and the whole view exports to
Markdown, CSV, or Excel. A later pass added a leftmost column for
cross-paper Evidence Patterns (so sorting clusters findings that feed the
same pattern together), made the Source column optional and hidden by
default, dropped all color-coding from the cell text in favor of plain
type, and combined what had been three separate export buttons into one
dropdown. The site-wide footer's build-provenance note (who curated it,
what method it follows, how the review layer works) moved to the bottom
of the About page, leaving the footer itself just a set of navigation
links.

## Catching up the graph view's filter to the full chip catalog

The graph view has always had a "Trust signals" filter dropdown for
narrowing the 232-node force-directed graph down to nodes matching a
particular Openness/Rigor/Transparency/Integrity signal, but it had been
built against an earlier, smaller version of the chip catalog and never
kept in sync as new chips were added over time (the Design/Analyses/
Reporting/Interpretation Rigor subrows, the Data/Code repository-liveness
checks). It was quietly missing more than a dozen of the signals now
shown on every source and evidence page. Brought it up to full parity
with the current chip catalog (the same one the Evidence Quality table's
column picker draws from): every rigor check that reads on a
addressed/partially-addressed/unresolved scale now gets its own three
filter checkboxes, statistical power and statistic-accuracy got their own
options, and the old single "Rigor" group was split into "Rigor —
Validity" so it reads consistently against the four new Rigor subrows
sitting alongside it. Verified in the browser that an obscure combination
("Data Repo Check: Live") narrows the graph to exactly the one matching
node.

## A targeted AI-writing recheck for the two papers with shaky numbers

Two of the 27 papers had already been flagged by an earlier, independent
check: their own reported statistics didn't add up when recomputed (a
confidence interval printed with its bounds reversed in one; an F1 score
that doesn't follow from the paper's own precision and recall in the
other). A finding like that raises a broader question worth checking:
is anything else about this paper's own writing suspect? Using Pangram
(a commercial AI-text-detection service), both papers' full PDF text was
run through an independent AI-generated-writing check — a narrow,
targeted follow-up on just the two flagged papers, not a sweep of the
whole corpus. Both came back clean: Pangram's own verdict was "fully
human-written" for one and "primarily human-written, with a small amount
of AI-assisted content" for the other. That result — a new "AI Writing
Check" signal — was wired in exactly like every other trust signal on the
site: a chip on the source and evidence pages, a row in the Quality
Appraisal table (this one citing the tool's own dashboard link rather
than a quote from the paper, since it's an external check on the prose
rather than something the paper itself says), a column in the Evidence
Quality table, and a checkbox in the graph view's filter. Pangram also
offers AI-generated-*image* detection, but that side of their product is
still a research preview with no stable, documented API, so it was left
for later.

## Separating "how trustworthy is this study" from "what is this finding about"

A collaborator's advisor pointed out a real conceptual gap: the graph
view's "Trust signals" filter lets someone ask "show me sources rated
high-risk on construct validity," but it can't answer a different,
more useful question — "across the whole corpus, what does the
evidence say about how good LLMs actually are at *doing* construct-
validity assessment?" Those sound alike but aren't: one rates a study's
own quality, the other asks about a capability being tested. Answering
the second question needed something that didn't exist yet: a tag on
every finding saying which evaluative task it's actually about (risk-
of-bias assessment, novelty assessment, citation-integrity checking,
and so on), independent of how rigorous that finding's source study is.

Also renamed "Statistical rigor" to "Statistical conclusion validity"
across every chip, dropdown, and Quality Appraisal table row (a more
precise, established term) while working through this.

Built a hierarchy of sixteen such evaluative-task categories, organized
under the site's existing five-Cs framework (Credibility, Clarity,
Creativity, Care, Connectivity) plus a sixth "Cross-cutting" bucket for
findings that are really about the evaluator's general behavior across
tasks (prompt sensitivity, cost, fine-tuning effects) rather than one
specific task. Every one of the 129 Evidence/Claim/Pattern nodes in the
corpus was then classified against that hierarchy — reusing each node's
own already quote-grounded finding statement as justification rather
than re-reading source PDFs — and the full classification was shown for
review before anything was written to a file. A new "Evaluative task"
filter on the graph view now lets someone check "risk-of-bias
assessment" and see exactly the handful of findings across the corpus
that are about that capability, regardless of which paper they came
from or how well-conducted that paper was.

## Splitting "Edit" into major and minor issues

The review form's five-state verdict vocabulary (correct / edit / wrong
/ missing / n/a) treated every edit the same, whether a reviewer fixed
a typo or rewrote a finding's core claim. Added two new, more specific
verdicts — "Edit: Major issues" and "Edit: Minor issues" — alongside
the original "Edit" rather than replacing it, so any reviews already
submitted with the plain "Edit" verdict keep rendering correctly. Both
new states get their own color (a stronger orange for major, a lighter
amber for minor) and show the same "proposed correction" text box the
original Edit verdict already had. Since the actual review database
lives in Supabase, separate from this repo, the schema file now also
carries the exact migration SQL needed to widen the database's
verdict check constraint on any already-provisioned instance.

## What's next

The "Contribute" page helps someone manually add a new note to the source vault.
Someone signs in with their GitHub account, fills out a short form, and the site
automatically creates a pull request (a formal "please merge my change" request)
on their behalf, the same way the reference site works.

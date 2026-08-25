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

## What's next

The "Contribute" page helps someone manually add a new note to the source vault.
Someone signs in with their GitHub account, fills out a short form, and the site
automatically creates a pull request (a formal "please merge my change" request)
on their behalf, the same way the reference site works.

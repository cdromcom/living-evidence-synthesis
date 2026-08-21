# How this site reviews its sources

Every SRC (source paper) page carries a set of automated, verifiable trust
and integrity signals, all computed from data already public — no paid
tools, no manual re-reading required to reproduce any single number here.
This document describes what's checked, where the data comes from, and —
just as importantly — what's deliberately *not* checked and why, since a
wrong signal is worse than a missing one.

**Contents:** [Guiding principle](#guiding-principle) ·
[What's on every source page](#whats-on-every-source-page) ·
[What we tried and deliberately did not ship](#what-we-tried-and-deliberately-did-not-ship) ·
[Data sources](#data-sources-all-freeopen-none-scraped-against-terms-of-service) ·
[Runbook for future passes](#runbook-adding-trust-signals-for-a-new-or-updated-source) ·
[Where this points next](#where-this-naturally-points-next)

## Guiding principle

**Every signal here was verified against real data before being published.**
Several checks were built, tested, found to produce false positives on this
specific corpus, and deliberately not shipped — see
["What we tried and deliberately did not ship"](#what-we-tried-and-deliberately-did-not-ship)
below. When a check can't be run reliably (data missing, a
publisher blocks automated access, a naive extraction turns out ambiguous),
the honest answer is "not applicable" or "not checked," never a guess. This
is the same discipline GRIM/GRIMMER-style forensic tools require of
themselves: the arithmetic is only as trustworthy as the data pairing that
feeds it.

## What's on every source page

### Citation (`components/SourceCitation.tsx`, `lib/apa.ts`)
A full APA 7th-edition reference — authors, year, sentence-cased title
(acronyms like GPT-4/LLM/CONSORT preserved, not mangled), italicized
journal + volume, DOI link — built from CrossRef/DataCite bibliographic
data pulled per source, not hand-typed.

### Transparency — COS TOP Guidelines (`components/TopBadges.tsx`)
Four of the [TOP Guidelines](https://www.cos.io/initiatives/top-guidelines)
standards, extracted from each source's own TRIPOD-LLM reporting table
(items 14c/14d/14e/14f, already vault content): **Data Transparency**,
**Analytic Code Transparency**, **Study Protocol**, **Study Registration**.
Each gets TOP's own Level 1 (Disclosed) / Level 2 (Shared and Cited)
language — never Level 3 (Certified), since that requires independent
verification we haven't done. Badge artwork for Data/Code/Registration
borrows COS's actual Open Science Badges (Open Data / Open Materials /
Preregistered — CC BY 4.0, confirmed via cos.io's own license footer,
downloaded from their OSF file store); shown full-color only at Level 2,
desaturated otherwise, so nothing implies a badge was earned when it wasn't.

### Risk of bias (`components/TopBadges.tsx`)
Construct validity, internal validity, external validity, statistical
rigor, and reproducibility — the five domains of each source's own
Critical Appraisal table (🟢/🟡/🔴), surfaced with original icon glyphs
(no open-licensed icon set exists for these specifically; checked —
Cochrane's RoB2 iconography is CC BY-NC-ND, which forbids derivatives).

### Study design rigor (NIH/NINDS icons)
Sample-size estimation and exploratory-vs-confirmatory framing, using the
real NIH/NINDS rigor icon set. Not extracted from a structured field —
grounded in direct textual evidence checked across the whole corpus before
tagging anything: every "sample size"/"power analysis" mention in all 27
sources is a caveat about its *absence*, and none of the 27 are registered,
protocolled, or claim a confirmatory pre-specified hypothesis.

### Research integrity
Ethical approval, funding disclosure, conflicts-of-interest disclosure —
same TRIPOD-LLM table (items 13, 14a, 14b), original glyphs (checked for
precedent first: ICMJE's COI material is a disclosure form, not an icon
convention).

### Source credibility (`components/SourceCredibility.tsx`)
- **DOI resolution** — every source's real DOI, matched against the
  citekey and verified by comparing the resolved title/authors against
  what we already knew about the paper's content (not just trusted a
  search API's top hit).
- **Critique status** — checked live against Crossref's `update-to`
  relation (Crossref has owned the Retraction Watch database since Sept
  2023) or DataCite for arXiv preprints, which has no equivalent registry
  (marked `not-registered`, not falsely implied clean).
- **Author track record** — INSPECT-SR item 1.3 ("do other studies by the
  research team highlight causes for concern"), checked via each author's
  ORCID publication history on Crossref. Only proceeds when an ORCID is on
  record — never plain name search, since a same-named different person's
  retraction misattributed to the real author would be exactly the kind of
  false claim this whole feature is trying to avoid.
- **PubPeer comment count** — a live count (no comment text, no commenter
  identities), via the same endpoint PubPeer's own official browser
  extension uses (`POST pubpeer.com/v3/publications`, read from their
  open-source extension code). One real finding this surfaced: the Roberts
  et al. paper has a PubPeer comment on record.
- **Publication type, DOAJ listing, self-citation rate** — publication
  type from Crossref/DataCite's own type field; DOAJ status from their free
  public API (journal legitimacy signal for open-access venues); self-
  citation rate computed from Crossref's own reference-list metadata where
  a publisher provides author info per reference (coverage varies —
  explicitly marked "not-assessable" when a publisher's references are
  bare DOIs).
- **Citation count and predatory-publisher screening** — via
  [`referencecheck`](https://github.com/giladfeldman/referencecheck)
  (Gilad Feldman, MIT, pinned to v0.1.1): citation counts from OpenCitations
  for non-arXiv sources, and publisher names checked against Beall's List
  of predatory publishers. Both spot-verified before use — correctly
  flagged a known predatory publisher (OMICS International) and cleared a
  known-legitimate one (Elsevier) in testing. Citation counts are
  deliberately *not* shown for arXiv-hosted sources: OpenCitations doesn't
  reliably index the arXiv DOI namespace (even "Attention Is All You Need"
  returns null there), so a low/zero count would misrepresent real
  citation activity rather than reflect it.
- **Peer review status** — checked directly against each source's actual
  landing page (or, where publishers blocked automated access, marked
  "not independently verified" rather than guessed). Preprints are marked
  not-applicable by definition.
- **Altmetric attention badge** — the free embeddable widget (no API key;
  their REST API now requires one as of Nov 2025, the embed badge doesn't).
  This tracks attention/engagement volume, not sentiment — Altmetric
  doesn't actually offer a sentiment feature, despite the name sounding
  like it might.

### Forensic-metascience checks on individual evidence claims
Run against the exact numbers quoted in each EVD (evidence) node, not the
source as a whole:
- **F1 consistency** — `F1 = 2PR/(P+R)`, flagged when a claim states
  precision, recall, and F1 together and they don't reconcile (with a
  caveat that macro/micro-averaged multi-class F1 can legitimately diverge
  from the plain formula).
- **Cohen's κ bounds** — flags any κ reported outside the mathematically
  valid [-1, 1] range.
- **Confidence-interval consistency** — bounds correctly ordered, and the
  point estimate actually falls inside its own reported interval. Caught a
  real, previously-manually-flagged error this way: the Roberts et al.
  paper prints a 95% CI as "(0.62%, 0.37%)" — lower bound above the upper
  bound.
- **Percentage-of-total closure** — where a claim breaks a total into
  subcategories, verifies the parts sum to the stated whole.
- **Trend monotonicity** — for "rose/dropped from X to Y" claims, verifies
  the stated direction matches the actual comparison.
- **Cross-node corroboration** — whether a source's own narrative summary
  restates at least one number from each evidence claim it cites (reported
  as a corroboration rate, not a contradiction hunter — paraphrasing
  without repeating a number is normal, not an error).
- **Model-name spelling consistency** — checked against the *full paper
  PDF* text (not just our curated summary) for 20 of 27 sources where a
  real, verified PDF was available locally (up from 8, once more PDFs
  synced and the arXiv-hosted sources — reliably fetchable straight from
  arxiv.org regardless of Zotero state — were pulled directly). Groups
  every GPT-4/Claude/Gemini/Llama mention by normalized form and flags a
  paper using 2+ distinct spellings for the same model. A naive first pass
  of this extension flagged 11 of 12 newly-checked papers as
  "inconsistent" — almost all false positives from citation-list titles,
  software/URL identifiers, and (in one case) genuinely *different* model
  variants being mistaken for spelling variants of the same one (e.g.
  "Llama 3.1-70B" vs. "Llama3-8B"). Hand-verifying each flag against its
  real context brought that down to 1 genuine inconsistency across all 20
  sources checked — Akyon et al., which alternates "GPT 4-0613" /
  "GPT-4-0613" / "ChatGPT 4-0613" for the same model throughout their
  results section.
- **statcheck** (p-value/test-statistic recomputation) — checked across
  the whole corpus; zero results were reported in a recomputable APA-style
  NHST format, so this is uniformly marked "not applicable" per source
  rather than silently omitted.

## What we tried and deliberately did not ship

Publishing an unreliable check is worse than publishing none — a false
"red flag" misrepresents a real, named paper. Three checks were built,
tested against real corpus data, and rejected on that basis:

- **GRIM** (does a reported percentage match some integer/N?) — a naive
  nearest-number pairing produced a clear false positive: "18.02% (552)"
  in one source's table means *552 is the count 18.02% of 3063
  represents*, not the denominator. A regex can't reliably tell these
  apart without reading the sentence.
- **"Too clean" / terminal-digit roundness** — several sources came back
  "100% round percentages," which looked like a red flag until checked:
  their underlying evaluation subsets are N=10 or N=20, where round
  percentages (100%, 57%, 70%) are a mathematical near-certainty, not a
  fabrication signal. Classic forensic techniques built for large-sample
  survey/clinical data have real, demonstrated limits on a small-N
  ML-benchmark corpus like this one.
- **GRIMMER/`strait`-style mean+SD+scale-bounds checks** (explored after
  the R packages `scrutiny` and `tides`/`strait` were suggested) — exactly
  one mean+SD candidate exists in the whole 77-node evidence corpus. Pulled
  the actual paper (a public arXiv PDF) to get the scale bounds needed to
  run the check, and the paper never states them. Not shipped rather than
  assumed.

Also explicitly out of scope, with reasons on record:
- **`referencecheck`'s OpenRetractions-based retraction check** — its
  primary data source (`api.openretractions.com`) doesn't resolve from our
  build environment, so it silently falls back to the same Crossref
  retraction data we'd already manually verified for `critiqueStatus`.
  Re-running it would add no new signal, just a second label for the same
  underlying fact — not shipped as a separate check for that reason.
- **Image/text-duplication forensics** (the single most common real
  retraction-case finding, per Elisabeth Bik's work) — no free API exists;
  the available tools (Proofig, ImageTwin) are paid B2B products.
- **PubPeer comment *content*** — only a live count is shown, never the
  comment text or commenter identities. PubPeer's platform has its own
  legal/moderation structure built for hosting serious misconduct
  allegations; republishing that content on a different site would inherit
  that exposure without the structure.
- **AI-generated-text detection on the papers' own prose** — explicitly
  declined. These detectors have a documented, specific failure mode: they
  flag non-native-English-speaker writing as "AI-generated" at
  disproportionate rates (Liang et al. 2023), and this corpus's authors are
  a genuinely international group. OpenAI shut down its own AI-text
  classifier in 2023 citing low accuracy; no major publisher uses these
  tools for exactly this reason.
- **Research Signals** (research-signals.com) — a commercial
  publisher-integration platform; no public or free-tier API, would
  require a business relationship to access.
- **Section-level (title/abstract/intro/results/discussion) consistency
  checking** — tested and found unreliable: one source's own methodology
  table uses "Methods"/"Results"/"Discussion" as plain row labels sitting
  right next to its real (ALL-CAPS) section headers, which a naive header
  matcher would confuse. This is a reliability problem independent of PDF
  coverage, so it stays unshipped even now that coverage has improved
  (below).

## Data sources, all free/open, none scraped against terms of service

Crossref REST API · DataCite REST API · DOAJ search API · ORCID (via
Crossref author records) · OpenCitations (via `referencecheck`) · Beall's
List of predatory publishers (bundled with `referencecheck`) · Center for
Open Science's Open Science Badges (CC BY 4.0) · PubPeer's own
public-extension API endpoint · Altmetric's free embeddable badge widget ·
each source's own vault-curated TRIPOD-LLM and Critical Appraisal tables.

## Runbook: adding trust signals for a new or updated source

This is the reusable procedure for extending trust-signal coverage —
whether new sources get added to `vault/source/`, or previously-missing
PDFs finally sync in. It's written so a future session can follow it
without re-deriving the method from scratch.

**Current priority**: DOI-based checks (below) over PDF-text-based checks.
Model-name spelling consistency is *deprioritized* per explicit direction —
it's a minor signal relative to the others and not worth spending a session
on unless separately requested. Don't restart it unprompted.

### 1. DOI-based checks — the default, do these first

These need only a DOI, not a PDF, so they're the highest-value, lowest-cost
pass for any source. All are already wired into `scripts/build-graph.mjs`
(passthrough) and `components/SourceCredibility.tsx` (rendering) — adding
a new field here means extending both.

- **Find the DOI** if missing: `curl -s "https://api.crossref.org/works?query.bibliographic=<title words>&rows=3"` and manually confirm the returned title is an exact match before trusting it. Conference-proceedings and ACL-Anthology-style papers often have a real DOI that's easy to miss on a first pass (this is how Zhou et al.'s DOI was found — a plain title search, nothing fancier).
- **`referencecheck` package** (`node_modules/referencecheck`, MIT, pinned to `github:giladfeldman/referencecheck#v0.1.1`) provides:
  - `getCitationCount(doi)` — OpenCitations. **Do not trust it blindly**: it doesn't reliably index arXiv DOIs at all (confirmed: even "Attention Is All You Need" returns `null`), and has been seen to undercount non-arXiv DOIs too (Zhou et al.: OpenCitations said 0, Crossref's own `is-referenced-by-count` said 26). When they disagree, prefer Crossref's own count and set `citationCountSource` to say so explicitly — the UI renders whatever string is in that field, so it's always accurate to the reader.
  - `checkBeallsList(publisher)` — predatory-journal screening. Needs the publisher name, pulled from `crossrefGet(...)`'s `data.publisher` field (or DataCite for arXiv — see below).
  - `checkRetraction(doi)` — **skip this one**. Its primary data source (`api.openretractions.com`) doesn't resolve from this environment and it silently falls back to the same Crossref data we already use for `critiqueStatus`. Re-running it adds no new signal.
- **Author track record** (`authorTrackRecord`): only proceeds when an author's ORCID is on record (via that paper's own Crossref author metadata). If Crossref 404s the paper (arXiv DOIs always do — they're DataCite-registered, not Crossref), check whether DataCite carries ORCIDs instead: `curl -s "https://api.datacite.org/dois/<doi>" | jq '.data.attributes.creators'` — as of this session it doesn't (every arXiv source tested has empty `nameIdentifiers`). When no ORCID is findable anywhere, set `authorTrackRecord: not-checked` explicitly — don't leave the field absent. An absent field silently omits the badge; an explicit `not-checked` value renders it and tells the reader why.
- **DOAJ, self-citation rate, publication type, peer-review status, APA citation fields**: same methodology as documented earlier in this file — DOAJ's free API, Crossref reference-list author metadata, Crossref/DataCite type field, direct landing-page fetch, Crossref bibliographic data respectively.

### 2. Finding local PDFs for the PDF-dependent checks

PDFs live in `~/Zotero/storage/<item-key>/`, but the Zotero desktop app
locks `zotero.sqlite` while running, so always query a copy:

```bash
python3 -c "
import shutil
shutil.copyfile('$HOME/Zotero/zotero.sqlite', '/tmp/zotero_ro.sqlite')
"
```

Match a source's citekey (e.g. `wrightsonGPTRCTsUsing2025`) to a Zotero
item by **surname (first-listed creator) + publication year + title-word
overlap — never surname+year alone**. A first pass this session that
matched on surname+year only produced real false positives (two different
citekeys both "matched" the same multi-author paper because it happened to
have co-authors with both surnames). Require the paper's Crossref/Zotero
title to share 2+ non-stopword words with the citekey's own title fragment
before trusting a match, and iterate *all* candidate items for a given
surname+year (Zotero often holds several duplicate entries for the same
paper across different libraries/collections) rather than stopping at the
first one — the correct match's downloaded attachment may be on a
different duplicate than the first one found.

For arXiv-hosted sources (`doi` contains `arXiv`), skip Zotero entirely and
fetch directly — it's more reliable and doesn't depend on any sync state:

```bash
curl -s -L -o ".cache/source-pdfs/<citekey>.pdf" "https://arxiv.org/pdf/<arxiv-id>.pdf"
```

**Always verify** the downloaded/located PDF actually matches the source
before using it for anything: extract the first page (`lit parse <path>
--format text --no-ocr | head -20`, see the `effective-liteparse` skill)
and confirm the title/DOI watermark matches what's in the vault frontmatter.
Never assume a filename match is correct.

### 3. Corpus-wide completeness audit

Before wrapping up a pass, check for silent gaps — a field that's present
on most sources but missing on a few, usually because an earlier pass
skipped a source without a clear reason (like Zhou's missing DOI, found
this way):

```bash
python3 - <<'PYEOF'
import os, re
FIELDS = ["doi", "predatoryPublisherFlag", "critiqueStatus", "authorTrackRecord",
          "selfCitationRate", "doajListed", "pubpeerCommentCount", "apaTitle", "peerReviewStatus"]
for f in sorted(os.listdir("vault/source")):
    if not f.endswith(".md"): continue
    fm = open(f"vault/source/{f}").read().split("---")[1]
    missing = [field for field in FIELDS if not re.search(rf"^{field}:", fm, re.M)]
    if missing:
        print(f[1:-3], missing)
PYEOF
```

`citationCount` is deliberately excluded from that list — its absence on
arXiv sources is intentional, not a gap (see above). Add fields to the
list as new trust signals get built.

### 4. After any vault edit

1. Validate YAML across all 27 files before moving on — a single misplaced
   list item breaks the whole frontmatter block silently:
   `python3 -c "import glob, yaml; [yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('vault/source/*.md')]"`
2. `node scripts/build-graph.mjs` to regenerate `lib/graph-data.generated.json`.
3. Spot-check the rendered page for at least one changed source (`curl -s
   http://localhost:3010/nodes/<id>` and grep for the new field's expected
   text — React splits text into multiple child nodes in the server-rendered
   payload, so search for a distinctive substring, not the full sentence).
4. Commit with a message that states what was verified and how, following
   this file's own standard: what shipped, what was checked before
   trusting it, what (if anything) was found unreliable and skipped.

## Where this naturally points next

Everything above is retrospective document analysis. The one thing
explicitly never claimed — TOP's own Level 3 "Certified" — would mean
picking sources with real public code+data and actually re-running their
pipeline to confirm the numbers match. That's full reproducibility
verification, a substantially larger and more valuable project, and a
deliberately separate piece of future work rather than something folded
into the checks above.

import Link from "next/link";
import { getForensicSignalsForSource, getStatcheckStatus, type GraphNode } from "@/lib/data";
import AltmetricBadge from "./AltmetricBadge";

type CritiqueStatus = "none" | "not-registered" | "correction" | "expression-of-concern" | "retraction";

const CRITIQUE_LABELS: Record<CritiqueStatus, string> = {
  none: "No corrections or retractions on record",
  "not-registered": "No retraction registry available for this source",
  correction: "Correction on record",
  "expression-of-concern": "Editorial expression of concern on record",
  retraction: "Retraction on record",
};

const CRITIQUE_TONE: Record<CritiqueStatus, string> = {
  none: "border-emerald-600 text-emerald-700",
  "not-registered": "border-zinc-300 text-muted-ink",
  correction: "border-amber-500 text-amber-700",
  "expression-of-concern": "border-amber-600 text-amber-800",
  retraction: "border-red-600 text-red-700",
};

// INSPECT-SR 1.3: "Do other studies by the research team highlight causes
// for concern?" — checked via each author's ORCID publication history
// (CrossRef), never plain name search: a same-named different person's
// retraction misattributed to our actual author would be exactly the kind
// of false claim this whole feature is trying to avoid.
type AuthorTrackRecord = "clean" | "flagged" | "not-checked";

const TRACK_LABELS: Record<AuthorTrackRecord, string> = {
  clean: "No flagged studies found among this author's other work (ORCID-checked)",
  flagged: "An author has another flagged study on record",
  "not-checked": "Not checked — no author ORCID on record for this source",
};

const TRACK_TONE: Record<AuthorTrackRecord, string> = {
  clean: "border-emerald-600 text-emerald-700",
  flagged: "border-red-600 text-red-700",
  "not-checked": "border-zinc-300 text-muted-ink",
};

function TrackRecordGlyph({ status }: { status: AuthorTrackRecord }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  return (
    <svg {...common}>
      <circle cx="9" cy="8" r="3.2" />
      <path d="M3.5 20c0-3.5 2.5-6 5.5-6s5.5 2.5 5.5 6" />
      {status === "flagged" ? <path d="M18 5v5M18 13v.5" /> : <path d="M16.5 8.5l1.5 1.5 3-3" />}
    </svg>
  );
}

// Original glyphs — no established open-licensed icon convention found for
// "editorial notice status" specifically.
function CritiqueGlyph({ status }: { status: CritiqueStatus }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  const doc = <path d="M6 3.5h9l3 3V20a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z" />;
  switch (status) {
    case "none":
      return (
        <svg {...common}>
          {doc}
          <path d="M9 12.5l2 2 4-4.5" />
        </svg>
      );
    case "correction":
      return (
        <svg {...common}>
          {doc}
          <path d="M9.5 16.5 15 11l-1.5-1.5-5.5 5.5-.5 2Z" />
        </svg>
      );
    case "expression-of-concern":
      return (
        <svg {...common}>
          {doc}
          <path d="M12 9v4.5" />
          <path d="M12 16.5v.5" />
        </svg>
      );
    case "retraction":
      return (
        <svg {...common}>
          {doc}
          <path d="M9 9l6 7M15 9l-6 7" />
        </svg>
      );
    case "not-registered":
      return (
        <svg {...common}>
          {doc}
          <path d="M9 12.5h6" />
        </svg>
      );
  }
}

type PubType =
  | "journal-article"
  | "conference-proceeding"
  | "preprint"
  | "thesis"
  | "dissertation"
  | "blog-post"
  | "micropublication"
  | "nanopublication"
  | "report"
  | "other";

const PUB_TYPE_LABELS: Record<PubType, string> = {
  "journal-article": "Journal article",
  "conference-proceeding": "Conference proceeding",
  preprint: "Preprint",
  thesis: "Thesis",
  dissertation: "Dissertation",
  "blog-post": "Blog post",
  micropublication: "Micropublication",
  nanopublication: "Nanopublication",
  report: "Report",
  other: "Other",
};

function PubTypeGlyph({ pubType }: { pubType: PubType }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (pubType) {
    case "journal-article":
      return (
        <svg {...common}>
          <path d="M4 4.5c3-1 6-1 8 0v15c-2-1-5-1-8 0Z" />
          <path d="M20 4.5c-3-1-6-1-8 0v15c2-1 5-1 8 0Z" />
        </svg>
      );
    case "conference-proceeding":
      return (
        <svg {...common}>
          <rect x="3" y="5" width="18" height="12" rx="1.5" />
          <path d="M8 21h8M12 17v4" />
        </svg>
      );
    case "preprint":
      return (
        <svg {...common}>
          <path d="M6 3.5h9l3 3V20a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z" />
          <path d="M9 13.5l2.5 2.5L16 11" strokeDasharray="1.5 2" />
        </svg>
      );
    case "thesis":
    case "dissertation":
      return (
        <svg {...common}>
          <path d="M2 9 12 4l10 5-10 5Z" />
          <path d="M6 11.5V17c2 1.5 10 1.5 12 0v-5.5" />
        </svg>
      );
    case "blog-post":
      return (
        <svg {...common}>
          <path d="M4 5h16v11H9l-4 4V5Z" />
          <path d="M8 9h8M8 12.5h5" />
        </svg>
      );
    case "micropublication":
    case "nanopublication":
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="2" />
          <ellipse cx="12" cy="12" rx="9" ry="4" />
          <ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(60 12 12)" />
        </svg>
      );
    case "report":
    case "other":
      return (
        <svg {...common}>
          <rect x="5" y="3.5" width="14" height="17" rx="1.5" />
          <path d="M8.5 8.5h7M8.5 12h7M8.5 15.5h4" />
        </svg>
      );
  }
}

/** DOI link, critique/retraction status, PubPeer link-out, and author list for a source node. */
export default function SourceCredibility({ node }: { node: GraphNode }) {
  const doi = node.extras.doi as string | undefined;
  const sourceUrl = node.extras.sourceUrl as string | undefined;
  const critiqueStatus = node.extras.critiqueStatus as CritiqueStatus | undefined;
  const critiqueNote = node.extras.critiqueNote as string | undefined;
  const authors = node.extras.authors as string[] | undefined;
  const trackRecord = node.extras.authorTrackRecord as AuthorTrackRecord | undefined;
  const trackRecordChecked = node.extras.authorTrackRecordChecked as string | undefined;
  const trackRecordNote = node.extras.authorTrackRecordNote as string | undefined;
  const pubType = node.extras.pubType as PubType | undefined;
  const doajListed = node.extras.doajListed as boolean | "not-applicable" | undefined;
  const selfCitationRate = node.extras.selfCitationRate as number | "not-assessable" | undefined;
  const selfCitationChecked = node.extras.selfCitationChecked as string | undefined;
  const pubpeerCommentCount = node.extras.pubpeerCommentCount as number | undefined;
  const pubpeerUrl = node.extras.pubpeerUrl as string | undefined;
  const citationCount = node.extras.citationCount as number | undefined;
  const predatoryPublisherFlag = node.extras.predatoryPublisherFlag as boolean | undefined;
  const predatoryPublisherNote = node.extras.predatoryPublisherNote as string | undefined;
  const forensicSignals = getForensicSignalsForSource(node.id);
  const statcheckStatus = getStatcheckStatus(node);
  const forensicFlagged = forensicSignals.filter((s) =>
    ["discrepancy", "out-of-bounds", "bounds-reversed", "point-outside-interval", "violated"].includes(s.result)
  );
  const crossNodeChecked = node.extras.crossNodeChecked as number | undefined;
  const crossNodeCorroborated = node.extras.crossNodeCorroborated as number | undefined;
  const nameConsistency = node.extras.nameConsistency as "consistent" | "inconsistent-formatting" | undefined;
  const nameConsistencyNote = node.extras.nameConsistencyNote as string | undefined;

  if (!doi && !sourceUrl && !critiqueStatus) return null;

  const externalHref = doi ? `https://doi.org/${doi}` : sourceUrl;
  const pubpeerHref = pubpeerUrl || (doi ? `https://pubpeer.com/search?q=${encodeURIComponent(doi)}` : null);
  const pubpeerLabel =
    pubpeerCommentCount && pubpeerCommentCount > 0
      ? `${pubpeerCommentCount} PubPeer comment${pubpeerCommentCount === 1 ? "" : "s"} ↗`
      : "No PubPeer comments found";

  return (
    <div className="mt-3 rounded-md border border-border bg-card p-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs">
        {externalHref && (
          <a
            href={externalHref}
            target="_blank"
            rel="noopener noreferrer"
            className="mono text-forest hover:underline"
          >
            {doi ? `doi.org/${doi}` : "Source ↗"}
          </a>
        )}
        {doi && <AltmetricBadge doi={doi} />}
        {pubType && (
          <span
            title={`Publication type: ${PUB_TYPE_LABELS[pubType]}`}
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-0.5 text-ink/70"
          >
            <PubTypeGlyph pubType={pubType} />
            {PUB_TYPE_LABELS[pubType]}
          </span>
        )}
        {doajListed === true && (
          <span
            title="Journal is indexed in the Directory of Open Access Journals (DOAJ) — a positive legitimacy signal for open-access venues"
            className="inline-flex items-center gap-1.5 rounded-full border border-emerald-600 bg-card px-2 py-0.5 text-emerald-700"
          >
            DOAJ-listed
          </span>
        )}
        {doajListed === false && (
          <span
            title="Journal was not found in the Directory of Open Access Journals — not necessarily a red flag (many reputable subscription/hybrid journals aren't DOAJ members), but worth a second look for open-access-only venues"
            className="inline-flex items-center gap-1.5 rounded-full border border-zinc-300 bg-card px-2 py-0.5 text-muted-ink"
          >
            Not DOAJ-listed
          </span>
        )}
        {typeof citationCount === "number" && (
          <span
            title="Citation count from OpenCitations (COCI) — an open, free citation index; coverage can lag behind Google Scholar or Semantic Scholar"
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-0.5 text-ink/70"
          >
            {citationCount} citation{citationCount === 1 ? "" : "s"}
          </span>
        )}
        {predatoryPublisherFlag === true && (
          <span
            title="Publisher appears on Beall's List of predatory publishers — treat this source's claims with extra scrutiny"
            className="inline-flex items-center gap-1.5 rounded-full border border-red-600 bg-card px-2 py-0.5 font-semibold text-red-700"
          >
            Predatory publisher flagged
          </span>
        )}
        {predatoryPublisherFlag === false && !predatoryPublisherNote && (
          <span
            title="Publisher not found on Beall's List of predatory publishers"
            className="inline-flex items-center gap-1.5 rounded-full border border-emerald-600 bg-card px-2 py-0.5 text-emerald-700"
          >
            Publisher checked, not predatory
          </span>
        )}
        {critiqueStatus && (
          <span
            title={critiqueNote || CRITIQUE_LABELS[critiqueStatus]}
            className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-0.5 ${CRITIQUE_TONE[critiqueStatus]}`}
          >
            <CritiqueGlyph status={critiqueStatus} />
            {CRITIQUE_LABELS[critiqueStatus]}
          </span>
        )}
        {trackRecord && (
          <span
            title={`${TRACK_LABELS[trackRecord]}${trackRecordChecked ? ` (checked ${trackRecordChecked})` : ""}${trackRecordNote ? `: ${trackRecordNote}` : ""}`}
            className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-0.5 ${TRACK_TONE[trackRecord]}`}
          >
            <TrackRecordGlyph status={trackRecord} />
            Author track record
          </span>
        )}
        {pubpeerHref && (
          <a
            href={pubpeerHref}
            target="_blank"
            rel="noopener noreferrer"
            className={
              pubpeerCommentCount && pubpeerCommentCount > 0
                ? "font-semibold text-amber-700 hover:underline"
                : "text-muted-ink hover:text-forest hover:underline"
            }
          >
            {pubpeerLabel}
          </a>
        )}
      </div>
      {authors && authors.length > 0 && (
        <p className="mt-2 text-xs text-muted-ink">
          <span className="font-semibold text-ink/70">Authors: </span>
          {authors.join(" · ")}
        </p>
      )}
      {typeof selfCitationRate === "number" && (
        <p className="mt-1 text-xs text-muted-ink">
          <span className="font-semibold text-ink/70">Self-citation rate: </span>
          {(selfCitationRate * 100).toFixed(0)}% of assessable references cite the paper's own
          authors{selfCitationChecked ? ` (${selfCitationChecked})` : ""}
        </p>
      )}
      {(forensicSignals.length > 0 || statcheckStatus) && (
        <div className="mt-3 border-t border-border pt-2">
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Forensic checks <span className="font-normal normal-case">(on this source's evidence claims)</span>
          </p>
          <p className="mt-1 text-xs text-muted-ink">
            {forensicSignals.length} numeric consistency check{forensicSignals.length === 1 ? "" : "s"} run (F1 =
            2PR/(P+R), Cohen&apos;s κ bounds, CI ordering/containment, percentage-of-total closure, trend
            monotonicity) —{" "}
            {forensicFlagged.length === 0 ? (
              <span className="text-emerald-700">none flagged</span>
            ) : (
              <span className="font-semibold text-amber-700">{forensicFlagged.length} flagged, see below</span>
            )}
            . statcheck (p-value/test-statistic recomputation): not applicable — no results in this corpus were
            reported in a recomputable APA-style format.
          </p>
          {typeof crossNodeChecked === "number" && crossNodeChecked > 0 && (
            <p className="mt-1 text-xs text-muted-ink">
              <span className="font-semibold text-ink/70">Cross-node corroboration: </span>
              {crossNodeCorroborated} of {crossNodeChecked} evidence claims restate a matching number in this
              source&apos;s own narrative summary (the rest may simply be paraphrased, not necessarily
              inconsistent).
            </p>
          )}
          {nameConsistency && (
            <p
              className="mt-1 text-xs text-muted-ink"
              title={nameConsistencyNote || undefined}
            >
              <span className="font-semibold text-ink/70">Model-name formatting: </span>
              {nameConsistency === "consistent" ? (
                <span className="text-emerald-700">consistent throughout the full text</span>
              ) : (
                <span className="font-semibold text-amber-700">
                  inconsistent spellings found for the same model{nameConsistencyNote ? ` (${nameConsistencyNote})` : ""}
                </span>
              )}{" "}
              — checked against the full paper PDF, not just this source&apos;s curated summary.
            </p>
          )}
          {forensicFlagged.length > 0 && (
            <ul className="mt-1.5 space-y-1">
              {forensicFlagged.map((s, i) => (
                <li key={i} className="text-xs">
                  <Link href={`/nodes/${s.evdId}`} className="text-forest hover:underline">
                    {s.evdTitle}
                  </Link>{" "}
                  <span className="text-muted-ink">
                    —{" "}
                    {s.kind === "f1-check"
                      ? "reported F1 doesn't match the harmonic-mean formula (can also happen legitimately with macro/micro-averaged multi-class F1 — not necessarily an error)"
                      : s.kind === "kappa-check"
                        ? "Cohen's κ value falls outside the mathematically valid [-1, 1] range"
                        : s.kind === "closure-check"
                          ? "subgroup counts/percentages don't sum to the stated total"
                          : s.kind === "monotonicity-check"
                            ? "reported direction (rose/fell) doesn't match the stated before/after values"
                            : s.result === "bounds-reversed"
                              ? "confidence interval's lower bound exceeds its upper bound"
                              : "point estimate falls outside its own reported confidence interval"}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
      <p className="mt-2 text-[0.625rem] text-muted-ink">
        Retraction/correction status checked against Crossref (which now includes the Retraction
        Watch database) or DataCite for arXiv preprints, at curation time — not a live guarantee;
        verify independently before relying on it.
      </p>
    </div>
  );
}

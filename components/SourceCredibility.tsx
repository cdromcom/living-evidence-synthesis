import type { GraphNode } from "@/lib/data";
import AltmetricBadge from "./AltmetricBadge";

// Original glyph — no official PubPeer mark is licensed for reuse here.
function PubPeerGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="M15.5 15.5 21 21" />
    </svg>
  );
}

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

const CRITIQUE_SHORT_LABELS: Record<CritiqueStatus, string> = {
  none: "No corrections/retractions",
  "not-registered": "No retraction registry",
  correction: "Correction on record",
  "expression-of-concern": "Expression of concern",
  retraction: "Retraction on record",
};

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

/** Altmetric badge, critique/retraction status, and PubPeer link-out for a source node. */
export default function SourceCredibility({ node }: { node: GraphNode }) {
  const doi = node.extras.doi as string | undefined;
  const sourceUrl = node.extras.sourceUrl as string | undefined;
  const critiqueStatus = node.extras.critiqueStatus as CritiqueStatus | undefined;
  const critiqueNote = node.extras.critiqueNote as string | undefined;
  const pubpeerCommentCount = node.extras.pubpeerCommentCount as number | undefined;
  const pubpeerUrl = node.extras.pubpeerUrl as string | undefined;
  const peerReviewStatus = node.extras.peerReviewStatus as
    | "not-applicable"
    | "not-found"
    | "not-checked"
    | undefined;
  const peerReviewNote = node.extras.peerReviewNote as string | undefined;
  const peerReviewUrl = node.extras.peerReviewUrl as string | undefined;

  if (!doi && !sourceUrl && !critiqueStatus) return null;

  const pubpeerHref = pubpeerUrl || (doi ? `https://pubpeer.com/search?q=${encodeURIComponent(doi)}` : null);
  const pubpeerLabel =
    pubpeerCommentCount && pubpeerCommentCount > 0
      ? `${pubpeerCommentCount} PubPeer comment${pubpeerCommentCount === 1 ? "" : "s"} ↗`
      : "No PubPeer comments found";
  const PEER_REVIEW_LABEL: Record<string, string> = {
    "not-applicable": "NA — preprint, not peer reviewed",
    "not-found": "NA — checked, no open peer review reports found",
    "not-checked": "NA — not independently verified (publisher blocked automated access)",
  };

  return (
    <div className="mt-3 rounded-md border border-border bg-card p-3">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs">
        {doi && <AltmetricBadge doi={doi} />}
        {critiqueStatus && (
          <span
            title={critiqueNote ? `${CRITIQUE_LABELS[critiqueStatus]}: ${critiqueNote}` : CRITIQUE_LABELS[critiqueStatus]}
            className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-0.5 ${CRITIQUE_TONE[critiqueStatus]}`}
          >
            <CritiqueGlyph status={critiqueStatus} />
            {CRITIQUE_SHORT_LABELS[critiqueStatus]}
          </span>
        )}
        {pubpeerHref && (
          <a
            href={pubpeerHref}
            target="_blank"
            rel="noopener noreferrer"
            title="View on PubPeer"
            className={
              pubpeerCommentCount && pubpeerCommentCount > 0
                ? "inline-flex items-center gap-1.5 rounded-full border border-amber-500 bg-card px-2 py-0.5 font-semibold text-amber-700 hover:underline"
                : "inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-0.5 text-muted-ink hover:text-forest hover:underline"
            }
          >
            <PubPeerGlyph />
            {pubpeerLabel}
          </a>
        )}
      </div>
      {peerReviewStatus && (
        <p className="mt-2 text-xs text-muted-ink">
          <span className="font-semibold text-ink/70">Open peer review reports: </span>
          {peerReviewUrl ? (
            <a href={peerReviewUrl} target="_blank" rel="noopener noreferrer" className="text-forest hover:underline">
              View reports ↗
            </a>
          ) : (
            <span title={peerReviewNote}>{PEER_REVIEW_LABEL[peerReviewStatus]}</span>
          )}
        </p>
      )}
      <p className="mt-2 text-[0.625rem] text-muted-ink">
        Retraction/correction status checked against Crossref (which now includes the Retraction
        Watch database) or DataCite for arXiv preprints, at curation time — not a live guarantee;
        verify independently before relying on it.
      </p>
    </div>
  );
}

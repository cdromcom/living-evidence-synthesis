import type { GraphNode } from "@/lib/data";

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

/** DOI link, critique/retraction status, PubPeer link-out, and author list for a source node. */
export default function SourceCredibility({ node }: { node: GraphNode }) {
  const doi = node.extras.doi as string | undefined;
  const sourceUrl = node.extras.sourceUrl as string | undefined;
  const critiqueStatus = node.extras.critiqueStatus as CritiqueStatus | undefined;
  const critiqueNote = node.extras.critiqueNote as string | undefined;
  const authors = node.extras.authors as string[] | undefined;

  if (!doi && !sourceUrl && !critiqueStatus) return null;

  const externalHref = doi ? `https://doi.org/${doi}` : sourceUrl;
  const pubpeerHref = doi ? `https://pubpeer.com/search?q=${encodeURIComponent(doi)}` : null;

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
        {critiqueStatus && (
          <span
            title={critiqueNote || CRITIQUE_LABELS[critiqueStatus]}
            className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-0.5 ${CRITIQUE_TONE[critiqueStatus]}`}
          >
            <CritiqueGlyph status={critiqueStatus} />
            {CRITIQUE_LABELS[critiqueStatus]}
          </span>
        )}
        {pubpeerHref && (
          <a
            href={pubpeerHref}
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-ink hover:text-forest hover:underline"
          >
            Check PubPeer comments ↗
          </a>
        )}
      </div>
      {authors && authors.length > 0 && (
        <p className="mt-2 text-xs text-muted-ink">
          <span className="font-semibold text-ink/70">Authors: </span>
          {authors.join(" · ")}
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

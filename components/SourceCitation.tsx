import { formatApaCitation } from "@/lib/apa";
import type { GraphNode } from "@/lib/data";

type PeerReviewStatus = "not-applicable" | "not-found" | "not-checked";

const PEER_REVIEW_LABEL: Record<PeerReviewStatus, string> = {
  "not-applicable": "NA — preprint, not peer reviewed",
  "not-found": "NA — checked, no open peer review reports found",
  "not-checked": "NA — not independently verified (publisher blocked automated access)",
};

/** A full APA 7th-edition citation plus open-peer-review link/status, shown at the top of each source page. */
export default function SourceCitation({ node }: { node: GraphNode }) {
  const citation = formatApaCitation(node);
  const peerReviewStatus = node.extras.peerReviewStatus as PeerReviewStatus | undefined;
  const peerReviewNote = node.extras.peerReviewNote as string | undefined;
  const peerReviewUrl = node.extras.peerReviewUrl as string | undefined;

  if (!citation.hasData && !peerReviewStatus) return null;

  return (
    <div className="mb-4 mt-2">
      {citation.hasData && (
        <p className="text-sm leading-relaxed text-ink/90">
          {citation.authors} ({citation.year}). {citation.title}.{" "}
          {citation.container && (
            <>
              <em>{citation.container}</em>
              {citation.volumeIssue && <em>, {citation.volumeIssue}</em>}
              {citation.pages && <>, {citation.pages}</>}.{" "}
            </>
          )}
          {citation.url && (
            <a href={citation.url} target="_blank" rel="noopener noreferrer" className="text-forest hover:underline">
              {citation.url}
            </a>
          )}
        </p>
      )}
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
    </div>
  );
}

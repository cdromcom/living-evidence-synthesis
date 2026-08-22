import type { GraphNode } from "@/lib/data";
import type { ReactNode } from "react";
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

// Original glyph — a partial ring, evoking the Altmetric attention donut.
function AltmetricGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" aria-hidden>
      <circle cx="12" cy="12" r="8" opacity={0.35} />
      <path d="M12 4a8 8 0 0 1 8 8" />
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

const CRITIQUE_SHORT_LABELS: Record<CritiqueStatus, string> = {
  none: "No corrections/retractions",
  "not-registered": "No retraction registry",
  correction: "Correction on record",
  "expression-of-concern": "Expression of concern",
  retraction: "Retraction on record",
};

const CRITIQUE_BORDER: Record<CritiqueStatus, string> = {
  none: "border-emerald-600/50",
  "not-registered": "border-border",
  correction: "border-amber-500/50",
  "expression-of-concern": "border-amber-600/50",
  retraction: "border-red-600/50",
};

const CRITIQUE_TEXT: Record<CritiqueStatus, string> = {
  none: "text-emerald-700",
  "not-registered": "text-muted-ink",
  correction: "text-amber-700",
  "expression-of-concern": "text-amber-800",
  retraction: "text-red-700",
};

const PEER_REVIEW_LABELS: Record<string, string> = {
  "not-applicable": "Preprint — not peer reviewed.",
  "not-found": "Checked; no open peer review reports found.",
  "not-checked": "Not independently verified (publisher blocked automated access).",
};

const PEER_REVIEW_SHORT_LABEL: Record<string, string> = {
  "not-applicable": "Not peer reviewed",
  "not-found": "No open reviews found",
  "not-checked": "Not checked",
};

// Original glyph — an open book, for open peer-review reports.
function PeerReviewGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M4 5.5h7v13H4a1 1 0 0 1-1-1v-11a1 1 0 0 1 1-1Z" />
      <path d="M20 5.5h-7v13h7a1 1 0 0 0 1-1v-11a1 1 0 0 0-1-1Z" />
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

/** One tile in the central box's horizontal card row. Renders as a link when `href` is given. */
function MiniCard({
  title,
  icon,
  border = "border-border",
  href,
  children,
}: {
  title: string;
  icon: ReactNode;
  border?: string;
  href?: string | null;
  children: ReactNode;
}) {
  const body = (
    <>
      <div className="flex items-center gap-1.5 text-[0.625rem] font-semibold uppercase tracking-wide text-muted-ink">
        {icon}
        {title}
      </div>
      <div className="mt-1 text-xs leading-snug">{children}</div>
    </>
  );
  const className = `flex min-w-0 flex-col rounded-md border bg-card p-2.5 ${border}`;
  return href ? (
    <a href={href} target="_blank" rel="noopener noreferrer" className={`${className} transition-colors hover:border-forest/50`}>
      {body}
    </a>
  ) : (
    <div className={className}>{body}</div>
  );
}

/** Altmetric, current status, PubPeer, and open-peer-review preview cards for a source node. */
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
  const hasPubpeerComments = Boolean(pubpeerCommentCount && pubpeerCommentCount > 0);

  return (
    <div className="mt-3 rounded-md bg-secondary-surface p-3">
      <div className="grid grid-cols-2 gap-2 lg:grid-cols-4">
        {doi && (
          <MiniCard title="Altmetric" icon={<AltmetricGlyph />}>
            <AltmetricBadge doi={doi} />
            <p className="mt-1.5 text-[0.625rem] leading-snug text-muted-ink">
              News, blog, social &amp; policy mentions — volume, not quality. Sentiment analysis of
              these mentions exists but is an Altmetric Explorer (paid) feature, not shown here.
            </p>
          </MiniCard>
        )}

        {critiqueStatus && (
          <MiniCard title="Current status" icon={<CritiqueGlyph status={critiqueStatus} />} border={CRITIQUE_BORDER[critiqueStatus]}>
            <span className={`font-semibold ${CRITIQUE_TEXT[critiqueStatus]}`}>
              {CRITIQUE_SHORT_LABELS[critiqueStatus]}
            </span>
            <p className="mt-1 text-[0.625rem] leading-snug text-muted-ink">
              {critiqueNote || CRITIQUE_LABELS[critiqueStatus]}
            </p>
          </MiniCard>
        )}

        {peerReviewStatus && (
          <MiniCard
            title="Open peer review"
            icon={<PeerReviewGlyph />}
            border={peerReviewUrl ? "border-emerald-600/50" : "border-border"}
            href={peerReviewUrl}
          >
            <span className={`font-semibold ${peerReviewUrl ? "text-emerald-700" : "text-ink/80"}`}>
              {peerReviewUrl ? "Reports available ↗" : PEER_REVIEW_SHORT_LABEL[peerReviewStatus]}
            </span>
            <p className="mt-1 text-[0.625rem] leading-snug text-muted-ink">
              {peerReviewUrl
                ? "Open review reports are published for this paper — view them."
                : peerReviewNote || PEER_REVIEW_LABELS[peerReviewStatus]}
            </p>
          </MiniCard>
        )}

        {pubpeerHref && (
          <MiniCard
            title="PubPeer"
            icon={<PubPeerGlyph />}
            border={hasPubpeerComments ? "border-amber-500/50" : "border-border"}
            href={pubpeerHref}
          >
            <span className={`font-semibold ${hasPubpeerComments ? "text-amber-700" : "text-ink/80"}`}>
              {hasPubpeerComments
                ? `${pubpeerCommentCount} comment${pubpeerCommentCount === 1 ? "" : "s"} ↗`
                : "No comments found"}
            </span>
            <p className="mt-1 text-[0.625rem] leading-snug text-muted-ink">
              {hasPubpeerComments
                ? "Post-publication discussion flagged on PubPeer — view the thread."
                : "Checked against PubPeer; no discussion threads found yet."}
            </p>
          </MiniCard>
        )}
      </div>
    </div>
  );
}

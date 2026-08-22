import { notFound } from "next/navigation";
import {
  ALL_NODES,
  getInboundEdges,
  getNodeById,
  getOutboundEdges,
} from "@/lib/data";
import { renderMarkdown } from "@/lib/markdown";
import NodeTypeBadge from "@/components/NodeTypeBadge";
import StatusBadge from "@/components/StatusBadge";
import EdgeGroups from "@/components/EdgeGroup";
import ReviewWidget from "@/components/ReviewWidget";
import NodeArticle from "@/components/NodeArticle";
import SourceToc from "@/components/SourceToc";
import TopBadges from "@/components/TopBadges";
import SourceCredibility from "@/components/SourceCredibility";
import SourceCitation from "@/components/SourceCitation";
import ClaimTruthValue from "@/components/ClaimTruthValue";
import CaveatMeta from "@/components/CaveatMeta";

export function generateStaticParams() {
  return ALL_NODES.map((n) => ({ id: n.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const node = getNodeById(id);
  return { title: node ? `${node.id} — ${node.title}` : "Node not found" };
}

const EXTRA_LABELS: Record<string, string> = {
  rating: "Rating",
};

function formatDate(d: string | null) {
  if (!d) return null;
  try {
    return new Date(d).toISOString().slice(0, 10);
  } catch {
    return d;
  }
}

export default async function NodeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const node = getNodeById(id);
  if (!node) notFound();

  const inbound = getInboundEdges(node.id);
  const outbound = getOutboundEdges(node.id);
  const { html, toc } = renderMarkdown(node.bodyMarkdown);
  const HANDLED_EXTRA_KEYS = new Set([
    "doi",
    "sourceUrl",
    "critiqueStatus",
    "critiqueNote",
    "authors",
    "authorTrackRecord",
    "authorTrackRecordChecked",
    "authorTrackRecordNote",
    "pubType",
    "selfCitationRate",
    "selfCitationChecked",
    "doajListed",
    "citationCount",
    "citationCountSource",
    "predatoryPublisherFlag",
    "predatoryPublisherNote",
    "pubpeerCommentCount",
    "pubpeerUrl",
    "crossNodeChecked",
    "crossNodeCorroborated",
    "nameConsistency",
    "nameConsistencyNote",
    "apaTitle",
    "apaContainer",
    "apaYear",
    "apaVolume",
    "apaIssue",
    "apaPages",
    "apaArticleNumber",
    "apaLandingUrl",
    "apaAuthors",
    "peerReviewStatus",
    "peerReviewNote",
    "peerReviewUrl",
    "citekey",
    "truthValue",
    "caveatType",
    "severity",
  ]);
  const truthValue = node.extras.truthValue as number | undefined;
  const caveatSeverity = node.extras.severity as "low" | "moderate" | "high" | undefined;
  const caveatType = node.extras.caveatType as "author-stated" | "inferred" | undefined;
  const extraEntries = Object.entries(node.extras).filter(
    ([k, v]) => v !== undefined && v !== null && v !== "" && !HANDLED_EXTRA_KEYS.has(k)
  );

  return (
    <main className="mx-auto max-w-[1400px] px-4 py-10 sm:px-6">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <NodeTypeBadge type={node.type} />
        <span className="mono text-xs text-muted-ink">{node.id}</span>
        <StatusBadge status={node.curationStatus} />
      </div>
      <h1 className="max-w-3xl text-2xl font-semibold leading-tight text-ink sm:text-3xl">
        {node.title}
      </h1>

      <SourceCitation node={node} />

      <div className="mt-3 flex flex-wrap gap-3 text-xs text-muted-ink">
        {node.created && <span>Created {formatDate(node.created)}</span>}
        {node.updated && <span>Updated {formatDate(node.updated)}</span>}
      </div>

      {typeof truthValue === "number" && (
        <div className="mt-3">
          <ClaimTruthValue value={truthValue} />
        </div>
      )}
      <CaveatMeta severity={caveatSeverity} caveatType={caveatType} />

      <TopBadges node={node} />
      <SourceCredibility node={node} />

      {extraEntries.length > 0 && (
        <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-1 text-xs sm:grid-cols-3">
          {extraEntries.map(([k, v]) => (
            <div key={k}>
              <dt className="text-muted-ink">{EXTRA_LABELS[k] || k}</dt>
              <dd className="mono font-medium">{String(v)}</dd>
            </div>
          ))}
        </dl>
      )}

      <div className="mt-8 grid gap-6 lg:grid-cols-[180px_1fr_240px] lg:items-start">
        {node.type === "SRC" ? (
          <SourceToc items={toc} />
        ) : (
          <div className="hidden lg:block" aria-hidden />
        )}

        <NodeArticle html={html} />

        <aside className="space-y-8 lg:sticky lg:top-20">
          <ReviewWidget nodeId={node.id} />
          <div>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted-ink">
              Inbound ({inbound.length})
            </h2>
            <EdgeGroups edges={inbound} otherEnd="from" />
          </div>
          <div>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-muted-ink">
              Outbound ({outbound.length})
            </h2>
            <EdgeGroups edges={outbound} otherEnd="to" />
          </div>
        </aside>
      </div>
    </main>
  );
}

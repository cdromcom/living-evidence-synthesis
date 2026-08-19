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
  truthValue: "Truth value",
  caveatType: "Caveat type",
  severity: "Severity",
  appraisalOverall: "Appraisal overall",
  tripodLlmPct: "TRIPOD-LLM compliance",
  citekey: "Citekey",
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
  const CREDIBILITY_EXTRA_KEYS = new Set([
    "doi",
    "sourceUrl",
    "critiqueStatus",
    "critiqueNote",
    "authors",
    "authorTrackRecord",
    "authorTrackRecordChecked",
    "authorTrackRecordNote",
  ]);
  const extraEntries = Object.entries(node.extras).filter(
    ([k, v]) => v !== undefined && v !== null && v !== "" && !CREDIBILITY_EXTRA_KEYS.has(k)
  );

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <NodeTypeBadge type={node.type} />
        <span className="mono text-xs text-muted-ink">{node.id}</span>
        <StatusBadge status={node.curationStatus} />
      </div>
      <h1 className="max-w-3xl text-2xl font-semibold leading-tight sm:text-3xl">
        {node.title}
      </h1>

      <div className="mt-3 flex flex-wrap gap-3 text-xs text-muted-ink">
        {node.created && <span>Created {formatDate(node.created)}</span>}
        {node.updated && <span>Updated {formatDate(node.updated)}</span>}
      </div>

      {(() => {
        const plainTags = node.tags.filter((t) => !t.startsWith("top/") && !t.startsWith("trust/"));
        return (
          plainTags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1.5">
              {plainTags.map((t) => (
                <span
                  key={t}
                  className="mono rounded-full bg-muted-surface px-2 py-0.5 text-[0.65rem] text-muted-ink"
                >
                  {t}
                </span>
              ))}
            </div>
          )
        );
      })()}

      <TopBadges node={node} />
      <SourceCredibility node={node} />

      {extraEntries.length > 0 && (
        <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-1 rounded-md border border-border bg-card p-3 text-xs sm:grid-cols-3">
          {extraEntries.map(([k, v]) => (
            <div key={k}>
              <dt className="text-muted-ink">{EXTRA_LABELS[k] || k}</dt>
              <dd className="mono font-medium">{String(v)}</dd>
            </div>
          ))}
        </dl>
      )}

      <div className="mt-8 grid gap-10 lg:grid-cols-[1fr_320px]">
        <div className="flex gap-6">
          {node.type === "SRC" && <SourceToc items={toc} />}
          <NodeArticle html={html} />
        </div>

        <aside className="space-y-8">
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

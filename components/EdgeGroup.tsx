import Link from "next/link";
import type { GraphEdge, EdgeType } from "@/lib/data";
import { EDGE_TYPE_LABELS, getNodeById } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";

export default function EdgeGroups({
  edges,
  otherEnd,
}: {
  edges: GraphEdge[];
  /** which side of the edge is the "other" node — 'from' or 'to' */
  otherEnd: "from" | "to";
}) {
  if (edges.length === 0) {
    return <p className="text-sm text-muted-ink">None.</p>;
  }
  const byType = new Map<EdgeType, GraphEdge[]>();
  for (const e of edges) {
    if (!byType.has(e.type)) byType.set(e.type, []);
    byType.get(e.type)!.push(e);
  }
  return (
    <div className="space-y-4">
      {Array.from(byType.entries()).map(([type, es]) => (
        <div key={type}>
          <h4 className="mono text-xs font-semibold uppercase tracking-wide text-muted-ink">
            {EDGE_TYPE_LABELS[type]} ({es.length})
          </h4>
          <ul className="mt-1.5 space-y-1.5">
            {es.map((e, i) => {
              const otherId = otherEnd === "from" ? e.from : e.to;
              const node = getNodeById(otherId);
              if (!node) return null;
              return (
                <li key={`${type}-${otherId}-${i}`}>
                  <Link
                    href={`/nodes/${node.id}`}
                    className="flex items-center gap-2 rounded-md border border-border bg-card px-3 py-2 text-sm transition-colors hover:border-forest/40"
                  >
                    <NodeTypeBadge type={node.type} typeLabel={node.type} />
                    <span className="truncate">{node.title}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </div>
  );
}

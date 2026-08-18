"use client";

import dynamic from "next/dynamic";
import { useMemo, useRef, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { GraphNode, GraphEdge, NodeType } from "@/lib/data";
import { NODE_TYPE_ORDER, getDegree } from "@/lib/data";
import { NODE_TYPE_COLOR_VAR, NODE_TYPE_BG_CLASS, NODE_TYPE_BORDER_CLASS, NODE_TYPE_TEXT_CLASS } from "@/lib/ui";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="flex h-[600px] items-center justify-center text-sm text-muted-ink">
      Loading graph…
    </div>
  ),
});

type FGNode = {
  id: string;
  type: NodeType;
  title: string;
  degree: number;
  status: string;
};
type FGLink = { source: string; target: string; type: string };

function resolveColor(varExpr: string): string {
  if (typeof window === "undefined") return "#888";
  const match = varExpr.match(/var\((--[a-z0-9-]+)\)/);
  if (!match) return varExpr;
  return getComputedStyle(document.documentElement)
    .getPropertyValue(match[1])
    .trim();
}

export default function GraphExplorer({
  nodes,
  edges,
}: {
  nodes: GraphNode[];
  edges: GraphEdge[];
}) {
  const router = useRouter();
  const fgRef = useRef<any>(null);
  const [typeFilter, setTypeFilter] = useState<Set<NodeType>>(
    new Set(NODE_TYPE_ORDER)
  );
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [hoverId, setHoverId] = useState<string | null>(null);

  const statuses = useMemo(
    () => Array.from(new Set(nodes.map((n) => n.curationStatus))).sort(),
    [nodes]
  );

  const graphData = useMemo(() => {
    const visibleIds = new Set(
      nodes
        .filter(
          (n) =>
            typeFilter.has(n.type) &&
            (statusFilter === "all" || n.curationStatus === statusFilter)
        )
        .map((n) => n.id)
    );
    const fgNodes: FGNode[] = nodes
      .filter((n) => visibleIds.has(n.id))
      .map((n) => ({
        id: n.id,
        type: n.type,
        title: n.title,
        degree: getDegree(n.id),
        status: n.curationStatus,
      }));
    const fgLinks: FGLink[] = edges
      .filter((e) => visibleIds.has(e.from) && visibleIds.has(e.to))
      .map((e) => ({ source: e.from, target: e.to, type: e.type }));
    return { nodes: fgNodes, links: fgLinks };
  }, [nodes, edges, typeFilter, statusFilter]);

  function toggleType(t: NodeType) {
    setTypeFilter((prev) => {
      const next = new Set(prev);
      if (next.has(t)) next.delete(t);
      else next.add(t);
      return next;
    });
  }

  const nodeCanvasObject = useCallback(
    (node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const r = 3 + Math.min(10, Math.sqrt(node.degree || 1) * 1.6);
      const color = resolveColor(NODE_TYPE_COLOR_VAR[node.type as NodeType]);
      ctx.beginPath();
      ctx.arc(node.x, node.y, r, 0, 2 * Math.PI, false);
      ctx.fillStyle = color;
      ctx.globalAlpha = hoverId && hoverId !== node.id ? 0.35 : 1;
      ctx.fill();
      if (hoverId === node.id) {
        ctx.lineWidth = 1.5 / globalScale;
        ctx.strokeStyle = resolveColor("var(--color-ink)");
        ctx.stroke();
      }
      ctx.globalAlpha = 1;
      if (globalScale > 2.5 || hoverId === node.id) {
        ctx.font = `${10 / globalScale}px var(--font-body, sans-serif)`;
        ctx.fillStyle = resolveColor("var(--color-ink)");
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(
          node.title.length > 60 ? node.title.slice(0, 60) + "…" : node.title,
          node.x + r + 2,
          node.y
        );
      }
    },
    [hoverId]
  );

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-2">
        {NODE_TYPE_ORDER.map((t) => (
          <button
            key={t}
            onClick={() => toggleType(t)}
            className={`rounded-full border px-3 py-1 text-xs font-semibold transition-colors ${
              typeFilter.has(t)
                ? `${NODE_TYPE_BG_CLASS[t]} ${NODE_TYPE_BORDER_CLASS[t]} text-white`
                : `${NODE_TYPE_BORDER_CLASS[t]} ${NODE_TYPE_TEXT_CLASS[t]} bg-card opacity-60 hover:opacity-100`
            }`}
          >
            {t}
          </button>
        ))}
        <span className="mx-1 h-4 w-px bg-border" />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs"
        >
          <option value="all">All statuses</option>
          {statuses.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <span className="mono ml-auto text-xs text-muted-ink">
          {graphData.nodes.length} nodes · {graphData.links.length} edges
        </span>
      </div>

      <div className="overflow-hidden rounded-lg border border-border bg-card">
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeId="id"
          nodeLabel={(n: any) => `${n.type}: ${n.title}`}
          nodeCanvasObject={nodeCanvasObject}
          nodePointerAreaPaint={(node: any, color: string, ctx: CanvasRenderingContext2D) => {
            const r = 3 + Math.min(10, Math.sqrt(node.degree || 1) * 1.6);
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, r + 2, 0, 2 * Math.PI, false);
            ctx.fill();
          }}
          onNodeHover={(n: any) => setHoverId(n ? n.id : null)}
          onNodeClick={(n: any) => router.push(`/nodes/${n.id}`)}
          linkColor={() => "rgba(107,102,96,0.35)"}
          linkDirectionalArrowLength={3}
          linkDirectionalArrowRelPos={1}
          linkWidth={0.6}
          height={620}
          cooldownTicks={100}
          backgroundColor="rgba(0,0,0,0)"
        />
      </div>
      <p className="mt-2 text-xs text-muted-ink">
        Node size reflects degree (number of connections). Click a node to
        open its detail page; hover to highlight and reveal its title.
      </p>
    </div>
  );
}

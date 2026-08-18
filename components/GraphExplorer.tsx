"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useMemo, useRef, useState, useCallback, useEffect } from "react";
import type { GraphNode, GraphEdge, NodeType } from "@/lib/data";
import { NODE_TYPE_ORDER, NODE_TYPE_LABELS, getNodeById } from "@/lib/data";
import { NODE_TYPE_COLOR_VAR, NODE_TYPE_BG_CLASS, NODE_TYPE_BORDER_CLASS, NODE_TYPE_TEXT_CLASS } from "@/lib/ui";

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="flex h-[620px] items-center justify-center text-sm text-muted-ink">
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
  // Injected by the force simulation at runtime, absent before the first tick.
  x?: number;
  y?: number;
};
type FGLink = { source: string; target: string; type: string };

function nodeRadius(node: { degree: number }): number {
  return 4 + Math.min(10, Math.sqrt(node.degree || 1) * 1.6);
}

function resolveColor(varExpr: string): string {
  if (typeof window === "undefined") return "#888";
  const match = varExpr.match(/var\((--[a-z0-9-]+)\)/);
  if (!match) return varExpr;
  return getComputedStyle(document.documentElement)
    .getPropertyValue(match[1])
    .trim();
}

/** Strip the most common Markdown/Obsidian-callout syntax down to plain text. */
function stripMarkdown(raw: string): string {
  return raw
    .replace(/^---[\s\S]*?---/, "") // frontmatter
    .replace(/!\[.*?\]\(.*?\)/g, "") // images
    .replace(/\[\[([^\]|]+)\|?[^\]]*\]\]/g, "$1") // wikilinks
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1") // links
    .replace(/>\s*\[!\w+\]\s*[^\n]*/g, "") // Obsidian callout markers, e.g. "> [!info] Quotes"
    .replace(/\(@\w+\d{4}[^)]*\)/g, "") // inline citation keys like (@leeSomething2024)
    .replace(/[#>*_`~]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

/** Truncate at the nearest sentence boundary under maxLen where possible, instead of mid-word. */
function truncateReadable(text: string, maxLen: number): string {
  if (text.length <= maxLen) return text;
  const cut = text.slice(0, maxLen);
  const lastStop = Math.max(cut.lastIndexOf(". "), cut.lastIndexOf("? "), cut.lastIndexOf("! "));
  if (lastStop > maxLen * 0.4) return cut.slice(0, lastStop + 1);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 0 ? cut.slice(0, lastSpace) : cut) + "…";
}

/** Pulls the plain-text content of one Markdown section (until the next heading of any level). */
function extractSection(markdown: string, headingPattern: RegExp): string | null {
  const lines = markdown.split("\n");
  const startIdx = lines.findIndex((l) => headingPattern.test(l));
  if (startIdx === -1) return null;
  const rest = lines.slice(startIdx + 1);
  const endIdx = rest.findIndex((l) => /^#{1,6}\s/.test(l));
  const sectionLines = endIdx === -1 ? rest : rest.slice(0, endIdx);
  const text = stripMarkdown(sectionLines.join(" "));
  return text || null;
}

// Each node type's template puts its most informative content under a
// different heading (a TL;DR callout for sources, the verbatim quote for
// evidence, the limitation statement for caveats, etc). The node's own
// title already states the claim/question for QUE and CLM, so for those we
// surface the first supporting quote instead of repeating the title.
const SUMMARY_SECTION_BY_TYPE: Partial<Record<NodeType, RegExp>> = {
  SRC: /TL;?DR/i,
  EVD: /^##\s*Description/im,
  CVT: /^###?\s*Limitation/im,
  EP: /^##\s*Pattern statement/im,
  QUE: /Quote/i,
  CLM: /Quote/i,
};

/** A compact, type-aware summary for the graph preview panel — not a blind character truncation. */
function nodeSummary(node: GraphNode, maxLen = 260): string | null {
  const pattern = SUMMARY_SECTION_BY_TYPE[node.type];
  const extracted = pattern ? extractSection(node.bodyMarkdown, pattern) : null;
  const text = extracted || stripMarkdown(node.bodyMarkdown) || null;
  return text ? truncateReadable(text, maxLen) : null;
}

export default function GraphExplorer({
  nodes,
  edges,
}: {
  nodes: GraphNode[];
  edges: GraphEdge[];
}) {
  const fgRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [typeFilter, setTypeFilter] = useState<Set<NodeType>>(
    new Set(NODE_TYPE_ORDER)
  );
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [focusMode, setFocusMode] = useState(false);

  const statuses = useMemo(
    () => Array.from(new Set(nodes.map((n) => n.curationStatus))).sort(),
    [nodes]
  );

  const baseGraphData = useMemo(() => {
    const visibleIds = new Set(
      nodes
        .filter(
          (n) =>
            typeFilter.has(n.type) &&
            (statusFilter === "all" || n.curationStatus === statusFilter)
        )
        .map((n) => n.id)
    );
    const degreeById = new Map<string, number>();
    for (const e of edges) {
      degreeById.set(e.from, (degreeById.get(e.from) ?? 0) + 1);
      degreeById.set(e.to, (degreeById.get(e.to) ?? 0) + 1);
    }
    const fgNodes: FGNode[] = nodes
      .filter((n) => visibleIds.has(n.id))
      .map((n) => ({
        id: n.id,
        type: n.type,
        title: n.title,
        degree: degreeById.get(n.id) ?? 0,
        status: n.curationStatus,
      }));
    const fgLinks: FGLink[] = edges
      .filter((e) => visibleIds.has(e.from) && visibleIds.has(e.to))
      .map((e) => ({ source: e.from, target: e.to, type: e.type }));
    return { nodes: fgNodes, links: fgLinks };
  }, [nodes, edges, typeFilter, statusFilter]);

  // Adjacency, built once per filtered graph — powers both hover/selection
  // highlighting and focus (ego-network) mode.
  const neighborsOf = useMemo(() => {
    const map = new Map<string, Set<string>>();
    for (const l of baseGraphData.links) {
      const s = typeof l.source === "string" ? l.source : (l.source as any).id;
      const t = typeof l.target === "string" ? l.target : (l.target as any).id;
      if (!map.has(s)) map.set(s, new Set());
      if (!map.has(t)) map.set(t, new Set());
      map.get(s)!.add(t);
      map.get(t)!.add(s);
    }
    return map;
  }, [baseGraphData.links]);

  const graphData = useMemo(() => {
    if (!focusMode || !selectedId) return baseGraphData;
    const keep = new Set([selectedId, ...(neighborsOf.get(selectedId) ?? [])]);
    return {
      nodes: baseGraphData.nodes.filter((n) => keep.has(n.id)),
      links: baseGraphData.links.filter((l) => {
        const s = typeof l.source === "string" ? l.source : (l.source as any).id;
        const t = typeof l.target === "string" ? l.target : (l.target as any).id;
        return keep.has(s) && keep.has(t);
      }),
    };
  }, [baseGraphData, focusMode, selectedId, neighborsOf]);

  const highlightId = hoverId ?? selectedId;
  const highlightNeighbors = highlightId ? neighborsOf.get(highlightId) : undefined;

  const nodeById = useMemo(() => new Map(graphData.nodes.map((n) => [n.id, n])), [graphData.nodes]);

  // Real per-frame label-overlap avoidance: every candidate label's screen
  // rect is checked against every rect already claimed this frame, and
  // skipped entirely (not drawn cropped/underneath) if it would collide.
  // Reset in onRenderFramePre, before any node's label is considered.
  const labelRectsRef = useRef<[number, number, number, number][]>([]);
  function rectsOverlap(a: [number, number, number, number], b: [number, number, number, number]) {
    return a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
  }
  function claimLabelRect(rect: [number, number, number, number]): boolean {
    for (const r of labelRectsRef.current) {
      if (rectsOverlap(rect, r)) return false;
    }
    labelRectsRef.current.push(rect);
    return true;
  }

  function toggleType(t: NodeType) {
    hasAutoFittedRef.current = false; // re-fit once for the newly-visible node set
    setTypeFilter((prev) => {
      const next = new Set(prev);
      if (next.has(t)) next.delete(t);
      else next.add(t);
      return next;
    });
  }

  function selectNode(id: string | null) {
    setSelectedId(id);
    if (!id) setFocusMode(false);
  }

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") selectNode(null);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  function zoomToFit() {
    fgRef.current?.zoomToFit(400, 48);
  }

  // Auto-fit only on the graph's first settle. Re-fitting on every engine
  // stop (which also fires after every filter/focus-mode change) zoomed out
  // further each time a large set of nodes came into view, shrinking dots
  // past the point of legibility — hence the "blurry, overlapping" look.
  // A user can always re-center manually with the "Fit to view" button.
  const hasAutoFittedRef = useRef(false);
  function handleEngineStop() {
    if (hasAutoFittedRef.current) return;
    hasAutoFittedRef.current = true;
    zoomToFit();
  }

  // Short "phrase" labels, not full titles — keeps individual labels small
  // enough that the collision check below can actually fit several at once.
  const MAX_LABEL_CHARS = 40;
  function shortLabel(title: string) {
    return title.length > MAX_LABEL_CHARS ? title.slice(0, MAX_LABEL_CHARS) + "…" : title;
  }

  function computeLabelRect(
    node: any,
    ctx: CanvasRenderingContext2D,
    globalScale: number,
    priority: boolean
  ): [number, number, number, number] {
    const r = nodeRadius(node);
    const fontSize = (priority ? 11 : 10) / globalScale;
    ctx.font = `${fontSize}px var(--font-body, sans-serif)`;
    const width = ctx.measureText(shortLabel(node.title)).width;
    const x0 = node.x + r + 2;
    const y0 = node.y - fontSize * 0.65;
    return [x0, y0, x0 + width, y0 + fontSize * 1.3];
  }

  function drawLabel(node: any, ctx: CanvasRenderingContext2D, globalScale: number, priority: boolean) {
    const r = nodeRadius(node);
    ctx.font = `${(priority ? 11 : 10) / globalScale}px var(--font-body, sans-serif)`;
    ctx.fillStyle = resolveColor("var(--color-ink)");
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(shortLabel(node.title), node.x + r + 2, node.y);
  }

  // Runs once per frame, before any node is drawn: reserve label space for
  // the hovered/selected node(s) first so they always win the collision
  // check below, instead of losing to whichever neighbor happens to be
  // iterated first.
  function onRenderFramePre(ctx: CanvasRenderingContext2D, globalScale: number) {
    labelRectsRef.current = [];
    for (const id of [hoverId, selectedId]) {
      if (!id) continue;
      const n = nodeById.get(id);
      if (!n || n.x == null || n.y == null) continue;
      claimLabelRect(computeLabelRect(n, ctx, globalScale, true));
    }
  }

  const nodeCanvasObject = useCallback(
    (node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const r = nodeRadius(node);
      const color = resolveColor(NODE_TYPE_COLOR_VAR[node.type as NodeType]);
      const isHighlighted = !highlightId || node.id === highlightId || highlightNeighbors?.has(node.id);
      ctx.beginPath();
      ctx.arc(node.x, node.y, r, 0, 2 * Math.PI, false);
      ctx.fillStyle = color;
      ctx.globalAlpha = isHighlighted ? 1 : 0.3;
      ctx.fill();
      const isPriority = node.id === selectedId || node.id === hoverId;
      if (isPriority) {
        ctx.lineWidth = (node.id === selectedId ? 2.5 : 1.5) / globalScale;
        ctx.strokeStyle = resolveColor("var(--color-ink)");
        ctx.stroke();
      }
      ctx.globalAlpha = 1;

      // Progressive label disclosure: at low zoom only the highlighted
      // cluster is even a candidate; among candidates, a label only ever
      // draws if it doesn't collide with one already claimed this frame —
      // so labels never overlap, they just thin out in crowded areas.
      const isCandidate =
        globalScale > 2.5 || isPriority || (highlightId != null && highlightNeighbors?.has(node.id));
      if (!isCandidate) return;

      if (isPriority) {
        // Already reserved in onRenderFramePre — draw unconditionally.
        drawLabel(node, ctx, globalScale, true);
        return;
      }
      const rect = computeLabelRect(node, ctx, globalScale, false);
      if (claimLabelRect(rect)) drawLabel(node, ctx, globalScale, false);
    },
    [hoverId, selectedId, highlightId, highlightNeighbors, nodeById]
  );

  const selectedNode = selectedId ? getNodeById(selectedId) : undefined;

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-2">
        {NODE_TYPE_ORDER.map((t) => (
          <button
            key={t}
            onClick={() => toggleType(t)}
            title={NODE_TYPE_LABELS[t]}
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
          onChange={(e) => {
            hasAutoFittedRef.current = false;
            setStatusFilter(e.target.value);
          }}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs"
        >
          <option value="all">All statuses</option>
          {statuses.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <button
          onClick={zoomToFit}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold text-ink/80 hover:bg-muted-surface"
        >
          Fit to view
        </button>
        <span className="mono ml-auto text-xs text-muted-ink">
          {graphData.nodes.length} nodes · {graphData.links.length} edges
          {focusMode ? " (focused)" : ""}
        </span>
      </div>

      <div className="grid gap-3 lg:grid-cols-[1fr_280px]">
        <div ref={containerRef} className="overflow-hidden rounded-lg border border-border bg-card">
          <ForceGraph2D
            ref={fgRef}
            graphData={graphData}
            nodeId="id"
            nodeLabel={(n: any) => `${NODE_TYPE_LABELS[n.type as NodeType]}: ${n.title}`}
            nodeCanvasObject={nodeCanvasObject}
            nodePointerAreaPaint={(node: any, color: string, ctx: CanvasRenderingContext2D) => {
              const r = nodeRadius(node);
              ctx.fillStyle = color;
              ctx.beginPath();
              ctx.arc(node.x, node.y, r + 2, 0, 2 * Math.PI, false);
              ctx.fill();
            }}
            onNodeHover={(n: any) => setHoverId(n ? n.id : null)}
            onNodeClick={(n: any) => selectNode(n.id === selectedId ? null : n.id)}
            onBackgroundClick={() => selectNode(null)}
            onEngineStop={handleEngineStop}
            minZoom={0.55}
            onRenderFramePre={onRenderFramePre}
            linkColor={(l: any) => {
              const s = typeof l.source === "string" ? l.source : l.source?.id;
              const t = typeof l.target === "string" ? l.target : l.target?.id;
              const touchesHighlight = highlightId && (s === highlightId || t === highlightId);
              return touchesHighlight ? "rgba(107,102,96,0.85)" : "rgba(107,102,96,0.18)";
            }}
            linkWidth={(l: any) => {
              const s = typeof l.source === "string" ? l.source : l.source?.id;
              const t = typeof l.target === "string" ? l.target : l.target?.id;
              const touchesHighlight = highlightId && (s === highlightId || t === highlightId);
              return touchesHighlight ? 1.4 : 0.5;
            }}
            linkDirectionalArrowLength={3}
            linkDirectionalArrowRelPos={1}
            height={620}
            cooldownTicks={100}
            backgroundColor="rgba(0,0,0,0)"
          />
        </div>

        <div className="rounded-lg border border-border bg-card p-4">
          {selectedNode ? (
            <div>
              <div className="flex items-start justify-between gap-2">
                <span
                  className={`inline-flex items-center rounded-full px-2 py-0.5 text-[0.6875rem] font-semibold uppercase tracking-wide text-white ${NODE_TYPE_BG_CLASS[selectedNode.type]}`}
                >
                  {selectedNode.type}
                </span>
                <button
                  onClick={() => selectNode(null)}
                  aria-label="Close preview"
                  className="text-muted-ink hover:text-ink"
                >
                  ✕
                </button>
              </div>
              <h3 className="mt-2 text-sm font-semibold leading-snug text-ink">{selectedNode.title}</h3>
              <p className="mt-1 text-xs text-muted-ink">
                {NODE_TYPE_LABELS[selectedNode.type]} · {selectedNode.curationStatus} ·{" "}
                {neighborsOf.get(selectedNode.id)?.size ?? 0} connection
                {(neighborsOf.get(selectedNode.id)?.size ?? 0) === 1 ? "" : "s"}
              </p>
              {(() => {
                const summary = nodeSummary(selectedNode);
                return summary ? (
                  <p className="mt-3 text-xs leading-relaxed text-ink/80">{summary}</p>
                ) : null;
              })()}
              <div className="mt-4 flex flex-col gap-2">
                <button
                  onClick={() => {
                    hasAutoFittedRef.current = false;
                    setFocusMode((f) => !f);
                  }}
                  className={`rounded-md border px-3 py-1.5 text-xs font-semibold transition-colors ${
                    focusMode
                      ? "border-forest bg-forest text-paper"
                      : "border-border bg-card text-ink/80 hover:bg-muted-surface"
                  }`}
                >
                  {focusMode ? "Show full graph" : "Focus this neighborhood"}
                </button>
                <Link
                  href={`/nodes/${selectedNode.id}`}
                  className="rounded-md border border-border bg-card px-3 py-1.5 text-center text-xs font-semibold text-ink/80 hover:bg-muted-surface"
                >
                  Open full page →
                </Link>
              </div>
            </div>
          ) : (
            <div className="text-xs text-muted-ink">
              <p className="font-semibold text-ink/80">How to read this graph</p>
              <ul className="mt-2 list-disc space-y-1.5 pl-4">
                <li>Chip color above = node type; dot size = number of connections.</li>
                <li>Hover a node to highlight it and its direct connections.</li>
                <li>Click a node to preview it here without leaving the graph.</li>
                <li>&quot;Focus this neighborhood&quot; isolates a node and its connections to cut clutter.</li>
                <li>Drag nodes to rearrange; scroll/pinch to zoom; &quot;Fit to view&quot; re-centers.</li>
              </ul>
              <p className="mt-3">
                Prefer a plain list?{" "}
                <Link href="/nodes" className="text-forest">
                  Browse all nodes
                </Link>
                .
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

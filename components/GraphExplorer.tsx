"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useMemo, useRef, useState, useCallback, useEffect } from "react";
import type { GraphNode, GraphEdge, NodeType, FiveC, ReproducibilityRisk, ReportingComplianceLevel } from "@/lib/data";
import {
  NODE_TYPE_ORDER,
  NODE_TYPE_LABELS,
  FIVE_C_ORDER,
  FIVE_C_LABELS,
  getFiveCs,
  getNodeById,
  TOP_STANDARD_ORDER,
  TOP_STANDARD_LABELS,
  getTopSignals,
  REPRODUCIBILITY_RISK_LABELS,
  getValiditySignals,
  REPORTING_COMPLIANCE_LABELS,
  getReportingCompliance,
  INTEGRITY_SIGNAL_ORDER,
  INTEGRITY_SIGNAL_LABELS,
  getIntegritySignals,
} from "@/lib/data";
import {
  NODE_TYPE_COLOR_VAR,
  NODE_TYPE_BG_CLASS,
  NODE_TYPE_BORDER_CLASS,
  NODE_TYPE_TEXT_CLASS,
  GRAPH_SELECT_NODE_EVENT,
} from "@/lib/ui";

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
  fiveCs: FiveC[];
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

type TrustSignalOption = { key: string; label: string; group: string; test: (n: GraphNode) => boolean };

// Mirrors the four trust-signal groups shown on each SRC page (TopBadges.tsx)
// — Openness (COS TOP standards), Rigor (validity-domain risk), Transparency
// (TRIPOD-LLM reporting compliance), and Integrity (disclosures). Extensibility
// is deliberately left out: those are unscored "not done yet" reminders, not
// real signals to filter by.
const TRUST_SIGNAL_OPTIONS: TrustSignalOption[] = [
  ...TOP_STANDARD_ORDER.map((standard) => ({
    key: `top:${standard}`,
    label: TOP_STANDARD_LABELS[standard],
    group: "Openness",
    test: (n: GraphNode) =>
      getTopSignals(n).some(
        (s) => s.standard === standard && (s.level === "level-1-disclosed" || s.level === "level-2-shared")
      ),
  })),
  ...(["low-risk", "some-concerns", "high-risk"] as ReproducibilityRisk[]).map((risk) => ({
    key: `rigor:${risk}`,
    label: REPRODUCIBILITY_RISK_LABELS[risk],
    group: "Rigor",
    test: (n: GraphNode) => getValiditySignals(n).some((v) => v.risk === risk),
  })),
  ...(["high", "moderate", "low"] as ReportingComplianceLevel[]).map((level) => ({
    key: `reporting:${level}`,
    label: `${REPORTING_COMPLIANCE_LABELS[level]} reporting`,
    group: "Transparency",
    test: (n: GraphNode) => getReportingCompliance(n.id)?.level === level,
  })),
  ...INTEGRITY_SIGNAL_ORDER.map((kind) => ({
    key: `integrity:${kind}`,
    label: INTEGRITY_SIGNAL_LABELS[kind],
    group: "Integrity",
    test: (n: GraphNode) =>
      getIntegritySignals(n).some((s) => s.kind === kind && (s.level === "disclosed" || s.level === "partial")),
  })),
];

/** A dropdown filter — a labeled toggle button that opens a grouped list of square checkboxes. */
function CheckboxDropdown({
  label,
  options,
  selected,
  onToggle,
  onClear,
}: {
  label: string;
  options: { key: string; label: string; group?: string }[];
  selected: Set<string>;
  onToggle: (key: string) => void;
  onClear: () => void;
}) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function onDocMouseDown(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onDocMouseDown);
    return () => document.removeEventListener("mousedown", onDocMouseDown);
  }, [open]);

  const groups = useMemo(() => {
    const map = new Map<string, { key: string; label: string; group?: string }[]>();
    for (const o of options) {
      const g = o.group ?? "";
      if (!map.has(g)) map.set(g, []);
      map.get(g)!.push(o);
    }
    return Array.from(map.entries());
  }, [options]);

  return (
    <div className="relative" ref={containerRef}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className={`flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-semibold transition-colors ${
          selected.size > 0
            ? "border-ink bg-ink text-paper"
            : "border-border bg-card text-ink/70 hover:bg-muted-surface"
        }`}
      >
        {label}
        {selected.size > 0 && <span className="mono">{selected.size}</span>}
        <span aria-hidden className="text-[0.6rem]">▾</span>
      </button>
      {open && (
        <div className="absolute z-20 mt-1 max-h-80 w-64 overflow-y-auto rounded-md border border-border bg-card p-2 shadow-md">
          {selected.size > 0 && (
            <button
              type="button"
              onClick={onClear}
              className="mb-1.5 text-[0.6875rem] font-semibold text-forest hover:underline"
            >
              Clear ({selected.size})
            </button>
          )}
          {groups.map(([group, opts]) => (
            <div key={group || "_"} className="mb-2 last:mb-0">
              {group && (
                <p className="mb-1 text-[0.625rem] font-semibold uppercase tracking-wide text-muted-ink">
                  {group}
                </p>
              )}
              <ul className="space-y-0.5">
                {opts.map((o) => (
                  <li key={o.key}>
                    <label className="flex cursor-pointer items-center gap-2 rounded px-1 py-0.5 text-xs text-ink/80 hover:bg-muted-surface">
                      <input
                        type="checkbox"
                        checked={selected.has(o.key)}
                        onChange={() => onToggle(o.key)}
                        className="h-3.5 w-3.5 shrink-0 rounded-none border-border accent-forest"
                      />
                      {o.label}
                    </label>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

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
  // Empty set = filter inactive (show everything, including nodes with no
  // 5C tag at all — most QUE/SRC/CVT/EP nodes). Non-empty = show only nodes
  // that carry at least one of the selected 5Cs.
  const [fiveCFilter, setFiveCFilter] = useState<Set<FiveC>>(new Set());
  // Same empty-set-means-inactive convention as fiveCFilter, OR'd across
  // whichever trust-signal checkboxes (Openness/Rigor/Transparency/Integrity)
  // are selected — see TRUST_SIGNAL_OPTIONS.
  const [trustSignalFilter, setTrustSignalFilter] = useState<Set<string>>(new Set());
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [focusMode, setFocusMode] = useState(false);
  const [showNodeList, setShowNodeList] = useState(false);
  const [expandedNeighbors, setExpandedNeighbors] = useState<Set<string>>(new Set());

  // force-graph defaults `width` to window.innerWidth when no width prop is
  // given — not the actual rendered width of our (narrower) grid column. The
  // canvas then draws at that oversized width and gets silently clipped by
  // this container's overflow-hidden, so zoomToFit ("Fit to view") computes
  // its target scale against a virtual viewport far wider than what's
  // visible: the graph "fits" a box you can't see most of. Measuring the
  // container and passing width explicitly fixes both that and the initial
  // auto-fit.
  const [graphWidth, setGraphWidth] = useState(0);
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const w = Math.round(entries[0].contentRect.width);
      setGraphWidth((prev) => (prev === w ? prev : w));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

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
            (statusFilter === "all" || n.curationStatus === statusFilter) &&
            (fiveCFilter.size === 0 || getFiveCs(n).some((c) => fiveCFilter.has(c))) &&
            (trustSignalFilter.size === 0 ||
              TRUST_SIGNAL_OPTIONS.filter((o) => trustSignalFilter.has(o.key)).some((o) => o.test(n)))
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
        fiveCs: getFiveCs(n),
      }));
    const fgLinks: FGLink[] = edges
      .filter((e) => visibleIds.has(e.from) && visibleIds.has(e.to))
      .map((e) => ({ source: e.from, target: e.to, type: e.type }));
    return { nodes: fgNodes, links: fgLinks };
  }, [nodes, edges, typeFilter, statusFilter, fiveCFilter, trustSignalFilter]);

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

  // Real per-frame label-overlap avoidance. A candidate label's screen rect
  // is checked against three kinds of obstacles claimed so far this frame —
  // other labels, every node's own dot, and every visible link line — and
  // skipped entirely (not drawn cropped/underneath/through) if it collides
  // with any of them. Node-dot and link obstacles are seeded once per frame
  // in onRenderFramePre, before any label is considered.
  type Rect = [number, number, number, number];
  const labelRectsRef = useRef<Rect[]>([]);
  const lineSegmentsRef = useRef<[number, number, number, number][]>([]);

  function rectsOverlap(a: Rect, b: Rect) {
    return a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
  }
  function pointInRect([x0, y0, x1, y1]: Rect, x: number, y: number) {
    return x >= x0 && x <= x1 && y >= y0 && y <= y1;
  }
  function cross(ox: number, oy: number, ax: number, ay: number, bx: number, by: number) {
    return (ax - ox) * (by - oy) - (ay - oy) * (bx - ox);
  }
  function segmentsIntersect(
    ax1: number, ay1: number, ax2: number, ay2: number,
    bx1: number, by1: number, bx2: number, by2: number
  ) {
    const d1 = cross(bx1, by1, bx2, by2, ax1, ay1);
    const d2 = cross(bx1, by1, bx2, by2, ax2, ay2);
    const d3 = cross(ax1, ay1, ax2, ay2, bx1, by1);
    const d4 = cross(ax1, ay1, ax2, ay2, bx2, by2);
    return ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0));
  }
  function segmentIntersectsRect(x1: number, y1: number, x2: number, y2: number, rect: Rect) {
    const [rx0, ry0, rx1, ry1] = rect;
    const segMinX = Math.min(x1, x2), segMaxX = Math.max(x1, x2);
    const segMinY = Math.min(y1, y2), segMaxY = Math.max(y1, y2);
    if (segMaxX < rx0 || segMinX > rx1 || segMaxY < ry0 || segMinY > ry1) return false;
    if (pointInRect(rect, x1, y1) || pointInRect(rect, x2, y2)) return true;
    const edges: [number, number, number, number][] = [
      [rx0, ry0, rx1, ry0],
      [rx1, ry0, rx1, ry1],
      [rx1, ry1, rx0, ry1],
      [rx0, ry1, rx0, ry0],
    ];
    return edges.some(([ex1, ey1, ex2, ey2]) => segmentsIntersect(x1, y1, x2, y2, ex1, ey1, ex2, ey2));
  }
  function claimLabelRect(rect: Rect): boolean {
    for (const r of labelRectsRef.current) {
      if (rectsOverlap(rect, r)) return false;
    }
    for (const [x1, y1, x2, y2] of lineSegmentsRef.current) {
      if (segmentIntersectsRect(x1, y1, x2, y2, rect)) return false;
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

  function toggleFiveC(c: FiveC) {
    hasAutoFittedRef.current = false;
    setFiveCFilter((prev) => {
      const next = new Set(prev);
      if (next.has(c)) next.delete(c);
      else next.add(c);
      return next;
    });
  }

  function toggleTrustSignal(key: string) {
    hasAutoFittedRef.current = false;
    setTrustSignalFilter((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  function selectNode(id: string | null) {
    setSelectedId(id);
    setExpandedNeighbors(new Set());
    if (!id) setFocusMode(false);
  }

  function toggleNeighborExpanded(id: string) {
    setExpandedNeighbors((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") selectNode(null);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  // Lets the global search palette (⌘K) preview a node in place when
  // already on /graph, instead of navigating away and losing state.
  // Widens the current filters if needed so the requested node is guaranteed
  // to be visible/selectable.
  useEffect(() => {
    function onExternalSelect(e: Event) {
      const id = (e as CustomEvent<string>).detail;
      const node = nodes.find((n) => n.id === id);
      if (!node) return;
      hasAutoFittedRef.current = false;
      setTypeFilter((prev) => (prev.has(node.type) ? prev : new Set(prev).add(node.type)));
      setStatusFilter((prev) => (prev === "all" || prev === node.curationStatus ? prev : "all"));
      setFocusMode(false);
      setSelectedId(id);
    }
    window.addEventListener(GRAPH_SELECT_NODE_EVENT, onExternalSelect);
    return () => window.removeEventListener(GRAPH_SELECT_NODE_EVENT, onExternalSelect);
  }, [nodes]);

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

  type LabelSide = "right" | "left" | "bottom" | "top";
  const LABEL_SIDES: LabelSide[] = ["right", "left", "bottom", "top"];

  function computeLabelRect(
    node: any,
    ctx: CanvasRenderingContext2D,
    globalScale: number,
    priority: boolean,
    side: LabelSide
  ): Rect {
    const r = nodeRadius(node);
    const fontSize = (priority ? 11 : 10) / globalScale;
    ctx.font = `${fontSize}px var(--font-body, sans-serif)`;
    const width = ctx.measureText(shortLabel(node.title)).width;
    const gap = 2;
    if (side === "right") {
      const x0 = node.x + r + gap;
      const y0 = node.y - fontSize * 0.65;
      return [x0, y0, x0 + width, y0 + fontSize * 1.3];
    }
    if (side === "left") {
      const x1 = node.x - r - gap;
      const y0 = node.y - fontSize * 0.65;
      return [x1 - width, y0, x1, y0 + fontSize * 1.3];
    }
    if (side === "bottom") {
      const x0 = node.x - width / 2;
      const y0 = node.y + r + gap;
      return [x0, y0, x0 + width, y0 + fontSize * 1.3];
    }
    // top
    const x0 = node.x - width / 2;
    const y1 = node.y - r - gap;
    return [x0, y1 - fontSize * 1.3, x0 + width, y1];
  }

  function drawLabel(
    node: any,
    ctx: CanvasRenderingContext2D,
    globalScale: number,
    priority: boolean,
    side: LabelSide,
    rect: Rect
  ) {
    ctx.font = `${(priority ? 11 : 10) / globalScale}px var(--font-body, sans-serif)`;
    ctx.fillStyle = resolveColor("var(--color-ink)");
    ctx.textAlign = side === "left" ? "right" : side === "right" ? "left" : "center";
    ctx.textBaseline = "middle";
    const x = side === "left" ? rect[2] : side === "right" ? rect[0] : (rect[0] + rect[2]) / 2;
    const y = (rect[1] + rect[3]) / 2;
    ctx.fillText(shortLabel(node.title), x, y);
  }

  /**
   * Tries each side in turn and draws at the first position that doesn't
   * collide with anything already claimed this frame (other labels, node
   * dots, link lines). Returns false only if literally every side collides
   * (dense-cluster edge case) — the label is then skipped rather than drawn
   * on top of something.
   */
  function placeLabel(
    node: any,
    ctx: CanvasRenderingContext2D,
    globalScale: number,
    priority: boolean
  ): boolean {
    for (const side of LABEL_SIDES) {
      const rect = computeLabelRect(node, ctx, globalScale, priority, side);
      if (claimLabelRect(rect)) {
        drawLabel(node, ctx, globalScale, priority, side, rect);
        return true;
      }
    }
    return false;
  }

  // Runs once per frame, before any node is drawn. Seeds the obstacle set
  // with every node's own dot and every visible link line, then reserves
  // label space for the hovered/selected node(s) so they get first pick of
  // position — all before any label-vs-label collision is considered.
  function onRenderFramePre(ctx: CanvasRenderingContext2D, globalScale: number) {
    labelRectsRef.current = [];
    lineSegmentsRef.current = [];

    for (const n of graphData.nodes as any[]) {
      if (n.x == null || n.y == null) continue;
      const r = nodeRadius(n);
      labelRectsRef.current.push([n.x - r, n.y - r, n.x + r, n.y + r]);
    }

    for (const l of graphData.links as any[]) {
      const s = typeof l.source === "string" ? nodeById.get(l.source) : l.source;
      const t = typeof l.target === "string" ? nodeById.get(l.target) : l.target;
      if (!s || !t || s.x == null || s.y == null || t.x == null || t.y == null) continue;
      lineSegmentsRef.current.push([s.x, s.y, t.x, t.y]);
    }

    for (const id of [hoverId, selectedId]) {
      if (!id) continue;
      const n = nodeById.get(id);
      if (!n || n.x == null || n.y == null) continue;
      placeLabel(n, ctx, globalScale, true);
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
      // Priority (hover/selected) labels are already placed in
      // onRenderFramePre (after obstacles were seeded, so they still dodge
      // every dot/line) — skip here to avoid drawing them a second time.
      if (isPriority) return;

      const isCandidate = globalScale > 2.5 || (highlightId != null && highlightNeighbors?.has(node.id));
      if (!isCandidate) return;

      placeLabel(node, ctx, globalScale, false);
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
        <CheckboxDropdown
          label="5Cs"
          options={FIVE_C_ORDER.map((c) => ({ key: c, label: FIVE_C_LABELS[c] }))}
          selected={fiveCFilter}
          onToggle={(key) => toggleFiveC(key as FiveC)}
          onClear={() => {
            hasAutoFittedRef.current = false;
            setFiveCFilter(new Set());
          }}
        />
        <CheckboxDropdown
          label="Trust signals"
          options={TRUST_SIGNAL_OPTIONS.map((o) => ({ key: o.key, label: o.label, group: o.group }))}
          selected={trustSignalFilter}
          onToggle={toggleTrustSignal}
          onClear={() => {
            hasAutoFittedRef.current = false;
            setTrustSignalFilter(new Set());
          }}
        />
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
        <button
          onClick={() => {
            hasAutoFittedRef.current = false;
            setTypeFilter(new Set(NODE_TYPE_ORDER));
            setStatusFilter("all");
            setFiveCFilter(new Set());
          }}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold text-ink/80 hover:bg-muted-surface"
        >
          Reset filters
        </button>
        <button
          onClick={() => setShowNodeList((v) => !v)}
          aria-expanded={showNodeList}
          aria-controls="graph-node-list"
          title="Browse and select nodes as a list — keyboard accessible"
          className="rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold text-ink/80 hover:bg-muted-surface"
        >
          {showNodeList ? "Hide node list" : "Node list"}
        </button>
        <span className="mono ml-auto text-xs text-muted-ink">
          {graphData.nodes.length} nodes · {graphData.links.length} edges
          {focusMode ? " (focused)" : ""}
        </span>
      </div>

      {showNodeList && (
        <div
          id="graph-node-list"
          className="mb-3 max-h-56 overflow-y-auto rounded-lg border border-border bg-card p-2"
        >
          {graphData.nodes.length === 0 ? (
            <p className="px-2 py-1 text-xs text-muted-ink">No nodes match the current filters.</p>
          ) : (
            <ul className="grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
              {graphData.nodes
                .slice()
                .sort((a, b) => a.title.localeCompare(b.title))
                .map((n) => (
                  <li key={n.id}>
                    <button
                      type="button"
                      onClick={() => selectNode(n.id === selectedId ? null : n.id)}
                      aria-pressed={n.id === selectedId}
                      className={`flex w-full items-center gap-1.5 truncate rounded-md px-2 py-1 text-left text-xs hover:bg-muted-surface ${
                        n.id === selectedId ? "bg-muted-surface font-semibold text-ink" : "text-ink/80"
                      }`}
                    >
                      <span className={`shrink-0 text-[0.6875rem] font-semibold ${NODE_TYPE_TEXT_CLASS[n.type]}`}>
                        {n.type}
                      </span>
                      <span className="truncate">{n.title}</span>
                    </button>
                  </li>
                ))}
            </ul>
          )}
        </div>
      )}

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
            // Low floor so zoomToFit ("Fit to view") can actually zoom out
            // far enough to fit the full ~250-node graph — a higher floor
            // (e.g. 0.55) silently clamps zoomToFit before it reaches the
            // bbox-fitting scale, making the button appear to do nothing.
            minZoom={0.05}
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
            width={graphWidth || undefined}
            height={620}
            cooldownTicks={100}
            backgroundColor="rgba(0,0,0,0)"
          />
        </div>

        <div className="min-w-0 rounded-lg border border-border bg-card p-4">
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
              <h3 className="mt-2 break-words text-sm font-semibold leading-snug text-ink">
                {selectedNode.title}
              </h3>
              <p className="mt-1 break-words text-xs text-muted-ink">
                {NODE_TYPE_LABELS[selectedNode.type]} · {selectedNode.curationStatus} ·{" "}
                {neighborsOf.get(selectedNode.id)?.size ?? 0} connection
                {(neighborsOf.get(selectedNode.id)?.size ?? 0) === 1 ? "" : "s"}
              </p>
              {getFiveCs(selectedNode).length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {getFiveCs(selectedNode).map((c) => (
                    <span
                      key={c}
                      className="inline-flex items-center rounded-full border border-border bg-muted-surface px-2 py-0.5 text-[0.625rem] font-semibold text-ink/70"
                    >
                      {FIVE_C_LABELS[c]}
                    </span>
                  ))}
                </div>
              )}
              {(() => {
                const summary = nodeSummary(selectedNode);
                return summary ? (
                  <p className="mt-3 break-words text-xs leading-relaxed text-ink/80">{summary}</p>
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

              {(() => {
                const neighborIds = Array.from(neighborsOf.get(selectedNode.id) ?? []);
                const neighborNodes = neighborIds
                  .map((id) => getNodeById(id))
                  .filter((n): n is GraphNode => !!n)
                  .sort((a, b) => a.title.localeCompare(b.title));
                if (neighborNodes.length === 0) return null;
                return (
                  <div className="mt-4 border-t border-border pt-3">
                    <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
                      Connected nodes ({neighborNodes.length})
                    </p>
                    <ul className="mt-2 max-h-72 space-y-1 overflow-y-auto">
                      {neighborNodes.map((n) => {
                        const isExpanded = expandedNeighbors.has(n.id);
                        const summary = isExpanded ? nodeSummary(n) : null;
                        return (
                          <li key={n.id} className="rounded-md border border-border">
                            <button
                              type="button"
                              onClick={() => toggleNeighborExpanded(n.id)}
                              aria-expanded={isExpanded}
                              className="flex w-full items-center gap-1.5 px-2 py-1.5 text-left text-xs hover:bg-muted-surface"
                            >
                              <span aria-hidden className="w-3 shrink-0 text-muted-ink">
                                {isExpanded ? "▾" : "▸"}
                              </span>
                              <span className={`shrink-0 text-[0.625rem] font-semibold ${NODE_TYPE_TEXT_CLASS[n.type]}`}>
                                {n.type}
                              </span>
                              <span className="min-w-0 truncate">{n.title}</span>
                            </button>
                            {isExpanded && (
                              <div className="border-t border-border px-2 py-2">
                                <p className="break-words text-xs leading-relaxed text-ink/80">
                                  {summary ?? "No summary available."}
                                </p>
                                <button
                                  type="button"
                                  onClick={() => selectNode(n.id)}
                                  className="mt-2 text-[0.6875rem] font-semibold text-forest hover:underline"
                                >
                                  Open this node →
                                </button>
                              </div>
                            )}
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                );
              })()}
            </div>
          ) : (
            <div className="text-xs text-muted-ink">
              <p className="font-semibold text-ink/80">How to read this graph</p>
              <ul className="mt-2 list-disc space-y-1.5 pl-4">
                <li>Chip color above = node type; dot size = number of connections.</li>
                <li>
                  The 5Cs dropdown filters by appraisal (Credibility, Clarity, Creativity, Care, Connectivity) —
                  most claims and evidence carry one or more; other node types usually don&apos;t.
                </li>
                <li>
                  The Trust signals dropdown filters by the same Openness/Rigor/Transparency/Integrity signals
                  shown on each source page — check any box to show nodes matching at least one.
                </li>
                <li>Hover a node to highlight it and its direct connections.</li>
                <li>Click a node to preview it here without leaving the graph.</li>
                <li>&quot;Focus this neighborhood&quot; isolates a node and its connections to cut clutter.</li>
                <li>Drag nodes to rearrange; scroll/pinch to zoom; &quot;Fit to view&quot; re-centers.</li>
                <li>
                  Press <kbd className="mono rounded border border-border bg-muted-surface px-1 py-0.5 text-[0.65rem]">⌘K</kbd>{" "}
                  (or Ctrl+K) any time to search all nodes by title, tag, or id.
                </li>
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

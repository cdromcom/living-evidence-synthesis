"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useMemo, useRef, useState, useCallback, useEffect } from "react";
import type { ForceGraphMethods, ForceGraphProps } from "react-force-graph-2d";
import type { GraphNode, GraphEdge, NodeType, ReproducibilityRisk, EvaluativeTask } from "@/lib/data";
import {
  NODE_TYPE_ORDER,
  NODE_TYPE_LABELS,
  FIVE_C_LABELS,
  getFiveCs,
  TASK_ORDER,
  TASK_LABELS,
  TASK_GROUPS,
  getEvaluativeTasks,
  getNodeById,
  TOP_STANDARD_LABELS,
  getTopSignals,
  VALIDITY_DOMAIN_ORDER,
  VALIDITY_DOMAIN_LABELS,
  getValiditySignals,
  getReportingCompliance,
  INTEGRITY_SIGNAL_ORDER,
  INTEGRITY_SIGNAL_LABELS,
  getIntegritySignals,
  getRepositoryCheck,
  getCodeCheck,
  getBaselineAdequacy,
  getTrainDevTestHygiene,
  getHumanBaselineComparability,
  getDataLeakageSignal,
  getPromptEngineering,
  getAblationExperiments,
  getConfidenceIntervals,
  getMultipleComparisonsCorrection,
  getChanceCorrectedMetrics,
  getSpinSignal,
  getAiWritingCheck,
  getCodeQualityFair,
  getDataQualityFair,
  getStatisticalPower,
  getStatisticalConsistency,
} from "@/lib/data";
import {
  NODE_TYPE_COLOR_VAR,
  NODE_TYPE_BG_CLASS,
  NODE_TYPE_BORDER_CLASS,
  NODE_TYPE_TEXT_CLASS,
  GRAPH_SELECT_NODE_EVENT,
} from "@/lib/ui";

// react-force-graph-2d's default export is generic (ForceGraphProps<NodeType,
// LinkType>); next/dynamic's own generic is what actually pins the node/link
// shape below back to FGNode/FGLink instead of collapsing to the library's
// untyped `{ [others: string]: any }` default. `ref` isn't part of
// ForceGraphProps itself (the library adds it separately via its own
// `FCwithRef` wrapper type, which `dynamic<P>` doesn't preserve), so it's
// added here to keep `ref={fgRef}` below typed too.
const ForceGraph2D = dynamic<
  ForceGraphProps<FGNode, FGLink> & {
    ref?: React.MutableRefObject<ForceGraphMethods<FGNode, FGLink> | undefined>;
  }
>(() => import("react-force-graph-2d"), {
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
// Once the simulation runs, react-force-graph replaces each link's
// source/target string in place with the actual FGNode it resolved to — the
// type reflects both states rather than casting through `any` at each call
// site that has to tell them apart.
type FGLink = { source: string | FGNode; target: string | FGNode; type: string };
// The canvas paint callbacks (nodeCanvasObject, nodePointerAreaPaint, and
// the label-placement helpers below) only ever run for a node the
// simulation has already positioned — x/y are required here rather than
// re-checked at every call site.
type PositionedFGNode = FGNode & { x: number; y: number };

function linkEndpointId(end: string | FGNode): string {
  return typeof end === "string" ? end : end.id;
}

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

// Mirrors every trust-signal chip shown on each SRC/EVD page (TopBadges.tsx
// + lib/qualityColumns.ts, the same catalog the Evidence Quality table's
// column picker draws from) — Openness (COS TOP standards + repo/code
// liveness checks), the five Rigor subrows (Validity, Design, Analyses,
// Reporting, Interpretation), Transparency (TRIPOD-LLM reporting
// compliance), and Integrity (disclosures). Extensibility is deliberately
// left out: those are unscored "not done yet" reminders, not real signals
// to filter by.
// The "did the paper address X" family of rigor checks (Step 6/6.b in the
// extraction Skill) — one checkbox per chip, labeled with exactly the
// chip's own on-page text (no colon/sublabel: the chip itself never shows
// its risk level as text either, only as the badge's dot color), testing
// the same "was this handled well" positive condition the pre-existing
// Openness/Integrity filters below already use.
const RIGOR_CHECK_DEFS: { id: string; label: string; group: string; getter: (n: GraphNode) => ReproducibilityRisk | "not-addressed" | null }[] = [
  { id: "data-repo-check", label: "Dataset check", group: "Openness", getter: getRepositoryCheck },
  { id: "code-check", label: "Code Check", group: "Openness", getter: getCodeCheck },
  { id: "baseline-adequacy", label: "Baseline Adequacy", group: "Rigor — Design", getter: getBaselineAdequacy },
  { id: "train-dev-test", label: "Train/Dev/Test Hygiene", group: "Rigor — Design", getter: getTrainDevTestHygiene },
  { id: "human-baseline", label: "Human-Baseline Comparability", group: "Rigor — Design", getter: getHumanBaselineComparability },
  { id: "data-leakage", label: "Data Leakage", group: "Rigor — Design", getter: getDataLeakageSignal },
  { id: "prompt-engineering", label: "Prompt Engineering", group: "Rigor — Design", getter: getPromptEngineering },
  { id: "ablation-experiments", label: "Ablation Experiment(s)", group: "Rigor — Design", getter: getAblationExperiments },
  { id: "confidence-intervals", label: "Confidence Intervals", group: "Rigor — Analyses", getter: getConfidenceIntervals },
  { id: "multiple-comparisons", label: "Multiple-Comparisons Correction", group: "Rigor — Analyses", getter: getMultipleComparisonsCorrection },
  { id: "chance-corrected-metrics", label: "Chance-Corrected Metrics", group: "Rigor — Analyses", getter: getChanceCorrectedMetrics },
  { id: "spin", label: "Non-Significant Result Spin", group: "Rigor — Interpretation", getter: getSpinSignal },
];

// Only Registration and Protocol get their own filter checkboxes here — Data
// and Code transparency have a newer, more specific equivalent already below
// (Dataset check / Code check, which test whether the claimed repo link is
// actually live, not just whether it was disclosed), so a bare "Data"/"Code"
// checkbox would just duplicate those.
const OPENNESS_FILTER_STANDARDS = ["study-registration", "study-protocol"] as const;

const TRUST_SIGNAL_OPTIONS: TrustSignalOption[] = [
  ...OPENNESS_FILTER_STANDARDS.map((standard) => ({
    key: `top:${standard}`,
    label: TOP_STANDARD_LABELS[standard],
    group: "Openness",
    test: (n: GraphNode) =>
      getTopSignals(n).some(
        (s) => s.standard === standard && (s.level === "level-1-disclosed" || s.level === "level-2-shared")
      ),
  })),
  ...RIGOR_CHECK_DEFS.map((def) => ({
    key: `check:${def.id}`,
    label: def.label,
    group: def.group,
    test: (n: GraphNode) => def.getter(n) === "low-risk",
  })),
  {
    key: "code-quality-fair",
    label: "Code Quality",
    group: "Openness",
    test: (n: GraphNode) => (getCodeQualityFair(n) ?? 0) >= 3,
  },
  {
    key: "data-quality-fair",
    label: "Data Quality",
    group: "Openness",
    // Same ~60%-of-scale "meets baseline" bar as Code Quality's >=3/5.
    test: (n: GraphNode) => (getDataQualityFair(n) ?? 0) >= 15,
  },
  // One checkbox per Validity domain — matches the four separate chips
  // (Construct validity, Internal validity, External validity, Statistical
  // rigor) actually shown under Rigor > Validity on SRC pages, rather than
  // three generic risk-level buckets aggregated across all four.
  ...VALIDITY_DOMAIN_ORDER.map((domain) => ({
    key: `validity:${domain}`,
    label: VALIDITY_DOMAIN_LABELS[domain],
    group: "Rigor — Validity",
    test: (n: GraphNode) => getValiditySignals(n).some((v) => v.domain === domain && v.risk === "low-risk"),
  })),
  {
    key: "statistical-power",
    label: "Statistical Power",
    group: "Rigor — Analyses",
    test: (n: GraphNode) => getStatisticalPower(n) === "adequate",
  },
  {
    key: "statistic-accuracy",
    label: "Statistic Accuracy",
    group: "Rigor — Reporting",
    test: (n: GraphNode) => getStatisticalConsistency(n) === "consistent",
  },
  // Ranges match the actual tripod-llm/compliance/* classification rule
  // used to hand-score every source (Skill-references.md): high >=80%,
  // moderate 60-79%, low <60%.
  {
    key: "reporting:low",
    label: "low reporting — <60%",
    group: "Transparency",
    test: (n: GraphNode) => getReportingCompliance(n.id)?.level === "low",
  },
  {
    key: "reporting:moderate",
    label: "moderate reporting — 60–79%",
    group: "Transparency",
    test: (n: GraphNode) => getReportingCompliance(n.id)?.level === "moderate",
  },
  {
    key: "reporting:high",
    label: "high reporting — ≥80%",
    group: "Transparency",
    test: (n: GraphNode) => getReportingCompliance(n.id)?.level === "high",
  },
  ...INTEGRITY_SIGNAL_ORDER.map((kind) => ({
    key: `integrity:${kind}`,
    label: INTEGRITY_SIGNAL_LABELS[kind],
    group: "Integrity",
    test: (n: GraphNode) =>
      getIntegritySignals(n).some((s) => s.kind === kind && (s.level === "disclosed" || s.level === "partial")),
  })),
  {
    key: "check:ai-writing-check",
    label: "AI Writing Check",
    group: "Integrity",
    test: (n: GraphNode) => getAiWritingCheck(n) === "low-risk",
  },
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
                    <label
                      className={`flex cursor-pointer items-center gap-2 rounded px-1 py-0.5 text-xs text-ink/80 hover:bg-muted-surface${
                        group ? " lowercase" : ""
                      }`}
                    >
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
  const fgRef = useRef<ForceGraphMethods<FGNode, FGLink> | undefined>(undefined);
  const containerRef = useRef<HTMLDivElement>(null);
  const [typeFilter, setTypeFilter] = useState<Set<NodeType>>(
    new Set(NODE_TYPE_ORDER)
  );
  const [statusFilter, setStatusFilter] = useState<string>("all");
  // Empty set = filter inactive (show everything, including nodes with no
  // Empty set means inactive; non-empty is OR'd across
  // whichever trust-signal checkboxes (Openness/Rigor/Transparency/Integrity)
  // are selected — see TRUST_SIGNAL_OPTIONS.
  const [trustSignalFilter, setTrustSignalFilter] = useState<Set<string>>(new Set());
  // Same empty-set-means-inactive convention — which evaluative task
  // (risk-of-bias assessment, novelty assessment, etc.) a finding is
  // ABOUT, as distinct from the Trust signals filter above (which rates
  // how trustworthy the source study itself is).
  const [taskFilter, setTaskFilter] = useState<Set<EvaluativeTask>>(new Set());
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
  // Height is fixed at 620 in the page flow, but in fullscreen the container is
  // sized by flex rather than by its content, so it can be measured.
  const [measuredHeight, setMeasuredHeight] = useState(0);
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const box = entries[0].contentRect;
      const w = Math.round(box.width);
      const h = Math.round(box.height);
      setGraphWidth((prev) => (prev === w ? prev : w));
      setMeasuredHeight((prev) => (prev === h ? prev : h));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // Fullscreen puts the whole explorer — filter chips, dropdowns and the
  // right-hand panel included — into the fullscreen element, so nothing the
  // reader was using disappears when the canvas gets bigger.
  const shellRef = useRef<HTMLDivElement>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  useEffect(() => {
    const onChange = () => setIsFullscreen(document.fullscreenElement === shellRef.current);
    document.addEventListener("fullscreenchange", onChange);
    return () => document.removeEventListener("fullscreenchange", onChange);
  }, []);
  async function toggleFullscreen() {
    hasAutoFittedRef.current = false; // re-fit to the new viewport
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await shellRef.current?.requestFullscreen();
    } catch {
      // Safari on iOS and some embedded browsers refuse; leave the page as-is
      // rather than half-applying a fullscreen layout.
    }
  }
  const graphHeight = isFullscreen && measuredHeight > 0 ? measuredHeight : 620;

  // Panel width is draggable. Kept in localStorage so the choice survives
  // navigating between the graph and a node page and back, which is the whole
  // point of widening it — reading a long summary without leaving the graph.
  const PANEL_MIN = 220;
  const PANEL_MAX = 560;
  const gridRef = useRef<HTMLDivElement>(null);
  const [panelWidth, setPanelWidth] = useState(280);
  useEffect(() => {
    // Applied a frame after mount rather than synchronously: the server has no
    // localStorage, so reading it during render would hydrate to a different
    // width than the markup was built with.
    const id = requestAnimationFrame(() => {
      try {
        const saved = Number(window.localStorage.getItem("graph:panelWidth"));
        if (Number.isFinite(saved) && saved >= PANEL_MIN && saved <= PANEL_MAX) setPanelWidth(saved);
      } catch {
        // private mode or blocked storage — the default width is fine
      }
    });
    return () => cancelAnimationFrame(id);
  }, []);
  const commitPanelWidth = useCallback((w: number) => {
    setPanelWidth(w);
    try {
      window.localStorage.setItem("graph:panelWidth", String(w));
    } catch {
      // nothing to do; the width still applies for this visit
    }
  }, []);

  const dragStateRef = useRef<{ startX: number; startW: number } | null>(null);
  const clampWidth = useCallback((w: number) => {
    const grid = gridRef.current?.getBoundingClientRect().width ?? 0;
    // Never let the panel squeeze the canvas below a usable width.
    const max = Math.min(PANEL_MAX, Math.max(PANEL_MIN, grid - 360));
    return Math.round(Math.min(max, Math.max(PANEL_MIN, w)));
  }, []);

  function onHandlePointerDown(e: React.PointerEvent<HTMLDivElement>) {
    e.preventDefault();
    // Record the drag before capturing: setPointerCapture throws if the pointer
    // is no longer active, and letting that abort the handler would leave the
    // splitter looking grabbable but doing nothing.
    dragStateRef.current = { startX: e.clientX, startW: panelWidth };
    try {
      (e.target as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      // Without capture the drag still tracks while the pointer stays on the
      // handle; it just stops early if it leaves.
    }
  }
  function onHandlePointerMove(e: React.PointerEvent<HTMLDivElement>) {
    const st = dragStateRef.current;
    if (!st) return;
    // Dragging left widens the panel, so the delta is inverted.
    setPanelWidth(clampWidth(st.startW - (e.clientX - st.startX)));
  }
  function endHandleDrag(e: React.PointerEvent<HTMLDivElement>) {
    if (!dragStateRef.current) return;
    dragStateRef.current = null;
    try {
      (e.target as HTMLElement).releasePointerCapture?.(e.pointerId);
    } catch {
      // already released
    }
    commitPanelWidth(clampWidth(panelWidth));
  }
  function onHandleKeyDown(e: React.KeyboardEvent<HTMLDivElement>) {
    const step = e.shiftKey ? 48 : 16;
    if (e.key === "ArrowLeft") commitPanelWidth(clampWidth(panelWidth + step));
    else if (e.key === "ArrowRight") commitPanelWidth(clampWidth(panelWidth - step));
    else if (e.key === "Home") commitPanelWidth(clampWidth(PANEL_MAX));
    else if (e.key === "End") commitPanelWidth(clampWidth(PANEL_MIN));
    else return;
    e.preventDefault();
  }

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
            (trustSignalFilter.size === 0 ||
              TRUST_SIGNAL_OPTIONS.filter((o) => trustSignalFilter.has(o.key)).some((o) => o.test(n))) &&
            (taskFilter.size === 0 || getEvaluativeTasks(n).some((t) => taskFilter.has(t)))
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
  }, [nodes, edges, typeFilter, statusFilter, trustSignalFilter, taskFilter]);

  // Adjacency, built once per filtered graph — powers both hover/selection
  // highlighting and focus (ego-network) mode.
  const neighborsOf = useMemo(() => {
    const map = new Map<string, Set<string>>();
    for (const l of baseGraphData.links) {
      const s = linkEndpointId(l.source);
      const t = linkEndpointId(l.target);
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
        const s = linkEndpointId(l.source);
        const t = linkEndpointId(l.target);
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

  function toggleTrustSignal(key: string) {
    hasAutoFittedRef.current = false;
    setTrustSignalFilter((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  function toggleTask(t: EvaluativeTask) {
    hasAutoFittedRef.current = false;
    setTaskFilter((prev) => {
      const next = new Set(prev);
      if (next.has(t)) next.delete(t);
      else next.add(t);
      return next;
    });
  }

  function clearTrustSignalFilter() {
    hasAutoFittedRef.current = false;
    setTrustSignalFilter(new Set());
  }

  function clearTaskFilter() {
    hasAutoFittedRef.current = false;
    setTaskFilter(new Set());
  }

  function changeStatusFilter(value: string) {
    hasAutoFittedRef.current = false;
    setStatusFilter(value);
  }

  function resetAllFilters() {
    hasAutoFittedRef.current = false;
    setTypeFilter(new Set(NODE_TYPE_ORDER));
    setStatusFilter("all");
    setTrustSignalFilter(new Set());
    setTaskFilter(new Set());
  }

  function toggleFocusMode() {
    hasAutoFittedRef.current = false;
    setFocusMode((f) => !f);
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
    // A plain non-reactive "run once" guard — deliberately a ref, not state,
    // since turning it into state would re-render on every settle instead of
    // only the first. onEngineStop is a callback out of force-graph's own
    // internal d3-force loop rather than a DOM event, which the compiler
    // can't classify as a safe context for mutating a ref the way it does
    // toggleType/toggleTask/etc. above (identical pattern, not flagged there).
    // eslint-disable-next-line react-hooks/immutability
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
    node: PositionedFGNode,
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
    node: FGNode,
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
    node: PositionedFGNode,
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

    for (const n of graphData.nodes) {
      if (n.x == null || n.y == null) continue;
      const r = nodeRadius(n);
      labelRectsRef.current.push([n.x - r, n.y - r, n.x + r, n.y + r]);
    }

    for (const l of graphData.links) {
      const s = typeof l.source === "string" ? nodeById.get(l.source) : l.source;
      const t = typeof l.target === "string" ? nodeById.get(l.target) : l.target;
      if (!s || !t || s.x == null || s.y == null || t.x == null || t.y == null) continue;
      lineSegmentsRef.current.push([s.x, s.y, t.x, t.y]);
    }

    for (const id of [hoverId, selectedId]) {
      if (!id) continue;
      const n = nodeById.get(id);
      if (!n || n.x == null || n.y == null) continue;
      // Just checked above — TS doesn't narrow FGNode's optional x/y into
      // PositionedFGNode's required ones from a `== null` guard on its own.
      placeLabel(n as PositionedFGNode, ctx, globalScale, true);
    }
  }

  const nodeCanvasObject = useCallback(
    // The library's own callback type declares x/y optional (true before the
    // first simulation tick) — this paint callback only ever runs after,
    // when they're always set.
    (rawNode: FGNode, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const node = rawNode as PositionedFGNode;
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
    // placeLabel (and the computeLabelRect/drawLabel/claimLabelRect it calls)
    // doesn't close over any reactive component state — only refs
    // (labelRectsRef, lineSegmentsRef) and its own arguments — so it's
    // effectively stable across renders despite being redeclared each one;
    // omitted deliberately rather than listed as a dependency that would
    // always "change".
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [hoverId, selectedId, highlightId, highlightNeighbors, nodeById]
  );

  const selectedNode = selectedId ? getNodeById(selectedId) : undefined;

  return (
    <div
      ref={shellRef}
      className={isFullscreen ? "flex h-full flex-col overflow-auto bg-paper p-4" : undefined}
    >
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
          label="Trust signals"
          options={TRUST_SIGNAL_OPTIONS.map((o) => ({ key: o.key, label: o.label, group: o.group }))}
          selected={trustSignalFilter}
          onToggle={toggleTrustSignal}
          onClear={clearTrustSignalFilter}
        />
        <CheckboxDropdown
          label="Evaluative task"
          options={TASK_ORDER.map((t) => ({ key: t, label: TASK_LABELS[t], group: TASK_GROUPS[t] }))}
          selected={taskFilter}
          onToggle={(key) => toggleTask(key as EvaluativeTask)}
          onClear={clearTaskFilter}
        />
        <span className="mx-1 h-4 w-px bg-border" />
        <select
          value={statusFilter}
          onChange={(e) => changeStatusFilter(e.target.value)}
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
          onClick={resetAllFilters}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs font-semibold text-ink/80 hover:bg-muted-surface"
        >
          Reset filters
        </button>
        <button
          onClick={() => setShowNodeList((v) => !v)}
          aria-expanded={showNodeList}
          aria-controls="graph-node-list"
          title="Browse and select nodes as a list, keyboard accessible"
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

      <div
        ref={gridRef}
        style={{ ["--panel-w" as string]: `${panelWidth}px` }}
        className={`grid gap-3 lg:grid-cols-[minmax(0,1fr)_0.5rem_var(--panel-w)] ${
          isFullscreen ? "min-h-0 flex-1" : ""
        }`}
      >
        <div
          ref={containerRef}
          // In page flow the canvas is a fixed 620 tall, so the box must not
          // stretch to a taller panel or it grows an empty band beneath the
          // drawing. In fullscreen the row height is the viewport and the canvas
          // is measured to fill it, so stretching is exactly what is wanted.
          className={`relative overflow-hidden rounded-lg border border-border bg-card ${
            isFullscreen ? "" : "self-start"
          }`}
        >
          <ForceGraph2D
            ref={fgRef}
            graphData={graphData}
            nodeId="id"
            nodeLabel={(n: FGNode) => `${NODE_TYPE_LABELS[n.type]}: ${n.title}`}
            nodeCanvasObject={nodeCanvasObject}
            nodePointerAreaPaint={(rawNode: FGNode, color: string, ctx: CanvasRenderingContext2D) => {
              const node = rawNode as PositionedFGNode;
              const r = nodeRadius(node);
              ctx.fillStyle = color;
              ctx.beginPath();
              ctx.arc(node.x, node.y, r + 2, 0, 2 * Math.PI, false);
              ctx.fill();
            }}
            onNodeHover={(n: FGNode | null) => setHoverId(n ? n.id : null)}
            onNodeClick={(n: FGNode) => selectNode(n.id === selectedId ? null : n.id)}
            onBackgroundClick={() => selectNode(null)}
            onEngineStop={handleEngineStop}
            // Low floor so zoomToFit ("Fit to view") can actually zoom out
            // far enough to fit the full ~250-node graph — a higher floor
            // (e.g. 0.55) silently clamps zoomToFit before it reaches the
            // bbox-fitting scale, making the button appear to do nothing.
            minZoom={0.05}
            onRenderFramePre={onRenderFramePre}
            linkColor={(l: FGLink) => {
              const s = linkEndpointId(l.source);
              const t = linkEndpointId(l.target);
              const touchesHighlight = highlightId && (s === highlightId || t === highlightId);
              return touchesHighlight ? "rgba(107,102,96,0.85)" : "rgba(107,102,96,0.18)";
            }}
            linkWidth={(l: FGLink) => {
              const s = linkEndpointId(l.source);
              const t = linkEndpointId(l.target);
              const touchesHighlight = highlightId && (s === highlightId || t === highlightId);
              return touchesHighlight ? 1.4 : 0.5;
            }}
            linkDirectionalArrowLength={3}
            linkDirectionalArrowRelPos={1}
            width={graphWidth || undefined}
            height={graphHeight}
            cooldownTicks={100}
            backgroundColor="rgba(0,0,0,0)"
          />

          {/* Sits over the canvas rather than in the toolbar: it belongs to the
              graph, and in fullscreen the toolbar is still on screen, so the
              control stays where the reader last saw it. Bottom-right keeps it
              clear of the node tooltip, which follows the cursor. */}
          <div className="absolute bottom-3 right-3 z-10 flex items-center gap-1.5">
          <button
            type="button"
            onClick={zoomToFit}
            title="Fit to view"
            className="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-white text-ink/70 shadow-sm transition-colors hover:border-forest/50 hover:text-forest focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-forest"
          >
            <span className="sr-only">Fit the whole graph in view</span>
            <svg
              width="15"
              height="15"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden
            >
              {/* arrows pulling inward: gather the graph back into the frame */}
              <path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" />
              <path d="M9.5 9.5l-4-4M14.5 9.5l4-4M9.5 14.5l-4 4M14.5 14.5l4 4" />
            </svg>
          </button>
          <button
            type="button"
            onClick={toggleFullscreen}
            aria-pressed={isFullscreen}
            title={isFullscreen ? "Exit full screen" : "Full screen"}
            className="flex h-8 w-8 items-center justify-center rounded-md border border-border bg-white text-ink/70 shadow-sm transition-colors hover:border-forest/50 hover:text-forest focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-forest"
          >
            <span className="sr-only">
              {isFullscreen ? "Exit full screen" : "View the graph full screen"}
            </span>
            <svg
              width="15"
              height="15"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden
            >
              {isFullscreen ? (
                <path d="M9 3v6H3M15 21v-6h6M3 15h6v6M21 9h-6V3" />
              ) : (
                <path d="M3 9V3h6M21 9V3h-6M3 15v6h6M21 15v6h-6" />
              )}
            </svg>
          </button>
          </div>
        </div>

        {/* Splitter. Below lg the two panes stack, so it is hidden there —
            there is no horizontal space to trade. */}
        <div
          role="separator"
          aria-orientation="vertical"
          aria-label="Resize the detail panel"
          aria-valuenow={panelWidth}
          aria-valuemin={PANEL_MIN}
          aria-valuemax={PANEL_MAX}
          tabIndex={0}
          onPointerDown={onHandlePointerDown}
          onPointerMove={onHandlePointerMove}
          onPointerUp={endHandleDrag}
          onPointerCancel={endHandleDrag}
          onKeyDown={onHandleKeyDown}
          className="group hidden cursor-col-resize touch-none select-none items-center justify-center rounded focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-forest lg:flex"
        >
          <span className="h-10 w-[3px] rounded-full bg-border transition-colors group-hover:bg-forest/60" />
        </div>

        <div className="flex min-h-0 min-w-0 flex-col rounded-lg border border-border bg-card p-4">
          {selectedNode ? (
            <div className="flex min-h-0 flex-1 flex-col">
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
                  onClick={toggleFocusMode}
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
                  <div className="mt-4 flex min-h-0 flex-1 flex-col border-t border-border pt-3">
                    <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
                      Connected nodes ({neighborNodes.length})
                    </p>
                    {/* Fills whatever height the panel has left rather than a
                        fixed 18rem, so the list only scrolls once it genuinely
                        outgrows the panel. */}
                    <ul className="mt-2 min-h-0 flex-1 space-y-1 overflow-y-auto">
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
                  The Trust signals dropdown filters by the same Openness/Rigor/Transparency/Integrity signals
                  shown on each source page. Check any box to show nodes matching at least one.
                </li>
                <li>
                  The Evaluative task dropdown is different: it filters Evidence/Claim/Pattern nodes by
                  what capability the finding is <em>about</em> (e.g. risk-of-bias assessment, novelty
                  assessment) &mdash; not by how trustworthy that finding is.
                </li>
                <li>Hover a node to highlight it and its direct connections.</li>
                <li>Click a node to preview it here without leaving the graph.</li>
                <li>&quot;Focus this neighborhood&quot; isolates a node and its connections to cut clutter.</li>
                <li>Drag nodes to rearrange; scroll/pinch to zoom; the fit-to-view icon over the canvas re-centers.</li>
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

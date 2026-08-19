import graphData from "./graph-data.generated.json";

export type NodeType = "QUE" | "CLM" | "EVD" | "CVT" | "SRC" | "EP";

export type GraphNode = {
  id: string;
  type: NodeType;
  typeLabel: string;
  title: string;
  filename: string;
  shortLabel: string;
  curationStatus: string;
  tags: string[];
  created: string | null;
  updated: string | null;
  extras: Record<string, unknown>;
  bodyMarkdown: string;
};

export type EdgeType =
  | "addresses"
  | "relatesTo"
  | "supports"
  | "qualifies"
  | "derivedFrom"
  | "instantiates"
  | "mentions";

export type GraphEdge = {
  type: EdgeType;
  from: string;
  to: string;
};

const data = graphData as { nodes: GraphNode[]; edges: GraphEdge[] };

export const ALL_NODES: GraphNode[] = data.nodes;
export const ALL_EDGES: GraphEdge[] = data.edges;

const nodeById = new Map(ALL_NODES.map((n) => [n.id, n]));

export function getNodeById(id: string): GraphNode | undefined {
  return nodeById.get(id);
}

export function getAllNodes(): GraphNode[] {
  return ALL_NODES;
}

export function getNodesByType(type: NodeType): GraphNode[] {
  return ALL_NODES.filter((n) => n.type === type);
}

export function getInboundEdges(id: string): GraphEdge[] {
  return ALL_EDGES.filter((e) => e.to === id);
}

export function getOutboundEdges(id: string): GraphEdge[] {
  return ALL_EDGES.filter((e) => e.from === id);
}

export function getDegree(id: string): number {
  return ALL_EDGES.filter((e) => e.from === id || e.to === id).length;
}

export const NODE_TYPE_ORDER: NodeType[] = ["QUE", "CLM", "EVD", "CVT", "SRC", "EP"];

export const NODE_TYPE_LABELS: Record<NodeType, string> = {
  QUE: "Question",
  CLM: "Claim",
  EVD: "Evidence",
  CVT: "Caveat",
  SRC: "Source",
  EP: "Evidence Pattern",
};

/**
 * "5Cs" appraisal dimensions, authored as vault frontmatter tags
 * (e.g. `5c/credibility`) and copied verbatim into node.tags by
 * scripts/build-graph.mjs. A node can carry more than one.
 */
export const FIVE_C_ORDER = [
  "credibility",
  "clarity",
  "creativity",
  "care",
  "connectivity",
] as const;
export type FiveC = (typeof FIVE_C_ORDER)[number];

export const FIVE_C_LABELS: Record<FiveC, string> = {
  credibility: "Credibility",
  clarity: "Clarity",
  creativity: "Creativity",
  care: "Care (ethics)",
  connectivity: "Connectivity",
};

const FIVE_C_TAG_PREFIX = "5c/";

export function getFiveCs(node: Pick<GraphNode, "tags">): FiveC[] {
  const known: readonly string[] = FIVE_C_ORDER;
  return node.tags
    .filter((t) => t.startsWith(FIVE_C_TAG_PREFIX))
    .map((t) => t.slice(FIVE_C_TAG_PREFIX.length))
    .filter((c): c is FiveC => known.includes(c));
}

/**
 * COS TOP (Transparency and Openness Promotion) Guidelines standards,
 * https://www.cos.io/initiatives/top-guidelines — the four covered here are
 * derived from data already authored in each SRC file's own TRIPOD-LLM
 * reporting table (items 14c–14f). TOP defines three levels (1 Disclosed,
 * 2 Shared and Cited, 3 Certified); we only ever assign 1 or 2 here, since
 * Level 3 requires independent verification we haven't performed.
 */
export const TOP_STANDARD_ORDER = [
  "data-transparency",
  "code-transparency",
  "study-protocol",
  "study-registration",
] as const;
export type TopStandard = (typeof TOP_STANDARD_ORDER)[number];

export const TOP_STANDARD_LABELS: Record<TopStandard, string> = {
  "data-transparency": "Data Transparency",
  "code-transparency": "Analytic Code Transparency",
  "study-protocol": "Study Protocol",
  "study-registration": "Study Registration",
};

export type TopLevel = "level-2-shared" | "level-1-disclosed" | "not-disclosed" | "not-applicable";

export const TOP_LEVEL_LABELS: Record<TopLevel, string> = {
  "level-2-shared": "Level 2 — Shared and Cited",
  "level-1-disclosed": "Level 1 — Disclosed",
  "not-disclosed": "Not Disclosed",
  "not-applicable": "Not Applicable",
};

export type TopSignal = { standard: TopStandard; level: TopLevel };

const TOP_TAG_PREFIX = "top/";

export function getTopSignals(node: Pick<GraphNode, "tags">): TopSignal[] {
  const knownStandards: readonly string[] = TOP_STANDARD_ORDER;
  const knownLevels: readonly string[] = Object.keys(TOP_LEVEL_LABELS);
  const out: TopSignal[] = [];
  for (const tag of node.tags) {
    if (!tag.startsWith(TOP_TAG_PREFIX)) continue;
    const rest = tag.slice(TOP_TAG_PREFIX.length);
    const slash = rest.indexOf("/");
    if (slash === -1) continue;
    const standard = rest.slice(0, slash);
    const level = rest.slice(slash + 1);
    if (knownStandards.includes(standard) && knownLevels.includes(level)) {
      out.push({ standard: standard as TopStandard, level: level as TopLevel });
    }
  }
  return TOP_STANDARD_ORDER.filter((s) => out.some((o) => o.standard === s)).map(
    (s) => out.find((o) => o.standard === s)!
  );
}

/**
 * Source-level reproducibility risk, from each SRC file's Critical
 * Appraisal table (Reproducibility domain: 🟢/🟡/🔴). Distinct from TOP's
 * own "Computational Transparency" verification standard, which requires an
 * independent party to actually re-run the study — this is a retrospective
 * risk rating, not a verified reproduction.
 */
export type ReproducibilityRisk = "low-risk" | "some-concerns" | "high-risk";

export const REPRODUCIBILITY_RISK_LABELS: Record<ReproducibilityRisk, string> = {
  "low-risk": "Low risk",
  "some-concerns": "Some concerns",
  "high-risk": "High risk",
};

export function getReproducibilityRisk(node: Pick<GraphNode, "tags">): ReproducibilityRisk | null {
  const prefix = "trust/reproducibility/";
  const tag = node.tags.find((t) => t.startsWith(prefix));
  if (!tag) return null;
  const risk = tag.slice(prefix.length);
  return risk in REPRODUCIBILITY_RISK_LABELS ? (risk as ReproducibilityRisk) : null;
}

export const EDGE_TYPE_LABELS: Record<EdgeType, string> = {
  addresses: "Addresses",
  relatesTo: "Relates to",
  supports: "Supports",
  qualifies: "Qualifies",
  derivedFrom: "Derived from",
  instantiates: "Instantiates",
  mentions: "Mentions",
};

export function getCounts(): Record<NodeType, number> {
  const counts = { QUE: 0, CLM: 0, EVD: 0, CVT: 0, SRC: 0, EP: 0 } as Record<
    NodeType,
    number
  >;
  for (const n of ALL_NODES) counts[n.type]++;
  return counts;
}

/** Claims ranked by number of supporting EVD edges (EVD --supports--> CLM). */
export function getBestSupportedClaims(limit = 6) {
  const supportCounts = new Map<string, number>();
  for (const e of ALL_EDGES) {
    if (e.type === "supports") {
      const target = getNodeById(e.to);
      if (target?.type === "CLM") {
        supportCounts.set(e.to, (supportCounts.get(e.to) || 0) + 1);
      }
    }
  }
  return Array.from(supportCounts.entries())
    .map(([id, count]) => ({ node: getNodeById(id)!, supportCount: count }))
    .filter((x) => x.node)
    .sort((a, b) => b.supportCount - a.supportCount)
    .slice(0, limit);
}

/** Curation status distribution per node type, for the /review dashboard. */
export function getCurationStatusMatrix(): Record<
  NodeType,
  Record<string, number>
> {
  const matrix = {} as Record<NodeType, Record<string, number>>;
  for (const t of NODE_TYPE_ORDER) matrix[t] = {};
  for (const n of ALL_NODES) {
    matrix[n.type][n.curationStatus] = (matrix[n.type][n.curationStatus] || 0) + 1;
  }
  return matrix;
}

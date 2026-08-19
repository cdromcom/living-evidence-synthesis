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

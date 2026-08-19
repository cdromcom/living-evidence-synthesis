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

/**
 * The other four domains of each SRC file's Critical Appraisal table
 * (Construct/Internal/External validity, Statistical rigor — same
 * 🟢/🟡/🔴 scale as Reproducibility, and the same `appraisal/*` tag
 * namespace already used per-EVD elsewhere in the vault, just applied here
 * at the whole-paper level).
 */
export const VALIDITY_DOMAIN_ORDER = [
  "construct-validity",
  "internal-validity",
  "external-validity",
  "statistical-rigor",
] as const;
export type ValidityDomain = (typeof VALIDITY_DOMAIN_ORDER)[number];

export const VALIDITY_DOMAIN_LABELS: Record<ValidityDomain, string> = {
  "construct-validity": "Construct validity",
  "internal-validity": "Internal validity",
  "external-validity": "External validity",
  "statistical-rigor": "Statistical rigor",
};

export type ValiditySignal = { domain: ValidityDomain; risk: ReproducibilityRisk };

const APPRAISAL_TAG_PREFIX = "appraisal/";

export function getValiditySignals(node: Pick<GraphNode, "tags">): ValiditySignal[] {
  const knownDomains: readonly string[] = VALIDITY_DOMAIN_ORDER;
  const knownRisks: readonly string[] = Object.keys(REPRODUCIBILITY_RISK_LABELS);
  const out: ValiditySignal[] = [];
  for (const tag of node.tags) {
    if (!tag.startsWith(APPRAISAL_TAG_PREFIX)) continue;
    const rest = tag.slice(APPRAISAL_TAG_PREFIX.length);
    const slash = rest.indexOf("/");
    if (slash === -1) continue;
    const domain = rest.slice(0, slash);
    const risk = rest.slice(slash + 1);
    if (knownDomains.includes(domain) && knownRisks.includes(risk)) {
      out.push({ domain: domain as ValidityDomain, risk: risk as ReproducibilityRisk });
    }
  }
  return VALIDITY_DOMAIN_ORDER.filter((d) => out.some((o) => o.domain === d)).map(
    (d) => out.find((o) => o.domain === d)!
  );
}

/**
 * NIH/NINDS-style study-design rigor signals
 * (ninds.nih.gov .../maximizing-data-transparency-rigor-icons). Unlike the
 * TOP/appraisal tags above, these two aren't extracted from a structured
 * table row — no SRC file has one for sample-size justification or
 * exploratory/confirmatory framing. Grounded instead in direct textual
 * evidence checked across the whole corpus: every "sample size"/"power
 * analysis" mention in all 27 files is a caveat about its ABSENCE, and none
 * of the 27 are registered, protocolled, or claim a confirmatory
 * pre-specified hypothesis — one even says its own result is "suggestive,
 * not confirmatory." So every paper here reads as exploratory/
 * hypothesis-generating with no a priori sample-size justification.
 */
export type SampleSizeEstimation = "done" | "not-done";
export type StudyType = "exploratory" | "confirmatory";

export function getSampleSizeEstimation(node: Pick<GraphNode, "tags">): SampleSizeEstimation | null {
  if (node.tags.includes("rigor/sample-size-estimation/done")) return "done";
  if (node.tags.includes("rigor/sample-size-estimation/not-done")) return "not-done";
  return null;
}

export function getStudyType(node: Pick<GraphNode, "tags">): StudyType | null {
  if (node.tags.includes("rigor/study-type/exploratory")) return "exploratory";
  if (node.tags.includes("rigor/study-type/confirmatory")) return "confirmatory";
  return null;
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

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
 * Evaluative Task taxonomy — what research-evaluation capability a finding
 * is *about* (e.g. "risk-of-bias assessment", "novelty assessment"), as
 * distinct from the appraisal/* tags above (which rate how trustworthy the
 * *source study itself* is). Only EVD/CLM/EP nodes carry these, since only
 * they represent a specific finding about LLM performance on some task.
 * Grouped by the 5C branch each leaf belongs to, with a sixth "Cross-cutting"
 * bucket for findings about the evaluator's general behavior (prompt
 * sensitivity, cost, fine-tuning) rather than one specific evaluative task —
 * added 2026-08 per advisor feedback distinguishing "how good is this study"
 * from "what does the evidence say about LLMs doing X".
 */
export const TASK_ORDER = [
  "risk-of-bias-assessment",
  "reporting-compliance-checking",
  "causal-inference-judgment",
  "decision-judgment",
  "error-detection",
  "review-generation",
  "extraction-fidelity",
  "novelty-assessment",
  "ethics-irb-review",
  "citation-integrity-checking",
  "prompt-sensitivity",
  "fine-tuning-effect",
  "cost-scalability",
  "modality-limitation",
  "rare-class-reliability",
  "aggregate-vs-instance-validity",
] as const;
export type EvaluativeTask = (typeof TASK_ORDER)[number];

export const TASK_LABELS: Record<EvaluativeTask, string> = {
  "risk-of-bias-assessment": "Risk-of-bias assessment",
  "reporting-compliance-checking": "Reporting-guideline compliance",
  "causal-inference-judgment": "Causal-inference judgment",
  "decision-judgment": "Holistic decision judgment",
  "error-detection": "Error & limitation detection",
  "review-generation": "Review generation & feedback",
  "extraction-fidelity": "Extraction fidelity",
  "novelty-assessment": "Novelty assessment",
  "ethics-irb-review": "Ethics & IRB review",
  "citation-integrity-checking": "Citation integrity checking",
  "prompt-sensitivity": "Prompt sensitivity",
  "fine-tuning-effect": "Fine-tuning effect",
  "cost-scalability": "Cost & scalability",
  "modality-limitation": "Modality limitation",
  "rare-class-reliability": "Rare-class reliability",
  "aggregate-vs-instance-validity": "Aggregate-vs-instance validity",
};

export const TASK_GROUPS: Record<EvaluativeTask, string> = {
  "risk-of-bias-assessment": "Credibility",
  "reporting-compliance-checking": "Credibility",
  "causal-inference-judgment": "Credibility",
  "decision-judgment": "Credibility",
  "error-detection": "Credibility",
  "review-generation": "Credibility",
  "extraction-fidelity": "Clarity",
  "novelty-assessment": "Creativity",
  "ethics-irb-review": "Care",
  "citation-integrity-checking": "Connectivity",
  "prompt-sensitivity": "Cross-cutting",
  "fine-tuning-effect": "Cross-cutting",
  "cost-scalability": "Cross-cutting",
  "modality-limitation": "Cross-cutting",
  "rare-class-reliability": "Cross-cutting",
  "aggregate-vs-instance-validity": "Cross-cutting",
};

const TASK_TAG_PREFIX = "task/";

export function getEvaluativeTasks(node: Pick<GraphNode, "tags">): EvaluativeTask[] {
  const known: readonly string[] = TASK_ORDER;
  return node.tags
    .filter((t) => t.startsWith(TASK_TAG_PREFIX))
    .map((t) => t.slice(TASK_TAG_PREFIX.length))
    .filter((t): t is EvaluativeTask => known.includes(t));
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
  "study-registration",
  "study-protocol",
  "data-transparency",
  "code-transparency",
] as const;
export type TopStandard = (typeof TOP_STANDARD_ORDER)[number];

// Labels deliberately drop "Transparency"/"Study" prefixes — these chips
// render under the "Openness" group header, so the word "Transparency" is
// redundant/misleading there now that Transparency means something else
// on this page (TRIPOD-LLM reporting compliance, above).
export const TOP_STANDARD_LABELS: Record<TopStandard, string> = {
  "data-transparency": "Data",
  "code-transparency": "Code",
  "study-protocol": "Protocol",
  "study-registration": "Registration",
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
  "some-concerns": "Some risk",
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
 * The other four domains of each SRC file's Quality Appraisal table
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
  "statistical-rigor": "Statistical conclusion validity",
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

/**
 * Data leakage / train-test contamination risk — is there a chance the
 * evaluation data (or information about it) reached the model outside the
 * intended eval channel, via pretraining exposure to the test items
 * themselves *or* via prompt-development reuse of eval data? Not a TOP or
 * TRIPOD-LLM field; hand-classified per source this pass by reading each
 * paper's own Internal Validity row, TRIPOD-LLM item 9b ("prompt-development
 * data"), and any linked CVT caveat nodes discussing pretraining/training-
 * corpus overlap. Verified against all 27 sources via two keyword passes
 * over the full corpus (leakage/contamination/held-out/pretraining-exposure
 * terms, then a second pass for memorization/cutoff/training-corpus
 * phrasing) before marking anything `not-addressed` — that value means the
 * paper doesn't discuss this, not that leakage is absent.
 */
export const DATA_LEAKAGE_LABELS: Record<ReproducibilityRisk | "not-addressed", string> = {
  "low-risk": "Addressed",
  "some-concerns": "Partially addressed",
  "high-risk": "Unresolved",
  "not-addressed": "Not addressed by authors",
};
const DATA_LEAKAGE_TAG_TO_RISK: Record<string, ReproducibilityRisk | "not-addressed"> = {
  addressed: "low-risk",
  partial: "some-concerns",
  unresolved: "high-risk",
  "not-addressed": "not-addressed",
};

export function getDataLeakageSignal(node: Pick<GraphNode, "tags">): ReproducibilityRisk | "not-addressed" | null {
  return getRigorCheck(node, "data-leakage");
}

/**
 * Shared reader for the "did the paper address X" family of checks (data
 * leakage, baseline adequacy, train/dev/test split hygiene, multiple-
 * comparisons correction, human-baseline comparability, confidence
 * intervals, effect sizes, exact p-values, spin) — same 4-level scale
 * everywhere: `{namespace}/{key}/{addressed|partial|unresolved|
 * not-addressed}`. Each is hand-classified per source by reading the paper,
 * never inferred from the presence/absence of other fields. Namespace
 * defaults to `rigor` (the original family) but is parameterized so
 * Transparency- and Integrity-side checks can reuse the same reader/tag
 * vocabulary instead of duplicating it.
 */
function getTaggedCheck(
  node: Pick<GraphNode, "tags">,
  key: string,
  namespace: string = "rigor"
): ReproducibilityRisk | "not-addressed" | null {
  const prefix = `${namespace}/${key}/`;
  const tag = node.tags.find((t) => t.startsWith(prefix));
  if (!tag) return null;
  const raw = tag.slice(prefix.length);
  return DATA_LEAKAGE_TAG_TO_RISK[raw] ?? null;
}

// Retained under its original name for existing call sites/readability.
function getRigorCheck(node: Pick<GraphNode, "tags">, key: string) {
  return getTaggedCheck(node, key, "rigor");
}

export function getBaselineAdequacy(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "baseline-adequacy");
}
export function getTrainDevTestHygiene(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "train-dev-test");
}
export function getMultipleComparisonsCorrection(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "multiple-comparisons");
}
export function getHumanBaselineComparability(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "human-baseline");
}
export function getConfidenceIntervals(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "confidence-intervals");
}
export function getPromptEngineering(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "prompt-engineering");
}
export function getChanceCorrectedMetrics(node: Pick<GraphNode, "tags">) {
  return getRigorCheck(node, "chance-corrected-metrics");
}
export function getEffectSizeReporting(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "effect-size", "transparency");
}
export function getExactPValues(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "exact-p-values", "transparency");
}
export function getSpinSignal(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "spin", "integrity");
}
/**
 * AI Writing Check — an independent Pangram (pangram.com) AI-text-detection
 * recheck of the paper's own prose, distinct from the TOP "AI disclosure"
 * transparency signal (whether authors *say* they used AI to write). Silent
 * unless actually run: as of 2026-08 only sources whose Statistic Accuracy
 * check flagged an issue ("issues-found") have been checked, as a broader
 * integrity recheck prompted by that flag — absence of this tag means "not
 * yet checked," not "clean." See misc/scripts/pangram_check.py in the vault.
 */
export function getAiWritingCheck(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "ai-writing-check", "integrity");
}
export const AI_WRITING_CHECK_LABELS: Record<ReproducibilityRisk | "not-addressed", string> = {
  "low-risk": "Human-written",
  "some-concerns": "AI-assisted",
  "high-risk": "AI-generated",
  "not-addressed": "Not checked",
};
/**
 * Ablation Experiment(s) — does the paper isolate a component's
 * contribution by removing/varying it and re-measuring (a prompt
 * component, a pipeline stage, a training-data slice, a model variant),
 * rather than only reporting end-to-end numbers? A design-time choice, so
 * lives in Rigor > Design alongside prompt engineering / baseline
 * adequacy, not Integrity.
 */
export function getAblationExperiments(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "ablation-experiments", "rigor");
}
export function getRepositoryCheck(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "repository-check", "top");
}
export function getCodeCheck(node: Pick<GraphNode, "tags">) {
  return getTaggedCheck(node, "code-check", "top");
}

/**
 * Code Quality — FAIR-software compliance of a source's released code
 * repository, per the fair-software.eu 5-criteria checklist (open
 * repository, license, package-registry listing, citation metadata,
 * quality-checklist badge), computed via the `howfairis` tool (2026-08).
 * Distinct from Data/Code Check above (which only ask "does the link
 * work"): this asks "does the repo follow baseline open-source-software
 * hygiene." Only supports GitHub/GitLab repos (howfairis's own
 * limitation) — silent (no tag) for sources with no code, or code hosted
 * elsewhere (HuggingFace, OSF), same "not yet checked" convention as
 * Statistical Power.
 */
export type CodeQualityScore = 0 | 1 | 2 | 3 | 4 | 5;
const CODE_QUALITY_TAG_PREFIX = "top/code-quality-fair/";

export function getCodeQualityFair(node: Pick<GraphNode, "tags">): CodeQualityScore | null {
  const tag = node.tags.find((t) => t.startsWith(CODE_QUALITY_TAG_PREFIX));
  if (!tag) return null;
  const n = Number(tag.slice(CODE_QUALITY_TAG_PREFIX.length));
  return Number.isInteger(n) && n >= 0 && n <= 5 ? (n as CodeQualityScore) : null;
}

/**
 * Data Quality — FAIRness of a source's released dataset, on a 0-24 scale
 * (FAIR-Checker's 12 semantic-web metrics, 0-2 each), computed 2026-08.
 * Unlike Code Quality (howfairis, GitHub/GitLab-only), this covers every
 * platform a source's data happens to live on (GitHub, OSF, HuggingFace)
 * on one consistent scale — but FAIR-Checker alone can't see inside a
 * plain GitHub repo (GitHub pages carry none of the schema.org/JSON-LD
 * metadata the tool looks for), so every GitHub-hosted dataset would
 * otherwise flatline at the same score (2 for having a URL + 2 for HTTPS,
 * nothing else) regardless of actual repo content. For GitHub/GitLab
 * sources, the score is topped up +2 if the repo has a real LICENSE file
 * (per howfairis, which reads repo content directly rather than page
 * metadata) — a deliberate, documented hybrid, not a raw single-tool
 * score. See misc/data_quality_2026-08.md in the vault for exactly which
 * sources got the license top-up and why.
 */
export type DataQualityScore = number; // 0-24
const DATA_QUALITY_TAG_PREFIX = "top/data-quality-fair/";

export function getDataQualityFair(node: Pick<GraphNode, "tags">): DataQualityScore | null {
  const tag = node.tags.find((t) => t.startsWith(DATA_QUALITY_TAG_PREFIX));
  if (!tag) return null;
  const n = Number(tag.slice(DATA_QUALITY_TAG_PREFIX.length));
  return Number.isInteger(n) && n >= 0 && n <= 24 ? n : null;
}

// Repository/Code Check reuse the same addressed/partial/unresolved/
// not-addressed tag vocabulary as the other checks above, but read oddly
// with the generic "Addressed"/"Unresolved" wording for a link-liveness
// check — this gives them their own live/dead phrasing instead.
export const REPO_CHECK_LABELS: Record<ReproducibilityRisk | "not-addressed", string> = {
  "low-risk": "Live",
  "some-concerns": "Partially reachable",
  "high-risk": "Dead link",
  "not-addressed": "No repository claimed",
};

export const RIGOR_CHECK_LABELS = {
  "baseline-adequacy": "Baseline Adequacy",
  "train-dev-test": "Train/Dev/Test Hygiene",
  "multiple-comparisons": "Multiple-Comparisons Correction",
  "human-baseline": "Human-Baseline Comparability",
  "data-leakage": "Data Leakage",
  "confidence-intervals": "Confidence Intervals",
  "effect-size": "Effect Size",
  "exact-p-values": "Exact p-Values",
  spin: "Non-Significant Result Spin",
  "repository-check": "Data Repo Check",
  "code-check": "Code Check",
  statcheck: "Statistical Consistency",
  "prompt-engineering": "Prompt Engineering",
  "chance-corrected-metrics": "Chance-Corrected Metrics",
  "ablation-experiments": "Ablation Experiment(s)",
  "ai-writing-check": "AI Writing Check",
} as const;

/**
 * Statistical power (a priori sample-size justification via a power
 * calculation) — deliberately absent rather than a graded 4-level check
 * like the others above. Per explicit direction: only render this chip
 * for a source that actually reports running (or explicitly discussing)
 * a power analysis; every source that's silent on it gets no chip at all,
 * not a muted "not-addressed" one — a benchmarking paper with no power
 * analysis is the norm here, not a flag-worthy gap (see the NIH/NINDS
 * rigor note above: none of the 27 sources report one). Corpus-checked
 * before shipping rather than assumed: only add `rigor/statistical-power/
 * {adequate|inadequate}` to a source's tags if it's actually there.
 */
export type StatisticalPowerStatus = "adequate" | "inadequate";
export const STATISTICAL_POWER_LABELS: Record<StatisticalPowerStatus, string> = {
  adequate: "Power analysis reported",
  inadequate: "Power analysis reported but underpowered",
};
export function getStatisticalPower(node: Pick<GraphNode, "tags">): StatisticalPowerStatus | null {
  const prefix = "rigor/statistical-power/";
  const tag = node.tags.find((t) => t.startsWith(prefix));
  if (!tag) return null;
  const raw = tag.slice(prefix.length);
  return raw === "adequate" || raw === "inadequate" ? raw : null;
}

/**
 * Research-integrity disclosures: Ethical approval (TRIPOD-LLM item 13),
 * Funding (14a), Conflicts of interest (14b) — same source table and
 * ✅/⚠️/❌/➖ scale as the TOP-aligned tags, but these aren't TOP
 * standards (TOP covers transparency of data/code/methods specifically),
 * so they live in their own `integrity/` tag namespace.
 */
export const INTEGRITY_SIGNAL_ORDER = ["ethical-approval", "funding-disclosure", "coi-disclosure"] as const;
export type IntegritySignalKind = (typeof INTEGRITY_SIGNAL_ORDER)[number];

export const INTEGRITY_SIGNAL_LABELS: Record<IntegritySignalKind, string> = {
  "ethical-approval": "Ethical approval",
  "funding-disclosure": "Funding disclosure",
  "coi-disclosure": "Conflicts of interest",
};

export type DisclosureLevel = "disclosed" | "partial" | "not-disclosed" | "not-applicable";

export const DISCLOSURE_LEVEL_LABELS: Record<DisclosureLevel, string> = {
  disclosed: "Disclosed",
  partial: "Partially disclosed",
  "not-disclosed": "Not disclosed",
  "not-applicable": "Not applicable",
};

export type IntegritySignal = { kind: IntegritySignalKind; level: DisclosureLevel };

const INTEGRITY_TAG_PREFIX = "integrity/";

export function getIntegritySignals(node: Pick<GraphNode, "tags">): IntegritySignal[] {
  const knownKinds: readonly string[] = INTEGRITY_SIGNAL_ORDER;
  const knownLevels: readonly string[] = Object.keys(DISCLOSURE_LEVEL_LABELS);
  const out: IntegritySignal[] = [];
  for (const tag of node.tags) {
    if (!tag.startsWith(INTEGRITY_TAG_PREFIX)) continue;
    const rest = tag.slice(INTEGRITY_TAG_PREFIX.length);
    const slash = rest.indexOf("/");
    if (slash === -1) continue;
    const kind = rest.slice(0, slash);
    const level = rest.slice(slash + 1);
    if (knownKinds.includes(kind) && knownLevels.includes(level)) {
      out.push({ kind: kind as IntegritySignalKind, level: level as DisclosureLevel });
    }
  }
  return INTEGRITY_SIGNAL_ORDER.filter((k) => out.some((o) => o.kind === k)).map(
    (k) => out.find((o) => o.kind === k)!
  );
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

/**
 * Forensic-metascience checks run against each EVD node's own quoted
 * numbers (F1 = 2PR/(P+R) consistency, Cohen's κ ∈ [-1,1] bounds, and
 * confidence-interval ordering + point-in-interval containment). Only
 * published where the check pattern actually matched text in that node —
 * see scripts' commit history for what was tried and dropped (a naive GRIM
 * — percentage-vs-denominator — check produced false positives from
 * ambiguous "X% (N)" prose and was not published).
 *
 * `reproduction-check` (added 2026-08) is a stronger variant: instead of
 * recomputing from numbers already printed in the paper, it recomputes the
 * EVD's headline statistic from the paper's own *released raw data*
 * (results: match | mismatch | partial), where doing so was computationally
 * feasible without re-running an LLM or retraining a model — see
 * misc/reproducibility_triage_*.md in the vault for the full audit of which
 * sources were attempted and why others were blocked.
 */
export type ForensicCheckKind =
  | "f1-check"
  | "kappa-check"
  | "ci-check"
  | "closure-check"
  | "monotonicity-check"
  | "reproduction-check";
export type ForensicSignal = { kind: ForensicCheckKind; result: string; evdId: string; evdTitle: string };

const FORENSIC_TAG_PREFIX = "forensic/";

export function getForensicSignalsForEvd(node: Pick<GraphNode, "tags" | "id" | "title">): ForensicSignal[] {
  const out: ForensicSignal[] = [];
  for (const tag of node.tags) {
    if (!tag.startsWith(FORENSIC_TAG_PREFIX)) continue;
    const rest = tag.slice(FORENSIC_TAG_PREFIX.length);
    const slash = rest.indexOf("/");
    if (slash === -1) continue;
    const kind = rest.slice(0, slash);
    const result = rest.slice(slash + 1);
    if (
      kind === "f1-check" ||
      kind === "kappa-check" ||
      kind === "ci-check" ||
      kind === "closure-check" ||
      kind === "monotonicity-check" ||
      kind === "reproduction-check"
    ) {
      out.push({ kind, result, evdId: node.id, evdTitle: node.title });
    }
  }
  return out;
}

/** Rolls up forensic signals from every EVD node derivedFrom a given source. */
export function getForensicSignalsForSource(srcId: string): ForensicSignal[] {
  const evdIds = ALL_EDGES.filter((e) => e.type === "derivedFrom" && e.to === srcId).map((e) => e.from);
  const out: ForensicSignal[] = [];
  for (const id of evdIds) {
    const evd = nodeById.get(id);
    if (evd) out.push(...getForensicSignalsForEvd(evd));
  }
  return out;
}

export type StatisticalConsistencyStatus = "consistent" | "issues-found" | "not-applicable";
export const STATISTICAL_CONSISTENCY_LABELS: Record<StatisticalConsistencyStatus, string> = {
  consistent: "Consistent",
  "issues-found": "Issues found",
  "not-applicable": "Not applicable",
};

/**
 * Statistical Consistency ("statcheck") — did an independent recheck of the
 * paper's own reported numbers (recomputed CIs, kappa bounds, closure/
 * monotonicity of tables) turn up anything that doesn't add up? Prefers an
 * explicit `integrity/statcheck/*` tag on the source itself (an override,
 * e.g. for a purely qualitative paper with nothing to recompute); otherwise
 * derives a verdict from the `forensic/*` tags already authored per EVD
 * (`getForensicSignalsForSource`) — any non-clean result across any derived
 * EVD marks the whole source "issues-found".
 */
export function getStatisticalConsistency(
  node: Pick<GraphNode, "id" | "tags">
): StatisticalConsistencyStatus | null {
  const explicit = node.tags.find((t) => t.startsWith("integrity/statcheck/"));
  if (explicit) {
    const raw = explicit.slice("integrity/statcheck/".length);
    if (raw === "consistent" || raw === "issues-found" || raw === "not-applicable") return raw;
  }
  const forensics = getForensicSignalsForSource(node.id);
  if (forensics.length === 0) return null;
  const CLEAN_RESULTS = new Set(["consistent", "in-bounds", "match"]);
  return forensics.some((f) => !CLEAN_RESULTS.has(f.result)) ? "issues-found" : "consistent";
}

export type ReportingComplianceLevel = "low" | "moderate" | "high";

export const REPORTING_COMPLIANCE_LABELS: Record<ReportingComplianceLevel, string> = {
  low: "Low",
  moderate: "Moderate",
  high: "High",
};

export type ReportingCompliance = { level: ReportingComplianceLevel; pct: number };

function readReportingCompliance(node: Pick<GraphNode, "tags" | "extras">): ReportingCompliance | null {
  const levelTag = node.tags.find((t) => t.startsWith("tripod-llm/compliance/"));
  const pctRaw = node.extras.tripodLlmPct as string | undefined;
  if (!levelTag || !pctRaw) return null;
  const level = levelTag.slice("tripod-llm/compliance/".length) as ReportingComplianceLevel;
  const pct = parseInt(pctRaw, 10);
  if (Number.isNaN(pct)) return null;
  return { level, pct };
}

/**
 * TRIPOD-LLM reporting-guideline adherence — our own computed measure,
 * hand-scored against the checklist per EVD (tripod-llm/compliance/* tag +
 * tripod_llm_pct field). Checks the node's own tags first (the EVD case),
 * then falls back to scanning inbound derivedFrom edges (the SRC case: the
 * score is repeated identically across every EVD derivedFrom the same
 * source — verified consistent across all 27 sources — so the first one
 * found is authoritative for the source as a whole).
 */
export function getReportingCompliance(nodeId: string): ReportingCompliance | null {
  const own = nodeById.get(nodeId);
  if (own) {
    const ownCompliance = readReportingCompliance(own);
    if (ownCompliance) return ownCompliance;
  }
  const evdIds = ALL_EDGES.filter((e) => e.type === "derivedFrom" && e.to === nodeId).map((e) => e.from);
  for (const id of evdIds) {
    const evd = nodeById.get(id);
    if (!evd) continue;
    const compliance = readReportingCompliance(evd);
    if (compliance) return compliance;
  }
  return null;
}

/**
 * The SRC node an EVD/CLM/CVT node was derived from, via its outbound
 * derivedFrom edge. Used to inherit paper-level signals (Openness,
 * Integrity, Rigor sub-checks) that live on the source rather than the
 * individual excerpt.
 */
export function getParentSource(nodeId: string): GraphNode | null {
  const edge = ALL_EDGES.find((e) => e.type === "derivedFrom" && e.from === nodeId);
  if (!edge) return null;
  return nodeById.get(edge.to) ?? null;
}

/** Evidence Patterns this EVD instantiates, via its outbound `instantiates` edges. */
export function getEvidencePatternsForEvd(evdId: string): GraphNode[] {
  return ALL_EDGES.filter((e) => e.type === "instantiates" && e.from === evdId)
    .map((e) => nodeById.get(e.to))
    .filter((n): n is GraphNode => Boolean(n));
}

import {
  getReportingCompliance,
  getValiditySignals,
  getTopSignals,
  getRepositoryCheck,
  getCodeCheck,
  getBaselineAdequacy,
  getTrainDevTestHygiene,
  getHumanBaselineComparability,
  getDataLeakageSignal,
  getPromptEngineering,
  getAblationExperiments,
  getConfidenceIntervals,
  getStatisticalPower,
  getMultipleComparisonsCorrection,
  getChanceCorrectedMetrics,
  getStatisticalConsistency,
  getSpinSignal,
  getIntegritySignals,
  getAiWritingCheck,
  getCodeQualityFair,
  getDataQualityFair,
  VALIDITY_DOMAIN_ORDER,
  VALIDITY_DOMAIN_LABELS,
  REPRODUCIBILITY_RISK_LABELS,
  DATA_LEAKAGE_LABELS,
  REPO_CHECK_LABELS,
  AI_WRITING_CHECK_LABELS,
  TOP_LEVEL_LABELS,
  DISCLOSURE_LEVEL_LABELS,
  STATISTICAL_POWER_LABELS,
  STATISTICAL_CONSISTENCY_LABELS,
  REPORTING_COMPLIANCE_LABELS,
  type GraphNode,
  type ReproducibilityRisk,
  type TopLevel,
  type DisclosureLevel,
} from "@/lib/data";

export type Tone = "green" | "gold" | "red" | "gray";
export type Cell = { text: string; tone: Tone } | null;

export type QualityColumn = {
  id: string;
  label: string;
  group: string;
  defaultVisible: boolean;
  /** evd = the EVD node itself; signalSource = its parent SRC if inherited, else evd. */
  value: (evd: GraphNode, signalSource: GraphNode) => Cell;
};

const RISK_TONE: Record<ReproducibilityRisk, Tone> = {
  "low-risk": "green",
  "some-concerns": "gold",
  "high-risk": "red",
};
const RISK_OR_NA_TONE: Record<ReproducibilityRisk | "not-addressed", Tone> = {
  ...RISK_TONE,
  "not-addressed": "gray",
};
const TOP_LEVEL_TONE: Record<TopLevel, Tone> = {
  "level-2-shared": "green",
  "level-1-disclosed": "gold",
  "not-disclosed": "red",
  "not-applicable": "gray",
};
const DISCLOSURE_TONE: Record<DisclosureLevel, Tone> = {
  disclosed: "green",
  partial: "gold",
  "not-disclosed": "red",
  "not-applicable": "gray",
};

function riskCell(risk: ReproducibilityRisk | "not-addressed" | null, labels = DATA_LEAKAGE_LABELS): Cell {
  if (!risk) return null;
  return { text: labels[risk], tone: RISK_OR_NA_TONE[risk] };
}

/** The full catalog of every per-EVD quality signal, grouped for the column picker. */
export const QUALITY_COLUMNS: QualityColumn[] = [
  {
    id: "transparency",
    label: "Transparency",
    group: "Transparency",
    defaultVisible: true,
    value: (evd) => {
      const c = getReportingCompliance(evd.id);
      if (!c) return null;
      const tone: Tone = c.level === "high" ? "green" : c.level === "moderate" ? "gold" : "red";
      return { text: `${c.pct}% (${REPORTING_COMPLIANCE_LABELS[c.level]})`, tone };
    },
  },
  ...VALIDITY_DOMAIN_ORDER.map(
    (domain): QualityColumn => ({
      id: `validity-${domain}`,
      label: VALIDITY_DOMAIN_LABELS[domain],
      group: "Rigor — Validity",
      defaultVisible: true,
      value: (evd) => {
        const signal = getValiditySignals(evd).find((v) => v.domain === domain);
        if (!signal) return null;
        return { text: REPRODUCIBILITY_RISK_LABELS[signal.risk], tone: RISK_TONE[signal.risk] };
      },
    })
  ),
  {
    id: "registration",
    label: "Registration",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => {
      const s = getTopSignals(src).find((t) => t.standard === "study-registration");
      if (!s) return null;
      return { text: TOP_LEVEL_LABELS[s.level], tone: TOP_LEVEL_TONE[s.level] };
    },
  },
  {
    id: "protocol",
    label: "Protocol",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => {
      const s = getTopSignals(src).find((t) => t.standard === "study-protocol");
      if (!s) return null;
      return { text: TOP_LEVEL_LABELS[s.level], tone: TOP_LEVEL_TONE[s.level] };
    },
  },
  {
    id: "data-repo-check",
    label: "Dataset check",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getRepositoryCheck(src), REPO_CHECK_LABELS),
  },
  {
    id: "code-check",
    label: "Code Check",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getCodeCheck(src), REPO_CHECK_LABELS),
  },
  {
    id: "baseline-adequacy",
    label: "Baseline Adequacy",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getBaselineAdequacy(src)),
  },
  {
    id: "train-dev-test",
    label: "Train/Dev/Test Hygiene",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getTrainDevTestHygiene(src)),
  },
  {
    id: "human-baseline",
    label: "Human-Baseline Comparability",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getHumanBaselineComparability(src)),
  },
  {
    id: "data-leakage",
    label: "Data Leakage",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getDataLeakageSignal(src)),
  },
  {
    id: "prompt-engineering",
    label: "Prompt Engineering",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getPromptEngineering(src)),
  },
  {
    id: "ablation-experiments",
    label: "Ablation Experiment(s)",
    group: "Rigor — Design",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getAblationExperiments(src)),
  },
  {
    id: "confidence-intervals",
    label: "Confidence Intervals",
    group: "Rigor — Analyses",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getConfidenceIntervals(src)),
  },
  {
    id: "statistical-power",
    label: "Statistical Power",
    group: "Rigor — Analyses",
    defaultVisible: false,
    value: (_evd, src) => {
      const status = getStatisticalPower(src);
      if (!status) return null;
      return { text: STATISTICAL_POWER_LABELS[status], tone: status === "adequate" ? "green" : "red" };
    },
  },
  {
    id: "multiple-comparisons",
    label: "Multiple-Comparisons Correction",
    group: "Rigor — Analyses",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getMultipleComparisonsCorrection(src)),
  },
  {
    id: "chance-corrected-metrics",
    label: "Chance-Corrected Metrics",
    group: "Rigor — Analyses",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getChanceCorrectedMetrics(src)),
  },
  {
    id: "statistic-accuracy",
    label: "Statistic Accuracy",
    group: "Rigor — Reporting",
    defaultVisible: false,
    value: (_evd, src) => {
      const status = getStatisticalConsistency(src);
      if (!status) return null;
      const tone: Tone = status === "consistent" ? "green" : status === "issues-found" ? "red" : "gray";
      return { text: STATISTICAL_CONSISTENCY_LABELS[status], tone };
    },
  },
  {
    id: "spin",
    label: "Non-Significant Result Spin",
    group: "Rigor — Interpretation",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getSpinSignal(src)),
  },
  {
    id: "ethical-approval",
    label: "Ethical Approval",
    group: "Integrity",
    defaultVisible: false,
    value: (_evd, src) => {
      const s = getIntegritySignals(src).find((i) => i.kind === "ethical-approval");
      if (!s) return null;
      return { text: DISCLOSURE_LEVEL_LABELS[s.level], tone: DISCLOSURE_TONE[s.level] };
    },
  },
  {
    id: "funding-disclosure",
    label: "Funding Disclosure",
    group: "Integrity",
    defaultVisible: false,
    value: (_evd, src) => {
      const s = getIntegritySignals(src).find((i) => i.kind === "funding-disclosure");
      if (!s) return null;
      return { text: DISCLOSURE_LEVEL_LABELS[s.level], tone: DISCLOSURE_TONE[s.level] };
    },
  },
  {
    id: "coi-disclosure",
    label: "Conflicts of Interest",
    group: "Integrity",
    defaultVisible: false,
    value: (_evd, src) => {
      const s = getIntegritySignals(src).find((i) => i.kind === "coi-disclosure");
      if (!s) return null;
      return { text: DISCLOSURE_LEVEL_LABELS[s.level], tone: DISCLOSURE_TONE[s.level] };
    },
  },
  {
    id: "ai-writing-check",
    label: "AI Writing Check",
    group: "Integrity",
    defaultVisible: false,
    value: (_evd, src) => riskCell(getAiWritingCheck(src), AI_WRITING_CHECK_LABELS),
  },
  {
    id: "code-quality-fair",
    label: "Code Quality",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => {
      const score = getCodeQualityFair(src);
      if (score === null) return null;
      const tone: Tone = score >= 4 ? "green" : score >= 2 ? "gold" : "red";
      return { text: `${score}/5`, tone };
    },
  },
  {
    id: "data-quality-fair",
    label: "Data Quality",
    group: "Openness",
    defaultVisible: false,
    value: (_evd, src) => {
      const score = getDataQualityFair(src);
      if (score === null) return null;
      const tone: Tone = score >= 16 ? "green" : score >= 8 ? "gold" : "red";
      return { text: `${score}/24`, tone };
    },
  },
];

export const QUALITY_COLUMN_GROUPS = Array.from(new Set(QUALITY_COLUMNS.map((c) => c.group)));

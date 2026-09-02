import {
  AI_WRITING_CHECK_LABELS,
  DATA_LEAKAGE_LABELS,
  DISCLOSURE_LEVEL_LABELS,
  REPO_CHECK_LABELS,
  REPORTING_COMPLIANCE_LABELS,
  REPRODUCIBILITY_RISK_LABELS,
  STATISTICAL_CONSISTENCY_LABELS,
  STATISTICAL_POWER_LABELS,
  TOP_LEVEL_LABELS,
} from "@/lib/data";

// One color vocabulary for every chip on the site, so a color always means
// the same thing no matter which signal it's attached to: gray = not
// applicable / unclear (no judgment implied), red = absent or a real
// problem, gold = partially met / some concern, green = fully met / no
// issues found.
export type Tone = "green" | "gold" | "red" | "gray";

export const TONE_BG: Record<Tone, string> = {
  green: "bg-emerald-600",
  gold: "bg-amber-500",
  red: "bg-red-600",
  gray: "bg-zinc-400",
};

export const TONE_RING: Record<Tone, string> = {
  green: "border-emerald-600",
  gold: "border-amber-500",
  red: "border-red-600",
  gray: "border-zinc-300",
};

/**
 * One rung of a chip's scale. `value` is what the reader sees as the level
 * itself — a band like "4-5" for a scored chip, or the level's own name for
 * a categorical one — and `label` says what that level means.
 */
export type ScaleStep = {
  /** Matches the chip's current value, so the active rung can be marked. */
  key: string;
  tone: Tone;
  value: string;
  label: string;
};

/**
 * The full range a chip can take, shown on hover so a reader never has to
 * infer the scale from the single value in front of them. `what` states what
 * is being measured; `note` carries the caveat that belongs to the whole
 * scale rather than to any one rung.
 */
export type Scale = {
  what: string;
  steps: ScaleStep[];
  note?: string;
};

const risk = (labels: Record<string, string>): ScaleStep[] => [
  { key: "low-risk", tone: "green", value: "Low risk", label: labels["low-risk"] },
  { key: "some-concerns", tone: "gold", value: "Some risk", label: labels["some-concerns"] },
  { key: "high-risk", tone: "red", value: "High risk", label: labels["high-risk"] },
];

const notAddressed = (labels: Record<string, string>): ScaleStep => ({
  key: "not-addressed",
  tone: "gray",
  value: "Not addressed",
  label: labels["not-addressed"],
});

export const TOP_LEVEL_SCALE: Scale = {
  what: "How openly this TOP standard was met.",
  steps: [
    { key: "level-2-shared", tone: "green", value: "Level 2", label: TOP_LEVEL_LABELS["level-2-shared"] },
    { key: "level-1-disclosed", tone: "gold", value: "Level 1", label: TOP_LEVEL_LABELS["level-1-disclosed"] },
    { key: "not-disclosed", tone: "red", value: "Level 0", label: TOP_LEVEL_LABELS["not-disclosed"] },
    { key: "not-applicable", tone: "gray", value: "n/a", label: TOP_LEVEL_LABELS["not-applicable"] },
  ],
  note: "COS TOP Guidelines. Red means the standard was never addressed — an absence, not merely unclear.",
};

export const DISCLOSURE_SCALE: Scale = {
  what: "Whether the paper disclosed this.",
  steps: [
    { key: "disclosed", tone: "green", value: "Disclosed", label: DISCLOSURE_LEVEL_LABELS.disclosed },
    { key: "partial", tone: "gold", value: "Partial", label: DISCLOSURE_LEVEL_LABELS.partial },
    { key: "not-disclosed", tone: "red", value: "Absent", label: DISCLOSURE_LEVEL_LABELS["not-disclosed"] },
    { key: "not-applicable", tone: "gray", value: "n/a", label: DISCLOSURE_LEVEL_LABELS["not-applicable"] },
  ],
};

export const VALIDITY_SCALE: Scale = {
  what: "Risk of bias in this validity domain.",
  steps: risk(REPRODUCIBILITY_RISK_LABELS),
};

export const RIGOR_CHECK_SCALE: Scale = {
  what: "How well this methodological check was met.",
  steps: [...risk(REPRODUCIBILITY_RISK_LABELS), notAddressed(DATA_LEAKAGE_LABELS)],
};

export const DATA_LEAKAGE_SCALE: Scale = {
  what: "Whether train/eval contamination was ruled out.",
  steps: [...risk(DATA_LEAKAGE_LABELS), notAddressed(DATA_LEAKAGE_LABELS)],
  note: "Gray is not a pass — it means the paper is silent on it.",
};

export const REPO_CHECK_SCALE: Scale = {
  what: "Whether the claimed repository actually resolves.",
  steps: [...risk(REPO_CHECK_LABELS), notAddressed(REPO_CHECK_LABELS)],
};

export const AI_WRITING_CHECK_SCALE: Scale = {
  what: "Pangram's estimate of how the prose was written.",
  steps: [...risk(AI_WRITING_CHECK_LABELS), notAddressed(AI_WRITING_CHECK_LABELS)],
};

export const STATISTICAL_CONSISTENCY_SCALE: Scale = {
  what: "Whether reported statistics are internally consistent.",
  steps: [
    { key: "consistent", tone: "green", value: "Consistent", label: STATISTICAL_CONSISTENCY_LABELS.consistent },
    { key: "issues-found", tone: "red", value: "Issues", label: STATISTICAL_CONSISTENCY_LABELS["issues-found"] },
    { key: "not-applicable", tone: "gray", value: "n/a", label: STATISTICAL_CONSISTENCY_LABELS["not-applicable"] },
  ],
  note: "statcheck-style recomputation of test statistic, df and p-value.",
};

export const STATISTICAL_POWER_SCALE: Scale = {
  what: "Whether an a priori power analysis was reported.",
  steps: [
    { key: "adequate", tone: "green", value: "Adequate", label: STATISTICAL_POWER_LABELS.adequate },
    { key: "inadequate", tone: "red", value: "Underpowered", label: STATISTICAL_POWER_LABELS.inadequate },
  ],
  note: "Sources silent on power get no chip at all rather than a muted one — for benchmarking papers that silence is the norm, not a flag.",
};

export const REPORTING_COMPLIANCE_SCALE: Scale = {
  what: "Share of TRIPOD-LLM checklist items reported.",
  steps: [
    { key: "high", tone: "green", value: "67-100%", label: REPORTING_COMPLIANCE_LABELS.high },
    { key: "moderate", tone: "gold", value: "34-66%", label: REPORTING_COMPLIANCE_LABELS.moderate },
    { key: "low", tone: "red", value: "0-33%", label: REPORTING_COMPLIANCE_LABELS.low },
  ],
  note: "Our own hand-scored measure, not the authors' claim.",
};

export const CODE_QUALITY_SCALE: Scale = {
  what: "fair-software.eu criteria, scored by howfairis.",
  steps: [
    { key: "green", tone: "green", value: "4-5 / 5", label: "Most FAIR criteria met" },
    { key: "gold", tone: "gold", value: "2-3 / 5", label: "Some criteria met" },
    { key: "red", tone: "red", value: "0-1 / 5", label: "Few or none met" },
  ],
};

export const DATA_QUALITY_SCALE: Scale = {
  what: "FAIR-Checker score for the dataset itself.",
  steps: [
    { key: "green", tone: "green", value: "16-24 / 24", label: "Largely FAIR" },
    { key: "gold", tone: "gold", value: "8-15 / 24", label: "Partially FAIR" },
    { key: "red", tone: "red", value: "0-7 / 24", label: "Largely not FAIR" },
  ],
  note: "GitHub/GitLab-hosted data gets a +2 top-up when the repo carries a real license file, since FAIR-Checker cannot see repo contents directly.",
};

export const TRUTH_VALUE_SCALE: Scale = {
  what: "Curator-assessed confidence in this claim.",
  steps: [
    { key: "high", tone: "green", value: "66-100%", label: "Well supported by the cited evidence" },
    { key: "medium", tone: "gold", value: "33-65%", label: "Mixed or partial support" },
    { key: "low", tone: "red", value: "0-32%", label: "Weakly supported or contested" },
  ],
  note: "A curator's judgment, not a computed statistic.",
};

export const CAVEAT_SEVERITY_SCALE: Scale = {
  what: "How much this limitation should change your reading.",
  steps: [
    { key: "high", tone: "red", value: "High", label: "Undercuts the source's main finding" },
    { key: "moderate", tone: "gold", value: "Moderate", label: "Qualifies the finding meaningfully" },
    { key: "low", tone: "gray", value: "Low", label: "Worth noting, not decisive" },
  ],
};


/**
 * Availability ladders for the two artifact rows. Same shape as the old repo
 * check, but worded for what is actually being looked for: a dataset in one
 * case, a code repository in the other. "No repository claimed" read oddly
 * under a row called Dataset.
 */
export const DATASET_CHECK_SCALE: Scale = {
  what: "Whether a dataset is claimed, and whether the link resolves.",
  steps: [
    { key: "low-risk", tone: "green", value: "Live", label: "Dataset link resolves" },
    { key: "some-concerns", tone: "gold", value: "Partial", label: "Partially reachable" },
    { key: "high-risk", tone: "red", value: "Dead", label: "Link does not resolve" },
    { key: "not-addressed", tone: "gray", value: "None", label: "No dataset claimed by the authors" },
  ],
  note: "Gray means the paper claims no dataset — nothing to reach, and nothing to score for FAIRness.",
};

export const CODE_CHECK_SCALE: Scale = {
  what: "Whether a code repository is claimed, and whether the link resolves.",
  steps: [
    { key: "low-risk", tone: "green", value: "Live", label: "Repository link resolves" },
    { key: "some-concerns", tone: "gold", value: "Partial", label: "Partially reachable" },
    { key: "high-risk", tone: "red", value: "Dead", label: "Link does not resolve" },
    { key: "not-addressed", tone: "gray", value: "None", label: "No code repository claimed by the authors" },
  ],
  note: "Gray means the paper claims no code — nothing to reach, and nothing to score for FAIRness.",
};

/** Which band a 0-5 code-quality score falls in. */
export function codeQualityBand(score: number): string {
  return score >= 4 ? "green" : score >= 2 ? "gold" : "red";
}

/** Which band a 0-24 data-quality score falls in. */
export function dataQualityBand(score: number): string {
  return score >= 16 ? "green" : score >= 8 ? "gold" : "red";
}

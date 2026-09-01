import ChipRows from "@/components/ChipRows";
import CollapsibleSignalBlock from "@/components/CollapsibleSignalBlock";
import {
  getTopSignals,
  getReproducibilityRisk,
  getValiditySignals,
  getIntegritySignals,
  getReportingCompliance,
  getDataLeakageSignal,
  getBaselineAdequacy,
  getTrainDevTestHygiene,
  getMultipleComparisonsCorrection,
  getHumanBaselineComparability,
  getConfidenceIntervals,
  getStatisticalPower,
  getPromptEngineering,
  getChanceCorrectedMetrics,
  getAblationExperiments,
  getSpinSignal,
  getStatisticalConsistency,
  getRepositoryCheck,
  getCodeCheck,
  getCodeQualityFair,
  getDataQualityFair,
  getAiWritingCheck,
  getParentSource,
  TOP_STANDARD_LABELS,
  TOP_LEVEL_LABELS,
  REPRODUCIBILITY_RISK_LABELS,
  VALIDITY_DOMAIN_LABELS,
  INTEGRITY_SIGNAL_LABELS,
  DISCLOSURE_LEVEL_LABELS,
  REPORTING_COMPLIANCE_LABELS,
  DATA_LEAKAGE_LABELS,
  RIGOR_CHECK_LABELS,
  REPO_CHECK_LABELS,
  AI_WRITING_CHECK_LABELS,
  STATISTICAL_CONSISTENCY_LABELS,
  STATISTICAL_POWER_LABELS,
  type GraphNode,
  type TopStandard,
  type TopLevel,
  type ReproducibilityRisk,
  type ValidityDomain,
  type IntegritySignalKind,
  type DisclosureLevel,
  type ReportingCompliance,
  type StatisticalPowerStatus,
  type StatisticalConsistencyStatus,
  type CodeQualityScore,
  type DataQualityScore,
} from "@/lib/data";

// One color vocabulary for every chip on this page, so a color always means
// the same thing no matter which signal it's attached to: gray = not
// applicable / unclear (no judgment implied), red = absent or a real
// problem, gold = partially met / some concern, green = fully met / no
// issues found.
type Tone = "green" | "gold" | "red" | "gray";
const TONE_BG: Record<Tone, string> = {
  green: "bg-emerald-600",
  gold: "bg-amber-500",
  red: "bg-red-600",
  gray: "bg-zinc-400",
};
const TONE_RING: Record<Tone, string> = {
  green: "border-emerald-600",
  gold: "border-amber-500",
  red: "border-red-600",
  gray: "border-zinc-300",
};

// Transparency is now our own computed measure of adherence to reporting
// guidelines (TRIPOD-LLM) — did the paper report what it did, in enough
// detail to assess and reproduce. Openness covers all four COS TOP
// Guidelines standards (data, code, protocol, registration) — did the
// authors make the underlying artifacts and commitments openly available.
const COMPLIANCE_TONE: Record<ReportingCompliance["level"], Tone> = {
  high: "green",
  moderate: "gold",
  low: "red",
};

function ReportingComplianceGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <rect x="5" y="3.5" width="14" height="17" rx="1.5" />
      <path d="M9 3v2h6V3" />
      <path d="M8.5 12.5l2 2 4.5-5" />
    </svg>
  );
}

function ReportingComplianceBadge({ compliance, linkBase = "" }: { compliance: ReportingCompliance; linkBase?: string }) {
  return (
    <a
      href={`${linkBase}#tripod-llm-reporting-summary`}
      title={`TRIPOD-LLM reporting-guideline adherence: ${compliance.pct}% of checklist items (Methods 5a-15, Results 16a-18) fully or partially reported: ${REPORTING_COMPLIANCE_LABELS[compliance.level].toLowerCase()} compliance. Hand-scored against the checklist, our own computed measure. Click to view the table.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[COMPLIANCE_TONE[compliance.level]]}`}>
        <ReportingComplianceGlyph />
      </span>
      TRIPOD-LLM · {compliance.pct}% reported
    </a>
  );
}

// level-2-shared = fully met (green), level-1-disclosed = partially met
// (gold), not-disclosed = the standard was never addressed at all — that's
// an absence, not just unclear (red), not-applicable = doesn't apply to
// this study (gray).
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

const RISK_TONE: Record<ReproducibilityRisk, Tone> = {
  "low-risk": "green",
  "some-concerns": "gold",
  "high-risk": "red",
};

// "not-addressed" (the paper doesn't discuss this at all) reads as unclear,
// not a confirmed problem, so it stays gray rather than red.
const DATA_LEAKAGE_TONE: Record<ReproducibilityRisk | "not-addressed", Tone> = {
  ...RISK_TONE,
  "not-addressed": "gray",
};

// Original glyph — two overlapping shapes with a "leak" drip, evoking
// train/eval data bleeding into each other. No established icon convention
// found for this (it isn't a TOP or TRIPOD-LLM field).
function DataLeakageGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M8.5 3.5h9v9a4.5 4.5 0 0 1-9 0v-9Z" />
      <path d="M8.5 8h9" />
      <path d="M12 17v2.5c0 1.1-1 2-2.5 2S7 20.6 7 19.5c0-1.4 2.5-3 2.5-3" />
    </svg>
  );
}

// Original glyphs for the four Openness (TOP) standards — one recognizable
// shape per standard, matched to its own tone color below rather than the
// real OSF/COS badge artwork (which is fixed-color raster art and can't
// take on our green/gold/red/gray scale).
function StandardGlyph({ standard }: { standard: TopStandard }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (standard) {
    case "study-protocol":
      // clipboard — the study's pre-specified plan
      return (
        <svg {...common}>
          <rect x="5" y="4" width="14" height="17" rx="2" />
          <path d="M9 3.5h6a1 1 0 0 1 1 1V6H8V4.5a1 1 0 0 1 1-1Z" />
          <path d="M8.5 12h7M8.5 16h5" />
        </svg>
      );
    case "study-registration":
      // ribbon seal — a claim staked and certified before results were known
      return (
        <svg {...common}>
          <circle cx="12" cy="10" r="6.5" />
          <path d="M9 15.5 7.5 21l4.5-2.5 4.5 2.5-1.5-5.5" />
          <path d="M9.3 10 11 11.8l3.7-4" />
        </svg>
      );
    case "data-transparency":
      // database cylinder — the underlying data made shareable
      return (
        <svg {...common}>
          <ellipse cx="12" cy="6" rx="7.5" ry="3" />
          <path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6" />
          <path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3" />
        </svg>
      );
    case "code-transparency":
      // angle brackets — the analysis code made shareable
      return (
        <svg {...common}>
          <path d="M9 7 4 12l5 5" />
          <path d="M15 7l5 5-5 5" />
        </svg>
      );
  }
}

// Original glyphs for the four validity domains — no established open-
// licensed icon set exists for these (checked: Cochrane's RoB2 icon set is
// CC BY-NC-ND, which forbids derivatives; nothing else turned up).
function ValidityGlyph({ domain }: { domain: ValidityDomain }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (domain) {
    case "construct-validity":
      // target — measuring the concept it's meant to measure
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="8" />
          <circle cx="12" cy="12" r="3.5" />
          <circle cx="12" cy="12" r="0.5" fill="currentColor" />
        </svg>
      );
    case "internal-validity":
      // linked chain — the causal link between design and outcome
      return (
        <svg {...common}>
          <rect x="3" y="9" width="9" height="7" rx="3.5" />
          <rect x="12" y="8" width="9" height="7" rx="3.5" />
        </svg>
      );
    case "external-validity":
      // globe — generalization beyond the study's own setting
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="8.5" />
          <path d="M3.5 12h17M12 3.5c3 3 3 14 0 17M12 3.5c-3 3-3 14 0 17" />
        </svg>
      );
    case "statistical-rigor":
      // bars with an error whisker — uncertainty-aware comparison
      return (
        <svg {...common}>
          <path d="M5 20V11M12 20V6M19 20v-4" />
          <path d="M9 6h6M12 3v6" />
        </svg>
      );
  }
}

// Original glyphs for research-integrity disclosures — no established
// open-licensed icon set found for these (checked: ICMJE's "conflict of
// interest" material is a disclosure form, not an icon convention; no
// canonical funding/ethics-approval badge turned up either).
function IntegrityGlyph({ kind }: { kind: IntegritySignalKind }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (kind) {
    case "coi-disclosure":
      // balance scale — weighing competing interests
      return (
        <svg {...common}>
          <path d="M12 3v18M7 21h10" />
          <path d="M4 7h6M14 7h6" />
          <path d="M4 7 1.5 12a2.5 2.5 0 0 0 5 0Z" />
          <path d="M20 7l-2.5 5a2.5 2.5 0 0 0 5 0Z" />
        </svg>
      );
    case "funding-disclosure":
      // coin — funding source
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="8.5" />
          <path d="M12 7.5v9M9.5 9.3c0-1 1-1.8 2.5-1.8s2.5.9 2.5 2-1 1.5-2.5 1.5-2.5.6-2.5 1.8 1 1.9 2.5 1.9 2.5-.7 2.5-1.8" />
        </svg>
      );
    case "ethical-approval":
      // shield with check — approval/certification
      return (
        <svg {...common}>
          <path d="M12 3.5 19 6.5v5.5c0 5-3 8-7 9-4-1-7-4-7-9V6.5Z" />
          <path d="M8.5 12.3l2.3 2.3L15.5 10" />
        </svg>
      );
  }
}

// Ethical approval, Funding disclosure, and Conflicts of interest are
// literally TRIPOD-LLM items 13/14a/14b — link straight to that row.
const INTEGRITY_HREF: Partial<Record<IntegritySignalKind, string>> = {
  "ethical-approval": "#tripod-13",
  "funding-disclosure": "#tripod-14a",
  "coi-disclosure": "#tripod-14b",
};

function IntegrityBadge({ kind, level, linkBase = "" }: { kind: IntegritySignalKind; level: DisclosureLevel; linkBase?: string }) {
  const href = INTEGRITY_HREF[kind] && `${linkBase}${INTEGRITY_HREF[kind]}`;
  const Tag = href ? "a" : "span";
  return (
    <Tag
      href={href}
      title={href ? `${INTEGRITY_SIGNAL_LABELS[kind]}: ${DISCLOSURE_LEVEL_LABELS[level]}. Click to view the row.` : `${INTEGRITY_SIGNAL_LABELS[kind]}: ${DISCLOSURE_LEVEL_LABELS[level]}`}
      className={`inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase${
        href ? " transition-colors hover:border-forest/50" : ""
      }`}
    >
      <span
        className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[DISCLOSURE_TONE[level]]}`}
      >
        <IntegrityGlyph kind={kind} />
      </span>
      {INTEGRITY_SIGNAL_LABELS[kind]}
    </Tag>
  );
}

// Registration and Protocol are literally TRIPOD-LLM items 14d/14c — link
// straight to that checklist row. Data/Code transparency aren't rendered as
// their own chips any more (superseded by Data Repo Check/Code Check), so
// no entries are needed for them here.
const TOP_STANDARD_HREF: Partial<Record<TopStandard, string>> = {
  "study-registration": "#tripod-14d",
  "study-protocol": "#tripod-14c",
};

function StandardBadge({ standard, level, linkBase = "" }: { standard: TopStandard; level: TopLevel; linkBase?: string }) {
  const tone = TOP_LEVEL_TONE[level];
  const href = TOP_STANDARD_HREF[standard] && `${linkBase}${TOP_STANDARD_HREF[standard]}`;
  const Tag = href ? "a" : "span";

  return (
    <Tag
      href={href}
      title={href ? `${TOP_STANDARD_LABELS[standard]}: ${TOP_LEVEL_LABELS[level]}. Click to view the row.` : `${TOP_STANDARD_LABELS[standard]}: ${TOP_LEVEL_LABELS[level]}`}
      className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase ${TONE_RING[tone]}${
        href ? " transition-colors hover:border-forest/50" : ""
      }`}
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[tone]}`}>
        <StandardGlyph standard={standard} />
      </span>
      {TOP_STANDARD_LABELS[standard]}
    </Tag>
  );
}

// Gray "?" reminder chips — Extensibility work we haven't actually done yet
// (computationally re-running the analysis, independently replicating the
// study). Deliberately neutral/unscored, not a graded signal like the risk
// badges above, so we never imply this checking has happened when it hasn't.
function ReminderGlyph() {
  return <span aria-hidden className="text-[9px] font-bold leading-none">?</span>;
}

function ReminderBadge({ label, title }: { label: string; title: string }) {
  return (
    <span title={title} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase">
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG.gray}`}>
        <ReminderGlyph />
      </span>
      {label}
    </span>
  );
}

function RiskBadge({
  label,
  risk,
  title,
  glyph,
  href,
}: {
  label: string;
  risk: ReproducibilityRisk;
  title: string;
  glyph: React.ReactNode;
  href?: string;
}) {
  const Tag = href ? "a" : "span";
  return (
    <Tag
      href={href}
      title={href ? `${title}. Click to view the row.` : title}
      className={`inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase${
        href ? " transition-colors hover:border-forest/50" : ""
      }`}
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[RISK_TONE[risk]]}`}>{glyph}</span>
      {label}
    </Tag>
  );
}

function DataLeakageBadge({ risk, linkBase = "" }: { risk: ReproducibilityRisk | "not-addressed"; linkBase?: string }) {
  return (
    <a
      href={`${linkBase}#qa-data-leakage`}
      title={`Data leakage: ${DATA_LEAKAGE_LABELS[risk]}. Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[DATA_LEAKAGE_TONE[risk]]}`}>
        <DataLeakageGlyph />
      </span>
      Data Leakage
    </a>
  );
}

// Original glyphs for the four new benchmarking-specific Rigor checks — same
// reasoning as the other original glyphs on this page: no established open-
// licensed icon convention exists for these (they aren't TOP or TRIPOD-LLM
// fields, and aren't in Cochrane's RoB2 set either).
type RigorCheckKind =
  | "baseline-adequacy"
  | "train-dev-test"
  | "multiple-comparisons"
  | "human-baseline"
  | "confidence-intervals"
  | "effect-size"
  | "exact-p-values"
  | "spin"
  | "repository-check"
  | "code-check"
  | "statcheck"
  | "prompt-engineering"
  | "chance-corrected-metrics"
  | "ablation-experiments"
  | "ai-writing-check";

// Where each Rigor sub-check's chip should navigate — the Quality Appraisal
// table row when one exists (`qa-<kind>`, tagged by lib/markdown.ts's
// tagAppraisalRows), the TRIPOD-LLM checklist row when the check *is*
// literally one of its items (prompt-engineering = item 9a), or omitted
// entirely when no real anchor exists yet, so the chip renders as a plain
// span rather than a link to nowhere.
const RIGOR_CHECK_HREF: Partial<Record<RigorCheckKind, string>> = {
  "baseline-adequacy": "#qa-baseline-adequacy",
  "train-dev-test": "#qa-train-dev-test",
  "multiple-comparisons": "#qa-multiple-comparisons",
  "human-baseline": "#qa-human-baseline",
  "prompt-engineering": "#tripod-9a",
  "repository-check": "#tripod-14e",
  "code-check": "#tripod-14f",
  "confidence-intervals": "#qa-confidence-intervals",
  "chance-corrected-metrics": "#qa-chance-corrected-metrics",
  spin: "#qa-spin",
  "ablation-experiments": "#qa-ablation-experiments",
  "ai-writing-check": "#qa-ai-writing-check",
};

function RigorCheckGlyph({ kind }: { kind: RigorCheckKind }) {
  const common = { width: 12, height: 12, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (kind) {
    case "baseline-adequacy":
      // a reference line with a bar rising above it — score measured against a real floor
      return (
        <svg {...common}>
          <path d="M3.5 17h17" />
          <path d="M8 17V9.5M14 17v-6M19 17V6" />
        </svg>
      );
    case "train-dev-test":
      // three stacked, separated bands — clean split hygiene
      return (
        <svg {...common}>
          <rect x="4" y="4" width="16" height="4.2" rx="1" />
          <rect x="4" y="9.9" width="16" height="4.2" rx="1" />
          <rect x="4" y="15.8" width="16" height="4.2" rx="1" />
        </svg>
      );
    case "multiple-comparisons":
      // a small grid — many pairwise comparisons at once
      return (
        <svg {...common}>
          <path d="M3.5 9h17M3.5 15h17M9 3.5v17M15 3.5v17" />
          <rect x="3.5" y="3.5" width="17" height="17" rx="1.5" />
        </svg>
      );
    case "human-baseline":
      // a person silhouette next to a bar — LLM-vs-human comparison
      return (
        <svg {...common}>
          <circle cx="8.5" cy="7" r="2.5" />
          <path d="M4.5 18.5c0-3 1.8-5 4-5s4 2 4 5" />
          <path d="M15.5 18.5V12M19 18.5v-8" />
        </svg>
      );
    case "confidence-intervals":
      // an error bar — whisker caps around a point estimate
      return (
        <svg {...common}>
          <path d="M12 4v16M7.5 4h9M7.5 20h9" />
          <circle cx="12" cy="12" r="2" fill="currentColor" stroke="none" />
        </svg>
      );
    case "effect-size":
      // a delta — the standard symbol for a magnitude of difference
      return (
        <svg {...common}>
          <path d="M12 4 20.5 19.5h-17Z" />
        </svg>
      );
    case "exact-p-values":
      // a magnifying glass over a decimal point — precise, not thresholded
      return (
        <svg {...common}>
          <circle cx="10.5" cy="10.5" r="6.5" />
          <path d="M15.3 15.3 20 20" />
          <circle cx="10.5" cy="10.5" r="0.75" fill="currentColor" stroke="none" />
        </svg>
      );
    case "spin":
      // a looping arrow — reframing/re-spinning the same result
      return (
        <svg {...common}>
          <path d="M5 12a7 7 0 0 1 12-5" />
          <path d="M17 3.5V7h-3.5" />
          <path d="M19 12a7 7 0 0 1-12 5" />
          <path d="M7 20.5V17h3.5" />
        </svg>
      );
    case "repository-check":
      // a link — the repository URL itself resolving or not
      return (
        <svg {...common}>
          <path d="M10 14 14 10" />
          <path d="M11.5 6.5 14 4a3.5 3.5 0 0 1 5 5l-2.5 2.5" />
          <path d="M12.5 17.5 10 20a3.5 3.5 0 0 1-5-5l2.5-2.5" />
        </svg>
      );
    case "code-check":
      // a terminal prompt — code actually runnable, not just linked
      return (
        <svg {...common}>
          <rect x="3.5" y="4.5" width="17" height="15" rx="1.5" />
          <path d="M7 9.5 10.5 12 7 14.5" />
          <path d="M12.5 14.5h4.5" />
        </svg>
      );
    case "statcheck":
      // an equals sign with a checkmark — an independently recomputed number
      // that does (or doesn't) match what the paper reported
      return (
        <svg {...common}>
          <path d="M5 9.5h9M5 14.5h9" />
          <path d="M16 15.5l2.2 2.2L22 13.5" />
        </svg>
      );
    case "ai-writing-check":
      // lines of prose with a magnifying glass over them — an independent
      // tool scanning the paper's own text for signs of AI generation
      return (
        <svg {...common}>
          <path d="M4 6h11M4 10h8M4 14h6" />
          <circle cx="17" cy="15" r="3.2" />
          <path d="M19.5 17.5L22 20" />
        </svg>
      );
    case "prompt-engineering":
      // a chat bubble with a slider/tune mark — the prompt itself as a
      // deliberately engineered input, not just "we called the API"
      return (
        <svg {...common}>
          <path d="M4 5.5h16v10.5H9.5L6 19.5v-3.5H4Z" />
          <path d="M8 10.5h2M8 10.5v-2M13 10.5h3M17 8h-2M17 8v2.5" />
        </svg>
      );
    case "chance-corrected-metrics":
      // a die face — the chance-level baseline a corrected metric adjusts against
      return (
        <svg {...common}>
          <rect x="4" y="4" width="16" height="16" rx="3" />
          <circle cx="8.5" cy="8.5" r="1.1" fill="currentColor" stroke="none" />
          <circle cx="15.5" cy="8.5" r="1.1" fill="currentColor" stroke="none" />
          <circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none" />
          <circle cx="8.5" cy="15.5" r="1.1" fill="currentColor" stroke="none" />
          <circle cx="15.5" cy="15.5" r="1.1" fill="currentColor" stroke="none" />
        </svg>
      );
    case "ablation-experiments":
      // a component removed from a row — isolating one part's contribution
      return (
        <svg {...common}>
          <rect x="3" y="9" width="5" height="6" rx="1" />
          <rect x="16" y="9" width="5" height="6" rx="1" />
          <path d="M8 12h2.5M15.5 12H13M11 9v6" strokeDasharray="1.5 2" />
        </svg>
      );
  }
}

function RigorCheckBadge({
  kind,
  risk,
  levelLabels = DATA_LEAKAGE_LABELS,
  linkBase = "",
}: {
  kind: RigorCheckKind;
  risk: ReproducibilityRisk | "not-addressed";
  levelLabels?: Record<ReproducibilityRisk | "not-addressed", string>;
  linkBase?: string;
}) {
  const label = RIGOR_CHECK_LABELS[kind];
  const href = RIGOR_CHECK_HREF[kind] && `${linkBase}${RIGOR_CHECK_HREF[kind]}`;
  const Tag = href ? "a" : "span";
  return (
    <Tag
      href={href}
      title={href ? `${label}: ${levelLabels[risk]}. Click to view the row.` : `${label}: ${levelLabels[risk]}`}
      className={`inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase${
        href ? " transition-colors hover:border-forest/50" : ""
      }`}
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[DATA_LEAKAGE_TONE[risk]]}`}>
        <RigorCheckGlyph kind={kind} />
      </span>
      {label}
    </Tag>
  );
}

function StatisticalConsistencyBadge({ status, linkBase = "" }: { status: StatisticalConsistencyStatus; linkBase?: string }) {
  const tone: Tone = status === "consistent" ? "green" : status === "issues-found" ? "red" : "gray";
  return (
    <a
      href={`${linkBase}#qa-statistic-accuracy`}
      title={`Statistic Accuracy: ${STATISTICAL_CONSISTENCY_LABELS[status]}. An independent recheck of the paper's own reported numbers (CIs, kappa bounds, table closure/monotonicity). Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[tone]}`}>
        <RigorCheckGlyph kind="statcheck" />
      </span>
      Statistic Accuracy
    </a>
  );
}

// Statistical Power glyph — a small gauge/dial, distinct from the other
// Rigor icons since this one only ever appears when a power analysis is
// actually on record (see getStatisticalPower's doc comment).
function StatisticalPowerGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M4 17a8 8 0 0 1 16 0" />
      <path d="M12 17l4.5-5.5" />
      <path d="M4 17h1M19 17h1M12 6.5v1" />
    </svg>
  );
}

function StatisticalPowerBadge({ status, linkBase = "" }: { status: StatisticalPowerStatus; linkBase?: string }) {
  const tone = TONE_BG[status === "adequate" ? "green" : "red"];
  return (
    <a
      href={`${linkBase}#qa-statistical-power`}
      title={`Statistical Power: ${STATISTICAL_POWER_LABELS[status]}. Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${tone}`}>
        <StatisticalPowerGlyph />
      </span>
      Statistical Power
    </a>
  );
}

// Code Quality glyph — a small braces/brackets mark, distinct from the
// repository-liveness glyphs since this measures the repo's own hygiene
// (license, citation metadata, registry listing) rather than whether the
// link resolves.
function CodeQualityGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M8 4L3 12l5 8" />
      <path d="M16 4l5 8-5 8" />
    </svg>
  );
}

function CodeQualityBadge({ score, linkBase = "" }: { score: CodeQualityScore; linkBase?: string }) {
  const tone: Tone = score >= 4 ? "green" : score >= 2 ? "gold" : "red";
  return (
    <a
      href={`${linkBase}#qa-code-quality-fair`}
      title={`Code Quality: ${score}/5 (fair-software.eu criteria via howfairis). Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[tone]}`}>
        <CodeQualityGlyph />
      </span>
      Code Quality {score}/5
    </a>
  );
}

// Data Quality glyph — a small database/cylinder mark, distinct from the
// code-braces glyph above since this measures the dataset's own FAIRness
// rather than the code repo's software hygiene.
function DataQualityGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <ellipse cx="12" cy="6" rx="8" ry="3" />
      <path d="M4 6v12c0 1.66 3.58 3 8 3s8-1.34 8-3V6" />
      <path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3" />
    </svg>
  );
}

function DataQualityBadge({ score, linkBase = "" }: { score: DataQualityScore; linkBase?: string }) {
  const tone: Tone = score >= 16 ? "green" : score >= 8 ? "gold" : "red";
  return (
    <a
      href={`${linkBase}#qa-data-quality-fair`}
      title={`Data Quality: ${score}/24 (FAIR-Checker; GitHub/GitLab-hosted data gets a +2 top-up if the repo has a real license file, since FAIR-Checker can't see repo content directly). Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 lowercase transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${TONE_BG[tone]}`}>
        <DataQualityGlyph />
      </span>
      Data Quality {score}/24
    </a>
  );
}

/** Transparency, Openness, Rigor, Extensibility, and integrity badges for a node. */
export default function TopBadges({ node }: { node: GraphNode }) {
  // Openness, Integrity, and the newer Rigor sub-checks (data leakage,
  // baseline adequacy, etc.) describe the paper's own practices/methodology,
  // not an individual excerpt — so on an EVD page they're read off the
  // parent SRC via its derivedFrom edge instead of the EVD's own (empty)
  // tags. Transparency and the validity-domain checks stay per-node below.
  const parentSource = node.type === "EVD" ? getParentSource(node.id) : null;
  const signalSource = parentSource ?? node;
  // EVD pages don't render their own Quality Appraisal/TRIPOD-LLM tables —
  // only the parent SRC page does — so every chip's anchor link must point
  // at the SRC page's URL when this is an EVD, regardless of whether the
  // chip's underlying value came from the EVD's own tags or the parent's
  // (validity/compliance are read per-node above; openness/integrity/rigor
  // sub-checks are inherited; either way the *table row* only exists on
  // the SRC page).
  const linkBase = parentSource ? `/nodes/${parentSource.id}` : "";
  // Registration/Protocol disclosure level is distinct from whether the
  // claimed data/code repo actually resolves — but the old Data/Code
  // disclosure-level chips duplicated what Data Repo Check/Code Check now
  // say more usefully (an actual liveness check, not just a disclosure
  // level), so only the two non-redundant TOP standards render here.
  const opennessSignals = getTopSignals(signalSource).filter(
    (s) => s.standard === "study-registration" || s.standard === "study-protocol"
  );
  const compliance = getReportingCompliance(node.id);
  const repro = getReproducibilityRisk(node);
  const validity = getValiditySignals(node);
  const integrity = getIntegritySignals(signalSource);
  const dataLeakage = getDataLeakageSignal(signalSource);
  const baselineAdequacy = getBaselineAdequacy(signalSource);
  const trainDevTest = getTrainDevTestHygiene(signalSource);
  const multipleComparisons = getMultipleComparisonsCorrection(signalSource);
  const humanBaseline = getHumanBaselineComparability(signalSource);
  const confidenceIntervals = getConfidenceIntervals(signalSource);
  const statisticalPower = getStatisticalPower(signalSource);
  const promptEngineering = getPromptEngineering(signalSource);
  const chanceCorrectedMetrics = getChanceCorrectedMetrics(signalSource);
  // Spin / Statistical Consistency / Repository & Code Check describe the
  // paper's own overall reporting practice, not one extracted finding —
  // same "paper-level, read via signalSource" reasoning as Openness/
  // Integrity/Rigor sub-checks above.
  const spin = getSpinSignal(signalSource);
  const ablationExperiments = getAblationExperiments(signalSource);
  const statisticalConsistency = getStatisticalConsistency(signalSource);
  const repositoryCheck = getRepositoryCheck(signalSource);
  const codeCheck = getCodeCheck(signalSource);
  const codeQualityFair = getCodeQualityFair(signalSource);
  const dataQualityFair = getDataQualityFair(signalSource);
  const aiWritingCheck = getAiWritingCheck(signalSource);

  const hasTransparency = Boolean(compliance);
  const hasOpenness =
    opennessSignals.length > 0 ||
    Boolean(repositoryCheck) ||
    Boolean(codeCheck) ||
    codeQualityFair !== null ||
    dataQualityFair !== null;
  const hasIntegrity = integrity.length > 0 || Boolean(aiWritingCheck);
  const hasRigor =
    validity.length > 0 ||
    Boolean(dataLeakage) ||
    Boolean(baselineAdequacy) ||
    Boolean(trainDevTest) ||
    Boolean(multipleComparisons) ||
    Boolean(humanBaseline) ||
    Boolean(confidenceIntervals) ||
    Boolean(statisticalPower) ||
    Boolean(promptEngineering) ||
    Boolean(chanceCorrectedMetrics) ||
    Boolean(statisticalConsistency) ||
    Boolean(spin) ||
    Boolean(ablationExperiments);

  if (!hasTransparency && !hasOpenness && !repro && !hasRigor && !hasIntegrity) return null;

  const summary = [
    hasTransparency && "Transparency",
    hasOpenness && "Openness",
    hasRigor && "Rigor",
    repro && "Extensibility",
    hasIntegrity && "Integrity",
  ]
    .filter(Boolean)
    .join(" · ");

  const opennessChips = [
    ...opennessSignals.map((s) => (
      <StandardBadge key={s.standard} standard={s.standard} level={s.level} linkBase={linkBase} />
    )),
    // Data Quality (FAIR-Checker) implies the data link was successfully
    // reached and assessed, which already subsumes "is the link live" —
    // same redundancy logic as Code Check vs. Code Quality above.
    repositoryCheck && dataQualityFair === null && (
      <RigorCheckBadge
        key="repository-check"
        kind="repository-check"
        risk={repositoryCheck}
        levelLabels={REPO_CHECK_LABELS}
        linkBase={linkBase}
      />
    ),
    dataQualityFair !== null && (
      <DataQualityBadge key="data-quality-fair" score={dataQualityFair} linkBase={linkBase} />
    ),
    // Code Quality (howfairis) implies the code repo was successfully
    // reached and analyzed, which already subsumes "is the link live" —
    // showing both chips would be redundant, so Code Check only renders
    // when there's no Code Quality score to fall back on.
    codeCheck && codeQualityFair === null && (
      <RigorCheckBadge
        key="code-check"
        kind="code-check"
        risk={codeCheck}
        levelLabels={REPO_CHECK_LABELS}
        linkBase={linkBase}
      />
    ),
    codeQualityFair !== null && (
      <CodeQualityBadge key="code-quality-fair" score={codeQualityFair} linkBase={linkBase} />
    ),
  ].filter(Boolean);

  // Rigor is organized into 5 labeled subrows rather than one flat/expandable
  // list: Validity (the 4 appraisal-domain risk verdicts), Design (how the
  // study/experiment was set up — splits, baselines, leakage, prompting),
  // Analyses (statistical methods applied to the results), Reporting
  // (whether the paper's own numbers check out), and Interpretation (how
  // results were framed/theorized once in). Each renders only if it has at
  // least one chip for this node.
  const validityChips = validity.map((v) => (
    <RiskBadge
      key={v.domain}
      label={VALIDITY_DOMAIN_LABELS[v.domain]}
      risk={v.risk}
      title={`${VALIDITY_DOMAIN_LABELS[v.domain]}: ${REPRODUCIBILITY_RISK_LABELS[v.risk]}`}
      glyph={<ValidityGlyph domain={v.domain} />}
      href={`${linkBase}#qa-${v.domain}`}
    />
  ));

  const designChips = [
    baselineAdequacy && (
      <RigorCheckBadge key="baseline-adequacy" kind="baseline-adequacy" risk={baselineAdequacy} linkBase={linkBase} />
    ),
    trainDevTest && (
      <RigorCheckBadge key="train-dev-test" kind="train-dev-test" risk={trainDevTest} linkBase={linkBase} />
    ),
    humanBaseline && (
      <RigorCheckBadge key="human-baseline" kind="human-baseline" risk={humanBaseline} linkBase={linkBase} />
    ),
    dataLeakage && <DataLeakageBadge key="data-leakage" risk={dataLeakage} linkBase={linkBase} />,
    promptEngineering && (
      <RigorCheckBadge key="prompt-engineering" kind="prompt-engineering" risk={promptEngineering} linkBase={linkBase} />
    ),
    ablationExperiments && (
      <RigorCheckBadge
        key="ablation-experiments"
        kind="ablation-experiments"
        risk={ablationExperiments}
        linkBase={linkBase}
      />
    ),
  ].filter(Boolean);

  const analysesChips = [
    confidenceIntervals && (
      <RigorCheckBadge
        key="confidence-intervals"
        kind="confidence-intervals"
        risk={confidenceIntervals}
        linkBase={linkBase}
      />
    ),
    statisticalPower && (
      <StatisticalPowerBadge key="statistical-power" status={statisticalPower} linkBase={linkBase} />
    ),
    multipleComparisons && (
      <RigorCheckBadge
        key="multiple-comparisons"
        kind="multiple-comparisons"
        risk={multipleComparisons}
        linkBase={linkBase}
      />
    ),
    chanceCorrectedMetrics && (
      <RigorCheckBadge
        key="chance-corrected-metrics"
        kind="chance-corrected-metrics"
        risk={chanceCorrectedMetrics}
        linkBase={linkBase}
      />
    ),
  ].filter(Boolean);

  const reportingChips = [
    statisticalConsistency && (
      <StatisticalConsistencyBadge key="statcheck" status={statisticalConsistency} linkBase={linkBase} />
    ),
  ].filter(Boolean);

  const interpretationChips = [
    spin && <RigorCheckBadge key="spin" kind="spin" risk={spin} linkBase={linkBase} />,
  ].filter(Boolean);

  const rigorGroups: [string, React.ReactNode[]][] = [
    ["Validity", validityChips],
    ["Design", designChips],
    ["Analyses", analysesChips],
    ["Reporting", reportingChips],
    ["Interpretation", interpretationChips],
  ];

  const extensibilityChips = [
    <ReminderBadge
      key="computationally-reproduced"
      label="Computationally Reproduced"
      title="Not yet independently reproduced: reminder to re-run this paper's own analysis/code ourselves and confirm the reported results."
    />,
    <ReminderBadge
      key="directly-replicated"
      label="Directly Replicated"
      title="Not yet directly replicated: reminder to run the same study design ourselves (same methods, new data) and compare results."
    />,
    <ReminderBadge
      key="indirectly-replicated"
      label="Indirectly Replicated"
      title="Not yet indirectly replicated: reminder to check whether independent studies using different methods reach the same conclusion."
    />,
  ];

  const integrityChips = [
    ...integrity.map((s) => (
      <IntegrityBadge key={s.kind} kind={s.kind} level={s.level} linkBase={linkBase} />
    )),
    aiWritingCheck && (
      <RigorCheckBadge
        key="ai-writing-check"
        kind="ai-writing-check"
        risk={aiWritingCheck}
        levelLabels={AI_WRITING_CHECK_LABELS}
        linkBase={linkBase}
      />
    ),
    <ReminderBadge
      key="plagiarism"
      label="Plagiarism"
      title="Not yet checked: reminder to screen this paper's text against other human-authored work for plagiarism or unattributed overlapping language."
    />,
  ].filter(Boolean);

  return (
    <CollapsibleSignalBlock summary={summary}>
      {hasTransparency && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Transparency
          </p>
          <ChipRows chips={[compliance && <ReportingComplianceBadge key="tripod-llm" compliance={compliance} linkBase={linkBase} />].filter(Boolean)} />
        </div>
      )}

      {hasOpenness && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Openness
          </p>
          <ChipRows chips={opennessChips} />
        </div>
      )}

      {hasRigor && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Rigor
          </p>
          <div className="mt-1.5 space-y-2">
            {rigorGroups.map(
              ([label, chips]) =>
                chips.length > 0 && (
                  <div key={label}>
                    <p className="text-[0.625rem] font-medium uppercase tracking-wide text-muted-ink/70">
                      {label}
                    </p>
                    {label === "Design" ? (
                      <ChipRows chips={chips} />
                    ) : (
                      <div className="mt-1 flex flex-wrap items-center gap-1.5">{chips}</div>
                    )}
                  </div>
                )
            )}
          </div>
        </div>
      )}

      {repro && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Extensibility
          </p>
          <ChipRows chips={extensibilityChips} />
        </div>
      )}

      {hasIntegrity && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Integrity
          </p>
          <ChipRows chips={integrityChips} />
        </div>
      )}
    </CollapsibleSignalBlock>
  );
}

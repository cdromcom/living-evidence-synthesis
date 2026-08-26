import Image from "next/image";
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
  getStatisticalPower,
  TOP_STANDARD_LABELS,
  TOP_LEVEL_LABELS,
  REPRODUCIBILITY_RISK_LABELS,
  VALIDITY_DOMAIN_LABELS,
  INTEGRITY_SIGNAL_LABELS,
  DISCLOSURE_LEVEL_LABELS,
  REPORTING_COMPLIANCE_LABELS,
  DATA_LEAKAGE_LABELS,
  RIGOR_CHECK_LABELS,
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
} from "@/lib/data";

// Transparency is now our own computed measure of adherence to reporting
// guidelines (TRIPOD-LLM) — did the paper report what it did, in enough
// detail to assess and reproduce. Openness covers all four COS TOP
// Guidelines standards (data, code, protocol, registration) — did the
// authors make the underlying artifacts and commitments openly available.
const COMPLIANCE_TONE: Record<ReportingCompliance["level"], string> = {
  high: "bg-emerald-600",
  moderate: "bg-amber-500",
  low: "bg-red-600",
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

function ReportingComplianceBadge({ compliance }: { compliance: ReportingCompliance }) {
  return (
    <a
      href="#tripod-llm-reporting-summary"
      title={`TRIPOD-LLM reporting-guideline adherence: ${compliance.pct}% of checklist items (Methods 5a-15, Results 16a-18) fully or partially reported: ${REPORTING_COMPLIANCE_LABELS[compliance.level].toLowerCase()} compliance. Hand-scored against the checklist, our own computed measure. Click to view the table.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${COMPLIANCE_TONE[compliance.level]}`}>
        <ReportingComplianceGlyph />
      </span>
      TRIPOD-LLM · {compliance.pct}% reported
    </a>
  );
}

// Center for Open Science's actual Open Science Badge artwork
// (cos.io/initiatives/badges, CC BY 4.0 — "free to use with attribution").
// OSF doesn't have a distinct "Open Code" badge, so Analytic Code
// Transparency borrows the Open Materials badge (materials explicitly
// includes code/software in OSF's own definition). Study Registration
// borrows the Preregistered badge image, but the tooltip always uses our
// own "Study Registration" TOP-standard language, not "preregistered" —
// item 14d in the source data means "was this study registered at all,"
// not the stricter "registered before data collection" that badge name
// implies. There's no official OSF badge for Study Protocol, so that one
// keeps an original glyph.
const BADGE_IMAGE: Partial<Record<TopStandard, { src: string; alt: string }>> = {
  "data-transparency": { src: "/badges/osf-open-data.png", alt: "Open Data badge" },
  "code-transparency": { src: "/badges/osf-open-materials.png", alt: "Open Materials badge" },
  "study-registration": { src: "/badges/osf-preregistered.png", alt: "Preregistered badge" },
};

const LEVEL_RING: Record<TopLevel, string> = {
  "level-2-shared": "border-emerald-600",
  "level-1-disclosed": "border-amber-500",
  "not-disclosed": "border-zinc-300",
  "not-applicable": "border-zinc-200",
};

const RISK_TONE: Record<ReproducibilityRisk, string> = {
  "low-risk": "bg-emerald-600",
  "some-concerns": "bg-amber-500",
  "high-risk": "bg-red-600",
};

// "not-addressed" (the paper doesn't discuss this at all) is deliberately
// gray, not red — it's an absence of discussion, not a confirmed problem.
// Reuses the same gray as TOP's "not-disclosed" ring for the same reason.
const DATA_LEAKAGE_TONE: Record<ReproducibilityRisk | "not-addressed", string> = {
  ...RISK_TONE,
  "not-addressed": "bg-zinc-400",
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

function ProtocolGlyph() {
  return (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <rect x="5" y="4" width="14" height="17" rx="2" />
      <path d="M9 3.5h6a1 1 0 0 1 1 1V6H8V4.5a1 1 0 0 1 1-1Z" />
      <path d="M8.5 12h7M8.5 16h5" />
    </svg>
  );
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

function IntegrityBadge({ kind, level }: { kind: IntegritySignalKind; level: DisclosureLevel }) {
  const earned = level === "disclosed";
  return (
    <span
      title={`${INTEGRITY_SIGNAL_LABELS[kind]}: ${DISCLOSURE_LEVEL_LABELS[level]}`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80"
    >
      <span
        className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${
          earned ? "bg-emerald-600" : level === "partial" ? "bg-amber-500" : "bg-zinc-400"
        }`}
      >
        <IntegrityGlyph kind={kind} />
      </span>
      {INTEGRITY_SIGNAL_LABELS[kind]}
    </span>
  );
}

function StandardBadge({ standard, level }: { standard: TopStandard; level: TopLevel }) {
  const img = BADGE_IMAGE[standard];
  // Only the official OSF badge criterion ("shared and cited in a trusted
  // repository") gets the full-color mark — anything less is shown
  // desaturated so we're never implying a badge was earned when it wasn't.
  const earned = level === "level-2-shared";

  return (
    <span
      title={`${TOP_STANDARD_LABELS[standard]}: ${TOP_LEVEL_LABELS[level]}`}
      className={`inline-flex items-center gap-1.5 rounded-full border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 ${LEVEL_RING[level]}`}
    >
      {img ? (
        <Image src={img.src} alt={img.alt} width={16} height={17.6} className={earned ? "" : "opacity-40 grayscale"} />
      ) : (
        <span
          className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${
            earned ? "bg-emerald-600" : level === "level-1-disclosed" ? "bg-amber-500" : "bg-zinc-400"
          }`}
        >
          <ProtocolGlyph />
        </span>
      )}
      {TOP_STANDARD_LABELS[standard]}
    </span>
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
    <span title={title} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80">
      <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-zinc-400 text-white">
        <ReminderGlyph />
      </span>
      {label}
    </span>
  );
}

function RiskBadge({ label, risk, title, glyph }: { label: string; risk: ReproducibilityRisk; title: string; glyph: React.ReactNode }) {
  return (
    <span title={title} className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80">
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${RISK_TONE[risk]}`}>{glyph}</span>
      {label}
    </span>
  );
}

function DataLeakageBadge({ risk }: { risk: ReproducibilityRisk | "not-addressed" }) {
  return (
    <a
      href="#qa-data-leakage"
      title={`Data leakage: ${DATA_LEAKAGE_LABELS[risk]}. Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${DATA_LEAKAGE_TONE[risk]}`}>
        <DataLeakageGlyph />
      </span>
      Data Leakage · {DATA_LEAKAGE_LABELS[risk]}
    </a>
  );
}

// Original glyphs for the four new benchmarking-specific Rigor checks — same
// reasoning as the other original glyphs on this page: no established open-
// licensed icon convention exists for these (they aren't TOP or TRIPOD-LLM
// fields, and aren't in Cochrane's RoB2 set either).
type RigorCheckKind = "baseline-adequacy" | "train-dev-test" | "multiple-comparisons" | "human-baseline";

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
  }
}

function RigorCheckBadge({ kind, risk }: { kind: RigorCheckKind; risk: ReproducibilityRisk | "not-addressed" }) {
  const label = RIGOR_CHECK_LABELS[kind];
  return (
    <a
      href={`#qa-${kind}`}
      title={`${label}: ${DATA_LEAKAGE_LABELS[risk]}. Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${DATA_LEAKAGE_TONE[risk]}`}>
        <RigorCheckGlyph kind={kind} />
      </span>
      {label} · {DATA_LEAKAGE_LABELS[risk]}
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

function StatisticalPowerBadge({ status }: { status: StatisticalPowerStatus }) {
  const tone = status === "adequate" ? "bg-emerald-600" : "bg-amber-500";
  return (
    <a
      href="#qa-statistical-power"
      title={`${STATISTICAL_POWER_LABELS[status]}. Click to view the row.`}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
    >
      <span className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${tone}`}>
        <StatisticalPowerGlyph />
      </span>
      Statistical Power · {STATISTICAL_POWER_LABELS[status]}
    </a>
  );
}

/** Transparency, Openness, Rigor, Extensibility, and integrity badges for a node. */
export default function TopBadges({ node }: { node: GraphNode }) {
  const opennessSignals = getTopSignals(node);
  const compliance = getReportingCompliance(node.id);
  const repro = getReproducibilityRisk(node);
  const validity = getValiditySignals(node);
  const integrity = getIntegritySignals(node);
  const dataLeakage = getDataLeakageSignal(node);
  const baselineAdequacy = getBaselineAdequacy(node);
  const trainDevTest = getTrainDevTestHygiene(node);
  const multipleComparisons = getMultipleComparisonsCorrection(node);
  const humanBaseline = getHumanBaselineComparability(node);
  const statisticalPower = getStatisticalPower(node);

  if (
    !compliance &&
    opennessSignals.length === 0 &&
    !repro &&
    validity.length === 0 &&
    integrity.length === 0 &&
    !dataLeakage &&
    !baselineAdequacy &&
    !trainDevTest &&
    !multipleComparisons &&
    !humanBaseline &&
    !statisticalPower
  )
    return null;

  return (
    <div className="mt-3 max-w-[70%] space-y-3">
      {compliance && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Transparency
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
            <ReportingComplianceBadge compliance={compliance} />
          </div>
        </div>
      )}

      {opennessSignals.length > 0 && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Openness
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
            {opennessSignals.map((s) => (
              <StandardBadge key={s.standard} standard={s.standard} level={s.level} />
            ))}
          </div>
        </div>
      )}

      {(validity.length > 0 ||
        dataLeakage ||
        baselineAdequacy ||
        trainDevTest ||
        multipleComparisons ||
        humanBaseline ||
        statisticalPower) && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Rigor
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
            {validity.map((v) => (
              <RiskBadge
                key={v.domain}
                label={VALIDITY_DOMAIN_LABELS[v.domain]}
                risk={v.risk}
                title={`${VALIDITY_DOMAIN_LABELS[v.domain]}: ${REPRODUCIBILITY_RISK_LABELS[v.risk]}`}
                glyph={<ValidityGlyph domain={v.domain} />}
              />
            ))}
            {dataLeakage && <DataLeakageBadge risk={dataLeakage} />}
            {baselineAdequacy && <RigorCheckBadge kind="baseline-adequacy" risk={baselineAdequacy} />}
            {trainDevTest && <RigorCheckBadge kind="train-dev-test" risk={trainDevTest} />}
            {multipleComparisons && <RigorCheckBadge kind="multiple-comparisons" risk={multipleComparisons} />}
            {humanBaseline && <RigorCheckBadge kind="human-baseline" risk={humanBaseline} />}
            {statisticalPower && <StatisticalPowerBadge status={statisticalPower} />}
          </div>
        </div>
      )}

      {repro && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Extensibility
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
            <ReminderBadge
              label="Computationally Reproduced"
              title="Not yet independently reproduced: reminder to re-run this paper's own analysis/code ourselves and confirm the reported results."
            />
            <ReminderBadge
              label="Directly Replicated"
              title="Not yet directly replicated: reminder to run the same study design ourselves (same methods, new data) and compare results."
            />
            <ReminderBadge
              label="Indirectly Replicated"
              title="Not yet indirectly replicated: reminder to check whether independent studies using different methods reach the same conclusion."
            />
          </div>
        </div>
      )}

      {integrity.length > 0 && (
        <div>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            Integrity
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
            {integrity.map((s) => (
              <IntegrityBadge key={s.kind} kind={s.kind} level={s.level} />
            ))}
            <ReminderBadge
              label="Plagiarism"
              title="Not yet checked: reminder to screen this paper's text against other human-authored work for plagiarism or unattributed overlapping language."
            />
          </div>
        </div>
      )}
    </div>
  );
}

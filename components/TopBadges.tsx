import {
  getTopSignals,
  getReproducibilityRisk,
  TOP_STANDARD_LABELS,
  TOP_LEVEL_LABELS,
  REPRODUCIBILITY_RISK_LABELS,
  type GraphNode,
  type TopStandard,
  type TopLevel,
  type ReproducibilityRisk,
} from "@/lib/data";

// Circular badge + single glyph mirrors the visual language of COS's Open
// Science Badges and NIH/NINDS's rigor icons, but these are original SVGs —
// not reproductions of their (copyrighted) artwork.
const LEVEL_TONE: Record<TopLevel, string> = {
  "level-2-shared": "bg-emerald-600",
  "level-1-disclosed": "bg-amber-500",
  "not-disclosed": "bg-zinc-400",
  "not-applicable": "bg-zinc-300",
};

const REPRO_TONE: Record<ReproducibilityRisk, string> = {
  "low-risk": "bg-emerald-600",
  "some-concerns": "bg-amber-500",
  "high-risk": "bg-red-600",
};

function Glyph({ standard }: { standard: TopStandard }) {
  const common = { width: 10, height: 10, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2.4, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  switch (standard) {
    case "data-transparency":
      // open padlock — data made accessible
      return (
        <svg {...common}>
          <rect x="4" y="11" width="16" height="10" rx="2" />
          <path d="M8 11V7a4 4 0 0 1 7.5-2" />
        </svg>
      );
    case "code-transparency":
      // angle brackets — analytic code
      return (
        <svg {...common}>
          <polyline points="9 6 3 12 9 18" />
          <polyline points="15 6 21 12 15 18" />
        </svg>
      );
    case "study-protocol":
      // clipboard/checklist — protocol document
      return (
        <svg {...common}>
          <rect x="5" y="4" width="14" height="17" rx="2" />
          <path d="M9 3.5h6a1 1 0 0 1 1 1V6H8V4.5a1 1 0 0 1 1-1Z" />
          <path d="M8.5 12h7M8.5 16h5" />
        </svg>
      );
    case "study-registration":
      // seal/stamp — registered
      return (
        <svg {...common}>
          <circle cx="12" cy="10" r="6" />
          <path d="M9 15.5 7.5 21l4.5-2.5L16.5 21 15 15.5" />
        </svg>
      );
  }
}

/** Transparency & rigor badges for a node, aligned to COS's TOP Guidelines vocabulary. */
export default function TopBadges({ node }: { node: GraphNode }) {
  const signals = getTopSignals(node);
  const repro = getReproducibilityRisk(node);
  if (signals.length === 0 && !repro) return null;

  return (
    <div className="mt-3">
      <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
        Transparency &amp; rigor <span className="font-normal normal-case">(COS TOP Guidelines)</span>
      </p>
      <div className="mt-1.5 flex flex-wrap gap-1.5">
        {signals.map((s) => (
          <span
            key={s.standard}
            title={`${TOP_STANDARD_LABELS[s.standard]}: ${TOP_LEVEL_LABELS[s.level]}`}
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80"
          >
            <span
              className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full text-white ${LEVEL_TONE[s.level]}`}
            >
              <Glyph standard={s.standard} />
            </span>
            {TOP_STANDARD_LABELS[s.standard]}
          </span>
        ))}
        {repro && (
          <span
            title={`Reproducibility risk (Critical Appraisal): ${REPRODUCIBILITY_RISK_LABELS[repro]}`}
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80"
          >
            <span aria-hidden className={`h-3 w-3 shrink-0 rounded-full ${REPRO_TONE[repro]}`} />
            Reproducibility
          </span>
        )}
      </div>
    </div>
  );
}

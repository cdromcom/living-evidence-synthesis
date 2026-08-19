import Image from "next/image";
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

const REPRO_TONE: Record<ReproducibilityRisk, string> = {
  "low-risk": "bg-emerald-600",
  "some-concerns": "bg-amber-500",
  "high-risk": "bg-red-600",
};

function ProtocolGlyph() {
  return (
    <svg
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2.4}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <rect x="5" y="4" width="14" height="17" rx="2" />
      <path d="M9 3.5h6a1 1 0 0 1 1 1V6H8V4.5a1 1 0 0 1 1-1Z" />
      <path d="M8.5 12h7M8.5 16h5" />
    </svg>
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
        <Image
          src={img.src}
          alt={img.alt}
          width={16}
          height={17.6}
          className={earned ? "" : "opacity-40 grayscale"}
        />
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
      <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
        {signals.map((s) => (
          <StandardBadge key={s.standard} standard={s.standard} level={s.level} />
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
      <p className="mt-1.5 text-[0.625rem] text-muted-ink">
        Open Data / Open Materials / Preregistered badge artwork ©{" "}
        <a href="https://www.cos.io/initiatives/badges" className="underline hover:text-forest">
          Center for Open Science
        </a>
        , CC BY 4.0. Shown full-color only at Level 2 (Shared and Cited); desaturated below that
        threshold — no badge here implies it was independently certified.
      </p>
    </div>
  );
}

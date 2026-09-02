import ScaleTooltip from "@/components/ScaleTooltip";
import { CAVEAT_SEVERITY_SCALE } from "@/lib/scales";

type Severity = "low" | "moderate" | "high";
type CaveatType = "author-stated" | "inferred";

const SEVERITY_LABEL: Record<Severity, string> = {
  low: "Low severity",
  moderate: "Moderate severity",
  high: "High severity",
};

const SEVERITY_TONE: Record<Severity, string> = {
  low: "border-zinc-300 text-muted-ink",
  moderate: "border-amber-500 text-amber-700",
  high: "border-red-600 text-red-700",
};

const TYPE_LABEL: Record<CaveatType, string> = {
  "author-stated": "Author-stated limitation",
  inferred: "Inferred by curator",
};

/** Severity + provenance pills for CVT (caveat) nodes. */
export default function CaveatMeta({
  severity,
  caveatType,
}: {
  severity?: Severity;
  caveatType?: CaveatType;
}) {
  if (!severity && !caveatType) return null;
  return (
    <div className="mt-3 flex flex-wrap items-center gap-1.5">
      {severity && (
        <ScaleTooltip
          scale={CAVEAT_SEVERITY_SCALE}
          current={severity}
          description={`${SEVERITY_LABEL[severity]}: how consequential this limitation is for interpreting the source's findings.`}
        >
          <span
            className={`inline-flex items-center rounded-full border bg-card px-2.5 py-1 text-xs font-medium ${SEVERITY_TONE[severity]}`}
          >
            {SEVERITY_LABEL[severity]}
          </span>
        </ScaleTooltip>
      )}
      {caveatType && (
        <span
          title={
            caveatType === "author-stated"
              ? "The paper's own authors identified this limitation"
              : "This limitation was identified by the curator, not stated by the paper's authors"
          }
          className="inline-flex items-center rounded-full border border-border bg-card px-2.5 py-1 text-xs text-ink/70"
        >
          {TYPE_LABEL[caveatType]}
        </span>
      )}
    </div>
  );
}

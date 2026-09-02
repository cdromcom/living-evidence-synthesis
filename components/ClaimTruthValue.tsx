import ScaleTooltip from "@/components/ScaleTooltip";
import { TRUTH_VALUE_SCALE } from "@/lib/scales";

const TONE = {
  high: "border-emerald-600 text-emerald-700",
  medium: "border-amber-500 text-amber-700",
  low: "border-red-600 text-red-700",
} as const;

const BAR_COLOR = {
  high: "bg-emerald-600",
  medium: "bg-amber-500",
  low: "bg-red-600",
} as const;

function bandFor(v: number): keyof typeof TONE {
  if (v >= 0.66) return "high";
  if (v >= 0.33) return "medium";
  return "low";
}

/** Visual truth-value indicator for CLM/EP nodes — a percentage badge plus a small fill bar. */
export default function ClaimTruthValue({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const band = bandFor(value);
  return (
    <ScaleTooltip
      scale={TRUTH_VALUE_SCALE}
      current={band}
      description={`Truth value ${pct}%: curator-assessed confidence that this claim is well-supported by the cited evidence, on a 0-100% scale.`}
    >
      <span className={`inline-flex items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs ${TONE[band]}`}>
        <span className="font-semibold">Truth value {pct}%</span>
        <span className="h-1.5 w-16 overflow-hidden rounded-full bg-muted-surface">
          <span
            className={`block h-full rounded-full ${BAR_COLOR[band]}`}
            style={{ width: `${pct}%` }}
          />
        </span>
      </span>
    </ScaleTooltip>
  );
}

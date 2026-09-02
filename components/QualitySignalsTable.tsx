import ScaleTooltip from "@/components/ScaleTooltip";
import { TONE_BG, type Scale, type Tone } from "@/lib/scales";

export type SignalRow = {
  /** What is being assessed, e.g. "Data leakage". */
  label: string;
  /** Where this node landed on that signal's scale, e.g. "Unresolved". */
  status: string;
  tone: Tone;
  /** Anchor to the row in the Quality-appraisal or TRIPOD table, when there is one. */
  href?: string;
  /** Full scale + current key, so hovering still shows every possible level. */
  scale?: Scale;
  current?: string;
  /** One-line description shown above the scale on hover. */
  description?: string;
};

export type SignalGroup = {
  name: string;
  /** Optional second-level grouping used by Rigor (Validity / Design / …). */
  subgroup?: string;
  rows: SignalRow[];
};

/**
 * Prototype: the quality signals as an aligned table rather than a cloud of
 * pills.
 *
 * The chip layout put ~24 variable-width pills into wrapped rows, so nothing
 * lined up and the eye had no column to run down — every signal had to be read
 * individually. A table gives one row per signal with the status in a fixed
 * column, which is what makes a checklist scannable. It sits behind the same
 * "Show / Hide Quality Signals" button as before.
 *
 * The scale hover card is attached inside the label cell rather than around the
 * row: `ScaleTooltip` renders a span, and a span may not wrap a `<tr>`.
 */
export default function QualitySignalsTable({ groups }: { groups: SignalGroup[] }) {
  const live = groups.filter((g) => g.rows.length > 0);
  if (live.length === 0) return null;

  return (
    <div className="space-y-3">
      {live.map((group) => (
        <div key={`${group.name}-${group.subgroup ?? ""}`}>
          <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
            {group.name}
            {group.subgroup && (
              <span className="ml-1.5 font-medium normal-case tracking-normal text-muted-ink/70">
                {group.subgroup}
              </span>
            )}
          </p>
          <table className="mt-1 w-full max-w-xl border-collapse text-[0.6875rem]">
            <tbody>
              {group.rows.map((row) => {
                const name = row.href ? (
                  <a href={row.href} className="text-ink/90 transition-colors hover:text-forest hover:underline">
                    {row.label}
                  </a>
                ) : (
                  <span className="text-ink/90">{row.label}</span>
                );

                return (
                  <tr key={row.label} className="border-b border-border/60 last:border-0">
                    <td className="w-[58%] py-1 pr-3 align-baseline">
                      {row.scale && row.current ? (
                        <ScaleTooltip
                          scale={row.scale}
                          current={row.current}
                          description={row.description ?? `${row.label}: ${row.status}.`}
                        >
                          {name}
                        </ScaleTooltip>
                      ) : (
                        name
                      )}
                    </td>
                    <td className="py-1 align-baseline">
                      <span className="inline-flex items-baseline gap-1.5">
                        <span
                          className={`mt-[0.3rem] inline-block h-2 w-2 shrink-0 rounded-full ${TONE_BG[row.tone]}`}
                          aria-hidden
                        />
                        <span className="text-muted-ink">{row.status}</span>
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}

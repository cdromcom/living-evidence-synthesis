import ScaleTooltip from "@/components/ScaleTooltip";
import { TONE_BG, type Scale, type Tone } from "@/lib/scales";

export type SignalRow = {
  /** What is being assessed, e.g. "Data leakage". */
  label: string;
  /** Where this node landed on that signal's scale, e.g. "unresolved". */
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

/** A band of rows under a category, e.g. Rigor › Validity. */
export type SignalSection = { subgroup?: string; rows: SignalRow[] };

export type SignalGroup = { name: string; sections: SignalSection[] };

function Rows({ rows }: { rows: SignalRow[] }) {
  return (
    <>
      {rows.map((row) => {
        const name = row.href ? (
          <a href={row.href} className="transition-colors hover:text-forest hover:underline">
            {row.label}
          </a>
        ) : (
          <span>{row.label}</span>
        );
        return (
          <tr key={row.label} className="border-t border-border/50">
            <th scope="row" className="w-[55%] py-[3px] pr-2 text-left align-baseline font-normal text-ink/90">
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
            </th>
            <td className="py-[3px] align-baseline">
              <span className="inline-flex items-baseline gap-1.5">
                <span
                  className={`mt-[0.32rem] inline-block h-[7px] w-[7px] shrink-0 rounded-full ${TONE_BG[row.tone]}`}
                  aria-hidden
                />
                <span className="lowercase text-muted-ink">{row.status}</span>
              </span>
            </td>
          </tr>
        );
      })}
    </>
  );
}

/**
 * The quality signals as a nutrition-style panel.
 *
 * Two things drive the layout. Category names are printed once and their
 * sub-bands nest underneath, rather than "RIGOR" repeating over four separate
 * blocks; and the categories run in two columns so the panel is landscape
 * rather than a single long strip, which is what let the old chip cloud push
 * the article far down the page.
 *
 * Rules do the hierarchy the way a nutrition label does: a heavy rule opens the
 * panel, a medium rule separates categories, hairlines separate rows. Colour is
 * never the only signal — every dot is followed by its status in words.
 */
export default function QualitySignalsTable({ groups }: { groups: SignalGroup[] }) {
  const live = groups
    .map((g) => ({ ...g, sections: g.sections.filter((s) => s.rows.length > 0) }))
    .filter((g) => g.sections.length > 0);
  if (live.length === 0) return null;

  // The single tallest category gets its own column; everything else stacks in
  // the other. Ties and small panels fall back to a plain stack.
  const rowsIn = (g: SignalGroup) => g.sections.reduce((n, s) => n + s.rows.length, 0);
  const biggest = live.reduce((a, b) => (rowsIn(b) > rowsIn(a) ? b : a), live[0]);
  const tall = live.length > 2 && rowsIn(biggest) >= 6 ? biggest : null;

  return (
    <section
      aria-label="Quality signals"
      className="mt-2 border border-ink/70 bg-card px-3 pb-2 pt-1.5 text-[0.6875rem] leading-snug"
    >
      <p className="border-b-[5px] border-ink/80 pb-1 font-semibold uppercase tracking-[0.08em] text-ink">
        Quality signals
      </p>

      {/* Explicit columns rather than CSS `columns-2`: Rigor carries roughly as
          many rows as every other category combined, so letting the browser flow
          them balances on height and leaves one column half empty. */}
      <div className="grid items-start gap-x-7 sm:grid-cols-2">
        {[tall ? live.filter((g) => g !== tall) : live, tall ? [tall] : []].map((column, ci) => (
          <div key={ci}>
            {column.map((group) => (
              <div key={group.name}>
                <p className="mt-2 border-b-2 border-ink/60 pb-[2px] font-semibold uppercase tracking-[0.06em] text-ink">
                  {group.name}
                </p>
                {group.sections.map((section, i) => (
                  <div key={section.subgroup ?? i}>
                    {section.subgroup && (
                      <p className="mt-1 text-[0.625rem] font-medium uppercase tracking-wide text-muted-ink/80">
                        {section.subgroup}
                      </p>
                    )}
                    <table className="w-full border-collapse">
                      <tbody>
                        <Rows rows={section.rows} />
                      </tbody>
                    </table>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}

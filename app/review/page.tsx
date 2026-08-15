import { getCurationStatusMatrix, NODE_TYPE_ORDER } from "@/lib/data";
import { VERDICT_VOCAB } from "@/lib/ui";
import NodeTypeBadge from "@/components/NodeTypeBadge";
import LiveReviewPanel from "@/components/LiveReviewPanel";

export const metadata = { title: "Review — Living Evidence Synthesis" };

export default function ReviewPage() {
  const matrix = getCurationStatusMatrix();
  const allStatuses = Array.from(
    new Set(NODE_TYPE_ORDER.flatMap((t) => Object.keys(matrix[t])))
  ).sort();

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">Review status</h1>
      <p className="mt-1 max-w-[65ch] text-sm text-muted-ink">
        Curation status across the corpus (frozen at the last vault export),
        plus live, sign-in-gated accuracy verdicts submitted by reviewers.
      </p>

      <section className="mt-8">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
          Live review submissions
        </h2>
        <LiveReviewPanel />
      </section>

      <section className="mt-10">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
          Curation status by node type
        </h2>
        <div className="mt-3 overflow-x-auto rounded-lg border border-border">
          <table className="w-full min-w-[560px] border-collapse text-sm">
            <thead>
              <tr className="bg-muted-surface">
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Type
                </th>
                {allStatuses.map((s) => (
                  <th
                    key={s}
                    className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink"
                  >
                    {s}
                  </th>
                ))}
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Total
                </th>
              </tr>
            </thead>
            <tbody>
              {NODE_TYPE_ORDER.map((t) => {
                const row = matrix[t];
                const total = Object.values(row).reduce((a, b) => a + b, 0);
                return (
                  <tr key={t} className="border-t border-border">
                    <td className="p-3">
                      <NodeTypeBadge type={t} />
                    </td>
                    {allStatuses.map((s) => {
                      const count = row[s] || 0;
                      const pct = total ? (count / total) * 100 : 0;
                      return (
                        <td key={s} className="p-3">
                          {count > 0 ? (
                            <div className="flex items-center gap-2">
                              <div className="mono w-6 text-right text-xs">
                                {count}
                              </div>
                              <div className="h-1.5 w-20 overflow-hidden rounded-full bg-muted-surface">
                                <div
                                  className="h-full bg-forest"
                                  style={{ width: `${pct}%` }}
                                />
                              </div>
                            </div>
                          ) : (
                            <span className="text-xs text-muted-ink">—</span>
                          )}
                        </td>
                      );
                    })}
                    <td className="mono p-3 text-sm font-semibold">{total}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-10">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
          Review verdict vocabulary
        </h2>
        <p className="mt-1 max-w-[65ch] text-sm text-muted-ink">
          The spec&apos;s five-state vocabulary for human review of
          AI-proposed discourse-node content — the same options offered on
          each node&apos;s review form above.
        </p>
        <ul className="mt-4 space-y-2">
          {VERDICT_VOCAB.map((v) => (
            <li
              key={v.key}
              className="flex items-start gap-3 rounded-lg border border-border bg-card p-3.5"
            >
              <span
                className="mono flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-semibold text-white"
                style={{ backgroundColor: v.color }}
              >
                {v.symbol}
              </span>
              <div>
                <div className="text-sm font-semibold">{v.label}</div>
                <div className="text-sm text-muted-ink">{v.description}</div>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}

"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  PROMPT_DIMENSIONS,
  variedShotCount,
  type PromptDimension,
  type PromptTactics,
} from "@/lib/promptTactics";

const SHOT: PromptDimension[] = ["zero", "one", "few"];

/** A tactic used by fewer than a quarter of the corpus is worth marking. */
function isRare(n: number, total: number) {
  return n <= Math.floor(total / 4);
}

function Mark({ row, dim }: { row: PromptTactics; dim: PromptDimension }) {
  const used = (row.tactics as string[]).includes(dim);
  if (!used) return <span className="text-border">·</span>;
  const varied = SHOT.includes(dim) && variedShotCount(row);
  return (
    <span className={varied ? "text-amber-600" : "text-forest"} title={varied ? "varied as a condition" : "used"}>
      {varied ? "◆" : "●"}
    </span>
  );
}

export default function PromptTacticsExplorer({ rows }: { rows: PromptTactics[] }) {
  const [active, setActive] = useState<PromptDimension[]>([]);
  const [open, setOpen] = useState<string | null>(null);

  const counts = useMemo(
    () =>
      PROMPT_DIMENSIONS.map((d) => ({
        ...d,
        n: rows.filter((r) => (r.tactics as string[]).includes(d.key)).length,
      })).sort((a, b) => b.n - a.n),
    [rows]
  );

  const shown = useMemo(
    () => rows.filter((r) => active.every((k) => (r.tactics as string[]).includes(k))),
    [rows, active]
  );

  const toggle = (k: PromptDimension) =>
    setActive((cur) => (cur.includes(k) ? cur.filter((x) => x !== k) : [...cur, k]));

  return (
    <>
      <section className="mt-8">
        <h2 className="text-lg font-semibold">Almost everyone prompts zero-shot, once</h2>
        <p className="mt-1 max-w-[68ch] text-sm text-muted-ink">
          Every square is one of the {rows.length} sources that uses the tactic, ranked most to
          least. Amber marks the tactics fewer than a quarter of the corpus uses — the corners of
          the design space that remain unexplored.
        </p>

        <div className="mt-4 grid max-w-2xl gap-[7px]">
          {counts.map((c) => {
            const rare = isRare(c.n, rows.length);
            return (
              <div key={c.key} className="grid items-center gap-3" style={{ gridTemplateColumns: "12.5rem auto 2.75rem" }}>
                <div className="text-[0.8125rem] lowercase text-ink">{c.label}</div>
                <div
                  className="flex gap-[2px]"
                  role="img"
                  aria-label={`${c.n} of ${rows.length} sources use ${c.label}`}
                >
                  {Array.from({ length: c.n }, (_, i) => (
                    <span
                      key={i}
                      className={`h-[15px] w-[13px] rounded-[1.5px] ${rare ? "bg-amber-500" : "bg-forest"}`}
                    />
                  ))}
                </div>
                <div className="text-right font-mono text-xs tabular-nums text-muted-ink">
                  {c.n}
                  <span className="text-border">/{rows.length}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="mt-10">
        <h2 className="text-lg font-semibold">The grid</h2>
        <p className="mt-1 max-w-[68ch] text-sm text-muted-ink">
          A source with more than one shot column filled is one that <em>varied</em> shot count as
          an experimental condition rather than fixing it — three sources do this. The last three
          columns describe the run rather than the prompt. Across all eleven, the {rows.length}{" "}
          sources produce <strong className="text-ink">23 distinct combinations</strong>: only three
          papers share a bundle with anyone else, so there is no house style to speak of.
        </p>

        <div className="mt-4 flex flex-wrap items-center gap-1.5">
          <span className="mr-1 font-mono text-[0.625rem] uppercase tracking-wide text-muted-ink">
            Filter
          </span>
          {PROMPT_DIMENSIONS.map((d) => {
            const on = active.includes(d.key);
            return (
              <button
                key={d.key}
                type="button"
                aria-pressed={on}
                onClick={() => toggle(d.key)}
                className={`rounded-full border px-3 py-1 text-xs transition-colors ${
                  on
                    ? "border-forest bg-forest font-medium text-paper"
                    : "border-border bg-card text-ink hover:border-forest/50"
                }`}
              >
                {d.label}
              </button>
            );
          })}
          {active.length > 0 && (
            <button
              type="button"
              onClick={() => setActive([])}
              className="ml-1 text-xs text-muted-ink underline hover:text-forest"
            >
              clear
            </button>
          )}
        </div>

        <div className="mt-2 flex flex-wrap gap-4 text-xs text-muted-ink">
          <span>
            <span className="text-forest">●</span> tactic used
          </span>
          <span>
            <span className="text-amber-600">◆</span> varied as a condition
          </span>
          <span>
            <span className="text-border">·</span> not used, or not reported
          </span>
        </div>

        <div className="mt-3 overflow-x-auto rounded-md border border-border bg-card">
          <table className="w-full min-w-[54rem] border-collapse text-sm">
            <thead>
              <tr className="bg-muted-surface">
                <th className="sticky left-0 z-10 bg-muted-surface px-4 py-2 text-left font-mono text-[0.625rem] uppercase tracking-wide text-muted-ink">
                  Source
                </th>
                {PROMPT_DIMENSIONS.map((d) => (
                  <th
                    key={d.key}
                    className={`px-1.5 py-2 text-center align-bottom font-mono text-[0.625rem] font-medium uppercase leading-tight tracking-wide text-muted-ink ${
                      d.group !== "shot" && PROMPT_DIMENSIONS.find((x) => x.group === d.group)?.key === d.key
                        ? "border-l border-border"
                        : ""
                    }`}
                  >
                    {d.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {shown.map((r) => {
                const isOpen = open === r.srcId;
                return (
                  <tr key={r.srcId} className="border-t border-border align-top">
                    <td className="sticky left-0 z-10 bg-card px-4 py-2">
                      <button
                        type="button"
                        onClick={() => setOpen(isOpen ? null : r.srcId)}
                        aria-expanded={isOpen}
                        className="text-left"
                      >
                        <span className="font-medium text-ink">{r.author}</span>{" "}
                        <span className="font-mono text-xs tabular-nums text-muted-ink">
                          {r.year ?? "n.d."}
                        </span>
                        <span className="ml-1.5 text-[0.625rem] text-muted-ink">
                          {isOpen ? "▲" : "▼"}
                        </span>
                      </button>
                      {isOpen && (
                        <div className="mt-2 max-w-[52ch] space-y-2 border-l-2 border-forest pl-3">
                          <p className="font-mono text-[0.625rem] uppercase tracking-wide text-muted-ink">
                            {r.prompts.length === 1
                              ? "1 prompt reported"
                              : `${r.prompts.length} prompts reported`}
                          </p>
                          <ul className="space-y-2.5">
                            {r.prompts.map((f, i) => (
                              <li key={`${f.item}-${i}`}>
                                <p className="font-mono text-[0.5625rem] uppercase tracking-wide text-muted-ink">
                                  {f.label}
                                  <span className="ml-1.5 text-border">TRIPOD {f.item}</span>
                                </p>
                                <blockquote className="mt-0.5 text-[0.8125rem] italic leading-relaxed text-ink">
                                  {f.text}
                                </blockquote>
                                {f.locator && (
                                  <p className="mt-0.5 font-mono text-[0.625rem] text-muted-ink">
                                    {f.locator}
                                  </p>
                                )}
                              </li>
                            ))}
                          </ul>
                          <p className="text-xs text-muted-ink">{r.reading}</p>
                          <p className="font-mono text-[0.6875rem] text-muted-ink">
                            Temperature{" "}
                            <span className="text-ink">{r.temperature ?? "not reported"}</span>
                          </p>
                          <Link
                            href={`/nodes/${r.srcId}`}
                            className="inline-block text-xs text-forest hover:underline"
                          >
                            Open {r.srcId} →
                          </Link>
                        </div>
                      )}
                    </td>
                    {PROMPT_DIMENSIONS.map((d) => (
                      <td
                        key={d.key}
                        className={`px-1.5 py-2 text-center font-mono ${
                          d.group !== "shot" && PROMPT_DIMENSIONS.find((x) => x.group === d.group)?.key === d.key
                            ? "border-l border-border"
                            : ""
                        }`}
                      >
                        <Mark row={r} dim={d.key} />
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {shown.length === 0 && (
          <p className="mt-3 text-sm text-muted-ink">
            No source uses every selected tactic. Clear a filter.
          </p>
        )}
        {shown.length > 0 && active.length > 0 && (
          <p className="mt-2 text-xs text-muted-ink">
            {shown.length} of {rows.length} sources match.
          </p>
        )}
      </section>
    </>
  );
}

"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { QUALITY_COLUMNS, QUALITY_COLUMN_GROUPS, type Cell, type Tone } from "@/lib/qualityColumns";

export type QualityRow = {
  evdId: string;
  evdTitle: string;
  srcId: string | null;
  eps: { id: string; title: string }[];
  values: Record<string, Cell>;
};

function cellText(cell: Cell): string {
  return cell ? cell.text : "—";
}

// Rank a cell's underlying judgment from best to worst so sorting a signal
// column clusters green→gold→red, with "no data" always last — the same
// good→bad ordering the color coding used to carry, just expressed as a
// sort key now that cells render in plain text.
const TONE_RANK: Record<Tone, number> = { green: 0, gold: 1, red: 2, gray: 3 };
function sortRank(cell: Cell): number {
  return cell ? TONE_RANK[cell.tone] : 4;
}

function downloadBlob(filename: string, blob: Blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function csvEscape(value: string): string {
  if (/[",\n]/.test(value)) return `"${value.replace(/"/g, '""')}"`;
  return value;
}

type SortKey = "ep" | "evidence" | "source" | string;
type SortState = { key: SortKey; direction: "asc" | "desc" } | null;

export default function EvidenceQualityTable({ rows }: { rows: QualityRow[] }) {
  const [visible, setVisible] = useState<Set<string>>(
    () => new Set(QUALITY_COLUMNS.filter((c) => c.defaultVisible).map((c) => c.id))
  );
  const [showSource, setShowSource] = useState(false);
  const [pickerOpen, setPickerOpen] = useState(false);
  const [exportMenuOpen, setExportMenuOpen] = useState(false);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortState>(null);

  const columns = useMemo(() => QUALITY_COLUMNS.filter((c) => visible.has(c.id)), [visible]);

  function toggleColumn(id: string) {
    setVisible((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function toggleSort(key: SortKey) {
    setSort((prev) => {
      if (!prev || prev.key !== key) return { key, direction: "asc" };
      if (prev.direction === "asc") return { key, direction: "desc" };
      return null;
    });
  }

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter((row) => {
      const haystack = [
        row.evdTitle,
        row.srcId ?? "",
        ...row.eps.flatMap((ep) => [ep.id, ep.title]),
      ]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [rows, search]);

  const sorted = useMemo(() => {
    if (!sort) return filtered;
    const list = [...filtered];
    const dir = sort.direction === "asc" ? 1 : -1;
    list.sort((a, b) => {
      if (sort.key === "ep") {
        const aKey = a.eps[0]?.id ?? "";
        const bKey = b.eps[0]?.id ?? "";
        return aKey.localeCompare(bKey) * dir;
      }
      if (sort.key === "evidence") return a.evdTitle.localeCompare(b.evdTitle) * dir;
      if (sort.key === "source") return (a.srcId ?? "").localeCompare(b.srcId ?? "") * dir;
      const aCell = a.values[sort.key];
      const bCell = b.values[sort.key];
      const rankDiff = sortRank(aCell) - sortRank(bCell);
      if (rankDiff !== 0) return rankDiff * dir;
      return cellText(aCell).localeCompare(cellText(bCell)) * dir;
    });
    return list;
  }, [filtered, sort]);

  function buildRows(): string[][] {
    return sorted.map((row) => [
      row.eps.map((ep) => ep.id).join(", "),
      row.evdTitle,
      ...(showSource ? [row.srcId ?? ""] : []),
      ...columns.map((c) => cellText(row.values[c.id])),
    ]);
  }

  function headerLabels(): string[] {
    return ["EP", "Evidence", ...(showSource ? ["Source"] : []), ...columns.map((c) => c.label)];
  }

  function exportMarkdown() {
    const headers = headerLabels();
    const data = buildRows();
    const lines = [
      `| ${headers.join(" | ")} |`,
      `| ${headers.map(() => "---").join(" | ")} |`,
      ...data.map((r) => `| ${r.map((cell) => cell.replace(/\|/g, "\\|")).join(" | ")} |`),
    ];
    downloadBlob("evidence-quality.md", new Blob([lines.join("\n")], { type: "text/markdown" }));
    setExportMenuOpen(false);
  }

  function exportCsv() {
    const lines = [headerLabels(), ...buildRows()].map((r) => r.map(csvEscape).join(","));
    downloadBlob("evidence-quality.csv", new Blob([lines.join("\n")], { type: "text/csv" }));
    setExportMenuOpen(false);
  }

  async function exportXlsx() {
    const XLSX = await import("xlsx");
    const worksheet = XLSX.utils.aoa_to_sheet([headerLabels(), ...buildRows()]);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Evidence Quality");
    XLSX.writeFile(workbook, "evidence-quality.xlsx");
    setExportMenuOpen(false);
  }

  function SortIndicator({ active, direction }: { active: boolean; direction?: "asc" | "desc" }) {
    if (!active) return <span className="ml-1 inline-block w-2.5 text-muted-ink/30">↕</span>;
    return <span className="ml-1 inline-block w-2.5">{direction === "asc" ? "↑" : "↓"}</span>;
  }

  return (
    <div>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter by evidence, source, or EP…"
          className="w-64 rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink placeholder:text-muted-ink focus:border-forest/50 focus:outline-none"
        />
        <button
          type="button"
          onClick={() => setPickerOpen((o) => !o)}
          className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
        >
          {pickerOpen ? "Hide column picker" : "Add/remove columns"}
        </button>
        <span className="text-xs text-muted-ink">
          {sorted.length} of {rows.length} rows
        </span>

        <div className="relative ml-auto">
          <button
            type="button"
            onClick={() => setExportMenuOpen((o) => !o)}
            className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
          >
            Export ▾
          </button>
          {exportMenuOpen && (
            <div className="absolute right-0 z-10 mt-1 w-32 overflow-hidden rounded-md border border-border bg-card shadow-sm">
              <button
                type="button"
                onClick={exportMarkdown}
                className="block w-full px-3 py-2 text-left text-xs text-ink/80 hover:bg-secondary-surface"
              >
                .md
              </button>
              <button
                type="button"
                onClick={exportCsv}
                className="block w-full px-3 py-2 text-left text-xs text-ink/80 hover:bg-secondary-surface"
              >
                .csv
              </button>
              <button
                type="button"
                onClick={exportXlsx}
                className="block w-full px-3 py-2 text-left text-xs text-ink/80 hover:bg-secondary-surface"
              >
                .xlsx
              </button>
            </div>
          )}
        </div>
      </div>

      {pickerOpen && (
        <div className="mt-3 space-y-3 rounded-md border border-border bg-card p-4">
          <div>
            <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">Identity</p>
            <div className="mt-1.5 flex flex-wrap gap-x-4 gap-y-1.5">
              <label className="flex items-center gap-1.5 text-xs text-ink/80">
                <input
                  type="checkbox"
                  checked={showSource}
                  onChange={() => setShowSource((v) => !v)}
                  className="h-3.5 w-3.5 accent-forest"
                />
                Source
              </label>
            </div>
          </div>
          {QUALITY_COLUMN_GROUPS.map((group) => (
            <div key={group}>
              <p className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">{group}</p>
              <div className="mt-1.5 flex flex-wrap gap-x-4 gap-y-1.5">
                {QUALITY_COLUMNS.filter((c) => c.group === group).map((c) => (
                  <label key={c.id} className="flex items-center gap-1.5 text-xs text-ink/80">
                    <input
                      type="checkbox"
                      checked={visible.has(c.id)}
                      onChange={() => toggleColumn(c.id)}
                      className="h-3.5 w-3.5 accent-forest"
                    />
                    {c.label}
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-4 overflow-x-auto">
        <table className="w-full min-w-[720px] border-collapse text-sm">
          <thead>
            <tr className="border-b border-border text-left text-[0.6875rem] uppercase tracking-wide text-muted-ink">
              <th className="py-2 pr-4">
                <button type="button" onClick={() => toggleSort("ep")} className="inline-flex items-center hover:text-ink">
                  EP
                  <SortIndicator active={sort?.key === "ep"} direction={sort?.direction} />
                </button>
              </th>
              <th className="py-2 pr-4">
                <button
                  type="button"
                  onClick={() => toggleSort("evidence")}
                  className="inline-flex items-center hover:text-ink"
                >
                  Evidence
                  <SortIndicator active={sort?.key === "evidence"} direction={sort?.direction} />
                </button>
              </th>
              {showSource && (
                <th className="py-2 pr-4">
                  <button
                    type="button"
                    onClick={() => toggleSort("source")}
                    className="inline-flex items-center hover:text-ink"
                  >
                    Source
                    <SortIndicator active={sort?.key === "source"} direction={sort?.direction} />
                  </button>
                </th>
              )}
              {columns.map((c) => (
                <th key={c.id} className="py-2 pr-4 text-left">
                  <button
                    type="button"
                    onClick={() => toggleSort(c.id)}
                    className="inline-flex items-center hover:text-ink"
                  >
                    {c.label}
                    <SortIndicator active={sort?.key === c.id} direction={sort?.direction} />
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((row) => (
              <tr key={row.evdId} className="border-b border-border align-top">
                <td className="py-2 pr-4">
                  {row.eps.length > 0 ? (
                    <div className="flex flex-col gap-0.5">
                      {row.eps.map((ep) => (
                        <Link
                          key={ep.id}
                          href={`/nodes/${ep.id}`}
                          title={ep.title}
                          className="text-forest hover:underline"
                        >
                          {ep.id}
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <span className="text-muted-ink">—</span>
                  )}
                </td>
                <td className="max-w-[28ch] py-2 pr-4">
                  <Link href={`/nodes/${row.evdId}`} className="text-forest hover:underline">
                    {row.evdTitle}
                  </Link>
                </td>
                {showSource && (
                  <td className="py-2 pr-4">
                    {row.srcId ? (
                      <Link href={`/nodes/${row.srcId}`} className="text-forest hover:underline">
                        {row.srcId}
                      </Link>
                    ) : (
                      <span className="text-muted-ink">—</span>
                    )}
                  </td>
                )}
                {columns.map((c) => (
                  <td key={c.id} className="py-2 pr-4 text-ink/90">
                    {cellText(row.values[c.id])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

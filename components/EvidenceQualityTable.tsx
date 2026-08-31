"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { QUALITY_COLUMNS, QUALITY_COLUMN_GROUPS, type Cell, type Tone } from "@/lib/qualityColumns";

export type QualityRow = {
  evdId: string;
  evdTitle: string;
  srcId: string | null;
  values: Record<string, Cell>;
};

const TONE_TEXT: Record<Tone, string> = {
  green: "text-emerald-700",
  gold: "text-amber-700",
  red: "text-red-700",
  gray: "text-muted-ink",
};

function cellText(cell: Cell): string {
  return cell ? cell.text : "—";
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

export default function EvidenceQualityTable({ rows }: { rows: QualityRow[] }) {
  const [visible, setVisible] = useState<Set<string>>(
    () => new Set(QUALITY_COLUMNS.filter((c) => c.defaultVisible).map((c) => c.id))
  );
  const [pickerOpen, setPickerOpen] = useState(false);

  const columns = useMemo(() => QUALITY_COLUMNS.filter((c) => visible.has(c.id)), [visible]);

  function toggleColumn(id: string) {
    setVisible((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  const headerLabels = ["Evidence", "Source", ...columns.map((c) => c.label)];

  function buildRows(): string[][] {
    return rows.map((row) => [
      row.evdTitle,
      row.srcId ?? "",
      ...columns.map((c) => cellText(row.values[c.id])),
    ]);
  }

  function exportMarkdown() {
    const data = buildRows();
    const lines = [
      `| ${headerLabels.join(" | ")} |`,
      `| ${headerLabels.map(() => "---").join(" | ")} |`,
      ...data.map((r) => `| ${r.map((cell) => cell.replace(/\|/g, "\\|")).join(" | ")} |`),
    ];
    downloadBlob("evidence-quality.md", new Blob([lines.join("\n")], { type: "text/markdown" }));
  }

  function exportCsv() {
    const data = buildRows();
    const lines = [headerLabels, ...data].map((r) => r.map(csvEscape).join(","));
    downloadBlob("evidence-quality.csv", new Blob([lines.join("\n")], { type: "text/csv" }));
  }

  async function exportXlsx() {
    const XLSX = await import("xlsx");
    const data = buildRows();
    const worksheet = XLSX.utils.aoa_to_sheet([headerLabels, ...data]);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Evidence Quality");
    XLSX.writeFile(workbook, "evidence-quality.xlsx");
  }

  return (
    <div>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={() => setPickerOpen((o) => !o)}
          className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
        >
          {pickerOpen ? "Hide column picker" : "Add/remove columns"}
        </button>
        <div className="ml-auto flex gap-2">
          <button
            type="button"
            onClick={exportMarkdown}
            className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
          >
            Export .md
          </button>
          <button
            type="button"
            onClick={exportCsv}
            className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
          >
            Export .csv
          </button>
          <button
            type="button"
            onClick={exportXlsx}
            className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-ink/80 transition-colors hover:border-forest/50"
          >
            Export .xlsx
          </button>
        </div>
      </div>

      {pickerOpen && (
        <div className="mt-3 space-y-3 rounded-md border border-border bg-card p-4">
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
              <th className="py-2 pr-4">Evidence</th>
              <th className="py-2 pr-4">Source</th>
              {columns.map((c) => (
                <th key={c.id} className="py-2 pr-4 text-left">
                  {c.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.evdId} className="border-b border-border align-top">
                <td className="max-w-[28ch] py-2 pr-4">
                  <Link href={`/nodes/${row.evdId}`} className="text-forest hover:underline">
                    {row.evdTitle}
                  </Link>
                </td>
                <td className="py-2 pr-4">
                  {row.srcId ? (
                    <Link href={`/nodes/${row.srcId}`} className="text-forest hover:underline">
                      {row.srcId}
                    </Link>
                  ) : (
                    <span className="text-muted-ink">—</span>
                  )}
                </td>
                {columns.map((c) => {
                  const cell = row.values[c.id];
                  return (
                    <td key={c.id} className={`py-2 pr-4 ${cell ? TONE_TEXT[cell.tone] : "text-muted-ink"}`}>
                      {cellText(cell)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

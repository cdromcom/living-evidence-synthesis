import type { ReactNode } from "react";

/** Splits a flat list of chips into rows of at most `size` (default 4). */
export function chunkChips<T>(items: T[], size = 4): T[][] {
  const rows: T[][] = [];
  for (let i = 0; i < items.length; i += size) rows.push(items.slice(i, i + size));
  return rows;
}

/**
 * Lays out a list of chips in fixed rows of at most 4, regardless of
 * viewport width — a wide screen shouldn't cram 6+ chips onto one line just
 * because there's room.
 */
export default function ChipRows({ chips }: { chips: ReactNode[] }) {
  if (chips.length === 0) return null;
  return (
    <div className="mt-1.5 space-y-1.5">
      {chunkChips(chips).map((row, i) => (
        <div key={i} className="flex flex-wrap items-center gap-1.5">
          {row}
        </div>
      ))}
    </div>
  );
}

// Names of the Quality signal rows come from one file in the vault,
// vault/pipeline/templates/quality-signal-labels.json, copied to
// lib/quality-labels.generated.json by scripts/build-graph.mjs. Renaming a row
// means editing that file (see the Skill), not this code. The labels written in
// the code are only a fallback for a row the file does not list.
import registry from "./quality-labels.generated.json";

type Row = { id: string; label: string; aliases: string[] };
const ROWS = (registry as { rows: Row[] }).rows;
const BY_ID = new Map(ROWS.map((r) => [r.id, r]));

/** The current name of a row, falling back to the name the caller already has. */
export function labelFor(id: string, fallback: string): string {
  return BY_ID.get(id)?.label ?? fallback;
}

/** Lower-cased current names and old names of every row, mapped to the row id. */
export const ROW_LABEL_TO_ID: Record<string, string> = Object.fromEntries(
  ROWS.flatMap((r) => [r.label, ...r.aliases].map((n) => [n.toLowerCase(), r.id] as const)),
);

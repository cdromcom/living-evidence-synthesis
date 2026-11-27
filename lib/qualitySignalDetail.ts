// Detail behind each Quality signals row, read from
// lib/quality-signal-detail.generated.json (written by scripts/build-graph.mjs
// from vault/pipeline/provenance/provenance-quality-signals.json). Server-side
// only: the table receives just the sections for the rows of the paper on screen.
import raw from "./quality-signal-detail.generated.json";

export type ToolCheck = {
  id: string;
  label: string;
  tool: string;
  status: string;
  result: string;
  detail: string;
  url: string;
  checked_utc: string;
};

export type Rating = {
  rater: string;
  rating: string;
  quote: string;
  locator: string;
  pdf_page: number | null;
  printed_page: string | null;
  /** "<citekey>/<file>.jpg", served from /quality-signals/. */
  screenshot: string | null;
};

export type VerifierCheck = { verifier: string; score: number | null; note: string };

export type SignalSection = {
  id: string;
  label: string;
  final: string;
  agreement: string;
  summary: string;
  ratings: Rating[];
  checks: VerifierCheck[];
  toolChecks: ToolCheck[];
  /** TRIPOD-LLM items only: the rating the earlier table on this site gave. */
  vaultValue?: string;
  matchesVault?: boolean;
};

export type TripodSummary = {
  fully: number;
  partial: number;
  "not-reported": number;
  "not-applicable": number;
  applicable: number;
  pct: number;
  level: string;
};

export type RowDetail = {
  sections: SignalSection[];
  /** Paper-level checks not already shown in a section. */
  paperChecks: ToolCheck[];
  /** Set on the TRIPOD-LLM row: the counts and every checklist item. */
  tripod?: { summary: TripodSummary; items: SignalSection[] };
};

type RawSignal = Omit<SignalSection, "toolChecks" | "vaultValue" | "matchesVault"> & {
  tool_checks: string[];
  vault_value?: string;
  matches_vault?: boolean;
};

type PaperData = {
  provenance: ToolCheck[];
  signals: Record<string, RawSignal>;
  tripod?: TripodSummary;
};

const PAPERS = (raw as unknown as { papers: Record<string, PaperData> }).papers;

/** Row id used by the TRIPOD-LLM reporting row; its detail is every tripod-* signal. */
export const TRIPOD_ROW = "tripod";

/** Checklist order: "tripod-5c" sorts after "tripod-5b" and "tripod-14a" after "tripod-9b". */
function itemOrder(id: string): string {
  const m = /^tripod-(\d+)([a-z]*)$/.exec(id);
  return m ? `${m[1].padStart(3, "0")}${m[2]}` : id;
}

/** The detail for one table row, or undefined when none of its signals has data. */
export function getRowDetail(citekey: string | null, signalIds: string[] | undefined): RowDetail | undefined {
  if (!citekey || !signalIds?.length) return undefined;
  const paper = PAPERS[citekey];
  if (!paper) return undefined;
  const byId = new Map(paper.provenance.map((t) => [t.id, t]));
  const shown = new Set<string>();
  const toSection = (s: RawSignal): SignalSection => {
    const { tool_checks, vault_value, matches_vault, ...rest } = s;
    const toolChecks = tool_checks.flatMap((t) => byId.get(t) ?? []);
    toolChecks.forEach((t) => shown.add(t.id));
    return { ...rest, toolChecks, vaultValue: vault_value, matchesVault: matches_vault };
  };

  if (signalIds.includes(TRIPOD_ROW)) {
    const items = Object.values(paper.signals)
      .filter((s) => s.id.startsWith("tripod-"))
      .sort((a, b) => itemOrder(a.id).localeCompare(itemOrder(b.id)))
      .map(toSection);
    if (items.length === 0) return undefined;
    const count = (r: string) => items.filter((i) => i.final === r).length;
    const fully = count("fully");
    const partial = count("partial");
    const applicable = items.length - count("not-applicable");
    const pct = applicable ? Math.round(((fully + partial / 2) / applicable) * 100) : 0;
    const summary: TripodSummary = paper.tripod ?? {
      fully,
      partial,
      "not-reported": count("not-reported"),
      "not-applicable": count("not-applicable"),
      applicable,
      pct,
      level: pct >= 75 ? "high" : pct >= 50 ? "moderate" : "low",
    };
    return { sections: [], paperChecks: [], tripod: { summary, items } };
  }

  const sections: SignalSection[] = [];
  for (const id of signalIds) {
    const s = paper.signals[id];
    if (s) sections.push(toSection(s));
  }
  if (sections.length === 0) return undefined;
  return { sections, paperChecks: paper.provenance.filter((t) => !shown.has(t.id)) };
}

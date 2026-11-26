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
};

export type RowDetail = {
  sections: SignalSection[];
  /** Paper-level checks not already shown in a section. */
  paperChecks: ToolCheck[];
};

type PaperData = {
  provenance: ToolCheck[];
  signals: Record<string, Omit<SignalSection, "toolChecks"> & { tool_checks: string[] }>;
};

const PAPERS = (raw as unknown as { papers: Record<string, PaperData> }).papers;

/** The detail for one table row, or undefined when none of its signals has data. */
export function getRowDetail(citekey: string | null, signalIds: string[] | undefined): RowDetail | undefined {
  if (!citekey || !signalIds?.length) return undefined;
  const paper = PAPERS[citekey];
  if (!paper) return undefined;
  const byId = new Map(paper.provenance.map((t) => [t.id, t]));
  const shown = new Set<string>();
  const sections: SignalSection[] = [];
  for (const id of signalIds) {
    const s = paper.signals[id];
    if (!s) continue;
    const { tool_checks, ...rest } = s;
    const toolChecks = tool_checks.flatMap((t) => byId.get(t) ?? []);
    toolChecks.forEach((t) => shown.add(t.id));
    sections.push({ ...rest, toolChecks });
  }
  if (sections.length === 0) return undefined;
  return { sections, paperChecks: paper.provenance.filter((t) => !shown.has(t.id)) };
}

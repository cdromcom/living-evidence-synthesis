// Review categories used in the accuracy GSheet: four judgment dimensions, each
// with its own verdict labels, plus the seven error types from the 2026-11-17
// PDF audit. Shared by the GitHub-linked panel (prefilled issue) and the
// Supabase review widget.
//
// Supabase storage: the category key goes in `node_reviews.dimension`
// (1-40 characters, no schema change) and the verdict goes in the existing
// `verdict` column, using the existing vocabulary (see VERDICT_VOCAB in
// lib/ui.ts). Within each dimension the labels map one-to-one onto distinct
// vocabulary keys, so the label can always be recovered from (dimension, verdict).
import type { Verdict } from "./supabase";

export type CategoryVerdict = { label: string; verdict: Verdict; help?: string };

export type JudgmentDimension = {
  key: string; // stored in node_reviews.dimension
  label: string;
  help: string;
  verdicts: CategoryVerdict[];
};

export const OVERALL_DIMENSION = "overall";

export const JUDGMENT_DIMENSIONS: JudgmentDimension[] = [
  {
    key: "selection-relevancy",
    label: "Selection relevancy",
    help: "Was this passage the right thing to extract for the node?",
    verdicts: [
      { label: "Relevant", verdict: "correct", help: "This passage is the right thing to extract for the node." },
      { label: "Irrelevant", verdict: "wrong", help: "This passage does not belong to the node." },
      { label: "NA", verdict: "na" },
    ],
  },
  {
    key: "fidelity",
    label: "Fidelity",
    help: "Does the node's wording stay faithful to what the paper says?",
    verdicts: [
      { label: "Met", verdict: "correct", help: "The wording is faithful to the paper." },
      { label: "Partially Met", verdict: "edit", help: "Mostly faithful, but scope, polarity or a number is off." },
      { label: "Unmet", verdict: "wrong", help: "The wording misstates the paper." },
      { label: "NA", verdict: "na" },
    ],
  },
  {
    key: "grounding-quote",
    label: "Grounding: Quote",
    help: "Is the quote screenshot a clean capture of the supporting passage?",
    verdicts: [
      { label: "Correct", verdict: "correct", help: "The whole quote is visible in a clean capture." },
      { label: "Partially Correct", verdict: "edit", help: "The capture is cut off or has extraneous content." },
      { label: "Incorrect", verdict: "wrong", help: "The capture shows a different passage." },
      { label: "Missing", verdict: "missing", help: "No screenshot." },
      { label: "NA", verdict: "na" },
    ],
  },
  {
    key: "grounding-figure",
    label: "Grounding: Table/Figure",
    help: "Is the table or figure screenshot the right one, shown cleanly?",
    verdicts: [
      { label: "Correct", verdict: "correct", help: "The whole table or figure with its caption only." },
      { label: "Partially Correct", verdict: "edit", help: "Trimmed, or extra content included." },
      { label: "Incorrect", verdict: "wrong", help: "The wrong table or figure." },
      { label: "Missing", verdict: "missing", help: "None shown." },
      { label: "NA", verdict: "na" },
    ],
  },
];

// Error types from the 2026-11-17 PDF audit. A review under one of these
// categories means "this error is present" (stored with verdict "wrong").
export const ERROR_TYPES = [
  { slug: "wrong-number", label: "Wrong number" },
  { slug: "claim-not-in-paper", label: "Claim not in the paper" },
  { slug: "paper-contradicts-itself", label: "Paper contradicts itself" },
  { slug: "wrong-page-reference", label: "Wrong page reference" },
  { slug: "credited-to-wrong-model", label: "Credited to the wrong model, rater or condition" },
  { slug: "missing-comparator", label: "Missing comparator" },
  { slug: "row-column-shift", label: "Row or column shift" },
] as const;

export const ERROR_DIMENSION_PREFIX = "error-";

export type Category =
  | { kind: "overall"; key: string; label: string }
  | { kind: "judgment"; key: string; label: string; dimension: JudgmentDimension }
  | { kind: "error"; key: string; label: string };

export const CATEGORIES: Category[] = [
  { kind: "overall", key: OVERALL_DIMENSION, label: "Overall (accuracy verdict)" },
  ...JUDGMENT_DIMENSIONS.map(
    (d): Category => ({ kind: "judgment", key: d.key, label: d.label, dimension: d }),
  ),
  ...ERROR_TYPES.map(
    (e): Category => ({ kind: "error", key: ERROR_DIMENSION_PREFIX + e.slug, label: e.label }),
  ),
];

export function getCategory(key: string): Category | undefined {
  return CATEGORIES.find((c) => c.key === key);
}

/** The label a reviewer picked, recovered from the stored (dimension, verdict). */
export function verdictLabelFor(dimension: string, verdict: Verdict): string | undefined {
  const cat = getCategory(dimension);
  if (cat?.kind === "judgment") return cat.dimension.verdicts.find((v) => v.verdict === verdict)?.label;
  if (cat?.kind === "error") return "Present";
  return undefined;
}

export const PAGE_PATTERN = /^[A-Za-z]{0,3}\d{1,5}([–-]\d{1,5})?$/;

export type IssueDraftInput = {
  nodeId: string;
  nodeTitle: string;
  categoryKey: string;
  verdictLabel: string;
  quote: string;
  page: string;
  note: string;
  nodeUrl: string;
};

/** Title and body for a prefilled GitHub issue. */
export function buildIssueDraft(i: IssueDraftInput): { title: string; body: string } {
  const cat = getCategory(i.categoryKey);
  const catLabel = cat?.label ?? i.categoryKey;
  const outcome = cat?.kind === "error" ? "error found" : i.verdictLabel;
  const title = `[${i.nodeId}] ${catLabel}${outcome ? `: ${outcome}` : ""}`;
  const lines = [
    `Node: ${i.nodeId} (${i.nodeTitle})`,
    `Page: ${i.nodeUrl}`,
    `Category: ${catLabel}`,
    cat?.kind === "error" ? `Error type: ${catLabel}` : `Verdict: ${i.verdictLabel || "(not chosen)"}`,
    `Quote: ${i.quote.trim() || "(none)"}`,
    `Printed page: ${i.page.trim() || "(none)"}`,
    "",
    "Note:",
    i.note.trim() || "(none)",
  ];
  return { title, body: lines.join("\n") };
}

export type MultiIssueEntry = { categoryKey: string; verdictLabel: string; proposed: string; note: string };

/** Title and body for one prefilled GitHub issue covering every category the reviewer ticked. */
export function buildMultiIssueDraft(i: {
  nodeId: string;
  nodeTitle: string;
  nodeUrl: string;
  entries: MultiIssueEntry[];
}): { title: string; body: string } {
  const label = (e: MultiIssueEntry) => {
    const cat = getCategory(e.categoryKey);
    const name = cat?.label ?? e.categoryKey;
    return cat?.kind === "error" ? `${name}: error found` : `${name}: ${e.verdictLabel || "(not chosen)"}`;
  };
  const title = `[${i.nodeId}] ${i.entries.map(label).join("; ")}`.slice(0, 200);
  const lines = [`Node: ${i.nodeId} (${i.nodeTitle})`, `Page: ${i.nodeUrl}`, ""];
  for (const e of i.entries) {
    lines.push(`- ${label(e)}`);
    if (e.proposed.trim()) lines.push(`  Proposed correction: ${e.proposed.trim().slice(0, 1500)}`);
    if (e.note.trim()) lines.push(`  Note: ${e.note.trim().slice(0, 1500)}`);
  }
  return { title, body: lines.join("\n") };
}

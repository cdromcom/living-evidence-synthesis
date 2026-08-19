import type { NodeType, FiveC } from "./data";

export const NODE_TYPE_COLOR_VAR: Record<NodeType, string> = {
  QUE: "var(--color-node-question)",
  CLM: "var(--color-node-claim)",
  EVD: "var(--color-node-evidence)",
  CVT: "var(--color-node-caveat)",
  SRC: "var(--color-node-source)",
  EP: "var(--color-node-ep)",
};

export const NODE_TYPE_BG_CLASS: Record<NodeType, string> = {
  QUE: "bg-node-question",
  CLM: "bg-node-claim",
  EVD: "bg-node-evidence",
  CVT: "bg-node-caveat",
  SRC: "bg-node-source",
  EP: "bg-node-ep",
};

export const NODE_TYPE_TEXT_CLASS: Record<NodeType, string> = {
  QUE: "text-node-question",
  CLM: "text-node-claim",
  EVD: "text-node-evidence",
  CVT: "text-node-caveat",
  SRC: "text-node-source",
  EP: "text-node-ep",
};

export const NODE_TYPE_BORDER_CLASS: Record<NodeType, string> = {
  QUE: "border-node-question",
  CLM: "border-node-claim",
  EVD: "border-node-evidence",
  CVT: "border-node-caveat",
  SRC: "border-node-source",
  EP: "border-node-ep",
};

/**
 * Selecting a node in the global search palette while already on /graph
 * should preview it in place (same as clicking it in the graph) rather
 * than navigating away and losing filter/zoom/focus state.
 */
export const GRAPH_SELECT_NODE_EVENT = "graph:select-node";

export const FIVE_C_COLOR_VAR: Record<FiveC, string> = {
  credibility: "var(--color-5c-credibility)",
  clarity: "var(--color-5c-clarity)",
  creativity: "var(--color-5c-creativity)",
  care: "var(--color-5c-care)",
  connectivity: "var(--color-5c-connectivity)",
};

export const FIVE_C_BG_CLASS: Record<FiveC, string> = {
  credibility: "bg-5c-credibility",
  clarity: "bg-5c-clarity",
  creativity: "bg-5c-creativity",
  care: "bg-5c-care",
  connectivity: "bg-5c-connectivity",
};

export const FIVE_C_TEXT_CLASS: Record<FiveC, string> = {
  credibility: "text-5c-credibility",
  clarity: "text-5c-clarity",
  creativity: "text-5c-creativity",
  care: "text-5c-care",
  connectivity: "text-5c-connectivity",
};

export const FIVE_C_BORDER_CLASS: Record<FiveC, string> = {
  credibility: "border-5c-credibility",
  clarity: "border-5c-clarity",
  creativity: "border-5c-creativity",
  care: "border-5c-care",
  connectivity: "border-5c-connectivity",
};

/** Curation status -> a stable visual family (draft vs. reviewed vs. other). */
export function curationStatusTone(status: string): "draft" | "reviewed" | "other" {
  if (status === "Initial AI draft") return "draft";
  if (status === "Reviewed") return "reviewed";
  return "other";
}

export const VERDICT_VOCAB = [
  {
    symbol: "✓",
    key: "correct",
    label: "Correct",
    color: "var(--color-verdict-correct)",
    description: "The AI-proposed content is accurate as stated; a human reviewer has confirmed it.",
  },
  {
    symbol: "✎",
    key: "edit",
    label: "Edit",
    color: "var(--color-verdict-edit)",
    description: "Substantially right, but a human reviewer revised wording, scope, or polarity.",
  },
  {
    symbol: "✗",
    key: "wrong",
    label: "Wrong",
    color: "var(--color-verdict-wrong)",
    description: "The AI-proposed content is incorrect and was rejected on review.",
  },
  {
    symbol: "⟳",
    key: "missing",
    label: "Missing",
    color: "var(--color-verdict-missing)",
    description: "The AI missed something a human reviewer judged should be present.",
  },
  {
    symbol: "—",
    key: "na",
    label: "N/A",
    color: "var(--color-muted-ink)",
    description: "Not applicable / not yet reviewed.",
  },
] as const;

import type { NodeType } from "@/lib/data";
import { NODE_TYPE_LABELS } from "@/lib/data";
import { NODE_TYPE_BG_CLASS } from "@/lib/ui";

export default function NodeTypeBadge({ type }: { type: NodeType }) {
  return (
    <span
      className={`inline-flex shrink-0 items-center rounded-full px-2 py-0.5 text-[0.6875rem] font-semibold uppercase tracking-wide text-white ${NODE_TYPE_BG_CLASS[type]}`}
    >
      {NODE_TYPE_LABELS[type]}
    </span>
  );
}

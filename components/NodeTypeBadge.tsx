import type { NodeType } from "@/lib/data";
import { NODE_TYPE_BG_CLASS } from "@/lib/ui";

export default function NodeTypeBadge({
  type,
  typeLabel,
}: {
  type: NodeType;
  typeLabel: string;
}) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-[0.6875rem] font-semibold uppercase tracking-wide text-white ${NODE_TYPE_BG_CLASS[type]}`}
    >
      <span className="mono opacity-90">{type}</span>
      <span className="hidden sm:inline">{typeLabel}</span>
    </span>
  );
}

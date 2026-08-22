import type { NodeType } from "@/lib/data";
import { NODE_TYPE_LABELS } from "@/lib/data";
import { NODE_TYPE_BG_CLASS } from "@/lib/ui";

/** Type pill (e.g. "SOURCE"). Pass `id` to merge the node's ID into the same chip. */
export default function NodeTypeBadge({ type, id }: { type: NodeType; id?: string }) {
  return (
    <span
      className={`inline-flex shrink-0 items-stretch overflow-hidden rounded-full text-[0.6875rem] font-semibold text-white ${NODE_TYPE_BG_CLASS[type]}`}
    >
      <span className="px-2 py-0.5 uppercase tracking-wide">{NODE_TYPE_LABELS[type]}</span>
      {id && (
        <span className="mono border-l border-white/25 bg-black/10 px-2 py-0.5 font-medium normal-case tracking-normal text-white/90">
          {id}
        </span>
      )}
    </span>
  );
}

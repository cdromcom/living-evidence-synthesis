"use client";

import { useState } from "react";

/**
 * Collapses the whole Transparency/Openness/Rigor/Integrity chip block
 * behind one toggle, so a node with data in every group doesn't push the
 * article content four labeled blocks down by default. The summary line
 * names which categories have data so there's still something to go on
 * before clicking.
 */
export default function CollapsibleSignalBlock({
  summary,
  children,
}: {
  summary: string;
  children: React.ReactNode;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mt-3 max-w-[70%]">
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
      >
        {expanded ? "Hide Quality Signals" : `Show Quality Signals: ${summary}`}
      </button>
      {expanded && <div className="mt-2 space-y-3">{children}</div>}
    </div>
  );
}

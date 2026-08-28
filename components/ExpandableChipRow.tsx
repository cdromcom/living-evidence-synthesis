"use client";

import { useState } from "react";

/**
 * Wraps a wrapped row of chips (badges) so only the first line shows by
 * default, with an Expand/Collapse toggle to reveal the rest. Used for the
 * Rigor group, which can carry a long tail of sub-check chips (data
 * leakage, baseline adequacy, train/dev/test hygiene, ...) beyond the four
 * validity-domain chips most nodes show.
 */
export default function ExpandableChipRow({ children }: { children: React.ReactNode }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div>
      <div
        className={`flex flex-wrap items-center gap-1.5 ${
          expanded ? "" : "max-h-8 overflow-hidden"
        }`}
      >
        {children}
      </div>
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        className="mt-1 text-[0.6875rem] font-medium text-forest hover:underline"
      >
        {expanded ? "collapse" : "expand"}
      </button>
    </div>
  );
}

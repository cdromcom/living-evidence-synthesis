"use client";

import { useState } from "react";

function ChevronGlyph({ expanded }: { expanded: boolean }) {
  return (
    <svg
      width="10"
      height="10"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2.4}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
      className={`shrink-0 transition-transform ${expanded ? "rotate-180" : ""}`}
    >
      <path d="M5 9l7 7 7-7" />
    </svg>
  );
}

/**
 * Collapses the whole Transparency/Openness/Rigor/Integrity chip block
 * behind one toggle, so a node with data in every group doesn't push the
 * article content four labeled blocks down by default. The button text
 * itself stays static ("Show"/"Hide Quality Signals") — `summary` (which
 * categories have data) is exposed only as an aria-label, so sighted users
 * get a short, stable label and screen-reader users still get the
 * category rundown before deciding whether to activate it.
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
    <div className="mt-3 max-w-[86%]">
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        aria-label={expanded ? "Hide quality signals" : `Show quality signals: ${summary}`}
        className="inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2 py-1 text-[0.6875rem] text-ink/80 transition-colors hover:border-forest/50"
      >
        <ChevronGlyph expanded={expanded} />
        {expanded ? "Hide Quality Signals" : "Show Quality Signals"}
      </button>
      {expanded && <div className="mt-2 space-y-3">{children}</div>}
    </div>
  );
}

"use client";

import { useState } from "react";
import { formatApaCitation } from "@/lib/apa";
import type { GraphNode } from "@/lib/data";

function CopyIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <rect x="8" y="8" width="12" height="12" rx="1.5" />
      <path d="M5.5 15.5H5a1.5 1.5 0 0 1-1.5-1.5V5a1.5 1.5 0 0 1 1.5-1.5h9A1.5 1.5 0 0 1 15.5 5v.5" />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.4} strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M4.5 12.5l5 5 10-11" />
    </svg>
  );
}

/** A full APA 7th-edition citation, shown at the top of each source page in a bounded, copyable box. */
export default function SourceCitation({ node }: { node: GraphNode }) {
  const citation = formatApaCitation(node);
  const [copied, setCopied] = useState(false);

  if (!citation.hasData) return null;

  const plainText = `${citation.authors} (${citation.year}). ${citation.title}.${
    citation.container
      ? ` ${citation.container}${citation.volumeIssue ? `, ${citation.volumeIssue}` : ""}${citation.pages ? `, ${citation.pages}` : ""}.`
      : ""
  }${citation.url ? ` ${citation.url}` : ""}`;

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(plainText);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // clipboard blocked (e.g. insecure context) — button just won't confirm
    }
  }

  return (
    <div className="group relative mb-4 mt-2 rounded-md bg-secondary-surface py-2.5 pl-3 pr-9">
      <p className="text-sm leading-relaxed text-ink/90">
        {citation.authors} ({citation.year}). {citation.title}.{" "}
        {citation.container && (
          <>
            <em>{citation.container}</em>
            {citation.volumeIssue && <em>, {citation.volumeIssue}</em>}
            {citation.pages && <>, {citation.pages}</>}.{" "}
          </>
        )}
        {citation.url && (
          <a href={citation.url} target="_blank" rel="noopener noreferrer" className="text-forest hover:underline">
            {citation.url}
          </a>
        )}
      </p>
      <button
        type="button"
        onClick={handleCopy}
        title={copied ? "Copied" : "Copy citation"}
        className="absolute right-2 top-2 rounded-md p-1.5 text-muted-ink transition-colors hover:bg-card hover:text-ink"
      >
        {copied ? <CheckIcon /> : <CopyIcon />}
      </button>
    </div>
  );
}

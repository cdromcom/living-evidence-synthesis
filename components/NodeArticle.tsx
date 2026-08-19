"use client";

import { useEffect, useRef } from "react";

/**
 * Renders a node's pre-built HTML body and boots mermaid for any
 * `.mermaid` blocks inside it (see lib/markdown.ts's activateMermaid) —
 * mermaid only runs client-side, so this can't happen in the server
 * component that renders the rest of the page.
 */
export default function NodeArticle({ html }: { html: string }) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const blocks = el.querySelectorAll<HTMLDivElement>(".mermaid");
    if (blocks.length === 0) return;

    let cancelled = false;
    import("mermaid").then(({ default: mermaid }) => {
      if (cancelled) return;
      mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "strict" });
      mermaid.run({ nodes: Array.from(blocks) });
    });
    return () => {
      cancelled = true;
    };
  }, [html]);

  return (
    <article
      ref={ref}
      className="prose-node min-w-0 flex-1"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

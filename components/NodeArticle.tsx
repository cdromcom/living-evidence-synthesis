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
    const blocks = Array.from(el.querySelectorAll<HTMLDivElement>(".mermaid"));
    if (blocks.length === 0) return;

    // Snapshot each diagram's source text synchronously, right now — before
    // the async `import("mermaid")` gap. Some browser extensions (glossary/
    // dictionary term highlighters, translators) rewrite page text
    // asynchronously and can inject markup (e.g. <a class="glossary-...">)
    // into this div in that window. mermaid.run() re-scans the live DOM node
    // when it finally runs, so it can end up parsing corrupted text through
    // no fault of the diagram source itself. Capturing the string now and
    // rendering from that string instead avoids the race entirely.
    const sources = blocks.map((b) => b.textContent || "");

    let cancelled = false;
    import("mermaid").then(async ({ default: mermaid }) => {
      if (cancelled) return;
      mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "strict" });
      for (let i = 0; i < blocks.length; i++) {
        try {
          const { svg } = await mermaid.render(`mermaid-svg-${i}-${Date.now()}`, sources[i]);
          if (!cancelled) blocks[i].innerHTML = svg;
        } catch (err) {
          console.error("Mermaid diagram failed to render:", err);
        }
      }
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

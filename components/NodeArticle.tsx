"use client";

import { useEffect, useRef } from "react";

const EXPAND_ICON =
  '<path d="M8 3H5a2 2 0 0 0-2 2v3M16 3h3a2 2 0 0 1 2 2v3M8 21H5a2 2 0 0 1-2-2v-3M16 21h3a2 2 0 0 0 2-2v-3"/>';
const COLLAPSE_ICON =
  '<path d="M3 8V5a2 2 0 0 1 2-2h3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M21 16v3a2 2 0 0 1-2 2h-3"/>';
const FIT_ICON =
  '<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/><path d="M9 15l-3 3m0 0v-3m0 3h3M15 9l3-3m0 0h-3m3 0v3"/>';

function iconSvg(path: string): string {
  return (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    path +
    "</svg>"
  );
}

/**
 * Wraps a rendered `.mermaid` block in a figure with a small toolbar: a
 * "fit to view" toggle (the diagram's native size is often wider than the
 * article column, so the default is a horizontal scroll — this scales it
 * down to see the whole shape at once) and a full screen toggle (for reading
 * the labels back at full size after fitting). The plotting area itself is
 * also a full screen toggle, so a reader doesn't have to aim for the button.
 * A diagram's legend, if it has one, lives in this same toolbar row rather
 * than under the diagram — see the append order below.
 */
function wrapWithToolbar(block: HTMLDivElement) {
  if (block.closest(".mermaid-figure")) return;
  const figure = document.createElement("div");
  figure.className = "mermaid-figure";

  // A diagram's legend (see lib/markdown.ts's rendering of a `.mermaid-legend`
  // block, written straight into the vault markdown right after the fenced
  // diagram) sits as the next sibling in the DOM. The Fullscreen API only
  // shows the element actually promoted to fullscreen and its descendants —
  // a sibling left outside `figure` would simply vanish in fullscreen — so it
  // has to move inside here to stay visible there.
  const legend =
    block.nextElementSibling?.classList.contains("mermaid-legend")
      ? (block.nextElementSibling as HTMLElement)
      : null;

  const toolbar = document.createElement("div");
  toolbar.className = "mermaid-toolbar";

  const buttons = document.createElement("div");
  buttons.className = "mermaid-toolbar-buttons";

  const fitBtn = document.createElement("button");
  fitBtn.type = "button";
  fitBtn.className = "mermaid-btn";
  fitBtn.innerHTML = `${iconSvg(FIT_ICON)}<span>Fit to view</span>`;
  fitBtn.setAttribute("aria-pressed", "false");
  const setFit = (fitted: boolean) => {
    figure.classList.toggle("is-fit", fitted);
    fitBtn.setAttribute("aria-pressed", String(fitted));
    fitBtn.querySelector("span")!.textContent = fitted ? "Actual size" : "Fit to view";
  };
  fitBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    setFit(!figure.classList.contains("is-fit"));
  });

  const fullscreenBtn = document.createElement("button");
  fullscreenBtn.type = "button";
  fullscreenBtn.className = "mermaid-btn";
  fullscreenBtn.innerHTML = `${iconSvg(EXPAND_ICON)}<span>Full screen</span>`;
  const toggleFullscreen = () => {
    if (document.fullscreenElement === figure) {
      document.exitFullscreen();
    } else {
      figure.requestFullscreen?.();
    }
  };
  fullscreenBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleFullscreen();
  });
  // The plotting area itself also opens/closes full screen on click — a
  // diagram big enough to want full screen for is reason enough to make the
  // whole thing the click target, not just the small toolbar button.
  block.addEventListener("click", toggleFullscreen);
  figure.addEventListener("fullscreenchange", () => {
    const active = document.fullscreenElement === figure;
    fullscreenBtn.innerHTML = `${iconSvg(active ? COLLAPSE_ICON : EXPAND_ICON)}<span>${
      active ? "Exit full screen" : "Full screen"
    }</span>`;
    figure.classList.toggle("is-fullscreen", active);
    // Entering full screen defaults to Fit to view — the diagram's native
    // size assumes a narrow article column, so at full-viewport scale that
    // reads as one small corner of a mostly-empty screen until scaled up.
    if (active && !figure.classList.contains("is-fit")) setFit(true);
  });

  buttons.append(fitBtn, fullscreenBtn);
  // Legend on the left, buttons on the right, one row — see globals.css's
  // .mermaid-toolbar (space-between, no wrap) for the layout this assumes.
  if (legend) toolbar.append(legend, buttons);
  else toolbar.append(buttons);
  block.replaceWith(figure);
  figure.append(toolbar, block);
}

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
          if (!cancelled) {
            blocks[i].innerHTML = svg;
            // mermaid's "neutral" theme sets an inline background-color on
            // its own root <svg> (light gray, meant for a white page) — strip
            // it so the diagram shows the site's own themed background
            // instead of a light rectangle sitting on top of it.
            blocks[i].querySelector("svg")?.style.removeProperty("background-color");
            wrapWithToolbar(blocks[i]);
          }
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

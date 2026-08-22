"use client";

import { useEffect, useRef } from "react";

declare global {
  interface Window {
    _altmetric_embed_init?: (el: HTMLElement) => void;
  }
}

const EMBED_SCRIPT_SRC = "https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js";

/**
 * Altmetric's free embeddable badge (badge-docs.altmetric.com) — shows the
 * "attention score" donut (news/blog/social/policy mentions) for a DOI, no
 * API key needed. Distinct from Altmetric's Details Page API, which now
 * requires a paid/registered key as of Nov 2025 — this widget is a
 * separate, still-free mechanism where their own script fetches the data
 * client-side. Altmetric does run a real AI-driven sentiment analysis
 * (-3 to +3 polarity on news/social mentions), but it's gated behind the
 * paid Altmetric Explorer product, not exposed via this free badge — so
 * this widget can only surface attention/engagement volume, not polarity.
 */
export default function AltmetricBadge({ doi }: { doi: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const existing = document.querySelector<HTMLScriptElement>(`script[src="${EMBED_SCRIPT_SRC}"]`);
    function init() {
      if (ref.current && window._altmetric_embed_init) window._altmetric_embed_init(ref.current);
    }
    if (existing) {
      init();
    } else {
      const script = document.createElement("script");
      script.src = EMBED_SCRIPT_SRC;
      script.async = true;
      script.onload = init;
      document.body.appendChild(script);
    }
  }, [doi]);

  return (
    <div
      ref={ref}
      className="altmetric-embed"
      data-badge-type="donut"
      data-badge-popover="right"
      data-badge-details="right"
      data-doi={doi}
      title="Altmetric attention score — volume of news, blog, social, and policy mentions. Sentiment analysis of these mentions exists but is an Altmetric Explorer (paid) feature, not available here."
    />
  );
}

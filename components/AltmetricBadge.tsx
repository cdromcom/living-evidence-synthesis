"use client";

import { useEffect, useRef, useState } from "react";

declare global {
  interface Window {
    _altmetric_embed_init?: (el: HTMLElement) => void;
  }
}

const EMBED_SCRIPT_SRC = "https://d1bxh8uas1mnw7.cloudfront.net/assets/embed.js";
// Probes the same image CDN Altmetric's own embed script draws the donut
// from — badges.altmetric.com has been intermittently returning 503s
// (service-wide, unrelated to any specific DOI), which leaves the embed
// div silently empty with no visual indication. This probe detects that
// and swaps in a text fallback instead of a blank box.
const BADGE_CDN_PROBE_SRC = "https://badges.altmetric.com/?size=1&score=1&types=t&style=donut";

/**
 * Altmetric's free embeddable badge (badge-docs.altmetric.com) — shows the
 * "attention score" donut (news/blog/social/policy mentions) for a DOI, no
 * API key needed. Distinct from Altmetric's Details Page API, which now
 * requires a paid/registered key as of Nov 2025 — this widget is a
 * separate, still-free mechanism where their own script fetches the data
 * client-side. Altmetric does run a real AI-driven sentiment analysis
 * (-3 to +3 polarity on news/social mentions), but it's gated behind the
 * paid Altmetric Explorer product, not exposed via this free badge, so
 * this widget can only surface attention/engagement volume, not polarity.
 */
export default function AltmetricBadge({ doi }: { doi: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [cdnDown, setCdnDown] = useState(false);

  useEffect(() => {
    // No need to reset cdnDown for a new doi here — the caller keys this
    // component by doi (see SourceCredibility.tsx), so a doi change remounts
    // it from scratch rather than reusing this instance's stale state.
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

    const probe = new Image();
    probe.onload = () => setCdnDown(false);
    probe.onerror = () => setCdnDown(true);
    probe.src = BADGE_CDN_PROBE_SRC;
  }, [doi]);

  if (cdnDown) {
    return (
      <span
        className="text-xs text-muted-ink"
        title="Altmetric's badge-image service is unavailable right now (their CDN is returning errors, not something specific to this paper); try again later."
      >
        Unavailable
      </span>
    );
  }

  return (
    <div
      ref={ref}
      className="altmetric-embed"
      data-badge-type="donut"
      data-badge-popover="right"
      data-badge-details="right"
      data-doi={doi}
      title="Altmetric attention score: volume of news, blog, social, and policy mentions. Sentiment analysis of these mentions exists but is an Altmetric Explorer (paid) feature, not available here."
    />
  );
}

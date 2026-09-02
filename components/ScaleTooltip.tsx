"use client";

import { useEffect, useId, useLayoutEffect, useRef, useState, type ReactNode } from "react";
import { TONE_BG, type Scale } from "@/lib/scales";

// These chips server-render, and React warns that useLayoutEffect does nothing
// on the server. The edge-flip below still wants to run before paint in the
// browser so the card never appears left and then jumps right.
const useIsomorphicLayoutEffect = typeof window === "undefined" ? useEffect : useLayoutEffect;

/**
 * Wraps a signal chip and, on hover or keyboard focus, shows the whole scale
 * the chip is drawn from — every level, its color, and what that level means —
 * with the chip's own value marked.
 *
 * A native `title` can't render a color swatch, and the color *is* half the
 * encoding, so the description that used to live in `title` moves in here.
 * It stays reachable without hover through the visually-hidden copy below.
 */
export default function ScaleTooltip({
  scale,
  current,
  description,
  children,
}: {
  scale: Scale;
  /** The chip's own value — matched against each step's `key`. */
  current: string;
  /** Sentence describing this chip's current value, shown above the scale. */
  description: string;
  children: ReactNode;
}) {
  const id = useId();
  const [open, setOpen] = useState(false);
  const [alignRight, setAlignRight] = useState(false);
  const wrapRef = useRef<HTMLSpanElement>(null);
  const popRef = useRef<HTMLSpanElement>(null);

  // Flip the popover to the chip's right edge when opening it on the left
  // would push it past the viewport — chips sit in wrapped rows, so the last
  // chip in a row is routinely close enough to matter.
  useIsomorphicLayoutEffect(() => {
    if (!open || !popRef.current) return;
    const rect = popRef.current.getBoundingClientRect();
    setAlignRight(rect.right > window.innerWidth - 8);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <span
      ref={wrapRef}
      className="relative inline-flex"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocusCapture={() => setOpen(true)}
      onBlurCapture={(e) => {
        if (!wrapRef.current?.contains(e.relatedTarget as Node)) setOpen(false);
      }}
    >
      <span aria-describedby={id} className="inline-flex">
        {children}
      </span>

      {/* Available to screen readers and to anyone who can't hover. */}
      <span className="sr-only">
        {description} Scale:{" "}
        {scale.steps.map((s) => `${s.value} — ${s.label}`).join("; ")}.
      </span>

      {open && (
        <span
          id={id}
          ref={popRef}
          role="tooltip"
          className={`absolute top-full z-30 mt-1.5 w-72 max-w-[calc(100vw-2rem)] rounded-lg border border-border bg-card p-3 text-left shadow-lg ${
            alignRight ? "right-0" : "left-0"
          }`}
        >
          <span className="block text-[0.6875rem] leading-snug text-ink/80">{description}</span>

          <span className="mt-2.5 block border-t border-border pt-2.5">
            <span className="mb-1.5 block text-[0.625rem] uppercase tracking-wide text-muted-ink">
              {scale.what}
            </span>
            <span className="block space-y-1">
              {scale.steps.map((step) => {
                const isCurrent = step.key === current;
                return (
                  <span
                    key={step.key}
                    className={`flex items-baseline gap-2 rounded px-1 py-0.5 text-[0.6875rem] leading-snug ${
                      isCurrent ? "bg-accent-wash text-ink" : "text-muted-ink"
                    }`}
                  >
                    <span
                      className={`mt-[0.3rem] h-2 w-2 shrink-0 rounded-full ${TONE_BG[step.tone]}`}
                      aria-hidden
                    />
                    <span className={`shrink-0 tabular-nums ${isCurrent ? "font-semibold" : "font-medium"}`}>
                      {step.value}
                    </span>
                    <span className="text-muted-ink">{step.label}</span>
                    {isCurrent && <span className="ml-auto shrink-0 text-[0.625rem] text-forest">this paper</span>}
                  </span>
                );
              })}
            </span>
          </span>

          {scale.note && (
            <span className="mt-2 block border-t border-border pt-2 text-[0.625rem] leading-snug text-muted-ink">
              {scale.note}
            </span>
          )}
        </span>
      )}
    </span>
  );
}

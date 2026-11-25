"use client";

import { useEffect, useId, useLayoutEffect, useRef, useState, type ReactNode } from "react";

// useLayoutEffect warns during server rendering; the flip below still needs to
// run before paint in the browser (same approach as ScaleTooltip).
const useIsoLayoutEffect = typeof window === "undefined" ? useEffect : useLayoutEffect;

/**
 * A small tooltip that opens on hover and on keyboard focus, closes on Escape
 * or blur, and stays readable to screen readers (the text is always in the DOM
 * and linked with aria-describedby). `Tip` wraps any control; `InfoTip` is a
 * "?" button for hiding a long explanation until someone asks for it.
 */
export function Tip({
  content,
  children,
  width = "16rem",
}: {
  content: ReactNode;
  children: ReactNode;
  width?: string;
}) {
  const id = useId();
  const [open, setOpen] = useState(false);
  const [flip, setFlip] = useState(false);
  const wrapRef = useRef<HTMLSpanElement>(null);
  const popRef = useRef<HTMLSpanElement>(null);

  useIsoLayoutEffect(() => {
    if (!open || !popRef.current) return;
    const rect = popRef.current.getBoundingClientRect();
    setFlip(rect.right > window.innerWidth - 8);
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
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
      <span
        id={id}
        ref={popRef}
        role="tooltip"
        hidden={!open}
        style={{ width }}
        className={`absolute top-full z-30 mt-1.5 max-w-[calc(100vw-2rem)] rounded-lg border border-border bg-card p-3 text-left text-xs font-normal leading-snug text-ink shadow-lg ${
          flip ? "right-0" : "left-0"
        }`}
      >
        {content}
      </span>
    </span>
  );
}

export default function InfoTip({
  label,
  children,
  width = "20rem",
}: {
  /** Accessible name of the "?" button, e.g. "About privacy". */
  label: string;
  children: ReactNode;
  width?: string;
}) {
  return (
    <Tip content={children} width={width}>
      <button
        type="button"
        aria-label={label}
        className="inline-flex h-5 w-5 items-center justify-center rounded-full border border-border text-[0.65rem] font-semibold text-muted-ink hover:text-ink focus-visible:text-ink"
      >
        ?
      </button>
    </Tip>
  );
}

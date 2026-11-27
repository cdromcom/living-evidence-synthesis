"use client";

import { useEffect, useId, useRef, useState } from "react";
import { createPortal } from "react-dom";
import type { RowDetail, SignalSection, ToolCheck } from "@/lib/qualitySignalDetail";

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "2026-11-26T20:00:00Z" becomes "26 Nov 2026". Done by hand so server and browser agree. */
function formatDate(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  if (!m) return "";
  return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
}

const words = (id: string) => {
  const s = id.replace(/-/g, " ");
  return s.charAt(0).toUpperCase() + s.slice(1);
};

const AGREEMENT: Record<string, string> = {
  agree: "All raters agree.",
  majority: "A majority of raters agree.",
  "no-majority": "No majority among the raters.",
};

const TOOL_STATUS: Record<string, string> = {
  ok: "No issue found",
  flag: "Needs a look",
  unavailable: "Could not be checked",
};

function reading(score: number | null): string {
  if (score === null) return "no score";
  if (score >= 0.8) return "supports the rating";
  if (score >= 0.5) return "partly supports the rating";
  return "does not support the rating";
}

function ToolCheckItem({ check }: { check: ToolCheck }) {
  const date = formatDate(check.checked_utc);
  const tool = check.url ? (
    <a href={check.url} target="_blank" rel="noreferrer" className="underline hover:text-forest">
      {check.tool}
    </a>
  ) : (
    check.tool
  );
  return (
    <li className="border-t border-border/70 py-2 first:border-t-0">
      <p className="font-medium">{check.label}</p>
      {check.result && <p>{check.result}</p>}
      {check.detail && <p className="text-muted-ink">{check.detail}</p>}
      <p className="mt-0.5 text-xs text-muted-ink">
        {TOOL_STATUS[check.status] ?? words(check.status)}. Checked {date && `on ${date} `}with {tool}.
      </p>
    </li>
  );
}

function RatingBlocks({ ratings }: { ratings: SignalSection["ratings"] }) {
  return (
    <>
      {ratings.map((r, i) => {
        const where = [r.locator, r.pdf_page != null && `PDF page ${r.pdf_page}`, r.printed_page && `printed page ${r.printed_page}`]
          .filter(Boolean)
          .join(", ");
        return (
          <div key={`${r.rater}-${i}`} className="mt-3 rounded-md border border-border bg-card p-3">
            <p className="font-medium">
              {r.rater}: <span className="font-normal">{words(r.rating)}</span>
            </p>
            {r.quote && (
              <blockquote className="mt-1.5 border-l-2 border-ink/25 pl-2.5 text-muted-ink">
                {r.quote}
              </blockquote>
            )}
            {where && <p className="mt-1 text-xs text-muted-ink">{where}</p>}
            {r.screenshot && (
              <a href={`/quality-signals/${r.screenshot}`} target="_blank" rel="noreferrer" className="mt-2 block">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={`/quality-signals/${r.screenshot}`}
                  alt={`Screenshot of the page with the quote from ${r.rater}`}
                  loading="lazy"
                  className="max-h-64 w-full rounded border border-border object-contain object-left"
                />
              </a>
            )}
          </div>
        );
      })}
    </>
  );
}

function VerifierChecks({ checks }: { checks: SignalSection["checks"] }) {
  if (checks.length === 0) return null;
  return (
    <div className="mt-3">
      <h4 className="text-xs font-semibold uppercase tracking-wide text-muted-ink">Verifier checks</h4>
      <ul className="mt-1">
        {checks.map((c, i) => (
          <li key={`${c.verifier}-${i}`} className="py-0.5">
            {c.verifier.replace(/^Claude /, "")}: {reading(c.score)}
            {c.score !== null && <small className="ml-1.5 text-xs text-muted-ink">{c.score.toFixed(2)}</small>}
            {c.note && <span className="block text-muted-ink">{c.note}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}

function Section({ section, showHeading }: { section: SignalSection; showHeading: boolean }) {
  const final = words(section.final);
  return (
    <section className="mt-5 first:mt-0" aria-label={showHeading ? section.label : undefined}>
      {showHeading ? (
        <h3 className="border-b border-ink/30 pb-1 text-sm font-semibold">
          {section.label}: <span className="font-normal">{final}</span>
        </h3>
      ) : (
        <p className="text-sm font-semibold">Result: {final}</p>
      )}
      {section.summary && <p className="mt-2">{section.summary}</p>}
      {section.ratings.length > 0 && (
        <p className="mt-1 text-xs text-muted-ink">{AGREEMENT[section.agreement] ?? ""}</p>
      )}
      <RatingBlocks ratings={section.ratings} />
      <VerifierChecks checks={section.checks} />

      {section.toolChecks.length > 0 && (
        <div className="mt-3">
          <h4 className="text-xs font-semibold uppercase tracking-wide text-muted-ink">Tool checks</h4>
          <ul>
            {section.toolChecks.map((t) => (
              <ToolCheckItem key={t.id} check={t} />
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

const TRIPOD_DOT: Record<string, string> = {
  fully: "bg-green-600",
  partial: "bg-amber-500",
  "not-reported": "bg-red-600",
  "not-applicable": "bg-muted-ink/50",
};

function TripodItem({ item }: { item: SignalSection }) {
  const label = item.label.replace(/^TRIPOD-LLM /, "");
  const head = (
    <>
      <span aria-hidden className={`mt-[0.35rem] h-[7px] w-[7px] shrink-0 rounded-full ${TRIPOD_DOT[item.final] ?? "bg-muted-ink/50"}`} />
      <span className="min-w-0 flex-1">{label}</span>
      <span className="shrink-0 text-muted-ink">{words(item.final)}</span>
    </>
  );
  const differs = item.matchesVault === false && item.vaultValue;
  const note = differs ? (
    <p className="pb-1 pl-[15px] text-xs text-muted-ink">Earlier table on this site: {words(item.vaultValue as string)}</p>
  ) : null;
  const expandable = item.ratings.length > 0 || Boolean(item.summary);
  return (
    <li className="border-t border-border/70 first:border-t-0">
      {expandable ? (
        <details className="group">
          <summary className="flex cursor-pointer items-baseline gap-2 py-1 marker:content-none [&::-webkit-details-marker]:hidden">
            {head}
          </summary>
          {note}
          <div className="pb-2 pl-[15px]">
            {item.summary && <p className="mt-1">{item.summary}</p>}
            <RatingBlocks ratings={item.ratings} />
            <VerifierChecks checks={item.checks} />
          </div>
        </details>
      ) : (
        <>
          <div className="flex items-baseline gap-2 py-1">{head}</div>
          {note}
        </>
      )}
    </li>
  );
}

function TripodBody({ tripod }: { tripod: NonNullable<RowDetail["tripod"]> }) {
  const { summary: s, items } = tripod;
  const todo = items.filter((i) => i.final === "partial" || i.final === "not-reported");
  const fully = items.filter((i) => i.final === "fully");
  const na = items.filter((i) => i.final === "not-applicable");
  return (
    <>
      <p className="text-sm font-semibold">
        {s.fully} fully, {s.partial} partial, {s["not-reported"]} not reported, {s["not-applicable"]} not applicable.
      </p>
      <p className="mt-1 text-muted-ink">
        {s.pct}% of the {s.applicable} applicable items reported (partial counts as half), {s.level}.
      </p>
      {todo.length > 0 && (
        <>
          <h3 className="mt-4 text-xs font-semibold uppercase tracking-wide text-muted-ink">Partial or not reported</h3>
          <ul>{todo.map((i) => <TripodItem key={i.id} item={i} />)}</ul>
        </>
      )}
      {fully.length > 0 && (
        <>
          <h3 className="mt-4 text-xs font-semibold uppercase tracking-wide text-muted-ink">Fully reported</h3>
          <ul>{fully.map((i) => <TripodItem key={i.id} item={i} />)}</ul>
        </>
      )}
      {na.length > 0 && (
        <details className="mt-4">
          <summary className="cursor-pointer text-xs font-semibold uppercase tracking-wide text-muted-ink">
            Not applicable ({na.length})
          </summary>
          <ul>{na.map((i) => <TripodItem key={i.id} item={i} />)}</ul>
        </details>
      )}
    </>
  );
}

const FOCUSABLE = 'a[href], button:not([disabled]), summary, [tabindex]:not([tabindex="-1"])';

/**
 * Side panel with the detail behind one Quality signals row. A dialog that
 * closes with its button, Escape, or a click outside; focus moves into it on
 * open and goes back to the row that opened it on close. It is fixed and does
 * not lock page scroll, so opening it moves nothing on the page.
 */
export default function QualitySignalDrawer({
  title,
  href,
  detail,
  returnFocusTo,
  onClose,
}: {
  title: string;
  /** Anchor of the row in the page's tables, when there is one. */
  href?: string;
  detail: RowDetail;
  returnFocusTo: HTMLElement | null;
  onClose: () => void;
}) {
  const titleId = useId();
  const panelRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const [entered, setEntered] = useState(false);
  const onCloseRef = useRef(onClose);

  useEffect(() => {
    onCloseRef.current = onClose;
  });

  useEffect(() => {
    const frame = requestAnimationFrame(() => setEntered(true));
    closeRef.current?.focus();
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") {
        e.preventDefault();
        onCloseRef.current();
      } else if (e.key === "Tab" && panelRef.current) {
        const items = Array.from(panelRef.current.querySelectorAll<HTMLElement>(FOCUSABLE));
        if (items.length === 0) return;
        const first = items[0];
        const last = items[items.length - 1];
        if (!panelRef.current.contains(document.activeElement)) {
          e.preventDefault();
          first.focus();
        } else if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }
    document.addEventListener("keydown", onKey);
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener("keydown", onKey);
      returnFocusTo?.focus({ preventScroll: true });
    };
  }, [returnFocusTo]);

  const many = detail.sections.length > 1;

  return createPortal(
    <div
      className="fixed inset-0 z-50 bg-black/30"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        className={`absolute inset-y-0 right-0 flex h-dvh w-full flex-col overflow-y-auto overscroll-contain border-l border-border bg-paper text-sm leading-snug text-ink shadow-xl transition-transform duration-200 ease-out motion-reduce:transition-none sm:w-[30rem] ${
          entered ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="sticky top-0 z-10 flex items-start justify-between gap-3 border-b border-border bg-paper px-4 py-3">
          <h2 id={titleId} className="text-base font-semibold">
            {title}
          </h2>
          <button
            ref={closeRef}
            type="button"
            onClick={onClose}
            className="-mr-1 shrink-0 rounded-md border border-border bg-card px-2 py-0.5 text-xs hover:border-forest/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-forest"
          >
            Close
          </button>
        </div>

        <div className="px-4 py-4">
          {detail.tripod && <TripodBody tripod={detail.tripod} />}
          {detail.sections.map((s) => (
            <Section key={s.id} section={s} showHeading={many} />
          ))}

          {detail.paperChecks.length > 0 && (
            <details className="mt-6 border-t border-border pt-3">
              <summary className="cursor-pointer text-sm font-semibold">Checks on the paper</summary>
              <ul className="mt-1">
                {detail.paperChecks.map((t) => (
                  <ToolCheckItem key={t.id} check={t} />
                ))}
              </ul>
            </details>
          )}

          {href && (
            <p className="mt-6 border-t border-border pt-3">
              <a href={href} onClick={onClose} className="underline hover:text-forest">
                Open in the table
              </a>
            </p>
          )}
        </div>
      </div>
    </div>,
    document.body
  );
}

"use client";

import { useId, useState } from "react";
import {
  CATEGORIES,
  PAGE_PATTERN,
  buildIssueDraft,
  getCategory,
} from "@/lib/review-categories";

const REPO = process.env.NEXT_PUBLIC_GITHUB_REPO || "cdromcom/living-evidence-synthesis";
const SITE = (process.env.NEXT_PUBLIC_SITE_URL || "").replace(/\/+$/, "");

const fieldClass =
  "mt-1 w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest";
const labelClass = "block text-xs font-semibold text-muted-ink";

/**
 * "Report on GitHub": pick a review category (and a verdict or error type),
 * add the quote, page and a note, and open a GitHub issue whose title and body
 * are already filled in. Nothing is sent from this site; the contributor
 * reviews and submits the issue on GitHub.
 */
export default function NodeIssuePanel({
  nodeId,
  nodeTitle,
}: {
  nodeId: string;
  nodeTitle: string;
}) {
  const uid = useId();
  const [categoryKey, setCategoryKey] = useState("");
  const [verdictLabel, setVerdictLabel] = useState("");
  const [quote, setQuote] = useState("");
  const [page, setPage] = useState("");
  const [note, setNote] = useState("");

  const category = getCategory(categoryKey);
  const needsVerdict = category?.kind === "judgment" || category?.kind === "overall";
  const pageBad = page.trim() !== "" && !PAGE_PATTERN.test(page.trim());
  const ready = Boolean(category) && (!needsVerdict || verdictLabel !== "") && !pageBad;

  const draft = buildIssueDraft({
    nodeId,
    nodeTitle,
    categoryKey,
    verdictLabel,
    quote: quote.slice(0, 1500),
    page,
    note: note.slice(0, 1500),
    nodeUrl: `${SITE}/nodes/${nodeId}`,
  });
  const href =
    `https://github.com/${REPO}/issues/new?` +
    new URLSearchParams({ title: draft.title, body: draft.body }).toString();

  const verdictOptions =
    category?.kind === "judgment"
      ? category.dimension.verdicts
      : category?.kind === "overall"
        ? [
            { label: "Correct" },
            { label: "Edit" },
            { label: "Wrong" },
            { label: "Missing" },
            { label: "N/A" },
          ]
        : [];

  return (
    <section aria-labelledby={`${uid}-h`} className="rounded-lg border border-border bg-card p-4">
      <h2 id={`${uid}-h`} className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
        Report on GitHub
      </h2>
      <p id={`${uid}-intro`} className="mt-1 text-xs text-muted-ink">
        Choose a category and we open a GitHub issue with the details already filled in. You
        review it and submit on GitHub.
      </p>

      <div className="mt-3">
        <label htmlFor={`${uid}-cat`} className={labelClass}>
          Category
        </label>
        <select
          id={`${uid}-cat`}
          value={categoryKey}
          onChange={(e) => {
            setCategoryKey(e.target.value);
            setVerdictLabel("");
          }}
          className={fieldClass}
        >
          <option value="">Choose a category…</option>
          <optgroup label="Judgment">
            {CATEGORIES.filter((c) => c.kind !== "error").map((c) => (
              <option key={c.key} value={c.key}>
                {c.label}
              </option>
            ))}
          </optgroup>
          <optgroup label="Error type">
            {CATEGORIES.filter((c) => c.kind === "error").map((c) => (
              <option key={c.key} value={c.key}>
                {c.label}
              </option>
            ))}
          </optgroup>
        </select>
        {category?.kind === "judgment" && (
          <p className="mt-1 text-xs text-muted-ink">{category.dimension.help}</p>
        )}
      </div>

      {needsVerdict && (
        <fieldset className="mt-3">
          <legend className={labelClass}>Verdict</legend>
          <div className="mt-1 space-y-1">
            {verdictOptions.map((v, i) => {
              const id = `${uid}-v${i}`;
              const help = "help" in v ? v.help : undefined;
              return (
                <div key={v.label} className="flex items-start gap-2 text-sm">
                  <input
                    id={id}
                    type="radio"
                    name={`${uid}-verdict`}
                    checked={verdictLabel === v.label}
                    onChange={() => setVerdictLabel(v.label)}
                    aria-describedby={help ? `${id}-d` : undefined}
                    className="mt-1 h-4 w-4"
                  />
                  <label htmlFor={id} className="min-h-6 flex-1">
                    {v.label}
                    {help && (
                      <span id={`${id}-d`} className="block text-xs text-muted-ink">
                        {help}
                      </span>
                    )}
                  </label>
                </div>
              );
            })}
          </div>
        </fieldset>
      )}

      {category && (
        <div className="mt-3 space-y-3">
          <div>
            <label htmlFor={`${uid}-quote`} className={labelClass}>
              Quote (optional)
            </label>
            <textarea
              id={`${uid}-quote`}
              rows={2}
              maxLength={1500}
              value={quote}
              onChange={(e) => setQuote(e.target.value)}
              className={fieldClass}
            />
          </div>
          <div>
            <label htmlFor={`${uid}-page`} className={labelClass}>
              Printed page (optional)
            </label>
            <input
              id={`${uid}-page`}
              value={page}
              onChange={(e) => setPage(e.target.value)}
              aria-invalid={pageBad}
              aria-describedby={`${uid}-page-d`}
              className={fieldClass}
            />
            <p id={`${uid}-page-d`} className="mt-1 text-xs text-muted-ink">
              The number printed on the page, such as 5 or 5-6, not the PDF position.
            </p>
            {pageBad && (
              <p role="alert" className="mt-1 text-xs text-destructive">
                Use a page like 5, 5-6 or S3.
              </p>
            )}
          </div>
          <div>
            <label htmlFor={`${uid}-note`} className={labelClass}>
              Note (optional)
            </label>
            <textarea
              id={`${uid}-note`}
              rows={3}
              maxLength={1500}
              value={note}
              onChange={(e) => setNote(e.target.value)}
              className={fieldClass}
            />
          </div>
        </div>
      )}

      <div className="mt-3">
        {ready ? (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex min-h-11 items-center rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper"
          >
            Open prefilled GitHub issue<span className="sr-only"> (opens in a new tab)</span>
            <span aria-hidden> ↗</span>
          </a>
        ) : (
          <p className="text-xs text-muted-ink">
            {category ? "Pick a verdict to continue." : "Pick a category to start."}
          </p>
        )}
      </div>
    </section>
  );
}

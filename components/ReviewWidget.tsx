"use client";

import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { supabase, supabaseConfigured, REVIEW_NOTE_MAX, type Verdict, type NodeReview } from "@/lib/supabase";
import { loadReviews } from "@/lib/reviews";
import { useAuth } from "@/lib/useAuth";
import { VERDICT_VOCAB } from "@/lib/ui";
import { CATEGORIES, OVERALL_DIMENSION, buildMultiIssueDraft, getCategory, verdictLabelFor, type Category } from "@/lib/review-categories";
import InfoTip, { Tip } from "./InfoTip";

const fieldClass =
  "w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest";

type Entry = { verdict: Verdict | ""; proposed: string; note: string };

function optionsFor(cat: Category): { key: Verdict; label: string; help?: string }[] {
  if (cat.kind === "judgment") return cat.dimension.verdicts.map((v) => ({ key: v.verdict, label: v.label, help: v.help }));
  if (cat.kind === "error") return [{ key: "wrong", label: "Error present", help: "You found this kind of error on this node." }];
  return VERDICT_VOCAB.map((v) => ({ key: v.key as Verdict, label: v.label, help: v.description }));
}

const REPO = process.env.NEXT_PUBLIC_GITHUB_REPO || "cdromcom/living-evidence-synthesis";
const SITE = (process.env.NEXT_PUBLIC_SITE_URL || "").replace(/\/+$/, "");

export default function ReviewWidget({ nodeId, nodeTitle }: { nodeId: string; nodeTitle: string }) {
  const { session, loading: authLoading } = useAuth();
  const pathname = usePathname();
  const uid = useId();

  const [picked, setPicked] = useState<string[]>([OVERALL_DIMENSION]);
  const [entries, setEntries] = useState<Record<string, Entry>>({});
  const [reviews, setReviews] = useState<NodeReview[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [viewMissing, setViewMissing] = useState(false);
  const [consent, setConsent] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mineFor = (key: string) => (session ? reviews.find((r) => r.is_mine && r.dimension === key) : undefined);
  const hasAnyMine = session ? reviews.some((r) => r.is_mine) : false;
  // What the form shows for a category: what the reviewer has typed, else their saved review.
  const entryFor = (key: string): Entry =>
    entries[key] ?? {
      verdict: mineFor(key)?.verdict ?? "",
      proposed: mineFor(key)?.proposed ?? "",
      note: mineFor(key)?.note ?? "",
    };
  const patch = (key: string, p: Partial<Entry>) => {
    setSavedAt(null);
    setEntries((prev) => ({ ...prev, [key]: { ...entryFor(key), ...p } }));
  };
  const toggle = (key: string) => setPicked((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]));

  async function refresh() {
    if (!session) return;
    setLoadingReviews(true);
    const r = await loadReviews({ userId: session.user.id, nodeId });
    setReviews(r.reviews);
    setViewMissing(r.viewMissing);
    setLoadError(r.error);
    setLoadingReviews(false);
  }

  useEffect(() => {
    if (!session) return;
    // A session or node change must show a loading state; this is not derivable during render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, nodeId]);

  // Someone who has already reviewed has already agreed to the privacy notice.
  const [consentSeeded, setConsentSeeded] = useState(false);
  if (hasAnyMine && !consentSeeded) {
    setConsentSeeded(true);
    setConsent(true);
  }

  const ready = picked.length > 0 && picked.every((k) => entryFor(k).verdict);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase || !session || !ready || !consent) return;
    setSaving(true);
    setError(null);
    const rows = picked.map((key) => {
      const en = entryFor(key);
      return {
        reviewer_id: session.user.id,
        node_id: nodeId,
        dimension: key,
        verdict: en.verdict,
        proposed: en.proposed || null,
        note: en.note || null,
      };
    });
    const { error } = await supabase.from("node_reviews").upsert(rows, { onConflict: "reviewer_id,node_id,dimension" });
    setSaving(false);
    if (error) {
      setError(error.message);
      return;
    }
    setSavedAt(Date.now());
    refresh();
  }

  if (!supabaseConfigured) return null;

  const myAlias = reviews.find((r) => r.is_mine)?.reviewer_name;
  const issueDraft = buildMultiIssueDraft({
    nodeId,
    nodeTitle,
    nodeUrl: `${SITE || (typeof window === "undefined" ? "" : window.location.origin)}/nodes/${nodeId}`,
    entries: picked.map((key) => {
      const en = entryFor(key);
      return { categoryKey: key, verdictLabel: verdictLabelFor(key, en.verdict as Verdict) ?? VERDICT_VOCAB.find((v) => v.key === en.verdict)?.label ?? "", proposed: en.proposed, note: en.note };
    }),
  });
  const issueHref = `https://github.com/${REPO}/issues/new?` + new URLSearchParams({ title: issueDraft.title, body: issueDraft.body }).toString();
  const needsProposed = (v: Verdict | "") => v === "edit" || v === "edit-major" || v === "edit-minor";
  const mainCats = CATEGORIES.filter((c) => c.kind !== "error");
  const errorCats = CATEGORIES.filter((c) => c.kind === "error");
  const anyErrorPicked = errorCats.some((c) => picked.includes(c.key));

  const checkbox = (c: Category) => (
    <label key={c.key} className="flex min-h-8 items-start gap-2 text-sm">
      <input
        type="checkbox"
        checked={picked.includes(c.key)}
        onChange={() => toggle(c.key)}
        className="mt-1 h-4 w-4"
      />
      <span>
        {c.label}
        {mineFor(c.key) && <span className="text-xs text-muted-ink"> (you reviewed this)</span>}
      </span>
    </label>
  );

  return (
    <section aria-labelledby={`${uid}-h`} className="rounded-lg border border-border bg-card p-4">
      <h2 id={`${uid}-h`} className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
        Review this node
      </h2>
      {session && (
        <p className="mt-1 text-xs text-muted-ink">
          Tick what applies. Submit saves your verdicts here; or open the same details as a GitHub issue.
        </p>
      )}

      {authLoading ? (
        <p role="status" className="mt-2 text-sm text-muted-ink">
          Checking sign-in…
        </p>
      ) : !session ? (
        <p className="mt-2 text-sm text-muted-ink">
          <Link href={`/login?next=${encodeURIComponent(pathname)}`} className="text-forest underline">
            Sign in
          </Link>{" "}
          to review this node or report a problem with it.
        </p>
      ) : (
        <form onSubmit={submit} className="mt-3 space-y-4">
          <fieldset>
            <legend className="text-xs font-semibold text-muted-ink">Categories (choose one or more)</legend>
            <div className="mt-1 space-y-0.5">{mainCats.map(checkbox)}</div>
            <details className="mt-1" open={anyErrorPicked || undefined}>
              <summary className="min-h-8 cursor-pointer text-sm text-muted-ink">Error types</summary>
              <div className="space-y-0.5">{errorCats.map(checkbox)}</div>
            </details>
          </fieldset>

          {picked.length === 0 && <p className="text-xs text-muted-ink">Choose at least one category.</p>}

          {picked.map((key) => {
            const cat = getCategory(key);
            if (!cat) return null;
            const en = entryFor(key);
            const opts = optionsFor(cat);
            const intro =
              cat.kind === "judgment"
                ? cat.dimension.help
                : cat.kind === "error"
                  ? "Mark this error type if you found it on this node."
                  : "One overall accuracy verdict for the node.";
            return (
              <fieldset key={key} className="space-y-2 rounded-md border border-border p-3">
                <legend className="px-1 text-xs font-semibold">{cat.label}</legend>
                <p className="text-xs text-muted-ink">{intro}</p>
                <div className="flex flex-wrap gap-1.5">
                  {opts.map((o) => {
                    const v = VERDICT_VOCAB.find((x) => x.key === o.key)!;
                    const on = en.verdict === o.key;
                    const btn = (
                      <button
                        type="button"
                        aria-pressed={on}
                        onClick={() => patch(key, { verdict: o.key })}
                        className="flex min-h-11 items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium transition-colors sm:min-h-8"
                        style={on ? { backgroundColor: v.color, borderColor: v.color, color: v.textColor } : { borderColor: "var(--color-border)" }}
                      >
                        <span className="mono" aria-hidden>
                          {v.symbol}
                        </span>
                        {o.label}
                      </button>
                    );
                    return o.help ? (
                      <Tip key={o.label} content={o.help} width="15rem">
                        {btn}
                      </Tip>
                    ) : (
                      <span key={o.label}>{btn}</span>
                    );
                  })}
                </div>

                {needsProposed(en.verdict) && (
                  <div>
                    <label htmlFor={`${uid}-${key}-prop`} className="block text-xs font-semibold text-muted-ink">
                      Proposed correction
                    </label>
                    <textarea
                      id={`${uid}-${key}-prop`}
                      value={en.proposed}
                      onChange={(e) => patch(key, { proposed: e.target.value })}
                      maxLength={REVIEW_NOTE_MAX}
                      rows={2}
                      className={`mt-1 ${fieldClass}`}
                    />
                  </div>
                )}

                <div>
                  <label htmlFor={`${uid}-${key}-note`} className="block text-xs font-semibold text-muted-ink">
                    Note (optional)
                  </label>
                  <textarea
                    id={`${uid}-${key}-note`}
                    value={en.note}
                    onChange={(e) => patch(key, { note: e.target.value })}
                    maxLength={REVIEW_NOTE_MAX}
                    rows={2}
                    className={`mt-1 ${fieldClass}`}
                  />
                </div>
              </fieldset>
            );
          })}

          <div className="flex items-center gap-2 text-xs text-muted-ink">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} className="h-4 w-4" />
              <span>I agree to the privacy notice</span>
            </label>
            <InfoTip label="About privacy" width="20rem">
              Privacy: your verdicts and notes are shown to other signed-in reviewers under a randomly assigned galaxy name
              {myAlias ? ` (yours is ${myAlias})` : ""}, which stays the same for all your reviews. Your email address is
              never shown to them. You can change or delete your reviews at any time.
            </InfoTip>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={!ready || !consent || saving}
              aria-describedby={!ready || !consent ? `${uid}-need` : undefined}
              className="min-h-11 rounded-lg bg-forest px-4 py-1.5 text-sm font-medium text-paper disabled:opacity-50 sm:min-h-9"
            >
              {saving
                ? "Saving…"
                : picked.length > 1
                  ? `Submit ${picked.length} verdicts`
                  : picked.length === 1 && mineFor(picked[0])
                    ? "Update verdict"
                    : "Submit verdict"}
            </button>
            {savedAt && !saving && (
              <span role="status" className="text-xs text-muted-ink">
                Saved.
              </span>
            )}
          </div>
          <p className="text-xs text-muted-ink">
            {ready ? (
              <a href={issueHref} target="_blank" rel="noopener noreferrer" className="underline hover:text-ink">
                Open these details as a GitHub issue
                <span className="sr-only"> (opens GitHub in a new tab)</span>
              </a>
            ) : (
              <span>Choose a verdict in each ticked category to open them as a GitHub issue.</span>
            )}
          </p>
          {(!ready || !consent) && (
            <p id={`${uid}-need`} className="text-xs text-muted-ink">
              {!ready ? "Choose a verdict in each category you ticked" : "Tick the privacy agreement"} to submit.
            </p>
          )}
          {error && (
            <p role="alert" className="text-xs text-destructive">
              Could not save: {error}
            </p>
          )}
        </form>
      )}

      {session && (
        <div className="mt-4 border-t border-border pt-3" aria-live="polite">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-ink">
            {viewMissing ? "Your verdicts" : "All verdicts"}
            {!loadingReviews && !loadError ? ` (${reviews.length})` : ""}
          </h3>
          {viewMissing && (
            <p className="mt-1 text-xs text-muted-ink">Other reviewers&apos; verdicts will appear here once the site&apos;s review list is switched on.</p>
          )}
          {loadingReviews ? (
            <p role="status" className="mt-2 text-xs text-muted-ink">
              Loading verdicts…
            </p>
          ) : loadError ? (
            <div role="alert" className="mt-2 text-xs text-destructive">
              Could not load verdicts: {loadError}{" "}
              <button type="button" onClick={() => refresh()} className="min-h-6 font-medium underline">
                Try again
              </button>
            </div>
          ) : reviews.length === 0 ? (
            <p className="mt-2 text-xs text-muted-ink">No verdicts yet for this node.</p>
          ) : (
            <ul className="mt-2 space-y-2">
              {reviews.map((r) => {
                const v = VERDICT_VOCAB.find((x) => x.key === r.verdict);
                const rc = getCategory(r.dimension);
                const catLabel = rc && rc.kind !== "overall" ? rc.label : null;
                const vLabel = verdictLabelFor(r.dimension, r.verdict) ?? v?.label;
                return (
                  <li key={r.id} className="flex items-start gap-2 text-xs">
                    <span
                      aria-hidden
                      className="mono flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[0.65rem] font-semibold"
                      style={{ backgroundColor: v?.color, color: v?.textColor }}
                    >
                      {v?.symbol}
                    </span>
                    <div>
                      <span className="font-medium">{r.reviewer_name}</span>
                      <span className="text-muted-ink">
                        {" "}
                        — {catLabel ? `${catLabel}: ` : ""}
                        {vLabel}
                      </span>
                      {r.note && <span className="text-muted-ink">: {r.note}</span>}
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}

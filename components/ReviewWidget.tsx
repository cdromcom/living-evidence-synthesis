"use client";

import { useEffect, useId, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { supabase, supabaseConfigured, REVIEW_NOTE_MAX, type Verdict, type NodeReview } from "@/lib/supabase";
import { useAuth } from "@/lib/useAuth";
import { VERDICT_VOCAB } from "@/lib/ui";
import { CATEGORIES, OVERALL_DIMENSION, getCategory, verdictLabelFor } from "@/lib/review-categories";

const fieldClass =
  "w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest";

export default function ReviewWidget({ nodeId }: { nodeId: string }) {
  const { session, loading: authLoading } = useAuth();
  const pathname = usePathname();
  const uid = useId();
  const [category, setCategory] = useState<string>(OVERALL_DIMENSION);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [reviews, setReviews] = useState<NodeReview[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(true);
  const [verdict, setVerdict] = useState<Verdict | "">("");
  const [proposed, setProposed] = useState("");
  const [note, setNote] = useState("");
  const [consent, setConsent] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mine = session ? reviews.find((r) => r.is_mine && r.dimension === category) : undefined;
  const hasAnyMine = session ? reviews.some((r) => r.is_mine) : false;
  const cat = getCategory(category) ?? CATEGORIES[0];
  // Verdict choices for the chosen category. "overall" and error types use the
  // existing vocabulary; judgment dimensions use their own labels, each stored
  // as the vocabulary key it maps to (see lib/review-categories.ts).
  const options: { key: Verdict; label: string; help?: string }[] =
    cat.kind === "judgment"
      ? cat.dimension.verdicts.map((v) => ({ key: v.verdict, label: v.label, help: v.help }))
      : cat.kind === "error"
        ? [{ key: "wrong", label: "Error present" }]
        : VERDICT_VOCAB.map((v) => ({ key: v.key as Verdict, label: v.label, help: v.description }));

  async function loadReviews() {
    if (!supabase || !session) return;
    setLoadingReviews(true);
    const { data, error } = await supabase
      .from("node_reviews_public")
      .select("*")
      .eq("node_id", nodeId)
      .order("updated_at", { ascending: false });
    if (error) setLoadError(error.message);
    else {
      setLoadError(null);
      if (data) setReviews(data as NodeReview[]);
    }
    setLoadingReviews(false);
  }

  useEffect(() => {
    // `loadingReviews` is only ever read once the JSX below already knows
    // `session` is truthy — nothing to reset here when there's no session to
    // fetch for (mirrors the same simplification in LiveReviewPanel).
    if (!session) return;
    // loadReviews's own first line flips loadingReviews to true, ahead of the
    // actual async fetch — genuinely needed so a session/nodeId change (e.g.
    // navigating to a different node) shows a loading state, not derivable
    // from anything available during render.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadReviews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, nodeId]);

  // Seeds the form from the signed-in user's own existing review for the
  // chosen category, once per (category, review id) — not a plain effect,
  // since after seeding these fields are freely user-editable. React's own
  // documented pattern for adjusting state during rendering:
  // https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes
  const seedKey = `${category}:${mine?.id ?? ""}`;
  const [seededKey, setSeededKey] = useState<string | undefined>(undefined);
  if (seedKey !== seededKey) {
    setSeededKey(seedKey);
    setVerdict(mine?.verdict ?? "");
    setProposed(mine?.proposed ?? "");
    setNote(mine?.note ?? "");
    setSavedAt(null);
  }
  // Someone who has already reviewed has already agreed to the privacy notice.
  const [consentSeeded, setConsentSeeded] = useState(false);
  if (hasAnyMine && !consentSeeded) {
    setConsentSeeded(true);
    setConsent(true);
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase || !session || !verdict || !consent) return;
    setSaving(true);
    setError(null);
    const { error } = await supabase.from("node_reviews").upsert(
      {
        reviewer_id: session.user.id,
        node_id: nodeId,
        dimension: category,
        verdict,
        proposed: proposed || null,
        note: note || null,
      },
      { onConflict: "reviewer_id,node_id,dimension" }
    );
    setSaving(false);
    if (error) {
      setError(error.message);
      return;
    }
    setSavedAt(Date.now());
    loadReviews();
  }

  if (!supabaseConfigured) return null;

  const needsProposed = verdict === "edit" || verdict === "edit-major" || verdict === "edit-minor";

  return (
    <section aria-labelledby={`${uid}-h`} className="rounded-lg border border-border bg-card p-4">
      <h2 id={`${uid}-h`} className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
        Review this node
      </h2>

      {authLoading ? (
        <p role="status" className="mt-2 text-sm text-muted-ink">
          Checking sign-in…
        </p>
      ) : !session ? (
        <p className="mt-2 text-sm text-muted-ink">
          <Link
            href={`/login?next=${encodeURIComponent(pathname)}`}
            className="text-forest underline"
          >
            Sign in
          </Link>{" "}
          to submit an accuracy verdict for this node.
        </p>
      ) : (
        <form onSubmit={submit} className="mt-3 space-y-3">
          <div>
            <label htmlFor={`${uid}-cat`} className="block text-xs font-semibold text-muted-ink">
              Category
            </label>
            <select
              id={`${uid}-cat`}
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              aria-describedby={`${uid}-cat-d`}
              className={`mt-1 ${fieldClass}`}
            >
              {CATEGORIES.filter((c) => c.kind !== "error").map((c) => (
                <option key={c.key} value={c.key}>
                  {c.label}
                </option>
              ))}
              <optgroup label="Error type">
                {CATEGORIES.filter((c) => c.kind === "error").map((c) => (
                  <option key={c.key} value={c.key}>
                    {c.label}
                  </option>
                ))}
              </optgroup>
            </select>
            <p id={`${uid}-cat-d`} className="mt-1 text-xs text-muted-ink">
              {cat.kind === "judgment"
                ? cat.dimension.help
                : cat.kind === "error"
                  ? "Mark this error type if you found it on this node."
                  : "One overall accuracy verdict for the node."}
            </p>
          </div>

          <fieldset>
            <legend className="text-xs font-semibold text-muted-ink">Verdict</legend>
            <div className="mt-1 flex flex-wrap gap-1.5">
              {options.map((o) => {
                const v = VERDICT_VOCAB.find((x) => x.key === o.key)!;
                const on = verdict === o.key;
                return (
                  <button
                    key={o.label}
                    type="button"
                    aria-pressed={on}
                    onClick={() => setVerdict(o.key)}
                    title={o.help}
                    className="flex min-h-11 items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium transition-colors sm:min-h-8"
                    style={
                      on
                        ? { backgroundColor: v.color, borderColor: v.color, color: v.textColor }
                        : { borderColor: "var(--color-border)" }
                    }
                  >
                    <span className="mono" aria-hidden>
                      {v.symbol}
                    </span>
                    {o.label}
                  </button>
                );
              })}
            </div>
            {options.some((o) => o.help) && cat.kind === "judgment" && (
              <ul className="mt-2 space-y-0.5 text-xs text-muted-ink">
                {options
                  .filter((o) => o.help)
                  .map((o) => (
                    <li key={o.label}>
                      <span className="font-medium text-ink">{o.label}:</span> {o.help}
                    </li>
                  ))}
              </ul>
            )}
          </fieldset>

          {needsProposed && (
            <div>
              <label htmlFor={`${uid}-prop`} className="block text-xs font-semibold text-muted-ink">
                Proposed correction
              </label>
              <textarea
                id={`${uid}-prop`}
                value={proposed}
                onChange={(e) => setProposed(e.target.value)}
                maxLength={REVIEW_NOTE_MAX}
                rows={2}
                className={`mt-1 ${fieldClass}`}
              />
            </div>
          )}

          <div>
            <label htmlFor={`${uid}-note`} className="block text-xs font-semibold text-muted-ink">
              Note (optional)
            </label>
            <textarea
              id={`${uid}-note`}
              value={note}
              onChange={(e) => setNote(e.target.value)}
              maxLength={REVIEW_NOTE_MAX}
              rows={2}
              className={`mt-1 ${fieldClass}`}
            />
          </div>

          <label className="flex items-start gap-2 text-xs text-muted-ink">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-0.5 h-4 w-4"
            />
            <span>
              Privacy: your verdict and note are shown to other signed-in
              reviewers under a randomly assigned galaxy name
              {hasAnyMine ? ` (yours is ${reviews.find((r) => r.is_mine)?.reviewer_name})` : ""}, which stays the same
              for all your reviews. Your email address is never shown to them.
              You can change or delete your review at any time. I agree.
            </span>
          </label>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={!verdict || !consent || saving}
              aria-describedby={!verdict || !consent ? `${uid}-need` : undefined}
              className="min-h-11 rounded-lg bg-forest px-4 py-1.5 text-sm font-medium text-paper disabled:opacity-50 sm:min-h-9"
            >
              {saving ? "Saving…" : mine ? "Update verdict" : "Submit verdict"}
            </button>
            {savedAt && !saving && (
              <span role="status" className="text-xs text-muted-ink">
                Saved.
              </span>
            )}
          </div>
          {(!verdict || !consent) && (
            <p id={`${uid}-need`} className="text-xs text-muted-ink">
              {!verdict ? "Choose a verdict" : "Tick the privacy agreement"} to submit.
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
            All verdicts{!loadingReviews && !loadError ? ` (${reviews.length})` : ""}
          </h3>
          {loadingReviews ? (
            <p role="status" className="mt-2 text-xs text-muted-ink">
              Loading verdicts…
            </p>
          ) : loadError ? (
            <div role="alert" className="mt-2 text-xs text-destructive">
              Could not load verdicts: {loadError}{" "}
              <button
                type="button"
                onClick={() => loadReviews()}
                className="min-h-6 font-medium underline"
              >
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

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { supabase, supabaseConfigured, type Verdict, type NodeReview } from "@/lib/supabase";
import { useAuth } from "@/lib/useAuth";
import { VERDICT_VOCAB } from "@/lib/ui";

export default function ReviewWidget({ nodeId }: { nodeId: string }) {
  const { session, loading: authLoading } = useAuth();
  const pathname = usePathname();

  const [reviews, setReviews] = useState<NodeReview[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(true);
  const [verdict, setVerdict] = useState<Verdict | "">("");
  const [proposed, setProposed] = useState("");
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mine = session
    ? reviews.find((r) => r.reviewer_id === session.user.id)
    : undefined;

  async function loadReviews() {
    if (!supabase || !session) return;
    setLoadingReviews(true);
    const { data, error } = await supabase
      .from("node_reviews")
      .select("*")
      .eq("node_id", nodeId)
      .order("updated_at", { ascending: false });
    if (!error && data) setReviews(data as NodeReview[]);
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

  // Seeds the form from the signed-in user's own existing review, once per
  // distinct review (by id) — not a plain effect, since after seeding these
  // fields are freely user-editable and must not keep snapping back to
  // `mine` on every render. This is React's own documented pattern for
  // adjusting state during rendering: https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes
  const [seededReviewId, setSeededReviewId] = useState<string | undefined>(undefined);
  if (mine && mine.id !== seededReviewId) {
    setSeededReviewId(mine.id);
    setVerdict(mine.verdict);
    setProposed(mine.proposed ?? "");
    setNote(mine.note ?? "");
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase || !session || !verdict) return;
    setSaving(true);
    setError(null);
    const { error } = await supabase.from("node_reviews").upsert(
      {
        reviewer_id: session.user.id,
        reviewer_email: session.user.email,
        node_id: nodeId,
        dimension: "overall",
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

  return (
    <section className="rounded-lg border border-border bg-card p-4">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
        Review this node
      </h2>

      {authLoading ? null : !session ? (
        <p className="mt-2 text-sm text-muted-ink">
          <Link
            href={`/login?next=${encodeURIComponent(pathname)}`}
            className="text-forest"
          >
            Sign in
          </Link>{" "}
          to submit an accuracy verdict for this node.
        </p>
      ) : (
        <form onSubmit={submit} className="mt-3 space-y-3">
          <div className="flex flex-wrap gap-1.5">
            {VERDICT_VOCAB.map((v) => (
              <button
                key={v.key}
                type="button"
                onClick={() => setVerdict(v.key as Verdict)}
                title={v.description}
                className="flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium transition-colors"
                style={
                  verdict === v.key
                    ? {
                        backgroundColor: v.color,
                        borderColor: v.color,
                        color: "var(--color-paper)",
                      }
                    : { borderColor: "var(--color-border)" }
                }
              >
                <span className="mono">{v.symbol}</span>
                {v.label}
              </button>
            ))}
          </div>

          {(verdict === "edit" || verdict === "edit-major" || verdict === "edit-minor") && (
            <textarea
              value={proposed}
              onChange={(e) => setProposed(e.target.value)}
              placeholder="Proposed correction…"
              rows={2}
              className="w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
            />
          )}

          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Note (optional)…"
            rows={2}
            className="w-full rounded-md border border-border bg-paper px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
          />

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={!verdict || saving}
              className="rounded-lg bg-forest px-4 py-1.5 text-sm font-medium text-paper disabled:opacity-50"
            >
              {saving ? "Saving…" : mine ? "Update verdict" : "Submit verdict"}
            </button>
            {savedAt && !saving && (
              <span className="text-xs text-muted-ink">Saved.</span>
            )}
          </div>
          {error && <p className="text-xs text-destructive">{error}</p>}
        </form>
      )}

      {session && !loadingReviews && reviews.length > 0 && (
        <div className="mt-4 border-t border-border pt-3">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-ink">
            All verdicts ({reviews.length})
          </h3>
          <ul className="mt-2 space-y-2">
            {reviews.map((r) => {
              const v = VERDICT_VOCAB.find((x) => x.key === r.verdict);
              return (
                <li key={r.id} className="flex items-start gap-2 text-xs">
                  <span
                    className="mono flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[0.65rem] font-semibold text-white"
                    style={{ backgroundColor: v?.color }}
                  >
                    {v?.symbol}
                  </span>
                  <div>
                    <span className="font-medium">{r.reviewer_email}</span>
                    {r.note && (
                      <span className="text-muted-ink">: {r.note}</span>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </section>
  );
}

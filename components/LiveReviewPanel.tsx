"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { supabase, supabaseConfigured, type NodeReview } from "@/lib/supabase";
import { useAuth } from "@/lib/useAuth";
import { VERDICT_VOCAB } from "@/lib/ui";
import { getNodeById } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";

export default function LiveReviewPanel() {
  const { session, loading: authLoading } = useAuth();
  const [reviews, setReviews] = useState<NodeReview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // `loading` is only ever read once the JSX below already knows `session`
    // is truthy (the `!session` branch renders and returns first) — so
    // there's nothing to reset here when there's no session to fetch for.
    if (!session || !supabase) return;
    supabase
      .from("node_reviews")
      .select("*")
      .order("updated_at", { ascending: false })
      .limit(200)
      .then(({ data, error }) => {
        if (error) setError(error.message);
        else setReviews((data as NodeReview[]) ?? []);
        setLoading(false);
      });
  }, [session]);

  if (!supabaseConfigured) {
    return (
      <p className="mt-2 text-sm text-muted-ink">
        Live review backend not configured on this deployment.
      </p>
    );
  }

  if (authLoading) return null;

  if (!session) {
    return (
      <p className="mt-2 text-sm text-muted-ink">
        <Link href="/login?next=/review" className="text-forest">
          Sign in
        </Link>{" "}
        to see live review submissions.
      </p>
    );
  }

  if (loading) return <p className="mt-2 text-sm text-muted-ink">Loading…</p>;
  if (error) return <p className="mt-2 text-sm text-destructive">{error}</p>;

  const counts: Record<string, number> = {};
  for (const r of reviews) counts[r.verdict] = (counts[r.verdict] ?? 0) + 1;

  return (
    <div className="mt-4 space-y-6">
      <div className="flex flex-wrap gap-3">
        {VERDICT_VOCAB.map((v) => (
          <div
            key={v.key}
            className="flex items-center gap-2 rounded-lg border border-border bg-card px-3 py-2"
          >
            <span
              className="mono flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold text-white"
              style={{ backgroundColor: v.color }}
            >
              {v.symbol}
            </span>
            <span className="text-sm">
              <span className="mono font-semibold">{counts[v.key] ?? 0}</span>{" "}
              <span className="text-muted-ink">{v.label}</span>
            </span>
          </div>
        ))}
      </div>

      {reviews.length === 0 ? (
        <p className="text-sm text-muted-ink">No reviews submitted yet. Be the first.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="w-full min-w-[600px] border-collapse text-sm">
            <thead>
              <tr className="bg-muted-surface">
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Node
                </th>
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Verdict
                </th>
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Reviewer
                </th>
                <th className="p-3 text-left text-xs font-semibold uppercase tracking-wide text-muted-ink">
                  Note
                </th>
              </tr>
            </thead>
            <tbody>
              {reviews.map((r) => {
                const v = VERDICT_VOCAB.find((x) => x.key === r.verdict);
                const node = getNodeById(r.node_id);
                return (
                  <tr key={r.id} className="border-t border-border">
                    <td className="p-3">
                      <Link
                        href={`/nodes/${r.node_id}`}
                        className="flex items-center gap-2 hover:text-forest"
                      >
                        {node && (
                          <NodeTypeBadge type={node.type} />
                        )}
                        <span className="mono text-xs">{r.node_id}</span>
                      </Link>
                    </td>
                    <td className="p-3">
                      <span
                        className="mono inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold text-white"
                        style={{ backgroundColor: v?.color }}
                        title={v?.label}
                      >
                        {v?.symbol}
                      </span>
                    </td>
                    <td className="p-3 text-xs text-muted-ink">{r.reviewer_email}</td>
                    <td className="p-3 text-xs text-muted-ink">{r.note || "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

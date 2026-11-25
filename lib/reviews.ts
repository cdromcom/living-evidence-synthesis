import { supabase, type NodeReview } from "@/lib/supabase";

/**
 * Loads reviews through the `node_reviews_public` view. If the view has not
 * been created in this Supabase project yet (see
 * supabase/migrations/2026-11-reviews-view-only.sql), it falls back to the
 * signed-in user's own rows, which the table always allows them to read, and
 * says so with `viewMissing` instead of showing a raw database error.
 */
export async function loadReviews(opts: {
  userId: string;
  nodeId?: string;
  limit?: number;
}): Promise<{ reviews: NodeReview[]; viewMissing: boolean; error: string | null }> {
  if (!supabase) return { reviews: [], viewMissing: false, error: "Reviews are not configured." };

  let q = supabase.from("node_reviews_public").select("*").order("updated_at", { ascending: false });
  if (opts.nodeId) q = q.eq("node_id", opts.nodeId);
  if (opts.limit) q = q.limit(opts.limit);
  const { data, error } = await q;
  if (!error) return { reviews: (data as NodeReview[]) ?? [], viewMissing: false, error: null };

  const missing =
    error.code === "PGRST205" ||
    error.code === "42P01" ||
    /node_reviews_public|schema cache|does not exist/i.test(error.message);
  if (!missing) return { reviews: [], viewMissing: false, error: error.message };

  let own = supabase
    .from("node_reviews")
    .select("id,node_id,dimension,verdict,proposed,note,created_at,updated_at")
    .eq("reviewer_id", opts.userId)
    .order("updated_at", { ascending: false });
  if (opts.nodeId) own = own.eq("node_id", opts.nodeId);
  if (opts.limit) own = own.limit(opts.limit);
  const res = await own;
  if (res.error) return { reviews: [], viewMissing: true, error: null };
  const rows = (res.data ?? []).map((r) => ({ ...(r as object), reviewer_name: "You", is_mine: true }) as NodeReview);
  return { reviews: rows, viewMissing: true, error: null };
}

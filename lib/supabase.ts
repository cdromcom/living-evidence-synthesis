import { createClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabaseConfigured = Boolean(url && anonKey);

// A single browser client, safe to import from client components. When env
// vars are absent (e.g. local dev without .env.local), `supabase` is null
// and callers should fall back to a signed-out state rather than throwing.
export const supabase = supabaseConfigured
  ? createClient(url!, anonKey!, {
      auth: { persistSession: true, autoRefreshToken: true },
    })
  : null;

export type Verdict = "correct" | "edit" | "wrong" | "missing" | "na";

export type NodeReview = {
  id: string;
  reviewer_id: string;
  reviewer_email: string;
  node_id: string;
  dimension: string;
  verdict: Verdict;
  proposed: string | null;
  note: string | null;
  created_at: string;
  updated_at: string;
};

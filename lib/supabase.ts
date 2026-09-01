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

// Origin that sign-in emails should point back at.
//
// When a sign-in request sends no `emailRedirectTo`, Supabase falls back to
// the project's Site URL — a single value shared by every user, so with it set
// to http://localhost:3000 everyone got a link to their own machine. Sending
// the origin explicitly keeps each sign-in on the site it started from.
// `NEXT_PUBLIC_SITE_URL` pins that to a stable domain in production, because a
// per-deployment Vercel preview origin stops resolving on the next push (the
// same reason GITHUB_OAUTH_REDIRECT_URI wants a stable domain).
export function authRedirectOrigin(): string {
  const configured = process.env.NEXT_PUBLIC_SITE_URL?.replace(/\/+$/, "");
  if (configured) return configured;
  return typeof window === "undefined" ? "" : window.location.origin;
}

export type Verdict = "correct" | "edit" | "edit-major" | "edit-minor" | "wrong" | "missing" | "na";

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

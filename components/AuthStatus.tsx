"use client";

import Link from "next/link";
import { supabase, supabaseConfigured } from "@/lib/supabase";
import { useAuth } from "@/lib/useAuth";

export default function AuthStatus() {
  const { session, loading, email } = useAuth();

  if (!supabaseConfigured) return null;
  if (loading) return <div className="h-8 w-16" aria-hidden />;

  if (!session) {
    return (
      <Link
        href="/login"
        className="inline-flex min-h-8 shrink-0 items-center rounded-lg border border-border bg-card px-3 py-1.5 pointer-coarse:min-h-11 text-sm font-medium text-ink transition-colors hover:border-forest hover:text-forest"
      >
        Sign in
      </Link>
    );
  }

  return (
    <div className="flex shrink-0 items-center gap-2 text-sm">
      <span className="hidden max-w-[10rem] truncate text-muted-ink sm:inline">
        {email}
      </span>
      <button
        type="button"
        onClick={() => supabase?.auth.signOut()}
        className="min-h-8 rounded-lg border border-border bg-card px-3 py-1.5 pointer-coarse:min-h-11 font-medium text-ink transition-colors hover:border-forest hover:text-forest"
      >
        Sign out
      </button>
    </div>
  );
}

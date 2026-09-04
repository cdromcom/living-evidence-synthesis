"use client";

import { useEffect, useState } from "react";
import type { Session } from "@supabase/supabase-js";
import { supabase } from "./supabase";

export function useAuth() {
  const [session, setSession] = useState<Session | null>(null);
  // `supabase` is a module-level constant (see lib/supabase.ts) — whether it's
  // null is already known at first render, identically on server and client
  // (both read the same NEXT_PUBLIC_* env vars), so there's nothing to wait
  // on for that branch: no effect needed just to flip loading to false.
  const [loading, setLoading] = useState(() => Boolean(supabase));

  useEffect(() => {
    if (!supabase) return;
    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session);
      setLoading(false);
    });
    const { data: sub } = supabase.auth.onAuthStateChange((_event, s) => {
      setSession(s);
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  return { session, loading, email: session?.user.email ?? null };
}

"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { supabase, supabaseConfigured } from "@/lib/supabase";

export default function LoginPage() {
  return (
    <Suspense fallback={null}>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") || "/review";

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [stage, setStage] = useState<"email" | "code">("email");
  const [status, setStatus] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function sendCode(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase) return;
    setBusy(true);
    setStatus(null);
    const { error } = await supabase.auth.signInWithOtp({ email });
    setBusy(false);
    if (error) {
      setStatus(error.message);
      return;
    }
    setStage("code");
    setStatus(`Code sent to ${email}. Check your inbox.`);
  }

  async function verifyCode(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase) return;
    setBusy(true);
    setStatus(null);
    const { error } = await supabase.auth.verifyOtp({
      email,
      token: code,
      type: "email",
    });
    setBusy(false);
    if (error) {
      setStatus(error.message);
      return;
    }
    router.push(next);
  }

  if (!supabaseConfigured) {
    return (
      <main className="mx-auto max-w-md px-4 py-16 sm:px-6">
        <h1 className="text-2xl font-semibold">Sign in</h1>
        <p className="mt-3 text-sm text-muted-ink">
          The review backend isn&apos;t configured on this deployment yet
          (missing <code className="mono">NEXT_PUBLIC_SUPABASE_URL</code> /{" "}
          <code className="mono">NEXT_PUBLIC_SUPABASE_ANON_KEY</code>).
        </p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-md px-4 py-16 sm:px-6">
      <h1 className="text-2xl font-semibold">Sign in to review</h1>
      <p className="mt-2 text-sm text-muted-ink">
        Any email works — we&apos;ll send a one-time code, no password
        needed. Signing in lets you submit accuracy verdicts on nodes and see
        the review dashboard.
      </p>

      {stage === "email" ? (
        <form onSubmit={sendCode} className="mt-6 space-y-3">
          <label className="block text-sm font-medium" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full rounded-md border border-border bg-card px-3 py-2 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
          />
          <button
            type="submit"
            disabled={busy}
            className="rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper disabled:opacity-60"
          >
            {busy ? "Sending…" : "Send code"}
          </button>
        </form>
      ) : (
        <form onSubmit={verifyCode} className="mt-6 space-y-3">
          <label className="block text-sm font-medium" htmlFor="code">
            6-digit code
          </label>
          <input
            id="code"
            type="text"
            inputMode="numeric"
            required
            autoFocus
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="123456"
            className="mono w-full rounded-md border border-border bg-card px-3 py-2 text-lg tracking-widest text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
          />
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={busy}
              className="rounded-lg bg-forest px-4 py-2 text-sm font-medium text-paper disabled:opacity-60"
            >
              {busy ? "Verifying…" : "Verify & sign in"}
            </button>
            <button
              type="button"
              onClick={() => {
                setStage("email");
                setStatus(null);
              }}
              className="rounded-lg border border-border bg-card px-4 py-2 text-sm font-medium text-ink"
            >
              Use a different email
            </button>
          </div>
        </form>
      )}

      {status && (
        <p className="mt-4 rounded-md border border-border bg-muted-surface p-3 text-sm text-muted-ink">
          {status}
        </p>
      )}
    </main>
  );
}

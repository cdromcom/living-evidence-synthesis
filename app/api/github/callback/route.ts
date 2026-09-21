import { NextResponse } from "next/server";
import { exchangeCodeForToken } from "@/lib/github";

/**
 * Where to send the visitor after the token exchange. The `next` cookie is
 * set from a query parameter on /api/github/login, so it is attacker-supplied:
 * without this check, `?next=https://example.com` resolves to that origin and
 * carries the visitor straight off the site the moment they sign in. Only a
 * same-site path is honoured — a leading `//` (or `/\`) is a protocol-relative
 * URL to somewhere else, so it is rejected too.
 */
function sameSitePath(raw: string | undefined): string {
  const fallback = "/contribute";
  if (!raw) return fallback;
  let decoded: string;
  try {
    decoded = decodeURIComponent(raw);
  } catch {
    return fallback;
  }
  if (!decoded.startsWith("/")) return fallback;
  if (/^\/[/\\]/.test(decoded)) return fallback;
  return decoded;
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const expectedState = request.headers
    .get("cookie")
    ?.match(/gh_oauth_state=([^;]+)/)?.[1];
  const next = sameSitePath(
    request.headers.get("cookie")?.match(/gh_oauth_next=([^;]+)/)?.[1]
  );

  if (!code || !state || state !== expectedState) {
    return NextResponse.redirect(new URL("/contribute?error=oauth_state", request.url));
  }

  try {
    const token = await exchangeCodeForToken(code);
    const res = NextResponse.redirect(new URL(next, request.url));
    res.cookies.set("gh_token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 30,
      path: "/",
    });
    res.cookies.delete("gh_oauth_state");
    res.cookies.delete("gh_oauth_next");
    return res;
  } catch {
    return NextResponse.redirect(new URL("/contribute?error=oauth_exchange", request.url));
  }
}

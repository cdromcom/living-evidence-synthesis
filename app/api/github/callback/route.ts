import { NextResponse } from "next/server";
import { exchangeCodeForToken } from "@/lib/github";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const expectedState = request.headers
    .get("cookie")
    ?.match(/gh_oauth_state=([^;]+)/)?.[1];
  const next =
    request.headers.get("cookie")?.match(/gh_oauth_next=([^;]+)/)?.[1] ||
    "/contribute";

  if (!code || !state || state !== expectedState) {
    return NextResponse.redirect(new URL("/contribute?error=oauth_state", request.url));
  }

  try {
    const token = await exchangeCodeForToken(code);
    const res = NextResponse.redirect(new URL(decodeURIComponent(next), request.url));
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

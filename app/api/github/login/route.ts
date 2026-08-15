import { NextResponse } from "next/server";
import { randomBytes } from "node:crypto";
import { githubAuthorizeUrl } from "@/lib/github";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const next = url.searchParams.get("next") || "/contribute";
  const state = randomBytes(16).toString("hex");

  const res = NextResponse.redirect(githubAuthorizeUrl(state));
  res.cookies.set("gh_oauth_state", state, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 600,
    path: "/",
  });
  res.cookies.set("gh_oauth_next", next, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 600,
    path: "/",
  });
  return res;
}

import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const res = NextResponse.json({ ok: true });
  res.cookies.delete("gh_token");
  return res;
}

export async function GET(request: Request) {
  const res = NextResponse.redirect(new URL("/contribute", request.url));
  res.cookies.delete("gh_token");
  return res;
}

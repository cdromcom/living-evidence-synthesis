import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { getViewer } from "@/lib/github";

export async function GET() {
  const token = (await cookies()).get("gh_token")?.value;
  if (!token) return NextResponse.json({ signedIn: false });
  try {
    const viewer = await getViewer(token);
    return NextResponse.json({ signedIn: true, login: viewer.login, avatarUrl: viewer.avatar_url });
  } catch {
    return NextResponse.json({ signedIn: false });
  }
}

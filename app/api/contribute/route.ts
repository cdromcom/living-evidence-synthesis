import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import {
  getViewer,
  ensureFork,
  getBaseBranchSha,
  createBranch,
  putFile,
  getBaseFileContent,
  compareUrl,
} from "@/lib/github";
import { buildContributionFiles, CONTRIBUTION_TYPES, type ContributionInput } from "@/lib/node-markdown";

// Best-effort per-user rate limit. In-memory, so it is per server instance (on
// serverless it resets on cold start); it stops a single signed-in user from
// hammering the GitHub API and spraying branches, which is the realistic abuse.
const RATE_WINDOW_MS = 60 * 60 * 1000;
const RATE_MAX = 5;
const recent = new Map<string, number[]>();

function rateLimited(user: string): boolean {
  const now = Date.now();
  const hits = (recent.get(user) ?? []).filter((t) => now - t < RATE_WINDOW_MS);
  if (hits.length >= RATE_MAX) {
    recent.set(user, hits);
    return true;
  }
  hits.push(now);
  recent.set(user, hits);
  return false;
}

const MAX_QUOTE = 1500;

export async function POST(request: Request) {
  const token = (await cookies()).get("gh_token")?.value;
  if (!token) {
    return NextResponse.json({ error: "Not signed in with GitHub" }, { status: 401 });
  }

  let input: ContributionInput;
  try {
    input = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid request body" }, { status: 400 });
  }

  // `type` ends up in a git branch name, so only accept known node types.
  if (!CONTRIBUTION_TYPES.includes(input.type)) {
    return NextResponse.json({ error: "Unknown node type" }, { status: 400 });
  }
  if (!input.title?.trim() || !input.body?.trim()) {
    return NextResponse.json({ error: "Type, title, and body are required" }, { status: 400 });
  }
  const wordCount = input.body.trim().split(/\s+/).length;
  if (wordCount < 50 || wordCount > 250) {
    return NextResponse.json(
      { error: `Body must be 50-250 words (got ${wordCount})` },
      { status: 400 }
    );
  }

  if (input.type === "EVD" || input.type === "CVT") {
    const page = (input.page ?? "").trim();
    if (!input.quote?.trim() || !page) {
      return NextResponse.json(
        { error: "Evidence and Caveats need a verbatim quote and the printed journal page number" },
        { status: 400 }
      );
    }
    if (!/^[A-Za-z]{0,3}\d{1,5}([\u2013-]\d{1,5})?$/.test(page)) {
      return NextResponse.json({ error: "Page must be a printed page number such as 5 or 5-6" }, { status: 400 });
    }
  }
  for (const [k, max] of [["quote", MAX_QUOTE], ["citation", 200], ["figureRef", 120], ["screenshot", 200]] as const) {
    if ((input[k] ?? "").length > max) {
      return NextResponse.json({ error: `${k} is too long` }, { status: 400 });
    }
  }
  if (input.screenshot && !/^[\w.-]+\.(png|jpe?g|webp)$/i.test(input.screenshot.trim())) {
    return NextResponse.json({ error: "Screenshot must be an image filename such as smith2026-evd-p5-1.png" }, { status: 400 });
  }

  try {
    const viewer = await getViewer(token);
    if (rateLimited(viewer.login)) {
      return NextResponse.json({ error: "Too many submissions; try again in an hour" }, { status: 429 });
    }
    await ensureFork(token, viewer.login);

    const baseSha = await getBaseBranchSha(token);
    const branch = `contribute/${input.type.toLowerCase()}-${Date.now()}`;
    await createBranch(token, viewer.login, branch, baseSha);

    const { newFile, patches } = buildContributionFiles(input);
    await putFile(
      token,
      viewer.login,
      branch,
      newFile.path,
      newFile.content,
      `Add ${input.type}: ${input.title.slice(0, 60)}`
    );

    for (const patch of patches) {
      const current = await getBaseFileContent(token, patch.path);
      if (current === null) continue; // target file not found; skip silently, reviewer can wire it manually
      const updated = patch.append(current);
      await putFile(token, viewer.login, branch, patch.path, updated, `Link new ${input.type} into ${patch.path}`);
    }

    return NextResponse.json({ compareUrl: compareUrl(viewer.login, branch) });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

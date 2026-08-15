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
import { buildContributionFiles, type ContributionInput } from "@/lib/node-markdown";

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

  if (!input.type || !input.title?.trim() || !input.body?.trim()) {
    return NextResponse.json({ error: "Type, title, and body are required" }, { status: 400 });
  }
  const wordCount = input.body.trim().split(/\s+/).length;
  if (wordCount < 50 || wordCount > 250) {
    return NextResponse.json(
      { error: `Body must be 50-250 words (got ${wordCount})` },
      { status: 400 }
    );
  }

  try {
    const viewer = await getViewer(token);
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

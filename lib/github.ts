// Server-only helpers for the GitHub OAuth "Contribute" flow: sign in with
// GitHub, fork this repo into the contributor's account, commit a new node
// file on a branch, and hand them a link to open the PR themselves.
import "server-only";

const API = "https://api.github.com";
const OWNER = process.env.GITHUB_REPO_OWNER!;
const REPO = process.env.GITHUB_REPO_NAME!;
const BASE_BRANCH = process.env.GITHUB_REPO_BASE_BRANCH || "main";

export function githubAuthorizeUrl(state: string) {
  const params = new URLSearchParams({
    client_id: process.env.GITHUB_CLIENT_ID!,
    redirect_uri: process.env.GITHUB_OAUTH_REDIRECT_URI!,
    scope: "public_repo",
    state,
  });
  return `https://github.com/login/oauth/authorize?${params.toString()}`;
}

export async function exchangeCodeForToken(code: string): Promise<string> {
  const res = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: process.env.GITHUB_CLIENT_ID,
      client_secret: process.env.GITHUB_CLIENT_SECRET,
      redirect_uri: process.env.GITHUB_OAUTH_REDIRECT_URI,
      code,
    }),
  });
  const data = await res.json();
  if (!data.access_token) {
    throw new Error(data.error_description || "GitHub token exchange failed");
  }
  return data.access_token as string;
}

function gh(token: string, path: string, init: RequestInit = {}) {
  return fetch(`${API}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      ...(init.headers || {}),
    },
  });
}

export async function getViewer(token: string) {
  const res = await gh(token, "/user");
  if (!res.ok) throw new Error("Could not read GitHub user");
  return (await res.json()) as { login: string; avatar_url: string };
}

/** Fork the repo into the viewer's account if not already forked; wait until it's ready. */
export async function ensureFork(token: string, viewerLogin: string) {
  const existing = await gh(token, `/repos/${viewerLogin}/${REPO}`);
  if (existing.ok) return;

  const forkRes = await gh(token, `/repos/${OWNER}/${REPO}/forks`, { method: "POST" });
  if (!forkRes.ok) throw new Error("Could not fork repository");

  // Forking is async on GitHub's side; poll until the fork is queryable.
  for (let i = 0; i < 10; i++) {
    await new Promise((r) => setTimeout(r, 1500));
    const check = await gh(token, `/repos/${viewerLogin}/${REPO}`);
    if (check.ok) return;
  }
  throw new Error("Fork did not become ready in time; try again in a moment");
}

export async function getBaseBranchSha(token: string): Promise<string> {
  const res = await gh(token, `/repos/${OWNER}/${REPO}/git/ref/heads/${BASE_BRANCH}`);
  if (!res.ok) throw new Error("Could not read base branch");
  const data = await res.json();
  return data.object.sha as string;
}

export async function createBranch(token: string, viewerLogin: string, branch: string, sha: string) {
  const res = await gh(token, `/repos/${viewerLogin}/${REPO}/git/refs`, {
    method: "POST",
    body: JSON.stringify({ ref: `refs/heads/${branch}`, sha }),
  });
  if (!res.ok && res.status !== 422) {
    // 422 = ref already exists, fine to proceed (retry submissions)
    throw new Error("Could not create branch on fork");
  }
}

/** Create or update a file on a branch. Looks up the current sha first if it exists (update case). */
export async function putFile(
  token: string,
  viewerLogin: string,
  branch: string,
  filePath: string,
  content: string,
  message: string
) {
  const encoded = encodeURIComponent(filePath).replace(/%2F/g, "/");
  let sha: string | undefined;
  const existing = await gh(
    token,
    `/repos/${viewerLogin}/${REPO}/contents/${encoded}?ref=${branch}`
  );
  if (existing.ok) {
    const data = await existing.json();
    sha = data.sha;
  }

  const res = await gh(token, `/repos/${viewerLogin}/${REPO}/contents/${encoded}`, {
    method: "PUT",
    body: JSON.stringify({
      message,
      content: Buffer.from(content, "utf8").toString("base64"),
      branch,
      ...(sha ? { sha } : {}),
    }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Could not write ${filePath}: ${err.slice(0, 300)}`);
  }
}

/** Read a file's current raw content from the BASE repo (not the fork), for patching (e.g. a Question that needs a new Claim appended). */
export async function getBaseFileContent(token: string, filePath: string): Promise<string | null> {
  const encoded = encodeURIComponent(filePath).replace(/%2F/g, "/");
  const res = await gh(token, `/repos/${OWNER}/${REPO}/contents/${encoded}?ref=${BASE_BRANCH}`);
  if (!res.ok) return null;
  const data = await res.json();
  return Buffer.from(data.content, "base64").toString("utf8");
}

export function compareUrl(viewerLogin: string, branch: string) {
  return `https://github.com/${OWNER}/${REPO}/compare/${BASE_BRANCH}...${viewerLogin}:${REPO}:${branch}?expand=1`;
}

export { OWNER, REPO, BASE_BRANCH };

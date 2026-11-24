import fs from "node:fs";
import path from "node:path";
import Link from "next/link";
import { renderMarkdown } from "@/lib/markdown";
import NodeArticle from "@/components/NodeArticle";

export const metadata = {
  title: "Data pipeline — Living Evidence Synthesis",
  description:
    "How papers become nodes: extraction, curation, review and publication of the evidence graph.",
};

/** The Welcome.md section from its "## 🛠️" heading up to the next "## " heading. */
function loadPipelineSection(): { title: string; body: string } | null {
  try {
    const md = fs
      .readFileSync(path.join(process.cwd(), "vault", "Welcome.md"), "utf8")
      .replace(/\r\n/g, "\n");
    const lines = md.split("\n");
    const start = lines.findIndex((l) => l.startsWith("## 🛠️"));
    if (start === -1) return null;
    let end = lines.findIndex((l, i) => i > start && l.startsWith("## "));
    if (end === -1) end = lines.length;
    const body = lines.slice(start + 1, end).join("\n").trim();
    if (!body) return null;
    return { title: lines[start].replace(/^##\s+/, "").replace(/^🛠️\s*/, ""), body };
  } catch {
    return null;
  }
}

export default function PipelinePage() {
  const section = loadPipelineSection();
  return (
    <main id="main-content" tabIndex={-1} className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">
        {section?.title ?? "The data pipeline"}
      </h1>
      {section ? (
        <div className="mt-6">
          <NodeArticle html={renderMarkdown(section.body).html} />
        </div>
      ) : (
        <p className="mt-6 text-sm text-muted-ink">
          The pipeline description is not available in this build of the
          site. See the{" "}
          <Link href="/about" className="text-forest">
            About page
          </Link>{" "}
          for the method.
        </p>
      )}
    </main>
  );
}

import { Suspense } from "react";
import { getAllNodes } from "@/lib/data";
import NodesExplorer from "@/components/NodesExplorer";

export const metadata = { title: "Nodes — Living Evidence Synthesis" };

export default function NodesPage() {
  const nodes = getAllNodes();
  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">All nodes</h1>
      <p className="mt-1 max-w-[65ch] text-sm text-muted-ink">
        Every Question, Claim, Evidence, Caveat, Source, and Evidence Pattern
        node in the corpus. Search, filter by type or curation status, and
        sort.
      </p>
      <div className="mt-6">
        <Suspense>
          <NodesExplorer nodes={nodes} />
        </Suspense>
      </div>
    </main>
  );
}

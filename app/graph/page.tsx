import { ALL_EDGES, ALL_NODES } from "@/lib/data";
import GraphExplorer from "@/components/GraphExplorer";

export const metadata = { title: "Graph — Living Evidence Synthesis" };

export default function GraphPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">Discourse graph</h1>
      <p className="mt-1 max-w-[65ch] text-sm text-muted-ink">
        Every node and edge in the corpus, force-directed. Filter by node
        type or curation status, then click any node to open its page.
      </p>
      <div className="mt-6">
        <GraphExplorer nodes={ALL_NODES} edges={ALL_EDGES} />
      </div>
    </main>
  );
}

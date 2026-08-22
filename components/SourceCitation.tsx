import { formatApaCitation } from "@/lib/apa";
import type { GraphNode } from "@/lib/data";

/** A full APA 7th-edition citation, shown at the top of each source page. Open-peer-review status now lives in SourceCredibility's central box. */
export default function SourceCitation({ node }: { node: GraphNode }) {
  const citation = formatApaCitation(node);

  if (!citation.hasData) return null;

  return (
    <div className="mb-4 mt-2">
      <p className="text-sm leading-relaxed text-ink/90">
        {citation.authors} ({citation.year}). {citation.title}.{" "}
        {citation.container && (
          <>
            <em>{citation.container}</em>
            {citation.volumeIssue && <em>, {citation.volumeIssue}</em>}
            {citation.pages && <>, {citation.pages}</>}.{" "}
          </>
        )}
        {citation.url && (
          <a href={citation.url} target="_blank" rel="noopener noreferrer" className="text-forest hover:underline">
            {citation.url}
          </a>
        )}
      </p>
    </div>
  );
}

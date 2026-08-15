import Link from "next/link";
import { getBestSupportedClaims, getCounts } from "@/lib/data";
import NodeTypeBadge from "@/components/NodeTypeBadge";

export default function HomePage() {
  const counts = getCounts();
  const bestSupported = getBestSupportedClaims(6);

  const statTiles: { type: keyof typeof counts; description: string }[] = [
    { type: "QUE", description: "Open questions the corpus addresses" },
    { type: "CLM", description: "Generalizations across evidence" },
    { type: "EVD", description: "Single-source observations" },
    { type: "CVT", description: "Caveats qualifying evidence" },
    { type: "SRC", description: "Source papers reviewed" },
    { type: "EP", description: "Cross-paper evidence patterns" },
  ];

  return (
    <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
      <section className="max-w-3xl">
        <p className="mono mb-3 text-xs uppercase tracking-wide text-muted-ink">
          Living evidence synthesis
        </p>
        <h1 className="text-3xl font-semibold leading-tight sm:text-4xl">
          Can LLMs be used for peer review and evidence appraisal of
          scientific literature?
        </h1>
        <p className="mt-5 max-w-[65ch] text-[1.05rem] leading-relaxed text-ink/90">
          This site renders a discourse graph: Questions, Claims, Evidence,
          Caveats, Sources, and cross-paper Evidence Patterns, extracted from
          a curated Obsidian vault surveying the literature on LLM-assisted
          peer review, risk-of-bias assessment, novelty evaluation, and
          related evidence-appraisal tasks. The extraction methodology
          (node types, verbatim-grounding rules, review verdict vocabulary,
          and the propose-then-commit human-AI workflow) follows the{" "}
          <a
            className="text-forest"
            href="https://github.com/oasisresearchlab/language-and-health-open-synthesis/blob/review-app-prototype/discourse-extraction/node-spec.md"
            target="_blank"
            rel="noreferrer"
          >
            discourse-extraction node spec
          </a>{" "}
          from the oasisresearchlab language-and-health-open-synthesis
          project; this corpus applies it to a new topic (LLMs for scientific
          peer review) and adds a sixth node type, Evidence Patterns, for
          findings that recur across independent papers.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            href="/graph"
            className="rounded-md bg-forest px-4 py-2 text-sm font-medium text-paper transition-opacity hover:opacity-90"
          >
            Explore the graph
          </Link>
          <Link
            href="/nodes"
            className="rounded-md border border-border px-4 py-2 text-sm font-medium hover:bg-muted-surface"
          >
            Browse all nodes
          </Link>
        </div>
      </section>

      <section className="mt-14">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
          Corpus at a glance
        </h2>
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {statTiles.map(({ type, description }) => (
            <Link
              key={type}
              href={`/nodes?type=${type}`}
              className="rounded-lg border border-border bg-card p-4 transition-colors hover:border-forest/40"
            >
              <div className="mb-2">
                <NodeTypeBadge type={type} />
              </div>
              <div className="mono text-2xl font-semibold">{counts[type]}</div>
              <div className="mt-1 text-xs text-muted-ink">{description}</div>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-14">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-ink">
          Best-supported claims
        </h2>
        <p className="mt-1 text-sm text-muted-ink">
          Ranked by number of distinct Evidence nodes citing support.
        </p>
        <ol className="mt-4 space-y-3">
          {bestSupported.map(({ node, supportCount }, idx) => (
            <li key={node.id}>
              <Link
                href={`/nodes/${node.id}`}
                className="flex items-start gap-4 rounded-lg border border-border bg-card p-4 transition-colors hover:border-forest/40"
              >
                <span className="mono w-6 shrink-0 pt-0.5 text-right text-muted-ink">
                  {idx + 1}
                </span>
                <div className="min-w-0 flex-1">
                  <div className="mb-1 flex items-center gap-2">
                    <NodeTypeBadge type={node.type} />
                    <span className="mono text-xs text-muted-ink">
                      {node.id}
                    </span>
                  </div>
                  <p className="text-sm leading-snug">{node.title}</p>
                </div>
                <div className="mono shrink-0 rounded-full bg-accent-wash px-2.5 py-1 text-xs font-semibold text-forest">
                  {supportCount} EVD
                </div>
              </Link>
            </li>
          ))}
        </ol>
      </section>

      <section className="mt-14 grid gap-3 sm:grid-cols-3">
        {[
          {
            href: "/narratives",
            title: "Narratives",
            body: "Hand-composed essays reading through the strongest findings, citing directly into the graph.",
          },
          {
            href: "/review",
            title: "Review status",
            body: "Curation-status breakdown per node type and the ✓ ✎ ✗ ⟳ — verdict vocabulary.",
          },
          {
            href: "/about",
            title: "About the method",
            body: "How discourse nodes are extracted, and how human-AI teaming curates them.",
          },
        ].map((c) => (
          <Link
            key={c.href}
            href={c.href}
            className="rounded-lg border border-border bg-card p-5 transition-colors hover:border-forest/40"
          >
            <h3 className="text-base font-semibold">{c.title}</h3>
            <p className="mt-1.5 text-sm text-muted-ink">{c.body}</p>
          </Link>
        ))}
      </section>
    </main>
  );
}

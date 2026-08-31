import Link from "next/link";
import { NODE_TYPE_ORDER, getCounts } from "@/lib/data";
import NodeTypeBadge from "@/components/NodeTypeBadge";

export const metadata = { title: "About — Living Evidence Synthesis" };

const TYPE_DESCRIPTIONS: Record<string, string> = {
  QUE: "The unknown a body of work addresses. Claims “address” a question; a question can have many competing or complementary claims answering it.",
  CLM: "A generalization across evidence, stated in the present tense, that transcends any single source. Linked to supporting (and, where present, opposing) Evidence with correct polarity.",
  EVD: "One specific observation from one source, stated in the past tense and grounded in a verbatim span plus a locator (typically a page number). The atomic unit of the graph.",
  CVT: "A caveat that qualifies a specific piece of Evidence, not a Claim. Caveats are either author-stated (the source paper names the limitation itself) or inferred (a reviewer identified it).",
  SRC: "A source paper. Every Evidence node derives from exactly one Source; Source pages aggregate structured abstracts and critical appraisals across their own Evidence/Claims/Caveats.",
  EP: "Evidence Pattern: an extension beyond the original five-type schema, added for this corpus. A cross-paper aggregation that names which independent papers instantiate a recurring finding and states a mechanism, distinct from a Claim in that it explicitly enumerates its instantiating Evidence.",
};

export default function AboutPage() {
  const counts = getCounts();
  return (
    <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">About this corpus</h1>

      <section className="prose-node mt-6">
        <p>
          This site renders a discourse graph on the question of whether
          large language models can be used for peer review and evidence
          appraisal of scientific literature: risk-of-bias assessment,
          reporting-guideline compliance, novelty evaluation, citation
          integrity, IRB/ethics review, and related tasks. The graph was
          extracted from a curated Obsidian vault: an analyst read the
          underlying papers, an AI agent proposed discourse nodes, and a
          human curator reviewed and promoted them.
        </p>

        <h2>The node-spec method</h2>
        <p>
          Node types, extraction rules, and terminology follow the{" "}
          <a
            href="https://github.com/oasisresearchlab/language-and-health-open-synthesis/blob/review-app-prototype/discourse-extraction/node-spec.md"
            target="_blank"
            rel="noreferrer"
          >
            discourse-extraction node spec
          </a>{" "}
          from the oasisresearchlab <code>language-and-health-open-synthesis</code>{" "}
          project (branch <code>review-app-prototype</code>). That project defines
          five core node types (Question, Claim, Evidence, Caveat, Source),
          plus conventions for verbatim grounding, methods-context facets
          (What / How / Who) on every Evidence node, and a review-verdict
          vocabulary. This corpus applies that method to a new topic and adds
          a sixth type, Evidence Pattern, for findings that recur across
          independent papers with a stated mechanism.
        </p>

        <h2>Node types in this corpus</h2>
      </section>

      <ul className="mt-4 space-y-3">
        {NODE_TYPE_ORDER.map((t) => (
          <li
            key={t}
            className="rounded-lg border border-border bg-card p-4"
          >
            <div className="mb-1.5 flex items-center gap-2">
              <NodeTypeBadge type={t} />
              <span className="mono text-xs text-muted-ink">
                {counts[t]} nodes
              </span>
            </div>
            <p className="text-sm text-ink/90">{TYPE_DESCRIPTIONS[t]}</p>
          </li>
        ))}
      </ul>

      <section className="prose-node mt-10">
        <h2>Curation status and human-AI teaming</h2>
        <p>
          Every node carries a <code>NodeFormality</code> field tracking where
          it sits in a propose-then-commit workflow: an AI agent extracts and
          drafts a node (<strong>Initial AI draft</strong>), and a human
          reviewer checks it against the source and promotes it
          (<strong>Reviewed</strong>). Nothing in this corpus is committed
          without that human step; the AI proposes, it never auto-commits.
          See the{" "}
          <Link href="/review" className="text-forest">
            review dashboard
          </Link>{" "}
          for the current status breakdown and the review-verdict vocabulary
          (✓ correct · ✎ edit, further split into major/minor issues · ✗ wrong
          · ⟳ missing · — n/a) the spec uses for field-level review.
        </p>
        <h2>Edges</h2>
        <p>
          Edges are derived from Obsidian wikilinks in each node&apos;s body.
          For example, a Claim&apos;s &quot;Supporting Evidence&quot; section becomes{" "}
          <code>EVD → supports → CLM</code> edges, an Evidence node&apos;s
          &quot;Caveats&quot; section becomes <code>CVT → qualifies → EVD</code>,
          and so on. Source pages additionally get a lower-priority{" "}
          <code>mentions</code> edge to any node they link to inline that
          isn&apos;t already connected by a typed edge. See the{" "}
          <Link href="/graph" className="text-forest">
            graph view
          </Link>{" "}
          for the full network.
        </p>
        <h2>What this site is not</h2>
        <p>
          The corpus itself is a static, read-only rendering of a vault
          export: nothing here is edited in place. The{" "}
          <Link href="/contribute" className="text-forest">
            Contribute
          </Link>{" "}
          page does use GitHub OAuth to open a real pull request against a
          fork of the source vault, but it doesn&apos;t write to this site or
          merge anything automatically: a human curator still has to review
          and promote the draft before it counts as part of the corpus. This
          site also makes no LLM API calls of its own: node drafting happens
          offline in the discourse-extraction pipeline, before a PR ever
          reaches here.
        </p>
      </section>

      <p className="mt-10 border-t border-border pt-4 text-xs leading-relaxed text-muted-ink">
        Extraction &amp; synthesis via Claude Code
        <br />
        Method adapted from{" "}
        <a
          href="https://github.com/oasisresearchlab/language-and-health-open-synthesis"
          target="_blank"
          rel="noopener noreferrer"
          className="transition-colors hover:text-ink"
        >
          OASIS Research Lab
        </a>
        &apos;s discourse-extraction spec
        <br />
        Live, sign-in-gated review layer for accuracy checks (Supabase).
      </p>
    </main>
  );
}

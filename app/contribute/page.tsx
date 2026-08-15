export const metadata = { title: "Contribute — Living Evidence Synthesis" };

const STEPS = [
  {
    title: "Extract",
    body: (
      <>
        Read the source paper and draft the node following the{" "}
        <a
          href="https://github.com/oasisresearchlab/language-and-health-open-synthesis/blob/review-app-prototype/discourse-extraction/node-spec.md"
          target="_blank"
          rel="noreferrer"
          className="text-forest"
        >
          discourse-extraction node spec
        </a>
        : Evidence must be grounded in a verbatim quote plus a locator (page
        number); Claims must generalize across evidence rather than restate a
        single source, in the present tense, with correct support/oppose
        polarity; Caveats attach to a specific Evidence node, not a Claim.
      </>
    ),
  },
  {
    title: "File it correctly",
    body: (
      <>
        Each node type lives in its own vault folder (<code>questions/</code>
        , <code>claims/</code>, <code>evidence/</code>, <code>caveats/</code>,{" "}
        <code>source/</code>, <code>evd-patterns/</code>) with a{" "}
        <code>PREFIX - Title.md</code> filename and YAML frontmatter including{" "}
        <code>NodeFormality: draft</code> to mark it as an unreviewed AI
        proposal.
      </>
    ),
  },
  {
    title: "Link it",
    body: (
      <>
        Wire the node into the graph with Obsidian <code>[[wikilinks]]</code>{" "}
        in the appropriate section (e.g. a Claim&apos;s &quot;Supporting
        Evidence&quot; heading, an Evidence node&apos;s &quot;Caveats&quot;
        heading). This is what this site&apos;s build step parses into typed
        edges.
      </>
    ),
  },
  {
    title: "Human review",
    body: (
      <>
        A human curator checks the draft against the source and, once
        satisfied, promotes <code>NodeFormality</code> to{" "}
        <code>ReadyForInternal</code>. This propose-then-commit step is
        required; nothing is treated as reviewed until a human has made that
        call. (For accuracy checks on already-published nodes, use the live{" "}
        <a href="/review" className="text-forest">
          review
        </a>{" "}
        layer instead. Sign in and leave a verdict on any node&apos;s page.)
      </>
    ),
  },
  {
    title: "Rebuild",
    body: (
      <>
        Re-run this site&apos;s parser (
        <code>node scripts/build-graph.mjs</code>) against the updated vault
        to regenerate the graph data and pick up the new node and its edges.
      </>
    ),
  },
];

export default function ContributePage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
      <header className="space-y-4">
        <h1 className="text-balance font-heading text-3xl font-semibold tracking-tight sm:text-4xl">
          Add a node to the graph
        </h1>
        <p className="max-w-[65ch] text-muted-ink">
          This site is a static, read-only rendering of a vault export; it
          has no GitHub sign-in and no in-browser pull-request form. New
          nodes are added directly to the source Obsidian vault, following the
          same conventions this whole corpus was built with.
        </p>
      </header>

      <hr className="my-10 border-border" />

      <ol className="space-y-6">
        {STEPS.map((step, i) => (
          <li key={step.title} className="flex gap-4">
            <span className="mono flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-accent-wash text-xs font-semibold text-forest">
              {i + 1}
            </span>
            <div>
              <h2 className="text-sm font-semibold text-ink">{step.title}</h2>
              <p className="mt-1 max-w-[65ch] text-sm text-muted-ink">
                {step.body}
              </p>
            </div>
          </li>
        ))}
      </ol>

      <hr className="my-10 border-border" />

      <p className="max-w-[65ch] text-sm text-muted-ink">
        For the full spec (verbatim-grounding rules, the methods-context
        What/How/Who facets required on every Evidence node, and the
        review-verdict vocabulary), see the{" "}
        <a
          href="https://github.com/oasisresearchlab/language-and-health-open-synthesis/tree/review-app-prototype"
          target="_blank"
          rel="noreferrer"
          className="text-forest"
        >
          oasisresearchlab/language-and-health-open-synthesis
        </a>{" "}
        repository, branch <code>review-app-prototype</code>.
      </p>
    </div>
  );
}

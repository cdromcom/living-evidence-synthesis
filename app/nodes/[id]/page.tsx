import { notFound } from "next/navigation";
import {
  ALL_NODES,
  getInboundEdges,
  getNodeById,
  getOutboundEdges,
  getReportingCompliance,
} from "@/lib/data";
import { renderMarkdown } from "@/lib/markdown";
import NodeTypeBadge from "@/components/NodeTypeBadge";
import StatusBadge from "@/components/StatusBadge";
import EdgeGroups from "@/components/EdgeGroup";
import ReviewWidget from "@/components/ReviewWidget";
import NodeArticle from "@/components/NodeArticle";
import SourceToc from "@/components/SourceToc";
import TopBadges from "@/components/TopBadges";
import SourceCredibility from "@/components/SourceCredibility";
import SourceCitation from "@/components/SourceCitation";
import ClaimTruthValue from "@/components/ClaimTruthValue";
import CaveatMeta from "@/components/CaveatMeta";

export function generateStaticParams() {
  return ALL_NODES.map((n) => ({ id: n.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const node = getNodeById(id);
  if (!node) return { title: "Node not found" };
  const titleText =
    node.type === "SRC" && typeof node.extras.apaTitle === "string" && node.extras.apaTitle
      ? (node.extras.apaTitle as string)
      : node.title;
  return { title: `${node.id} — ${titleText}` };
}

const EXTRA_LABELS: Record<string, string> = {
  rating: "Rating",
};

function formatDate(d: string | null) {
  if (!d) return null;
  try {
    return new Date(d).toISOString().slice(0, 10);
  } catch {
    return d;
  }
}

export default async function NodeDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const node = getNodeById(id);
  if (!node) notFound();

  const inbound = getInboundEdges(node.id);
  const outbound = getOutboundEdges(node.id);
  const { html, toc } = renderMarkdown(node.bodyMarkdown);
  const HANDLED_EXTRA_KEYS = new Set([
    "doi",
    "sourceUrl",
    "critiqueStatus",
    "critiqueNote",
    "authors",
    "authorTrackRecord",
    "authorTrackRecordChecked",
    "authorTrackRecordNote",
    "pubType",
    "selfCitationRate",
    "selfCitationChecked",
    "doajListed",
    "citationCount",
    "citationCountSource",
    "predatoryPublisherFlag",
    "predatoryPublisherNote",
    "pubpeerCommentCount",
    "pubpeerUrl",
    "crossNodeChecked",
    "crossNodeCorroborated",
    "nameConsistency",
    "nameConsistencyNote",
    "apaTitle",
    "apaContainer",
    "apaYear",
    "apaVolume",
    "apaIssue",
    "apaPages",
    "apaArticleNumber",
    "apaLandingUrl",
    "apaAuthors",
    "peerReviewStatus",
    "peerReviewNote",
    "peerReviewUrl",
    "citekey",
    "truthValue",
    "caveatType",
    "severity",
    "rating",
    "curatedWithModel",
    "curatedWithModelDate",
    "appraisalOverall",
    "tripodLlmPct",
  ]);
  // SRC nodes are filed under their citekey ("@louAAAR10AssessingAIs2025")
  // so coding agents and the maintainer can find them by exact match — that's
  // useful in the vault, but it's not a title. Show the real paper title
  // (already used by SourceCitation's APA line) to actual page viewers instead.
  const displayTitle =
    node.type === "SRC" && typeof node.extras.apaTitle === "string" && node.extras.apaTitle
      ? (node.extras.apaTitle as string)
      : node.title;
  const truthValue = node.extras.truthValue as number | undefined;
  const caveatSeverity = node.extras.severity as "low" | "moderate" | "high" | undefined;
  const caveatType = node.extras.caveatType as "author-stated" | "inferred" | undefined;
  const rating = node.extras.rating as number | undefined;
  const extraEntries = Object.entries(node.extras).filter(
    ([k, v]) => v !== undefined && v !== null && v !== "" && !HANDLED_EXTRA_KEYS.has(k)
  );
  const hasCritiqueStatus = Boolean(node.extras.critiqueStatus);
  const hasTripodCompliance = Boolean(getReportingCompliance(node.id));
  const curatedWithModel = node.extras.curatedWithModel as string | undefined;
  const curatedWithModelDate = node.extras.curatedWithModelDate as string | undefined;
  const hasReferences = Boolean(hasCritiqueStatus || hasTripodCompliance || curatedWithModel);
  const hasDates = Boolean(node.created || node.updated);
  const showFooter = hasReferences || hasDates;
  const tocItems = hasReferences ? [...toc, { id: "references", level: 2 as const, text: "References" }] : toc;

  return (
    <main className="py-10">
      {/* Hero section and the footer below both use Header.tsx's own
          container (mx-auto max-w-6xl px-4 sm:px-6) exactly, so the title
          and the References heading line up with the turtle-icon logo
          above. The TOC/article/aside grid is wider (max-w-[1560px]) to fit
          the TOC and aside columns, but 1560 = 1152 (6xl) + 2 * 204
          (TOC's 180px + the 24px gap before the article) is chosen so the
          *article* column — not the grid container itself — lines up with
          that same left edge once the viewport is wide enough for both
          containers to sit at their full max-width. */}
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <NodeTypeBadge type={node.type} id={node.id} />
        <StatusBadge status={node.curationStatus} />
        {typeof rating === "number" && (
          <span
            title="Curator-assigned rating"
            className="inline-flex items-center rounded-full border border-border px-2 py-0.5 text-xs font-medium text-ink/70"
          >
            Rating {rating}
          </span>
        )}
      </div>
      <h1 className="max-w-3xl text-2xl font-semibold leading-tight text-ink sm:text-3xl">
        {displayTitle}
      </h1>

      <SourceCitation node={node} />

      {typeof truthValue === "number" && (
        <div className="mt-3">
          <ClaimTruthValue value={truthValue} />
        </div>
      )}
      <CaveatMeta severity={caveatSeverity} caveatType={caveatType} />

      <TopBadges node={node} />
      <SourceCredibility node={node} />

      {extraEntries.length > 0 && (
        <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-1 text-xs sm:grid-cols-3">
          {extraEntries.map(([k, v]) => (
            <div key={k}>
              <dt className="text-muted-ink">{EXTRA_LABELS[k] || k}</dt>
              <dd className="mono font-medium">{String(v)}</dd>
            </div>
          ))}
        </dl>
      )}
      </div>

      <div className="mx-auto mt-8 max-w-[1560px] px-4 sm:px-6">
      <div className="grid gap-6 lg:grid-cols-[180px_1fr_240px] lg:items-start">
        {tocItems.length > 0 ? (
          <SourceToc items={tocItems} />
        ) : (
          <div className="hidden lg:block" aria-hidden />
        )}

        <NodeArticle html={html} />

        <aside className="space-y-8">
          <ReviewWidget nodeId={node.id} />
          <div>
            <h2 className="mb-2 border-b border-border pb-1.5 text-xs font-semibold uppercase tracking-wide text-ink/70">
              Inbound <span className="text-muted-ink">({inbound.length})</span>
            </h2>
            <EdgeGroups edges={inbound} otherEnd="from" />
          </div>
          <div>
            <h2 className="mb-2 border-b border-border pb-1.5 text-xs font-semibold uppercase tracking-wide text-ink/70">
              Outbound <span className="text-muted-ink">({outbound.length})</span>
            </h2>
            <EdgeGroups edges={outbound} otherEnd="to" />
          </div>
        </aside>
      </div>
      </div>

      {showFooter && (
        <footer id="references" className="mx-auto mt-12 max-w-6xl space-y-2 border-t border-border px-4 pt-3 sm:px-6">
          {hasDates && (
            <div className="flex flex-wrap gap-3 text-xs text-muted-ink">
              {node.created && <span>Created {formatDate(node.created)}</span>}
              {node.updated && <span>Updated {formatDate(node.updated)}</span>}
            </div>
          )}

          {hasReferences && (
            <div className="space-y-1">
              <h2 className="text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
                References
              </h2>
              {/* Footer text is capped at 40% of the page width — these are short
                  attribution/provenance lines, not article copy, and reading the
                  full-width article measure here just looks like an unstyled
                  afterthought. */}
              <ol className="max-w-[40vw] list-decimal space-y-1 pl-4">
                {hasCritiqueStatus && (
                  <li className="text-[0.625rem] text-muted-ink">
                    Retraction/correction status checked against Crossref (which now includes the
                    Retraction Watch database) or DataCite for arXiv preprints, at curation time, not a
                    live guarantee; verify independently before relying on it.
                  </li>
                )}
                {hasTripodCompliance && (
                  <li className="text-[0.625rem] text-muted-ink">
                    Gallifant, J., Afshar, M., et al.{" "}
                    <a
                      href="https://www.nature.com/articles/s41591-024-03425-5"
                      className="underline hover:text-forest"
                    >
                      (2025). The TRIPOD-LLM reporting guideline for studies using large language
                      models. <em>Nature Medicine</em>, 31, 60–69.
                    </a>{". "}
                    Transparency, Openness, and reporting-compliance sections above are scored against
                    this checklist.
                  </li>
                )}
                {curatedWithModel && (
                  <li className="text-[0.625rem] text-muted-ink">
                    Trust-signal analysis on this page was curated with {curatedWithModel}
                    {curatedWithModelDate ? `, ${curatedWithModelDate}` : ""}, an AI assistant, not an
                    independent human reviewer; verify anything load-bearing.
                  </li>
                )}
              </ol>
            </div>
          )}
        </footer>
      )}
    </main>
  );
}

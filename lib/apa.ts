import type { GraphNode } from "./data";

type ApaAuthor = { given: string; family: string };

/**
 * Sentence-cases a title per APA 7 (only first word, first word after a
 * colon, and proper nouns capitalized) while preserving tokens that are
 * already ALL CAPS (treated as acronyms — GPT, LLM, CONSORT, STROBE, ...)
 * or that mix letters with digits/hyphens (GPT-4, COVID-19) rather than
 * blindly lowercasing them.
 */
function sentenceCaseTitle(title: string): string {
  const words = title.split(" ");
  let afterColon = true;
  return words
    .map((word, i) => {
      const isAcronym = /^[A-Z0-9][A-Z0-9.\-]*$/.test(word) && /[A-Z]/.test(word) && word.length > 1;
      const hasDigit = /\d/.test(word);
      const preserve = isAcronym || hasDigit;
      const capitalize = i === 0 || afterColon;
      afterColon = /:$/.test(word);
      if (preserve) return word;
      if (capitalize) return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
      return word.toLowerCase();
    })
    .join(" ");
}

function formatAuthorApa(a: ApaAuthor): string {
  const initials = a.given
    .split(/\s+/)
    .filter(Boolean)
    .map((n) => n.charAt(0).toUpperCase() + ".")
    .join(" ");
  return initials ? `${a.family}, ${initials}` : a.family;
}

function formatAuthorList(authors: ApaAuthor[]): string {
  if (authors.length === 0) return "";
  if (authors.length === 1) return formatAuthorApa(authors[0]);
  if (authors.length <= 20) {
    const formatted = authors.map(formatAuthorApa);
    return formatted.slice(0, -1).join(", ") + ", & " + formatted[formatted.length - 1];
  }
  // 21+ authors: first 19, ellipsis, then last author (APA 7 rule).
  const first19 = authors.slice(0, 19).map(formatAuthorApa);
  const last = formatAuthorApa(authors[authors.length - 1]);
  return first19.join(", ") + ", ... " + last;
}

export type ApaCitation = {
  hasData: boolean;
  authors: string;
  year: string;
  title: string;
  /** Journal/venue name — italicized in APA. */
  container: string;
  /** "12(3)" — the volume number is italicized in APA, the (issue) is not; kept as one string for simplicity. */
  volumeIssue: string;
  pages: string;
  url: string;
};

/** Builds an APA 7th-edition reference-list citation from a SRC node's extracted bibliographic extras. */
export function formatApaCitation(node: Pick<GraphNode, "extras">): ApaCitation {
  const e = node.extras;
  const rawAuthors = e.apaAuthors as ApaAuthor[] | undefined;
  const title = e.apaTitle as string | undefined;
  const container = e.apaContainer as string | undefined;
  const year = e.apaYear as number | undefined;
  const volume = e.apaVolume as string | undefined;
  const issue = e.apaIssue as string | undefined;
  const pages = e.apaPages as string | undefined;
  const articleNumber = e.apaArticleNumber as string | undefined;
  const doi = e.doi as string | undefined;
  const landingUrl = e.apaLandingUrl as string | undefined;

  if (!title || !rawAuthors || rawAuthors.length === 0) {
    return { hasData: false, authors: "", year: "", title: "", container: "", volumeIssue: "", pages: "", url: "" };
  }

  let volumeIssue = "";
  if (volume) volumeIssue = issue ? `${volume}(${issue})` : volume;

  return {
    hasData: true,
    authors: formatAuthorList(rawAuthors),
    year: String(year ?? "n.d."),
    title: sentenceCaseTitle(title),
    container: container || "",
    volumeIssue,
    pages: pages || (articleNumber ? `Article ${articleNumber}` : ""),
    url: doi ? `https://doi.org/${doi}` : landingUrl || "",
  };
}

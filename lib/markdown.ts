import { marked } from "marked";

marked.setOptions({ gfm: true, breaks: false });

const CALLOUT_LABELS: Record<string, string> = {
  info: "Info",
  success: "Success",
  tip: "Tip",
  note: "Note",
  warning: "Warning",
  danger: "Danger",
  question: "Question",
  quote: "Quote",
  abstract: "Summary",
  example: "Example",
};

/**
 * Pre-process Obsidian-style callouts (`> [!type] Title` blockquotes) into
 * raw HTML blocks (rendered via marked for their inner content), since
 * marked's default blockquote handling doesn't know about the `[!type]` marker.
 */
function transformCallouts(md: string): string {
  const lines = md.split("\n");
  const out: string[] = [];
  let i = 0;
  const calloutStart = /^>\s*\[!(\w+)\]([+-]?)\s*(.*)$/;

  while (i < lines.length) {
    const m = lines[i].match(calloutStart);
    if (!m) {
      out.push(lines[i]);
      i++;
      continue;
    }
    const [, rawType, , titleRest] = m;
    const type = rawType.toLowerCase();
    const label = CALLOUT_LABELS[type] || rawType;
    const title = titleRest.trim();
    const bodyLines: string[] = [];
    i++;
    while (i < lines.length && /^>(\s?)/.test(lines[i])) {
      bodyLines.push(lines[i].replace(/^>(\s?)/, ""));
      i++;
    }
    // allow a single blank line to continue the callout as blockquote
    // (already handled by the >? regex requiring '>' prefix)
    const innerHtml = marked.parse(bodyLines.join("\n").trim(), {
      async: false,
    }) as string;
    // Titles can carry inline markdown (e.g. `> [!success] **TL;DR**`) — parse
    // it instead of escaping, so it renders as `<strong>TL;DR</strong>`
    // rather than literal asterisks.
    const titleHtml = title ? (marked.parseInline(title, { async: false }) as string) : "";
    out.push(
      `<div class="callout callout-${escapeAttr(type)}">` +
        `<div class="callout-title">${escapeHtml(label)}${
          title ? `: ${titleHtml}` : ""
        }</div>` +
        `<div class="callout-body">${innerHtml}</div>` +
        `</div>`
    );
  }
  return out.join("\n");
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
function escapeAttr(s: string): string {
  return s.replace(/[^a-z0-9-]/gi, "");
}

/**
 * `marked` emits fenced ```mermaid blocks as an inert, HTML-escaped
 * `<pre><code class="language-mermaid">` — no diagram ever renders. Mermaid's
 * client-side runtime looks for `<div class="mermaid">` elements containing
 * the raw diagram source, so swap the wrapper; the code's HTML-entity
 * escaping is preserved (and still correct) since the browser decodes it
 * back to the original text when parsing this HTML.
 */
function activateMermaid(html: string): string {
  return html.replace(
    /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
    (_m, escaped) => `<div class="mermaid">${escaped}</div>`
  );
}

function stripTags(html: string): string {
  return html.replace(/<[^>]+>/g, "");
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export type TocItem = { id: string; level: 2 | 3; text: string };

/** Tags every H2/H3 with a stable id and returns a flat outline for a TOC. */
function injectHeadingIds(html: string): { html: string; toc: TocItem[] } {
  const toc: TocItem[] = [];
  const usedSlugs = new Map<string, number>();
  const tagged = html.replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_match, lvl, inner) => {
    const text = stripTags(inner).trim();
    let slug = slugify(text) || "section";
    const seen = usedSlugs.get(slug) ?? 0;
    usedSlugs.set(slug, seen + 1);
    if (seen > 0) slug = `${slug}-${seen + 1}`;
    toc.push({ id: slug, level: Number(lvl) as 2 | 3, text });
    return `<h${lvl} id="${slug}">${inner}</h${lvl}>`;
  });
  return { html: tagged, toc };
}

export function renderMarkdown(md: string): { html: string; toc: TocItem[] } {
  const withCallouts = transformCallouts(md);
  const rawHtml = marked.parse(withCallouts, { async: false }) as string;
  const withMermaid = activateMermaid(rawHtml);
  return injectHeadingIds(withMermaid);
}

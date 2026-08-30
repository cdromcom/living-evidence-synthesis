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
 * Obsidian renders each callout type with a Lucide icon baked into its own
 * app chrome — that icon simply doesn't exist on the web (no equivalent
 * asset ships here), so callouts rendered flat text-only, title but no
 * glyph. These are small inline SVGs standing in for the missing icons,
 * one shape per type, colored via `currentColor` so each inherits its
 * callout's own `--callout-accent` (set in globals.css) automatically.
 */
const CALLOUT_ICONS: Record<string, string> = {
  info: '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5"/><circle cx="12" cy="8" r="0.75" fill="currentColor" stroke="none"/>',
  success: '<circle cx="12" cy="12" r="8.5"/><path d="M8 12.3l2.6 2.6L16.5 9"/>',
  tip: '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5.9 1 .9 1.6v.5h5.2v-.5c0-.6.3-1.1.9-1.6A6 6 0 0 0 12 3Z"/>',
  note: '<path d="M5 4.5h11l3 3V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5.5a1 1 0 0 1 1-1Z"/><path d="M8 10h8M8 14h5"/>',
  warning: '<path d="M12 3.5 21 19.5H3Z"/><path d="M12 10v4.5"/><circle cx="12" cy="17.3" r="0.75" fill="currentColor" stroke="none"/>',
  danger: '<circle cx="12" cy="12" r="8.5"/><path d="M9 9l6 6M15 9l-6 6"/>',
  question: '<circle cx="12" cy="12" r="8.5"/><path d="M9.5 9.3c0-1.5 1.1-2.6 2.5-2.6s2.5 1 2.5 2.3c0 1.6-2.5 1.9-2.5 3.8"/><circle cx="12" cy="17" r="0.75" fill="currentColor" stroke="none"/>',
  quote: '<path d="M7 8.5c-1.7 0-3 1.3-3 3v1c0 1.7 1.3 3 3 3M7 8.5v7M17 8.5c-1.7 0-3 1.3-3 3v1c0 1.7 1.3 3 3 3M17 8.5v7"/>',
  abstract: '<path d="M6 4.5h9l3 3V19a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V5.5a1 1 0 0 1 1-1Z"/><path d="M8.5 9.5h7M8.5 13h7M8.5 16.5h4"/>',
  example: '<rect x="4" y="5.5" width="16" height="12" rx="1.5"/><path d="M4 9h16M9 9v8.5"/>',
};

function calloutIconSvg(type: string): string {
  const path = CALLOUT_ICONS[type] || CALLOUT_ICONS.note;
  return `<svg class="callout-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${path}</svg>`;
}

/**
 * The Critical-Appraisal and TRIPOD-LLM tables use emoji (🟢🟡🔴 and
 * ✅⚠️❌➖) as a 4-level good→bad status scale. Full-saturation rainbow
 * emoji read as loud/inconsistent next to the rest of the page's restrained
 * palette, and rely on hue alone (a real accessibility problem for
 * red/green color-blindness — ~8% of men). Swapped for one shared,
 * single-hue icon family (shape encodes the level, not color): solid dot =
 * good, half dot = partial/concern, ring = bad, dash = not applicable.
 * Applies to both emoji sets identically since they're the same underlying
 * 4-level scale under different glyphs.
 */
const STATUS_ICON_MAP: Record<string, { shape: string; level: string }> = {
  "🟢": { shape: "solid", level: "good" },
  "✅": { shape: "solid", level: "good" },
  "🟡": { shape: "half", level: "partial" },
  "⚠️": { shape: "half", level: "partial" },
  "🔴": { shape: "ring", level: "bad" },
  "❌": { shape: "ring", level: "bad" },
  "➖": { shape: "dash", level: "na" },
};

const STATUS_SHAPE_SVG: Record<string, string> = {
  solid: '<circle cx="12" cy="12" r="7.5" fill="currentColor" stroke="none"/>',
  half: '<circle cx="12" cy="12" r="7.5" fill="none"/><path d="M12 4.5a7.5 7.5 0 0 1 0 15Z" fill="currentColor" stroke="none"/>',
  ring: '<circle cx="12" cy="12" r="7.5" fill="none"/>',
  dash: '<path d="M7 12h10"/>',
};

const STATUS_LEVEL_LABELS: Record<string, string> = {
  good: "Reported / low risk",
  partial: "Partial / some concerns",
  bad: "Not reported / high risk",
  na: "Not applicable",
};

function statusIconSvg(shape: string, level: string): string {
  return (
    `<svg class="status-icon status-icon-${level}" width="19" height="19" viewBox="0 0 24 24" ` +
    `stroke="currentColor" stroke-width="2" aria-hidden="true">${STATUS_SHAPE_SVG[shape]}</svg>`
  );
}

/**
 * Replace a bare status emoji sitting alone in a table cell with the muted
 * icon. Only matches a cell whose *entire* trimmed content is one of the
 * known glyphs, so emoji used as regular prose elsewhere on the page are
 * left untouched.
 */
function muteStatusIcons(html: string): string {
  return html.replace(
    /<td([^>]*)>\s*(🟢|🟡|🔴|✅|⚠️|❌|➖)\s*<\/td>/g,
    (_m, attrs, glyph) => {
      const info = STATUS_ICON_MAP[glyph];
      if (!info) return _m;
      return `<td${attrs} class="status-icon-cell"><span title="${STATUS_LEVEL_LABELS[info.level]}">${statusIconSvg(info.shape, info.level)}</span></td>`;
    }
  );
}

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
        `<div class="callout-title">${calloutIconSvg(type)}<span>${escapeHtml(label)}${
          title ? `: ${titleHtml}` : ""
        }</span></div>` +
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

// Maps a Quality Appraisal table row's bolded domain label to the same
// slug used by its corresponding top-of-page trust-signal chip (matching
// the `rigor/<slug>/*` frontmatter tag namespace), so a chip can link
// straight to `#qa-<slug>` and land on its row.
const APPRAISAL_ROW_SLUGS: Record<string, string> = {
  "construct validity": "construct-validity",
  "internal validity": "internal-validity",
  "external validity": "external-validity",
  "statistical rigor": "statistical-rigor",
  reproducibility: "reproducibility",
  "data leakage": "data-leakage",
  "baseline adequacy": "baseline-adequacy",
  "train/dev/test hygiene": "train-dev-test",
  "multiple-comparisons correction": "multiple-comparisons",
  "human-baseline comparability": "human-baseline",
  "statistical power": "statistical-power",
  "confidence intervals": "confidence-intervals",
  "chance-corrected metrics": "chance-corrected-metrics",
  "statistic accuracy": "statistic-accuracy",
  "non-significant result spin": "spin",
  "ablation experiment(s)": "ablation-experiments",
};

/**
 * Tags each row of the "## Quality appraisal" table with a stable
 * `id="qa-<slug>"` so a top-of-page trust-signal chip can link directly to
 * its row (`components/TopBadges.tsx`'s badges use the same slugs).
 */
function tagAppraisalRows(html: string): string {
  const section = html.match(/<h2 id="[^"]*">\s*Quality appraisal\s*<\/h2>([\s\S]*?)(?=<h2 |$)/i);
  if (!section) return html;
  const [full, body] = section;
  const taggedBody = body.replace(/<tr>\s*<td>\s*<strong>([^<]+)<\/strong>/g, (rowMatch, label) => {
    const slug = APPRAISAL_ROW_SLUGS[label.trim().toLowerCase()];
    return slug ? rowMatch.replace("<tr>", `<tr id="qa-${slug}">`) : rowMatch;
  });
  return html.replace(full, full.replace(body, taggedBody));
}

/**
 * Tags each row of the "## TRIPOD-LLM reporting summary" table with a
 * stable `id="tripod-<item>"` (e.g. `tripod-14d`, `tripod-9a`) so a
 * top-of-page trust-signal chip (Registration, Protocol, Data/Code Repo
 * Check, Ethical Approval, Funding, COI, Prompt Engineering) can link
 * straight to its own checklist row instead of just the table's heading.
 */
function tagTripodRows(html: string): string {
  const section = html.match(/<h2 id="[^"]*">\s*TRIPOD-LLM reporting summary\s*<\/h2>([\s\S]*?)(?=<h2 |$)/i);
  if (!section) return html;
  const [full, body] = section;
  const taggedBody = body.replace(/<tr>\s*<td>\s*<strong>([^<]+)<\/strong>/g, (rowMatch, item) => {
    const slug = item.trim().toLowerCase();
    return rowMatch.replace("<tr>", `<tr id="tripod-${slug}">`);
  });
  return html.replace(full, full.replace(body, taggedBody));
}

/**
 * Wraps every H3 subsection (e.g. Methods Context's What?/How?/Who?) in its
 * own collapsible <details>, nested inside its parent H2's accordion body.
 */
function wrapH3Subsections(html: string): string {
  const h3Regex = /<h3 id="[^"]*">[\s\S]*?<\/h3>/g;
  const matches = [...html.matchAll(h3Regex)];
  if (matches.length === 0) return html;
  let result = html.slice(0, matches[0].index);
  for (let i = 0; i < matches.length; i++) {
    const heading = matches[i][0];
    const start = matches[i].index! + heading.length;
    const end = i + 1 < matches.length ? matches[i + 1].index! : html.length;
    const body = html.slice(start, end);
    result += `<details class="accordion-section" open><summary>${heading}</summary><div class="accordion-body">${body}</div></details>`;
  }
  return result;
}

/**
 * Wraps every top-level (H2) section in a collapsible <details>, so long
 * bodies (Description, Methods Context, Other Notes, Caveats, Supports
 * Claim(s), ...) can be collapsed independently, and wraps each H2
 * section's own H3 subsections (e.g. Methods Context's What?/How?/Who?) the
 * same way. The "Source" section is left alone — it's just the citation
 * link, not worth collapsing, and users expect it visible immediately.
 * Sections start open so nothing looks different from before until a reader
 * chooses to collapse one; the native <details> element also means an
 * in-page anchor (from the TOC or a chip link) auto-expands a closed
 * section on navigation, no JS required.
 */
function wrapAccordionSections(html: string): string {
  const h2Regex = /<h2 id="[^"]*">[\s\S]*?<\/h2>/g;
  const matches = [...html.matchAll(h2Regex)];
  if (matches.length === 0) return html;
  let result = html.slice(0, matches[0].index);
  for (let i = 0; i < matches.length; i++) {
    const heading = matches[i][0];
    const start = matches[i].index! + heading.length;
    const end = i + 1 < matches.length ? matches[i + 1].index! : html.length;
    const body = wrapH3Subsections(html.slice(start, end));
    const headingText = stripTags(heading).trim();
    if (headingText.toLowerCase() === "source") {
      result += heading + body;
    } else {
      result += `<details class="accordion-section" open><summary>${heading}</summary><div class="accordion-body">${body}</div></details>`;
    }
  }
  return result;
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
  const withMutedIcons = muteStatusIcons(withMermaid);
  const { html, toc } = injectHeadingIds(withMutedIcons);
  return { html: wrapAccordionSections(tagTripodRows(tagAppraisalRows(html))), toc };
}

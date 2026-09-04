import { marked } from "marked";
import katex from "katex";

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

/**
 * Renders `$…$` and `$$…$$` to HTML with KaTeX, at build time — no client-side
 * math runtime ships.
 *
 * The delimiter rule has to survive a corpus full of dollar amounts
 * ("$0.038 per paper versus o3 at $0.321"). Requiring that no whitespace sit
 * immediately inside the delimiters separates the two cleanly: real math like
 * `$\hat{p}_{i,g} = 1$` keeps its internal spaces, while a currency pair always
 * has a space before the closing `$`. Checked against every vault file — 40
 * matches, all genuine LaTeX, no false positives.
 *
 * Runs before marked so KaTeX's markup is emitted as raw HTML, and math
 * containing `_` or `*` never reaches the emphasis parser.
 */
function renderMath(md: string): string {
  const render = (tex: string, displayMode: boolean): string => {
    try {
      return katex.renderToString(tex, {
        displayMode,
        throwOnError: false,
        strict: false,
        output: "html",
      });
    } catch {
      // A malformed expression should show as its own source, not vanish.
      return `<code class="math-error">${escapeHtml(displayMode ? `$$${tex}$$` : `$${tex}$`)}</code>`;
    }
  };
  return md
    .replace(/\$\$([\s\S]+?)\$\$/g, (_m, tex) => render(tex.trim(), true))
    .replace(/(?<!\$)\$(?!\s)((?:[^$\n])+?)(?<!\s)\$(?!\d)/g, (_m, tex) => render(tex, false));
}

/**
 * A figure embed sits on its own line but usually directly under the quote it
 * illustrates, with no blank line between them — so marked folds the image into
 * the quote's paragraph. Give each image its own block (respecting any
 * blockquote prefix) so it can be lifted into a `<figure>` afterwards; a
 * `<details>` element is not valid inside a `<p>`.
 */
function isolateImageLines(md: string): string {
  const out: string[] = [];
  for (const line of md.split("\n")) {
    const m = line.match(/^((?:\s*>\s?)*)(.*)$/);
    const prefix = m ? m[1] : "";
    const rest = m ? m[2] : line;
    if (/^!\[/.test(rest.trim()) && out.length > 0) {
      const prevRest = out[out.length - 1].replace(/^(?:\s*>\s?)*/, "").trim();
      if (prevRest !== "") out.push(prefix.trimEnd());
    }
    out.push(line);
  }
  return out.join("\n");
}

/**
 * Turns a crop's filename into something a reader can place. The vault names
 * them `<citekey>-<what>-p<page>[-<n>].png`, so the page number and what was
 * cropped are both recoverable — which is exactly the caption a table or figure
 * lifted straight out of a paper needs in order not to be presented as ours.
 */
function describeCrop(filename: string): { label: string; page: string | null } {
  const stem = filename.replace(/\.[a-z0-9]+$/i, "");
  const pageMatch = stem.match(/-p(\d+)(?:[-_].*)?$/i);
  const page = pageMatch ? pageMatch[1] : null;
  let what = stem
    .replace(/-p\d+(?:[-_].*)?$/i, "")
    .replace(/^[a-z]+[A-Za-z]*\d{4}[a-z]?-?/, "") // drop the leading citekey
    .replace(/[-_]+/g, " ")
    .trim();
  what = what
    .replace(/\bfig(\d+)/gi, "Figure $1")
    .replace(/\btable(\d+)/gi, "Table $1")
    .replace(/\bevd\b/gi, "Evidence excerpt")
    .replace(/\bcombined\b/gi, "")
    .trim();
  const label = what ? what.charAt(0).toUpperCase() + what.slice(1) : "Figure";
  return { label, page };
}

function figureIconSvg(): string {
  return (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M3.5 15l4.5-4 4 3.5 3.5-3 5 4.5"/>' +
    '<circle cx="9" cy="9.5" r="1.4"/></svg>'
  );
}

/**
 * Lifts each figure crop out of its paragraph into a collapsed `<details>`
 * carrying a caption that names the crop and its page in the source paper.
 *
 * Collapsed by default on purpose: an EVD typically embeds three or four
 * full-width screenshots, and inline they push the prose that cites them off
 * the screen. The summary says what the reader would be opening.
 */
function renderFigureEmbeds(html: string): string {
  return html.replace(
    /<p>\s*<img src="\/vault-img\/([^"]+)" alt="([^"]*)"\s*\/?>\s*<\/p>/g,
    (_m, src, alt) => {
      const filename = decodeURIComponent(src);
      const { label, page } = describeCrop(filename);
      const cite = page ? `${label} — reproduced from the source paper, p.&nbsp;${page}` : `${label} — reproduced from the source paper`;
      const summary = page ? `${label} · p.&nbsp;${page}` : label;
      return (
        `<details class="figure-embed">` +
        `<summary>${figureIconSvg()}<span>${summary}</span></summary>` +
        `<figure class="figure-embed-body">` +
        `<img src="/vault-img/${src}" alt="${escapeHtml(alt)}" loading="lazy" />` +
        `<figcaption>${cite}</figcaption>` +
        `</figure></details>`
      );
    }
  );
}

/**
 * On a Question page, collapses the EVD list nested under each supporting Claim.
 *
 * The section answers "which claims address this question", but the evidence
 * nested beneath outnumbers the claims several times over (QUE-001: 8 claims,
 * 32 evidence items), so the claims — the actual answer — are buried. The claims
 * stay visible and each claim's evidence folds behind a count.
 */
function collapseNestedEvidence(html: string): string {
  const section = html.match(
    /<h3 id="[^"]*">\s*Supporting Claims[\s\S]*?<\/h3>([\s\S]*?)(?=<h[23] |$)/i
  );
  if (!section) return html;
  const [full, body] = section;

  const collapsed = body.replace(/<ul>([\s\S]*?)<\/ul>\s*<\/li>/g, (whole, inner) => {
    const count = (inner.match(/<li>/g) || []).length;
    if (count === 0) return whole;
    const label = count === 1 ? "1 supporting evidence node" : `${count} supporting evidence nodes`;
    return (
      `<details class="evd-nest"><summary>${label}</summary>` +
      `<ul>${inner}</ul></details></li>`
    );
  });

  return html.replace(full, full.replace(body, collapsed));
}

/**
 * Collapses the long verbatim quotes inside Methods Context.
 *
 * These run to a median of ~336 characters and there are several per subsection,
 * so they crowd out the curator's own summary of the method — which is the part
 * a reader is usually there for. Collapsed, each shows its opening words and its
 * citation, and expands on click. Only quotes past `MIN` collapse; a short one
 * costs nothing to leave in place.
 *
 * Scoped to Methods Context deliberately: a quote in Description is doing
 * different work (it *is* the evidence) and should stay visible.
 */
function collapseLongQuotes(html: string): string {
  const MIN = 200;
  const section = html.match(
    /<h2 id="[^"]*">\s*Methods Context\s*<\/h2>([\s\S]*?)(?=<h2 |$)/i
  );
  if (!section) return html;
  const [full, body] = section;

  const collapsed = body.replace(/<p>(&quot;|“)([\s\S]*?)<\/p>/g, (whole, openQuote, rest) => {
    const plain = stripTags(`${openQuote}${rest}`).replace(/&quot;/g, '"').trim();
    if (plain.length < MIN) return whole;
    // Split the trailing attribution — "(Author, Year, p. N)" — off the preview,
    // so the summary says who is being quoted without opening the quote.
    const citeMatch = plain.match(/(\([^()]*\d{4}[^()]*\))\s*$/);
    const cite = citeMatch ? citeMatch[1] : "";
    const words = plain.slice(0, 90).replace(/\s+\S*$/, "");
    return (
      `<details class="quote-collapse">` +
      `<summary><span class="quote-preview">${escapeHtml(words)}…</span>` +
      (cite ? `<span class="quote-cite">${escapeHtml(cite)}</span>` : "") +
      `</summary>` +
      `<div class="quote-collapse-body">${whole}</div>` +
      `</details>`
    );
  });

  return html.replace(full, full.replace(body, collapsed));
}

/**
 * Promotes an italic line sitting directly above a table into that table's
 * `<caption>`.
 *
 * A table lifted out of a paper has to say so — otherwise the site presents
 * someone else's numbers as if we assembled them. Writing the attribution as a
 * plain italic line keeps the vault file readable in Obsidian, where `<caption>`
 * would not render at all; the convention is `*Table N — Author Year, p. N*`
 * immediately before the table, with no blank line between.
 */
function promoteTableCaptions(html: string): string {
  return html.replace(
    /<p><em>([\s\S]*?)<\/em><\/p>\s*<table>/g,
    (_m, caption) => `<table><caption class="table-source">${caption}</caption>`
  );
}

/**
 * A run of `**Label:** value` paragraphs is a field list written as prose.
 * Obsidian stacks them as separate paragraphs, which reads as an undifferentiated
 * wall inside the Methods Context subsections; as a description list the labels
 * line up and the values become scannable.
 */
function renderFieldLists(html: string): string {
  // `(?!</p>)` matters more than it looks: with a plain lazy `[\s\S]*?` the
  // engine backtracks across paragraph boundaries to satisfy the {2,}, so a run
  // starting at one label swallows every paragraph up to the *next* label —
  // including quotes and figures — and rebuilding from the label pairs alone
  // then drops them. Confining each item to a single paragraph keeps the
  // transform incapable of losing content.
  // Two label conventions live in the vault: EVD Methods Context writes
  // `**Tools:**` and SRC structured abstracts write `**Tools.**`. Both are field
  // labels; accept either terminator. Capped at 60 characters and required to
  // contain no sentence punctuation of its own, so an ordinary bolded sentence
  // ending in a period is not mistaken for a label.
  const CELL = String.raw`<p><strong>([^<.:!?]{1,60}?)[.:]<\/strong>((?:(?!<\/p>)[\s\S])*)<\/p>`;
  const item = new RegExp(CELL, "g");
  const run = new RegExp(`(?:${CELL}\\s*){2,}`, "g");
  return html.replace(run, (matched) => {
    const rows: string[] = [];
    for (const m of matched.matchAll(item)) {
      rows.push(`<dt>${m[1]}</dt><dd>${m[2].trim()}</dd>`);
    }
    return rows.length >= 2 ? `<dl class="field-list">${rows.join("")}</dl>` : matched;
  });
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
  "statistical conclusion validity": "statistical-rigor",
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
  "ai writing check": "ai-writing-check",
  "code quality": "code-quality-fair",
  "data quality": "data-quality-fair",
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
function wrapH3Subsections(html: string, isOpen: (text: string, level: 2 | 3) => boolean): string {
  const h3Regex = /<h3 id="[^"]*">[\s\S]*?<\/h3>/g;
  const matches = [...html.matchAll(h3Regex)];
  if (matches.length === 0) return html;
  let result = html.slice(0, matches[0].index);
  for (let i = 0; i < matches.length; i++) {
    const heading = matches[i][0];
    const start = matches[i].index! + heading.length;
    const end = i + 1 < matches.length ? matches[i + 1].index! : html.length;
    const body = html.slice(start, end);
    const open = isOpen(stripTags(heading).trim(), 3) ? " open" : "";
    result += `<details class="accordion-section"${open}><summary>${heading}</summary><div class="accordion-body">${body}</div></details>`;
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
function wrapAccordionSections(html: string, isOpen: (text: string, level: 2 | 3) => boolean): string {
  const h2Regex = /<h2 id="[^"]*">[\s\S]*?<\/h2>/g;
  const matches = [...html.matchAll(h2Regex)];
  if (matches.length === 0) return html;
  let result = html.slice(0, matches[0].index);
  for (let i = 0; i < matches.length; i++) {
    const heading = matches[i][0];
    const start = matches[i].index! + heading.length;
    const end = i + 1 < matches.length ? matches[i + 1].index! : html.length;
    const body = wrapH3Subsections(html.slice(start, end), isOpen);
    const headingText = stripTags(heading).trim();
    if (headingText.toLowerCase() === "source") {
      result += heading + body;
    } else {
      const open = isOpen(headingText, 2) ? " open" : "";
      result += `<details class="accordion-section"${open}><summary>${heading}</summary><div class="accordion-body">${body}</div></details>`;
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

/**
 * Which sections start expanded.
 *
 * A Source page opens on the Question alone: everything below it — Methods,
 * Findings, the appraisal tables — is reference material a reader consults, not
 * prose they read straight through, and leaving it all open pushed the question
 * the paper answers off the top of the screen. "Abstract" stays open only
 * because it is the Question's parent; a closed parent would hide it.
 *
 * Every other node type keeps its sections open: their bodies are short enough
 * to read in one pass, and collapsing them would hide the node's whole content
 * behind a click.
 */
export type AccordionPolicy = "source" | "open";

/**
 * Drops a block of ready-made HTML immediately after the Procedure entry in
 * Methods Context.
 *
 * The prompts belong next to the procedure they were part of, not stacked at
 * the top of the page above the abstract — a reader meets "Claude was prompted
 * once with the Appendix-A instruction" and the prompt itself should be right
 * there. Falls back to the end of Methods Context when a node writes its
 * procedure without that label, and returns the page unchanged when there is no
 * Methods Context at all, so a node type that has none is never altered.
 */
function insertAfterProcedure(html: string, block: string): string {
  if (!block) return html;
  const section = html.match(
    /<h2 id="[^"]*">\s*Methods Context\s*<\/h2>([\s\S]*?)(?=<h2 |$)/i
  );
  if (!section) return html;
  const [full, body] = section;

  // The field list renders Procedure as <dt>Procedure</dt><dd>…</dd>; put the
  // block after the whole list so it does not break the dl's structure.
  const dl = body.match(/<dl class="field-list">[\s\S]*?<dt>Procedure<\/dt>[\s\S]*?<\/dl>/i);
  const next = dl
    ? body.replace(dl[0], `${dl[0]}${block}`)
    : `${body}${block}`;
  return html.replace(full, full.replace(body, next));
}

/**
 * Drops a block of ready-made HTML into a source's Methods field list, as
 * its own `<dt>Prompt</dt><dd>…</dd>` entry immediately before "At a
 * glance" (the entry that introduces the flowchart diagram; rendered by
 * renderFieldLists as `<dt>At a glance</dt><dd></dd>`, directly followed by
 * the `.mermaid` block).
 *
 * The prompt belongs right where the diagram it fed shows the prompt-template
 * step, not stacked at the top of the page above the abstract — a reader
 * meeting the flowchart's "Prompt template" node should be able to see the
 * actual prompt without scrolling back up. Wrapping it in a "Prompt" dt gives
 * it the same bold-label treatment as Design/Tools/Procedure/Sample, and
 * keeps it a normal dt/dd pair in the field list's grid rather than a
 * foreign child that would throw off the dt/dd column auto-placement (see
 * globals.css's `.field-list`).
 *
 * Falls back to the end of the field list when a source writes "At a
 * glance" without it collapsing into that list (field-list detection
 * requires 2+ consecutive `**Label.**` paragraphs), then to the end of the
 * Methods section when there is no field list at all, and returns the page
 * unchanged when there is no Methods section. A source without an "At a
 * glance" diagram is never altered — it keeps its prompt block at the top of
 * the page instead (see app/nodes/[id]/page.tsx).
 */
function insertBeforeAtAGlance(html: string, block: string): string {
  if (!block) return html;
  const section = html.match(/<h3 id="[^"]*">\s*Methods\s*<\/h3>([\s\S]*?)(?=<h[23] |$)/i);
  if (!section) return html;
  const [full, body] = section;
  const wrapped = `<dt>Prompt</dt><dd>${block}</dd>`;

  const dl = body.match(/<dl class="field-list">([\s\S]*?)<\/dl>/i);
  if (!dl) return html.replace(full, full.replace(body, `${body}${wrapped}`));
  const [dlFull, dlInner] = dl;

  const at = dlInner.match(/<dt>At a glance<\/dt>/i);
  const newInner = at ? dlInner.replace(at[0], `${wrapped}${at[0]}`) : `${dlInner}${wrapped}`;
  return html.replace(full, full.replace(body, body.replace(dlFull, `<dl class="field-list">${newInner}</dl>`)));
}

function openPredicate(policy: AccordionPolicy) {
  if (policy === "open") return () => true;
  return (text: string, level: 2 | 3) => {
    const t = text.trim().toLowerCase();
    return (level === 2 && t === "abstract") || (level === 3 && t === "question");
  };
}

export function renderMarkdown(
  md: string,
  policy: AccordionPolicy = "open",
  /** Optional HTML dropped in after the Procedure entry (see insertAfterProcedure). */
  procedureBlock = "",
  /** Optional HTML dropped in before "Methods at a glance" (see insertBeforeAtAGlance). */
  atAGlanceBlock = ""
): { html: string; toc: TocItem[] } {
  const withCallouts = transformCallouts(renderMath(isolateImageLines(md)));
  const rawHtml = marked.parse(withCallouts, { async: false }) as string;
  const withMermaid = activateMermaid(rawHtml);
  const withMutedIcons = muteStatusIcons(withMermaid);
  const withFigures = renderFigureEmbeds(withMutedIcons);
  const withCaptions = promoteTableCaptions(withFigures);
  const withFieldLists = renderFieldLists(withCaptions);
  const { html, toc } = injectHeadingIds(withFieldLists);
  const withQuotes = insertBeforeAtAGlance(
    insertAfterProcedure(collapseNestedEvidence(collapseLongQuotes(html)), procedureBlock),
    atAGlanceBlock
  );
  return {
    html: wrapAccordionSections(tagTripodRows(tagAppraisalRows(withQuotes)), openPredicate(policy)),
    toc,
  };
}

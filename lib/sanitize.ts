import sanitizeHtml from "sanitize-html";

/**
 * Allow-list sanitiser for the HTML that lib/markdown.ts produces before it is
 * handed to dangerouslySetInnerHTML. The list covers everything the vault pages
 * use today (callouts, accordion <details>, tables, figures/images, links,
 * footnotes, mermaid <div>s, inline SVG icons, KaTeX output) and drops the rest:
 * scripts, event-handler attributes, iframes, forms, javascript: URLs, etc.
 * scripts/check-sanitize.ts renders real vault pages with and without it.
 */
const TAGS = [
  // text and structure
  "a", "abbr", "b", "blockquote", "br", "caption", "cite", "code", "dd", "del", "details", "div", "dl", "dt",
  "em", "figcaption", "figure", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "ins", "kbd", "li", "mark",
  "ol", "p", "pre", "q", "s", "section", "small", "span", "strong", "sub", "summary", "sup", "table", "tbody",
  "td", "tfoot", "th", "thead", "tr", "u", "ul", "input", // input: GFM task-list checkboxes (disabled, see below)
  // inline SVG icons
  "svg", "g", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse",
  // KaTeX MathML
  "math", "semantics", "annotation", "mrow", "mi", "mn", "mo", "ms", "mtext", "mspace", "msup", "msub",
  "msubsup", "mfrac", "msqrt", "mroot", "mover", "munder", "munderover", "mtable", "mtr", "mtd", "mpadded",
  "mphantom", "menclose", "mstyle",
];

const SVG_ATTRS = [
  "viewBox", "width", "height", "fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin",
  "d", "cx", "cy", "r", "x", "y", "rx", "ry", "x1", "x2", "y1", "y2", "points", "transform", "xmlns",
];

// Inline styles come from KaTeX (sizes/offsets) and the status icon spans.
// Only plain length/keyword values are allowed: no url(), expression(), etc.
const SAFE_VALUE = [/^[-\w\s.,#%+]*$/];
const STYLE_PROPS = [
  "height", "width", "min-width", "vertical-align", "top", "left", "right", "bottom", "position",
  "margin-left", "margin-right", "margin-top", "margin-bottom", "padding-left", "padding-right",
  "border-bottom-width", "border-top-width", "color", "display", "font-size", "text-align",
];

export function sanitizeRenderedHtml(html: string): string {
  return sanitizeHtml(html, {
    allowedTags: TAGS,
    allowedAttributes: {
      "*": ["class", "id", "title", "role", "style", "aria-*", "data-*", "lang", "dir"],
      a: ["href", "name", "target", "rel"],
      img: ["src", "alt", "loading", "width", "height"],
      details: ["open"],
      th: ["align", "colspan", "rowspan", "scope"],
      td: ["align", "colspan", "rowspan"],
      ol: ["start"],
      input: ["type", "checked", "disabled"],
      annotation: ["encoding"],
      math: ["xmlns", "display"],
      svg: SVG_ATTRS,
      g: SVG_ATTRS,
      path: SVG_ATTRS,
      circle: SVG_ATTRS,
      rect: SVG_ATTRS,
      line: SVG_ATTRS,
      polyline: SVG_ATTRS,
      polygon: SVG_ATTRS,
      ellipse: SVG_ATTRS,
    },
    allowedStyles: {
      "*": Object.fromEntries(STYLE_PROPS.map((p) => [p, SAFE_VALUE])),
    },
    allowedSchemes: ["http", "https", "mailto"],
    allowedSchemesByTag: { img: ["http", "https"] },
    // Relative links (/nodes/CLM-003, #anchors) and images (/vault-img/...) are kept.
    allowProtocolRelative: false,
    // Keep SVG attribute case (viewBox) and don't rewrite empty SVG children.
    parser: { lowerCaseAttributeNames: false, lowerCaseTags: false },
    disallowedTagsMode: "discard",
  });
}

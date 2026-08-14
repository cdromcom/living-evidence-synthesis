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
    out.push(
      `<div class="callout callout-${escapeAttr(type)}">` +
        `<div class="callout-title">${escapeHtml(label)}${
          title ? `: ${escapeHtml(title)}` : ""
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

export function renderMarkdown(md: string): string {
  const withCallouts = transformCallouts(md);
  return marked.parse(withCallouts, { async: false }) as string;
}

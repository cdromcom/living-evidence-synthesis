import "server-only";
import { ALL_NODES, type NodeType } from "./data";

const idToFilename = new Map(ALL_NODES.map((n) => [n.id, n.filename]));

const VAULT_DIR: Record<NodeType, string> = {
  QUE: "sysrev/questions",
  CLM: "sysrev/claims",
  EVD: "sysrev/evidence",
  CVT: "sysrev/caveats",
  SRC: "sysrev/source",
  EP: "sysrev/evd-patterns",
};

function wikilink(id: string): string {
  const filename = idToFilename.get(id);
  if (!filename) throw new Error(`Unknown node id: ${id}`);
  return `[[${filename}]]`;
}

function linkList(ids: string[]): string {
  return ids.map((id) => `- ${wikilink(id)}`).join("\n");
}

function sanitizeForFilename(title: string): string {
  return title.replace(/[\\/:*?"<>|]/g, "").trim();
}

// Keep `vault/<dir>/<file>` at or under this length so the repo still checks
// out on Windows when cloned into a deep folder (e.g. OneDrive Documents).
const MAX_VAULT_PATH = 150;

/** The title part of a node filename: Windows-safe and short enough to fit MAX_VAULT_PATH. */
function fitTitleForFilename(title: string, dir: string, prefix: string): string {
  const clean = sanitizeForFilename(title);
  const room = MAX_VAULT_PATH - `vault/${dir}/`.length - prefix.length - ".md".length;
  if (clean.length <= room) return clean;
  const cut = clean.slice(0, room);
  const space = cut.lastIndexOf(" ");
  return (space > 0 ? cut.slice(0, space) : cut).replace(/[\s,;:.\-]+$/, "");
}

export type ContributionEdges = {
  addresses?: string[]; // CLM -> QUE
  supports?: string[]; // CLM's supporting EVD ids, or EVD's supported CLM ids
  derivedFrom?: string[]; // EVD -> SRC (exactly one expected)
  qualifies?: string[]; // CVT -> EVD
  instantiates?: string[]; // EP's supporting EVD ids
  relatesTo?: string[]; // EP -> CLM/EP
};

export type ContributionInput = {
  type: NodeType;
  title: string;
  body: string;
  edges: ContributionEdges;
  citekey?: string; // SRC only
  // Quote grounding (EVD and CVT), matching the vault's format.
  quote?: string; // verbatim text from the paper
  citation?: string; // e.g. "Sarol et al., 2024"
  page?: string; // the PRINTED journal page number, not the PDF page position
  figureRef?: string; // e.g. "Table 1" or "Figure 2"
  screenshot?: string; // image filename, e.g. smithExample2026-evd-p5-1.png (added to the PR by the reviewer)
};

export const CONTRIBUTION_TYPES: readonly NodeType[] = ["QUE", "CLM", "EVD", "CVT", "SRC", "EP"];

/** Single-line, no markdown-structure characters: safe inside a blockquote line or [[embed]]. */
function oneLine(s: string): string {
  return s.replace(/\s+/g, " ").trim();
}

/**
 * The vault's quote block:
 *   > "quote" (Author, Year, p. N)
 *   > ![[screenshot.png]]
 *   >
 *   > Grounding table (Table 1, p. 5)
 * Returns "" when there is no quote.
 */
export function buildQuoteBlock(input: ContributionInput): string {
  const quote = oneLine(input.quote ?? "").replace(/^["\u201c]|["\u201d]$/g, "");
  if (!quote) return "";
  const cite = oneLine(input.citation ?? "");
  const page = oneLine(input.page ?? "");
  const where = [cite, page ? `p. ${page}` : ""].filter(Boolean).join(", ");
  const lines = [`> "${quote}"${where ? ` (${where})` : ""}`];
  const shot = oneLine(input.screenshot ?? "");
  if (shot) lines.push(`> ![[${shot}]]`);
  const ref = oneLine(input.figureRef ?? "");
  if (ref) {
    lines.push(">", `> Grounding table (${ref}${page ? `, p. ${page}` : ""})`);
  }
  return lines.join("\n");
}

/** Builds { path, content } for the new node file, plus any files that must be patched (e.g. a Question gaining a new Claim in its Supporting Claims list). */
export function buildContributionFiles(input: ContributionInput): {
  newFile: { path: string; content: string };
  patches: { path: string; append: (current: string) => string }[];
} {
  const { type, title, body, edges } = input;
  const quoteBlock = buildQuoteBlock(input);
  const created = new Date().toISOString().slice(0, 10);
  const dir = VAULT_DIR[type];

  // Keep the real title when the filename has to drop Windows-invalid
  // characters or be shortened.
  const fileTitle = type === "SRC" ? null : fitTitleForFilename(title, dir, `${type} - `);
  const titleLine = fileTitle !== null && fileTitle !== title.trim() ? [`title: ${JSON.stringify(title.trim())}`] : [];
  const frontmatter = ["---", "NodeFormality: draft", ...titleLine, "tags: []", `created: ${created}`, "---", ""].join("\n");

  let filename: string;
  let sections = "";
  const patches: { path: string; append: (current: string) => string }[] = [];

  switch (type) {
    case "QUE": {
      filename = `QUE - ${fileTitle}.md`;
      sections = `### Snippet: Quote(s) & Screenshots\n\n${body}\n\n### Supporting Claims\n\n`;
      break;
    }
    case "CLM": {
      filename = `CLM - ${fileTitle}.md`;
      sections = `${body}\n`;
      if (edges.supports?.length) {
        sections += `\n### Supporting Evidence\n\n${linkList(edges.supports)}\n`;
      }
      for (const queId of edges.addresses || []) {
        const path = `vault/sysrev/questions/${idToFilename.get(queId)}.md`;
        patches.push({
          path,
          append: (current) =>
            appendUnderHeading(current, /^###\s+Supporting Claims/i, `- [[${filename.replace(/\.md$/, "")}]]`),
        });
      }
      break;
    }
    case "EVD": {
      filename = `EVD - ${fileTitle}.md`;
      const srcId = edges.derivedFrom?.[0];
      sections = `## Description\n\n${quoteBlock ? quoteBlock + "\n\n" : ""}${body}\n`;
      if (srcId) sections += `\n## Source\n\n${wikilink(srcId)}\n`;
      if (edges.supports?.length) {
        sections += `\n## Supports Claim(s)\n\n${linkList(edges.supports)}\n`;
      }
      if (edges.instantiates?.length) {
        sections += `\n## Instantiates Pattern\n\n${linkList(edges.instantiates)}\n`;
      }
      break;
    }
    case "CVT": {
      filename = `CVT - ${fileTitle}.md`;
      sections = `## Limitation\n\n${body}\n`;
      if (quoteBlock) sections += `\n### Supporting Quote\n\n> [!info] Quotes\n${quoteBlock}\n`;
      if (edges.qualifies?.length) {
        sections += `\n### Applies To\n\n${linkList(edges.qualifies)}\n`;
      }
      break;
    }
    case "SRC": {
      const citekey = sanitizeForFilename(input.citekey || title);
      filename = `@${citekey}.md`;
      sections = `## Description\n\n${body}\n`;
      break;
    }
    case "EP": {
      filename = `EP - ${fileTitle}.md`;
      sections = `## Pattern statement\n\n${body}\n`;
      if (edges.instantiates?.length) {
        sections += `\n## Supporting Evidence\n\n${linkList(edges.instantiates)}\n`;
      }
      if (edges.relatesTo?.length) {
        sections += `\n## Connected discourse-graph nodes\n\n${linkList(edges.relatesTo)}\n`;
      }
      break;
    }
  }

  return {
    newFile: { path: `vault/${dir}/${filename}`, content: frontmatter + "\n" + sections },
    patches,
  };
}

/** Appends a list item under the first heading matching `headingRe`, right after any existing items in that section. */
function appendUnderHeading(body: string, headingRe: RegExp, newLine: string): string {
  const lines = body.split("\n");
  const startIdx = lines.findIndex((l) => headingRe.test(l.trim()));
  if (startIdx === -1) {
    // Heading not found: append a new section at the end.
    return body.trimEnd() + `\n\n### Supporting Claims\n\n${newLine}\n`;
  }
  const startLevel = (lines[startIdx].match(/^#+/) || ["#"])[0].length;
  let endIdx = lines.length;
  for (let i = startIdx + 1; i < lines.length; i++) {
    const hm = lines[i].match(/^(#+)\s/);
    if (hm && hm[1].length <= startLevel) {
      endIdx = i;
      break;
    }
  }
  lines.splice(endIdx, 0, newLine);
  return lines.join("\n");
}

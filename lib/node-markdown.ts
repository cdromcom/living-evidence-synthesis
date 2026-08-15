import "server-only";
import { ALL_NODES, type NodeType } from "./data";

const idToFilename = new Map(ALL_NODES.map((n) => [n.id, n.filename]));

const VAULT_DIR: Record<NodeType, string> = {
  QUE: "questions",
  CLM: "claims",
  EVD: "evidence",
  CVT: "caveats",
  SRC: "source",
  EP: "evd-patterns",
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
};

/** Builds { path, content } for the new node file, plus any files that must be patched (e.g. a Question gaining a new Claim in its Supporting Claims list). */
export function buildContributionFiles(input: ContributionInput): {
  newFile: { path: string; content: string };
  patches: { path: string; append: (current: string) => string }[];
} {
  const { type, title, body, edges } = input;
  const created = new Date().toISOString().slice(0, 10);
  const dir = VAULT_DIR[type];

  const frontmatter = ["---", "NodeFormality: draft", "tags: []", `created: ${created}`, "---", ""].join("\n");

  let filename: string;
  let sections = "";
  const patches: { path: string; append: (current: string) => string }[] = [];

  switch (type) {
    case "QUE": {
      filename = `QUE - ${sanitizeForFilename(title)}.md`;
      sections = `### Snippet: Quote(s) & Screenshots\n\n${body}\n\n### Supporting Claims\n\n`;
      break;
    }
    case "CLM": {
      filename = `CLM - ${sanitizeForFilename(title)}.md`;
      sections = `${body}\n`;
      if (edges.supports?.length) {
        sections += `\n### Supporting Evidence\n\n${linkList(edges.supports)}\n`;
      }
      for (const queId of edges.addresses || []) {
        const path = `vault/questions/${idToFilename.get(queId)}.md`;
        patches.push({
          path,
          append: (current) =>
            appendUnderHeading(current, /^###\s+Supporting Claims/i, `- [[${filename.replace(/\.md$/, "")}]]`),
        });
      }
      break;
    }
    case "EVD": {
      filename = `EVD - ${sanitizeForFilename(title)}.md`;
      const srcId = edges.derivedFrom?.[0];
      sections = `## Description\n\n${body}\n`;
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
      filename = `CVT - ${sanitizeForFilename(title)}.md`;
      sections = `## Limitation\n\n${body}\n`;
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
      filename = `EP - ${sanitizeForFilename(title)}.md`;
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

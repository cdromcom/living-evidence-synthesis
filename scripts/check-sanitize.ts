/**
 * Renders every node page (or the ids given as arguments) with and without the
 * sanitiser and reports any difference in the resulting DOM.
 *
 *   npx tsx --conditions=react-server scripts/check-sanitize.ts [ID ...]
 *
 * Both sides are re-parsed and re-serialised before comparing, so harmless
 * serialisation noise (attribute order, <path/> vs <path></path>) is ignored.
 * Exit code 1 if any page differs.
 */
import { parseDocument } from "htmlparser2";
import render from "dom-serializer";
import { renderMarkdown, renderMarkdownUnsanitized } from "../lib/markdown";
import { ALL_NODES } from "../lib/data";

function canon(html: string): string {
  // <pdf_path> is a literal placeholder in a few vault pages that the browser treats as an
  // unknown, invisible element; the sanitiser drops the tag, so rendering is unchanged.
  html = html.replace(/<\/?pdf_path>/g, "");
  const doc = parseDocument(html, { lowerCaseAttributeNames: false });
  return render(doc, { selfClosingTags: false, encodeEntities: "utf8" } as never)
    .replace(/;"/g, '"') // trailing semicolon in style values
    .replace(/<(\w+)([^>]*?)>/g, (_m, tag, attrs) => {
      const list = (attrs.match(/\s[\w:-]+(?:="[^"]*")?/g) ?? []).map((a: string) => a.trim()).sort();
      return `<${tag}${list.length ? " " + list.join(" ") : ""}>`;
    });
}

const ids = process.argv.slice(2);
const nodes = ids.length ? ALL_NODES.filter((n) => ids.includes(n.id)) : ALL_NODES;
let differing = 0;
for (const n of nodes) {
  const policy = n.type === "SRC" ? "source" : "open";
  const before = canon(renderMarkdownUnsanitized(n.bodyMarkdown, policy).html);
  const after = canon(renderMarkdown(n.bodyMarkdown, policy).html);
  if (before === after) continue;
  differing++;
  let i = 0;
  while (i < before.length && before[i] === after[i]) i++;
  console.log(`DIFF ${n.id} at char ${i}\n  before: ...${before.slice(Math.max(0, i - 40), i + 100)}\n  after:  ...${after.slice(Math.max(0, i - 40), i + 100)}`);
}
console.log(`${nodes.length} pages checked, ${differing} differ`);
process.exit(differing ? 1 : 0);

#!/usr/bin/env node
// One-time parser: reads the Obsidian vault and produces lib/graph-data.generated.json
// Run with: node scripts/build-graph.mjs

import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const VAULT = path.join(process.cwd(), "vault");
const OUT = path.join(process.cwd(), "lib", "graph-data.generated.json");

const TYPE_CONFIG = [
  { type: "QUE", dir: "questions", expected: 27 },
  { type: "CLM", dir: "claims", expected: 31 },
  { type: "EVD", dir: "evidence", expected: 77 },
  { type: "CVT", dir: "caveats", expected: 49 },
  { type: "SRC", dir: "source", expected: 27 }, // spec said 28; actual vault has 27 .md files
  { type: "EP", dir: "evd-patterns", expected: 21 },
];

function listMdFiles(dir) {
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isFile() && e.name.toLowerCase().endsWith(".md"))
    .map((e) => e.name)
    .sort((a, b) => a.localeCompare(b));
}

function humanize(v) {
  if (!v) return v;
  return String(v)
    .replace(/[-_]/g, " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/^./, (c) => c.toUpperCase());
}

function mapCurationStatus(nodeFormality, fallbackStatus) {
  if (nodeFormality === "draft") return "Initial AI draft";
  if (nodeFormality === "ReadyForInternal") return "Reviewed";
  if (nodeFormality) return humanize(nodeFormality);
  if (fallbackStatus) return humanize(fallbackStatus);
  return "Unknown";
}

// ---- Pass 1: load all files, assign IDs, build filename -> id lookup ----

const rawNodes = []; // { id, type, filename (no ext), frontmatter, body }
const titleToId = new Map(); // normalized filename -> id

for (const cfg of TYPE_CONFIG) {
  const dir = path.join(VAULT, cfg.dir);
  const files = listMdFiles(dir);
  files.forEach((fname, idx) => {
    const filePath = path.join(dir, fname);
    const raw = fs.readFileSync(filePath, "utf8");
    const { data, content } = matter(raw);
    const filenameNoExt = fname.replace(/\.md$/i, "");
    const id = `${cfg.type}-${String(idx + 1).padStart(3, "0")}`;
    rawNodes.push({
      id,
      type: cfg.type,
      filename: filenameNoExt,
      frontmatter: data || {},
      body: content || "",
    });
    titleToId.set(filenameNoExt.trim().toLowerCase(), id);
  });
  if (files.length !== cfg.expected) {
    console.warn(
      `WARNING: ${cfg.type} (${cfg.dir}) expected ${cfg.expected} files, found ${files.length}`
    );
  }
}

function resolveWikilink(rawTarget) {
  // rawTarget is the text between [[ and ]], possibly "Target|Alias" and "Target#^anchor" / "Target#Section"
  let target = rawTarget.split("|")[0].trim();
  target = target.split("#")[0].trim();
  const id = titleToId.get(target.toLowerCase());
  return id || null;
}

const WIKILINK_RE = /\[\[([^\]]+)\]\]/g;

function extractLinksFromText(text) {
  const out = [];
  let m;
  WIKILINK_RE.lastIndex = 0;
  while ((m = WIKILINK_RE.exec(text))) {
    if (m[1].trim().startsWith("!")) continue; // image embed guard (rare)
    const id = resolveWikilink(m[1]);
    if (id) out.push(id);
  }
  return out;
}

// Extracts the text of a named section (## or ### heading) up to the next heading of same-or-higher level.
function extractSection(body, headingRegexes) {
  const lines = body.split("\n");
  for (const re of headingRegexes) {
    const startIdx = lines.findIndex((l) => re.test(l.trim()));
    if (startIdx === -1) continue;
    const startLevel = (lines[startIdx].match(/^#+/) || ["#"])[0].length;
    let endIdx = lines.length;
    for (let i = startIdx + 1; i < lines.length; i++) {
      const hm = lines[i].match(/^(#+)\s/);
      if (hm && hm[1].length <= startLevel) {
        endIdx = i;
        break;
      }
    }
    return lines.slice(startIdx + 1, endIdx).join("\n");
  }
  return "";
}

// Only wikilinks that are on TOP-LEVEL list items (not nested under indentation) in a section.
function extractTopLevelListLinks(sectionText) {
  const out = [];
  for (const line of sectionText.split("\n")) {
    if (/^-\s/.test(line)) {
      out.push(...extractLinksFromText(line));
    }
  }
  return out;
}

// ---- Pass 2: build edges ----

const edgeSet = new Map(); // key `${type}:${from}:${to}` -> edge object
function addEdge(type, from, to) {
  if (!from || !to || from === to) return;
  const key = `${type}:${from}:${to}`;
  if (!edgeSet.has(key)) edgeSet.set(key, { type, from, to });
}

// pair tracker to dedupe generic `mentions` edges against any typed edge already
// connecting the same two nodes (in either direction)
const connectedPairs = new Set();
function markConnected(a, b) {
  connectedPairs.add(`${a}|${b}`);
  connectedPairs.add(`${b}|${a}`);
}
function isConnected(a, b) {
  return connectedPairs.has(`${a}|${b}`);
}

const byId = new Map(rawNodes.map((n) => [n.id, n]));

for (const n of rawNodes) {
  if (n.type === "QUE") {
    const supportingClaims = extractSection(n.body, [
      /^###\s+Supporting Claims/i,
    ]);
    for (const clmId of extractTopLevelListLinks(supportingClaims)) {
      addEdge("addresses", clmId, n.id);
      markConnected(clmId, n.id);
    }
    const crossPaper = extractSection(n.body, [/^###\s+Cross-paper patterns/i]);
    for (const epId of extractTopLevelListLinks(crossPaper)) {
      addEdge("relatesTo", epId, n.id);
      markConnected(epId, n.id);
    }
  } else if (n.type === "CLM") {
    const supportingEvidence = extractSection(n.body, [
      /^###\s+Supporting Evidence/i,
    ]);
    const groundingEvd = extractSection(n.body, [/^###\s+Grounding EVDs/i]);
    for (const evdId of [
      ...extractTopLevelListLinks(supportingEvidence),
      ...extractLinksFromText(groundingEvd),
    ]) {
      addEdge("supports", evdId, n.id);
      markConnected(evdId, n.id);
    }
  } else if (n.type === "EVD") {
    const caveats = extractSection(n.body, [/^##\s+Caveats/i]);
    for (const cvtId of extractLinksFromText(caveats)) {
      addEdge("qualifies", cvtId, n.id);
      markConnected(cvtId, n.id);
    }
    const supportsClaims = extractSection(n.body, [/^##\s+Supports Claim/i]);
    for (const clmId of extractLinksFromText(supportsClaims)) {
      addEdge("supports", n.id, clmId);
      markConnected(n.id, clmId);
    }
    const sourceSection = extractSection(n.body, [
      /^##\s+Source$/i,
      /^##\s+Source2$/i,
    ]);
    for (const srcId of extractLinksFromText(sourceSection)) {
      addEdge("derivedFrom", n.id, srcId);
      markConnected(n.id, srcId);
    }
    const instantiatesSection = extractSection(n.body, [
      /^##\s+Instantiates Pattern/i,
    ]);
    for (const epId of extractLinksFromText(instantiatesSection)) {
      addEdge("instantiates", n.id, epId);
      markConnected(n.id, epId);
    }
  } else if (n.type === "CVT") {
    // frontmatter appliesTo array
    const appliesTo = n.frontmatter.appliesTo;
    if (Array.isArray(appliesTo)) {
      for (const raw of appliesTo) {
        const m = String(raw).match(/\[\[([^\]]+)\]\]/);
        if (m) {
          const evdId = resolveWikilink(m[1]);
          if (evdId) {
            addEdge("qualifies", n.id, evdId);
            markConnected(n.id, evdId);
          }
        }
      }
    }
    const appliesToSection = extractSection(n.body, [/^###\s+Applies To/i]);
    for (const evdId of extractLinksFromText(appliesToSection)) {
      addEdge("qualifies", n.id, evdId);
      markConnected(n.id, evdId);
    }
  } else if (n.type === "EP") {
    const supportingEvidence = extractSection(n.body, [
      /^##\s+Supporting Evidence/i,
    ]);
    for (const evdId of extractTopLevelListLinks(supportingEvidence)) {
      addEdge("instantiates", evdId, n.id);
      markConnected(evdId, n.id);
    }
    const connected = extractSection(n.body, [
      /^##\s+Connected discourse-graph nodes/i,
    ]);
    for (const targetId of extractLinksFromText(connected)) {
      const target = byId.get(targetId);
      if (target && (target.type === "CLM" || target.type === "EP")) {
        addEdge("relatesTo", n.id, targetId);
        markConnected(n.id, targetId);
      }
    }
  }
}

// SRC: generic `mentions` edges from inline wikilinks throughout the body,
// deduped against any pair already connected by a typed edge.
for (const n of rawNodes) {
  if (n.type !== "SRC") continue;
  const seen = new Set();
  for (const targetId of extractLinksFromText(n.body)) {
    if (targetId === n.id) continue;
    if (isConnected(n.id, targetId)) continue;
    if (seen.has(targetId)) continue;
    seen.add(targetId);
    addEdge("mentions", n.id, targetId);
    markConnected(n.id, targetId);
  }
}

// ---- Pass 3: rewrite wikilinks in body markdown to internal links, strip image embeds ----

function rewriteBody(body) {
  let text = body;
  // strip image embeds ![[...]]
  text = text.replace(/!\[\[[^\]]+\]\]/g, "");
  // rewrite [[Target|Alias]] / [[Target#^anchor]] / [[Target]]
  text = text.replace(/\[\[([^\]]+)\]\]/g, (whole, inner) => {
    const [targetRaw, aliasRaw] = inner.split("|");
    const target = targetRaw.split("#")[0].trim();
    const label = (aliasRaw || targetRaw.split("#")[0]).trim();
    const id = titleToId.get(target.toLowerCase());
    if (id) return `[${label}](/nodes/${id})`;
    return label; // broken link: render as plain text
  });
  return text;
}

// ---- Pass 4: assemble final node objects ----

const PREFIX_LABEL = {
  QUE: "Question",
  CLM: "Claim",
  EVD: "Evidence",
  CVT: "Caveat",
  SRC: "Source",
  EP: "Evidence Pattern",
};

function shortLabel(title, max = 90) {
  if (title.length <= max) return title;
  return title.slice(0, max - 1).trimEnd() + "…";
}

const nodes = rawNodes.map((n) => {
  const fm = n.frontmatter;
  let title = n.filename;
  // strip leading "PREFIX - " and, for SRC, keep the @citekey form as-is
  const prefixMatch = title.match(/^(QUE|CLM|EVD|CVT|EP)\s*-\s*/);
  if (prefixMatch) title = title.slice(prefixMatch[0].length);
  if (n.type === "EVD") {
    // strip trailing " - @citekey"
    title = title.replace(/\s*-\s*@[^-]+$/, "");
  }

  const curationStatus = mapCurationStatus(fm.NodeFormality, fm.status);

  const extras = {};
  if (fm.TruthValue !== undefined) extras.truthValue = fm.TruthValue;
  if (fm.type !== undefined) extras.caveatType = fm.type; // author-stated | inferred
  if (fm.severity !== undefined) extras.severity = fm.severity;
  if (fm.appraisal_overall !== undefined)
    extras.appraisalOverall = fm.appraisal_overall;
  if (fm.tripod_llm_pct !== undefined) extras.tripodLlmPct = fm.tripod_llm_pct;
  if (fm.citekey !== undefined) extras.citekey = fm.citekey;
  if (fm.rating !== undefined) extras.rating = fm.rating;

  return {
    id: n.id,
    type: n.type,
    typeLabel: PREFIX_LABEL[n.type],
    title,
    filename: n.filename,
    shortLabel: shortLabel(title),
    curationStatus,
    tags: Array.isArray(fm.tags) ? fm.tags.filter(Boolean) : [],
    created: fm.created || null,
    updated: fm.updated || null,
    extras,
    bodyMarkdown: rewriteBody(n.body).trim(),
  };
});

const edges = Array.from(edgeSet.values());

// ---- Sanity checks ----

const counts = {};
for (const n of nodes) counts[n.type] = (counts[n.type] || 0) + 1;
console.log("Node counts:", counts);
console.log("Total nodes:", nodes.length, "Total edges:", edges.length);

const edgeTypeCounts = {};
for (const e of edges) edgeTypeCounts[e.type] = (edgeTypeCounts[e.type] || 0) + 1;
console.log("Edge type counts:", edgeTypeCounts);

// Spot check: EP "Human-AI collaboration outperforms either alone" should have
// 2 supporting EVD edges and 2 relatesTo CLM edges.
const spotCheckEp = nodes.find(
  (n) =>
    n.type === "EP" &&
    /Human-AI collaboration outperforms either alone/i.test(n.title)
);
if (spotCheckEp) {
  const supportingEvd = edges.filter(
    (e) => e.type === "instantiates" && e.to === spotCheckEp.id
  );
  const relatesToClm = edges.filter(
    (e) =>
      e.type === "relatesTo" &&
      e.from === spotCheckEp.id &&
      byId.get(e.to)?.type === "CLM"
  );
  console.log(
    `Spot check "${spotCheckEp.title}" (${spotCheckEp.id}): ${supportingEvd.length} supporting EVD edges, ${relatesToClm.length} relatesTo CLM edges`
  );
} else {
  console.warn(
    'WARNING: spot-check EP "Human-AI collaboration outperforms either alone..." not found by title match'
  );
}

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify({ nodes, edges }, null, 2));
console.log(`Wrote ${OUT}`);

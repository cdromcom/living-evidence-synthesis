#!/usr/bin/env node
/**
 * Copies the figure/table screenshots referenced by vault node files into
 * `public/vault-img/` so Next can actually serve them.
 *
 * The crops live in `vault/**\/Attachments/` because that is where Obsidian puts
 * them, and Obsidian is where they are authored. Next only serves `public/`,
 * so without this step every `![[...]]` embed points at a file the browser can
 * never fetch. Copying rather than moving keeps Obsidian working unchanged.
 *
 * Only referenced files are copied — roughly half the attachments on disk are
 * orphans from earlier crops, and there is no reason to ship them. The
 * destination is gitignored: the originals are already committed under vault/,
 * and committing a second copy would double the repo for no benefit.
 */
import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync, rmSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { join, extname, basename, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const VAULT = join(ROOT, "vault");
const OUT = join(ROOT, "public", "vault-img");

const EMBED_RE = /!\[\[([^\]]+)\]\]/g;

/** Every file under a directory tree, recursively. */
function walk(dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

const all = walk(VAULT);
const markdown = all.filter((p) => extname(p) === ".md");

// Index every image on disk by bare filename — embeds reference the filename
// alone, not a path, exactly as Obsidian resolves them.
const byName = new Map();
for (const p of all) {
  if (/\.(png|jpe?g|gif|webp|svg)$/i.test(p)) {
    if (!byName.has(basename(p))) byName.set(basename(p), p);
  }
}

const referenced = new Set();
const referencedBy = new Map();
for (const file of markdown) {
  const text = await readFile(file, "utf8");
  for (const m of text.matchAll(EMBED_RE)) {
    const name = m[1].split("|")[0].trim();
    if (!/\.(png|jpe?g|gif|webp|svg)$/i.test(name)) continue;
    referenced.add(name);
    if (!referencedBy.has(name)) referencedBy.set(name, []);
    referencedBy.get(name).push(basename(file));
  }
}

if (process.argv.includes("--clean") && existsSync(OUT)) rmSync(OUT, { recursive: true });
mkdirSync(OUT, { recursive: true });

let copied = 0;
let skipped = 0;
const missing = [];

for (const name of [...referenced].sort()) {
  const src = byName.get(name);
  if (!src) {
    missing.push(name);
    continue;
  }
  const dest = join(OUT, name);
  // Only copy when absent or stale, so repeat runs during `next dev` are cheap.
  if (existsSync(dest) && statSync(dest).mtimeMs >= statSync(src).mtimeMs) {
    skipped++;
    continue;
  }
  copyFileSync(src, dest);
  copied++;
}

const label = "[attachments]";
console.log(`${label} ${referenced.size} referenced · ${copied} copied · ${skipped} up to date`);

if (missing.length) {
  console.warn(`${label} ${missing.length} referenced image(s) not found in the vault:`);
  for (const name of missing) {
    const where = [...new Set(referencedBy.get(name) || [])];
    console.warn(`${label}   ${name}`);
    for (const w of where.slice(0, 2)) console.warn(`${label}     ← ${w}`);
  }
  console.warn(`${label} Those embeds render as a labelled placeholder rather than a broken image.`);
}

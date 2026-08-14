#!/usr/bin/env node
// Pre-build/pre-dev sanity check. Fails fast with a clear reason instead of
// letting a build silently crawl or get OOM-killed 20 minutes in.
// See README.md "Build reliability" for why this exists.

import { execSync } from "node:child_process";
import os from "node:os";

const MIN_FREE_GB = 2;
const HOG_CPU_PCT = 50;

function warn(msg) {
  console.warn(`\x1b[33m[preflight]\x1b[0m ${msg}`);
}
function fail(msg) {
  console.error(`\x1b[31m[preflight]\x1b[0m ${msg}`);
  process.exit(1);
}

// 1. Free memory
const freeGB = os.freemem() / 1024 ** 3;
if (freeGB < MIN_FREE_GB) {
  warn(
    `only ${freeGB.toFixed(1)}GB free RAM (want >= ${MIN_FREE_GB}GB). ` +
      `A build can hang or get killed under this. Close some apps first.`,
  );
}

// 2. Node version sanity (belt-and-suspenders on top of .nvmrc/engines)
const [major] = process.versions.node.split(".").map(Number);
if (major >= 23) {
  warn(
    `running on Node ${process.versions.node}, which is newer than this ` +
      `project's pinned/tested version (see .nvmrc). If the build hangs or ` +
      `crashes with no clear error, try the pinned version first.`,
  );
}

// 3. Competing heavy processes (best-effort, macOS/Linux `ps`; skip on other platforms)
try {
  const out = execSync("ps -eo pcpu,comm", { encoding: "utf8" });
  const hogs = out
    .split("\n")
    .slice(1)
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => {
      const [pct, ...rest] = l.split(/\s+/);
      return { pct: parseFloat(pct), name: rest.join(" ") };
    })
    .filter((p) => p.pct >= HOG_CPU_PCT);
  if (hogs.length) {
    warn(
      `heavy CPU usage detected (>${HOG_CPU_PCT}%): ` +
        hogs.map((h) => `${h.name} (${h.pct}%)`).join(", ") +
        ". This will slow the build and can look like a hang. Consider closing it.",
    );
  }
} catch {
  // ps not available or failed — non-fatal, just skip this check.
}

// 4. Another next build/dev already running against this project?
try {
  const out = execSync("ps -eo command", { encoding: "utf8" });
  const matches = out
    .split("\n")
    .filter((l) => /next (build|dev|start)/.test(l) && !l.includes("preflight"));
  if (matches.length > 1) {
    fail(
      "another `next build`/`dev`/`start` process appears to already be running. " +
        "Running two at once against the same .next directory causes races and " +
        "unreliable failures — stop the other one first (see README).",
    );
  }
} catch {
  // non-fatal
}

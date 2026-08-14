# Build postmortem: bugs, dead ends, and fixes

This documents a long debugging session getting the first `next build` of
this project to succeed. It's written for whoever hits a similar "build
just won't finish" wall — several of the things that looked like the
problem weren't, and the actual fixes are cheap once you know them.

**Symptom:** `next build` (Next.js 16.3.1) either got killed
(`exit 137` / SIGKILL) or appeared to hang indefinitely at "Creating an
optimized production build...", with no error message, across many
consecutive attempts.

## What it actually was (in the order we found them)

### 1. Two builds racing on the same `.next` directory
Two separate processes (an automated agent still iterating in the
background, and a person debugging in parallel) each ran `next build`
against the same project folder at the same time, both doing a clean wipe
of `.next` first. That alone produces confusing, inconsistent failures.

**Fix:** never run two `build`/`dev`/`start` invocations against one
project concurrently. We now enforce this with an atomic `mkdir`-based
lock (`scripts/with-lock.sh`) wrapping `npm run dev`/`build` — a second
concurrent attempt fails immediately with a clear message instead of
racing silently.

### 2. `outputFileTracingRoot` was scanning the entire home directory
Every build log carried this easy-to-miss warning:
```
Next.js ignored package-lock.json in /Users/<you> because it is outside
the current Git repository. To use this directory, set
`outputFileTracingRoot` in your Next.js config.
```
A stray lockfile one level above the project made Next infer the
workspace root as the *entire home folder*, so its output-file-tracing
step walked a huge, unrelated directory tree.

**Fix:** set it explicitly in `next.config.mjs`:
```js
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
const __dirname = dirname(fileURLToPath(import.meta.url));

const nextConfig = {
  outputFileTracingRoot: __dirname,
  // ...
};
```
This was a real bug worth fixing, but on its own it did not resolve the
hangs — there was more going on.

### 3. Resource contention from other running apps
A browser (Firefox) with several hundred open tabs was consuming 80%+ CPU
and multi-GB of RAM at the exact times builds were failing. On a machine
under that much pressure, a legitimately CPU/memory-hungry cold build can
get starved or OOM-killed by the OS.

**Fix (partial):** closing the browser freed real memory and let the build
progress further than any previous attempt. But it *still* eventually
failed afterward — this was a real contributing factor, not the root
cause.

**Prevention:** `scripts/preflight.mjs` now runs automatically before
`dev`/`build` and warns if free RAM is low or any process is using >50%
CPU, so this gets caught in seconds instead of after a 20-minute failed
build.

### 4. Dead end: "the SWC binary is 0 bytes / the install is broken"
A `du -sh` reading on `node_modules/@next/swc-darwin-arm64` briefly showed
`0B`, which looked like a corrupted native binary. This was a **false
alarm** — a transient/flaky filesystem read. `ls -la` and `file` on the
same path immediately after showed a perfectly valid 85MB Mach-O binary.

**Lesson:** cross-check a suspicious disk-usage reading with a second,
different tool (`ls -la`, `file`) before trusting it as a root cause.

### 5. Misdiagnosis: throttling to 1 CPU core made it *look* more broken
After a build died with a genuine `SIGKILL` on the compile worker, we
capped concurrency (`experimental.cpus: 1`, `workerThreads: false`) to
reduce peak memory. The next attempt then sat at what looked like 0% CPU
for many minutes — which we initially read as "still hung."

**It wasn't.** A proper stack sample proved the process was continuously,
busily executing real work (webpack's file-system module resolution:
`fs.readFileUtf8`, `fs.lstat`, V8 object/hash-map construction) — it was
just single-threaded now, and therefore much slower, because of the
throttling *we* had just applied.

```bash
# macOS: take a 5-second stack sample of a process that "looks" stuck
sample <pid> 5
```
This is the single most useful command from this whole session. `ps`'s
coarse, decayed CPU% column can read near-zero even while a process is
genuinely saturating a core — it is not reliable evidence of a hang.

**Fix:** removed the concurrency cap, kept the legitimate fixes (`
outputFileTracingRoot`, `experimental.webpackMemoryOptimizations: true`,
`productionBrowserSourceMaps: false`), and let it run with normal
concurrency.

### 6. The actual remaining cause: Node version skew
The system's global Node was v25.8.1 — newer than what Next.js
16.3.1's webpack build-worker plumbing (and, separately, Turbopack) had
clearly been tested against in this environment. Both bundlers exhibited
the same "technically alive, suspiciously slow/quiet" behavior under it.

**Fix:** ran the build under Node 22 LTS instead. Since no nvm/fnm/volta
was installed, we downloaded the official Node 22 tarball into a
project-local, non-invasive folder (`.node-local/`, gitignored) rather
than touching the machine's global Node install:
```bash
curl -fsSL -o node22.tar.gz \
  "https://nodejs.org/dist/v22.14.0/node-v22.14.0-darwin-arm64.tar.gz"
tar -xzf node22.tar.gz
```
This, combined with reverting the concurrency throttling from #5, is what
finally produced a clean build: compiled in 2.3 min, typechecked in
9.5 min with zero errors, generated all 242 static pages in 2.9s.

**Prevention:** `.nvmrc` + `package.json#engines` now pin Node 22.
`scripts/with-lock.sh` transparently prepends the local Node 22 install to
`PATH` when present, so `npm run dev`/`build` use it automatically without
anyone needing to remember the workaround.

## Net result

| Symptom seen | Real cause | Fix |
|---|---|---|
| Random, inconsistent build failures | Two builds racing on one `.next` dir | `scripts/with-lock.sh` (atomic lock) |
| Warning about ignored lockfile | `outputFileTracingRoot` unset, scanning whole home dir | Set explicitly in `next.config.mjs` |
| SIGKILL / OOM-looking failures | Other apps (browser, etc.) starving CPU/RAM | `scripts/preflight.mjs` (pre-run resource check) |
| "0 byte" native binary | Flaky `du` reading, not a real bug | N/A — false alarm, verified and moved on |
| Build looked frozen at 0% CPU | Self-inflicted: throttled to 1 core while diagnosing | Removed throttling; verified activity with `sample`, not `ps` |
| Builds crawling / silently stalling under both webpack and Turbopack | Node version too new for this Next.js version | Pinned Node 22 via a local, non-global install |

## Diagnostic technique worth keeping

If a build/process looks hung, don't trust `ps` CPU%/RSS alone and don't
guess-and-check with config flags. Take a real stack sample first:
```bash
sample <pid> 5          # macOS
# or, for a Node-specific view:
node --prof ...          # then `node --prof-process` on the output
```
If it shows real, changing stack frames doing real work, it's slow, not
stuck — the fix is patience or parallelism, not more flags. If it shows
the exact same frame every time, it's genuinely stuck, and *that* frame
tells you what it's stuck on.

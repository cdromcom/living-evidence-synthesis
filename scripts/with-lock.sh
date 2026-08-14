#!/bin/sh
# Wraps a command with an atomic mkdir-based lock so two builds/dev-servers
# can never run against this project at once (this bit us badly once —
# see README.md "Build reliability").
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCK_DIR="$SCRIPT_DIR/../.build.lock"

# Prefer the project-local Node 22 install (no nvm on this machine, and the
# system Node has been observed to be too new for this Next.js version —
# see README.md "Build reliability" #1). Falls back to whatever's on PATH.
LOCAL_NODE="$SCRIPT_DIR/../.node-local/node-v22.14.0-darwin-arm64/bin"
if [ -d "$LOCAL_NODE" ]; then
  PATH="$LOCAL_NODE:$PATH"
  export PATH
fi

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "\033[31m[with-lock]\033[0m Another build/dev/start is already running" \
       "(lock dir exists: $LOCK_DIR)." >&2
  echo "If you're sure nothing is actually running, remove it manually: rm -rf '$LOCK_DIR'" >&2
  exit 1
fi

cleanup() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

"$@"

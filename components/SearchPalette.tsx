"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Fuse from "fuse.js";
import { Search } from "lucide-react";
import { ALL_NODES } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";

export default function SearchPalette() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const fuse = useMemo(
    () =>
      new Fuse(ALL_NODES, {
        keys: ["title", "tags", "id"],
        threshold: 0.35,
      }),
    []
  );

  const results = useMemo(() => {
    if (!query.trim()) return [];
    return fuse.search(query).slice(0, 8);
  }, [fuse, query]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    if (open) {
      setQuery("");
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [open]);

  function goTo(id: string) {
    setOpen(false);
    router.push(`/nodes/${id}`);
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="flex items-center gap-2 rounded-md border border-border bg-card px-2.5 py-1.5 text-sm text-muted-ink transition-colors hover:border-forest hover:text-ink"
      >
        <Search className="h-3.5 w-3.5" aria-hidden />
        <span className="hidden sm:inline">Search</span>
        <kbd className="mono hidden rounded border border-border bg-muted-surface px-1.5 py-0.5 text-[0.65rem] text-muted-ink sm:inline">
          ⌘K
        </kbd>
      </button>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-start justify-center bg-ink/40 px-4 pt-24"
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-lg overflow-hidden rounded-lg border border-border bg-card shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <input
              ref={inputRef}
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && results.length > 0) {
                  goTo(results[0].item.id);
                }
              }}
              placeholder="Search nodes by title, tag, or id…"
              className="w-full border-b border-border bg-transparent px-4 py-3 text-sm text-ink placeholder:text-muted-ink focus:outline-none"
            />
            <ul className="max-h-96 overflow-y-auto">
              {results.length === 0 && query.trim() && (
                <li className="px-4 py-3 text-sm text-muted-ink">No matches.</li>
              )}
              {results.map((r) => (
                <li key={r.item.id}>
                  <button
                    type="button"
                    onClick={() => goTo(r.item.id)}
                    className="flex w-full items-center gap-2 px-4 py-2.5 text-left text-sm hover:bg-muted-surface"
                  >
                    <NodeTypeBadge type={r.item.type} />
                    <span className="truncate">{r.item.title}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </>
  );
}

"use client";

import Link from "next/link";
import { useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import Fuse from "fuse.js";
import { NotebookText } from "lucide-react";
import { ALL_NODES } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";
import ThemeToggle from "./ThemeToggle";
import AuthStatus from "./AuthStatus";

const METHOD_SOURCE_URL =
  "https://github.com/oasisresearchlab/language-and-health-open-synthesis/tree/review-app-prototype/discourse-extraction";

const NAV = [
  { href: "/graph", label: "Graph" },
  { href: "/narratives", label: "Narratives" },
  { href: "/nodes", label: "Nodes" },
  { href: "/review", label: "Review" },
  { href: "/contribute", label: "Contribute" },
  { href: "/about", label: "About" },
];

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" className={className}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.847-2.339 4.695-4.566 4.943.359.31.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z"
      />
    </svg>
  );
}

export default function Header() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
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

  function goTo(id: string) {
    setOpen(false);
    setQuery("");
    inputRef.current?.blur();
    router.push(`/nodes/${id}`);
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-paper/85 backdrop-blur supports-[backdrop-filter]:bg-paper/65">
      <div className="mx-auto flex h-14 max-w-6xl items-center gap-6 px-4 sm:px-6">
        <Link
          href="/"
          className="flex shrink-0 items-center gap-2 font-heading text-base font-semibold tracking-tight"
        >
          <NotebookText className="h-5 w-5 text-forest" aria-hidden />
          <span>Living Evidence Synthesis</span>
        </Link>

        <nav className="hidden items-center gap-5 text-sm text-muted-ink md:flex">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="transition-colors hover:text-ink"
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          <div className="relative w-40 sm:w-64">
            <input
              ref={inputRef}
              type="search"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setOpen(true);
              }}
              onFocus={() => setOpen(true)}
              onBlur={() => setTimeout(() => setOpen(false), 120)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && results.length > 0) {
                  goTo(results[0].item.id);
                }
              }}
              placeholder="Search nodes…"
              className="w-full rounded-md border border-border bg-card px-3 py-1.5 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
            />
            {open && results.length > 0 && (
              <ul className="absolute right-0 z-50 mt-1 w-72 overflow-hidden rounded-md border border-border bg-card shadow-sm">
                {results.map((r) => (
                  <li key={r.item.id}>
                    <button
                      type="button"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={() => goTo(r.item.id)}
                      className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-muted-surface"
                    >
                      <NodeTypeBadge type={r.item.type} typeLabel={r.item.type} />
                      <span className="truncate">{r.item.title}</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <a
            href={METHOD_SOURCE_URL}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View the discourse-extraction methodology source"
            className="inline-flex h-8 w-8 items-center justify-center rounded-md text-muted-ink transition-colors hover:bg-secondary-surface hover:text-ink"
          >
            <GithubIcon className="h-4 w-4" />
          </a>

          <AuthStatus />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}

"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import Fuse from "fuse.js";
import type { GraphNode, NodeType } from "@/lib/data";
import { NODE_TYPE_ORDER, getDegree } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";
import StatusBadge from "./StatusBadge";

type SortKey = "relevance" | "title" | "degree" | "updated";

export default function NodesExplorer({ nodes }: { nodes: GraphNode[] }) {
  const searchParams = useSearchParams();
  const initialType = searchParams.get("type") as NodeType | null;

  const [query, setQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState<Set<NodeType>>(
    new Set(initialType ? [initialType] : [])
  );
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [sortKey, setSortKey] = useState<SortKey>("title");

  const fuse = useMemo(
    () => new Fuse(nodes, { keys: ["title", "tags", "id"], threshold: 0.35 }),
    [nodes]
  );

  const statuses = useMemo(
    () => Array.from(new Set(nodes.map((n) => n.curationStatus))).sort(),
    [nodes]
  );

  const filtered = useMemo(() => {
    let list = query.trim() ? fuse.search(query).map((r) => r.item) : nodes;
    if (typeFilter.size > 0) {
      list = list.filter((n) => typeFilter.has(n.type));
    }
    if (statusFilter !== "all") {
      list = list.filter((n) => n.curationStatus === statusFilter);
    }
    const sorted = [...list];
    if (sortKey === "title") {
      sorted.sort((a, b) => a.title.localeCompare(b.title));
    } else if (sortKey === "degree") {
      sorted.sort((a, b) => getDegree(b.id) - getDegree(a.id));
    } else if (sortKey === "updated") {
      sorted.sort((a, b) => (b.updated || "").localeCompare(a.updated || ""));
    }
    return sorted;
  }, [query, fuse, nodes, typeFilter, statusFilter, sortKey]);

  function toggleType(t: NodeType) {
    setTypeFilter((prev) => {
      const next = new Set(prev);
      if (next.has(t)) next.delete(t);
      else next.add(t);
      return next;
    });
  }

  return (
    <div>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by title or tag…"
          className="w-full max-w-sm rounded-md border border-border bg-card px-3 py-2 text-sm focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
        />
        <div className="flex items-center gap-2 text-sm">
          <label className="text-muted-ink">Sort</label>
          <select
            value={sortKey}
            onChange={(e) => setSortKey(e.target.value as SortKey)}
            className="rounded-md border border-border bg-card px-2 py-1.5 text-sm"
          >
            <option value="title">Title</option>
            <option value="degree">Connections</option>
            <option value="updated">Recently updated</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        {NODE_TYPE_ORDER.map((t) => (
          <button
            key={t}
            onClick={() => toggleType(t)}
            className={`rounded-full border px-3 py-1 text-xs font-semibold transition-colors ${
              typeFilter.has(t)
                ? "border-forest bg-forest text-paper"
                : "border-border bg-card text-ink/80 hover:bg-muted-surface"
            }`}
          >
            {t}
          </button>
        ))}
        <span className="mx-1 h-4 w-px bg-border" />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded-full border border-border bg-card px-3 py-1 text-xs"
        >
          <option value="all">All statuses</option>
          {statuses.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        {(typeFilter.size > 0 || statusFilter !== "all" || query) && (
          <button
            onClick={() => {
              setTypeFilter(new Set());
              setStatusFilter("all");
              setQuery("");
            }}
            className="text-xs text-muted-ink underline underline-offset-2 hover:text-forest"
          >
            Clear filters
          </button>
        )}
        <span className="mono ml-auto text-xs text-muted-ink">
          {filtered.length} of {nodes.length}
        </span>
      </div>

      <ul className="mt-5 grid gap-2 sm:grid-cols-2">
        {filtered.map((n) => (
          <li key={n.id}>
            <Link
              href={`/nodes/${n.id}`}
              className="block rounded-lg border border-border bg-card p-3.5 transition-colors hover:border-forest/40"
            >
              <div className="mb-1.5 flex items-center justify-between gap-2">
                <NodeTypeBadge type={n.type} typeLabel={n.typeLabel} />
                <span className="mono text-[0.65rem] text-muted-ink">{n.id}</span>
              </div>
              <p className="text-sm leading-snug">{n.shortLabel}</p>
              <div className="mt-2 flex items-center justify-between">
                <StatusBadge status={n.curationStatus} />
                <span className="text-[0.65rem] text-muted-ink">
                  {getDegree(n.id)} connections
                </span>
              </div>
            </Link>
          </li>
        ))}
      </ul>
      {filtered.length === 0 && (
        <p className="mt-8 text-center text-sm text-muted-ink">
          No nodes match these filters.
        </p>
      )}
    </div>
  );
}

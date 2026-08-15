"use client";

import { useMemo, useState } from "react";
import Fuse from "fuse.js";
import { ALL_NODES, type NodeType } from "@/lib/data";
import NodeTypeBadge from "./NodeTypeBadge";

export default function NodePicker({
  label,
  hint,
  targetType,
  value,
  onChange,
}: {
  label: string;
  hint: string;
  targetType: NodeType;
  value: string[];
  onChange: (ids: string[]) => void;
}) {
  const [query, setQuery] = useState("");
  const candidates = useMemo(
    () => ALL_NODES.filter((n) => n.type === targetType),
    [targetType]
  );
  const fuse = useMemo(
    () => new Fuse(candidates, { keys: ["title", "id"], threshold: 0.35 }),
    [candidates]
  );
  const results = useMemo(() => {
    if (!query.trim()) return [];
    return fuse.search(query).slice(0, 6);
  }, [fuse, query]);

  function add(id: string) {
    if (!value.includes(id)) onChange([...value, id]);
    setQuery("");
  }
  function remove(id: string) {
    onChange(value.filter((v) => v !== id));
  }

  return (
    <div>
      <label className="block text-xs font-semibold uppercase tracking-wide text-muted-ink">
        {label}
      </label>
      <p className="mt-0.5 text-xs text-muted-ink">{hint}</p>

      {value.length > 0 && (
        <ul className="mt-2 flex flex-wrap gap-1.5">
          {value.map((id) => {
            const node = ALL_NODES.find((n) => n.id === id);
            return (
              <li
                key={id}
                className="flex items-center gap-1.5 rounded-full border border-border bg-muted-surface px-2 py-1 text-xs"
              >
                <span className="mono">{id}</span>
                <span className="max-w-[16rem] truncate">{node?.title}</span>
                <button
                  type="button"
                  onClick={() => remove(id)}
                  aria-label={`Remove ${id}`}
                  className="text-muted-ink hover:text-destructive"
                >
                  ×
                </button>
              </li>
            );
          })}
        </ul>
      )}

      <div className="relative mt-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={`Search ${targetType} nodes by title…`}
          className="w-full rounded-md border border-border bg-paper px-3 py-1.5 text-sm text-ink placeholder:text-muted-ink focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
        />
        {results.length > 0 && (
          <ul className="absolute z-20 mt-1 w-full overflow-hidden rounded-md border border-border bg-card shadow-sm">
            {results.map((r) => (
              <li key={r.item.id}>
                <button
                  type="button"
                  onClick={() => add(r.item.id)}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-muted-surface"
                >
                  <NodeTypeBadge type={r.item.type} />
                  <span className="mono text-xs text-muted-ink">{r.item.id}</span>
                  <span className="truncate">{r.item.title}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

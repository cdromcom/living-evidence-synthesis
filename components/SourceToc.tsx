import type { TocItem } from "@/lib/markdown";

/**
 * A persistent outline of a source page's headings, docked in the left
 * margin. Always visible/expanded — no hover or click needed to read it.
 */
export default function SourceToc({ items }: { items: TocItem[] }) {
  if (items.length === 0) return null;

  return (
    <nav
      aria-label="Table of contents"
      className="sticky top-20 hidden w-48 shrink-0 self-start lg:block"
    >
      <p className="mb-1.5 whitespace-nowrap text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
        On this page
      </p>
      <ol className="space-y-1.5 border-l border-border py-0.5 pl-3">
        {items.map((h) => (
          <li key={h.id} className={h.level === 3 ? "ml-3" : undefined}>
            <a
              href={`#${h.id}`}
              className="block whitespace-nowrap text-xs leading-snug text-muted-ink hover:text-forest"
            >
              {h.text}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

import type { TocItem } from "@/lib/markdown";

/**
 * A minimal, hover-to-expand outline of a source page's headings. At rest
 * it's just a rail of small ticks (unobtrusive); hovering the rail widens
 * it and reveals the heading text, each a real link to that section.
 */
export default function SourceToc({ items }: { items: TocItem[] }) {
  if (items.length === 0) return null;

  return (
    <nav
      aria-label="Table of contents"
      className="group sticky top-20 hidden w-6 shrink-0 overflow-hidden transition-[width] duration-200 hover:w-64 lg:block"
    >
      <p className="mb-1.5 whitespace-nowrap text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink opacity-0 transition-opacity duration-150 group-hover:opacity-100">
        On this page
      </p>
      <ol className="space-y-1.5 border-l border-border py-0.5 pl-3">
        {items.map((h) => (
          <li key={h.id} className={h.level === 3 ? "ml-3" : undefined}>
            <a
              href={`#${h.id}`}
              className="flex h-[3px] items-center gap-2 rounded-full transition-all duration-150 group-hover:h-auto"
            >
              <span aria-hidden className="h-[3px] w-4 shrink-0 rounded-full bg-border group-hover:bg-forest" />
              <span className="hidden whitespace-nowrap text-xs text-muted-ink group-hover:inline hover:text-forest">
                {h.text}
              </span>
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

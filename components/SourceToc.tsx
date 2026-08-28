import type { TocItem } from "@/lib/markdown";

/**
 * A persistent outline of a source page's headings, docked in the left
 * margin. Always visible/expanded — no hover or click needed to read it.
 * Sticky (not fixed): it scrolls normally with the page until it reaches
 * `top-20`, then holds there so clicking one heading link after another
 * doesn't require scrolling back up each time — and once you scroll back
 * up past where the TOC originally sat (e.g. back to the top of the page),
 * it un-sticks and returns to that original position automatically, since
 * that's how CSS position:sticky behaves relative to its own container.
 */
export default function SourceToc({ items }: { items: TocItem[] }) {
  if (items.length === 0) return null;

  return (
    <nav aria-label="Table of contents" className="sticky top-20 hidden lg:block">
      <p className="mb-1.5 whitespace-nowrap text-[0.6875rem] font-semibold uppercase tracking-wide text-muted-ink">
        On this page
      </p>
      <ol className="space-y-1.5 border-l border-border py-0.5 pl-3">
        {items.map((h) => (
          <li key={h.id} className={h.level === 3 ? "ml-3" : undefined}>
            <a
              href={`#${h.id}`}
              className="block text-xs leading-snug text-muted-ink hover:text-forest"
            >
              {h.text}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

import Link from "next/link";
import { promptsFor } from "@/lib/promptTactics";

/**
 * The prompts a paper reports, collapsed until asked for.
 *
 * The same fragments already sit in the TRIPOD-LLM table, but spread across
 * rows 9a, 6c, 6d and 9b in a table that is itself collapsed — so "what did
 * they actually type at the model" is recoverable but not findable. This
 * gathers them in reading order behind one disclosure, on the pages where the
 * question comes up: a Source page, and an Evidence page via its parent.
 *
 * Rendered server-side; `<details>` needs no JavaScript to open.
 */
export default function PromptDetail({
  srcId,
  inherited = false,
  className = "",
}: {
  /** The Source whose prompts to show. */
  srcId: string;
  /** True when shown on an EVD page, where the prompts belong to its parent. */
  inherited?: boolean;
  className?: string;
}) {
  const prompts = promptsFor(srcId);
  if (prompts.length === 0) return null;

  return (
    <details className={`rounded-md border border-border bg-card ${className}`}>
      <summary className="flex cursor-pointer list-none items-center gap-2 px-3 py-2 text-[0.6875rem] text-muted-ink transition-colors hover:text-ink">
        <svg
          width="13"
          height="13"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden
        >
          <path d="M4 6h16M4 12h10M4 18h13" />
        </svg>
        <span>
          {prompts.length === 1 ? "1 prompt reported" : `${prompts.length} prompts reported`}
          {inherited && " by the source paper"}
        </span>
      </summary>

      <div className="border-t border-border px-3 pb-3 pt-2">
        {inherited && (
          <p className="mb-2 text-[0.6875rem] text-muted-ink">
            Read from{" "}
            <Link href={`/nodes/${srcId}`} className="text-forest hover:underline">
              {srcId}
            </Link>
            , the paper this evidence comes from.
          </p>
        )}
        <ul className="space-y-3">
          {prompts.map((p, i) => (
            <li key={`${p.item}-${i}`}>
              <p className="font-mono text-[0.625rem] uppercase tracking-wide text-muted-ink">
                {p.label}
                <span className="ml-1.5 text-border">TRIPOD {p.item}</span>
              </p>
              <blockquote className="mt-1 border-l-2 border-forest pl-2.5 text-[0.8125rem] italic leading-relaxed text-ink/90">
                {p.text}
              </blockquote>
              {p.locator && (
                <p className="mt-1 font-mono text-[0.625rem] text-muted-ink">{p.locator}</p>
              )}
            </li>
          ))}
        </ul>
        <p className="mt-3 border-t border-border pt-2 text-[0.625rem] text-muted-ink">
          Quoted verbatim from the paper.{" "}
          <Link href="/prompts" className="text-forest hover:underline">
            Compare prompting across all 27 sources →
          </Link>
        </p>
      </div>
    </details>
  );
}

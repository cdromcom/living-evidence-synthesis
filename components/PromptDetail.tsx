import Link from "next/link";
import { PROMPT_TACTICS, promptsFor } from "@/lib/promptTactics";

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
  const row = PROMPT_TACTICS.find((r) => r.srcId === srcId);
  const full = row?.fullPrompts ?? [];
  if (prompts.length === 0 && full.length === 0) return null;

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
          {full.length > 0
            ? "Prompt in full"
            : prompts.length === 1
              ? "1 prompt reported"
              : `${prompts.length} prompts reported`}
          {inherited && (full.length > 0 ? ", from the source paper" : " by the source paper")}
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
        {full.length > 0 && (
          <div className="mb-3">
            {full.map((f) => (
              <div key={f.role} className="mb-3 last:mb-0">
                <p className="font-mono text-[0.625rem] uppercase tracking-wide text-muted-ink">
                  {f.role}
                </p>
                {/* Kept as-sent: line breaks and numbering are part of the prompt. */}
                <pre className="mt-1 overflow-x-auto whitespace-pre-wrap rounded-r border-l-2 border-forest bg-muted-surface px-3 py-2 font-mono text-[0.75rem] leading-relaxed text-ink">
                  {f.text}
                </pre>
              </div>
            ))}
            {row?.fullPromptSource && (
              <p className="font-mono text-[0.625rem] text-muted-ink">{row.fullPromptSource}</p>
            )}
            {prompts.length > 0 && (
              <p className="mt-3 border-t border-border pt-2 text-[0.6875rem] text-muted-ink">
                As recorded against the TRIPOD-LLM checklist:
              </p>
            )}
          </div>
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

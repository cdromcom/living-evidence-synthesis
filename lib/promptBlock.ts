import "server-only";
import { PROMPT_TACTICS, promptsFor } from "@/lib/promptTactics";

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

/**
 * The prompts disclosure as an HTML string.
 *
 * Node bodies are injected with `dangerouslySetInnerHTML`, so a React component
 * cannot be placed inside them. This renders the same block as
 * `components/PromptDetail.tsx` for the one case that has to live *within* the
 * article: alongside the Procedure it describes. Server-only, and it emits a
 * plain `<details>`, so it needs no JavaScript to open.
 *
 * Both are driven by the same data, so they cannot disagree about what a paper
 * reported — only about where the block is placed.
 */
export function promptBlockHtml(srcId: string, opts: { inherited?: boolean } = {}): string {
  const prompts = promptsFor(srcId);
  const row = PROMPT_TACTICS.find((r) => r.srcId === srcId);
  const full = row?.fullPrompts ?? [];
  if (prompts.length === 0 && full.length === 0) return "";

  const label = full.length
    ? `Prompt in full${opts.inherited ? ", from the source paper" : ""}`
    : `${prompts.length} prompt${prompts.length === 1 ? "" : "s"} reported${
        opts.inherited ? " by the source paper" : ""
      }`;

  // When the PDF prints the prompt in full, that is what a reader wants; the
  // TRIPOD excerpts stay underneath as the shorter, quotable record.
  const fullHtml = full.length
    ? `<div class="prompt-full">` +
      full
        .map(
          (p) =>
            `<p class="prompt-role">${esc(p.role)}</p>` +
            `<pre class="prompt-verbatim">${esc(p.text)}</pre>`
        )
        .join("") +
      (row?.fullPromptSource
        ? `<p class="prompt-locator">${esc(row.fullPromptSource)}</p>`
        : "") +
      `</div>`
    : "";

  const excerptHtml = prompts.length
    ? `<ul class="prompt-excerpts">` +
      prompts
        .map(
          (p) =>
            `<li><p class="prompt-role">${esc(p.label)}` +
            `<span class="prompt-item">TRIPOD ${esc(p.item)}</span></p>` +
            `<blockquote>${esc(p.text)}</blockquote>` +
            (p.locator ? `<p class="prompt-locator">${esc(p.locator)}</p>` : "") +
            `</li>`
        )
        .join("") +
      `</ul>`
    : "";

  return (
    `<details class="prompt-detail">` +
    `<summary>${esc(label)}</summary>` +
    `<div class="prompt-detail-body">` +
    fullHtml +
    (fullHtml && excerptHtml
      ? `<p class="prompt-sep">As recorded against the TRIPOD-LLM checklist:</p>`
      : "") +
    excerptHtml +
    `<p class="prompt-foot">Quoted verbatim. <a href="/prompts">Compare prompting across all 27 sources →</a></p>` +
    `</div></details>`
  );
}

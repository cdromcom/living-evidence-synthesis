import PromptTacticsExplorer from "@/components/PromptTacticsExplorer";
import { PROMPT_TACTICS } from "@/lib/promptTactics";

export const metadata = {
  title: "Prompt Tactics — Living Evidence Synthesis",
  description:
    "How the 27 source papers actually prompted their LLMs, coded across eleven dimensions with the prompt each paper reports.",
};

export default function PromptTacticsPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <p className="mb-3 font-mono text-[0.6875rem] uppercase tracking-wide text-muted-ink">
        Methods audit
      </p>
      <h1 className="max-w-[22ch] text-2xl font-semibold leading-tight">
        Prompt tactics across {PROMPT_TACTICS.length} reviews
      </h1>
      <p className="mt-3 max-w-[65ch] text-sm leading-relaxed text-muted-ink">
        Every source in the corpus asks an LLM to appraise a paper. Almost none of them treat{" "}
        <strong className="text-ink">how they ask</strong> as a variable. This grid pulls the
        prompting method out of all {PROMPT_TACTICS.length} sources and sorts it along eleven
        dimensions, so the design space the literature has actually explored, and the parts it has
        left untouched, are visible at once.
      </p>
      <p className="mt-4 max-w-[70ch] border-t border-border pt-3 font-mono text-[0.6875rem] leading-relaxed text-muted-ink">
        Coded by hand from each source&apos;s TRIPOD-LLM item 9a (prompt design), 6c (inference
        settings) and 6d (output), cross-checked against its Methods section. Quotes are verbatim.
        Coding is conservative: a tactic is marked only where the source states it, so &ldquo;not
        used&rdquo; and &ldquo;not reported&rdquo; collapse into the same mark. Click any source for
        the evidence behind its row.
      </p>

      <PromptTacticsExplorer rows={PROMPT_TACTICS} />
    </main>
  );
}

import Link from "next/link";
import type { ReactNode } from "react";

export const metadata = { title: "Narratives — Living Evidence Synthesis" };

function N({ id, children }: { id: string; children: ReactNode }) {
  return (
    <Link
      href={`/nodes/${id}`}
      className="text-forest"
    >
      {children}
    </Link>
  );
}

export default function NarrativesPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-semibold">Narratives</h1>
      <p className="mt-1 text-sm text-muted-ink">
        Linear readings composed from the graph. Entry into this corpus is
        normally non-linear; you can explore <Link className="text-forest" href="/graph">the graph</Link> or{" "}
        <Link className="text-forest" href="/nodes">browse nodes</Link> directly.
        These essays instead walk through three of its strongest cross-cutting
        findings, citing through to the underlying nodes at every step.
      </p>

      <article className="prose-node mt-10">
        <h2 className="text-xl font-semibold">
          Can LLMs replace human peer reviewers?
        </h2>
        <p>
          Not on their own, but they get closer than a skeptic might expect;
          closer on some dimensions than others. On raw prediction, LLM
          systems can hit near-human accuracy: <N id="EP-010">LLM peer-review systems can predict paper acceptance and preference at near-human accuracy</N>{" "}
          is instantiated by a Generative Adversarial Reviewer that reached an{" "}
          <N id="EVD-022">F1 of 0.66 on ICLR&apos;23 acceptance prediction against a 0.49 human baseline</N>,
          and by a fine-tuned OpenReviewer model that{" "}
          <N id="EVD-069">won 60% of head-to-head preference evaluations against GPT-4o and 76% against Llama-3.1-70B</N>. Users
          also report the feedback itself is genuinely useful, not boilerplate:{" "}
          <N id="EP-021">users find LLM-generated peer-review feedback substantively helpful at rates comparable to human reviewers</N>, with{" "}
          <N id="EVD-002">57.4% of 308 researchers finding GPT-4 feedback helpful, and 82.4% finding it more beneficial than at least some human reviewers</N>{" "}
          they had received.
        </p>
        <p>
          But there is a systematic bias underneath those numbers: general-purpose
          models are lenient graders. <N id="EP-005">General-purpose LLMs systematically over-rate papers compared to human reviewers</N>.
          On the same 400 NeurIPS/ICLR papers,{" "}
          <N id="EVD-067">GPT-4o averaged a recommendation of 7.7 versus a human average of 5.4</N>, and{" "}
          <N id="EVD-068">a fine-tuned reviewer matched at least one human recommendation on 55.5% of papers versus 23.8% for GPT-4o</N>. This
          is exactly what <N id="CLM-010">general-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions</N>{" "}
          claims, and it is why <N id="CLM-030">specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments</N>{" "}
          shows up as a distinct, better-supported claim rather than a footnote. The
          practical upshot: an LLM reviewer trained generically will be a soft touch; one
          fine-tuned specifically on review data closes most of that gap.
        </p>
      </article>

      <article className="prose-node mt-14 border-t border-border pt-10">
        <h2 className="text-xl font-semibold">
          Where do LLMs fail at evidence appraisal?
        </h2>
        <p>
          The failures cluster in a specific, worrying place: not average performance,
          but performance on the rare class that actually matters for deployment. <N id="EP-014">LLMs collapse on the rare deployment-critical class even when aggregate metrics look reasonable</N>.
          The sharpest example is citation-integrity checking, where{" "}
          <N id="EVD-029">GPT-4 reached F1 = 0.80 for correctly flagging accurate citations but only F1 = 0.09 for flagging inaccurate ones</N>, the
          class any real fact-checking deployment cares about. A similar pattern shows
          up in scientific quality-checking, where{" "}
          <N id="EVD-014">Claude 3.7 Sonnet found no problem in 64.9% of test papers and hit only a 16.3% detection rate</N>.
          A model that mostly says everything is fine will look calibrated on
          aggregate accuracy while missing almost everything worth catching. That
          connects to a second pattern, poor confidence calibration: <N id="EP-008">LLM confidence calibration on scientific-error tasks is poor with extreme distributions</N>, where{" "}
          <N id="EVD-049">LLM confidence approached zero across 498 model-instance evaluations, with only two full-confidence cases</N>.
        </p>
        <p>
          Aggregate agreement statistics can also be misleading in a second way: they can
          look fine while hiding zero real signal. <N id="EP-003">Aggregate-level LLM-human agreement masks near-zero per-paper correlation</N>.
          GPT-4&apos;s feedback overlap with human reviewers was 30.85% until the
          papers were shuffled, at which point{" "}
          <N id="EVD-072">the overlap dropped to 0.43%, confirming the original agreement was paper-specific and not coincidental</N>{" "}
          (reassuring in that direction, but a reminder that overlap statistics need
          this kind of control to mean anything). Finally, modality is a hard
          constraint: <N id="EP-020">text-only LLMs underperform on tasks where figures or tables carry primary information</N>, since{" "}
          <N id="EVD-062">a reasoning model scored 62.6% on equation-proof errors extractable from LaTeX source but near 0% on figure-duplication errors</N>. Text-only
          pipelines are structurally blind to an entire category of scientific error.
        </p>
      </article>

      <article className="prose-node mt-14 border-t border-border pt-10">
        <h2 className="text-xl font-semibold">
          What does human-AI collaboration buy you?
        </h2>
        <p>
          Across the corpus, the strongest and most consistent result is not
          &quot;LLM alone&quot; or &quot;human alone&quot; but the combination: <N id="EP-006">human-AI collaboration outperforms either alone on structured appraisal tasks</N>. On
          checklist-style evidence appraisal,{" "}
          <N id="EVD-045">human-AI collaboration reached up to 96% accuracy on PRISMA and 95% on AMSTAR, surpassing individual human raters</N>{" "}
          working alone. On novelty prediction, folding human reviewer knowledge into
          an LLM-assisted pipeline pushed performance measurably higher: <N id="EVD-070">a knowledge-guided model combining human and LLM signal reached F1 = 0.83 and accuracy = 0.84</N>,
          and the ablation is direct evidence the human signal is load-bearing:{" "}
          <N id="EVD-076">removing the knowledge-guided module dropped accuracy from 0.84 to 0.74</N>. Both
          results back <N id="CLM-011">human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks</N>{" "}
          and <N id="CLM-005">combining human reviewer knowledge with LLM-generated method summaries improves automated novelty prediction beyond either source alone</N>.
        </p>
        <p>
          This is the same underlying mechanism as the fine-tuning result above,
          generalized: <N id="EP-019">task-specific fine-tuning substantially closes the LLM-human gap on structured evaluation tasks</N>.
          Whether the &quot;task-specific&quot; signal comes from fine-tuning on domain
          data or from a human collaborator in the loop, injecting structure the
          base model doesn&apos;t have on its own is what moves accuracy. The
          corpus&apos;s clearest actionable conclusion is less &quot;can LLMs replace
          reviewers&quot; and more &quot;LLMs are a force-multiplier for reviewers who stay
          in the loop, and a systematically over-generous one when they don&apos;t.&quot;
        </p>
      </article>
    </main>
  );
}

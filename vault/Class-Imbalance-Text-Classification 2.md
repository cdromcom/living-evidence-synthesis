# Classifying Text Under Major Class Imbalance — Insights

Synthesis drawn from the vault's source papers on LLM-based scientific paper classification (where minority classes — "not novel", "contains error", "non-compliant with reporting standard" — are frequently the class of interest) plus broader ML practice. Cite the underlying paper, not this note.

## Signals from the source papers

- **Retrieval quality dominates minority-class accuracy.** Removing Shahid 2025's facet-based RankGPT re-ranker dropped *not-novel* prediction accuracy from 89.66% → 13.79% while the majority class was barely affected. When the minority class is the one of interest, invest in retrieval/grounding before model choice.
- **LLMs collapse onto the majority class by default.** Idahl & Ahmadi 2025 showed GPT-4o averaged a 7.7 acceptance recommendation vs human 5.4 — a positivity bias that hides the reject class. Fine-tuning on peer-review data (OpenReviewer) pulled the mean back to 5.4 and lifted minority-class agreement 23.8% → 55.5%.
- **"Found no problem" is the imbalance failure mode.** Zhang & Abernethy 2025: Claude 3.7 Sonnet returned no problem on 64.9% of papers (HR@5 = 16.3%). Always measure how often the model picks the majority/abstain class, not just overall accuracy.
- **Macro-F1 lags micro-F1 when minority is hard.** Sarol 2024's best NLP model hit micro-F1 0.59 but macro-F1 0.52 on citation-accuracy classification — the gap is the minority-class tax. Report both.
- **Reasoning models recover minority-class recall.** o3 reached 64.9–71% hit rate vs Claude 3.7 Sonnet 16.3% on the same error-detection task (Zhang 2025); Son 2025 reports proprietary reasoning models hold meaningful recall (o3 21.1%) on SPOT errors where open-source collapses to ~0.
- **RAG augmentation lifts minority-class recall by giving the model the comparison cases it lacks.** +12.2pp coarse accuracy in Xu 2025 for limitation identification.
- **Multi-agent / multi-prompt decomposition surfaces minority instances.** D'Arcy 2024's MARG cut generic-comment rate 60% → 29%; Sridharan 2025 found single prompts missed ethical issues that multi-prompt setups caught. Single-pass classifiers under-predict the minority class.
- **Per-item-type variance is huge** (Alharbi 2024, Leucuta 2025, Akyon 2024). Within a single checklist, factual items reach ~80% while methodological-judgment items sit at ~35–45%. Don't average across item types — route the hard (often imbalanced) subtypes to heavier techniques.
- **Selective prediction beats forced labeling.** Woelfle 2024's consistency-deferral approach reached 75–88% PRISMA accuracy while deferring 4–74% of cases. Abstention preserves minority-class precision when the model is unsure.

## Practical playbook

### Framing the task
- Define the minority class sharply in the prompt — list distinguishing features and explicit negative examples. Ambiguity in the class definition is the first thing LLMs paper over by defaulting to majority.
- If the minority class has subtypes (e.g., kinds of errors, kinds of bias), classify the subtype, not a binary. Forcing the model to commit to a specific failure mode reduces majority-class collapse.

### Prompting and context
- **Balance in-context examples, not the prior.** Even if the true base rate is 5%, show ~50/50 examples — and surface the minority examples first.
- **Use expert-annotated examples** over LLM-generated or OpenReview-style examples (Shahid 2025 — concrete gain over zero-shot, DSPy, TextGRAD).
- **Force explicit reasoning over minority criteria.** Chain-of-thought that itemizes each minority-class indicator before deciding is harder to short-circuit than free-form CoT.
- **Multi-prompt or multi-agent** — one pass per minority subtype, then aggregate. Increases recall at modest precision cost.

### Decision policy
- **Tune the decision threshold per class.** LLM token-logprob or self-reported confidence works as a score; pick the threshold that maximizes minority-class F1 on a held-out set rather than accepting argmax.
- **Two-stage cascade**: a cheap, high-recall model flags candidate positives → a more capable (reasoning) model adjudicates. Keeps cost down while protecting minority recall.
- **Allow abstention.** A 3-way (positive / negative / unsure) head with deferral to a human or stronger model — Woelfle's deferral curve quantifies the tradeoff.

### Training (when fine-tuning is on the table)
- Fine-tune on the minority-skewed task distribution (Idahl 2025) — corrects systematic positivity/majority bias that prompting alone won't.
- Class weights / focal loss for supervised heads; rejection sampling or DPO with minority-class preferred outputs for generative heads.
- Synthetic minority augmentation (paraphrase, back-translation, LLM-generated counterfactuals) helps small heads but watch for label noise — verify a sample.

### Evaluation
- Report per-class precision/recall/F1 and macro-F1. Never report accuracy alone on imbalanced data.
- Track the model's empirical class distribution vs the data's — a model that predicts the minority at half its true rate is broken even if accuracy looks fine.
- Stratify error analysis by minority subtype — the easy items mask failures on the hard ones (Alharbi/Leucuta/Akyon pattern).
- Include a minority-only evaluation slice to expose collapse-to-majority behavior (the Claude-3.7-Sonnet pattern from Zhang 2025).
- Use human inter-rater reliability on the same task as a ceiling — Woelfle showed human agreement itself drops from 91% (PRISMA) to 57% (PRECIS-2), and no LLM should be benchmarked against a ceiling it can't see.

### Cost / deployment
- Heavy techniques (reasoning models, RAG, multi-agent) pay off most on the minority class. Apply them selectively via a router rather than uniformly — Woelfle reports GPT-4 was ~100× more expensive than Mixtral-8x22B for similar task accuracy.

## Anti-patterns observed
- Reporting overall accuracy or micro-F1 only.
- Few-shot prompts that mirror the natural (imbalanced) prior — model learns to predict majority.
- Single-pass binary classification on a composite construct (e.g., "is this paper sound?") — decompose into sub-checks.
- Using full-text input on the assumption that more context always helps — Thelwall 2024 found abstracts beat full text for quality scoring; long context can dilute minority-class signals.
- Treating the LLM's verbalized confidence as calibrated without checking — Son 2025 found LLM confidence approaches zero across 498 SPOT evaluations even when the model is correct.

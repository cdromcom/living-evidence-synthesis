---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/decision-judgment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M3-H2
  - tripod-llm/compliance/low
  - tripod-llm/proportion/56pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b80-7713-af4a-560f2b17057c
appraisal_overall: L0-M3-H2
tripod_llm_pct: 56pct
---

## Source

[[@idahlOpenReviewerSpecializedLarge2025]]

## Description

> "While OpenReviewer matches the human reviewers with an average recommendation of 5.4 out of 10, the baseline LLMs produce average recommendations of 6.9 and higher, topped by Llama-3.1-8B-Instruct with an average recommendation of 8.1." (Idahl & Ahmadi, 2025, p. 4)
>
> ![[idahlOpenReviewer2025-table2fig2-p5-1.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark comparing one fine-tuned LLM (OpenReviewer) against four general-purpose LLM baselines on a held-out peer-review test set.
>
> **Method type:** automatic metric (mean recommendation rating with standard deviation) compared against human-reviewer reference distribution.
>
> **Tools:** Llama-OpenReviewer-8B (full-finetune of Llama-3.1-8B-Instruct on ~79K filtered ICLR/NeurIPS reviews via axolotl + Deepspeed ZeRO-3 + Flash Attention V2 + LIGER kernel); Llama-3.1-8B-Instruct, Llama-3.1-70B-Instruct, Claude-3.5-Sonnet (Oct. 22), GPT-4o (2024-11-20); vLLM serving for OpenReviewer/Llama and OpenRouter for Claude/GPT-4o; Marker for PDF→markdown.
>
> **Dependent variable:** average recommendation rating (normalized to 1=strong reject … 10=strong accept) ± SD per model.
>
> **Independent variable:** model identity (5 LLMs + human reviewer reference).

> "While OpenReviewer matches the human reviewers with an average recommendation of 5.4 out of 10, the baseline LLMs produce average recommendations of 6.9 and higher, topped by Llama-3.1-8B-Instruct with an average recommendation of 8.1, which would lead to an "accept" for most of the papers in the test dataset." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-1.png]]

### How?

> **Procedure:** (1) Construct test set of 400 held-out NeurIPS 2024 + ICLR 2025 papers (most-recent venues in the dataset; not used during fine-tuning). (2) For each model, generate one review per paper using greedy decoding (temperature=0) and the same OpenReviewer system + user prompts (Figures 3–4). (3) Parse the recommendation field from each generated review and normalize to a 1–10 scale. (4) Compute the mean and SD of recommendations per model and compare to the human-reviewer mean (5.4 ± 1.2) computed from OpenReview annotations on the same 400 papers.

> "We generate one review for each paper in the test set using greedy decoding (temperature of 0). All LLMs are instructed with the same system and user prompts used by OpenReviewer. We use vLLM (Kwon et al., 2023) to serve the OpenReviewer and Llama models, and access Claude-3.5-Sonnet and GPT-4o via OpenRouter." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-2.png]]

### Who?

> **Models / participants:** 5 LLMs evaluated (OpenReviewer + 4 baselines). Human reference = real OpenReview reviewers for the same 400 papers.
>
> **Sample-size flow:** OpenReview ICLR + NeurIPS 2022-onwards crawl → 36K papers + 141K reviews → filter by length (top + bottom 1% removed) → keep only "Confident, but not absolutely certain" or higher reviewer-confidence reviews → ≈79K reviews used for fine-tuning. Test set: 400 held-out papers from NeurIPS 2024 + ICLR 2025 (the most-recent venues, withheld from training). Per-model evaluation N = 400 generated reviews each.

> "To measure how well OpenReviewer reviews align with reviews from human reviewers, we conduct experiments using a test set of 400 held-out papers and their reviews from NeurIPS 2024 and ICLR 2025, the most recent venues in our dataset." (Idahl & Ahmadi, 2025, p. 4)
> ![[idahlOpenReviewerSpecializedLarge2025-evd-p4-3.png]]

## Other Notes

- High recommendation scores (e.g., 8.1 for Llama-3.1-8B-Instruct) would lead to an "accept" outcome for most papers in the test set, making such scores misleading for pre-submission feedback.
- Llama-OpenReviewer-8B is the full-finetune of the same base model that, off-the-shelf, gives the most inflated recommendations (8.1), so the 5.4 result is attributable to the peer-review fine-tune rather than the base model.

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@idahlOpenReviewerSpecializedLarge2025#TRIPOD-LLM reporting]].

| Model | Avg. recommendation (1–10) ± SD |
| --- | :---: |
| Llama-3.1-8B-Instruct | 8.1 ± 1.4 |
| Llama-3.1-70B-Instruct | 6.9 ± 2.8 |
| Claude-3.5-Sonnet | 7.6 ± 1.7 |
| GPT-4o (2024-11-20) | 7.7 ± 0.8 |
| **OpenReviewer (Llama-OpenReviewer-8B)** | **5.4 ± 1.1** |
| Human reviewers (reference) | 5.4 ± 1.2 |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - General-purpose LLMs produce overly positive peer review recommendations that do not reflect human reviewer distributions]]

- [[CLM - Specialized fine-tuning on peer review data overcomes LLM tendency toward overly favorable assessments]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]]

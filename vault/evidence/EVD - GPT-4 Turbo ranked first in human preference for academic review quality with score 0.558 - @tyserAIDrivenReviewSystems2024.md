---
NodeFormality: draft
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L0-M2-H3
  - tripod-llm/compliance/low
  - tripod-llm/proportion/25pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b68-7025-a508-4eb106d8ce56
appraisal_overall: L0-M2-H3
tripod_llm_pct: 25pct
---

## Source

[[@tyserAIDrivenReviewSystems2024]]

## Description

> *Table 1 contents (rows reformatted as inline text):* "Rank 1: GPT-4 Turbo (April 9, 2024) Score: 0.558; Rank 2: Human Score: 0.501; Rank 3: Command R+ Score: 0.277; Rank 4: Claude 3 Opus Score: 0.000; Rank 5: Gemini Pro (Bard) Score: -0.522" (Tyser et al., 2024, p. 5, Table 1)
>
> ![[tyserAIDrivenReviewSystems2024-table1-p5.png]]

## Methods Context

### What?

> **Study design:** cross-sectional pairwise-preference benchmark ("Reviewer Arena") modeled on Chatbot Arena.
>
> **Method type:** Bradley-Terry (BT) model fit by logistic regression on a win matrix derived from human pairwise preferences over reviews of the same paper.
>
> **Tools:** 5 reviewer "competitors" — Human (OpenReview), GPT-4 Turbo (Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), Command R+; in-house Reviewer Arena platform; BT optimization via logistic loss with the constraint ξ₁ = 0 (Listings 1–2, Appendix P).
>
> **Dependent variables:** BT coefficient ξ per reviewer; resulting reviewer ranking (Table 1).
>
> **Independent variable:** reviewer identity (5 levels). Pairwise comparisons are anonymized so evaluators do not know which review was authored by whom.
>
> "This work quantifies and ranks reviewers based on observed match outcomes using a win matrix, Bradley-Terry (BT) model coefficients, and logistic regression. The win matrix represents the outcomes of matches between competitors. For N competitors, the matrix W is an N × N matrix where each element wij represents the probability of competitor i winning against competitor j" (Tyser et al., 2024, p. 4)
> ![[tyserAIDrivenReviewSystems2024-evd-p4-1.png]]

### How?

> **Procedure:** (1) collect academic papers from open-access venues (ICLR 2023/2024, NeurIPS 2022/2023, open-access Nature journals) along with their human OpenReview reviews. (2) For each of 150 papers, generate one review per LLM competitor and pair it with the OpenReview human review; randomly assign **2 reviewers from the 5-competitor pool** per paper. (3) 5 expert evaluators view each pair anonymously and indicate which review they prefer. (4) Tally pairwise outcomes into a win matrix W (probability of i beating j = wins_i_vs_j / total_matches_i_vs_j). (5) Estimate BT coefficients ξ̂ = argminξ Σₜ ℓ(Hₜ, 1/(1+exp(ξ_A2 − ξ_A1))) by minimizing binary cross-entropy under the constraint ξ₁ = 0. (6) Sort competitors by ξ in descending order to produce Table 1. The same protocol is repeated using GPT-4 Turbo as the evaluator (Table 2 / Figure 5) using the PPI++ estimate (Angelopoulos et al. 2023) for autoevaluation.
>
> "To evaluate the quality of the LLM-generated reviews, five expert evaluators were provided with 150 papers together with two anonymous reviews for each paper. Each paper was randomly assigned two reviewers from the list of five potential reviewers: Human, GPT-4 (Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), and Command R+. The human reviews were obtained from OpenReview submissions. The evaluators were asked which of the two reviews for each paper they preferred. Therefore, this methodology evaluates the relative quality of each reviewer as determined by human evaluators through a series of one-on-one comparisons." (Tyser et al., 2024, p. 4)
> ![[tyserAIDrivenReviewSystems2024-evd-p4-2.png]]

### Who?

> **Reviewers compared (5):** Human (OpenReview reviewers of ICLR/NeurIPS papers), GPT-4 Turbo (Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), Command R+. LLM reviews generated under the full P5 context (paper + review form + reviewer guide + code of ethics + code of conduct + area chair guidelines + previous year statistics).
>
> **Papers (sample-size flow):** open-access source venues — ICLR 2024 (7,404 papers), ICLR 2023 (4,955), NeurIPS 2023 (12,345), NeurIPS 2022 (10,411), and open-access Nature journals (Table 3, Appendix B) → **150 papers sampled** for the Reviewer Arena evaluation. Each paper assigned 2 of 5 reviewers at random.
>
> **Human evaluators:** 5 expert evaluators (the paper does not further characterize their background, discipline, or recruitment). A second pass uses **GPT-4 Turbo as the evaluator** (Table 2) for autoevaluation via PPI++.
>
> "We deploy a system called Papers with Reviews illustrated in Figure 2 that collects around five hundred academic papers daily from arXiv and around a thousand open-access Nature journal papers monthly." (Tyser et al., 2024, p. 3)
> ![[tyserAIDrivenReviewSystems2024-evd-p3-1.png]]

## Other Notes

- GPT-4 Turbo wins under both judging regimes — human evaluators (BT score 0.558, Table 1) and GPT-4 Turbo as evaluator (BT score 0.179, Table 2) — but the gap to Human collapses in the autoeval (0.179 vs. 0.119) and the LLM rankings of weaker models reorder substantially (Command R+ falls from rank 3 under humans to rank 5 under GPT-4 Turbo).
- The BT model imposes ξ₁ = 0 for identifiability; ranks are relative, not absolute.
- The 5-evaluator pool is small and the paper does not report per-evaluator agreement, so the human-preference ranking has a wide implicit confidence interval that the BT score does not display.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@tyserAIDrivenReviewSystems2024#TRIPOD-LLM reporting summary]].

| Rank | Reviewer | BT score (human evaluators) | BT score (GPT-4 Turbo evaluator) |
| :---: | --- | :---: | :---: |
| **1** | **GPT-4 Turbo (April 9, 2024)** | **0.558** | **0.179** |
| 2 | Human (OpenReview) | 0.501 | 0.119 |
| 3 | Command R+ | 0.277 | −1.267 |
| 4 | Claude 3 Opus | 0.000 (reference) | 0.000 (reference) |
| 5 | Gemini Pro (Bard) | −0.522 | −0.819 |

| Design parameter | Value |
| --- | --- |
| Papers | 150 |
| Reviewers per paper | 2 of 5 (random) |
| Expert human evaluators | 5 |
| Estimator | Bradley-Terry via logistic regression; PPI++ for GPT-4 evaluator pass |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - LLM review alignment findings based on venue-specific guidelines requiring yearly updates and subject to human preference biases]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - LLM peer-review systems can predict paper acceptance and preference at near-human accuracy]]

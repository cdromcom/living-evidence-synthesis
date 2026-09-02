---
NodeFormality: ReadyForInternal
aliases:
tags:
  - task/novelty-assessment
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/some-concerns
  - appraisal/overall/L1-M3-H1
  - tripod-llm/compliance/low
  - tripod-llm/proportion/55pct
  - 5c/credibility
  - 5c/clarity
  - 5c/creativity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b6c-7583-b3b7-c100895b138d
appraisal_overall: L1-M3-H1
tripod_llm_pct: 55pct
---

## Source

[[@liangCanLargeLanguage2024a]]

## Description

> "LLM comments on the implications of research 7.27 times more frequently than humans do. Conversely, LLM is 10.69 times less likely to comment on novelty than humans are." (Liang et al., 2024, p. 5)
>
> ![[liangCanLargeLanguage2024a-quote-7x-desc-p5.png]]
>
> Grounding figure context (p. 5): aspect distribution discussion alongside Fig. 3 reference.
>
> ![[liangCanLargeLanguage2024a-aspects-p5-5.png]]

## Methods Context

### What?

> **Study design:** retrospective comparative content analysis of LLM vs. human peer-review comments.
>
> **Method type:** human aspect-coding of GPT-4 and human reviewer comments against an 11-aspect schema, with log-frequency-ratio comparison.
>
> **Tools:** GPT-4 feedback pipeline (zero-shot, single-pass, 4-section structured prompt); GPT-4 extractive summarization to convert raw feedback into JSON-keyed comment lists; the authors' 11-aspect annotation schema (Novelty, Implications of the Research, Add experiments on more datasets, Add ablation experiments, Clarity and Presentation, Ethical Aspects, Algorithm Efficiency, Reproducibility, Comparison to Previous Studies, Theoretical Soundness, Missing Citations).
>
> **Dependent variable:** per-aspect log frequency ratio log(freq_LLM / freq_human) (Fig. 3).
>
> **Independent variables:** comment source (LLM vs. human reviewer); aspect category.
>
> "Fig. 3 presents the relative frequency of each of the 11 aspects of comments raised by humans and LLM. LLM comments on the implications of research 7.27 times more frequently than humans do. Conversely, LLM is 10.69 times less likely to comment on novelty compared to human reviewers." (Liang et al., 2024, p. 5)
> ![[liangCanLargeLanguage2024a-evd-p5-2.png]]

### How?

> **Procedure:** restricted to ICLR (more topically homogeneous than the multidisciplinary Nature corpus). 11 aspects selected from prior ML peer-review literature plus initial annotator exploration. From the ICLR dataset, **a random sample of 500 papers** was drawn. For each paper, the extractive-summarization pipeline (GPT-4) produced JSON comment lists from both the GPT-4 review and the human reviews. Two ML-background human annotators then labeled every extracted comment with any subset of the 11 aspects (multi-label). Aspect prevalences were aggregated within source (LLM vs. human) and converted to a log frequency ratio per aspect (Fig. 3). Bubble area in Fig. 3 represents the absolute prevalence in human feedback.
>
> "We curated an annotation schema of 11 key aspects to identify and measure the prevalence of these aspects in human and LLM feedback. This schema was developed with a focus on the ICLR dataset, due to its specialized emphasis on Machine Learning. Each aspect was defined by its underlying emphasis, such as novelty, research implications, suggestions for additional experiments, and more. The selection of these 11 key aspects was based on a combination of the common schemes identified in the literature within the machine learning domain, comments from machine learning researchers, and initial exploration by the annotators. From the ICLR dataset, a random sample of 500 papers was selected to ensure a broad yet manageable representation. Using our extractive text summarization pipeline, we extracted lists of comments from both the LLM and human feedback for each paper. Each comment was then annotated according to our predefined schema, identifying any of the 11 aspects it represented (Supp. Table 5,6,7). To ensure annotation reliability, two researchers with a background in machine learning performed the annotations." (Liang et al., 2024, p. 10)
> ![[liangCanLargeLanguage2024a-evd-p10-1.png]]

### Who?

> **Source corpus:** ICLR 2022 + ICLR 2023 OpenReview dataset = **1,709 papers / 6,505 human reviewer comments** (stratified across Oral, Spotlight, Poster, Reject-after-rebuttal, and Withdrawn decisions; Supp. Table 2).
>
> **Aspect-analysis sample (sample-size flow):** 1,709 ICLR papers → randomly sampled subset of **500 papers** → comment lists from both LLM and human reviews extracted → each comment double-annotated by **2 ML-background annotators** under the 11-aspect schema. Inter-annotator agreement / κ for this sub-task is not reported in the main text.
>
> "The second dataset comprises 6,505 comments from human reviewers for 1,709 papers from the International Conference on Learning Representations (ICLR), a leading venue for artificial intelligence research in computer science" (Liang et al., 2024, p. 3)
> ![[liangCanLargeLanguage2024a-evd-p3-2.png]]

## Other Notes

- Both LLMs and humans frequently request additional experiments, but their focus differs: humans are **6.71×** more likely than GPT-4 to request additional **ablation** experiments, whereas GPT-4 is **2.19×** more likely than humans to request experiments on **more datasets** (Fig. 3).
- Authors interpret the divergence as an argument for human-AI complementarity rather than full LLM automation of review.
- IAA on the 11-aspect coding is not reported in the main text; only "two researchers with a background in machine learning performed the annotations."

> [!info] TRIPOD-LLM item 17 (Performance), EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@liangCanLargeLanguage2024a#TRIPOD-LLM reporting summary]].

| Aspect (ICLR, n=500 papers) | Frequency ratio (GPT-4 / Human) | Direction |
| --- | :---: | --- |
| Implications of the Research | **7.27×** | GPT-4 ≫ human |
| Add experiments on more datasets | 2.19× | GPT-4 > human |
| Clarity and Presentation | ≈ 1× | comparable |
| Algorithm Efficiency | ≈ 1× | comparable |
| Reproducibility | ≈ 1× | comparable |
| Comparison to Previous Studies | ≈ 1× | comparable |
| Add ablation experiments | 1 / 6.71 ≈ 0.149× | human > GPT-4 |
| **Novelty** | **1 / 10.69 ≈ 0.094×** | **human ≫ GPT-4** |
| Theoretical Soundness, Missing Citations, Ethical Aspects | < 1× | human > GPT-4 (smaller gaps) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]

- [[CLM - LLM-generated scientific feedback is paper-specific and not merely generic boilerplate]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - General-purpose LLMs systematically over-rate papers compared to human reviewers]]

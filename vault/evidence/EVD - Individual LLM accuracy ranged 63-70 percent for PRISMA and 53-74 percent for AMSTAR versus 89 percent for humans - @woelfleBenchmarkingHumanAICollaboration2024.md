---
NodeFormality: ReadyForInternal
aliases:
tags:
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/low-risk
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L2-M2-H1
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/67pct
  - 5c/clarity
  - 5c/credibility
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b75-77f2-8f5f-2ee12134dbb3
appraisal_overall: L2-M2-H1
tripod_llm_pct: 67pct
---

## Source

[[@woelfleBenchmarkingHumanAICollaboration2024]]

## Description

> "Individual LLM accuracy was ranging from 63% (GPT-3.5) to 70% (Claude-3-Opus) for PRISMA, 53% (GPT-3.5) to 74% (Claude-3-Opus) for AMSTAR, and 38% (GPT-4) to 55% (GPT-3.5) for PRECIS-2." (Woelfle et al., 2024, p. 1 [Abstract])
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p1-2.png]]
>
> Grounding table (Table 2, p. 5): individual human rater + individual LLM accuracy with Cohen's kappa and 95% CIs.
>
> ![[woelfleBenchmarkingHumanAICollaboration2024-table2-p5-05.png]]

## Methods Context

### What?

> **Study design:** cross-sectional benchmark of individual zero-shot LLMs against fixed human consensus on three evidence-appraisal tools.
>
> **Method type:** zero-shot LLM evaluation with prompt-based extract-quote-and-rate scaffolding (no fine-tuning).
>
> **Tools:** 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B-instruct-v0.1) × 3 appraisal tools (PRISMA 27 items × 112 reviews; AMSTAR 11 items × 112 reviews; PRECIS-2 9 domains × 56 RCTs).
>
> **Dependent variables:** agreement (% identical to human consensus) and Cohen's kappa (weighted Cohen's kappa for ordinal PRECIS-2).
>
> **Independent variables:** LLM (5 levels); appraisal tool (3 levels); also intrarater reliability from duplicate runs.
>
> "Our main outcome was agreement with human consensus measured by accuracy (agreement fraction, i.e., the proportion of identical ratings between rater and human consensus) and Cohen's kappa." (Woelfle et al., 2024, p. 3)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p3-3.png]]

### How?

> **Procedure:** Five LLMs were queried via APIs (Anthropic, OpenAI, OpenRouter for Mixtral) at temperature 0 for maximum intrarater reliability. For each publication and tool, the prompt asked the LLM to (1) extract 1–3 relevant quotes from the full text, (2) explain reasoning in one paragraph, and (3) assign a per-item rating (no/yes/NA for PRISMA/AMSTAR; ordinal 1–5 or NA for PRECIS-2). Claude-3-Opus received page-level PNG images (multimodal, implicit OCR — fully exposing figures/tables); the other four models received plain text the authors extracted (image-blind). Each prompt was run twice (GPT-4 only on 25% of publications due to cost) and the duplicate runs are treated as intrarater reliability.
>
> **For this analysis (individual LLMs):** each LLM run was directly compared to human consensus, item-by-item, computing accuracy and Cohen's kappa (weighted κ for PRECIS-2 with the 1/2 and 4/5 ordinal pairs collapsed). 1000-resample publication-level bootstrap 95% CIs in R 4.3. Quote handling and post-processing in Python 3.11.4 (parasail, rapidfuzz).
>
> "We performed LLM prompts twice (ie, in duplicate for Claude-3-Opus, Claude-2, GPT-4 [only 25% of publications, due to high cost], GPT-3.5, Mixtral-8x22B) and compared the ratings of each of the 2 runs… All application programming interface (API) queries were performed with minimal randomness ('temperature' 0) to allow the highest possible intrarater reliability." (Woelfle et al., 2024, p. 5)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p5-3.png]]

### Who?

> **Models:** 5 LLMs (Claude-3-Opus / Claude-2 / GPT-4-32k-0613 / GPT-3.5-turbo-16k-0613 / Mixtral-8x22B-instruct-v0.1), each prompted twice.
>
> **Datasets / sample-size flow:** PRISMA & AMSTAR — 112 systematic reviews & meta-analyses in pediatric surgery (Cullis et al.); PRECIS-2 — 56 RCTs from PragMeta. Maximum potential ratings: PRISMA up to 3024 (27 × 112); AMSTAR up to 1232 (11 × 112); PRECIS-2 up to 504 (9 × 56).
>
> **Processing failures (excluded from N):** Claude-3-Opus 3/112 (Anthropic content filtering / overly long); GPT-4 3/112 (context length); GPT-3.5 3/112 PRISMA-AMSTAR + 2/56 PRECIS-2; Mixtral 1/112; Claude-2 processed all. Reflected in Table 2 N (e.g., GPT-3.5 PRISMA: 1868/2943 = 63%).
>
> **Human comparator:** 2 human raters per publication and their consensus (PRISMA/AMSTAR: British pediatric surgeons; PRECIS-2: experienced systematic reviewer + MSc epidemiology student or senior clinical epidemiologist).
>
> "We used 4 proprietary LLMs (Anthropic's Claude-3-Opus and Claude-2, OpenAI's GPT-4 and GPT-3.5) and 1 open-source LLM (Mistral AI's Mixtral-8x22B)… Claude-3-Opus was the only multimodal model we employed. To fully take advantage of the multimodality, we converted PDF files to plain images (one PNG file per page) for this model. This way, it processed the normal page layout, including all figures and tables alongside the full text, which it extracted itself by implicitly performing optical character recognition. The 4 other models could only process full text (extracted by us) and no images." (Woelfle et al., 2024, p. 2–3)
> ![[woelfleBenchmarkingHumanAICollaboration2024-evd-p2-3.png]]

## Other Notes

- All five individual LLMs performed significantly worse than humans (89% PRISMA / 89% AMSTAR / 75% PRECIS-2 for human rater 1) on every tool.
- Counter-intuitive PRECIS-2 finding: smaller/cheaper GPT-3.5 (55%) and Mixtral (48%) outperformed larger Claude-3-Opus (45%) and Claude-2 (44%) and GPT-4 (38%) — authors attribute this partly to the dataset being skewed toward pragmatic trials (smaller models may default toward more pragmatic scores).

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@woelfleBenchmarkingHumanAICollaboration2024#TRIPOD-LLM reporting summary]].

| Tool | Model | Agreement (95% CI) | Cohen's kappa (95% CI) | Intrarater agreement (95% CI) |
| --- | --- | --- | --- | --- |
| **PRISMA** | Human rater 1 | 89% (87–90%) | 0.81 (0.78–0.83) | 91% (89–93%, vs human 2) |
| PRISMA | Claude-3-Opus | **70%** (68–72%) | 0.51 (0.47–0.55) | 89% (87–91%) |
| PRISMA | Claude-2 | 70% (68–72%) | 0.51 (0.47–0.55) | 89% (87–91%) |
| PRISMA | GPT-4 | 69% (66–71%) | 0.45 (0.42–0.48) | 90% (85–93%) |
| PRISMA | GPT-3.5 | **63%** (62–66%) | 0.40 (0.37–0.44) | 94% (92–96%) |
| PRISMA | Mixtral-8x22B | 64% (61–67%) | 0.42 (0.37–0.47) | 67% (63–70%) |
| **AMSTAR** | Human rater 1 | 89% (87–91%) | 0.80 (0.76–0.83) | 88% (85–90%, vs human 2) |
| AMSTAR | Claude-3-Opus | **74%** (72–76%) | 0.56 (0.52–0.60) | 80% (78–83%) |
| AMSTAR | Claude-2 | 63% (60–66%) | 0.39 (0.34–0.43) | 94% (92–96%) |
| AMSTAR | GPT-4 | 70% (67–73%) | 0.45 (0.40–0.51) | 89% (83–94%) |
| AMSTAR | GPT-3.5 | **53%** (50–56%) | 0.27 (0.22–0.32) | 87% (83–90%) |
| AMSTAR | Mixtral-8x22B | 59% (56–63%) | 0.34 (0.29–0.39) | 64% (60–68%) |
| **PRECIS-2** | Human rater 1 | 75% (70–80%) | 0.57 weighted (0.48–0.65) | 57% (51–63%, vs human 2) |
| PRECIS-2 | Claude-3-Opus | 45% (40–49%) | 0.12 (0.06–0.19) | 72% (68–77%) |
| PRECIS-2 | Claude-2 | 44% (39–49%) | 0.01 (–0.08 to 0.08) | 76% (71–81%) |
| PRECIS-2 | GPT-4 | **38%** (33–43%) | 0.02 (–0.07 to 0.04) | 63% (52–75%) |
| PRECIS-2 | GPT-3.5 | **55%** (50–58%) | 0.04 (–0.05 to 0.12) | 78% (71–84%) |
| PRECIS-2 | Mixtral-8x22B | 48% (43–54%) | 0.05 (–0.03 to 0.13) | 61% (54–67%) |

## Caveats

> [!info] Caveats applying to this evidence

- [[CVT - Evidence appraisal benchmark used only two human raters and datasets skewed toward pragmatic trials limiting PRECIS-2 findings]]

- [[CVT - Human consensus datasets used as comparators were openly available online raising train test contamination concerns]]

- [[CVT - Most LLMs were text-only and blind to figures and image-rendered tables relevant for evidence appraisal]]

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - Human-AI collaboration outperforms individual LLMs and can match or exceed human rater accuracy for evidence appraisal tasks]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Aggregate LLM accuracy on evidence-appraisal benchmarks lands in the moderate 60-80 percent range]]

---
NodeFormality: draft
aliases:
tags:
  - task/reporting-compliance-checking
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - appraisal/reproducibility/low-risk
  - appraisal/overall/L1-M2-H2
  - tripod-llm/compliance/moderate
  - tripod-llm/proportion/64pct
  - 5c/clarity
created: 2026-04-17
updated: 2026-04-29
nodeID: 019ddb4e-6b69-72e8-9f18-009f9165c9d1
appraisal_overall: L1-M2-H2
tripod_llm_pct: 64pct
---

## Source

[[@wrightsonGPTRCTsUsing2025]]

## Description

> "The GPT-4 Vision model accurately identified all flowcharts (accuracy (95% CI) = 100% (89% to 100%)) but was less accurate at identifying when details were missing from the flow chart (accuracy (95% CI) = 57% (39% to 73%))." (Wrightson et al., 2025, p. 5)
>
> ![[wrightsonGPTRCTsUsing2025-gpt4-results-p5-1.png]]

## Methods Context

### What?

> **Study design:** opportunistic image-only sub-study of the same CONSORT-adherence benchmark, performed when OpenAI released GPT-4 Vision during the project; treats two **image-based** CONSORT items separately from the 9 text-based items.
>
> **Method type:** zero-shot multimodal generative question-answering — Base64-encoded participant flow-diagram image + system prompt + question all sent through the OpenAI 'chat' API call.
>
> **Tools:** OpenAI **GPT-4 Vision** (closed, hyperparameters not separately reported for the vision call); same engineered system + user prompts as the text analysis; Schulz et al. labels (where available) and authors' manual labelling for the 10 supplementary distractor diagrams.
>
> **Dependent variables:** classification accuracy (95% Clopper–Pearson CI) and F1-score for two CONSORT-image items: **Q10** "Does this image contain a CONSORT flow diagram showing, for each group, the number of participants who were randomly assigned, received the intended treatment and were analysed for the primary outcome?" and **Q11** "Does this image display a CONSORT flow diagram that details both the number of participants lost to follow-up and excluded after randomisation and specifies the reasons for these losses in each group?"
>
> **Independent variables:** the two CONSORT items (Q10 vs. Q11) and the diagram source (10 papers known to contain a flow diagram, plus 10 supplementary non-flow-diagram images included to test that the model does not just label every image as a CONSORT diagram).
>
> "During the study, OpenAI made their GPT-4 Vision model available for general use. We used this model to assess adherence to two further research guideline items (table 2, questions 10 and 11) related to the participant flow diagrams in a subset of papers (n=20). We encoded the papers' participant flow diagram images in Base64 and appended the system prompt and item questions to the encoded image using the same 'chat' format API call used for the analysis of the text." (Wrightson et al., 2025, p. 4)
> ![[wrightsonGPTRCTsUsing2025-evd-p4-5.png]]

### How?

> **Procedure:** (1) Identify, using Schulz et al.'s labels, the **10 papers** in the dataset whose Results contain a CONSORT-style participant flow diagram with per-group randomised / received / analysed counts (Q10 = YES). (2) Build a 10-paper distractor set — sample 10 flow diagrams from the dataset that show clinical-trial flow but **not** the participant-level CONSORT structure (Q10 = NO). (3) Combine to form n = 20 images drawn from **both** TRAIN and TEST splits (the small candidate pool prevented restricting to TEST only). (4) Encode each image in Base64; build the API payload by concatenating the same system prompt used for text analysis + a Q10 (or Q11) user-prompt question + the encoded image. (5) Submit to GPT-4 Vision via the OpenAI chat-completion endpoint. (6) Compare returned YES/NO against Schulz et al. labels (Q10) or against author labelling (Q11, "are reasons for losses given?"). (7) Report classification accuracy with 95% Clopper–Pearson CIs and F1 for each of Q10, Q11 in Table 2.
>
> "Ten of the papers contained a flow diagram which showed the number of participants randomised to each group (answer 'YES' to table 2, question 10) but did not include reasons for exclusions and loss to follow-up (answer 'NO' to table 2, question 11). These papers were identified using the labels from Schulz et al; 10 of these papers were in the dataset. The remainder had complete flow diagrams (answer 'Yes' to both questions). The PubMed Identifiers for the papers included in the Image analysis are available in the online materials. Because the number of suitable papers was so low, the included papers were drawn from both the test and training datasets. To ensure the model did not simply label any flow diagram as a participant flow diagram, a sample of 10 flow diagrams that did not show participant flow through a clinical trial was included in the dataset for one question (table 2, question 10)." (Wrightson et al., 2025, p. 4)
> ![[wrightsonGPTRCTsUsing2025-evd-p4-6.png]]

### Who?

> **Models / participants:** OpenAI **GPT-4 Vision** (closed; specific snapshot date not disclosed beyond "during the study" — i.e., on or before manuscript submission, May 2024). No human evaluators perform image classification; Schulz et al. labels and author-derived labels serve as ground truth.
>
> **Sample-size flow:** Schulz et al. base set 160 papers → 113 included in the text analysis after exclusions → among those, only **10 papers** had a CONSORT-style participant flow diagram of the right form (Q10 = YES) → augmented with **10 papers** drawn from the 113 whose Results figures showed clinical-trial flow but not CONSORT participant-level flow (distractors / Q10 = NO) → **n = 20 images** analysed (drawn from **both TRAIN and TEST**, breaking the strict held-out evaluation used in the text analysis). The same 20 images are reused for both Q10 (n=20) and Q11 (n=20 in Table 2; CIs match the n=20 analysis).
>
> "The flow diagrams from a subset of the data (n=20) were assessed for adherence to two further reporting guideline items (questions 10 and 11, table 2). The GPT-4 Vision model accurately identified all flowcharts (accuracy (95% CI) = 100% (89% to 100%)) but was inaccurate at identifying when details were missing from the flow chart (accuracy (95% CI) = 57% (39 to 73%))." (Wrightson et al., 2025, p. 5)
> ![[wrightsonGPTRCTsUsing2025-evd-p5-1.png]]

## Other Notes

- The image sample was drawn from **both TRAIN and TEST**, so this EVD is not a held-out evaluation in the same sense as the text analysis. The authors are explicit that they did this because the candidate pool of 10 true-CONSORT flow diagrams was too small to split.
- The asymmetry (100% identification vs. 57% missing-detail detection) is the headline finding: GPT-4 Vision can recognise that a figure is a CONSORT flow diagram but cannot reliably detect which CONSORT-required participant counts are missing from it. The authors interpret this as the model being able to classify the genre of the figure but not to do fine-grained content extraction.
- Q11's 57% accuracy (95% CI 39%–73%) is barely above chance for a binary task, and the lower CI bound (39%) is well below 50%.
- No mention of whether GPT-4 Vision was prompted with the same temperature=0.2, Top P=0.2 settings used for GPT-4 Turbo text analysis.

> [!info] TRIPOD-LLM item 17 (Performance) — EVD-specific. For Methods (5a–15) and Results (16a, 16b, 16c, 16d, 18) compliance, see [[@wrightsonGPTRCTsUsing2025#TRIPOD-LLM reporting summary]].

| CONSORT image question | n | F1-score | Accuracy (95% CI) |
| --- | :---: | :---: | :---: |
| **Q10. Flow diagram shows random-assignment / received / analysed counts per group** | 20 | **1.0** | **100% (89% to 100%)** |
| **Q11. Flow diagram details lost-to-follow-up & exclusion reasons per group** | 20 | **0.58** | **57% (39% to 73%)** |

| Sample composition (n=20 images, drawn from both TRAIN and TEST) |
| --- |
| 10 papers: CONSORT-style participant flow diagram present, no exclusion reasons (Q10=YES, Q11=NO) |
| 10 papers: trial-flow figure present but not CONSORT participant-level (Q10=NO; Q11 — see Table 2 for n) |

## Caveats

> [!info] No caveats currently linked to this evidence.

## Supports Claim(s)

> [!info] Claims this evidence may support (auto-derived from paper-level overlap; verify before citing)

- [[CLM - LLMs can assess clinical trial reporting guideline adherence with acceptable accuracy approaching 90%]]

## Instantiates Pattern(s)

> [!info] Cross-paper EvidencePattern(s) this evidence contributes to

- [[EP - Per-item LLM-human agreement varies sharply by item type]]
- [[EP - Text-only LLMs underperform on tasks where figures or tables carry primary information]]

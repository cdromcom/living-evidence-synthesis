---
dg_type: Source
status: seed
keywords: ""
rating: 3
tags:
  - dg/source
  - trust/reproducibility/some-concerns
  - top/study-protocol/not-disclosed
  - top/study-registration/not-applicable
  - top/data-transparency/level-1-disclosed
  - top/code-transparency/level-1-disclosed
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/high-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - rigor/sample-size-estimation/not-done
  - rigor/study-type/exploratory
  - integrity/ethical-approval/partial
  - integrity/funding-disclosure/not-disclosed
  - integrity/coi-disclosure/not-disclosed
doi: 10.48550/arXiv.2408.10365
critiqueStatus: not-registered
critiqueNote: "No retraction registry exists for arXiv preprints (checked via DataCite)"
authors:
  - "Tyser, Keith"
  - "Segev, Ben"
  - "Longhitano, Gaston"
  - "Zhang, Xin-Yu"
  - "Meeks, Zachary"
  - "Lee, Jason"
  - "Garg, Uday"
  - "Belsten, Nicholas"
  - "Shporer, Avi"
  - "Udell, Madeleine"
  - "Te'eni, Dov"
  - "Drori, Iddo"
pubType: preprint
selfCitationRate: not-assessable
doajListed: not-applicable
pubpeerCommentCount: 0
citekey: tyserAIDrivenReviewSystems2024
nodeTypeId: node_WloBZlAOaEodMKQ82S_Dn
nodeInstanceId: 019dd17a-f952-7812-8b4b-cd633d0b6ddb
---

> [!success] **TL;DR**
> The paper makes a real contribution by showing that GPT-4 with a fully assembled venue-context bundle can produce reviews that judges prefer at roughly the same rate as human OpenReview reviews. But the headline "LLM ≥ human" rests on a 5-judge preference tournament over 150 papers, no confidence intervals, an 8-paper rubric sub-study with one human evaluator, and a context bundle that has to be rebuilt each year.

## Structured abstract

> [!info] A plain-language summary built from this paper's discourse-graph nodes. Numbers and findings link back to specific EVD nodes — click any link to drill in.

### Question

Can a large language model write peer reviews of machine-learning papers that are as good as the reviews human experts post on OpenReview? The authors set up a head-to-head contest between five "reviewers" — four LLMs and one human — and let expert judges pick which reviews they preferred. They also test what happens when you feed the LLM more of the venue's reviewing context, like the conference review form, code of ethics, and area-chair guidelines. See [[QUE - How do LLM-generated academic reviews compare to human reviews in quality and alignment with reviewer preferences?]].

### Methods

**Design.** The authors ran three nested studies on the same paper corpus: a pairwise-preference tournament called Reviewer Arena, a context-ablation comparing GPT-4 reviews against human reviews across five increasingly rich prompt bundles, and a small blind 2 × 2 cross-evaluation in which both humans and GPT-4 graded each other's reviews on a rubric.

**Tools.** Four commercial LLMs played the role of reviewer: GPT-4 Turbo (snapshot Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), and Command R+. The fifth competitor was the human OpenReview reviewer of record. The ranking used a **Bradley-Terry model** — a logistic-regression method that turns pairwise win counts into a single score per competitor, the way chess Elo ratings work. The autoevaluation pass used **PPI++**, a statistical correction (Angelopoulos et al. 2023) that combines a few real human labels with many model-generated labels. Reviews were generated through the authors' OpenReviewer pipeline and judged on the in-house Reviewer Arena platform.

**Procedure.** The pipeline pulls open-access papers and their human reviews from OpenReview (ICLR and NeurIPS) and from open-access Nature journals. For each paper, the system generates one review per LLM under the full P5 context — paper text, review form, reviewer guide, code of ethics, code of conduct, area-chair guidelines, and prior-year statistics. The Reviewer Arena randomly assigns 2 of the 5 competitors to each paper, hides the authorship, and asks 5 expert evaluators which review they prefer. The authors tally wins into an N by N matrix, fit Bradley-Terry coefficients by minimizing binary cross-entropy under the constraint that Claude's score equals zero (so ranks are relative), and sort to produce the leaderboard. They repeat the protocol with GPT-4 Turbo as the judge for an autoevaluation pass. Separately, they ablate the prompt context P1 through P5 and compare GPT-4's average recommendation score against the human average. A final 5% sub-sample of the 150 papers feeds a blind 2 × 2 rubric study where each review (human-written or GPT-4 P5-written) is scored on three 0-to-5 questions by both a human ICLR 2023 reviewer and GPT-4.

**Sample.** The source pool spans **ICLR 2024 (7,404 papers), ICLR 2023 (4,955), NeurIPS 2023 (12,345), NeurIPS 2022 (10,411)**, plus 16 open-access Nature titles. From this pool the authors sampled **150 papers** for Reviewer Arena, each judged by 2 of 5 reviewers under the eyes of **5 expert human evaluators**. The blind rubric sub-study used a 5% random subset of those 150 papers, roughly 7 to 8 papers, scored by 1 ICLR 2023 reviewer plus GPT-4.

### Findings

- **GPT-4 Turbo edged out humans in head-to-head review preference.** Across 150 papers and 5 expert judges, GPT-4 Turbo took rank 1 with a Bradley-Terry score of **0.558**, ahead of the human OpenReview reviewer at **0.501**. Command R+ came third (0.277), Claude 3 Opus fourth (0.000, the reference anchor), and Gemini Pro last (-0.522). When GPT-4 Turbo itself acted as the judge instead of humans, it still ranked itself first (0.179) but the gap to humans collapsed to 0.060 BT points, and the weaker models reordered substantially. [[EVD - GPT-4 Turbo ranked first in human preference for academic review quality with score 0.558 - @tyserAIDrivenReviewSystems2024]]

- **Adding area-chair guidelines is what makes GPT-4's scores match humans.** Without venue-specific stringency context, GPT-4 graded papers far too generously: human mean recommendation was **5.88 ± 1.61**; GPT-4 with just paper text plus the review form (P1) averaged **7.21**, and adding the reviewer guide (P2) and ethics codes (P3) pushed it slightly higher to 7.58 and 7.62. Only when the area-chair guidelines were added (P4) did the LLM swing to 4.61 — now too stringent. The full P5 bundle (adding prior-year statistics) settled at **5.36**, within roughly half a point of the human average. The Confidence dimension, however, stayed skewed higher than human even at P5. [[EVD - LLM review recommendation scores exceeded human scores without area-chair context but matched with it - @tyserAIDrivenReviewSystems2024]]

- **Humans rated GPT-4 P5 reviews as comparable to human reviews on a rubric.** On a 0-to-5 rubric covering whether a review explains its score, guides authors to improve, and contains paper-specific content, the human evaluator rated human-written reviews at **4.80 / 4.66 / 4.53** and GPT-4 P5 reviews at **4.76 / 4.79 / 4.68** — statistically indistinguishable on a 7-to-8 paper sample. But when GPT-4 was the evaluator, it scored its own reviews higher (4.65) than human reviews (4.27) on the score-explanation question, a sign of self-enhancement bias. A confusion-matrix check showed the LLM was more prone to false-rejects than false-accepts: **22 papers** the LLM rated 4 or below were actually rated 6 or above by humans, versus only **8** the other way. [[EVD - LLM reviews scored comparably to human reviews on all three expert evaluation criteria - @tyserAIDrivenReviewSystems2024]]

### Claim supported

These findings collectively support the claim that [[CLM - LLM review quality is comparable to human review quality when provided with sufficient contextual information]]. The practical caveat is that the comparability hinges almost entirely on the prompt: the LLM is over-generous out of the box, and only the carefully assembled venue-specific bundle of area-chair guidelines plus prior-year score statistics drags its calibration into the human range. A journal or conference deploying this would need to maintain those documents annually, and a 5-judge preference signal on 150 papers is a thin reed for the "as good as humans" headline.

### Caveats

- **The match-to-human result depends on yearly-updated venue documents and biased preference judgments.** The P5 context bundle relies on area-chair guidelines, codes of ethics, and prior-year statistics that each conference rewrites annually, so the calibration will drift. And human pairwise preferences are known to favor verbose, confident, and self-similar text — biases the authors only partially correct for. [[CVT - LLM review alignment findings based on venue-specific guidelines requiring yearly updates and subject to human preference biases]]

### Methods at a glance

```mermaid
flowchart TD
    A["Open-access source venues<br/>ICLR 2023/24, NeurIPS 2022/23<br/>Nature open-access titles"] --> B["OpenReviewer pipeline<br/>extracts paper text + human reviews"]
    B --> C["<b>150 papers sampled</b><br/>for Reviewer Arena"]
    C --> D["Generate one review per LLM<br/>under P5 context bundle<br/>(paper + review form + RG +<br/>CE + CC + AC + statistics)"]
    D --> E{"Three evaluation studies"}
    E --> F["Reviewer Arena<br/>2 of 5 reviewers / paper<br/>5 expert judges<br/>pairwise preference"]
    E --> G["Context ablation<br/>P1 through P5<br/>mean ± SD per dimension"]
    E --> H["Blind 2 x 2 rubric<br/>5% sub-sample (~7-8 papers)<br/>writer x evaluator<br/>0-to-5 Likert"]
    F --> I["Win matrix W<br/>Bradley-Terry fit<br/>logistic regression"]
    G --> J["Compare to human<br/>recommendation distribution"]
    H --> K["Per-cell mean score<br/>+ confusion matrix"]
    I --> L["<b>Reviewer leaderboard</b><br/>(Tables 1 & 2)"]
    J --> L
    K --> L

    classDef data fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef step fill:#FFF8E1,stroke:#F57F17,color:#5D4037;
    classDef model fill:#F1F8E9,stroke:#2E7D32,color:#1B5E20;
    classDef result fill:#FCE4EC,stroke:#AD1457,color:#880E4F;
    class A,B,C data;
    class D,E,F,G,H step;
    class I,J,K model;
    class L result;
```
---

## Critical appraisal

> [!info] A risk-of-bias and validity assessment across five domains, synthesized from this paper's discourse-graph nodes. Each domain gets a rating (🟢 Low risk · 🟡 Some concerns · 🔴 High risk) plus a brief, EVD-grounded justification. The TRIPOD-LLM table below covers *reporting compliance*; this section covers *methodological quality*.

| Domain | Rating | Justification |
| --- | :---: | --- |
| **Construct validity** — does the metric actually measure the construct? | 🟡 | Bradley-Terry preference scores capture which review a judge *likes more*, not which review is more *correct*. The authors themselves flag that pairwise preference is colored by verbosity, position, length, and self-enhancement biases (see [[CVT - LLM review alignment findings based on venue-specific guidelines requiring yearly updates and subject to human preference biases]]). The recommendation-score match at P5 is calibration, not accuracy — it does not establish that the LLM is identifying the *same* papers as accept or reject as humans (the confusion matrix shows 22 false-rejects and 8 false-accepts on the rubric sub-sample). |
| **Internal validity** — could the comparison be biased? | 🔴 | Three serious threats. (1) The autoevaluation uses GPT-4 Turbo as judge of its own reviews, the classic LLM-judge-of-LLM problem; the gap to human compresses from 0.057 BT under human judges to 0.060 BT under GPT-4 self-judging only because Command R+ collapses, not because the gap is real. (2) The 2 of 5 random pairing in Reviewer Arena means each LLM faces only a fraction of all matchups, and per-cell sample sizes are not reported. (3) The blind rubric sub-study (~7-8 papers, 1 human evaluator described only as "an ICLR 2023 reviewer") leaves the score-comparability headline resting on a single rater. |
| **External validity** — do findings generalize? | 🔴 | The corpus is restricted to two ML conferences (ICLR, NeurIPS) plus open-access Nature journals; the authors do not report discipline mix or paper-type stratification. The P5 calibration depends on documents (area-chair guidelines, prior-year statistics) that the authors explicitly say "require yearly updates," so any deployment outside the calibrated venue-year would lose the match-to-human result. The 150-paper Arena set and the 7-to-8-paper rubric sub-set are too small to support generalization to a journal-screening workflow. |
| **Statistical rigor** — appropriate uncertainty + comparisons? | 🔴 | No confidence intervals on Bradley-Terry scores (a 0.558 vs. 0.501 gap with N=150 papers and 5 judges is plausibly within sampling noise). No inter-evaluator agreement reported for the 5 expert judges — the BT ranking treats their preferences as homogeneous. No multiple-comparison correction across the 5 review dimensions × 6 context conditions in Figure 14. The rubric sub-study reports means but no statistical tests at N ≈ 7 (per TRIPOD-LLM 16d ⚠️). |
| **Reproducibility** — code, data, determinism? | 🟡 | Live deployments exist at openreviewer.com, papersWithReviews.com, and reviewerarena.com (TRIPOD-LLM 14e ⚠️), and Listings 1–2 in Appendix P show the win-matrix and Bradley-Terry code. But no static dataset DOI is cited, no GitHub repository link appears in the text, and inference parameters for the Reviewer Arena LLMs (temperature, top_p, system prompt) are not reported (TRIPOD-LLM 6c ⚠️), so the GPT-4 review numbers carry irreducible run-to-run variance. |

**Bottom line.** The paper makes a real contribution by showing that GPT-4 with a fully assembled venue-context bundle can produce reviews that judges prefer at roughly the same rate as human OpenReview reviews. But the headline "LLM ≥ human" rests on a 5-judge preference tournament over 150 papers, no confidence intervals, an 8-paper rubric sub-study with one human evaluator, and a context bundle that has to be rebuilt each year. Anyone considering deployment should treat this as a feasibility demonstration on ML conference papers, not as evidence that LLM reviews are deployment-ready in any reviewing pipeline that cares about catching weak papers (where the confusion matrix shows GPT-4 mis-rejects 22 of the rubric sub-sample's strong submissions).

> [!tip] **Applicable external appraisal frameworks beyond TRIPOD-LLM** (already covered by the table below): **HELM** (Liang et al. 2022) for holistic LLM-evaluation principles · **Datasheets for Datasets** (Gebru et al. 2021) for the evaluation corpus · **Model Cards** (Mitchell et al. 2019) for the LLMs being evaluated

---

## TRIPOD-LLM reporting summary

> [!info] Reporting compliance for this paper, mapped to the TRIPOD-LLM checklist (Methods items 5a–15 and Results items 16a–18). Compliance icons: ✅ fully reported · ⚠️ partially reported / unclear · ❌ should be reported but not reported · ➖ not applicable to this study. Item 17 (Performance) is reported per-EVD; see each EVD's `## Other Notes`.

| # | Item | ✓ | Reported in this study |
| --- | --- | :---: | --- |
| **5a** | Data sources | ✅ | Open-access conference and journal venues: ICLR 2023/2024, NeurIPS 2022/2023 (with OpenReview reviews), open-access Nature journals (12 Nature titles + 4 Communications titles, Table 4). arXiv used for Papers with Reviews deployment. |
| **5b** | Data points + distribution | ⚠️ | Source-pool sizes given (ICLR 2024: 7,404; ICLR 2023: 4,955; NeurIPS 2023: 12,345; NeurIPS 2022: 10,411 — Table 3). Reviewer Arena uses 150 papers with 2-of-5 reviewers per paper. Discipline / topic distribution not characterized. |
| **5c** | Date range of data | ⚠️ | ICLR 2023/2024 and NeurIPS 2022/2023 implied by venue. Specific date ranges, GPT-4 inference dates, and OpenReview pull dates not explicitly stated; only "GPT-4 Turbo (Turbo-2024-04-09)" snapshot identifier is given. |
| **5d** | Pre-processing / quality checks | ❌ | Pipeline figures (Figs. 1–3, 6, 7) describe the system but no preprocessing or quality-control protocol (e.g., paper-text extraction, table/figure handling, deduplication) is reported. |
| **5e** | Missing / imbalanced data | ❌ | Not addressed. Class balance across paper types / accept-reject status not reported; no handling described for papers with missing reviews. |
| **6a** | LLM name + version | ✅ | Reviewer Arena: GPT-4 Turbo (Turbo-2024-04-09), Claude 3 Opus, Gemini Pro (Bard), Command R+. Ablation/Blind eval: GPT-4 (snapshot not specified). Fine-tuning experiments (Appendix N): Gemma-2-9b-it, Llama-3.1-8b, Mistral-Nemo-Instruct-2407 (4-bit quantized). |
| **6b** | Development process | ⚠️ | Reviewer Arena LLMs used as-is (no fine-tuning). Open-weight LLMs in Appendix N fine-tuned with data augmentation, hyperparameter tuning (Optuna), and bias correction; described in prose, not in formal training-procedure detail. |
| **6c** | Inference settings / prompting | ⚠️ | Context bundles (P1–P5) defined; meta-prompt for editorial roles given (Fig. 29); review-question prompts shown for several venues (Tables 10–12). Inference parameters (temperature, top_p, max tokens, system prompt for Reviewer Arena LLMs) not reported. |
| **6d** | Output | ✅ | Reviews containing 5 standardized subscores (Correctness, Tech Novelty, Empirical Novelty, Recommendation, Confidence) plus free-text. Editorial role-play outputs structured "Review score: …; [Review decision Reject/Accept]". |
| **6e** | Classification thresholds | ➖ | Not applicable — primary outputs are continuous review scores and pairwise preferences, not classification labels. |
| **7a** | Quality metrics | ✅ | Bradley-Terry coefficients; mean ± SD per review dimension; 0–5 Likert rubric scores; weighted Jaccard similarity for summary-overlap; confusion-matrix counts (Appendix E). |
| **7b** | Relevance to downstream | ⚠️ | Downstream use cases described qualitatively (author feedback, conference desk-rejection, trend analysis) but no formal utility analysis (e.g., reviewer-time savings, accept/reject decision impact) reported. |
| **7c** | Outcome definition | ✅ | Each outcome (BT-rank, recommendation score, rubric score) defined alongside the table/figure that reports it. |
| **7d** | Subjective interpretation | ⚠️ | Pairwise preference is acknowledged as subjective; LLM biases (position, verbosity, self-enhancement, length, sentiment, negativity) discussed and partially mitigated for the human-preference predictor, but not for the Reviewer Arena human evaluators. No human-evaluator IAA reported. |
| **7e** | Comparison | ✅ | LLMs compared to human OpenReview reviewers (BT, recommendation ablation, blind rubric); LLMs compared against each other (Reviewer Arena); human-judge vs. LLM-judge comparison (Tables 1 vs. 2). |
| **8a** | Annotation guidelines | ❌ | Reviewer-Arena evaluators were "asked which of the two reviews … they preferred"; no formal preference-judgment guideline document or training described. Blind-eval rubric (3 questions, 0–5) defined but no scoring guideline. |
| **8b** | Annotators + IAA | ❌ | 5 expert evaluators in Reviewer Arena; "an ICLR 2023 reviewer" for the blind rubric. No inter-annotator agreement, no per-evaluator workload, no overlap structure reported. |
| **8c** | Annotator background | ⚠️ | Described only as "expert evaluators" / "ICLR 2023 reviewer." No discipline, seniority, demographics, or recruitment process reported. |
| **9a** | Prompt design | ⚠️ | Cumulative context conditions P1–P5 and editorial-role meta-prompt shown; no systematic prompt-engineering search reported. Prompts for autoeval / preference judgment not shown. |
| **9b** | Prompt-development data | ❌ | Not reported. Context documents (review form, ethics, area-chair guidelines) described as venue-supplied; no prompt-tuning held-out set described. |
| **10** | Summarization | ✅ | GPT-4 used (with function calling) to extract structured summary points from each review and compute weighted Jaccard overlap (Appendix I). |
| **11** | Instruction tuning / alignment | ✅ | Open-weight LLMs (Gemma-2-9b-it, Llama-3.1-8b, Mistral-Nemo-Instruct-2407) fine-tuned for the LMSYS Chatbot Arena Human Preference Predictions Kaggle competition with data augmentation + Optuna hyperparameter search + length / sentiment / negative-pattern penalties (Appendix N). Reviewer-Arena LLMs not fine-tuned. |
| **12** | Compute | ❌ | Not reported. Quantization to 4 bits and sequence-length / batch-size grids mentioned for fine-tuning, but no GPU-hours, hardware, or cost figures. |
| **13** | Ethical approval | ⚠️ | Section 5 + Appendix M discuss preventive ethical actions for LLM reviewing (declaration, gatekeeping checklist, debiasing). No IRB / ethics-board approval reported for the human evaluators. |
| **14a** | Funding | ❌ | Not reported in the manuscript. |
| **14b** | Conflicts of interest | ❌ | Not reported. |
| **14c** | Protocol | ❌ | No pre-registered or publicly archived protocol referenced. |
| **14d** | Registration | ➖ | Not applicable (not a clinical study). |
| **14e** | Data availability | ⚠️ | Live deployments at openreviewer.com, papersWithReviews.com, reviewerarena.com. Reviews and scores stated to be publicly available online; no static dataset DOI / archive cited. |
| **14f** | Code availability | ⚠️ | Two key Python listings shown (Listing 1: win-matrix; Listing 2: BT log-likelihood, Appendix P). No GitHub repository link in the manuscript text reviewed. |
| **15** | Patient/public involvement | ➖ | Not applicable. |
| **16a** | Flow of data | ⚠️ | Reviewer Arena: 150 papers → 2-of-5 reviewers per paper. Blind-eval sub-study: "5% random sample" of 150 (~7–8 papers). Per-condition N for Figure 14 ablation not explicitly reported. |
| **16b** | Characteristics | ⚠️ | Source venues and discipline mix (ML conferences + Nature open-access journals) implied; per-paper characteristics (length, subfield, accept/reject status) not tabulated for the 150-paper Arena set. |
| **16c** | Distribution comparison | ➖ | Not applicable (no clinical-subgroup comparison). Authors do compare LLM-vs.-human score distributions (Figs. 30–31). |
| **16d** | N per analysis | ⚠️ | Reviewer Arena: 150 papers, 5 evaluators (Tables 1–2). Blind eval: ~7–8 papers (5% of 150) (Table 5). Recommendation-score ablation (Fig. 14): N not reported per condition. Source-pool counts in Table 3. |
| **17** | Performance | (per-EVD) | Reported per-EVD. See each EVD's `## Other Notes` for the EVD-specific BT scores, recommendation means/SDs, and 2 × 2 rubric scores. |
| **18** | LLM updating | ⚠️ | Authors note that venue-dependent context documents "require yearly updates" and that the live Papers with Reviews / Reviewer Arena deployments are designed to ingest fresh data continuously. No model-updating / re-training cadence described. |

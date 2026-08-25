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
  - top/data-transparency/level-2-shared
  - top/code-transparency/not-applicable
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/low-risk
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/high-risk
  - rigor/sample-size-estimation/not-done
  - rigor/study-type/exploratory
  - rigor/data-leakage/addressed
  - integrity/ethical-approval/not-applicable
  - integrity/funding-disclosure/disclosed
  - integrity/coi-disclosure/disclosed
  - integrity/statcheck/not-applicable
doi: 10.3390/diagnostics15121451
citationCount: 3
citationCountSource: OpenCitations
predatoryPublisherFlag: false
critiqueStatus: none
authors:
  - "Daniel-Corneliu Leucuța — Department of Medical Informatics and Biostatistics, Iuliu Hațieganu University of Medicine and Pharmacy, 400349 Cluj-Napoca, Romania"
  - "Andrada Elena Urda-Cîmpean — Department of Medical Informatics and Biostatistics, Iuliu Hațieganu University of Medicine and Pharmacy, 400349 Cluj-Napoca, Romania"
  - "Dan Istrate — Department of Medical Informatics and Biostatistics, Iuliu Hațieganu University of Medicine and Pharmacy, 400349 Cluj-Napoca, Romania"
  - "Tudor Drugan — Department of Medical Informatics and Biostatistics, Iuliu Hațieganu University of Medicine and Pharmacy, 400349 Cluj-Napoca, Romania"
authorTrackRecord: clean
authorTrackRecordChecked: 3 of 4 authors (ORCID on record)
pubType: journal-article
selfCitationRate: 0.000
selfCitationChecked: "37 of 37 references had author metadata"
doajListed: true
pubpeerCommentCount: 0
crossNodeChecked: 2
crossNodeCorroborated: 2
apaTitle: "Risk of Bias Assessment of Diagnostic Accuracy Studies Using QUADAS 2 by Large Language Models"
apaContainer: "Diagnostics"
apaYear: 2025
apaVolume: "15"
apaIssue: "12"
apaPages: "1451"
apaLandingUrl: "https://www.mdpi.com/2075-4418/15/12/1451/pdf"
apaAuthors:
  - given: "Daniel-Corneliu"
    family: "Leucuța"
  - given: "Andrada Elena"
    family: "Urda-Cîmpean"
  - given: "Dan"
    family: "Istrate"
  - given: "Tudor"
    family: "Drugan"
peerReviewStatus: not-checked
peerReviewNote: "MDPI blocked automated access (403)"
citekey: leucutaRiskBiasAssessment2025
nodeTypeId: node_WloBZlAOaEodMKQ82S_Dn
nodeInstanceId: 019dd17a-f942-782f-99e1-d83f3cbbc264
---

> [!success] **TL;DR**
> This is a careful, transparent snapshot of how four free chatbots perform at one slice of risk-of-bias appraisal, and the qualitative error analysis is the paper's most durable contribution — it names specific reasoning failures (consecutive sampling under case-control, exclusion-stage confusion) that any future LLM-for-systematic-review tool will need to fix. The headline 72.95% accuracy should not be taken as a benchmark for LLM capability, because the small sample, single prompt, and free-tier model versions all push the estimate toward a lower bound.

## Structured abstract

> [!info] A plain-language summary built from this paper's discourse-graph nodes. Numbers and findings link back to specific EVD nodes — click any link to drill in.

### Question

Can off-the-shelf chatbots judge how trustworthy a medical study is the same way a trained methodologist would? The authors test four popular general-purpose large language models on QUADAS-2, a standard checklist for rating risk of bias in diagnostic-accuracy studies. They feed each model the same 10 papers and the same prompt, then score every answer against a two-expert human consensus. See [[QUE - How does LLM performance vary across specific structured tasks in systematic review and evidence appraisal workflows?]].

### Methods

**Design.** The authors ran a cross-sectional benchmark of four LLMs against a two-expert consensus reference, paired with a qualitative analysis of the reasoning errors the models made.

**Tools.** Four general-purpose chatbots accessed through their free public web interfaces — ChatGPT 4o (OpenAI), x.AI Grok 3, Gemini 2.0 Flash (Google), and DeepSeek V3. The rubric was QUADAS-2 (Whiting et al. 2011), a standard checklist for diagnostic-accuracy studies covering four domains — patient selection, index test, reference standard, and flow and timing — with 11 yes/no/unclear signaling questions in total. The full per-article LLM responses were captured in Supplementary Table S1.

**Procedure.** The authors searched PubMed on 9 May 2025 for diagnostic-accuracy studies on diabetes, kept only original research with free full text, and screened for medical-specialty diversity. They uploaded each paper as a PDF into a fresh chat session for every model, so no model could carry context from one article to the next. They sent every model the exact same prompt, asking it to answer each QUADAS-2 signaling question and give a low, high, or unclear risk-of-bias verdict per domain, plus written reasoning. Two human authors independently scored every paper and resolved disagreements by consensus to set the reference. An LLM answer counted as correct only if both the answer and the supporting argument matched the human reference.

**Sample.** PubMed search returned candidate diagnostic-accuracy articles, screened for specialty diversity, leaving 10 retained articles spanning seven medical fields (cardiology, gastroenterology, neurology, rheumatology, sleep medicine, vascular surgery, and ophthalmology), plus 2 non-diagnostic control articles handled separately. The unit of analysis is the signaling-question assessment: 10 articles times 11 questions times 4 models equals 440 LLM assessments. Two authors from a medical informatics and biostatistics department served as the human reference raters.

### Findings

- **The four chatbots got about three out of four answers right on average.** Across 110 signaling-question assessments per model, the mean correct rate was 72.95%. Grok 3 led at 77.27% (85/110), followed by ChatGPT 4o at 75.45%, DeepSeek V3 at 71.82%, and Gemini 2.0 Flash at 67.27%. Accuracy varied sharply by QUADAS-2 domain: flow and timing was easiest at 80.63%, while reference standard was hardest at 63.75%. About 3% of "right" answers were actually backed by wrong reasoning — a small but real reminder that matching the verdict does not mean understanding the study. [[EVD - Mean correct QUADAS-2 assessment rate across four LLMs was 72.95% with Grok 3 highest at 77.27% and Gemini 2.0 Flash lowest at 67.27% - @leucutaRiskBiasAssessment2025]]

- **The mistakes followed a pattern, not random noise.** In the patient-selection domain — the second-hardest at 65.83% — the models made four recurring kinds of error. They misunderstood "consecutive sampling" inside case-control or subgroup studies, treating it as logically impossible. They drew unjustified inferences from what authors did or did not say, treating silence as proof. They picked one of two contradictory author statements rather than calling the design uninterpretable. And they misjudged whether a study population (for example, "patients with suspected disease") was representative. The models also confused exclusions made when picking patients with exclusions made when running the analysis, which belong in a different QUADAS-2 domain. [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]]

### Claim supported

These findings support the broader claim that [[CLM - LLMs achieve moderate accuracy on structured quality appraisal tasks but cannot yet substitute for expert human judgment]], and the more specific point that [[CLM - LLM performance on structured checklist tasks varies substantially by item type with simpler factual items showing higher agreement than items requiring methodological judgment]]. For someone considering plugging an off-the-shelf chatbot into a systematic-review workflow, the message is: a 73% mean accuracy with systematic blind spots on study-design judgment is not safe to run unsupervised. These tools could realistically pre-screen or assist a human reviewer, but every domain-level verdict still needs a methodologist to check.

### Caveats

- **Only one prompt was tested across all four models.** The authors deliberately used a single, simple prompt to mimic a non-expert user, with no per-model tuning. Better prompts almost certainly would lift accuracy, so the 67–77% range is best read as a floor rather than a ceiling. [[CVT - A single standardized prompt was used across all LLMs without prompt engineering potentially underestimating LLM capabilities in QUADAS-2 assessment]]

- **Only the free public web versions of each chatbot were tested.** Paid tiers, API access, and newer model snapshots may behave differently. The numbers reflect what a typical clinician-researcher with a free account would see, not the frontier of each vendor's stack. [[CVT - Only publicly available web-based LLM interfaces were used rather than APIs potentially missing superior performance of paid or fine-tuned model versions]]

### Methods at a glance

```mermaid
flowchart TD
    A["PubMed search 9 May 2025<br/>'diagnostic accuracy' AND diabetes<br/>free full-text"] --> B["Filter to original<br/>diagnostic-accuracy articles"]
    B --> C["Screen for<br/>medical-specialty diversity"]
    C --> D["<b>10 articles retained</b><br/>(7 specialties)<br/>+ 2 non-diagnostic controls"]
    D --> E["Upload PDF into<br/>fresh chat session<br/>per article per model"]
    E --> F["Issue identical prompt<br/>to all 4 models"]
    F --> G{"4 LLMs scored zero-shot"}
    G --> H["ChatGPT 4o"]
    G --> I["x.AI Grok 3"]
    G --> J["Gemini 2.0 Flash"]
    G --> K["DeepSeek V3"]
    H --> L["<b>440 LLM assessments</b><br/>(11 Qs x 10 articles x 4 models)"]
    I --> L
    J --> L
    K --> L
    L --> M["Score vs.<br/>2-expert consensus<br/>(answer AND reasoning must match)"]
    M --> N["Quantitative:<br/>% correct per model,<br/>per domain, per question"]
    M --> O["Qualitative:<br/>thematic analysis<br/>of reasoning errors"]

    classDef data fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef step fill:#FFF8E1,stroke:#F57F17,color:#5D4037;
    classDef model fill:#F1F8E9,stroke:#2E7D32,color:#1B5E20;
    classDef result fill:#FCE4EC,stroke:#AD1457,color:#880E4F;
    class A,B,C,D data;
    class E,F,M step;
    class G,H,I,J,K model;
    class L,N,O result;
```
---

## Critical appraisal

> [!info] A risk-of-bias and validity assessment across five domains, synthesized from this paper's discourse-graph nodes. Each domain gets a rating (🟢 Low risk · 🟡 Some concerns · 🔴 High risk) plus a brief, EVD-grounded justification. The TRIPOD-LLM table below covers *reporting compliance*; this section covers *methodological quality*.

| Domain | Rating | Justification |
| --- | :---: | --- |
| **Construct validity** — does the metric actually measure the construct? | 🟡 | "Percent correct" is a sensible first-pass metric, but the construct of interest — "is this LLM safe to use for risk-of-bias appraisal?" — is not the same as "does the LLM match the human verdict on average". The strict scoring rule (answer plus reasoning must both match) helps, and the qualitative error analysis [[EVD - LLMs demonstrated systematic reasoning errors in QUADAS-2 patient selection domain including misinterpreting consecutive sampling and case-control design - @leucutaRiskBiasAssessment2025]] shows the systematic blind spots that raw accuracy hides. No precision/recall, no inter-rater statistic between LLM and human, and no domain-level risk-of-bias judgment was scored end-to-end. |
| **Internal validity** — could the comparison be biased? | 🟢 | The four models saw identical prompts on identical PDFs in fresh sessions, with no context carryover. The human reference was set by two-rater consensus before LLM scoring. There is no plausible test-set contamination risk for QUADAS-2 verdicts on these specific 2024–2025 articles, and the strict "answer plus reasoning" rule rules out lucky guesses. The main residual concern is that the human reference itself rests on only two raters with no reported pre-consensus agreement (TRIPOD-LLM 8b ⚠️). |
| **External validity** — do findings generalize? | 🔴 | Three large constraints. First, the corpus is 10 papers — a small, opportunistic sample drawn from a diabetes-keyword PubMed search. Second, only one prompt was tested per model, deliberately a "naive user" prompt; see [[CVT - A single standardized prompt was used across all LLMs without prompt engineering potentially underestimating LLM capabilities in QUADAS-2 assessment]]. Third, only free public web versions of the four models were tested; see [[CVT - Only publicly available web-based LLM interfaces were used rather than APIs potentially missing superior performance of paid or fine-tuned model versions]]. The findings describe one slice of model-times-prompt space, not the capability ceiling. |
| **Statistical rigor** — appropriate uncertainty + comparisons? | 🔴 | Results are reported as raw counts and percentages with no confidence intervals, no significance tests between models, no inter-rater agreement statistic between LLM and human, and no multiple-comparison correction across the 4 models times 4 domains times 11 signaling questions matrix. With only 20–40 assessments per domain per model, the apparent ranking of models is well within sampling noise, and Gemini's 50% on patient selection (n=30) has wide error bars the paper does not show. |
| **Reproducibility** — code, data, determinism? | 🟡 | Supplementary Table S1 contains the full per-article LLM responses, the prompt is reproduced verbatim, and the models and study window are named (TRIPOD-LLM 14e ✅). But four web-UI chatbots with undisclosed temperature, top-p, seed, and system-prompt settings (TRIPOD-LLM 6c ⚠️) are intrinsically non-deterministic; rerunning today against floating model versions would not reproduce the numbers exactly. No code repository applies because no code was written. |

**Bottom line.** This is a careful, transparent snapshot of how four free chatbots perform at one slice of risk-of-bias appraisal, and the qualitative error analysis is the paper's most durable contribution — it names specific reasoning failures (consecutive sampling under case-control, exclusion-stage confusion) that any future LLM-for-systematic-review tool will need to fix. The headline 72.95% accuracy should not be taken as a benchmark for LLM capability, because the small sample, single prompt, and free-tier model versions all push the estimate toward a lower bound. Before a result like this is deployment-ready, a real evaluation would need many more articles, multiple prompts per model, frozen API model snapshots, confidence intervals, and a domain-level risk-of-bias verdict scored against an inter-rater statistic — not just a percent-correct table.

> [!tip] **Applicable external appraisal frameworks beyond TRIPOD-LLM** (already covered by the table below): **MI-CLAIM** (Norgeot et al. 2020) for clinical-AI minimum information · **MINIMAR** (Hernandez-Boussard et al. 2020) for medical-AI reporting · **PROBAST+AI** (Wolff et al. 2019 base; AI extension in development) for prediction-model risk of bias · **STARD-AI** and **QUADAS-AI** (in development) for AI-assisted diagnostic-accuracy assessment.

---

## TRIPOD-LLM reporting summary

> [!info] Reporting compliance for this paper, mapped to the TRIPOD-LLM checklist (Methods items 5a–15 and Results items 16a–18). Compliance icons: ✅ fully reported · ⚠️ partially reported / unclear · ❌ should be reported but not reported · ➖ not applicable to this study. Item 17 (Performance) is reported per-EVD; see each EVD's `## Other Notes`.

| # | Item | ✓ | Reported in this study |
| --- | --- | :---: | --- |
| **5a** | Data sources | ✅ | 10 open-access PubMed diagnostic-accuracy articles (search "diagnostic accuracy"[TI/AB] AND diabetes[TI/AB], 9 May 2025, free full-text) + 2 non-diagnostic control articles. Articles uploaded as PDFs from publisher / PMC. |
| **5b** | Data points + distribution | ✅ | 10 articles spanning cardiology (2), gastroenterology (2), neurology (1), rheumatology (1), sleep medicine (1), vascular surgery (1), ophthalmology (2). 11 QUADAS-2 signaling questions per article; 110 assessments per LLM; 440 LLM assessments in total. Per-domain n: patient selection 30, index test 20, reference standard 20, flow and timing 40 (per model). |
| **5c** | Date range of data | ⚠️ | Search date 9 May 2025; "most recent papers first" — implies recently published articles, but exact publication-date span of the 10 articles not given in the text (references list spans 2024–2025). |
| **5d** | Pre-processing / quality checks | ⚠️ | PDFs sourced from publisher's site or PubMed Central; no pre-processing or PDF-conversion verification reported. New chat session per article to prevent context carryover. |
| **5e** | Missing / imbalanced data | ⚠️ | No imputation. "Not applicable" answers were a permitted response option. Class imbalance per signaling question not addressed. |
| **6a** | LLM name + version | ⚠️ | ChatGPT 4o, x.AI Grok 3, Gemini 2.0 Flash, DeepSeek V3 — all via public web UIs. Specific model build dates / API versions not reported (though study window dated by 9 May 2025 search). |
| **6b** | Development process | ➖ | No development; off-the-shelf zero-shot use of public LLM web interfaces. |
| **6c** | Inference settings / prompting | ⚠️ | Prompt text reproduced verbatim (p. 3). New session per article. Identical prompt across all four models. Inference parameters (temperature, top_p, max tokens, system prompt) not reported (default web-UI settings). |
| **6d** | Output | ✅ | Per signaling question: yes / no / unclear / not applicable; per domain: low / high / unclear risk of bias; followed by free-text rationale. |
| **6e** | Classification thresholds | ➖ | No probability thresholds (LLMs return categorical labels directly). |
| **7a** | Quality metrics | ⚠️ | Counts and percentages of correct assessments overall, per model, per domain, and per signaling question. No precision/recall/F1, no inter-rater statistic between LLM and humans, no confidence intervals or significance tests. |
| **7b** | Relevance to downstream | ⚠️ | Discussion frames LLMs as "complementary tools" requiring "compulsory human supervision" in systematic reviews; no formal downstream-utility analysis (e.g., reviewer time saved, screening throughput). |
| **7c** | Outcome definition | ✅ | Assessment "considered correct only if it matched the human expert's answer and included a proper argument." Identical answer with incorrect argument scored as incorrect. |
| **7d** | Subjective interpretation | ⚠️ | Reasoning-error categorization is qualitative and investigator-driven; categorization by single team without inter-rater agreement on the qualitative themes themselves. |
| **7e** | Comparison | ⚠️ | Four LLMs compared head-to-head; no comparison to a non-LLM baseline (e.g., random / majority class). Comparison to prior LLM RoB studies discussed narratively in Discussion. |
| **8a** | Annotation guidelines | ✅ | QUADAS-2 instrument (Whiting et al. 2011) used as the labeling rubric; 4 domains, 11 signaling questions, low/high/unclear domain judgements. |
| **8b** | Annotators + IAA | ⚠️ | Two human experts independently assessed each article and resolved disagreements by consensus. Pre-consensus inter-rater agreement (κ or % agreement) not reported. |
| **8c** | Annotator background | ⚠️ | Authors are from the Department of Medical Informatics and Biostatistics, Iuliu Hațieganu University of Medicine and Pharmacy. Specific clinical-methodology training of the two assessors not detailed. |
| **9a** | Prompt design | ⚠️ | Single hand-written prompt reproduced verbatim. Authors explicitly note no prompt engineering: "we used only one single standardized prompt to ensure comparability across LLMs… We used a simple prompt to enact a scenario where researchers that are not trained in prompt engineering would use LLMs." |
| **9b** | Prompt-development data | ❌ | Not reported. No held-out development set or prompt-tuning corpus described. |
| **10** | Summarization | ➖ | Not applicable (RoB classification, not summarization). |
| **11** | Instruction tuning / alignment | ➖ | No fine-tuning. Off-the-shelf models. |
| **12** | Compute | ❌ | Not reported. (Authors note PDF-processing time was "adequate and similar between ChatGPT 4o, Grok 3, and Gemini 2.0 flash, but longer for DeepSeek V3" — qualitative only, no wall-clock numbers.) |
| **13** | Ethical approval | ➖ | "Institutional Review Board Statement: Not applicable." No human-subjects data; analysis on published articles. |
| **14a** | Funding | ✅ | "This research received no external funding." |
| **14b** | Conflicts of interest | ✅ | "The authors declare no conflicts of interest." |
| **14c** | Protocol | ❌ | Not reported. No prospective protocol referenced. |
| **14d** | Registration | ➖ | Not registered (not a clinical study). |
| **14e** | Data availability | ✅ | "Data are contained within the article or Supplementary Material." Supplementary Table S1 contains full per-article LLM responses + reasoning-error annotations (https://www.mdpi.com/article/10.3390/diagnostics15121451/s1). |
| **14f** | Code availability | ➖ | No code was developed (web-UI prompting only); no code repository applicable. |
| **15** | Patient/public involvement | ➖ | Not applicable. |
| **16a** | Flow of data | ✅ | PubMed search (9 May 2025, "diagnostic accuracy"[TI/AB] AND diabetes[TI/AB], free full-text, most recent first) → original diagnostic-accuracy articles only (excluded reviews/systematic reviews/editorials/protocols) → screened for medical-field diversity → 10 articles retained + 2 non-diagnostic controls. |
| **16b** | Characteristics | ✅ | Article-level characteristics described: medical specialty distribution (cardiology ×2, gastroenterology ×2, neurology, rheumatology, sleep medicine, vascular surgery, ophthalmology ×2). Individual article references and topics listed (§3.1, p. 3). |
| **16c** | Distribution comparison | ➖ | Not applicable (no clinical-outcome subgroup / case-mix comparison). |
| **16d** | N per analysis | ✅ | Quantitative analysis: 110 assessments per model (= 11 × 10); per domain n per model: 30 / 20 / 20 / 40. Qualitative reasoning-error analysis: subset of incorrect or wrong-reason assessments across the same 440. Inapplicability test on 2 non-diagnostic articles reported separately (§3.5). |
| **17** | Performance | (per-EVD) | Reported per-EVD. See each EVD's `## Other Notes`. |
| **18** | LLM updating | ➖ | Not applicable (no model updating reported; one-shot evaluation of fixed model versions). |

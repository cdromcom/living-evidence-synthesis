---
dg_type: Source
status: seed
keywords: ""
rating: 3
tags:
  - top/code-quality-fair/2
  - integrity/ai-writing-check/addressed
  - dg/source
  - top/data-quality-fair/6
  - trust/reproducibility/some-concerns
  - top/study-protocol/not-disclosed
  - top/study-registration/not-applicable
  - top/data-transparency/level-1-disclosed
  - top/code-transparency/level-1-disclosed
  - appraisal/construct-validity/some-concerns
  - appraisal/internal-validity/some-concerns
  - appraisal/external-validity/high-risk
  - appraisal/statistical-rigor/some-concerns
  - rigor/sample-size-estimation/not-done
  - rigor/study-type/exploratory
  - rigor/data-leakage/unresolved
  - rigor/baseline-adequacy/not-addressed
  - rigor/train-dev-test/partial
  - rigor/multiple-comparisons/not-addressed
  - rigor/human-baseline/not-addressed
  - rigor/confidence-intervals/not-addressed
  - integrity/ethical-approval/not-applicable
  - integrity/funding-disclosure/not-disclosed
  - integrity/coi-disclosure/not-disclosed
  - top/repository-check/not-addressed
  - top/code-check/not-addressed
  - transparency/effect-size/not-addressed
  - transparency/exact-p-values/not-addressed
  - integrity/spin/addressed
  - rigor/prompt-engineering/partial
  - rigor/chance-corrected-metrics/not-addressed
  - rigor/ablation-experiments/addressed
doi: 10.48550/arXiv.2505.23824
predatoryPublisherFlag: false
authorTrackRecord: not-checked
predatoryPublisherNote: "arXiv preprint — not applicable (not a journal publisher)"
critiqueStatus: not-registered
critiqueNote: "No retraction registry exists for arXiv preprints (checked via DataCite)"
authors:
  - "Zhang, Tianmai M."
  - "Abernethy, Neil F."
pubType: preprint
selfCitationRate: not-assessable
doajListed: not-applicable
pubpeerCommentCount: 0
crossNodeChecked: 3
crossNodeCorroborated: 3
nameConsistency: consistent
apaTitle: "Reviewing Scientific Papers for Critical Problems With Reasoning LLMs: Baseline Approaches and Automatic Evaluation"
apaContainer: "arXiv (NeurIPS 2025 Workshop: AI for Science)"
apaYear: 2026
apaLandingUrl: "https://arxiv.org/abs/2505.23824"
apaAuthors:
  - given: "Tianmai M."
    family: "Zhang"
  - given: "Neil F."
    family: "Abernethy"
peerReviewStatus: not-applicable
peerReviewNote: "arXiv v3 (1 Apr 2026); arXiv comments say accepted and presented at the NeurIPS 2025 AI for Science Workshop; workshop review process not checked"
curatedWithModel: "Claude Sonnet 5"
curatedWithModelDate: 2026-08-25
citekey: zhangReviewingScientificPapers2025a
nodeTypeId: node_WloBZlAOaEodMKQ82S_Dn
nodeInstanceId: 019dd17a-f95d-7879-86c1-70337328c988
---

> [!success] **TL;DR**
> The paper makes a clean, well-instrumented case that today's reasoning LLMs, above all OpenAI's o3, can flag the *specific* author-stated retraction error on about half of withdrawn math and physics papers (o3: 48.2% with PDFs, 50.6% with LaTeX, judged by two LLMs that must both agree), ahead of Gemini 2.5 Pro (39.2%), Gemini 2.5 Flash (38.4%), o4-mini (38.0%) and Claude 3.7 Sonnet (11.0%) on PDFs. In the current arXiv v3 o4-mini's cost edge over o3 is small ($0.038 vs. $0.064 per paper) and Gemini 2.5 Flash matches it for less. The result that holds up cleanly is o3's lead on hit rate and the weak showing of Claude on PDF input.

> [!info] **Version used (updated 2026-11-24)**
> arXiv:2505.23824v3 [cs.CL], 1 Apr 2026 (NeurIPS 2025 Workshop: AI for Science; arXiv comments: "Accepted and presented at NeurIPS 2025 AI for Science Workshop"; no journal reference). DOI 10.48550/arXiv.2505.23824. Printed page numbers equal PDF positions, pp. 1 to 11 (body pp. 1 to 8, references pp. 8 to 10, appendices pp. 10 to 11); page 1 prints no page number. PDF: `source/pdfs/Zhang and Abernethy - 2026 - Reviewing Scientific Papers for Critical Problems With Reasoning LLMs.pdf`.
>
> Earlier version: arXiv v1 (28 May 2025; `source/pdfs/Archive - Zhang and Abernethy - 2025.pdf`), superseded 2026-11-24. An arXiv v2 (7 Jul 2025) exists and was not compared.

- PDF check 2026-11-24: Findings and TL;DR numbers moved from v1 to v3: o3 HR@5 64.9%/71.0% -> 48.2%/50.6%; o4-mini 59.6%/61.6% -> 38.0%/38.8%; Claude 3.7 Sonnet 16.3%/33.1% -> 11.0%/24.1%; o3 cost $0.321/$0.383 -> $0.064/$0.077 per paper (v3 Table 2, p. 5); single-judge o3 HR@5 72.7%/75.5% (Gemini judge) and 75.5%/80.4% (o3 judge) -> 80.4%/79.2% and 50.2%/51.4% (v3 Table 3, p. 6).
- PDF check 2026-11-24: "tripled the average problems submitted (1.6 to 3.4)" -> "raised ... 1.6 to 3.4" (a 2.1-fold rise; v3 Table 2, p. 5).
- PDF check 2026-11-24: o4-mini cost-effectiveness claim and "specialized LaTeX training" reading dropped; v3 states "resistance to format change or a higher familiarity with LaTeX" (p. 4) and no longer calls o4-mini the most cost-effective choice.
- PDF check 2026-11-24: Quality appraisal quotes for non-significant-result spin and ablation replaced with v3 wording (p. 4 and p. 3); TRIPOD item 7e page "p.7" -> "pp.7-8".

## Abstract

### Question

Can today's top reasoning-style large language models (LLMs), chatbots that "think step-by-step" before answering, actually catch the kinds of critical errors that get a scientific paper withdrawn? The authors test five proprietary reasoning LLMs as zero-shot manuscript quality checkers (no fine-tuning, just a single fixed prompt) on 245 real arXiv papers that authors withdrew because of factual or methodological errors. They also compare two ways of feeding the paper into the model: as a PDF attachment versus as the raw LaTeX source code. See [[QUE - Can reasoning LLMs find critical errors in papers|QUE - Can reasoning LLMs identify critical errors and unsoundness problems in scientific papers?]].

### Methods

**Design.** The authors built a single cross-sectional benchmark in which five reasoning LLMs each reviewed the same 245 withdrawn arXiv papers under two ingestion conditions, with two separate LLMs serving as judges of whether the model's flagged problem matched the author's stated retraction reason.

**Tools.** The five "checker" models were Google's Gemini 2.5 Pro and Gemini 2.5 Flash (preview-04-17 and preview-05-06; Google's flagship reasoning models, "Flash" is the cheaper sibling), OpenAI's o3 and o4-mini (snapshot 2025-04-16; OpenAI's reasoning models, "mini" is the cheaper sibling), and Anthropic's Claude 3.7 Sonnet (snapshot 20250219, with extended thinking enabled). All ran via official APIs in Python. The two "judge" models were Gemini 2.5 Pro (preview-06-05 in v3, chosen "for its better performance on related benchmarks than preview-05-06") and o3 (Claude was disqualified as a judge because its "overly low hit rate under the PDF-based approach indicates that it might not qualify"). The dataset is WITHDRARXIV-CHECK, a curated subset of WITHDRARXIV (Rao et al. 2024), itself a corpus of papers withdrawn from arXiv with author-supplied retraction comments.

**Procedure.** The authors first built WITHDRARXIV-CHECK by filtering 6,018 candidate withdrawn papers down to 1,225 cases with clearly-specified, manuscript-detectable errors. They split this 80/20 into a 980-paper training set (set aside, not used) and a 245-paper test set. For each test paper, each checker LLM was prompted once with a fixed simplistic instruction asking for up to five critical problems, returned as JSON entries with fields Problem, Location, and Explanation. Each paper was given to the model two ways: as a PDF attachment, and as the raw LaTeX source pasted into the prompt. For papers without LaTeX source (12% of the test set), the LaTeX-row results re-used the model's PDF-row prediction. Each problem the checker submitted was then independently scored by the two judge LLMs, who saw the gold retraction comment and answered yes-or-no whether the checker had found the same problem. A paper counted as a "hit" only if both judges said yes, a stricter rule designed to resist the well-known LLM-judge inflation problem. The headline metric is Hit Rate at 5 (HR@5): the share of the 245 test papers on which the model scored at least one confirmed hit. New in v3, the same two judges also rated each submitted problem as a true problem or a false alarm against the paper PDF, giving an Average Precision (AP@5) for the PDF approach only. The authors also tracked cost per paper at standard June-2025 API pricing.

**Sample.** No human subjects. Papers flowed from 6,018 WITHDRARXIV critical-error candidates, through a Gemini 2.5 Flash filter (down to 2,190), then a five-rule manual exclusion pass (misclassified, duplicate-version, non-English, template-like, or not-detectable-from-manuscript), to a final WITHDRARXIV-CHECK corpus of 1,225 papers, randomly split into a 245-paper test set. Test composition skews heavily toward formal sciences: Math 52%, Physics 29%, Computer Science 15%, Other 4%. Median page count was 14 (range 2–136); 88% had LaTeX source available.


**At a glance.**

```mermaid
flowchart TD
    A["WITHDRARXIV<br/>(Rao et al. 2024)"] --> B["Critical-errors subset<br/>n=6,018"]
    B --> C["Gemini 2.5 Flash filter<br/>on de-identified comments"]
    C --> D["n=2,190"]
    D --> E["Manual exclusions<br/>(misclassified · duplicates ·<br/>non-English · template ·<br/>not-detectable from manuscript)"]
    E --> F["<b>WITHDRARXIV-CHECK<br/>n=1,225</b>"]
    F --> G["80/20 random split"]
    G --> H["Train n=980<br/>(set aside)"]
    G --> I["<b>Test n=245</b><br/>Math 52% / Physics 29% /<br/>CS 15% / Other 4%"]
    I --> J{"Ingestion approach"}
    J --> K["PDF attachment"]
    J --> L["LaTeX script in prompt"]
    K --> M["5 checker LLMs<br/>Gemini 2.5 Pro/Flash ·<br/>o3 · o4-mini ·<br/>Claude 3.7 Sonnet<br/>(k=5, n_c=1)"]
    L --> M
    M --> N["JSON list:<br/>{Problem, Location,<br/>Explanation}"]
    N --> O["2 LLM judges<br/>Gemini 2.5 Pro + o3<br/>(both must affirm, m=2)"]
    O --> P["<b>HR@5 + cost/paper</b>"]

    classDef data fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef step fill:#FFF8E1,stroke:#F57F17,color:#5D4037;
    classDef model fill:#F1F8E9,stroke:#2E7D32,color:#1B5E20;
    classDef result fill:#FCE4EC,stroke:#AD1457,color:#880E4F;
    class A,B,D,F,H,I data;
    class C,E,G,J,K,L,N step;
    class M,O model;
    class P result;
```
---

### Findings

- **OpenAI o3 was the best error catcher overall.** o3 hit on 48.2% of papers when fed PDFs and 50.6% when fed LaTeX (HR@5: share of test papers on which the model raised at least one judge-confirmed real error, out of 245), ahead of the next-best checker under PDF, Gemini 2.5 Pro, at 39.2%. Its single-judge HR@5 ran much higher with the Gemini 2.5 Pro judge (80.4% PDF, 79.2% LaTeX) and about level with the o3 judge (50.2%, 51.4%); the both-judges-must-agree fusion is what sets the headline number, which the authors read as "some resistance of our multi-judge approach to potential false positives". o3 also used markedly fewer thinking tokens than the Gemini family (3,152 vs. 14,228 for Gemini 2.5 Pro under PDF), so "more thinking" did not translate into "more hits". On the precision estimate new in v3 (AP@5, PDF only) o3 scored 29.5%, below Gemini 2.5 Pro (35.2%) and Claude 3.7 Sonnet (36.4%), though o3 produced the most submissions that both judges confirmed as true problems (350, vs. 293 for Gemini 2.5 Pro and 149 for Claude). [[EVD - o3 led reasoning LLMs with 48.2% hit rate on PDF and 50.6% on LaTeX|EVD - OpenAI o3 achieved the highest hit rate of 48.2% (PDF) and 50.6% (LaTeX) among all reasoning LLMs tested as scientific paper quality checkers]]

- **o4-mini's cost advantage over o3 is small in v3.** o4-mini reached 38.0% HR@5 on PDFs and 38.8% on LaTeX (10.2 and 11.8 percentage points behind o3), at $0.038 and $0.043 per paper against $0.064 and $0.077 for o3, so o3 costs about 1.7 to 1.8 times as much (v1 had put o3 at $0.321 and $0.383, about 8 times). Gemini 2.5 Flash matches o4-mini's PDF hit rate (38.4% vs. 38.0%) at $0.033 per paper, and v3 no longer calls o4-mini the most cost-effective choice. Both OpenAI models' hit rates "remained around the same or slightly increased" under LaTeX while the Gemini models' decreased, which the authors read as "resistance to format change or a higher familiarity with LaTeX". [[EVD - o4-mini reached 38.0% HR@5 at 0.038 USD per paper vs 0.064 USD for o3|EVD - o4-mini achieved 38.0% HR@5 as a scientific paper quality checker at a cost of $0.038 per paper versus o3 at $0.064 per paper]]

- **Claude 3.7 Sonnet collapsed on PDF inputs.** When given PDFs, Claude returned an empty problem list on 64.9% of test papers and reached only 11.0% HR@5. Switching to LaTeX more than doubled its hit rate to 24.1% and raised the average problems submitted from 1.6 to 3.4. Claude's PDF input-token usage was 9.3 times Gemini's and 2.6 times o3's; the authors say the vendor differences "reflect distinct PDF ingestion pipelines" but that it "remains unclear why Claude has an exceptionally high input token usage for PDF files", and suggest "potential obstacles in Claude's PDF ingestion pipeline or scientific understanding via PDF". The result was severe enough that the authors judged Claude might not qualify as a judge. [[EVD - Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 11.0%|EVD - Claude 3.7 Sonnet found no problem in 64.9% of test papers and achieved only 11.0% hit rate as a PDF-based scientific quality checker]]

### Claim supported

These findings support the claim that [[CLM - Reasoning LLMs substantially outperform non-reasoning LLMs at finding paper errors|CLM - Reasoning LLMs substantially outperform non-reasoning models at identifying critical scientific errors in papers and are viable as manuscript quality checkers]]. For someone considering deployment: o3 sets the current ceiling at roughly 1-in-2 papers caught (50.6% with LaTeX), o4-mini and the Gemini models catch about 35 to 39% at somewhat lower cost, and Claude's PDF input is currently a non-starter for this use case (11.0%). The authors frame the practical implication explicitly: these tools belong as a pre-screen feeding human reviewers, not as a replacement.

### Caveats

- **Only closed-source proprietary models were tested.** No open-source reasoning model (e.g., DeepSeek-R1, Qwen-QwQ, Llama-with-thinking variants) was evaluated, so we cannot tell whether o3's lead reflects reasoning-LLM capability in general or just one vendor's tooling. The Claude PDF collapse in particular may reflect the PDF pipeline rather than the model (the authors suggest "potential obstacles in Claude's PDF ingestion pipeline or scientific understanding via PDF"), and that cannot be tested without open-source comparators. [[CVT - Only closed-source reasoning LLMs were tested as checkers|CVT - Only closed-source reasoning LLMs were evaluated as scientific paper quality checkers excluding open-source alternatives]]

- **The corpus is dominated by math and physics.** Math (52%) and physics (29%) papers together make up over 80% of the test set, and the kinds of "critical errors" in those fields tend to be formal: wrong equations, broken proofs, sign errors. Errors in empirical sciences (biology, medicine, social science) often hinge on study design, statistical analysis, or data quality, which look structurally different. The headline hit rates may not transfer. [[CVT - Error detection dataset was mostly math and physics and may not generalize|CVT - The error detection dataset was rich in math and physics papers and may not generalize to other scientific domains]]

## Quality appraisal

> [!info] Risk-of-bias and validity assessment, synthesized from this paper's discourse-graph nodes and grounded in the same paper this page's top trust-signal chips summarize. Covers *methodological quality*; the TRIPOD-LLM table below covers *reporting compliance* instead.
> <dl class="callout-legend">
> <dt><span class="status-icon status-icon-low-risk">○</span> Low risk</dt><dd>No meaningful threat to this domain identified</dd>
> <dt><span class="status-icon status-icon-some-risk">◐</span> Some risk</dt><dd>A real but non-fatal limitation</dd>
> <dt><span class="status-icon status-icon-high-risk">●</span> High risk</dt><dd>A significant, unaddressed threat to validity</dd>
> </dl>

| Domain | Rating | Quote |
| --- | :---: | --- |
| **Construct validity**: does the metric actually measure the construct? | 🟡 | *"Please note that there is no gold standard for precision evaluation in our experiment, and that a case in which an LLM checker found no problem is skipped because a precision value cannot be calculated."* `§2.3, p.4` |
| **Internal validity**: could the comparison be biased? | 🟡 | *"We initially planned for m = 3 with Claude 3.7 Sonnet as the last judge, but its overly low hit rate under the PDF-based approach indicates that it might not qualify for serving as a judge in this task."* `§2.4, p.4` |
| **External validity**: do findings generalize? | 🔴 | *"our results based on a dataset rich in math and physics papers published in the past may not generalize well to papers in other scientific domains or future papers."* `§5 Limitation, p.7` |
| **Statistical conclusion validity**: appropriate uncertainty + comparisons? | 🟡 | *"our settings that each LLM checker was tested only once per paper and each LLM judge graded each submission only once. Nevertheless, a higher score under parallel evaluation still reasonably indicates better performance of an LLM checker."* `§5 Limitation, p.7` |
| **Reproducibility**: code, data, determinism? | 🟡 | *"Our WITHDRARXIV-CHECK dataset, experiment code, and model outputs (including thinking outputs if available) are available on Github."* `Data Availability, p.8` |
| **Data leakage**: could models have seen this data pretraining? | 🔴 | *"One potential concern over the validity of our evaluation results is that LLMs might have seen the test papers (or other versions of them) in their training data. ... Nevertheless, it would be beneficial to evaluate LLMs on papers that are unlikely to be included in the training phase, such as those published after the knowledge cutoff dates of LLMs."* `§4 Discussion, p.6–7` |
| **Baseline adequacy**: is there a meaningful floor to beat? | 🔴 | Not reported, no trivial or naive comparator (e.g., a keyword-matching or random-guess checker) is evaluated alongside the five reasoning LLMs |
| **Train/dev/test hygiene**: are data splits kept separate? | 🟡 | *"We randomly sampled 20% of the dataset (245 cases) as the test set for evaluation experiments. The remaining 80% (980 cases) of the dataset was set aside for training and validation, although these latter two steps were not considered in this work whose main objective was to establish baseline approaches and evaluation methods."* `§2.1, p.2` |
| **Multiple-comparisons correction**: controlled for repeated testing? | 🔴 | Not reported, no correction is stated across the 5 checkers × 2 ingestion approaches × 2 judge configurations in Tables 2–3 |
| **Human-baseline comparability**: is there a human reference point? | 🔴 | Not addressed, no live human-expert reviewer was run alongside the LLM checkers; gold labels are the authors' own retraction comments |
| **Confidence Intervals**: are point estimates accompanied by an interval? | 🔴 | Not reported: hit-rate figures (HR@5, e.g. 48.2%, 11.0%) are given as point estimates with no interval |
| **Chance-Corrected Metrics**: does agreement/accuracy correct for chance? | 🔴 | Not reported: only hit rate / mean hit rate at k are reported `Table 2-3`; no chance-corrected statistic appears anywhere |
| **Non-Significant Result Spin**: are null or negative findings framed plainly? | 🟢 | *"Claude 3.7 Sonnet found no problem in 64.9% of test papers, leading to a low hit rate compared to other reasoning models."* `§3, p.4`, and the authors explicitly disqualified Claude from the judge pool as a result, no attempt to soften or omit this negative result |
| **Statistic Accuracy**: do the paper's own reported numbers check out? | 🟢 | Reported hit-rate figures decrease monotonically as expected between the single-judge and stricter dual-judge-fusion conditions (e.g. o3's single-judge HR@5 of 50.2–80.4% in Table 3, p.6, falling to a lower dual-judge headline of 48.2–50.6% in Table 2, p.5), with no internal inconsistency |
| **Ablation Experiment(s)**: does the paper isolate a component's contribution? | 🟢 | *"we evaluated the PDF-based approach and the LaTeX-based approach in this work"*, with Table 2 reporting hit rates for both input-format conditions per model, *"After switching to LaTeX, the hit rates of Gemini models decreased, likely due to the information loss. In contrast, the hit rates of OpenAI o-series models remained around the same or slightly increased, suggesting resistance to format change or a higher familiarity with LaTeX obtained in its training processes."* `§3, p.4` (the ablation design is in `§2.2, p.3`) |
| **AI writing check**: does the paper's own prose read as AI-generated? | 🟢 | Independent recheck run because this source's Dataset check and Code check both returned "No repository claimed". Pangram v3.3.2 AI-text detector: *"We believe that this document is fully human-written"* (0% AI-generated, 0% AI-assisted). [Dashboard](https://www.pangram.com/history/153df094-7481-4582-901a-075c6a6714f7) |
| **Code Quality**: does the released code follow FAIR-software practices? | 🟡 | `howfairis` (fair-software.eu 5-criteria checklist) against https://github.com/tianmai-zhang/WithdrarXiv-Check: **2/5**: open repository + license: no package-registry listing, citation metadata, or quality-checklist badge. |
| **Data Quality**: is the released dataset FAIR? | 🔴 | FAIR-Checker (12 semantic-web metrics, 0-2 each) against https://github.com/tianmai-zhang/WithdrarXiv-Check: **6/24**, includes a +2 top-up for having a real license file, since FAIR-Checker can't see repo content on GitHub pages. |

**Bottom line.** The paper makes a clean, well-instrumented case that today's reasoning LLMs (especially OpenAI's o3 and o4-mini) can flag the *specific* author-stated retraction error on about half of withdrawn math and physics papers (o3: 48.2% to 50.6%), with o4-mini and the Gemini models at about 35 to 39% and Claude 3.7 Sonnet at 11.0% on PDFs. The result that holds up cleanly is o3's lead on hit rate. The result that does *not* hold up cleanly is "reasoning LLMs are viable manuscript quality checkers" in general: the test bed is overwhelmingly formal-sciences, precision is only roughly estimated by LLM judges with no gold standard (new in v3, PDF only), no open-source models are tested, and the Claude PDF result may be more a story about PDF ingestion than about reasoning capability. Before deployment in a real journal-screening workflow, future work needs precision/recall on a domain-balanced corpus, open-source comparators, and a head-to-head against expert human reviewers on the same papers.

> [!tip] **Applicable external appraisal frameworks beyond TRIPOD-LLM** (already covered by the table below): **HELM** (Liang et al. 2022) for holistic LLM-evaluation principles · **Datasheets for Datasets** (Gebru et al. 2021) for the evaluation corpus · **Model Cards** (Mitchell et al. 2019) for the LLMs being evaluated

---

## TRIPOD-LLM reporting

> [!info] Reporting compliance for this paper, mapped to the TRIPOD-LLM checklist (Title/Abstract/Introduction items 1–4, Methods items 5a–15, Results items 16a–18). TRIPOD-LLM is a clinical-ML guideline being applied here to a non-clinical AI-research benchmark, where an item's own wording says "healthcare context" or "care pathway," it's read as "research-evaluation context" / "research workflow" instead. Item 17 (Performance) is reported per-EVD; see each EVD's `## Other Notes`.
> <div class="callout-legend-flat">
> <span><span class="status-icon status-icon-good">●</span>Fully reported</span>
> <span><span class="status-icon status-icon-partial">◐</span>Partial / unclear</span>
> <span><span class="status-icon status-icon-bad">○</span>Not reported</span>
> <span><span class="status-icon status-icon-na">–</span>Not applicable</span>
> </div>

| # | Item | ✓ | Quote |
| --- | --- | :---: | --- |
| **1** | Title | ✅ | *"Reviewing Scientific Papers for Critical Problems With Reasoning LLMs: Baseline Approaches and Automatic Evaluation"* `Title, p.1` |
| **2** | Abstract | ➖ | Assessed separately under TRIPOD-LLM's own Abstract extension, not scored here |
| **3a** | Background: context + rationale | ✅ | *"Recent advancements in the domain intelligence of large language models (LLMs) have fostered interest in utilizing them to aid the peer review process of scientific publication, especially in consideration of the peer review crisis due to the skyrocketing number of paper submissions in recent years"* `§1, p.1` |
| **3b** | Background: target population | ⚠️ | *"In this work, we consider the identification of critical errors and unsoundness problems that may invalidate the conclusions of a paper, a key sub-task in peer review, as the main goal of an LLM manuscript checker."* `§1, p.2` |
| **4** | Objectives | ✅ | *"we propose adopting LLMs as manuscript quality checkers. We introduce several baseline approaches and an extendable automatic evaluation framework using top reasoning LLMs as judges to tackle the difficulty of recruiting domain experts for manual evaluation."* `Abstract, p.1` |
| **5a** | Data sources | ✅ | *"We utilized WITHDRARXIV [Rao et al., 2024], a large-scale dataset of papers withdrawn from arXiv by September 2024, along with associated retraction comments from authors and well-defined retraction categories."* `§2.1, p.2` |
| **5b** | Data points + distribution | ✅ | *"Sample size — Train 980 / Test 245 · Main subject: Math 492 (50%)/128 (52%), Physics 256 (26%)/70 (29%), Computer Science 196 (20%)/37 (15%), Others 36 (4%)/10 (4%)"* `Table 1, p.3` |
| **5c** | Date range of data | ⚠️ | *"a large-scale dataset of papers withdrawn from arXiv by September 2024"* `§2.1, p.2`, exact earliest withdrawal date and dataset-construction date not stated, only decade-scale buckets in Table 1 |
| **5d** | Pre-processing / quality checks | ✅ | *"de-identified retraction comments were first provided to Gemini 2.5 Flash (preview-04-17) to determine whether each retraction comment clearly specified the error... We also corrected mistakenly redacted theorem names in the retraction comments."* `§2.1, p.2` |
| **5e** | Missing / imbalanced data | ⚠️ | *"For the small proportion of papers without available LaTeX scripts (Table 1), we resorted to utilizing the problems identified by the same model through the PDF-based approach."* `§2.2, p.3` |
| **6a** | LLM name + version | ✅ | *"The following reasoning LLMs were tested as paper quality checkers: Google's Gemini 2.5 Pro (preview-05-06) and Gemini 2.5 Flash (preview-04-17); OpenAI's o3 (2025-04-16) and o4-mini (2025-04-16); Anthropic's Claude 3.7 Sonnet (20250219)."* `§2.4, p.4` |
| **6b** | Development process | ➖ | Not applicable: no model development, fine-tuning, or training performed; off-the-shelf API models used as-is |
| **6c** | Inference settings / prompting | ✅ | *"Gemini 2.5 Pro and Gemini 2.5 Flash: thinking budget: default (automatic) ... tools: [] temperature: 0 seed: 42 ... o3 and o4-mini: reasoning effort: defaults to \"medium\" ... temperature and seed: not supported ... Claude 3.7 Sonnet: max tokens: 16,000 ... temperature: 1 (required for thinking) seed: not supported"* `Appendix B, p.11` |
| **6d** | Output | ✅ | *"give me up to {k} most critical problems as a JSON object using the following schema: Entry = {\"Problem\": str, \"Location\": str, \"Explanation\": str}, Return: list[Entry]."* `Appendix A, p.10` |
| **6e** | Classification thresholds | ➖ | Not applicable: outputs are free-text JSON entries with no probability thresholding; hit / true-positive decisions are majority-vote judge labels |
| **7a** | Quality metrics | ✅ | *"LLM checkers were primarily evaluated by their hit rates on test papers... we report this metric as the Hit Rate at k (HR@k)."* `§2.3, p.3` |
| **7b** | Relevance to downstream use | ✅ | *"journal publishers and conference organizers may consider incorporating LLM quality checkers into initial assessments of manuscripts [Bauchner and Rivara, 2024], thereby reducing the burden on reviewers."* `§4, p.7` |
| **7c** | Outcome definition | ✅ | *"If an LLM checker receives a majority of (or all, for a stricter evaluation) affirmative votes from LLM judges, it is deemed to have made a hit on a paper."* `§2.3, p.3` |
| **7d** | Subjective interpretation | ⚠️ | *"Considering the daunting cost of recruiting domain experts to manually evaluate LLM-identified scientific errors, we propose an automatic evaluation pipeline to streamline the process."* `§2.3, p.3`, LLM judges substitute for human expert interpretation; no human spot-check of judge accuracy reported |
| **7e** | Comparison | ✅ | *"A concurrent work on arXiv by Son et al. [2025] also utilizes the WITHDRARXIV dataset for automatic error detection in scientific papers... The two efforts are complementary, and both report the leading performance of o3."* `§4, pp.7–8` |
| **8a** | Annotation guidelines | ➖ | Not applicable: no human annotation in this study; gold labels are author-supplied retraction comments, and the LLM-judge prompt (Appendix A) defines the matching criterion |
| **8b** | Annotators + IAA | ⚠️ | Not applicable: no human annotators; inter-judge agreement between Gemini 2.5 Pro and o3 not reported as a κ / agreement statistic |
| **8c** | Annotator background | ➖ | Not applicable |
| **9a** | Prompt design | ✅ | *"In our experiments, both approaches utilized the same simplistic, general task instruction (Appendix A)... The prompt was not customized for our dataset that is rich in math and physics papers."* `§2.2, p.3` |
| **9b** | Prompt-development data | ❌ | Not reported |
| **10** | Summarization | ➖ | Not applicable: no summarization endpoint evaluated |
| **11** | Instruction tuning / alignment | ➖ | Not applicable: no model training, fine-tuning, or alignment performed |
| **12** | Compute | ⚠️ | *"we recorded token usage to inform future work that seeks to apply LLMs at a larger scale. Average costs of reviewing a paper under each pipeline-LLM combination were estimated based on the standard API pricing of the LLM vendors in June 2025."* `§3, p.4`, no GPU / wall-clock compute reported |
| **13** | Ethical approval | ➖ | *"In this work, we circumvent this challenge by utilizing publicly available arXiv papers."* `§4, p.7`, no IRB/ethics-committee statement present (not human-subjects research) |
| **14a** | Funding | ✅ | *"This work is supported by the Ira Kalet and Fred Wolf Endowment Fund from the Department of Biomedical Informatics and Medical Education, University of Washington."* `Acknowledgments and Disclosure of Funding, p.8` |
| **14b** | Conflicts of interest | ✅ | *"The authors declare no competing interest."* `Acknowledgments and Disclosure of Funding, p.8` |
| **14c** | Protocol | ❌ | Not reported |
| **14d** | Registration | ➖ | Not applicable: not a registered clinical study |
| **14e** | Data availability | ✅ | *"Our WITHDRARXIV-CHECK dataset, experiment code, and model outputs (including thinking outputs if available) are available on Github."* `Data Availability, p.8` |
| **14f** | Code availability | ✅ | *"experiment code, and model outputs (including thinking outputs if available) are available on Github."* `Data Availability, p.8` |
| **15** | Patient/public involvement | ➖ | Not applicable |
| **16a** | Flow of data | ✅ | *"This step resulted in a subset of 2,190 cases. Our manual review further excluded cases that (1) were incorrectly identified during LLM screening... The final dataset, named WITHDRARXIV-CHECK, contains 1,225 cases in total."* `§2.1, p.2` |
| **16b** | Characteristics | ✅ | *"Dataset characteristics are provided in Table 1."* `§2.1, p.2` (Table 1 itself is on p.3) |
| **16c** | Distribution comparison | ⚠️ | *"2007-2012 155 (16%) 32 (13%) · 2013-2018 487 (50%) 114 (47%) · 2019-2024 338 (34%) 99 (40%)"* `Table 1, p.3`, train/test time-span distributions shown side by side but no formal balance test reported |
| **16d** | N per analysis | ✅ | *"we took k = 5, nc = nj = 1, and m = 2, i.e., each LLM checker was tested once with each paper and was allowed to report up to 5 problems, and 2 LLMs served as judges"* `§2.4, p.4` |
| **17** | Performance | `per-EVD` | Reported per-EVD. See each EVD's `## Other Notes`. |
| **18** | LLM updating | ➖ | Not applicable: no model updating reported |

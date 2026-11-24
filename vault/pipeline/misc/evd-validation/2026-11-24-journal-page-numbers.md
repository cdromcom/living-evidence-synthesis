---
tags: [misc/evd-validation]
---
# Journal page numbers in EVD citations (2026-11-24)

Rule: citations use the journal printed page number, not the PDF position. Page located by searching each quoted text in the PDF with PyMuPDF (hyphenation, quote marks, spacing and punctuation normalised). Screenshot filenames were not renamed. A second pass re-checked all 27 applied rows against the PDFs (quote on the cited printed page, and that page number printed on the page); all 27 verified and none was reverted. Sridharan 2025 (p. 131 changed to 126): the quote is the abstract, found only on the first PDF page (printed 126), although its screenshot filename says p4, so JP may want to re-crop or re-check that screenshot.

Counts: citations checked 322; changes applied 27; already correct 160; left for review 89 (quote not found exactly on one page, or odd citation form); no printed numbers (PDF position only) 46.

Notes: Zhang & Abernethy (2025, Archive v1) pages are intentionally on v1 numbers and were left out; their rows are listed for information only (action = left). Huntington-Klein & Murray uses the Archive 2024 PDF (the 2026 version matched only 2 of the 8 quotes). Thelwall uses the 2025 journal PDF (printed pages 7-25); Shahid, Xu, Zhou, Wu, Sridharan use the proceedings/journal PDFs, so their printed numbers are large (for example Xu 20652+). Confidence: high = quote found whole on exactly one page; medium = start or end of the quote matches one page only (never applied); low = not found, split across pages or no quote.

## Per-paper mapping

| Paper | PDF file | PDF pages | How printed number found | Printed = PDF position + | Header/footer coverage |
|---|---|---|---|---|---|
| akyon 2024 | Akyon et al. - 2024 - Evaluating the capabilities of generative AI tools in understanding medical papers Qualitative stud.pdf | 30 | PDF position only | n/a (PDF position only) | - |
| alharbi 2024 | Alharbi and Asiri - 2024 - Automated Assessment of Reporting Completeness in Orthodontic Research Using LLMs An Observational.pdf | 10 | header/footer numbers (equal to PDF position) | 0 | 10/10 |
| bougie 2024 | Bougie et al. - 2024 - Generative Adversarial Reviews.pdf | 25 | header/footer numbers (equal to PDF position) | 0 | 25/25 |
| d'arcy 2024 | D'Arcy et al. - 2024 - MARG Multi-Agent Review Generation for Scientific Papers.pdf | 52 | PDF position only | n/a (PDF position only) | - |
| hasan 2024 | Hasan et al_2024_Integrating large language models in systematic reviews.pdf | 5 | header/footer numbers (equal to PDF position) | 0 | 5/5 |
| huntington-klein 2024 | Archive - superseded versions/Archive - Huntington-Klein and Murray - 2024.pdf | 27 | PDF position only | n/a (PDF position only) | - |
| idahl 2025 | Idahl and Ahmadi - 2025 - OpenReviewer A Specialized LLM.pdf | 13 | header/footer numbers (equal to PDF position) | 0 | 13/13 |
| leucuta 2025 | Leucuta et al. 2025 - Risk of Bias Assessment of Diagnositic Accuracy Studies.pdf | 20 | header/footer numbers (equal to PDF position) | 0 | 20/20 |
| liang 2024 | Liang et al. - 2024 - Can Large Language Models Provide Useful Feedback on Research Papers A Large-Scale Empirical Analys.pdf | 39 | header/footer numbers (equal to PDF position) | 0 | 38/39 |
| liu 2023 | Liu and Shah - 2023 - ReviewerGPT An Exploratory Study on Using Large Language Models for Paper Reviewing.pdf | 60 | header/footer numbers (equal to PDF position) | 0 | 60/60 |
| lou 2025 | Lou et al. - 2025 - AAAR-1.0 Assessing AI's Potential to Assist Resea.pdf | 25 | header/footer numbers (equal to PDF position) | 0 | 25/25 |
| roberts 2023 | Roberts et al. 2023 - Comparative study of ChatGPT and human evaluators.pdf | 5 | header/footer numbers (equal to PDF position) | 0 | 5/5 |
| sarol 2024 | Sarol et al. - 2024 - Assessing citation integrity.pdf | 9 | header/footer numbers (equal to PDF position) | 0 | 8/9 |
| shahid 2025 | Shahid et al. - 2025 - Literature-Grounded Novelty Assessment of Scientific Ideas.pdf | 18 | PDF page labels | 95 | 18/18 |
| son 2025 | Son et al. - 2025 - When AI Co-Scientists Fail SPOT-a Benchmark for Automated Verification of Scientific Research.pdf | 40 | header/footer numbers (equal to PDF position) | 0 | 39/40 |
| sridharan 2024 | Sridharan and Sivaramakrishnan - 2024 - Assessing the Decision-Making Capabilities of AI.pdf | 9 | PDF page labels | 82 | 9/9 |
| sridharan 2025 | Sridharan and Sivaramakrishnan - 2024 - Leveraging artificial intelligence.pdf | 9 | PDF page labels | 125 | 9/9 |
| srinivasan 2025 | Srinivasan et al. - 2025 - Evaluating the reporting quality of 21,041 randomized controlled trial articles.pdf | 18 | header/footer numbers (equal to PDF position) | 0 | 12/18 |
| thelwall 2024 | Thelwall - 2025 - Evaluating research quality with Large Language Models An analysis of ChatGPT's effectiveness with.pdf | 19 | PDF page labels | 6 | 19/19 |
| tyser 2024 | Tyser et al. - 2024 - AI-Driven Review Systems Evaluating LLMs in Scalable and Bias-Aware Academic Reviews.pdf | 42 | PDF position only | n/a (PDF position only) | - |
| woelfle 2024 | Woelfle et al. - 2024 - Benchmarking Human–AI collaboration for common evidence appraisal tools.pdf | 11 | header/footer numbers (equal to PDF position) | 0 | 10/11 |
| wrightson 2025 | Wrightson et al. - 2025 - GPT for RCTs Using AI to determine adherence to clinical trial reporting guidelines.pdf | 7 | header/footer numbers (equal to PDF position) | 0 | 7/7 |
| wu 2024 | Wu et al. - 2024 - Automated novelty evaluation.pdf | 18 | header/footer numbers | 1451 | 18/18 |
| xu 2025 | Xu et al. - 2025 - Can LLMs Identify Critical Limitations within Scientific Research A Systematic Evaluation on AI Res.pdf | 55 | PDF page labels | 20651 | 55/55 |
| zhang 2024 | Zhang and Abernethy - 2024 - Detecting Reference Errors in Scientific Literature with Large Language Models.pdf | 8 | PDF position only | n/a (PDF position only) | - |
| zhang 2025 | Archive - superseded versions/Archive - Zhang and Abernethy - 2025.pdf | 8 | PDF position only | n/a (PDF position only) | - |
| zhou 2024 | Zhou - Is LLM a Reliable Reviewer A Comprehensive Evalua.pdf | 12 | header/footer numbers | 9339 | 12/12 |

## Citations

| EVD page | Quote start | Current page | Screenshot page | PDF page found | Printed page found | Proposed citation | Confidence | Action | Verified against PDF |
|---|---|---|---|---|---|---|---|---|---|
| 39.18% of 3063 biomedical citations had accuracy errors | A total of 3063 citation instances corresponding 3 | 5 | 5 | 5 | 5 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| 39.18% of 3063 biomedical citations had accuracy errors | Our citation accuracy classification is based on a | 3 | 3 | 3 | 3 | - | high | already correct | - |
| 39.18% of 3063 biomedical citations had accuracy errors | In the first annotation phase, all 5 annotators an | 3 | 3 | 3 | 3 | - | high | already correct | - |
| 39.18% of 3063 biomedical citations had accuracy errors | We collected 100 highly-cited research articles av | 2 | 2 | 2 | 2 | - | high | already correct | - |
| 57.4% of 308 researchers found GPT-4 feedback helpful | more than half (57.4%) of the users found GPT-4 ge | 1, Abstract | 1 | 1 | 1 | - | high | left for JP: non-simple citation form | - |
| 57.4% of 308 researchers found GPT-4 feedback helpful | Participants were surveyed about the extent to whi | 5 | 5 | 5 | 5 | - | high | already correct | - |
| 57.4% of 308 researchers found GPT-4 feedback helpful | The survey takes around 15-20 minutes and users wi | 11 | 11 | 11 | 11 | - | high | already correct | - |
| 57.4% of 308 researchers found GPT-4 feedback helpful | Through recruitment over institute mailing lists,  | 3 | 3 | 3 | 3 | - | high | already correct | - |
| AI Scientist reached 0.47 accuracy on novelty test set | Our approach achieved over 10 times more agreement | 7 | 6 | 6 | 101 | (Shahid et al., 2025, p. 101) | high | APPLIED | verified 2026-11-24: quote on printed page 101 (PDF page 6), number printed on that page, both copies edited |
| AI Scientist reached 0.47 accuracy on novelty test set | > AI Scientist results from Table 1: Accuracy=0.47 | 7 | - | - | - | - | low | left for JP: no quote | - |
| AI Scientist reached 0.47 accuracy on novelty test set | In addition to these baselines, we also compare ou | 5 | 5 | - | - | - | low | left for JP: not found | - |
| AI Scientist reached 0.47 accuracy on novelty test set | It is important to note that AI Scientist defaults | 7 | 6 | 6 | 101 | (Shahid et al., 2025, p. 101) | high | APPLIED | verified 2026-11-24: quote on printed page 101 (PDF page 6), number printed on that page, both copies edited |
| AI Scientist reached 0.47 accuracy on novelty test set | we standardize the most relevant papers to ensure  | 6 | 6 | 6 | 101 | (Shahid et al., 2025, p. 101) | high | APPLIED | verified 2026-11-24: quote on printed page 101 (PDF page 6), number printed on that page, both copies edited |
| AI platforms drafted SOPs covering fundamental sections with variations | The SOP-related outputs from the AI platforms are  | 85 | 7 | 3 | 85 | - | high | already correct | - |
| AI platforms drafted SOPs covering fundamental sections with variations | In addition, we used specific prompts (Electronic  | 84 | 2 | 2 | 84 | - | high | already correct | - |
| AI platforms drafted SOPs covering fundamental sections with variations | Two authors independently assessed the outputs of  | 85 | 3 | 3 | 85 | - | high | already correct | - |
| AI platforms drafted SOPs covering fundamental sections with variations | The following three AI platforms were used in this | 84 | 2 | 2 | 84 | - | high | already correct | - |
| All AI platforms missed post-trial herbal medicine access | Significantly, all platforms fell short in explain | 85 | 6 | 3 | 85 | - | high | already correct | - |
| All AI platforms missed post-trial herbal medicine access | An observational study was conducted using three A | 83 | 1 | 1 | 83 | - | high | already correct | - |
| All AI platforms missed post-trial herbal medicine access | Significantly, all platforms fell short in explain | 85 | 3 | 3 | 85 | - | high | already correct | - |
| All AI platforms missed post-trial herbal medicine access | The AI platforms were prompted with ten case studi | 84 | 2 | 2 | 84 | - | high | already correct | - |
| All four LLMs gave similar answers to all 7 IRB cases | All four LLMs were able to provide answers to the  | 127 | 4 | - | - | - | low | left for JP: not found | - |
| All four LLMs gave similar answers to all 7 IRB cases | The present study was conducted as an observationa | 126 | 1 | 1 | 126 | - | high | already correct | - |
| All four LLMs gave similar answers to all 7 IRB cases | We compared the responses of the LLMs with a singl | 127 | 2 | 2 | 127 | - | high | already correct | - |
| All four LLMs gave similar answers to all 7 IRB cases | Four AI platforms were evaluated as follows: 1. Go | 127 | 2 | 2 | 127 | - | high | already correct | - |
| All four LLMs included core ICD elements in all 7 cases | Each of the LLMs included all of the fundamental e | 127 | 7 | - | - | - | low | left for JP: not found | - |
| All four LLMs included core ICD elements in all 7 cases | A separate query was posed to the LLMs for conceiv | 127 | 2 | 2 | 127 | - | high | already correct | - |
| All four LLMs included core ICD elements in all 7 cases | We compared the responses of the LLMs with a singl | 127 | 2 | 2 | 127 | - | high | already correct | - |
| All four LLMs included core ICD elements in all 7 cases | Four AI platforms were evaluated as follows: 1. Go | 127 | 2 | 2 | 127 | - | high | already correct | - |
| Annotator agreement on citation labels was only kappa 0.18-0.31 | Agreement was lower on evidence sentence and accur | 5 | 5 | 5 | 5 | - | high | already correct | - |
| Annotator agreement on citation labels was only kappa 0.18-0.31 | We calculated pairwise inter-annotator agreement f | 4 | 3 | - | - | - | low | left for JP: not found | - |
| Annotator agreement on citation labels was only kappa 0.18-0.31 | Cohen's kappa (κ) was used for all tasks, and the  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| Annotator agreement on citation labels was only kappa 0.18-0.31 | five annotators were involved in the annotation pr | 3 | 3 | 3 | 3 | - | high | already correct | - |
| CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology | Urology/nephrology had the highest proportion of i | 6 | 6 | 6 | 6 | - | high | already correct | - |
| CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology | We applied our best-performing model to assess CON | 4 | 4 | 4 | 4 | - | high | already correct | - |
| CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology | We applied our most efficient and best performing  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| CONSORT compliance ranged from 35.16% in pharmacology to 63.35% in urology | For large-scale analysis, we identified 53,137 ope | 3 | 3 | 3 | 3 | - | high | already correct | - |
| CONSORT compliance rose from 27.3% to 56.1% over decades | The mean compliance rate increased from 27.3% (95% | 6 | 6 | 6 | 6 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| CONSORT compliance rose from 27.3% to 56.1% over decades | Statistical significance was evaluated using chi-s | 5 | 5 | 5 | 5 | - | high | already correct | - |
| CONSORT compliance rose from 27.3% to 56.1% over decades | We observed substantial improvement in CONSORT rep | 6 | 6 | 6 | 6 | - | high | already correct | - |
| CONSORT compliance rose from 27.3% to 56.1% over decades | For large-scale analysis, we identified 53,137 ope | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT and humans differed by 4.92% on CONSORT-A compliance | Bland-Altman analysis revealed a mean difference o | 3 | 3 | - | - | - | low | left for JP: not found | - |
| ChatGPT and humans differed by 4.92% on CONSORT-A compliance | We compared ChatGPT's scoring of implant dentistry | 1 | 1 | 1 | 1 | - | high | already correct | - |
| ChatGPT and humans differed by 4.92% on CONSORT-A compliance | Bland-Altman analysis was used to evaluate the ove | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT and humans differed by 4.92% on CONSORT-A compliance | In this study, we used a previously published pape | 1, 3 | 1 | - | - | - | low | left for JP: fragments on different pages | - |
| ChatGPT diverged most on CONSORT-A conclusions by 0.764 | The mean difference in absolute OCS was highest fo | 4 | 4 | 4 | 4 | - | high | already correct | - |
| ChatGPT diverged most on CONSORT-A conclusions by 0.764 | Error analysis revealed small mean differences bet | 3–4 | 3 | - | - | - | low | left for JP: not found | - |
| ChatGPT diverged most on CONSORT-A conclusions by 0.764 | ChatGPT was used to score the same set of abstract | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT diverged most on CONSORT-A conclusions by 0.764 | In this study, we used a previously published pape | 1, 3 | 1 | 1 | 1 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria | The human and ChatGPT ratings achieved perfect agr | 6 | 6 | - | - | - | low | left for JP: not found | - |
| ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria | Similar to the RCT abstracts, two independent revi | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria | This study utilized the large language model GPT-3 | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT matched humans on 3 of 12 PRISMA items but not on eligibility criteria | Following the initial search, a random sample of 2 | 2 | 2 | 2 | 2 | - | high | already correct | - |
| ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization | The human raters and ChatGPT achieved perfect agre | 4 | 4 | 4 | 4 | - | high | already correct | - |
| ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization | This study evaluated the usability of Large Langua | 1 | 1 | 1 | 1 | - | high | already correct | - |
| ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization | To ensure the quality of the LLM output, we employ | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT matched humans on 6 of 17 CONSORT-A items but not on randomization | This cross-sectional observational study investiga | 2 | 2 | 2 | 2 | - | high | already correct | - |
| ChatGPT-human correlation weakest on CONSORT-A intervention and objective | The domains with a strong positive correlation wer | 4 | 4 | 4 | 4 | - | high | already correct | - |
| ChatGPT-human correlation weakest on CONSORT-A intervention and objective | the Pearson's correlation coefficient provides inf | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT-human correlation weakest on CONSORT-A intervention and objective | ChatGPT was used to score the same set of abstract | 3 | 3 | 3 | 3 | - | high | already correct | - |
| ChatGPT-human correlation weakest on CONSORT-A intervention and objective | The processes of selection and data extraction wer | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3% | When papers are provided as PDFs, Claude 3.7 Sonne | 3 | 4 | 3 | - | - | high | left (v1 numbers by design) | - |
| Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3% | When papers are provided as PDFs, Claude 3.7 Sonne | 3 | 3 | - | - | - | low | left (v1 numbers by design) | - |
| Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3% | We initially planned for $m=3$ with Claude 3.7 Son | 3 | 3 | 3 | - | - | high | left (v1 numbers by design) | - |
| Claude 3.7 Sonnet found no problem in 64.9% of papers and hit only 16.3% | Each LLM quality checker was tested $n_c$ ($c$ for | 2 | 3 | - | - | - | low | left (v1 numbers by design) | - |
| Claude Opus led AAAR ReviewCritique at 21.99% F1 | > Claude Opus best F1=21.99% on REVIEWCRITIQUE tas | 11 | - | - | - | - | low | left for JP: no quote | - |
| Claude Opus led AAAR ReviewCritique at 21.99% F1 | Closed-source models (GPT-4, Claude Opus, and Gemi | 11 | 10 | 10 | 10 | (Lou et al., 2025, p. 10) | high | APPLIED | verified 2026-11-24: quote on printed page 10 (PDF page 10), number printed on that page, both copies edited |
| Claude Opus led AAAR ReviewCritique at 21.99% F1 | For REVIEWCRITIQUE, we use F1 score as the classif | 6 | 6 | - | - | - | low | left for JP: not found | - |
| Claude Opus led AAAR ReviewCritique at 21.99% F1 | As individual review comments are split into multi | 10 | 10 | 10 | 10 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Claude Opus led AAAR ReviewCritique at 21.99% F1 | We reuse the REVIEWCRITIQUE dataset from our recen | 10 | 6 | 6 | 6 | (Lou et al., 2025, p. 6) | high | APPLIED | verified 2026-11-24: quote on printed page 6 (PDF page 6), number printed on that page, both copies edited |
| Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74% | Combined LLM ratings led to accuracies of 75%−88%  | 1 [Abstract] | 1 | - | - | - | low | left for JP: not found | - |
| Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74% | Combining multiple assessments from LLMs in a 'con | 3 | 3 | 3 | 3 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74% | All nine LLM assessments were combined using only  | 7 | 7 | 7 | 7 | - | high | already correct | - |
| Combined LLMs reached 75-88% PRISMA accuracy while deferring 4-74% | We selected datasets for which independent ratings | 2 | 2 | 2 | 2 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% | Table 2 shows that the complete system, which empl | 7 | 7 | 7 | 102 | (Shahid et al., 2025, p. 102) | high | APPLIED | verified 2026-11-24: quote on printed page 102 (PDF page 7), number printed on that page, both copies edited |
| Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% | > Complete system accuracy for 'not novel' predict | 7, Table 2 | - | - | - | - | low | left for JP: no quote | - |
| Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% | To assess the contribution of each component in ou | 6 | 6 | 6 | 101 | (Shahid et al., 2025, p. 101) | high | APPLIED | verified 2026-11-24: quote on printed page 101 (PDF page 6), number printed on that page, both copies edited |
| Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% | We use o3-mini for evaluating novelty (Step 3) and | 7 | 7 | 7 | 102 | (Shahid et al., 2025, p. 102) | high | APPLIED | verified 2026-11-24: quote on printed page 102 (PDF page 7), number printed on that page, both copies edited |
| Dropping RankGPT re-ranker cut accuracy 89.66% to 13.79% | ablation studies using 58 ideas (comprising 13 'no | 6 | 6 | 6 | 101 | (Shahid et al., 2025, p. 101) | high | APPLIED | verified 2026-11-24: quote on printed page 101 (PDF page 6), number printed on that page, both copies edited |
| Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions | Pooled across all questions and papers in the TEST | 5 | 5 | 5 | 5 | - | high | already correct | - |
| Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions | We also tested the open-source Llama 2 AI-LLM. We  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions | The Llama 2 model was fine-tuned using the correct | 4 | 4 | 4 | 4 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Fine-tuned Llama 2 improved from F1=0.63 to F1=0.84 on CONSORT questions | The limit on the size of data (the 'context window | 2 | 2 | 2 | 2 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Four LLMs averaged 72.95% correct on QUADAS-2 | Out of 110 signaling questions assessments (11 que | 9 | 9 | 9 | 9 | - | high | already correct | - |
| Four LLMs averaged 72.95% correct on QUADAS-2 | Four artificial intelligence generative large lang | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Four LLMs averaged 72.95% correct on QUADAS-2 | Each article was uploaded as a PDF file, sourced f | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Four LLMs averaged 72.95% correct on QUADAS-2 | Ten diagnostic accuracy articles were selected fro | 2 | 2 | 2 | 2 | - | high | already correct | - |
| Full text scored worse than abstracts for 3 ChatGPT models | The optimal input for ChatGPT 3.5-turbo seems to b | 7 | 7 | 8 | 14 | (Thelwall, 2024, p. 14) | high | APPLIED | verified 2026-11-24: quote on printed page 14 (PDF page 8), number printed on that page, both copies edited |
| Full text scored worse than abstracts for 3 ChatGPT models | This article assesses which ChatGPT inputs (full t | 1 | 1 | 1 | 7 | (Thelwall, 2024, p. 7) | high | APPLIED | verified 2026-11-24: quote on printed page 7 (PDF page 1), number printed on that page, both copies edited |
| Full text scored worse than abstracts for 3 ChatGPT models | Several different datasets were generated to try d | 4 | 4 | 5 | 11 | (Thelwall, 2024, p. 11) | high | APPLIED | verified 2026-11-24: quote on printed page 11 (PDF page 5), number printed on that page, both copies edited |
| Full text scored worse than abstracts for 3 ChatGPT models | The raw data for this paper is a set of 51 informa | 3 | 3 | 4 | 10 | (Thelwall, 2024, p. 10) | high | APPLIED | verified 2026-11-24: quote on printed page 10 (PDF page 4), number printed on that page, both copies edited |
| GAR beat human reviewers on preference 0.684 vs 0.523 | GAR leads with a score of 0.684, outperforming the | 11 | 10 | 11 | 11 | - | high | already correct | - |
| GAR beat human reviewers on preference 0.684 vs 0.523 | Therefore, this experiment measures and ranks revi | 10 | 10 | 10 | 10 | - | high | already correct | - |
| GAR beat human reviewers on preference 0.684 vs 0.523 | For every paper, two reviewers were randomly assig | 10 | 10 | 10 | 10 | - | high | already correct | - |
| GAR beat human reviewers on preference 0.684 vs 0.523 | In order to assess the quality of reviews generate | 10 | 10 | 10 | 10 | - | high | already correct | - |
| GAR human-likeness 3.89-4.02 significantly beat all LLM baselines | As shown in Table 7, our method significantly outp | 14 | 15 | 15 | 15 | (Bougie & Watanabe, 2024, p. 15) | high | APPLIED | verified 2026-11-24: quote on printed page 15 (PDF page 15), number printed on that page, both copies edited |
| GAR human-likeness 3.89-4.02 significantly beat all LLM baselines | GAR: NeurIPS 3.89 ± 0.11\*, ICLR 22 4.02 ± 0.10\*, | 15, Table 7 | 15 | - | - | - | low | left for JP: not found | - |
| GAR human-likeness 3.89-4.02 significantly beat all LLM baselines | Specifically, we collect agent-generated reviews a | 14–15 | 14 | - | - | - | low | left for JP: not found | - |
| GAR human-likeness 3.89-4.02 significantly beat all LLM baselines | All agents are powered by the GPT-4o-mini version  | 9 | 9 | 9 | 9 | - | high | already correct | - |
| GAR human-likeness 3.89-4.02 significantly beat all LLM baselines | We primary conduct the experiments on the ICLR 202 | 9 | 9 | 9 | 9 | - | high | already correct | - |
| GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49 | Our method outperforms previous state-of-the-art m | 11 | 11 | 11 | 11 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49 | To evaluate the effectiveness of our LLM-powered r | 11 | 11 | 11 | 11 | - | high | already correct | - |
| GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49 | In GAR^>, we set the decision threshold at a score | 12 | 12 | 12 | 12 | - | high | already correct | - |
| GAR predicted ICLR acceptance at F1 0.66 significantly above human 0.49 | Each run on Llama-3.1 (8b) takes approximately 20  | 9 | 9 | 9 | 9 | - | high | already correct | - |
| GPT 3.5-turbo topped STROBE questions at 66.9% correct | The percentage of correct answers for each LLM is  | 16 | 18 | 13 | - | - | high | left for JP: no printed numbers | - |
| GPT 3.5-turbo topped STROBE questions at 66.9% correct | Using this benchmark pipeline, we compared the ans | 6 | 3 | 3 | - | - | high | left for JP: no printed numbers | - |
| GPT 3.5-turbo topped STROBE questions at 66.9% correct | The benchmark pipeline itself is designed to proce | 11 | 11 | 11 | - | - | high | left for JP: no printed numbers | - |
| GPT 3.5-turbo topped STROBE questions at 66.9% correct | Using this benchmark pipeline, we compared the ans | 12 | 12 | 12 | - | - | high | left for JP: no printed numbers | - |
| GPT 4-0613 was lowest on STROBE questions at 44.1% | The lowest correct answer percentage was provided  | 16 | 18 | 14 | - | - | high | left for JP: no printed numbers | - |
| GPT 4-0613 was lowest on STROBE questions at 44.1% | Using this benchmark pipeline, we compared the ans | 12 | 12 | 12 | - | - | high | left for JP: no printed numbers | - |
| GPT 4-0613 was lowest on STROBE questions at 44.1% | Each LLM was compared with another LLM that provid | 14 | 14 | 14 | - | - | high | left for JP: no printed numbers | - |
| GPT 4-0613 was lowest on STROBE questions at 44.1% | Of the 39 articles analyzed, 28 (71.8%) were publi | 14 | 14 | 14 | - | - | high | left for JP: no printed numbers | - |
| GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context | Unlike GPT-3.5 Turbo, GPT-4 Turbo and GPT-4o tend  | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context | Three LLMs in OpenAI's GPT family were evaluated i | 3 | 3 | 3 | - | - | high | left for JP: no printed numbers | - |
| GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context | When more information is provided, GPT-3.5 Turbo w | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| GPT-3.5 Turbo quotation accuracy peaked at 68.0% and fell to 54.0% with context | Statement-reference pairs in the dataset were coll | 7 | 7 | 7 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-3.5 predicted review aspect scores at r=0.651 | when predicting scores given the review, GPT-3.5 a | 9342 | 4 | 4 | 9343 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-3.5 predicted review aspect scores at r=0.651 | For the task of aspect score prediction, we use th | 9341 | 2 | 2 | 9341 | - | high | already correct | - |
| GPT-3.5 predicted review aspect scores at r=0.651 | We conduct experiments under two different setting | 9342 | 3 | 3 | 9342 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-3.5 predicted review aspect scores at r=0.651 | This subset contains 1.3k manually annotated aspec | 9341 | 2 | 2 | 9341 | - | high | already correct | - |
| GPT-4 RR-MCQ macro accuracy was 0.276 | the best micro accuracy 0.710 comes from the GPT-4 | 9346 | 7 | 7 | 9346 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 RR-MCQ macro accuracy was 0.276 | Our RR-MCQ dataset is targeted for a more specific | 9345 | 6 | 6 | 9345 | - | high | already correct | - |
| GPT-4 RR-MCQ macro accuracy was 0.276 | We test both GPT-3.5-turbo-0613 and GPT-4-0613 on  | 9346 | 7 | 7 | 9346 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 RR-MCQ macro accuracy was 0.276 | To construct the MCQ test dataset, we select 55 re | 9345 | 6 | 6 | 9345 | - | high | already correct | - |
| GPT-4 Turbo detected quotation errors at 70.0% accuracy | GPT-4 Turbo and GPT-4o performed much better than  | 3 | 4 | 3 | - | - | high | left for JP: no printed numbers | - |
| GPT-4 Turbo detected quotation errors at 70.0% accuracy | Three LLMs in OpenAI's GPT family were evaluated i | 3 | 3 | 3 | - | - | high | left for JP: no printed numbers | - |
| GPT-4 Turbo detected quotation errors at 70.0% accuracy | Local retrieval of excerpts from the main body of  | 3 | 3 | 3 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 Turbo detected quotation errors at 70.0% accuracy | Statement-reference pairs in the dataset were coll | 7 | 7 | 7 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 Turbo ranked first in human review preference | Rank 1: GPT-4 Turbo (April 9, 2024) Score: 0.558;  | 5, Table 1 | 5 | - | - | - | low | left for JP: not found | - |
| GPT-4 Turbo ranked first in human review preference | This work quantifies and ranks reviewers based on  | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| GPT-4 Turbo ranked first in human review preference | To evaluate the quality of the LLM-generated revie | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| GPT-4 Turbo ranked first in human review preference | We deploy a system called Papers with Reviews illu | 3 | 3 | 3 | - | - | high | left for JP: no printed numbers | - |
| GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions | Pooled across all questions and papers in the TEST | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions | For the GPT-4 analysis, we used the following hype | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions | Each reporting guideline item of each paper was as | 4 | 4 | 4 | 4 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 Turbo reached F1=0.89 on 9 CONSORT questions | We used a subsample of the dataset provided by Sch | 2 | 2 | 2 | 2 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57% | The GPT-4 Vision model accurately identified all f | 5 | 5 | - | - | - | low | left for JP: not found | - |
| GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57% | During the study, OpenAI made their GPT-4 Vision m | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57% | Ten of the papers contained a flow diagram which s | 4 | 4 | - | - | - | low | left for JP: not found | - |
| GPT-4 Vision read CONSORT flow diagrams at 100% but missing details at only 57% | The flow diagrams from a subset of the data (n=20) | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I | Raw agreement about the overall risk of bias acros | 1 | 3 | 1 | 1 | - | high | already correct | - |
| GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I | This study evaluates GPT-4 agreement with human re | 1 | 1 | 1 | 1 | - | high | already correct | - |
| GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I | We measured the agreement between Cochrane reviewe | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 agreed 61% with Cochrane reviewers on ROBINS-I | The initial search yielded 98 SRs, from which 36 p | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate | In-context learning outperforms MultiVerS models i | 6 | 6 | 6 | 6 | - | high | already correct | - |
| GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate | Generative large language models (LLMs) have been  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate | The prompt consists of a detailed task instruction | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 citation F1 0.80 for accurate but 0.09 for inaccurate | We evaluated two LLMs from OpenAI (GPT-3.5-turbo-0 | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans | LLM comments on the implications of research 7.27  | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans | Fig. 3 presents the relative frequency of each of  | 5 | 5 | - | - | - | low | left for JP: not found | - |
| GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans | We curated an annotation schema of 11 key aspects  | 10 | 10 | 10 | 10 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 commented on implications 7.27x more and novelty 10.69x less than humans | The second dataset comprises 6,505 comments from h | 3 | 3 | 3 | 3 | - | high | already correct | - |
| GPT-4 cost about 100x more than Mixtral-8x22B | Mixtral-8x22B was the most affordable model with a | 8 | 3 | 8 | 8 | - | high | already correct | - |
| GPT-4 cost about 100x more than Mixtral-8x22B | Mixtral-8x22B was the most affordable model with a | 8 | 8 | 8 | 8 | - | high | already correct | - |
| GPT-4 cost about 100x more than Mixtral-8x22B | API querying, extraction of ratings, fixing minor  | 5 | 5 | 5 | 5 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 cost about 100x more than Mixtral-8x22B | All application programming interface (API) querie | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 detected errors in 7 of 13 constructed papers | We find that the LLM (GPT-4) can detect the error  | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 detected errors in 7 of 13 constructed papers | we deliberately inserted an error, encompassing ma | 4 | 4 | 4 | 4 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 detected errors in 7 of 13 constructed papers | We queried the LLM for three responses per prompt  | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4 detected errors in 7 of 13 constructed papers | We constructed 13 short papers (detailed in Sectio | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 favored the worse abstract in 6 of 10 pairs | We found that the LLM performs surprisingly poorly | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 favored the worse abstract in 6 of 10 pairs | We then tested the LLM's ability to accurately ide | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 favored the worse abstract in 6 of 10 pairs | We created 10 pairs of research abstracts, with ea | 33 | - | 33 | 33 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 favored the worse abstract in 6 of 10 pairs | We constructed 10 such pairs of abstracts. In a su | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 feedback overlap fell from 30.85% to 0.43% after shuffling | the pairwise overlap significantly decreased from  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 feedback overlap fell from 30.85% to 0.43% after shuffling | Is it possible that LLM merely generates generic f | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4 feedback overlap fell from 30.85% to 0.43% after shuffling | For each paper in the Nature family journal data,  | 4 | 4 | 4 | 4 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 feedback overlap fell from 30.85% to 0.43% after shuffling | For papers published in the Nature family, the LLM | 9 | 9 | - | - | - | low | left for JP: not found | - |
| GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human | When comparing LLM feedback with comments from eac | 3 | 3 | 3 | 3 | - | high | already correct | - |
| GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human | When comparing LLM feedback with comments from eac | 3 | 3 | 3 | 3 | - | high | already correct | - |
| GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human | We developed a retrospective comment matching pipe | 3 | 3 | 3 | 3 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 feedback overlapped 30.85% with humans vs 28.58% human-human | The first dataset, sourced from Nature family jour | 3 | 3 | 3 | 3 | - | high | already correct | - |
| GPT-4 reached 86.6% accuracy on NeurIPS checklist items | We found that across 119 unique {checklist questio | 2 | 2 | 2 | 2 | - | high | already correct | - |
| GPT-4 reached 86.6% accuracy on NeurIPS checklist items | We queried GPT-4 for three responses per {question | 28 | 28 | 28 | 28 | - | high | already correct | - |
| GPT-4 reached 86.6% accuracy on NeurIPS checklist items | Throughout our experiments, for the LLM, we used t | 28 | 28 | 28 | 28 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| GPT-4 reached 86.6% accuracy on NeurIPS checklist items | We selected 15 papers from the NeurIPS 2022 confer | 27 | 27 | 27 | 27 | - | high | already correct | - |
| GPT-4o abstract scores correlated r=0.67 with humans | The optimal input is the article title and abstrac | 1 | 1 | 1 | 7 | (Thelwall, 2024, p. 7) | high | APPLIED | verified 2026-11-24: quote on printed page 7 (PDF page 1), number printed on that page, both copies edited |
| GPT-4o abstract scores correlated r=0.67 with humans | GPT-4o Abstracts | 8 | 8 | - | - | - | low | left for JP: no quote | - |
| GPT-4o abstract scores correlated r=0.67 with humans | The overall research design was to run a series of | 3 | 3 | 4 | 10 | (Thelwall, 2024, p. 10) | high | APPLIED | verified 2026-11-24: quote on printed page 10 (PDF page 4), number printed on that page, both copies edited |
| GPT-4o abstract scores correlated r=0.67 with humans | Each score request was a single API call, specifyi | 5 | 5 | - | - | - | low | left for JP: not found | - |
| GPT-4o abstract scores correlated r=0.67 with humans | The raw data for this paper is a set of 51 informa | 3 | 3 | 4 | 10 | (Thelwall, 2024, p. 10) | high | APPLIED | verified 2026-11-24: quote on printed page 10 (PDF page 4), number printed on that page, both copies edited |
| GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG | > GPT-4o coarse accuracy = 52.0%, Human = 86.0%, M | 9 | - | - | - | - | low | left for JP: no quote | - |
| GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG | Even the best-performing LLM, GPT-4o, can only ide | 9 | 8 | 8 | 20659 | (Xu et al., 2025, p. 20659) | high | APPLIED | verified 2026-11-24: quote on printed page 20659 (PDF page 8), number printed on that page, both copies edited |
| GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG | We evaluate the performance of 4 frontier LLMs acr | 6 | 7 | 7 | 20658 | (Xu et al., 2025, p. 20658) | high | APPLIED | verified 2026-11-24: quote on printed page 20658 (PDF page 7), number printed on that page, both copies edited |
| GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG | For LIMITGEN-Syn, we use GPT-4o to classify the ge | 5 | 6 | 6 | 20657 | (Xu et al., 2025, p. 20657) | high | APPLIED | verified 2026-11-24: quote on printed page 20657 (PDF page 6), number printed on that page, both copies edited |
| GPT-4o reached 52% on LimitGen-Syn vs 86% for experts and 68.1% for MARG | In total, we compile an initial pool of 1,408 NLP  | 4 | 5 | 5 | 20656 | (Xu et al., 2025, p. 20656) | high | APPLIED | verified 2026-11-24: quote on printed page 20656 (PDF page 5), number printed on that page, both copies edited |
| GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% | All GPT models with our prompting scheme substanti | 5 | 5 | 5 | 5 | - | high | already correct | - |
| GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% | We evaluated the ability of our LLMs to determine  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% | To extract methods-related CONSORT checklist items | 4 | 4 | 4 | 4 | - | high | already correct | - |
| GPT-4o-mini reached F1 0.85 on CONSORT-TM beating prior SOTA by over 40% | For model evaluation, we used a previously curated | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Human agreement fell from 91% on PRISMA to 57% on PRECIS-2 | Human inter-rater reliability measured by agreemen | 8 | 8 | 8 | 8 | - | high | already correct | - |
| Human agreement fell from 91% on PRISMA to 57% on PRECIS-2 | Human inter-rater reliability measured by agreemen | 8 | 8 | 8 | 8 | - | high | already correct | - |
| Human agreement fell from 91% on PRISMA to 57% on PRECIS-2 | We performed 4 analyses for each of the 3 evidence | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Human agreement fell from 91% on PRISMA to 57% on PRECIS-2 | The 2 raters were content experts (British pediatr | 2 | 2 | 2 | 2 | - | high | already correct | - |
| Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR | > Human Review ITF-IDF = 7.69; GPT-4o ITF-IDF = 5. | 10 | - | - | - | - | low | left for JP: no quote | - |
| Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR | there is still a considerable gap in the weakness  | 9 | 9 | 9 | 9 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR | Inspired by the classic TF-IDF, we propose a novel | 6 | 6 | 6 | 6 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR | in WEAKNESS, we try to utilize the whole paper. As | 9 | 9 | 9 | 9 | - | high | already correct | - |
| Human weakness diversity 7.69 vs only 5.95 for best LLM GPT-4o on AAAR | We first crawl a total of 3,779 anonymous submissi | 5 | 5 | 5 | 5 | - | high | already correct | - |
| Human-AI collaboration reached up to 96% on PRISMA surpassing human raters | Human−AI collaboration resulted in the best accura | 1 [Abstract] | 4 | - | - | - | low | left for JP: not found | - |
| Human-AI collaboration reached up to 96% on PRISMA surpassing human raters | Human−AI collaboration resulted in the best accura | 1 | - | - | - | - | low | left for JP: not found | - |
| Human-AI collaboration reached up to 96% on PRISMA surpassing human raters | We combined ratings of individual human raters wit | 5 | 4 | - | - | - | low | left for JP: not found | - |
| Human-AI collaboration reached up to 96% on PRISMA surpassing human raters | Human−AI collaboration with Claude-3-Opus, Claude- | 8 | - | - | - | - | low | left for JP: not found | - |
| Human-AI collaboration reached up to 96% on PRISMA surpassing human raters | best accuracies from 89% to 96%" is the range from | 7 | - | - | - | - | low | left for JP: not found | - |
| Idea Novelty Checker reached 0.81 accuracy beating baselines | Our extensive experiments demonstrate that our nov | 1 | 1 | 1 | 96 | (Shahid et al., 2025, p. 96) | high | APPLIED | verified 2026-11-24: quote on printed page 96 (PDF page 1), number printed on that page, both copies edited |
| Idea Novelty Checker reached 0.81 accuracy beating baselines | > Full results from Table 1: Complete system with  | 7 | - | - | - | - | low | left for JP: no quote | - |
| Idea Novelty Checker reached 0.81 accuracy beating baselines | We evaluated multiple baselines to benchmark our n | 5 | 5 | 5 | 100 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Idea Novelty Checker reached 0.81 accuracy beating baselines | For our novelty evaluation system, we use SPECTER- | 6 | 6 | 6 | 101 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Idea Novelty Checker reached 0.81 accuracy beating baselines | From our formative study, we collected 67 consensu | 5 | 5 | 5 | 100 | (Shahid et al., 2025, p. 100) | high | APPLIED | verified 2026-11-24: quote on printed page 100 (PDF page 5), number printed on that page, both copies edited |
| LLM confidence was near zero across 498 SPOT evaluations | Across 498 model–instance evaluations (83 instance | 7 | 7 | 7 | 7 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM confidence was near zero across 498 SPOT evaluations | Alongside pass@4, calibration indicates how much w | 6 | 6 | 6 | 6 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM confidence was near zero across 498 SPOT evaluations | To assign each ground-truth error g ∈ Gi a confide | 24 | 24 | 24 | 24 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM confidence was near zero across 498 SPOT evaluations | We provide the full paper as interleaved text and  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| LLM confounder choices were highly inconsistent with kappa as low as 0.16 | For GPT o1-preview, there was fair agreement acros | 14–15 | 14 | 14 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM confounder choices were highly inconsistent with kappa as low as 0.16 | In Claude 3.5, 36.7% of variables had different de | 16 | 16 | 16 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM confounder choices were highly inconsistent with kappa as low as 0.16 | In order to assess the consistency of LLM response | 6 | 6 | 6 | - | - | high | left for JP: no printed numbers | - |
| LLM confounder choices were highly inconsistent with kappa as low as 0.16 | For the direct version of the prompt with reasonin | 16 | 16 | 16 | - | - | high | left for JP: no printed numbers | - |
| LLM confounder choices were highly inconsistent with kappa as low as 0.16 | GPT-4o and Claude 3.5 Sonnet are run using a tempe | 6 | 6 | 6 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM review scores exceeded humans without area-chair context but matched with it | The human reviewers have an average recommendation | 10 [Appendix D] | 10 | 13 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM review scores exceeded humans without area-chair context but matched with it | Figure 14 shows the average and standard deviation | 10 | 13 | 13 | - | - | high | left for JP: no printed numbers | - |
| LLM review scores exceeded humans without area-chair context but matched with it | We use multiple documents related to the review as | 6 | 7 | 7 | - | - | high | left for JP: no printed numbers | - |
| LLM review scores exceeded humans without area-chair context but matched with it | We modify the papers by introducing errors or shor | 6 | 6 | 6 | - | - | high | left for JP: no printed numbers | - |
| LLM reviews scored like human reviews on all 3 criteria | Reviews written by humans and GPT-4 with all relat | 13 [Appendix F] | 12 | 14 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| LLM reviews scored like human reviews on all 3 criteria | The human review evaluator assesses reviews writte | 12 | 14 | 14 | - | - | high | left for JP: no printed numbers | - |
| LLM reviews scored like human reviews on all 3 criteria | five expert evaluators were provided with 150 pape | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| LLM reviews scored like human reviews on all 3 criteria | Table 5: The human review evaluator evaluates huma | 12 | 14 | 14 | - | - | high | left for JP: no printed numbers | - |
| LLM-extracted quotes had 99% median similarity to source | The median quote similarity with the original full | 8 | 8 | 8 | 8 | - | high | already correct | - |
| LLM-extracted quotes had 99% median similarity to source | All prompts required the LLMs to 'extract 1-3 rele | 8 | 8 | 8 | 8 | - | high | already correct | - |
| LLM-extracted quotes had 99% median similarity to source | API querying, extraction of ratings, fixing minor  | 5 | 5 | 5 | 5 | - | high | already correct | - |
| LLM-extracted quotes had 99% median similarity to source | Claude-3-Opus, Claude-2, and Mixtral-8x22B sometim | 8 | 8 | 8 | 8 | - | high | already correct | - |
| LLMs flagged expert and trimmed confounders at similar rates | the confounders trimmed from the causal diagram in | 9 | 9 | 9 | - | - | high | left for JP: no printed numbers | - |
| LLMs flagged expert and trimmed confounders at similar rates | Our general approach to checking LLM capabilities  | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| LLMs flagged expert and trimmed confounders at similar rates | We take several different approaches to designing  | 4 | 4 | 4 | - | - | high | left for JP: no printed numbers | - |
| LLMs flagged expert and trimmed confounders at similar rates | From CDPRG (1980), Murray and Hernán (2016), and D | 7 | 7 | 7 | - | - | high | left for JP: no printed numbers | - |
| LLMs made systematic QUADAS-2 patient selection errors | In the patient selection domain, common issues inc | 15 | 14 | - | - | - | low | left for JP: not found | - |
| LLMs made systematic QUADAS-2 patient selection errors | For each article and each signaling question, we q | 10 | 10 | 10 | 10 | - | high | already correct | - |
| LLMs made systematic QUADAS-2 patient selection errors | Concerning the patient selection domain of QUADAS- | 10–11 | 10 | - | - | - | low | left for JP: fragments on different pages | - |
| LLMs made systematic QUADAS-2 patient selection errors | The human assessment was performed by two authors  | 2 | 2 | 2 | 2 | - | high | already correct | - |
| LLMs performed suboptimally on placebo arm and risk issues in a single prompt | LLMs performed suboptimally in identifying the sui | 131 | 4 | 1 | 126 | (Sridharan & Sivaramakrishnan, 2025, p. 126) | high | APPLIED | verified 2026-11-24: quote on printed page 126 (PDF page 1), number printed on that page, both copies edited |
| LLMs performed suboptimally on placebo arm and risk issues in a single prompt | We compared the responses of the LLMs with a singl | 127 | 2 | 2 | 127 | - | high | already correct | - |
| LLMs performed suboptimally on placebo arm and risk issues in a single prompt | Then, an additional query was posted as follows: ' | 128 | 3 | 3 | 128 | - | high | already correct | - |
| LLMs performed suboptimally on placebo arm and risk issues in a single prompt | Four AI platforms were evaluated as follows: 1. Go | 127 | 2 | 2 | 127 | - | high | already correct | - |
| LLMs were least accurate on software and funding questions | When all LLMs are collectively considered, the thr | 16 | 19 | 14 | - | - | high | left for JP: no printed numbers | - |
| LLMs were least accurate on software and funding questions | When all LLMs are collectively considered, the thr | 14 | 14 | 14 | - | - | high | left for JP: no printed numbers | - |
| LLMs were least accurate on software and funding questions | The percentages of correct answers given by all LL | 15 | 15 | 15 | - | - | high | left for JP: no printed numbers | - |
| LLMs were least accurate on software and funding questions | In this study, 15 questions selected from the STRO | 12 | 12 | 12,13 | - | - | low | left for JP: multiple pages | - |
| MARG-S beat baselines by 6.1 recall points on ARIES | our method outperforms the strongest baseline by 6 | 1 | 2 | 2 | - | - | high | left for JP: no printed numbers | - |
| MARG-S beat baselines by 6.1 recall points on ARIES | We find that our proposed MARG-S method outperform | 11 | 10 | 10 | - | - | high | left for JP: no printed numbers | - |
| MARG-S beat baselines by 6.1 recall points on ARIES | To automatically evaluate the quality of generated | 9 | 8 | 8 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| MARG-S beat baselines by 6.1 recall points on ARIES | we begin with a 'many-many' matching stage that ef | 9 | 8 | 8 | - | - | high | left for JP: no printed numbers | - |
| MARG-S beat baselines by 6.1 recall points on ARIES | we use GPT to extract comments from all reviews fo | 9 | 8 | 8 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 | MARG-S generated 3.7 'good' comments per paper (ra | 1 | 1 | 1 | - | - | high | left for JP: no printed numbers | - |
| MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 | 71% of MARG-S's comments were rated as specific. | 2 | 2 | 2 | - | - | high | left for JP: no printed numbers | - |
| MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 | We conduct a user study to obtain a more reliable  | 13 | 13 | 13 | - | - | high | left for JP: no printed numbers | - |
| MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 | When all reviews were generated, participants woul | 14 | 13 | - | - | - | low | left for JP: not found | - |
| MARG-S gave 3.7 good comments per paper vs 1.7 for GPT-4 | We recruit 9 volunteers from a large research orga | 13 | 13 | 13 | - | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| MultiVerS reached micro-F1 0.59 on citation accuracy | The best performing model—which uses citation sent | 1 | 1 | 1 | 1 | - | high | already correct | - |
| MultiVerS reached micro-F1 0.59 on citation accuracy | We report standard evaluation metrics, precision,  | 5 | 5 | 5 | 5 | - | high | already correct | - |
| MultiVerS reached micro-F1 0.59 on citation accuracy | we leveraged a state-of-the-art claim verification | 4 | 4 | 4 | 4 | - | high | already correct | - |
| MultiVerS reached micro-F1 0.59 on citation accuracy | We collected 100 highly-cited research articles av | 2 | 2 | 2 | 2 | - | high | already correct | - |
| No AI platform recognized the IRB quorum requirement | Concerning the SOP for the initial review of propo | 85 | 7 | 3 | 85 | - | high | already correct | - |
| No AI platform recognized the IRB quorum requirement | Management of initial protocol submissions to IRB | 84 | 2 | 2 | 84 | - | high | already correct | - |
| No AI platform recognized the IRB quorum requirement | Concerning the SOP for the initial review of propo | 85 | 3 | 3 | 85 | - | high | already correct | - |
| No AI platform recognized the IRB quorum requirement | Two authors independently assessed the outputs of  | 85 | 3 | 3 | 85 | - | high | already correct | - |
| Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment | validity, 9.7% reported randomization sequence gen | 6 | 6 | 6 | 6 | - | high | already correct | - |
| Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment | We analyzed reporting patterns across CONSORT sect | 4 | 4 | 4 | 4 | - | high | already correct | - |
| Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment | validity, 9.7% reported randomization sequence gen | 6 | 6 | 6 | 6 | - | high | already correct | - |
| Only 9.7% of RCTs reported sequence generation and 15.25% allocation concealment | For large-scale analysis, we identified 53,137 ope | 3 | 3 | 3 | 3 | - | high | already correct | - |
| OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o | While OpenReviewer matches the human reviewers wit | 4 | 5 | 4 | 4 | - | high | already correct | - |
| OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o | While OpenReviewer matches the human reviewers wit | 4 | 4 | 4 | 4 | - | high | already correct | - |
| OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o | We generate one review for each paper in the test  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| OpenReviewer averaged 5.4 like humans vs 7.7 for GPT-4o | To measure how well OpenReviewer reviews align wit | 4 | 4 | 4 | 4 | - | high | already correct | - |
| OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons | According to the LLM judge, OpenReviewer wins agai | 5 | 5 | 5 | 5 | - | high | already correct | - |
| OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons | We run an arena-style preference evaluation with a | 4 | 4 | - | - | - | low | left for JP: not found | - |
| OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons | Given a set of human "expert" reviews and two revi | 5 | 5 | 5 | 5 | - | high | already correct | - |
| OpenReviewer beat GPT-4o in 60% and Llama-3.1-70B in 76% of judge comparisons | we conduct experiments using a test set of 400 hel | 4 | 4 | 4 | 4 | - | high | already correct | - |
| OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o | OpenReviewer matches at least one human reviewer f | 4 | 4 | 4 | 4 | - | high | already correct | - |
| OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o | To measure how well the recommendation of a genera | 4 | 4 | - | - | - | low | left for JP: not found | - |
| OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o | we conduct experiments using a test set of 400 hel | 4 | 4 | 4 | 4 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| OpenReviewer matched a human reviewer on 55.5% of papers vs 23.8% for GPT-4o | To measure how well OpenReviewer reviews align wit | 4 | 4 | 4 | 4 | - | high | already correct | - |
| Ours-SciBERT reached F1=0.83 on method novelty prediction | As shown in Table 2, the model based on SciBERT pe | 1462 | 11 | 11 | 1462 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Ours-SciBERT reached F1=0.83 on method novelty prediction | We adopt Accuracy and Weighted F1 as the evaluatio | 1460 | 9 | 9 | 1460 | - | high | already correct | - |
| Ours-SciBERT reached F1=0.83 on method novelty prediction | We split our dataset by a ratio of 8:1:1 for train | 1460 | 9 | 9 | 1460 | - | high | already correct | - |
| Ours-SciBERT reached F1=0.83 on method novelty prediction | Following all the aforementioned preprocessing ste | 1458 | 7 | 7 | 1458 | - | high | already correct | - |
| RAG raised GPT-4o limitation accuracy by 12.2 points | > GPT-4o coarse accuracy without RAG = 52.0%; with | 9 | - | - | - | - | low | left for JP: no quote | - |
| RAG raised GPT-4o limitation accuracy by 12.2 points | incorporating the RAG method can enhance LLM perfo | 9 | 8 | 8 | 20659 | (Xu et al., 2025, p. 20659) | high | APPLIED | verified 2026-11-24: quote on printed page 20659 (PDF page 8), number printed on that page, both copies edited |
| RAG raised GPT-4o limitation accuracy by 12.2 points | we enhanced the evaluated systems' capabilities by | 7 | 7 | 7 | 20658 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| RAG raised GPT-4o limitation accuracy by 12.2 points | Specifically, the retrieval process leverages the  | 7 | 7 | 7 | 20658 | (Xu et al., 2025, p. 20658) | high | APPLIED | verified 2026-11-24: quote on printed page 20658 (PDF page 7), number printed on that page, both copies edited |
| RAG raised GPT-4o limitation accuracy by 12.2 points | We collect a total of 9,844 papers and randomly sa | 5 | 6 | 6 | 20657 | (Xu et al., 2025, p. 20657) | high | APPLIED | verified 2026-11-24: quote on printed page 20657 (PDF page 6), number printed on that page, both copies edited |
| Removing knowledge module cut novelty accuracy from 0.84 to 0.74 | Results from Table 4 indicate a significant decrea | 1463 | 11 | 12 | 1463 | - | high | already correct | - |
| Removing knowledge module cut novelty accuracy from 0.84 to 0.74 | To better understand the effectiveness of each com | 1463 | 12 | 12 | 1463 | - | high | already correct | - |
| Removing knowledge module cut novelty accuracy from 0.84 to 0.74 | We systematically removed three components, namely | 1463 | 12 | 12 | 1463 | - | high | already correct | - |
| Removing knowledge module cut novelty accuracy from 0.84 to 0.74 | We split our dataset by a ratio of 8:1:1 for train | 1460 | 9 | 9 | 1460 | - | high | already correct | - |
| Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans | Individual LLM accuracy was ranging from 63% (GPT- | 1 [Abstract] | 1 | 1 | 1 | - | high | left for JP: non-simple citation form | - |
| Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans | Our main outcome was agreement with human consensu | 3 | 3 | 3 | 3 | - | high | already correct | - |
| Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans | We performed LLM prompts twice (ie, in duplicate f | 5 | 5 | 5 | 5 | - | high | already correct | - |
| Single LLMs scored 63-70% on PRISMA and 53-74% on AMSTAR vs 89% for humans | We used 4 proprietary LLMs (Anthropic's Claude-3-O | 2–3 | 2 | 2 | 2 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| Three AI platforms answered all 10 IRB cases correctly | The trio of AI platforms successfully responded to | 85 | 6 | 3 | 85 | - | high | already correct | - |
| Three AI platforms answered all 10 IRB cases correctly | The present work represents a cross-sectional, obs | 84 | 2 | 2 | 84 | - | high | already correct | - |
| Three AI platforms answered all 10 IRB cases correctly | The AI platforms were prompted with ten case studi | 84 | 2 | 2 | 84 | - | high | already correct | - |
| Three AI platforms answered all 10 IRB cases correctly | Two authors independently assessed the AI outputs, | 84 | 2 | 2 | 84 | - | high | already correct | - |
| o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication | In the Equation/Proof category, o3 leads with a 62 | 6 | 6 | 6 | 6 | - | high | already correct | - |
| o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication | Error Types: We derive the six categories in Table | 3 | 3 | 3 | 3 | - | high | already correct | - |
| o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication | For each pass@K we draw K runs without replacement | 5 | 5 | 5 | 5 | - | high | already correct | - |
| o3 hit 62.6% pass@4 on equation-proof errors but near 0% on figure duplication | We classify each paper into ten research domains:  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| o3 led SPOT with 37.8% pass@4 | Evaluating state-of-the-art LLMs on SPOT, we find  | 1 | 1 | 1 | 1 | - | high | already correct | - |
| o3 led SPOT with 37.8% pass@4 | > Table 2 data: o3 (2025-04-16): Precision=6.1±1.3 | 5 | 5 | - | - | - | low | left for JP: no quote | - |
| o3 led SPOT with 37.8% pass@4 | We mainly evaluate verification performance throug | 4 | 4 | 4 | 4 | - | high | already correct | - |
| o3 led SPOT with 37.8% pass@4 | We provide the full paper as interleaved text and  | 4 | 4 | 4 | 4 | - | high | already correct | - |
| o3 led SPOT with 37.8% pass@4 | The final SPOT benchmark comprises 83 manuscripts  | 3 | 3 | 3 | 3 | - | high | already correct | - |
| o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX | The OpenAI o3 model performed the best, while o4-m | 1 | 4 | 1 | - | - | high | left (v1 numbers by design) | - |
| o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX | Each LLM judge independently evaluates an LLM qual | 3 | 3 | 3 | - | - | high | left (v1 numbers by design) | - |
| o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX | In this work, we took $k=5$, $n_c=1$, $n_j=1$, and | 3 | 3 | 3 | - | - | medium | left (v1 numbers by design) | - |
| o3 led reasoning LLMs with 64.9% hit rate on PDF and 71.0% on LaTeX | We utilized WITHDRARXIV (Rao et al., 2024), a larg | 2 | 2 | 2 | - | - | high | left (v1 numbers by design) | - |
| o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline | a simple baseline that predicts all equations as p | 7 | 7 | 7 | 7 | - | medium | left for JP: partial (start/end of quote matches one page) | - |
| o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline | For EQINFER, we adopt F1 as the classification cri | 6 | 6 | 6 | 6 | - | high | already correct | - |
| o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline | we fix the maximum input length for all models. Ac | 7 | 7 | 7 | 7 | - | high | already correct | - |
| o3-mini led AAAR EqInfer at 47.98% F1 barely above 40% baseline | we get a total of 1,762 papers' source LaTeX packa | 3–4 | 3 | - | - | - | low | left for JP: fragments on different pages | - |
| o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3 | o4-mini seems to be the most cost-effective choice | 3 | 4 | 3 | - | - | high | left (v1 numbers by design) | - |
| o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3 | Average costs of reviewing a paper under each pipe | 3 | 3 | 3 | - | - | high | left (v1 numbers by design) | - |
| o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3 | In our experiments, both approaches utilized the s | 3 | 3 | 3 | - | - | high | left (v1 numbers by design) | - |
| o4-mini reached 59.6% HR@5 at 0.038 USD per paper vs 0.321 USD for o3 | We randomly sampled 20% of the dataset (245 cases) | 2 | 2 | 2 | - | - | high | left (v1 numbers by design) | - |

# Screening run 2026-11-25_Zotero-all-libraries

Every item in all Zotero libraries screened against the 27 seed papers and the Elicit papers. Built 2026-11-25. Reported following TRIPOD+LLM as far as it fits (embedding models only, no text generation). The Google Sheet has the full per-paper tables; this folder holds the metadata-only data and the settings.

## Reporting guideline
TRIPOD+LLM (Gallifant et al.), applied as far as it fits. The models only embed text, so items about generation, prompting and fine-tuning are not applicable.
- [TRIPOD+LLM statement](https://www.tripod-statement.org/tripod-llm/)

The review sheet: `https://docs.google.com/spreadsheets/d/1R70T7JJD3-RDM5kPc6-rI1ZZ2qCb82TVE19OjzyuyrA/edit` (private; ask JP for access).

## 1. Purpose
Support the Stage 2 ingest: find every paper in JP's Zotero libraries that is close to the seed set and the Elicit papers, sort the ingest folders (Metascience, SysRev-LLMApp, the Elicit sets, Include-CA-Rep) into categories, and mark which have an open-access copy or a PDF on disk. JP reviews every row; the output is a proposal.

## 2. Data source and population
Read-only copy of the Zotero database (2026-11-25): 19,992 regular items and standalone PDFs in 7 libraries (Gesture Elicitation Studies 295, OASIS Lab 13,978, OTTRS Mental Models 94, Open Science Readings 2,174, Trust & Co 13, personal 3,256, preprint_literature 182). After merging duplicates (same DOI, same arXiv id or a near-identical title): 17,544 distinct papers. Sheet rows: 3,441 (all papers in an ingest folder, plus 436 found elsewhere because they are close to the seed and Elicit papers). Nothing in Zotero was changed by the screening.
- [Inventory script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/zotero_inventory.py)
- [Seed papers and task groups](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/screening/shared/seed-papers_task-groups.json)

## 3. Text embedded
Title plus the Zotero abstract (at most 1,800 characters); if there is none, the abstract section of a PDF on disk; if none, the text of an HTML snapshot; otherwise the title alone. Counts: abstract (Zotero) 13,270, HTML snapshot 321, title only 2,424, PDF (abstract section) 1,529. Title-only papers are placed weakly.
- [Pipeline script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/screen_all.py)

## 4. Models
Three open-weight embedding models run locally on one Apple-silicon computer (no API, no data leaves the machine): EmbeddingGemma 2 (Google), harrier-oss-v1-0.6b (Microsoft; prompt sts_query) and DNA-VL-STEER-2B (Dnotitia; float16). No generation and no fine-tuning.
- [Settings and results](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_Zotero-all-libraries/data/settings_and_results.json)

## 5. Method
1. **Closeness.** A paper is marked close to the seed and Elicit papers when, in any one of the three models, its highest cosine similarity to the 125 reference papers (27 seeds, the Elicit 2026-11-24 papers, Include-CA-Rep) is above the 10th percentile of how similar the reference papers are to each other. Any-model was chosen on purpose to favour false positives, because JP reviews every row but would not find a missed paper.
2. **Categories.** Each sheet row gets the task group of its most similar seed paper in each model, or NEW if below that model's 15th percentile of seed-to-seed nearest similarity. The majority of three decides.
3. **New categories.** NEW papers are clustered (Ward linkage on the joined embeddings, 15 to 30 clusters, best silhouette). Names and task types were written by Claude Sonnet 5.5 and are not yet checked by JP.
4. **Open access.** From OpenAlex by DOI (public DOIs only); papers without a DOI are not checked. "PDF on disk" and "HTML snapshot on disk" report what is in Zotero.
- [Open-access script](https://github.com/cdromcom/living-evidence-synthesis/blob/main/vault/pipeline/scripts/oa_lookup.py)

## 6. Performance (proxy labels, not JP's decisions)
- **Category assignment**, leave-one-out on the 26 testable seed papers: majority of three 77%; EmbeddingGemma 2 73%, harrier 81%, DNA-VL-STEER-2B 88%. The small test set (26) gives wide uncertainty.
- **Closeness**, 98 reference papers left out one at a time against 401 papers from clearly unrelated collections: any-model rule sensitivity 94%, specificity 99.8%, balanced accuracy 96.8%, AUC 0.999; majority rule sensitivity 90%, specificity 100%. The any-model rule flags 436 papers outside the ingest folders, the majority rule 123.
- **New categories** are weak: silhouette 0.017 for 30 clusters of 3,318 papers. The Metascience folder is mostly far from the seed papers, so its categories describe topics, not LLM tasks; treat them as a browsing aid.
- Real accuracy on JP's include and exclude decisions is unknown until the JP columns are filled.

## 7. Time and cost
Computing about 4.7 h on one Mac: inventory 2 s, preparation 127 s, embedding 17,571 texts with three models 4.3 h (EmbeddingGemma 2 28 min, harrier 59 min, DNA-VL-STEER-2B 2.8 h), open-access lookup about 10 min, analysis a few minutes. API cost $0 (local models; OpenAlex is free).

## 8. Limits
Embedding similarity is not a judgment of relevance. Abstracts in Zotero can be wrong. The Elicit set includes the 2023 "elicit-results (1)" folder, which is mostly bibliometrics. The reference papers are in the ingest by JP's choice, so a proxy accuracy can overstate performance on papers unlike them.

## 9. Files
- [Papers, categories and model votes (metadata only)](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_Zotero-all-libraries/data/papers_categories-and-model-votes.tsv)
- [Categories summary](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_Zotero-all-libraries/data/categories_summary.tsv)
- [New category names and task types](https://github.com/cdromcom/living-evidence-synthesis/tree/main/vault/pipeline/screening/2026-11-25_Zotero-all-libraries/data/new-category-names_and-task-types.json)
- Abstracts and local file paths are not published.

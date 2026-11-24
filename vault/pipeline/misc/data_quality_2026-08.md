# Data Quality (FAIRness of released datasets) — 2026-08

Goal: a single 0–24 "Data Quality" signal, analogous to the existing Code Quality
(howfairis, 0–5, GitHub/GitLab only) signal, but covering every platform a source's
dataset happens to live on — GitHub, OSF, HuggingFace — on one consistent scale.

## Tool and the GitHub problem

Used [FAIR-Checker](https://fair-checker.france-bioinformatique.fr) (IFB/ElixirFr),
a semantic-web/schema.org-based FAIR assessor. Its REST endpoint
(`GET /api/check/metrics_all?url=<url>`) scores 12 metrics 0–2 each (max 24):
Unique IDs, Persistent IDs, Open resolution protocol, Structured metadata, Machine
readable format, Use shared ontologies, Shared vocabularies for metadata, External
links, Metadata includes provenance, Community standards, Metadata includes
license, Authorisation procedure or access rights.

Testing against every GitHub-hosted dataset in the corpus returned an identical,
uninformative flat score of **4/24** every time — only "Unique IDs" (has a URL) and
"Open resolution protocol" (HTTPS) ever passed. The other 10 metrics all require
schema.org/JSON-LD metadata embedded in the page, which plain GitHub repo pages
never carry. A raw FAIR-Checker score is therefore meaningless as a cross-source
signal for the ~11 of 14 datasets that live on GitHub.

## The hybrid fix

For GitHub/GitLab-hosted data, the FAIR-Checker score is topped up **+2** if the
repo has a real LICENSE file — reusing the license-detection result already
computed for the Code Quality signal (howfairis reads repo content directly,
which FAIR-Checker's page-metadata approach can't see). This is a deliberate,
documented departure from a single-tool score, not a raw FAIR-Checker number.
Native FAIR-Checker scores (OSF, HuggingFace — both do carry real structured
metadata) are used as-is, unmodified.

Chip/badge tone thresholds: 🟢 ≥16/24, 🟡 ≥8/24, 🔴 <8/24. Graph-view filter
checkbox uses ≥15/24 (~62%), chosen to match Code Quality's existing "meets
baseline" bar of ≥3/5 (60%).

## Per-source scores (14 of 27 sources with a checkable dataset)

| Source | Score | URL | Native or +2 topup |
|---|---|---|---|
| Huntington-Klein & Murray 2024 | **16/24** | osf.io/spzbu | native (OSF) |
| Liu & Shah 2023 (ReviewerGPT) | **4/24** | github.com/niharshah/ReviewerGPT2023 | GitHub, no license |
| Lou et al. 2025 (AAAR-1.0) | **6/24** | github.com/RenzeLou/AAAR-1.0 | GitHub, +2 (has license) |
| Sarol et al. 2024 (Citation-Integrity) | **6/24** | github.com/ScienceNLP-Lab/Citation-Integrity | GitHub, +2 (has license) |
| Shahid et al. 2025 (idea_novelty_checker) | **4/24** | github.com/simra-shahid/idea_novelty_checker | GitHub, no license |
| Son et al. 2025 (AI Co-Scientists) | **9/24** | huggingface.co/datasets/amphora/SPOT-MetaData | native (HuggingFace) |
| Srinivasan et al. 2025 (RCT-Transparency) | **6/24** | github.com/ScienceNLP-Lab/RCT-Transparency | GitHub, +2 (has license) |
| Woelfle et al. 2024 (Evidence-Appraisal-AI) | **4/24** | github.com/timwoelfle/Evidence-Appraisal-AI | GitHub, no license |
| Wrightson et al. 2025 | **16/24** | osf.io/4shmt | native (OSF) |
| Wu et al. 2024 (method_novelty_predict) | **4/24** | github.com/njust-winchy/method_novelty_predict | GitHub, no license |
| Xu et al. 2025 (LimitGen) | **4/24** | github.com/yale-nlp/LimitGen | GitHub, no license |
| Zhang & Abernethy 2024 (ReferenceErrorDetection) | **6/24** | github.com/tianmai-zhang/ReferenceErrorDetection | GitHub, +2 (has license) |
| Zhang & Abernethy 2025 (WithdrarXiv-Check) | **6/24** | github.com/tianmai-zhang/WithdrarXiv-Check | GitHub, +2 (has license) |
| Zhou et al. 2024 (RR-MCQ) | **9/24** | huggingface.co/datasets/zhouruiyang/RR-MCQ | native (HuggingFace) |

Two repo URLs (Wrightson's OSF link, Zhang 2024's GitHub link) and one HuggingFace
dataset URL (Son 2025) were not present in the extracted text layer of the source
PDFs at all — they were recovered by reading each PDF's embedded hyperlink
annotations directly via PyMuPDF (`page.get_links()` → `uri`), since the actual
URL only lived in the link-annotation layer behind a footnote-style superscript
in the visible text.

## The 13 sources with no Data Quality tag

No available/redistributed dataset to check: Akyon, Alharbi, Bougie, D'Arcy
(MARG — the ARIES corpus requires a separate S3 pull, not a simple checkable
URL), Hasan, Idahl (HuggingFace page is a *model* card only — the dataset
itself is "not itself redistributed"), Leucuta (embedded in the article/
supplement, no separately hosted dataset), Liang (sourced live from external
Nature/OpenReview APIs, not their own redistributed dataset), Roberts,
Sridharan (both papers — embedded in supplemental material only), Thelwall
(data availability explicitly ❌ — "never disclosed to anyone else"), Tyser
(no static dataset URL, only a mention of a live "free service").

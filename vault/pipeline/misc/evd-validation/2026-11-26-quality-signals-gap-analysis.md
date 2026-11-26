---
page_type: analysis
created: 2026-11-26
author: Claude (Sonnet 5.5) for Jay Patel (JP)
status: items 1 to 9 of the code problems built and run on the four pilot papers (2026-11-26 night); cost changes not built
---

# Quality signals: what the paper processor checks, what it trusts, and what to add

## What runs today
- The `qs` stage of `lives_run.py` has two models (Gemini 4 Neon High, Claude Opus 5.5) rate 25 signals per paper from the PDF alone, with a quote anchored in the PDF text; GPT-6.2 Sol decides disagreements. Measured cost on one paper (Sarol, run `test-anchors`): $0.41 for the whole stage.
- It does **not** call the earlier scripts: `provenance/run_provenance.py` (OpenAlex, DOAJ, OpenCitations, PubPeer, howfairis, FAIR-Checker), `stat_checks.py` and `stat_checks_more.py` (eighteen scripted checks), Pangram. No file in `lives_run.py` or `lives_stages.py` imports them. TRIPOD-LLM rows, `appraisal/overall`, `sample-size-estimation`, `study-type`, `code-quality-fair`, `data-quality-fair`, `ai-writing-check` and `statistic-accuracy` are not produced by the stage.
- Ran 2026-11-26: `openalex.py`, `doaj.py`, `opencitations.py` and `pubpeer.py` still work (Woelfle 10.1016/j.jclinepi.2024.111533 and Sarol 10.1093/bioinformatics/btae420).

## Which signals need more than the paper
| Signal | What the paper gives | What must be checked outside the paper | Tool |
|---|---|---|---|
| `top/study-registration`, `top/study-protocol` | a claim of preregistration | the registry record exists, its date is before data collection, the outcomes match | OSF API, ClinicalTrials.gov API, PROSPERO search |
| `top/code-transparency`, `top/code-check`, `top/code-quality-fair` | a link or "on request" | the link resolves; the repository is not empty; licence; release or archive DOI; last commit versus the paper date; run instructions; pinned dependencies | GitHub API, Zenodo, Software Heritage, howfairis (github.com and gitlab.com only) |
| `top/data-transparency`, `top/repository-check`, `top/data-quality-fair` | a link or "on request" | link resolves; persistent identifier; machine-readable licence; metadata; access conditions | DataCite, Zenodo, OSF, Hugging Face APIs; FAIR-Checker plus F-UJI |
| `integrity/funding-disclosure`, `coi-disclosure` | a statement | author affiliations and funders on record (an author employed by the vendor of an evaluated model with "no conflicts" is a flag) | OpenAlex (institutions, grants), Crossref funder data, ORCID |
| `integrity/ethical-approval` | a statement | approval number or exemption plausible for the institution | manual spot check |
| `rigor/data-leakage` | what the authors say | model training cutoff versus the date the test data became public; whether the test set is online | model cards, dataset first-public date (Zenodo, GitHub, Hugging Face commit history) |
| `appraisal/reproducibility`, `trust/reproducibility` | versions, temperature, seed | pinned model ids still available or deprecated; repository runs | provider deprecation pages; a run attempt (costly) |
| `statistic-accuracy`, `statcheck` | numbers | recomputation (GRIM, percentages, CI containment, F1 from precision and recall, p from t and df) | `stat_checks.py` (free) |
| `integrity/ai-writing-check` | text | detector score | Pangram, only on JP's command |
| Provenance fields: retraction status, author track record, PubPeer, DOAJ, citations, peer-review status, preprint versus published | none | all external | OpenAlex, Crossref (Retraction Watch data), DOAJ, OpenCitations, PubPeer |
Paper-only (the paper is the evidence, judged by raters): construct, internal and external validity, statistical conclusion validity, baseline adequacy, human baseline, ablations, confidence intervals, chance-corrected metrics, multiple comparisons, effect size, exact p-values, power, sample-size estimation, study type, spin. Two of these have an outside part: `prompt-engineering` (are the prompts actually in the appendix or repository) and `train-dev-test` (does the released data have the splits).

## Problems found in the earlier code (read, and ran the OpenAlex part)
1. **Retraction match by author id gives false positives.** Woelfle: OpenAlex matched "Letter Re: Retraction: Risedronate Therapy For Pre..." (2017) to author Ludwig Kappos. That is a letter about a retraction, not a retracted work by the author, and OpenAlex author ids clash. Fix: require an ORCID match, ignore letters, editorials and retraction notices, and cross-check Crossref relations.
2. **Papers without a DOI cannot be looked up.** Bougie (arXiv) and Tyser have no DOI in the extraction; `openalex.py` takes a DOI only. Fix: look up by arXiv id (`10.48550/arXiv.<id>`) or by title, and link preprints to their published versions.
3. **The paper's references are not checked for retractions.** `openalex.py` already fetches every referenced work to compute self-citation; adding `is_retracted` to its `select` costs no extra call and tells JP whether the paper cites retracted work.
4. **howfairis scores code libraries, not analysis code.** Its "registry" and "checklist" criteria are 0 for most research repositories, so a good analysis repository scores 3 of 5 at best. It only supports github.com and gitlab.com, and needs its own virtual environment (old click pin). Fix: a small checker on the GitHub API and Software Heritage for the criteria that matter for research code (public, licence, README with run instructions, pinned dependencies, release or archive DOI, CITATION.cff, commit date).
5. **FAIR-Checker top-up is arbitrary.** `fair_checker.py` adds 2 points when a GitHub-hosted dataset has a licence. Fix: report F, A, I and R sub-scores separately; give datasets with a DOI on Zenodo, OSF or Dryad a DataCite check; mark GitHub-only data "no persistent identifier"; add F-UJI as a second assessor.
6. **PubPeer uses an undocumented endpoint with a browser-extension dev key.** It works today (0 comments for both papers) but can stop without notice and may breach PubPeer's terms; keep it as a link-only fallback and record the HTTP status.
7. **Two quote checkers.** `audit_signal_quotes.py` and the processor's anchors (`pdf_pages.text_between`) verify quotes differently. Use the processor's.
8. **Stale lists.** `check_quality_signals.py` has a hard-coded `REQUIRED` list that lacks signals added later; `signals_decision_models.py` still names d1-ultra and Jev. Derive the list from `quality-signal-labels.json` and use the current decision models.
9. **No provenance record.** Provenance results are printed, not stored. Store `provenance.json` per paper with the query date, URLs, HTTP status and a response hash (OpenAlex changes over time).

## Cost ideas
Measured: $0.41 per paper for the whole `qs` stage (Sarol), with the full PDF sent to each rater and 25 signals per request. The rest are estimates until tried.
1. Do the factual-presence signals with code and send the model only the hits: registration ids, code and data links, funding, COI and ethics statements, exact p-values, CIs, effect sizes, kappa or MCC. The model then judges a few passages, not the PDF.
2. Use one rater for presence signals and two raters only for the judgment signals (validity domains, baseline adequacy, human baseline, leakage, spin, reproducibility; about 10 of 25). Skip the second rater when the first says "none" and the code finds no hit.
3. Gemini 4 Neon at medium instead of High for presence signals (Woelfle extraction already needs medium; High used a 40,000-token budget).
4. Cache provenance results by DOI and URL for 30 days; the APIs are free.
5. Prompt caching and batch (already batch): cache the paper text when one paper is rated in several requests.

## Proposed order
1. Wire `provenance/` and `stat_checks.py` into the runner as a code-only stage that writes `provenance.json`; fix items 1 to 3 above.
2. Link and repository checker (resolve, archive, licence, commit date, empty repository).
3. Give the raters the tool results as evidence for registration, code, data, funding and COI signals.
4. Cost changes 1 and 2, measured on the four pilot papers against JP's labels.

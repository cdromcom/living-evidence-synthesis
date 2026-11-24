---
author: Claude (Opus 5.5), [[Jay Patel]]
page_type: index/methods
created: 2026-11-20
updated: 2026-11-20
generated_by: human-collaborated authoring
prompt_source: "pipeline/misc/prompts/2026-11-11-evd-validation-gsheet-prompt-log.md (prompts 51-52)"
vault: living-synthesis
human_verified: no
---

# 🛠️ Tools and models

What this vault has used to read PDFs and write its nodes, and what it will use from now on. For maintainers; readers can skip it. Linked from [[Welcome]].

---

## Used so far (as of 2026-11-20)

Checked against `Skill.md`, `Skill-references.md`, `Skill-templates.md`, `History.md`, `Log.md`, `pipeline/scripts/` and `pipeline/misc/scripts/`.

### PDF tools

| Tool | What it did | Where it is recorded |
|---|---|---|
| **PyMuPDF** (`fitz`), v1.27.2.3 | Main tool: word coordinates for locating quotes, 250 DPI quote crops with colour highlights, and text for the audit and keyword scripts | `Skill.md` Step 3b; `History.md` (install); `pipeline/scripts/quote_pipeline.py`, `extract_quotes.py`, `cvt_screenshot_pipeline.py`, `verbatim_audit.py`; `pipeline/misc/scripts/keyword_freq_check.py`, `pangram_check.py` |
| **poppler `pdftoppm`** | Full-page figure and table screenshots (`-r 250 -png`) and page renders for reading tables | `Skill.md` Steps 3a and 6b; installed with Homebrew in the April session (`Log.md`) |
| **poppler `pdftotext`** | Text extraction (`-layout`) for quote and number checks. `-bbox-layout` was used for word coordinates at first, then dropped because it crashed on some PDFs | `Skill.md`; `History.md` |
| Ghostscript, ImageMagick, `pdfimages` | **Not used.** Only probed in April; none were installed | `Log.md` |

> [!warning] Known weaknesses of the tools used so far
> - `pdftotext` garbles dashes ("Human−AI" becomes "HumaneAI"), so verbatim checks fail on correct quotes.
> - No OCR: a scanned PDF with no text layer gives empty output.
> - `pdftotext -layout` interleaves two-column pages and misaligns wide tables; this caused the row and column shifts found in the 2026-11-17 number audit.
> - Only one text extractor was used, so there was nothing to cross-check its output against.

### Models

| Model | Role | Where it is recorded |
|---|---|---|
| Claude Sonnet 4.6 and Claude Opus 4.7 (Claude Code) | Built the vault in April 2026: first extraction of QUE, EVD, CLM and CVT nodes, EVD rewrites, subagent batches | `Log.md`; `History.md` (`author: Claude (Opus 4.7 / Sonnet 4.6)`; the April notes were "Claude 4.7, per user recollection, only partly sure") |
| "Claude Sonnet 5" | Recorded as the curation model on 27 source pages | `curatedWithModel` in source frontmatter; convention in `Skill-references.md` |
| Claude Opus 5.5 (Claude Code) | All work from 2026-11-11 to 2026-11-20: EVD drafts, PDF number audit, Fidelity/Grounding grading, version comparisons | AI Prompt Log tab in the GSheet; `pipeline/misc/prompts/2026-11-11-evd-validation-gsheet-prompt-log.md` |
| Pangram `pangram-4` (API) | AI-writing detection on the source PDFs (text only) | `pipeline/misc/scripts/pangram_check.py` |

Model names such as GPT-4 or o3-mini that appear in these files are models studied by the papers, not tools used here.

---

## v2 toolchain (decided by JP, 2026-11-24): hosted APIs, simpler

> [!important] Supersedes the local-model plan below
> JP chose hosted APIs over local models and a smaller toolchain. The 2026-11-20 plan below is kept for the record.

| Step | Tool or model | Notes |
|---|---|---|
| Read PDFs | **GPT-6.2 Sol** (OpenAI; PDF input; reasoning effort High) | replaces Gemini 4 Neon, which replaced LlamaParse (JP, 2026-11-24: Google AI Studio would not issue an API key); page-by-page markdown, HTML tables, printed page numbers; $2 in and $10 out per million tokens, batch $1 and $5 (third-party pages; confirm on OpenAI's pricing page); requests over about 272K input tokens may be billed at a higher long-context rate; LlamaParse ($0.0375 per page) stays as the fallback |
| Second vote | PyMuPDF text layer | born-digital PDFs; the rendered page image decides disagreements |
| Crop and highlight | PyMuPDF word coordinates and `pdftoppm` | cross-checked against the parsed table cells; printed page numbers from the page map |
| Bulk extraction, question splitting and restyling, alt text, link repair | **GPT-6.2 Sol** (High for extraction; Medium for restyling, alt text, link repair) | Max only if a pilot shows it removes errors High leaves (5 papers at Medium, High and Max, scored on the 147 audit corrections); no independent extraction benchmark found |
| Alt text from screenshots | GPT-6.2 Sol vision (Medium) | reads each image; replaces Gemini 4 Argon |
| Writing, judging, tie-breaks, spot checks | **Claude Opus 5.5** ($4 and $20; batch $2 and $10) | fallbacks to compare: Fable 5.2, GPT 6.2 Sol |
| QA of PICOST extractions | Liquid d1-ultra decision model | **on hold (JP, 2026-11-24); remind JP after the first new batch**; Opus 5.5 on parser disagreements plus a 10% sample meanwhile |
| Unattended runs | **Batch APIs** (Anthropic, OpenAI) | about half price; cached Skill instructions; standard API only for pilots |
| EVD candidate voting | GPT-6.2 Sol (Medium) + Inkling 2 Small on Tinker | JP loaded USD 50 on Tinker (2026-11-24); Inkling 2 Small is JP's Inkling model of choice; listed at about USD 0.30 in and 1.00 out per million tokens on third-party sites (confirm on Tinker's pricing page); the Tinker key is in `.env` |
| Embeddings, deduplication, linking | tabled | not needed at 77 EVDs from 27 papers |

Open: Anthropic and OpenAI API keys are not set (Google dropped: no key available) in `~/.config/lives-ai-raters/.env` (only Perplexity, Liquid and Jev are).

## Planned toolchain (decided by JP, 2026-11-20)

> [!todo] Not yet in `Skill.md`
> `Skill.md` and the related Skill files still describe the old tools. Updating them is on the TODO list (`pipeline/misc/evd-validation/TODO.md`, item 0e).

1. **OCR and extraction: two OCR models must agree (JP, 2026-11-20).** Run **Chandra OCR 2** and **OXR-1.0** on every PDF and accept text, numbers and table cells only where they agree. For born-digital PDFs, the PDF's own text layer (PyMuPDF) is a third vote that settles most disagreements for free. Where the two still disagree, or on scanned pages with no text layer, the page image decides (Claude Opus 5.5 or a human looks at it). Add a third local OCR model (Granite-Docling) only if the pilot shows many unresolved disagreements.
   - **Chandra OCR 2** (Datalab, US; base model to check).
   - **OXR-1.0**: ranked first on the OmniDocBench v1.6 end-to-end table (overall 97.03; 1.3B parameters) as of 2026-11-20 (https://github.com/opendatalab/OmniDocBench). The page does not name its developer or licence. **Exception to the model-origin policy (JP, 2026-11-20): OXR-1.0 may come from any country, as long as it is open and runs locally.** Still check that its licence allows research use and that its weights are downloadable.
   - Dropped under the model-origin policy: GLM-OCR (Zhipu), PaddleOCR-VL-1.6 (Baidu), LightOnOCR-3-4B (LightOn, France). olmOCR 2 is no longer in the plan.
2. **Fallbacks.** If those tools fail on a paper, use other tools.
3. **Highlights and screenshots.** Once the OCR models agree on the text and tables, use **PyMuPDF** and **`pdftoppm`** to locate the agreed quotes, highlight them and take the screenshots. The screenshot pipeline needs exact word coordinates, which these two provide for born-digital PDFs.
4. **Writing the nodes.** Claude Opus 5.5 works from the extractions and the Skill files to write the EVDs and fill in the SRC, QUE, EVD, CLM, CVT and other discourse-graph `.md` files.
5. **Quality signals (optional, later).** JP may run **Pangram 4.1** to detect AI-generated text and images and plagiarism, alone or with Claude's help. It could become part of a later-stage Quality Signals check pipeline. The existing `pipeline/misc/scripts/pangram_check.py` calls `pangram-4` and checks text only; it would need updating for 4.1 and images.

### Model ensembles: 2-3 open models for each closed model (JP, 2026-11-20)

Every step that uses a closed model also runs open models, and their outputs are combined by majority vote with an **odd number of voters** (3 for the Skill steps), so votes cannot tie. This gives a cross-check, keeps the pipeline running if a closed API changes or is unavailable, and keeps costs down.

| Step | Closed model | Open models to contrast | How votes are combined |
|---|---|---|---|
| OCR and extraction | none (LlamaParse kept only as a fallback) | **Chandra OCR 2 + OXR-1.0** (OXR-1.0 exempt from the origin policy: open and local), plus the PDF text layer as a third vote | Accepted where they agree; the text layer settles born-digital disagreements; otherwise the page image decides |
| Skill steps: extracting, writing, judging, linking | **Claude Opus 5.5** | **Inkling 2 Mini + Gemma 4** for the first extraction pass, both run locally (JP, 2026-11-20). Backups via hosted APIs, if local speed or quality falls short: Ripple-65B Preview and Reflection Beam | **Extracting:** Inkling 2 Mini and Gemma 4 extract; a value is accepted when they agree exactly. **Claude Opus 5.5 breaks ties, and does all writing and judging**, with effort set to each task's demands (low for simple pass/fail checks, higher for nuanced judgments; tune on the test set). Linking: EmbeddingGemma 4 finds candidates, Opus 5.5 decides |
| Contrast for the Skill steps' closed role (optional, JP, 2026-11-20) | Claude Opus 5.5 vs **Gemini 4 Neon** (Google) and **GPT-6.2 Sol** (OpenAI) | none (closed models, hosted APIs) | Run on the fixed test set only, at matched effort, not as extra voters. Compare agreement with JP, verbatim quotes, number correctness and cost per paper from usage logs. To verify before use: version, official pricing (Neon's "slightly higher score, about 40% cheaper at x-high" and Sol's $2 / $10 per million tokens are unverified), data-storage region. Both US developers, so they pass the origin policy |
| Fast decisions (relevancy, pass/fail) | Google Decision 1 (optional cross-check only) | **Perplexity Decider 1.3** (open, runs locally; preferred, JP 2026-11-20; base model to check) | Perplexity Decider 1.3 decides; disagreements with Opus 5.5 or the human reviewer are logged |
| Embeddings | none | **EmbeddingGemma 4** (open, local; JP 2026-11-20) for deduplication, linking related nodes, screening and similar tasks | n/a |
| AI-writing and plagiarism checks | **Pangram 4.1** (closed API; acceptable, JP 2026-11-20) | none needed | n/a |

> [!important] Model-origin policy: US models only (JP, 2026-11-20)
> Use the best open and closed models from **US developers**. This replaced an earlier rule the same day (North American and European models, no Chinese models). Dropped: Kimi K3.1 Pro (Moonshot), DeepSeek, GLM and GLM-OCR (Zhipu), Qwen (Alibaba), Tencent Hy and PaddleOCR-VL (Baidu); then Mistral Large 3, Mistral OCR 3 and LightOnOCR (France) and EuroLLM.
> - **Check each model's base model too.** Some US open models are fine-tuned from Chinese base models. (As far as Claude knows, olmOCR was fine-tuned from a Qwen model, which is why it left the plan.) Check Chandra OCR 2, OXR-1.0, Ripple-65B Preview, Inkling 2 Mini and Perplexity Decider 1.3 before adopting them. Claude has treated a Chinese base model as failing the policy; JP to confirm.
> - Record each model's developer, base model, licence and where it runs in the model registry (implementation notes below).

> [!note] Models for each role (JP, 2026-11-20)
> | Role | Model | Open or closed | Runs |
> |---|---|---|---|
> | Writing, judging, breaking ties | **Claude Opus 5.5** (Anthropic) | Closed | API |
> | First extraction pass | **Inkling 2 Mini** (Thinking Machines Lab) and **Gemma 4** (Google) | Open | Locally on JP's Framework PC |
> | Extraction backups (only if needed later, for speed or quality) | **Ripple-65B Preview** (Ricursive Intelligence) and **Reflection Beam** (Reflection AI) | Open | Called through hosted APIs (Beam is too large to run locally; JP, 2026-11-20) |
> | OCR | **Chandra OCR 2** (Datalab) and **OXR-1.0**, plus the PDF text layer | Open | Locally |
> | Fast decisions | **Perplexity Decider 1.3** | Open | Locally |
> | Embeddings (deduplication, linking, screening) | **EmbeddingGemma 4** (Google) | Open | Locally |
> | AI-writing and plagiarism checks | **Pangram 4.1** | Closed | API |
>
> Set aside: OpenAI gpt-oss and Olmo 3 (JP, 2026-11-20). Gemma 4 is back as a local extractor (2026-11-20). Not in Roam yet and to check before use: Ripple-65B Preview, Reflection Beam, OXR-1.0, and Gemma 4's licence (earlier Gemma models used Google's own Gemma terms, not Apache 2.0). Under the model-origin policy, check the developer and base model of Chandra OCR 2, Inkling 2 Mini, Gemma 4, Perplexity Decider 1.3, Ripple-65B Preview and Reflection Beam (OXR-1.0 is exempt as long as it is open and local).
>
> **Ripple-65B Preview** (backup, via a hosted API; checked 2026-11-20 at https://www.ricursive.com/ripple and https://huggingface.co/ricursiveAI/Ripple-65B-Preview): developer Ricursive Intelligence, Inc. (country not stated on either page; confirm it is a US company). **Dense** 65B model (all 65B parameters active), **Apache 2.0** licence, **trained from scratch** (not fine-tuned from another model, so it passes the base-model check) on 12 trillion tokens of mostly English text and code; text only, no image input; context up to about 1 million tokens. Released 2026-11-19 as a preview with "relatively light" post-training focused on agentic coding. No document-extraction benchmarks are published, so its extraction quality must be measured on the test set. Official files: BF16 (instruction-tuned and base) and NVFP4.
>
> **Hardware (JP): a Framework PC with an AMD Ryzen chip and 128 GB of RAM.** Claude assumes this is the Framework Desktop (Ryzen AI Max+ 395, 128 GB unified memory shared with the built-in GPU). For Ripple-65B Preview:
> - The official **BF16** files need about 130 GB, so they do **not** fit.
> - The official **NVFP4** files are a 4-bit format for NVIDIA's newest GPUs; AMD chips cannot run them efficiently.
> - Use a community **GGUF** build instead (the Hugging Face page lists 48 quantized variants, not yet checked): at 4-bit about 40 GB, at 8-bit about 70 GB, run with llama.cpp (Vulkan or ROCm), Ollama or LM Studio. That leaves room for Inkling 2 Mini (about 20 GB) and the OCR models.
> - Because the model is dense, expect only a few tokens per second at 4-bit on this machine: fine for short JSON extractions run as a batch, slow for long outputs.
>
> **Reflection Beam** (backup, via a hosted API or institutional GPUs; checked 2026-11-20 at https://reflection.ai/blog/introducing-beam and https://reflection.ai/beam-model-card): developer Reflection AI (described as a US lab by third-party sources; confirm). Mixture-of-experts, 501B parameters in total with about 23B used per token; Apache 2.0 licence (training data not released); trained from scratch, as far as the pages show; text only; context about 1 million tokens; weights released October 2026 in BF16 (about 934 GiB), FP8 (about 469 GiB) and NVFP4 (about 273 GiB); no GGUF build listed. It does **not** fit JP's 128 GB machine (reported to need about 4 NVIDIA B300 GPUs in its smallest format). Self-reported scores are somewhat higher than Ripple-65B's (SWE-bench Verified 81.6 vs 76.5; GPQA Diamond 90.6 vs 85.2; long context AA-LCR 78.2 vs 75.0; Terminal-Bench and IFBench about equal). No extraction benchmarks published.

### Pipeline requirements (added 2026-11-20)

The aim is a pipeline that is highly accurate, cost-effective, scales to larger corpora, is reproducible and reliable, and is usable by other labs in other countries. As of 2026-11-20 it is a plan, not yet that pipeline. To get there, in priority order:

1. **Measure before scaling.** Build a fixed test set from what is already validated: JP's EVD judgments, the 147 PDF-audit corrections and the version comparisons. Set a pass bar per stage (for example every quote verbatim, every number correct, agreement with JP of kappa 0.6 or higher) and re-run the test set whenever a model, prompt or Skill changes.
2. **Use the PDF text layer as a vote, and escalate.** Born-digital text from PyMuPDF is already exact. Run one OCR model by default and the others only on tables, scanned pages, or where the first disagrees with the text layer. This saves roughly two thirds of the OCR compute.
3. **Make it a fixed pipeline, not an improvised agent session.** One script: OCR, agreement check, crops and screenshots, draft, automatic checks, human review. Claude and the other models work only at the drafting and judging steps. Save each step's output so a failed batch can resume. Put paths in a config file (the current scripts hard-code `/Users/ppatel/...`, are duplicated in `pipeline/scripts/` and `pipeline/misc/scripts/`, and one imports a missing `quote_pipeline_v3`).
4. **Record everything needed to rerun it.** For each run, a manifest of model names, versions and dates, the weight hashes of open models, every prompt (in version control), temperature and other settings, and the raw outputs. Run the open models in a container.
5. **Keep every model step swappable.** The ensemble table above, plus the benchmark, lets an open model replace a closed one without changing the pipeline.
6. **Check cross-country use:** each model's licence, where each API stores data (for example GDPR), the copyright rules for published screenshots, and a small test on non-English papers.
7. **Package it:** a short README with a sample paper, one command to run it, and the human-review step in the LIVES app rather than a spreadsheet.

### Status check against the six criteria (2026-11-20, after the Kimi K3.1 Pro swap)

| Criterion | First check (before the plan) | Now, with the current plan | What would make it pass |
|---|---|---|---|
| Accurate | Unknown; number errors on 57 of 77 pages; Claude-JP kappa 0.31 (relevancy), 0.13 (Fidelity) | **Still unknown, better on paper.** OCR agreement plus the text-layer vote targets the table and number errors; the 3-voter majority helps only if the models make different mistakes; selection and judgment errors still need human review | Test set built; every stage meets its pass bar; correlated errors measured (as in Benchmark Summary Table 5) |
| Reproducible | Weak | **Partly addressed.** Two of three Skill voters, all OCR candidates and the embeddings are open and can be pinned by version and weight hash; prompts are now saved in the vault. Opus 5.5 is still closed and can change. No run manifest or containers yet | Run manifest, containers and pinned versions; a rerun of the open models gives identical output |
| Stable and reliable | Weak | **Unchanged until built**, and the ensemble adds moving parts (several OCR models, three voters, local and hosted setups). Scripts are still duplicated with hard-coded paths | One resumable script with a config file, tested end to end on a sample paper, with retries and timeouts |
| Cost-effective at scale | Unclear | **Good on paper.** Local OCR, embeddings and Inkling 2 Mini; escalation; caching; Batch API (roughly $17 for 50 papers in an illustrative estimate). Kimi K3.1 Pro needs a paid hosted API or GPUs | Measured cost per paper and per step from the usage logs |
| Usable across countries | Not yet | **Improved.** With an open majority, a lab can self-host without US APIs. Not yet checked: licences (Kimi, Inkling, the OCR models, GLM-OCR), where hosted APIs store data (some institutions restrict sending data to US or China-based APIs; self-hosting avoids this), screenshot copyright, non-English papers | Each check done and recorded on this page |
| User-friendly | Only for JP | **Unchanged**; more tools mean a steeper setup | README, one-command run, sample paper, review step in the LIVES app |

**Overall:** the plan now addresses each criterion, but none passes yet, because nothing has been built or measured. The next step is the test set and a pilot on a few papers.

> [!note] Models changed after this check
> Later on 2026-11-20 the model choices changed: Kimi K3.1 Pro left (model-origin policy), the extraction pair became Inkling 2 Mini and Ripple-65B Preview, and the OCR pair became Chandra OCR 2 and OXR-1.0. The judgments above still hold; the licence and data-storage checks now apply to the new list.

## Implementation notes: making it pass (JP, 2026-11-20)

Steps to build, grouped by the criterion they serve. To analyse next week with TODO 0e and 0h, then build (TODO 0i).

### Reproducible

- **Pin every version.** Open models: name, version, release date, weight file hash (sha256), quantization. Python packages: an exact lock file (`requirements.lock` or `uv.lock`), e.g. PyMuPDF 1.27.2.3. System tools: the poppler version.
- **Container.** A Dockerfile (plus an Apptainer recipe for university clusters, which often don't allow Docker) holding the local models and tools. Publish the image with a version tag.
- **Run manifest.** One JSON file per run: config, model IDs and versions, prompt and Skill file hashes, settings (effort, temperature for open models), sha256 of every input PDF, output paths, start and end times, and token counts and cost.
- **Prompts and Skill files in git**, with a tag per release; every EVD records the prompt version and the model that produced it.
- **Fix what can be fixed.** Temperature 0 and fixed seeds for open models. Claude Opus 5.5 does not accept temperature settings, so its outputs can differ between runs: save them and rely on the manifest.
- **Keep raw outputs**: each OCR model's text, every vote and every draft, not only the final result.
- **Regression run.** Re-run the test set automatically whenever a model, prompt or Skill file changes, and compare with the last release.

### Stable and reliable

- **One package with one command** (for example `lives-pipeline run --config config.yaml`), replacing the duplicated `pipeline/scripts/` and `pipeline/misc/scripts/`. No hard-coded paths; everything in the config file.
- **Resumable steps.** Each step writes `runs/<run_id>/<paper>/<step>.json` and is skipped if that file exists, so a failed run resumes where it stopped.
- **Fail per paper, not per run.** Retries with back-off, timeouts and rate-limit handling; one bad PDF is logged and skipped, not fatal.
- **Validate every model output** against a JSON schema; reject and retry, or flag for review.
- **Automatic checks after each paper:** quotes verbatim against the PDF (fix the dash-normalisation bug first), numbers against the text layer, screenshots present, links resolve.
- **Tests:** unit tests, plus an end-to-end run on three sample papers: one born-digital, one scanned, one two-column paper with dense tables.
- **Clean up known breakages:** the missing `quote_pipeline_v3` module, and the stale Zhang & Abernethy filename in `keyword_freq_check.py` and `pangram_check.py`.

### Cost-effective at scale, including in low- and middle-income countries

- **An open-only mode.** The whole pipeline must run without any paid API, on one consumer GPU or a 32 GB laptop; Claude Opus 5.5 is an optional upgrade switched on in the config. Then no lab is locked out by API prices, payment methods or currency.
- **Hardware tiers, documented with measured time and cost per paper:** (1) CPU only: PyMuPDF text layer and screenshots, smallest models; (2) laptop with 16-32 GB RAM: quantized Inkling 2 Mini and small OCR models; (3) one GPU: the full open ensemble; (4) cloud or API: optional.
- **Quantized models** (4-bit or GGUF) so the open models fit small machines.
- **The cost levers in TODO 0h:** Methods and Results sections first, cheap models extract, Opus 5.5 only on disagreement and for writing and judging, effort per task, caching, Batch API, short JSON outputs, pilot first, resume instead of rerun.
- **Offline after setup.** One download of the models (list their sizes in the README), then no internet needed, which matters where bandwidth is limited or expensive.
- **Share extraction outputs** for open-access papers, so other labs don't pay to re-run OCR and extraction on the same papers.

### Usable across countries

- **Model registry.** A table of every model: developer, country, licence, base model, where it runs (local or which API and region), and the date checked. Applies the model-origin policy above.
- **Licences.** Prefer permissive open licences (Apache 2.0, MIT). Check for restrictions by country or use (some model licences have excluded certain regions or commercial use).
- **Data protection.** Process locally by default. When an API is used, record where data is processed (Anthropic: US; check each API) and the relevant laws (for example GDPR in the EU). Don't send non-public PDFs to an API without permission.
- **Copyright.** Screenshots of figures and tables from openly licensed papers (for example CC BY) can be published with attribution; for others, keep screenshots private or link to the source instead. Fair use and fair dealing differ by country.
- **Languages.** Test on non-English papers; Claude Opus 5.5 and the extraction models are to be checked on non-English text; check each on the test set. Translate the README later if other labs ask.
- **Neutral formats.** ISO dates (YYYY-MM-DD), UTF-8 text, plain Markdown and JSON outputs.

### Documentation and packaging (user-friendly)

Files to add to the pipeline repository:

| File | Contents |
|---|---|
| `README.md` | What the pipeline does; quick start (install, then one command on the sample paper); hardware tiers; config; outputs; the human-review step; troubleshooting |
| `config.example.yaml` | Every setting with a comment; open-only mode as the default |
| `.env.example` | API key names only (never real keys); keys stay out of git |
| `LICENSE` | A code licence (for example Apache 2.0 or MIT) and a content licence for the EVDs (for example CC BY 4.0); JP to choose |
| `CITATION.cff` | How to cite the pipeline and the vault |
| `CHANGELOG.md` | What changed in each release, including model and prompt changes |
| `CONTRIBUTING.md` | How other labs add papers, models or fixes |
| `MODELS.md` | The model registry (above) |
| `sample_data/` | One or two openly licensed PDFs, with expected outputs, for testing a new install |
| `docs/` | Method details; links to `Skill.md` and this page |

Pushing these to the GitHub repository needs JP's approval.

> [!important] Keep human review at the end
> This week's checks showed that human review catches the selection, wording and judgment errors that model agreement does not. Make the review faster; do not remove it.

### For later

- **GROBID, for reference checks in the Quality Signals pipeline.** GROBID parses each PDF's reference list (and header and section structure) into structured TEI XML. That is what a reference check needs: matching citations to references, resolving DOIs, and flagging missing, wrong or retracted references. It is not needed for OCR or node writing, because source metadata comes from Zotero.
- **EmbeddingGemma 4, for deduplication, screening and linking** (JP, 2026-11-20; Roam notes record EmbeddingGemma 2, 740M parameters, text, image and code embeddings; confirm the version). Local, free and open. Planned uses:
  - finding duplicate or near-duplicate EVDs, CLMs and other nodes (it would replace the keyword-overlap score in `pipeline/misc/scripts/find_redundancies.py`);
  - screening papers found by the AI-assisted search;
  - suggesting links between nodes (EVD to CLM, EVD to QUE, EVD to EVD).

> [!tip] Embeddings and Claude Opus 5.5 do different jobs
> Use EmbeddingGemma to **find candidates** (fast, free, scores every pair) and Claude Opus 5.5 to **decide** on each candidate (whether two EVDs are really the same finding, and which relation applies: supports, opposes, consistent with). A human confirms merges and links. The April redundancy audit (`pipeline/misc/redundancy_audit_2026-04-27.md`) can serve as a first test set for comparing the two.

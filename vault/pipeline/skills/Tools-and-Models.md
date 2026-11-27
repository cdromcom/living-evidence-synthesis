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
| Claude Sonnet 4.6 (Claude Code; Opus 4.7 only appears in a welcome banner, not as the model used) | Built the vault in April 2026 (correction 2026-11-24 from `Log.md`: banner reads "Sonnet 4.6", orchestrator messages are stamped `claude-sonnet-4-6`; the 2026-04-17 run created 52 EVD, 12 CLM and 45 CVT nodes; the model of the batch agents and of the roughly 22 earlier EVDs is not recorded): first extraction of QUE, EVD, CLM and CVT nodes, EVD rewrites, subagent batches | `Log.md`; `History.md` (`author: Claude (Opus 4.7 / Sonnet 4.6)`; the April notes were "Claude 4.7, per user recollection, only partly sure") |
| "Claude Sonnet 5" | Recorded as the curation model on 27 source pages | `curatedWithModel` in source frontmatter; convention in `Skill-references.md` |
| Claude Opus 5.5 (Claude Code) | All work from 2026-11-11 to 2026-11-20: EVD drafts, PDF number audit, Fidelity/Grounding grading, version comparisons | AI Prompt Log tab in the GSheet; `pipeline/misc/prompts/2026-11-11-evd-validation-gsheet-prompt-log.md` |
| Pangram `pangram-4` (API) | AI-writing detection on the source PDFs (text only) | `pipeline/scripts/pangram_check.py` |

Model names such as GPT-4 or o3-mini that appear in these files are models studied by the papers, not tools used here.

---

## v2 toolchain (decided by JP, 2026-11-24): hosted APIs, simpler

> [!important] Supersedes the local-model plan below
> JP chose hosted APIs over local models and a smaller toolchain. The 2026-11-20 plan below is kept for the record.

| Step | Tool or model | Notes |
|---|---|---|
| Read PDFs and bulk extraction | **Gemini 4 Neon** (Google; `gemini-4-neon`; PDF input; thinking level High; $3 in and $15 out per million tokens, batch about $1.50 and $7.50; third-party pages, confirm on Google's pricing page) | JP's decision 2026-11-25: primary reader and extractor again now that a paid Google key works; **GPT-6.2 Sol** (OpenAI; effort High; $2 and $10, batch $1 and $5) re-reads low-confidence and multi-page items independently; LlamaParse stays the fallback; page-by-page markdown, HTML tables, printed page numbers; $2 in and $10 out per million tokens, batch $1 and $5 (third-party pages; confirm on OpenAI's pricing page); requests over about 272K input tokens may be billed at a higher long-context rate; LlamaParse ($0.0375 per page) stays as the fallback |
| Second vote | PyMuPDF text layer | born-digital PDFs; the rendered page image decides disagreements |
| Crop and highlight | PyMuPDF word coordinates and `pdftoppm` | cross-checked against the parsed table cells; printed page numbers from the page map |
| Bulk extraction, question splitting and restyling, alt text, link repair | **GPT-6.2 Sol** (High for extraction; Medium for restyling, alt text, link repair) | Max only if a pilot shows it removes errors High leaves (5 papers at Medium, High and Max, scored on the 147 audit corrections); no independent extraction benchmark found |
| Alt text from screenshots | GPT-6.2 Sol vision (Medium) | reads each image; replaces Gemini 4 Argon |
| Writing nodes (EVD, QUE, CLM, CVT) by debate | **Claude Sonnet 5.5**, **GPT-6.2 Sol** and **Gemini 4 Neon (Medium thinking)** draft, critique and revise; **Sol and Sonnet vote**, Neon breaks ties; **Inkling 2 Small** votes for benchmarking only; **Claude Opus 5.5** ($4 and $20; batch $2 and $10) on escalation (JP, 2026-11-25) | Sonnet $2 and $10; Sol $2 and $10 (unverified); Neon $3 and $15 | fallbacks to compare: Opus 5.5 as sole author. Fable 5.2 is not used (JP, 2026-11-24: too costly) |
| QA of PICOST extractions | decision models (Liquid d1.2-ultra, Perplexity Decider 1.3): relevancy, fidelity, numbers-in-source, table and figure grounding | shadow mode until calibrated (JP, 2026-11-24); low-confidence and multi-page items go to GPT-6.2 Sol and Opus 5.5; Opus 5.5 also checks parser disagreements plus a 10% sample |
| Unattended runs | **Batch APIs** (Anthropic, OpenAI) | about half price; cached Skill instructions; standard API only for pilots |
| EVD candidate voting | GPT-6.2 Sol and Claude Sonnet 5.5 vote (Neon breaks ties) | JP dropped Inkling 2 Small on 2026-11-25 (not useful in the pilot) | |
| Embeddings, deduplication, linking | tabled | not needed at 77 EVDs from 27 papers |

Open: Anthropic and OpenAI API keys are not set (Google dropped: no key available) in `~/.config/lives-ai-raters/.env` (only Perplexity and Liquid are).

## Planned toolchain (decided by JP, 2026-11-20)

> [!todo] Not yet in `Skill.md`
> `Skill.md` and the related Skill files still describe the old tools. Updating them is on the TODO list (`pipeline/misc/evd-validation/TODO.md`, item 0e).

1. **OCR and extraction: two OCR models must agree (JP, 2026-11-20).** Run **Chandra OCR 2** and **OXR-1.0** on every PDF and accept text, numbers and table cells only where they agree. For born-digital PDFs, the PDF's own text layer (PyMuPDF) is a third vote that settles most disagreements for free. Where the two still disagree, or on scanned pages with no text layer, the page image decides (Claude Opus 5.5 or a human looks at it). Add a third local OCR model (Granite-Docling) only if the pilot shows many unresolved disagreements.
   - **Chandra OCR 2** (Datalab, US; base model to check).
   - **OXR-1.0**: ranked first on the OmniDocBench v1.6 end-to-end table (overall 97.03; 1.3B parameters) as of 2026-11-20 (https://github.com/opendatalab/OmniDocBench). The page does not name its developer or licence. **OXR-1.0 may come from any country, as long as it is open and runs locally (JP, 2026-11-20); since 2026-11-25 this is the general rule for open-weight models.** Still check that its licence allows research use and that its weights are downloadable.
   - Dropped on 2026-11-20 under the earlier US-only policy: GLM-OCR (Zhipu), PaddleOCR-VL-1.6 (Baidu), LightOnOCR-3-4B (LightOn, France). **Since 2026-11-25 these are eligible again** if they are near the state of the art for OCR and run locally; they are not back in the plan until tested. olmOCR 2 is no longer in the plan.
2. **Fallbacks.** If those tools fail on a paper, use other tools.
3. **Highlights and screenshots.** Once the OCR models agree on the text and tables, use **PyMuPDF** and **`pdftoppm`** to locate the agreed quotes, highlight them and take the screenshots. The screenshot pipeline needs exact word coordinates, which these two provide for born-digital PDFs.
4. **Writing the nodes.** Sonnet 5.5, Sol and Neon (Medium) draft the primary EVDs from the checked extractions (Sonnet 5.5 alone drafts everything else) and the Skill files, critique one another and revise (two rounds at most); Sol and Sonnet vote, Neon breaks ties; the cheaper of Sol and Sonnet checks the claims; Opus 5.5 only on escalation. Same loop for EVD, QUE, CLM and CVT (`Skill-controls.md`, "Drafting by debate").
5. **Quality signals (optional, later).** JP may run **Pangram 4.1** to detect AI-generated text and images and plagiarism, alone or with Claude's help. It could become part of a later-stage Quality Signals check pipeline. The existing `pipeline/scripts/pangram_check.py` calls `pangram-4` and checks text only; it would need updating for 4.1 and images.

### Model ensembles: 2-3 open models for each closed model (JP, 2026-11-20)

Every step that uses a closed model also runs open models, and their outputs are combined by majority vote with an **odd number of voters** (3 for the Skill steps), so votes cannot tie. This gives a cross-check, keeps the pipeline running if a closed API changes or is unavailable, and keeps costs down.

| Step | Closed model | Open models to contrast | How votes are combined |
|---|---|---|---|
| OCR and extraction | none (LlamaParse kept only as a fallback) | **Chandra OCR 2 + OXR-1.0** (OXR-1.0 exempt from the origin policy: open and local), plus the PDF text layer as a third vote | Accepted where they agree; the text layer settles born-digital disagreements; otherwise the page image decides |
| Skill steps: extracting, writing, judging, linking | **Claude Opus 5.5** | **Inkling 2 Mini + Gemma 4** for the first extraction pass, both run locally (JP, 2026-11-20). Backups via hosted APIs, if local speed or quality falls short: Ripple-65B Preview and Reflection Beam | **Extracting:** Inkling 2 Mini and Gemma 4 extract; a value is accepted when they agree exactly. **Claude Opus 5.5 breaks ties, and does all writing and judging**, with effort set to each task's demands (low for simple pass/fail checks, higher for nuanced judgments; tune on the test set). Linking: EmbeddingGemma 2 finds candidates, Claude Opus 5.5 decides |
| Contrast for the Skill steps' closed role (optional, JP, 2026-11-20) | Claude Opus 5.5 vs **Gemini 4 Neon** (Google) and **GPT-6.2 Sol** (OpenAI) | none (closed models, hosted APIs) | Run on the fixed test set only, at matched effort, not as extra voters. Compare agreement with JP, verbatim quotes, number correctness and cost per paper from usage logs. To verify before use: version, official pricing (Neon's "slightly higher score, about 40% cheaper at x-high" and Sol's $2 / $10 per million tokens are unverified), data-storage region. Both US developers, so they pass the origin policy. Neon is parked (JP, 2026-11-25): the Google billing setup did not work |
| Fast decisions (relevancy, pass/fail) | Google Decision 1 (optional cross-check only) | **Perplexity Decider 1.3** (open, runs locally; preferred, JP 2026-11-20; base model to check) | Perplexity Decider 1.3 decides; disagreements with Claude Opus 5.5 or the human reviewer are logged |
| Embeddings | none | **EmbeddingGemma 2** (open, local; JP 2026-11-20) for deduplication, linking related nodes, screening and similar tasks | n/a |
| AI-writing and plagiarism checks | **Pangram 4.1** (closed API; acceptable, JP 2026-11-20) | none needed | n/a |

> [!important] Model-origin policy (JP, 2026-11-25; replaces "US models only" of 2026-11-20)
> - **Hosted APIs: US developers only.** Never send data to a foreign provider's API or hosted endpoint (closed or open model alike). Third-party hosting of an open model counts as an API.
> - **Open-weight models from any country are allowed if they run locally** (on JP's computer or the lab's own environment) **and are state of the art or close to it for the task.** Check that the licence allows research use, and record developer, country, base model, licence and the date checked in the model registry.
> - **History.** On 2026-11-20 the rule was first "North American and European models, no Chinese models" and then "US developers only"; that dropped Kimi K3.1 Pro (Moonshot), DeepSeek, GLM and GLM-OCR (Zhipu), Qwen (Alibaba), Tencent Hy and PaddleOCR-VL (Baidu), Mistral Large 3, Mistral OCR 3, LightOnOCR (France) and EuroLLM. Those are **eligible again as local open-weight models** if they are near the state of the art; none is back in the plan automatically, and a hosted API for any of them stays excluded.
> - **Still record each model's base model.** A US model fine-tuned from a foreign open base is fine when run locally; the registry should say what the base is (olmOCR, for example, was fine-tuned from a Qwen model). This is for transparency and licence checks, not a ban. Check the licence and developer of Chandra OCR 2, OXR-1.0, Ripple-65B Preview, Inkling 2 Mini and Perplexity Decider 1.3 before adopting them.
> - **Check "near state of the art" against a named benchmark** (for example the MTEB leaderboard for embeddings, OmniDocBench for OCR) and write the rank and date next to the model.
> - Record each model's developer, base model, licence and where it runs in the model registry (implementation notes below).

> [!note] Decision 2026-11-25 (JP): no local extraction stack
> Frontier hosted models do the reading and extraction (Gemini 4 Neon, GPT-6.2 Sol, Claude Opus 5.5), checked by PyMuPDF and the decision models. The local models listed below (Chandra OCR 2, OXR-1.0, Inkling 2 Mini, Gemma 4 and the backups) are **not planned**: they were never installed and may not reach the needed accuracy. Accuracy comes first. Inkling 2 Small on Tinker stays for picking between EVD drafts and merge judgments, run in parallel because it has no batch mode. Batch calls go through `pipeline/scripts/llm_batch.py` (Anthropic Message Batches, OpenAI Batch, Gemini Batch).

> [!note] Models for each role (JP, 2026-11-20)
> | Role | Model | Open or closed | Runs |
> |---|---|---|---|
> | Reading, extracting, drafting | **Gemini 4 Neon** (Google) | Closed | API |
> | Adjudicating, demanding judgments, EVD node-detail check | **Claude Opus 5.5** (Anthropic) | Closed | API |
> | First extraction pass | **Inkling 2 Mini** (Thinking Machines Lab) and **Gemma 4** (Google) | Open | Locally on JP's Framework PC |
> | Extraction backups (only if needed later, for speed or quality) | **Ripple-65B Preview** (Ricursive Intelligence) and **Reflection Beam** (Reflection AI) | Open | Called through hosted APIs (Beam is too large to run locally; JP, 2026-11-20) |
> | OCR | **Chandra OCR 2** (Datalab) and **OXR-1.0**, plus the PDF text layer | Open | Locally |
> | Fast decisions | **Perplexity Decider 1.3** | Open | Locally |
> | Embeddings (deduplication, linking, screening) | **EmbeddingGemma 2** (Google) | Open | Locally |
> | AI-writing and plagiarism checks | **Pangram 4.1** | Closed | API |
>
> Set aside: OpenAI gpt-oss and Olmo 3 (JP, 2026-11-20). Gemma 4 is back as a local extractor (2026-11-20). Not in Roam yet and to check before use: Ripple-65B Preview, Reflection Beam, OXR-1.0, and Gemma 4's licence (earlier Gemma models used Google's own Gemma terms, not Apache 2.0). Under the model-origin policy, check the developer, licence and base model of Chandra OCR 2, Inkling 2 Mini, Gemma 4, Perplexity Decider 1.3, Ripple-65B Preview and Reflection Beam; open-weight models from any country are fine if local and near-SOTA (policy of 2026-11-25).
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
> Later on 2026-11-20 the model choices changed: Kimi K3.1 Pro left (the US-only policy of that day; since 2026-11-25 it would be eligible again as a local open-weight model, if it is near the state of the art and can run locally), the extraction pair became Inkling 2 Mini and Ripple-65B Preview, and the OCR pair became Chandra OCR 2 and OXR-1.0. The judgments above still hold; the licence and data-storage checks now apply to the new list.

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
- **EmbeddingGemma 2, for deduplication, screening and linking** (JP, 2026-11-20; version 2 confirmed by JP 2026-11-25; released 2026-10-06 under Apache 2.0; reports describe about 740M parameters and text, image, audio and code embeddings; Google's model card is the source to check). Local, free and open. **Downloaded 2026-11-25** (Hugging Face `google/embeddinggemma-2`, 1.4 GB, runs via sentence-transformers in `~/.cache/lives-bench/venv-embed`; the installed Ollama is too old to pull it). Planned uses:
  - finding duplicate or near-duplicate EVDs, CLMs and other nodes (it would replace the keyword-overlap score in `pipeline/misc/scripts/find_redundancies.py`);
  - screening papers found by the AI-assisted search;
  - suggesting links between nodes (EVD to CLM, EVD to QUE, EVD to EVD).

> [!tip] Embeddings and Claude Opus 5.5 do different jobs
> Use EmbeddingGemma 2 to **find candidates** (fast, free, scores every pair) and, since JP's 2026-11-25 decision, **Inkling 2 Small plus Claude Sonnet 5.5, which must agree**, to decide on each candidate (Claude Opus 5.5 only if they disagree and JP asks) (whether two EVDs are really the same finding, and which relation applies: supports, opposes, consistent with). A human confirms merges and links. The April redundancy audit (`pipeline/misc/redundancy_audit_2026-04-27.md`) can serve as a first test set for comparing the two.


> Dropped 2026-11-25 (JP): Inkling is no longer used anywhere in the pipeline. The next section is kept as a record.

## Inkling on Tinker: prices and model card (read 2026-11-25; partly unverified)
- **Source:** Tinker's models and pricing page (tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/). The page was truncated for the reader, so the Inkling rows below came from a model-extracted summary and are **not verified**; confirm on the page before spending.
- **Inkling 2 Small** (64K context): prefill $0.30, cached prefill $0.03, sample $1.00, **train $1.50** per million tokens; the 256K row trains at $3.00.
- **Inkling 2 Mini** (64K): prefill $0.15, sample $0.50, **train $0.75**; 256K trains at $1.50; the page also lists a free row with rate limits.
- **Inkling (largest):** train $5.61 at 64K, $11.23 at 256K.
- **Model card** (thinkingmachines.ai/model-card/inkling/, the 975B Inkling only; the Small and Mini cards were not read): Apache 2.0, open weights on Hugging Face, 975B total and 41B active parameters, 1M context, text, image and audio in, text out, released 2026-07-15 by Thinking Machines Lab. No base model is named and training from scratch is not stated, so the model-origin policy check for Small and Mini is still open. Limitations listed: hallucination, instruction-following errors, weaker long multi-turn use; not for medical, legal or safety-critical use without extra work.
- **Rough budget:** at $1.50 per million training tokens, 1,000 examples of 800 tokens for 3 epochs is about 2.4M tokens, about $3.60. $50 of credit therefore pays for many small runs.

## Statistical accuracy checks (scripts; added 2026-11-25)
- **Where:** `pipeline/scripts/stat_checks.py` and `stat_checks_more.py`; run `python3 stat_checks.py` (all papers), `--only @citekey`, `selftest`, or `grim <mean> <n>`. Output: `pipeline/misc/evd-validation/stat-checks/`. Needs PyMuPDF and scipy.
- **Checks:** PERCENT sums, GRIM, GRIMMER, SAMPLE size agreement, ANALYTIC (full minus exclusions), SCALE (mean in range, percentage metric not above 100%), INTERVAL (estimate inside its CI), RATIO (a of b), METRIC (F1, kappa), EFFECT (impossible or outlying effect sizes), PROP (accuracy times N whole), CIP (p against CI), MONO (pass@k order, text and tables), DELTA (from a to b arithmetic), SDBOUND, STATCHECK (p from t, F, chi-square, z, r), CONFUSION (counts), MACRO (average rows).
- **Source ideas:** GRIM, GRIMMER, DEBIT, SPRITE and statcheck are documented in the metascience literature; [STRAIT](https://github.com/ianhussey/strait) and [Statlint](https://statlint.com/) do similar bound checks. RIVETS is named in a Springer Nature post citing Brown and Heathers (2019) with no method details found; STALT could not be found. Neither is implemented.
- **Limits:** all are clues for a person, not verdicts; they read the PDF text layer, so numbers in images are missed; table checks depend on the PDF keeping rows on single lines. On the 27 seed papers they flagged only three estimates outside their own confidence intervals (Roberts 2023 abstract).

## Local embedding and merge tooling (added 2026-11-25)
- **Embeddings:** EmbeddingGemma 2, weights in `~/.cache/lives-bench/models/embeddinggemma-2/`, run with `~/.cache/lives-bench/venv-embed/bin/python` (transformers 5.24.1, sentence-transformers 6.3.0, torch 2.15.0). `pipeline/scripts/embed_candidates.py` lists same-type candidate pairs with difference hints.
- **Second opinion:** `pipeline/scripts/merge_judge.py` with `pipeline/prompts/merge-judge-v1.md` (Claude Sonnet 5.5, effort medium; 35 calls cost about $0.12). Inkling 2 Small is wired up as a second judge (`merge_judge.py --inkling`, via `call_logger.logged_tinker`, Tinker's OpenAI-compatible endpoint, model id `thinkingmachines/Inkling-2-Small`, 90 pairs cost about $0.05). First result: Inkling over-groups (89 of 90 "group under an umbrella"); Sonnet 5.5 was more discriminating. A human verifies every merge.

## Embedding model choice: the MTEB leaderboard (checked 2026-11-25)
- **Leaderboard** (huggingface.co/spaces/mteb/leaderboard, Multilingual benchmark, 178 models): top model per size group was `harrier-oss-v1-27b` (more than 5B parameters), `Qwen3-Embedding-4B` (1 to 5B), `harrier-oss-v1-0.6b` (500M to 1B) and `harrier-oss-v1-270m` (under 500M). Retrieval-only (RTEB Multilingual) leaders were `Qwen3-Embedding-8B` and `F2LLM-v2-4B`.
- **Not downloaded:** `harrier-oss-v1-27b` (Microsoft, MIT): 54 GB of weights; this Mac has 41 GB free disk and 24 GB RAM. It would need a larger machine (a hosted endpoint is not allowed for a US model run by a foreign provider, nor for any foreign provider). Qwen3-Embedding (Alibaba) is allowed under the 2026-11-25 policy as a local open-weight model; the 4B and 8B versions would fit this Mac's disk and are candidates for the bake-off.
- **Downloaded 2026-11-25:** `microsoft/harrier-oss-v1-0.6b` (MIT, 596M parameters, 1.1 GB) in `~/.cache/lives-bench/models/harrier-oss-v1-0.6b/`, run with the same environment as EmbeddingGemma 2 (`~/.cache/lives-bench/venv-embed`). Use `prompt_name="sts_query"` for similarity between nodes.
- **First comparison with EmbeddingGemma 2 on our node titles:** JP's one labeled merge pair (the two LLM-versus-human review questions) ranks 3rd of 351 question pairs under harrier-0.6b and 9th under EmbeddingGemma 2; both models make the pair mutual nearest neighbors. Spread of similarity scores (95th minus 50th percentile): questions 0.061 harrier vs 0.085 EmbeddingGemma; caveats 0.072 vs 0.064; claims 0.082 vs 0.056. One labeled pair is thin evidence; choose after JP labels more pairs.

## DNA-VL-STEER-2B and the three-way embedding test (2026-11-25)
- **Model:** `dnotitia/DNA-VL-STEER-2B` (Dnotitia, Korea; Apache 2.0; 2.1B parameters; 4.0 GB) in `~/.cache/lives-bench/models/DNA-VL-STEER-2B/`. It is a language-bias-calibrated variant of Alibaba's `Qwen/Qwen3-VL-Embedding-2B` (only early layers adjusted; the vision tower is identical to the base). It embeds text, images, screenshots and video in one 2048-dimension space. It needs `transformers >= 5` and `qwen-vl-utils` (installed in `~/.cache/lives-bench/venv-embed`) and runs on the Mac's GPU (MPS).
- **Model-origin policy: allowed** (2026-11-25 rule: open weights, run locally, near the state of the art; it was best of the three on the screenshot test below). Registry entry: developer Dnotitia (Korea), base model `Qwen/Qwen3-VL-Embedding-2B` (Alibaba), Apache 2.0, checked 2026-11-25. Local use only; no API.
- **Test** (`pipeline/scripts/compare_embedders.py`; results `pipeline/misc/evd-validation/embedder-comparison/2026-11-25.md`; 200 quote texts each with the screenshot of that quote; one run):

| Model | text to image R@1 / R@5 | image to text R@1 / R@5 | JP merge pair rank (of 351) |
|---|---|---|---|
| DNA-VL-STEER-2B (2.1B) | 0.93 / 0.99 | 0.90 / 0.99 | 4 |
| EmbeddingGemma 2 (740M) | 0.86 / 0.99 | 0.87 / 0.98 | 9 |
| harrier-oss-v1-0.6b (596M) | text-only, not tested | text-only, not tested | 3 |

- **Reading:** both multimodal models can match a quote screenshot to its text, which suggests a cheap automatic check for the "does this crop show the quote" step (a rule to test: flag a crop whose own text is not the nearest to its image). EmbeddingGemma 2 (Google, US, 740M) comes within a few points of the 2.1B model and passes the origin policy. On title similarity DNA has the widest spread of scores; harrier ranks JP's merge pair highest. One labeled pair and one run: not enough to pick a winner.

## E-means (checked 2026-11-25): not used for screening
- [E-means](https://e-means.github.io/) (Meta FAIR and ENPC; arXiv 2611.09501, 2026-11-06; in the faiss library as `faiss.contrib.e_means`) is a faster replacement for k-means on very large datasets: mini-batch updates with exponential moving averages and batch size and step size set from fitted scaling laws. It reports 8 to 45 times faster training. It still takes the number of clusters k from the user.
- For about 80 to 200 papers, ordinary clustering is instant, so E-means adds nothing. The screening uses average-linkage clustering with the number of clusters chosen by silhouette score. Revisit E-means only for a corpus of hundreds of thousands of papers or passages. (Summary from a model-assisted read of the project page and repository; the full paper was not read.)

## Paper screening by embedding categories (2026-11-25)
- Scripts: `zotero_collection.py` (export a Zotero collection from a copy of the database), `screen_dedup.py` (duplicates by DOI, arXiv id and title; overlap with the seed set and an older pool), `screen_embed.py` (three-model vote against the seed task groups; clusters of papers that fit none), `screen_to_gsheet.py` (review workbook). Working files live in `~/.cache/lives-bench/screening/` because they hold abstracts and local paths; only metadata-only data and a TRIPOD+LLM-style README are in the vault (`pipeline/screening/<run>/`).
- Seed task groups come from the Review-Arena sections (`pipeline/screening/shared/seed-papers_task-groups.json`): peer review reports (7 seeds), reporting-guideline compliance (10), error and quality-issue detection (6), novelty (2), ethics (2), causal inference (1); one seed has two groups.
- Leave-one-out on the seeds: EmbeddingGemma 2 73%, harrier-oss-v1-0.6b 73%, DNA-VL-STEER-2B 77% (26 seeds testable; one task group has a single seed).

## Open models as a benchmark (dropped 2026-11-25)
JP dropped the open-model benchmark and Inkling after the pilot (it found 22 to 68% of Neon's primary numbers and none of its quotes on the longest paper). The spec is in `pipeline/misc/archive/open-model-benchmark-2026-11-25/`.

## Token budgets per model and stage (JP, 2026-11-25)

Measured on the 27 seed PDFs (`pdf_pages.py` text, the Claude and Gemini token counters) and on one real run (a 10-page paper). Max tokens means the output budget per request, **including thinking tokens**; it is a ceiling, and you pay only for what is used.

| Seed-paper length | Smallest | Median | p90 | Largest |
|---|---|---|---|---|
| Pages | 5 | 18 | 42 | 60 |
| Words | 2,500 | 8,900 | 18,900 | 35,000 |
| Claude input tokens for the PDF (about 2,700 per page) | 15,000 | 49,000 | 118,000 | 165,000 |
| Gemini or Sol input tokens as billed (about 1,400 per page; the Gemini counter says about 560, which the billed call did not match) | 7,000 | 25,000 | 59,000 | 84,000 |
| EVDs JP extracted per paper | 1 | 3 | 4 | 6 |

| Stage | Model | Input per request | Max tokens (output plus thinking) | Basis |
|---|---|---|---|---|
| PICOST extraction | Gemini 4 Neon, High thinking | whole PDF, 7,000 to 84,000 | 24,000 + 1,000 per page, at most 64,000 (34,000 at 10 pages, 42,000 at the 18-page median, 64,000 from 40 pages) | measured at 10 pages with 12 findings: 27,317 tokens (about 11,000 visible JSON, 16,000 thinking); the per-page growth is an extrapolation to check on the first batch of four |
| Independent recheck | GPT-6.2 Sol | only the cited pages plus one on each side (usually 3 to 9 pages) | 3,000 + 1,000 per flagged finding, at most 16,000 | measured about 670 per finding |
| Adjudication | Claude Opus 5.5 | the same excerpt plus both readings | 1,000 + 450 per disputed finding, at most 8,000 | measured about 226 per finding |
| EVD draft, critique and revision (three authors, up to two rounds) | Claude Sonnet 5.5, GPT-6.2 Sol, Gemini 4 Neon (Medium) | card about 3,000 (a critique round adds the three drafts, about 5,000) | draft 3,000; critique plus revision 4,000 | about 0.5k visible plus thinking |
| Draft vote | Sol and Sonnet 5.5 decide (Neon breaks ties) | card, three drafts, span about 3,500 | 2,000 each; Inkling 3,000 (includes its reasoning) | |
| Node-detail check | Claude Opus 5.5 | draft, span, crop about 4,000 | 4,000 | |
| Crop QA | GPT-6.2 Sol (vision) | one image, checklist | 1,500 | |
| Decision models | d1.2-ultra (text and images), Decider 1.3 (text) | page image or passage | not applicable | priced per call |

Two changes follow from the measurements. (1) The extraction prompt now sorts findings into three tiers (`picost-v3.md`: primary answers the research question, secondary is meta or contextual about a primary finding, tertiary is other context) with first-guess caps of 6, 4 and 2 (the seed maximum of 6 EVDs is the primary cap) and an `omitted` note per tier; v1 returned 29 findings for a 10-page paper and cost $0.60 for extraction alone. (2) Sol and Opus read only the cited pages, not the whole PDF (the 60-page seed papers are 165,000 Claude tokens). Real cost of the same 10-page paper through the paper processor: $1.24 before these changes, $0.52 after (Neon $0.46, Sol $0.06, Opus not needed).

### Stages added on 2026-11-25 (`lives_stages.py`): budgets and cost
| Stage | Models | Max tokens per request | Notes |
|---|---|---|---|
| Checks, decision models | Perplexity Decider 1.3, Liquid d1.2-ultra | not applicable | two calls per finding; cents per paper |
| Checks, vision | GPT-6.2 Sol (images) | 1,500 | every finding (pass, fail or cannot verify) |
| Checks, disputes | Claude Opus 5.5 (image) | 3,000 | only where Sol and the checks disagree |
| Draft, round 0 | Sonnet 5.5, Sol, Neon (Medium) | 9,000 | all nodes of a paper in one request per model |
| Draft, critique and revision | Sonnet 5.5, Sol, Neon (Medium) | 14,000 | each sees all three first drafts, anonymous and shuffled |
| Draft, vote | Sol and Sonnet | 5,000 | Neon tie-break 3,000, only for split nodes |
| Draft, node-detail check | the cheaper of Sol and Sonnet that did not write the winner | 6,000 | one request per checker per paper |
| Quality signals | Opus 5.5, Sol, Neon (Medium) | 9,000 | 25 signals per paper, one request per rater |

Cost so far (measured only on a one-page synthetic paper, standard mode): $0.61 for extraction, checks, drafting of 4 nodes and 25 quality signals. Rough planning figures per paper in standard mode: checks about $0.15, drafting about $1.9 (it grows with the number of nodes), quality signals about $0.25 plus $0.015 per page; batch mode is half. For the four-paper seed pilot the full pipeline is therefore about $6.7 in batch mode and $13 in standard mode, above the $5.55 cap. The pilot replaces these guesses with measurements.

## Model review and vision tests (2026-11-26)
**Decision models.** Liquid d1.2-ultra (released 2026-11-16, id `d1.2-ultra`, $0.042 per million input tokens, reads text, images and audio, US company) replaced d1-ultra. Liquid reports a Decision Index v2.1 score of 75 (first of 24) and a calibration error of 0.8 against 3.7 for Perplexity Decider 1.3; these are Liquid's own figures, and no outside group had replicated them in the pages found. Other decision models found: Drex Max v1.1 (Nace.AI, index 73), Gemini Decision 1 (Google, $0.10 per million input tokens, launched 2026-11-11, no independent check found), GPT-6 Luna Decisions API (OpenAI, calibration error 7.2). Nobody has published a test of using two or three decision models together. We keep Perplexity Decider 1.3 as a third voter because it costs cents and decided 27 PICOST slot judgments and 14 quality-rating judgments where Sonnet 5.5 and d1.2-ultra disagreed (it was outvoted on 10 and 17); drop it only if JP's labels show it is wrong when it decides.
**Does d1.2-ultra replace a vision model or PyMuPDF?** Measured on our data: (1) digit comparison between a quote and its highlighted screenshot separates correct quotes from quotes with one changed digit (60 quotes, pairwise AUC 1.0) and agrees with Sonnet 5.5's reading on 228 digit-containing quotes 98% of the time (223 agree, 2 are quotes d1.2-ultra scored low that Sonnet read as equal, 3 are symbol differences Sonnet flagged and d1.2-ultra missed); (2) word comparison failed: it scored 18 of 55 correct no-digit quotes below 0.5, so quotes without digits are read by Sonnet 5.5; (3) locating a quote on a page image (`box` answer, 100 dpi page, 40 quotes found by PyMuPDF): median intersection over union with the PyMuPDF box 0.57, 65% at 0.5 or more, 23% at 0.8 or more. It finds the rough place, not the exact words, so PyMuPDF stays the locator (exact word boxes and text) and d1.2-ultra can only serve as a fallback to crop a rough region when PyMuPDF cannot find a quote. It is not an OCR model: text, number and date answers read only the supplied text, so scanned pages need an OCR or layout model first.
**Other Liquid models.** LFM2.5-VL-1.6B-Extract and LFM2.5-VL-450M-Extract (image to structured data, local) and LFM2.5-Embedding-350M are candidates to test; none has been tested on our PDFs.
**Candidates found by a web survey (secondary sources, not verified, not adopted).** Embeddings: Harrier-OSS v1 (Microsoft; `harrier-oss-v1-0.6b` is already in our local embedding list) scores higher than EmbeddingGemma 2 on the MTEB average but no clustering scores were found for either; test both on the Question groups clustering before changing. LLMs: Claude Fable 5.2 leads the Artificial Analysis Intelligence Index v5 page found (64.8, above Opus 5.5 at 59.1) and is worth a test as adjudicator; Gemini 4 Neon (61.5) and GPT-6.2 Sol (57.3) stay for extraction and second reading. Document parsing: MinerU and Marker (local) are candidate fallbacks for scanned PDFs and table cells; no head-to-head against PyMuPDF was found.
**MinerU and Marker against PyMuPDF (evidence found 2026-11-26, secondary reading, not tested on our PDFs).** For tables, formulas and heading structure they are clearly better than pymupdf4llm: on READoc (benchmark authors) the overall average was 73.1 for MinerU, 65.0 for Marker and 40.6 for pymupdf4llm; on OmniDocBench (MinerU's own group) MinerU's table score was 81.9 to 87.9 against 65.8 for Marker; on olmOCR-Bench (AI2) MinerU scored 75.2 and Marker 76.1 (Marker's own README reports 76.0 for its balanced mode and 83.7 with a model server). An independent study (Adhikari and Agarwal 2024, DocLayNet) put PyMuPDF at 0.84 text F1 on scientific documents and 0.18 on table detection. No benchmark found compares verbatim text accuracy or word boxes on born-digital papers for all three, and parsers that use OCR or a vision-language model can paraphrase or invent text, which would break exact quote matching. Both need a GPU for reasonable speed. Marker's weights carry a modified Open Rail-M licence. Decision: keep PyMuPDF for quote text and word boxes; test MinerU or Marker only for table cells, on 20 to 30 of our papers with 10 to 15 hand-checked tables.
**Exploratory use case (JP, 2026-11-26): Marker and MinerU for table cells only.** Installed in `~/.cache/lives-bench/venv-tables`; tested on the 27 seed papers against PyMuPDF `find_tables()` and against the verified table numbers of the four pilot papers; results in `pipeline/misc/evd-validation/table-parsers/RESULTS.md`. Marker's LLM mode stays off. No other use is approved beyond the Stage II benchmarking run (JP, 2026-11-27; no LLM calls); PyMuPDF with symbol repairs is the preferred reader. **Result:** neither is worth adding for table cells (PyMuPDF 91.6%, Marker 91.6%, MinerU 93.1% of 463 verified numbers; MinerU is 6 times slower; MinerU's extra values come from an en-dash text-layer quirk that a one-line repair fixes). Install sizes: venv 1.7 GB, Marker models about 123 MB, MinerU basic models 857 MB.

## Update 2026-11-27 (lean model plan, local aim, tables, verification)

**Lean model plan (JP, 2026-11-27; pending validation, not built).** Target at most $2.49 per paper for extraction, quality signals, TRIPOD-LLM and the quality appraisal table. Quality signals and TRIPOD-LLM rows: Gemini 4 Neon (high) rates every row; low-confidence rows go to GPT-6.2 Sol (high); if Sol is also unsure the row goes to JP; Opus 5.5 is not used. Verification: when the two decision models disagree, Neon (medium) judges instead of Sonnet 5.5. Quote reading from screenshots: Neon replaces Sonnet. Drafting: first drafts by GPT-6.2 Sol only, critique by Neon only, tiebreaker Sonnet 5.5. EVD rework below 0.60: Sol (medium). Classifying sampled problems: a small local model to try (Neon low as the hosted fallback). Grouping questions, claims, evidence and caveats: EmbeddingGemma 2 (local) finds candidates, Neon (medium) decides. The estimate from pilot logs is about $3.0 to $3.5, above the target (see `misc/evd-validation/TODO.md`). Until JP validates it, the three-rater maximum-accuracy setting remains the default in `config/models.json`.

**Verification and decision models (2026-11-27).** `decision_models.resolve_preferred()` tries `d1.3-ultra` first and keeps `d1.2-ultra` while the API returns 404 (it did on 2026-11-27). Baseten bison-1 (31B, $0.10 per million tokens) runs as a text-only shadow verifier and is not in any vote: on 226 Woelfle items it agrees with d1.2-ultra 79%, Perplexity 81%, Sonnet 86%, passes PICOST slots almost always (1% below 0.5), and its image test was unreliable. Each stage now records elapsed seconds and request count in `stage_log`.

**Table cells and Word files (2026-11-27).** `pdf_pages.table_numbers(page)` matches a verified value against numbers in any table cell plus table captions and footnotes: 463 of 463 values found (strict cell match 431, any cell 451). Five any-cell matches are accidental (for example the 5 in a 'Recall@5' header). `derotate.derotate_page(page)` turns a rotated page upright before MinerU reads it (MinerU 380 to 431 at /Rotate 90). `pdf_pages.docx_tables(path)` reads .docx tables through python-docx with merged cells repeated (10 of 10 supplement values; the four `sj-docx-*` files return 0, 0, 0 and 1 table). Do not convert Word files to PDF; save an old .doc as .docx first.

**Long-term aim (JP, 2026-11-27): a fully local and open LIVES-DP** within 6 to 12 months, for user control, fine-tuning, privacy, security and reliability, and so that a review of 100 or more papers does not cost hundreds of dollars. Needed: one multimodal (text and image, English) model that is fairly capable and runs in 24 to 128 GB of RAM. Candidates to benchmark on the pilot papers (from a web search on 2026-11-27, not tested here): Qwen3-VL in the 8B to 32B sizes (quantized) and InternVL3 (MIT license); Gemma 3 is the older option. Steps already local: PyMuPDF, python-docx, MinerU, Marker, EmbeddingGemma 2.

**LIVES-DP Explorer (2026-11-27).** An interactive page (30 steps in 7 phases; tool type, cost per paper, time and the evidence behind each accuracy figure) is at https://claude.ai/artifact/L5EBs2wZX1fiRkXUJH7WnA (private; source `pipeline/docs/lives-dp-explorer.html`). No step is scored against JP's labels yet.

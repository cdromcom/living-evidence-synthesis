---
page_type: research-note
date: 2026-11-27
topic: reproducibility checks for the LIVES quality signals table
---

# Reproducibility check options for LIVES (2026-11-27)

Outcome: start with cheap code-free checks (links, archives, badges, repository vs paper audit, statistic recomputation), then run an agent re-run only on small CPU-only packages with open data. Agents now score high on curated tasks but are weak on messy social science packages. No paid calls were made and no vault or repo files were changed. Figures come from search summaries and abstracts, not full papers; UNVERIFIED marks items I could not confirm.

## 1. Agent benchmarks

- CORE-Bench (re-run a package, answer questions): 21% best in 2024 (https://arxiv.org/abs/2409.11363). HAL lists Claude Code with Claude Opus 4.5 at 77.78% official, 95.5% after manual grading fixes, $87.16 per run, and declares the benchmark solved (https://hal.cs.princeton.edu/corebench_hard). A June 2026 paper reports 100% at the top, adds v1.1 (39 tasks) and an out-of-distribution suite, and measures a 2x speedup for human plus agent (https://arxiv.org/abs/2606.26158). Median about $1.47 per task (UNVERIFIED, search summary of https://arxiv.org/pdf/2603.23749). Curated tasks with known shortcuts.
- REPRO-Bench (112 social science packages, rate 1 to 4): best baseline 21.4%, below the 25% random rate (https://arxiv.org/abs/2507.18901). PaperRepro reaches 44.6% (50.9% on the cleaned REPRO-Bench-S) at about $1.93 per paper with GPT-4o. Accuracy falls from 75.0% to 55.6% to 33.3% across easy, medium, hard packages; setup errors (missing dependencies, versions) are most common; Stata 38.1% vs R 56.0% (https://arxiv.org/html/2603.00058).
- Kohler et al. 2026 (48 I4R social science papers, agent sees methods and data only): agents largely recover published results, varying by model, scaffold and paper; problems come from agents and from under-specified papers (https://arxiv.org/abs/2604.21965). Cost not read.
- ReplicatorBench (KDD 2026): human-verified replicable and non-replicable claims, three stages (https://arxiv.org/abs/2602.11354). Scores not read.
- PaperBench (rebuild 20 ICML 2024 papers): 21.0% original best, 27% later version vs human PhDs 41%; judge cost about $66 per paper, $10 for Code-Dev (https://arxiv.org/abs/2504.01848, https://the-decoder.com/ai-struggles-to-match-human-researchers-in-paper-replication-test/). Kimi K2.5 at 63.5% is self-reported (https://llm-stats.com/benchmarks/paperbench). This is paper-to-code, not package checking.
- SciReplicate-Bench: 39% best (https://arxiv.org/abs/2504.00255).
- ReproRepo (1,149 ML papers): paper vs repository audit without running code; Codex with GPT-5.5 found a human-reported blocker for about 90% of papers but is weaker on exact cause (https://arxiv.org/abs/2606.18237).
- ARA (paper text only): workflow-graph score, about 61% accuracy vs human labels, F1 12 to 13% (https://arxiv.org/html/2605.02651v1).
- Seen, not read: AgentActionBench (https://arxiv.org/html/2609.11117), ReproAgent (https://arxiv.org/pdf/2608.24291).

## 2. Re-run tooling

- Base rates: 74% of 9,078 R files in 2,109 Harvard Dataverse packages crashed on first run, 56% after automatic code cleaning (preprint figures) (https://arxiv.org/abs/2103.12793). Of 1.4 million GitHub notebooks, 24% ran to the end and about 4% matched stored outputs (https://leomurta.github.io/papers/pimentel2019a.pdf).
- Containers (Docker, Binder with repo2docker, Code Ocean capsules) give stability but not bit-wise reproducibility (https://arxiv.org/html/2604.01072v1). Code Ocean current status: UNVERIFIED (https://codeocean.com/product/compute-capsules).
- Software Heritage SWHID plus CodeMeta identify the exact archived code (https://arxiv.org/pdf/2004.00514). RO-Crate: no source found, UNVERIFIED.
- F-UJI: REST service, 14 of 15 FAIRsFAIR metrics, surface-level on interoperability and reuse (https://github.com/pangaea-data-publisher/fuji).
- Papers with Code closed July 2025 and redirects to Hugging Face Trending Papers; leaderboards were not carried over (https://www.codesota.com/papers-with-code/shutdown, secondary source).

## 3. Recomputing reported statistics

- statcheck (APA-style tests): developers report sensitivity 85 to 100% (https://research.tilburguniversity.edu/en/publications/the-validity-of-the-tool-statcheck-in-discovering-statistical-rep/); a reanalysis reports about 52% sensitivity and 60% precision and about 40% of statistics missed (https://arxiv.org/pdf/1610.01010).
- GRIM and SPRITE (R package scrutiny): an AI-extraction GRIM script exists, accuracy unevaluated (https://theses.liacs.nl/pdf/2024-2025-PleunesSJStijn.pdf, thesis).
- Pattern to reuse: LLM extracts numbers, a script recomputes (a vendor describes this: https://manusights.com/tools/stats-audit/methodology). An opinion page says LLMs should not do the arithmetic (https://seandavi.github.io/scriptorium/concepts/knowledge/critique-techniques/statistical-inconsistency/).

## 4. Human and community programs

- I4R replication games (PNAS 2026): 288 researchers, 103 teams; AI-assisted teams beat AI-led teams but not human-only teams (https://repository.essex.ac.uk/43026/1/pnas_2025-24747RR_Manuscript_File.pdf).
- ML Reproducibility Challenge: reports on OpenReview and ReScience C; 2021 had 102 submissions, 43 accepted (https://paperswithcode.com/rc2021). ReScience C has 213+ open articles, used as labels by ARA.
- ACM badges (Available, Evaluated Functional or Reusable, Results Reproduced or Replicated) can be read from the paper page (https://www.acm.org/publications/policies/artifact-review-badging/).
- Brazilian Reproducibility Initiative (wet-lab replications; headline rate not read) (https://elifesciences.org/reviewed-preprints/111001); Dutch Reproducibility Network, founded 2023, with NWO replication grants (https://www.erasmusmagazine.nl/en/?p=160639). I found no per-paper lookup from either.

## 5. Local vs frontier, cost, safety, limits

- Local open models: suitable for link, badge and statistic extraction feeding scripts. I found no open-weight entries on CORE-Bench; strong results used frontier or GPT-4o class models, and PaperRepro's ablation shows the execution agent is most sensitive to model strength.
- Cost per paper (my estimate, not measured): metadata audit near zero; repository audit cents to $2; agent re-run $2 to $20 and 15 to 60 minutes.
- Sandbox: plain Docker shares the host kernel; prefer Firecracker or Kata microVMs, or gVisor, with outbound network explicitly blocked (https://fly.io/learn/firecracker-vs-gvisor/, vendor source). Use no credentials, read-only mounts, a time limit, and a pinned package mirror.
- Limits: GPU or long jobs, closed data, Stata and MATLAB licenses, hard-coded paths. "Not run" should be its own status.

## Options table

| Option | Checks | Accuracy evidence | Cost / time | Local | URL |
|---|---|---|---|---|---|
| Metadata audit (DOI, SWHID, CodeMeta, F-UJI, badges) | Package exists, archived, citable | F-UJI surface-level | near zero | yes | https://github.com/pangaea-data-publisher/fuji |
| Repo vs paper audit | Gaps and mismatches without running | about 90% blocker hit | cents to $2 | partly | https://arxiv.org/abs/2606.18237 |
| ARA paper-only score | Methods reconstructable | about 61% | UNVERIFIED | maybe | https://arxiv.org/html/2605.02651v1 |
| statcheck, GRIM | Internal numeric consistency | 52 to 100%, disputed | seconds | yes | https://arxiv.org/pdf/1610.01010 |
| Claude Code class re-run | Package runs, outputs match | 78 to 95% CORE-Bench Hard | about $1.5 per task | no | https://hal.cs.princeton.edu/corebench_hard |
| PaperRepro | Score 1 to 4 | 44.6% exact | about $1.93 | no | https://arxiv.org/html/2603.00058 |
| Human programs | Independent reproduction | gold labels | not scalable | n/a | https://www.acm.org/publications/policies/artifact-review-badging/ |

## Recommended staged plan

1. Stage 0, all papers: extract code and data links, license, archive IDs, badges, and any ReScience C or I4R report. Output: available, archived, badge.
2. Stage 1, papers with a package: scripted statistic checks and a repository vs paper audit. Output: flags with the sentence or cell cited.
3. Stage 2, small CPU-only open-data packages: agent re-run in a microVM without network, one frontier model, hard budget per paper. Output: ran and matched, partial, not run.
4. Stage 3: check 5 to 10% of Stage 2 results by hand against the source PDFs, and validate in the Google Sheet before anything goes to the vault.

## Open questions for JP

1. Should "not run" be a neutral status separate from "did not reproduce"?
2. Which fields first? Social science (Stata, R) is hardest; ML is easier to run but often needs GPUs.
3. What budget and size cap per paper for Stage 2? Agent loops are interactive, so batch mode probably does not fit.
4. Local Docker on the Mac, or a rented microVM service?
5. Signal per paper or per claim?

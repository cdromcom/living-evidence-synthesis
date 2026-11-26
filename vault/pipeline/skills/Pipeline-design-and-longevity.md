---
type: reflection
title: Pipeline design and longevity
author: Claude (Sonnet 5.5), for Jay Patel (JP)
written: 2026-11-25
status: living document; update it when a rule here changes
---

# Pipeline design and longevity

This page says how LIVES is put together so it can last for years, how to change each part without breaking the others, and where it is still fragile. It is written for JP and for anyone who forks the project for another review topic.

## 1. The layers

Each layer changes at its own speed. Keep them separate and let changes flow downward only.

1. **Data** (the vault): discourse-graph nodes in `sysrev/dgraph/`, PICOST records, screening data. Changes with every paper. Ground truth.
2. **Instructions**: `Skill.md` and its companions, node templates in `pipeline/templates/`, prompts in `pipeline/prompts/`. Changes when the method changes.
3. **Configuration**: `pipeline/config/models.json` (models, prices, roles, origin policy) and `pipeline/config/pipeline.json` (limits, budgets, thresholds, ethics switches). Changes when a model, price or budget changes.
4. **Code**: `pipeline/scripts/`. Reads layers 2 and 3, never hard-codes a model or a limit.
5. **Apps**: the LIVES web app, the MkDocs render and the Google Sheets. Built from layer 1.
6. **Records**: `pipeline/runs/` (call logs and manifests), `History.md`, `LOG.md`, the AI-use footers. Append only.

## 2. How to change each thing

| To change | Edit | Then |
|---|---|---|
| A model for one job | the role in `models.json` | `python3 pipeline/scripts/selftest.py` |
| A model's price | its entry in `models.json` (add the source and date) | selftest; note it in `LOG.md` |
| Add a provider | a route in `llm_batch.py`, an entry in `models.json` | selftest, then one cheap live call |
| A budget or limit | `pipeline.json` and a note in `LOG.md` | selftest |
| A Python package | `requirements.txt` | selftest; run one cheap live call |
| A prompt | save a **new version file** (`picost-v4.md`), point the stage at it | never edit a used prompt: old runs and benchmarks point at it |
| A Skill rule | the Skill file | add a line to `History.md`; update the related prompt |
| A node template | the file in `pipeline/templates/` | check the Obsidian discourse-graph plugin still points at it; run `check_links.py` |
| A quality signal | `quality-signal-labels.json`, `SIGNALS` in `lives_stages.py` | selftest checks that the ids match |
| The web app or repo | the app code; it reads the vault format | `scripts/build-graph.mjs` must still produce the same graph for unchanged nodes |

## 3. Recipes

### Swap a model
1. Add or edit the model in `models.json` (provider, country, weights, price, source, date).
2. Point the role at it.
3. Run `selftest.py`. It checks the price, the route and the origin policy.
4. Run one dry run (`lives_run.py ... --dry-run`) to see the new cost estimate.
5. Run one cheap live paper before a batch. Record what happened in `LOG.md`.

### Fork for another review topic
1. Replace the seed set (`pipeline/screening/shared/`) and the research questions.
2. Replace the category names and task types, and the quality signals if the field needs others.
3. Keep `models.json` and `pipeline.json`, and set your own keys and caps.
4. Rewrite the node examples in `Skill-templates.md` for your field.
5. Re-run the pilot on four papers and calibrate the check thresholds on your own labels.

### Update a package
1. Change the pin in `requirements.txt` in a branch.
2. Run `selftest.py`, then one cheap live run.
3. If PyMuPDF changes, also run `pdf_pages.py` on three PDFs and compare the page maps by eye.

### Manage the graph in Obsidian
- The node type ids in the templates (`nodeTypeId`) tie the vault to the discourse-graph plugin. Never change them.
- Edit nodes in Obsidian or by script, then run `check_links.py` and regenerate `DGRAPH.md`.
- Write new nodes into the vault only after JP's spot check. The paper processor keeps drafts in `pipeline/runs/`.
- Export the plugin list and versions into a note when you upgrade Obsidian (the `.obsidian` folder is not in the repository).

## 4. Robustness over time

- **Pin and record.** Packages are pinned. Every run's manifest stores script and prompt hashes, package versions and model ids with dates. A result can be explained years later.
- **Freeze benchmarks.** The Stage II snapshot (inputs, prompts, models, outputs, labels) is never edited, so open models can be compared against it later (`Open-model-benchmark-spec.md`).
- **Expect API drift.** Model names, prices and parameters change. The self-test and one live call catch most breakage. The registry holds the price source and the date, so a stale price is visible.
- **Expect link rot.** Papers are identified by DOI and PDF hash. Supplements are saved locally.
- **Keep a degraded mode.** If API money runs out, screening still runs locally and humans can extract by hand with the same templates. Open models are the long-term fallback.

## 5. Robustness across budgets

1. Every batch has a hard cap, a worst-case check before each stage, stop rules and a ledger (`pipeline.json`).
2. Batch mode costs about half; use it once prompts are stable.
3. Replace estimates with measurements after every pilot and put them in `pipeline.json`.
4. Set a monthly limit at each provider as a second fence. The paper processor's cap covers only its own calls.
5. Cheap checks come first (scripts, decision models). Expensive models see only what the cheap ones could not settle.

## 6. Ethical constraints

- **Human in the loop.** Nothing enters the vault without a person's spot check. The footer on every page names the models and the human check.
- **Disclosure.** The GAMER answers (`AI-disclosure.md`), `model-history.md` and per-call logs say what AI did.
- **Privacy and rights.** PDFs, local paths and keys never go to the public repository, and abstracts do not either, except the whole-library screening table that JP asked to keep in the repository (2026-11-26). Only short verbatim spans are quoted. Downloads are limited to freely available files, listed in chat, and never bypass a paywall or login. Uploaded files are deleted from provider storage at the end of a run.
- **Model origin.** Hosted APIs only from allowed countries (the policy is in `models.json` and enforced in code). Open-weight models may run locally from any country.
- **Fairness and uncertainty.** Report accuracy against human labels with ranges. Models are benchmarks, not authorities.
- **Environmental cost.** Prefer local and small models where accuracy allows. Report time and cost per paper.

## 7. What was hardened on 2026-11-25

- One model registry and one limits file replaced constants scattered through scripts.
- The origin policy is enforced in code, not only written down.
- `selftest.py` checks 36 things offline, for free.
- Packages are pinned and the keys are listed in `.env.example`.
- Prompts are versioned files; runs record their hashes.
- Uploaded provider files are cleaned up automatically.

## 8. Weak points that remain, most serious first

1. **The vault has no version control.** It is the ground truth, but only the repository copy has history. During this session a bad edit damaged a script and the only good copy was the last push. Recommendation: put the vault under git (for example with the Obsidian Git plugin) or take scheduled snapshots, and push often.
2. **No automated tests in CI.** GitHub Actions is locked by a billing issue. Until it is fixed, run `selftest.py` before every pull request.
3. **`Skill.md` is too long.** It mixes rules, history and decisions. Split it into a short core plus modules, and move dated decisions to `History.md`.
4. **Docs repeat model names.** A model swap needs edits in several documents. Generate the model tables in `Tools-and-Models.md` from `models.json`.
5. **Single maintainer.** Add `CONTRIBUTING.md`, a five-minute quickstart, sample data and a license note so others can start.
6. **The web app depends on the vault format.** Add a small contract test (a fixture vault and the expected graph) so a template change cannot silently break the site.
7. **Unverified numbers.** Several prices and the decision-model thresholds are first guesses. The pilot replaces them.

## 9. Ideas for the app and the repository

- Show evidence tiers (primary first, secondary as context) and the run's checks on node pages.
- A review mode in the app for spot checks, so labels go straight into the benchmark sheets.
- Accessibility pass (contrast, keyboard use, screen readers) and a mobile layout check.
- Issue and pull-request templates, a CODEOWNERS file and a changelog in the repository.
- A demo mode with sample data so a visitor can try the app without the full vault.

## 10. Principles to keep

1. Ground truth lives in one place (the vault) and everything else is rebuilt from it.
2. Configuration, not code, holds anything that will change.
3. Never edit what an old result depends on; add a new version.
4. Cheap checks first, expensive judgment only where needed.
5. Prefer false positives that a human can filter over misses no one will find.
6. Measure before trusting an estimate.
7. Keep a human decision at every point where content enters the vault.

---
type: tips
author: Claude (Sonnet 5.5), for Jay Patel (JP)
updated: 2026-11-25
---

# Tips

Short, practical notes learned while running the pipeline. Add one entry per lesson, newest first.

## Google Cloud and the Gemini API (personal Gmail account)

- **Reopen a closed billing account (JP, 2026-11-25).** In the Google Cloud console open Billing and the list of billing accounts. Closed accounts are hidden by default (clear the "Status: Active" filter). Click the **three vertical dots** on the account's row and choose the **active / open** option. Reopening is a payment-profile step, so do it yourself in the browser.
- **Check that the project is really on the paid tier.** In Google AI Studio open the rate-limits page for the project. A "Free tier" badge, or `gemini-4-neon` showing 0 / 0 / 0 for requests per minute, tokens per minute and requests per day, means calls will fail with HTTP 429 (free-tier quota, limit 0). Once billing is active and linked, the badge goes away and the limits are above 0.
- **One-call test.** `call_logger.logged_gemini(...)` with a one-word prompt costs about $0.001. A test is also the quickest way to see that the key belongs to the paid project.
- **Thinking tokens are billed as output.** Set the thinking level per step (`effort` in `logged_gemini`): low for routine steps, high for extraction.
- **Where the key lives.** `GEMINI_API_KEY` in `~/.config/lives-ai-raters/.env`. Never paste it in chat or the repo. Set a spending limit on the credit you loaded.

## Zotero

- Quit Zotero completely (Cmd+Q, not only the window) before a script writes to `zotero.sqlite`. Check with `pgrep -f Zotero.app`.
- Merge duplicates only after a backup; `pipeline/scripts/zotero_merge_duplicates.py` writes one automatically and trashes (never deletes) the older copies.

## Screening sheet
- To add new papers, follow "Adding new papers to the whole-library screening sheet" in `pipeline/screening/README.md`. Do not re-upload the sheet: that would replace your labels.

## Version control for the vault (Obsidian Git)
- The vault is the ground truth but had no history; only the GitHub copy did. Install the **Obsidian Git** plugin and initialize a repository in the vault folder (the `.gitignore` is already there).
- Suggested settings: auto commit every 10 minutes, commit message `vault: {{date}}`, pull and push only if you add a **private** remote. Keep the history local if you prefer.
- The GitHub repository stays the public mirror (`vault/` inside it). Syncing to it is still a pull request made with `check_repo_sync.py`; the vault's own git history is separate.
- PDFs, local run outputs and backups are ignored on purpose (see `.gitignore`).
- Before a risky edit, make a commit by hand. A bad edit on 2026-11-25 damaged a script and the only good copy was the last GitHub push.

# Archived EvidencePatterns (2026-11-25)

JP retired EvidencePatterns (EPs) from the pipeline and the LIVES web app, because CLMs can be cross-paper (a CLM lists every paper that makes the claim) and human-generated syntheses cover the rest. The nodes are kept here for later use.

## What is here
- `nodes/`: the 21 EP pages exactly as they were.
- `pages-before-removal/`: the 60 EVD pages and 27 QUE pages as they were before their EP link sections were removed.
- `removed-sections.json`: the removed text, by page path.
- `EvidencePattern Nodes.base` and `T - EP.md`: the Obsidian Base and the template for EP nodes.

## What changed in the vault
- The section "Instantiates Pattern(s)" was removed from 60 EVD pages and "Cross-paper patterns" from 27 QUE pages.
- Scripts no longer read, check or generate EPs (`check_links.py`, `vault_to_gsheet.py`, `embed_candidates.py`, `merge_judge.py`, `compare_embedders.py`, `add_link_aliases.py`, the MkDocs hook).

## To restore
1. Move `nodes/` back to `sysrev/dgraph/evd-patterns/`, the Base to `sysrev/indexes/` and the template to `pipeline/templates/`.
2. Copy the pages from `pages-before-removal/` over the current EVD and QUE pages (or re-insert the sections from `removed-sections.json`). Edits made to those pages since 2026-11-25 would be lost, so merge by hand if they changed.
3. Re-add the EP entries to the scripts listed above (see the History entry of 2026-11-25) and to the web app (see the pull request that removed them).

## Why CLMs can take over
The CLM template lists "Key Papers Making This Claim", so a CLM can span papers. On 2026-11-25, 8 of 31 CLMs already list two to four papers. Going forward, write cross-paper claims as CLMs that list every paper that makes them, and keep human-written syntheses in the Review-Arena.

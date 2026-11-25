---
prompt_type: vault-generation
target_page: DGRAPH.md
generated_by: Claude (Opus 4.7 / Sonnet 4.6 across the session)
date: 2026-04-27
---

## Original user prompts

### Initial creation request

> Can you create a DGRAPH.md file that nest questions, claims, and evidence in a nested structure (be comprehensive) to provide a central resourcing synthesizing the nodes? Each QUE, CLM, and EVD should be clickable.

### Follow-up — graph attachment invariants

> All CLMs and EVD should be attached to questions. All EVDs should ALSO be attached to CLMs. All CVTs should be attached to EVDs only.

### Follow-up — properties + callouts

> yes, and also ensure that a properties/metadata table exists for dgraph include author, type of page, date created, date updated, and a link to the prompt that generated the page. Notes can still appear below the properties page using callout boxes in Obsidian markdown (info, caution, tips, etc.)

## Generation pipeline

`/tmp/build_dgraph.py` reads:

1. Each QUE's `### Supporting Claims (with their evidence)` section — the canonical source for QUE → CLM → EVD nesting.
2. Each CLM's `### Supporting Evidence` section — for EVDs not already surfaced via a QUE.
3. Each CVT's `appliesTo:` frontmatter list — for EVD → CVT links.

It produces a comprehensive nested document with every node as an Obsidian wikilink. Re-run the script to regenerate after any structural change to the vault.

## Graph invariants enforced

- Every CLM appears in at least one QUE's nested structure.
- Every EVD appears in at least one CLM's `### Supporting Evidence` AND at least one QUE's nested structure.
- Every CVT's `appliesTo` lists only EVDs (no CLMs).

## Related history entries

See `HISTORY.md`:
- Phase 8 — nested QUE → CLM → EVD hierarchy in QUE files
- Phase 10 — DGRAPH.md central index creation
- Phase 11 — graph attachment rules enforced
- Phase 12 — properties/metadata + callouts (this prompt)

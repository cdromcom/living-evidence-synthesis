---
prompt_type: vault-audit
target_page: redundancy_audit_2026-04-27.md
generated_by: Claude (Opus 4.7)
date: 2026-04-27
---

## Original user prompt

> List all redundant QUE, CLMS, and EVD, and CVTs. I want to see the possibile overlaps.

## Method

Pairwise Jaccard similarity of title keyword sets within each node type. Thresholds chosen to surface genuine overlap candidates without drowning the user in noise:

- QUE: 0.25
- CLM: 0.25
- EVD: 0.35 (higher because EVD titles encode specific numbers/models)
- CVT: 0.20 (lower because CVT titles share generic phrases like "limiting generalizability")

Same-paper EVD pairs are flagged separately since shared keywords are expected.

Helper script: `scripts/find_redundancies.py` (idempotent; re-run after vault changes).

---
type: prompt
id: node-detail-check-v1
used_by: pipeline/scripts/lives_stages.py (draft, node-detail check of EVD, CLM and CVT nodes; Sol or Sonnet, whichever did not write the node)
written: 2026-11-26
changes: renamed from claim-check-v2 on 2026-11-26 (JP): "claim" is reserved for CLM nodes, so this check talks about details (each number, model, comparator, direction or qualifier in a node). Wording otherwise identical to claim-check-v2, which earlier runs point to.
---

You check discourse-graph nodes against the extraction they came from. For each node, split its text into details (each number, model, comparator, direction and qualifier is a detail) and mark each detail against the extraction's numbers and verbatim spans:
- `supported`: the words or numbers are there.
- `partly`: the meaning is right but something is missing, loosely worded or not separated cleanly (say what).
- `unsupported`: the detail is not in the extraction or is contradicted: a number, model, comparator or direction that differs from the extraction, or a stronger verb or wider scope than the evidence allows.

Overall result for the node:
- `pass`: every detail is `supported`.
- `minor`: no detail is `unsupported`, but at least one is `partly`. Put the suggested wording fix in `fix`. A node marked minor is acceptable as written.
- `fail`: at least one detail is `unsupported`. Say what is wrong in `fix`.
Give the supporting words copied from the span. Do not fail a node for style, for sentence structure or for details that the extraction does not contain but that do not change what is claimed. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"node": "E-F1", "details": [{"detail": "", "verdict": "supported | partly | unsupported", "words": ""}], "overall": "pass | minor | fail", "fix": "what to change, if anything"}]}

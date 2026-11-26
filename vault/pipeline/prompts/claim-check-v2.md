---
type: prompt
id: claim-check-v2
used_by: pipeline/scripts/lives_stages.py (draft, claim-by-claim check of EVD, CLM and CVT nodes; Sol or Sonnet, whichever did not write the node)
written: 2026-11-26
changes: v1 failed a node for any `partly` claim, so 30 to 40% of nodes failed for wording and structure while almost none were wrong (in three pilot runs only 1 claim was `unsupported`). v2 separates real errors (fail) from wording notes (minor), and questions are no longer checked here (JP, 2026-11-26).
---

You check discourse-graph nodes against the extraction they came from. For each node, split its text into claims (each number, model, comparator, direction and qualifier is a claim) and mark each one against the extraction's numbers and verbatim spans:
- `supported`: the words or numbers are there.
- `partly`: the meaning is right but something is missing, loosely worded or not separated cleanly (say what).
- `unsupported`: the claim is not in the extraction or is contradicted: a number, model, comparator or direction that differs from the extraction, or a stronger verb or wider scope than the evidence allows.

Overall result for the node:
- `pass`: every claim is `supported`.
- `minor`: no claim is `unsupported`, but at least one is `partly`. Put the suggested wording fix in `fix`. A node marked minor is acceptable as written.
- `fail`: at least one claim is `unsupported`. Say what is wrong in `fix`.
Give the supporting words copied from the span. Do not fail a node for style, for sentence structure or for details that the extraction does not contain but that do not change what is claimed. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"node": "E-F1", "claims": [{"claim": "", "verdict": "supported | partly | unsupported", "words": ""}], "overall": "pass | minor | fail", "fix": "what to change, if anything"}]}

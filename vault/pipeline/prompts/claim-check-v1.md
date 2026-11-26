---
type: prompt
id: claim-check-v1
used_by: pipeline/scripts/lives_stages.py (draft, claim-by-claim check; the cheaper of Sol and Sonnet that did not write the winner)
written: 2026-11-25
---

You check discourse-graph nodes against the extraction they came from. For each node, split its text into claims (each number, model, comparator, direction and qualifier is a claim) and mark each one against the extraction's numbers and verbatim spans: `supported` (the words or numbers are there), `partly` (something is missing or changed, say what) or `unsupported` (not in the extraction or contradicted). Give the supporting words copied from the span. Mark the node `pass` only if every claim is supported. Be strict: a changed number, a missing comparator or a stronger verb is a failure. Return one JSON object and nothing else.

## Output (JSON only)
{"checks": [{"node": "E-F1", "claims": [{"claim": "", "verdict": "supported", "words": ""}], "overall": "pass", "fix": "what to change, if anything"}]}

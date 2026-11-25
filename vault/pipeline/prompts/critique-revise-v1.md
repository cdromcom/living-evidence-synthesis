---
type: prompt
id: critique-revise-v1
used_by: pipeline/scripts/lives_stages.py (draft, round 1; the three authors)
written: 2026-11-25
---

Three authors drafted discourse-graph nodes from the same extraction. You see all three drafts (labelled A, B and C, in random order; one is yours, but you are not told which) and the automatic lint results. Critique every draft, then write your own best revised version of every node. Work ONLY from the extraction. Return one JSON object and nothing else.

## Critique rules
- Judge accuracy first (every number, model name, comparator and direction must match the extraction's numbers and spans), then completeness (a comparator, the sample, the metric names), then length (EVD statements at most 247 characters), then readability (short active sentences, jargon explained), then little things (spelled-out metric names, rounding, consistent model names, no arrows or slashes).
- Each point names the draft, the node id, the problem, and the extraction field or span that shows it. Do not praise; list problems only. At most 12 points, most serious first.
- Then revise: for every node write the best version you can, taking the best parts of all drafts and fixing the problems. Keep the node ids and types. The same rules as the first round apply (EVD statement pattern, QUE canonical phrasings, one claim or limitation per node, verbatim quotes).

## Output (JSON only)
{"critiques": [{"draft": "A", "node": "E-F1", "problem": "", "evidence": "", "severity": "major"}],
 "revised": {"nodes": [ ...the same node objects as the first round... ]}}

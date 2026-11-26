---
type: prompt
id: vote-v1
used_by: pipeline/scripts/lives_stages.py (draft, vote; Sol and Sonnet decide, Neon breaks ties, Inkling logs a benchmark-only pick)
written: 2026-11-25
---

Three revised versions (A, B and C, in random order) of the same discourse-graph nodes are given with the extraction they come from. For each node choose the best version. Judge accuracy first (every number, model, comparator and direction supported by the extraction), then completeness, then length (EVD statements at most 247 characters), then readability. Do not prefer a version because it is longer. If two versions are equally good, pick the more accurate one. Return one JSON object and nothing else.

## Output (JSON only)
{"picks": [{"node": "E-F1", "pick": "B", "reason": "one sentence"}]}

---
type: prompt
id: vote-v2
used_by: pipeline/scripts/lives_stages.py (draft, vote; the voters named in pipeline/config/models.json, roles.voters, decide and roles.tiebreak breaks ties)
written: 2026-11-27
changes: v2 (JP, 2026-11-27) allows two versions (the original draft and the critic's revision) as well as three.
---

Two or three versions (labelled A, B, ... in random order) of the same discourse-graph nodes are given with the extraction they come from. For each node choose the best version. Judge accuracy first (every number, model, comparator and direction supported by the extraction), then completeness, then length (EVD statements at most 247 characters), then readability. Do not prefer a version because it is longer. If two versions are equally good, pick the more accurate one. Return one JSON object and nothing else.

## Output (JSON only)
{"picks": [{"node": "E-F1", "pick": "B", "reason": "one sentence"}]}

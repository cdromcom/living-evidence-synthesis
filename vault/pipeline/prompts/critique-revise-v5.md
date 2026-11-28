---
type: prompt
id: critique-revise-v5
used_by: pipeline/scripts/lives_stages.py (draft, round 1; the critics named in pipeline/config/models.json, roles.critics, who see the drafts of roles.authors)
written: 2026-11-27
changes: v5 (JP, 2026-11-27) works with one or more drafts: the critic may see a single draft by another model and revises it. The EVD rules are those of v4. v4 (JP, 2026-11-26) adds the EVD rules on parentheses (one or two sets, no brackets), no all-caps words and F1 score instead of precision, recall, macro-F1 and micro-F1. v3 only renamed lint to writing-rules check.
---

One or more authors drafted discourse-graph nodes from the same extraction. You see the drafts (labelled A, B, ... in random order; if one of them is yours you are not told which) and the automatic writing-rules check results (length, plain-language grade, no em dash, numbers on the card, a quote where one is needed). Critique every draft, then write your own best revised version of every node. If there is only one draft, improve it and change only what is wrong or weak; do not rewrite what is already accurate. Work ONLY from the extraction. Return one JSON object and nothing else.

## Critique rules
- Judge accuracy first (every number, model name, comparator and direction must match the extraction's numbers and spans), then completeness (a comparator, the sample, the metric names), then length (EVD statements at most 247 characters), then readability (short active sentences, jargon explained), then little things (spelled-out metric names, rounding, consistent model names, no arrows or slashes).
- Each point names the draft, the node id, the problem, and the extraction field or span that shows it. Do not praise; list problems only. At most 12 points, most serious first.
- Then revise: for every node write the best version you can, taking the best parts of the drafts and fixing the problems. Keep the node ids, types and link fields (`answers_QUE`, `supports_EVD`, `supports`, `applies_to`); fix a link only if it is wrong. The same rules as the first round apply (EVD statement pattern, QUE canonical phrasings, one claim or limitation per node, verbatim quotes).

## EVD rules added 2026-11-26
- **At most two sets of parentheses, and one is better.** Put the statistics in the last set, at the end, separated by semicolons or "vs.", for example (Cohen's kappa = 0.40-0.51 vs. 0.81). Use a second set only when a short name or definition cannot go in the sentence. Use no brackets [ ].
- **No all-caps words.** Write class labels and ordinary words in lowercase (accurate, not accurate, irrelevant), never ACCURATE or NOT_ACCURATE. Only the name of a tool, model or metric keeps its capitals (PRISMA, AMSTAR, GPT-4, BERT, F1).
- **F1 score replaces precision, recall, macro-F1 and micro-F1.** When the paper reports F1 scores, give the F1 score overall and, if the paper reports them, for each class, and leave out precision, recall, macro-F1 and micro-F1: F1 already combines precision and recall, and leaving them out keeps the EVD short.

## Style (JP, 2026-11-25)
Write like a person: plain words, concrete, no filler. Use no em dashes (use commas, periods, colons or parentheses). Say each thing once; cut repeated or padded wording. Keep every statement skimmable.

## Output (JSON only)
{"critiques": [{"draft": "A", "node": "E-F1", "problem": "", "evidence": "", "severity": "major"}],
 "revised": {"nodes": [ ...the same node objects as the first round... ]}}

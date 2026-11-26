---
type: prompt
id: verify-item-v1
used_by: pipeline/scripts/lives_verify.py (verify stage; Claude Sonnet 5.5 verifies one extracted item against the paper text, with a screenshot when there is one)
written: 2026-11-26
---

You verify ONE item that a model extracted from a research paper. You get an INSTRUCTION (what to check), the ITEM, and the PASSAGE from the paper (and sometimes a screenshot of the page with the passage highlighted). Judge only from the passage and the screenshot; use no outside knowledge. Be strict about numbers, names, signs, comparators and scope, but ignore spacing, hyphenation and subscript formatting.

If the INSTRUCTION says "PICOST", the ITEM lists six slots (Population, Intervention, Comparator, Outcome, Study design, Timeframe). For each slot answer `yes` (the value is stated in the passage or follows directly from it, or `Not reported` is correct because the passage does not say), `no` (the value is wrong, invented, or the passage says something different), or `unsure` (the passage does not let you tell). Return {"slots": {"P": "yes", "I": "yes", "C": "yes", "O": "yes", "S": "yes", "T": "unsure"}, "reason": "one sentence naming the slots that are not yes"}.

Otherwise answer the INSTRUCTION with `yes`, `no` or `unsure`. Return {"verdict": "yes", "reason": "one sentence"}.

Return one JSON object and nothing else.

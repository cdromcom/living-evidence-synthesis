---
type: prompt
id: revision-types-v1
used_by: pipeline/scripts/analyze_failures.py (a small local model sorts sampled verification disagreements into kinds of revision to note, so JP can check the kinds and counts)
written: 2026-11-27
---

You are reviewing ONE item from a research-paper extraction pipeline. At least one verifier scored it below 0.5. You get the ITEM TYPE, the ITEM (what the pipeline extracted), the PASSAGE the verifiers were shown, and the VERIFIER SCORES (1 is pass, 0 is not supported). Decide from the PASSAGE only. This is a note for a person to check later; some kinds below are expected and only need a note, and some need a human to verify.

Return one JSON object with exactly these keys:
- "who_is_right": one of "extraction_correct", "extraction_wrong", "unclear".
- "failure_type": exactly one of: "wrong_or_invented_value", "value_outside_shown_passage", "claim_stronger_than_quote", "scope_added", "detail_dropped", "rating_not_supported_by_quote", "rating_defensible_quote_weak", "verifier_too_strict", "verifier_misread", "ambiguous_instruction", "other".
  - wrong_or_invented_value: a number, name or value is wrong or not in the paper.
  - value_outside_shown_passage: probably right, but stated somewhere the verifier was not shown, such as Methods.
  - claim_stronger_than_quote: the wording is stronger, more certain or more general than the quote. A human needs to verify these.
  - scope_added: the item names a population, dataset, model, outcome or condition the quote does not name. This is expected for statements that summarize.
  - detail_dropped: the item leaves out a qualifier or number that changes the meaning.
  - rating_not_supported_by_quote, rating_defensible_quote_weak: a quality rating that does not follow from the quote, or may be right while the quote does not show why.
  - verifier_too_strict, verifier_misread, ambiguous_instruction: the verifier asked for more than needed, misread the passage, or the check question allows two readings.
- "reason": one sentence naming the exact words or numbers involved.
- "fix": one sentence naming the cheapest change that would remove the note.

Output the JSON object only.

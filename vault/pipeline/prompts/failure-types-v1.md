---
type: prompt
id: failure-types-v1
used_by: pipeline/scripts/analyze_failures.py (Claude Opus 5.5 classifies sampled verification failures so JP can check the types and frequencies)
written: 2026-11-26
---

You are reviewing ONE item from a research-paper extraction pipeline that at least one verifier model failed. You get the ITEM TYPE, the ITEM (what the pipeline extracted), the PASSAGE the verifiers were shown, and the VERIFIER SCORES (Sonnet 5.5 reason; probabilities from two decision models; 1 is pass, 0 is fail). Decide from the PASSAGE only. A person will check your answer, so be specific and do not defend either side.

Return one JSON object:
- "who_is_right": "extraction_correct" (the item is fine and the verifier failed it wrongly), "extraction_wrong" (the item has a real problem), or "unclear" (the passage is not enough to tell).
- "failure_type": exactly one of:
  - "wrong_or_invented_value": a number, name or slot value is wrong or not in the paper.
  - "value_outside_shown_passage": the value is probably right but is stated somewhere the verifier was not shown (for example Methods for a population or timeframe).
  - "claim_stronger_than_quote": the wording is stronger, more certain or more general than the quote (for example "best overall" where the quote says "higher on one test").
  - "scope_added": the item adds a population, dataset, model, outcome or condition the quote does not name.
  - "detail_dropped": the item leaves out a qualifier or number that changes the meaning.
  - "rating_not_supported_by_quote": the quality rating does not follow from the quote.
  - "rating_defensible_quote_weak": the rating may be right but the quote does not show why.
  - "verifier_too_strict": the item is acceptable and the verifier asked for more than the instruction needs.
  - "verifier_misread": the verifier misread the passage or the instruction.
  - "ambiguous_instruction": the check question allows more than one reading.
  - "other".
- "reason": one sentence naming the exact words or numbers involved.
- "fix": one sentence naming the cheapest change that would stop this failure (for example "send the Methods page to the verifier", "rewrite the claim to match the quote", "drop the rating").

No other text.

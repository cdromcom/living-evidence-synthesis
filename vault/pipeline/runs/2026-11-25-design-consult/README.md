# Design consult, 2026-11-25

One-page design and dev summary (`pipeline/prompts/design-consult-v1.md`) sent to Claude Fable 5.2 and GPT-6.2 Sol for a high-level critique; both critiques then went, with the summary, to Claude Opus 5.5 and Claude Sonnet 5.5, which each wrote a revised plan (`pipeline/prompts/design-enhance-v1.md`). All four calls are in `calls.jsonl` (model, effort, time, prompt link and hash, tokens, cost). Measured cost: Fable 5.2 about $0.24, Opus 5.5 about $0.15, Sonnet 5.5 about $0.06; GPT-6.2 Sol 966 tokens in and 997 out, price not confirmed.

Both critiques agreed on: verification path first (CLM and EVD templates), caveat beside the finding, domain rows instead of a strong-and-weak tally with "not reported", "not applicable" and "judges split" kept apart, graph as an optional list-first view, tests and gates from phase 1, a library combobox, the resize handle cut, focus rules on route change, and cite, report-error, last-updated and print support. Provenance moves up into a byline under the title as well as the footer.
Files: `design-consult-*.md` (critiques), `design-improve-*.md` (revised plans).

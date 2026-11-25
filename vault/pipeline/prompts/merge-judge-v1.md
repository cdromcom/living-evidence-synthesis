# Merge judge for two discourse-graph nodes (v1, 2026-11-25)

You compare two nodes from an evidence graph about whether large language models can help review scientific papers. Both nodes have the same type (a Question, a Claim, a Caveat, an Evidence item or a Pattern). Decide whether they should be merged into one node.

Rules:
- Merge only when the two nodes say the same thing about the same subject, so that one page could replace both without losing any detail. Do not merge if they differ in a number, a named model, a dataset, a population, a condition, a direction (more or less) or a negation, even if the wording is close.
- "Group under an umbrella" means the nodes are different but share a theme that a parent node could cover (for example, two datasets that are both limited to machine-learning conference papers).
- Judge only from the text given. Do not guess what a paper says.
- Say what differs, if anything, in the shortest plain words.

Answer with JSON only, no other text:
{"verdict": "merge" | "keep_separate" | "group_under_umbrella", "differences": ["..."], "reason": "one sentence, at most 30 words"}

Node A:
{A}

Node B:
{B}

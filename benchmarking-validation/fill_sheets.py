#!/usr/bin/env python3
"""Build the K:W answer block (77 rows) for each model-only GSheet from results/<provider>.<run>.jsonl."""
import json, sys
RUN = sys.argv[2] if len(sys.argv) > 2 else "r1"
prov = sys.argv[1]
VER = {"perplexity": "pplx-decider-v1.3", "liquid": "d1-ultra", "jev": "jev-1.14.0"}[prov]
R = {}
for r in map(json.loads, open(f"results/{prov}.{RUN}.jsonl")):
    if not r.get("error") and r.get("answers"): R[(r["evd"], r["task"])] = r
def pct(x): return f"{x:.2f}"
rows = []
for e in range(1, 78):
    rel = R[(e, "relevancy")]["answers"]["relevant"]["noul"]
    row = ["Relevant" if rel >= .5 else "Irrelevant", pct(rel), f"P(Relevant) = {pct(rel)}"]
    f = R.get((e, "fidelity"))
    if f:
        c = f["answers"]["fidelity"]; allnum = f["answers"]["all_numbers_in_quote"]["noul"]
        pr = c["probabilities"]
        row += [c["choice"], pct(allnum), "Met %s | Partially Met %s | Unmet %s" % tuple(pct(pr.get(k, 0)) for k in ("Met", "Partially Met", "Unmet"))]
    else:
        row += ["", "", "Used as a worked example in the fidelity prompt; excluded from held-out comparisons."]
    q = R[(e, "quote")]["answers"]; c = q["quote_grounding"]; sh = q.get("screenshot_shows_quote", {}).get("noul")
    row += [c["choice"], pct(sh) if sh is not None else "", ""]
    t = R[(e, "table")]
    if t.get("rule_based"):
        row += ["Missing", "Rule: no table/figure screenshot shown, so Missing (no model call)."]
    else:
        c = t["answers"]["table_fig_grounding"]; pr = c["probabilities"]
        row += [c["choice"], " | ".join(f"{k} {pct(v)}" for k, v in sorted(pr.items(), key=lambda kv: -kv[1])[:3])]
    row += [f"{R[(e, 'quote')].get('images_sent', 0) + (R[(e, 'table')].get('images_sent', 0) if not t.get('rule_based') else 0)} image(s) over quote+table tasks", f"{VER}; run {RUN}; 2026-11-24 UTC"]
    rows.append(row)
json.dump(rows, open(f"sheets/fill_{prov}.json", "w"), ensure_ascii=False)
print(prov, len(rows), "rows x", len(rows[0]), "cols,", sum(len(json.dumps(r)) for r in rows), "chars")

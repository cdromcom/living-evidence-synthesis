#!/usr/bin/env python3
"""Error analysis of Run 2 (r2t = r2 relevancy/fidelity/quote + table/figure rerun) for all four raters against JP, and Run 1 vs Run 2 change.
ANALYSIS ONLY (reads reference/reference.csv). Writes results/error-analysis-r2t.md. Held-out EVD 4-77."""
import csv, json
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
P = {"perplexity": "Perplexity", "liquid": "Liquid", "jev": "Jev", "opus": "Opus 5.5"}
ref = {int(r["EVD"]): r for r in csv.DictReader(open(HERE / "reference/reference.csv")) if r["EVD"].isdigit()}
col = {"relevancy": "jp_relevancy", "fidelity": "jp_fidelity", "quote": "jp_quote", "table": "jp_tablefig"}
key = {"fidelity": "fidelity", "quote": "quote_grounding", "table": "table_fig_grounding"}
def load(p, runs):
    R = {}
    for run in runs:
        f = HERE / f"results/{p}.{run}.jsonl"
        if not f.exists(): continue
        for r in map(json.loads, open(f)):
            if r.get("error") or not r.get("answers"): continue
            A = r["answers"]
            R[(r["evd"], r["task"])] = ("Relevant" if A["relevant"]["noul"] >= .5 else "Irrelevant") if r["task"] == "relevancy" else A[key[r["task"]]]["choice"]
    return R
R1 = {p: load(p, ["r1", "r1fix"]) for p in P}; R2 = {p: load(p, ["r2t"]) for p in P}
held = range(4, 78)
EXC = {k: set(v["evds"]) for k, v in json.load(open(HERE / "inputs/exclusions.json")).items() if isinstance(v, dict)}
jp = lambda e, t: (ref[e][col[t]] or None) if ref[e][col[t]] != "NA" else None
out = ["# Error analysis, Run 2 (r2t) and change from Run 1", "",
       "Held-out EVD 4-77 after JP's exclusions of 2026-11-24 (inputs/exclusions.json): relevancy n=68 (EVD 7, 17, 49, 72, 75, 76 dropped), fidelity n=66 (EVD 4, 19, 26, 36, 38, 54, 56, 65 dropped), quote n=66 (EVD 5, 6, 9, 18, 45, 51, 53, 66 dropped pending JP re-rating), table/figure n=72 (two JP NA rows excluded). The earlier all-rows analysis is in the previous commit and in results/metrics-*-all.json. JP = reference. r2t = Run 2 relevancy, fidelity and quote plus the table/figure rerun with Missing-by-rule when the page has no table/figure-slot screenshot. Run 1 uses r1 with the r1fix overrides for EVD 21 and 38.", ""]
for t in ("relevancy", "fidelity", "quote", "table"):
    ev = [e for e in held if jp(e, t) and e not in EXC.get(t, set())]
    out += [f"## {t}", "", f"JP labels (n={len(ev)}): {dict(Counter(jp(e, t) for e in ev))}", "",
            "| Rater | Run 1 correct | Run 2 correct | Changed label | Moved toward JP | Moved away from JP | Run 2 error types (JP -> model) |", "|---|---|---|---|---|---|---|"]
    wrong2 = {}
    for p, n in P.items():
        a1 = [e for e in ev if R1[p].get((e, t)) == jp(e, t)]; a2 = [e for e in ev if R2[p].get((e, t)) == jp(e, t)]
        ch = [e for e in ev if R1[p].get((e, t)) != R2[p].get((e, t))]
        tw = [e for e in ch if R2[p].get((e, t)) == jp(e, t)]; aw = [e for e in ch if R1[p].get((e, t)) == jp(e, t)]
        wrong2[p] = {e for e in ev if R2[p].get((e, t)) != jp(e, t)}
        conf = Counter((jp(e, t), R2[p].get((e, t))) for e in wrong2[p])
        out.append(f"| {n} | {len(a1)}/{len(ev)} | {len(a2)}/{len(ev)} | {len(ch)} | {len(tw)} | {len(aw)} | " + "; ".join(f"{a}->{b} x{c}" for (a, b), c in conf.most_common(4)) + " |")
    allw = set.intersection(*wrong2.values()); anyw = set.union(*wrong2.values())
    out += ["", f"Wrong in all four raters in Run 2: {len(allw)} EVDs {sorted(allw)}. Wrong in at least one: {len(anyw)}. Wrong in exactly one: {len([e for e in anyw if sum(e in wrong2[p] for p in P) == 1])}.", ""]
    if t == "table":
        out += ["Rows a model actually judged in Run 2 (the rule decides the rest): " + ", ".join(f"EVD {e}: JP {jp(e,t)} / models {[R2[p][(e,t)] for p in P]}" for e in sorted(ev) if len({R2[p][(e, t)] for p in P}) > 1 or R2['jev'][(e, t)] != 'Missing'), ""]
        out += ["JP Missing but the page has a table/figure-slot screenshot and models said Correct: " + str(sorted(e for e in ev if jp(e, t) == "Missing" and R2["jev"][(e, t)] == "Correct")),
                "JP non-Missing but the rule said Missing (no table/figure-slot screenshot): " + str(sorted(e for e in ev if jp(e, t) != "Missing" and R2["jev"][(e, t)] == "Missing")), ""]
    if t == "quote":
        out += ["Run 2 quote: JP Correct but model not Correct, per rater: " + "; ".join(f"{n} {sorted(e for e in ev if jp(e,t)=='Correct' and R2[p][(e,t)]!='Correct')}" for p, n in P.items()), ""]
    if t == "fidelity":
        out += ["Run 2 fidelity: model Partially Met/Unmet where JP Met, per rater: " + "; ".join(f"{n} {len([e for e in ev if jp(e,t)=='Met' and R2[p][(e,t)]!='Met'])}" for p, n in P.items()), ""]
    if t == "relevancy":
        out += ["Run 2 relevancy errors per rater: " + "; ".join(f"{n} {sorted(wrong2[p])}" for p, n in P.items()), ""]
Path(HERE / "results/error-analysis-r2t.md").write_text("\n".join(out)); print("\n".join(out))

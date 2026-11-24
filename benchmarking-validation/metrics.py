#!/usr/bin/env python3
"""Accuracy, raw ratio, Cohen's kappa, F1 (macro, micro, weighted) and confusion matrices for every rater and ensemble
against JP on the held-out EVDs (4-77). Also tokens, time and cost per model and run. Writes results/metrics-<run>.json.
ANALYSIS ONLY: reads reference/reference.csv."""
import csv, json, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
RUN = sys.argv[1] if len(sys.argv) > 1 else "r1"
NAMES = {"perplexity": "Perplexity Decider 1.3", "liquid": "Liquid d1-ultra", "jev": "Jev", "opus": "Claude Opus 5.5"}
TASKS = ["relevancy", "fidelity", "quote", "table"]
LABELS = {"relevancy": ["Relevant", "Irrelevant"], "fidelity": ["Met", "Partially Met", "Unmet"],
          "quote": ["Correct", "Partially Correct", "Incorrect", "Missing", "NA"], "table": ["Correct", "Partially Correct", "Incorrect", "Missing", "NA"]}
REFCOL = {"relevancy": "jp_relevancy", "fidelity": "jp_fidelity", "quote": "jp_quote", "table": "jp_tablefig"}
ref = {int(r["EVD"]): r for r in csv.DictReader(open(HERE / "reference/reference.csv"))}
def dist(task, a):                       # probability distribution over labels for one answer block
    if task == "relevancy":
        p = a["relevant"]["noul"]; return {"Relevant": p, "Irrelevant": 1 - p}
    k = {"fidelity": "fidelity", "quote": "quote_grounding", "table": "table_fig_grounding"}[task]
    d = a[k]["probabilities"]; z = sum(d.values()) or 1; return {l: d.get(l, 0) / z for l in LABELS[task]}
D = {p: {} for p in NAMES}
for p in NAMES:
    files = [HERE / f"results/{p}.{RUN}.jsonl"] + sorted((HERE / "results").glob(f"{p}.{RUN}fix*.jsonl"))   # fix runs override same EVD+task
    for f in files:
        if not f.exists(): continue
        for r in map(json.loads, open(f)):
            if not r.get("error") and r.get("answers"): D[p][(r["evd"], r["task"])] = dist(r["task"], r["answers"])
def argmax(d): return max(d, key=d.get)
ENS = {"Average of Perplexity + Liquid + Opus": ["perplexity", "liquid", "opus"], "Average of Perplexity + Liquid + Jev": ["perplexity", "liquid", "jev"],
       "Average of all four": ["perplexity", "liquid", "jev", "opus"]}
pred = {NAMES[p]: {k: argmax(v) for k, v in D[p].items()} for p in NAMES if D[p]}
for name, members in ENS.items():
    if all(D[m] for m in members):
        pred[name] = {k: argmax({l: sum(D[m][k][l] for m in members) / len(members) for l in LABELS[k[1]]}) for k in D[members[0]] if all(k in D[m] for m in members)}
def majority(members):
    out = {}
    for k in D[members[0]]:
        v = Counter(argmax(D[m][k]) for m in members if k in D[m]); lab, c = v.most_common(1)[0]
        out[k] = lab if c >= 2 else "TIE"
    return out
if all(D[m] for m in ("perplexity", "liquid", "opus")): pred["Majority vote of Perplexity + Liquid + Opus"] = majority(["perplexity", "liquid", "opus"])
if all(D[m] for m in ("perplexity", "liquid", "jev")): pred["Majority vote of Perplexity + Liquid + Jev"] = majority(["perplexity", "liquid", "jev"])
def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")
def f1s(y, p):
    labs = sorted(set(y) | set(p)); tp = {l: sum(a == b == l for a, b in zip(y, p)) for l in labs}
    f = {}; sup = Counter(y)
    for l in labs:
        pr = tp[l] / max(1, sum(b == l for b in p)); rc = tp[l] / max(1, sup[l]); f[l] = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    macro = sum(f.values()) / len(f); micro = sum(tp.values()) / len(y)      # micro-F1 = accuracy for single-label multiclass
    weighted = sum(f[l] * sup[l] for l in labs) / len(y)
    return macro, micro, weighted
held = range(4, 78); res = {}
for task in TASKS:
    ev = [e for e in held if ref[e][REFCOL[task]] not in ("", "NA")]
    y = [ref[e][REFCOL[task]] for e in ev]; base = Counter(y).most_common(1)[0]
    res[task] = {"n": len(ev), "baseline": {"label": base[0], "correct": base[1], "accuracy": base[1] / len(ev)}, "raters": {}}
    for name, P in pred.items():
        p = [P.get((e, task), "MISSING") for e in ev]
        if "MISSING" in p: continue
        macro, micro, w = f1s(y, p); corr = sum(a == b for a, b in zip(y, p))
        cm = {a: {b: sum(1 for t, q in zip(y, p) if t == a and q == b) for b in sorted(set(p) | set(LABELS[task]))} for a in LABELS[task]}
        res[task]["raters"][name] = {"correct": corr, "n": len(ev), "accuracy": corr / len(ev), "kappa": kappa(y, p), "f1_macro": macro, "f1_micro": micro, "f1_weighted": w, "confusion": cm}
# tokens, time, cost per model and run
PRICE = {"perplexity": 0.02, "liquid": 0.042, "jev": 0.042}
usage = []
for p in NAMES:
    for f in sorted((HERE / "results").glob(f"{p}.*.jsonl")):
        R = [json.loads(l) for l in open(f)]
        tok = sum((r.get("usage") or {}).get("input_tokens", 0) for r in R); lat = sum(r.get("latency_s") or 0 for r in R)
        cost = sum((r.get("usage") or {}).get("cost", 0) for r in R)
        usage.append({"model": NAMES[p], "run": f.name.split(".")[1], "records": len(R), "model_calls": sum(1 for r in R if not r.get("rule_based")),
                      "input_tokens": tok, "request_time_s": round(lat, 1), "cost_usd": round(cost if cost else tok / 1e6 * PRICE.get(p, 0), 4),
                      "cost_source": "API-reported" if cost else ("computed from list price" if p in PRICE else "see notes")})
json.dump({"run": RUN, "tasks": res, "usage": usage}, open(HERE / f"results/metrics-{RUN}.json", "w"), indent=1)
for task in TASKS:
    print(f"\n{task}  n={res[task]['n']}  baseline {res[task]['baseline']['label']} {res[task]['baseline']['accuracy']:.1%}")
    for name, m in res[task]["raters"].items():
        print(f"  {name:<46} {m['correct']:>2}/{m['n']} acc {m['accuracy']:.1%}  kappa {m['kappa']:.2f}  F1 macro {m['f1_macro']:.2f} micro {m['f1_micro']:.2f} weighted {m['f1_weighted']:.2f}")

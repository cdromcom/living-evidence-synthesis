#!/usr/bin/env python3
"""Agreement between all raters (every pair), per task: % agreement and Cohen's kappa.

Raters: the three AI models (from results/<provider>.<run-id>.jsonl) plus JP and Claude (from
reference/reference.csv, ANALYSIS ONLY). Run this AFTER the models have judged, never before.

  python3 -I agreement.py                        # judgment run r1
  python3 -I agreement.py --run-id r1 --stability r2   # also each model's r1 vs r2 repeat agreement
Writes results/agreement.csv (long format) and prints a matrix per task.
"""
import argparse, csv, itertools, json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES, REF = HERE / "results", HERE / "reference" / "reference.csv"
PROVIDERS = {"perplexity": "Perplexity Decider 1.3", "liquid": "Liquid d1-ultra", "jev": "Jev"}
TASKS = {"relevancy": {"Relevant", "Irrelevant"},
         "fidelity": {"Met", "Partially Met", "Unmet", "NA"},
         "quote": {"Correct", "Partially Correct", "Incorrect", "Missing", "NA"},
         "tablefig": {"Correct", "Partially Correct", "Incorrect", "Missing", "NA"}}


def model_labels(provider, run):
    f = RES / f"{provider}.{run}.jsonl"
    out = {t: {} for t in TASKS}
    if not f.exists():
        return out
    for r in map(json.loads, f.read_text().splitlines()):
        if r.get("error") or not r.get("answers"):
            continue
        A, e = r["answers"], r["evd"]
        if r["task"] == "relevancy":
            out["relevancy"][e] = "Relevant" if A["relevant"]["noul"] >= 0.5 else "Irrelevant"
        elif r["task"] == "fidelity":
            out["fidelity"][e] = A["fidelity"]["choice"]
        elif r["task"] == "quote":
            out["quote"][e] = A["quote_grounding"]["choice"]
        elif r["task"] == "table":
            out["tablefig"][e] = A["table_fig_grounding"]["choice"]
    return out


def kappa(a, b):
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="r1")
    ap.add_argument("--stability", default="", help="second run id to compare each model against its own --run-id")
    ap.add_argument("--no-claude", action="store_true")
    ap.add_argument("--exclude", default="1-3", help="EVDs left out of every comparison (the worked-example EVDs); '' to keep all")
    a = ap.parse_args()
    skip = set()
    for part in filter(None, a.exclude.split(",")):
        lo, _, hi = part.partition("-")
        skip |= set(range(int(lo), int(hi or lo) + 1))
    raters = {t: {} for t in TASKS}
    for pv, name in PROVIDERS.items():
        L = model_labels(pv, a.run_id)
        for t in TASKS:
            if L[t]:
                raters[t][name] = L[t]
    if REF.exists():
        rows = list(csv.DictReader(open(REF)))
        for who in ("jp",) + (() if a.no_claude else ("claude",)):
            for t in TASKS:
                d = {int(r["EVD"]): r[f"{who}_{t}"] for r in rows if r[f"{who}_{t}"] in TASKS[t]}
                raters[t]["JP (human expert)" if who == "jp" else "Claude Opus 5.5"] = d
    for t in TASKS:
        for nm in raters[t]:
            raters[t][nm] = {e: v for e, v in raters[t][nm].items() if e not in skip}
    print(f"Held-out comparison: EVDs {sorted(skip) or 'none'} excluded")
    out = []
    for t in TASKS:
        names = list(raters[t])
        print(f"\n=== {t}: % agreement (kappa), n ===")
        for x, y in itertools.permutations(names, 2):
            ev = sorted(set(raters[t][x]) & set(raters[t][y]))
            la, lb = [raters[t][x][e] for e in ev], [raters[t][y][e] for e in ev]
            ag = sum(p == q for p, q in zip(la, lb))
            k = kappa(la, lb)
            out.append({"task": t, "rater_a": x, "rater_b": y, "n": len(ev), "agree": ag,
                        "pct": round(100 * ag / len(ev), 1) if ev else "", "kappa": round(k, 2) if k is not None else ""})
        for x, y in itertools.combinations(names, 2):
            r = [o for o in out if o["task"] == t and o["rater_a"] == x and o["rater_b"] == y][0]
            print(f"  {x:<26} vs {y:<26} {r['pct']}% (kappa {r['kappa']}), n={r['n']}")
        if all(p in raters[t] for p in PROVIDERS.values()):
            ev = sorted(set.intersection(*[set(raters[t][p]) for p in PROVIDERS.values()]))
            un = sum(len({raters[t][p][e] for p in PROVIDERS.values()}) == 1 for e in ev)
            print(f"  all three models unanimous: {un}/{len(ev)}")
            out.append({"task": t, "rater_a": "all 3 models", "rater_b": "unanimous", "n": len(ev), "agree": un,
                        "pct": round(100 * un / len(ev), 1) if ev else "", "kappa": ""})
    if a.stability:
        print(f"\n=== stability: each model's {a.run_id} vs {a.stability} ===")
        for pv, name in PROVIDERS.items():
            A_, B_ = model_labels(pv, a.run_id), model_labels(pv, a.stability)
            for t in TASKS:
                ev = sorted(set(A_[t]) & set(B_[t]))
                if not ev:
                    continue
                ag = sum(A_[t][e] == B_[t][e] for e in ev)
                k = kappa([A_[t][e] for e in ev], [B_[t][e] for e in ev])
                print(f"  {name:<24} {t:<10} {ag}/{len(ev)} same label" + (f" (kappa {k:.2f})" if k is not None else ""))
                out.append({"task": t, "rater_a": f"{name} {a.run_id}", "rater_b": f"{name} {a.stability}", "n": len(ev),
                            "agree": ag, "pct": round(100 * ag / len(ev), 1), "kappa": round(k, 2) if k is not None else ""})
    RES.mkdir(exist_ok=True)
    with open(RES / "agreement.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["task", "rater_a", "rater_b", "n", "agree", "pct", "kappa"])
        w.writeheader(); w.writerows(out)
    print(f"\nWrote {RES / 'agreement.csv'}")


if __name__ == "__main__":
    main()

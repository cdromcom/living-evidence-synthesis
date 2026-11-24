#!/usr/bin/env python3
"""Error analysis of the three decision models against JP on the held-out EVDs (4-77). ANALYSIS ONLY.

Writes results/error-analysis-<run>.md. Needs results/<provider>.<run>.jsonl and reference/reference.csv
(JP's and Claude's ratings and notes, made with reference/extract_reference.py)."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
RUN = sys.argv[1] if len(sys.argv) > 1 else "r1"
P = {"perplexity": "Perplexity Decider 1.3", "liquid": "Liquid d1-ultra", "jev": "Jev"}
ref = {int(r["EVD"]): r for r in csv.DictReader(open(HERE / "reference/reference.csv"))}
packets = {n: json.load(open(HERE / f"packets/EVD-{n:02d}/packet.json")) for n in range(1, 78)}
col = {"relevancy": "jp_relevancy", "fidelity": "jp_fidelity", "quote": "jp_quote", "table": "jp_tablefig"}
R = {p: {} for p in P}
for p in P:
    for r in map(json.loads, open(HERE / f"results/{p}.{RUN}.jsonl")):
        if r.get("error") or not r.get("answers"): continue
        A, e, t = r["answers"], r["evd"], r["task"]
        if t == "relevancy": R[p][(e, t)] = ("Relevant" if A["relevant"]["noul"] >= .5 else "Irrelevant", A["relevant"]["noul"], A)
        elif t == "fidelity": R[p][(e, t)] = (A["fidelity"]["choice"], A["fidelity"]["probabilities"].get(A["fidelity"]["choice"]), A)
        elif t == "quote": R[p][(e, t)] = (A["quote_grounding"]["choice"], A.get("screenshot_shows_quote", {}).get("noul"), A)
        else: R[p][(e, t)] = (A["table_fig_grounding"]["choice"], A["table_fig_grounding"]["confidence"], A)
held = range(4, 78)
def jp(e, t): 
    v = ref[e][col[t]]; return v if v and v != "NA" else None
MISMATCH = re.compile(r"different passage|does not show|not show the quot|shows a different|mismatch|not the (?:quoted|relevant)|not highlight|shows the next|shows only|screenshot shows", re.I)
out = [f"# Error analysis, run {RUN}", "", "Held-out EVD 4-77 (74 EVDs; table/figure n=72 because two JP NA rows are excluded). JP = reference. Models see only the sheet content.", ""]
def errs(p, t):
    return [e for e in held if jp(e, t) and (e, t) in R[p] and R[p][(e, t)][0] != jp(e, t)]
for t in ("relevancy", "fidelity", "quote", "table"):
    out += [f"## {t}", ""]
    ev = [e for e in held if jp(e, t)]
    out += [f"JP labels: {dict(Counter(jp(e, t) for e in ev))}", ""]
    for p, name in P.items():
        E = errs(p, t); conf = Counter((jp(e, t), R[p][(e, t)][0]) for e in E)
        out += [f"### {name}: {len(E)} errors of {len(ev)} ({100*(len(ev)-len(E))/len(ev):.0f}% agreement)", "",
                "Error types (JP label -> model label): " + "; ".join(f"{a}->{b} x{c}" for (a, b), c in conf.most_common()), ""]
        if t == "relevancy":
            border = [e for e in E if abs(R[p][(e, t)][1] - .5) < .2]
            out += [f"- {len(border)} of {len(E)} errors are borderline (P within 0.2 of 0.5).",
                    f"- Wrong EVDs: {sorted(E)}", ""]
        elif t == "fidelity":
            low_num = [e for e in E if R[p][(e, t)][2]["all_numbers_in_quote"]["noul"] < .5]
            strict = [e for e in E if R[p][(e, t)][0] != "Met" and jp(e, t) == "Met"]
            out += [f"- {len(strict)} of {len(E)} errors are the model calling Partially Met/Unmet where JP said Met; in {len([e for e in strict if e in low_num])} of those the model also says not every number in the EVD is in the quote (it is applying a numbers-in-the-quote test that JP's gist rule does not require).",
                    f"- Model Partially Met/Unmet total: {sum(1 for e in held if (e,t) in R[p] and R[p][(e,t)][0]!='Met')} vs JP {sum(1 for e in ev if jp(e,t)!='Met')}.",
                    f"- Wrong EVDs: {sorted(E)}", ""]
        elif t == "quote":
            inc_cor = [e for e in E if R[p][(e, t)][0] == "Incorrect" and jp(e, t) == "Correct"]
            cl_note = [e for e in inc_cor if (ref[e].get("claude_quote_mismatch_flag") == "1" if "claude_quote_mismatch_flag" in ref[e] else bool(MISMATCH.search(ref[e].get("claude_quote_note", ""))))]
            sure = [e for e in inc_cor if (R[p][(e, t)][1] is not None and R[p][(e, t)][1] < .2)]
            out += [f"- {len(inc_cor)} errors are the model saying Incorrect where JP said Correct; the model was confident the screenshot does not show the quote (P<0.2) in {len(sure)}, and Claude's earlier note also reports a mismatched/different passage in {len(cl_note)}. These are likely JP-rule inconsistencies (JP rated verbatim quotes with mismatched screenshots Correct before the 2026-11-23 rule), not model errors: {sorted(cl_note)}.",
                    f"- Wrong EVDs: {sorted(E)}", ""]
        else:
            out += [f"- Wrong EVDs: {sorted(E)}  (JP vs model on EVDs with a table image: " + ", ".join(f"EVD {e}: JP {jp(e,t)} / model {R[p][(e,t)][0]}" for e in ev if packets[e]['images'] and any(i['kind']=='tablefig' for i in packets[e]['images'])) + ")", ""]
    wrong = {p: set(errs(p, t)) for p in P}
    allw = set.intersection(*wrong.values()); anyw = set.union(*wrong.values())
    out += [f"**Shared errors:** wrong in all three models: {len(allw)} EVDs {sorted(allw)}; wrong in at least one: {len(anyw)}; wrong in exactly one: {len([e for e in anyw if sum(e in wrong[p] for p in P)==1])}.", ""]
# fidelity detail for the all-three-wrong rows
out += ["## Rows wrong in all three models (fidelity)", ""]
fw = set.intersection(*[set(errs(p, "fidelity")) for p in P])
for e in sorted(fw):
    labs = {P[p][:4]: R[p][(e, "fidelity")][0] for p in P}
    out += [f"- EVD {e} ({packets[e]['evd_statement'][:90]}): models {labs}; JP {jp(e,'fidelity')}; Claude {ref[e]['claude_fidelity']}"]
Path(HERE / f"results/error-analysis-{RUN}.md").write_text("\n".join(out))
print("\n".join(out))

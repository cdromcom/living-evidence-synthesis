#!/usr/bin/env python3
"""Build the answer block (columns L..X, rows 2-78) of a Run tab from results/<provider>.<run>.jsonl, as an xlsx with a tab named 'tmp'.
The tab is copied into the GSheet and pasted over the Run tab's answer columns (values only). Usage: make_run_fill.py <provider> <run>"""
import json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
HERE = Path(__file__).resolve().parent
prov, run = sys.argv[1], sys.argv[2]
VER = {"perplexity": "pplx-decider-v1.3", "liquid": "d1-ultra", "jev": "jev-1.14.0", "opus": "claude-opus-5-5 (Claude Code subagent)"}[prov]
R = {}
EXC = json.load(open(HERE / "inputs/exclusions.json"))
for r in map(json.loads, open(HERE / f"results/{prov}.{run}.jsonl")):
    if not r.get("error") and r.get("answers"): R[(r["evd"], r["task"])] = r
f = lambda x: round(float(x), 2)
def shots(a): return ", ".join(f"S{k} {f(a[f'shot{k}_connects_to_quote']['noul'])}" for k in range(1, 9) if f"shot{k}_connects_to_quote" in a)
wb = Workbook(); ws = wb.active; ws.title = "tmp"
for e in range(1, 78):
    row = {}
    rel = R[(e, "relevancy")]; p = rel["answers"]["relevant"]["noul"]
    row[12] = "Relevant" if p >= .5 else "Irrelevant"; row[13] = f(p); row[14] = rel.get("reason", "")
    fi = R.get((e, "fidelity"))
    if fi:
        c = fi["answers"]["fidelity"]; pr = c["probabilities"]
        row[15] = c["choice"]; row[16] = f(fi["answers"]["all_numbers_in_quote"]["noul"]) if "all_numbers_in_quote" in fi["answers"] else ""
        row[17] = fi.get("reason") or "Met %.2f; Partially Met %.2f; Unmet %.2f" % (pr.get("Met", 0), pr.get("Partially Met", 0), pr.get("Unmet", 0))
    else:
        row[15] = "test data - ignored"
    q = R[(e, "quote")]; qa = q["answers"]
    row[18] = qa["quote_grounding"]["choice"]; row[19] = f(qa["screenshot_shows_quote"]["noul"]) if "screenshot_shows_quote" in qa else ""
    row[20] = q.get("reason", "")                                    # Opus reason; blank for the decision models (light-red column is for page-number flags)
    t = R[(e, "table")]; ta = t["answers"]; tc = ta["table_fig_grounding"]
    row[21] = tc["choice"]
    row[22] = t.get("reason") or (" | ".join(f"{k} {v:.2f}" for k, v in sorted(tc.get("probabilities", {}).items(), key=lambda kv: -kv[1])[:3]) + (" (rule: no screenshot)" if t.get("rule_based") else ""))
    n = q.get("images_sent", t.get("images_sent", ""))
    row[23] = (f"{n} screenshot(s); connects to quote, quote task: {shots(qa)}; table task: {shots(ta)}").strip()
    row[24] = f"{VER}; run {run if run != 'r7' else 'r7 (published as Run 6)'}; 2026-11-24 UTC" + (" (relevancy/fidelity/quote = r2; table/figure rerun with Missing-by-rule when no table/figure-slot screenshot)" if run=="r2t" else "") + (" (quote re-run with the strict definitions; relevancy/fidelity/table = r2t)" if run=="r3" else "") + (" (fidelity v4 and quote v4 prompts; relevancy and table/figure = r3)" if run=="r4" else "") + ((" (repeat of Run 4 prompts, all four tasks)" if prov != "opus" else " (carried over from r4; Opus not re-run)") if run=="r5" else "") + ((" (relevancy and fidelity re-run for Perplexity, Liquid, Jev, carried from r5 for Opus; quote v7 and table/figure v7 wording, no slot rule)") if run=="r7" else "")
    for task, c0 in (("relevancy", 12), ("fidelity", 15), ("quote", 18), ("table", 21)):
        if e in EXC[task]["evds"]:
            row[c0] = "dropped from analysis (JP)"; row[c0 + 1] = ""; row[c0 + 2] = ""
    for col, v in row.items(): ws.cell(e + 1, col, v)
wb.save(HERE / f"sheets/fill-{prov}-{run}.xlsx"); print(prov, run, "ok")

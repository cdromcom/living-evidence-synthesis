#!/usr/bin/env python3
"""Build the 'Decision Models Summary' tab (xlsx) from results/metrics-<run>.json: metrics tables, ensemble comparison,
colour-coded confusion matrices (colour-blind-friendly pastel blue = agreement, pastel orange = disagreement), and
tokens / time / cost notes. Static values, computed by metrics.py; upload and copy into the main GSheet."""
import json, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
HERE = Path(__file__).resolve().parent
RUN = sys.argv[1] if len(sys.argv) > 1 else "r1"
M = json.loads((HERE / f"results/metrics-{RUN}.json").read_text())
extra = json.loads((HERE / "opus_usage.json").read_text()) if (HERE / "opus_usage.json").exists() else None
wb = Workbook(); ws = wb.active; ws.title = "Decision Models Summary"
H = PatternFill("solid", fgColor="DDE6F0"); T = PatternFill("solid", fgColor="F2F2F2")
B = Font(bold=True); thin = Side(style="thin", color="BBBBBB")
def blend(c, t):  # white -> pastel colour, t in [0,1]
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4)); mix = lambda v: round(255 + (v - 255) * t)
    return "%02X%02X%02X" % (mix(r), mix(g), mix(b))
BLUE, ORANGE = "7FBFE6", "F3B65E"       # pastel sky blue / orange (Okabe-Ito family), safe for common colour blindness
r = 1
def put(row, col, v, bold=False, fill=None, fmt=None, wrap=False, align=None):
    c = ws.cell(row, col, v); c.font = Font(bold=bold)
    if fill: c.fill = PatternFill("solid", fgColor=fill) if isinstance(fill, str) else fill
    if fmt: c.number_format = fmt
    c.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=align)
    return c
put(r, 1, "Decision models vs the human expert (JP): metrics, confusion matrices, cost and time", True).font = Font(bold=True, size=14); r += 1
put(r, 1, f"Run {M['run']}. Held-out EVD 4-77 (74 EVDs; table/figure n=72 because two JP NA rows are excluded). Reference = JP's ratings. Static values computed by metrics.py from the model outputs in the repository folder benchmarking-validation/; they are not live formulas. micro-F1 equals accuracy for single-label problems; 'overall' F1 = support-weighted F1. Kappa = unweighted Cohen's kappa. 'Raw ratio' = correct/n. Averages combine each model's probabilities before choosing the label.", wrap=True)
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9); ws.row_dimensions[r].height = 62; r += 2
TITLE = {"relevancy": "Selection relevancy", "fidelity": "Fidelity (JP's gist rule)", "quote": "Grounding: Quote", "table": "Grounding: Table/Fig (70 of 77 rows are rule-based Missing)"}
put(r, 1, "A. Agreement with JP", True).font = Font(bold=True, size=12); r += 1
cols = ["Rater / ensemble", "n", "Raw ratio (correct/n)", "Accuracy %", "Cohen's kappa", "F1 macro", "F1 micro", "F1 overall (weighted)"]
for task, t in M["tasks"].items():
    put(r, 1, TITLE[task], True, T); [put(r, c, "", fill=T) for c in range(2, 9)]; r += 1
    for i, h in enumerate(cols, 1): put(r, i, h, True, H, wrap=True)
    r += 1
    b = t["baseline"]; put(r, 1, f"Baseline: always '{b['label']}'"); put(r, 2, t["n"]); put(r, 3, f"{b['correct']}/{t['n']}"); put(r, 4, b["accuracy"], fmt="0.0%"); put(r, 5, 0.0, fmt="0.00"); r += 1
    for name, m in t["raters"].items():
        for i, v in enumerate([name, m["n"], f"{m['correct']}/{m['n']}", m["accuracy"], m["kappa"], m["f1_macro"], m["f1_micro"], m["f1_weighted"]], 1):
            put(r, i, v, bold=name.startswith("Average of Perplexity + Liquid + Opus"), fmt={4: "0.0%", 5: "0.00", 6: "0.00", 7: "0.00", 8: "0.00"}.get(i))
        r += 1
    r += 1
# ---- ensemble verdict
put(r, 1, "B. Does averaging help? (accuracy against JP; best single model vs Perplexity + Liquid + Opus average vs the three decision models averaged)", True).font = Font(bold=True, size=12); r += 1
for i, h in enumerate(["Task", "Best single model", "Best single %", "Avg Perplexity + Liquid + Opus %", "Avg Perplexity + Liquid + Jev %", "Avg all four %", "Always-commonest baseline %", "Opus-trio average minus best single (points)"], 1): put(r, i, h, True, H, wrap=True)
r += 1
for task, t in M["tasks"].items():
    R = t["raters"]; singles = {k: v for k, v in R.items() if not k.startswith(("Average", "Majority"))}
    best = max(singles, key=lambda k: singles[k]["accuracy"]); g = lambda k: R.get(k, {}).get("accuracy")
    trio = g("Average of Perplexity + Liquid + Opus")
    for i, v in enumerate([TITLE[task].split(" (")[0], best, singles[best]["accuracy"], trio, g("Average of Perplexity + Liquid + Jev"), g("Average of all four"), t["baseline"]["accuracy"],
                           None if trio is None else round(100 * (trio - singles[best]["accuracy"]), 1)], 1):
        put(r, i, v, fmt="0.0%" if i in (3, 4, 5, 6, 7) else None)
    r += 1
r += 1
# ---- confusion matrices
put(r, 1, "C. Confusion matrices (rows = JP, columns = model). Blue = agreement (diagonal), orange = disagreement; deeper colour = more EVDs.", True).font = Font(bold=True, size=12); r += 1
show = ["Perplexity Decider 1.3", "Liquid d1-ultra", "Jev", "Claude Opus 5.5", "Average of Perplexity + Liquid + Opus"]
for task, t in M["tasks"].items():
    put(r, 1, TITLE[task], True, T); [put(r, c, "", fill=T) for c in range(2, 40)]; r += 1
    top = r; col = 1
    for name in show:
        if name not in t["raters"]: continue
        cm = t["raters"][name]["confusion"]; rows_ = list(cm); cols_ = rows_ + sorted({c for row in cm.values() for c in row if c not in rows_})   # same order as rows so agreement sits on the diagonal
        put(top, col, name, True); ws.merge_cells(start_row=top, start_column=col, end_row=top, end_column=col + len(cols_))
        put(top + 1, col, "JP \\ model", True, H, wrap=True)
        for j, c in enumerate(cols_): put(top + 1, col + 1 + j, c, True, H, wrap=True, align="center")
        mx = max([v for row in cm.values() for v in row.values()] or [1]) or 1
        for i, a in enumerate(rows_):
            put(top + 2 + i, col, a, True, H)
            for j, c in enumerate(cols_):
                v = cm[a].get(c, 0); diag = a == c
                put(top + 2 + i, col + 1 + j, v, fill=blend(BLUE if diag else ORANGE, 0.0 if v == 0 else 0.25 + 0.75 * v / mx), align="center", bold=diag)
        col += len(cols_) + 2
    r = top + 2 + len(t["raters"][show[0]]["confusion"]) + 2
# ---- usage
put(r, 1, "D. Tokens, time and cost per model and run", True).font = Font(bold=True, size=12); r += 1
for i, h in enumerate(["Model", "Run", "Records", "Model calls", "Input tokens", "Request time (s, summed)", "Cost (USD)", "Cost source"], 1): put(r, i, h, True, H, wrap=True)
r += 1
tot = {}
for u in M["usage"]:
    for i, v in enumerate([u["model"], u["run"], u["records"], u["model_calls"], u["input_tokens"], u["request_time_s"], u["cost_usd"], u["cost_source"]], 1): put(r, i, v, fmt="#,##0" if i == 5 else ("0.0000" if i == 7 else None))
    r += 1
if extra:
    for b in extra["batches"]:
        for i, v in enumerate(["Claude Opus 5.5 (Claude Code subagent)", extra["run"], b["evds"], b["evds_n"], b["tokens"], round(b["duration_ms"] / 1000, 1), extra.get("cost_usd_per_batch", ""), extra.get("cost_note", "")], 1): put(r, i, v, fmt="#,##0" if i == 5 else None)
        r += 1
put(r + 1, 1, "Notes: Perplexity and Jev do not report cost; it is computed from list prices ($0.02 and $0.042 per million input tokens). Liquid reports its own cost. Output tokens are free for the three decision models. 'Request time' sums each request's wait and is not wall-clock time (4 requests ran at once). Opus 5.5 ran as six parallel Claude Code subagents on a blind folder of the same inputs, so its tokens include agent overhead and image reading; time is each subagent's duration. The smoke and lat runs are pilots with earlier prompts.", wrap=True)
ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=9); ws.row_dimensions[r + 1].height = 75
ws.column_dimensions["A"].width = 46
for c in range(2, 45): ws.column_dimensions[ws.cell(1, c).column_letter].width = 13
ws.freeze_panes = "B4"
wb.save(HERE / f"sheets/decision-models-summary-{RUN}.xlsx"); print("saved sheets/decision-models-summary-%s.xlsx, %d rows" % (RUN, r + 2))

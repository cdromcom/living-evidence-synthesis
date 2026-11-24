#!/usr/bin/env python3
"""Build the LOG tab (xlsx) for one rater: prompt text per run, example requests as sent, and every output record, for later review.
Usage: python3 -I make_log_tab.py <perplexity|liquid|jev|opus>"""
import glob, json, re, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
HERE = Path(__file__).resolve().parent
prov = sys.argv[1]
NAME = {"perplexity": "Perplexity Decider 1.3", "liquid": "Liquid d1-ultra", "jev": "Jev", "opus": "Claude Opus 5.5"}[prov]
META = {"perplexity": ("pplx-decider-v1.3", "api.perplexity.ai/v1/decisions"), "liquid": ("d1-ultra", "api.liquid.ai/decisions/v1/systemone"),
        "jev": ("jev-1.14.0", "api.typesafe.ai/v1/systemone"), "opus": ("claude-opus-5-5", "Claude Code subagents (model opus), blind folder")}[prov]
FN, GREEN, TXT = "Spectral", "D9EAD2", "38761D"
wb = Workbook(); ws = wb.active; ws.title = "LOG"
r = 1
def cell(row, col, v, bold=False, fill=None, color=None, size=10, wrap=True):
    c = ws.cell(row, col, v if not isinstance(v, str) else v[:49000]); c.font = Font(name=FN, bold=bold, size=size, color=color)
    c.fill = PatternFill("solid", fgColor=fill or "FFFFFF"); c.alignment = Alignment(wrap_text=wrap, vertical="top"); return c
def bar(text, ncols=8):
    global r
    for c in range(1, ncols + 1): cell(r, c, "", True, GREEN, TXT)
    cell(r, 1, text, True, GREEN, TXT); r += 1
cell(r, 1, f"LOG: {NAME}. Prompts, example requests and every output, kept for later review", True, size=14); r += 1
for k, v in [("Model id / access", f"{META[0]} via {META[1]}"),
             ("Runs", "smoke and lat = pilots (earlier prompts, EVD 4-6 and 7-9); r1 = Run 1 (judgment of record, 2026-11-24 UTC); r1fix = EVD 21 and 38 re-judged after the quote-parser fix, overriding r1 for those two EVDs; r2 = Run 2 (2026-11-24 UTC, every screenshot shown, paraphrased text added to the table task); r2t = Run 2 table/figure rerun with JP's Missing-by-rule (r2t holds the r2 relevancy, fidelity and quote records unchanged plus the rerun table/figure records; r2 table/figure rows are superseded by r2t); r3 = Run 3 (2026-11-24 UTC): the quote task re-run with the strict quote definitions, with relevancy, fidelity and table/figure records copied unchanged from r2t."),
             ("Run 1 prompt state", "fidelity prompt v3 (JP gist rule, worked examples from EVD 1-3), review questions, verbatim-quote rule, quote and table/figure judged from the slot the vault page used, no-table-screenshot = Missing by rule."),
             ("Run 2 prompt state", "every Description screenshot shown without slot labels with a per-screenshot question; table/figure task also gets the paraphrased text under the table/figure; Missing by rule only when the page has no screenshot (r2). r2t: Missing by rule when the page has no screenshot in the table/figure slot (JP's rule), otherwise the models judge with every screenshot shown; Opus's r2 judgements were reused for the EVDs that have one."),
             ("Analysis exclusions (JP, 2026-11-24)", "Scores are reported after JP's exclusions (inputs/exclusions.json) and, next to them, on every row. Relevancy drops EVD 7, 17, 49, 72, 75, 76 (JP's notes say they are not true EVDs; EVD 32 stays), n=68. Fidelity drops EVD 4, 19, 26, 36, 38, 54, 56, 65 (the quote is a table paraphrase or needs methods context to give rise to the headline EVD; a result of how JP guided earlier Claude Sonnet and Opus models to write headline EVDs, not the raters' fault), n=66. Quote drops EVD 5, 6, 9, 18, 45, 51, 53, 66 pending JP re-rating, n=66. The fidelity and quote sets were chosen from rows all four raters got wrong, so those exclusions are outcome-selected."),
             ("Quote grounding definitions (from the next run)", "Correct = the full quote is shown with no extraneous content in the way. Partially Correct = the right passage but incomplete or cropped. Incorrect = a screenshot is present but shows a different passage. Missing = no screenshot at all. Runs r1 and r2 used the earlier wording (see section A), so their quote labels were not judged against the strict Correct definition."),
             ("Run 3 prompt state", "Quote task only changed: Correct = the full quote shown with no extraneous content; Partially Correct = right passage but incomplete or cropped; Incorrect = a screenshot is present but a different passage; Missing = no screenshot at all. The Run 3 text in section A is the full current prompt document; example requests are as in Run 2 apart from the quote rubric."),
             ("Code and data", "github.com/cdromcom/living-evidence-synthesis, folder benchmarking-validation (pull request 8). Raw outputs: results/<provider>.<run>.jsonl.")]:
    cell(r, 1, k, True); cell(r, 2, v); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8); r += 1
r += 1
bar("A. PROMPT TEXT AS SENT (rubrics, criterion and question wording; the per-EVD inputs are in the packets)")
for c, h in enumerate(["Run", "Component", "Text"], 1): cell(r, c, h, True)
r += 1
def sections(md):
    parts = re.split(r"^## ", md, flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1].strip()) for p in parts]
for run, f in (("Run 1", "log_src/prompts_run1.md"), ("Run 2", "log_src/prompts_run2.md"), ("Run 3", "log_src/prompts_run3.md")):
    for title, body in sections((HERE / f).read_text()):
        cell(r, 1, run); cell(r, 2, title, True); cell(r, 3, body); ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8); r += 1
if prov == "opus":
    cell(r, 1, "Run 1"); cell(r, 2, "Instructions given to each Opus rater", True)
    cell(r, 3, (HERE / "OPUS_RATER_INSTRUCTIONS.md").read_text() if (HERE / "OPUS_RATER_INSTRUCTIONS.md").exists() else ""); ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8); r += 1
r += 1
if prov != "opus":
    bar("B. EXAMPLE REQUESTS AS SENT (Perplexity's text; the other two decision models receive the same text in their own request format)")
    for c, h in enumerate(["Run", "Example", "Text"], 1): cell(r, c, h, True)
    r += 1
    for run, d in (("Run 1", "log_src/run1"), ("Run 2", "log_src/run2")):
        for f in sorted((HERE / d).glob("*.txt")):
            cell(r, 1, run); cell(r, 2, f.stem.replace("perplexity-", ""), True); cell(r, 3, f.read_text()); ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8); r += 1
    r += 1
bar("C. OUTPUTS (one row per record; r1fix rows supersede r1 for the same EVD and task)", 14)
H = ["Run id", "EVD", "Task", "Rule-based (no model call)", "Model id returned", "Time (UTC)", "Input tokens", "Latency (s)", "Images sent", "Label", "Probabilities", "All answers (JSON)", "Reason (Opus only)", "Superseded (r1fix, or r2t for r2 table rows)"]
for c, h in enumerate(H, 1): cell(r, c, h, True)
head_row = r; r += 1
fixed = set()
for f in glob.glob(str(HERE / f"results/{prov}.r1fix*.jsonl")):
    for x in map(json.loads, open(f)): fixed.add((x["evd"], x["task"]))
def label(x):
    a = x.get("answers") or {}
    if "relevant" in a: return "Relevant" if a["relevant"]["noul"] >= .5 else "Irrelevant"
    for k in ("fidelity", "quote_grounding", "table_fig_grounding"):
        if k in a: return a[k].get("choice")
def probs(x):
    a = x.get("answers") or {}
    if "relevant" in a: return f"P(Relevant)={a['relevant']['noul']:.3f}"
    for k in ("fidelity", "quote_grounding", "table_fig_grounding"):
        if k in a: return "; ".join(f"{kk} {vv:.3f}" for kk, vv in sorted(a[k].get("probabilities", {}).items(), key=lambda t: -t[1]))
rows = []
for f in sorted(glob.glob(str(HERE / f"results/{prov}.*.jsonl"))):
    if f.endswith(".r3q.jsonl"): continue   # quote-only file; its records are inside r3
    run = Path(f).name.split(".")[1]
    for x in map(json.loads, open(f)):
        rows.append((run, x["evd"], x["task"], "yes" if x.get("rule_based") else "", x.get("model", ""), (x.get("ts") or "")[:19].replace("T", " "),
                     (x.get("usage") or {}).get("input_tokens", ""), x.get("latency_s", ""), x.get("images_sent", ""), label(x), probs(x),
                     json.dumps(x.get("answers"), ensure_ascii=False), x.get("reason", ""), "yes" if (run == "r1" and (x["evd"], x["task"]) in fixed) or (run == "r2" and x["task"] == "table") else ""))
order = {"smoke": 0, "lat": 1, "r1": 2, "r1fix": 3, "r2": 4, "r2t": 5, "r3": 6}
for row in sorted(rows, key=lambda t: (order.get(t[0], 9), t[1], t[2])):
    for c, v in enumerate(row, 1): cell(r, c, v, wrap=(c in (11, 13)))
    r += 1
if prov == "opus" and (HERE / "opus_usage.json").exists():
    u = json.load(open(HERE / "opus_usage.json")); r += 1; bar("D. OPUS SUBAGENT BATCHES (tokens and time)", 8)
    for c, h in enumerate(["Batch", "EVDs", "Subagent tokens", "Duration (s)"], 1): cell(r, c, h, True)
    r += 1
    u2 = json.load(open(HERE / "opus_usage_r2.json"))
    for lab, uu in (("Run 1", u), ("Run 2", u2)):
        for b in uu["batches"]:
            for c, v in enumerate([f"{lab}: {b['evds']}", b["evds_n"], b["tokens"], round(b["duration_ms"] / 1000, 1)], 1): cell(r, c, v)
            r += 1
        cell(r, 1, uu["cost_note"]); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); r += 1
for col, w in zip("ABCDEFGHIJKLMN", [26, 34, 70, 22, 22, 20, 14, 12, 12, 18, 60, 70, 60, 14]): ws.column_dimensions[col].width = w / 7 * 1.0 if w < 30 else w / 7
wb.save(HERE / f"sheets/log-{prov}.xlsx"); print(prov, "log rows:", len(rows), "total rows:", r)

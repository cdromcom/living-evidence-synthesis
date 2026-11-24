#!/usr/bin/env python3
"""Build the three model-only tracking workbooks (xlsx) from the vault. No ratings from JP or Claude are read."""
import re, sys, json, concurrent.futures as cf
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import requests
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
import build_packets as bp

BASE = "https://living-evidence-synthesis.vercel.app/vault-img/"
pages = []
for f in sorted(bp.EVD_DIR.glob("EVD - *.md")):
    title, body = bp.front(f.read_text()); pages.append((title or f.stem[6:], f, body))
pages.sort(key=lambda t: t[0].lower())

recs = []
for n, (title, f, body) in enumerate(pages, 1):
    sec = bp.sections(body)
    quotes, grounding, other, shots = bp.split_description(sec.get("Description", ""))
    meth = re.findall(r"!\[\[(.*?)\]\]", sec.get("Methods Context", ""))
    ck = bp.citekey_of(sec.get("Source", "")); pdf = bp.resolve_pdf(ck) if ck else None
    recs.append(dict(evd=n, title=title, quote="\n".join(quotes), grounding="\n".join(grounding), pdf=pdf.name if pdf else "",
                     tf=[s["file"] for s in shots if s["kind"] == "tablefig"],
                     qs=[s["file"] for s in shots if s["kind"] == "quote"], meth=meth))
names = sorted({x for r in recs for k in ("tf", "qs", "meth") for x in r[k]})
def head(nm):
    try: return nm, requests.head(BASE + nm, timeout=20, allow_redirects=True).status_code
    except Exception as e: return nm, 0
with cf.ThreadPoolExecutor(10) as ex: status = dict(ex.map(head, names))
bad = {k: v for k, v in status.items() if v != 200}
print(len(names), "distinct screenshots;", len(bad), "not on live site:", bad)
json.dump(status, open("image_url_status.json", "w"), indent=1)

def cell(nm):
    return f'=IMAGE("{BASE}{nm}",1)' if status[nm] == 200 else f"Not on the live site (HTTP {status[nm]}): {nm}"

MODELS = {
 "perplexity": ("Perplexity Decider 1.3", "pplx-decider-v1.3 (pinned, 27B). Fill in run date in column R.", "The model saw the vault copy of each image, resized to at most 1400 px, plus the full paper text."),
 "liquid": ("Liquid d1-ultra", "d1-ultra (the id JP asked for). Liquid's docs list d1-ultra as deprecated, replaced by d1.2-ultra (same request format and price); results from the two are not interchangeable. Record the id and run date in column R.", "d1-ultra's context is about 32K tokens (gateway page; unconfirmed), so for the Quote and Table/Fig tasks it was sent only the ~16K tokens of paper pages that best overlap the quote and EVD statement, not the whole paper. The other two models see the full paper text. Report this difference in the write-up."),
 "jev": ("Jev", "jev-1.14.0 by default (the pin is recorded in column R; jev-1.13.0 is the other listed version).", "Jev was sent TEXT ONLY (its image input is a preview feature), so its Table/Fig answers rest on the paper text and the page's table note, not the screenshots."),
}
HDR = ["EVD", "EVD statement (headline)", "Description quote text", "Review question(s) (JP-edited)", "Table/Figure screenshot 1", "Table/Figure screenshot 2", "Table/Figure caption",
       "Quote screenshot 1", "Quote screenshot 2", "Source PDF used", "Relevancy (model)", "P(Relevant)", "Fidelity (model)", "P(every number in quote)",
       "Grounding: Quote (model)", "P(quote verbatim in paper)", "Grounding: Table/Fig (model)", "Images the model was sent", "Run date / model version",
       "{M} Notes", "Methods Context quote screenshot 1", "Methods Context quote screenshot 2", "Methods Context quote screenshot 3", "Quote screenshot 3 (extra)"]
WID = [50, 240, 400, 320, 320, 220, 320, 320, 200, 110, 90, 110, 100, 120, 100, 120, 110, 130, 260, 320, 320, 320, 320]
GREEN, BROWN, RED, GRAY = "D9EAD3", "FFF2CC", "F4CCCC", "EFEFEF"

def build(key):
    M, ver, imgnote = MODELS[key]
    wb = Workbook(); ws = wb.active; ws.title = "EVD"
    ws.append([h.replace("{M}", M) for h in HDR])
    for r in recs:
        tf = [cell(x) for x in r["tf"]]; qs = [cell(x) for x in r["qs"]]; me = [cell(x) for x in r["meth"]]
        ws.append([r["evd"], r["title"], r["quote"],
                   tf[0] if tf else "Missing (no table/figure .png on the page)", tf[1] if len(tf) > 1 else "", r["grounding"],
                   qs[0] if qs else "Missing (no quote .png)", qs[1] if len(qs) > 1 else "", r["pdf"],
                   "", "", "", "", "", "", "", "", "", "",
                   me[0] if me else "Missing (no .png)", me[1] if len(me) > 1 else "", me[2] if len(me) > 2 else "", qs[2] if len(qs) > 2 else ""])
    n = len(recs) + 1
    for i, w in enumerate(WID, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = w / 7
    for row in ws.iter_rows(min_row=1, max_row=n):
        for c in row: c.alignment = Alignment(vertical="top", wrap_text=True)
    for c in ws[1]: c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="D9E6F7")
    for r in range(2, n + 1): ws.row_dimensions[r].height = 175
    ws.freeze_panes = "C2"
    lists = {"J": ["Relevant", "Irrelevant", "NA"], "L": ["Met", "Partially Met", "Unmet", "NA"],
             "N": ["Correct", "Partially Correct", "Missing", "Incorrect", "NA"], "P": ["Correct", "Partially Correct", "Missing", "Incorrect", "NA"]}
    for col, opts in lists.items():
        dv = DataValidation(type="list", formula1='"' + ",".join(opts) + '"', allow_blank=True, showDropDown=False)
        ws.add_data_validation(dv); dv.add(f"{col}2:{col}{n}")
        for val, color in [("Relevant", GREEN), ("Met", GREEN), ("Correct", GREEN), ("Partially Met", BROWN), ("Partially Correct", BROWN),
                           ("Irrelevant", RED), ("Unmet", RED), ("Incorrect", RED), ("NA", GRAY), ("Missing", GRAY)]:
            if val in opts:
                ws.conditional_formatting.add(f"{col}2:{col}{n}", CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", bgColor=color, fgColor=color)))
    ab = wb.create_sheet("ABOUT")
    for row in [
        [f"About: LIVES AI Rater - {M} (model-only)"],
        ["Created", "2026-11-23, by Claude (Sonnet 5.5) in a Claude Code session with JP."],
        ["Purpose", f"A human-readable record of what {M} was shown and what it answered for each EVD. It is kept apart from the main LIVES-EVD-Benchmarking tab so no JP or Claude judgment can bias the model, and so the three models' results can be merged into the main sheet later."],
        ["Blinding", "Every column except the model's own answers holds only vault content (EVD statement, Description quote, screenshots, source PDF name). There are no JP or Claude ratings, notes, drafts or flags anywhere in this file. The API script never reads this sheet or the main sheet; it reads local packet files and writes local results."],
        ["Columns J-S", "Model answers, filled after the run from results/<provider>.<run-id>.jsonl (run_raters.py export). Relevancy = Relevant if P(Relevant) >= 0.5. Fidelity, Quote and Table/Fig are the model's top choice; probabilities are in the results file. The dropdown lists and colors mirror LIVES - AAA Benchmarking (HAI). Column S is for JP's notes on this model's answers."],
        ["Screenshots", f"All screenshots load from the live LIVES site (living-evidence-synthesis.vercel.app/vault-img). Columns D-E and G-H hold the Description's table/figure and quote screenshots; columns T-V hold the Methods Context quote screenshots from the same evidence page. 'Missing' = the vault page has no .png for that slot; 'Not on the live site' = the page references a file that is not served. {imgnote}"],
        ["Rows", "77 EVDs. Continuation rows (EVD 45 and 47 splits) are left out; they are NA on the main sheet."],
        ["Model and version", ver],
        ["Fidelity rule", "JP's gist rule (2026-11-23): Met when the gist of the headline EVD is in the Description quote; matching specifics are a bonus. Grounding rubrics follow the grader prompt of 2026-11-17 and are provisional."],
    ]: ab.append(row)
    ab.column_dimensions["A"].width = 22; ab.column_dimensions["B"].width = 120
    for row in ab.iter_rows():
        for c in row: c.alignment = Alignment(vertical="top", wrap_text=True)
    Path("sheets").mkdir(exist_ok=True); p = f"sheets/{key}.xlsx"; wb.save(p); return p

for k in MODELS: print(build(k))
print("max quote shots:", max(len(r["qs"]) for r in recs), "max methods shots:", max(len(r["meth"]) for r in recs), "max tablefig:", max(len(r["tf"]) for r in recs))

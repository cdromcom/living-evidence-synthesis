#!/usr/bin/env python3
"""Build JP's review mirror of the LIVES vault as an .xlsx that Google Sheets can open.

The markdown vault stays the source of truth. This script reads the parsed graph
(nodes and edges) plus the per-EVD PICOST JSON files and writes one workbook with
the tabs README, SRC, QUE, CLM, EVD, CVT, PICOST and SCREENING. Each tab has
a "JP accuracy judgment" column group on the right (dropdowns with pastel colours
and a Notes column). Screenshots are real =IMAGE("<url>",1) formulas that point at
the live site, so the workbook needs no embedded pictures.

Usage
    python3 scripts/vault_to_gsheet.py [options]

Options (all optional)
    --graph PATH        graph-data.generated.json
                        (default: lib/graph-data.generated.json next to the vault folder)
    --picost DIR        folder of <EVD-id>.json files
                        (default <vault>/sysrev/picost; in the repo: vault/sysrev/picost)
    --out PATH          output .xlsx
                        (default <vault>/pipeline/misc/evd-validation/2026-11-24-vault-mirror.xlsx)
    --pdf-dir DIR       source PDF folder, used only to name each paper's PDF file
                        (default <vault>/sysrev/dgraph/source/pdfs)
    --permissions PATH  PERMISSIONS.md, used only for the licence column
                        (default <vault>/pipeline/legal/PERMISSIONS.md)
    --img-base URL      prefix for screenshots
                        (default https://living-evidence-synthesis.vercel.app/vault-img/)
    --build-date DATE   date shown in the README and stored in the file properties (default today)
    --commit TEXT       source commit shown in the README (default: git HEAD of the folder that holds --graph)

Needs Python 3 and openpyxl. No network access. Missing optional inputs (PDF folder,
permissions file, picost folder) give empty cells and a warning on stderr, not a failure.

Idempotent: the same inputs and the same --build-date produce the same cells, and the
output file is overwritten. To refresh the Google Sheet, upload the new .xlsx; JP's
judgments live in the Sheet, so upload to a new Sheet or copy them over first.
"""
import argparse
import datetime as dt
import glob
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
import urllib.parse

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])

# ---- pastel colours copied from the benchmark sheets' Run tabs --------------
GREEN, YELLOW, RED, GREY, BLUE = "D9EAD3", "FFF2CC", "F4CCCC", "EFEFEF", "DDEBF7"

RELEVANCY = {"Relevant": GREEN, "Irrelevant": RED, "NA": GREY}
FIDELITY = {"Met": GREEN, "Partially Met": YELLOW, "Unmet": RED, "NA": GREY}
GROUNDING = {"Correct": GREEN, "Partially Correct": YELLOW, "Incorrect": RED,
             "Missing": GREY, "NA": GREY}
YNF = {"Yes": GREEN, "Needs fix": YELLOW, "No": RED}
WORDING = {"OK": GREEN, "Edit": YELLOW, "Split": BLUE, "Drop": RED}
INCLUDE = {"Include": GREEN, "Exclude": RED}

HEAD_FILL = PatternFill("solid", fgColor="44546A")
JP_FILL = PatternFill("solid", fgColor="C55A11")
MODEL_FILL = PatternFill("solid", fgColor="7F7F7F")
JP_CELL_FILL = PatternFill("solid", fgColor="FFFBF2")
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
HEAD_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="center")


# ---- small markdown helpers --------------------------------------------------
def section(body, heading, level=2):
    """Text under '<#*level> heading' up to the next heading of the same or higher level."""
    pat = r"^%s %s\s*$" % ("#" * level, re.escape(heading))
    m = re.search(pat, body, re.M)
    if not m:
        return ""
    rest = body[m.end():]
    n = re.search(r"^#{1,%d} " % level, rest, re.M)
    return rest[:n.start()] if n else rest


def quote_lines(text, keep_citation_only=False):
    """Quoted text lines (blockquote lines that are real quotes, no images/callouts)."""
    out = []
    for ln in text.split("\n"):
        if not ln.startswith(">"):
            continue
        s = ln.lstrip("> ").strip()
        if not s or s.startswith("![") or s.startswith("[!") or s.startswith("Grounding table"):
            continue
        if s.startswith("[Inferred"):
            continue
        out.append(s)
    return out


def images(text):
    return re.findall(r"!\[([^\]]*)\]\(/vault-img/([^)]+)\)", text)


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return re.sub(r"[*_`]", "", s).strip()


def short(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def node_links(text, prefix):
    seen, out = set(), []
    for m in re.finditer(r"\(/nodes/(%s-\d+)\)" % prefix, text):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(1))
    return out


def cite_links(text):
    seen, out = set(), []
    for m in re.finditer(r"\[@([^\]]+)\]\(/nodes/(SRC-\d+)\)", text):
        if m.group(2) not in seen:
            seen.add(m.group(2))
            out.append(m.group(1))
    return out


def tag_value(node, prefix):
    for t in node["tags"]:
        if t.startswith(prefix):
            return t[len(prefix):]
    return ""


# ---- sheet builder -----------------------------------------------------------
class Tab:
    """Two header rows (group band + column names), data from row 3, frozen at C3."""

    def __init__(self, wb, title, cols, jp_cols, mid_cols=(), band_note=None, tab_color=None):
        self.ws = wb.create_sheet(title)
        self.cols = list(cols)          # (header, width)
        self.mid = list(mid_cols)
        self.jp = list(jp_cols)         # (header, width, dropdown-dict or None)
        self.row = 3
        ws = self.ws
        ncol = len(self.cols) + len(self.mid) + len(self.jp)
        # band row
        left_end = len(self.cols)
        ws.cell(1, 1, band_note or "Vault data (read-only mirror; edit the markdown, not here)")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=left_end)
        if self.mid:
            ws.cell(1, left_end + 1, "Decision model")
            ws.merge_cells(start_row=1, start_column=left_end + 1, end_row=1,
                           end_column=left_end + len(self.mid))
        jp_start = left_end + len(self.mid) + 1
        ws.cell(1, jp_start, "JP accuracy judgment")
        ws.merge_cells(start_row=1, start_column=jp_start, end_row=1, end_column=ncol)
        for c in range(1, ncol + 1):
            cell = ws.cell(1, c)
            cell.fill = JP_FILL if c >= jp_start else (MODEL_FILL if c > left_end else HEAD_FILL)
            cell.font = Font(bold=True, color="FFFFFF", size=11)
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        # column header row
        allcols = [(h, w) for h, w in self.cols] + [(h, w) for h, w in self.mid] + \
                  [(h, w) for h, w, _ in self.jp]
        for i, (h, w) in enumerate(allcols, 1):
            cell = ws.cell(2, i, h)
            cell.fill = JP_FILL if i >= jp_start else (MODEL_FILL if i > left_end else HEAD_FILL)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = HEAD_ALIGN
            cell.border = BORDER
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.row_dimensions[1].height = 22
        ws.row_dimensions[2].height = 34
        ws.freeze_panes = "C3"
        if tab_color:
            ws.sheet_properties.tabColor = tab_color
        self.ncol, self.jp_start, self.left_end = ncol, jp_start, left_end

    def add(self, values, height=None):
        ws = self.ws
        for i in range(1, self.ncol + 1):
            v = values[i - 1] if i - 1 < len(values) else None
            cell = ws.cell(self.row, i, v)
            cell.alignment = WRAP
            cell.border = BORDER
            if i >= self.jp_start:
                cell.fill = JP_CELL_FILL
        if height:
            ws.row_dimensions[self.row].height = height
        self.row += 1

    def finish(self, extra_rows=0):
        """Dropdowns + colour rules for every JP/model dropdown column."""
        last = max(self.row - 1, 3) + extra_rows
        start_idx = self.left_end + len(self.mid)
        for k, (h, w, dd) in enumerate(self.jp):
            if not dd:
                continue
            col = get_column_letter(start_idx + k + 1)
            rng = "%s3:%s%d" % (col, col, last)
            dv = DataValidation(type="list", formula1='"%s"' % ",".join(dd), allow_blank=True,
                                showErrorMessage=True, errorTitle="Pick from the list",
                                error="Choose one of: " + ", ".join(dd))
            self.ws.add_data_validation(dv)
            dv.add(rng)
            for val, colr in dd.items():
                self.ws.conditional_formatting.add(
                    rng, CellIsRule(operator="equal", formula=['"%s"' % val],
                                    fill=PatternFill("solid", start_color=colr, end_color=colr)))
        self.ws.auto_filter.ref = "A2:%s%d" % (get_column_letter(self.ncol), max(self.row - 1, 2))


# ---- main --------------------------------------------------------------------
def load_licences(path):
    out = {}
    if not path or not os.path.exists(path):
        print("warning: permissions file not found; licence column left empty", file=sys.stderr)
        return out
    for ln in open(path, encoding="utf-8"):
        if not ln.startswith("| @"):
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        key, lic = c[0].lstrip("@"), c[2]
        m = re.search(r"creativecommons\.org/licenses/([a-z\-]+)/([\d.]+)", lic)
        if m:
            lic = "CC %s %s" % (m.group(1).upper(), m.group(2))
        out[key] = lic
    return out


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).casefold().replace("\u2019", "'")


def match_pdf(src, pdfs):
    if not pdfs:
        return ""
    fam = fold((src["extras"].get("apaAuthors") or [{}])[0].get("family", ""))
    words = set(re.findall(r"[a-z]{5,}", fold(src["extras"].get("apaTitle", ""))))
    best, best_s = "", 0
    for p in pdfs:
        low = fold(p)
        if low.startswith("archive") or low.startswith("supp"):
            continue
        s = (3 if fam and fam in low else 0)
        pw = set(re.findall(r"[a-z]{5,}", low))
        s += len(words & pw) / max(len(words), 1) * 2
        if s > best_s:
            best, best_s = p, s
    return best if best_s >= 3 else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--graph", default=str(VAULT.parent / "lib" / "graph-data.generated.json"))
    ap.add_argument("--picost", default=str(VAULT / "sysrev" / "picost"))
    ap.add_argument("--out", default=str(VAULT / "pipeline" / "misc" / "evd-validation" / "2026-11-24-vault-mirror.xlsx"))
    ap.add_argument("--pdf-dir", default=str(VAULT / "sysrev" / "dgraph" / "source" / "pdfs"))
    ap.add_argument("--permissions", default=str(VAULT / "pipeline" / "legal" / "PERMISSIONS.md"))
    ap.add_argument("--img-base", default="https://living-evidence-synthesis.vercel.app/vault-img/")
    ap.add_argument("--build-date", default=dt.date.today().isoformat())
    ap.add_argument("--commit", default=None)
    a = ap.parse_args()

    g = json.load(open(a.graph, encoding="utf-8"))
    N = {n["id"]: n for n in g["nodes"]}
    by_type = {}
    for n in g["nodes"]:
        by_type.setdefault(n["type"], []).append(n)
    for v in by_type.values():
        v.sort(key=lambda n: n["id"])
    E = g["edges"]

    def out_edges(frm, typ, to_type=None):
        return sorted(e["to"] for e in E if e["from"] == frm and e["type"] == typ
                      and (to_type is None or N[e["to"]]["type"] == to_type))

    def in_edges(to, typ, from_type=None):
        return sorted(e["from"] for e in E if e["to"] == to and e["type"] == typ
                      and (from_type is None or N[e["from"]]["type"] == from_type))

    cite_of = {s["id"]: s["extras"]["citekey"] for s in by_type["SRC"]}
    evd_src = {}
    for e in by_type["EVD"]:
        t = out_edges(e["id"], "derivedFrom", "SRC")
        evd_src[e["id"]] = t[0] if t else None

    def lines(ids, with_title=True):
        return "\n".join(("%s: %s" % (i, N[i]["title"])) if with_title else i for i in ids)

    picost = {}
    if os.path.isdir(a.picost):
        for f in sorted(glob.glob(os.path.join(a.picost, "EVD-*.json"))):
            j = json.load(open(f, encoding="utf-8"))
            picost[j["evd_id"]] = j
    else:
        print("warning: picost folder not found; PICOST columns left empty", file=sys.stderr)
    pdfs = sorted(os.listdir(a.pdf_dir)) if os.path.isdir(a.pdf_dir) else []
    pdfs = [p for p in pdfs if p.lower().endswith(".pdf")]
    if not pdfs:
        print("warning: no PDFs found; PDF file column left empty", file=sys.stderr)
    lic = load_licences(a.permissions)

    commit = a.commit
    if commit is None:
        gd = os.path.dirname(os.path.abspath(a.graph))
        try:
            h = subprocess.run(["git", "-C", gd, "rev-parse", "--short", "HEAD"], capture_output=True,
                               text=True, check=True).stdout.strip()
            b = subprocess.run(["git", "-C", gd, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True,
                               text=True, check=True).stdout.strip()
            commit = "%s (branch %s)" % (h, b)
        except Exception:
            commit = "unknown"

    def img(fn):
        return '=IMAGE("%s%s",1)' % (a.img_base, urllib.parse.quote(fn))

    wb = Workbook()
    wb.remove(wb.active)
    d = dt.datetime.fromisoformat(a.build_date)
    wb.properties.created = d
    wb.properties.modified = d
    wb.properties.creator = "vault_to_gsheet.py"

    # README (built first so it is the first tab; filled at the end with counts)
    readme = wb.create_sheet("README")

    # SRC
    t = Tab(wb, "SRC", [("ID", 9), ("Citekey", 34), ("Title", 46), ("Year", 7), ("Venue / version", 30),
                        ("DOI", 28), ("Licence", 14), ("PDF file", 40), ("TL;DR", 70)],
            [("Metadata and TL;DR accurate?", 16, YNF), ("Notes", 40, None)], tab_color="44546A")
    for s in by_type["SRC"]:
        x = s["extras"]
        vol = x.get("apaVolume", "")
        if x.get("apaIssue"):
            vol += "(%s)" % x["apaIssue"]
        pg = x.get("apaPages") or x.get("apaArticleNumber") or ""
        venue = x.get("apaContainer") or x.get("pubType", "")
        venue = ", ".join(p for p in [venue, vol, pg] if p)
        m = re.search(r"\[!success\] \*\*TL;DR\*\*\n((?:>.*\n?)+)", s["bodyMarkdown"])
        tldr = " ".join(l.lstrip("> ").strip() for l in m.group(1).split("\n")) if m else ""
        t.add([s["id"], x["citekey"], x.get("apaTitle", ""), x.get("apaYear"), venue, x.get("doi", ""),
               lic.get(x["citekey"], ""), match_pdf(s, pdfs), tldr])
    t.finish()
    n_src = len(by_type["SRC"])

    # QUE
    t = Tab(wb, "QUE", [("ID", 9), ("Question", 50), ("Original wording quote(s)", 70), ("Papers", 34),
                        ("CLMs addressing it", 60), ("Status", 12)],
            [("Wording OK?", 14, WORDING), ("JP edited wording", 40, None), ("Notes", 40, None)],
            tab_color="2E75B6")
    for q in by_type["QUE"]:
        b = q["bodyMarkdown"]
        snip = section(b, "Snippet: Quote(s) & Screenshots", 3)
        t.add([q["id"], q["title"], "\n".join(quote_lines(snip)),
               "\n".join(cite_links(section(b, "Key Papers Asking Question", 3))),
               lines(in_edges(q["id"], "addresses", "CLM")), q["curationStatus"]])
    t.finish()

    # CLM
    t = Tab(wb, "CLM", [("ID", 9), ("Claim", 50), ("QUE ids", 16), ("Supporting EVD titles", 70),
                        ("Key papers", 34), ("Truth value", 9), ("Status", 12)],
            [("Claim accurate?", 14, YNF), ("Notes", 40, None)], tab_color="548235")
    for c in by_type["CLM"]:
        b = c["bodyMarkdown"]
        t.add([c["id"], c["title"], "\n".join(out_edges(c["id"], "addresses", "QUE")),
               lines(in_edges(c["id"], "supports", "EVD")),
               "\n".join(cite_links(section(b, "Key Papers Making This Claim", 3))),
               c["extras"].get("truthValue"), c["curationStatus"]])
    t.finish()

    # EVD
    t = Tab(wb, "EVD", [("ID", 9), ("Headline statement", 44), ("Benchmark #", 9), ("Source", 28),
                        ("Description quote with citation", 56), ("Quote screenshot", 40),
                        ("Table / figure screenshot 1", 40), ("Table / figure screenshot 2", 40),
                        ("P", 28), ("I", 28), ("C", 28), ("O", 30), ("S", 24), ("T", 24),
                        ("Methods: What", 42), ("Methods: How", 42), ("Methods: Who", 42),
                        ("CLM ids", 10), ("CVT ids", 10), ("Status", 12)],
            [("Relevancy", 13, RELEVANCY), ("Fidelity", 13, FIDELITY), ("Quote grounding", 15, GROUNDING),
             ("Table/Fig grounding", 15, GROUNDING), ("Numbers verified", 13, YNF), ("Notes", 40, None)],
            tab_color="C00000")
    for e in by_type["EVD"]:
        b = e["bodyMarkdown"]
        desc = section(b, "Description")
        ims = images(desc)
        quote_im = next((f for a_, f in ims if not re.match(r"(Table|Figure)", a_)), None)
        tf = [f for a_, f in ims if re.match(r"(Table|Figure)", a_)][:2]
        mc = section(b, "Methods Context")

        def ctx(h):
            sec = section(mc, h, 3)
            ls = [strip_md(l.lstrip("> ").strip()) for l in sec.split("\n") if l.startswith("> **")]
            return short(" ".join(ls), 600)

        pj = picost.get(e["id"], {})
        sid = evd_src[e["id"]]
        bench = int(e["id"].split("-")[1]) if pj else None
        t.add([e["id"], e["title"], bench, "%s (%s)" % (cite_of.get(sid, ""), sid),
               "\n".join(quote_lines(desc)),
               img(quote_im) if quote_im else None,
               img(tf[0]) if len(tf) > 0 else None, img(tf[1]) if len(tf) > 1 else None,
               pj.get("P"), pj.get("I"), pj.get("C"), pj.get("O"), pj.get("S"), pj.get("T"),
               ctx("What?"), ctx("How?"), ctx("Who?"),
               "\n".join(out_edges(e["id"], "supports", "CLM")),
               "\n".join(in_edges(e["id"], "qualifies", "CVT")), e["curationStatus"]], height=175)
    t.finish()
    n_evd = len(by_type["EVD"])

    # CVT
    t = Tab(wb, "CVT", [("ID", 9), ("Caveat", 50), ("Type", 12), ("Severity", 10),
                        ("Applies to EVDs", 60), ("Supporting quote", 70), ("Status", 12)],
            [("Caveat accurate?", 14, YNF), ("Notes", 40, None)], tab_color="7030A0")
    for c in by_type["CVT"]:
        applies = out_edges(c["id"], "qualifies", "EVD")
        applies_clm = out_edges(c["id"], "qualifies", "CLM")
        t.add([c["id"], c["title"], c["extras"].get("caveatType"), c["extras"].get("severity"),
               lines(applies) + ("\n" if applies and applies_clm else "") + lines(applies_clm),
               "\n".join(quote_lines(section(c["bodyMarkdown"], "Supporting Quote", 3))), c["curationStatus"]])
    t.finish()

    # PICOST
    t = Tab(wb, "PICOST", [("EVD", 9), ("EVD title", 44), ("Source", 28), ("P", 34), ("I", 34), ("C", 34),
                           ("O", 38), ("S", 26), ("T", 26), ("Numbers parsed", 9), ("Locators status", 18)],
            [("PICOST accurate?", 14, YNF), ("Notes", 40, None)], tab_color="00B0F0")
    for e in by_type["EVD"]:
        pj = picost.get(e["id"])
        if not pj:
            continue
        t.add([e["id"], pj["evd_title"], pj["citekey"], pj["P"], pj["I"], pj["C"], pj["O"], pj["S"], pj["T"],
               len(pj["numbers"]), pj["locators_status"]])
    t.finish()
    n_picost = t.row - 3

    # SCREENING
    t = Tab(wb, "SCREENING", [("Paper", 40), ("Title", 56)],
            [("JP label", 13, INCLUDE), ("Notes", 40, None)],
            mid_cols=[("Decision-model P(include)", 14), ("Model decision", 14)],
            band_note="Seed set: all 27 papers are Include. JP will add Include/Exclude sets of dozens more "
                      "PDFs below the last row (dropdowns already extend to row 500).",
            tab_color="808080")
    t.ws.row_dimensions[1].height = 48
    for s in by_type["SRC"]:
        t.add([s["extras"]["citekey"], s["extras"].get("apaTitle", ""), None, None, "Include", None])
    t.finish(extra_rows=500 - (t.row - 1))

    # README
    ws = readme
    ws.sheet_properties.tabColor = "000000"
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 110
    rows = [
        ("LIVES vault mirror (JP review)", None),
        ("Purpose", "A readable copy of the LIVES vault for JP to judge. The markdown vault stays the source of "
                    "truth: change the vault, not this sheet, and rebuild. JP's judgments are recorded in the "
                    "orange 'JP accuracy judgment' columns on the right of every tab."),
        ("Built", "%s by scripts/vault_to_gsheet.py" % a.build_date),
        ("Source commit", "%s (graph file: %s)" % (commit, os.path.basename(a.graph))),
        ("Row counts", "SRC %d, QUE %d, CLM %d, EVD %d, CVT %d, PICOST %d, SCREENING %d" % (
            n_src, len(by_type["QUE"]), len(by_type["CLM"]), n_evd, len(by_type["CVT"]),
            n_picost, n_src)),
        ("How to judge", "1. Start on EVD. For each row read the headline statement, the quote and the screenshots, "
                         "then set Relevancy, Fidelity, Quote grounding, Table/Fig grounding and Numbers verified. "
                         "2. On PICOST, check P, I, C, O, S, T against the paper and set 'PICOST accurate?'. "
                         "3. On QUE set 'Wording OK?' and, for Edit or Split, type your wording. "
                         "4. On SRC, CLM and CVT set the accuracy dropdown. 5. Use Notes for anything else. "
                         "Rows stay in id order; use the filter arrows on row 2 to sort or filter."),
        ("Images", "Screenshots are =IMAGE() formulas that load from https://living-evidence-synthesis.vercel.app. "
                   "If a cell shows an error or an 'Allow access' prompt, click the cell and choose Allow access. "
                   "Images need internet and a deployed site."),
        ("Legend: Relevancy", "Relevant (green), Irrelevant (red), NA (grey). Is the EVD relevant to its review question?"),
        ("Legend: Fidelity", "Met (green), Partially Met (yellow), Unmet (red), NA (grey). Does every number in the quote match the paper?"),
        ("Legend: Grounding", "Correct (green), Partially Correct (yellow), Incorrect (red), Missing (grey), NA (grey). "
                              "Does the screenshot show the quote (Quote grounding) or the table/figure (Table/Fig grounding)?"),
        ("Legend: Yes / Needs fix / No", "Yes (green), Needs fix (yellow), No (red). Used for Numbers verified, PICOST accurate?, "
                                         "and the accuracy column on SRC, CLM and CVT."),
        ("Legend: Wording OK?", "OK (green), Edit (yellow), Split (blue), Drop (red). Question wording on QUE."),
        ("Legend: JP label", "Include (green), Exclude (red). Screening decision for a paper."),
        ("PICOST", "Legacy values imported from the 2026-11-17 PICOST tab. No page, table, row or column locators were "
                   "recorded, so numbers are not yet checked against the PDFs (locators status 'legacy-not-recorded'). "
                   "Benchmark # equals the EVD id number."),
        ("SCREENING", "The 27 seed papers are all Include. JP will add Include/Exclude sets of dozens more PDFs; "
                      "the dropdown and colours already cover rows down to 500. The decision-model columns are empty until a model run."),
    ]
    for i, (k, v) in enumerate(rows, 1):
        ca, cb = ws.cell(i, 1, k), ws.cell(i, 2, v)
        ca.alignment = cb.alignment = WRAP
        ca.font = Font(bold=True, size=14 if i == 1 else 11)
    ws.cell(1, 1).font = Font(bold=True, size=16)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    wb.save(a.out)
    print("wrote %s" % a.out)
    print("rows: SRC %d QUE %d CLM %d EVD %d CVT %d PICOST %d SCREENING %d" % (
        n_src, len(by_type["QUE"]), len(by_type["CLM"]), n_evd, len(by_type["CVT"]),
        n_picost, n_src))


if __name__ == "__main__":
    main()

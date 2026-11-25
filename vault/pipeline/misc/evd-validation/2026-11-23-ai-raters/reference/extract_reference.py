#!/usr/bin/env python3
"""Pull JP's and Claude's ratings out of an xlsx export of the main sheet into reference.csv.
ANALYSIS ONLY: run_raters.py and build_packets.py never read this folder (blinding).
Usage: python3 -I extract_reference.py <export.xlsx>"""
import csv, sys
from pathlib import Path
import openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True, read_only=True)
ws = wb["LIVES-EVD-Benchmarking"]
COLS = {"claude_relevancy": "G", "jp_relevancy": "I", "claude_fidelity": "K", "jp_fidelity": "M",
        "claude_quote": "O", "jp_quote": "Q", "claude_tablefig": "S", "jp_tablefig": "U",
        "claude_relevancy_note": "H", "jp_relevancy_note": "J", "claude_fidelity_note": "L", "jp_fidelity_note": "N",
        "claude_quote_note": "P", "jp_quote_note": "R", "claude_tablefig_note": "T", "jp_tablefig_note": "V"}
hdr = ["EVD"] + list(COLS)
out = Path(__file__).resolve().parent / "reference.csv"
rows = []
for r in range(2, 83):
    evd = ws[f"D{r}"].value
    if evd is None or "cont" in str(evd):
        continue
    rows.append([int(evd)] + [str(ws[f"{c}{r}"].value or "").replace("\n", " ") for c in COLS.values()])
with open(out, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(hdr); w.writerows(rows)
print(len(rows), "EVDs written to", out)

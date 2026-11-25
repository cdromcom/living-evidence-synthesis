#!/usr/bin/env python3
"""Put screenshot URLs (or the 'Missing' / 'Not on the live site' texts) back into the exported GSheet CSVs.
Google Sheets drops =IMAGE() cells on CSV export. Usage: python3 -I merge_image_urls.py <in.csv> <out.csv>"""
import csv, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_packets as bp
BASE = "https://living-evidence-synthesis.vercel.app/vault-img/"
status = json.load(open(HERE / "image_url_status.json"))
pages = sorted(((t or f.stem[6:], f, b) for f in bp.EVD_DIR.glob("EVD - *.md") for t, b in [bp.front(f.read_text())]), key=lambda x: x[0].lower())
def cell(nm): return BASE + nm if status.get(nm) == 200 else f"Not on the live site (HTTP {status.get(nm)}): {nm}"
cells = {}
for n, (title, f, body) in enumerate(pages, 1):
    sec = bp.sections(body); _, _, _, shots = bp.split_description(sec.get("Description", ""))
    tf = [s["file"] for s in shots if s["kind"] == "tablefig"]; qs = [s["file"] for s in shots if s["kind"] == "quote"]
    me = re.findall(r"!\[\[(.*?)\]\]", sec.get("Methods Context", ""))
    g = lambda L, i: cell(L[i]) if len(L) > i else ""
    cells[n] = {"Table/Figure screenshot 1": g(tf, 0), "Table/Figure screenshot 2": g(tf, 1), "Quote screenshot 1": g(qs, 0), "Quote screenshot 2": g(qs, 1),
                "Methods Context quote screenshot 1": g(me, 0), "Methods Context quote screenshot 2": g(me, 1), "Methods Context quote screenshot 3": g(me, 2), "Quote screenshot 3 (extra)": g(qs, 2)}
rows = list(csv.reader(open(sys.argv[1]))); hdr = rows[0]; out = [hdr]
for r in rows[1:]:
    n = int(r[0])
    for h, v in cells[n].items():
        i = hdr.index(h)
        if not r[i] and v: r[i] = v
    out.append(r)
csv.writer(open(sys.argv[2], "w", newline="")).writerows(out)
print(sys.argv[2], len(out) - 1, "rows")

#!/usr/bin/env python3
"""Map each EVD to the review question(s) it was found under, in JP's edited wording.

Pairing: the vault's DGRAPH-TABLE (a question is paired with an EVD when the EVD's paper is a 'Key Paper Asking' that
question). Wording: inputs/que_tab.csv (QUE tab of LIVES - AAA Benchmarking Results): JP's edit, else the original.
Output: questions_by_evd.json."""
import csv, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_packets as bp
ALIAS = {"Is LLM a reliable reviewer for automatic paper reviewing tasks?": "To which extent are LLMs accurate peer reviewers?"}
clean = {}
for r in csv.DictReader(open(HERE / "inputs/que_tab.csv")):
    a, c, d = r["llm_question"], r["jp_edited_question"].strip(), r["jp_verdict"].strip()
    if c in ("", "NA"): qs = [a]
    else:
        quoted = re.findall(r'["“]([^"”]+\?)["”]', c); numbered = re.findall(r"^\s*\d+\.\s*(.+\?)\s*$", c, re.M)
        qs = quoted or [x.strip() for x in numbered] or [c]
        dq = re.findall(r'\d+\.\s*["“]([^"”]+\?)["”]', d)
        if len(qs) == 1 and len(dq) >= 2: qs = dq      # a split described only in the verdict text
    clean[a] = qs
QU = []
for f in sorted((bp.VAULT / "questions").glob("QUE - *.md")):
    title, body = bp.front(f.read_text())
    keyp = re.search(r"### Key Papers Asking Question(.*?)###", body, re.S)
    QU.append({"title": title.strip(), "papers": set(re.findall(r"\[\[@([^\]|#]+)", keyp.group(1))) if keyp else set()})
pages = sorted(((bp.front(f.read_text())[0].strip(), bp.front(f.read_text())[1]) for f in bp.EVD_DIR.glob("EVD - *.md")), key=lambda t: t[0].lower())
out = {}
for n, (title, body) in enumerate(pages, 1):
    ck = bp.citekey_of(bp.sections(body).get("Source", ""))
    items = []
    for q in (q["title"] for q in QU if ck in q["papers"]):
        for t in clean.get(ALIAS.get(q, q), [q]):      # vault wording where the QUE tab has no row
            if t not in items: items.append(t)
    out[str(n)] = items[0] if len(items) == 1 else "\n".join("- " + t for t in items)
json.dump(out, open(HERE / "questions_by_evd.json", "w"), indent=2, ensure_ascii=False)
print(len(out), "EVDs mapped")

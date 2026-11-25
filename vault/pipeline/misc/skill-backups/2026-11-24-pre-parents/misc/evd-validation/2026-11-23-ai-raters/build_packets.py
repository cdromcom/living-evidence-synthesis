#!/usr/bin/env python3
"""NO PAPER TEXT OR PDFs go into packets (JP, 2026-11-23): models see only what is in the model-only GSheets.
Build blinded input packets for the three AI raters (Jev, Gemini Decision 1, Perplexity Decider 1.3).

BLINDING: every packet is built only from the vault (evidence pages, source PDFs, screenshots).
It never reads the Google Sheet, so no JP or Claude rating, note, draft or flag can leak in.
EVD numbers are derived from the alphabetical order of the vault page titles (the same order
as the sheet) and checked against a few known titles below.

Usage:  python3 -I build_packets.py            (writes ./packets/EVD-NN/)
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

import os
VAULT = Path(os.environ.get("LIVES_VAULT", Path(__file__).resolve().parent.parent / "vault"))  # the vault/ folder of this repository by default
EVD_DIR = VAULT / "evidence"
ATT = EVD_DIR / "Attachments"
PDF_DIR = VAULT / "source/pdfs"
OUT = Path(__file__).resolve().parent / "packets"
QUESTIONS = json.loads((Path(__file__).resolve().parent / "questions_by_evd.json").read_text())  # JP-edited review questions (QUE tab), mapped via paper
MAX_SIDE, MIN_SIDE = 1400, 280  # fits Perplexity (<=2048 32px tiles) and Jev (each side 280-1568 px, 78,400-2,458,624 px total)

# Titles copied from the sheet's EVD/title columns only (never ratings) to sanity-check numbering.
CHECK = {
    1: "39.18% of 3063 annotated biomedical citation instances contained accuracy errors",
    2: "57.4% of 308 researchers found GPT-4 feedback helpful",
    77: "Three AI platforms responded correctly to all 10 IRB case study queries",
}

LEAK_PATTERNS = [r"\bJP\b", r"\bJay\b", r"Jay Patel", r"Opus 5\.5", r"Selection error", r"FLAG for human",
                 r"\[JP", r"graded", r"Partially Met", r"human_reviewed: yes"]


def front(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = m.group(1) if m else ""
    t = re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M)
    return (t.group(1) if t else ""), text[m.end():] if m else text


def sections(body):
    parts = re.split(r"^## ", body, flags=re.M)
    return {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] if "\n" in p else "" for p in parts[1:]}


def clean(s):
    s = re.sub(r"!\[\[.*?\]\]", "", s)                       # image embeds
    s = re.sub(r"\[\[([^\]|]*)\|([^\]]*)\]\]", r"\2", s)     # [[a|b]] -> b
    s = re.sub(r"\[\[([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"^>\s*\[!info\].*$", "", s, flags=re.M)      # TRIPOD pointer callouts
    s = re.sub(r"^> ?", "", s, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def split_description(desc):
    """Return quote lines, grounding-table lines, and screenshots tagged quote / tablefig."""
    mode, quotes, grounding, other, shots = "quote", [], [], [], []
    for line in desc.splitlines():
        s = line.strip()
        em = re.findall(r"!\[\[(.*?)\]\]", s)
        if em:
            shots += [{"file": e, "kind": mode} for e in em]
            continue
        body = re.sub(r"^>\s*", "", s)
        if not body:
            continue
        if re.match(r"Grounding (table|figure)", body, re.I):
            mode = "tablefig"
            grounding.append(body)
        elif body.startswith('"') or re.search(r'"[^"]{30,}"\s*\([^)]*\d{4}', body):  # a quotation, also when a note precedes it
            mode = "quote"
            quotes.append(body)
        else:
            other.append(body)
    return quotes, grounding, other, shots


def citekey_of(src):
    m = re.search(r"\[\[@([^\]|#]+)", src)
    return m.group(1) if m else None


def resolve_pdf(citekey):
    if not PDF_DIR.exists():
        return None
    m = re.match(r"([a-z\-]+)", citekey)
    author = m.group(1).replace("-", "").lower()
    ym = re.search(r"(20\d\d)", citekey)
    year = ym.group(1) if ym else "@@"
    words = set(re.findall(r"[A-Z][a-z]+", citekey))
    best, score = None, -1
    for p in PDF_DIR.rglob("*.pdf"):  # rglob: superseded versions live in "Archive - superseded versions/"
        name = p.stem
        base = re.sub(r"^Archive - ", "", name)
        first = re.sub(r"[^a-z]", "", base.split(" ")[0].lower()) if "Hasan" not in base else "hasan"
        first = re.sub(r"[^a-z]", "", re.split(r" et al| and |_| - ", base)[0].lower())
        if not (first.startswith(author) or author.startswith(first)):
            continue
        sc = 3 if year in name else 0
        sc += 2 if name.startswith("Archive - ") else 0     # pages were built from the archived version (TODO 0d)
        sc += 0.2 * len([w for w in words if w.lower() in name.lower()])
        if sc > score:
            best, score = p, sc
    return best


def pdf_text(pdf):
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    pages = out.split("\f")
    return "\n".join(f"[[PDF page {i + 1}]]\n{t.strip()}" for i, t in enumerate(pages) if t.strip())


def prep_image(name, dest):
    src = ATT / name
    if not src.exists():
        return None
    im = Image.open(src).convert("RGB")
    w, h = im.size
    k = min(1.0, MAX_SIDE / max(w, h))
    if k != 1.0:
        im = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    w, h = im.size
    if min(w, h) < MIN_SIDE:  # pad with white instead of upscaling (Jev rejects, never resizes)
        canvas = Image.new("RGB", (max(w, MIN_SIDE), max(h, MIN_SIDE)), "white")
        canvas.paste(im, ((canvas.width - w) // 2, (canvas.height - h) // 2))
        im = canvas
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG")
    return dest.name


def main():
    pages = []
    for f in sorted(EVD_DIR.glob("EVD - *.md")):
        title, body = front(f.read_text())
        pages.append((title or f.stem[6:], f, body))
    pages.sort(key=lambda t: t[0].lower())
    # sheet numbering = alphabetical order of titles
    for n, t in CHECK.items():
        got = pages[n - 1][0]
        ratio = difflib.SequenceMatcher(None, got.lower(), t.lower()).ratio()
        if not (got.lower().startswith(t.lower()[:40]) or ratio > 0.8):
            sys.exit(f"Numbering check failed for EVD {n}: vault has '{got}' but expected '{t}'")
    OUT.mkdir(exist_ok=True)
    manifest, leaks, paper_cache = [], [], {}
    for n, (title, f, body) in enumerate(pages, 1):
        sec = sections(body)
        quotes, grounding, other, shots = split_description(sec.get("Description", ""))
        ck = citekey_of(sec.get("Source", ""))
        pdf = resolve_pdf(ck) if ck else None
        d = OUT / f"EVD-{n:02d}"
        imgs = []
        for i, s in enumerate(shots, 1):
            nm = prep_image(s["file"], d / f"{s['kind']}-{i}.png")
            if nm:
                imgs.append({"file": nm, "kind": s["kind"], "orig": s["file"]})
        methods = clean(sec.get("Methods Context", ""))
        packet = {
            "evd": n, "evd_statement": title, "review_questions": QUESTIONS[str(n)], "citekey": ck, "pdf": pdf.name if pdf else None,
            "quote_text": "\n".join(quotes),
            "description_other_text": "\n".join(other),
            "grounding_table_text": "\n".join(grounding),
            "methods_context": methods,
            "images": imgs,
        }
        d.mkdir(exist_ok=True)
        (d / "packet.json").write_text(json.dumps(packet, indent=1))
        vault_text = "\n".join([title, packet["quote_text"], packet["description_other_text"],
                                packet["grounding_table_text"], methods])
        for pat in LEAK_PATTERNS:
            for m in re.finditer(pat, vault_text):
                leaks.append((n, pat, vault_text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")))
        manifest.append({"evd": n, "title": title, "page": f.name, "pdf": packet["pdf"],
                         "quote_images": sum(1 for i in imgs if i["kind"] == "quote"),
                         "tablefig_images": sum(1 for i in imgs if i["kind"] == "tablefig"),
                         "quote_chars": len(packet["quote_text"])})
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"{len(manifest)} packets written to {OUT}")
    print("EVD  pdf  (check each mapping)")
    for m in manifest:
        flag = "  <-- NO PDF" if not m["pdf"] else ""
        print(f"{m['evd']:>3}  {m['pdf']}  q-img={m['quote_images']} tf-img={m['tablefig_images']}{flag}")
    print(f"\nBlinding scan of vault-derived text: {len(leaks)} hits")
    for l in leaks[:40]:
        print("  EVD", l[0], l[1], "|", l[2])


if __name__ == "__main__":
    main()

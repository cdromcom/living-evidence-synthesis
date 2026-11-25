"""Unified quote-region extraction pipeline using PyMuPDF.

Replaces the prior pdftotext -bbox-layout + pdftoppm pipeline. Same logic
(opening/closing word match → padded bbox → cropped PNG) but immune to
poppler crashes on certain PDFs.

Usage:
    python3 extract_quotes.py <pdf_path> <out_dir> <citekey> <quotes_json>

Where quotes_json is a path to a JSON file of:
    [
      {"label": "evd-foo-p3", "page": 3, "opening": "We find that", "closing": "p < 0.05."},
      ...
    ]

Page numbers are 1-based. Output filenames: <citekey>-<label>.png
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def find_quote(words, opening: str, closing: str):
    """words: list of (x0, y0, x1, y1, word_text). Returns (start_idx, end_idx) or None."""
    norm_words = [normalize(w[4]) for w in words]
    concat = ""
    char_to_idx = []
    for i, nw in enumerate(norm_words):
        concat += nw
        char_to_idx.extend([i] * len(nw))
    no = normalize(opening)
    nc = normalize(closing)
    s = concat.find(no)
    if s == -1:
        return None
    e = concat.find(nc, s + len(no))
    if e == -1:
        return None
    return char_to_idx[s], char_to_idx[e + len(nc) - 1]


def bbox_of_range(words, start: int, end: int, padding: float = 8.0):
    chunk = words[start : end + 1]
    return (
        min(w[0] for w in chunk) - padding,
        min(w[1] for w in chunk) - padding,
        max(w[2] for w in chunk) + padding,
        max(w[3] for w in chunk) + padding,
    )


def render_crop(page, bbox: tuple, out_path: Path, dpi: int = 250):
    rect = fitz.Rect(*bbox)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=rect)
    pix.save(str(out_path))


def main():
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    citekey = sys.argv[3]
    quotes_json = Path(sys.argv[4])
    quotes = json.loads(quotes_json.read_text())

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))

    for q in quotes:
        label = q["label"]
        page_num = q["page"]
        opening = q["opening"]
        closing = q["closing"]
        page = doc[page_num - 1]
        words = page.get_text("words")  # list of (x0,y0,x1,y1,text,bn,ln,wn)
        match = find_quote(words, opening, closing)
        if not match:
            print(f"NOT_FOUND\t{label}\tpage={page_num}\topening='{opening}'", file=sys.stderr)
            continue
        s, e = match
        bbox = bbox_of_range(words, s, e)
        out_path = out_dir / f"{citekey}-{label}.png"
        render_crop(page, bbox, out_path)
        first = words[s][4]
        last = words[e][4]
        print(f"OK\t{label}\tpage={page_num}\tfirst='{first}'\tlast='{last}'\tfile={out_path.name}")

    doc.close()


if __name__ == "__main__":
    main()

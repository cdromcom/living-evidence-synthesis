#!/usr/bin/env python3
"""Grounding crops for SRC pages (JP, 2026-11-27): one PNG per table or figure that a page cites, cut from the source PDF with PyMuPDF, no model and no network.
Rules of Skill-templates.md ("Grounding rules for screenshots"): the table or figure and its caption only, every row, column and panel, no body text, no neighbouring table or figure.

  find_caption(doc, kind, num)            (PDF page, caption rect, caption text) of 'Table 2' or 'Figure 1' (a block that starts with the label followed by a period or colon), or None
  crop_region(doc, kind, num)             the rectangle to cut and how it was found; a table uses the PyMuPDF table box next to its caption (plus footnote lines under it), a figure uses the images and drawings next to its caption
  make_crop(doc, kind, num, out_png)      writes the PNG; returns the record {'file','pdf_page','bbox','caption','method'} or {'error': ...}
  embed_name(citekey, kind, num, page)    '<citekey>-src-table2-p5.png' (the 'src' keeps the name different from the EVD crops '<citekey>-table2-p5-1.png', because the vault resolves an embed by its bare file name)
  embeds_resolve(text, dirs)              [(embed name, found)] for every ![[...]] image embed of a page; found means a file of that name exists in one of the folders"""
import re
from pathlib import Path
import fitz
fitz.TOOLS.mupdf_display_errors(False)

LABEL = {'table': r'(?:Table|TABLE)', 'figure': r'(?:Figure|FIGURE|Fig\.|FIG\.)'}
DPI = 200; PAD = 6


def embed_name(citekey, kind, num, page):
    return f'{citekey}-src-{kind}{num}-p{page}.png'


def _blocks(page):
    return [b for b in page.get_text('blocks') if b[6] == 0 and b[4].strip()]


def find_caption(doc, kind, num):
    pat = re.compile(rf'^\s*{LABEL[kind]}\s+{re.escape(str(num))}\s*[.:]')
    for i, p in enumerate(doc):
        for b in _blocks(p):
            if pat.match(b[4]): return i + 1, fitz.Rect(b[:4]), ' '.join(b[4].split())
    return None


def _small_text_below(page, rect, body_size, gap=30):
    """Footnote lines directly under a table: text blocks within `gap` points below it that start with a note marker or are set in a smaller type size."""
    out = fitz.Rect(rect)
    for _ in range(4):
        grew = False
        for b in page.get_text('dict')['blocks']:
            if b['type'] != 0: continue
            r = fitz.Rect(b['bbox']); text = ' '.join(s['text'] for l in b['lines'] for s in l['spans']).strip()
            if not text or r.y0 < out.y1 - 1 or r.y0 - out.y1 > gap or r.x1 < out.x0 or r.x0 > out.x1: continue
            n = max(sum(len(s['text']) for l in b['lines'] for s in l['spans']), 1); size = sum(s['size'] * len(s['text']) for l in b['lines'] for s in l['spans']) / n
            norm = ' '.join(text.split())
            if re.match(r'[A-Z][A-Za-z0-9\-]{1,12},\s', norm) and ';' in norm: out |= r; grew = True; continue   # an abbreviation list under the table (AMSTAR, A MeaSurement Tool ...; LLM, large language model)
            if re.match(r'[*†‡§¶¹²³⁰-⁹]|[a-d]\s|(?:Note|Notes|Source|Abbreviations?)\b', text) or size <= body_size - 0.4:
                out |= r; grew = True
        if not grew: break
    return out


def _body_size(page):
    sizes = sorted(s['size'] for b in page.get_text('dict')['blocks'] if b['type'] == 0 for l in b['lines'] for s in l['spans'] for _ in range(max(len(s['text'].strip()), 0)))
    return sizes[len(sizes) // 2] if sizes else 10.0


def _table_region(page, cap):
    tabs = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
    if not tabs: return None
    below = [t for t in tabs if t.y0 >= cap.y0 - 2]; above = [t for t in tabs if t.y1 <= cap.y1 + 2]
    t = min(below, key=lambda r: r.y0 - cap.y1) if below and (not above or min(r.y0 - cap.y1 for r in below) <= 60) else (max(above, key=lambda r: r.y1) if above else None)
    if t is None: return None
    reg = cap | t
    return _small_text_below(page, reg, _body_size(page)) if cap.y1 <= t.y0 + 2 else reg


def _figure_region(page, cap, other_tables):
    """The images and drawings next to the caption (above it, or below it for a caption on top), grown while the next one lies within 24 points; text blocks inside the grown box are included."""
    items = []
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]): items.append(fitz.Rect(r))
    for d in page.get_drawings():
        r = fitz.Rect(d['rect'])
        if r.width < 3 and r.height < 3: continue
        if any(r.intersects(t) for t in other_tables): continue
        items.append(r)
    items = [r for r in items if r.width > 4 or r.height > 4]
    if not items: return None
    for direction in ('above', 'below'):
        cand = [r for r in items if (r.y1 <= cap.y0 + 4 if direction == 'above' else r.y0 >= cap.y1 - 4)]
        if not cand: continue
        reg = fitz.Rect(cap); added = True; used = set()
        while added:
            added = False
            for i, r in enumerate(cand):
                if i in used: continue
                gap = (reg.y0 - r.y1) if direction == 'above' else (r.y0 - reg.y1)
                inside_y = r.y1 >= reg.y0 - 24 and r.y0 <= reg.y1 + 24
                if inside_y and gap <= 24 and r.x1 > reg.x0 - 5 and r.x0 < reg.x1 + 5: reg |= r; used.add(i); added = True
            for b in _blocks(page):
                br = fitz.Rect(b[:4])
                if br.intersects(reg) and not br.contains(reg) and br not in (cap,): reg |= br
        if len(used) >= 1: return reg
    return None


def crop_region(doc, kind, num):
    c = find_caption(doc, kind, num)
    if not c: return None, 'caption not found in the PDF text'
    pg, cap, text = c; page = doc[pg - 1]
    try:
        if kind == 'table':
            reg = _table_region(page, cap)
            if reg is not None: return (pg, reg, text, 'PyMuPDF table box next to the caption, plus footnote lines'), None
            return None, 'no table box found next to the caption'
        others = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
        reg = _figure_region(page, cap, others)
        if reg is not None: return (pg, reg, text, 'images and drawings next to the caption'), None
        return None, 'no image or drawing found next to the caption'
    except Exception as e:
        return None, f'{type(e).__name__}: {str(e)[:120]}'


def make_crop(doc, kind, num, out_png):
    r, err = crop_region(doc, kind, num)
    if r is None: return {'error': err}
    pg, reg, text, how = r; page = doc[pg - 1]
    clip = (reg + (-PAD, -PAD, PAD, PAD)) & page.rect
    pix = page.get_pixmap(dpi=DPI, clip=clip)
    if pix.width < 40 or pix.height < 20: return {'error': f'crop too small ({pix.width}x{pix.height})'}
    Path(out_png).parent.mkdir(parents=True, exist_ok=True); pix.save(str(out_png))
    return {'file': Path(out_png).name, 'pdf_page': pg, 'bbox': [round(x, 1) for x in clip], 'caption': text, 'method': how, 'pixels': [pix.width, pix.height]}


EMBED = re.compile(r'!\[\[([^\]|\n]+\.(?:png|jpg|jpeg|gif|webp))(?:\|[^\]]*)?\]\]', re.I)


def embeds_resolve(text, dirs):
    names = []
    for m in EMBED.finditer(text):
        n = m.group(1).strip()
        if n not in names: names.append(n)
    return [(n, any((Path(d) / n).exists() or (Path(d) / Path(n).name).exists() for d in dirs)) for n in names]

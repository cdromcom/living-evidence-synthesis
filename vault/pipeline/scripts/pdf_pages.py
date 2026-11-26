#!/usr/bin/env python3
"""PDF backbone for the Skill (v2): page map, quote locator, verbatim check, quote crop, link extraction. Needs PyMuPDF.

  python3 pdf_pages.py map  <pdf>                 printed page label for every PDF page
  python3 pdf_pages.py find <pdf> "quote text"    where the quote appears (PDF page, printed page)
  python3 pdf_pages.py crop <pdf> "quote" out.png [--dpi 250] [--kind EVD|CLM|QUE|EP|CVT]   crop of the quote region, highlighted in that node type's pastel
  python3 pdf_pages.py links <pdf>                hyperlinks embedded in the PDF (code and data URLs)
  merge_regions(pdf, [(page, [rects]), ...], out)  one screenshot from pieces on several pages, stacked with a thin white gap (see its docstring)

Printed page = the number printed on the page (the journal page), NOT the position in the PDF file. If the file prints no page
numbers (preprints), the map falls back to the PDF position and marks it source='pdf-position'; record that in the locator."""
import os, re, sys, unicodedata
from pathlib import Path
import fitz  # PyMuPDF
fitz.TOOLS.mupdf_display_errors(False)   # silence harmless MuPDF colour-space warnings

VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
PDF_DIR = VAULT / 'sysrev' / 'dgraph' / 'source' / 'pdfs'
_FIX = {'¼': '=', '−': '-', '‐': '-', '‑': '-', '‒': '-', '–': '-', '—': '-', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}


_SUP_SUB = dict.fromkeys(map(ord, '\u00b9\u00b2\u00b3\u2070\u2074\u2075\u2076\u2077\u2078\u2079\u207a\u207b\u207c\u207d\u207e\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089\u208a\u208b\u208c\u208d\u208e\u2020\u2021'), None)


def norm(s: str) -> str:
    """Letters and digits only, lower case, so punctuation never decides a match: dashes, curly quotes, hyphenated line breaks, ligatures, footnote
    superscripts and subscripts are ignored. The one exception is the decimal point between digits (0.79 must not match 079): it becomes 'dot'."""
    s = re.sub(r'-\s*\n\s*', '', s)
    s = ''.join(_FIX.get(c, c) for c in s).translate(_SUP_SUB)   # superscript and subscript marks (footnote numbers, daggers) are dropped, not turned into digits
    s = unicodedata.normalize('NFKD', s)
    s = re.sub(r'(?<=[\d%)])e(?=\d)', '', s)   # some PDFs map an en dash between numbers to the letter e in the text layer ("0.78e0.83"); dropping it on both sides keeps a visible "0.78\u20130.83" matching
    s = re.sub(r'(?<=\d)\.(?=\d)', 'dot', s)
    return re.sub(r'[^a-z0-9]', '', s.lower())


def page_map(doc) -> list:
    """Printed label for each PDF page: PDF page labels if the file has them, else the page number printed in the header or footer,
    else inferred from a constant offset. Returns [{'pdf': 1-based, 'printed': str|None, 'source': 'label'|'text'|'offset'|None}]."""
    n = len(doc); out = []; offs = []
    for i, page in enumerate(doc):
        lab = (page.get_label() or '').strip()
        src = 'label' if lab else None
        if not lab:
            lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]
            cand = lines[:3] + lines[-3:]
            nums = [l for l in cand if re.fullmatch(r'\d{1,4}', l)]
            if nums:
                lab, src = nums[-1], 'text'
        out.append({'pdf': i + 1, 'printed': lab or None, 'source': src})
        if lab.isdigit(): offs.append(int(lab) - (i + 1))
    if not offs:   # no printed numbers in the file (typical for preprints): the PDF position is the page reference; flag it
        for r in out: r['printed'] = str(r['pdf']); r['source'] = 'pdf-position'
    if offs:
        off = max(set(offs), key=offs.count)
        for r in out:
            if r['printed'] is None and offs.count(off) >= 3:
                r['printed'] = str(r['pdf'] + off); r['source'] = 'offset'
    return out


def page_text(page) -> str:
    """Page text without superscript spans (footnote numbers, daggers) and without tiny-font marks, so 'OpenReview5 we' reads 'OpenReview we'."""
    d = page.get_text('dict'); sizes = [sp['size'] for b in d['blocks'] if b.get('type') == 0 for l in b['lines'] for sp in l['spans'] if sp['text'].strip()]
    med = sorted(sizes)[len(sizes) // 2] if sizes else 10; out = []
    for b in d['blocks']:
        if b.get('type') != 0: continue
        for l in b['lines']:
            out.append(''.join(sp['text'] for sp in l['spans'] if not (sp['flags'] & 1) and not (sp['size'] < 0.72 * med and sp['text'].strip().isdigit())))
            out.append('\n')
    return ''.join(out)


_NORM_CACHE = {}


def _norms(doc):
    k = id(doc)
    if k not in _NORM_CACHE:
        _NORM_CACHE.clear(); _NORM_CACHE[k] = ([norm(page_text(p)) for p in doc], [norm(p.get_text()) for p in doc])
    return _NORM_CACHE[k]


def _page_texts(doc):
    return [page_text(p) for p in doc]


def find_quote(doc, quote: str, min_frag: int = 18) -> dict:
    """Locate a quote. Quotes with '...' are checked fragment by fragment. A fragment is on the page whose own text contains it;
    only if no page does, it may run across a page break (then the page where it starts is reported).
    Returns {'found': bool, 'fragments': [{'text','pages':[pdf pages],'ok':bool}], 'pages': sorted pdf pages}."""
    frags = [f.strip() for f in re.split(r'\.{3}|\u2026|\[\.\.\.\]', quote) if len(norm(f)) >= min_frag]
    if not frags: frags = [quote]
    nc, nr = _norms(doc)   # cleaned text (no footnote marks) and raw text, computed once per document: a quote may or may not include the marks
    nt = [a + '\x00' + b for a, b in zip(nc, nr)]
    res = []
    for f in frags:
        k = norm(f)
        pages = [i + 1 for i, t in enumerate(nt) if k and k in t]
        if not pages:   # across a page break: tail of page i plus head of page i+1
            pages = [i + 1 for i in range(len(nc) - 1) if k and (k in (nc[i][-600:] + nc[i + 1][:600]) or k in (nr[i][-600:] + nr[i + 1][:600]))]
        if not pages and len(f.split()) >= 16:   # a float (figure or table caption) can sit inside a sentence in the text layer: match the sentence in 2 or 3 pieces on one page
            w = f.split()
            for k in (2, 3):
                step = len(w) // k; chunks = [norm(' '.join(w[i * step:(i + 1) * step if i < k - 1 else len(w)])) for i in range(k)]
                pages = [i + 1 for i, t in enumerate(nt) if all(c and c in t for c in chunks)]
                if pages: break
        res.append({'text': f[:80], 'pages': pages, 'ok': bool(pages)})
    allp = sorted({p for r in res for p in r['pages']})
    return {'found': all(r['ok'] for r in res), 'fragments': res, 'pages': allp}


def repair_quote(doc, quote: str, hint_page: int = None, min_cov: float = 0.9):
    """A quote that is not verbatim in the PDF text (a dropped word, a changed symbol, a different hyphenation) is replaced by the PDF's own words when at
    least min_cov of its letters and digits (compared with norm) match one stretch of one page. Looks at the cited page first, then every page. Returns
    {'text', 'page', 'coverage'} or None. Never changes a quote that is found; never invents words (the replacement is copied from the page)."""
    import difflib
    qn = norm(quote)
    if len(qn) < 40: return None
    order = ([hint_page] if hint_page and 1 <= hint_page <= len(doc) else []) + [i for i in range(1, len(doc) + 1) if i != hint_page]; best = None
    for pg in order:
        words = page_text(doc[pg - 1]).split(); parts = [norm(w) for w in words]
        if not any(parts): continue
        txt = ''.join(parts); owner = [wi for wi, part in enumerate(parts) for _ in part]
        sm = difflib.SequenceMatcher(None, txt, qn, autojunk=False); blocks = [b for b in sm.get_matching_blocks() if b.size >= 5]
        for i, b in enumerate(blocks):   # a run of blocks that fits inside one quote-length stretch of the page
            j = i; matched = b.size; end_a = b.a + b.size; end_b = b.b + b.size
            while j + 1 < len(blocks) and blocks[j + 1].a + blocks[j + 1].size - b.a <= len(qn) + 20 and blocks[j + 1].b >= end_b - 3: j += 1; matched += blocks[j].size; end_a = blocks[j].a + blocks[j].size; end_b = blocks[j].b + blocks[j].size
            cov = matched / len(qn)
            if cov >= min_cov and (best is None or cov > best['coverage']):
                a0 = max(0, b.a - b.b); a1 = min(len(txt), end_a + (len(qn) - end_b))
                best = {'text': ' '.join(words[owner[a0]:owner[a1 - 1] + 1]), 'page': pg, 'coverage': round(cov, 3)}
        if best and best['coverage'] >= 0.97: break   # a near-perfect match on the cited page is enough
    return best


def _light(s: str) -> str:
    """Gentle normalization for judging whether a quote is character-for-character the PDF's text: ligatures, curly quotes and dashes, line-break hyphens and spacing only."""
    s = re.sub(r'-\s*\n\s*', '', s); s = unicodedata.normalize('NFKC', s)
    for a_, b_ in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'), ('\u2013', '-'), ('\u2014', '-'), ('\u2212', '-'), ('\u00ad', '')): s = s.replace(a_, b_)
    return re.sub(r'\s+', ' ', s).strip().lower()


def match_level(doc, quote: str, pages) -> str:
    """'exact' when the quote is the PDF's text apart from spacing, line-break hyphens, ligatures and curly quotes or dashes; otherwise 'letters_digits' (the same letters and digits, but a symbol or punctuation differs, for example an equals sign or an en dash). Call it for a quote that find_quote found."""
    q = _light(quote)
    for pg in pages or []:
        if q and q in _light(page_text(doc[pg - 1])): return 'exact'
    return 'letters_digits'


def clean_text(raw: str) -> str:
    """The PDF text with its extraction artifacts undone where that is certain: ligatures (NFKC), soft hyphens, a hyphen plus space inside a word broken at a line end ('previ- ous'), and the glyph for one quarter used as an equals sign ('P ¼ .0085')."""
    s = unicodedata.normalize('NFKC', raw).replace('\u00ad', '')
    s = re.sub(r'(?<=[a-z])-\s+(?=[a-z])', '', s)
    s = re.sub(r'\s¼\s', ' = ', s)
    return re.sub(r'\s+', ' ', s).strip()


def text_between(doc, start: str, end: str, hint_page: int = None, max_chars: int = 1200):
    """JP, 2026-11-26: the exact PDF text from where `start` begins to where `end` ends (both are a few words a model copied from the page). The quote is taken from the PDF itself, so it is the PDF's own words by construction. Looks on the hinted page first, then all pages. Returns {'raw', 'text', 'page'} (raw = the text layer as is, text = clean_text of it) or None."""
    sn, en = norm(start), norm(end)
    if len(sn) < 10 or len(en) < 10: return None
    order = ([hint_page] if hint_page and 1 <= hint_page <= len(doc) else []) + [i for i in range(1, len(doc) + 1) if i != hint_page]
    for pg in order:
        words = page_text(doc[pg - 1]).split(); parts = [norm(w) for w in words]; txt = ''.join(parts)
        i = txt.find(sn)
        if i < 0: continue
        owner = [wi for wi, part in enumerate(parts) for _ in part]; j = txt.find(en, i); endlen = len(en); how = 'anchors'
        if j < 0:   # the end anchor has a wrong word: try its last 5, 4 and 3 words, then fall back to the end of the sentence that holds the start
            ew = end.split()
            for k in (5, 4, 3):
                tail = norm(' '.join(ew[-k:]))
                if len(tail) >= 10 and txt.find(tail, i) >= 0: j = txt.find(tail, i); endlen = len(tail); how = 'anchors (end repaired)'; break
        if j < 0:
            w0 = owner[i]; wi = w0
            while wi < len(words) - 1 and not (re.search(r'[.?!]$', words[wi]) and wi - w0 >= 3 and (wi + 1 >= len(words) or words[wi + 1][:1].isupper())): wi += 1
            raw = ' '.join(words[w0:wi + 1]); how = 'anchors (start only: sentence end)'
        else: raw = ' '.join(words[owner[i]:owner[j + endlen - 1] + 1])
        if len(raw) <= max_chars: return {'raw': raw, 'text': clean_text(raw), 'page': pg, 'how': how}
    return None


def locate_rects(page, quote: str):
    """Exact word rectangles of a quote on one page: match the quote's normalized text inside the page's normalized word stream
    (robust to hyphenated line breaks and ligatures), then return the boxes of the covered words."""
    words = page.get_text('words')   # (x0, y0, x1, y1, word, block, line, wordno)
    stream, spans = '', []
    for w in words:
        t = norm(w[4])
        if t: spans.append((len(stream), len(stream) + len(t), fitz.Rect(w[:4]))); stream += t
    k = norm(quote); i = stream.find(k)
    if i < 0 or not k: return []
    return [r for (s0, s1, r) in spans if s1 > i and s0 < i + len(k)]


# Highlight colors by node type (JP, 2026-11-25): light pastels, easy on the eyes. RGB 0-1.
HIGHLIGHT = {'QUE': (1.0, 0.86, 0.68),   # light orange
             'EVD': (1.0, 0.80, 0.80),   # light red
             'CLM': (0.80, 0.93, 0.82),  # light green (mint, not lime)
             'EP': (0.80, 0.88, 1.0),    # light blue
             'CVT': (0.86, 0.86, 0.87)}  # soft gray


def crop_quote(doc, quote: str, out: str, dpi: int = 250, pad: float = 14, kind: str = 'EVD', box_outline: bool = False, tight_x: bool = False) -> dict:   # box_outline draws a thin blue rectangle around the whole quote (JP, 2026-11-26)
    hit = find_quote(doc, quote)
    if not hit['pages']: return {'ok': False, 'reason': 'quote not found'}
    page = doc[hit['pages'][0] - 1]
    rects = locate_rects(page, quote.split('...')[0].split('…')[0])
    if not rects: return {'ok': False, 'reason': 'found in text but no word coordinates (scanned or odd encoding)'}
    box = fitz.Rect(rects[0])
    for r in rects[1:]: box |= r
    lines = {}   # one band per text line, drawn behind the text, so the color is exactly the pastel (annotation highlights blend to tan)
    for r in rects: lines.setdefault(round(r.y0 / 3), fitz.Rect(r)).include_rect(r)
    for r in lines.values(): page.draw_rect(fitz.Rect(r.x0 - 1, r.y0 - 0.5, r.x1 + 1, r.y1 + 0.5), color=None, fill=HIGHLIGHT.get(kind, HIGHLIGHT['EVD']), overlay=False)
    if box_outline: page.draw_rect(fitz.Rect(box.x0 - 3, box.y0 - 2, box.x1 + 3, box.y1 + 2), color=(0.1, 0.3, 0.75), fill=None, width=1.3, overlay=True)
    x0, x1 = page.rect.x0, page.rect.x1
    if tight_x:   # only the width of the quote's own column or table, so the text stays large enough to read in a spreadsheet cell
        x0 = max(page.rect.x0, box.x0 - 24); x1 = min(page.rect.x1, box.x1 + 24)
        if x1 - x0 < 260: mid = (x0 + x1) / 2; x0 = max(page.rect.x0, mid - 130); x1 = min(page.rect.x1, mid + 130)
    clip = fitz.Rect(x0, max(page.rect.y0, box.y0 - pad), x1, min(page.rect.y1, box.y1 + pad))
    page.get_pixmap(dpi=dpi, clip=clip).save(out)
    return {'ok': True, 'pdf_page': hit['pages'][0], 'out': out, 'size_px': Path(out).stat().st_size}


def merge_regions(pdf, regions, out, dpi: int = 200, pad: float = 6, gap_px: int = 10, kind: str = 'EVD', max_height_px: int = 0) -> dict:
    """One screenshot from pieces on several pages (a table, figure or quote that runs over a page break) (JP, 2026-11-25).
    regions = [(pdf_page, [(x0, y0, x1, y1), ...]), ...] in reading order (the rectangles are the word boxes of the highlighted text, e.g. spans' 'bbox').
    Each piece is the full page width and the band from the first to the last rectangle on that page plus `pad` points, with the text lines highlighted
    in the node type's pastel; the pieces are stacked top to bottom with `gap_px` pixels of white between them, so the join looks like one continuous page.
    A fresh copy of the PDF is opened, so the caller's document is not marked."""
    from PIL import Image
    d = fitz.open(pdf if isinstance(pdf, (str, Path)) else pdf.name); pieces = []
    for pg, rects in regions:
        page = d[pg - 1]; rs = [fitz.Rect(*r) for r in rects]
        if not rs: return {'ok': False, 'reason': f'no rectangles for page {pg}'}
        lines = {}
        for r in rs: lines.setdefault(round(r.y0 / 3), fitz.Rect(r)).include_rect(r)
        for r in lines.values(): page.draw_rect(fitz.Rect(r.x0 - 1, r.y0 - 0.5, r.x1 + 1, r.y1 + 0.5), color=None, fill=HIGHLIGHT.get(kind, HIGHLIGHT['EVD']), overlay=False)
        box = fitz.Rect(rs[0]);
        for r in rs[1:]: box |= r
        allw = [fitz.Rect(w[:4]) for w in page.get_text('words')]   # snap the band to the gap between text lines, so no sliver of the neighbouring line shows at the join
        below = [w.y0 for w in allw if w.y0 > box.y1 - 0.5 and not any(abs(w.y0 - r.y0) < 1 and w.x0 >= r.x0 - 1 and w.x1 <= r.x1 + 1 for r in rs)]; above = [w.y1 for w in allw if w.y1 < box.y0 + 0.5 and not any(abs(w.y0 - r.y0) < 1 and w.x0 >= r.x0 - 1 and w.x1 <= r.x1 + 1 for r in rs)]
        y_bot = min([box.y1 + pad] + [y - 0.5 for y in below if y >= box.y1 - 0.5]); y_top = max([box.y0 - pad] + [y + 0.5 for y in above if y <= box.y0 + 0.5])
        clip = fitz.Rect(page.rect.x0, max(page.rect.y0, min(y_top, box.y0)), page.rect.x1, min(page.rect.y1, max(y_bot, box.y1)))
        pm = page.get_pixmap(dpi=dpi, clip=clip); pieces.append(Image.frombytes('RGB', (pm.width, pm.height), pm.samples))
    d.close()
    W = max(i.width for i in pieces); H = sum(i.height for i in pieces) + gap_px * (len(pieces) - 1); img = Image.new('RGB', (W, H), 'white'); y = 0
    for i in pieces: img.paste(i, (0, y)); y += i.height + gap_px
    if max_height_px and H > max_height_px: img = img.resize((round(W * max_height_px / H), max_height_px))
    img.save(out); return {'ok': True, 'pages': [pg for pg, _ in regions], 'out': str(out), 'size_px': img.size}


def links(doc) -> list:
    out = []
    for i, page in enumerate(doc):
        for l in page.get_links():
            if l.get('uri'): out.append({'pdf_page': i + 1, 'uri': l['uri']})
    return out


def resolve_pdf(citekey: str):
    """Top-level PDF in the vault's pdf folder for a citekey like @akyonEvaluatingCapabilitiesGenerative2024."""
    ck = citekey.lstrip('@'); m = re.match(r'([a-z\-]+)', ck)
    if not m: return None
    author = m.group(1).replace('-', '').lower(); ym = re.search(r'(20\d\d)', ck); year = ym.group(1) if ym else '@@'
    words = {w.lower() for w in re.findall(r'[A-Z][a-z]+', ck)}
    best, score = None, -1
    for p in PDF_DIR.glob('*.pdf'):
        name = p.stem; first = re.sub(r'[^a-z]', '', re.split(r' et al| and |_| - ', name)[0].lower())
        if not (first.startswith(author) or author.startswith(first)): continue
        sc = (3 if year in name else 0) + 0.2 * sum(w in name.lower() for w in words)
        if sc > score: best, score = p, sc
    return best


if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    cmd, pdf = sys.argv[1], sys.argv[2]
    doc = fitz.open(pdf)
    if cmd == 'map':
        for r in page_map(doc): print(r['pdf'], r['printed'], r['source'])
    elif cmd == 'find':
        pm = {r['pdf']: r['printed'] for r in page_map(doc)}; h = find_quote(doc, sys.argv[3])
        print('found' if h['found'] else 'NOT FOUND', [(p, pm.get(p)) for p in h['pages']])
    elif cmd == 'crop':
        print(crop_quote(doc, sys.argv[3], sys.argv[4], int(sys.argv[sys.argv.index('--dpi') + 1]) if '--dpi' in sys.argv else 250,
                         kind=sys.argv[sys.argv.index('--kind') + 1] if '--kind' in sys.argv else 'EVD'))
    elif cmd == 'links':
        for l in links(doc): print(l['pdf_page'], l['uri'])

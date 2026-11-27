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
    lines = {}   # one band per text line, drawn over the text at 35% opacity so it shows on shaded table rows too
    for r in rects: lines.setdefault(round(r.y0 / 3), fitz.Rect(r)).include_rect(r)
    for r in lines.values(): page.draw_rect(fitz.Rect(r.x0 - 1, r.y0 - 0.5, r.x1 + 1, r.y1 + 0.5), color=None, fill=HIGHLIGHT.get(kind, HIGHLIGHT['EVD']), fill_opacity=0.35, overlay=True)   # drawn over the page, see-through: a band behind the text vanished under shaded table rows (Bougie Table 5), which made the wrong row look highlighted
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
        for r in lines.values(): page.draw_rect(fitz.Rect(r.x0 - 1, r.y0 - 0.5, r.x1 + 1, r.y1 + 0.5), color=None, fill=HIGHLIGHT.get(kind, HIGHLIGHT['EVD']), fill_opacity=0.35, overlay=True)   # drawn over the page, see-through: a band behind the text vanished under shaded table rows (Bougie Table 5), which made the wrong row look highlighted
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

# ---------------------------------------------------------------- table cells and symbol repair (JP, 2026-11-26)
_NUMCH = r'[\d\s.,%\u00b1+\-\u2212\u2013()\[\]/:=<>\u2265\u2264\u00d7]'
_NUMLIKE = re.compile(r'^' + _NUMCH + r'*(?:\bto\b' + _NUMCH + r'*)*$')   # an otherwise numeric cell: digits, signs, brackets, percent, 'to'
_SUPCH = '\u00b9\u00b2\u00b3\u2070\u2074\u2075\u2076\u2077\u2078\u2079\u207a\u207b'
_SUPMAP = str.maketrans(_SUPCH, '1230456789+-')


def repair_cell_text_notes(text):
    """Repair symbol problems that some publisher fonts leave in the text layer (table-parser test, 124 table pages; table-parsers/RESULTS.md). Returns (repaired text, notes); notes may hold
    'footnotes' (footnote letters removed), 'superscripts' (superscript footnote markers removed) and 'unreadable' (True when unreadable script was marked). Rules:
    1 en dash stored as the letter e between digits (0.37e0.44, 62%e66%) -> en dash; a whole-cell scientific number (1e-5) is left alone.
    2 control character U+0004 for the minus sign -> U+2212; U+0003 for the times sign -> x; thorn (U+00FE) for plus -> +; quarter sign (U+00BC) for equals -> =; private-use digits
      U+F130..U+F139 -> 0..9; soft hyphen removed; ff, fi, fl, ffi, ffl ligature code points expanded.
    3 a lone 5 standing for equals in 'A x B 5 C' when A times B equals C -> =.
    4 Khmer-script characters (OCR noise) -> '[unreadable]'; nothing is guessed.
    5 a vertical bar standing for a tilde before a number ('(|24k)') -> '~'; a bar before letters is left alone.
    6 power of ten with a superscript exponent ('x10' plus a superscript 2) -> 'x10^2'; a flattened negative power ('10' U+2212 '3', a token with no letters in the cell) -> '10^' U+2212 '3'.
    7 footnote markers glued to numbers: a letter a to d or a Unicode superscript digit or sign after a number, only when the whole cell is otherwise numeric and the number is a bracket,
      percent, interval or fraction (a to d) or a decimal (a to c). The marker is removed and returned in notes. Units and words are never touched ('3d', '2b', 'ChatGPT4o', 'cm2' stay)."""
    t = text; notes = {}
    if not re.match(r'^\s*[-+]?\d+(\.\d+)?e[-+]?\d+\s*$', t): t = re.sub(r'(?<=[\d%)\]])e(?=[\d.])', '\u2013', t)
    for ch, rep in (('\x04', '\u2212'), ('\x03', ' \u00d7 '), ('\u00fe', '+'), ('\u00bc', '='), ('\u00ad', '')): t = t.replace(ch, rep)
    t = re.sub('[\uf130-\uf139]', lambda m: str(ord(m.group()) - 0xf130), t)
    for lig, rep in (('\ufb00', 'ff'), ('\ufb01', 'fi'), ('\ufb02', 'fl'), ('\ufb03', 'ffi'), ('\ufb04', 'ffl')): t = t.replace(lig, rep)
    m = re.search(r'(\d+)\D*\u00d7\s*(\d+)\D+?\s(5)\s(?:up to\s)?(\d+)', t)
    if m and int(m.group(1)) * int(m.group(2)) == int(m.group(4)): t = t[:m.start(3)] + '=' + t[m.end(3):]
    if re.search('[\u1780-\u17ff]', t): notes['unreadable'] = True; t = re.sub(r'[\u1780-\u17ff]+(?:\s+[\u1780-\u17ff]+)*', '[unreadable]', t)
    t = re.sub(r'(?<=[\s(])\|\s?(?=\d)', '~', t)
    t = re.sub(r'(\u00d7\s?10|(?<![\w.,])10)([' + _SUPCH + r']+)(?![\w])', lambda m: m.group(1) + '^' + m.group(2).translate(_SUPMAP), t)
    if not re.search('[A-Za-z]', t): t = re.sub(r'(?<![\w.,\^])10\u2212(\d{1,2})(?![\d\w])', '10^\u2212\\1', t)
    out = []
    for tok in t.split(' '):
        m = re.match(r'^(.*[\d)%\]])([a-d\u00aa]|[' + _SUPCH + r'])$', tok)
        if m and _NUMLIKE.match(m.group(1)) and (re.search(r'[)%\u00b1/]', m.group(1)) and m.group(2) not in 'e' or (re.search(r'\d\.\d', m.group(1)) and m.group(2) in 'abc\u00aa' + _SUPCH)): out.append((m.group(1), m.group(2)))
        else: out.append((tok, ''))
    stripped = ' '.join(a for a, _ in out)
    if any(b for _, b in out) and _NUMLIKE.match(stripped.replace('^', '')):
        fn = [('a' if b == '\u00aa' else b) for _, b in out if b and b not in _SUPCH]; sp = [b.translate(_SUPMAP) for _, b in out if b and b in _SUPCH]
        if fn: notes['footnotes'] = fn
        if sp: notes['superscripts'] = sp
        t = stripped
    return (re.sub(r'\s{2,}', ' ', t).strip() if t != text else t), notes


def repair_cell_text(text):
    """Cell text with the symbol repairs of repair_cell_text_notes applied; returns only the text."""
    return repair_cell_text_notes(text)[0]


def table_cells(page):
    """Tables of one page as lists of rows of repaired cell strings, from PyMuPDF find_tables() (no model, no network). PyMuPDF is the preferred reader (JP, 2026-11-26): on 463 verified table numbers it found 91.6% as read and 92.9% with the repair."""
    out = []; rot = page.rotation
    try:
        if rot: page.set_rotation(0)   # find_tables found no table on pages with a rotation set (0 of 463 values at 90 and 270 degrees); the content is upright in unrotated page space
        tabs = page.find_tables().tables
    except Exception: return out
    finally:
        if rot: page.set_rotation(rot)
    for tb in tabs:
        rows = [[repair_cell_text((c or '').replace('\n', ' ')) for c in row] for row in tb.extract()]
        if any(any(c for c in r) for r in rows): out.append(rows)
    return out

# ---------------------------------------------------------------- numbers in table cells and in table captions and footnotes (JP, 2026-11-27)
def _number_set(text):
    """Normalized numbers in a text: commas removed, leading zeros and trailing decimal zeros dropped (0.90 -> 0.9, 007 -> 7), plus-minus and percent signs ignored.
    A number with a minus sign is returned with and without the sign (the unsigned form lets '0-5' and 'p < -0.05' match 5 and 0.05); a hyphen between two numbers is not a sign."""
    out = set(); t = text.replace('−', '-').replace('±', ' ').replace('%', ' ')
    for m in re.finditer(r'(?<![A-Za-z0-9.])(-?)(\d[\d,]*(?:\.\d+)?|\.\d+)', t):
        s = m.group(2).replace(',', '')
        if '.' in s: a, b = s.split('.', 1); s = (a.lstrip('0') or '0') + ('.' + b.rstrip('0') if b.rstrip('0') else '')
        else: s = s.lstrip('0') or '0'
        out.add(s)
        if m.group(1) and s != '0': out.add('-' + s)
    return out

def caption_footnote_text(page):
    """Caption and footnote text that belongs to tables on one page, as a list of strings (no model, no network). A text block counts when it
    (1) starts with 'Table N' or 'Supplementary Table N' followed by a period or colon (a table caption; a body sentence such as 'Table 4 shows' is not),
    (2) starts with Note, Notes, Source, Sources or Abbreviations, or
    (3) lies directly below a table (find_tables box, gap of at most 40 points, overlapping it sideways) and starts with a footnote symbol (* dagger double-dagger section sign, a superscript digit)
        or a lowercase letter marker followed by a space ('a Rater 1 ...'), or is set in a smaller type size than the page body text (a footnote without a marker)."""
    blocks = [b for b in page.get_text('dict')['blocks'] if b['type'] == 0]
    sizes = sorted(s['size'] for b in blocks for l in b['lines'] for s in l['spans'] for _ in range(max(len(s['text'].strip()), 0)))
    body = sizes[len(sizes) // 2] if sizes else 10.0
    try: boxes = [fitz.Rect(t.bbox) for t in page.find_tables().tables]
    except Exception: boxes = []
    out = []
    for b in blocks:
        text = ' '.join(s['text'] for l in b['lines'] for s in l['spans']).strip()
        if not text: continue
        r = fitz.Rect(b['bbox']); n = max(sum(len(s['text']) for l in b['lines'] for s in l['spans']), 1)
        size = sum(s['size'] * len(s['text']) for l in b['lines'] for s in l['spans']) / n
        if re.match(r'(Supplementary\s+)?(Table|TABLE)\s+S?\d+\s*[.:]', text) or re.match(r'(Notes?|NOTES?|Source|Sources|Abbreviations?)\b', text): out.append(text); continue
        below = any(0 <= r.y0 - t.y1 <= 40 and r.x0 < t.x1 and r.x1 > t.x0 for t in boxes)
        if below and (re.match(r'[*†‡§¶¹²³⁰-⁹]', text) or re.match(r'[a-d]\s', text) or size <= body - 0.4): out.append(text)
    return out

def table_numbers(page):
    """Set of normalized numbers on one PDF page that a verifier may match a table value against (strings such as '0.9', '1000', '-0.05'; see _number_set).
    It is the union of (1) the numbers inside ANY cell of the tables PyMuPDF finds on the page (table_cells, cells repaired with repair_cell_text), including mixed text cells such as
    '$ 1.15 (0.65-1.98) ~2 mins' and label cells such as 'Top 5 sentences', and (2) the numbers in the captions and footnotes of tables on the page (caption_footnote_text).
    A match is therefore a hint that the value is on the page in a table or its caption, not proof that it sits in the right cell: a short number such as 5 or 9 can match by accident
    (the 5 in a header 'Recall@5'). Use a cell-level check (row and column label) when the cell matters."""
    out = set()
    for rows in table_cells(page):
        for row in rows:
            for c in row: out |= _number_set(c)
    for t in caption_footnote_text(page): out |= _number_set(repair_cell_text(t))
    return out

# ---------------------------------------------------------------- Word tables (JP, 2026-11-27)
def docx_tables(path):
    """Tables of a .docx file as a list of tables, each a list of rows of repaired cell strings (python-docx, no network, no model).
    Merged cells: a cell spanning several columns (gridSpan) or rows (vMerge) repeats its text in every grid position it covers, so every row has the same number of columns.
    Nested tables and tables inside text boxes are returned as extra tables after the table that holds them (the outer cell keeps the text of the nested table, joined with spaces).
    Not read: tables in headers, footers, footnotes and comments; text inside pictures. Old .doc files must first be saved as .docx (Word, or LibreOffice / macOS textutil when installed).
    Cell text: the text runs of all paragraphs of the cell, tabs and line breaks as spaces, whitespace collapsed; then repair_cell_text."""
    import docx
    from docx.oxml.ns import qn
    d = docx.Document(path); found = []
    def cell_text(tc):
        parts = []
        for p in tc.iter(qn('w:p')):
            parts.append(''.join((' ' if e.tag in (qn('w:tab'), qn('w:br')) else (e.text or '')) for e in p.iter() if e.tag in (qn('w:t'), qn('w:tab'), qn('w:br'))))
        return repair_cell_text(' '.join(' '.join(parts).split()))
    def read(tbl):
        grid = {}; r = 0
        for tr in tbl.findall(qn('w:tr')):
            c = 0
            for tc in tr.findall(qn('w:tc')):
                pr = tc.find(qn('w:tcPr')); span = 1; vm = None
                if pr is not None:
                    gs = pr.find(qn('w:gridSpan')); span = int(gs.get(qn('w:val'))) if gs is not None else 1
                    v = pr.find(qn('w:vMerge')); vm = None if v is None else (v.get(qn('w:val')) or 'continue')
                while (r, c) in grid: c += 1
                txt = grid[(r - 1, c)] if vm == 'continue' and (r - 1, c) in grid else cell_text(tc)
                for k in range(span): grid[(r, c + k)] = txt
                c += span
            r += 1
        if not grid: return []
        R = max(k[0] for k in grid) + 1; C = max(k[1] for k in grid) + 1
        return [[grid.get((i, j), '') for j in range(C)] for i in range(R)]
    seen = set()
    for tbl in d.element.body.iter(qn('w:tbl')):   # document order: outer table first, then nested tables and text-box tables
        if id(tbl) in seen: continue
        seen.add(id(tbl)); rows = read(tbl)
        if rows: found.append(rows)
    return found

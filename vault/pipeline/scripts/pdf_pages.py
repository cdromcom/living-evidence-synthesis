#!/usr/bin/env python3
"""PDF backbone for the Skill (v2): page map, quote locator, verbatim check, quote crop, link extraction. Needs PyMuPDF.

  python3 pdf_pages.py map  <pdf>                 printed page label for every PDF page
  python3 pdf_pages.py find <pdf> "quote text"    where the quote appears (PDF page, printed page)
  python3 pdf_pages.py crop <pdf> "quote" out.png [--dpi 250]   highlighted crop of the quote region
  python3 pdf_pages.py links <pdf>                hyperlinks embedded in the PDF (code and data URLs)

Printed page = the number printed on the page (the journal page), NOT the position in the PDF file. If the file prints no page
numbers (preprints), the map falls back to the PDF position and marks it source='pdf-position'; record that in the locator."""
import os, re, sys, unicodedata
from pathlib import Path
import fitz  # PyMuPDF
fitz.TOOLS.mupdf_display_errors(False)   # silence harmless MuPDF colour-space warnings

VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
PDF_DIR = VAULT / 'sysrev' / 'dgraph' / 'source' / 'pdfs'
_FIX = {'−': '-', '‐': '-', '‑': '-', '‒': '-', '–': '-', '—': '-', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}


_SUP_SUB = dict.fromkeys(map(ord, '\u00b9\u00b2\u00b3\u2070\u2074\u2075\u2076\u2077\u2078\u2079\u207a\u207b\u207c\u207d\u207e\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089\u208a\u208b\u208c\u208d\u208e\u2020\u2021'), None)


def norm(s: str) -> str:
    """Letters and digits only, lower case, so punctuation never decides a match: dashes, curly quotes, hyphenated line breaks, ligatures, footnote
    superscripts and subscripts are ignored. The one exception is the decimal point between digits (0.79 must not match 079): it becomes 'dot'."""
    s = re.sub(r'-\s*\n\s*', '', s)
    s = ''.join(_FIX.get(c, c) for c in s).translate(_SUP_SUB)   # superscript and subscript marks (footnote numbers, daggers) are dropped, not turned into digits
    s = unicodedata.normalize('NFKD', s)
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


def crop_quote(doc, quote: str, out: str, dpi: int = 250, pad: float = 14) -> dict:
    hit = find_quote(doc, quote)
    if not hit['pages']: return {'ok': False, 'reason': 'quote not found'}
    page = doc[hit['pages'][0] - 1]
    rects = locate_rects(page, quote.split('...')[0].split('…')[0])
    if not rects: return {'ok': False, 'reason': 'found in text but no word coordinates (scanned or odd encoding)'}
    box = fitz.Rect(rects[0])
    for r in rects[1:]: box |= r
    for r in rects: page.add_highlight_annot(r)
    clip = fitz.Rect(page.rect.x0, max(page.rect.y0, box.y0 - pad), page.rect.x1, min(page.rect.y1, box.y1 + pad))
    page.get_pixmap(dpi=dpi, clip=clip).save(out)
    return {'ok': True, 'pdf_page': hit['pages'][0], 'out': out, 'size_px': Path(out).stat().st_size}


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
        print(crop_quote(doc, sys.argv[3], sys.argv[4], int(sys.argv[sys.argv.index('--dpi') + 1]) if '--dpi' in sys.argv else 250))
    elif cmd == 'links':
        for l in links(doc): print(l['pdf_page'], l['uri'])

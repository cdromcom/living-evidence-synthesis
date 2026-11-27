"""Derotation step for MinerU (and any reader that does not turn pages itself).

derotate_page(page) -> (upright_page, info)
  page   a pymupdf.Page
  returns a copy of the page in a new in-memory document (keep a reference to upright_page.parent) whose text lines run left to right, plus info:
  {'method': 'text-direction' | 'no-text-layer', 'angle_deg': text angle found, 'old_rotation': ..., 'new_rotation': ..., 'chars': ...}.
Decision rule (text layer present):
  1. For every text line take its direction vector page.get_text('dict') line['dir'] (in unrotated page space, y down); angle = atan2(dy, dx) rounded to a multiple of 90 degrees.
  2. The angle that holds the most characters wins (needs at least 20 characters; otherwise the page has no usable text layer and is returned unchanged with method 'no-text-layer').
  3. The copy gets rotation 0 and its content is turned by -angle: nothing to do for angle 0 (a page that only carried a /Rotate value is simply reset to 0); for 90, 180 and 270 the page is placed
     on a new page of swapped size with show_pdf_page(rotate=angle) so that the text layer is kept and no /Rotate value is left (MinerU reads /Rotate pages badly: 367 of 463 values on a /Rotate copy). Upside-down text (180) is turned over too.
For pages without a text layer use choose_orientation(page, score) below.
"""
import math, collections, pymupdf

def text_angle(page):
    c = collections.Counter()
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            n = sum(len(s['text'].strip()) for s in l['spans'])
            if n: c[int(round(math.degrees(math.atan2(l['dir'][1], l['dir'][0])) / 90.0) * 90) % 360] += n
    return (c.most_common(1)[0][0], sum(c.values())) if c else (None, 0)

def _copy(page):
    d = pymupdf.open(); d.insert_pdf(page.parent, from_page=page.number, to_page=page.number); return d[0]

def derotate_page(page, min_chars=20):
    ang, n = text_angle(page); old = page.rotation
    if ang is None or n < min_chars: return _copy(page), {'method': 'no-text-layer', 'angle_deg': None, 'old_rotation': old, 'new_rotation': old, 'chars': n, 'flattened': False}
    src = _copy(page); src.set_rotation(0)   # content only; the old /Rotate value is dropped
    if ang == 0:
        return src, {'method': 'text-direction', 'angle_deg': 0, 'old_rotation': old, 'new_rotation': 0, 'chars': n, 'flattened': False}
    # content itself is turned: place it on a new page with rotation 0 (readers such as MinerU read a /Rotate page badly), keeping the text layer
    w, h = src.rect.width, src.rect.height; swap = ang in (90, 270)
    d = pymupdf.open(); out = d.new_page(width=(h if swap else w), height=(w if swap else h))
    out.show_pdf_page(out.rect, src.parent, src.number, rotate=ang)
    return out, {'method': 'text-direction', 'angle_deg': ang, 'old_rotation': old, 'new_rotation': 0, 'chars': n, 'flattened': True}

def choose_orientation(page, score):
    """Pages without a text layer: try the four orientations and keep the one with the highest score(copy_of_page) (for example the number of numeric table cells a reader returns).
    Ties go to the orientation the page already has. Returns (best_copy, rotation_applied, scores)."""
    best, scores = None, {}
    for add in (0, 90, 180, 270):
        c = _copy(page); c.set_rotation((c.rotation + add) % 360); scores[add] = score(c)
        if best is None or scores[add] > scores[best[1]]: best = (c, add)
    return best[0], best[1], scores

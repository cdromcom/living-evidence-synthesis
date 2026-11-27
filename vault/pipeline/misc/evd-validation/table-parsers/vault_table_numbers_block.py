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

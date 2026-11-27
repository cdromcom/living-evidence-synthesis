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

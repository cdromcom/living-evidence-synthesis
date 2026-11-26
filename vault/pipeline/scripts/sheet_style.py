#!/usr/bin/env python3
"""One place for how every LIVES spreadsheet looks (JP, 2026-11-26): Butterick's Practical Typography for the text, Stephen Few's Show Me the Numbers (chapter 8, tables) for the table.

What it does to a sheet that already has its header row and data rows:
- Fonts (JP, 2026-11-26): Spectral 11 bold for column names and ABOUT headings, Google Sans 11 for the data (default text size 11, JP 2026-11-26) (neither is a default font). No italics, underlines or capitals for emphasis.
- Table: gridlines off, no fills except a faint grey zebra stripe and the yellow JP input columns; one dark rule under the header, nothing else.
- Alignment: numbers and brief words or phrases are centered; longer text is left aligned and wraps. Each header is aligned like its data, so titles line up with what is under them.
- Width: every column is sized to its data (not one width for all); wrapped text columns stop at a comfortable line length (about 45 to 75 characters).
- Numbers: one number format per column (same decimals down the column; dollars with a dollar sign; shares as percents when the header says so).
- Padding: left aligned text gets a one-step indent so it does not touch the cell edge; the header row is a little taller.
Cells that already carry a fill (for example the light green "screen this" rows) keep it, and image columns keep the width their pictures need.
Use polish(ws, ...) after the rows are in; for sheets that already exist in Google Sheets, sheets_requests(...) returns the same look as batchUpdate requests so labels are not touched."""
import re
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

FONT_HEAD = 'Spectral'; FONT = FONT_BODY = 'Google Sans'; SIZE = 11   # Spectral (a serif) for column names and headings, Google Sans for the data (JP, 2026-11-26)
INK = '222222'; RULE = '222222'; STRIPE = 'F4F4F4'; JP_FILL = 'FFF6D6'
NUM = re.compile(r'^[-+]?\$?\d[\d,]*(\.\d+)?%?$')
BRIEF = 22          # at most this many characters: brief word or phrase, centered
TEXT_MIN, TEXT_MAX = 28, 72


def kind_of(values):
    """'number', 'brief' or 'text' from the data in a column."""
    vals = [v for v in values if v not in (None, '')]
    if not vals: return 'brief'
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) or (isinstance(v, str) and NUM.match(v.strip())) for v in vals): return 'number'
    if max(len(str(v)) for v in vals) <= BRIEF: return 'brief'
    return 'text'


def decimals(values):
    d = 0
    for v in values:
        if isinstance(v, float): d = max(d, min(len(repr(round(v, 4)).split('.')[-1].rstrip('0')), 3))
    return d


def width_for(kind, header, values):
    lens = sorted(len(str(v)) for v in values if v not in (None, ''))
    longest_word = max((len(w) for w in str(header).split()), default=4)
    if kind == 'text':
        if lens and lens[-1] <= 60: return max(TEXT_MIN, lens[-1] + 2, longest_word + 3)   # fits on one line: no mid-word wrapping
        p90 = lens[int(0.9 * (len(lens) - 1))] if lens else 10
        return max(TEXT_MIN, min(TEXT_MAX, round(p90 * 0.9) + 2, TEXT_MAX), longest_word + 3)
    top = lens[-1] if lens else 4
    return max(8, min(30, max(top, longest_word) + 3))


def polish(ws, header_row=1, jp_from=None, image_cols=(), keep_widths=(), header_height=30, max_lines=8):
    """Apply the house style. jp_from: first column (1-based) of JP's input columns. image_cols: columns holding pictures (width and height are left to the picture code). keep_widths: columns whose width is left alone."""
    ws.sheet_view.showGridLines = False
    body = Font(name=FONT_BODY, size=SIZE, color=INK); bold = Font(name=FONT_HEAD, size=SIZE, color=INK, bold=True)
    top, bottom = header_row + 1, ws.max_row; ncol = ws.max_column
    thin = Side(style='medium', color=RULE); stripe = PatternFill('solid', fgColor=STRIPE); jpf = PatternFill('solid', fgColor=JP_FILL)
    for col in range(1, ncol + 1):
        letter = get_column_letter(col); head = ws.cell(header_row, col).value; vals = [ws.cell(r, col).value for r in range(top, bottom + 1)]
        is_img = col in image_cols; kind = 'brief' if is_img else kind_of(vals); is_jp = bool(jp_from and col >= jp_from)
        if is_jp and kind == 'number': kind = 'brief'
        h = 'center' if kind in ('number', 'brief') else 'left'; indent = 1 if h == 'left' else 0
        if col not in image_cols and col not in keep_widths: ws.column_dimensions[letter].width = round(width_for(kind, head, vals) * 1.1)   # 11 pt text is wider than 10 pt
        fmt = None
        if kind == 'number' and not is_jp:
            d = decimals([v for v in vals if isinstance(v, (int, float))]); hs = str(head or '').lower()
            fmt = ('$#,##0.00' if re.search(r'usd|cost|\$', hs) else '0%' if (re.search(r'share|rate|percent', hs) and vals and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in vals if v not in (None, ''))) else ('0.' + '0' * d if d else '0'))
        hc = ws.cell(header_row, col); hc.font = bold; hc.alignment = Alignment(horizontal=h, vertical='bottom', wrap_text=True, indent=indent); hc.border = Border(bottom=thin)
        hc.fill = jpf if is_jp else PatternFill(fill_type=None)
        for r in range(top, bottom + 1):
            c = ws.cell(r, col); c.font = (Font(name=FONT, size=SIZE, color='888888', strike=True) if (c.font and c.font.strike) else body)   # struck-through rows (duplicates) keep their strike
            c.alignment = Alignment(horizontal=h, vertical='top', wrap_text=(kind == 'text' or kind == 'brief' and not is_img), indent=indent)
            if fmt and isinstance(c.value, (int, float)): c.number_format = fmt
            if c.fill is None or c.fill.fill_type is None:
                if is_jp: c.fill = jpf
                elif (r - top) % 2 == 1: c.fill = stripe
    ws.row_dimensions[header_row].height = header_height
    # row heights: Google Sheets does not grow imported rows to fit wrapped text, so estimate them (about 15 points per line at 11 pt), at most max_lines lines
    import math
    widths = {c: (ws.column_dimensions[get_column_letter(c)].width or 10) for c in range(1, ncol + 1)}
    for r in range(top, bottom + 1):
        if ws.row_dimensions[r].height: continue
        lines = 1
        for c in range(1, ncol + 1):
            v = ws.cell(r, c).value
            if c in image_cols or not isinstance(v, str) or not ws.cell(r, c).alignment.wrap_text: continue
            lines = max(lines, sum(max(1, math.ceil(len(par) / max(widths[c] * 0.95, 5))) for par in v.split('\n')))
        if lines > 1: ws.row_dimensions[r].height = min(lines, max_lines) * 15 + 6
    return ws


def polish_about(ws, key_width=26, text_width=90):
    """ABOUT tabs: a bold key column and one readable text column (line length of about 85 characters)."""
    ws.sheet_view.showGridLines = False
    for row in ws.iter_rows():
        for c in row:
            if c.value is None: continue
            first = c.column == 1
            c.font = Font(name=FONT_HEAD if first else FONT_BODY, size=SIZE, color=INK, bold=first); c.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True, indent=1)
    ws.column_dimensions['A'].width = key_width; ws.column_dimensions['B'].width = text_width
    if ws.max_column >= 3: ws.column_dimensions['C'].width = 40
    import math
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 2).value
        if isinstance(v, str): ws.row_dimensions[r].height = max(1, sum(max(1, math.ceil(len(par) / (text_width * 0.95))) for par in v.split('\n'))) * 15 + 6
    if str(ws.cell(1, 1).value or '') in ('Item',):   # a header row (the screening ABOUT tabs have one): headings style, no fill
        for c in ws[1]: c.font = Font(name=FONT_HEAD, size=SIZE, color=INK, bold=True); c.fill = PatternFill(fill_type=None); c.alignment = Alignment(horizontal='left', vertical='bottom', indent=1); c.border = Border(bottom=Side(style='medium', color=RULE))


def layout_of(ws, header_row=1):
    """Per column: (kind, width in characters, is JP input column) for a worksheet that holds the data, so an existing Google Sheet can be styled to match without being rebuilt."""
    jp_from = next((i + 1 for i, c in enumerate(ws[header_row]) if str(c.value or '').startswith('JP')), None); out = []
    for col in range(1, ws.max_column + 1):
        vals = [ws.cell(r, col).value for r in range(header_row + 1, min(ws.max_row, 3000) + 1)]; head = ws.cell(header_row, col).value; k = kind_of(vals)
        if jp_from and col >= jp_from and k == 'number': k = 'brief'
        out.append((k, width_for(k, head, vals), bool(jp_from and col >= jp_from)))
    return out


def sheets_requests(sheet_id, n_rows, layout, header_rows=1, zebra=True):
    """Google Sheets batchUpdate requests with the same look, for a sheet that already exists (labels and values are untouched). layout: from layout_of()."""
    def rgb(h): return {'red': int(h[0:2], 16) / 255, 'green': int(h[2:4], 16) / 255, 'blue': int(h[4:6], 16) / 255}
    n_cols = len(layout); rng = lambda r0, r1, c0, c1: {'sheetId': sheet_id, 'startRowIndex': r0, 'endRowIndex': r1, 'startColumnIndex': c0, 'endColumnIndex': c1}
    reqs = [{'repeatCell': {'range': rng(0, n_rows, 0, n_cols), 'cell': {'userEnteredFormat': {'textFormat': {'fontFamily': FONT, 'fontSize': SIZE, 'foregroundColor': rgb(INK), 'bold': False, 'italic': False}, 'verticalAlignment': 'TOP'}}, 'fields': 'userEnteredFormat(textFormat,verticalAlignment)'}},
            {'updateSheetProperties': {'properties': {'sheetId': sheet_id, 'gridProperties': {'hideGridlines': True}}, 'fields': 'gridProperties.hideGridlines'}},
            {'repeatCell': {'range': rng(0, header_rows, 0, n_cols), 'cell': {'userEnteredFormat': {'textFormat': {'bold': True, 'fontFamily': FONT_HEAD, 'fontSize': SIZE, 'foregroundColor': rgb(INK)}, 'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'wrapStrategy': 'WRAP', 'verticalAlignment': 'BOTTOM'}}, 'fields': 'userEnteredFormat(textFormat,backgroundColor,wrapStrategy,verticalAlignment)'}},
            {'updateBorders': {'range': rng(header_rows - 1, header_rows, 0, n_cols), 'bottom': {'style': 'SOLID_MEDIUM', 'color': rgb(RULE)}}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': header_rows}, 'properties': {'pixelSize': 44}, 'fields': 'pixelSize'}}]
    for col, (k, w, jp) in enumerate(layout):
        h = 'CENTER' if k in ('number', 'brief') else 'LEFT'; fmt = {'horizontalAlignment': h, 'wrapStrategy': 'WRAP' if k != 'number' else 'OVERFLOW_CELL'}; fields = 'userEnteredFormat(horizontalAlignment,wrapStrategy' + (',padding' if h == 'LEFT' else '')
        if h == 'LEFT': fmt['padding'] = {'left': 6}
        reqs.append({'repeatCell': {'range': rng(0, n_rows, col, col + 1), 'cell': {'userEnteredFormat': fmt}, 'fields': fields + ')'}})
        reqs.append({'repeatCell': {'range': rng(0, header_rows, col, col + 1), 'cell': {'userEnteredFormat': {'horizontalAlignment': h, 'wrapStrategy': 'WRAP'}}, 'fields': 'userEnteredFormat(horizontalAlignment,wrapStrategy)'}})
        if jp: reqs.append({'repeatCell': {'range': rng(0, n_rows, col, col + 1), 'cell': {'userEnteredFormat': {'backgroundColor': rgb(JP_FILL)}}, 'fields': 'userEnteredFormat.backgroundColor'}})
        reqs.append({'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col + 1}, 'properties': {'pixelSize': int(w * 8 + 10)}, 'fields': 'pixelSize'}})
    if zebra: reqs.append({'addConditionalFormatRule': {'rule': {'ranges': [rng(header_rows, n_rows, 0, n_cols)], 'booleanRule': {'condition': {'type': 'CUSTOM_FORMULA', 'values': [{'userEnteredValue': '=ISEVEN(ROW())'}]}, 'format': {'backgroundColor': rgb(STRIPE)}}}, 'index': 0}})
    return reqs

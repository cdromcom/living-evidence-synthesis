"""Shared parsing of the TRIPOD-LLM and Quality appraisal tables on source pages (used by the audit, the sheet builder and the model checker)."""
import os, re
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
SRC_DIR = VAULT / 'sysrev' / 'dgraph' / 'source'
ICON = {'🟢': 'Addressed', '🟡': 'Partly addressed', '🔴': 'Not addressed', '✅': 'Addressed', '🟠': 'Partly addressed', '❌': 'Not addressed',
        '●': 'Addressed', '◐': 'Partly addressed', '○': 'Not addressed', '➖': 'Not applicable', '': 'Not applicable'}
QRE = re.compile(r'\*["“](.+?)["”]\*\s*(?:`([^`]*)`)?', re.S)


def section(text: str, heading: str) -> str:
    m = re.search(r'^## ' + re.escape(heading) + r'.*?\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1) if m else ''


def parse_table(block: str, kind: str, citekey: str):
    """Rows of one table as dicts: kind, citekey, row, item, rating_icon, rating, quote, locator, page, comment, raw."""
    rows = []
    for line in block.splitlines():
        if not line.startswith('|') or re.match(r'^\|\s*-', line) or re.match(r'^\|\s*(#|Domain)\s*\|', line): continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        if kind == 'TRIPOD' and len(cells) >= 4: rid, item, icon, cell = re.sub(r'[*]', '', cells[0]), cells[1], cells[2], '|'.join(cells[3:])
        elif kind == 'QUALITY' and len(cells) >= 3: rid, item, icon, cell = re.sub(r'\*\*(.+?)\*\*.*', r'\1', cells[0]), cells[0], cells[1], '|'.join(cells[2:])
        else: continue
        qs = QRE.findall(cell)
        quote = ' ... '.join(q[0].strip() for q in qs); loc = '; '.join(q[1].strip() for q in qs if q[1].strip())
        pages = re.findall(r'\bpp?\.\s*(\d+)', loc)
        rows.append({'kind': kind, 'citekey': citekey, 'row': rid, 'item': item[:160], 'rating_icon': icon, 'rating': ICON.get(icon, icon),
                     'quote': quote, 'locator': loc, 'page': pages[0] if pages else '', 'comment': QRE.sub('', cell).strip()[:300], 'raw': line})
    return rows


def source_rows(path: Path):
    t = path.read_text(encoding='utf-8'); ck = path.stem
    return parse_table(section(t, 'Quality appraisal'), 'QUALITY', ck) + parse_table(section(t, 'TRIPOD-LLM reporting'), 'TRIPOD', ck)

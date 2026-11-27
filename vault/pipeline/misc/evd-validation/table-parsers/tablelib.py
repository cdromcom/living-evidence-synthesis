"""Shared helpers: HTML table to grid, number normalisation."""
import re
from html.parser import HTMLParser

class _T(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.cur=None; s.row=None; s.cell=None; s.depth=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='table':
            s.depth+=1
            if s.depth==1: s.cur=[]
        elif t=='tr' and s.cur is not None: s.row=[]
        elif t in('td','th') and s.row is not None:
            s.cell=[]; s.span=(int(a.get('colspan',1) or 1), int(a.get('rowspan',1) or 1))
        elif t=='br' and s.cell is not None: s.cell.append(' ')
    def handle_endtag(s,t):
        if t in('td','th') and s.cell is not None:
            s.row.append((re.sub(r'\s+',' ',''.join(s.cell)).strip(),)+s.span); s.cell=None
        elif t=='tr' and s.row is not None:
            s.cur.append(s.row); s.row=None
        elif t=='table':
            s.depth-=1
            if s.depth==0 and s.cur is not None: s.tables.append(s.cur); s.cur=None
    def handle_data(s,d):
        if s.cell is not None: s.cell.append(d)

def html_to_grids(html, expand=True):
    """Return list of tables; each table = list of rows of strings (spans expanded by repeating the text)."""
    p=_T(); p.feed(html); out=[]
    for t in p.tables:
        grid={}; 
        for r,row in enumerate(t):
            c=0
            for (txt,cs,rs) in row:
                while (r,c) in grid: c+=1
                for dr in range(rs):
                    for dc in range(cs):
                        grid[(r+dr,c+dc)]=txt if expand else (txt if (dr==0 and dc==0) else '')
                c+=cs
        if not grid: out.append([]); continue
        R=max(k[0] for k in grid)+1; C=max(k[1] for k in grid)+1
        out.append([[grid.get((r,c),'') for c in range(C)] for r in range(R)])
    return out

NUM=re.compile(r'(?<![A-Za-z0-9])[-+]?\d[\d,]*(?:\.\d+)?|(?<![A-Za-z0-9])[-+]?\.\d+')
def norm_num(tok):
    t=tok.replace('−','-').replace(',','').strip()
    t=t.lstrip('+')
    neg=t.startswith('-'); t=t.lstrip('-')
    if '.' in t:
        a,b=t.split('.',1); a=a.lstrip('0') or '0'; b=b.rstrip('0'); t=a+('.'+b if b else '')
    else: t=t.lstrip('0') or '0'
    return ('-' if neg and t!='0' else '')+t
def numbers_in(text):
    text=text.replace('−','-').replace('±',' ').replace('%',' ')
    return [norm_num(m) for m in NUM.findall(text)]
def cell_numbers(cell):
    return numbers_in(cell)


# ---------------------------------------------------------------- symbol repair for text-layer problems
# (same code as repair_cell_text in pipeline/scripts/pdf_pages.py; tablelib_tests.py checks that the two blocks are identical)
#BEGIN_REPAIR
REPAIR_COUNTS = {}   # rule name -> number of cells it changed (callers may clear it)
def _count(k): REPAIR_COUNTS[k] = REPAIR_COUNTS.get(k, 0) + 1
_SCI = re.compile(r'^\s*[-+]?\d+(\.\d+)?e[-+]?\d+\s*$')
_NUMCH = r'[\d\s.,%±+\-−–()\[\]/:=<>≥≤×]'
_NUMLIKE = re.compile(r'^' + _NUMCH + r'*(?:\bto\b' + _NUMCH + r'*)*$')   # an "otherwise numeric" cell: digits, signs, brackets, percent, 'to'
_SUPCH = '¹²³⁰⁴⁵⁶⁷⁸⁹⁺⁻'
_SUPMAP = str.maketrans(_SUPCH, '1230456789+-')

def repair_cell_text_notes(text):
    """Repair symbol problems that some publisher fonts leave in the text layer (found in the table-parser test, 124 table pages; table-parsers/RESULTS.md). Returns (repaired text, notes);
    notes is a dict that may hold 'footnotes' (footnote letters removed), 'superscripts' (superscript footnote markers removed) and 'unreadable' (True when unreadable script was marked).
    1 en dash stored as the letter e between digits (0.37e0.44, 62%e66%) -> en dash. A whole-cell scientific number (1e-5) is left alone.
    2 control character U+0004 for the minus sign -> U+2212; U+0003 for the times sign -> x; thorn (U+00FE) for plus -> +; quarter sign (U+00BC) for equals -> =;
      private-use digits U+F130..U+F139 -> 0..9; soft hyphen removed; ff, fi, fl, ffi, ffl ligature code points expanded.
    3 a lone 5 standing for equals in 'A x B 5 C' when A times B equals C -> =.
    4 Khmer-script characters (OCR noise, Marker) -> '[unreadable]' (nothing is guessed; digits next to it are kept); notes['unreadable'] = True.
    5 a vertical bar standing for a tilde before a number ('(|24k)', '| 1-2 mins') -> '~'. A bar before letters ('|diff|') is left alone.
    6 power of ten whose superscript minus was flattened ('10-3' written with U+2212, as a token with no letters in the cell) -> '10^-3'; a superscript exponent after a times sign or on a bare 10
      (x10 with superscript 2) -> 'x10^2'.
    7 footnote markers glued to numbers: a letter a-d (or U+00AA) or a Unicode superscript digit/sign after a number, only when the whole cell is otherwise numeric
      (digits, signs, brackets, percent, 'to') and the number is a bracket, percent, interval or fraction (a-d), or a decimal (a-c). The marker is removed and returned in notes.
      Units and words are never touched: '3d' (3 days), '2b', 'ChatGPT4o', 'cm2' and '37.5 d' stay as they are; '*', dagger, section and degree signs are kept.
    The repair is for text-layer readers (PyMuPDF, Marker); it is also safe on OCR output."""
    t = text; notes = {}
    if not _SCI.match(t):
        n = re.subn(r'(?<=[\d%)\]])e(?=[\d.])', '–', t)
        if n[1]: _count('e_for_en_dash'); t = n[0]
    for ch, rep, k in (('\x04', '−', 'x04_for_minus'), ('\x03', ' × ', 'x03_for_times'), ('þ', '+', 'thorn_for_plus'), ('¼', '=', 'quarter_for_equals'), ('­', '', 'soft_hyphen')):
        if ch in t: _count(k); t = t.replace(ch, rep)
    if re.search('[-]', t): _count('private_use_digits'); t = re.sub('[-]', lambda m: str(ord(m.group()) - 0xf130), t)
    for lig, rep in (('ﬀ', 'ff'), ('ﬁ', 'fi'), ('ﬂ', 'fl'), ('ﬃ', 'ffi'), ('ﬄ', 'ffl')):
        if lig in t: _count('ligature'); t = t.replace(lig, rep)
    m = re.search(r'(\d+)\D*×\s*(\d+)\D+?\s(5)\s(?:up to\s)?(\d+)', t)
    if m and int(m.group(1)) * int(m.group(2)) == int(m.group(4)): _count('five_for_equals'); t = t[:m.start(3)] + '=' + t[m.end(3):]
    if re.search('[ក-៿]', t):
        _count('unreadable_script'); notes['unreadable'] = True; t = re.sub(r'[ក-៿]+(?:\s+[ក-៿]+)*', '[unreadable]', t)
    n = re.subn(r'(?<=[\s(])\|\s?(?=\d)', '~', t)
    if n[1]: _count('bar_for_tilde'); t = n[0]
    n = re.subn(r'(×\s?10|(?<![\w.,])10)([' + _SUPCH + r']+)(?![\w])', lambda m: m.group(1) + '^' + m.group(2).translate(_SUPMAP), t)
    if n[1]: _count('superscript_exponent'); t = n[0]
    if not re.search('[A-Za-z]', t):
        n = re.subn(r'(?<![\w.,\^])10−(\d{1,2})(?![\d\w])', '10^−\\1', t)
        if n[1]: _count('flattened_power_of_ten'); t = n[0]
    fn, sp = [], []; out = []
    for tok in t.split(' '):
        m = re.match(r'^(.*[\d)%\]])([a-dª]|[' + _SUPCH + r'])$', tok)
        if m and _NUMLIKE.match(m.group(1)) and (re.search(r'[)%±/]', m.group(1)) and m.group(2) not in 'e' or (re.search(r'\d\.\d', m.group(1)) and m.group(2) in 'abcª' + _SUPCH)):
            out.append((m.group(1), m.group(2)))
        else: out.append((tok, ''))
    stripped = ' '.join(a for a, _ in out)
    if any(b for _, b in out) and _NUMLIKE.match(stripped.replace('^', '')):
        for _, b in out:
            if b: (sp if b in _SUPCH else fn).append(b.translate(_SUPMAP) if b in _SUPCH else ('a' if b == 'ª' else b))
        if fn: _count('footnote_letter'); notes['footnotes'] = fn
        if sp: _count('superscript_footnote'); notes['superscripts'] = sp
        t = stripped
    return (re.sub(r'\s{2,}', ' ', t).strip() if t != text else t), notes

def repair_cell_text(text):
    """Cell text with the symbol repairs of repair_cell_text_notes applied (see its doc comment); returns only the text."""
    return repair_cell_text_notes(text)[0]
#END_REPAIR

def repair_tables(tables): return [[[repair_cell_text(c) for c in row] for row in t] for t in tables]

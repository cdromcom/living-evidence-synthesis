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
REPAIR_COUNTS={}
def _count(k): REPAIR_COUNTS[k]=REPAIR_COUNTS.get(k,0)+1
_SCI=re.compile(r'^\s*[-+]?\d+(\.\d+)?e[-+]?\d+\s*$')
def repair_cell_text(text):
    """Repair symbol problems of some publisher fonts in a text-layer cell. Each rule is listed in REPAIR_COUNTS when it fires.
    1 en dash stored as the letter e between digits (0.37e0.44, 62%e66%)       -> en dash
    2 control character U+0004 used for the minus sign ((\x040.05 to 0.12))      -> minus sign U+2212
    3 control character U+0003 used for the multiplication sign                 -> x sign
    4 thorn (U+00FE) used for plus                                              -> +
    5 quarter sign (U+00BC) used for equals                                     -> =
    6 private-use digits U+F130..U+F139 (font maps digit d to U+F130+d)         -> 0..9
    7 soft hyphen U+00AD and ligature code points (ff, fi, fl, ffi, ffl)        -> removed / expanded
    8 a lone digit 5 standing for '=' in 'A x B 5 up to C' when A*B equals C    -> =
    Not repaired (only counted elsewhere): footnote letters glued to numbers (0.90 (0.88e0.93)a), unicode superscripts."""
    t=text
    if not _SCI.match(t):
        n=re.subn(r'(?<=[\d%)\]])e(?=[\d.])','\u2013',t)
        if n[1]: _count('e_for_en_dash'); t=n[0]
    for ch,rep,k in (('\x04','\u2212','x04_for_minus'),('\x03',' \u00d7 ','x03_for_times'),('\u00fe','+','thorn_for_plus'),('\u00bc','=','quarter_for_equals'),('\u00ad','','soft_hyphen')):
        if ch in t: _count(k); t=t.replace(ch,rep)
    if re.search('[\uf130-\uf139]',t):
        _count('private_use_digits'); t=re.sub('[\uf130-\uf139]',lambda m:str(ord(m.group())-0xf130),t)
    for lig,rep in (('\ufb00','ff'),('\ufb01','fi'),('\ufb02','fl'),('\ufb03','ffi'),('\ufb04','ffl')):
        if lig in t: _count('ligature'); t=t.replace(lig,rep)
    m=re.search(r'(\d+)\D*\u00d7\s*(\d+)\D+?\s(5)\s(?:up to\s)?(\d+)',t)
    if m and int(m.group(1))*int(m.group(2))==int(m.group(4)):
        _count('five_for_equals'); t=t[:m.start(3)]+'='+t[m.end(3):]
    t=re.sub(r'\s{2,}',' ',t).strip() if t!=text else t
    return t
def repair_tables(tables): return [[[repair_cell_text(c) for c in row] for row in t] for t in tables]

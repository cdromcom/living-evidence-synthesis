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
import os
def numbers_in(text):
    if os.environ.get('REPAIR_E_DASH'): text=re.sub(r'(?<=[\d%)])e(?=[\d.])',' ',text)   # some text layers encode an en dash between numbers as the letter e
    text=text.replace('−','-').replace('±',' ').replace('%',' ')
    return [norm_num(m) for m in NUM.findall(text)]
def cell_numbers(cell):
    return numbers_in(cell)

import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Evaluations A and B. Reads results/*, writes eval.json plus tsv files."""
import json, glob, os, re, sys, itertools, statistics, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tablelib import numbers_in, norm_num, repair_tables
import pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
PAGES=json.load(open('pages.json'))
PARS=['pymupdf','marker','mineru']

def load(root='results',repair=None):
    """repair: apply tablelib.repair_cell_text to pymupdf and marker output (default: env REPAIR=1)"""
    if repair is None: repair=os.environ.get('REPAIR')=='1'
    R={p:{} for p in PARS}   # R[parser][(citekey,page)] = {'tables':[...], 'seconds':..., 'error':...}
    for p in PARS:
        for f in glob.glob(f'{root}/{p}/*.json'):
            r=json.load(open(f))
            if repair and p in ('pymupdf','marker'): r['tables']=repair_tables(r['tables'])
            R[p][(r['citekey'],r['page'])]=r
    return R

def is_numeric_cell(c):
    c=c.strip()
    if not re.search(r'\d',c): return False
    rest=re.sub(r'[\d\s.,%±+\-−–()\[\]/:*†‡=<>]','',c)
    return len(rest)<=2
def numset(tables):
    s=collections.Counter()
    for t in tables:
        for row in t:
            for c in row:
                if is_numeric_cell(c): s.update(set(numbers_in(c)))
    return s
def numcells(tables): return sum(1 for t in tables for row in t for c in row if is_numeric_cell(c))
def allcells(tables): return sum(1 for t in tables for row in t for c in row if c.strip())

# ---------- A
def words(s): return [w for w in re.findall(r'[a-z0-9]+',s.lower()) if len(w)>1 and not w.isdigit()]
def load_truth():
    out=[]
    for f in glob.glob(VAULT + '/pipeline/runs/2026-11-26_batch0[57]/*/picost.json'):
        paper=f.split('/')[-2]; d=json.load(open(f))
        for fi in d.get('findings',[]):
            for n in fi.get('numbers',[]):
                if str(n.get('table_or_figure','')).strip().lower().startswith('table') and n.get('pdf_page') and n.get('value') not in (None,''):
                    out.append({'paper':paper,**n})
    return out
KEYMAP={'Bougie':'@bougie','Sarol':'@sarol','Tyser':'@tyser','Woelfle':'@woelfle'}
def row_hit(tables,val,rowlabel):
    """value is a numeric token of a cell in some row whose context (cells of the row + first-column cells above it) contains >=60% of the row-label words"""
    lw=set(words(rowlabel)); 
    for t in tables:
        for ri,row in enumerate(t):
            if any(val in numbers_in(c) for c in row if is_numeric_cell(c)):
                ctx=' '.join(c for c in row if not is_numeric_cell(c))+' '+' '.join((t[k][0] if t[k] else '') for k in range(ri))
                cw=set(words(ctx))
                if not lw or len(lw&cw)/len(lw)>=0.6: return True
    return False
def eval_A(R):
    T=load_truth(); res={p:{'n':0,'val':0,'nrow':0,'row':0,'strict_n':0,'strict_val':0,'strict_nrow':0,'strict_row':0} for p in PARS}; per={}; detail=[]
    for t in T:
        ck=[P['citekey'] for P in PAGES if any(P['citekey'].startswith(v) for k,v in KEYMAP.items() if t['paper'].startswith(k))][0]
        nums=numbers_in(str(t['value']))
        if not nums: continue
        v=nums[0]; pg=int(t['pdf_page']); rl=(t.get('row') or '').strip()
        strict=bool(re.fullmatch(r'Table\s+\d+',t['table_or_figure'].strip())) and rl.lower() not in ('caption','footnote','header')
        d={'paper':t['paper'][:12],'page':pg,'value':t['value'],'row':rl,'table':t['table_or_figure']}
        for p in PARS:
            rec=R[p].get((ck,pg)); res[p]['n']+=1
            tabs=rec['tables'] if rec else []
            hit=any(v in numbers_in(c) for tb in tabs for row in tb for c in row if is_numeric_cell(c))
            res[p]['val']+=hit; d[p]=hit
            pp=per.setdefault((t['paper'][:12],p),{'n':0,'val':0,'nrow':0,'row':0}); pp['n']+=1; pp['val']+=hit
            if strict: res[p]['strict_n']+=1; res[p]['strict_val']+=hit
            if rl:
                res[p]['nrow']+=1; rh=hit and row_hit(tabs,v,rl); res[p]['row']+=bool(rh); d[p+'_row']=bool(rh)
                pp['nrow']+=1; pp['row']+=bool(rh)
                if strict: res[p]['strict_nrow']+=1; res[p]['strict_row']+=bool(rh)
        detail.append(d)
    res['per_paper']={f'{k[0]}|{k[1]}':v for k,v in per.items()}
    return res,detail
# ---------- B
PROSE=re.compile(r'[a-z]{3,}')
def regions(pdf,pageno,doc_cache={}):
    """numeric tokens from the text layer between each 'Table N' caption block and the next prose paragraph (downwards; if few numbers, upwards)."""
    doc=doc_cache.setdefault(pdf,pymupdf.open(pdf)); page=doc[pageno-1]
    bl=[b for b in page.get_text('blocks') if b[6]==0]; bl.sort(key=lambda b:(round(b[1]),b[0]))
    caps=[i for i,b in enumerate(bl) if re.match(r'\s*(Table|TABLE)\s+S?\d+',b[4])]
    toks=collections.Counter()
    def prose(b): 
        t=b[4]; return len(t.split())>=25 and len(PROSE.findall(t))>=18 and not re.match(r'\s*(Table|TABLE)\s',t)
    for ci in caps:
        down=[];
        for b in bl[ci+1:]:
            if prose(b) or re.match(r'\s*(Table|TABLE|Figure|FIGURE|Fig\.)\s+S?\d+',b[4]): break
            down.append(b)
        up=[]
        for b in reversed(bl[:ci]):
            if prose(b) or re.match(r'\s*(Table|TABLE|Figure|FIGURE|Fig\.)\s+S?\d+',b[4]): break
            up.append(b)
        nd=sum(len(numbers_in(b[4])) for b in down); nu=sum(len(numbers_in(b[4])) for b in up)
        use=down if nd>=nu else up
        for b in use: toks.update(set(numbers_in(b[4])))
    return toks
def jac(a,b):
    a,b=set(a),set(b)
    return (len(a&b)/len(a|b)) if (a|b) else None
def eval_B(R):
    rows=[]
    for P in PAGES:
        if not P['pdf']: continue
        for pg in P['pages']:
            k=(P['citekey'],pg['page']); reg=regions(P['pdf'],pg['page'])
            row={'citekey':P['citekey'],'page':pg['page'],'tables_in_caption_text':','.join(pg['tables']),'region_numbers':len(reg)}
            ns={}
            for p in PARS:
                rec=R[p].get(k); tabs=rec['tables'] if rec else []
                ns[p]=numset(tabs)
                row[p+'_tables']=len([t for t in tabs if t]); row[p+'_cells']=allcells(tabs); row[p+'_numcells']=numcells(tabs)
                row[p+'_cover']=(sum(1 for x in reg if x in ns[p])/len(reg)) if len(reg)>=3 else None
                row[p+'_sec']=rec['seconds'] if rec else None; row[p+'_error']=(rec or {}).get('error') or ('no result' if not rec else '')
            for a,b in itertools.combinations(PARS,2): row[f'jac_{a}_{b}']=jac(ns[a],ns[b])
            rows.append(row)
    return rows
def mean(x): x=[v for v in x if v is not None]; return round(sum(x)/len(x),3) if x else None
if __name__=='__main__':
    R=load(); A,det=eval_A(R); B=eval_B(R)
    json.dump({'A':A,'A_detail':det},open('eval_A.json','w'),indent=1)
    import csv
    with open('eval_B_pages.tsv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(B[0]),delimiter='\t'); w.writeheader(); w.writerows(B)
    S={}
    for p in PARS:
        S[p]={'pages_with_table_caption':len(B),'tables':sum(r[p+'_tables'] for r in B),'cells_nonempty':sum(r[p+'_cells'] for r in B),'numeric_cells':sum(r[p+'_numcells'] for r in B),
              'pages_zero_tables':sum(1 for r in B if r[p+'_tables']==0),'mean_cover':mean([r[p+'_cover'] for r in B]),
              'sec_per_page_mean':mean([r[p+'_sec'] for r in B]),'sec_per_page_median':(round(statistics.median([r[p+'_sec'] for r in B if r[p+'_sec'] is not None]),3)),
              'errors':sum(1 for r in B if r[p+'_error'])}
    for a,b in itertools.combinations(PARS,2): S[f'jac_{a}_{b}']=mean([r[f'jac_{a}_{b}'] for r in B])
    json.dump({'A':A,'B':S},open('eval_summary.json','w'),indent=1)
    print(json.dumps({'A':{p:{**v,'val_share':round(v['val']/max(v['n'],1),3),'row_share':round(v['row']/max(v['nrow'],1),3)} for p,v in A.items() if p!='per_paper'},'B':S},indent=1))

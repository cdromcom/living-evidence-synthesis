"""Evaluation C: pick 12 pages, write review/ PNGs + grids, index.tsv, review.html"""
import csv, json, os, html, itertools, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pymupdf; pymupdf.TOOLS.mupdf_display_errors(False)
from evaluate import load, PARS, PAGES
R=load(); rows=list(csv.DictReader(open('eval_B_pages.tsv'),delimiter='\t'))
pdfof={P['citekey']:P['pdf'] for P in PAGES}
def f(x): 
    try: return float(x)
    except: return None
def minjac(r): 
    v=[f(r[f'jac_{a}_{b}']) for a,b in itertools.combinations(PARS,2)]; v=[x for x in v if x is not None]; return min(v) if v else None
def merged(r):
    for p in ('marker','mineru'):
        for t in R[p].get((r['citekey'],int(r['page'])),{}).get('tables',[]):
            for row in t[:3]:
                for a,b in zip(row,row[1:]):
                    if a and a==b and not a.replace('.','').isdigit(): return True
    return False
cand=[r for r in rows if sum(int(r[p+'_numcells']) for p in PARS)>=15]
for r in cand: r['mj']=minjac(r)
cand=[r for r in cand if r['mj'] is not None]
chosen=[]; why={}
def take(lst,n,reason):
    k=0
    for r in lst:
        key=(r['citekey'],r['page'])
        if key in why: continue
        why[key]=reason; chosen.append(r); k+=1
        if k==n: break
srt=sorted(cand,key=lambda r:r['mj'])
take(srt,5,'parsers disagree most')
take(srt[::-1],3,'parsers agree')
take([r for r in cand if merged(r)],2,'merged header cells')
take([r for r in rows if any(r[p+'_tables']=='0' for p in PARS) and any(r[p+'_tables']!='0' for p in PARS) and int(r['region_numbers'])>=5],2,'one parser found no table')
take([r for r in sorted(cand,key=lambda r:-int(r['marker_numcells'])) if 0.2<r['mj']<0.95],12-len(chosen),'partial agreement')
os.makedirs('review',exist_ok=True); idx=[]; blocks=[]
def grid(tabs):
    if not tabs: return '(no table found)'
    out=[]
    for i,t in enumerate(tabs):
        if not t: out.append(f'[table {i+1}: empty]'); continue
        w=[min(max(len(row[c]) if c<len(row) else 0 for row in t),24) for c in range(max(len(r) for r in t))]
        out.append(f'[table {i+1}: {len(t)} rows x {len(w)} cols]')
        for row in t: out.append(' | '.join((row[c] if c<len(row) else '')[:24].ljust(w[c]) for c in range(len(w))))
    return '\n'.join(out)
for n,r in enumerate(chosen,1):
    ck,pg=r['citekey'],int(r['page']); stem=f"{n:02d}_{ck.lstrip('@')[:28]}_p{pg}"
    doc=pymupdf.open(pdfof[ck]); doc[pg-1].get_pixmap(dpi=110).save(f'review/{stem}.png')
    g={}
    for p in PARS:
        g[p]=grid(R[p].get((ck,pg),{}).get('tables',[])); open(f'review/{stem}_{p}.txt','w').write(g[p])
    idx.append({'n':n,'citekey':ck,'pdf_page':pg,'table_numbers':r['tables_in_caption_text'],'why_chosen':why[(ck,str(pg))] if (ck,str(pg)) in why else why[(ck,r['page'])],
        **{p+'_tables':r[p+'_tables'] for p in PARS},**{p+'_numcells':r[p+'_numcells'] for p in PARS},
        **{k:(round(float(r[k]),3) if r[k] not in ('','None') else '') for k in r if k.startswith('jac_')}})
    cols=''.join(f'<div class="c"><h3>{p} ({r[p+"_tables"]} tables, {r[p+"_numcells"]} numeric cells)</h3><pre>{html.escape(g[p])}</pre></div>' for p in PARS)
    blocks.append(f'<section id="p{n}"><h2>{n}. {html.escape(ck)}, PDF page {pg} (Table {html.escape(r["tables_in_caption_text"])})</h2><p>{idx[-1]["why_chosen"]}. Jaccard: '+', '.join(f'{k[4:]} {idx[-1][k]}' for k in idx[-1] if k.startswith('jac_'))+f'</p><img src="review/{stem}.png" alt="page"><div class="row">{cols}</div></section>')
with open('review_index.tsv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(idx[0]),delimiter='\t'); w.writeheader(); w.writerows(idx)
open('review.html','w').write('<!doctype html><meta charset="utf-8"><title>Table parser review</title><style>body{font-family:system-ui;margin:1em 2em}img{max-width:700px;border:1px solid #888;display:block;margin:.5em 0}.row{display:flex;gap:1em;align-items:flex-start}.c{flex:1;min-width:0;overflow-x:auto}pre{font:11px/1.3 ui-monospace,monospace;background:#f4f4f4;padding:.5em;white-space:pre}section{border-top:2px solid #444;margin-top:2em}</style><h1>Table cells: PyMuPDF find_tables vs Marker vs MinerU</h1><p>Each section shows the PDF page (110 dpi) and the cells each parser returned. Spanned cells are repeated in every covered position.</p>'+''.join(blocks))
print(open('review_index.tsv').read())

import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Summaries and scoring for supplementary files. Writes supp_results.json"""
import json, glob, os, re, sys, itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import evaluate
from evaluate import numset, numcells, allcells, words, is_numeric_cell, numbers_in, jac
from tablelib import repair_tables
PARS=['reader','pymupdf','marker','mineru']
R={p:{} for p in PARS}
for p in PARS:
    for f in glob.glob(f'results_supp/{p}/*.json'):
        r=json.load(open(f)); R[p][os.path.basename(f)[:-5]]=r
files=sorted(set(k for p in PARS for k in R[p]))
rows=[]
for fn in files:
    row={'file':fn,'type':fn.rsplit('.',1)[-1]}
    for p in PARS:
        r=R[p].get(fn)
        if not r: row[p]='not run'; continue
        if isinstance(r.get('pages'),int): row['pages']=max(row.get('pages',0),r['pages'])
        row[p]={'tables':len([t for t in r['tables'] if t]),'cells':allcells(r['tables']),'numeric_cells':numcells(r['tables']),'seconds':r['seconds'],'error':(r.get('error') or '')[:110]}
    rows.append(row)
# Wrightson supplement PDF: agreement between parsers (with repair for pymupdf, marker)
wk='Supp Mat - Wrightson et al 2025.pdf'
ns={p:numset(repair_tables(R[p][wk]['tables']) if p in('pymupdf','marker') else R[p][wk]['tables']) for p in ('pymupdf','marker','mineru')}
wj={f'{a}_{b}':jac(ns[a],ns[b]) for a,b in itertools.combinations(ns,2)}
# ground truth: Woelfle mmc5 hand-corrected values
T=[]
d=json.load(open(glob.glob(VAULT + '/pipeline/runs/2026-11-26_batch07/Woelfle*/picost.json')[0]))
for f in d['findings']:
    for n in f.get('numbers',[]):
        if n.get('from_supplement'): T.append(n)
comp=lambda s:re.sub(r'\s+','',s)
def hit(tables,n):
    val=str(n['value']); tok=numbers_in(val)[0]; rowl=re.sub(r'\(.*?\)','',n['row']).replace(':',' ').replace('/',' '); colw=set(words(n['column'].split('/')[-1] if 'Human Rater' not in n['column'] else n['column']))
    lw=set(words(rowl)); out={'value':False,'row':False,'row_and_column':False}
    for t in tables:
        hdr=t[:2]
        for ri,row in enumerate(t):
            for ci,c in enumerate(row):
                ok=(tok in numbers_in(c)) if is_numeric_cell(c) else False
                if '/' in val: ok=ok and comp(val.split('(')[0]) in comp(c)
                if not ok: continue
                out['value']=True
                ctx=' '.join(x for x in row if not is_numeric_cell(x))+' '+' '.join(t[k][0] for k in range(ri) if t[k])
                if not lw or len(lw&set(words(ctx)))/len(lw)>=0.6:
                    out['row']=True
                    hw=set(words(' '.join(h[ci] for h in hdr if ci<len(h))))
                    if not colw or len(colw&hw)/len(colw)>=0.6: out['row_and_column']=True
    return out
sc={}
mk='1-s2.0-S0895435624002890-mmc5.docx'
for p in PARS:
    r=R[p].get(mk)
    if not r or r.get('error') or not any(r['tables']): sc[p]={'n':len(T),'value':0,'row':0,'row_and_column':0,'note':('not run' if not r else (r.get('error') or 'parser ran, no tables found'))}; continue
    tb=r['tables']; res=[hit(tb,n) for n in T]
    sc[p]={'n':len(T),**{k:sum(x[k] for x in res) for k in ('value','row','row_and_column')}}
json.dump({'files':rows,'wrightson_supp_jaccard':wj,'woelfle_supp_truth':sc},open('supp_results.json','w'),indent=1)
for r in rows: print(json.dumps(r)[:430])
print(wj); print(json.dumps(sc))

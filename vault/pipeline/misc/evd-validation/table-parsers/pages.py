import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Select table pages: lines starting with 'Table <num>' ; cap 10 per paper. Writes pages.json."""
import sys, re, json, glob, os
sys.path.insert(0,VAULT + '/pipeline/scripts')
import pdf_pages, fitz
RX=re.compile(r'^\s*(Table|TABLE)\s+(S?\d+)', re.M)
out=[]
for f in sorted(glob.glob(VAULT + '/sysrev/dgraph/source/@*.md')):
    ck=os.path.basename(f)[:-3]; pdf=pdf_pages.resolve_pdf(ck)
    if not pdf: out.append({'citekey':ck,'pdf':None,'pages':[]}); continue
    doc=fitz.open(pdf); pg=[]
    for i,p in enumerate(doc):
        m=RX.findall(p.get_text())
        if m: pg.append({'page':i+1,'tables':sorted({x[1] for x in m})})
    out.append({'citekey':ck,'pdf':str(pdf),'npages':len(doc),'pages_all':len(pg),'pages':pg[:10]})
json.dump(out,open('pages.json','w'),indent=1)
for o in out: print(o['citekey'][:40], o.get('npages'), o.get('pages_all'), len(o['pages']))
print(sum(len(o['pages']) for o in out))

"""PyMuPDF find_tables. usage: run_pymupdf.py [pages.json] [out_dir]  (pages entries may carry 'pdfpage' = page number inside the PDF)"""
import json, os, sys, time, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
pages=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'pages.json')); outd=sys.argv[2] if len(sys.argv)>2 else 'results/pymupdf'
os.makedirs(outd,exist_ok=True)
for P in pages:
    if not P['pdf']: continue
    doc=pymupdf.open(P['pdf'])
    for pg in P['pages']:
        t=time.time(); rec={'citekey':P['citekey'],'page':pg['page']}
        try:
            tabs=doc[pg.get('pdfpage',pg['page'])-1].find_tables()
            rec['tables']=[[[('' if c is None else ' '.join(str(c).split())) for c in row] for row in tb.extract()] for tb in tabs.tables]
        except Exception as e: rec['error']=repr(e)[:300]; rec['tables']=[]
        rec['seconds']=round(time.time()-t,3)
        json.dump(rec,open(f"{outd}/{P['citekey']}__p{pg['page']}.json",'w'))
print('done',pymupdf.__version__)

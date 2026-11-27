import json, os, time, resource, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
pages=json.load(open('pages.json')); os.makedirs('results/pymupdf',exist_ok=True)
for P in pages:
    if not P['pdf']: continue
    doc=pymupdf.open(P['pdf'])
    for pg in P['pages']:
        t=time.time(); rec={'citekey':P['citekey'],'page':pg['page']}
        try:
            tabs=doc[pg['page']-1].find_tables()
            rec['tables']=[[[('' if c is None else ' '.join(str(c).split())) for c in row] for row in tb.extract()] for tb in tabs.tables]
        except Exception as e: rec['error']=repr(e)[:300]; rec['tables']=[]
        rec['seconds']=round(time.time()-t,3)
        json.dump(rec,open(f"results/pymupdf/{P['citekey']}__p{pg['page']}.json",'w'))
print('done', pymupdf.__version__ if hasattr(pymupdf,'__version__') else '')

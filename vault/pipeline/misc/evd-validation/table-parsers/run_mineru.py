"""MinerU 4.x local parse, tier 'basic' (pipeline models, no VLM), one page per call, models stay loaded in the process.
usage: run_mineru.py pages.json out_dir [citekey_substring]"""
import sys, json, os, time, resource, traceback
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tablelib import html_to_grids
def tables_of(pg):
    out=[]
    def walk(o):
        if isinstance(o,dict):
            if o.get('type')=='table_body' and isinstance(o.get('content'),str): out.append(o['content'])
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(pg); return out
def main():
    from mineru.parser import parse
    pages=json.load(open(sys.argv[1])); outd=sys.argv[2]; flt=sys.argv[3] if len(sys.argv)>3 else ''
    os.makedirs(outd,exist_ok=True)
    for P in pages:
        if flt not in P['citekey'] or not P['pdf']: continue
        for pg in P['pages']:
            fn=f"{outd}/{P['citekey']}__p{pg['page']}.json"
            if os.path.exists(fn): continue
            t=time.time(); rec={'citekey':P['citekey'],'page':pg['page']}
            try:
                r=parse(P['pdf'],tier='basic',ocr_mode='auto',image_analysis=False,page_range=str(pg.get('pdfpage',pg['page'])))
                mj=r.middle_json.to_dict()
                rec['tables']=[g for pgd in mj['pages'] for h in tables_of(pgd) for g in (html_to_grids(h) or [[]])]
            except Exception as e:
                rec['error']=repr(e)[:300]; rec['tables']=[]; traceback.print_exc()
            rec['seconds']=round(time.time()-t,2); rec['maxrss_mb']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6
            json.dump(rec,open(fn,'w')); print(P['citekey'][:30],pg['page'],len(rec['tables']),rec['seconds'],rec.get('error',''),flush=True)
if __name__=='__main__': main()

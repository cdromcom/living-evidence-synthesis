"""Marker table cells. usage: run_marker.py pages.json out_dir [citekey_substring]"""
import sys, json, time, os, resource, traceback
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tablelib import html_to_grids
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
pages=json.load(open(sys.argv[1])); outd=sys.argv[2]; flt=sys.argv[3] if len(sys.argv)>3 else ''
os.makedirs(outd,exist_ok=True)
t0=time.time(); models=create_model_dict(); print('models loaded',round(time.time()-t0,1),flush=True)
def walk(b,acc):
    if b.get('block_type')=='Table': acc.append(b)
    for c in b.get('children') or []: walk(c,acc)
for P in pages:
    if flt not in P['citekey'] or not P['pdf']: continue
    for pg in P['pages']:
        fn=f"{outd}/{P['citekey']}__p{pg['page']}.json"
        if os.path.exists(fn): continue
        t=time.time(); rec={'citekey':P['citekey'],'page':pg['page']}
        try:
            cp=ConfigParser({'page_range':str(pg['page']-1),'output_format':'json','disable_image_extraction':True})
            conv=PdfConverter(artifact_dict=models,config=cp.generate_config_dict(),renderer=cp.get_renderer())
            r=conv(P['pdf']); d=json.loads(r.model_dump_json())
            acc=[]; walk(d,acc)
            rec['tables']=[g for b in acc for g in (html_to_grids(b.get('html','')) or [[]])]
            rec['n_blocks']=len(acc)
        except Exception as e:
            rec['error']=repr(e)[:300]; rec['tables']=[]; traceback.print_exc()
        rec['seconds']=round(time.time()-t,2); rec['maxrss_mb']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6
        json.dump(rec,open(fn,'w')); print(P['citekey'][:30],pg['page'],len(rec['tables']),rec['seconds'],rec.get('error',''),flush=True)

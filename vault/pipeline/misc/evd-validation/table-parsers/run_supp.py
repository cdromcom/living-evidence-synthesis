import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Supplementary files. usage: run_supp.py <pymupdf|marker|mineru|reader>  -> results_supp/<parser>/<file>.json
Files: every PDF/docx/xlsx/csv under the vault pdf folder that is not a seed paper main PDF or an Archive copy."""
import sys, os, json, time, signal, traceback, glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tablelib import html_to_grids
ROOT=VAULT + '/sysrev/dgraph/source/pdfs'
def files():
    out=[]
    for dp,dn,fs in os.walk(ROOT):
        if 'Archive' in dp: continue
        for fn in sorted(fs):
            p=os.path.join(dp,fn); ext=fn.rsplit('.',1)[-1].lower()
            if ext in ('docx','xlsx','xls','csv','pptx'): out.append(p)
            elif ext=='pdf' and (dp!=ROOT or 'supp' in fn.lower()): out.append(p)
    return sorted(out)
class TO(Exception): pass
def alarm(*a): raise TO()
def save(parser,path,rec):
    d=f'results_supp/{parser}'; os.makedirs(d,exist_ok=True)
    rec['file']=os.path.relpath(path,ROOT); json.dump(rec,open(f"{d}/{os.path.basename(path)}.json",'w')); print(parser,os.path.basename(path)[:40],'tables',len(rec.get('tables',[])),'sec',rec.get('seconds'),rec.get('error','')[:100],flush=True)
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
    parser=sys.argv[1]; flt=sys.argv[2] if len(sys.argv)>2 else ''
    if parser=='marker':
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.config.parser import ConfigParser
        models=create_model_dict()
    if parser=='mineru': from mineru.parser import parse
    for path in files():
        if flt and flt not in path: continue
        ext=path.rsplit('.',1)[-1].lower(); rec={'type':ext,'tables':[]}; t=time.time()
        signal.signal(signal.SIGALRM,alarm); signal.alarm(480)
        try:
            if parser=='pymupdf':
                import pymupdf; pymupdf.TOOLS.mupdf_display_errors(False)
                d=pymupdf.open(path); rec['pages']=len(d); rec['tables']=[]
                for p in d:
                    for tb in p.find_tables().tables: rec['tables'].append([[('' if c is None else ' '.join(str(c).split())) for c in row] for row in tb.extract()])
            elif parser=='reader':
                if ext=='docx':
                    import docx; D=docx.Document(path)
                    rec['tables']=[[[' '.join(c.text.split()) for c in row.cells] for row in tb.rows] for tb in D.tables]; rec['pages']='n/a'
                elif ext=='xlsx':
                    import openpyxl; wb=openpyxl.load_workbook(path,data_only=True); rec['pages']=len(wb.sheetnames)
                    rec['tables']=[[[('' if c is None else str(c)) for c in row] for row in ws.iter_rows(values_only=True)] for ws in wb]
                else: rec['error']='reader only handles docx and xlsx'
            elif parser=='marker':
                cp=ConfigParser({'output_format':'json','disable_image_extraction':True})
                conv=PdfConverter(artifact_dict=models,config=cp.generate_config_dict(),renderer=cp.get_renderer())
                d=json.loads(conv(path).model_dump_json())
                def walk(b,acc):
                    if b.get('block_type')=='Table': acc.append(b)
                    for c in b.get('children') or []: walk(c,acc)
                acc=[]; walk(d,acc); rec['pages']=len([c for c in d.get('children',[]) if c.get('block_type')=='Page'])
                rec['tables']=[g for b in acc for g in (html_to_grids(b.get('html','')) or [[]])]
            elif parser=='mineru':
                tier='basic' if ext=='pdf' else 'flash'
                r=parse(path,tier=tier,image_analysis=False,**({'page_range':'all'} if ext=='pdf' else {}))
                mj=r.middle_json.to_dict(); rec['pages']=len(mj['pages']); rec['tier']=tier
                rec['tables']=[g for pg in mj['pages'] for h in tables_of(pg) for g in (html_to_grids(h) or [[]])]
        except TO: rec['error']='timeout 480 s'
        except Exception as e: rec['error']=repr(e)[:300]; traceback.print_exc()
        signal.alarm(0); rec['seconds']=round(time.time()-t,2); save(parser,path,rec)
if __name__=='__main__': main()

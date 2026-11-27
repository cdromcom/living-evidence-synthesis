"""The verified table values that PyMuPDF (with symbol repair) did not find: what each parser returned, a cause category, a highlighted page crop.
Writes missed_values.json and missed-values-images/*.png (local only). Needs the results/ folders (run_*.py) and pages.json."""
import json, os, re, sys, glob, importlib.util
here=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,here)
import evaluate
from evaluate import load, load_truth, PAGES, numbers_in, is_numeric_cell, row_hit, KEYMAP, numcells
import pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
spec=importlib.util.spec_from_file_location('tablelib_v1',os.path.join(here,'scratch','tablelib.before.py')); V1=importlib.util.module_from_spec(spec); spec.loader.exec_module(V1)
from tablelib import repair_tables as repair_v2
R0=load(repair=False)
def repaired(fn):
    R={p:{} for p in R0}
    for p in R0:
        for k,r in R0[p].items():
            r2=dict(r); r2['tables']=fn(r['tables']) if p in ('pymupdf','marker') else r['tables']; R[p][k]=r2
    return R
R1=repaired(V1.repair_tables); R2=repaired(repair_v2)
VAULT=evaluate.VAULT
def found(R,p,ck,pg,v,relaxed=False):
    tabs=R[p].get((ck,pg),{}).get('tables',[])
    return any(v in numbers_in(c) for tb in tabs for row in tb for c in row if relaxed or is_numeric_cell(c))
def rowfound(R,p,ck,pg,v,rl):
    tabs=R[p].get((ck,pg),{}).get('tables',[]); return bool(rl) and row_hit(tabs,v,rl)
allv=[]
for t in load_truth():
    ck=[P['citekey'] for P in PAGES if any(P['citekey'].startswith(v) for k,v in KEYMAP.items() if t['paper'].startswith(k))][0]
    nums=numbers_in(str(t['value']))
    if not nums: continue
    v=nums[0]; pg=int(t['pdf_page']); rl=(t.get('row') or '').strip()
    r={'paper':t['paper'],'ck':ck,'page':pg,'table':t['table_or_figure'],'row':rl,'column':t.get('column',''),'value':str(t['value']),'token':v,'label':t.get('label',''),'unit':t.get('unit','')}
    for name,R in (('plain',R0),('repair_v1',R1),('repair_v2',R2)):
        for p in ('pymupdf','marker','mineru'):
            if p=='mineru' and name!='plain': continue
            r[f'{p}_{name}']=found(R,p,ck,pg,v); r[f'{p}_{name}_relaxed']=found(R,p,ck,pg,v,True)
            r[f'{p}_{name}_row']=found(R,p,ck,pg,v) and rowfound(R,p,ck,pg,v,rl)
    allv.append(r)
miss=[r for r in allv if not r['pymupdf_repair_v1']]
pdfof={P['citekey']:P['pdf'] for P in PAGES}; docs={}
def classify(r):
    tabs=R1['pymupdf'].get((r['ck'],r['page']),{}).get('tables',[]); rl=r['row']
    cells=[c for tb in tabs for row in tb for c in row]
    if r['table'].lower().endswith('caption') or rl.lower() in ('caption','footnote'):
        return 'caption_or_footnote_text','The value is written in the caption or a footnote of the table (for example "scale 0 to 5", "top five sentences", "1,000 reviews"), not in a table cell.'
    if r['pymupdf_repair_v2'] and not r['pymupdf_repair_v1']:
        return 'symbol_problem','The value was in the PyMuPDF cell but the cell held a text-layer symbol problem (a U+0004 minus sign and a footnote letter) that the first repair did not cover; the extended repair recovers it.'
    hold=[c for c in cells if re.search(r'(?<![\d.])'+re.escape(r['value'])+r'(?!\d)',c)]
    if hold and all(re.match(r'^(Top|PRISMA|AMSTAR|PRECIS|\(\d\)|[A-Za-z][A-Za-z -]*\b)',c) and not re.match(r'^[\$\d~.-]',c) for c in hold):
        return 'value_in_label_cell','The number is part of a row label or header text (for example "Top 5 sentences", "(3) Combined LLMs (consistent in 9/9)", "27 items x 112 publications"), so it is a label, not a measured cell value.'
    if hold:
        return 'value_in_mixed_text_cell','PyMuPDF returned the value inside a cell that also holds words or units (for example "$ 1.15 (0.65-1.98) ~2 mins"); my scorer accepts only number-like cells, so it did not count it. The value is present.'
    return 'other','not classified'
for r in miss:
    r['cause'],r['what_happened']=classify(r)
    tabs=R1['pymupdf'].get((r['ck'],r['page']),{}).get('tables',[]); r['pymupdf_tables']=len([t for t in tabs if t])
    doc=docs.setdefault(r['ck'],pymupdf.open(pdfof[r['ck']])); page=doc[r['page']-1]
    r['page_text_blocks_with_value']=[{'bbox':[round(x,1) for x in b[:4]],'text':' '.join(b[4].split())[:100]} for b in page.get_text('blocks') if b[6]==0 and r['token'] in numbers_in(b[4])][:3]
    r['marker_found_plain_strict']=r['marker_plain']; r['mineru_found_strict']=r['mineru_plain']
# images with a highlighted value
os.makedirs(os.path.join(here,'missed-values-images'),exist_ok=True)
def find_rects(page,r):
    rects=[]
    key=r['value'] if r['cause']!='value_in_label_cell' else (r['row'].split('/')[-1].strip()[:30] if r['row'] else r['value'])
    if r['cause']=='caption_or_footnote_text':
        words=page.get_text('words'); cap=[b for b in page.get_text('blocks') if b[6]==0 and re.match(r'\s*(Table|TABLE)\s+\d+',b[4])]
        for w in words:
            if numbers_in(w[4])[:1]==[r['token']] or w[4].strip('.,;()')==r['value']:
                if any(c[0]-2<=w[0]<=c[2]+2 and c[1]-2<=w[1]<=c[3]+2 for c in cap): rects.append(pymupdf.Rect(w[:4]))
        if not rects:
            for b in page.get_text('blocks'):
                if b[6]==0 and re.search(r'\b(five|top five|'+re.escape(r['value'])+r')\b',b[4]) and ('Top-k' in b[4] or 'In-context' in b[4]): rects+=page.search_for('top five sentences')
    else:
        rects=page.search_for(key) or page.search_for(r['value'])
        if not rects and r['cause']=='value_in_label_cell': rects=page.search_for(r['value'])
    return rects[:4]
seen={}
for r in miss:
    k=(r['ck'],r['page'],r['value'],r['row'],r['cause']); 
    if k in seen: r['image']=seen[k]; continue
    doc=pymupdf.open(pdfof[r['ck']]); page=doc[r['page']-1]; rects=find_rects(page,r)
    fn=f"{len(seen)+1:02d}_{r['ck'].lstrip('@')[:14]}_p{r['page']}.png"
    clip=None
    if rects:
        u=pymupdf.Rect(rects[0])
        for q in rects[1:]: u|=q
        for q in rects: page.draw_rect(q+(-1.5,-1.5,1.5,1.5),color=(1,0,0),width=1.6)
        clip=pymupdf.Rect(max(0,u.x0-230),max(0,u.y0-90),min(page.rect.x1,u.x1+230),min(page.rect.y1,u.y1+110))
        if clip.width<420: clip.x0=max(0,clip.x0-(420-clip.width)/2); clip.x1=min(page.rect.x1,clip.x1+(420-clip.width)/2)
    page.get_pixmap(dpi=130,clip=clip).save(os.path.join(here,'missed-values-images',fn))
    r['image']=seen[k]=fn; r['highlighted']=bool(rects)
for r in miss: r['highlighted']=any(x.get('image')==r['image'] and x.get('highlighted') for x in miss)
mo=[r for r in allv if r['mineru_plain'] and not r['pymupdf_repair_v2']]
mo_plain=[r for r in allv if r['mineru_plain'] and not r['pymupdf_plain']]
summary={'values':len(allv),'found_by_pymupdf_plain':sum(r['pymupdf_plain'] for r in allv),'found_by_pymupdf_repair_v1':sum(r['pymupdf_repair_v1'] for r in allv),'found_by_pymupdf_repair_v2':sum(r['pymupdf_repair_v2'] for r in allv),
 'found_by_marker_plain':sum(r['marker_plain'] for r in allv),'found_by_marker_repair_v1':sum(r['marker_repair_v1'] for r in allv),'found_by_marker_repair_v2':sum(r['marker_repair_v2'] for r in allv),'found_by_mineru':sum(r['mineru_plain'] for r in allv),
 'relaxed_any_cell':{p+'_'+n:sum(r[f'{p}_{n}_relaxed'] for r in allv) for p in ('pymupdf','marker') for n in ('plain','repair_v1','repair_v2')}|{'mineru':sum(r['mineru_plain_relaxed'] for r in allv)}}
json.dump({'summary':summary,'missed_repair_v1':miss,'mineru_found_pymupdf_v1_missed':[r for r in allv if r['mineru_plain'] and not r['pymupdf_repair_v1']],'mineru_found_pymupdf_plain_missed':mo_plain,'mineru_found_pymupdf_v2_missed':mo,'all':allv},open('missed_values.json','w'),indent=1,ensure_ascii=False)
print(summary); import collections
print(collections.Counter(r['cause'] for r in miss)); print(collections.Counter((r['paper'][:8],r['cause']) for r in miss))
print('mineru-only v1',len([r for r in allv if r['mineru_plain'] and not r['pymupdf_repair_v1']]),'v2',len(mo),'plain',len(mo_plain))
print('highlighted',sum(1 for r in miss if r.get('highlighted')),'of',len(miss),'images',len(seen))

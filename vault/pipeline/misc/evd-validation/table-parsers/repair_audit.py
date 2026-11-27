"""Compare every cell with and without repair on the 124 pages (all three parsers, repair applied to all for the audit). Writes repair_audit.json"""
import json, glob, os, sys, collections, re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import tablelib
from tablelib import repair_cell_text_notes, numbers_in
out={}
for p in ('pymupdf','marker','mineru'):
    rules=collections.Counter(); ex=collections.defaultdict(list); numchg=[]; changed=0; cells=0; notes=collections.Counter()
    for f in sorted(glob.glob(f'results/{p}/*.json')):
        r=json.load(open(f))
        for t in r['tables']:
            for row in t:
                for c in row:
                    cells+=1; tablelib.REPAIR_COUNTS.clear()
                    n,nt=repair_cell_text_notes(c)
                    if n==c: continue
                    changed+=1; fired=sorted(tablelib.REPAIR_COUNTS)
                    for k in fired:
                        rules[k]+=1
                        if len(ex[k])<4 and (c,n) not in ex[k]: ex[k].append((c[:60],n[:60]))
                    for k in nt: notes[k]+=1
                    a=sorted(numbers_in(c)); b=sorted(numbers_in(n))
                    if a!=b: numchg.append({'file':f.split('/')[-1][:34],'rules':fired,'before':c[:70],'after':n[:70]})
    out[p]={'cells':cells,'changed':changed,'rule_cells':dict(rules),'notes':dict(notes),'examples':ex,'cells_whose_number_tokens_changed':len(numchg),'number_change_samples':numchg[:12]}
json.dump(out,open('repair_audit.json','w'),indent=1,ensure_ascii=False)
for p,v in out.items(): print(p,v['cells'],v['changed'],v['rule_cells'],v['notes'],'numchg',v['cells_whose_number_tokens_changed'])

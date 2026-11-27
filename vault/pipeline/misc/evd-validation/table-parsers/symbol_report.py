"""Count symbol problems per parser over results/<parser>/*.json (tables on the 124 table pages)."""
import json, glob, re, collections, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import tablelib
from tablelib import repair_cell_text, repair_cell_text_notes
root=sys.argv[1] if len(sys.argv)>1 else 'results'
UNREP={'footnote_letter_glued_to_number':r'(?<=[\d)%\]])[a-d*]$','unicode_superscript':r'[²³¹⁰-₟]','khmer_or_other_script_garbage':r'[ក-៿]','plus_minus_sign':'±','unicode_minus_U+2212':'−','en_dash_U+2013':'–','soft_hyphen':'­'}
out={}
for p in ('pymupdf','marker','mineru'):
    tablelib.REPAIR_COUNTS.clear(); after=collections.Counter(); notes=collections.Counter(); changed=0; cells=0; ex={}; un=collections.Counter(); unex={}
    for f in glob.glob(f'{root}/{p}/*.json'):
        r=json.load(open(f))
        for t in r['tables']:
            for row in t:
                for c in row:
                    cells+=1
                    n,nt=repair_cell_text_notes(c)
                    for kk,vv in nt.items(): notes[kk]+=1
                    for k,rx in UNREP.items():
                        if re.search(rx,n): after[k]+=1
                    if n!=c:
                        changed+=1; ex.setdefault(len(ex),(f.split('/')[-1][:26],c[:48],n[:48]))
                    for k,rx in UNREP.items():
                        if re.search(rx,c): un[k]+=1; unex.setdefault(k,c[:48])
                    if re.search('[\x00-\x08\x0e-\x1f]',n): un['control_character_left_after_repair']+=1; unex.setdefault('control_character_left_after_repair',n[:48])
                    if re.search('[-]',n): un['private_use_left_after_repair']+=1; unex.setdefault('private_use_left_after_repair',n[:48])
    out[p]={'cells':cells,'cells_changed_by_repair':changed,'rule_counts':dict(tablelib.REPAIR_COUNTS),'examples':list(ex.values())[:6],'present_not_repaired':dict(un),'present_after_repair':dict(after),'notes':dict(notes),'not_repaired_examples':unex}
json.dump(out,open('symbol_report.json','w'),indent=1,ensure_ascii=False)
for p,v in out.items(): print(p,v['cells'],v['cells_changed_by_repair'],v['rule_counts'],'after:',v['present_after_repair'])

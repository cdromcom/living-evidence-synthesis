"""Score Evaluation A values on the rotation variants. Writes rotation_results.json"""
import json, os, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import evaluate
out={}
pil=lambda ck:ck.startswith(('@sarol','@bougie','@tyser','@woelfle'))
for v in ('rot0','rot90','rot270','img0','img90'):
    for rep in (False,True):
        R=evaluate.load(f'scratch/rot/results/{v}',repair=rep)
        A,_=evaluate.eval_A(R)
        tabs={p:sum(len([t for t in r['tables'] if t]) for r in R[p].values()) for p in evaluate.PARS}
        cells={p:evaluate.numcells([t for r in R[p].values() for t in r['tables']]) for p in evaluate.PARS}
        secs={p:round(sum(r['seconds'] for r in R[p].values())/max(len(R[p]),1),2) for p in evaluate.PARS}
        for p in evaluate.PARS:
            a=A[p]; out[f'{v}|{"repair" if rep else "plain"}|{p}']={'n':a['n'],'value_found':a['val'],'row_found':a['row'],'row_n':a['nrow'],'tables':tabs[p],'numeric_cells':cells[p],'sec_per_page':secs[p],'pages':len(R[p])}
json.dump(out,open('rotation_results.json','w'),indent=1)
for rep in ('plain','repair'):
    print(rep)
    for p in evaluate.PARS:
        print(' ',p,' | '.join(f"{v}: {out[f'{v}|{rep}|{p}']['value_found']}/{out[f'{v}|{rep}|{p}']['n']} row {out[f'{v}|{rep}|{p}']['row_found']} tabs {out[f'{v}|{rep}|{p}']['tables']}" for v in ('rot0','rot90','rot270','img0','img90')))

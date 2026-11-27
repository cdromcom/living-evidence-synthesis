import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Appends rotation, symbol-repair and supplementary examples to review.html (run after build_review.py). Images stay local in review/."""
import json, html, os, re, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
from tablelib import repair_cell_text
PARS=['pymupdf','marker','mineru']
def grid(tabs,maxrows=14):
    if not tabs: return '(no table found)'
    out=[]
    for i,t in enumerate(tabs):
        if not t: out.append(f'[table {i+1}: empty]'); continue
        C=max(len(r) for r in t); w=[min(max(len(row[c]) if c<len(row) else 0 for row in t),22) for c in range(C)]
        out.append(f'[table {i+1}: {len(t)} rows x {C} cols]')
        for row in t[:maxrows]: out.append(' | '.join((row[c] if c<len(row) else '')[:22].ljust(w[c]) for c in range(C)))
        if len(t)>maxrows: out.append('...')
    return '\n'.join(out)
def cols(items): return '<div class="row">'+''.join(f'<div class="c"><h3>{html.escape(h)}</h3><pre>{html.escape(g)}</pre></div>' for h,g in items)+'</div>'
S=[]
# --- symbol repairs
sr=json.load(open('symbol_report.json'))
rows=''.join(f'<tr><td>{p}</td><td>{v["cells_changed_by_repair"]} of {v["cells"]}</td><td>{html.escape(json.dumps(v["rule_counts"]))}</td></tr>' for p,v in sr.items())
ex=''.join(f'<tr><td>{html.escape(a)}</td><td><code>{html.escape(repr(b))}</code></td><td><code>{html.escape(c)}</code></td></tr>' for p in ('pymupdf','marker') for a,b,c in sr[p]['examples'][:0])
pairs=[]
for p in ('pymupdf','marker','mineru'):
    seen=set()
    import glob
    for f in sorted(glob.glob(f'results/{p}/*.json')):
        r=json.load(open(f))
        for t in r['tables']:
            for row in t:
                for c in row:
                    n=repair_cell_text(c)
                    if n!=c:
                        key=(p,tuple(sorted(set(re.findall(r'[\x00-\x08eþ-­]',c)))))
                        if key not in seen and len(seen)<5: seen.add(key); pairs.append((p,f.split('/')[-1][:30],c[:60],n[:60]))
tr=''.join(f'<tr><td>{p}</td><td>{html.escape(f)}</td><td><code>{html.escape(repr(a))}</code></td><td><code>{html.escape(b)}</code></td></tr>' for p,f,a,b in pairs)
S.append(f'<section id="sym"><h2>Symbol repairs (tablelib.repair_cell_text)</h2><table border=1 cellpadding=4><tr><th>parser</th><th>cells changed</th><th>rules fired (cell counts)</th></tr>{rows}</table><h3>Examples before and after</h3><table border=1 cellpadding=4><tr><th>parser</th><th>file</th><th>before</th><th>after</th></tr>{tr}</table></section>')
# --- rotation
def rot_example(ck,page,variants,title):
    stem=f"rot_{ck.lstrip('@')[:20]}_p{page}"; out=[]
    for v in variants:
        pdf=json.load(open(f'scratch/rot/pages_{v}.json')); P=[x for x in pdf if x['citekey']==ck][0]; k=[e['pdfpage'] for e in P['pages'] if e['page']==page][0]
        pymupdf.open(P['pdf'])[k-1].get_pixmap(dpi=110).save(f'review/{stem}_{v}.png')
    items=[]
    for v in variants:
        for p in PARS:
            r=json.load(open(f'scratch/rot/results/{v}/{p}/{ck}__p{page}.json')); items.append((f'{v} / {p} ({len(r["tables"])} tables)',grid(r['tables'],8)))
    imgs=''.join(f'<figure style="margin:0"><figcaption>{v}</figcaption><img src="review/{stem}_{v}.png" style="max-width:340px"></figure>' for v in variants)
    body=''
    for i in range(0,len(items),3): body+=cols(items[i:i+3])
    return f'<section><h2>{html.escape(title)}</h2><div class="row">{imgs}</div>{body}</section>'
S.append(rot_example('@sarolAssessingCitationIntegrity2024',5,['rot0','rot90','img90'],'Rotation: Sarol page 5 (tables 1 and 2), page copies at 0 and 90 degrees and an image-only copy at 90 degrees'))
S.append(rot_example('@woelfleBenchmarkingHumanAICollaboration2024',5,['rot270','img90'],'Rotation: Woelfle page 5 (Table 2), 270 degrees and an image-only copy at 90 degrees'))
# --- supplementary
sup=[]
for p,lab in (('reader','python-docx reader'),('mineru','MinerU (flash tier, docx)'),('pymupdf','PyMuPDF opened as document'),('marker','Marker')):
    r=json.load(open(f'results_supp/{p}/1-s2.0-S0895435624002890-mmc5.docx.json'))
    sup.append((f'{lab}: {len(r["tables"])} tables'+(' / not converted: WeasyPrint system library (pango) missing' if r.get('error') else ''),grid(r['tables'][1:2],8) if r['tables'] else '(nothing returned)'))
S.append('<section><h2>Supplementary: Woelfle mmc5.docx, Supplementary Table 2 (first rows)</h2>'+cols(sup[:2])+cols(sup[2:])+'</section>')
wk='Supp Mat - Wrightson et al 2025.pdf'; src=pymupdf.open(VAULT + '/sysrev/dgraph/source/pdfs/'+wk)
src[2].get_pixmap(dpi=110).save('review/supp_wrightson_p3.png')
items=[]
for p in PARS:
    r=json.load(open(f'results_supp/{p}/{wk}.json')); items.append((f'{p}: {len(r["tables"])} tables, whole file',grid(r['tables'][:2],8)))
S.append('<section><h2>Supplementary: Wrightson supplement PDF, page 3 (landscape page)</h2><img src="review/supp_wrightson_p3.png" style="max-width:700px;display:block">'+cols(items)+'</section>')
h=open('review.html').read()
h=h.split('<!--EXTRA-->')[0]+'<!--EXTRA-->'+''.join(S)
open('review.html','w').write(h)
print('ok',len(h))

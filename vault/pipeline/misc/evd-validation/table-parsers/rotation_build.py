"""Build rotated and rasterised copies of the table pages of the four pilot papers (scratch/rot/<variant>/...)."""
import json, os, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
pages=[P for P in json.load(open('pages.json')) if P['citekey'][:6] in ('@sarol','@bougie'[:6],'@tyser','@woelf')]
pages=[P for P in pages if P['citekey'].startswith(('@sarol','@bougie','@tyser','@woelfle'))]
VARS={'rot0':0,'rot90':90,'rot270':270,'img0':0,'img90':90}
for v,deg in VARS.items():
    os.makedirs(f'scratch/rot/{v}',exist_ok=True); plist=[]
    for P in pages:
        src=pymupdf.open(P['pdf']); out=pymupdf.open(); entries=[]
        for k,pg in enumerate(P['pages']):
            sp=src[pg['page']-1]
            if v.startswith('rot'):
                out.insert_pdf(src,from_page=pg['page']-1,to_page=pg['page']-1); out[-1].set_rotation((sp.rotation+deg)%360)
            else:
                pix=sp.get_pixmap(dpi=200); w,h=sp.rect.width,sp.rect.height
                np_=out.new_page(width=(h if deg else w),height=(w if deg else h))
                np_.insert_image(np_.rect,pixmap=pix,rotate=deg)
            entries.append({'page':pg['page'],'tables':pg['tables'],'pdfpage':k+1})
        fn=os.path.abspath(f"scratch/rot/{v}/{P['citekey']}.pdf"); out.save(fn)
        plist.append({'citekey':P['citekey'],'pdf':fn,'pages':entries})
    json.dump(plist,open(f'scratch/rot/pages_{v}.json','w'))
    print(v,sum(len(p['pages']) for p in plist))

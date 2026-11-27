import os
VAULT = os.environ.get('LIVES_VAULT') or os.path.expanduser('~/Documents/living-synthesis')
"""Scan every PDF under the vault pdf folder (all subfolders) for table-caption pages that are rotated or sideways."""
import os, re, json, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
ROOT=VAULT + '/sysrev/dgraph/source/pdfs'
RX=re.compile(r'^\s*(Table|TABLE|Supplementary Table|Supplemental Table)\s+S?\d+',re.M)
out=[]; npdf=0; npages=0; ncap=0
for dp,_,fs in os.walk(ROOT):
    for fn in sorted(fs):
        if not fn.lower().endswith('.pdf'): continue
        path=os.path.join(dp,fn); npdf+=1
        try: doc=pymupdf.open(path)
        except Exception as e: out.append({'file':fn,'error':repr(e)}); continue
        for i,p in enumerate(doc):
            npages+=1
            t=p.get_text()
            if not RX.search(t): continue
            ncap+=1
            ch_v=ch_all=0
            for b in p.get_text('dict')['blocks']:
                for l in b.get('lines',[]):
                    n=sum(len(s['text']) for s in l['spans']); ch_all+=n
                    if abs(l['dir'][0])<0.5: ch_v+=n
            r=p.rect; frac=ch_v/ch_all if ch_all else 0
            flags=[]
            if p.rotation: flags.append(f'page.rotation={p.rotation}')
            if frac>0.5: flags.append(f'{frac:.0%} of characters in vertical lines')
            elif frac>0.15: flags.append(f'{frac:.0%} of characters in vertical lines (partial)')
            if r.width>r.height*1.1: flags.append('landscape page')
            if flags: out.append({'file':os.path.relpath(path,ROOT),'pdf_page':i+1,'flags':flags,'vertical_char_share':round(frac,3),'rotation':p.rotation})
json.dump({'pdfs':npdf,'pages':npages,'caption_pages':ncap,'flagged':out},open('rotated_scan.json','w'),indent=1)
print(npdf,npages,ncap,len(out))
for o in out: print(o)

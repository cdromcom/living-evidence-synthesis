import json,sys,collections,re
S=sys.argv[1]
TR='/Users/ppatel/.claude/projects/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28/tool-results'
B='/Users/ppatel/Documents/living-synthesis/pipeline/misc/evd-validation/2026-11-16-benchmark'
cur=json.load(open(TR+'/mcp-claude_ai_Google_Sheets-get_values-1794964804316-nlpode.txt'))['values']
snap=json.load(open(B+'/hai-copy-snapshot-2026-11-11-1831EST.json'))
orig=json.load(open(TR+'/mcp-claude_ai_Google_Sheets-get_values-1794964964546-8olnfi.txt'))['values']
omap=json.load(open(S+'/orig_rowmap.json'))
W=json.load(open(S+'/prov_writes.json')); split=W['split_ts']
Q=json.load(open(S+'/q_writes_1111.json'))
def g(rows,r,c):
    if r-1>=len(rows): return ''
    row=rows[r-1]; return (row[c] if c<len(row) else '').strip()
pre={6:6,7:7,10:10,11:11,12:14,13:15,14:18,15:19,16:22,17:23}
last={}
for ts,r,c,v,kind,ok in W['writes']:
    if kind not in('update_values','updateCells','update_formulas') or not ok or r<2: continue
    if ts<split: c=pre.get(c, c+6 if c>=18 else c)
    last[(r,c)]=(ts,str(v).strip())
def batch(ts,r,c):
    if ts.startswith('2026-11-17T04:07'): return 'C1: Claude Opus 5.5 relevancy, written 2026-11-16 (this session)'
    if ts.startswith('2026-11-17T04:1') or ts.startswith('2026-11-17T05:49'): return 'C2: Claude Opus 5.5 draft, 2026-11-16/17 (this session)'
    if ts.startswith('2026-11-17T04:56:2'): return 'cleared'
    if ts.startswith('2026-11-17T04:56:'): return 'R1: restored to Claude original text from original sheet (2026-11-16)'
    if ts.startswith('2026-11-17T05:11'): return 'R2: restored 2026-11-17 because JP said rows 79-82 were Claude-generated'
    if ts.startswith('2026-11-18T00:18'): return 'C3: Claude Opus 5.5 fresh relevancy, 2026-11-17 (this session)'
    if ts.startswith('2026-11-18T00:20'): return 'C4: Claude Opus 5.5 note, 2026-11-17 (this session)'
    if ts.startswith('2026-11-18T00:42'): return 'R3: restored from 2026-11-11 snapshot (Claude rows), 2026-11-17'
    if ts.startswith('2026-11-18T00:53'): return 'C5: continuation-row NA marker written by Claude 2026-11-17'
    if ts>='2026-11-18T01:00': return 'C6: Claude Opus 5.5 Fidelity/Grounding, graded 2026-11-17 (this session)'
    return 'other '+ts
JPCOLS=[9,12,13,16,17,20,21]  # I(8) J(9) M N Q R U V
jp_texts=set()
for r in range(2,83):
    for c in (9,13,17,21,8,12,16,20):
        t=g(cur,r,c)
        if len(t)>25: jp_texts.add(t)
# Jay-row notes in original/snapshot (JP-authored)
for r in range(2,83):
    if g(snap,r,0)=='Jay':
        for c in (8,10,12,14):
            t=g(snap,r,c)
            if len(t)>25: jp_texts.add(t)
JPMARK=re.compile(r'\[JP|\bJP:|\bJP\b approved|Jay:|^qQ$',re.I)
PAIRS=[(6,7,'G','H'),(10,11,'K','L'),(14,15,'O','P'),(18,19,'S','T')]
snapc={6:7,7:8,10:9,11:10,14:11,15:12,18:13,19:14}
rows=[];issues=[];cnt=collections.Counter()
for r in range(2,83):
    for c in [6,7,10,11,14,15,18,19,23]:
        L='GHKLOPSTX'[[6,7,10,11,14,15,18,19,23].index(c)]
        v=g(cur,r,c); w=last.get((r,c))
        if w:
            src=batch(w[0],r,c); exp=w[1]
        elif c==23:
            q=Q.get(str(r)); src='C0: Claude draft written 2026-11-11/13 (session 321443ce, LIVES - EVD col Q)' if q else 'no record'; exp=q[1] if q else None
        else:
            src='S0: unchanged since 2026-11-11 snapshot'; exp=g(snap,r,snapc[c])
            if g(snap,r,0)=='Claude':
                om=omap.get(str(r)); ov=(orig[om-1]+['']*12)[ [3,4,5,6,7,8,9,10][[6,7,10,11,14,15,18,19].index(c)] ].strip() if om else None
                src+=' = original sheet' if ov==exp else ' (added to this copy before 2026-11-11 18:31 EST; not in original sheet)' if not ov else ' (differs slightly from original sheet)'
            else: src+=' [JAY ROW]'
        match=(exp is not None and v==exp)
        flags=[]
        if not match: flags.append('VALUE CHANGED after last Claude write' if exp is not None else 'NO PROVENANCE RECORD')
        if v and JPMARK.search(v): flags.append('JP marker in text')
        if v in jp_texts: flags.append('IDENTICAL TO JP TEXT')
        if '[JAY ROW]' in src and v: flags.append('JAY-ROW value never replaced')
        if src.startswith('R2'): flags.append('provenance = JP statement only')
        if src=='cleared' and v: flags.append('cleared cell now has a value')
        rows.append(dict(row=r,col=L,value=v[:80],source=src,flags=flags))
        for f in flags: cnt[(L,f)]+=1
        cnt[(L,src.split(':')[0])]+=1
# pairing
pairs=[]
for r in range(2,83):
    for a,b,La,Lb in PAIRS:
        va,vb=g(cur,r,a),g(cur,r,b)
        if bool(va)!=bool(vb): pairs.append((r,La,va[:30],Lb,vb[:60]))
json.dump(rows,open(S+'/prov_final.json','w'),indent=1)
for k,n in sorted(cnt.items()): print(n,k)
print('\nPAIRING PROBLEMS:',pairs)
print('\nFLAGGED CELLS:')
for x in rows:
    if x['flags']: print(x['row'],x['col'],x['flags'],'|',x['source'][:70],'|',x['value'][:60])

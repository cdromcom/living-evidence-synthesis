import json,re,sys
T='/Users/ppatel/.claude/projects/-Users-ppatel/8b1a8cc8-fee8-4b43-8bb9-1a0f568cde28.jsonl'
SID=1173184436
def col2i(s):
    n=0
    for ch in s: n=n*26+ord(ch)-64
    return n-1
writes=[]  # (ts, row1, colidx, value, kind)
split_ts=None
results={}
# map tool_use_id -> success?
lines=[json.loads(l) for l in open(T) if l.strip()]
for d in lines:
    m=d.get('message',{})
    if d.get('type')=='user' and isinstance(m.get('content'),list):
        for x in m['content']:
            if x.get('type')=='tool_result':
                c=x.get('content'); s=json.dumps(c)
                results[x['tool_use_id']]=('"status":"success"' in s.replace('\\','') or 'success' in s) and 'Error' not in s[:200]
for d in lines:
    m=d.get('message',{})
    if d.get('type')!='assistant' or not isinstance(m.get('content'),list): continue
    for x in m['content']:
        if x.get('type')!='tool_use': continue
        n=x['name'].split('__')[-1]; i=x['input']
        if i.get('spreadsheetId')!='1uEBhz2ReUFsXYRdy70UPZ4F_QZhAZmMrmksDWy-pPq8': continue
        ok=results.get(x['id'])
        ts=d['timestamp']
        if n in('update_values','update_formulas'):
            rng=i.get('range','')
            if 'Benchmarking' not in rng: continue
            mm=re.search(r"!([A-Z]+)(\d+)",rng); c0=col2i(mm.group(1)); r0=int(mm.group(2))
            vals=i.get('values') or i.get('formulas')
            if isinstance(vals,str): vals=json.loads(vals)
            for dr,row in enumerate(vals):
                for dc,v in enumerate(row):
                    writes.append((ts,r0+dr,c0+dc,v,n,ok))
        elif n=='update_spreadsheet':
            rs=i.get('requests'); rs=json.loads(rs) if isinstance(rs,str) else rs
            for r in rs:
                k=list(r)[0]; v=r[k]
                if k=='insertDimension' and v['range'].get('sheetId')==SID and v['range']['dimension']=='COLUMNS' and ok:
                    split_ts=split_ts or ts; writes.append((ts,0,v['range']['startIndex'],'<<INSERT %d>>'%(v['range']['endIndex']-v['range']['startIndex']),'insert',ok))
                if k=='updateCells' and v.get('start',{}).get('sheetId')==SID:
                    st=v['start']
                    for dr,row in enumerate(v['rows']):
                        for dc,cell in enumerate(row.get('values',[])):
                            uv=cell.get('userEnteredValue')
                            if uv is not None: writes.append((ts,st['rowIndex']+1+dr,st['columnIndex']+dc,list(uv.values())[0],'updateCells',ok))
                if k in('cutPaste','copyPaste','pasteData','findReplace','moveDimension','deleteDimension') :
                    s=json.dumps(v)
                    if str(SID) in s or (k=='findReplace' and v.get('allSheets')): writes.append((ts,-1,-1,s[:300],k,ok))
json.dump({'split_ts':split_ts,'writes':writes},open(sys.argv[1],'w'))
print('split_ts',split_ts,'writes',len(writes))
import collections
print(collections.Counter((w[4],w[5]) for w in writes))
for w in writes:
    if w[4] not in('update_values','updateCells','update_formulas'): print(w[0],w[4],w[5],str(w[3])[:250])

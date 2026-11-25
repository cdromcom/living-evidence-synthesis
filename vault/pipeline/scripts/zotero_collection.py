#!/usr/bin/env python3
"""Export one Zotero collection (records and PDF paths) for screening (JP, 2026-11-25). Read-only: works on a COPY of zotero.sqlite. Output goes to ~/.cache/lives-bench/screening/ (not the vault: it holds abstracts and local file paths).
  python3 zotero_collection.py "SysRev - Elicit 2026-11-24" [--library 1] [--out FILE.json]
Each record: zotero key, library, item type, title, creators, year, date, DOI, URL, arXiv id, publication, abstract, tags, PDF path(s) and sizes."""
import argparse, json, os, re, shutil, sqlite3, sys, tempfile
from pathlib import Path
Z = Path.home() / 'Zotero'
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('collection'); ap.add_argument('--library', type=int, default=1); ap.add_argument('--out'); a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp())
    for f in ('zotero.sqlite', 'zotero.sqlite-wal', 'zotero.sqlite-shm'):
        if (Z / f).exists(): shutil.copy(Z / f, tmp / f)
    db = sqlite3.connect(tmp / 'zotero.sqlite')
    cid = db.execute('select collectionID from collections where collectionName=? and libraryID=?', (a.collection, a.library)).fetchone()
    if not cid: sys.exit(f'collection not found: {a.collection} in library {a.library}')
    cid = cid[0]
    items = db.execute("""select i.itemID, i.key, t.typeName, i.dateAdded from collectionItems ci join items i on i.itemID=ci.itemID join itemTypes t on t.itemTypeID=i.itemTypeID
                          where ci.collectionID=? and t.typeName not in ('attachment','note') order by i.dateAdded""", (cid,)).fetchall()
    def fields(iid):
        return {n: v for n, v in db.execute("select f.fieldName, v.value from itemData d join fields f on f.fieldID=d.fieldID join itemDataValues v on v.valueID=d.valueID where d.itemID=?", (iid,))}
    out = []
    for iid, key, typ, added in items:
        f = fields(iid)
        cr = [f"{(l or '').strip()}, {(fn or '').strip()}".strip(', ') for l, fn in db.execute("select c.lastName, c.firstName from itemCreators ic join creators c on c.creatorID=ic.creatorID where ic.itemID=? order by ic.orderIndex", (iid,))]
        tags = [t for (t,) in db.execute("select t.name from itemTags it join tags t on t.tagID=it.tagID where it.itemID=?", (iid,))]
        pdfs = []
        for aid, akey, path in db.execute("select a.itemID, i.key, a.path from itemAttachments a join items i on i.itemID=a.itemID where a.parentItemID=? and a.contentType='application/pdf'", (iid,)):
            if path and path.startswith('storage:'):
                p = Z / 'storage' / akey / path[len('storage:'):]
                if p.exists(): pdfs.append({'path': str(p), 'bytes': p.stat().st_size})
        doi = (f.get('DOI') or '').strip().lower() or (re.search(r'10\.\d{4,9}/\S+', f.get('extra', '') + ' ' + f.get('url', '')) or [None])[0]
        arx = re.search(r'arxiv(?:\.org/(?:abs|pdf)/|:)\s*(\d{4}\.\d{4,6})', (f.get('url', '') + ' ' + f.get('extra', '') + ' ' + (f.get('DOI') or '')), re.I)
        out.append({'key': key, 'library': a.library, 'type': typ, 'title': (f.get('title') or '').strip(), 'creators': cr, 'date': f.get('date', ''), 'year': (re.search(r'(19|20)\d\d', f.get('date', '')) or [''])[0] if re.search(r'(19|20)\d\d', f.get('date', '')) else '',
                    'doi': doi, 'url': f.get('url', ''), 'arxiv': arx.group(1) if arx else '', 'publication': f.get('publicationTitle') or f.get('proceedingsTitle') or f.get('repository') or '', 'abstract': (f.get('abstractNote') or '').strip(),
                    'tags': tags, 'added': added, 'pdfs': pdfs})
    out_path = Path(a.out or Path.home() / '.cache/lives-bench/screening' / (re.sub(r'\W+', '-', a.collection).strip('-') + f'-lib{a.library}.json'))
    out_path.parent.mkdir(parents=True, exist_ok=True); out_path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{len(out)} items; {sum(1 for r in out if r['pdfs'])} with a PDF file on disk; {sum(1 for r in out if r['abstract'])} with an abstract; {sum(1 for r in out if r['doi'])} with a DOI; wrote {out_path}")
if __name__ == '__main__': main()

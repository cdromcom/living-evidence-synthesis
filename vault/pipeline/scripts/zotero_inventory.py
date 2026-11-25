#!/usr/bin/env python3
"""Inventory every item in all Zotero libraries (personal, groups; not feeds), read-only from a COPY of zotero.sqlite (JP, 2026-11-25).
  python3 zotero_inventory.py [--out ~/.cache/lives-bench/screening/zotero-all.jsonl]
One JSON line per regular item: key, library, type, title, creators, date, year, doi, url, arxiv, publication, abstract, tags, collections (full paths), pdfs (files on disk), html snapshots (files on disk), added.
Standalone PDF attachments (no parent item) become items too, with the file name as the title. Output stays outside the vault (abstracts and local paths)."""
import argparse, collections, json, re, shutil, sqlite3, tempfile
from pathlib import Path
Z = Path.home() / 'Zotero'
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=str(Path.home() / '.cache/lives-bench/screening/zotero-all.jsonl')); a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp())
    for f in ('zotero.sqlite', 'zotero.sqlite-wal', 'zotero.sqlite-shm'):
        if (Z / f).exists(): shutil.copy(Z / f, tmp / f)
    db = sqlite3.connect(tmp / 'zotero.sqlite')
    libs = {r[0]: (r[1] if r[1] else ('personal' if r[2] == 'user' else str(r[0]))) for r in db.execute("select l.libraryID, g.name, l.type from libraries l left join groups g on g.libraryID=l.libraryID")}
    skip_types = {r[0] for r in db.execute("select itemTypeID from itemTypes where typeName in ('attachment','note','annotation')")}
    items = {r[0]: {'key': r[1], 'library': libs.get(r[2], str(r[2])), 'libid': r[2], 'type': r[3], 'added': r[4][:10]} for r in db.execute("select i.itemID, i.key, i.libraryID, t.typeName, i.dateAdded from items i join itemTypes t on t.itemTypeID=i.itemTypeID where i.itemTypeID not in (%s) and i.itemID not in (select itemID from deletedItems)" % ','.join(map(str, skip_types)))}
    items = {k: v for k, v in items.items() if v['libid'] in {l for l in libs if not db.execute('select 1 from libraries where libraryID=? and type=?', (l, 'feed')).fetchone()}}
    fld = {r[0]: r[1] for r in db.execute('select fieldID, fieldName from fields')}; val = {}
    want = {'title', 'abstractNote', 'date', 'DOI', 'url', 'publicationTitle', 'proceedingsTitle', 'repository', 'extra'}
    wantid = {i for i, n in fld.items() if n in want}
    for iid, fid, v in db.execute('select d.itemID, d.fieldID, v.value from itemData d join itemDataValues v on v.valueID=d.valueID where d.fieldID in (%s)' % ','.join(map(str, wantid))):
        if iid in items: items[iid].setdefault('f', {})[fld[fid]] = v
    cre = collections.defaultdict(list)
    for iid, ln, fn in db.execute('select ic.itemID, c.lastName, c.firstName from itemCreators ic join creators c on c.creatorID=ic.creatorID order by ic.itemID, ic.orderIndex'):
        if iid in items: cre[iid].append(f"{(ln or '').strip()}, {(fn or '').strip()}".strip(', '))
    tags = collections.defaultdict(list)
    for iid, t in db.execute('select it.itemID, t.name from itemTags it join tags t on t.tagID=it.tagID'):
        if iid in items: tags[iid].append(t)
    cnames = {r[0]: (r[1], r[2]) for r in db.execute('select collectionID, collectionName, parentCollectionID from collections')}
    def cpath(c):
        n = []
        while c: nm, par = cnames[c]; n.append(nm); c = par
        return ' / '.join(reversed(n))
    cols = collections.defaultdict(list)
    for iid, c in db.execute('select itemID, collectionID from collectionItems'):
        if iid in items: cols[iid].append(cpath(c))
    att = collections.defaultdict(lambda: {'pdfs': [], 'html': []})
    for pid, akey, path, ct in db.execute('select a.parentItemID, i.key, a.path, a.contentType from itemAttachments a join items i on i.itemID=a.itemID where a.parentItemID is not null'):
        if pid in items and path and path.startswith('storage:'):
            p = Z / 'storage' / akey / path[8:]
            if p.exists():
                if ct == 'application/pdf': att[pid]['pdfs'].append(str(p))
                elif ct in ('text/html', 'application/xhtml+xml'): att[pid]['html'].append(str(p))
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True); n = 0
    with open(out, 'w', encoding='utf-8') as f:
        for iid, it in items.items():
            fl = it.pop('f', {}); date = fl.get('date', ''); m = re.search(r'(19|20)\d\d', date)
            doi = (fl.get('DOI') or '').strip().lower() or ((re.search(r'10\.\d{4,9}/[^\s"<>]+', fl.get('extra', '') + ' ' + fl.get('url', '')) or [None])[0] or '').lower()
            arx = re.search(r'arxiv(?:\.org/(?:abs|pdf)/|:)\s*(\d{4}\.\d{4,6})', fl.get('url', '') + ' ' + fl.get('extra', '') + ' ' + doi, re.I)
            f.write(json.dumps({**it, 'title': (fl.get('title') or '').strip(), 'creators': cre.get(iid, []), 'date': date, 'year': m.group(0) if m else '', 'doi': doi, 'url': fl.get('url', ''), 'arxiv': arx.group(1) if arx else '',
                                'publication': fl.get('publicationTitle') or fl.get('proceedingsTitle') or fl.get('repository') or '', 'abstract': (fl.get('abstractNote') or '').strip(), 'tags': tags.get(iid, []), 'collections': cols.get(iid, []),
                                'pdfs': att[iid]['pdfs'], 'html': att[iid]['html']}, ensure_ascii=False) + '\n'); n += 1
        sa = db.execute("select i.key, i.libraryID, a.path, substr(i.dateAdded,1,10) from itemAttachments a join items i on i.itemID=a.itemID where a.parentItemID is null and a.contentType='application/pdf'").fetchall()
        for akey, lib, path, added in sa:
            if path and path.startswith('storage:') and (Z / 'storage' / akey / path[8:]).exists() and lib in libs:
                p = Z / 'storage' / akey / path[8:]; f.write(json.dumps({'key': akey, 'library': libs.get(lib, str(lib)), 'libid': lib, 'type': 'standalone-pdf', 'added': added, 'title': p.stem, 'creators': [], 'date': '', 'year': '', 'doi': '', 'url': '', 'arxiv': '', 'publication': '', 'abstract': '', 'tags': [], 'collections': [], 'pdfs': [str(p)], 'html': []}, ensure_ascii=False) + '\n'); n += 1
    shutil.rmtree(tmp, ignore_errors=True)
    rows = [json.loads(l) for l in open(out)]
    print(f'{n} items written to {out}'); print('by library:', dict(collections.Counter(r['library'] for r in rows)))
    print('with abstract:', sum(1 for r in rows if r['abstract']), '| with PDF on disk:', sum(1 for r in rows if r['pdfs']), '| with HTML snapshot on disk:', sum(1 for r in rows if r['html']), '| with PDF or HTML:', sum(1 for r in rows if r['pdfs'] or r['html']), '| title only:', sum(1 for r in rows if not r['abstract'] and not r['pdfs'] and not r['html']))
if __name__ == '__main__': main()

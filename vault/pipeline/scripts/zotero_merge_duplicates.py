#!/usr/bin/env python3
"""Merge exact-duplicate items in the PERSONAL Zotero library (libraryID 1) according to a plan file; Zotero must be closed (JP, 2026-11-25).
  python3 zotero_merge_duplicates.py PLAN.json [--lib N] [--apply]      (without --apply: validate only; N = Zotero libraryID, default 1 = personal)
Plan entries: {master, others[], trash_attachments[]} (item keys). Per group, inside ONE transaction:
  - the master (newest copy) gains the older copies' child attachments and notes, collections, tags, relations, and any field or creators it lacks;
  - the older copies and the listed identical older PDF attachments go to the Zotero trash (deletedItems), so they can be restored from the trash;
  - every changed item is marked unsynced (synced = 0, new clientDateModified) so Zotero uploads the change at the next sync.
A full backup (sqlite backup API) is written first; the integrity check runs before and after. """
import json, shutil, sqlite3, subprocess, sys, time
from pathlib import Path
Z = Path.home() / 'Zotero' / 'zotero.sqlite'; LIB = int(sys.argv[sys.argv.index('--lib') + 1]) if '--lib' in sys.argv else 1   # 1 = personal library; a group library only with the owner's say-so (and only copies the owner created)
def main():
    plan = json.load(open(sys.argv[1])); apply = '--apply' in sys.argv
    if subprocess.run(['pgrep', '-f', 'Zotero.app/Contents/MacOS/zotero'], capture_output=True).stdout.strip(): sys.exit('Zotero is running: quit it first (Cmd+Q).')
    db = sqlite3.connect(Z, timeout=5); db.execute('pragma foreign_keys=on')
    print('integrity before:', db.execute('pragma integrity_check').fetchone()[0])
    key2id = dict(db.execute('select key, itemID from items where libraryID=?', (LIB,))); typ = dict(db.execute('select itemID, itemTypeID from items'))
    deleted = {r[0] for r in db.execute('select itemID from deletedItems')}; ok = []; bad = 0
    for g in plan:
        ids = [key2id.get(k) for k in [g['master']] + g['others']]
        if None in ids or any(i in deleted for i in ids) or len({typ[i] for i in ids}) > 1: bad += 1; continue
        ok.append({'m': ids[0], 'o': ids[1:], 'att': [key2id[k] for k in g['trash_attachments'] if k in key2id and key2id[k] not in deleted]})
    print(f'plan: {len(plan)} groups, valid {len(ok)}, skipped as changed or invalid {bad}')
    if not apply: return
    bk = Path.home() / 'Zotero-backup-2026-11-25' / f'zotero-before-merge-lib{LIB}.sqlite'; b = sqlite3.connect(bk); db.backup(b); b.close(); print('backup:', bk, round(bk.stat().st_size / 1e6), 'MB')
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()); cnt = {'merged': 0, 'children': 0, 'collections': 0, 'tags': 0, 'fields': 0, 'att_trashed': 0}
    try:
        db.execute('begin')
        touch = lambda i: db.execute('update items set synced=0, clientDateModified=?, dateModified=? where itemID=?', (now, now, i))
        for g in ok:
            m = g['m']
            for o in g['o']:
                for t in ('itemAttachments', 'itemNotes'):
                    cnt['children'] += db.execute(f'select count(*) from {t} where parentItemID=?', (o,)).fetchone()[0]
                    for (c,) in db.execute(f'select itemID from {t} where parentItemID=?', (o,)).fetchall(): touch(c)
                    db.execute(f'update {t} set parentItemID=? where parentItemID=?', (m, o))
                have = {r[0] for r in db.execute('select collectionID from collectionItems where itemID=?', (m,))}
                for (c, ox) in db.execute('select collectionID, orderIndex from collectionItems where itemID=?', (o,)).fetchall():
                    if c not in have: db.execute('insert into collectionItems(collectionID,itemID,orderIndex) values(?,?,?)', (c, m, ox)); have.add(c); cnt['collections'] += 1
                for (tg, ty) in db.execute('select tagID, type from itemTags where itemID=?', (o,)).fetchall():
                    cnt['tags'] += db.execute('insert or ignore into itemTags(itemID,tagID,type) values(?,?,?)', (m, tg, ty)).rowcount
                db.execute('insert or ignore into itemRelations(itemID,predicateID,object) select ?,predicateID,object from itemRelations where itemID=?', (m, o))
                hf = {r[0] for r in db.execute('select fieldID from itemData where itemID=?', (m,))}
                for (f, v) in db.execute('select fieldID, valueID from itemData where itemID=?', (o,)).fetchall():
                    if f not in hf: db.execute('insert into itemData(itemID,fieldID,valueID) values(?,?,?)', (m, f, v)); hf.add(f); cnt['fields'] += 1
                if not db.execute('select 1 from itemCreators where itemID=?', (m,)).fetchone():
                    db.execute('insert into itemCreators(itemID,creatorID,creatorTypeID,orderIndex) select ?,creatorID,creatorTypeID,orderIndex from itemCreators where itemID=?', (m, o))
                db.execute('insert or ignore into deletedItems(itemID,dateDeleted) values(?,?)', (o, now)); touch(o); cnt['merged'] += 1
            touch(m)
            for a in g['att']:
                cnt['att_trashed'] += db.execute('insert or ignore into deletedItems(itemID,dateDeleted) values(?,?)', (a, now)).rowcount; touch(a)
        db.execute('commit')
    except Exception as e:
        db.execute('rollback'); sys.exit(f'ROLLED BACK, nothing changed: {e!r}')
    print('applied:', cnt); print('integrity after:', db.execute('pragma integrity_check').fetchone()[0])
if __name__ == '__main__': main()

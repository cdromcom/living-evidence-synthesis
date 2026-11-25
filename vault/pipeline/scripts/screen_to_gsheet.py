#!/usr/bin/env python3
"""Build the review workbook (.xlsx, opens in Google Sheets) from screen_embed.py and screen_dedup.py output (JP, 2026-11-25).
  python3 screen_to_gsheet.py --result pipeline/misc/screening/screen-result.json --dedup pipeline/misc/screening/dedup.json [--out FILE.xlsx]
Tabs: ABOUT, Papers (one row per distinct paper, with each model's pick and similarity, hints, and JP's decision columns), Piles, New pile candidates, Duplicates (every Zotero record), Seed set, Model check."""
import argparse, collections, json, os, re
from datetime import date
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis')
def authors(c): 
    a = [x for x in c if x]; return '; '.join(a[:3]) + (' et al.' if len(a) > 3 else '')
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--result', required=True); ap.add_argument('--dedup', required=True); ap.add_argument('--out'); a = ap.parse_args()
    R = json.load(open(a.result)); D = json.load(open(a.dedup)); cl = R['clusters']; rep = R['report']
    pile_of = {m: cid for cid, c in cl.items() for m in c['members']}
    def pile_label(p):
        if p['majority'] == 'NEW':
            cid = pile_of.get(p['id']); return f"NEW {cid}: {', '.join(cl[cid]['terms'][:3])}" if cid else 'NEW (no similar paper yet)'
        return p['majority'].replace('  ', ' ')
    names = ['EmbeddingGemma 2', 'harrier-oss-v1-0.6b', 'DNA-VL-STEER-2B']
    copies = collections.defaultdict(lambda: collections.Counter())
    for r in D: copies[r['dup_group']][r['source']] += 1
    rows = []
    for p in R['papers']:
        rec = p['rec']; hints = []
        if rec.get('seed_match'): hints.append('Already in the seed set (not a new paper)')
        if rec.get('in_older_pool'): hints.append(f"Already in the older SysRev-LLMApp pool (added {rec['in_older_pool'][:10]})")
        y = rec.get('year') or ''
        if y and int(y) <= 2022: hints.append('Published 2022 or earlier: check that it involves LLMs')
        if not y: hints.append('Year missing')
        if p['majority'] == 'NEW' and p['id'] not in pile_of: hints.append('Unlike every seed and unlike the other new papers')
        if p['majority'] == 'NEW' and p['id'] in pile_of: hints.append(f"Candidate new pile of {len(cl[pile_of[p['id']]]['members'])} papers")
        if p['mean_best_sim'] < 0.80: hints.append('Low similarity to every seed')
        if p['text_chars'] < 500: hints.append('Little text in the PDF (scanned?)')
        if p['agreement'] != '3 of 3': hints.append('Models split (2 of 3)')
        v = p['votes']; row = [pile_label(p), p['agreement'], pile_of.get(p['id'], ''), p['title'], authors(rec['creators']), y, rec.get('publication', ''), rec.get('doi', ''), rec.get('url', ''), rec['key'], p['pdf'],
                               ', '.join(f'{k.replace("personal library", "personal").replace("OASIS Lab group copy", "group")} x{n}' for k, n in copies[rec['dup_group']].items()) if rec['dup_group'] else '1',
                               rec.get('seed_match', ''), rec.get('in_older_pool', ''), '; '.join(hints)]
        for n in names: x = v[n]; row += [x['pick'].replace('  ', ' '), round(x['sim'], 3), x['second'].replace('  ', ' '), round(x['second_sim'], 3)]
        row += [v[names[0]]['nearest_seed'][:90], (rec.get('abstract') or '')[:1800], '', '', '']
        rows.append((p['mean_best_sim'], row))
    rows.sort(key=lambda x: (x[1][0], -x[0])); rows = [r for _, r in rows]
    piles = sorted({g for p in R['papers'] for g in [p['majority']] if g not in ('NEW', 'no majority')}); seed_groups = R['categories']
    wb = Workbook(); ab = wb.active; ab.title = 'ABOUT'
    hdr = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='2F5D3A'); wrap = Alignment(wrap_text=True, vertical='top')
    def sheet(title, header, data, widths=None, freeze='A2'):
        ws = wb.create_sheet(title); ws.append(header)
        for c in ws[1]: c.font = hdr; c.fill = fill; c.alignment = wrap
        for r in data: ws.append(r)
        for row in ws.iter_rows(min_row=2):
            for c in row: c.alignment = wrap
        ws.freeze_panes = freeze
        for i, w in enumerate(widths or [], 1): ws.column_dimensions[get_column_letter(i)].width = w
        return ws
    cols = ['Proposed pile', 'Models agreeing', 'New pile id', 'Title', 'Authors', 'Year', 'Venue', 'DOI', 'URL', 'Zotero key', 'PDF file', 'Copies in Zotero', 'Matches seed (file)', 'In older pool (added)', 'Screening hints']
    for n in names: s = n.split(' (')[0]; cols += [f'{s}: pile', f'{s}: similarity', f'{s}: 2nd choice', f'{s}: 2nd similarity']
    cols += ['Nearest seed paper (EmbeddingGemma 2)', 'Abstract (Zotero)', 'JP: decision', 'JP: pile', 'JP: notes']
    ws = sheet('Papers', cols, rows, [34, 10, 8, 60, 28, 6, 26, 24, 24, 11, 40, 14, 18, 18, 50] + [18, 9, 18, 9] * 3 + [40, 80, 14, 28, 40], freeze='E2')
    n = len(rows); dv = DataValidation(type='list', formula1='"Include,Exclude,Maybe,Duplicate of another paper"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'{get_column_letter(len(cols) - 2)}2:{get_column_letter(len(cols) - 2)}{n + 1}')
    dv2 = DataValidation(type='list', formula1='"' + ','.join([g.replace('  ', ' ') for g in seed_groups] + list(cl) + ['Other']) + '"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'{get_column_letter(len(cols) - 1)}2:{get_column_letter(len(cols) - 1)}{n + 1}')
    cnt = collections.Counter(r[0] for r in rows); seedcnt = collections.Counter(g for s in R['seeds'] for g in s['groups'])
    sheet('Piles', ['Pile', 'Kind', 'Seed papers (guide)', 'New papers', 'Pile name'], [[g.replace('  ', ' '), 'seed task type', seedcnt.get(g, 0), cnt.get(g.replace('  ', ' '), 0), g] for g in seed_groups] + [[f'NEW {k}', 'candidate new task type', 0, len(c['members']), ', '.join(c['terms'][:4])] for k, c in cl.items()] + [['NEW (no similar paper yet)', 'unclustered', 0, cnt.get('NEW (no similar paper yet)', 0), '']], [44, 24, 16, 12, 60])
    title = {p['id']: p['title'] for p in R['papers']}
    sheet('New pile candidates', ['Pile', 'Most distinctive words', 'Papers', 'Mean similarity inside the pile', 'Member titles'], [[k, ', '.join(c['terms']), len(c['members']), round(c['mean_sim_within'], 3), '\n'.join(title[m] for m in c['members'])] for k, c in cl.items()], [8, 40, 8, 14, 120])
    sheet('Duplicates', ['Group', 'Role', 'Library', 'Zotero key', 'Title', 'Year', 'DOI', 'Has PDF', 'Why grouped'], [[r['dup_group'], r['dup_role'], r['source'], r['key'], r['title'], r['year'], r['doi'], 'yes' if r['pdfs'] else 'no', r['dup_why']] for r in sorted(D, key=lambda r: (r['dup_group'], r['dup_role']))], [8, 24, 22, 11, 70, 6, 28, 8, 24])
    sheet('Seed set', ['Source page', 'PDF file', 'Task group(s)'], [[s['id'], s['pdf'], '; '.join(g.replace('  ', ' ') for g in s['groups'])] for s in R['seeds']], [48, 70, 60])
    mc = [[k, round(v['loo_accuracy'], 3), v['loo_n'], round(v['loo_median_nearest_sim'], 3), round(v['novel_threshold'], 3)] for k, v in rep.items() if k != 'cluster_choice']
    sheet('Model check', ['Model', 'Leave-one-out accuracy on the seeds', 'Seeds tested', 'Median nearest-seed similarity', 'Similarity below which a paper counts as NEW'], mc, [34, 16, 12, 16, 22])
    t = ['What this sheet is', 'Papers from the Zotero collection "SysRev - Elicit 2026-11-24" (personal library) sorted into piles by the task the models perform, using your %d seed papers as the guide. Nothing was deleted, moved or changed in Zotero.' % len(R['seeds']), '',
         'How the piles were made', 'Each paper = title + the first 3 PDF pages. Three embedding models (EmbeddingGemma 2, harrier-oss-v1-0.6b, DNA-VL-STEER-2B) each give a paper the task group of its most similar seed paper, or NEW if no seed is similar enough (below that model\'s 15th percentile of seed-to-seed similarity). A pile needs 2 of 3 models to agree. Papers voted NEW are clustered with each other (average linkage on the mean of the three models\' distances) to suggest new task types.', '',
         'How reliable', 'Leave-one-out on the seeds (each seed hidden, then classified from the others): see the Model check tab. With few seeds per task type (one has a single seed) this is a rough guide only.', '',
         'Scope', f'{len(D)} Zotero records (personal %d, group copy %d) = {len(R["papers"])} distinct papers; each appears about 4 times. The older SysRev-LLMApp pool is checked for overlap, not screened here.' % (sum(1 for r in D if r['source'] == 'personal library'), sum(1 for r in D if r['source'] != 'personal library')), '',
         'Caveats', 'DNA-VL-STEER-2B (Korean developer, Qwen base) is allowed because it is open-weight, local and near state of the art; no foreign API is used. Drop any model and rerun to see how the vote changes. Hints are suggestions, not decisions. E-means (a fast k-means for huge datasets) was not used: with this few papers ordinary clustering is instant and E-means still needs the number of clusters.', '',
         'To review', 'Use the Papers tab: filter by Proposed pile or Screening hints, then fill JP: decision and JP: pile. Duplicates tab lists every Zotero record; "keep (preferred)" is the published or newest version.', '', 'Built', str(date.today())]
    for i in range(0, len(t), 3): ab.append([t[i], t[i + 1] if i + 1 < len(t) else '']); 
    for r in ab.iter_rows():
        r[0].font = Font(bold=True); r[0].alignment = wrap; r[1].alignment = wrap
    ab.column_dimensions['A'].width = 24; ab.column_dimensions['B'].width = 140
    out = Path(a.out or Path(a.result).parent / 'screening-review.xlsx'); wb.save(out); print('wrote', out, '| papers', n)
    # metadata-only summary for the vault (no abstracts, no local paths)
    import csv
    tsv = VAULT / 'pipeline/misc/screening' / f'{date.today()}-screening-summary.tsv'; tsv.parent.mkdir(parents=True, exist_ok=True)
    keep = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14] + list(range(15, 27))
    with open(tsv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow([cols[i] for i in keep]); [w.writerow([r[i] for i in keep]) for r in rows]
    print('wrote', tsv)
if __name__ == '__main__': main()

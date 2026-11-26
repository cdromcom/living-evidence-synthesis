#!/usr/bin/env python3
"""Build the Stage 2 whole-library screening workbook from ~/.cache/lives-bench/screening/all/result.json (JP, 2026-11-25).
  python3 screen_all_to_gsheet.py [--out FILE]      (needs the new-category names file in pipeline/screening/<run>/data/ when new categories exist)
Tabs: ABOUT, Papers, Categories, New category candidates, Lists, Seed set, Model check. 'PDF on disk' and 'HTML snapshot on disk' are real booleans (the sheet turns them into checkboxes)."""
import argparse, collections, json, os, re, sys, unicodedata
from pathlib import Path
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
import sheet_style as SS
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
sys.path.insert(0, str(Path(__file__).resolve().parent)); from screen_to_gsheet import keywords
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis'); RUN = '2026-11-25_Zotero-all-libraries'; GH = 'https://github.com/cdromcom/living-evidence-synthesis'
def gh(p, d=False): return f"{GH}/{'tree' if d else 'blob'}/main/vault/{p}"
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default=str(Path.home() / '.cache/lives-bench/screening/all/stage2-all-zotero.xlsx')); ap.add_argument('--stats-json', default=''); ap.add_argument('--only-new', default='', help='file of stable ids already in the sheet (one per line): build only the rows that are not there yet, ready to append; the repo data files are left alone'); a = ap.parse_args()
    W = Path.home() / '.cache/lives-bench/screening/all'; R = json.load(open(W / 'result.json')); prep = json.load(open(W / 'prepare-stats.json')); rep = R['report']; cats = R['categories']; cl = R['clusters']
    run = VAULT / 'pipeline/screening' / RUN; (run / 'data').mkdir(parents=True, exist_ok=True)
    seed_names = json.load(open(VAULT / 'pipeline/screening/shared/seed-task-groups_names-and-task-types.json')); nf = run / 'data/new-category-names_and-task-types.json'; new_names = json.load(open(nf)) if nf.exists() else {}
    stat = json.load(open(a.stats_json)) if a.stats_json else {}
    category_of = {m: c for c, v in cl.items() for m in v['members']}; sid = lambda c: 'S' + str(cats.index(c) + 1)
    known = set(Path(a.only_new).read_text().split()) if a.only_new else None
    def info(p):
        if known is not None and p['majority'] in ('NEW', 'no majority'): return 'U', 'Unsorted: new since the last sort', 'Place by hand, or wait for the next full sort'   # new papers are not forced into the old new-category numbering
        if p['majority'] in ('NEW', 'no majority'):
            c = category_of.get(p['id'], 'unclustered'); n = new_names.get(c, {'name': c if c != 'unclustered' else 'Unclustered (unlike every seed)', 'task_type': ''}); return c, n['name'], n['task_type']
        g = seed_names.get(p['majority'], {'name': p['majority'], 'task_type': ''}); return sid(p['majority']), g['name'], g['task_type']
    names = list(next(iter(R['papers']))['votes'].keys()) if R['papers'] and 'votes' in R['papers'][0] else []
    P = [p for p in R['papers'] if 'votes' in p and (known is None or p['keys'][0] not in known)]
    txt = {p['id']: f"{p['title']}. {p['text']}" for p in P}; by = collections.defaultdict(list)
    for p in P:
        by[info(p)[0]].append(txt[p['id']])
    for s in R['seeds']:
        for g in s['groups']: by[sid(g)].append(s['title'])
    oa = json.load(open(W / 'oa.json')) if (W / 'oa.json').exists() else {}; get_oa = lambda d: oa.get((d or '').lower().replace('https://doi.org/', ''), {})
    kw = keywords(by, list(txt.values()) + [s['title'] for s in R['seeds']])
    wb = Workbook(); wb.remove(wb.active); hdr = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='2F5D3A'); wrap = Alignment(wrap_text=True, vertical='top'); link = Font(name=SS.FONT_BODY, size=SS.SIZE, color='0B5CAD')   # blue, no underline (Butterick)
    def tab(title, header, rows, widths):
        ws = wb.create_sheet(title); ws.append(header)
        for r in rows: ws.append([ILLEGAL_CHARACTERS_RE.sub('', x) if isinstance(x, str) else x for x in r])   # text taken from PDFs can hold control characters that spreadsheets refuse
        jp = next((i + 1 for i, h in enumerate(header) if str(h).startswith('JP')), None)
        SS.polish(ws, jp_from=jp, max_lines=4 if title == 'Papers' else 8); ws.freeze_panes = 'B2'; return ws
    rows = []; GREEN = []; SORTV = []; tau = rep['relevance_threshold']; dna = next((n for n in names if n.startswith('DNA')), names[-1])   # DNA-VL-STEER-2B did best on the seed test, so it also ranks the screening list
    for p in P:
        pid, pname, ptask = info(p); v = p['votes']; hints = []
        if p.get('seed_match'): hints.append('Already in the seed set (not a new paper)')
        if not p['sets']: hints.append('Not in an ingest folder: found because it is close to the seed and Elicit papers')
        if p['year'] and int(p['year']) <= 2022: hints.append('Published 2022 or earlier: check that it involves LLMs')
        if p['text_source'] == 'title only': hints.append('Title only: no abstract, PDF text or HTML')
        if p['agreement'] != f'{len(names)} of {len(names)}': hints.append('Models split')
        if pid == 'unclustered': hints.append('Unlike every seed and unlike the other new papers')
        dna_yes = p['relevance'][dna] >= tau[dna]; screen = '' if p.get('seed_match') else ('Screen first: all 3 models' if p['relevant_votes'] == len(names) else ('Screen: 2 of 3 models or DNA-VL-STEER-2B' if (p['relevant_votes'] >= 2 or dna_yes) else '')); GREEN.append(bool(screen))
        row = [pname + (' (new)' if p['majority'] in ('NEW', 'no majority') and pid != 'unclustered' else ''), ptask, pid, screen, p['agreement'], 'yes' if p['relevant'] else 'no', p['relevant_votes'], p['title'], (p.get('text') or '')[:1800], '; '.join(p['authors']), p['year'], p['publication'], p['doi'], p['url'], '; '.join(p['sets']) or '(other folder)',
               ' | '.join(p['collections'])[:300], ', '.join(p['libraries']), p['copies'], p['text_source'], bool(get_oa(p['doi']).get('oa')), get_oa(p['doi']).get('url', '') if get_oa(p['doi']).get('oa') else ('no DOI: not checked' if not p['doi'] else ''), bool(p['pdf_on_disk']), bool(p['html_on_disk']), p.get('seed_match', ''), '; '.join(hints)]
        for n in names: x = v[n]; row += [x['pick'], round(x['sim'], 3), x['best_group'], round(x['second_sim'], 3)]
        row += [round(float(np.mean(list(p['relevance'].values()))), 3), '', '', '', p['keys'][0]]; rows.append(row); SORTV.append(p['relevance'][dna])   # the last column is the stable id (Zotero library:key), the key for merging JP's labels
    order = sorted(range(len(rows)), key=lambda i: (0 if GREEN[i] else 1, 0 if rows[i][3].startswith('Screen first') else 1, -SORTV[i]) if GREEN[i] else (1, 2, rows[i][0], -rows[i][-5]))   # screening rows first (3 of 3 models, then the rest, best DNA similarity first), then everything else by category
    rows = [rows[i] for i in order]; GREEN = [GREEN[i] for i in order]
    header = ['Category', 'Task type', 'Category id', 'Screen this? (suggested)', 'Models agreeing', 'Close to the seed and Elicit papers? (any model)', 'Models saying yes', 'Title', 'Abstract (or the text used)', 'Authors', 'Year', 'Venue', 'DOI', 'URL', 'Ingest set', 'Zotero folders', 'Zotero libraries', 'Zotero records merged', 'Text embedded', 'Open access (checkbox)', 'Open-access link', 'PDF on disk (checkbox)', 'HTML snapshot on disk (checkbox)', 'Already in the vault seed set', 'Hints'] \
        + [f'{n}: {w}' for n in names for w in ('pick', 'similarity', 'best category', '2nd similarity')] + ['Mean similarity to seed and Elicit papers', 'JP: decision', 'JP: category', 'JP: notes', 'Stable id (Zotero library:key)']
    ws = tab('Papers', header, rows, [30, 34, 8, 24, 9, 10, 8, 60, 90, 28, 6, 24, 24, 30, 22, 40, 18, 8, 16, 10, 30, 10, 10, 24, 40] + [12, 8, 22, 8] * len(names) + [10, 14, 20, 30, 26])
    ws.auto_filter.ref = ws.dimensions; lightgreen = PatternFill('solid', fgColor='E2F0D9'); ci = {h: i + 1 for i, h in enumerate(header)}   # light green marks the rows JP should screen for include or exclude
    for r in range(2, ws.max_row + 1):
        green = GREEN[r - 2]
        if green:
            for c in range(1, len(header) + 1): ws.cell(r, c).fill = lightgreen
        u = ws.cell(r, ci['URL'])
        if u.value and str(u.value).startswith('http'): u.font = link; u.hyperlink = u.value
    print('rows to screen (light green):', sum(GREEN), 'of', len(GREEN)); print('column positions (1-based):', {k: ci[k] for k in ('Screen this? (suggested)', 'Open access (checkbox)', 'PDF on disk (checkbox)', 'HTML snapshot on disk (checkbox)', 'JP: decision', 'JP: category', 'JP: notes', 'Stable id (Zotero library:key)')})
    # categories
    pr = []; cnt = collections.Counter(info(p)[0] for p in P); seedn = collections.Counter(sid(g) for s in R['seeds'] for g in s['groups'])
    for c in cats: pr.append([seed_names.get(c, {}).get('name', c), seed_names.get(c, {}).get('task_type', ''), 'Seed category', sid(c), seedn[sid(c)], cnt[sid(c)], ', '.join(kw.get(sid(c), []))])
    for c in cl: pr.append([new_names.get(c, {}).get('name', c), new_names.get(c, {}).get('task_type', ''), 'New category candidate', c, 0, cnt[c], ', '.join(kw.get(c, []))])
    pr.append(['Unclustered (unlike every seed)', '', 'Unclustered', 'unclustered', 0, cnt['unclustered'], ''])
    tab('Categories', ['Category', 'Task type', 'Kind', 'Category id', 'Seed papers', 'New papers', 'Top 7 keywords (TF-IDF)'], pr, [38, 44, 18, 10, 10, 10, 60])
    nr = [[(new_names.get(category_of[p['id']], {}).get('name', category_of[p['id']])), category_of[p['id']], p['title'], p['year'], p['doi'], '; '.join(p['sets'])] for p in P if p['id'] in category_of]
    nr.sort(key=lambda r: (r[1], r[2])); tab('New category candidates', ['Category', 'Category id', 'Paper (one per row)', 'Year', 'DOI', 'Ingest set'], nr, [38, 8, 80, 6, 26, 24])
    ls = wb.create_sheet('Lists'); ls.append(['Category choices']); [ls.append([r[0]]) for r in pr]; ls.append(['Not relevant']); ls.append(['Other / unsure']); ls.append(['Unsorted: new since the last sort'])
    dv = DataValidation(type='list', formula1=f"=Lists!$A$2:$A${ls.max_row}", allow_blank=True); ws.add_data_validation(dv); jp = header.index('JP: category') + 1; dv.add(f'{get_column_letter(jp)}2:{get_column_letter(jp)}{ws.max_row}')
    dv2 = DataValidation(type='list', formula1='"include,exclude,unsure"', allow_blank=True); ws.add_data_validation(dv2); jd = header.index('JP: decision') + 1; dv2.add(f'{get_column_letter(jd)}2:{get_column_letter(jd)}{ws.max_row}')
    tab('Seed set', ['Id', 'Seed paper (title)', 'Task groups'], [[s['id'], s['title'], '; '.join(s['groups'])] for s in R['seeds']], [8, 90, 60])
    mc = [[n, rep['category_loo_by_model'][n]['accuracy'], rep['category_loo_by_model'][n]['n'], rep['novel_threshold'][n], rep['relevance_threshold'][n]] for n in names]
    mc.append(['Majority of the models', rep['category_loo_majority']['accuracy'], rep['category_loo_majority']['n'], '', ''])
    tab('Model check', ['Model', 'Category leave-one-out accuracy on seeds', 'Seeds tested', 'New-category threshold (15th percentile of seed nearest similarity)', 'Relevance threshold (10th percentile of reference papers)'], mc, [30, 18, 10, 30, 30])
    ab = wb.create_sheet('ABOUT', 0); ab.append(['Item', 'What was done', 'Links'])
    rp = rep.get('relevance_proxy', {}); cc = R['counts']
    abt = [('Title', 'LIVES Stage 2 ingest: screening of every item in all Zotero libraries against the 27-paper seed set and the Elicit 2026-11-24 papers (reported in the style of TRIPOD+LLM; generation items are not applicable because the models only embed text)', gh(f'pipeline/screening/{RUN}/README.md')),
           ('Data source', f"Read-only copy of the Zotero database: {prep['items']:,} regular items and standalone PDFs in {len(prep['by_library'])} libraries; {prep['distinct']:,} distinct papers after merging duplicates (same DOI, arXiv id or near-identical title). Ingest sets: " + '; '.join(f'{k} {v}' for k, v in cc['ingest_sets'].items()) + '.', gh('pipeline/scripts/zotero_inventory.py')),
           ('Text embedded', 'Title plus the Zotero abstract; if none, the abstract section of a PDF on disk; if none, the text of an HTML snapshot on disk; otherwise the title alone (at most 1,800 characters). Counts: ' + ', '.join(f'{k} {v:,}' for k, v in prep['text_sources'].items()) + '. The Open access checkbox comes from OpenAlex (a free full-text copy exists; papers without a DOI are not checked) and links to that copy. The PDF and HTML checkboxes say whether a file is on disk in your Zotero.', gh('pipeline/scripts/screen_all.py')),
           ('Models', 'EmbeddingGemma 2, harrier-oss-v1-0.6b and DNA-VL-STEER-2B, all local open-weight models; no API calls. Each paper gets a vote from each model; the majority of three decides.', gh('pipeline/skills/Tools-and-Models.md')),
           ('Step 1: relevance', f"A paper is marked close to the seed and Elicit papers when its highest cosine similarity to the {rep['n_reference']} reference papers (27 seeds, Elicit 2026-11-24, Include-CA-Rep) is above the 10th percentile of how similar the reference papers are to each other, in ANY one of the 3 models (chosen on purpose to favor false positives, since JP reviews every row but would not find a missed paper). The 'Models saying yes' column shows how many of the 3 agreed.", gh('pipeline/scripts/screen_all.py')),
           ('Step 2: categories', f"Each target paper gets the task group of the most similar seed paper in each model, or NEW if below that model's 15th percentile of seed-to-seed nearest similarity. Majority of 3 decides. NEW papers are clustered (Ward linkage on the joined embeddings of the 3 models; 15 to 30 clusters, best silhouette); clusters of 3 or more become new category candidates. Names and task types were written by Claude Sonnet 5.5 and are not yet checked by JP.", gh('pipeline/scripts/screen_all.py')),
           ('Accuracy (expected)', f"Category assignment, leave-one-out on the {rep['category_loo_majority']['n']} seeds, majority of models: {rep['category_loo_majority']['accuracy']:.0%}. " + (f"Relevance, proxy labels (positives: {rp['positives_n']} reference papers left out one at a time; negatives: {rp['negatives_proxy'] if 'negatives_proxy' in rp else rp['negatives_n']} papers from clearly unrelated collections): sensitivity {rp['sensitivity']:.0%}, specificity {rp['specificity']:.0%}, balanced accuracy {rp['balanced_accuracy']:.0%}" + (f", AUC {rp['auc']:.2f}" if 'auc' in rp else '') + '. These are proxy labels, not your decisions; accuracy on your real include/exclude calls is unknown until you fill the JP columns.' if rp else ''), ''),
           ('Time and cost', stat.get('time', 'See the README.') + ' ' + stat.get('cost', ''), ''),
           ('What to screen', f"Screen the {sum(GREEN)} light green rows at the top of the Papers tab, not all {len(GREEN)}. A row is light green when all three models call it close to the seed and Elicit papers (Screen first), or two of three do, or DNA-VL-STEER-2B does (it scored best on the seed test). Within each group rows are sorted by DNA-VL-STEER-2B similarity. White rows are listed for completeness. The Abstract column is the Zotero abstract, or the start of the PDF or web page when Zotero has none.", ''),
           ('Adding new papers', 'New Zotero papers are screened the same way and appended as new rows at the bottom, so labels stay where they are (column Stable id). New papers that the models call NEW show as "Unsorted: new since the last sort" until the next full sort. Steps: pipeline/screening/README.md.', gh('pipeline/screening/README.md')),
           ('Limits', 'Embedding similarity is not a judgment of relevance; title-only papers are weakly placed; abstracts can be wrong in Zotero. Every row needs your decision (JP columns). Nothing was deleted or merged in Zotero.', ''),
           ('Code and data on GitHub', f'Metadata-only data files and the README are in pipeline/screening/{RUN}/ (local file paths are left out of the public repo; at JP's request, 2026-11-26, the whole-library table including abstracts is in the repo too). Links work once the pull request is merged.', gh(f'pipeline/screening/{RUN}', True))]
    for it, tx, ln in abt:
        ab.append([it, tx, ln]); r = ab.max_row
        if ln: ab.cell(r, 3).hyperlink = ln
    SS.polish_about(ab)
    for r in range(2, ab.max_row + 1):
        if ab.cell(r, 3).hyperlink: ab.cell(r, 3).font = link
    wb.save(a.out); print('saved', a.out, '| papers rows', len(rows), '| categories', len(pr))
    if known is not None: print('only-new mode: the repo data files were not touched'); return
    # metadata-only files for the repo
    import csv
    with open(run / 'data/papers_categories-and-model-votes.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow([h for h in header if not h.startswith('JP:')]); [w.writerow([c if not isinstance(c, str) else c.replace('\t', ' ') for c in r[:len(header) - 4] + [r[-1]]]) for r in rows]
    json.dump({'report': rep, 'counts': cc, 'prepare': prep, 'models': names}, open(run / 'data/settings_and_results.json', 'w'), indent=1, default=float)
if __name__ == '__main__': main()

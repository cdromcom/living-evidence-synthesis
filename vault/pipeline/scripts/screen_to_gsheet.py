#!/usr/bin/env python3
"""Build the review workbook (.xlsx, opens in Google Sheets) AND the tidy GitHub folder for one screening run (JP, 2026-11-25).
  ~/.cache/lives-bench/venv-embed/bin/python screen_to_gsheet.py --result RESULT.json --dedup DEDUP.json --run-dir 2026-11-25_SysRev-Elicit-2026-11-24 --collection "SysRev - Elicit 2026-11-24" [--text-mode pdf|abstract] [--other-label "In the older pool (added)"]
Writes (metadata only: no abstracts, no local paths) to pipeline/screening/<run-dir>/: README.md (TRIPOD-LLM-style report) and data/*.tsv|json. Reads data/new-category-names_and-task-types.json (hand-written names for the new categories).
Workbook tabs: ABOUT, Papers, Categories, New category candidates (one paper per row), Duplicates (struck through = duplicate within its folder), Folder dedup, Seed set, Model check, Lists."""
import argparse, collections, csv, importlib.metadata as md, json, os, re
from datetime import date
from pathlib import Path
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
import sheet_style as SS
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis')
GH = 'https://github.com/cdromcom/living-evidence-synthesis'
def gh_file(p): return f'{GH}/blob/main/vault/{p}'
def gh_dir(p): return f'{GH}/tree/main/vault/{p}'
def authors(c): a = [x for x in c if x]; return '; '.join(a[:3]) + (' et al.' if len(a) > 3 else '')
import unicodedata
GENERIC = {'zero', 'shot', 'few', 'inter', 'abstracts', 'journal', 'articles', 'llm', 'llms', 'language', 'model', 'models', 'large', 'paper', 'papers', 'study', 'using', 'based', 'use', 'used', 'results', 'research', 'scientific', 'approach', 'method', 'methods', 'show', 'propose', 'new', 'also', 'work', 'analysis'}
def keywords(texts_by_category, all_texts, k=7):
    from sklearn.feature_extraction.text import TfidfVectorizer
    norm = lambda t: unicodedata.normalize('NFKC', t).lower()
    all_texts = [norm(t) for t in all_texts]; texts_by_category = {k: [norm(t) for t in v] for k, v in texts_by_category.items()}
    v = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=2, max_df=0.5, sublinear_tf=True, token_pattern=r'(?u)\b[a-z][a-z\-]{2,}\b'); X = v.fit_transform(all_texts); terms = np.array(v.get_feature_names_out()); pos = {t: i for i, t in enumerate(all_texts)}
    out = {}
    for category, tx in texts_by_category.items():
        if not tx: out[category] = []; continue
        w = np.asarray(X[[pos[t] for t in tx]].mean(axis=0)).ravel(); picked = []
        for j in np.argsort(-w):
            t = terms[j]
            if w[j] <= 0 or any(g in GENERIC for g in t.split()): continue
            if any(t in p or p in t for p in picked): continue
            picked.append(t)
            if len(picked) == k: break
        out[category] = picked
    return out
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--result', required=True); ap.add_argument('--dedup', required=True); ap.add_argument('--run-dir', required=True); ap.add_argument('--collection', required=True)
    ap.add_argument('--other-label', default='In the other set (added)'); ap.add_argument('--text-mode', default='pdf'); ap.add_argument('--out'); a = ap.parse_args()
    R = json.load(open(a.result)); D = json.load(open(a.dedup)); cl = R['clusters']; rep = R['report']
    run = VAULT / 'pipeline/screening' / a.run_dir; (run / 'data').mkdir(parents=True, exist_ok=True); runrel = f'pipeline/screening/{a.run_dir}'
    seed_names = json.load(open(VAULT / 'pipeline/screening/shared/seed-task-groups_names-and-task-types.json')); new_names = json.load(open(run / 'data/new-category-names_and-task-types.json'))
    category_of = {m: cid for cid, c in cl.items() for m in c['members']}; clean = lambda n: n.replace(' (test-only)', ''); names = list(R['papers'][0]['votes'].keys())
    def info(p):   # (category id, category name, task type)
        if p['majority'] == 'NEW':
            cid = category_of.get(p['id'], 'unclustered'); n = new_names.get(cid, {'name': cid, 'task_type': ''}); return cid, n['name'], n['task_type']
        g = seed_names.get(p['majority'], {'name': p['majority'], 'task_type': ''}); return 'S' + str(R['categories'].index(p['majority']) + 1) if p['majority'] in R['categories'] else '', g['name'], g['task_type']
    # ----- keywords per category (title + Zotero abstract; seeds: title)
    paper_text = {p['id']: f"{p['title']}. {p['rec'].get('abstract') or ''}" for p in R['papers']}; seed_text = {s['id']: s['title'] for s in R['seeds']}
    by_category = collections.defaultdict(list)
    for p in R['papers']:
        pid, name, _ = info(p); by_category[pid].append(paper_text[p['id']])
    for s in R['seeds']:
        for g in s['groups']: by_category['S' + str(R['categories'].index(g) + 1)].append(seed_text[s['id']])
    kw = keywords(by_category, list(paper_text.values()) + list(seed_text.values()))
    copies = collections.defaultdict(collections.Counter)
    for r in D: copies[r['dup_group']][r['source']] += 1
    rows = []
    for p in R['papers']:
        rec = p['rec']; pid, pname, ptask = info(p); hints = []
        if rec.get('seed_match'): hints.append('Already in the seed set (not a new paper)')
        if rec.get('in_older_pool'): hints.append(f"Already in {a.other_label.replace('In ', '', 1)} (added {rec['in_older_pool'][:10]})")
        y = rec.get('year') or ''
        if y and int(y) <= 2022: hints.append('Published 2022 or earlier: check that it involves LLMs')
        if not y: hints.append('Year missing')
        if not re.search(r'[A-Za-z]{4,} [A-Za-z]{3,}', p['title']) or '@' in p['title']: hints.append('Title looks wrong in Zotero (check the record)')
        if p['majority'] == 'NEW' and pid == 'unclustered': hints.append('Unlike every seed and unlike the other new papers')
        if p['majority'] == 'NEW' and pid != 'unclustered': hints.append(f"Candidate new category of {len(cl[pid]['members'])} papers")
        if p['mean_best_sim'] < 0.80: hints.append('Low similarity to every seed')
        if p['text_chars'] < 500: hints.append('Little text to embed (check the PDF or abstract)')
        if p['agreement'] != '3 of 3': hints.append('Models split (2 of 3)')
        v = p['votes']; row = [pname + (' (new)' if p['majority'] == 'NEW' and pid != 'unclustered' else ''), ptask, pid, p['agreement'], p['title'], authors(rec['creators']), y, rec.get('publication', ''), rec.get('doi', ''), rec.get('url', ''), rec['key'], p['pdf'],
                               ', '.join(f'{k.replace("personal library", "personal").replace("OASIS Lab group copy", "group")} x{n}' for k, n in copies[rec['dup_group']].items()) if rec['dup_group'] else '1', rec.get('seed_match', ''), rec.get('in_older_pool', ''), '; '.join(hints)]
        for n in names:
            x = v[n]; row += [(x['pick'] if x['pick'] != 'NEW' else 'NEW').replace('  ', ' '), round(x['sim'], 3), x['best_group'].replace('  ', ' '), round(x['second_sim'], 3)]
        row += [v[names[0]]['nearest_seed'][:90], (rec.get('abstract') or '')[:1800], '', '', '']; rows.append((p['mean_best_sim'], row))
    rows.sort(key=lambda x: (x[1][0], -x[0])); rows = [r for _, r in rows]
    # ----- workbook
    wb = Workbook(); ab = wb.active; ab.title = 'ABOUT'
    hdr = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='2F5D3A'); wrap = Alignment(wrap_text=True, vertical='top'); link = Font(name='Google Sans', size=10, color='0B5CAD')   # blue, no underline (Butterick)
    def sheet(title, header, data, widths=None, freeze='A2'):
        ws = wb.create_sheet(title); ws.append(header)
        for r in data: ws.append(r)
        SS.polish(ws, jp_from=next((i + 1 for i, h in enumerate(header) if str(h).startswith('JP')), None), max_lines=4 if title == 'Papers' else 8); ws.freeze_panes = freeze
        return ws
    cols = ['Proposed category', 'Task type', 'Category id', 'Models agreeing', 'Title', 'Authors', 'Year', 'Venue', 'DOI', 'URL', 'Zotero key', 'PDF file', 'Copies in Zotero', 'Matches seed (file)', a.other_label, 'Screening hints']
    for n in names: s = clean(n).split(' (')[0]; cols += [f'{s}: category', f'{s}: similarity', f'{s}: best seed group', f'{s}: 2nd similarity']
    cols += ['Nearest seed paper (first model)', 'Abstract (Zotero)', 'JP: decision', 'JP: category', 'JP: notes']
    ws = sheet('Papers', cols, rows, [34, 34, 8, 10, 60, 28, 6, 26, 24, 24, 11, 40, 14, 18, 18, 50] + [18, 9, 22, 9] * len(names) + [40, 80, 14, 34, 40], freeze='E2')
    n = len(rows)
    # categories
    category_rows = []
    cnt = collections.Counter(); 
    for p in R['papers']:
        pid, pname, _ = info(p); cnt[pid] += 1
    for i, g in enumerate(R['categories'], 1):
        s = seed_names.get(g, {'name': g, 'task_type': ''}); category_rows.append([s['name'], s['task_type'], 'seed task type', f'S{i}', sum(1 for x in R['seeds'] if g in x['groups']), cnt.get(f'S{i}', 0), ', '.join(kw.get(f'S{i}', []))])
    for cid in list(cl) + ['unclustered']:
        s = new_names.get(cid, {'name': cid, 'task_type': ''}); category_rows.append([s['name'], s['task_type'], 'candidate new task type' if cid != 'unclustered' else 'unclustered', cid, 0, cnt.get(cid, len(cl[cid]['members']) if cid in cl else 0), ', '.join(kw.get(cid, []))])
    sheet('Categories', ['Category', 'Task type', 'Kind', 'Category id', 'Seed papers (guide)', 'New papers', 'Top 7 keywords (from titles and abstracts)'], category_rows, [40, 52, 22, 9, 14, 11, 70])
    sheet('Lists', ['Category names (for the dropdown)'], [[r[0]] for r in category_rows] + [['Other']], [50]); lw = wb['Lists']
    dv = DataValidation(type='list', formula1='"Include,Exclude,Maybe,Duplicate of another paper"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'{get_column_letter(len(cols) - 2)}2:{get_column_letter(len(cols) - 2)}{n + 1}')
    dv2 = DataValidation(type='list', formula1=f"=Lists!$A$2:$A${len(category_rows) + 2}", allow_blank=True); ws.add_data_validation(dv2); dv2.add(f'{get_column_letter(len(cols) - 1)}2:{get_column_letter(len(cols) - 1)}{n + 1}')
    # new category candidates: one paper per row
    P = {p['id']: p for p in R['papers']}; npc = []
    for cid, c in cl.items():
        nm = new_names.get(cid, {'name': cid, 'task_type': ''})
        for m in c['members']:
            p = P[m]; npc.append([cid, nm['name'], nm['task_type'], ', '.join(kw.get(cid, [])), p['title'], p['rec'].get('year') or '', authors(p['rec']['creators']), p['rec']['key'], p['rec'].get('doi', ''), p['agreement']])
    sheet('New category candidates', ['Category id', 'Category', 'Task type', 'Top 7 keywords', 'Paper title', 'Year', 'Authors', 'Zotero key', 'DOI', 'Models agreeing'], npc, [8, 36, 44, 56, 80, 6, 30, 11, 26, 10])
    drows = sorted(D, key=lambda r: (r['source'], r.get('folder_group') or 'zzz' + r['key'], r.get('folder_role') or ''))
    dws = sheet('Duplicates', ['Folder (Zotero library copy)', 'Within this folder', 'Group in this folder', 'Zotero key', 'Title', 'Year', 'DOI', 'Has PDF', 'Why grouped', 'Across both folders: group', 'Across both folders: role'],
                [[r['source'], r.get('folder_role', ''), r.get('folder_group', ''), r['key'], r['title'], r['year'], r['doi'], 'yes' if r['pdfs'] else 'no', r['dup_why'], r['dup_group'], r['dup_role']] for r in drows], [24, 30, 12, 11, 70, 6, 28, 8, 24, 12, 26])
    for i, r in enumerate(drows, 2):   # a duplicate record within its own folder is struck through
        if r.get('folder_role') == 'duplicate within this folder':
            for c in dws[i]: c.font = Font(strike=True)
    fsum = []
    for src in sorted({r['source'] for r in D}):
        recs = [r for r in D if r['source'] == src]; dups = sum(1 for r in recs if r.get('folder_role') == 'duplicate within this folder')
        fsum.append([a.collection + ' / ' + src, len(recs), len(recs) - dups, dups, f'{100 * dups / max(len(recs), 1):.0f}%'])
    sheet('Folder dedup', ['Folder', 'Zotero records', 'Distinct papers', 'Duplicate records (struck through on the Duplicates tab)', 'Share duplicate'], fsum, [60, 16, 16, 30, 14])
    sheet('Seed set', ['Source page', 'PDF file', 'Task group(s)'], [[s['id'], s['pdf'], '; '.join(seed_names.get(g, {'name': g})['name'] for g in s['groups'])] for s in R['seeds']], [48, 70, 60])
    mc = [[clean(k), round(v['loo_accuracy'], 3), v['loo_n'], round(v['loo_median_nearest_sim'], 3), round(v['novel_threshold'], 3)] for k, v in rep.items() if k != 'cluster_choice']
    sheet('Model check', ['Model', 'Leave-one-out accuracy on the seeds', 'Seeds tested', 'Median nearest-seed similarity', 'Similarity below which a paper counts as NEW'], mc, [34, 16, 12, 16, 22])
    # ----- the report (ABOUT tab and README.md share it): TRIPOD+LLM-style items
    pers = sum(1 for r in D if r['source'] == 'personal library'); grp = len(D) - pers; modes = {'abstract': 'title + abstract (at most 1,800 characters; for seed papers the abstract section of the PDF)', 'pdf': 'title + the first 3 PDF pages (at most 6,000 characters)'}[a.text_mode]
    dd = {s: sum(1 for r in D if r['source'] == s and r.get('folder_role') == 'duplicate within this folder') for s in sorted({r['source'] for r in D})}
    mcs = '; '.join(f"{clean(k)} {100 * v['loo_accuracy']:.0f}%" for k, v in rep.items() if k != 'cluster_choice'); cc = rep.get('cluster_choice') or {}
    S = lambda p: gh_file('pipeline/scripts/' + p); F = lambda p: gh_dir(runrel + '/' + p) if p else gh_dir(runrel)
    items = [
     ('Reporting guideline', 'TRIPOD+LLM (Gallifant et al.), applied as far as it fits: the models here only embed text (no text is generated, no prompts or fine-tuning), so items about generation and prompting are marked not applicable.', [('TRIPOD+LLM statement', 'https://www.tripod-statement.org/tripod-llm/')]),
     ('1. Title and purpose', f'Screening papers in the Zotero collection "{a.collection}" into task-type categories, guided by the {len(R["seeds"])} seed papers; run {a.run_dir}. Purpose: help JP decide which incoming papers to include in the living synthesis and which task types exist.', [('This run on GitHub', F(''))]),
     ('2. Objectives', 'Assign each distinct paper to one of the seed task types, or to a new candidate task type; flag duplicates and papers already seen. Nothing in Zotero was changed.', []),
     ('3. Data source and population', f'Zotero collection "{a.collection}": personal library ({pers} records) and the OASIS Lab group copy ({grp} records), exported from a copy of zotero.sqlite on {date.today()}. After de-duplication: {len(R["papers"])} distinct papers. The collection is the output of an Elicit search imported on 2026-11-24 (not a sample). Seed set: {len(R["seeds"])} papers already in the vault, grouped into {len(R["categories"])} task types by the Review-Arena sections.', [('Seed papers and task groups', gh_file('pipeline/screening/shared/seed-papers_task-groups.json')), ('Export script', S('zotero_collection.py'))]),
     ('4. De-duplication', f'Records match when they share a DOI or arXiv id, have the same normalized title, or have a title similarity of at least 0.90 (a preprint and its journal version). Done inside each folder on its own, across the two library copies, against the seed papers and against {a.other_label.replace("In ", "", 1)}. Duplicate records within a folder: {"; ".join(f"{s}: {n}" for s, n in dd.items())}. The preferred record is the published, newest one; nothing is deleted. See the Duplicates tab (struck through = duplicate within its folder) and the Folder dedup tab.', [('Script', S('screen_dedup.py')), ('Data', F('data/duplicates_all-zotero-records.tsv'))]),
     ('5. Outcome', 'The task type of each paper: one of the seed task groups, or NEW (then clustered into a candidate new category).', []),
     ('6. Models (predictors)', f'Three open-weight embedding models, run locally on one Apple-silicon computer (no API, no data leaves the machine): EmbeddingGemma 2 (Google, 2026-10, Apache 2.0), harrier-oss-v1-0.6b (Microsoft, MIT; similarity prompt "sts_query"), DNA-VL-STEER-2B (Dnotitia, Korea; Apache 2.0; a calibrated variant of Qwen3-VL-Embedding-2B). Versions and packages: settings_and_versions.json. Origin policy: open-weight foreign models are allowed when local and near state of the art (JP, 2026-11-25).', [('Settings and versions', F('data/settings_and_versions.json')), ('Model notes', gh_file('pipeline/skills/Tools-and-Models.md'))]),
     ('7. Input and prompts', f'Each paper is represented by {modes}. No generation, no instructions beyond the models\' default prompts, no fine-tuning. Papers with no usable text are flagged.', [('Script', S('screen_embed.py'))]),
     ('8. Reference standard', 'The seed papers\' task groups come from the Review-Arena sections of the vault (JP\'s own grouping of the questions each paper answers). There are no human labels for the new papers yet: JP\'s decisions in the Papers tab will become the reference standard.', [('Seed labels', gh_file('pipeline/screening/shared/seed-papers_task-groups.json'))]),
     ('9. Analysis', f'(a) Each model: cosine similarity between the paper and every seed; the paper gets the task group of its most similar seed, or NEW if that similarity is below the model\'s own 15th percentile of seed-to-seed nearest similarity. (b) Majority vote: a category needs 2 of 3 models to agree. (c) Papers voted NEW are clustered (average linkage on the mean of the three models\' distances); the distance threshold is chosen by silhouette score ({cc.get("silhouette", "n/a") if not isinstance(cc.get("silhouette"), float) else round(cc["silhouette"], 3)}, {cc.get("pool", "n/a")} papers clustered); clusters of 2 or more papers become candidate categories. (d) Category keywords: the 7 highest mean TF-IDF terms of the members\' titles and abstracts. (e) Category names and task-type phrases were written by Claude Sonnet 5.5 from the keywords and member titles and are not yet checked by a person. E-means (a fast k-means for huge datasets) was not used: with this few papers ordinary clustering is instant.', [('Script (votes and clusters)', S('screen_embed.py')), ('Script (this workbook and data files)', S('screen_to_gsheet.py')), ('Category names', F('data/new-category-names_and-task-types.json'))]),
     ('10. Performance', f'Leave-one-out on the seed papers (each seed hidden, then classified from the others): {mcs}. This is the only accuracy measure so far; the sample is small (one task group has a single seed). Agreement with JP\'s decisions will be added when the Papers tab is filled in.', [('Data', F('data/model-check_leave-one-out.tsv'))]),
     ('11. Missing data', 'Papers with no abstract or little PDF text are flagged in Screening hints; a record with a wrong title in Zotero is flagged too. No imputation.', []),
     ('12. Limitations', 'Categories reflect how similar the first pages or abstracts are, not a reading of the paper. Seed task groups are few and uneven. Category names are suggestions. Embeddings may group by topic or field more than by the task a model performs.', []),
     ('13. Ethics and privacy', 'Only titles, abstracts, DOIs and Zotero keys of published papers are used. Abstracts and local file paths stay out of the public repository; the repository holds metadata only.', []),
     ('14. Open science (data and code)', 'All code and metadata-only data are on GitHub in the folders linked here; the working files with abstracts stay on the computer that ran the analysis. To reproduce: run zotero_collection.py, screen_dedup.py, screen_embed.py and screen_to_gsheet.py in that order (commands in the run folder README).', [('Run folder', F('')), ('All scripts', gh_dir('pipeline/scripts')), ('Run folder README', F('README.md'))]),
     ('15. AI-use disclosure (GAMER)', f'The scripts, the category names and this report were written by Claude Sonnet 5.5 (Claude Code) on {date.today()}; the embedding models are the three named above. A person has not yet reviewed them.', [('AI disclosure', gh_file('pipeline/provenance/AI-disclosure.md'))]),
     ('How to review', 'Use the Papers tab: filter by Proposed category or Screening hints, then fill JP: decision and JP: category (dropdown from the Lists tab).', []),
     ('Built', str(date.today()), [])]
    ab.append(['Item', 'What was done', 'Links (GitHub, main branch)']); 
    for item, text, links in items:
        ab.append([item, text, '']); r = ab.max_row; 
        if links:
            ab.cell(r, 3).value = links[0][0]; ab.cell(r, 3).hyperlink = links[0][1]; ab.cell(r, 3).font = link
            for lt, lu in links[1:]:
                ab.append(['', '', lt]); rr = ab.max_row; ab.cell(rr, 3).hyperlink = lu; ab.cell(rr, 3).font = link
    SS.polish_about(ab, text_width=86)
    for row in ab.iter_rows(min_row=2):
        if row[2].hyperlink: row[2].font = link
    ab.freeze_panes = 'A2'
    out = Path(a.out or Path(a.result).parent / 'screening-review.xlsx'); wb.save(out); print('wrote', out, '| papers', n)
    # ----- tidy GitHub folder: metadata only
    def tsv(name, header, data):
        with open(run / 'data' / name, 'w', newline='', encoding='utf-8') as f: w = csv.writer(f, delimiter='\t'); w.writerow(header); w.writerows(data)
    keep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15] + list(range(16, 16 + 4 * len(names)))
    tsv('papers_categories-and-model-votes.tsv', [cols[i] for i in keep], [[r[i] for i in keep] for r in rows])
    tsv('new-categories_one-paper-per-row.tsv', ['Category id', 'Category', 'Task type', 'Top 7 keywords', 'Paper title', 'Year', 'Authors', 'Zotero key', 'DOI', 'Models agreeing'], npc)
    tsv('categories_summary.tsv', ['Category', 'Task type', 'Kind', 'Category id', 'Seed papers', 'New papers', 'Top 7 keywords'], category_rows)
    tsv('duplicates_all-zotero-records.tsv', ['Folder (Zotero library copy)', 'Within this folder', 'Group in this folder', 'Zotero key', 'Title', 'Year', 'DOI', 'Has PDF', 'Why grouped', 'Across both folders: group', 'Across both folders: role'], [[r['source'], r.get('folder_role', ''), r.get('folder_group', ''), r['key'], r['title'], r['year'], r['doi'], 'yes' if r['pdfs'] else 'no', r['dup_why'], r['dup_group'], r['dup_role']] for r in drows])
    tsv('folder-dedup_summary.tsv', ['Folder', 'Zotero records', 'Distinct papers', 'Duplicate records', 'Share duplicate'], fsum)
    tsv('model-check_leave-one-out.tsv', ['Model', 'Leave-one-out accuracy', 'Seeds tested', 'Median nearest-seed similarity', 'NEW threshold'], mc)
    pk = {k: md.version(k) for k in ('transformers', 'sentence-transformers', 'torch', 'scikit-learn', 'numpy', 'pymupdf') if k in {d.metadata['Name'].lower() for d in md.distributions()}}
    json.dump({'run': a.run_dir, 'date': str(date.today()), 'collection': a.collection, 'text_mode': a.text_mode, 'models': [clean(n) for n in names], 'novel_threshold_percentile': 15, 'majority_rule': '2 of 3', 'novel_thresholds': {clean(k): v['novel_threshold'] for k, v in rep.items() if k != 'cluster_choice'},
               'clustering': {'method': 'agglomerative, average linkage, mean of the three models\' cosine distances', **cc}, 'keywords': 'top 7 mean TF-IDF terms (unigrams and bigrams) of member titles and Zotero abstracts', 'packages': pk, 'hardware': 'Apple silicon, 24 GB, PyTorch MPS', 'max_sequence_length_tokens': 1024}, open(run / 'data/settings_and_versions.json', 'w'), indent=1)
    readme = [f'# Screening run {a.run_dir}', '', f'Collection: {a.collection}. Built {date.today()}. Reported following TRIPOD+LLM as far as it fits (embedding models, no generation). The Google Sheet has the same content with the full per-paper tables.', '']
    for item, text, links in items: readme += [f'## {item}', text] + [f'- [{lt}]({lu})' for lt, lu in links] + ['']
    readme += ['## Files in `data/`', '- `papers_categories-and-model-votes.tsv`: one row per distinct paper, category, task type, each model\'s pick and similarity, hints (no abstracts, no local paths).', '- `new-categories_one-paper-per-row.tsv`, `categories_summary.tsv`: the candidate new categories and all categories with task types and keywords.', '- `duplicates_all-zotero-records.tsv`, `folder-dedup_summary.tsv`: every Zotero record with its duplicate role inside its folder and across folders.', '- `model-check_leave-one-out.tsv`, `settings_and_versions.json`: how well each model recovers the seed groups; every setting and package version.', '- `new-category-names_and-task-types.json`: the names written for the new categories (edit here, rerun the last script).', '', '## Commands (run from the vault root; Python environment `~/.cache/lives-bench/venv-embed`)', '```', f'python3 pipeline/scripts/zotero_collection.py "{a.collection}" --library 1', f'python3 pipeline/scripts/screen_dedup.py <export>.json --also <group-copy export>.json --pool <other-set export>.json', f'python pipeline/scripts/screen_embed.py --dedup dedup.json --text-mode {a.text_mode}', f'python pipeline/scripts/screen_to_gsheet.py --result screen-result.json --dedup dedup.json --run-dir {a.run_dir} --collection "{a.collection}" --text-mode {a.text_mode}', '```']
    (run / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8'); print('wrote', run)
if __name__ == '__main__': main()

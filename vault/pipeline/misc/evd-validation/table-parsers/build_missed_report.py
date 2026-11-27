"""Writes missed-values.md and missed-values.html from missed_values.json (run analyze_missed.py first)."""
import json, html, collections, os
D=json.load(open('missed_values.json')); S=D['summary']; M=D['missed_repair_v1']
CAUSES=[('caption_or_footnote_text','Caption or footnote text','The value is written in the caption or a footnote of the table, not in a table cell.'),
 ('value_in_label_cell','Value inside a label cell','The number is part of a row label or header text, for example "Top 5 sentences" or "(3) Combined LLMs (consistent in 9/9)".'),
 ('value_in_mixed_text_cell','Value inside a mixed text cell','PyMuPDF returned the value, but inside a cell that also holds words or units; the scorer accepts only number-like cells.'),
 ('symbol_problem','Symbol problem still unrepaired (first repair)','A U+0004 minus sign and a footnote letter in the cell kept the cell from being read as a number; the extended repair fixes it.'),
 ('no_table_detected','No table detected','find_tables returned nothing on the page.'),
 ('no_ruling_lines_merged','No ruling lines, columns or rows merged','The table has no lines, so cells were merged.'),
 ('figure_or_image','Value in a figure or image','The value is drawn in an image, with no text layer.'),
 ('header_spans','Header spans','A merged header cell moved the columns.'),
 ('other','Other','Anything else.')]
cnt=collections.Counter(r['cause'] for r in M); papers=sorted({r['paper'].split('-et-al')[0] for r in M})
per=collections.defaultdict(collections.Counter)
for r in M: per[r['paper'].split('-et-al')[0]][r['cause']]+=1
def pm(r):
    n=r['pymupdf_tables']
    base=f"{n} table(s) found on the page. "
    return base+{'caption_or_footnote_text':'The value is in the caption or footnote text only.','value_in_label_cell':'The number is inside a label or header cell.','value_in_mixed_text_cell':'The value is present, inside a cell that also holds text.','symbol_problem':'The value is in a cell with a U+0004 minus sign and a footnote letter; found after the extended repair.'}.get(r['cause'],'')
def yn(b): return 'yes' if b else 'no'
def short(r): return f"{r['row'] or '(caption or text)'}"
mo7=D['mineru_found_pymupdf_plain_missed']
# ---------------- markdown
L=[]
L+=['# Missed table values: what the 33 are and why','',
'## What the 463 values are','',
'The project reads scientific papers and records the numbers that support each finding. Four pilot papers (Sarol et al. 2024, Bougie et al. 2024, Tyser et al. 2024, Woelfle et al. 2024) were checked by hand against the PDF; the 463 values here are the numbers from those papers whose location was recorded as a table (file picost.json of the batch05 and batch07 runs, fields value, pdf_page, table_or_figure, row, column). '
'A parser "finds" a value when, on that PDF page, the value appears as a number in a number-like cell of a table the parser returned (commas, leading zeros, plus-minus signs and percent signs ignored). PyMuPDF find_tables is the baseline; Marker and MinerU are the two alternatives; "repair" is tablelib.repair_cell_text, which fixes symbols the PDF text layer stores wrongly.','',
f"Result with the first repair (the version the 33 were counted with): PyMuPDF {S['found_by_pymupdf_repair_v1']} of {S['values']}; Marker {S['found_by_marker_repair_v1']}; MinerU {S['found_by_mineru']}. After the extended repair described in RESULTS.md, PyMuPDF and Marker find {S['found_by_pymupdf_repair_v2']} of {S['values']}, so 32 values remain.",'',
'## Summary: cause of each missed value','',
'| Cause | Values | '+' | '.join(papers)+' |','|---|---|'+'---|'*len(papers)]
for k,name,desc in CAUSES:
    if cnt.get(k) or k in ('no_table_detected','no_ruling_lines_merged','figure_or_image','header_spans'): L.append(f"| {name} | {cnt.get(k,0)} | "+' | '.join(str(per[p].get(k,0)) for p in papers)+' |')
L.append(f"| Total | {len(M)} | "+' | '.join(str(sum(per[p].values())) for p in papers)+' |')
L+=['','Cause definitions (fixed list): '+'; '.join(f"{n}: {d}" for k,n,d in CAUSES),'',
'Main finding: none of the 33 is a table cell that PyMuPDF read wrongly or did not see. In 17 cases the value is in a caption or footnote, in 10 it is part of a row or header label, in 5 it is present in a cell with text around it that the scorer did not accept, and in 1 a symbol problem hid it (recovered by the extended repair). No table was undetected, no figure was involved, and no merged header moved a column for these values.','',
'## One row per missed value','',
'Marker and MinerU columns: found as a number-like cell value on the page (Marker plain / Marker with first repair / Marker with extended repair / MinerU).','',
'| # | Paper | PDF page | Table | Row label | Column label | Value | Location text given by the pipeline | What PyMuPDF returned | Marker (plain / repair 1 / repair 2) | MinerU | Cause |','|---|---|---|---|---|---|---|---|---|---|---|---|']
for i,r in enumerate(M,1):
    loc=f"{r['table']}; label: {r['label']}"+(f"; unit {r['unit']}" if r['unit'] else '')
    L.append(f"| {i} | {r['paper'].split('-et-al')[0]} | {r['page']} | {r['table']} | {short(r)} | {r['column'] or '-'} | {r['value']} | {loc[:90]} | {pm(r)} | {yn(r['marker_plain'])} / {yn(r['marker_repair_v1'])} / {yn(r['marker_repair_v2'])} | {yn(r['mineru_plain'])} | {dict((k,n) for k,n,_ in CAUSES)[r['cause']]} |")
L+=['','## Values MinerU found that PyMuPDF did not','',
f"Without any repair, MinerU found {len(mo7)} values that PyMuPDF did not (all in Woelfle et al.): "+'; '.join(f"page {r['page']} {r['table']} row \"{r['row']}\" value {r['value']}" for r in mo7)+'.',
f"With the first repair on PyMuPDF, {len(D['mineru_found_pymupdf_v1_missed'])} remained (the 0.04 in Table 2, PRECIS-2, GPT-3.5, Cohen's kappa). With the extended repair {len(D['mineru_found_pymupdf_v2_missed'])} remain: PyMuPDF and Marker now find all 431 values MinerU finds.",
'The reason for the original gap was the text layer: Woelfle encodes the en dash inside confidence intervals as the letter e, minus signs as a control character and footnote markers as letters glued to numbers; MinerU reads the page image and avoids these.','',
'## What a code change could fix','',
'| Cause | Values | Change | Values recovered (estimate) |','|---|---|---|---|',
f"| Caption or footnote text | {cnt.get('caption_or_footnote_text',0)} | These are not cell values. Either relabel them in the ground truth as caption or footnote text (no code), or let the checker also search the caption and footnote text of the page (a few lines on top of table_cells). | up to 17 of 17 by caption search; the 12 in the Bougie and Tyser captions appear in no cell at all |",
f"| Value inside a label cell | {cnt.get('value_in_label_cell',0)} | Accept a match in any cell of the table, label cells included, when the ground truth row is a header or label. | 10 of 10 |",
f"| Value inside a mixed text cell | {cnt.get('value_in_mixed_text_cell',0)} | Accept a number token inside a cell that also contains units or words (split the cell on spaces and brackets). | 5 of 5 |",
f"| Symbol problem still unrepaired | {cnt.get('symbol_problem',0)} | Already done in the extended repair_cell_text (U+0004 minus plus the footnote letter). | 1 of 1 |",
'','If the scorer accepted a number token in any cell (labels and text cells included), every parser would find '+str(S['relaxed_any_cell']['pymupdf_repair_v2'])+f" of {S['values']}; 5 of those extra matches are accidental (the token 5 in a header such as Recall@5, the token 9 in other cells) and are not the cell the ground truth means. The remaining 12 are the Bougie and Tyser caption values.",
'Pages and images: missed-values.html shows a crop of the page with the value highlighted for each value (local images in missed-values-images/).','']
open('missed-values.md','w').write('\n'.join(L))
# ---------------- html
css='body{font-family:system-ui,sans-serif;margin:1.5em 2em;max-width:1200px}table{border-collapse:collapse;margin:1em 0}td,th{border:1px solid #999;padding:4px 8px;font-size:13px;vertical-align:top}th{background:#eee}img{max-width:560px;border:1px solid #888;display:block;margin:4px 0}.c1{background:#fde}.c2{background:#eef}.c3{background:#efe}.c4{background:#ffd}'
H=[f'<!doctype html><meta charset="utf-8"><title>Missed table values</title><style>{css}</style><h1>Missed table values: what the 33 are and why</h1>']
H.append('<h2>What the 463 values are</h2><p>The project reads scientific papers and records the numbers that support each finding. Four pilot papers (Sarol, Bougie, Tyser and Woelfle) were checked by hand against the PDF. The 463 values are the numbers from those papers whose location was recorded as a table. A parser finds a value when, on that PDF page, the value appears as a number in a number-like cell of a table the parser returned. PyMuPDF find_tables is the baseline; Marker and MinerU are alternatives.</p>')
H.append(f"<p>With the first symbol repair: PyMuPDF {S['found_by_pymupdf_repair_v1']} of {S['values']}, Marker {S['found_by_marker_repair_v1']}, MinerU {S['found_by_mineru']}. After the extended repair PyMuPDF and Marker find {S['found_by_pymupdf_repair_v2']}.</p>")
H.append('<h2>Cause of each missed value</h2><table><tr><th>Cause</th><th>Values</th>'+''.join(f'<th>{p}</th>' for p in papers)+'<th>Meaning</th></tr>')
for k,n,d in CAUSES[:4]+CAUSES[4:]:
    H.append(f"<tr><td>{html.escape(n)}</td><td>{cnt.get(k,0)}</td>"+''.join(f'<td>{per[p].get(k,0)}</td>' for p in papers)+f'<td>{html.escape(d)}</td></tr>')
H.append(f"<tr><th>Total</th><th>{len(M)}</th>"+''.join(f'<th>{sum(per[p].values())}</th>' for p in papers)+'<th></th></tr></table>')
H.append('<p>None of the 33 is a table cell that PyMuPDF read wrongly or did not see: 17 are caption or footnote text, 10 are label text, 5 are present in a mixed text cell the scorer did not accept, 1 was a symbol problem now repaired.</p>')
H.append('<h2>One entry per value, with the page region (value highlighted in red)</h2>')
cls={'caption_or_footnote_text':'c1','value_in_label_cell':'c2','value_in_mixed_text_cell':'c3','symbol_problem':'c4'}
names=dict((k,n) for k,n,_ in CAUSES); shown=set()
H.append('<table><tr><th>#</th><th>Paper, PDF page, table</th><th>Row label</th><th>Column label</th><th>Value</th><th>Location text from the pipeline</th><th>What PyMuPDF returned</th><th>Marker plain / repair 1 / repair 2</th><th>MinerU</th><th>Cause</th><th>Page region</th></tr>')
for i,r in enumerate(M,1):
    img='' if r['image'] in shown else f'<img src="missed-values-images/{r["image"]}" alt="page crop">'; shown.add(r['image'])
    loc=f"{r['table']}; label: {r['label']}"
    H.append(f"<tr class=\"{cls[r['cause']]}\"><td>{i}</td><td>{html.escape(r['paper'].split('-et-al')[0])}, p. {r['page']}, {html.escape(r['table'])}</td><td>{html.escape(short(r))}</td><td>{html.escape(r['column'] or '-')}</td><td>{html.escape(r['value'])}</td><td>{html.escape(loc)}</td><td>{html.escape(pm(r))}</td><td>{yn(r['marker_plain'])} / {yn(r['marker_repair_v1'])} / {yn(r['marker_repair_v2'])}</td><td>{yn(r['mineru_plain'])}</td><td>{html.escape(names[r['cause']])}</td><td>{img or 'see the same image above'}</td></tr>")
H.append('</table><h2>Values MinerU found that PyMuPDF did not</h2><ul>')
for r in mo7: H.append(f"<li>page {r['page']}, {html.escape(r['table'])}, row {html.escape(r['row'])}, value {html.escape(r['value'])}</li>")
H.append(f"</ul><p>{len(mo7)} without repair, {len(D['mineru_found_pymupdf_v1_missed'])} after the first repair, {len(D['mineru_found_pymupdf_v2_missed'])} after the extended repair.</p>")
open('missed-values.html','w').write(''.join(H))
print('written')

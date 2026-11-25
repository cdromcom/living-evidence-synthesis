#!/usr/bin/env python3
"""Traceability audit: for every row of the TRIPOD-LLM and Quality appraisal tables, is the quote verbatim in the PDF, and is the cited
page right? Read-only. Writes <outdir>/signal-quote-audit.csv and prints a summary.
  python3 audit_signal_quotes.py [--only @citekey] [--outdir DIR]
Page check: the locator's page is compared with the PDF's printed page labels (page_map); 'pdf-position' means the PDF prints no page
numbers (preprints) so the PDF position is the reference."""
import csv, sys, collections
from pathlib import Path
import pdf_pages as pp, signals_common as sc
import fitz

only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
outdir = Path(sys.argv[sys.argv.index('--outdir') + 1]) if '--outdir' in sys.argv else Path('.')
rows_out, per_src = [], {}
for path in sorted(sc.SRC_DIR.glob('@*.md')):
    if only and path.stem != only.lstrip('@') and ('@' + path.stem) != only: continue
    rows = sc.source_rows(path); pdf = pp.resolve_pdf(path.stem)
    if not pdf: per_src[path.stem] = 'no PDF'; continue
    doc = fitz.open(pdf); pm = {r['pdf']: r for r in pp.page_map(doc)}
    for r in rows:
        st, found_pages = 'no quote', ''
        if r['quote']:
            h = pp.find_quote(doc, r['quote'])
            if not h['found']: st = 'quote NOT found in PDF'
            else:
                found_pages = ','.join(f"{p}:{pm[p]['printed']}" for p in h['pages'])
                if not r['page']: st = 'verbatim, no page cited'
                else:
                    printed = {pm[p]['printed'] for p in h['pages']}; pos = {str(p) for p in h['pages']}
                    src = pm[h['pages'][0]]['source']
                    st = ('verbatim, page ok (printed)' if r['page'] in printed and src != 'pdf-position' else
                          'verbatim, page ok (pdf-position; no printed numbers in file)' if r['page'] in printed else
                          'verbatim, cites PDF position not printed page' if r['page'] in pos else 'verbatim, page WRONG')
        r.update(status=st, found_pages=found_pages); rows_out.append({k: v for k, v in r.items() if k != 'raw'})
    per_src[path.stem] = len(rows)
if rows_out:
    with open(outdir / 'signal-quote-audit.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0])); w.writeheader(); w.writerows(rows_out)
c = collections.Counter(r['status'] for r in rows_out)
withq = sum(v for k, v in c.items() if k != 'no quote')
print(f"sources: {len(per_src)}; rows: {len(rows_out)}; rows with a quote: {withq}")
for k, v in c.most_common(): print(f"  {v:5d}  {k}")
print('sources without PDF:', [k for k, v in per_src.items() if v == 'no PDF'])

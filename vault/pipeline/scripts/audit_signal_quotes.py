#!/usr/bin/env python3
"""Traceability audit: for every row of the TRIPOD-LLM and Quality appraisal tables, is the quote verbatim in the PDF, and is the cited
page right? Read-only. Writes <outdir>/signal-quote-audit.csv and prints a summary.
  python3 audit_signal_quotes.py [--only @citekey] [--outdir DIR]
Page check: the locator's page is compared with the PDF's printed page labels (page_map); 'pdf-position' means the PDF prints no page
numbers (preprints, or a page without one) so the PDF position is the reference (JP, 2026-11-25: fine when the PDF has no page numbers)."""
import csv, re, sys, collections, difflib
from pathlib import Path
import pdf_pages as pp, signals_common as sc
import fitz

only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None
outdir = Path(sys.argv[sys.argv.index('--outdir') + 1]) if '--outdir' in sys.argv else Path('.')
rows_out, per_src = [], {}
for path in sorted(sc.SRC_DIR.glob('@*.md')):
    if only and path.stem.lstrip('@') != only.lstrip('@'): continue
    rows = sc.source_rows(path); pdf = pp.resolve_pdf(path.stem)
    if not pdf: per_src[path.stem] = 'no PDF'; continue
    doc = fitz.open(pdf); pm = {r['pdf']: r for r in pp.page_map(doc)}
    for r in rows:
        st, found_pages, cause, ratio = 'no quote', '', '', ''
        if r['quote']:
            urls = re.findall(r'(?:https?://|www\.|doi\.org/|osf\.io/|github\.com/)[^\s)\]>,;]+', r['quote'])
            h = pp.find_quote(doc, r['quote'])
            if urls and not h['found']:   # a quote that is a link: look in the text and in the PDF's link annotations
                norm_u = lambda u: re.sub(r'^https?://(www\.)?', '', u.rstrip('.,;)')).lower()
                alltext = ' '.join(norm_u(x) for x in re.findall(r'\S+', ' '.join(p.get_text() for p in doc)))
                links = {norm_u(l['uri']) for l in pp.links(doc)}
                ok = [norm_u(u) in alltext or any(norm_u(u) in L or L in norm_u(u) for L in links) for u in urls]
                h = {'found': all(ok), 'pages': [1] if all(ok) else []}; cause = 'URL: found in text or link annotation' if all(ok) else 'URL: not found in text or links'
                if h['found']: st = 'URL verified (no page check)'; found_pages = ''; r.update(status=st, found_pages=found_pages, cause=cause, ratio=ratio); rows_out.append({k: v for k, v in r.items() if k != 'raw'}); continue
            if not h['found']:
                st = 'quote NOT found in PDF'
                cp = int(r['page']) if r['page'].isdigit() else None
                inv = {v['printed']: k for k, v in pm.items() if v['printed']}; ppg = int(inv.get(r['page'], cp or 0)) if cp else 0
                pages = [p for p in (ppg - 1, ppg, ppg + 1) if 1 <= p <= len(doc)] or list(range(1, min(len(doc), 40) + 1))
                tgt = pp.norm(r['quote']); text = ''.join(pp.norm(doc[p - 1].get_text()) for p in pages)
                m = difflib.SequenceMatcher(None, tgt, text, autojunk=False).find_longest_match(0, len(tgt), 0, len(text)) if tgt and text else None
                ratio = round(m.size / len(tgt), 2) if m and tgt else 0
                cause = ('URL: not found in text or links' if urls else 'near match (typographic: hyphen, symbol, ligature, footnote mark)' if ratio >= 0.9 else
                         'trimmed or lightly edited quote' if ratio >= 0.5 else 'not in the text layer (table or figure, other version, or paraphrase)')
            else:
                found_pages = ','.join(f"{p}:{pm[p]['printed']}" for p in h['pages'])
                if not r['page']: st = 'verbatim, no page cited'
                else:
                    printed = {pm[p]['printed'] for p in h['pages']}; pos = {str(p) for p in h['pages']}
                    src = pm[h['pages'][0]]['source']
                    st = ('verbatim, page ok (printed)' if r['page'] in printed and src != 'pdf-position' else
                          'verbatim, page ok (pdf-position; no printed numbers in file)' if r['page'] in printed else
                          'verbatim, page ok (pdf-position; page prints no number)' if r['page'] in pos and any(pm[p]['printed'] is None for p in h['pages'] if str(p) == r['page']) else
                          'verbatim, cites PDF position not printed page' if r['page'] in pos else 'verbatim, page WRONG')
        r.update(status=st, found_pages=found_pages, cause=cause, ratio=ratio); rows_out.append({k: v for k, v in r.items() if k != 'raw'})
    per_src[path.stem] = len(rows)
if rows_out:
    with open(outdir / 'signal-quote-audit.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0])); w.writeheader(); w.writerows(rows_out)
c = collections.Counter(r['status'] for r in rows_out)
fail = collections.Counter(r['cause'] for r in rows_out if r['status'] == 'quote NOT found in PDF')
withq = sum(v for k, v in c.items() if k != 'no quote')
print(f"sources: {len(per_src)}; rows: {len(rows_out)}; rows with a quote: {withq}")
for k, v in c.most_common(): print(f"  {v:5d}  {k}")
print('why quotes were not found:', dict(fail))
print('sources without PDF:', [k for k, v in per_src.items() if v == 'no PDF'])

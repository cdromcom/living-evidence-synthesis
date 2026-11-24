"""Verbatim audit: scan every quote line in EVDs/CLMs/CVTs and verify it appears
verbatim (after NFKD + alnum normalization) in the source PDF.

Reports paraphrased quotes with the cited page, the first 8 normalized chars
that diverge, and a snippet of the actual page text near where the opening
words match (if they match anywhere). The output is a TSV-style file the user
can scan or that downstream scripts can consume to replace with verbatim text.
"""
import re
import sys
import unicodedata
from pathlib import Path
from collections import defaultdict

import fitz

VAULT = Path('/Users/ppatel/Documents/living-synthesis')
PDFS = VAULT / 'source' / 'pdfs'

sys.path.insert(0, '/tmp')
from quote_pipeline_v3 import find_pdf, normalize, CITEKEY_TO_PDF_HINT


def get_node_citekey(text: str, filename: str = '') -> str | None:
    m = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)\.md$', filename)
    if m:
        return m.group(1)
    m = re.search(r'^## Source\s*\n+\[\[@([a-zA-Z][a-zA-Z0-9-]+)\]\]', text, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def get_clm_citekeys(text: str) -> list[str]:
    """Return list of citekeys for CLM (multi-paper)."""
    m = re.search(r'> \[!info\] Papers\s*\n((?:>\s*\[\[@.*?\]\]\s*\n?)+)', text)
    if not m:
        return []
    return list(set(re.findall(r'@([a-zA-Z][a-zA-Z0-9-]+)\b', m.group(1))))


def attribute_clm_quote(line: str, citekeys: list[str]) -> str | None:
    """Try to attribute a CLM quote to one of its papers via author surname/year."""
    m = re.search(r'\(([A-Z][A-Za-z\'-]+)(?:\s+et al\.|\s+&\s+\w+|\s+and\s+\w+)?,\s*(\d{4})', line)
    if not m:
        return None
    surname = m.group(1).lower()
    year = m.group(2)
    cands = [ck for ck in citekeys if surname in ck.lower() and year in ck]
    if len(cands) == 1:
        return cands[0]
    if surname == 'sridharan':
        if 'irb' in line.lower() or 'sop' in line.lower() or 'decision' in line.lower():
            cs = [ck for ck in citekeys if 'AssessingDecisionMaking' in ck]
        else:
            cs = [ck for ck in citekeys if 'LeveragingArtificialIntelligence' in ck]
        if cs:
            return cs[0]
    if cands:
        return cands[0]
    return None


def quote_in_pdf(doc, quote_text: str) -> tuple[bool, int | None, str | None]:
    """Returns (found, page_1based_or_none, divergence_info).
    Verbatim if the entire normalized quote is contained on some page.
    Otherwise, finds the page with the longest matching prefix and reports
    `matched X of Y chars` — useful to distinguish minor truncation from major paraphrase.
    """
    target = normalize(quote_text)
    n = len(target)
    if n < 30:
        return True, None, None
    # Concat per page
    page_concats = []
    for pn in range(len(doc)):
        page_concats.append(''.join(normalize(w[4]) for w in doc[pn].get_text('words')))
    # Full match?
    for pn, concat in enumerate(page_concats):
        if target in concat:
            return True, pn + 1, None
    # Cross-page: try splitting target and matching across consecutive pages
    for pn in range(len(page_concats) - 1):
        combined = page_concats[pn] + page_concats[pn + 1]
        if target in combined:
            return True, pn + 1, f'spans p.{pn+1}-{pn+2}'
    # Find longest prefix match
    best_page = None
    best_match = 0
    for pn, concat in enumerate(page_concats):
        # Binary search for longest prefix in this page
        lo, hi = 30, n
        cur_best = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if target[:mid] in concat:
                cur_best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        if cur_best > best_match:
            best_match = cur_best
            best_page = pn + 1
    return False, best_page, f'matched {best_match} of {n} chars'


def main():
    paraphrases = []  # (file, quote_text_first_120, citekey, cited_page, found_page, snippet)
    pdf_doc_cache = {}
    for kind, dir_name in [('EVD', 'evidence'), ('CLM', 'claims'), ('CVT', 'caveats')]:
        for f in sorted((VAULT / dir_name).glob(f'{kind}*.md')):
            text = f.read_text()
            if kind == 'CLM':
                citekeys = get_clm_citekeys(text)
            else:
                citekeys = []
                ck = get_node_citekey(text, f.name)
                if ck:
                    citekeys = [ck]
            if not citekeys:
                continue
            lines = text.split('\n')
            for line in lines:
                m = re.match(r'>\s*"(.+?)"\s*\(([^)]+)\)', line)
                if not m:
                    continue
                quote = m.group(1)
                citation = m.group(2)
                pgm = re.search(r'\bp{1,2}\.?\s*(\d+)', citation)
                cited_page = int(pgm.group(1)) if pgm else None
                # Skip very short quotes
                if len(quote) < 40:
                    continue
                # Determine citekey
                if kind == 'CLM' and len(citekeys) > 1:
                    quote_ck = attribute_clm_quote(line, citekeys)
                else:
                    quote_ck = citekeys[0]
                if not quote_ck:
                    continue
                if quote_ck not in pdf_doc_cache:
                    pdf = find_pdf(quote_ck)
                    if not pdf:
                        pdf_doc_cache[quote_ck] = None
                        continue
                    pdf_doc_cache[quote_ck] = fitz.open(str(pdf))
                doc = pdf_doc_cache[quote_ck]
                if doc is None:
                    continue
                found, found_pg, snippet = quote_in_pdf(doc, quote)
                if not found:
                    paraphrases.append((f.name, quote[:120], quote_ck, cited_page, found_pg, snippet))
    for d in pdf_doc_cache.values():
        if d:
            d.close()
    # Write report
    out = Path('/tmp/paraphrase_report.tsv')
    with out.open('w') as fp:
        fp.write('file\tcitekey\tcited_page\tfound_partial_page\tdivergence\tquote_first_120\n')
        for row in paraphrases:
            fp.write(f'{row[0]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[1]}\n')
    print(f'Audited. Paraphrases found: {len(paraphrases)}. Report: {out}')
    # Group by paper
    by_paper = defaultdict(list)
    for row in paraphrases:
        by_paper[row[2]].append(row)
    print()
    for ck in sorted(by_paper):
        rows = by_paper[ck]
        print(f'=== {ck} ({len(rows)}) ===')
        for r in rows[:10]:
            print(f'  {r[0][:60]}')
            print(f'    cited p.{r[3]} → {r[4] if r[4] else "no match"}; {r[5]}')
            print(f'    quote: "{r[1]}…"')


if __name__ == '__main__':
    main()

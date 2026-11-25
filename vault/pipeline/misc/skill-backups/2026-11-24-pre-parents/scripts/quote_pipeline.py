"""V4 of the screenshot pipeline: handles EVDs, CLMs, CVTs, and QUEs uniformly.

Differences from v3:
- Full-quote match is tried first (yields precise highlight rects).
- Ellipsis-separated quotes are matched segment by segment; the crop is the
  union of all segments so the entire quoted material is visible.
- Final fallback uses a 300pt tall region (was 90pt) so long quotes never get
  clipped at the bottom.
- Cropped screenshots include a coloured highlight over the matched text:
    EVD = light red, CLM = light green, QUE = light blue, CVT = light gold.
- QUE files (under questions/) are now processed using the same per-quote
  citekey attribution logic as CLMs.
- A `--force` flag regenerates existing screenshots in place (preserving the
  original filename), rather than skipping quotes that already have an embed.

Usage:
    python3 quote_pipeline.py [evd|clm|cvt|que ...] [--force]
"""
import re
import sys
import unicodedata
from pathlib import Path

import fitz

VAULT = Path('/Users/ppatel/Documents/living-synthesis')
PDFS = VAULT / 'source' / 'pdfs'
ATTACH = VAULT / 'evidence' / 'Attachments'

# Light pastel highlight colours, as RGB tuples in [0, 1].
COLORS = {
    'evd': (1.00, 0.70, 0.70),   # light red
    'clm': (0.72, 1.00, 0.72),   # light green
    'que': (0.72, 0.86, 1.00),   # light blue
    'cvt': (1.00, 0.90, 0.55),   # light gold
}

CITEKEY_TO_PDF_HINT = {
    'sonWhenAICoScientists2025': 'son et al',
    'akyonEvaluatingCapabilitiesGenerative2024': 'akyon',
    'alharbiAutomatedAssessmentReporting2024': 'alharbi',
    'bougieGenerativeAdversarialReviews2024a': 'bougie',
    'darcyMARGMultiAgentReview2024': "d'arcy",
    'hasanIntegratingLargeLanguage2024': 'hasan',
    'huntington-kleinLLMsActRepositories2024': 'huntington-klein',
    'idahlOpenReviewerSpecializedLarge2025': 'idahl',
    'leucutaRiskBiasAssessment2025': 'leucuta',
    'louAAAR10AssessingAIs2025': 'lou',
    'robertsComparativeStudyChatGPT2023': 'roberts et al. - 2023 - comparative study',
    'shahidLiteratureGroundedNoveltyAssessment2025': 'shahid et al. - 2025 - literature-grounded novelty assessment of scientific ideas.pdf',
    'sridharanAssessingDecisionMakingCapabilities2024': 'sridharan and sivaramakrishnan - 2024 - assessing the decision-making capabilities',
    'sridharanLeveragingArtificialIntelligence2025': 'sridharan and sivaramakrishnan - 2024 - leveraging artificial intelligence',
    'srinivasanEvaluatingReportingQuality2025a': 'srinivasan',
    'thelwallEvaluatingResearchQuality2024': 'thelwall',
    'tyserAIDrivenReviewSystems2024': 'tyser',
    'wrightsonGPTRCTsUsing2025': 'wrightson',
    'wuAutomatedNoveltyEvaluationa': 'wu',
    'xuCanLLMsIdentify2025': 'xu',
    'zhangDetectingReferenceErrors2024': 'zhang and abernethy - 2024',
    'zhangReviewingScientificPapers2025a': 'zhang and abernethy - 2025',
    'zhouLLMReliableReviewer2024': 'zhou',
    'woelfleBenchmarkingHumanAICollaboration2024': 'woelfle',
    'sarolAssessingCitationIntegrity2024': 'sarol',
    'liangCanLargeLanguage2024a': 'liang',
    'liuReviewerGPTExploratoryStudy2023': 'liu and shah',
}

PADDING = 12.0          # margin around bbox (PDF points)
FALLBACK_HEIGHT = 300.0 # tall fallback so long quotes don't clip
DPI = 250


def find_pdf(citekey: str):
    hint = CITEKEY_TO_PDF_HINT.get(citekey, citekey.split('20')[0].lower())
    matches = [p for p in sorted(PDFS.glob('*.pdf')) if hint.lower() in p.name.lower()]
    return matches[0] if matches else None


def normalize(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '', s)
    return s


def _page_concat(page):
    """Return (words, concat_string, char_to_word_idx)."""
    words = page.get_text('words')
    concat = ''
    char_to_idx = []
    for i, w in enumerate(words):
        nw = normalize(w[4])
        concat += nw
        char_to_idx.extend([i] * len(nw))
    return words, concat, char_to_idx


def _bbox_and_rects(words, si, ei):
    chunk = words[si:ei + 1]
    bbox = (
        min(w[0] for w in chunk) - PADDING,
        min(w[1] for w in chunk) - PADDING,
        max(w[2] for w in chunk) + PADDING,
        max(w[3] for w in chunk) + PADDING,
    )
    rects = [(w[0], w[1], w[2], w[3]) for w in chunk]
    return bbox, rects


def find_full_segment(page, segment: str):
    """Match an entire (ellipsis-free) segment on the page.
    Returns (bbox, word_rects) or None.
    """
    words, concat, char_to_idx = _page_concat(page)
    if not words:
        return None
    nq = normalize(segment)
    if not nq:
        return None
    s = concat.find(nq)
    if s == -1:
        return None
    si = char_to_idx[s]
    ei = char_to_idx[s + len(nq) - 1]
    return _bbox_and_rects(words, si, ei)


def find_open_close(page, opening: str, closing: str):
    """Find opening then closing after it. Returns (bbox, word_rects) or None."""
    words, concat, char_to_idx = _page_concat(page)
    if not words:
        return None
    no, nc = normalize(opening), normalize(closing)
    if not no or not nc:
        return None
    s = concat.find(no)
    if s == -1:
        return None
    e = concat.find(nc, s + len(no))
    if e == -1:
        return None
    si = char_to_idx[s]
    ei = char_to_idx[e + len(nc) - 1]
    return _bbox_and_rects(words, si, ei)


def fallback_open_height(page, opening: str, height_pt: float = FALLBACK_HEIGHT):
    """Last resort: find opening, then crop a tall region in the same column.
    Highlights only the opening words.
    """
    words, concat, char_to_idx = _page_concat(page)
    if not words:
        return None
    no = normalize(opening)
    if not no:
        return None
    s = concat.find(no)
    if s == -1:
        return None
    si = char_to_idx[s]
    ei = char_to_idx[s + len(no) - 1]
    open_chunk = words[si:ei + 1]
    open_x = open_chunk[0][0]
    open_y = open_chunk[0][1]
    relevant = [w for w in words
                if open_y - 2 <= w[1] <= open_y + height_pt
                and abs(w[0] - open_x) < 280]
    if not relevant:
        relevant = open_chunk
    bbox = (
        min(w[0] for w in relevant) - PADDING,
        min(w[1] for w in relevant) - PADDING,
        max(w[2] for w in relevant) + PADDING,
        max(w[3] for w in relevant) + PADDING,
    )
    rects = [(w[0], w[1], w[2], w[3]) for w in open_chunk]
    return bbox, rects


def locate_quote(doc, hinted_page: int, quote_text: str):
    """Returns (page_num, bbox, word_rects) or None.
    word_rects is the list of rects to highlight.
    """
    n_pages = len(doc)
    pages = []
    if 1 <= hinted_page <= n_pages:
        pages.append(hinted_page)
    pages += [p for p in range(1, n_pages + 1) if p not in pages]

    segments = [s.strip() for s in re.split(r'\.{3}|…', quote_text) if s.strip()]

    # Pass 1: full-segment match (most precise; supports ellipsis-separated quotes)
    if segments:
        for page_num in pages:
            page = doc[page_num - 1]
            seg_results = []
            for seg in segments:
                r = find_full_segment(page, seg)
                if r is None:
                    seg_results = None
                    break
                seg_results.append(r)
            if seg_results:
                all_bbox = [r[0] for r in seg_results]
                all_rects = [rect for r in seg_results for rect in r[1]]
                bbox = (
                    min(b[0] for b in all_bbox),
                    min(b[1] for b in all_bbox),
                    max(b[2] for b in all_bbox),
                    max(b[3] for b in all_bbox),
                )
                return page_num, bbox, all_rects

    # Pass 2 + 3 use the first segment's words for opening/closing fallback
    primary = segments[0] if segments else quote_text
    words = primary.split()
    if len(words) < 3:
        words = quote_text.split()
    if len(words) < 3:
        return None

    open_sizes = [min(8, len(words)), 5, 3]
    close_sizes = [min(6, len(words)), 4, 2]

    # Pass 2: opening + closing
    for page_num in pages:
        page = doc[page_num - 1]
        for o in open_sizes:
            opening = ' '.join(words[:o])
            for c in close_sizes:
                if o + c > len(words):
                    continue
                closing = ' '.join(words[-c:])
                r = find_open_close(page, opening, closing)
                if r:
                    return page_num, r[0], r[1]

    # Pass 3: opening + tall height
    for page_num in pages:
        page = doc[page_num - 1]
        for o in open_sizes:
            opening = ' '.join(words[:o])
            r = fallback_open_height(page, opening)
            if r:
                return page_num, r[0], r[1]

    return None


def render(pdf_path: Path, page_num: int, bbox: tuple, word_rects: list,
           color: tuple, out_path: Path):
    doc = fitz.open(str(pdf_path))
    page = doc[page_num - 1]
    if word_rects:
        rects = [fitz.Rect(*r) for r in word_rects]
        annot = page.add_highlight_annot(rects)
        annot.set_colors(stroke=color)
        annot.update()
    mat = fitz.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(*bbox))
    pix.save(str(out_path))
    doc.close()


def get_node_citekey(text: str, filename: str = '') -> str | None:
    m = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)\.md$', filename)
    if m:
        return m.group(1)
    m = re.search(r'^## Source\s*\n+\[\[@([a-zA-Z][a-zA-Z0-9-]+)\]\]', text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r'^appliesTo:[^\n]*\n((?:^\s*-\s*"\[\[.*?\]\]"\s*\n?)+)', text, re.MULTILINE)
    if m:
        refm = re.search(r'@([a-zA-Z][a-zA-Z0-9-]+)\b', m.group(1))
        if refm:
            return refm.group(1)
    return None


def get_papers_from_block(text: str) -> list[str]:
    """Extract list of citekeys from a `> [!info] Papers` block (CLM and QUE).
    Tolerates blank `>` separator lines between citekey rows.
    """
    m = re.search(r'> \[!info\] Papers\s*\n((?:>.*\n?)+)', text)
    if not m:
        return []
    return re.findall(r'\[\[@([a-zA-Z][a-zA-Z0-9-]+)\]\]', m.group(1))


def get_quote_citekey_from_attribution(line: str, fallback_citekeys: list[str]) -> str | None:
    """Determine citekey for a multi-paper node's quote by parsing
    `(Author, Year, ...)` attribution against the candidate list.
    """
    m = re.search(r'\(([A-Z][A-Za-z\'-]+?)(?:\s+et al\.|\s+&\s+\w+|\s+and\s+\w+)?,\s*(\d{4})', line)
    if not m:
        # Single-paper QUE: if only one candidate, use it.
        if len(fallback_citekeys) == 1:
            return fallback_citekeys[0]
        return None
    surname = m.group(1).lower()
    year = m.group(2)
    candidates = [ck for ck in fallback_citekeys
                  if surname in ck.lower() and year in ck]
    if len(candidates) == 1:
        return candidates[0]
    if surname == 'sridharan':
        if any(k in line.lower() for k in ('irb', 'decision', 'sop', 'so ps')):
            cand = [ck for ck in fallback_citekeys if 'AssessingDecisionMaking' in ck]
        else:
            cand = [ck for ck in fallback_citekeys if 'LeveragingArtificialIntelligence' in ck]
        if cand:
            return cand[0]
    if candidates:
        return candidates[0]
    if len(fallback_citekeys) == 1:
        return fallback_citekeys[0]
    return None


def find_existing_embed(lines, i):
    """Look at lines after the quote at index `i` for an existing
    `> ![[X.png]]` reference. Returns (line_idx, filename) or None.
    """
    for j in range(i + 1, min(i + 6, len(lines))):
        nxt = lines[j].strip()
        if not nxt:
            continue
        em = re.match(r'>\s*!\[\[([^\]]+\.png)\]\]', nxt)
        if em:
            return j, em.group(1)
        if nxt.startswith('>') and re.search(r'\([A-Za-z][^)]+\bp{1,2}\.?\s*\d+', nxt):
            return None
        if not nxt.startswith('>') and not nxt.startswith('!'):
            return None
    return None


def process_node(path: Path, kind: str, force: bool = False,
                 global_counts: dict | None = None):
    """kind ∈ {'evd', 'clm', 'cvt', 'que'}.
    `global_counts` is a shared {(citekey, kind, page): last_idx} map so canonical
    -p{N}-{idx}.png names don't collide across multiple node files of the same
    citekey within a single pipeline run. Pass the same dict across calls.
    Returns (added, regenerated, failed, fails).
    """
    text = path.read_text()
    lines = text.split('\n')
    color = COLORS[kind]

    if kind in ('evd', 'cvt'):
        node_ck = get_node_citekey(text, path.name)
        candidates = []
    else:  # clm or que
        node_ck = None
        candidates = get_papers_from_block(text)

    quote_count_per_page = global_counts if global_counts is not None else {}
    pdf_cache = {}
    edits = []        # (insert_after_idx, text) for new embeds
    added = 0
    regenerated = 0
    fails = []

    for i, line in enumerate(lines):
        m = re.match(r'>\s*"(.+?)"\s*\(([^)]+)\)', line)
        if not m:
            continue
        quote_text = m.group(1)
        citation = m.group(2)
        pgm = re.search(r'\bp{1,2}\.?\s*(\d+)', citation)
        if not pgm:
            continue
        cited_page = int(pgm.group(1))

        if kind in ('clm', 'que'):
            quote_ck = get_quote_citekey_from_attribution(line, candidates)
            if not quote_ck:
                continue
        else:
            quote_ck = node_ck
            if not quote_ck:
                continue

        existing = find_existing_embed(lines, i)
        if existing and not force:
            continue

        if quote_ck not in pdf_cache:
            pdf = find_pdf(quote_ck)
            pdf_cache[quote_ck] = (pdf, fitz.open(str(pdf))) if pdf else (None, None)
        pdf_path, doc = pdf_cache[quote_ck]
        if not pdf_path:
            fails.append((quote_ck, cited_page, quote_text[:60]))
            continue

        result = locate_quote(doc, cited_page, quote_text)
        if not result:
            fails.append((quote_ck, cited_page, quote_text[:60]))
            continue
        page_num, bbox, word_rects = result

        if existing:
            out_name = existing[1]
            out_path = ATTACH / out_name
            render(pdf_path, page_num, bbox, word_rects, color, out_path)
            regenerated += 1
        else:
            key = (quote_ck, kind, page_num)
            idx = quote_count_per_page.get(key, 0) + 1
            quote_count_per_page[key] = idx
            out_name = f'{quote_ck}-{kind}-p{page_num}-{idx}.png'
            out_path = ATTACH / out_name
            render(pdf_path, page_num, bbox, word_rects, color, out_path)
            edits.append((i, f'> ![[{out_name}]]'))
            added += 1

    for v in pdf_cache.values():
        if v[1] is not None:
            v[1].close()

    if edits:
        for i, embed in sorted(edits, reverse=True):
            lines.insert(i + 1, embed)
        path.write_text('\n'.join(lines))

    return (added, regenerated, len(fails), fails)


def main():
    args = [a for a in sys.argv[1:] if a != '--force']
    force = '--force' in sys.argv[1:]
    targets = args if args else ['evd', 'clm', 'cvt', 'que']

    folders = {
        'evd': (VAULT / 'evidence', 'EVD*.md'),
        'clm': (VAULT / 'claims', 'CLM*.md'),
        'cvt': (VAULT / 'caveats', 'CVT*.md'),
        'que': (VAULT / 'questions', 'QUE*.md'),
    }

    totals = {'added': 0, 'regen': 0, 'failed': 0}
    global_counts: dict = {}
    for kind in targets:
        folder, glob = folders[kind]
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob(glob)):
            a, r, fc, fails = process_node(f, kind, force=force,
                                           global_counts=global_counts)
            if a or r or fc:
                totals['added'] += a
                totals['regen'] += r
                totals['failed'] += fc
                parts = []
                if a: parts.append(f'+{a}')
                if r: parts.append(f'~{r}')
                if fc: parts.append(f'✗{fc}')
                print(f'{kind.upper()} {" ".join(parts)}: {f.name}')
                for ck, pg, q in fails:
                    print(f'   FAIL {ck} p.{pg}: {q!r}')
    print(f'\nTotal: {totals["added"]} new, {totals["regen"]} regenerated, '
          f'{totals["failed"]} failed')


if __name__ == '__main__':
    main()

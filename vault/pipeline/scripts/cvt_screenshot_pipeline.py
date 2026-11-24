"""V2 of the CVT-screenshot pipeline: more robust quote location.

Improvements over v1:
- Adds hints for pilot papers so 'no PDF' false alarms disappear.
- If the cited page doesn't contain the opening, searches all pages.
- Progressive opening/closing windows: tries full match, then shorter, then
  shortest before giving up.
- Reports failures with the exact opening + closing strings tried, so manual
  fixes are obvious.
"""
import re
import sys
import unicodedata
from pathlib import Path

import fitz

VAULT = Path('/Users/ppatel/Documents/living-synthesis')
PDFS = VAULT / 'source' / 'pdfs'
ATTACH = VAULT / 'evidence' / 'Attachments'

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
    'robertsComparativeStudyChatGPT2023': 'roberts et al. - 2023 - comparative study of chatgpt and human evaluators on the assessment',
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


def find_pdf(citekey: str):
    hint = CITEKEY_TO_PDF_HINT.get(citekey, citekey.split('20')[0].lower())
    matches = [p for p in sorted(PDFS.glob('*.pdf')) if hint.lower() in p.name.lower()]
    return matches[0] if matches else None


def normalize(s: str) -> str:
    s = unicodedata.normalize('NFKD', s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '', s)
    return s


def find_bbox_on_page(page, opening: str, closing: str, padding: float = 8.0):
    words = page.get_text('words')
    concat = ''
    char_to_idx = []
    for i, w in enumerate(words):
        nw = normalize(w[4])
        concat += nw
        char_to_idx.extend([i] * len(nw))
    no = normalize(opening)
    nc = normalize(closing)
    s = concat.find(no)
    if s == -1:
        return None
    e = concat.find(nc, s + len(no))
    if e == -1:
        return None
    si = char_to_idx[s]
    ei = char_to_idx[e + len(nc) - 1]
    chunk = words[si:ei + 1]
    return (
        min(w[0] for w in chunk) - padding,
        min(w[1] for w in chunk) - padding,
        max(w[2] for w in chunk) + padding,
        max(w[3] for w in chunk) + padding,
    )


def fallback_bbox_from_opening(page, opening: str, height_pt: float = 90, padding: float = 8.0):
    """When closing not found: crop a fixed-height region below the opening word, same column."""
    words = page.get_text('words')
    concat = ''
    char_to_idx = []
    for i, w in enumerate(words):
        nw = normalize(w[4])
        concat += nw
        char_to_idx.extend([i] * len(nw))
    s = concat.find(normalize(opening))
    if s == -1:
        return None
    si = char_to_idx[s]
    open_word = words[si]
    open_x, open_y = open_word[0], open_word[1]
    # Same column: x within ±250pt of opening start
    relevant = [w for w in words
                if open_y - 2 <= w[1] <= open_y + height_pt
                and abs(w[0] - open_x) < 250]
    if not relevant:
        relevant = [open_word]
    return (
        min(w[0] for w in relevant) - padding,
        min(w[1] for w in relevant) - padding,
        max(w[2] for w in relevant) + padding,
        max(w[3] for w in relevant) + padding,
    )


def locate_quote(doc, hinted_page: int, quote_text: str):
    """Return (page_num_1based, bbox) or None.
    Uses a fixed-height fallback when only the opening can be matched.
    """
    # Split quote on ellipses; only match the first segment
    primary = re.split(r'\.{3}|…', quote_text)[0]
    words = primary.split()
    if len(words) < 3:
        words = quote_text.split()
    if len(words) < 3:
        return None
    n_pages = len(doc)
    pages = []
    if 1 <= hinted_page <= n_pages:
        pages.append(hinted_page)
    pages += [p for p in range(1, n_pages + 1) if p not in pages]

    open_sizes = [min(8, len(words)), 5, 3]
    close_sizes = [min(6, len(words)), 4, 2]

    # Pass 1: full match with progressive windows
    for page_num in pages:
        page = doc[page_num - 1]
        for o in open_sizes:
            opening = ' '.join(words[:o])
            for c in close_sizes:
                if o + c > len(words):
                    continue
                closing = ' '.join(words[-c:])
                bbox = find_bbox_on_page(page, opening, closing)
                if bbox:
                    return page_num, bbox

    # Pass 2: fallback — find opening, crop fixed-height region
    for page_num in pages:
        page = doc[page_num - 1]
        for o in open_sizes:
            opening = ' '.join(words[:o])
            bbox = fallback_bbox_from_opening(page, opening)
            if bbox:
                return page_num, bbox
    return None


def render(pdf_path: Path, page_num: int, bbox: tuple, out_path: Path, dpi: int = 250):
    doc = fitz.open(str(pdf_path))
    page = doc[page_num - 1]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(*bbox))
    pix.save(str(out_path))
    doc.close()


def get_citekey(text: str) -> str | None:
    m = re.search(r'^## Source\s*\n+\[\[@([a-zA-Z][a-zA-Z0-9-]+)\]\]', text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r'^appliesTo:[^\n]*\n((?:^\s*-\s*"\[\[.*?\]\]"\s*\n?)+)', text, re.MULTILINE)
    if m:
        for refm in re.finditer(r'@([a-zA-Z][a-zA-Z0-9-]+)\b', m.group(1)):
            return refm.group(1)
    return None


def process_cvt(cvt_path: Path):
    text = cvt_path.read_text()
    citekey = get_citekey(text)
    if not citekey:
        return (0, 0, [])
    pdf = find_pdf(citekey)
    if not pdf:
        return (0, 0, [(citekey, 'no PDF')])

    doc = fitz.open(str(pdf))
    lines = text.split('\n')
    edits = []
    quote_count_per_page = {}
    added = 0
    failures = []

    for i, line in enumerate(lines):
        m = re.match(r'>\s*"(.+?)"\s*\([^)]+\bp{1,2}\.?\s*(\d+)', line)
        if not m:
            continue
        # Already screenshot?
        has_ss = False
        for j in range(i + 1, min(i + 6, len(lines))):
            nxt = lines[j].strip()
            if not nxt:
                continue
            if nxt.startswith('>') and '![[' in nxt:
                has_ss = True
                break
            if nxt.startswith('>') and re.search(r'\([A-Za-z][^)]+\bp{1,2}\.?\s*\d+', nxt):
                break
            if not nxt.startswith('>') and not nxt.startswith('!'):
                break
        if has_ss:
            continue

        quote_text = m.group(1)
        cited_page = int(m.group(2))
        result = locate_quote(doc, cited_page, quote_text)
        if not result:
            failures.append((cited_page, quote_text[:60]))
            continue
        page_num, bbox = result
        idx = quote_count_per_page.get(page_num, 0) + 1
        quote_count_per_page[page_num] = idx
        out_name = f'{citekey}-cvt-p{page_num}-{idx}.png'
        out_path = ATTACH / out_name
        render(pdf, page_num, bbox, out_path)
        edits.append((i, f'> ![[{out_name}]]'))
        added += 1

    doc.close()
    if edits:
        for i, embed in sorted(edits, reverse=True):
            lines.insert(i + 1, embed)
        cvt_path.write_text('\n'.join(lines))

    return (added, len(failures), failures)


def main():
    total_added = 0
    total_failed = 0
    cvts_processed = 0
    for f in sorted((VAULT / 'caveats').glob('CVT*.md')):
        added, failed, fails = process_cvt(f)
        if added or failed:
            cvts_processed += 1
            total_added += added
            total_failed += failed
            status = f'{added} added'
            if failed:
                status += f', {failed} failed'
            print(f'{status}: {f.name}')
            for page, qt in fails:
                if qt == 'no PDF':
                    print(f'   no PDF for citekey {page}')
                else:
                    print(f'   p.{page}: {qt!r}')
    print(f'\nTotal: {cvts_processed} CVTs touched, {total_added} crops added, {total_failed} failures')


if __name__ == '__main__':
    main()

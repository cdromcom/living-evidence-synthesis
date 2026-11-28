#!/usr/bin/env python3
"""Methods table check (JP, 2026-11-27): compare a table copied into a vault page (a markdown table or a list of rows) cell by cell with the same table in the source PDF page.
No LLM call, no network: the source table is read by MinerU first (local models, run in the table-parsers virtual environment, one subprocess per page, cached per PDF hash and page),
by PyMuPDF find_tables (with pdf_pages.repair_cell_text and a derotated page) for cells MinerU lacks, or by python-docx for .docx files. Every cell records which parser supplied it.

  python3 methods_table_check.py PAGE.md [PAGE.md ...] [--out DIR] [--all] [--prose]      check every markdown table of a vault page that has a source citation
  python3 methods_table_check.py --selftest                                                  offline tests (tests/test_methods_table_check.py runs the same checks)
  check_table(md_table, pdf_path, page, parsers=('mineru', 'pymupdf'))                       one table; returns the audit record (a dict)
  check_prose_numbers(sentence, pdf_path, page)                                              summarised tables: which numbers of the sentence are found on the page (pdf_pages.table_numbers)

A table of a vault page has a source citation when the page names its source ([[source/@key]]) and the table is introduced by a line that names it: 'Table 2' and/or a page ('p. 5', 'PDF page 5'),
or by a comment <!-- table-source: pdf_page=5 table=2 key=@key -->. The PDF page is found from an explicit page, else from the caption 'Table N', else from the page whose text holds most of the numbers of the copy.
Per cell the result is one of: exact; match_after_repair (equal after symbol repair, unicode dashes, case, spaces, markdown marks); number_format (same numbers, other format: 0.90 and .9);
match_in_merged_cell (the copy cell is part of a larger source cell) and match_split_or_joined_cells (the copy splits or joins source cells); text_differs (a source cell is found but differs;
both values are listed); missing_in_source (no source cell in the matched row); extra_in_copy (a copy row has no row in the source table). The audit record is JSON with paths relative to the vault."""
import argparse, datetime, difflib, hashlib, json, math, os, re, subprocess, sys, tempfile, time, unicodedata
from html.parser import HTMLParser
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz   # PyMuPDF
fitz.TOOLS.mupdf_display_errors(False)
import pdf_pages as pp

VAULT = pp.VAULT
BENCH = Path(os.environ.get('LIVES_BENCH') or Path.home() / '.cache' / 'lives-bench')
VENV_PY = Path(os.environ.get('METHODS_TABLE_VENV') or BENCH / 'venv-tables' / 'bin' / 'python')
CACHE = Path(os.environ.get('METHODS_TABLE_CACHE') or VAULT / 'pipeline' / 'misc' / 'evd-validation' / 'table-parsers' / 'cache')
OUT = VAULT / 'pipeline' / 'runs' / '_table_checks'
MATCHED = ('exact', 'match_after_repair', 'number_format', 'match_in_merged_cell', 'match_split_or_joined_cells')
RANK = {'exact': 0, 'match_after_repair': 1, 'number_format': 2, 'match_split_or_joined_cells': 3, 'match_in_merged_cell': 3, 'text_differs': 4, 'missing_in_source': 5, 'extra_in_copy': 6}


def rel(path):
    """Path relative to the vault (never an absolute home path); a path outside the vault is reduced to its file name."""
    p = Path(path).resolve()
    try: return str(p.relative_to(VAULT.resolve()))
    except ValueError: return p.name


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ markdown tables
def strip_md(cell):
    """Cell text of a markdown cell: wiki links, bold and italic marks, code ticks, <sup>, <br> and escaped bars removed."""
    t = cell.replace('\\|', '|')
    t = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'<br\s*/?>', ' ', t); t = re.sub(r'</?(sup|sub|b|i|em|strong|span)[^>]*>', '', t)
    t = re.sub(r'(\*\*|__|`)', '', t); t = re.sub(r'(?<![\w*])\*(?!\s)([^*]+)\*(?!\w)', r'\1', t)
    return ' '.join(t.split())


def parse_md_tables(text):
    """Markdown pipe tables of a text: [{'rows': [[cell,...],...], 'line': first line number (1-based), 'before': up to 3 lines above, 'after': up to 2 lines below}]; the separator row is dropped."""
    lines = text.splitlines(); out = []; i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|?\s*$', lines[i + 1]) and '-' in lines[i + 1]:
            j = i; rows = []
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                if j != i + 1:
                    raw = lines[j].strip().strip('|'); cells = [strip_md(c) for c in re.split(r'(?<!\\)\|', raw)]
                    rows.append(cells)
                j += 1
            out.append({'rows': rows, 'line': i + 1, 'before': [l for l in lines[max(0, i - 3):i]], 'after': lines[j:j + 2]}); i = j
        else: i += 1
    return out


def as_rows(md_table):
    """A table given as markdown text or as a list of rows -> list of rows of cell strings."""
    if isinstance(md_table, str):
        t = parse_md_tables(md_table)
        if t: return t[0]['rows']
        return [[strip_md(c) for c in l.strip().strip('|').split('|')] for l in md_table.splitlines() if l.strip()]
    return [[strip_md(str(c)) for c in r] for r in md_table]


# ------------------------------------------------------------------ cell normalisation and similarity
def _canon_num(s):
    s = s.replace(',', '').replace('+', '')
    neg = s.startswith('-'); s = s.lstrip('-')
    if s.startswith('.'): s = '0' + s
    if '.' in s: a, b = s.split('.', 1); s = (a.lstrip('0') or '0') + ('.' + b.rstrip('0') if b.rstrip('0') else '')
    else: s = s.lstrip('0') or '0'
    return ('-' if neg and s != '0' else '') + s


_RULE_TESTS = (('en_dash_stored_as_e', lambda t: not re.match(r'^\s*[-+]?\d+(\.\d+)?e[-+]?\d+\s*$', t) and re.search(r'(?<=[\d%)\]])e(?=[\d.])', t)),
               ('u0004_for_minus', lambda t: '\x04' in t), ('u0003_for_times', lambda t: '\x03' in t), ('thorn_for_plus', lambda t: '\u00fe' in t), ('quarter_for_equals', lambda t: '\u00bc' in t),
               ('private_use_digits', lambda t: re.search('[\uf130-\uf139]', t)), ('soft_hyphen', lambda t: '\u00ad' in t), ('ligature', lambda t: re.search('[\ufb00-\ufb04]', t)),
               ('unreadable_script', lambda t: re.search('[\u1780-\u17ff]', t)), ('bar_for_tilde', lambda t: re.search(r'(?<=[\s(])\|\s?(?=\d)', t)),
               ('superscript_exponent', lambda t: re.search(r'(\u00d7\s?10|(?<![\w.,])10)[\u00b9\u00b2\u00b3\u2070\u2074-\u2079\u207a\u207b]+(?![\w])', t)),
               ('flattened_power_of_ten', lambda t: not re.search('[A-Za-z]', t) and re.search(r'(?<![\w.,\^])10\u2212(\d{1,2})(?![\d\w])', t)))


def repair_with_rules(text):
    """pdf_pages.repair_cell_text with the names of the rules that changed the text (found by testing each rule's pattern on the input). Returns (text, [rule names])."""
    out, notes = pp.repair_cell_text_notes(text or ''); rules = [n for n, f in _RULE_TESTS if f(text or '')]
    if notes.get('footnotes'): rules.append('footnote_letter_removed')
    if notes.get('superscripts'): rules.append('superscript_footnote_removed')
    if re.search(r'(?<=[\d)])\s?5\s', text or '') and '\x03' in (text or ''): rules.append('five_for_equals')
    return out, sorted(set(rules)) if out != (text or '') else []


def ncell(text):
    """Normal form of a cell for comparison: symbol repair, NFKC, dashes and minus to '-', case folded, spaces collapsed, tilde and approximately signs equal."""
    t = pp.repair_cell_text(text or '')
    t = unicodedata.normalize('NFKC', t)
    t = re.sub('[‐-―−‒]', '-', t).replace(' ', ' ').replace('≈', '~')
    t = re.sub(r'\s+', ' ', t).strip().casefold()
    return re.sub(r'\s*([%,;:()\[\]/])\s*', r'\1', t)


def numbers(nt):
    """Canonical number tokens of a normalised cell, in order (a minus counts as a sign only at the start or after a space or bracket)."""
    return [_canon_num(m.group()) for m in re.finditer(r'(?:(?<![\w.)\]])-)?(?:\d[\d,]*(?:\.\d+)?|\.\d+)', nt)]


def skeleton(nt):
    return re.sub(r'\s+', '', re.sub(r'(?:(?<![\w.)\]])-)?(?:\d[\d,]*(?:\.\d+)?|\.\d+)', '#', nt))


def sim(a, b, contain=True):
    """Similarity 0..1 of two normalised cells: 1 when equal; 0.97 when only the number format differs; else the character ratio, with a containment bonus for a short cell inside a long one."""
    if a == b: return 1.0 if a else 0.0
    if not a or not b: return 0.0
    na, nb = numbers(a), numbers(b)
    if na and na == nb and skeleton(a) == skeleton(b): return 0.97
    r = difflib.SequenceMatcher(None, a, b).ratio()
    if contain and len(a) >= 3 and len(b) >= 3 and (a in b or b in a): r = max(r, 0.9 if min(len(a), len(b)) >= 4 else 0.0)
    if contain and len(a) >= 2 and len(b) > len(a) and a in b.split(' '): r = max(r, 0.85)   # a whole word of a larger cell
    return r


def pair_result(copy_raw, src_text, src_raw=None):
    """Kind of match for one copy cell and one source cell: ('exact'|'match_after_repair'|'number_format'|'text_differs', normalisations).
    src_text is the repaired source text and src_raw the text as the parser returned it; exact means equal to the raw text, so a cell that equals only after symbol repair is match_after_repair."""
    c, s = (copy_raw or '').strip(), (src_text or '').strip(); raw = (src_raw if src_raw is not None else src_text or '').strip()
    if c == raw: return 'exact', []
    if c == s and s != raw: return 'match_after_repair', repair_with_rules(raw)[1] or ['repair']
    nc, ns = ncell(c), ncell(s)
    if nc == ns:
        _, rules = repair_with_rules(s); _, rules_c = repair_with_rules(c)
        return 'match_after_repair', sorted(set(rules + rules_c)) or ['unicode_case_space']
    if numbers(nc) and numbers(nc) == numbers(ns) and skeleton(nc) == skeleton(ns): return 'number_format', ['number_format']
    return 'text_differs', []


# ------------------------------------------------------------------ source readers
def _html_grids(html):
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.t = []; s.cur = None; s.row = None; s.cell = None; s.d = 0
        def handle_starttag(s, tag, a):
            a = dict(a)
            if tag == 'table':
                s.d += 1
                if s.d == 1: s.cur = []
            elif tag == 'tr' and s.cur is not None: s.row = []
            elif tag in ('td', 'th') and s.row is not None: s.cell = []; s.sp = (int(a.get('colspan', 1) or 1), int(a.get('rowspan', 1) or 1))
            elif tag == 'br' and s.cell is not None: s.cell.append(' ')
        def handle_endtag(s, tag):
            if tag in ('td', 'th') and s.cell is not None: s.row.append((' '.join(''.join(s.cell).split()),) + s.sp); s.cell = None
            elif tag == 'tr' and s.row is not None: s.cur.append(s.row); s.row = None
            elif tag == 'table':
                s.d -= 1
                if s.d == 0 and s.cur is not None: s.t.append(s.cur); s.cur = None
        def handle_data(s, d):
            if s.cell is not None: s.cell.append(d)
    p = P(); p.feed(html); out = []
    for t in p.t:
        g = {}
        for r, row in enumerate(t):
            c = 0
            for txt, cs, rs in row:
                while (r, c) in g: c += 1
                for dr in range(rs):
                    for dc in range(cs): g[(r + dr, c + dc)] = txt
                c += cs
        if g:
            R = max(k[0] for k in g) + 1; C = max(k[1] for k in g) + 1; out.append([[g.get((r, c), '') for c in range(C)] for r in range(R)])
    return out


def _text_angle(page):
    import collections
    c = collections.Counter()
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            n = sum(len(s['text'].strip()) for s in l['spans'])
            if n: c[int(round(math.degrees(math.atan2(l['dir'][1], l['dir'][0])) / 90.0) * 90) % 360] += n
    return (c.most_common(1)[0][0], sum(c.values())) if c else (None, 0)


def derotated_page(page):
    """(upright copy of a page, info). Text-direction rule of table-parsers/derotate.py: the angle holding most characters; rotation 0 and content turned with show_pdf_page when needed.
    A page without a text layer is returned as it is (info['method'] = 'no-text-layer')."""
    ang, n = _text_angle(page); old = page.rotation
    d = fitz.open(); d.insert_pdf(page.parent, from_page=page.number, to_page=page.number); src = d[0]
    if ang is None or n < 20: return src, {'method': 'no-text-layer', 'angle_deg': None, 'old_rotation': old}
    src.set_rotation(0)
    if ang == 0: return src, {'method': 'text-direction', 'angle_deg': 0, 'old_rotation': old}
    w, h = src.rect.width, src.rect.height; swap = ang in (90, 270)
    d2 = fitz.open(); out = d2.new_page(width=(h if swap else w), height=(w if swap else h)); out.show_pdf_page(out.rect, d, 0, rotate=ang)
    return out, {'method': 'text-direction', 'angle_deg': ang, 'old_rotation': old, 'flattened': True}


def read_pymupdf_inprocess(pdf_path, page_no):
    """Tables of one page by PyMuPDF find_tables on the derotated page: [{'bbox': [x0,y0,x1,y1] in points, 'rows': [[repaired cell,...]], 'cells': [[{'text','raw','rules'}]], 'caption': ''}]."""
    doc = fitz.open(pdf_path); up, info = derotated_page(doc[page_no - 1]); tabs = []
    try: found = up.find_tables().tables
    except Exception: found = []
    for tb in found:
        raw = [[('' if c is None else ' '.join(str(c).split())) for c in row] for row in tb.extract()]
        if not any(any(r) for r in raw): continue
        cells = []; rows = []
        for row in raw:
            cr = []; tr = []
            for c in row:
                t, rules = repair_with_rules(c); cr.append({'text': t, 'raw': c, 'rules': rules}); tr.append(t)
            cells.append(cr); rows.append(tr)
        tabs.append({'bbox': [round(x, 1) for x in tb.bbox], 'rows': rows, 'cells': cells, 'caption': ''})
    return tabs, info, [round(up.rect.width, 1), round(up.rect.height, 1)]


_PYMUPDF_WORKER_NOTE = 'PyMuPDF 1.27 (the system python) finds far fewer tables than PyMuPDF 2.2 with pymupdf-layout (the table-parsers venv): 232 against 463 of the 463 verified values'


def read_pymupdf(pdf_path, page_no, sha=None, cache_dir=None):
    """PyMuPDF tables of one page. Run in the table-parsers virtual environment when it exists (PyMuPDF 2.2 with pymupdf-layout, cached per PDF hash and page), else in this process.
    Returns (tables, info, page_size, version string)."""
    sha = sha or sha256(pdf_path); cd = Path(cache_dir or CACHE) / 'pymupdf'; cd.mkdir(parents=True, exist_ok=True); f = cd / f'{sha}_p{page_no}.json'
    if f.exists():
        r = json.load(open(f)); return r['tables'], r['info'], r['size'], r['version']
    if VENV_PY.exists():
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parent)); tmp = tempfile.mktemp(suffix='.json')
        try:
            r = subprocess.run([str(VENV_PY), str(Path(__file__).resolve()), '--pymupdf-worker', str(pdf_path), str(page_no), tmp], capture_output=True, text=True, env=env, timeout=300)
            if not r.returncode and os.path.exists(tmp):
                res = json.load(open(tmp)); json.dump(res, open(f, 'w')); return res['tables'], res['info'], res['size'], res['version']
        except subprocess.TimeoutExpired: pass
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
    tabs, info, size = read_pymupdf_inprocess(pdf_path, page_no)
    return tabs, info, size, 'PyMuPDF ' + fitz.VersionBind + ' (this process)'


def pymupdf_worker(pdf_path, page_no, out_json):
    tabs, info, size = read_pymupdf_inprocess(pdf_path, page_no); json.dump({'tables': tabs, 'info': info, 'size': size, 'version': 'PyMuPDF ' + fitz.VersionBind}, open(out_json, 'w'))


def mineru_worker(pdf_path, page_no, out_json):
    """Runs inside the table-parsers virtual environment: derotate the page, read it with MinerU (basic tier, local models), write {'page_size','tables':[{'bbox_norm','caption','html','rows'}]}."""
    from mineru.parser import parse
    doc = fitz.open(pdf_path); up, info = derotated_page(doc[page_no - 1])
    tmp = tempfile.mkdtemp(prefix='mtc_'); fn = os.path.join(tmp, 'p.pdf'); up.parent.save(fn)
    r = parse(fn, tier='basic', ocr_mode='auto', image_analysis=False, page_range='1'); mj = r.middle_json.to_dict(); tabs = []
    def texts(o, kinds):
        out = []
        def w(x, on):
            if isinstance(x, dict):
                on2 = on or x.get('type') in kinds
                if on2 and x.get('type') == 'text' and isinstance(x.get('content'), str): out.append(x['content'])
                for v in x.values(): w(v, on2)
            elif isinstance(x, list):
                for v in x: w(v, on)
        w(o, False); return ' '.join(out)
    def walk(o):
        if isinstance(o, dict):
            if o.get('type') == 'table':
                body = []
                def find(x):
                    if isinstance(x, dict):
                        if x.get('type') == 'table_body' and isinstance(x.get('content'), str): body.append(x['content'])
                        for v in x.values(): find(v)
                    elif isinstance(x, list):
                        for v in x: find(v)
                find(o)
                for h in body:
                    for g in _html_grids(h) or [[]]:
                        tabs.append({'bbox_norm': o.get('bbox'), 'caption': texts(o, ('table_caption',)), 'footnote': texts(o, ('table_footnote',)), 'html': h, 'rows': g})
                return
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(mj['pages'])
    json.dump({'page_size': [up.rect.width, up.rect.height], 'derotate': info, 'tables': tabs}, open(out_json, 'w'))


def read_mineru(pdf_path, page_no, sha=None, cache_dir=None):
    """MinerU tables of one page; cached per (PDF sha256, page). Returns (result dict or None, status, seconds). status: cached | run | not available | error: ..."""
    sha = sha or sha256(pdf_path); cd = Path(cache_dir or CACHE) / 'mineru'; cd.mkdir(parents=True, exist_ok=True); f = cd / f'{sha}_p{page_no}.json'
    if f.exists(): return json.load(open(f)), 'cached', 0.0
    if not VENV_PY.exists(): return None, 'not available (no table-parsers virtual environment)', 0.0
    env = dict(os.environ, HF_HOME=str(BENCH / 'mc' / 'hf'), XDG_CACHE_HOME=str(BENCH / 'mc' / 'cache'), MODELSCOPE_CACHE=str(BENCH / 'mc' / 'ms'), MINERU_HOME=str(BENCH / 'mc' / 'mineru-home'),
               MINERU_TELEMETRY_DISABLED='1', HF_HUB_DISABLE_TELEMETRY='1', PYTHONPATH=str(Path(__file__).resolve().parent))
    t = time.time(); tmp = tempfile.mktemp(suffix='.json')
    try:
        r = subprocess.run([str(VENV_PY), str(Path(__file__).resolve()), '--mineru-worker', str(pdf_path), str(page_no), tmp], capture_output=True, text=True, env=env, timeout=1200)
        if r.returncode or not os.path.exists(tmp): return None, 'error: ' + (r.stderr or r.stdout)[-200:].replace(str(Path.home()), '~'), round(time.time() - t, 1)
        res = json.load(open(tmp)); json.dump(res, open(f, 'w')); return res, 'run', round(time.time() - t, 1)
    except subprocess.TimeoutExpired: return None, 'error: timeout 1200 s', round(time.time() - t, 1)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def mineru_tables(res, page_w_h=None):
    """MinerU result -> tables in the same shape as read_pymupdf (bbox in points of the derotated page)."""
    W, H = res['page_size']; out = []
    for t in res['tables']:
        b = t.get('bbox_norm') or [0, 0, 1, 1]
        cells = []; rows = []
        for row in t['rows']:
            cr = []; tr = []
            for c in row:
                txt, rules = repair_with_rules(c); cr.append({'text': txt, 'raw': c, 'rules': rules}); tr.append(txt)
            cells.append(cr); rows.append(tr)
        out.append({'bbox': [round(b[0] * W, 1), round(b[1] * H, 1), round(b[2] * W, 1), round(b[3] * H, 1)], 'rows': rows, 'cells': cells, 'caption': t.get('caption', ''), 'footnote': t.get('footnote', '')})
    return out


# ------------------------------------------------------------------ alignment
def _cands(cells):
    """Source cells of a row as candidates: single non-empty cells, and joins of 2 and 3 neighbouring non-empty cells. [(start, end, text_raw, normalised)]"""
    idx = [i for i, c in enumerate(cells) if c['text'].strip()]; out = []
    for a in range(len(idx)):
        for n in (1, 2, 3):
            if a + n > len(idx): break
            sl = idx[a:a + n]; raw = ' '.join(cells[i]['text'] for i in sl)
            out.append((a, a + n, sl, raw, ncell(raw)))
    return out, idx


def align_row(copy_row, src_cells):
    """Needleman-Wunsch between the copy cells and the source cells of a row; a copy cell may match one source cell, a join of 2 or 3 neighbours, and 2 copy cells may match one source cell.
    Returns a list per copy cell: {'src': [source column indexes], 'kind_hint': 'one'|'join'|'split', 'sim'} or None (no counterpart). Empty copy cells are returned as 'empty'."""
    cc = [ncell(c) for c in copy_row]; ci = [i for i, c in enumerate(cc) if c]
    cand, idx = _cands(src_cells); m, n = len(ci), len(idx)
    byA = {}
    for c in cand: byA.setdefault(c[0], []).append(c)
    GAP = 0.3; NEG = -1e9
    # dp[i][j]: best score using first i copy cells and first j source cells
    dp = [[NEG] * (n + 1) for _ in range(m + 1)]; bt = [[None] * (n + 1) for _ in range(m + 1)]; dp[0][0] = 0
    for i in range(m + 1):
        for j in range(n + 1):
            if dp[i][j] == NEG: continue
            v = dp[i][j]
            if i < m and v - GAP > dp[i + 1][j]: dp[i + 1][j] = v - GAP; bt[i + 1][j] = (i, j, None)
            if j < n and v - GAP * 0.5 > dp[i][j + 1]: dp[i][j + 1] = v - GAP * 0.5; bt[i][j + 1] = (i, j, 'skip')
            if i < m:
                for (a, b, sl, raw, nr) in byA.get(j, []):
                    s = sim(cc[ci[i]], nr, contain=(b - a == 1))
                    if s >= 0.5 and v + s > dp[i + 1][b]: dp[i + 1][b] = v + s; bt[i + 1][b] = (i, j, ('one' if b - a == 1 else 'join', sl, s))
                if i + 1 < m and j < n:
                    jc = (cc[ci[i]] + ' ' + cc[ci[i + 1]]).strip(); s = sim(jc, ncell(src_cells[idx[j]]['text']), contain=False)
                    if s >= 0.85 and v + 2 * s > dp[i + 2][j + 1]: dp[i + 2][j + 1] = v + 2 * s; bt[i + 2][j + 1] = (i, j, ('split', [idx[j]], s))
    res = {}; i, j = m, n
    while i > 0 or j > 0:
        pi, pj, how = bt[i][j]
        if isinstance(how, tuple):
            kind, sl, s = how
            if kind == 'split': res[ci[pi]] = {'src': sl, 'hint': 'split', 'sim': s}; res[ci[pi + 1]] = {'src': sl, 'hint': 'split', 'sim': s}
            else: res[ci[pi]] = {'src': sl, 'hint': kind, 'sim': s}
        i, j = pi, pj
    out = []
    for k, c in enumerate(cc): out.append('empty' if not c else res.get(k))
    # second chance for unmatched copy cells: any unused source cell of the row, order ignored
    used = {s for r in res.values() for s in r['src']}
    for k, r in enumerate(out):
        if r is None:
            best = None
            for si, sc in enumerate(src_cells):
                if si in used or not sc['text'].strip(): continue
                s = sim(cc[k], ncell(sc['text']))
                if s >= 0.8 and (best is None or s > best[1]): best = (si, s)
            if best: out[k] = {'src': [best[0]], 'hint': 'reordered', 'sim': best[1]}; used.add(best[0])
    return out


def row_score(copy_row, src_cells):
    cc = [ncell(c) for c in copy_row if ncell(c)]
    if not cc: return 0.0
    cand, _ = _cands(src_cells)
    if not cand: return 0.0
    return sum(max((sim(c, x[4], contain=(x[1] - x[0] == 1)) for x in cand), default=0.0) for c in cc) / len(cc)


def table_score(copy_rows, src_rows_cells):
    """How well a source table fits the copy: mean over copy rows of the best row score."""
    sc = [max((row_score(r, sr) for sr in src_rows_cells), default=0.0) for r in copy_rows]
    return sum(sc) / len(sc) if sc else 0.0


def align_table(copy_rows, src_table):
    """Cell-by-cell alignment of the copy with one source table. Returns {(i, j): result dict} for every copy cell."""
    srows = src_table['cells']; n_s = len(srows)
    nc = max(len(copy_rows), 1)
    scores = [[row_score(cr, sr) - 0.04 * abs(i / nc - k / max(n_s, 1)) for k, sr in enumerate(srows)] for i, cr in enumerate(copy_rows)]   # small bonus for the same relative position: identical-looking rows pair in order
    pairs = sorted(((scores[i][k], i, k) for i in range(len(copy_rows)) for k in range(n_s)), reverse=True)
    rowmap = {}; used = set()
    for s, i, k in pairs:
        if s < 0.5: break
        if i in rowmap or k in used: continue
        rowmap[i] = k; used.add(k)
    for i in range(len(copy_rows)):   # second pass: a source row that holds several lines in one cell may serve several copy rows
        if i not in rowmap and n_s:
            k = max(range(n_s), key=lambda k: scores[i][k])
            if scores[i][k] >= 0.6: rowmap[i] = k
    out = {}
    for i, cr in enumerate(copy_rows):
        if i not in rowmap:
            for j, c in enumerate(cr):
                out[(i, j)] = {'result': 'empty' if not ncell(c) else 'extra_in_copy', 'copy': c}
            continue
        sc = srows[rowmap[i]]; al = align_row(cr, sc)
        for j, c in enumerate(cr):
            a = al[j] if j < len(al) else None
            if a == 'empty': out[(i, j)] = {'result': 'empty', 'copy': c}; continue
            if a is None: out[(i, j)] = {'result': 'missing_in_source', 'copy': c, 'src_row': rowmap[i]}; continue
            cells = [sc[s] for s in a['src']]; raw = ' '.join(x['text'] for x in cells)
            kind, norm = pair_result(c, raw, ' '.join(x['raw'] for x in cells))
            if a['hint'] == 'split' and kind != 'exact': kind = 'match_split_or_joined_cells'; norm = ['copy splits a source cell']
            elif a['hint'] == 'join' and kind in ('text_differs',) : kind = 'text_differs'
            elif a['hint'] == 'join' and kind != 'exact': kind = 'match_split_or_joined_cells'; norm = ['copy joins source cells']
            if kind == 'text_differs' and a['sim'] >= 0.85 and ncell(c) in ncell(raw) and (len(ncell(c)) >= 4 or ncell(c) in ncell(raw).split(' ')): kind = 'match_in_merged_cell'; norm = ['copy cell is part of a larger source cell']
            if kind == 'text_differs' and a['sim'] < 0.5: kind = 'missing_in_source'
            out[(i, j)] = {'result': kind, 'copy': c, 'source': raw, 'src_row': rowmap[i], 'src_cols': a['src'], 'normalizations': norm, 'rules': sorted({r for x in cells for r in x['rules']}), 'hint': a['hint']}
    return out, rowmap


# ------------------------------------------------------------------ the check
def locate_page(pdf_path, rows, table_no=None):
    """PDF page (1-based) and how it was found: 'caption' ('Table N' line start with a good overlap) or 'overlap' (the page whose text holds most of the numbers of the copy)."""
    doc = fitz.open(pdf_path); toks = {t for r in rows for c in r for t in numbers(ncell(c)) if len(t.replace('.', '').replace('-', '')) >= 2}
    best = (0, None, None)
    for i, p in enumerate(doc):
        text = ncell(p.get_text()); have = sum(1 for t in toks if re.search(r'(?<![\d.])' + re.escape(t) + r'(?!\d)', text.replace(',', '')))
        frac = have / len(toks) if toks else 0
        cap = bool(table_no and re.search(r'(?m)^\s*table\s+' + re.escape(str(table_no).lower()) + r'\s*[.:]', p.get_text().casefold()))
        score = frac + (0.5 if cap else 0)
        if score > best[0]: best = (score, i + 1, 'caption' if cap else 'overlap')
    return best[1], best[2]


def check_table(md_table, pdf_path, page=None, parsers=('mineru', 'pymupdf'), table_no=None, origin=None, out_dir=None, crop=True, cache_dir=None):
    """Check one table. md_table: markdown text or list of rows; pdf_path: the source PDF (or a .docx); page: 1-based PDF page (None: located from table_no or from the numbers);
    parsers: order of preference. Returns the audit record (a dict, JSON-able, paths relative to the vault). With out_dir the record and the crop image are written there."""
    t0 = time.time(); rows = as_rows(md_table); pdf_path = Path(pdf_path); sha = sha256(pdf_path)
    rec = {'schema': 1, 'tool': 'scripts/methods_table_check.py', 'date': datetime.date.today().isoformat(),
           'source': {'file': rel(pdf_path), 'sha256': sha, 'type': pdf_path.suffix.lower().lstrip('.')}, 'copy': {'origin': origin, 'rows': len(rows), 'cols': max((len(r) for r in rows), default=0)}, 'parsers': {}}
    if pdf_path.suffix.lower() == '.docx':
        tabs = pp.docx_tables(str(pdf_path)); cand = [{'bbox': None, 'rows': t, 'cells': [[{'text': c, 'raw': c, 'rules': []} for c in r] for r in t], 'caption': ''} for t in tabs]
        sources = {'python-docx': cand}; rec['source'].update({'pdf_page': None, 'printed_page': None, 'page_source': 'docx has no pages'}); up = None
    else:
        doc = fitz.open(pdf_path); ps = 'explicit'
        if page is None: page, ps = locate_page(pdf_path, rows, table_no)
        if page is None: rec['error'] = 'page not found'; return rec
        pm = {r['pdf']: r['printed'] for r in pp.page_map(doc)}
        rec['source'].update({'pdf_page': page, 'printed_page': pm.get(page), 'page_source': ps, 'table_number': table_no})
        sources = {}; up, info = derotated_page(doc[page - 1]); rec['source']['derotation'] = info
        for p in parsers:
            if p == 'mineru':
                res, st, sec = read_mineru(str(pdf_path), page, sha, cache_dir); rec['parsers']['mineru'] = {'status': st, 'seconds': sec}
                if res: sources['mineru'] = mineru_tables(res)
            elif p == 'pymupdf':
                t = time.time(); tabs, info, wh, ver = read_pymupdf(str(pdf_path), page, sha, cache_dir); sources['pymupdf'] = tabs; rec['parsers']['pymupdf'] = {'status': 'run', 'seconds': round(time.time() - t, 2), 'version': ver}
    chosen = {}
    for p, tabs in sources.items():
        if not tabs: rec['parsers'].setdefault(p, {})['tables_on_page'] = 0; continue
        sc = []
        for k, t in enumerate(tabs):
            s = table_score(rows, t['cells'])
            if table_no and re.search(r'table\s+' + re.escape(str(table_no)) + r'\b', t.get('caption', ''), re.I): s += 0.3
            sc.append((s, k))
        s, k = max(sc); rec['parsers'].setdefault(p, {}).update({'tables_on_page': len(tabs), 'chosen_table': k, 'table_match_score': round(min(s, 1.0), 3)})
        chosen[p] = (tabs[k], *align_table(rows, tabs[k]))
    order = [p for p in list(parsers) + ['python-docx'] if p in chosen]
    cells = []; per = collections_counter()
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            opts = {p: chosen[p][1][(i, j)] for p in order}
            if not opts: cells.append({'row': i, 'col': j, 'copy': c, 'result': 'missing_in_source', 'parser': None}); continue
            best_p = min(order, key=lambda p: (RANK.get(opts[p]['result'], 9), order.index(p))); o = opts[best_p]
            if o['result'] == 'empty': continue
            entry = {'row': i, 'col': j, 'copy': c, 'result': o['result'], 'parser': best_p if o['result'] not in ('extra_in_copy', 'missing_in_source') else None}
            if 'source' in o: entry.update({'source': o['source'], 'source_pos': [o['src_row'], o['src_cols']], 'normalizations': o.get('normalizations', []), 'repair_rules': o.get('rules', [])})
            entry['alternates'] = {p: opts[p]['result'] for p in order if p != best_p}
            if len(order) > 1:
                srcs = {p: opts[p].get('source') for p in order if 'source' in opts[p]}
                if len({ncell(v) for v in srcs.values()}) > 1: entry['parser_texts'] = srcs
            cells.append(entry); per[entry['result']] += 1
    mism = [{'row': e['row'], 'col': e['col'], 'copy': e['copy'], 'source': e.get('source'), 'result': e['result'], 'parser': e.get('parser')} for e in cells if e['result'] in ('text_differs', 'missing_in_source', 'extra_in_copy')]
    nsrc = 0
    if order:
        tb, al, rm = chosen[order[0]]; nsrc = sum(1 for r in tb['cells'] for c in r if c['text'].strip())
    total = len(cells); matched = sum(per[k] for k in MATCHED)
    rec['cells'] = cells
    rec['summary'] = {'cells': total, 'matched': matched, 'matched_share': round(matched / total, 3) if total else None, 'by_result': dict(per), 'mismatches': mism,
                      'weak_matches': per['match_in_merged_cell'] + per['match_split_or_joined_cells'], 'source_cells_in_chosen_table': nsrc, 'parser_used_for_rows': order[0] if order else None}
    if order:
        tb = chosen[order[0]][0]; rec['source']['table_bbox_points'] = tb['bbox']; rec['source']['bbox_parser'] = order[0]
        rec['source']['table_caption'] = tb.get('caption') or ''
    rec['seconds'] = round(time.time() - t0, 2)
    if out_dir is not None and up is not None and rec['source'].get('table_bbox_points') and crop:
        od = Path(out_dir); od.mkdir(parents=True, exist_ok=True); b = rec['source']['table_bbox_points']
        stem = f"{sha[:10]}_p{rec['source']['pdf_page']}_{table_no or 't'}_{hashlib.md5(json.dumps(rows).encode()).hexdigest()[:6]}"
        r = fitz.Rect(b) + (-10, -10, 10, 10); r &= up.rect; up.get_pixmap(dpi=130, clip=r).save(str(od / (stem + '.png')))
        rec['crop'] = rel(od / (stem + '.png'))
    if out_dir is not None:
        od = Path(out_dir); od.mkdir(parents=True, exist_ok=True); stem = f"{sha[:10]}_p{rec['source'].get('pdf_page')}_{table_no or 't'}_{hashlib.md5(json.dumps(rows).encode()).hexdigest()[:6]}"
        (od / (stem + '.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding='utf-8'); rec['record'] = rel(od / (stem + '.json'))
    return rec


def collections_counter():
    import collections
    return collections.Counter()


# ------------------------------------------------------------------ prose
def check_prose_numbers(sentence, pdf_path, page):
    """Summarised table (prose): the numbers written in the sentence and which of them are on the source page in a table cell or in a table caption or footnote (pdf_pages.table_numbers).
    Returns {'numbers': [{'text','found'}], 'found': n, 'not_found': [..]}; a found number is a hint, not proof that it is the right cell."""
    page_obj = fitz.open(pdf_path)[page - 1]; have = pp.table_numbers(page_obj); res = []
    for m in re.finditer(r'(?<![\w.])[-+]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)%?', sentence):
        s = m.group(); ns = pp._number_set(s); res.append({'text': s, 'found': bool(ns & have)})
    return {'numbers': res, 'found': sum(r['found'] for r in res), 'not_found': [r['text'] for r in res if not r['found']]}


# ------------------------------------------------------------------ vault pages
def source_of_page(text):
    m = re.search(r'\[\[(?:source/)?(@[^\]|#]+)', text)
    return m.group(1) if m else None


def citation_of_table(t, text_all):
    """(page or None, printed page or None, table number or None, found) from the lines around a table or a table-source comment."""
    ctx = ' '.join(t['before'][-3:] + t['after'][:1])
    m = re.search(r'<!--\s*table-source:([^>]*)-->', ' '.join(t['before'] + t['after']))
    if m:
        kv = dict(re.findall(r'(\w+)=(\S+)', m.group(1))); return (int(kv['pdf_page']) if 'pdf_page' in kv else None, None, kv.get('table'), kv.get('key') or True)
    tn = re.search(r'\bTable\s+(S?\d+)', ctx, re.I); pdfp = re.search(r'(?:PDF\s+page|pdf_page|pdf p\.?)\s*[:=]?\s*(\d+)', ctx, re.I); pr = re.search(r'\bpp?\.\s*(\d+)', ctx)
    if tn or pdfp or pr: return (int(pdfp.group(1)) if pdfp else None, int(pr.group(1)) if pr and not pdfp else None, tn.group(1) if tn else None, True)
    return None, None, None, False


def check_vault_page(path, out_dir=None, all_tables=False, parsers=('mineru', 'pymupdf'), prose=False):
    """Check every markdown table of a vault page that has a source citation; returns {'page': rel path, 'source': citekey, 'tables': [records], 'skipped': [...], 'prose': [...]}."""
    path = Path(path); text = path.read_text(encoding='utf-8'); key = source_of_page(text); out = {'page': rel(path), 'source': key, 'tables': [], 'skipped': [], 'prose': []}
    pdf = pp.resolve_pdf(key) if key else None
    if not pdf: out['skipped'].append('no source with a resolvable PDF on the page'); return out
    doc = fitz.open(pdf); pm = {r['printed']: r['pdf'] for r in pp.page_map(doc) if r['printed']}
    for t in parse_md_tables(text):
        pg, printed, tno, found = citation_of_table(t, text)
        if not found and not all_tables: out['skipped'].append({'line': t['line'], 'reason': 'no source citation next to the table (use --all to try)'}); continue
        if pg is None and printed is not None: pg = int(pm[str(printed)]) if str(printed) in pm else None
        out['tables'].append(check_table(t['rows'], pdf, pg, parsers, table_no=tno, origin=f"{rel(path)}:{t['line']}", out_dir=out_dir))
    if prose:
        in_table = {i for t in parse_md_tables(text) for i in range(t['line'] - 3, t['line'] + len(t['rows']) + 2)}   # table rows and the three lines above (the citation line)
        for n, line in enumerate(text.splitlines(), 1):
            m = re.search(r'\bTable\s+(S?\d+)', line)
            if m and n not in in_table and re.search(r'\d', line.replace(m.group(), '')) and not line.lstrip().startswith('|'):
                pg, _ = locate_page(pdf, [[line]], m.group(1)); out['prose'].append({'line': n, 'table': m.group(1), 'pdf_page': pg, **check_prose_numbers(re.sub(r'\b(?:PDF\s+)?pp?\.\s*\d+', ' ', line.replace(m.group(), ' ')), pdf, pg)})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('pages', nargs='*'); ap.add_argument('--out', default=str(OUT)); ap.add_argument('--all', action='store_true')
    ap.add_argument('--prose', action='store_true'); ap.add_argument('--parsers', default='mineru,pymupdf'); ap.add_argument('--mineru-worker', nargs=3, metavar=('PDF', 'PAGE', 'OUT')); ap.add_argument('--pymupdf-worker', nargs=3, metavar=('PDF', 'PAGE', 'OUT')); ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.mineru_worker: mineru_worker(a.mineru_worker[0], int(a.mineru_worker[1]), a.mineru_worker[2]); return
    if a.pymupdf_worker: pymupdf_worker(a.pymupdf_worker[0], int(a.pymupdf_worker[1]), a.pymupdf_worker[2]); return
    if a.selftest:
        sys.path.insert(0, str(Path(__file__).resolve().parent / 'tests')); import test_methods_table_check as T; sys.exit(T.run())
    for p in a.pages:
        r = check_vault_page(p, a.out, a.all, tuple(a.parsers.split(',')), a.prose)
        print(f"{r['page']}: source {r['source']}; {len(r['tables'])} table(s) checked, {len(r['skipped'])} skipped")
        for t in r['tables']:
            s = t['summary']; print(f"  {t['copy']['origin']} -> PDF page {t['source'].get('pdf_page')} (printed {t['source'].get('printed_page')}): {s['matched']}/{s['cells']} cells matched {s['by_result']} {t.get('seconds')} s")
            for m in s['mismatches'][:10]: print(f"    {m['result']}: row {m['row']} col {m['col']} copy {m['copy']!r} source {m['source']!r} ({m['parser']})")
        for x in r['prose']: print(f"  prose line {x['line']} Table {x['table']}: {x['found']}/{len(x['numbers'])} numbers found; not found {x['not_found']}")


if __name__ == '__main__': main()

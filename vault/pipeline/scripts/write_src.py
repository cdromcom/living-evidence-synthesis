#!/usr/bin/env python3
"""Writes the SRC (source) page of a paper with GPT-6.2 Sol, in batch mode, then checks the page without a model (JP, 2026-11-27).

  python3 write_src.py RUN_ID [--paper CITEKEY] [--mode batch] [--out DIR] [--cap-usd 1.0] [--parsers mineru,pymupdf]

Inputs come from pipeline/runs/<RUN_ID>/: manifest.json, <paper>/picost.json (findings with numbers and spans), <paper>/drafts.json (the drafted EVD, QUE, CLM and CVT nodes with ids),
<paper>/checks.json (what the checks said about each finding), table-check records of the PDF if any, and the PDF text (pdf_pages). The model is roles.src_writer in config/models.json
(stage 'src_write', prompt prompts/src-write-v2.md, batch API only; all papers of the run, or the one named by --paper, go in one batch). A second batch (roles.src_judge, Gemini 4 Neon, prompt src-judge-v1) judges each Findings bullet against its EVD node and the extraction. Nothing here writes to sysrev/.
Output (default pipeline/misc/src-test-2026-11-27/): <citekey>.md (front matter 'status: test, not validated') and <citekey>.audit.json (every check result, and the flags for a human to examine).
The answers are saved in the run folder (<paper>/src_write_response.json, <paper>/src_judge_response.json, runs/<run>/<stage>_job.json) and labeled in the manifest stage_log with a note; running the script again re-checks the saved answer and makes no new call.

Checks (deterministic, no model): writing rules (lives_stages.writing_rules plus the skimmability rules of Skill-templates.md); every number of the page found in the paper (pdf_pages: page text and
table_numbers); every quoted passage located in the PDF (pdf_pages.find_quote) on the page cited; every node id linked exists in the run; every table or figure cited has a screenshot placeholder
whose PDF page holds its caption; every sentence with a number cites a table, figure or page, and each of its numbers is printed on the cited page (table cells for a table); one or two Methods tables are copied; every markdown table with a source citation compared cell by cell with the PDF (methods_table_check.check_table)."""
import argparse, collections, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import call_logger as cl, config as C, llm_batch as L, pdf_pages as pp, methods_table_check as M, node_names as N, src_crops as K, src_sections as X
import fitz
fitz.TOOLS.mupdf_display_errors(False)

VAULT = cl.VAULT
STAGE = 'src_write'; PROMPT_FILE = 'pipeline/prompts/src-write-v3.md'; PROMPT_ID = 'src-write-v3'
JUDGE_STAGE = 'src_judge'; JUDGE_PROMPT_FILE = 'pipeline/prompts/src-judge-v1.md'; JUDGE_PROMPT_ID = 'src-judge-v1'
JUDGE_ROLE = C.ROLES['src_judge']; JUDGE_MODEL = C.role_model(JUDGE_ROLE); JUDGE_EFFORT = C.role_effort(JUDGE_ROLE, 'medium'); JUDGE_MAX_TOKENS = 16000
SRC_ROLE = C.ROLES['src_writer']; SRC_MODEL = C.role_model(SRC_ROLE); SRC_EFFORT = C.role_effort(SRC_ROLE, 'medium')
MAX_TOKENS = 30000   # Sol's reasoning counts against the output budget
OUT_DEFAULT = VAULT / 'pipeline' / 'misc' / 'src-test-2026-11-27'
NODE_TYPE_OF_PREFIX = {'E': 'EVD', 'Q': 'QUE', 'C': 'CLM', 'V': 'CVT'}
EMOJI = {'Question': '❓', 'Methods': '🔬', 'Findings': '📊', 'Claim supported': '💡', 'Caveats': '🚧', 'Not reported': '📭'}   # one emoji per subheading (JP, 2026-11-27)
HEADINGS = [f'### {e} {n}' for n, e in EMOJI.items()]
SUMMARY_WORDS = (100, 125)


def rel(p):
    return M.rel(p)


# ------------------------------------------------------------------ inputs
def vault_citekey(doi, fallback):
    """The vault citekey of the paper (from the DOI of an existing source page, read only), else the run's folder name."""
    if doi:
        for f in (VAULT / 'source').glob('@*.md'):
            head = f.read_text(encoding='utf-8')[:6000]
            m = re.search(r'^doi:\s*"?([^\s"]+)', head, re.M)
            if m and m.group(1).lower() == doi.lower(): return f.stem.lstrip('@')
    return fallback


def pdf_pages_text(doc):
    pm = {r['pdf']: r['printed'] for r in pp.page_map(doc)}
    return '\n\n'.join(f"[PDF page {i + 1} | printed page {pm.get(i + 1)}]\n{pp.page_text(p)}" for i, p in enumerate(doc))


def slim_finding(f):
    out = {k: f.get(k) for k in ('id', 'tier', 'answers_QUE', 'supports', 'section', 'statement', 'P', 'I', 'C', 'O', 'S', 'T', 'numbers', 'notes')}
    out['spans'] = [{'text': s.get('text'), 'pdf_page': s.get('pdf_page'), 'printed_page': s.get('printed_page')} for s in f.get('spans', [])]
    return out


def load_table_audits(sha):
    """Earlier cell-by-cell table checks of this PDF (runs/_table_checks/<sha10>_*.json), reduced to a summary line each."""
    out = []
    for f in sorted((C.VAULT / 'pipeline' / 'runs' / '_table_checks').glob(f'{sha[:10]}_*.json')) if (C.VAULT / 'pipeline' / 'runs' / '_table_checks').exists() else []:
        try:
            r = json.loads(f.read_text(encoding='utf-8')); s = r.get('summary', {})
            out.append({'table': r['source'].get('table_number'), 'pdf_page': r['source'].get('pdf_page'), 'cells': s.get('cells'), 'matched': s.get('matched'), 'mismatches': s.get('mismatches', [])[:5]})
        except Exception: pass
    return out


def load_inputs(run_id, paper=None):
    rd = cl.RUNS / run_id; man = json.loads((rd / 'manifest.json').read_text(encoding='utf-8'))
    keys = list(man['papers']); paper = paper or keys[0]
    if paper not in man['papers']: raise SystemExit(f'paper {paper} is not in run {run_id}; the run has {keys}')
    pdir = rd / paper; ps = json.loads((pdir / 'picost.json').read_text(encoding='utf-8')); dr = json.loads((pdir / 'drafts.json').read_text(encoding='utf-8'))
    ck_f = pdir / 'checks.json'; checks = json.loads(ck_f.read_text(encoding='utf-8')) if ck_f.exists() else []
    pdf = Path(str(man['papers'][paper].get('pdf', '')).replace('~', str(Path.home()), 1))
    if not pdf.exists(): raise SystemExit('the PDF named in the manifest was not found on this machine')
    nodes = {}
    for k, v in dr['finals'].items():
        n = dict(v['node']); n['review_status'] = v.get('status'); nodes[n['id']] = n
    return {'run_dir': rd, 'paper_dir': pdir, 'paper_key': paper, 'manifest': man, 'picost': ps, 'nodes': nodes, 'checks': checks, 'pdf': pdf}


def build_user_text(inp, citekey, doc):
    ps = inp['picost']; nodes = []
    for n in inp['nodes'].values():
        d = {k: v for k, v in n.items() if k not in ('source_id',)}; d['id'] = n['id']; nodes.append(d)
    ck = [{'finding': c['id'], 'tier': c.get('tier'), 'final': c.get('final'), 'reason': (c.get('sol') or {}).get('reason'), 'decision_model_score': (c.get('summary') or {}).get('score')} for c in inp['checks']]
    pdf_sha = M.sha256(inp['pdf'])
    parts = ['PAPER\n' + json.dumps({**ps['paper'], 'vault_citekey': citekey}, ensure_ascii=False),
             'PDF_PAGES\n' + pdf_pages_text(doc),
             'FINDINGS\n' + json.dumps({'findings': [slim_finding(f) for f in ps['findings']], 'not_reported': ps.get('not_reported', [])}, ensure_ascii=False),
             'NODES\n' + json.dumps(nodes, ensure_ascii=False),
             'CHECKS\n' + json.dumps(ck, ensure_ascii=False),
             'TABLE_AUDITS\n' + (json.dumps(load_table_audits(pdf_sha), ensure_ascii=False) or '[]')]
    return '\n\n=====\n\n'.join(parts)


def system_prompt(file=None):
    t = (VAULT / (file or PROMPT_FILE)).read_text(encoding='utf-8')
    return t.split('---', 2)[2].strip() if t.startswith('---') else t


# ------------------------------------------------------------------ links
def resolve_links(text, nodes):
    """Turns [[E-F4]] into a vault link to the node, written as [[sysrev/dgraph/evidence/EVD - <title>|EVD E-F4]]. Returns (text, used ids, unknown links). Unknown ids stay as typed so a reader sees them."""
    used, unknown = [], []
    def sub(m):
        i = m.group(1).strip()
        if i in nodes: used.append(i); return N.node_link(nodes[i])
        unknown.append(m.group(0)); return m.group(0)
    out = re.sub(r'\[\[([^\]|\n]+)\]\]', sub, text)   # an embed ![[...]] has a dot in its name and is left alone below
    return out, used, unknown


def resolve_links_keep_embeds(text, nodes):
    """As resolve_links, but a screenshot embed (![[...png]]) is never treated as a node link."""
    keep = []; hold = lambda m: (keep.append(m.group(0)) or f'\x01{len(keep) - 1}\x01')
    t = re.sub(r'!\[\[[^\]]*\]\]', hold, text); t, used, unknown = resolve_links(t, nodes)
    return re.sub(r'\x01(\d+)\x01', lambda m: keep[int(m.group(1))], t), used, unknown


# ------------------------------------------------------------------ checks on the page
NUM_RE = re.compile(r'(?<![\w.])[-+]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)')


def clean_pdf_text(s):
    return re.sub(r'(?<=\d)e(?=\d)', ' ', s)   # the text layer of some PDFs turns an en dash between numbers into the letter e


def paper_numbers(doc):
    """{normalized number: sorted PDF pages} from the page text and from table cells, captions and footnotes (pdf_pages.table_numbers)."""
    where = collections.defaultdict(set)
    for i, p in enumerate(doc):
        for n in pp._number_set(clean_pdf_text(pp.page_text(p))): where[n].add(i + 1)
        try:
            for n in pp.table_numbers(p): where[n].add(i + 1)
        except Exception: pass
    return {k: sorted(v) for k, v in where.items()}


def prose_for_numbers(body):
    """(cleaned line, original line) pairs: the text whose numbers are checked against the paper: no node links, embeds, page and table citations, list markers, quotes (checked as quotes) or table rows (checked as tables)."""
    out = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith('|') or '![[' in s or s.startswith('> Grounding'): continue
        s = re.sub(r'\[\[[^\]]*\]\]', ' ', s)
        s = re.sub(r'^(?:[>\s]*)(?:[-*]\s+|\d+\.\s+)', '', s)
        s = re.sub(r'"[^"\n]{20,}"|“[^”\n]{20,}”', ' ', s)
        s = re.sub(r'\b(?:PDF\s+)?pp?\.\s*\d+(?:\s*[-–]\s*\d+)?', ' ', s)
        s = re.sub(r'\b(?:Supplementary\s+)?(?:Table|Figure|Fig\.|Section|Box|Appendix)\s+S?\d+(?:\.\d+)*', ' ', s, flags=re.I)
        s = re.sub(r'\b[A-Z]-F?\d+\b', ' ', s)
        out.append((s, line))
    return out


def card_numbers(ps):
    nums = set()
    for f in ps.get('findings', []):
        for n in f.get('numbers', []): nums |= pp._number_set(str(n.get('value', '')))
        nums |= pp._number_set(' '.join([str(f.get('statement', ''))] + [str(x.get('text', '')) for x in f.get('spans', [])]))
    return nums


def check_numbers(body, pdf_nums, card_nums=frozenset()):
    """Every number written in the prose of the page: found in the paper (pages listed), found only in the extraction card (a supplement number, for example), or not found (flag)."""
    res = []
    for line, raw in prose_for_numbers(body):
        for m in NUM_RE.finditer(line):
            tok = m.group().strip(); ns = pp._number_set(tok.lstrip('+'))
            if not ns: continue
            pages = sorted({p for x in ns for p in pdf_nums.get(x, [])})
            status = 'found_in_paper' if pages else ('found_in_extraction_only' if ns & set(card_nums) else 'not_found')
            res.append({'number': tok, 'status': status, 'pdf_pages': pages, 'context': raw.strip()[:170]})
    return res


QUOTE_RE = re.compile(r'"([^"\n]{20,}?)"|“([^”\n]{20,}?)”')


def check_quotes(body, doc):
    """Every quoted passage (20 letters or more): located in the PDF text, and on the printed page cited right after it."""
    pm = {r['pdf']: r['printed'] for r in pp.page_map(doc)}; to_pdf = {}
    for k, v in pm.items(): to_pdf.setdefault(str(v), k)
    res = []
    for line in body.splitlines():
        if line.lstrip().startswith('|') or '![[' in line: continue
        for m in QUOTE_RE.finditer(line):
            q = m.group(1) or m.group(2); h = pp.find_quote(doc, q)
            tail = line[m.end():m.end() + 40]; c = re.match(r'[\s*`)]*\(?\s*pp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?', tail)
            cited = None
            if c:
                a = int(c.group(1)); b = int(c.group(2)) if c.group(2) else a; cited = [to_pdf[str(x)] for x in range(a, b + 1) if str(x) in to_pdf]
            page_ok = None if cited is None else (bool(set(h['pages']) & set(cited)) if h['found'] else None)
            res.append({'quote': q[:140], 'found': h['found'], 'pdf_pages': h['pages'], 'printed_pages': [pm.get(p) for p in h['pages']], 'cited_printed': c.group(1) if c else None, 'page_ok': page_ok})
    return res


def check_links(text_in, nodes):
    """Node ids written as [[id]]: all must exist in the run. Also lists the nodes of the run that the page never links."""
    ids = re.findall(r'(?<!!)\[\[([^\]|\n]+)\]\]', text_in); unknown = sorted({i for i in ids if i not in nodes}); used = sorted({i for i in ids if i in nodes})
    return {'used': used, 'unknown_ids': unknown, 'not_linked': sorted(set(nodes) - set(used))}


EMBED_RE = re.compile(r'!\[\[([^\]\n]*?)-(table|figure)(S?\d+)-p(\d+)-\d+\.png\]\]', re.I)
CITED_RE = re.compile(r'(?<!Supplementary )(?<!supplementary )\b(Table|Figure|Fig\.)\s+(\d+)\b')


def check_embeds(body, doc):
    """Each table or figure cited gets a screenshot placeholder whose PDF page holds the caption 'Table N' or 'Figure N'."""
    embeds = [(m.group(2).lower(), m.group(3), int(m.group(4))) for m in EMBED_RE.finditer(body)]
    cited = set()
    for line in body.splitlines():
        if '![[' in line: continue
        for m in CITED_RE.finditer(line): cited.add(('figure' if m.group(1).lower().startswith('fig') else 'table', m.group(2)))
    res = []
    for kind, num in sorted(cited, key=lambda x: (x[0], int(x[1]))):
        eb = [e for e in embeds if e[0] == kind and e[1] == num]
        if not eb: res.append({'cited': f'{kind} {num}', 'status': 'no_placeholder'}); continue
        pg = eb[0][2]; ok = 1 <= pg <= len(doc) and re.search(rf'\b{kind}\s+{num}\b', pp.page_text(doc[pg - 1]), re.I) is not None
        res.append({'cited': f'{kind} {num}', 'status': 'placeholder_ok' if ok else 'caption_not_on_placeholder_page', 'pdf_page': pg})
    for kind, num, pg in embeds:
        if (kind, num) not in cited: res.append({'cited': f'{kind} {num}', 'status': 'placeholder_without_citation', 'pdf_page': pg})
    return res


def check_tables(body, pdf, parsers=('mineru', 'pymupdf'), cache_dir=None, check_fn=None):
    """Every markdown table: needs a citation line above it (Table N and/or a page); then each cell is compared with the PDF table (methods_table_check.check_table)."""
    check_fn = check_fn or M.check_table; doc = fitz.open(pdf); pm = {r['printed']: r['pdf'] for r in pp.page_map(doc) if r['printed']}; res = []
    for t in M.parse_md_tables(body):
        pg, printed, tno, found = M.citation_of_table(t, body)
        if not found: res.append({'line': t['line'], 'status': 'no_source_citation', 'rows': len(t['rows'])}); continue
        if pg is None and printed is not None: pg = int(pm[str(printed)]) if str(printed) in pm else None
        try: r = check_fn(t['rows'], pdf, pg, parsers, table_no=tno, origin=f"page line {t['line']}", cache_dir=cache_dir)
        except Exception as e: res.append({'line': t['line'], 'status': 'check_error', 'detail': f'{type(e).__name__}: {str(e)[:150]}'}); continue
        s = r.get('summary') or {}
        res.append({'line': t['line'], 'status': 'checked' if s else 'no_source_table', 'table': tno, 'pdf_page': r.get('source', {}).get('pdf_page'), 'printed_page': r.get('source', {}).get('printed_page'),
                    'cells': s.get('cells'), 'matched': s.get('matched'), 'by_result': s.get('by_result'), 'mismatches': s.get('mismatches', []), 'parser_used': s.get('parser_used_for_rows'), 'error': r.get('error')})
    return res


CITE_RE = re.compile(r'\(\s*(Tables?|Figures?|Fig\.|Sections?|Box)\s*([A-Za-z]?\d+(?:\.\d+)*(?:\s*(?:and|,|&)\s*[A-Za-z]?\d+)*)\s*,\s*pp?\.\s*(\d+)(?:\s*[-\u2013]\s*(\d+))?\s*\)', re.I)
SUPP_RE = re.compile(r'\(\s*supplement', re.I)
MODEL_NAME_RE = re.compile(r'\b[A-Za-z][A-Za-z0-9.]*-\d[\w.-]*|\b(?:GPT|Claude|Mixtral|Llama|Gemini|Mistral)\s+\d[\d.]*')


def sentence_numbers(s):
    """Numbers of a sentence that are data: the citations, quotes, node links and model names (GPT-4, Claude-3-Opus, PRECIS-2) are taken out first."""
    s = CITE_RE.sub(' ', s); s = re.sub(r'\[\[[^\]]*\]\]', ' ', s); s = re.sub(r'"[^"\n]{20,}"', ' ', s); s = MODEL_NAME_RE.sub(' ', s)
    s = re.sub(r'\b(?:PDF\s+)?pp?\.\s*\d+', ' ', s); s = re.sub(r'^\s*\d+\.\s+', ' ', s)
    return [m.group().strip() for m in NUM_RE.finditer(s) if pp._number_set(m.group().strip().lstrip('+'))]


def check_cited_numbers(body, doc):
    """JP, 2026-11-27: every sentence with a number carries its own citation, and each of its numbers is printed in what the citation names: the cited table (cells, caption and notes of that
    page, pdf_pages.table_numbers) for a Table, the cited page text for a Figure, Section or Box. This is a number-level check on the cited page, not a row-and-column check (that is check_tables).
    Results per sentence: ok, uncited (numbers but no citation), not_on_cited_page (lists the numbers)."""
    pm = {}; [pm.setdefault(str(r['printed']), r['pdf']) for r in pp.page_map(doc)]; cache = {}
    def page_nums(pg, kind):
        k = (pg, kind)
        if k not in cache:
            try: cache[k] = pp.table_numbers(doc[pg - 1]) if kind == 'table' else pp._number_set(clean_pdf_text(pp.page_text(doc[pg - 1])))
            except Exception: cache[k] = set()
        return cache[k]
    res = []
    for line in strip_summary(body).splitlines():
        s = line.strip()
        if not s or s.startswith(('#', '|', '```')) or '![[' in s or s.startswith('> Grounding') or re.match(r'\*\*(?:Table|Figure)\s', s): continue
        s = re.sub(r'^(?:>\s*(?:\[![a-z]+\]-?\s*)?)?(?:[-*]\s+|\d+\.\s+)?', '', s)
        for sent in sentences(s):
            nums = sentence_numbers(sent)
            if not nums: continue
            cites = CITE_RE.findall(sent); supp = bool(SUPP_RE.search(sent))
            if not cites and not supp: res.append({'status': 'uncited', 'numbers': nums, 'sentence': sent[:170]}); continue
            if not cites: continue
            have = set(); pages = []
            for kind, no, a, b in cites:
                for printed in range(int(a), int(b or a) + 1):
                    pg = pm.get(str(printed))
                    if pg: pages.append(pg); have |= page_nums(pg, 'table' if kind.lower().startswith('table') else 'text')
            miss = [n for n in nums if not (pp._number_set(n.lstrip('+')) & have)]
            res.append({'status': 'not_on_cited_page' if miss else 'ok', 'numbers': nums, 'missing': miss, 'cited': [f'{k} {n}, p. {a}' for k, n, a, _ in cites], 'sentence': sent[:170]})
    return res


def summary_block(body):
    """The Summary callout: its lines (without the callout marker) and the text."""
    lines = body.splitlines(); out = []; on = False
    for l in lines:
        if re.match(r'^>\s*\[!\w+\]-?\s*\*\*Summary\*\*', l): on = True; continue
        if on:
            if l.startswith('>'): out.append(re.sub(r'^>\s?', '', l))
            else: break
    return ' '.join(' '.join(out).split()) if on else None


def strip_summary(body):
    out = []; on = False
    for l in body.splitlines():
        if re.match(r'^>\s*\[!\w+\]-?\s*\*\*Summary\*\*', l): on = True; continue
        if on and l.startswith('>'): continue
        on = False; out.append(l)
    return '\n'.join(out)


def check_summary(body):
    """Summary of 100 to 125 words, high level (questions, methods, claims, caveats), no citations inside it."""
    s = summary_block(body)
    if s is None: return {'present': False, 'words': 0, 'ok': False, 'citations': 0}
    n = len(s.split()); cites = len(CITE_RE.findall(s)) + len(re.findall(r'\(\s*(?:p|pp)\.\s*\d', s)) + len(re.findall(r'\b(?:Table|Figure)\s+\d', s)) + len(re.findall(r'\[\[', s))
    return {'present': True, 'words': n, 'in_range': SUMMARY_WORDS[0] <= n <= SUMMARY_WORDS[1], 'citations': cites, 'ok': SUMMARY_WORDS[0] <= n <= SUMMARY_WORDS[1] and cites == 0}


def normalize_body(raw):
    """Brings an older answer (src-write-v1 or v2) to the v3 layout without changing its words: TL;DR becomes Summary, the Abstract heading is dropped, each subheading gets its emoji, and the
    Grounding section is removed (the script now builds it from the PDF)."""
    t = raw.replace('**TL;DR**', '**Summary**'); t = re.sub(r'^## Abstract\s*\n', '', t, flags=re.M)
    i = t.find('\n## Grounding'); t = t[:i] if i >= 0 else t
    for n, e in EMOJI.items(): t = re.sub(rf'^### {re.escape(n)}\s*$', f'### {e} {n}', t, flags=re.M)
    return t.strip() + '\n'


def space_lists(text):
    """A blank line between top-level bullets (the vault's list spacing), a blank line around headings and two before a subheading, so a page reads with air between items."""
    out = []; prev = ''
    for l in text.splitlines():
        if re.match(r'^- ', l) and prev.strip() and not prev.lstrip().startswith(('>', '|')) and out and out[-1].strip(): out.append('')
        if re.match(r'^#{2,3} ', l) and out and out[-1].strip(): out.append('')
        if re.match(r'^### ', l) and out and out[-1] == '' and not (len(out) > 1 and out[-2] == ''): out.append('')
        out.append(l); prev = l
        if re.match(r'^#{2,3} ', l): out.append('')
    return re.sub(r'\n{4,}', '\n\n\n', '\n'.join(out))


def cited_labels(body):
    """Tables and figures cited anywhere in the body (not supplements), in order of first mention: [('table', '2'), ('figure', '1')]."""
    seen = []
    for line in body.splitlines():
        if '![[' in line: continue
        for m in CITED_RE.finditer(line):
            k = ('figure' if m.group(1).lower().startswith('fig') else 'table', m.group(2))
            if k not in seen: seen.append(k)
    return sorted(seen, key=lambda k: (k[0] != 'table', int(re.sub(r'\D', '', k[1]) or 0)))


def build_grounding(body, doc, citekey, att_dir):
    """The Grounding section: for each cited table and figure, a crop from the PDF (src_crops) under a 'Grounding table' line with its printed page and one-line caption. Returns (text, records, flags)."""
    pm = {r['pdf']: r['printed'] for r in pp.page_map(doc)}; recs = []; flags = []; out = ['### 🖼️ Grounding: tables and figures cited', '']
    for kind, num in cited_labels(body):
        f = K.find_caption(doc, kind, num)
        if not f: recs.append({'cited': f'{kind} {num}', 'error': 'caption not found in the PDF'}); flags.append({'kind': 'screenshot', 'what': f'{kind} {num} is cited but its caption was not found in the PDF, so no crop could be made'}); continue
        pg = f[0]; name = K.embed_name(citekey, kind, num, pg); r = K.make_crop(doc, kind, num, Path(att_dir) / name)
        if 'error' in r: recs.append({'cited': f'{kind} {num}', 'error': r['error']}); flags.append({'kind': 'screenshot', 'what': f"{kind} {num}: crop not made ({r['error']})"}); continue
        cap = re.sub(r'^\s*\S+\s+\S+\s*[.:]\s*', '', r['caption']); cap = re.split(r'(?<=[.!?])\s+(?=[A-Z(])', cap)[0]; cap = cap if len(cap) <= 220 else cap[:220].rsplit(' ', 1)[0].rstrip(' ,;:') + ' ...'
        out += [f"> Grounding {kind} ({kind.capitalize()} {num}, p. {pm.get(pg)}): {cap}", f'> ![[{name}]]', '']
        recs.append({'cited': f'{kind} {num}', **r})
    return ('\n'.join(out) + '\n') if recs else '', recs, flags


def check_table_count(body):
    """One or two copied Methods tables are required (src-write-v2)."""
    n = len(M.parse_md_tables(body)); return {'tables': n, 'ok': 1 <= n <= 2}


def findings_bullets(body):
    """{node id: bullet text} for the bullets of the Findings section that start with a node link [[id]] (sub-bullets belong to the bullet above)."""
    m = re.search(r'^### (?:[^\w\s]+\s+)?Findings\s*\n(.*?)(?=^### |^## |\Z)', body, re.S | re.M)
    if not m: return {}
    out = {}; cur = None
    for line in m.group(1).splitlines():
        b = re.match(r'^- \[\[([^\]|\n]+)\]\]', line)
        if b: cur = b.group(1).strip(); out[cur] = line
        elif cur and (line.startswith('  ') or not line.strip()): out[cur] += '\n' + line
        elif line.strip(): cur = None
    return {k: v.strip() for k, v in out.items()}


def judge_text(bullets, nodes, ps):
    """The Neon judge's input: each Findings bullet with its EVD node and the extraction finding behind it."""
    fnd = {f['id']: f for f in ps['findings']}; items = []
    for i, b in bullets.items():
        n = nodes.get(i, {}); f = fnd.get(n.get('source_id'), {})
        items.append({'id': i, 'bullet': b, 'evd_node': {'statement': n.get('statement'), 'quote': n.get('quote'), 'tier': n.get('tier'), 'review_status': n.get('review_status')},
                      'finding': {'statement': f.get('statement'), 'numbers': f.get('numbers'), 'spans': [s.get('text') for s in f.get('spans', [])], 'notes': f.get('notes')}})
    return json.dumps({'bullets': items}, ensure_ascii=False)


def parse_judge(text):
    try:
        t = re.sub(r'^```(?:json)?|```$', '', (text or '').strip(), flags=re.M).strip(); return {x['id']: x for x in json.loads(t[t.find('{'):t.rfind('}') + 1])['bullets']}
    except Exception: return None


def judge_flags(verdicts, bullets):
    """Flags for a human: a bullet judged partly or unsupported, a bullet with no verdict, or no judge answer at all."""
    if verdicts is None: return [{'kind': 'judge', 'what': 'the judge answer could not be read; no Findings bullet was judged'}] if bullets else []
    fl = []
    for i in bullets:
        v = verdicts.get(i)
        if not v: fl.append({'kind': 'judge', 'what': f'{i}: the judge gave no verdict'})
        elif v.get('verdict') not in ('supported', 'partly', 'unsupported'): fl.append({'kind': 'judge', 'what': f"{i}: unreadable verdict {v.get('verdict')!r}"})
        elif v['verdict'] != 'supported': fl.append({'kind': 'judge', 'what': f"{i}: judged {v['verdict']}", 'reason': v.get('reason', ''), 'bullet': bullets[i][:160]})
    return fl


def sentences(text):
    t = re.sub(r'\b(p|pp|vs|e\.g|i\.e|Fig|Sec|approx|al)\.', lambda m: m.group().replace('.', '\x00'), text)
    return [s.replace('\x00', '.') for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"(\[*`])', t) if s.strip()]


def plain(s):
    s = re.sub(r'\[\[[^\]]*\]\]', 'NODE', s); s = re.sub(r'"[^"\n]{20,}"', 'QUOTE', s); s = re.sub(r'\([^()]*\)', '', s)
    return re.sub(r'(\*\*|__|`|\*)', '', s)


def check_style(body):
    """Skimmability rules of Skill-templates.md (soft flags): headings in order, link first in a bullet, at most 25 words a sentence, at most 3 sentences in a plain paragraph, no arrows or slashes in prose."""
    flags = []; pos = -1
    for h in HEADINGS:
        i = body.find('\n' + h) if not body.startswith(h) else 0
        if i < 0: flags.append({'rule': 'heading_missing', 'detail': h})
        elif i < pos: flags.append({'rule': 'heading_order', 'detail': h})
        else: pos = i
    if '**Summary**' not in body: flags.append({'rule': 'heading_missing', 'detail': 'Summary callout'})
    if re.search(r'^## Abstract', body, re.M): flags.append({'rule': 'abstract_heading', 'detail': 'the Abstract subheading is removed (JP, 2026-11-27)'})
    for sec in ('Not reported',):
        m = re.search(rf'^### \S+ {sec}\s*\n(.*?)(?=^### |^## |\Z)', body, re.S | re.M)
        for l in (m.group(1).splitlines() if m else []):
            if l.strip() and not l.lstrip().startswith('- '): flags.append({'rule': 'not_reported_not_one_line', 'detail': l.strip()[:80]})
            elif l.strip() and len(sentences(plain(l.strip()[2:]))) > 1: flags.append({'rule': 'not_reported_not_one_line', 'detail': l.strip()[:80]})
    sumlines = set(); on = False
    for n, line in enumerate(body.splitlines(), 1):
        if re.match(r'^>\s*\[!\w+\]-?\s*\*\*Summary\*\*', line): on = True; continue
        if on and line.startswith('>'): sumlines.add(n)
        else: on = False
    for n, line in enumerate(body.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('|') or '![[' in s or s.startswith('> Grounding') or s.startswith('```'): continue
        bullet = re.match(r'^(?:[-*]|\d+\.)\s+(.*)$', s); text = bullet.group(1) if bullet else re.sub(r'^>\s*(\[![a-z]+\]\s*)?', '', s)
        if bullet and '[[' in text and not re.match(r'^(?:\*\*)?\[\[', text): flags.append({'rule': 'link_not_first', 'line': n, 'detail': text[:80]})
        for sent in sentences(plain(text)):
            w = len(sent.split())
            if w > 25: flags.append({'rule': 'sentence_over_25_words', 'line': n, 'detail': f'{w} words: {sent[:80]}'})
        if not bullet and len(sentences(plain(text))) > (6 if n in sumlines else 3): flags.append({'rule': 'paragraph_over_3_sentences', 'line': n, 'detail': text[:80]})
        if bullet and len(sentences(plain(text))) > 6: flags.append({'rule': 'bullet_over_6_sentences', 'line': n, 'detail': text[:80]})
        if re.search(r'→|->|=>', plain(text)): flags.append({'rule': 'arrow_in_prose', 'line': n, 'detail': text[:80]})
        if re.search(r'\b[A-Za-z]{3,}/[A-Za-z]{3,}\b', plain(text)): flags.append({'rule': 'slash_in_prose', 'line': n, 'detail': text[:80]})
        if re.search(r'\bhonest', text, re.I): flags.append({'rule': 'banned_word', 'line': n, 'detail': 'honest'})
    return flags


def writing_rules_check(body):
    """lives_stages.writing_rules on the whole page (no em dash, all-caps words not on the allowed list), loaded lazily because lives_stages loads the decision-model keys."""
    import lives_stages as S
    r = S.writing_rules({'type': 'SRC', 'statement': body}, set())
    caps_allowed = set(C.PIPE.get('writing', {}).get('caps_allowed', [])) | {'TL', 'DR', 'LLM', 'LLMs', 'PICOST', 'CI', 'SRC', 'EVD', 'QUE', 'CLM', 'CVT', 'PDF', 'RCT', 'AI', 'API', 'TRIPOD', 'PRECIS', 'ROBINS', 'GPT', 'USD', 'OSF'}
    text = re.sub(r'\[\[[^\]]*\]\]|!\[\[[^\]]*\]\]|`[^`]*`', ' ', body)
    caps = sorted({w for w in re.findall(r'\b[A-Z][A-Z_]{3,}\b', text) if w not in caps_allowed})
    return {'no_emdash': r['no_emdash'], 'all_caps_words': caps, 'pass': r['no_emdash'] and not caps}


def validate(body_raw, nodes, doc, pdf, card_nums=frozenset(), parsers=('mineru', 'pymupdf'), cache_dir=None, check_fn=None):
    """All checks of one model answer. Returns (page body with real node links, validation dict, flags for human examination)."""
    links = check_links(re.sub(r'!\[\[[^\]]*\]\]', '', body_raw), nodes)
    body, _, _ = resolve_links_keep_embeds(body_raw, nodes)
    pdf_nums = paper_numbers(doc)
    v = {'writing_rules': writing_rules_check(body_raw), 'links': links, 'numbers': check_numbers(body_raw, pdf_nums, card_nums), 'quotes': check_quotes(body_raw, doc), 'embeds': check_embeds(body_raw, doc) if '![[' in body_raw else [], 'summary': check_summary(body_raw),
         'tables': check_tables(body_raw, pdf, parsers, cache_dir, check_fn), 'style': check_style(body_raw), 'cited_numbers': check_cited_numbers(body_raw, doc), 'table_count': check_table_count(body_raw)}
    flags = []
    if not v['writing_rules']['no_emdash']: flags.append({'kind': 'writing_rules', 'what': 'an em dash is on the page'})
    for w in v['writing_rules']['all_caps_words']: flags.append({'kind': 'writing_rules', 'what': f'all-caps word {w}'})
    for i in links['unknown_ids']: flags.append({'kind': 'link', 'what': f'node id [[{i}]] does not exist in the run'})
    for x in v['numbers']:
        if x['status'] == 'not_found': flags.append({'kind': 'number', 'what': f"{x['number']} not found in the paper text or tables", 'context': x['context']})
        elif x['status'] == 'found_in_extraction_only': flags.append({'kind': 'number', 'what': f"{x['number']} found only in the extraction (supplement or derived), not in the PDF text", 'context': x['context']})
    for x in v['cited_numbers']:
        if x['status'] == 'uncited': flags.append({'kind': 'citation', 'what': f"sentence with number(s) {x['numbers']} has no table, figure or page citation", 'context': x['sentence']})
        elif x['status'] == 'not_on_cited_page': flags.append({'kind': 'citation', 'what': f"number(s) {x['missing']} not printed in {x['cited']}", 'context': x['sentence']})
    sm = v['summary']
    if not sm['present']: flags.append({'kind': 'summary', 'what': 'the Summary callout is missing'})
    else:
        if not sm['in_range']: flags.append({'kind': 'summary', 'what': f"the Summary has {sm['words']} words; {SUMMARY_WORDS[0]} to {SUMMARY_WORDS[1]} are required"})
        if sm['citations']: flags.append({'kind': 'summary', 'what': f"the Summary holds {sm['citations']} citation(s) or node link(s); none are allowed"})
    if not v['table_count']['ok']: flags.append({'kind': 'table', 'what': f"the page has {v['table_count']['tables']} copied table(s); one or two are required"})
    for x in v['quotes']:
        if not x['found']: flags.append({'kind': 'quote', 'what': 'quoted passage not located in the PDF text', 'quote': x['quote']})
        elif x['page_ok'] is False: flags.append({'kind': 'quote', 'what': f"quote found on printed page {x['printed_pages']} but cited as p. {x['cited_printed']}", 'quote': x['quote']})
    for x in v['embeds']:
        if x['status'] != 'placeholder_ok': flags.append({'kind': 'screenshot', 'what': f"{x['cited']}: {x['status']}"})
    for t in v['tables']:
        if t['status'] == 'no_source_citation': flags.append({'kind': 'table', 'what': f"table at line {t['line']} has no source citation line above it"})
        elif t['status'] != 'checked': flags.append({'kind': 'table', 'what': f"table at line {t['line']}: {t['status']} {t.get('detail') or t.get('error') or ''}".strip()})
        else:
            for m in t['mismatches']: flags.append({'kind': 'table_cell', 'what': f"Table {t['table']} (printed p. {t['printed_page']}) row {m['row']} col {m['col']}: copy {m['copy']!r} vs source {m['source']!r} ({m['result']})"})
    return body, v, flags


# ------------------------------------------------------------------ call (batch only)
def est_input_tokens(system, text):
    return (len(system) + len(text)) / 3.5


def label_manifest(run_id, key, info):
    """Writes what this script did into the run's manifest (stage_log[key]) with a note, because the run was finished before it. spent_usd is not changed."""
    f = cl.RUNS / run_id / 'manifest.json'; m = json.loads(f.read_text(encoding='utf-8'))
    m.setdefault('stage_log', {})[key] = {**info, 'note': 'added after the run by scripts/write_src.py (SRC pages); the cost is not counted in spent_usd above; the call records are in calls.jsonl with the same note'}
    tmp = f.with_suffix('.tmp'); tmp.write_text(json.dumps(m, indent=1, ensure_ascii=False, default=str), encoding='utf-8'); tmp.replace(f)


def run_stage(run_id, key, model, effort, prompt_file, reqs, paper_dirs, max_tokens, cap_usd):
    """One batch for all requests of a stage (llm_batch.submit_batch, one model). Resumable: the job is kept in runs/<run>/<key>_job.json and each answer in <paper folder>/<key>_response.json;
    papers whose answer is saved are not sent again. Returns ({paper key: Res}, {paper key: fresh}, seconds). The call log and the manifest stage_log are written for new answers."""
    rd = cl.RUNS / run_id; jf = rd / f'{key}_job.json'; res = {}; fresh = {}
    for pk, r in reqs.items():
        rf = paper_dirs[pk] / f'{key}_response.json'
        if rf.exists(): d = json.loads(rf.read_text(encoding='utf-8')); res[pk] = L.Res(**d['res']); fresh[pk] = False
    todo = {pk: r for pk, r in reqs.items() if pk not in res}
    if not todo: print(f'{key}: using the saved answers (no new call)'); return res, fresh, None
    worst = sum(L.cost(model, est_input_tokens(r.system, r.text), max_tokens, batch=True) for r in todo.values())
    if worst > cap_usd: raise SystemExit(f'{key}: worst case ${worst:.2f} is over the cap of ${cap_usd:.2f}; nothing was submitted')
    t0 = time.time()
    if jf.exists(): job = json.loads(jf.read_text(encoding='utf-8')); t0 = job.get('submitted', t0); print(f'{key}: resuming the saved batch job')
    else: print(f'{key}: submitting one {model} batch of {len(todo)} request(s) ({effort} effort); worst case ${worst:.3f}, cap ${cap_usd:.2f}'); job = L.submit_batch(list(todo.values())); jf.write_text(json.dumps(job), encoding='utf-8')
    last = 0
    while True:
        st = L.poll_batch(job)
        if st == 'done': break
        if st == 'failed': raise SystemExit(f'{key}: the batch job failed or expired; the saved job is kept in the run folder')
        if time.time() - last > 120: print(f'  {key}: waiting, {int(time.time() - t0)} s since submission'); last = time.time()
        time.sleep(20)
    got = L.fetch_batch(job); secs = round(time.time() - t0, 1); usd = 0.0
    for pk, r in todo.items():
        x = got[r.id]; res[pk] = x; fresh[pk] = True; c = L.cost(model, x.tin, x.tout, batch=True); usd += c
        (paper_dirs[pk] / f'{key}_response.json').write_text(json.dumps({'res': vars(x), 'seconds': secs}), encoding='utf-8')
        cl.record(run_id, key, model, prompt_file, provider=L.provider_of(model), citekey=pk, effort=effort, tokens_in=x.tin, tokens_out=x.tout, latency_s=secs, output_text=x.text or None,
                  notes=f'mode=batch; cost_usd={c:.4f}; finish={x.finish}; err={x.err}; added after the run finished by write_src.py, not in the manifest spent_usd')
    label_manifest(run_id, key, {'model': model, 'effort': effort, 'mode': 'batch', 'prompt': prompt_file, 'requests': len(todo), 'papers': list(todo), 'actual_usd': round(usd, 4), 'elapsed_s': secs, 'job_file': f'{key}_job.json', 'response_files': f'<paper folder>/{key}_response.json'})
    return res, fresh, secs


# ------------------------------------------------------------------ page assembly
def front_matter(citekey, ps, run_id, usd, prompt_id=PROMPT_ID):
    p = ps['paper']; q = lambda s: '"' + str(s).replace('"', "'") + '"'
    return '\n'.join(['---', 'dg_type: Source', 'status: test, not validated', f'citekey: {citekey}', f'title: {q(p.get("title", ""))}', f'authors: {q(p.get("authors", ""))}', f'year: {q(p.get("year", ""))}',
                      f'venue: {q(p.get("venue", ""))}', f'doi: {p.get("doi", "")}', f'written_by: {C.display(SRC_MODEL)} ({SRC_MODEL}, {SRC_EFFORT} effort, batch)', f'prompt: {prompt_id}', f'judged_by: {C.display(JUDGE_MODEL)} ({JUDGE_MODEL}, {JUDGE_EFFORT} effort, batch)', f'run_id: {run_id}',
                      'checked_by: write_src.py checks only; no human has read this page', '---'])


def qs_calls(paper, calls):
    """Calls for the AI-use table: the run's call log without its old quality-signal steps, plus the raters named in the quality-signals export that the two tables were made from."""
    keep = [c for c in calls if c['step'] not in ('qs', 'qs_adjudicate')]; q = (paper or {}).get('qs_run') or {}; by_name = {v['display']: k for k, v in C.MODELS.items()}
    for r in q.get('raters', []):
        m = re.match(r'(.+?) \((\w+)', r); mid = by_name.get(m.group(1)) if m else None
        if mid: keep.append({'step': 'qs', 'model_id': mid, 'model': m.group(1), 'effort': m.group(2), 'ts_utc': q.get('exported_utc', ''), 'prompt_file': q.get('prompt'), 'run_id': q.get('run_id')})
    return keep


def printed_map(doc):
    return {r['pdf']: r['printed'] for r in pp.page_map(doc)}


def assemble_page(citekey, inp, body_resolved, run_id, usd, doc, att_dir, out_dir, flags, human, prompt_id=PROMPT_ID):
    """The whole page: front matter, test banner, Properties, the model's text (Summary to Not reported), Quality appraisal, TRIPOD-LLM reporting, Grounding with its crops, Evidence provenance, AI use.
    Returns (page text, extra flags, extras for the audit)."""
    paper = X.load_paper(citekey); printed = printed_map(doc); extra = []; info = {'quality_export': bool(paper)}
    body_text = space_lists(body_resolved.strip())
    ground, grecs, gflags = build_grounding(body_text, doc, citekey, att_dir); extra += gflags; info['grounding'] = grecs
    qa = tr = prov = ''
    keys = []
    if paper:
        qa, k1 = X.quality_table(paper, printed); tr, k2 = X.tripod_table(paper, printed, len(k1) + 1); keys = k1 + k2
        prov = X.provenance_table(paper, keys, citekey, lambda rel: (VAULT / rel).exists())
        bad = []
        for k, sid in keys:
            for r in paper['signals'][sid].get('ratings', []):
                if r.get('quote') and not pp.find_quote(doc, r['quote'])['found']: bad.append({'key': k, 'signal': sid, 'quote': r['quote'][:120]}); extra.append({'kind': 'quote', 'what': f'{k} ({sid}): quality-signal quote not located in the PDF text', 'quote': r['quote'][:120]})
                if r.get('screenshot') and not (VAULT / SHOTS_DIR / r['screenshot']).exists(): extra.append({'kind': 'screenshot', 'what': f"{k} ({sid}): screenshot file {r['screenshot']} is missing"})
        info['quality'] = {'rows': len(keys), 'keys': [k for k, _ in keys], 'quotes_not_located': bad}
    else: extra.append({'kind': 'quality', 'what': 'no entry for this paper in pipeline/provenance/provenance-quality-signals.json; the Quality appraisal and TRIPOD-LLM tables are left out'})
    calls = qs_calls(paper, [c for c in cl.read_calls(run_id) if c.get('citekey') == inp['paper_key']])
    ai, models, when = X.ai_use_table(calls, human)
    props = X.properties_table(X.properties_rows(citekey, inp['picost']['paper'], paper, models, when))
    nflags = len(flags) + len(extra)
    top = f'> [!warning] Test page, not validated. {nflags} item(s) are flagged for a human to examine in `{citekey}.audit.json`. No person has read this page.\n'
    parts = [front_matter(citekey, inp['picost'], run_id, usd, prompt_id), '', top, props, body_text]
    if paper: parts += ['', '---', '', qa, tr]
    parts += ['', '---', '', ground, prov, '', ai]
    page = '\n'.join(parts)
    res = K.embeds_resolve(page, [att_dir, out_dir]); info['embeds_resolved'] = [{'embed': n, 'found': f} for n, f in res]
    for n, f in res:
        if not f: extra.append({'kind': 'screenshot', 'what': f'embed {n} does not resolve to an existing file'})
    return re.sub(r'\n{4,}', '\n\n\n', page).rstrip() + '\n', extra, info


SHOTS_DIR = 'pipeline/provenance/quality-signal-screenshots'


def summarize(v, flags):
    n = collections.Counter(x['status'] for x in v['numbers']); qs = collections.Counter('located' if x['found'] else 'not_located' for x in v['quotes'])
    return {'flags_for_human_examination': len(flags), 'numbers': dict(n), 'quotes': dict(qs), 'quote_page_mismatch': sum(1 for x in v['quotes'] if x['page_ok'] is False),
            'unknown_node_ids': v['links']['unknown_ids'], 'nodes_not_linked': v['links']['not_linked'],
            'tables': [{'line': t['line'], 'status': t['status'], 'matched': t.get('matched'), 'cells': t.get('cells')} for t in v['tables']], 'style_flags': len(v['style']), 'cited_numbers': dict(collections.Counter(x['status'] for x in v['cited_numbers'])),
            'copied_tables': v['table_count']['tables'], 'summary_words': v['summary']['words'], 'writing_rules_pass': v['writing_rules']['pass']}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('run_id'); ap.add_argument('--paper', help='one paper (the run folder name); default: every paper of the run, in one batch')
    ap.add_argument('--mode', default='batch', choices=['batch'], help='batch only (JP, 2026-11-27)')
    ap.add_argument('--out', default=str(OUT_DEFAULT)); ap.add_argument('--attachments', help='folder for the table and figure crops (default: <out>/Attachments)'); ap.add_argument('--cap-usd', type=float, default=1.0, help='hard cap per stage')
    ap.add_argument('--parsers', default='mineru,pymupdf'); ap.add_argument('--no-judge', action='store_true')
    ap.add_argument('--saved-answer', help='offline: use this saved model answer (a src_write_response.json or a text file) for the one --paper instead of calling the model; no judge runs'); ap.add_argument('--saved-prompt', default='unknown', help='prompt id the saved answer was written with'); a = ap.parse_args()
    C.assert_allowed(SRC_MODEL); C.assert_allowed(JUDGE_MODEL); out = Path(a.out); out.mkdir(parents=True, exist_ok=True); att = Path(a.attachments) if a.attachments else out / 'Attachments'
    for d in (out, att):
        if (VAULT / 'sysrev') in [d.resolve(), *d.resolve().parents]: raise SystemExit('this script never writes into sysrev/')
    man = json.loads((cl.RUNS / a.run_id / 'manifest.json').read_text(encoding='utf-8')); keys = [a.paper] if a.paper else list(man['papers'])
    P = {}
    for k in keys:
        inp = load_inputs(a.run_id, k); ps = inp['picost']; ck = vault_citekey(ps['paper'].get('doi'), k); doc = fitz.open(inp['pdf']); P[k] = {'inp': inp, 'ck': ck, 'doc': doc}
    dirs = {k: P[k]['inp']['paper_dir'] for k in keys}; prompt_id = PROMPT_ID
    if a.saved_answer:
        if len(keys) != 1: raise SystemExit('--saved-answer needs --paper')
        raw = Path(a.saved_answer).read_text(encoding='utf-8'); txt = json.loads(raw)['res']['text'] if raw.lstrip().startswith('{') else raw; prompt_id = a.saved_prompt
        wres = {keys[0]: L.Res(keys[0], True, txt, 0, 0, 'saved')}; wsecs = None; no_judge = True
    else:
        for k in keys: P[k]['text'] = build_user_text(P[k]['inp'], P[k]['ck'], P[k]['doc'])
        system = system_prompt(); no_judge = a.no_judge
        reqs = {k: L.Req(f'{k}__src_write', SRC_MODEL, P[k]['text'], system=system, effort=SRC_EFFORT, max_tokens=MAX_TOKENS) for k in keys}
        wres, wfresh, wsecs = run_stage(a.run_id, STAGE, SRC_MODEL, SRC_EFFORT, PROMPT_FILE, reqs, dirs, MAX_TOKENS, a.cap_usd)
    parsers = tuple(x for x in a.parsers.split(',') if x != 'mineru' or M.VENV_PY.exists())
    for k in keys:
        r = wres[k]
        if not r.ok or not r.text.strip(): print(f'{k}: the model call did not return a page: finish={r.finish} err={r.err}'); continue
        raw = normalize_body(r.text)
        P[k]['raw'] = raw; P[k]['body'], P[k]['v'], P[k]['flags'] = validate(raw, P[k]['inp']['nodes'], P[k]['doc'], P[k]['inp']['pdf'], card_numbers(P[k]['inp']['picost']), parsers)
        P[k]['bullets'] = findings_bullets(raw)
    ok = [k for k in keys if 'v' in P[k]]
    jres = {}
    if ok and not no_judge:
        jsys = system_prompt(JUDGE_PROMPT_FILE)
        jreqs = {k: L.Req(f'{k}__src_judge', JUDGE_MODEL, judge_text(P[k]['bullets'], P[k]['inp']['nodes'], P[k]['inp']['picost']), system=jsys, effort=JUDGE_EFFORT, max_tokens=JUDGE_MAX_TOKENS) for k in ok if P[k]['bullets']}
        if jreqs: jres, _, _ = run_stage(a.run_id, JUDGE_STAGE, JUDGE_MODEL, JUDGE_EFFORT, JUDGE_PROMPT_FILE, jreqs, dirs, JUDGE_MAX_TOKENS, a.cap_usd)
    human = 'not yet human-checked'
    for k in ok:
        d = P[k]; verd = parse_judge(jres[k].text) if k in jres and jres[k].ok else None
        d['v']['judge'] = {'model': JUDGE_MODEL, 'prompt': JUDGE_PROMPT_ID, 'verdicts': verd, 'run': k in jres}
        if not no_judge: d['flags'] += judge_flags(verd, d['bullets'])
        elif a.saved_answer: d['flags'].append({'kind': 'judge', 'what': 'the Neon judge was not run (offline regeneration from a saved answer)'})
        usd = round(L.cost(SRC_MODEL, wres[k].tin, wres[k].tout, batch=True), 4); jusd = round(L.cost(JUDGE_MODEL, jres[k].tin, jres[k].tout, batch=True), 4) if k in jres else 0.0
        ck = d['ck']; page, extra, info = assemble_page(ck, d['inp'], d['body'], a.run_id, usd, d['doc'], att, out, d['flags'], human, prompt_id); d['flags'] += extra
        (out / f'{ck}.md').write_text(page, encoding='utf-8')
        jc = collections.Counter(x.get('verdict') for x in (verd or {}).values())
        audit = {'status': 'test, not validated', 'citekey': ck, 'run_id': a.run_id, 'paper_folder': k, 'source_pdf': {'file': rel(d['inp']['pdf']), 'sha256': M.sha256(d['inp']['pdf'])},
                 'model': {'id': SRC_MODEL, 'display': C.display(SRC_MODEL), 'effort': SRC_EFFORT, 'mode': 'batch'}, 'prompt': {'id': prompt_id, 'file': PROMPT_FILE if prompt_id == PROMPT_ID else None, 'sha256': cl.prompt_info(PROMPT_FILE)['prompt_sha256'] if prompt_id == PROMPT_ID else None, 'saved_answer': bool(a.saved_answer)},
                 'judge': {'id': JUDGE_MODEL, 'display': C.display(JUDGE_MODEL), 'effort': JUDGE_EFFORT, 'mode': 'batch', 'prompt': JUDGE_PROMPT_ID, 'verdicts': dict(jc)},
                 'cost': {'tokens_in': wres[k].tin, 'tokens_out': wres[k].tout, 'usd_batch_price': usd, 'judge_usd_batch_price': jusd, 'seconds_submit_to_answer': wsecs}, 'date_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                 'summary': {**summarize(d['v'], d['flags']), 'embeds': collections.Counter('resolved' if x['found'] else 'missing' for x in info['embeds_resolved'])}, 'flags_for_human_examination': d['flags'], 'validation': d['v'], 'page_parts': info}
        (out / f'{ck}.audit.json').write_text(json.dumps(audit, indent=1, ensure_ascii=False), encoding='utf-8')
        s = audit['summary']; print(f"{ck}: wrote the page and the audit; cost ${usd + jusd:.3f}; {s['flags_for_human_examination']} flag(s) for a human; embeds {dict(s['embeds'])}; numbers {s['numbers']}; quotes {s['quotes']}; judge {dict(jc)}")


if __name__ == '__main__':
    main()

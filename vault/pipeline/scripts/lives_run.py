#!/usr/bin/env python3
"""LIVES batch runner: PDFs in, checked PICOST records out, with a hard limit of four papers, a spending cap, stop rules and a run manifest (JP, 2026-11-25).

  python3 lives_run.py PDF [PDF ...] [--mode standard|batch] [--cap 5.55] [--question "..."] [--dry-run]
  python3 lives_run.py --resume RUN_ID              continue a stopped or interrupted run (a submitted batch job is picked up again, not paid twice)

Stages (one request per paper, or per paper with flagged findings, per stage; the whole stage goes out as ONE batch or one parallel standard run):
  1 picost      Gemini 4 Neon reads each PDF and returns PICOST records with locators and verbatim spans (prompts/picost-v6.md)
  2 spans       local, free: PyMuPDF finds every span, returns bounding boxes, saves highlighted pages, checks that each number is on the page; flags low-confidence,
                multi-page, scanned and not-found items
  3 recheck     GPT-6.2 Sol re-extracts the flagged findings independently, without seeing Neon's values (prompts/recheck-v1.md)
  4 adjudicate  Claude Opus 5.5 decides, from the PDF, where Neon and Sol disagree (prompts/adjudicate-v1.md)
  5 checks      decision models score every finding (relevancy, fidelity, quote and table grounding); Sol vision on flagged, low-confidence and 10% sampled crops; Opus on rare disputes
  6 draft       EVD, QUE, CLM, CVT nodes by debate (Sonnet 5.5, Sol, Neon Medium; Sol and Sonnet vote; Neon tie-break; Inkling benchmark only); drafts stay in the run folder
  7 qs          quality signals rated by Opus 5.5, Sol and Neon (majority vote); Inkling benchmark only (--skip checks draft qs leaves stages out)
  then STOP: status awaiting_spot_check_a. A person reviews review.md; writing nodes and the decision-model gates are separate, later steps.

Safety rails (constants below, not options):
  MAX_PAPERS = 4          more PDFs are refused; PDFs already processed (same SHA-256) are refused unless --allow-repeat
  CAP = $5.55 per batch   --cap may lower it, never raise it. Before each stage the worst case (all input tokens plus the full max output) is added to the spend so far;
                          if that would pass the cap, the run stops BEFORE submitting. After each stage the actual spend is added.
  stop-the-batch rules    spend over the cap; a stage costing more than 1.5 times its expected cost; two or more papers failing a stage; more than 25% of a paper's
                          spans not found in its PDF (the extraction is unreliable); a file named STOP in the run folder (touch it to halt before the next stage).
                          A halt cancels any batch job still running.
  The cap covers calls made by this runner. Google AI Studio and OpenAI also allow a monthly limit per project: set one as a second fence.
Standard mode is for pilots and when someone is waiting (full price); batch mode is about half price and takes minutes to hours (up to 24 h).
Outputs (not in the public repo): pipeline/runs/<run_id>/{manifest.json, calls.jsonl, responses/, <citekey>/{picost.json, review.md, highlights/}}"""
import argparse, hashlib, json, os, platform, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import call_logger as cl, llm_batch as L, pdf_pages as pp, lives_stages as S
import fitz

import config as C
LIM = C.PIPE['limits']; TOK = C.PIPE['tokens']
MAX_PAPERS = LIM['max_papers']; CAP = LIM['cap_usd']; OVERRUN = LIM['overrun_factor']; MAX_SPAN_MISS = LIM['max_span_miss']   # all from pipeline/config/pipeline.json
TOK_PER_PAGE = TOK['per_page_input']   # input tokens per PDF page (measured on the 27 seed PDFs and billed calls)
MAX_FINDINGS = LIM['worst_case_findings_per_paper']   # planning number for output budgets only; there is no cap on findings (JP, 2026-11-25)
STAGE_MODEL = {'picost': C.ROLES['extract'], 'recheck': C.ROLES['recheck'], 'adjudicate': C.ROLES['adjudicate']}   # roles in pipeline/config/models.json
STAGE_PROMPT = {'picost': 'pipeline/prompts/picost-v6.md', 'recheck': 'pipeline/prompts/recheck-v1.md', 'adjudicate': 'pipeline/prompts/adjudicate-v1.md'}
def max_out(stage, n=0):   # n = pages for picost, flagged or disputed findings for recheck and adjudicate
    """Output plus thinking budget (max tokens) per request, from pipeline/config/pipeline.json. Measured on real runs: Neon 27,317 tokens for 10 pages and 12 findings (about 11,000 visible,
    16,000 thinking); Sol about 670 per flagged finding; Opus about 226 per dispute plus a thinking floor (it ran out at 1,450 on one dispute). Beyond 10 pages the picost growth is an extrapolation."""
    if stage == 'picost': t = TOK['picost']; return min(t['max'], t['base'] + t['per_page'] * max(n, 10))
    t = TOK[stage]; return min(t['max'], t['base'] + t['per_finding'] * max(n, 1))
STAGE_MAX_OUT = {'picost': max_out('picost', 20), 'recheck': max_out('recheck', MAX_FINDINGS), 'adjudicate': max_out('adjudicate', MAX_FINDINGS)}   # worst case, used by the dry run
VAULT = cl.VAULT; RUNS = cl.RUNS
now = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds')
sha = lambda b: hashlib.sha256(b).hexdigest()


Halt = S.Halt
GEM_FILES = {}   # PDFs already uploaded to the Gemini File API in this process


# ---------------------------------------------------------------- manifest
class Manifest:
    def __init__(self, run_id, d=None):
        import threading; self.lock = threading.RLock(); self.gem_files = GEM_FILES; self.dir = RUNS / run_id; self.path = self.dir / 'manifest.json'; self.dir.mkdir(parents=True, exist_ok=True)
        self.m = json.loads(self.path.read_text()) if self.path.exists() else d
    def save(self):
        with self.lock: tmp = self.path.with_suffix('.tmp'); tmp.write_text(json.dumps(self.m, indent=1, ensure_ascii=False, default=str), encoding='utf-8'); tmp.replace(self.path)   # atomic
    def event(self, msg):
        self.m.setdefault('events', []).append({'t': now(), 'msg': msg}); print(msg, flush=True); self.save()


def environment():
    import importlib.metadata as md
    pk = {}
    for n in ('anthropic', 'openai', 'pymupdf'):
        try: pk[n] = md.version(n)
        except Exception: pk[n] = None
    here = Path(__file__).resolve().parent
    return {'python': platform.python_version(), 'platform': platform.platform(), 'packages': pk,
            'scripts_sha256': {f: sha((here / f).read_bytes())[:16] for f in ('lives_run.py', 'llm_batch.py', 'call_logger.py', 'pdf_pages.py')},
            'prompts_sha256': {Path(p).name: sha((VAULT / p).read_bytes())[:16] for p in STAGE_PROMPT.values()}}


# ---------------------------------------------------------------- helpers
def ex(p): return str(Path(p).expanduser())   # manifests store ~ instead of the home folder


def slug(p): return re.sub(r'[^A-Za-z0-9]+', '-', Path(p).stem).strip('-')[:48] or 'paper'


def preflight(pdf):
    doc = fitz.open(pdf); n = len(doc); chars = [len(pp.page_text(doc[i])) for i in range(n)]; pm = pp.page_map(doc); doc.close()
    return {'pages': n, 'chars_per_page': round(sum(chars) / max(n, 1)), 'text_layer': sum(chars) / max(n, 1) >= 200, 'page_map': pm, 'printed_page_source': pm[0]['source'] if pm else None, 'size_mb': round(Path(pdf).stat().st_size / 1e6, 2)}


def slice_pdf(pdf, pages, out, around=1, limit=0.5):
    """An excerpt of the PDF: the cited pages plus `around` neighbours on each side. Sol and Opus read only these pages (cheaper, and the long papers of the seed set run to 60 pages);
    returns (path, original page numbers) or (pdf, None) when the excerpt would be more than `limit` of the paper."""
    d = fitz.open(pdf); n = len(d); keep = sorted({q for pg in pages if pg for q in range(max(1, pg - around), min(n, pg + around) + 1)})
    if not keep or len(keep) > limit * n: d.close(); return pdf, None
    o = fitz.open()
    for q in keep: o.insert_pdf(d, from_page=q - 1, to_page=q - 1)
    o.save(out); o.close(); d.close(); return out, keep


def supp_note(p):
    if not p.get('supplements'): return ''
    n = p['main_pages']; out = f"\nPDF pages 1 to {n} are the paper. "
    for s_ in p['supplements']: out += f"PDF pages {n + 1} to {n + s_['pages']} are supplementary material ({s_['file']}); say 'Supplement' in the locator for evidence from them. "; n += s_['pages']
    return out


def excerpt_note(keep): return '' if not keep else '\nThis PDF is an excerpt. Its pages, in order, are original PDF pages ' + ', '.join(map(str, keep)) + '; use the ORIGINAL page numbers in your answer.'


def find_supplements(pdf):
    """Supplementary files next to a PDF: '<name> - supplement*.pdf' or '<name> - appendix*.pdf' in the same folder."""
    pdf = Path(pdf); out = []
    for x in sorted(pdf.parent.glob('*.pdf')):
        n = x.stem.lower()
        if x != pdf and any(n.startswith(pdf.stem.lower() + ' - ' + w) for w in ('supplement', 'appendix', 'supplementary')): out.append(x)
    return out


def combine_pdfs(main, supps, out):
    """One PDF: the paper, then each supplementary file; returns the page count of the paper and of each supplement."""
    o = fitz.open(); spans = []
    for f in [main] + list(supps):
        d = fitz.open(f); o.insert_pdf(d); spans.append((Path(f).name, len(d))); d.close()
    Path(out).parent.mkdir(parents=True, exist_ok=True); o.save(out); o.close(); return spans


def parse_json(text):
    t = text.strip(); t = re.sub(r'^```(?:json)?|```$', '', t, flags=re.M).strip(); i, j = t.find('{'), t.rfind('}')
    return json.loads(t[i:j + 1])


def pagemap_text(pm): return '; '.join(f"PDF page {r['pdf']} = printed page {r['printed']}" for r in pm[:80])


def est_tokens(r): return (len(r.system) + len(r.text)) / 3.5 + (TOK_PER_PAGE[L.provider_of(r.model)] * fitz.open(r.pdf).page_count if r.pdf else 0)


EXPECT_OUT = TOK['expected_share_used']   # expected share of the output budget actually used (the picost budget is sized close to need: 27,317 of 32,000 in the test)


def stage_cost(reqs, batch):
    worst = expected = 0.0
    for r in reqs:
        tin = est_tokens(r); pi, po = L.PRICE[r.model]; d = L.BATCH_DISCOUNT if batch else 1; fr = EXPECT_OUT.get(r.id.split('__')[-1], 0.7)
        worst += (tin * pi + r.max_tokens * po) / 1e6 * d; expected += (tin * pi + fr * r.max_tokens * po) / 1e6 * d
    return worst, expected


def digits_text(f):
    t = ' '.join([str(f.get('statement', ''))] + [str(x.get('text', '')) for x in f.get('spans', [])] + [str(n.get('value', '')) for n in f.get('numbers', [])])
    return {norm_num(x) for x in re.findall(r'-?\d*\.?\d+', t.replace(',', ''))}


def conflict(a, b):
    """True when the second reading (Sol) has a number that the first (Neon) lacks everywhere (numbers, statement, spans). A first-reader-only number (for example a sample
    size Sol left out) is not a conflict: the first real test counted every finding as a disagreement because Neon listed one more number than Sol, and Opus sided with Neon every time."""
    na = {norm_num(n.get('value')) for n in a.get('numbers', [])}; nb = {norm_num(n.get('value')) for n in b.get('numbers', [])}
    return any(x not in digits_text(a) for x in nb - na)   # the second reader found a value the first does not have: a different value or one the first missed. A number only the first reader has is not a conflict here: it was already checked to be on the PDF page


def norm_num(v):
    s = str(v).replace('−', '-').replace(',', '').replace('%', '').replace(' ', '').lower(); m = re.search(r'-?\d*\.?\d+', s); return m.group(0).lstrip('0') or '0' if m else s


# ---------------------------------------------------------------- requests per stage
def build(stage, M, run):
    P = M.m['papers']; reqs = []; system = (VAULT / STAGE_PROMPT[stage]).read_text(encoding='utf-8')
    q = f"\nReview-level question (context only; the paper's own questions come first): {M.m['question']}\n" if M.m.get('question') else ''
    for ck, p in P.items():
        if p.get('failed'): continue
        if stage == 'picost':
            if 'picost' in p.get('stages', {}): continue   # already extracted (a resume re-runs only the papers that failed)
            reqs.append(L.Req(f'{ck}__picost', STAGE_MODEL[stage], f"{q}Page map: {pagemap_text(p['preflight']['page_map'])}{supp_note(p)}\nExtract the findings now.", system, ex(p['pdf']), 'high', max_out('picost', p['preflight']['pages'])))
        elif stage == 'recheck':
            fl = [f for f in p.get('flagged', [])]
            if not fl or p.get('stages', {}).get('recheck', {}).get('status') == 'done': continue   # a finished recheck is not paid for twice on resume
            ps = json.loads((run / ck / 'picost.json').read_text())
            lines = []
            for f in ps['findings']:
                if f['id'] in fl:
                    pages = sorted({s.get('pdf_page') for s in f.get('spans', []) if s.get('pdf_page')} | {n.get('pdf_page') for n in f.get('numbers', []) if n.get('pdf_page')})
                    lines.append(f"- {f['id']}: outcome: {f.get('O', '')[:200]}; section: {f.get('section', '')}; look at PDF pages {pages}")
            pgs = sorted({s.get('pdf_page') for f in ps['findings'] if f['id'] in fl for s in f.get('spans', [])} | {n.get('pdf_page') for f in ps['findings'] if f['id'] in fl for n in f.get('numbers', [])}); sp, keep = slice_pdf(ex(p['pdf']), pgs, str(run / ck / 'slice_recheck.pdf'))
            reqs.append(L.Req(f'{ck}__recheck', STAGE_MODEL[stage], f"Page map: {pagemap_text(p['preflight']['page_map'])}{excerpt_note(keep)}\nFindings to extract independently:\n" + '\n'.join(lines), system, sp, 'high', max_out('recheck', len(fl))))
        elif stage == 'adjudicate':
            dis = p.get('disagreements', [])
            if not dis or p.get('stages', {}).get('adjudicate', {}).get('status') == 'done': continue
            ps = {f['id']: f for f in json.loads((run / ck / 'picost.json').read_text())['findings']}; rc = {f['id']: f for f in p.get('recheck', {}).get('findings', [])}
            blob = json.dumps([{'id': i, 'reader_A': {k: ps[i].get(k) for k in ('statement', 'P', 'I', 'C', 'O', 'numbers', 'spans')}, 'reader_B': rc.get(i)} for i in dis], ensure_ascii=False)
            pgs = sorted({s.get('pdf_page') for i in dis for s in ps[i].get('spans', [])} | {s.get('pdf_page') for i in dis for s in (rc.get(i) or {}).get('spans', [])}); sp, keep = slice_pdf(ex(p['pdf']), pgs, str(run / ck / 'slice_adjudicate.pdf'))
            reqs.append(L.Req(f'{ck}__adjudicate', STAGE_MODEL[stage], f"Page map: {pagemap_text(p['preflight']['page_map'])}{excerpt_note(keep)}\nFindings in dispute:\n{blob}", system, sp, 'high', max_out('adjudicate', len(dis))))
    return reqs


# ---------------------------------------------------------------- local stage: spans
def stage_spans(M, run):
    P = M.m['papers']
    for ck, p in P.items():
        if p.get('failed') or 'picost' not in p.get('stages', {}): continue
        out = run / ck; hl = out / 'highlights'; hl.mkdir(parents=True, exist_ok=True); ps = json.loads((out / 'picost.json').read_text()); doc = fitz.open(ex(p['pdf'])); flagged = {}; total = miss = 0; ptxt = ' '.join(pp.norm(pp.page_text(doc[i])) for i in range(len(doc)))
        for f in ps.get('findings', []):
            why = []; regs = {}
            if f.get('confidence', 'high') == 'low': why.append('low_confidence')
            if M.m.get('flag_medium') and f.get('confidence') == 'medium': why.append('medium_confidence')
            pgs = {s.get('pdf_page') for s in f.get('spans', []) if s.get('pdf_page')} | {n.get('pdf_page') for n in f.get('numbers', []) if n.get('pdf_page')}
            if len(pgs) > 1: why.append('multi_page')   # judged from the pages actually cited: the first real test showed Neon's own multi_page flag was true for 24 of 29 single-page findings, which cost $0.64 in needless rechecks
            elif f.get('multi_page'): f['model_says_multi_page_but_one_page'] = True
            if not p['preflight']['text_layer']: why.append('no_text_layer')
            for k, s in enumerate(f.get('spans', [])):
                total += 1; r = pp.find_quote(doc, s.get('text', ''))
                s['found'] = r['found']; s['pages_found'] = r['pages']
                if not r['found']: miss += 1; why.append('span_not_found'); continue
                if s.get('pdf_page') and s['pdf_page'] not in r['pages']: why.append('span_on_other_page')
                page = doc[r['pages'][0] - 1]; rects = pp.locate_rects(page, s['text']); s['bbox'] = [[round(x, 1) for x in (q.x0, q.y0, q.x1, q.y1)] for q in rects]
                if rects: regs.setdefault(r['pages'][0], []).extend(s['bbox'])
                if rects:
                    pg = fitz.open(ex(p['pdf']))[r['pages'][0] - 1]
                    for q in rects: a = pg.add_highlight_annot(q); a.set_colors(stroke=pp.HIGHLIGHT['EVD']); a.update()
                    pg.get_pixmap(dpi=120).save(str(hl / f"{f['id']}_s{k + 1}_p{r['pages'][0]}.png"))
            if len(regs) > 1:   # evidence over a page break: one merged screenshot, pieces stacked with a thin white gap
                m = pp.merge_regions(ex(p['pdf']), sorted(regs.items()), str(hl / f"{f['id']}_merged_p{'-'.join(map(str, sorted(regs)))}.png"), dpi=150); f['merged_screenshot'] = Path(m['out']).name if m.get('ok') else None
            for n in f.get('numbers', []):   # loosened (JP, 2026-11-25): look at each number inside the value, ignore single digits, and flag only if fewer than half of them are anywhere in the PDF text
                toks = [t for t in re.findall(r'\d+(?:[.,]\d+)?', str(n.get('value', ''))) if len(re.sub(r'\D', '', t)) >= 2]
                if toks and sum(1 for t in toks if pp.norm(t) in ptxt) / len(toks) < 0.5: why.append('number_not_in_pdf_text')
            f['flags'] = sorted(set(why))
            if why: flagged[f['id']] = f['flags']
        qmiss = 0
        for kind, key_ in (('questions', 'original_wording'), ('claims', None), ('caveats', None)):   # the quotes behind the questions, claims and caveats must be in the PDF too
            for it in ps.get(kind, []):
                qt = it.get(key_) if key_ else (it.get('span') or {}).get('text', '')
                it['found'] = bool(qt) and pp.find_quote(doc, qt)['found']; qmiss += 0 if it['found'] else 1
        p['quotes_not_found_other'] = qmiss
        doc.close(); (out / 'picost.json').write_text(json.dumps(ps, indent=1, ensure_ascii=False), encoding='utf-8')
        p['flagged'] = sorted(flagged); p['span_miss_rate'] = round(miss / max(total, 1), 3); p['stages']['spans'] = {'status': 'done', 'spans': total, 'not_found': miss, 'flagged': len(flagged)}
        M.event(f"[{ck}] spans: {total} checked, {miss} not found, {len(flagged)} of {len(ps.get('findings', []))} findings flagged")
        if total and miss / total > MAX_SPAN_MISS: raise Halt(f'{ck}: {miss} of {total} spans not found in the PDF (over {MAX_SPAN_MISS:.0%}): the extraction is unreliable')


# ---------------------------------------------------------------- remote stage
def stop_file(M): return (M.dir / 'STOP').exists()


def run_stage(stage, M, mode):
    run = M.dir; reqs = build(stage, M, run); st = M.m['stage_log'].setdefault(stage, {})
    if st.get('status') == 'done': return
    if not reqs: st.update(status='done', note='nothing to do'); M.event(f'stage {stage}: nothing to do'); return
    batch = mode == 'batch'; worst, expected = stage_cost(reqs, batch)
    if 'job' not in st:   # fresh submission
        if stop_file(M): raise Halt('STOP file present')
        if M.m['spent_usd'] + worst > M.m['cap_usd']: raise Halt(f"stage {stage}: spent ${M.m['spent_usd']:.2f} + worst case ${worst:.2f} would pass the ${M.m['cap_usd']:.2f} cap; nothing was submitted")
        st.update(model=STAGE_MODEL[stage], mode=mode, requests=len(reqs), est_expected_usd=round(expected, 3), est_worst_usd=round(worst, 3), started=now()); M.save()
        M.event(f"stage {stage}: {len(reqs)} request(s) to {STAGE_MODEL[stage]} ({mode}); expected ${expected:.2f}, worst case ${worst:.2f}; spent so far ${M.m['spent_usd']:.2f} of ${M.m['cap_usd']:.2f}")
        up = L.upload_pdfs(reqs, GEM_FILES)
        if up: M.m.setdefault('gemini_files', []).extend(up); M.save(); M.event(f'{len(up)} PDF(s) sent through the Gemini File API')
        if batch:
            job = L.submit_batch(reqs); st['job'] = job; M.save(); M.event(f"stage {stage}: batch job {job['id']} submitted")
        else:
            res = L.run_standard(reqs); st['job'] = {'provider': L.provider_of(STAGE_MODEL[stage]), 'id': 'standard', 'ids': {r.id: r.id for r in reqs}, 'results': {k: vars(v) for k, v in res.items()}}; M.save()
    job = st['job']
    strag = S.wait_jobs(M, [job]) if job['id'] != 'standard' else False   # a batch job: wait; stragglers are cancelled after the grace period and go to human review
    if job['id'] != 'standard' and not strag and L.poll_batch(job) == 'failed': raise Halt(f"stage {stage}: batch job {job['id']} failed or expired")
    results = {k: L.Res(**v) for k, v in job['results'].items()} if job['id'] == 'standard' else L.fetch_batch(job)
    actual = 0.0; failed = 0
    for r in reqs:
        x = results[r.id]; ck = r.id.split('__')[0]; c = L.cost(r.model, x.tin, x.tout, batch); actual += c
        cl.record(M.m['run_id'], stage, r.model, STAGE_PROMPT[stage], provider=L.provider_of(r.model), citekey=ck, effort=r.effort, tokens_in=x.tin, tokens_out=x.tout, latency_s=None, output_text=x.text or None, notes=f"mode={mode}; cost_usd={c:.4f}; finish={x.finish}; err={x.err}")
        p = M.m['papers'][ck]
        try:
            if not x.ok or x.finish in ('MAX_TOKENS', 'max_tokens', 'incomplete'): raise ValueError(f'request not completed ({x.finish} {x.err})')
            data = parse_json(x.text)
            if stage == 'picost':
                (run / ck).mkdir(exist_ok=True); (run / ck / 'picost.json').write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding='utf-8'); p['stages']['picost'] = {'status': 'done', 'findings': len(data.get('findings', [])), 'tokens_in': x.tin, 'tokens_out': x.tout, 'cost_usd': round(c, 4)}
            elif stage == 'recheck':
                p['recheck'] = data; ps = {f['id']: f for f in json.loads((run / ck / 'picost.json').read_text())['findings']}; dis = []
                for f in data.get('findings', []):
                    if conflict(ps.get(f['id'], {}), f) or not f.get('found', True): dis.append(f['id'])
                p['disagreements'] = dis; p['stages']['recheck'] = {'status': 'done', 'rechecked': len(data.get('findings', [])), 'disagree': len(dis), 'cost_usd': round(c, 4)}
            elif stage == 'adjudicate':
                p['adjudication'] = data; p['unsure'] = [a['id'] for a in data.get('adjudications', []) if a.get('verdict') in ('unsure', 'neither')]; p['stages']['adjudicate'] = {'status': 'done', 'unsure': len(p['unsure']), 'cost_usd': round(c, 4)}
        except Exception as e:
            failed += 1; p['failed'] = f'{stage}: {str(e)[:200]}'; M.event(f"[{ck}] {stage} FAILED: {p['failed']}")
    M.m['spent_usd'] = round(M.m['spent_usd'] + actual, 4); st.update(status='done', actual_usd=round(actual, 4), ended=now(), failed=failed); M.save()
    M.event(f"stage {stage}: done, actual ${actual:.3f} (expected ${expected:.3f}); total spent ${M.m['spent_usd']:.2f} of ${M.m['cap_usd']:.2f}")
    if M.m['spent_usd'] > M.m['cap_usd']: raise Halt('spend passed the cap')
    if actual > OVERRUN * expected: raise Halt(f'stage {stage} cost ${actual:.2f}, more than {OVERRUN}x its expected ${expected:.2f}')
    if sum(1 for p in M.m['papers'].values() if p.get('failed')) >= 2: raise Halt('two or more papers failed')


# ---------------------------------------------------------------- final report
def finish(M):
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        ps = json.loads((M.dir / ck / 'picost.json').read_text()); lines = [f"# Review: {ck}", '', f"PDF: {Path(p['pdf']).name} ({p['preflight']['pages']} pages, text layer: {p['preflight']['text_layer']})", '', '## Spot check A (JP): read these first', '']
        adj = {a['id']: a for a in (p.get('adjudication') or {}).get('adjudications', [])}
        for f in ps.get('findings', []):
            tag = f.get('flags', []); a = adj.get(f['id'])
            mark = 'NEEDS JP' if (f['id'] in p.get('unsure', [])) else ('adjudicated: ' + a['verdict'] if a else ('agreed by GPT-6.2 Sol' if f['id'] in p.get('flagged', []) and f['id'] not in p.get('disagreements', []) else 'not flagged'))
            lines.append(f"- **{f['id']}** ({f.get('tier', '?')}) [{mark}] {f.get('statement', '')[:220]} (flags: {', '.join(tag) or 'none'})")
        (M.dir / ck / 'review.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    M.m['status'] = 'awaiting_spot_check_a'; M.event(f"run finished: status awaiting_spot_check_a; spent ${M.m['spent_usd']:.2f} of ${M.m['cap_usd']:.2f}")
    with open(RUNS / 'ledger.jsonl', 'a') as f: f.write(json.dumps({'run_id': M.m['run_id'], 'date': now(), 'mode': M.m['mode'], 'spent_usd': M.m['spent_usd'], 'status': M.m['status'], 'pdf_sha256': [p['sha256'] for p in M.m['papers'].values()]}) + '\n')


def seen_hashes():
    f = RUNS / 'ledger.jsonl'; return {h for l in f.read_text().splitlines() if l.strip() for h in json.loads(l).get('pdf_sha256', [])} if f.exists() else set()


def cleanup_files(M):
    for n in M.m.pop('gemini_files', []): L.gemini_delete(n)   # uploaded PDFs are deleted when the run ends
    M.save()


def halt(M, reason):
    cleanup_files(M)
    for st in M.m['stage_log'].values():
        j = st.get('job')
        if j and j.get('id') != 'standard' and st.get('status') != 'done': M.event(f"cancelling batch job {j['id']}: {L.cancel_batch(j)}")
    M.m['status'] = 'stopped'; M.m['stop_reason'] = reason; M.event(f'STOPPED: {reason}'); sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); ap.add_argument('pdfs', nargs='*'); ap.add_argument('--mode', choices=['standard', 'batch'], help='REQUIRED for a new run. Ask JP each time papers are given: standard (answers now, full price) or batch (about half price, slower, can stall)')
    ap.add_argument('--cap', type=float, default=CAP); ap.add_argument('--question', default=C.PIPE.get('project_question', ''), help='the overarching project question (default: project_question in pipeline.json); every question found in a paper is taken to fit under it. Pass "" to leave it out'); ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--resume'); ap.add_argument('--new-batch', action='store_true', help='with --resume: start a new batch of the same run with a fresh cap (the earlier spend is kept in spent_previous_batches)'); ap.add_argument('--run-id')
    ap.add_argument('--fast', action='store_true', help='standard mode for every stage, and drafting and quality signals at the same time: about 25 minutes for four papers, at about twice the cost'); ap.add_argument('--skip', nargs='*', default=[], choices=['checks', 'draft', 'qs'], help='leave out the later stages'); ap.add_argument('--allow-repeat', action='store_true'); ap.add_argument('--flag-medium', action='store_true', help='also send medium-confidence findings to the independent recheck (more cost, fewer misses)'); a = ap.parse_args()
    cl.load_env()
    if a.resume:
        M = Manifest(a.resume)
        if not M.m: sys.exit('no such run')
        mode = M.m['mode']
        M.m['status'] = 'running'; M.m.pop('stop_reason', None)
        if a.new_batch:
            M.m.setdefault('spent_previous_batches', []).append({'spent_usd': M.m['spent_usd'], 'ended': now(), 'cap_usd': M.m['cap_usd']}); M.m['spent_usd'] = 0.0; M.m['cap_usd'] = min(a.cap, CAP) if a.cap else CAP; M.save()
    else:
        if not a.pdfs: ap.error('give 1 to %d PDFs' % MAX_PAPERS)
        if len(a.pdfs) > MAX_PAPERS: sys.exit(f'Refused: {len(a.pdfs)} PDFs. The limit is {MAX_PAPERS} papers per batch.')
        if a.cap > CAP: sys.exit(f'Refused: the cap per batch is ${CAP}; --cap can only lower it.')
        pdfs = [Path(p).expanduser().resolve() for p in a.pdfs]
        for p in pdfs:
            if not p.exists() or p.suffix.lower() != '.pdf': sys.exit(f'Not a PDF: {p}')
        if len({str(p) for p in pdfs}) != len(pdfs): sys.exit('The same PDF is listed twice.')
        papers = {}; seen = seen_hashes(); day = datetime.now().strftime('%Y-%m-%d'); n = 1 + len(list(RUNS.glob(f'{day}_batch*'))); run_id = a.run_id or f'{day}_batch{n:02d}'; mode = 'standard' if a.fast else a.mode
        if not (a.fast or a.mode): sys.exit('Refused: choose a mode. Ask JP each time papers are given: --mode standard (answers now, full price, no queue) or --mode batch (about half price, slower, can stall) or --fast. See Skill-controls.md, "Standard or batch: always ask".')
        for p in pdfs:
            h = sha(p.read_bytes()); ck = slug(p)
            if h in seen and not a.allow_repeat: sys.exit(f'Refused: {p.name} was already processed in an earlier run (same SHA-256). Use --allow-repeat to run it again.')
            if ck in papers: ck = f'{ck}-{h[:6]}'
            entry = {'sha256': h, 'stages': {}}; src = p; supps = find_supplements(p)
            if supps:   # the paper and its supplementary files are read as one PDF
                comb = RUNS / run_id / ck / 'combined.pdf'; sp = combine_pdfs(p, supps, comb); src = comb
                entry['supplements'] = [{'file': n_, 'pages': k} for n_, k in sp[1:]]; entry['main_pages'] = sp[0][1]; entry['supplement_sha256'] = [sha(x.read_bytes())[:16] for x in supps]
                print(f"{p.name}: {len(supps)} supplementary file(s) combined after the paper ({sp[0][1]} + {sum(k for _, k in sp[1:])} pages)")
            entry['pdf'] = str(src).replace(str(Path.home()), '~'); entry['preflight'] = preflight(src); entry['source_pdf'] = p.name; papers[ck] = entry
        M = Manifest(run_id, {'run_id': run_id, 'created_utc': now(), 'status': 'planned', 'mode': mode, 'cap_usd': a.cap, 'max_papers': MAX_PAPERS, 'overrun_factor': OVERRUN, 'max_span_miss': MAX_SPAN_MISS, 'spent_usd': 0.0,
                              'question': a.question, 'flag_medium': a.flag_medium, 'models': STAGE_MODEL, 'prompts': STAGE_PROMPT, 'environment': environment(), 'papers': papers, 'stage_log': {}})
        M.save()
    print(f"run {M.m['run_id']}: {len(M.m['papers'])} paper(s), mode {mode}, cap ${M.m['cap_usd']}")
    if a.dry_run:
        batch = mode == 'batch'; tot_w = tot_e = 0.0
        for st in ('picost', 'recheck', 'adjudicate'):
            reqs = []
            for ck, p in M.m['papers'].items():
                reqs.append(L.Req(f'{ck}__{st}', STAGE_MODEL[st], 'x' * 800, (VAULT / STAGE_PROMPT[st]).read_text(encoding='utf-8'), ex(p['pdf']), 'high', max_out('picost', p['preflight']['pages']) if st == 'picost' else STAGE_MAX_OUT[st]))
            w, e = stage_cost(reqs, batch); tot_w += w; tot_e += e; print(f'  {st:11s} {STAGE_MODEL[st]:18s} expected ${e:5.2f}  worst case ${w:5.2f}   (recheck and adjudicate run only for flagged findings; shown for all papers)')
        pg = sum(p['preflight']['pages'] for p in M.m['papers'].values()); n_p = len(M.m['papers']); d_ = 0.5 if batch else 1.0
        rough = {'checks': 0.15 * n_p * d_, 'draft': 1.9 * n_p * d_, 'qs': (0.25 * n_p + 0.015 * pg) * d_}   # rough, from the one-page smoke test and per-call prices; the pilot replaces these
        for k_, v_ in rough.items(): print(f'  {k_:11s} (several models) rough estimate ${v_:5.2f}   (not measured on a real paper yet)'); tot_e += v_; tot_w += v_ * 1.4
        for ck, p in M.m['papers'].items(): pf = p['preflight']; print(f"  {ck}: {pf['pages']} pages, text layer {pf['text_layer']}, {pf['size_mb']} MB, page numbers from {pf['printed_page_source']}")
        print(f'  total expected ${tot_e:.2f}, worst case ${tot_w:.2f}, cap ${M.m["cap_usd"]}'); M.m['status'] = 'dry-run'; M.save(); return
    M.m['status'] = 'running'; M.save()
    try:
        run_stage('picost', M, mode)
        if 'spans' not in M.m['stage_log'] or M.m['stage_log']['spans'].get('status') != 'done': stage_spans(M, M.dir); M.m['stage_log']['spans'] = {'status': 'done'}; M.save()
        run_stage('recheck', M, mode); run_stage('adjudicate', M, mode)
        if 'checks' not in a.skip: S.stage_checks(M, mode)
        if a.fast and 'draft' not in a.skip and 'qs' not in a.skip:   # drafting and quality signals do not depend on each other: run them at the same time
            import threading; errs = []
            def _go(fn):
                try: fn(M, mode)
                except Exception as e_: errs.append(e_)
            ts = [threading.Thread(target=_go, args=(S.stage_draft,)), threading.Thread(target=_go, args=(S.stage_qs,))]; [t_.start() for t_ in ts]; [t_.join() for t_ in ts]
            if errs: raise errs[0]
        else:
            if 'draft' not in a.skip: S.stage_draft(M, mode)
            if 'qs' not in a.skip: S.stage_qs(M, mode)
        cleanup_files(M); finish(M)
    except Halt as e: halt(M, str(e))
    except KeyboardInterrupt:
        M.m['status'] = 'interrupted'; M.event(f"interrupted; resume with: python3 lives_run.py --resume {M.m['run_id']}"); sys.exit(130)


if __name__ == '__main__': main()

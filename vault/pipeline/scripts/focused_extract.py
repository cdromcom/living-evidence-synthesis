#!/usr/bin/env python3
"""Focused extraction from supplementary material (JP, 2026-11-26). For the findings of one paper that are wrong or incomplete in a finished run, a model (Claude Sonnet 5.5, batch API) reads the supplementary Word files and returns the missing numbers and the exact supplement text that holds them. The code checks that each returned span really is in the supplement text, then adds the numbers and spans to the run's picost.json (marked source = supplement) and re-runs the numbers-list check.
  python3 focused_extract.py RUN PAPER_PREFIX SUPPLEMENT_DIR --findings F1 F9 F10 ... [--model claude-sonnet-5-5] [--cap-usd 1.0] [--apply-only]
Supplement text comes from every .docx in SUPPLEMENT_DIR (paragraphs and table rows; pictures are not read, only their captions)."""
import argparse, json, re, sys, time, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import llm_batch as L, call_logger as cl, pdf_pages as pp, lives_run as LR

def docx_text(path):
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf8'); out = []
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p[ >].*?</w:p>', xml, flags=re.S):
        s = m.group(0)
        if s.startswith('<w:tbl>'):
            for r in re.findall(r'<w:tr[ >].*?</w:tr>', s, flags=re.S):
                cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<w:tc>.*?</w:tc>', r, flags=re.S)]
                out.append(' | '.join(cells))
        else:
            t = re.sub(r'<[^>]+>', '', s).strip()
            if t and 'PAGEREF' not in t and not t.startswith('TOC'): out.append(t)
    return '\n'.join(out)

SYS = """You correct the extraction of ONE finding from a research paper using the paper's SUPPLEMENTARY MATERIAL (given below, as text; each file is introduced by its name). You are given the finding as extracted from the main paper (statement, numbers list, spans). Some numbers in the statement may be missing from the numbers list, or may be supported only by a supplementary table or figure caption.
Do this:
1. For every number in the finding's statement that has no entry in its numbers list, or whose entry is wrong, find it in the supplement. Return a `numbers_to_add` entry: label, value (as printed), unit, `source` (file name and table or figure, for example "mmc5 Supplementary Table 2"), `row` and `column` labels exactly as printed.
2. Return `spans_to_add`: each is the table row or sentence of the supplement that holds the numbers, copied CHARACTER FOR CHARACTER from the supplement text (a table row is one line with cells separated by " | "), with its `source`. Keep each span to one row or one sentence.
3. If a number in the statement is contradicted by the supplement, say so in `contradictions` (what the statement says, what the supplement says). Do not rewrite the statement.
4. If the supplement does not hold what is missing, return empty lists and say so in `note`.
Use only the supplement text. Return one JSON object and nothing else:
{"id": "F1", "numbers_to_add": [{"label": "", "value": "", "unit": "", "source": "", "row": "", "column": ""}], "spans_to_add": [{"text": "", "source": ""}], "contradictions": [], "note": ""}

SUPPLEMENTARY MATERIAL:
"""
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('paper'); ap.add_argument('supp_dir'); ap.add_argument('--findings', nargs='+', required=True); ap.add_argument('--model', default='claude-sonnet-5-5'); ap.add_argument('--cap-usd', type=float, default=1.0); a = ap.parse_args()
    cl.load_env(); run = cl.RUNS / a.run; M = json.load(open(run / 'manifest.json')); ck = next(k for k in M['papers'] if k.startswith(a.paper))
    files = sorted(Path(a.supp_dir).expanduser().glob('*.docx')); supp = ''; texts = {}
    for f in files: texts[f.name] = docx_text(f); supp += f"\n\n=== FILE {f.name} ===\n" + texts[f.name]
    alltext = pp.norm(supp); ps = json.load(open(run / ck / 'picost.json')); fnd = {f['id']: f for f in ps['findings']}; reqs = []
    for fid in a.findings:
        f = fnd[fid]; body = {'id': fid, 'statement': f['statement'], 'numbers_list': f.get('numbers', []), 'spans': [s['text'] for s in f.get('spans', [])]}
        reqs.append(L.Req(f'{ck[:12]}__focus__{fid}', a.model, 'The finding to correct:\n' + json.dumps(body, ensure_ascii=False), SYS + supp, None, 'medium', 4000))
    worst = sum(L.cost(r.model, (len(r.system) + len(r.text)) / 3.5, r.max_tokens, True) for r in reqs); print(len(reqs), 'findings; worst case $%.2f' % worst)
    if worst > a.cap_usd: sys.exit('over the cap')
    job = L.submit_batch(reqs)
    while L.poll_batch(job) == 'running': time.sleep(20)
    res = L.fetch_batch(job); spent = 0.0; report = {}
    for r in reqs:
        x = res[r.id]; spent += L.cost(a.model, x.tin, x.tout, True); fid = r.id.split('__')[-1]
        try: j = json.loads(re.search(r'\{.*\}', x.text, re.S).group(0))
        except Exception: report[fid] = {'error': (x.err or x.text or '')[:120]}; continue
        f = fnd[fid]; added_n = added_s = 0; rejected = []
        for s in j.get('spans_to_add', []):
            t = (s.get('text') or '').strip()
            if t and pp.norm(t) in alltext:
                f.setdefault('spans', []).append({'text': t, 'pdf_page': None, 'found': True, 'match': 'exact', 'source': s.get('source', 'supplement'), 'from_supplement': True}); added_s += 1
            else: rejected.append(t[:80])
        for n in j.get('numbers_to_add', []):
            f.setdefault('numbers', []).append({'label': n.get('label', ''), 'value': n.get('value', ''), 'unit': n.get('unit', ''), 'table_or_figure': n.get('source', ''), 'row': n.get('row', ''), 'column': n.get('column', ''), 'pdf_page': None, 'printed_page': '', 'from_supplement': True}); added_n += 1
        f['numbers_list_gaps'] = LR.numbers_list_gaps(f); f['corrected_from_supplement'] = True
        f['flags'] = sorted((set(f.get('flags', [])) - {'span_not_found', 'number_not_in_numbers_list'}) | ({'number_not_in_numbers_list'} if f['numbers_list_gaps']['missing'] else set()))
        report[fid] = {'numbers_added': added_n, 'spans_added': added_s, 'spans_rejected_not_in_supplement': rejected, 'contradictions': j.get('contradictions', []), 'still_missing': f['numbers_list_gaps']['missing'], 'note': j.get('note', '')}
    (run / ck / 'picost.json').write_text(json.dumps(ps, indent=1, ensure_ascii=False), encoding='utf-8')
    (run / ck / 'focused_extraction_from_supplement.json').write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(report, indent=1, ensure_ascii=False)[:3500]); print('cost about $%.2f' % spent)
if __name__ == '__main__': main()

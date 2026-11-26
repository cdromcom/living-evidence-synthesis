#!/usr/bin/env python3
"""Vision check of quotes that differ from the PDF text layer (JP, 2026-11-26). For every extracted span whose match level is `letters_digits`, a vision model (Claude Sonnet 5.5, batch API) is shown the highlighted screenshot plus two texts, the extraction model's quote and the PDF text layer's text, and says what is printed, and whether each text equals the print.
  python3 quote_vision_check.py RUN [--model claude-sonnet-5-5] [--cap-usd 1.0]
Writes pipeline/runs/<RUN>/quote_vision_check.json and prints a summary."""
import argparse, json, os, re, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz, pdf_pages as pp, llm_batch as L, call_logger as cl
SYS = """You compare quotes with a screenshot of a research paper page. The highlighted text in the screenshot is the passage. You are given two texts: TEXT A (written by a model that read the page) and TEXT B (the PDF's hidden text layer at that spot). Step 1: transcribe the highlighted passage exactly as it is printed, character for character, including symbols, Greek letters, dashes and signs. Step 2: for each of TEXT A and TEXT B say whether it equals the print. Ignore line breaks, extra spaces and words split by a hyphen at a line end. Name every real difference in a few words (for example: "print has the superscript plus sign, text A has no sign"). Return one JSON object and nothing else:
{"printed": "...", "a_equals_print": true, "a_differences": ["..."], "b_equals_print": true, "b_differences": ["..."]}"""
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--model', default='claude-sonnet-5-5'); ap.add_argument('--cap-usd', type=float, default=1.0); a = ap.parse_args()
    cl.load_env(); run = cl.RUNS / a.run; M = json.load(open(run / 'manifest.json')); reqs = []; meta = {}
    for ck, p in M['papers'].items():
        f_ = run / ck / 'picost.json'
        if not f_.exists(): continue
        ps = json.load(open(f_)); pdf = os.path.expanduser(p['pdf']); doc = fitz.open(pdf); out = run / ck / 'vision_crops'; out.mkdir(exist_ok=True)
        for f in ps['findings']:
            for k, s in enumerate(f['spans'], 1):
                if s.get('match') != 'letters_digits': continue
                w = s['text'].split(); tb = pp.text_between(doc, ' '.join(w[:8]), ' '.join(w[-8:]), s.get('pdf_page'))
                if not tb: continue
                d2 = fitz.open(pdf); r = pp.crop_quote(d2, tb['raw'], str(out / f"{f['id']}_s{k}.png"), dpi=170, pad=26, tight_x=True); d2.close()
                if not r.get('ok'): continue
                rid = f"{ck[:12]}__{f['id']}_s{k}"; meta[rid] = {'paper': ck, 'finding': f['id'], 'span': k, 'pdf_page': tb['page'], 'text_a': s['text'], 'text_b': tb['raw']}
                reqs.append(L.Req(rid, a.model, f"TEXT A (model):\n{s['text']}\n\nTEXT B (PDF text layer):\n{tb['raw']}", SYS, None, 'low', 1500, images=[r['out']]))
    print(len(reqs), 'quotes to check with', a.model)
    worst = sum(L.cost(r.model, 1800, r.max_tokens, True) for r in reqs); print(f'worst case ${worst:.2f}')
    if worst > a.cap_usd: sys.exit('over the cap')
    job = L.submit_batch(reqs)
    while L.poll_batch(job) == 'running': time.sleep(20)
    res = L.fetch_batch(job); outj = {}; spent = 0.0
    for rid, x in res.items():
        spent += L.cost(a.model, x.tin, x.tout, True)
        try: j = json.loads(re.search(r'\{.*\}', x.text, re.S).group(0))
        except Exception: j = {'error': (x.err or x.text or '')[:100]}
        outj[rid] = {**meta[rid], **j}
    (run / 'quote_vision_check.json').write_text(json.dumps(outj, indent=1, ensure_ascii=False), encoding='utf-8')
    n = len(outj); a_ok = sum(1 for v in outj.values() if v.get('a_equals_print')); b_ok = sum(1 for v in outj.values() if v.get('b_equals_print'))
    print(f'{n} checked: the extraction model\'s quote equals the print in {a_ok}; the PDF text layer equals the print in {b_ok}; cost about ${spent:.2f}')
if __name__ == '__main__': main()

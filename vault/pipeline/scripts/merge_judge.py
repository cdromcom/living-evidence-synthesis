#!/usr/bin/env python3
"""Blinded second opinion on candidate node pairs (JP, 2026-11-25): Claude Sonnet 5.5 reads each pair and says merge / keep_separate / group_under_umbrella.
It never merges anything. With --second, GPT-6.2 Sol is a blinded second judge; a human verifies every merge.
  python3 merge_judge.py --type CVT --top 25 --run-id 2026-11-25-merge-judge [--type QUE --top 10]
Reads pipeline/misc/evd-validation/embedding-candidates/candidates.tsv; writes judgments.tsv and judgments.md beside it; logs every call with call_logger."""
import argparse, csv, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2]); D = VAULT / 'sysrev/dgraph'
FOLDER = {'QUE': 'questions', 'CLM': 'claims', 'CVT': 'caveats', 'EVD': 'evidence'}
def body(typ, name):
    t = (D / FOLDER[typ] / (name + '.md')).read_text(encoding='utf-8'); m = re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M)
    q = re.search(r'> \[!info\] Quotes\s*\n((?:>[^\n]*\n?)+)', t); p = re.search(r'> \[!info\] Papers\s*\n((?:>[^\n]*\n?)+)', t)
    return f"Title: {m.group(1) if m else name}\nPapers: {', '.join(sorted(set(re.findall(r'(@[A-Za-z0-9-]+)', p.group(1))))) if p else 'n/a'}\nQuote: {re.sub(r'^> ?', '', q.group(1), flags=re.M).strip()[:700] if q else 'n/a'}"
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--type', action='append', required=True); ap.add_argument('--top', type=int, action='append', required=True)
    ap.add_argument('--run-id', required=True); ap.add_argument('--model', default='claude-sonnet-5-5'); ap.add_argument('--second', action='store_true', help='also ask GPT-6.2 Sol, blinded to the first judge'); a = ap.parse_args()
    cdir = VAULT / 'pipeline/misc/evd-validation/embedding-candidates'; rows = list(csv.DictReader(open(cdir / 'candidates.tsv'), delimiter='\t'))
    prompt_file = 'pipeline/prompts/merge-judge-v1.md'; tpl = (VAULT / prompt_file).read_text(encoding='utf-8').split('\n', 2)[2]
    jobs = []
    for typ, top in zip(a.type, a.top): jobs += [r for r in rows if r['type'] == typ][:top]
    def parse(text):
        m = re.search(r'\{.*\}', text, re.S)
        try: return json.loads(m.group(0))
        except Exception: return {'verdict': 'unparsed', 'differences': [], 'reason': (text or '')[:120]}
    def one(r):
        prompt = tpl.replace('{A}', body(r['type'], r['node_a'])).replace('{B}', body(r['type'], r['node_b'])); node = f"{r['node_a']} || {r['node_b']}"
        text, rec = cl.logged_anthropic(a.run_id, 'merge-judge', a.model, prompt_file, prompt, effort='medium', max_tokens=800, node=node)
        j = parse(text); out = {**r, 'verdict': j.get('verdict'), 'differences': '; '.join(j.get('differences', [])), 'reason': j.get('reason', '')}
        if a.second:
            try: it, _ = cl.logged_openai(a.run_id, 'merge-judge', 'gpt-6.2-sol', prompt_file, prompt, effort='medium', node=node); ij = parse(it)
            except Exception as e: ij = {'verdict': 'error', 'differences': [], 'reason': repr(e)[:100]}
            out.update({'second_verdict': ij.get('verdict'), 'second_reason': ij.get('reason', ''), 'agree': 'yes' if ij.get('verdict') == j.get('verdict') else 'no'})
        return out
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(one, jobs))
    with open(cdir / 'judgments.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, list(res[0].keys()), delimiter='\t'); w.writeheader(); w.writerows(res)
    md = ['# Second opinion on candidate pairs (Claude Sonnet 5.5' + (' and GPT-6.2 Sol' if a.second else '') + ', each blinded to the other)', '', 'Verdicts are advice for the human verifier, not decisions. Nothing was merged.', '']
    for typ in a.type:
        ink = a.second
        md += [f'## {typ}', '', '| # | A | B | Similarity | Sonnet 5.5 | ' + ('GPT-6.2 Sol | Agree | ' if ink else '') + 'What differs | Reason |', '|---|---|---|---|---|' + ('---|---|' if ink else '') + '---|---|']
        for n, r in enumerate([x for x in res if x['type'] == typ], 1): md.append(f"| {n} | {r['node_a'].split(' - ', 1)[-1][:90]} | {r['node_b'].split(' - ', 1)[-1][:90]} | {r['sim_title']} | **{r['verdict']}** | " + (f"**{r['second_verdict']}** | {r['agree']} | " if ink else '') + f"{r['differences'][:120]} | {r['reason']} |")
        md.append('')
    (cdir / 'judgments.md').write_text('\n'.join(md), encoding='utf-8')
    import collections; print(collections.Counter((r['type'], r['verdict']) for r in res))
    if a.second: print('agreement Sol vs Sonnet:', collections.Counter((r['type'], r['agree']) for r in res))
if __name__ == '__main__': main()

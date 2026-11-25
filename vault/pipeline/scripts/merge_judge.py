#!/usr/bin/env python3
"""Blinded second opinion on candidate node pairs (JP, 2026-11-25): Claude Sonnet 5.5 reads each pair and says merge / keep_separate / group_under_umbrella.
It never merges anything. Inkling 2 Small (Tinker) is the planned second judge and is not wired up yet; a human verifies every merge.
  python3 merge_judge.py --type CVT --top 25 --run-id 2026-11-25-merge-judge [--type QUE --top 10]
Reads pipeline/misc/evd-validation/embedding-candidates/candidates.tsv; writes judgments.tsv and judgments.md beside it; logs every call with call_logger."""
import argparse, csv, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2]); D = VAULT / 'sysrev/dgraph'
FOLDER = {'QUE': 'questions', 'CLM': 'claims', 'CVT': 'caveats', 'EP': 'evd-patterns', 'EVD': 'evidence'}
def body(typ, name):
    t = (D / FOLDER[typ] / (name + '.md')).read_text(encoding='utf-8'); m = re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M)
    q = re.search(r'> \[!info\] Quotes\s*\n((?:>[^\n]*\n?)+)', t); p = re.search(r'> \[!info\] Papers\s*\n((?:>[^\n]*\n?)+)', t)
    return f"Title: {m.group(1) if m else name}\nPapers: {', '.join(sorted(set(re.findall(r'(@[A-Za-z0-9-]+)', p.group(1))))) if p else 'n/a'}\nQuote: {re.sub(r'^> ?', '', q.group(1), flags=re.M).strip()[:700] if q else 'n/a'}"
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--type', action='append', required=True); ap.add_argument('--top', type=int, action='append', required=True)
    ap.add_argument('--run-id', required=True); ap.add_argument('--model', default='claude-sonnet-5-5'); a = ap.parse_args()
    cdir = VAULT / 'pipeline/misc/evd-validation/embedding-candidates'; rows = list(csv.DictReader(open(cdir / 'candidates.tsv'), delimiter='\t'))
    prompt_file = 'pipeline/prompts/merge-judge-v1.md'; tpl = (VAULT / prompt_file).read_text(encoding='utf-8').split('\n', 2)[2]
    jobs = []
    for typ, top in zip(a.type, a.top): jobs += [r for r in rows if r['type'] == typ][:top]
    def one(r):
        text, rec = cl.logged_anthropic(a.run_id, 'merge-judge', a.model, prompt_file, tpl.replace('{A}', body(r['type'], r['node_a'])).replace('{B}', body(r['type'], r['node_b'])), effort='medium', max_tokens=800, node=f"{r['node_a']} || {r['node_b']}")
        m = re.search(r'\{.*\}', text, re.S)
        try: j = json.loads(m.group(0))
        except Exception: j = {'verdict': 'unparsed', 'differences': [], 'reason': text[:120]}
        return {**r, 'verdict': j.get('verdict'), 'differences': '; '.join(j.get('differences', [])), 'reason': j.get('reason', '')}
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(one, jobs))
    with open(cdir / 'judgments.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, list(res[0].keys()), delimiter='\t'); w.writeheader(); w.writerows(res)
    md = ['# Second opinion on candidate pairs (Claude Sonnet 5.5, blinded; Inkling 2 Small not wired up yet)', '', 'Verdicts are advice for the human verifier, not decisions. Nothing was merged.', '']
    for typ in a.type:
        md += [f'## {typ}', '', '| # | A | B | Similarity | Verdict | What differs | Reason |', '|---|---|---|---|---|---|---|']
        for n, r in enumerate([x for x in res if x['type'] == typ], 1): md.append(f"| {n} | {r['node_a'].split(' - ', 1)[-1][:90]} | {r['node_b'].split(' - ', 1)[-1][:90]} | {r['sim_title']} | **{r['verdict']}** | {r['differences'][:120]} | {r['reason']} |")
        md.append('')
    (cdir / 'judgments.md').write_text('\n'.join(md), encoding='utf-8')
    import collections; print(collections.Counter((r['type'], r['verdict']) for r in res))
if __name__ == '__main__': main()

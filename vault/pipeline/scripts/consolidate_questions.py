#!/usr/bin/env python3
"""Group the research questions that papers state into unified questions, and nest them (primary, secondary, tertiary). JP, 2026-11-25.
Nothing merges automatically: the output is a proposal and JP verifies every group in the TSV.
  python3 consolidate_questions.py --runs 2026-11-25_batch01 [RUN ...] [--threshold 0.92] [--dry-run] [--model MODEL]   (default: roles.grouping in pipeline/config/models.json, Gemini 4 Neon at medium effort since 2026-11-27; Claude Sonnet 5.5 before)
Steps: read questions from runs/<run>/<paper>/picost.json; embed the reframed text with EmbeddingGemma 2 (local, venv-embed python);
cluster by average-linkage on cosine similarity; one grouping-model call per multi-member cluster (unified wording, duplicate or related);
one more call over all unified questions for the nesting under the project question. Writes question_groups.json and question_groups.tsv into runs/<first run>/.
Spend: ledger of this script's calls is runs/<first run>/calls.jsonl (call_logger); --cap-usd (default 0.50) stops before a call that could pass it."""
import argparse, csv, json, subprocess, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import call_logger as cl, config as C
VAULT = cl.VAULT; RUNS = cl.RUNS
EMBED_PY = Path.home() / '.cache/lives-bench/venv-embed/bin/python'
EMBED_DIR = Path.home() / '.cache/lives-bench/models/embeddinggemma-2'
ME = str(Path(__file__).resolve())   # logged as the "prompt file": the prompts are inside this script

def collect(runs):
    qs = []
    for run in runs:
        for f in sorted((RUNS / run).glob('*/picost.json')):
            for q in json.load(open(f, encoding='utf-8')).get('questions', []):
                qs.append(dict(run=run, paper=f.parent.name, id=q.get('id'), text=q.get('reframed') or q.get('original_wording', ''),
                               original=q.get('original_wording', ''), section=q.get('section', ''), kind=q.get('kind', ''), pdf_page=q.get('pdf_page')))
    for i, q in enumerate(qs): q['key'] = f'Q{i + 1:03d}'
    return qs

def embed(texts):
    """Cosine similarity matrix from EmbeddingGemma 2, run in the embedding venv when the current python lacks sentence-transformers."""
    code = ("import sys,json\nfrom sentence_transformers import SentenceTransformer\nt=json.load(sys.stdin)\n"
            f"m=SentenceTransformer({str(EMBED_DIR)!r})\ne=m.encode(t,normalize_embeddings=True,batch_size=16)\nprint(json.dumps((e@e.T).tolist()))")
    py = str(EMBED_PY) if EMBED_PY.exists() else sys.executable
    r = subprocess.run([py, '-c', code], input=json.dumps(texts), capture_output=True, text=True)
    if r.returncode: sys.exit('embedding failed: ' + r.stderr[-400:])
    return json.loads(r.stdout.strip().splitlines()[-1])

def cluster(S, threshold):
    """Average-linkage agglomerative: merge the two clusters with the highest mean similarity while it is at or above the threshold."""
    cl_ = [[i] for i in range(len(S))]
    while True:
        best, bi, bj = -1, None, None
        for i in range(len(cl_)):
            for j in range(i + 1, len(cl_)):
                s = sum(S[a][b] for a in cl_[i] for b in cl_[j]) / (len(cl_[i]) * len(cl_[j]))
                if s > best: best, bi, bj = s, i, j
        if best < threshold or bi is None: return cl_
        cl_[bi] += cl_.pop(bj)

def parse(text):
    for i in reversed([k for k, c in enumerate(text) if c == '{']):   # the last complete object wins if the model rambles
        try:
            o = json.JSONDecoder().raw_decode(text[i:])[0]
            if isinstance(o, dict) and ('subgroups' in o or 'nodes' in o): return o
        except ValueError: pass
    raise ValueError('no JSON in reply: ' + text[:200])

RULES = ("Rules: use only the questions given, never invent one. Write for a reader who is not a specialist: everyday words, clear, granular, "
         "name the capability being asked about, not the method or the tool. Subtle differences mean do not merge. No em dashes. Short plain sentences.")

GROUP_EFFORT = C.role_effort(C.ROLES['grouping'], 'medium')


def call(run_id, step, model, prompt, max_tokens):
    """One standard-mode call through the provider of the grouping model (roles.grouping). Thinking tokens count against max_tokens for Gemini, so the budget is larger there."""
    pv = C.provider_of(model)
    if pv == 'google': text, rec = cl.logged_gemini(run_id, step, model, ME, prompt, effort=GROUP_EFFORT, max_tokens=max_tokens * 4)
    elif pv == 'anthropic': text, rec = cl.logged_anthropic(run_id, step, model, ME, prompt, effort=GROUP_EFFORT, max_tokens=max_tokens)
    elif pv == 'openai': text, rec = cl.logged_openai(run_id, step, model, ME, prompt, effort=GROUP_EFFORT)
    else: raise ValueError(f'no route for {model} (provider {pv})')
    return parse(text), rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', nargs='+', required=True); ap.add_argument('--threshold', type=float, default=0.92)
    ap.add_argument('--dry-run', action='store_true', help='show clusters only; no model calls, no spend')
    ap.add_argument('--model', default=C.role_model(C.ROLES['grouping'])); ap.add_argument('--cap-usd', type=float, default=0.50); a = ap.parse_args()
    C.assert_allowed(a.model)
    qs = collect(a.runs)
    if not qs: sys.exit('no questions found')
    S = embed([q['text'] for q in qs]); groups = cluster(S, a.threshold)
    groups.sort(key=lambda g: (-len(g), g[0]))
    print(f'{len(qs)} questions from {len({q["paper"] for q in qs})} papers -> {len(groups)} clusters at threshold {a.threshold}')
    for n, g in enumerate(groups, 1):
        if len(g) > 1:
            print(f'\nG{n} ({len(g)} members)')
            for i in g: print(f'   {qs[i]["key"]} {qs[i]["paper"][:14]}: {qs[i]["text"]}')
    if a.dry_run:
        pairs = sorted(((S[i][j], i, j) for i in range(len(qs)) for j in range(i + 1, len(qs))), reverse=True)[:12]
        print('\nTop pairs:'); [print(f'  {s:.3f} {qs[i]["key"]} / {qs[j]["key"]}') for s, i, j in pairs]; return
    run_id = a.runs[0]; project_q = C.PIPE['project_question']; spent = 0.0
    def guard(est_in, max_out):
        worst = cl.cost_usd(a.model, est_in, max_out * (4 if C.provider_of(a.model) == 'google' else 1)) or 0
        if spent + worst > a.cap_usd: sys.exit(f'stopping: spent ${spent:.3f} + worst case ${worst:.3f} would pass the ${a.cap_usd:.2f} cap')
    out = []   # unified groups
    for n, g in enumerate(groups, 1):
        gid = f'G{n:02d}'; members = [dict(key=qs[i]['key'], paper=qs[i]['paper'], id=qs[i]['id'], wording=qs[i]['text'], original=qs[i]['original'], section=qs[i]['section']) for i in g]
        if len(g) == 1:
            out.append(dict(group=gid, unified=members[0]['wording'], members=members, relation='single', reason='Only one paper or question like this.')); continue
        listing = '\n'.join(f'{m["key"]} ({m["paper"][:20]}, {m["id"]}): {m["wording"]}' for m in members)
        prompt = (f'These research questions came from papers. A machine flagged them as possibly the same question.\n{listing}\n\n{RULES}\n'
                  'Decide whether they are true duplicates (same capability, same thing measured, same kind of subject) or only related. '
                  'If any differ in a subtle way (different task, population, comparison, outcome), split them into separate subgroups instead of merging.\n'
                  'Reply with exactly one JSON object and nothing else: {"subgroups":[{"members":["Q001","Q002"],"unified_question":"...","relation":"duplicate"|"related","reason":"one sentence"}]}. '
                  'Every key above must appear in exactly one subgroup. A subgroup of one member keeps its own wording as unified_question.')
        guard(len(prompt) // 3 + 200, 1500)
        j, rec = call(run_id, 'consolidate-cluster', a.model, prompt, 1500); spent += rec['cost_usd_est'] or 0
        byk = {m['key']: m for m in members}; seen = set()
        for k, sg in enumerate(j['subgroups']):
            ms = [byk[x] for x in sg['members'] if x in byk and x not in seen]; seen.update(m['key'] for m in ms)
            if ms: out.append(dict(group=f'{gid}{"abcdefgh"[k]}' if len(j['subgroups']) > 1 else gid, unified=sg['unified_question'], members=ms, relation=sg.get('relation', 'related') if len(ms) > 1 else 'single', reason=sg.get('reason', '')))
        for m in members:
            if m['key'] not in seen: out.append(dict(group=f'{gid}x{m["key"]}', unified=m['wording'], members=[m], relation='single', reason='Model left this one out; kept on its own.'))
    # second call: nesting
    listing = '\n'.join(f'{g["group"]}: {g["unified"]}  [{len(g["members"])} member(s), {len({m["paper"] for m in g["members"]})} paper(s)]' for g in out)
    prompt = (f'Overarching project question:\n{project_q}\n\nUnified research questions:\n{listing}\n\n{RULES}\n'
              'Arrange these questions into a nested hierarchy. A primary question is broad and sits directly under the project question. A secondary question is a narrower part of one primary question. '
              'A tertiary question is a narrower part of one secondary question. Use only the groups listed, with their ids; do not invent new questions or new groups. '
              'Every group needs a level and, unless primary, a parent id one level up. If a question fits no other, make it primary. '
              'Do not force a parent where the link is weak: separate siblings are better than a stretched parent. '
              f'Give one sentence on why it sits there, and one sentence on how it fits under the project question.\n'
              'Reply with exactly one JSON object and nothing else: {"nodes":[{"group":"G01","level":"primary"|"secondary"|"tertiary","parent":null|"G02","reason":"...","fit_under_project_question":"..."}]}')
    guard(len(prompt) // 3 + 200, 6000)
    j, rec = call(run_id, 'consolidate-nesting', a.model, prompt, 6000); spent += rec['cost_usd_est'] or 0
    nest = {n['group']: n for n in j['nodes']}; by = {g['group']: g for g in out}
    def depth(gid, seen=()):
        p = nest.get(gid, {}).get('parent')
        return 0 if not p or p not in by or gid in seen else 1 + depth(p, seen + (gid,))
    for g in out:
        n = nest.get(g['group'], {}); d = depth(g['group']); p = n.get('parent') if d else None
        g.update(level=['primary', 'secondary', 'tertiary'][min(d, 2)], parent=p, nest_reason=n.get('reason', 'Model gave no placement; treated as primary.'), fit=n.get('fit_under_project_question', ''))
        if d > 2: g['nest_reason'] += ' (Nested deeper than tertiary; shown as tertiary, check.)'
    lv = {'primary': 0, 'secondary': 1, 'tertiary': 2}
    out.sort(key=lambda g: (g['group'] if g['level'] == 'primary' else ''))
    def order(parent=None, acc=None):
        acc = [] if acc is None else acc
        for g in sorted(out, key=lambda x: x['group']):
            if g['parent'] == parent: acc.append(g); order(g['group'], acc)
        return acc
    ordered = order(None)
    ordered += [g for g in out if g not in ordered]
    d = RUNS / run_id
    (d / 'question_groups.json').write_text(json.dumps(dict(runs=a.runs, project_question=project_q, model=a.model, threshold=a.threshold, spent_usd=round(spent, 4), groups=ordered), indent=2, ensure_ascii=False), encoding='utf-8')
    with open(d / 'question_groups.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['group id', 'level', 'parent group id', 'unified question', 'member paper', 'member id', 'member wording', 'duplicate or related', 'reason', 'JP: group right? (yes/no)', 'JP: better wording or notes'])
        for g in ordered:
            for m in g['members']: w.writerow([g['group'], g['level'], g['parent'] or '', g['unified'], m['paper'], m['id'], m['wording'], g['relation'], g['reason'] + ' Placement: ' + g['nest_reason'], '', ''])
    print(f'\n{len(qs)} questions -> {len(ordered)} unified questions; levels: ' + ', '.join(f'{k} {sum(g["level"] == k for g in ordered)}' for k in lv) + f'; cost ${spent:.3f}')
    for g in ordered: print('  ' * lv[g['level']] + f'{g["group"]} [{g["level"]}, {g["relation"]}, {len(g["members"])}] {g["unified"]}')
    print('wrote', d / 'question_groups.json', 'and .tsv')

if __name__ == '__main__': main()

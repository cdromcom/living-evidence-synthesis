#!/usr/bin/env python3
"""Candidate duplicate nodes with EmbeddingGemma 2 (local). Run with the embedding environment:
  ~/.cache/lives-bench/venv-embed/bin/python embed_candidates.py [--top 30] [--outdir DIR]
For each node type (QUE, CLM, CVT, EP, EVD) it embeds the title and, separately, the title plus the node's first quote, then lists same-type pairs by similarity.
Nothing is merged. Each pair carries "difference hints" (numbers, model names, negations that differ) because near-duplicates that differ in one detail must NOT be merged.
JP, 2026-11-25: subtle differences mean do not merge; a human verifies every merge in addition to the two model judges."""
import argparse, itertools, os, re, sys
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis')
D = VAULT / 'sysrev' / 'dgraph'; MODEL = Path.home() / '.cache/lives-bench/models/embeddinggemma-2'
TYPES = {'QUE': 'questions', 'CLM': 'claims', 'CVT': 'caveats', 'EP': 'evd-patterns', 'EVD': 'evidence'}
def read(p):
    t = p.read_text(encoding='utf-8'); m = re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M); title = m.group(1) if m else p.stem.split(' - ', 1)[-1]
    papers = sorted(set(re.findall(r'\[\[(?:[^\]|]*/)?(@[^\]|#]+)', (re.search(r'> \[!info\] Papers\s*\n((?:>[^\n]*\n?)+)', t) or [None, ''])[1])))
    q = re.search(r'> \[!info\] Quotes\s*\n>\s*"?(.{20,400}?)"?\s*(?:\n|$)', t)
    return dict(path=str(p.relative_to(VAULT)), name=p.stem, title=title, papers=papers, quote=q.group(1) if q else '')
NEG = re.compile(r'\b(not|no|never|only|without|cannot|fail\w*|lack\w*|unable)\b', re.I)
def hints(a, b):
    na, nb = set(re.findall(r'\d+(?:\.\d+)?%?', a)), set(re.findall(r'\d+(?:\.\d+)?%?', b))
    ma, mb = set(re.findall(r'\b(?:GPT-?[\w.-]+|Claude[\w. -]*?\d|Llama[\w.-]*|Gemini[\w.-]*|o\d(?:-mini)?|ChatGPT|PaLM|Mistral|Qwen[\w.-]*|ICLR|NeurIPS|CONSORT|PRISMA|STROBE|QUADAS-?2|AMSTAR)\b', a)), set(re.findall(r'\b(?:GPT-?[\w.-]+|Claude[\w. -]*?\d|Llama[\w.-]*|Gemini[\w.-]*|o\d(?:-mini)?|ChatGPT|PaLM|Mistral|Qwen[\w.-]*|ICLR|NeurIPS|CONSORT|PRISMA|STROBE|QUADAS-?2|AMSTAR)\b', b))
    h = []
    if na ^ nb: h.append('numbers differ: ' + ', '.join(sorted(na ^ nb))[:60])
    if ma ^ mb: h.append('names differ: ' + ', '.join(sorted(ma ^ mb))[:70])
    if bool(NEG.findall(a)) != bool(NEG.findall(b)) or {x.lower() for x in NEG.findall(a)} ^ {x.lower() for x in NEG.findall(b)}: h.append('negation or "only" differs')
    return '; '.join(h) or 'none found'
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--top', type=int, default=30); ap.add_argument('--outdir', default=str(VAULT / 'pipeline/misc/evd-validation/embedding-candidates')); a = ap.parse_args()
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(str(MODEL)); out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    md = ['# Candidate duplicate nodes (EmbeddingGemma 2, local test on the 27-paper set)', '', 'Similarity is cosine similarity of the title (A) and of title plus first quote (B). **Nothing has been merged.** A high score means "worth a look", not "same". Read the difference hints first. Rule (JP, 2026-11-25): if the nodes differ in a subtle way, do not merge; a human verifies every merge.', '']
    tsv = ['type\tsim_title\tsim_title_quote\tcross_paper\tnode_a\tnode_b\tpapers_a\tpapers_b\thints']; stats = []
    for typ, folder in TYPES.items():
        nodes = [read(p) for p in sorted((D / folder).glob('*.md'))]
        if len(nodes) < 2: continue
        ea = m.encode([n['title'] for n in nodes], normalize_embeddings=True, batch_size=16)
        eb = m.encode([n['title'] + '. ' + n['quote'] for n in nodes], normalize_embeddings=True, batch_size=16)
        Sa, Sb = ea @ ea.T, eb @ eb.T
        pairs = sorted(((float(Sa[i, j]), float(Sb[i, j]), i, j) for i, j in itertools.combinations(range(len(nodes)), 2)), reverse=True)
        n90, n85, n80 = (sum(1 for p in pairs if p[0] >= t) for t in (0.90, 0.85, 0.80)); stats.append((typ, len(nodes), n90, n85, n80))
        md += [f'## {typ}: {len(nodes)} nodes; pairs at or above 0.90: {n90}, 0.85: {n85}, 0.80: {n80}', '', '| # | A | B | A sim | B sim | Same paper? | Difference hints |', '|---|---|---|---|---|---|---|']
        for r, (sa, sb, i, j) in enumerate(pairs[:a.top], 1):
            x, y = nodes[i], nodes[j]; cross = 'no' if set(x['papers']) & set(y['papers']) else 'yes (different papers)'
            md.append(f"| {r} | {x['title'][:110]} | {y['title'][:110]} | {sa:.3f} | {sb:.3f} | {cross} | {hints(x['title'], y['title'])} |")
            tsv.append('\t'.join([typ, f'{sa:.3f}', f'{sb:.3f}', cross, x['name'], y['name'], ','.join(x['papers']), ','.join(y['papers']), hints(x['title'], y['title'])]))
        md.append('')
    md.insert(3, '| Type | Nodes | pairs >= 0.90 | >= 0.85 | >= 0.80 |\n|---|---|---|---|---|\n' + '\n'.join(f'| {t} | {n} | {a} | {b} | {c} |' for t, n, a, b, c in stats) + '\n')
    (out / 'candidates.md').write_text('\n'.join(md), encoding='utf-8'); (out / 'candidates.tsv').write_text('\n'.join(tsv), encoding='utf-8')
    print('\n'.join(f'{t}: {n} nodes, pairs >=0.90: {a}, >=0.85: {b}, >=0.80: {c}' for t, n, a, b, c in stats)); print('wrote', out)
if __name__ == '__main__': main()

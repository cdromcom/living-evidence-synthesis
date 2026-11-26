#!/usr/bin/env python3
"""Compare local embedding models on LIVES data (JP, 2026-11-25). Run with the embedding environment:
  ~/.cache/lives-bench/venv-embed/bin/python compare_embedders.py [--models gemma harrier dna] [--max-pairs 200]
Tests
  1 TITLES   similarity spread of node titles per type, and the rank of JP's one labeled merge pair (the two LLM-versus-human review questions)
  2 SCREENSHOTS   quote text <-> screenshot of that quote: for each pair, is the right image the nearest to the text, and the right text the nearest to the image (R@1, R@5, MRR)
Models that cannot embed images are skipped for test 2. Writes pipeline/misc/evd-validation/embedder-comparison/<date>.md"""
import argparse, csv, itertools, os, random, re, time
from datetime import date
from pathlib import Path
import numpy as np
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis'); D = VAULT / 'sysrev/dgraph'; M = Path.home() / '.cache/lives-bench/models'
MODELS = {'gemma': ('EmbeddingGemma 2 (740M)', M / 'embeddinggemma-2', None, True), 'harrier': ('harrier-oss-v1-0.6b (596M)', M / 'harrier-oss-v1-0.6b', 'sts_query', False),
          'dna': ('DNA-VL-STEER-2B (2.1B)', M / 'DNA-VL-STEER-2B', None, True)}   # last field: can the model embed images? (a text-only model must not be handed file paths: it embeds the path as text and scores at chance)
TYPES = {'QUE': 'questions', 'CLM': 'claims', 'CVT': 'caveats', 'EVD': 'evidence'}
def title(p):
    t = p.read_text(encoding='utf-8'); m = re.search(r'^title:\s*"?(.+?)"?\s*$', t, re.M); return m.group(1) if m else p.stem
def merge_pair():
    f = VAULT / 'pipeline/misc/evd-validation/embedding-candidates/judgments.tsv'
    r = [x for x in csv.DictReader(open(f), delimiter='\t') if x['inkling_verdict'] == 'merge']; return (r[0]['node_a'], r[0]['node_b']) if r else None
def pairs(max_pairs):
    rx = re.compile(r'> "(.{40,700}?)"[^\n]*\n> !\[\[([^\]|]+\.png)\]\]'); seen = set(); out = []
    pngs = {p.name: p for p in D.rglob('*.png')}
    for kind in TYPES.values():
        for f in sorted((D / kind).glob('*.md')):
            for m in rx.finditer(f.read_text(encoding='utf-8')):
                img = pngs.get(m.group(2))
                if img and img.name not in seen and '-evd-' in img.name or (img and img.name not in seen and re.search(r'-(que|clm|cvt)-', img.name)):
                    if img.name in seen: continue
                    seen.add(img.name); out.append((re.sub(r'\s+', ' ', m.group(1)).strip(), str(img)))
    random.Random(0).shuffle(out); return out[:max_pairs]
def retrieval(S):   # S[i, j] = similarity of text i and image j; right answer is the diagonal
    ranks = [int((S[i] > S[i, i]).sum()) + 1 for i in range(len(S))]; return {'R@1': np.mean([r == 1 for r in ranks]), 'R@5': np.mean([r <= 5 for r in ranks]), 'MRR': np.mean([1 / r for r in ranks])}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--models', nargs='+', default=list(MODELS)); ap.add_argument('--max-pairs', type=int, default=200); a = ap.parse_args()
    from sentence_transformers import SentenceTransformer
    nodes = {t: [(f.stem, title(f)) for f in sorted((D / k).glob('*.md'))] for t, k in TYPES.items()}; mp = merge_pair(); P = pairs(a.max_pairs)
    md = [f'# Embedding model comparison ({date.today()})', '', 'Local models, same data. Test 1 uses node titles; test 2 uses %d quote texts with the screenshot of each quote.' % len(P), '']
    res = {}
    for key in a.models:
        name, path, pn, has_images = MODELS[key]; m = SentenceTransformer(str(path)); r = {'name': name}
        enc = lambda x, **k: m.encode(x, normalize_embeddings=True, prompt_name=pn, **k) if pn else m.encode(x, normalize_embeddings=True, **k)
        for t, items in nodes.items():
            e = enc([x[1] for x in items]); S = e @ e.T; iu = np.triu_indices(len(items), 1); v = S[iu]
            r[t] = (len(items), float(v.mean()), float(np.percentile(v, 95) - np.percentile(v, 50)))
            if t == 'QUE' and mp:
                names = [x[0] for x in items]; i, j = sorted((names.index(mp[0]), names.index(mp[1]))); order = np.argsort(-v); idx = np.where((iu[0] == i) & (iu[1] == j))[0][0]
                r['merge'] = (float(S[i, j]), int(np.where(order == idx)[0][0]) + 1, len(v))
        if not has_images: r['img'] = 'text-only model, not tested'; res[key] = r; del m; continue
        try:
            t0 = time.time(); te = enc([p[0] for p in P], batch_size=16); ie = enc([p[1] for p in P], batch_size=8); S = te @ ie.T
            r['img'] = {'text->image': retrieval(S), 'image->text': retrieval(S.T), 'seconds': time.time() - t0}
        except Exception as ex: r['img'] = f'not supported: {type(ex).__name__}: {str(ex)[:120]}'
        res[key] = r; del m
    md += ['## 1. Titles: spread of similarity scores and JP\'s merge pair', '', '| Model | ' + ' | '.join(f'{t} (n)' for t in TYPES) + ' | Merge pair: sim, rank |', '|---|' + '---|' * (len(TYPES) + 1)]
    for r in res.values(): md.append(f"| {r['name']} | " + ' | '.join(f"spread {r[t][2]:.3f}, mean {r[t][1]:.3f} ({r[t][0]})" for t in TYPES) + f" | {r['merge'][0]:.3f}, rank {r['merge'][1]} of {r['merge'][2]} |" if 'merge' in r else ' | n/a |')
    md += ['', 'Spread = 95th minus 50th percentile of pairwise similarity (a wider spread separates close pairs from the pack better).', '', '## 2. Quote text and its screenshot', '', '| Model | text to image R@1 | R@5 | MRR | image to text R@1 | R@5 | MRR |', '|---|---|---|---|---|---|---|']
    for r in res.values():
        if isinstance(r['img'], dict): x, y = r['img']['text->image'], r['img']['image->text']; md.append(f"| {r['name']} | {x['R@1']:.2f} | {x['R@5']:.2f} | {x['MRR']:.2f} | {y['R@1']:.2f} | {y['R@5']:.2f} | {y['MRR']:.2f} |")
        else: md.append(f"| {r['name']} | {r['img']} | | | | | |")
    out = VAULT / 'pipeline/misc/evd-validation/embedder-comparison'; out.mkdir(parents=True, exist_ok=True); (out / f'{date.today()}.md').write_text('\n'.join(md) + '\n', encoding='utf-8'); print('\n'.join(md))
if __name__ == '__main__': main()

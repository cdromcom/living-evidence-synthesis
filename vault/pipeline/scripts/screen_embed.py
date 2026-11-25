#!/usr/bin/env python3
"""Sort newly ingested papers into task-type categories by embedding similarity to the seed set, with a majority vote over three embedding models (JP, 2026-11-25).
Run with the embedding environment:  ~/.cache/lives-bench/venv-embed/bin/python screen_embed.py --dedup ~/.cache/lives-bench/screening/dedup.json
Method
  1 text      first 3 PDF pages (superscripts removed), at most 6,000 characters, after the title; the Zotero abstract is used if the PDF has little text
  2 embed     EmbeddingGemma 2, harrier-oss-v1-0.6b, DNA-VL-STEER-2B (open weights, local; allowed by the 2026-11-25 origin policy, see Tools-and-Models.md), each on its own
  3 vote      each model gives a paper the task group of its most similar seed paper(s); 'NEW' if even the nearest seed is less similar than the model's own 15th percentile of seed-to-seed similarity
  4 majority  2 of 3 models agree -> that category; otherwise 'no majority' (a person decides). Leave-one-out on the seeds reports how often each model is right.
  5 new categories papers voted NEW or with no majority are clustered together (average linkage on the mean of the three models' distances) and named from their most distinctive words
Nothing is deleted or moved; the output is a JSON for the review sheet."""
import argparse, collections, json, os, re, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import pdf_pages as pp
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis'); M = Path.home() / '.cache/lives-bench/models'
MODELS = [('EmbeddingGemma 2', M / 'embeddinggemma-2', None), ('harrier-oss-v1-0.6b', M / 'harrier-oss-v1-0.6b', 'sts_query'), ('DNA-VL-STEER-2B', M / 'DNA-VL-STEER-2B', None)]
def pdf_text(path, chars=6000, pages=3):
    import fitz
    try: doc = fitz.open(path); t = ' '.join(pp.page_text(doc[i]) for i in range(min(pages, len(doc))))
    except Exception: return ''
    t = re.sub(r'-\s*\n\s*', '', t); t = re.sub(r'\s+', ' ', t).strip(); return t[:chars]
def pdf_abstract(path, chars=1800):
    """The abstract section of a PDF (text after the word Abstract on the first two pages), else the start of page 1 after the title block."""
    t = pdf_text(path, chars=9000, pages=2); m = re.search(r'\babstract\b[:.\s\-\u2014]*', t, re.I)
    return (t[m.end():] if m else t[300:])[:chars]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dedup', required=True); ap.add_argument('--out'); ap.add_argument('--novel-pct', type=float, default=15)
    ap.add_argument('--text-mode', choices=['pdf', 'abstract'], default='pdf', help="pdf: title + first 3 PDF pages (needs a PDF). abstract: title + abstract (Zotero abstract; for seed papers the abstract section of the PDF), for sets where most papers have no PDF"); a = ap.parse_args()
    seeds = json.load(open(VAULT / 'pipeline/screening/shared/seed-papers_task-groups.json')); R = json.load(open(a.dedup))
    # --- documents: seeds first, then one record per duplicate group (the preferred one that has a PDF on disk)
    docs = []
    for ck, s in seeds.items():
        title = (s['pdf'] or ck).split(' - ', 2)[-1].rsplit('.pdf', 1)[0]; path = VAULT / 'sysrev/dgraph/source/pdfs' / s['pdf']
        docs.append({'kind': 'seed', 'id': ck, 'title': title, 'groups': s['groups'], 'text': (pdf_abstract(path) if a.text_mode == 'abstract' else pdf_text(path)), 'pdf': s['pdf']})
    byg = collections.defaultdict(list)
    for r in R: byg[r['dup_group'] or r['key']].append(r)
    for g, rs in byg.items():
        if a.text_mode == 'abstract':
            keep = max(rs, key=lambda r: ('keep' in r['dup_role'], len(r['abstract']), r['source'] == 'personal library'))
            t = keep['abstract'][:1800] or (pdf_abstract(keep['pdfs'][0]['path']) if keep['pdfs'] else '')
        else:
            cand = [r for r in rs if r['pdfs'] and r['source'] == 'personal library'] or [r for r in rs if r['pdfs']] or rs
            keep = max(cand, key=lambda r: ('keep' in r['dup_role'], bool(r['pdfs']), r['source'] == 'personal library'))
            t = pdf_text(keep['pdfs'][0]['path']) if keep['pdfs'] else ''
            if len(t) < 500 and keep['abstract']: t = keep['abstract']
        docs.append({'kind': 'new', 'id': keep['key'], 'group': g, 'title': keep['title'], 'text': t, 'rec': keep, 'copies': len(rs), 'pdf': Path(keep['pdfs'][0]['path']).name if keep['pdfs'] else '', 'text_mode': a.text_mode})
    inputs = [f"{d['title']}. {d['text']}" for d in docs]
    seed_idx = [i for i, d in enumerate(docs) if d['kind'] == 'seed']; new_idx = [i for i, d in enumerate(docs) if d['kind'] == 'new']
    cats = sorted({g for d in docs if d['kind'] == 'seed' for g in d['groups']})
    from sentence_transformers import SentenceTransformer
    sims = {}; embs = {}
    for name, path, pn in MODELS:
        import hashlib, time; cache = Path.home() / '.cache/lives-bench/screening/emb-cache'; cache.mkdir(parents=True, exist_ok=True)
        ck = cache / (hashlib.sha1((name + '\x00'.join(inputs)).encode()).hexdigest()[:16] + '.npy')   # reuse embeddings of the same texts and model (a rerun costs nothing)
        if ck.exists(): e = np.load(ck); print('loaded cached embeddings for', name, flush=True)
        else:
            m = SentenceTransformer(str(path)); m.max_seq_length = 1024; parts = []; t0 = time.time()
            for i in range(0, len(inputs), 24):   # chunks with progress, so a stall is visible
                chunk = inputs[i:i + 24]
                parts.append(m.encode(chunk, normalize_embeddings=True, batch_size=4, prompt_name=pn) if pn else m.encode(chunk, normalize_embeddings=True, batch_size=4))
                print(f'  {name}: {min(i + 24, len(inputs))}/{len(inputs)} texts, {time.time() - t0:.0f}s', flush=True)
                try:
                    import torch; torch.mps.empty_cache()
                except Exception: pass
            e = np.concatenate(parts); np.save(ck, e); del m
        embs[name] = e; sims[name] = e @ e.T; print('embedded with', name, flush=True)
    # --- per model: seed-to-seed leave-one-out, then vote for each new paper
    def cat_scores(S, i, exclude=None):   # nearest seed similarity per category (and which seed)
        out = {}
        for c in cats:
            best = (-1, None)
            for j in seed_idx:
                if j == exclude or j == i or c not in docs[j]['groups']: continue
                if S[i, j] > best[0]: best = (float(S[i, j]), j)
            out[c] = best
        return out
    report = {}; votes = {d['id']: {} for d in docs if d['kind'] == 'new'}; loo = {}
    for name, S in sims.items():
        loo_sims = []; ok = tot = 0
        for i in seed_idx:
            sc = cat_scores(S, i); sc = {c: v for c, v in sc.items() if v[1] is not None}
            if not sc: continue
            top = max(sc, key=lambda c: sc[c][0]); loo_sims.append(sc[top][0])
            if all(len([x for x in seed_idx if c in docs[x]['groups'] and x != i]) > 0 for c in docs[i]['groups']): tot += 1; ok += top in docs[i]['groups']
        tau = float(np.percentile(loo_sims, a.novel_pct)); report[name] = {'loo_accuracy': ok / max(tot, 1), 'loo_n': tot, 'novel_threshold': tau, 'loo_median_nearest_sim': float(np.median(loo_sims))}
        for i in new_idx:
            sc = cat_scores(S, i); ranked = sorted(sc.items(), key=lambda kv: -kv[1][0]); top_c, (top_s, top_j) = ranked[0]
            votes[docs[i]['id']][name] = {'pick': 'NEW' if top_s < tau else top_c, 'best_group': top_c, 'sim': top_s, 'second': ranked[1][0], 'second_sim': ranked[1][1][0], 'nearest_seed': docs[top_j]['pdf'], 'novel': top_s < tau}
    # --- majority
    for d in docs:
        if d['kind'] != 'new': continue
        v = votes[d['id']]; cnt = collections.Counter(x['pick'] for x in v.values()); top, n = cnt.most_common(1)[0]
        d['votes'] = v; d['majority'] = top if n >= 2 else 'no majority'; d['agreement'] = f'{n} of 3'
        # tie-break hint: which group do the models lean to if they are split?
        d['mean_best_sim'] = float(np.mean([x['sim'] for x in v.values()]))
    # --- new categories: cluster papers that are NEW or split
    pool = [i for i in new_idx if docs[i]['majority'] in ('NEW', 'no majority')]
    clusters = {}
    if len(pool) >= 3:
        from sklearn.cluster import AgglomerativeClustering; from sklearn.metrics import silhouette_score; from sklearn.feature_extraction.text import TfidfVectorizer
        D = np.mean([1 - S[np.ix_(pool, pool)] for S in sims.values()], axis=0); np.fill_diagonal(D, 0); best = (None, -2)
        for t in np.linspace(float(np.percentile(D[D > 0], 5)), float(np.percentile(D[D > 0], 60)), 14):
            lab = AgglomerativeClustering(n_clusters=None, metric='precomputed', linkage='average', distance_threshold=t).fit_predict(D)
            if 2 <= len(set(lab)) < len(pool): sc = silhouette_score(D, lab, metric='precomputed')
            else: continue
            if sc > best[1]: best = (lab, sc, t)
        lab = best[0] if best[0] is not None else np.arange(len(pool))
        tf = TfidfVectorizer(stop_words='english', max_features=4000, ngram_range=(1, 2), min_df=1); X = tf.fit_transform([f"{docs[i]['title']} {docs[i]['text'][:3000]}" for i in new_idx]); terms = np.array(tf.get_feature_names_out())
        pos = {i: k for k, i in enumerate(new_idx)}
        for c in sorted(set(lab)):
            mem = [pool[k] for k in range(len(pool)) if lab[k] == c]
            if len(mem) < 2: continue
            w = np.asarray(X[[pos[i] for i in mem]].mean(axis=0)).ravel(); top_terms = [terms[j] for j in np.argsort(-w)[:5]]
            clusters[f'N{len(clusters) + 1}'] = {'members': [docs[i]['id'] for i in mem], 'terms': top_terms, 'mean_sim_within': float(np.mean([1 - D[np.ix_([pool.index(i) for i in mem], [pool.index(i) for i in mem])]][0]))}
        report['cluster_choice'] = {'silhouette': float(best[1]) if best[0] is not None else None, 'distance_threshold': float(best[2]) if best[0] is not None else None, 'pool': len(pool)}
    for cid, c in clusters.items():
        for pid in c['members']: next(d for d in docs if d['id'] == pid)['new_pile'] = cid
    out = {'categories': cats, 'report': report, 'clusters': clusters, 'seeds': [{k: d[k] for k in ('id', 'title', 'groups', 'pdf')} for d in docs if d['kind'] == 'seed'],
           'papers': [{'id': d['id'], 'title': d['title'], 'pdf': d['pdf'], 'copies': d['copies'], 'majority': d['majority'], 'agreement': d['agreement'], 'votes': d['votes'], 'mean_best_sim': d['mean_best_sim'], 'new_pile': d.get('new_pile', ''), 'text_chars': len(d['text']), 'text_mode': d.get('text_mode', 'pdf'), 'rec': d['rec']} for d in docs if d['kind'] == 'new']}
    Path(a.out or Path(a.dedup).parent / 'screen-result.json').write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float), encoding='utf-8')
    print(json.dumps(report, indent=1, default=float)); print('majority:', collections.Counter(p['majority'] for p in out['papers'])); print('agreement:', collections.Counter(p['agreement'] for p in out['papers'])); print('new categories:', {k: (len(v['members']), v['terms'][:3]) for k, v in clusters.items()})
if __name__ == '__main__': main()

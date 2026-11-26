#!/usr/bin/env python3
"""Screen the whole Zotero library against the seed papers with three local embedding models (JP, 2026-11-25). Stages (each resumes):
  prepare   de-duplicate every item (DOI, arXiv id, normalized title; version-like titles inside a block), choose the text to embed, record whether a PDF / HTML snapshot is on disk
  embed     embed the texts and the seed papers with each model; every text is cached by hash, so a rerun only does what is missing
  analyze   relevance to the seed and Include set, task-type categories (majority of 3 models), new categories, proxy-label accuracy, outputs for the sheet
Run with the embedding environment:  ~/.cache/lives-bench/venv-embed/bin/python screen_all.py prepare|embed|analyze
Text rule (JP: use metadata and html when there is no PDF): title + Zotero abstract; else the abstract section of a PDF on disk; else the text of an HTML snapshot; else the title alone. At most 1,800 characters.
Working files are in ~/.cache/lives-bench/screening/all/ (they hold abstracts and local paths; not for the vault)."""
import argparse, collections, difflib, hashlib, json, os, re, sys, time
from html.parser import HTMLParser
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import pdf_pages as pp
VAULT = Path(os.environ.get('LIVES_VAULT') or Path.home() / 'Documents/living-synthesis'); C = Path.home() / '.cache/lives-bench/screening'; W = C / 'all'; W.mkdir(parents=True, exist_ok=True)
M = Path.home() / '.cache/lives-bench/models'
MODELS = [('EmbeddingGemma 2', 'embeddinggemma-2', None, 'float32', 32), ('harrier-oss-v1-0.6b', 'harrier-oss-v1-0.6b', 'sts_query', 'float32', 32), ('DNA-VL-STEER-2B', 'DNA-VL-STEER-2B', None, 'float16', 16)]
def norm(t): return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()
PRE = re.compile(r'arxiv|biorxiv|medrxiv|preprint|ssrn|openreview|research square|techrxiv', re.I)
class _P(HTMLParser):
    def __init__(s): super().__init__(); s.skip = 0; s.out = []
    def handle_starttag(s, t, a):
        if t in ('script', 'style', 'nav', 'header', 'footer', 'noscript'): s.skip += 1
    def handle_endtag(s, t):
        if t in ('script', 'style', 'nav', 'header', 'footer', 'noscript') and s.skip: s.skip -= 1
    def handle_data(s, d):
        if not s.skip and len(d.strip()) >= 60: s.out.append(d.strip())
def html_text(path, chars=1800):
    try: raw = open(path, encoding='utf-8', errors='ignore').read(400000)
    except Exception: return ''
    p = _P()
    try: p.feed(raw)
    except Exception: pass
    return re.sub(r'\s+', ' ', ' '.join(p.out))[:chars]
def pdf_abstract(path, chars=1800):
    import fitz
    try: doc = fitz.open(path); t = ' '.join(pp.page_text(doc[i]) for i in range(min(2, len(doc))))
    except Exception: return ''
    t = re.sub(r'-\s*\n\s*', '', t); t = re.sub(r'\s+', ' ', t).strip(); m = re.search(r'\babstract\b[:.\s\-—]*', t, re.I)
    return (t[m.end():] if m else t[300:])[:chars]
def rank(r):
    pre = bool(PRE.search(r['publication'] or '') or r['type'] == 'preprint' or (r['arxiv'] and not (r['doi'] and not r['doi'].startswith('10.48550'))))
    return (0 if pre else 1, r['year'] or '0', 1 if r['pdfs'] else 0, 1 if r['library'] == 'personal' else 0, r['added'])
def group(R, same_lib=False):
    parent = list(range(len(R)))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    blocks = collections.defaultdict(list)
    for i, r in enumerate(R):
        r['nt'] = norm(r['title'])
        if r['doi']: blocks[('d', r['doi'], r['library'] if same_lib else '')].append(i)
        if r['arxiv']: blocks[('a', r['arxiv'], r['library'] if same_lib else '')].append(i)
        if len(r['nt']) >= 12: blocks[('t', r['nt'], r['library'] if same_lib else '')].append(i); blocks[('p', r['nt'][:28], r['library'] if same_lib else '')].append(i)
    for (kind, _, _), ids in blocks.items():
        if len(ids) < 2: continue
        if kind == 'p':   # a shared 28-character prefix: only a very similar full title counts (a preprint and its journal version)
            base = ids[0]
            for j in ids[1:]:
                x, y = R[base]['nt'], R[j]['nt']
                if abs(len(x) - len(y)) < 25 and difflib.SequenceMatcher(None, x, y).ratio() >= 0.90: parent[find(j)] = find(base)
        else:
            for j in ids[1:]: parent[find(j)] = find(ids[0])
    g = collections.defaultdict(list)
    for i in range(len(R)): g[find(i)].append(i)
    return list(g.values())
SEG = lambda p: p.split(' / ')   # a folder path is "Library folder / subfolder / ..."
SETS = [('Elicit set', lambda p: any(x.startswith(('SysRev - Elicit', 'Elicit', 'elicit-results')) for x in SEG(p))),
        ('SysRev-LLMApp pool', lambda p: p.startswith('SysRev-LLMApp') and not any(x.startswith('SysRev - Elicit') or x == 'Include-CA-Rep' for x in SEG(p))),
        ('Include-CA-Rep', lambda p: 'Include-CA-Rep' in SEG(p)), ('Metascience', lambda p: p.startswith('Metascience'))]
def prepare():
    R = [json.loads(l) for l in open(C / 'zotero-all.jsonl')]; t0 = time.time()
    for r in R: r['title'] = r['title'] or ''
    G = group(R); GL = group(R, same_lib=True); print(f'{len(R)} items -> {len(G)} distinct papers ({time.time() - t0:.0f}s)', flush=True)
    lib_stats = {}
    for lib in sorted({r['library'] for r in R}):
        n = sum(1 for r in R if r['library'] == lib); d = sum(1 for g in GL if R[g[0]]['library'] == lib); lib_stats[lib] = {'records': n, 'distinct_within_library': d}
    docs = []; t1 = time.time()
    for k, g in enumerate(G):
        mem = [R[i] for i in g]; best = max(mem, key=rank); colls = sorted({c for m in mem for c in m['collections']}); flags = [n for n, f in SETS if any(f(c) for c in colls)]
        abstract = max((m['abstract'] for m in mem), key=len); pdfs = [p for m in mem for p in m['pdfs']]; htmls = [h for m in mem for h in m['html']]
        title = best['title'] or max((m['title'] for m in mem), key=len)
        if abstract: text, src = abstract[:1800], 'abstract (Zotero)'
        else:
            text = pdf_abstract(pdfs[0]) if pdfs else ''; src = 'PDF (abstract section)' if text else ''
            if not text and htmls: text = html_text(htmls[0]); src = 'HTML snapshot' if text else ''
            if not text: src = 'title only'
        docs.append({'id': f'D{k:05d}', 'kind': 'paper', 'title': title, 'text': text, 'text_source': src, 'year': best['year'], 'doi': best['doi'], 'url': best['url'], 'authors': best['creators'][:3] + (['et al.'] if len(best['creators']) > 3 else []),
                     'publication': best['publication'], 'keys': [f"{m['library']}:{m['key']}" for m in mem], 'libraries': sorted({m['library'] for m in mem}), 'collections': colls, 'sets': flags, 'copies': len(mem),
                     'pdf_on_disk': bool(pdfs), 'html_on_disk': bool(htmls), 'type': best['type'], 'added': min(m['added'] for m in mem)})
        if k % 1000 == 0: print(f'  texts {k}/{len(G)} ({time.time() - t1:.0f}s)', flush=True)
    seeds = json.load(open(VAULT / 'pipeline/screening/shared/seed-papers_task-groups.json'))
    for ck, s in seeds.items():
        path = VAULT / 'sysrev/dgraph/source/pdfs' / s['pdf']; title = s['pdf'].split(' - ', 2)[-1].rsplit('.pdf', 1)[0]
        docs.append({'id': ck, 'kind': 'seed', 'title': title, 'text': pdf_abstract(path), 'text_source': 'PDF (abstract section)', 'groups': s['groups'], 'pdf': s['pdf']})
    with open(W / 'docs.jsonl', 'w', encoding='utf-8') as f:
        for d in docs: f.write(json.dumps(d, ensure_ascii=False) + '\n')
    json.dump({'items': len(R), 'distinct': len(G), 'by_library': lib_stats, 'text_sources': collections.Counter(d['text_source'] for d in docs if d['kind'] == 'paper'), 'prepare_seconds': time.time() - t0}, open(W / 'prepare-stats.json', 'w'), indent=1)
    print(json.dumps({'text_sources': collections.Counter(d['text_source'] for d in docs if d['kind'] == 'paper'), 'sets': collections.Counter(s for d in docs if d['kind'] == 'paper' for s in d['sets']), 'with PDF on disk': sum(d['pdf_on_disk'] for d in docs if d['kind'] == 'paper')}, indent=1))
def embed():
    from sentence_transformers import SentenceTransformer
    import torch
    docs = [json.loads(l) for l in open(W / 'docs.jsonl')]; texts = [f"{d['title']}. {d['text']}"[:2000] for d in docs]; hs = [hashlib.sha1(t.encode()).hexdigest()[:20] for t in texts]
    for name, folder, pn, dtype, bs in MODELS:
        store = W / f'emb-{folder}.npz'; cache = dict(np.load(store, allow_pickle=True)['cache'].item()) if store.exists() else {}
        todo = [i for i, h in enumerate(hs) if h not in cache]; print(f'{name}: {len(cache)} cached, {len(todo)} to embed', flush=True)
        if not todo: continue
        kw = {'model_kwargs': {'torch_dtype': getattr(torch, dtype)}} if dtype == 'float16' else {}
        m = SentenceTransformer(str(M / folder), **kw); m.max_seq_length = 512; t0 = time.time(); step = 256
        for s in range(0, len(todo), step):
            ids = todo[s:s + step]; b = [texts[i] for i in ids]
            e = m.encode(b, batch_size=bs, normalize_embeddings=True, prompt_name=pn) if pn else m.encode(b, batch_size=bs, normalize_embeddings=True)
            for i, v in zip(ids, e): cache[hs[i]] = v.astype('float32')
            np.savez(store, cache=np.array(cache, dtype=object)); done = min(s + step, len(todo))
            print(f'  {name}: {done}/{len(todo)} texts, {time.time() - t0:.0f}s, {done / (time.time() - t0):.1f} texts/s', flush=True)
            try: torch.mps.empty_cache()
            except Exception: pass
        del m
    print('embedding done', flush=True)

NEG = [('library', 'Gesture Elicitation Studies'), ('library', 'OTTRS Mental Models'), ('library', 'Trust & Co'), ('collection', 'Killer Whale Research')]   # clearly unrelated areas: negatives for the proxy accuracy estimate
def analyze(models=None, novel_pct=15, rel_pct=10):
    docs = [json.loads(l) for l in open(W / 'docs.jsonl')]; texts = [f"{d['title']}. {d['text']}"[:2000] for d in docs]; hs = [hashlib.sha1(t.encode()).hexdigest()[:20] for t in texts]
    use = [m for m in MODELS if not models or m[1] in models or m[0] in models]; E = {}
    for name, folder, *_ in use:
        c = np.load(W / f'emb-{folder}.npz', allow_pickle=True)['cache'].item(); missing = [i for i, h in enumerate(hs) if h not in c]
        if missing: sys.exit(f'{name}: {len(missing)} texts not embedded yet; run: screen_all.py embed')
        E[name] = np.stack([c[h] for h in hs])
    names = [m[0] for m in use]; sd = [i for i, d in enumerate(docs) if d['kind'] == 'seed']; pp_ = [i for i, d in enumerate(docs) if d['kind'] == 'paper']
    cats = sorted({g for i in sd for g in docs[i]['groups']})
    # seed duplicates among the papers (the same paper already in the vault)
    st = {norm(docs[i]['title']): i for i in sd}
    for i in pp_:
        nt = norm(docs[i]['title']); docs[i]['seed_match'] = ''
        for k, j in st.items():
            if nt and abs(len(k) - len(nt)) < 30 and (nt[:40] == k[:40] or difflib.SequenceMatcher(None, k, nt[:len(k)]).ratio() >= 0.88): docs[i]['seed_match'] = docs[j]['pdf']; break
    seedmatched = {i for i in pp_ if docs[i]['seed_match']}
    # reference set P: seeds + the Elicit 2026-11-24 papers + Include-CA-Rep (the papers JP treats as in scope)
    elic = [i for i in pp_ if any('SysRev - Elicit 2026-11-24' in c for c in docs[i]['collections'])]; inc = [i for i in pp_ if 'Include-CA-Rep' in docs[i]['sets']]
    P = sorted(set(sd) | set(elic) | set(inc) | seedmatched)
    neg = [i for i in pp_ if any((k == 'library' and v in docs[i]['libraries']) or (k == 'collection' and any(c.endswith(v) or c.startswith(v) for c in docs[i]['collections'])) for k, v in NEG) and i not in set(P)]
    report = {'models': names, 'n_seeds': len(sd), 'n_reference': len(P), 'n_negatives_proxy': len(neg)}
    rel = {}; tau_rel = {}; tau_new = {}; loo = {}
    for name in names:
        X = E[name]; S = X @ X[P].T   # all docs x P
        selfmask = {i: k for k, i in enumerate(P)}
        for i, k in selfmask.items(): S[i, k] = -1
        r = S.max(axis=1); rel[name] = r; loo_p = r[P]; tau_rel[name] = float(np.percentile(loo_p, rel_pct))
        # seed groups: nearest seed per category
        Ss = X @ X[sd].T; sdi = {i: k for k, i in enumerate(sd)}
        for i, k in sdi.items(): Ss[i, k] = -1
        ok = tot = 0; nn = []
        for i in sd:
            best = None
            for c in cats:
                v = max([Ss[i, sdi[j]] for j in sd if j != i and c in docs[j]['groups']] or [-1])
                if best is None or v > best[0]: best = (v, c)
            if best[0] > -1 and all(any(c in docs[j]['groups'] for j in sd if j != i) for c in docs[i]['groups']): tot += 1; ok += best[1] in docs[i]['groups']; nn.append(best[0])
        tau_new[name] = float(np.percentile(nn, novel_pct)); loo[name] = {'accuracy': ok / max(tot, 1), 'n': tot}
    # relevance vote and proxy accuracy
    relv = np.stack([rel[n] >= tau_rel[n] for n in names]); relmaj = relv.sum(axis=0) >= (len(names) // 2 + 1); relany = relv.any(axis=0)   # JP, 2026-11-25: prefer false positives; a paper is flagged close to the seed when ANY model says so
    pos = [i for i in P if i not in set(sd)]
    if neg and pos:
        tpm = int(relmaj[pos].sum()); tnm = int((~relmaj[neg]).sum()); report['relevance_majority_rule'] = {'sensitivity': tpm / len(pos), 'specificity': tnm / len(neg), 'flagged_outside_ingest_sets': int(sum(1 for i in pp_ if relmaj[i] and not docs[i]['sets'] and i not in seedmatched))}
        tp = int(relany[pos].sum()); tn = int((~relany[neg]).sum())
        report['relevance_proxy'] = {'rule': 'any model above its threshold (favors false positives)', 'positives_n': len(pos), 'negatives_n': len(neg), 'sensitivity': tp / len(pos), 'specificity': tn / len(neg), 'balanced_accuracy': (tp / len(pos) + tn / len(neg)) / 2, 'note': 'positives = papers JP already treats as in scope (Elicit 2026-11-24 set, Include-CA-Rep; leave-one-out), negatives = clearly unrelated collections; a proxy, not JP labels'}
        try:
            from sklearn.metrics import roc_auc_score; sc = np.mean([rel[n] for n in names], axis=0); report['relevance_proxy']['auc'] = float(roc_auc_score([1] * len(pos) + [0] * len(neg), list(sc[pos]) + list(sc[neg])))
        except Exception: pass
    # categories for ingest sets and relevant papers
    target = [i for i in pp_ if i not in seedmatched and (docs[i]['sets'] or relany[i])]
    votes = {}
    for name in names:
        X = E[name]; Ss = X[target] @ X[sd].T
        for row, i in enumerate(target):
            sc = {c: max([Ss[row, k] for k, j in enumerate(sd) if c in docs[j]['groups']]) for c in cats}; rk = sorted(sc.items(), key=lambda kv: -kv[1]); top, ts = rk[0]
            votes.setdefault(i, {})[name] = {'pick': 'NEW' if ts < tau_new[name] else top, 'best_group': top, 'sim': float(ts), 'second': rk[1][0], 'second_sim': float(rk[1][1])}
    need = len(names) // 2 + 1
    for i in target:
        v = votes[i]; cnt = collections.Counter(x['pick'] for x in v.values()); top, n = cnt.most_common(1)[0]; docs[i]['majority'] = top if n >= need else 'no majority'; docs[i]['agreement'] = f'{n} of {len(names)}'; docs[i]['votes'] = v
        docs[i]['relevance'] = {n_: round(float(rel[n_][i]), 3) for n_ in names}; docs[i]['relevant'] = bool(relany[i]); docs[i]['relevant_votes'] = int(relv[:, i].sum())
    # majority-vote leave-one-out on seeds (category accuracy of the final rule)
    ok = tot = 0
    for i in sd:
        picks = []
        for name in names:
            X = E[name]; best = None
            for c in cats:
                v = max([float(X[i] @ X[j]) for j in sd if j != i and c in docs[j]['groups']] or [-1])
                if best is None or v > best[0]: best = (v, c)
            picks.append('NEW' if best[0] < tau_new[name] else best[1])
        if all(any(c in docs[j]['groups'] for j in sd if j != i) for c in docs[i]['groups']):
            tot += 1; c = collections.Counter(picks).most_common(1)[0]; ok += (c[1] >= need and c[0] in docs[i]['groups'])
    report['category_loo_majority'] = {'accuracy': ok / max(tot, 1), 'n': tot}; report['category_loo_by_model'] = loo; report['novel_threshold'] = tau_new; report['relevance_threshold'] = tau_rel
    # new categories: papers whose majority is NEW (or split), clustered on the mean distance of the models
    pool = [i for i in target if docs[i]['majority'] in ('NEW', 'no majority')]; clusters = {}
    if len(pool) >= 6:
        from sklearn.cluster import AgglomerativeClustering; from sklearn.metrics import silhouette_score
        Xc = np.hstack([E[n][pool] for n in names]) / np.sqrt(len(names)); D = np.clip(1 - Xc @ Xc.T, 0, None); np.fill_diagonal(D, 0); D = (D + D.T) / 2; best = (None, -2, None)   # Ward on the joined, normalized embeddings of all models
        for k in (15, 20, 25, 30):   # a reviewable number of new categories (JP can read 8-30 categories, not 200)
            if k >= len(pool): continue
            lab = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(Xc)
            sc = silhouette_score(D, lab, metric='precomputed')
            if sc > best[1]: best = (lab, sc, k)
        lab = best[0] if best[0] is not None else np.arange(len(pool)); sizes = collections.Counter(lab); order = [c for c, n in sizes.most_common() if n >= 3]
        for k, c in enumerate(order, 1):
            mem = [pool[j] for j in range(len(pool)) if lab[j] == c]; clusters[f'N{k}'] = {'members': [docs[i]['id'] for i in mem]}
            for i in mem: docs[i]['new_pile'] = f'N{k}'
        report['cluster_choice'] = {'pool': len(pool), 'silhouette': float(best[1]) if best[0] is not None else None, 'k_chosen': int(best[2]) if best[0] is not None else None, 'clusters_of_3_or_more': len(clusters), 'papers_in_small_or_no_cluster': sum(1 for i in pool if not docs[i].get('new_pile'))}
    out = {'categories': cats, 'report': report, 'clusters': clusters, 'seeds': [{k: d[k] for k in ('id', 'title', 'groups', 'pdf')} for d in docs if d['kind'] == 'seed'], 'papers': [d for d in docs if d['kind'] == 'paper' and (d['id'] in {docs[i]['id'] for i in target} or d['seed_match'] or d['id'] in {docs[i]['id'] for i in neg})], 'counts': {'distinct_papers': len(pp_), 'target_rows': len(target), 'relevant_not_in_ingest_sets': sum(1 for i in target if not docs[i]['sets']), 'ingest_sets': dict(collections.Counter(s for i in pp_ for s in docs[i]['sets']))}}
    (W / 'result.json').write_text(json.dumps(out, ensure_ascii=False, default=float), encoding='utf-8')
    print(json.dumps({'report': report, 'counts': out['counts']}, indent=1, default=float)); print('majority:', collections.Counter(docs[i]['majority'] for i in target).most_common(12))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=['prepare', 'embed', 'analyze']); ap.add_argument('--models', nargs='*', help='analyze only these models (for a test)'); a = ap.parse_args()
    {'prepare': prepare, 'embed': embed}.get(a.stage, lambda: analyze(a.models))()

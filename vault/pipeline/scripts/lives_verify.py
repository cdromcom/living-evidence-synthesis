#!/usr/bin/env python3
"""Verification layer (JP, 2026-11-26): every extracted item is checked by a foundation model (Claude Sonnet 5.5, with the screenshot where there is one) AND by the two decision models (Perplexity Decider 1.3, Liquid d1-ultra, text only), so that no extraction rests on one model. Item types: PICOST (the six slots of each finding), QUOTE (the quotes behind findings, questions, claims and caveats, against what is printed), QUE (reframed question against the original wording), CLM and CVT (claim or caveat against its passage), QUALITY (a quality-signal rating against its quote).
Output: pipeline/runs/<run>/verification.json, shown in the review sheet tabs "Verification (all nodes)" and "Verification summary". For each item: one score per model (Sonnet 1, 0.5 or 0; each decision model a probability), the majority vote, the mean across models and how many models agree with the majority. JP's ground-truth columns stay empty until JP fills them; the summary tab then computes accuracy, precision, recall and specificity per model, for the majority vote and for the mean.
Decision models cannot read images. They see text: the passage, the item, and the printed text that Sonnet 5.5 read from the screenshot."""
import collections, concurrent.futures as cf, json, os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz, lives_stages as S, llm_batch as L, pdf_pages as pp, decision_models as dm, config as C

R = S.R; SLOTS = {'P': 'Population', 'I': 'Intervention', 'C': 'Comparator', 'O': 'Outcome', 'S': 'Study design', 'T': 'Timeframe'}
SAME = 'Do TEXT A and TEXT P say exactly the same thing, with the same numbers, names, signs and symbols (ignore spacing, hyphenation and subscript formatting)?'


def short(s, n=300): s = re.sub(r'\s+', ' ', str(s or '')).strip(); return s if len(s) <= n else s[:n - 1] + '\u2026'


def pages_text(doc, pages, cap=3500):
    return '\n\n'.join(f'[PDF page {p}]\n' + pp.page_text(doc[p - 1])[:cap] for p in pages if 1 <= p <= len(doc))


def build_items(M):
    items = []; groups = []; sig = S.SIGNALS
    for ck, p in M.m['papers'].items():
        f_ = M.dir / ck / 'picost.json'
        if p.get('failed') or not f_.exists(): continue
        ps = json.loads(f_.read_text(encoding='utf-8')); doc = fitz.open(S.ex(p['pdf'])); qdir = M.dir / ck / 'quote_crops'
        def crop_of(fid, k): c = qdir / f'{fid}_s{k}.png'; return str(c) if c.exists() else None
        for f in ps.get('findings', []):
            pgs = sorted({s.get('pdf_page') for s in f.get('spans', []) if s.get('pdf_page')} | {n.get('pdf_page') for n in f.get('numbers', []) if n.get('pdf_page')})[:2]
            rec = '\n'.join(f"{SLOTS[k]}: {f.get(k) or 'Not reported'}" for k in SLOTS); passage = pages_text(doc, pgs) or '(no cited page)'; gid = f"{ck}|{f['id']}"
            groups.append({'gid': gid, 'instruction': 'PICOST: for each slot, is the value supported by the passage?', 'item': rec, 'passage': passage, 'crop': crop_of(f['id'], 1)})
            for k in SLOTS:   # one row per slot, so each slot can be judged and benchmarked on its own
                items.append({'paper': ck, 'ntype': 'PICOST', 'nid': f"{f['id']}: {SLOTS[k]}", 'what': f'{SLOTS[k]} slot supported by the cited pages', 'text': short(f.get(k) or 'Not reported', 400), 'kind': 'slot', 'gid': gid, 'slot': k, 'item': rec, 'passage': passage, 'crop': crop_of(f['id'], 1),
                              'dm_q': {k: dm.noul(f"Is the {SLOTS[k]} slot value in the record supported by the passage (or correctly marked Not reported)?")}})
            for k, s in enumerate(f.get('spans', []), 1):
                v = s.get('vision')
                if v: items.append(quote_item(ck, 'QUOTE', f"{f['id']} quote {k}", s['text'], v, crop_of(f['id'], k)))
        for kind, tag in (('questions', 'QUE'), ('claims', 'CLM'), ('caveats', 'CVT')):
            for it in ps.get(kind, []):
                text = it.get('original_wording') if kind == 'questions' else (it.get('span') or {}).get('text', ''); v = it.get('vision')
                if v: items.append(quote_item(ck, tag, f"{it['id']} quote", text, v, None))
                if kind == 'questions':
                    items.append({'paper': ck, 'ntype': 'QUE', 'nid': it['id'], 'what': 'reframed question asks the same as the original wording', 'text': short(f"Original: {it.get('original_wording')}\nReframed: {it.get('reframed')}", 500), 'kind': 'text', 'instruction': 'Does the reframed question ask the same thing as the original wording, without adding or dropping anything?', 'item': f"Original wording: {it.get('original_wording')}\nReframed question: {it.get('reframed')}", 'passage': it.get('original_wording', ''), 'crop': None, 'dm_q': {'same': dm.noul('Does the reframed question ask the same thing as the original wording, without adding or dropping anything?')}})
                else:
                    ins = 'Is the claim fully supported by the passage, with no stronger wording and no wider scope?' if tag == 'CLM' else 'Does the passage state this limitation or caveat, without adding anything?'
                    items.append({'paper': ck, 'ntype': tag, 'nid': it['id'], 'what': 'claim supported by its passage' if tag == 'CLM' else 'caveat stated in its passage', 'text': short(it.get('text'), 500), 'kind': 'text', 'instruction': ins, 'item': it.get('text', ''), 'passage': (it.get('vision') or {}).get('printed') or (it.get('span') or {}).get('text', ''), 'crop': None, 'dm_q': {'ok': dm.noul(ins)}})
        qf = M.dir / ck / 'quality_signals.json'
        if qf.exists():
            for x in json.loads(qf.read_text(encoding='utf-8')).get('raw', []):
                if not x.get('quote_found') or x['rating'] not in {a.strip() for a in sig.get(x['signal'], ('', ''))[1].split('|')}: continue
                what, vals = sig[x['signal']]; ins = f"Does the passage support the rating '{x['rating']}' for the quality signal '{x['signal']}' ({what})?"
                items.append({'paper': ck, 'ntype': 'QUALITY', 'nid': f"{x['signal']} ({x['rater']})", 'what': 'rating supported by its quote', 'text': short(f"{x['signal']} = {x['rating']} (rater {x['rater']}): {x['quote']}", 500), 'kind': 'text', 'instruction': ins, 'item': f"Signal: {x['signal']}\nRating: {x['rating']}", 'passage': x.get('quote', ''), 'crop': x.get('crop'), 'dm_q': {'ok': dm.noul(ins)}})
        doc.close()
    return items, groups


def quote_item(ck, tag, nid, text, v, crop):
    """A quote against what is printed: the screenshot reading (Sonnet 5.5, quote_check stage) is the foundation verdict; the decision models compare the two texts."""
    score = 0.0 if v.get('a_changes_meaning') else 1.0
    return {'paper': ck, 'ntype': tag, 'nid': nid, 'what': 'quote equals the printed text', 'text': short(f"A (model): {text}\nP (printed): {v.get('printed')}", 600), 'kind': 'precomputed', 'sonnet_score': score, 'sonnet_reason': '; '.join(v.get('a_differences') or []) or 'equals print', 'item': f'TEXT A:\n{text}\n\nTEXT P:\n{v.get("printed", "")}', 'crop': crop, 'dm_q': {'same': dm.noul(SAME)}}


def to_score(v): return {'yes': 1.0, 'no': 0.0}.get(str(v).lower(), 0.5)


def stage_verify(M, mode):
    st = M.m['stage_log'].setdefault('verify', {})
    if st.get('status') == 'done': return
    items, groups = build_items(M); sysv = S.prompt('verify-item-v1.md'); st['prompt'] = 'pipeline/prompts/verify-item-v1.md'; reqs = []
    for g in groups: reqs.append(L.Req('g::' + g['gid'], R['quote_check'], f"INSTRUCTION: {g['instruction']}\n\nITEM:\n{g['item']}\n\nPASSAGE:\n{g['passage']}", sysv, None, 'low', 900, images=[g['crop']] if g.get('crop') else []))
    for i, it in enumerate(items):
        it['id'] = f'v{i:04d}'
        if it['kind'] == 'text':
            body = f"INSTRUCTION: {it['instruction']}\n\nITEM:\n{it['item']}\n\nPASSAGE:\n{it['passage']}"
            reqs.append(L.Req(it['id'], R['quote_check'], body, sysv, None, 'low', 600, images=[it['crop']] if it.get('crop') else []))
    res = S.dispatch(M, 'verify_sonnet', reqs, mode)
    def run(it):
        state = it['item'] if it['kind'] == 'precomputed' else f"PASSAGE:\n{it['passage']}\n\nITEM:\n{it['item']}"
        return S.run_dm(state, it['dm_q'])
    with cf.ThreadPoolExecutor(8) as ex_: dres = list(ex_.map(run, items))
    for it, r in zip(items, dres):
        it['scores'] = {}; it['reasons'] = {}
        if it['kind'] == 'precomputed': it['scores']['sonnet'] = it['sonnet_score']; it['reasons']['sonnet'] = it['sonnet_reason']
        else:
            if it['kind'] == 'slot':
                j = S.safe_json(res.get('g::' + it['gid']) or L.Res('', False)) or {}; sl = j.get('slots') or {}
                it['scores']['sonnet'] = to_score(sl.get(it['slot'])) if it['slot'] in sl else None; it['reasons']['sonnet'] = j.get('reason', '')
            else:
                j = S.safe_json(res.get(it['id']) or L.Res('', False)) or {}
                it['scores']['sonnet'] = to_score(j['verdict']) if 'verdict' in j else None; it['reasons']['sonnet'] = j.get('reason', '')
        for pv in R['decision_models']:
            a = {k: v for k, v in (r.get(pv) or {}).items() if not k.startswith('_') and isinstance(v, (int, float))}
            it['scores'][pv] = min(a.values()) if a else None
        votes = {}
        for m_, sc in it['scores'].items():
            if sc is None: continue
            if m_ == 'sonnet': votes[m_] = 'pass' if sc >= 0.75 else ('fail' if sc < 0.5 else None)   # 0.5 (unsure) abstains
            else: votes[m_] = 'pass' if sc >= 0.5 else 'fail'
        c = collections.Counter(v for v in votes.values() if v)
        it['majority'] = 'pass' if c['pass'] > c['fail'] else ('fail' if c['fail'] > c['pass'] else 'split'); it['votes'] = votes
        sc_ = [s for s in it['scores'].values() if s is not None]; it['mean'] = round(sum(sc_) / len(sc_), 3) if sc_ else None
        it['agree'] = sum(1 for v in votes.values() if v and v == it['majority']); it.pop('instruction', None); it.pop('item', None); it.pop('passage', None); it.pop('dm_q', None); it.pop('kind', None); it.pop('gid', None); it.pop('slot', None)
    (M.dir / 'verification.json').write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    cnt = collections.Counter((it['ntype'], it['majority']) for it in items); st['status'] = 'done'; st['summary'] = {f'{a} {b}': n for (a, b), n in sorted(cnt.items())}; M.save(); M.event(f"verify: {len(items)} items; {st['summary']}")

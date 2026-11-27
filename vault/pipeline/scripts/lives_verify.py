#!/usr/bin/env python3
"""Verification layer (JP, 2026-11-26): every extracted item is checked by a foundation model (Claude Sonnet 5.5, with the screenshot where there is one) AND by the two decision models (Perplexity Decider 1.3, Liquid d1-ultra, text only), so that no extraction rests on one model. Item types: PICOST (the six slots of each finding), QUOTE (the quotes behind findings, questions, claims and caveats, against what is printed), QUE (reframed question against the original wording), CLM and CVT (claim or caveat against its passage), QUALITY (a quality-signal rating against its quote).
Output: pipeline/runs/<run>/verification.json, shown in the review sheet tabs "Verification (all nodes)" and "Verification summary". For each item: one score per model (Sonnet 1, 0.5 or 0; each decision model a probability), the majority vote, the mean across models and how many models agree with the majority. JP's ground-truth columns stay empty until JP fills them; the summary tab then computes accuracy, precision, recall and specificity per model, for the majority vote and for the mean.
Decision models cannot read images. They see text: the passage, the item, and the printed text that Sonnet 5.5 read from the screenshot."""
import collections, concurrent.futures as cf, json, os, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz, lives_stages as S, llm_batch as L, pdf_pages as pp, decision_models as dm, config as C

INS_QUE = 'The question was restyled on purpose. Does the reframed question still ask about what the original wording is about (same topic, methods and outcomes), allowing different phrasing, order and question form?'
INS_CLM = 'Does the claim keep the meaning of the passage? Different wording is fine. Answer no only if the claim states a fact, number, comparison or degree of certainty that the passage does not support.'
INS_CVT = 'Does the passage state this limitation or caveat? Different wording is fine. Answer no only if the caveat adds a fact, number or cause that the passage does not support.'
QS_MAX = S.QS_MAX   # maximum accuracy for quality ratings: all verifiers judge every rating (no cascade)
R = S.R; SLOTS = {'P': 'Population', 'I': 'Intervention', 'C': 'Comparator', 'O': 'Outcome', 'S': 'Study design', 'T': 'Timeframe'}
SAME = 'Do TEXT A and TEXT P say exactly the same thing, with the same numbers, names, signs and symbols (ignore spacing, hyphenation and subscript formatting)?'


def short(s, n=300): s = re.sub(r'\s+', ' ', str(s or '')).strip(); return s if len(s) <= n else s[:n - 1] + '\u2026'


def pages_text(doc, pages, cap=3500):
    return '\n\n'.join(f'[PDF page {p}]\n' + pp.page_text(doc[p - 1])[:cap] for p in pages if 1 <= p <= len(doc))


METHODS_HEAD = re.compile(r'^\s*(?:\d+(?:\.\d+)*\.?\s+)?(?:materials and methods|methods?|methodology|study design|experimental setup|experiments?|experimental design|data collection|datasets?|approach|setup)\s*$', re.I | re.M)
WITH_METHODS = True   # JP, 2026-11-26: the verifier also sees page 1 and the Methods pages, because population, design and timeframe are usually defined there


def methods_pages(doc, exclude=(), n_methods=2):
    """Page 1 (abstract) and the first pages that carry a Methods-type heading, as 1-based page numbers, skipping pages already shown."""
    out = [1]; start = next((i + 1 for i in range(len(doc)) if METHODS_HEAD.search(pp.page_text(doc[i]))), None)
    if start: out += list(range(start, min(start + n_methods, len(doc) + 1)))
    return [p for p in dict.fromkeys(out) if p not in exclude]


def build_items(M):
    items = []; groups = []; sig = S.SIGNALS
    for ck, p in M.m['papers'].items():
        f_ = M.dir / ck / 'picost.json'
        if p.get('failed') or not f_.exists(): continue
        ps = json.loads(f_.read_text(encoding='utf-8')); doc = fitz.open(S.ex(p['pdf'])); qdir = M.dir / ck / 'quote_crops'
        def crop_of(fid, k): c = qdir / f'{fid}_s{k}.png'; return str(c) if c.exists() else None
        for f in ps.get('findings', []):
            pgs = sorted({s.get('pdf_page') for s in f.get('spans', []) if s.get('pdf_page')} | {n.get('pdf_page') for n in f.get('numbers', []) if n.get('pdf_page')})[:2]
            rec = '\n'.join(f"{SLOTS[k]}: {f.get(k) or 'Not reported'}" for k in SLOTS); passage = pages_text(doc, pgs) or '(no cited page)'; passage += ('\n\n[CONTEXT: page 1 and Methods pages, for population, design and timeframe]\n' + pages_text(doc, methods_pages(doc, exclude=pgs), cap=3000)) if WITH_METHODS else ''; gid = f"{ck}|{f['id']}"
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
                    items.append({'paper': ck, 'ntype': 'QUE', 'nid': it['id'], 'what': INS_QUE, 'text': short(f"Original: {it.get('original_wording')}\nReframed: {it.get('reframed')}", 500), 'kind': 'text', 'instruction': INS_QUE, 'item': f"Original wording: {it.get('original_wording')}\nReframed question: {it.get('reframed')}", 'passage': it.get('original_wording', ''), 'crop': None, 'dm_q': {'same': dm.noul(INS_QUE)}})
                else:
                    ins = INS_CLM if tag == 'CLM' else INS_CVT
                    items.append({'paper': ck, 'ntype': tag, 'nid': it['id'], 'what': ins, 'text': short(it.get('text'), 500), 'kind': 'text', 'instruction': ins, 'item': it.get('text', ''), 'passage': (it.get('vision') or {}).get('printed') or (it.get('span') or {}).get('text', ''), 'crop': None, 'dm_q': {'ok': dm.noul(ins)}})
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
    for i, it in enumerate(items): it['id'] = f'v{i:04d}'
    def run(it):
        state = it['item'] if it['kind'] == 'precomputed' else f"PASSAGE:\n{it['passage']}\n\nITEM:\n{it['item']}"
        return S.run_dm(state, it['dm_q'])
    with cf.ThreadPoolExecutor(8) as ex_: dres = list(ex_.map(run, items))   # first pass: Liquid d1.2-ultra and Perplexity Decider 1.3 (JP, 2026-11-26)
    def dm_low(r, pv):
        a = [x for k, x in (r.get(pv) or {}).items() if not k.startswith('_') and isinstance(x, (int, float))]
        return min(a) if a else None
    def disagree(r):   # Sonnet 5.5 is called only when the two decision models differ (or one gave no answer)
        p, l = dm_low(r, 'perplexity'), dm_low(r, 'liquid')
        return p is None or l is None or ((p >= 0.5) != (l >= 0.5))
    call_ids = {it['id'] for it, r in zip(items, dres) if it['kind'] == 'text' and disagree(r)}; call_gids = {it['gid'] for it, r in zip(items, dres) if it['kind'] == 'slot' and disagree(r)}
    for g in groups:
        if g['gid'] in call_gids: reqs.append(L.Req('g::' + g['gid'], R['quote_check'], f"INSTRUCTION: {g['instruction']}\n\nITEM:\n{g['item']}\n\nPASSAGE:\n{g['passage']}", sysv, None, 'low', 900, images=[g['crop']] if g.get('crop') else []))
    for it in items:
        if it['kind'] == 'text' and it['id'] in call_ids:
            body = f"INSTRUCTION: {it['instruction']}\n\nITEM:\n{it['item']}\n\nPASSAGE:\n{it['passage']}"
            reqs.append(L.Req(it['id'], R['quote_check'], body, sysv, None, 'low', 600, images=[it['crop']] if it.get('crop') else []))
    res = S.dispatch(M, 'verify_sonnet', reqs, mode); st['sonnet_called_for'] = {'text items': len(call_ids), 'PICOST findings': len(call_gids), 'of text items': sum(1 for it in items if it['kind'] == 'text'), 'of PICOST findings': len({it['gid'] for it in items if it['kind'] == 'slot'})}
    for it, r in zip(items, dres):
        it['scores'] = {}; it['reasons'] = {}
        if it['kind'] == 'precomputed': it['scores']['sonnet'] = it['sonnet_score']; it['reasons']['sonnet'] = it['sonnet_reason']; it['sonnet_called'] = True   # quote_check stage: Sonnet reads every quote screenshot
        else:
            called = (it['gid'] in call_gids) if it['kind'] == 'slot' else (it['id'] in call_ids); it['sonnet_called'] = called
            if not called: it['scores']['sonnet'] = None; it['reasons']['sonnet'] = 'not called: Perplexity and d1.2-ultra agree'
            elif it['kind'] == 'slot':
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


NUM_PHRASE = 'Compare every digit in TEXT A with the digits in the highlighted (pink) part of the image. Are all digits identical and in the same order?'
WORD_PHRASE = 'Does TEXT A match the highlighted (pink) passage in the image exactly, with the same words, names, signs and symbols (ignore spacing and hyphenation)?'
INTRO = 'The image is a page excerpt with the passage of interest highlighted in pink. '


def image_question(x, text):
    """The question Liquid d1.2-ultra answers about the screenshot. Test on 60 Bougie/Sarol quotes (2026-11-26): the digit phrasing separated correct quotes from quotes with one digit changed with pairwise AUC 1.0 (0 of 60 correct quotes failed, 2 of 60 altered ones passed); the general phrasing gave AUC 0.92 with 9 false alarms, so digits are compared whenever the text has any."""
    a = text.split('\nP (printed)')[0].replace('A (model): ', '')
    if x['ntype'] in ('QUOTE',) or x['nid'].endswith(' quote'):
        return 'TEXT A:\n' + a, INTRO + (NUM_PHRASE if re.search(r'\d', a) else WORD_PHRASE)
    if x['ntype'] == 'QUALITY':
        sig, rest = a.split(' = ', 1); rating, quote = rest.split('): ', 1); rating = rating.split(' (')[0]
        return 'TEXT A:\n' + quote, INTRO + f"Does the highlighted passage support the rating '{rating}' for the quality signal '{sig.split(' (')[0]}'?"
    return 'TEXT A:\n' + a, INTRO + (INS_CLM.replace('the passage', 'the highlighted passage') if x['ntype'] == 'CLM' else INS_CVT.replace('the passage', 'the highlighted passage'))


def add_image_scores(M):
    """Second verifier on every item that has a screenshot: Liquid d1.2-ultra looks at the image (JP, 2026-11-26). PICOST slots and QUE rewordings are skipped (the screenshot shows one quote, not the Methods page or the reframing)."""
    f_ = M.dir / 'verification.json'
    if not f_.exists(): return
    items = json.loads(f_.read_text(encoding='utf-8')); todo = []
    for ck in M.m['papers']:
        pass
    for x in items:
        if x['ntype'] == 'PICOST' or (x['ntype'] == 'QUE' and not x['nid'].endswith(' quote')): continue
        crop = x.get('crop')
        if not crop and x['ntype'] in ('QUE', 'CLM', 'CVT'):
            base = x['nid'].split()[0]; d = M.dir / x['paper'] / 'quote_crops'; k = {'Q': 'questions', 'C': 'claims', 'V': 'caveats'}.get(base[0])
            c = d / f'{base}_{k[0]}.png' if k else None; crop = str(c) if c and c.exists() else None; x['crop'] = crop
        if crop and Path(crop).exists(): todo.append(x)
    def run(x):
        state, q = image_question(x, x['text'])
        if x['ntype'] in ('CLM', 'CVT'): state = 'TEXT A:\n' + x['text']
        r, e = dm.decide('liquid', state, {'ok': dm.noul(q)}, images=[x['crop']]); return (r or {}).get('answers', {}).get('ok', {}).get('noul')
    with cf.ThreadPoolExecutor(6) as ex_: res = list(ex_.map(run, todo))
    for x, sc in zip(todo, res):
        x['scores'].pop('liquid_image', None); x.pop('liquid_image_untested', None)
        # Only digit comparisons on quotes are a validated voter (pairwise AUC 1.0 on 60 quotes). Word comparisons gave false alarms on 5 of 8 correct quotes, and claim, caveat and quality-rating judgments from screenshots are untested: those scores are shown but do not vote.
        if x['ntype'] == 'QUOTE' or x['nid'].endswith(' quote'):
            if re.search(r'\d', x['text'].split('\nP (printed)')[0]): x['scores']['liquid_image'] = sc
            else: x['liquid_image_untested'] = sc
        else: x['liquid_image_untested'] = sc
        if 'liquid_image' not in x['scores']: pass
        votes = {k: ('pass' if (k == 'sonnet' and s >= 0.75) or (k != 'sonnet' and s >= 0.5) else 'fail' if (k != 'sonnet' or s < 0.5) else None) for k, s in x['scores'].items() if s is not None}
        c = collections.Counter(v for v in votes.values() if v); x['votes'] = votes
        x['majority'] = 'pass' if c['pass'] > c['fail'] else ('fail' if c['fail'] > c['pass'] else 'split')
        sc_ = [s for s in x['scores'].values() if s is not None]; x['mean'] = round(sum(sc_) / len(sc_), 3) if sc_ else None; x['agree'] = sum(1 for v in votes.values() if v and v == x['majority'])
    f_.write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    n = sum(1 for sc in res if sc is not None); M.m['stage_log'].setdefault('verify_images', {}).update(status='done', summary={'items with image': len(todo), 'scored': n, 'voting (digit comparisons on quotes)': sum(1 for x in todo if x['scores'].get('liquid_image') is not None), 'judged correct': sum(1 for x in todo if (x['scores'].get('liquid_image') or 0) >= 0.5)}); M.save()
    M.event(f"verify_images: {n} of {len(todo)} screenshots scored by Liquid d1.2-ultra")


def revote(x):
    """Majority and mean from the scores that vote: Sonnet (1 pass, 0.5 abstains, 0 fail), Perplexity, Liquid text, and Liquid screenshot digit comparisons."""
    votes = {}
    for k, sc in x['scores'].items():
        if sc is None: continue
        if k == 'sonnet': votes[k] = 'pass' if sc >= 0.75 else ('fail' if sc < 0.5 else None)
        else: votes[k] = 'pass' if sc >= 0.5 else 'fail'
    c = collections.Counter(v for v in votes.values() if v); x['votes'] = votes
    x['majority'] = 'pass' if c['pass'] > c['fail'] else ('fail' if c['fail'] > c['pass'] else 'split')
    sc_ = [s for s in x['scores'].values() if s is not None]; x['mean'] = round(sum(sc_) / len(sc_), 3) if sc_ else None
    x['agree'] = sum(1 for v in votes.values() if v and v == x['majority'])


def rerun_liquid_text(M):
    """Rerun the Liquid text checks of the verification stage with the model now set in decision_models.MODELS (d1.2-ultra). The earlier scores (d1-ultra) stay in `liquid_d1_ultra` for comparison; the new ones become the voting `liquid` score. Also attaches the passage each non-PICOST item was checked against, so a person can judge it in the sheet."""
    f_ = M.dir / 'verification.json'; items = json.loads(f_.read_text(encoding='utf-8')); fresh, _ = build_items(M)
    assert len(fresh) == len(items), (len(fresh), len(items))
    for a, b in zip(fresh, items): assert (a['paper'], a['ntype'], a['nid']) == (b['paper'], b['ntype'], b['nid']), (a['nid'], b['nid'])
    def run(a):
        state = a['item'] if a['kind'] == 'precomputed' else f"PASSAGE:\n{a['passage']}\n\nITEM:\n{a['item']}"
        r, e = dm.decide('liquid', state, a['dm_q']); ans = {k: v.get('noul') for k, v in ((r or {}).get('answers') or {}).items() if isinstance(v, dict) and v.get('noul') is not None}
        return min(ans.values()) if ans else None
    with cf.ThreadPoolExecutor(8) as ex_: res = list(ex_.map(run, fresh))
    for a, b, sc in zip(fresh, items, res):
        if 'liquid_d1_ultra' not in b: b['liquid_d1_ultra'] = b['scores'].get('liquid')
        b['scores']['liquid'] = sc; b['liquid_model'] = dm.MODELS['liquid']
        if a['ntype'] != 'PICOST': b['passage'] = short(a.get('passage') or a['item'], 600)
        revote(b)
    f_.write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    M.m['stage_log'].setdefault('verify_liquid_rerun', {}).update(status='done', model=dm.MODELS['liquid'], scored=sum(1 for r in res if r is not None)); M.save()
    return items


def queue_order(V):
    """Order for the review sheet and JP's labeling session (2026-11-26): 1 every CLM, 2 every CVT, 3 a random 25% of quality ratings (fixed seed), 4 every QUE reframing; inside a group the items the models disagree on or fail come first; everything else follows in the original order. Sets x['queue']."""
    import random
    qual = [x for x in V if x['ntype'] == 'QUALITY']; rnd = random.Random(2026); pick = {id(x) for x in rnd.sample(qual, max(1, round(0.25 * len(qual))))} if qual else set()
    for x in V:
        jq = not x['nid'].endswith(' quote')   # the quote-versus-print rows of claims and caveats are not queued
        x['queue'] = ('1 CLM' if x['ntype'] == 'CLM' and jq else '2 CVT' if x['ntype'] == 'CVT' and jq else '3 QUALITY (25% random sample)' if id(x) in pick else '4 QUE reframing' if x['ntype'] == 'QUE' and not x['nid'].endswith(' quote') else '')
    order = {'1 CLM': 1, '2 CVT': 2, '3 QUALITY (25% random sample)': 3, '4 QUE reframing': 4, '': 9}
    idx = {id(x): i for i, x in enumerate(V)}
    return sorted(V, key=lambda x: (order[x['queue']], 0 if x['majority'] != 'pass' else 1, x['mean'] if x['mean'] is not None else 1, idx[id(x)]) if x['queue'] else (9, 0, 0, idx[id(x)]))


STOP = set('the a an of and or to in on for with by is are was were be been that this these those as at from it its their than then which who whom into over under between across not no also can could may might would should will'.split())


def novel_share(item, passage):
    """Share of the item's content words (4+ letters, not stop words) and numbers that do not appear in the passage. A cheap similarity measure for claims, caveats and rewordings that go beyond their quote: 0 means every word is in the quote."""
    toks = lambda t: [w for w in re.findall(r"[A-Za-z][A-Za-z\-]{3,}|\d+(?:[.,]\d+)?", t.lower()) if w not in STOP]
    a = toks(item); b = set(toks(passage))
    stem = lambda w: w[:5]
    bs = {stem(w) for w in b}
    return round(sum(1 for w in a if stem(w) not in bs) / len(a), 3) if a else None


def add_novel_share(M):
    f_ = M.dir / 'verification.json'; items = json.loads(f_.read_text(encoding='utf-8')); fresh, _ = build_items(M)
    for a, b in zip(fresh, items):
        b.pop('novel_share', None)
        if b['ntype'] in ('CLM', 'CVT', 'QUE') and not b['nid'].endswith(' quote'):
            item = a['item'].split('Reframed question: ')[-1] if b['ntype'] == 'QUE' else a['item']
            b['novel_share'] = novel_share(item, a.get('passage') or '')
    f_.write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    return items


def rerun_with_new_questions(M, mode='standard'):
    """Rerun the verifiers (Sonnet 5.5, Perplexity, Liquid d1.2-ultra) on PICOST slots (now with page 1 and the Methods pages) and on CLM, CVT and QUE judgments (now with meaning-based questions: rewording and restyling are fine). The earlier scores are kept in `scores_before_rerun` for comparison."""
    f_ = M.dir / 'verification.json'; items = json.loads(f_.read_text(encoding='utf-8')); fresh, groups = build_items(M)
    assert len(fresh) == len(items)
    idx = [i for i, (a, b) in enumerate(zip(fresh, items)) if a['ntype'] == 'PICOST' or (a['ntype'] in ('CLM', 'CVT', 'QUE') and not a['nid'].endswith(' quote'))]
    for i in idx: assert (fresh[i]['paper'], fresh[i]['ntype'], fresh[i]['nid']) == (items[i]['paper'], items[i]['ntype'], items[i]['nid'])
    sysv = S.prompt('verify-item-v1.md'); reqs = []
    for g in groups: reqs.append(L.Req('g::' + g['gid'], R['quote_check'], f"INSTRUCTION: {g['instruction']}\n\nITEM:\n{g['item']}\n\nPASSAGE:\n{g['passage']}", sysv, None, 'low', 900, images=[g['crop']] if g.get('crop') else []))
    for i in idx:
        a = fresh[i]
        if a['kind'] == 'text': reqs.append(L.Req(f'v{i:04d}', R['quote_check'], f"INSTRUCTION: {a['instruction']}\n\nITEM:\n{a['item']}\n\nPASSAGE:\n{a['passage']}", sysv, None, 'low', 600, images=[a['crop']] if a.get('crop') else []))
    res = S.dispatch(M, 'verify_methods', reqs, mode)
    def run_dms(i):
        a = fresh[i]; state = f"PASSAGE:\n{a['passage']}\n\nITEM:\n{a['item']}"; out = {}
        for pv in R['decision_models']:
            r, e = dm.decide(pv, state, a['dm_q']); ans = [x.get('noul') for x in ((r or {}).get('answers') or {}).values() if isinstance(x, dict) and x.get('noul') is not None]
            out[pv] = min(ans) if ans else None
        return out
    with cf.ThreadPoolExecutor(8) as ex_: dres = list(ex_.map(run_dms, idx))
    for i, d_ in zip(idx, dres):
        a, b = fresh[i], items[i]
        if 'scores_before_rerun' not in b: b['scores_before_rerun'] = {k: b['scores'].get(k) for k in ('sonnet', 'perplexity', 'liquid')}; b['what_before_rerun'] = b['what']
        if a['kind'] == 'slot':
            j = S.safe_json(res.get('g::' + a['gid']) or L.Res('', False)) or {}; sl = j.get('slots') or {}; b['scores']['sonnet'] = to_score(sl.get(a['slot'])) if a['slot'] in sl else None; b['reasons']['sonnet'] = j.get('reason', '')
        else:
            j = S.safe_json(res.get(f'v{i:04d}') or L.Res('', False)) or {}; b['scores']['sonnet'] = to_score(j['verdict']) if 'verdict' in j else None; b['reasons']['sonnet'] = j.get('reason', '')
        b['scores']['perplexity'] = d_.get('perplexity'); b['scores']['liquid'] = d_.get('liquid'); b['what'] = a['what']
        if a['ntype'] != 'PICOST': b['passage'] = short(a.get('passage') or a['item'], 600)
        revote(b)
    f_.write_text(json.dumps(items, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    M.m['stage_log'].setdefault('verify_rerun_methods', {}).update(status='done', items=len(idx)); M.save(); return items


def rescore_quality(M, mode='standard'):
    """After the quality-signal ratings are rerun: score the new QUALITY items (rating against its quote) with Sonnet 5.5, Perplexity and Liquid d1.2-ultra, replace the old QUALITY items in verification.json, then read their screenshots with d1.2-ultra (digits)."""
    f_ = M.dir / 'verification.json'; items = json.loads(f_.read_text(encoding='utf-8')) if f_.exists() else []
    fresh, _ = build_items(M); new = [a for a in fresh if a['ntype'] == 'QUALITY']
    sysv = S.prompt('verify-item-v1.md'); reqs = []
    for i, a in enumerate(new): a['id'] = f'q{i:04d}'
    def run(a):
        state = f"PASSAGE:\n{a['passage']}\n\nITEM:\n{a['item']}"; out = {}
        for pv in R['decision_models']:
            r, e = dm.decide(pv, state, a['dm_q']); ans = [y.get('noul') for y in ((r or {}).get('answers') or {}).values() if isinstance(y, dict) and y.get('noul') is not None]; out[pv] = min(ans) if ans else None
        return out
    with cf.ThreadPoolExecutor(8) as ex_: dres = list(ex_.map(run, new))   # first pass: d1.2-ultra and Perplexity; Sonnet 5.5 only where they differ
    def split(d_): return QS_MAX or d_.get('perplexity') is None or d_.get('liquid') is None or ((d_['perplexity'] >= 0.5) != (d_['liquid'] >= 0.5))
    called = {a['id'] for a, d_ in zip(new, dres) if split(d_)}
    for a in new:
        if a['id'] in called: reqs.append(L.Req(a['id'], R['quote_check'], f"INSTRUCTION: {a['instruction']}\n\nITEM:\n{a['item']}\n\nPASSAGE:\n{a['passage']}", sysv, None, 'low', 600, images=[a['crop']] if a.get('crop') else []))
    res = S.dispatch(M, 'verify_quality', reqs, mode)
    kept = [x for x in items if x['ntype'] != 'QUALITY']; added = []
    for a, d_ in zip(new, dres):
        j = (S.safe_json(res.get(a['id']) or L.Res('', False)) or {}) if a['id'] in called else {}
        it = {k: a[k] for k in ('paper', 'ntype', 'nid', 'what', 'text', 'crop')}; it['passage'] = short(a.get('passage') or a['item'], 600)
        it['scores'] = {'sonnet': to_score(j['verdict']) if 'verdict' in j else None, 'perplexity': d_.get('perplexity'), 'liquid': d_.get('liquid')}; it['reasons'] = {'sonnet': j.get('reason', '') if a['id'] in called else 'not called: Perplexity and d1.2-ultra agree'}; it['sonnet_called'] = a['id'] in called
        revote(it); added.append(it)
    f_.write_text(json.dumps(kept + added, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    M.m['stage_log'].setdefault('verify_quality', {}).update(status='done', items=len(added)); M.save()
    add_image_scores(M); return added

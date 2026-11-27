#!/usr/bin/env python3
"""Quality-signal checks after a batch (JP, 2026-11-26): code-only checks (provenance, links, statistics) next to the model ratings, written to one file the web app and the review sheet read.
  python3 qs_export.py RUN            run the code-only checks (once per paper), then export every paper of the run
  python3 qs_export.py RUN --export   export only (no network)
Output: pipeline/provenance/provenance-quality-signals.json (papers[citekey].provenance written by provenance/store.py, papers[citekey].signals written here) and
pipeline/provenance/quality-signal-screenshots/<citekey>/<signal>__<rater>.jpg. Nothing here changes the vault pages."""
import json, sys, time
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); sys.path.insert(0, str(Path(__file__).resolve().parent / 'provenance'))
import fitz
from PIL import Image
import signal_registry as SR, lives_stages as S

PROV = SR.VAULT / 'pipeline' / 'provenance'; STORE = PROV / 'provenance-quality-signals.json'; SHOTS = PROV / 'quality-signal-screenshots'
NAMES = {'neon': 'Gemini 4 Neon', 'opus': 'Claude Opus 5.5', 'sol': 'GPT-6.2 Sol'}; SHORT = {'neon': 'Neon', 'opus': 'Opus', 'sol': 'Sol'}
VERIFIERS = {'sonnet': 'Claude Sonnet 5.5', 'perplexity': 'Perplexity Decider 1.3', 'liquid': 'Liquid d1.2-ultra'}


def now(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load_store():
    return json.loads(STORE.read_text(encoding='utf-8')) if STORE.exists() else {'schema': 1, 'papers': {}}


def save_store(d):
    PROV.mkdir(parents=True, exist_ok=True); d['schema'] = 1; d['_about'] = 'Quality-signal detail for the web app and the review sheets: provenance (code-only checks with date and source) and signals (model ratings, quotes, screenshots, verifier scores) per paper. Written by provenance/store.py and qs_export.py; read by scripts/build-graph.mjs.'
    STORE.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding='utf-8')


def stat_item(pdf):
    import stat_checks as sc
    for k in list(sc.EXAMINED): sc.EXAMINED[k] = 0
    sc.EFFECT_VALUES.clear(); doc = fitz.open(pdf); finds = list(sc.run(doc)); doc.close(); ex = dict(sc.EXAMINED); n = sum(ex.values())
    res = (f"Examined {n} passages with 18 scripted checks; {len(finds)} clue{'s' if len(finds) != 1 else ''} for a person." if finds else f"Examined {n} passages with 18 scripted checks; nothing to flag. This is not proof the numbers are right.")
    detail = ' '.join(f"{f['check']} on {f['page']}: {f['finding']}" for f in finds[:4])
    return {'id': 'stat-checks', 'label': 'Statistical accuracy (scripted)', 'tool': 'stat_checks.py and stat_checks_more.py', 'status': 'flag' if finds else 'ok', 'result': res, 'detail': detail, 'url': '', 'checked_utc': now(), 'http_status': None, 'data': {'examined': ex, 'findings': finds[:20]}}


def run_code_checks(M, log=print):
    """Provenance, links and statistics for every paper of the run; stored per citekey. Network errors are recorded, never raised: the checks use public web services."""
    store = load_store(); report = {}
    try: import run_provenance as RP
    except Exception as e: RP = None; log(f'provenance module not available: {e}')
    for ck, p in M.m['papers'].items():
        if p.get('failed'): continue
        t0 = time.time(); meta = {}
        pj = M.dir / ck / 'picost.json'
        if pj.exists(): meta = json.loads(pj.read_text(encoding='utf-8')).get('paper', {})
        key = SR.resolve_citekey(ck, meta.get('title', ''), meta.get('year', '')) or ck; pdf = S.ex(p['pdf']); items = []; err = None
        if RP:
            try: items += RP.collect(pdf, key, doi=meta.get('doi') or None, title=meta.get('title'), vendors=('OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral'))
            except Exception as e: err = f'{type(e).__name__}: {e}'; items.append({'id': 'provenance-error', 'label': 'Provenance checks', 'tool': 'run_provenance.py', 'status': 'unavailable', 'result': 'The provenance checks could not run.', 'detail': err[:300], 'url': '', 'checked_utc': now(), 'http_status': None})
        try: items.append(stat_item(pdf))
        except Exception as e: items.append({'id': 'stat-checks', 'label': 'Statistical accuracy (scripted)', 'tool': 'stat_checks.py', 'status': 'unavailable', 'result': 'The statistics checks could not run.', 'detail': f'{type(e).__name__}: {e}'[:300], 'url': '', 'checked_utc': now(), 'http_status': None})
        store = load_store(); pp_ = store['papers'].setdefault(key, {'citekey': key}); pp_.update(title=meta.get('title', ''), doi=meta.get('doi', ''), checked_utc=now())
        have = {i['id']: i for i in pp_.get('provenance', [])}
        for i in items: have[i['id']] = i
        pp_['provenance'] = list(have.values()); save_store(store); report[ck] = {'citekey': key, 'items': len(items), 'elapsed_s': round(time.time() - t0), 'error': err}
        log(f"{ck[:24]}: {len(items)} checks in {report[ck]['elapsed_s']} s")
    st = M.m['stage_log'].setdefault('qs_code_checks', {}); st.update(status='done', papers=report, elapsed_s=sum(r['elapsed_s'] for r in report.values())); M.save(); return report


def jpeg(src, dst, side=900):
    dst.parent.mkdir(parents=True, exist_ok=True); im = Image.open(src).convert('RGB'); im.thumbnail((side, side)); im.save(dst, 'JPEG', quality=70, optimize=True); return dst


def summary_sentence(final, rows, agg, checks):
    by = {r['rater']: r['rating'] for r in rows if r.get('rating') and not str(r['rating']).startswith(('invalid', 'no answer'))}; counted = [r for r in ('neon', 'opus') if r in by]
    if not by: s = 'No rater gave a valid rating.'
    elif final == 'no majority': s = f"The raters gave different ratings ({', '.join(f'{SHORT[r]} {v}' for r, v in by.items())}), so this needs your judgment."
    elif len(set(by.values())) == 1 and len(by) >= 2: s = (f"{' and '.join(SHORT[r] for r in by)} both rate this {final}." if len(by) == 2 else f"All three raters (Neon, Opus, Sol) rate this {final}.")
    else:
        agree = [SHORT[r] for r, v in by.items() if v == final]; other = [f"{SHORT[r]} rated it {v}" for r, v in by.items() if v != final]
        s = f"{' and '.join(agree)} rate this {final}" + (f"; {', '.join(other)}." if other else '.')
    if checks:
        low = [c['verifier'] for c in checks if c['score'] is not None and c['score'] < 0.5]
        s += ' The quote check agrees.' if not low else f" {', '.join(low)} judge that the quote does not clearly support the rating."
    return s


def export_paper(M, ck, log=print):
    p = M.m['papers'][ck]; pj = M.dir / ck / 'picost.json'; meta = json.loads(pj.read_text(encoding='utf-8')).get('paper', {}) if pj.exists() else {}
    key = SR.resolve_citekey(ck, meta.get('title', ''), meta.get('year', '')) or ck
    qf = M.dir / ck / 'quality_signals.json'
    if not qf.exists(): return None
    q = json.loads(qf.read_text(encoding='utf-8')); raws = q['raw']; aggs = {a['signal']: a for a in q['aggregate']}
    ver = {}; vf = M.dir / 'verification.json'
    if vf.exists():
        for x in json.loads(vf.read_text(encoding='utf-8')):
            if x['ntype'] == 'QUALITY' and x['paper'] == ck: ver[x['nid']] = x
    store = load_store(); entry = store['papers'].setdefault(key, {'citekey': key}); vtags = SR.vault_tags(key); vtrip = SR.vault_tripod(key); signals = {}
    for sg in S.SIGNALS:
        rows = [r for r in raws if r['signal'] == sg]
        if not rows: continue
        ratings = []; verdicts = {k: [] for k in VERIFIERS}
        for r in rows:
            shot = None
            if r.get('crop') and Path(r['crop']).exists(): shot = f"{key}/{sg}__{r['rater']}.jpg"; jpeg(r['crop'], SHOTS / key / f"{sg}__{r['rater']}.jpg")
            qt = (r.get('quote') or '').strip(); v = ver.get(f"{sg} ({r['rater']})")
            if v:
                for k in VERIFIERS:
                    sc = v['scores'].get(k)
                    if sc is not None and r['rater'] in ('neon', 'opus', 'sol'): verdicts[k].append((sc, (v['reasons'].get('sonnet') if k == 'sonnet' else '')))
            ratings.append({'rater': NAMES.get(r['rater'], r['rater']), 'rating': r['rating'], 'quote': '' if qt.lower() == 'none' else qt, 'locator': r.get('locator', ''), 'pdf_page': r.get('pdf_page'), 'printed_page': None,
                            'quote_found': r.get('quote_found'), 'screenshot': shot, 'counted': bool(r.get('counted', True)) and r['rater'] in ('neon', 'opus', 'sol')})
        a = aggs.get(sg, {}); final = a.get('majority', 'no majority')
        checks = [{'verifier': VERIFIERS[k], 'score': round(sum(s for s, _ in v) / len(v), 2), 'note': next((n for s, n in v if n and s < 0.75), '')} for k, v in verdicts.items() if v]
        tag = SR.SIGNAL_TAGS.get(sg); vv = vtags.get(tag) if tag else None
        if sg.startswith('tripod-'): vv = vtrip.get(sg)   # the old curated TRIPOD-LLM table on the source page
        signals[sg] = {'id': sg, 'label': SR.label_for(sg), 'final': final, 'agreement': 'agree' if a.get('agreement') in ('both raters agree', 'all raters agree') else ('no-majority' if final == 'no majority' else 'majority'),
                       'summary': summary_sentence(final, rows, a, checks), 'ratings': ratings, 'checks': checks, 'tool_checks': SR.TOOL_CHECKS.get(sg, []), 'vault_value': vv, 'matches_vault': (None if vv is None else vv == final)}
    prov = {i['id']: i for i in entry.get('provenance', [])}
    for sg, tag in SR.TOOL_SIGNAL_TAGS.items():
        ids = SR.TOOL_CHECKS.get(sg, []); items = [prov[i] for i in ids if i in prov]
        if not items: continue
        worst = 'flag' if any(i['status'] == 'flag' for i in items) else ('unavailable' if all(i['status'] == 'unavailable' for i in items) else 'ok')
        signals[sg] = {'id': sg, 'label': SR.label_for(sg), 'final': ' '.join(i['result'] for i in items[:1]), 'agreement': 'agree', 'summary': items[0]['result'], 'ratings': [], 'checks': [], 'tool_checks': ids, 'vault_value': vtags.get(tag), 'matches_vault': None, 'status': worst}
    import tripod_items as TI
    sl = M.m['stage_log']; entry['signals'] = signals; entry['tripod'] = TI.summary({s_: x_['final'] for s_, x_ in signals.items() if s_.startswith('tripod-')}); entry['tripod_old_table'] = TI.summary(vtrip)
    entry['qs_run'] = {'run_id': M.m['run_id'], 'exported_utc': now(), 'raters': ['Gemini 4 Neon (High)', 'Claude Opus 5.5', 'GPT-6.2 Sol (adjudicates disagreements)'], 'prompt': sl.get('qs', {}).get('prompt'), 'elapsed_s': sl.get('qs', {}).get('elapsed_s'), 'signals_rated': len(S.SIGNALS), 'tripod_items_rated': len(TI.ITEMS)}
    save_store(store); log(f"{ck[:24]}: {len(signals)} signals exported for {key}"); return key


def run(M, code_checks=True, log=print):
    if code_checks: run_code_checks(M, log)
    keys = {}
    for ck in M.m['papers']:
        if M.m['papers'][ck].get('failed'): continue
        k = export_paper(M, ck, log)
        if k: keys[ck] = k
    M.m['stage_log'].setdefault('qs_export', {}).update(status='done', papers=keys); M.save(); return keys


if __name__ == '__main__':
    import lives_run as LR, decision_models as dm; dm.load_env()
    M = LR.Manifest(sys.argv[1]); run(M, code_checks='--export' not in sys.argv)

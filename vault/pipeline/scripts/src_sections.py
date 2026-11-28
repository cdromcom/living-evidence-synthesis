#!/usr/bin/env python3
"""Generated parts of an SRC page (JP, 2026-11-27). Nothing here calls a model: the Properties table, the Quality appraisal table, the TRIPOD-LLM reporting table, the evidence provenance table
and the AI-use table are written from data (the paper's entry in pipeline/provenance/provenance-quality-signals.json, the run's call log and manifest, the extraction), so a model cannot change a rating,
a quote or a model name. Layout mirrors the older source pages and the LIVES web app (lib/markdown.ts reads '## Quality appraisal' and '## TRIPOD-LLM reporting', a bold first cell, and a cell that holds
one status glyph alone, which it draws as a dot).

  load_paper(citekey)                       the paper's entry in the quality-signals export, or None
  quality_table(paper, printed)             ('## Quality appraisal' section text, [(S-key, signal id)])
  tripod_table(paper, printed, start)       ('## TRIPOD-LLM reporting' section text, keys)
  provenance_table(paper, keys, citekey)    collapsed callout with the quote, locator, models and verifier scores behind every S-key
  properties_table(...)                     collapsed callout 'Properties' in the field order of the older Woelfle source page
  ai_use_table(...)                         collapsed callout 'AI use': one row per model"""
import json, re
from pathlib import Path
import call_logger as cl, config as C

VAULT = cl.VAULT; STORE = VAULT / 'pipeline' / 'provenance' / 'provenance-quality-signals.json'; SHOTS = 'pipeline/provenance/quality-signal-screenshots'

# ------------------------------------------------------------------ Quality appraisal (rows and order of the older source pages)
QA_ROWS = [
    ('construct-validity', 'Construct validity', 'does the metric actually measure the construct?'),
    ('internal-validity', 'Internal validity', 'could the comparison be biased?'),
    ('external-validity', 'External validity', 'do findings generalize?'),
    ('statistical-rigor', 'Statistical conclusion validity', 'appropriate uncertainty + comparisons?'),
    ('reproducibility', 'Reproducibility', 'code, data, determinism?'),
    ('data-leakage', 'Data leakage', 'could models have seen this data in pretraining?'),
    ('baseline-adequacy', 'Baseline adequacy', 'is there a meaningful floor to beat?'),
    ('train-dev-test', 'Train/dev/test hygiene', 'are data splits kept separate?'),
    ('multiple-comparisons', 'Multiple-comparisons correction', 'controlled for repeated testing?'),
    ('human-baseline', 'Human-baseline comparability', 'is there a human reference point?'),
    ('confidence-intervals', 'Confidence Intervals', 'are point estimates accompanied by an interval?'),
    ('chance-corrected-metrics', 'Chance-Corrected Metrics', 'does agreement or accuracy correct for chance?'),
    ('spin', 'Hype/spin', 'are null or negative findings framed plainly?'),
    ('statistic-accuracy', 'Statistical Accuracy', "do the paper's own reported numbers check out?"),
    ('ablation-experiments', 'Ablation Experiment(s)', "does the paper isolate a component's contribution?"),
    ('code-quality-fair', 'Code Quality', 'does the released code follow FAIR-software practices?'),
    ('data-quality-fair', 'Data Quality', 'is the released dataset FAIR?'),
]
RISK_EMOJI = {'low-risk': '🟢', 'some-concerns': '🟡', 'high-risk': '🔴', 'addressed': '🟢', 'partial': '🟡', 'unresolved': '🟡', 'not-addressed': '🔴', 'not-done': '🔴', 'not-applicable': '➖', 'exploratory': '🟡', 'disclosed': '🟢', 'not-disclosed': '🔴'}
TOOL_EMOJI = {'ok': '🟢', 'flag': '🟡', 'unavailable': '➖'}
TRIPOD_EMOJI = {'fully': '✅', 'partial': '⚠️', 'not-reported': '❌', 'not-applicable': '➖'}
TRIPOD_FIXED = {'2': ('Abstract', '➖', 'Assessed separately under the TRIPOD-LLM abstract extension, not scored here.'), '17': ('Performance', 'per-EVD', 'Reported per EVD; see each EVD node of this paper.')}
TRIPOD_WORD = {'fully': 'Fully reported', 'partial': 'Partly reported', 'not-reported': 'Not reported', 'not-applicable': 'Not applicable'}
QUOTE_CHARS = 190


def words(s):
    s = str(s).replace('-', ' '); return s[:1].upper() + s[1:]


def load_paper(citekey):
    if not STORE.exists(): return None
    return json.loads(STORE.read_text(encoding='utf-8')).get('papers', {}).get(citekey)


def cell(s):
    return ' '.join(str(s).replace('|', '/').replace('\n', ' ').split())


def shorten(q, n=QUOTE_CHARS):
    q = ' '.join(q.split())
    if len(q) <= n: return q
    return q[:n].rsplit(' ', 1)[0].rstrip('.,;: ') + ' ...'


def where(r, printed):
    pg = r.get('pdf_page'); pr = r.get('printed_page') or (printed.get(pg) if pg else None)
    return (f'p. {pr}' if pr else (f'PDF p. {pg}' if pg else ''))


def evidence_cell(sig, key, printed, names=None):
    """Rating word, the shortest quote that carries it with its printed page, and the S-key that opens the provenance row."""
    rs = [r for r in sig.get('ratings', []) if r.get('quote')]
    rating = (names or {}).get(sig['final']) or words(sig['final']) if sig.get('ratings') else None
    if rs:
        r = rs[0]; q = shorten(r['quote']).replace('"', "'"); return f"{rating}. *\"{q}\"* `{where(r, printed)}` [{key}]".replace(' ``', '')
    if rating: return f"{rating}. {cell(shorten(sig.get('summary') or 'No quote: the paper does not say.', 160))} [{key}]"
    return f"{cell(shorten(sig.get('summary') or sig.get('final') or '', 200))} [{key}]"


def tool_status(paper, sig):
    ids = sig.get('tool_checks') or []; prov = {p['id']: p for p in paper.get('provenance', [])}
    st = [prov[i]['status'] for i in ids if i in prov]
    return sig.get('status') if sig.get('status') in TOOL_EMOJI else ('flag' if 'flag' in st else 'ok' if st and all(s == 'ok' for s in st) else 'unavailable' if 'unavailable' in st else None)


def quality_table(paper, printed):
    """## Quality appraisal: Domain, Rating (one glyph), Evidence. Rows follow the older pages; a row with no rating in the export says so."""
    sigs = paper['signals']; keys = []; n = [0]
    def key(sid): n[0] += 1; k = f'S-{n[0]:02d}'; keys.append((k, sid)); return k
    out = ['## Quality appraisal', '',
           '> [!info] Risk-of-bias and validity appraisal. Ratings come from the quality-signals export (model ratings with a quote and its page, scripted checks for code, data and statistics). Each evidence cell ends with a key, such as [S-01], that opens its row under Evidence provenance.',
           '> 🟢 low risk or addressed · 🟡 some concerns or partial · 🔴 high risk or not addressed · ➖ not applicable', '', '| Domain | Rating | Evidence |', '| --- | :---: | --- |']
    for sid, label, q in QA_ROWS:
        s = sigs.get(sid)
        if not s: out.append(f'| **{label}**: {q} | ➖ | Not in the export for this paper. |'); continue
        emoji = RISK_EMOJI.get(s['final']) if s.get('ratings') else TOOL_EMOJI.get(tool_status(paper, s), '➖')
        out.append(f'| **{label}**: {q} | {emoji or "➖"} | {cell(evidence_cell(s, key(sid), printed))} |')
    return '\n'.join(out) + '\n', keys


def item_sort(i):
    m = re.match(r'(\d+)([a-z]?)', i); return (int(m.group(1)), m.group(2))


def tripod_table(paper, printed, start=1):
    sigs = paper['signals']; items = {k[len('tripod-'):]: v for k, v in sigs.items() if k.startswith('tripod-')}; keys = []; n = [start - 1]
    out = ['## TRIPOD-LLM reporting', '', "> [!info] Reporting compliance mapped to the TRIPOD-LLM checklist (items 1 to 18). Item 17 (Performance) is reported per EVD. Each evidence cell ends with a key that opens its row under Evidence provenance.",
           '> ✅ fully reported · ⚠️ partial or unclear · ❌ not reported · ➖ not applicable', '', '| # | Item | ✓ | Evidence |', '| ------- | ------------------------------- | :-----: | --- |']
    for i in sorted(set(items) | set(TRIPOD_FIXED), key=item_sort):
        if i in TRIPOD_FIXED and i not in items: name, em, txt = TRIPOD_FIXED[i]; out.append(f'| **{i}** | {name} | {em} | {txt} |'); continue
        s = items[i]; n[0] += 1; k = f'S-{n[0]:02d}'; keys.append((k, 'tripod-' + i)); name = s['label'].split(': ', 1)[-1]
        out.append(f"| **{i}** | {name} | {TRIPOD_EMOJI.get(s['final'], '➖')} | {cell(evidence_cell(s, k, printed, TRIPOD_WORD))} |")
    return '\n'.join(out) + '\n', keys


def provenance_table(paper, keys, citekey, doc_has_shot=lambda rel: True):
    """Collapsed callout: one row per S-key with the full quote, locator, rater models and confidence, verifier scores, screenshot, and the scripted checks that bear on the row."""
    sigs = paper['signals']; prov = {p['id']: p for p in paper.get('provenance', [])}
    out = ['> [!info]- Evidence provenance (what each key in the two tables above points to)', '>',
           '> | Key | Signal | Rating | Rated by (model, confidence) | Verified by (score 0 to 1) | Locator | Quote or scripted result | Screenshot |', '> | --- | --- | --- | --- | --- | --- | --- | --- |']
    for k, sid in keys:
        s = sigs[sid]; rs = s.get('ratings', []); rated = '; '.join(f"{r['rater']} ({r.get('confidence') or 'n/a'})" for r in rs) or 'script, no model'
        ver = ' · '.join(f"{c['verifier']} {c['score']:.2f}" for c in s.get('checks', []) if c.get('score') is not None) or 'n/a'
        loc = '; '.join(sorted({r.get('locator') for r in rs if r.get('locator')})) or ''
        quote = ' / '.join(f'"{cell(r["quote"])}"' for r in rs if r.get('quote')) or ''
        if not quote:
            t = [prov[i] for i in (s.get('tool_checks') or []) if i in prov]
            quote = cell(s.get('summary') or '') + ((' Checks: ' + '; '.join(f"{p['label']} ({p['status']}, {p['tool']}, {p['checked_utc'][:10]})" for p in t)) if t else '')
        shots = [r['screenshot'] for r in rs if r.get('screenshot')]; shot = ' '.join(f'[[{SHOTS}/{x}|image]]' if doc_has_shot(f'{SHOTS}/{x}') else f'{x} (file missing)' for x in shots) or 'none'
        out.append(f"> | {k} | {s['label'].replace('TRIPOD-LLM ', '')} | {words(s['final']) if rs else 'script result'} | {cell(rated)} | {cell(ver)} | {cell(loc)} | {cell(quote)} | {shot} |")
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ Properties (field order of the older Woelfle source page)
PROPERTY_ORDER = ['dg_type', 'status', 'keywords', 'rating', 'tags', 'doi', 'license', 'license_source', 'oa_status', 'citationCount', 'citationCountSource', 'predatoryPublisherFlag', 'critiqueStatus', 'authors',
                  'authorTrackRecord', 'pubType', 'selfCitationRate', 'selfCitationChecked', 'doajListed', 'pubpeerCommentCount', 'crossNodeChecked', 'crossNodeCorroborated', 'nameConsistency', 'nameConsistencyNote',
                  'apaTitle', 'apaContainer', 'apaYear', 'apaVolume', 'apaArticleNumber', 'apaLandingUrl', 'apaAuthors', 'peerReviewStatus', 'peerReviewNote', 'curatedWithModel', 'curatedWithModelDate', 'citekey', 'nodeTypeId', 'nodeInstanceId']
NA = 'not available'


def _tags(paper):
    import signal_registry as SR
    out = ['dg/source']
    for sid, tag in {**SR.SIGNAL_TAGS}.items():
        s = paper['signals'].get(sid)
        if s and s.get('ratings'): out.append(f"{tag}/{s['final']}")
    return out


def properties_rows(citekey, pic_paper, paper, models, date):
    p = pic_paper; prov = {x['id']: x for x in (paper or {}).get('provenance', [])}
    def res(i): return (prov.get(i) or {}).get('result', '')
    def m(rx, i, g=1):
        mm = re.search(rx, res(i)); return mm.group(g) if mm else None
    cit = m(r'OpenAlex counts (\d+)', 'citations'); selfc = re.search(r'(\d+) of (\d+) references with author data \((\d+)%\)', res('self-citation')); pub = m(r'PubPeer lists (\d+)', 'pubpeer')
    doaj = res('doaj'); peer = res('peer-review-status'); typ = re.search(r'Published as ([\w-]+)', peer)
    auths = [a.strip() for a in str(p.get('authors', '')).split(',') if a.strip()]
    lic = next((re.match(r'(\S+):', x['result']).group(1) for k, x in prov.items() if k.startswith('link-') and 'creativecommons' in x['result']), None)
    rows = {
        'dg_type': ('Source', 'template'), 'status': ('test, not validated', 'write_src.py'), 'keywords': (NA, 'not extracted by the pipeline yet'), 'rating': ('not rated', 'set by JP after review'),
        'tags': (', '.join(_tags(paper)) if paper else NA, 'quality-signals export (signal tag plus rating)'), 'doi': (p.get('doi') or NA, 'extraction (picost)'),
        'license': (lic or NA, 'link check in the provenance store'), 'license_source': ('provenance link check' if lic else NA, ''), 'oa_status': (NA, 'needs the open-access lookup (oa_lookup.py)'),
        'citationCount': (cit or NA, 'OpenAlex, provenance store'), 'citationCountSource': ('OpenAlex' if cit else NA, ''), 'predatoryPublisherFlag': (NA, 'not checked'), 'critiqueStatus': (NA, 'not checked'),
        'authors': ('; '.join(auths) or NA, 'extraction (picost)'), 'authorTrackRecord': (res('author-track-record') or NA, 'OpenAlex, provenance store'), 'pubType': (typ.group(1) if typ else NA, 'provenance store'),
        'selfCitationRate': (f'{int(selfc.group(1)) / int(selfc.group(2)):.3f}' if selfc else NA, 'provenance store'), 'selfCitationChecked': (f'{selfc.group(1)} of {selfc.group(2)} references had author metadata sharing an author' if selfc else NA, 'provenance store'),
        'doajListed': (('no' if 'not listed' in doaj else 'yes') if doaj else NA, 'DOAJ, provenance store'), 'pubpeerCommentCount': (pub or NA, 'PubPeer, provenance store'),
        'crossNodeChecked': (NA, 'needs the cross-node check'), 'crossNodeCorroborated': (NA, 'needs the cross-node check'), 'nameConsistency': (NA, 'not checked'), 'nameConsistencyNote': (NA, ''),
        'apaTitle': (p.get('title') or NA, 'extraction (picost)'), 'apaContainer': (p.get('venue') or NA, 'extraction (picost)'), 'apaYear': (p.get('year') or NA, 'extraction (picost)'),
        'apaVolume': (NA, 'needs the Crossref record'), 'apaArticleNumber': (NA, 'needs the Crossref record'), 'apaLandingUrl': (f"https://doi.org/{p['doi']}" if p.get('doi') else NA, 'built from the DOI'),
        'apaAuthors': ('; '.join(auths) or NA, 'extraction (picost)'), 'peerReviewStatus': ('peer-reviewed' if typ and typ.group(1) == 'journal-article' else NA, 'provenance store'), 'peerReviewNote': (peer or NA, 'provenance store'),
        'curatedWithModel': (models, 'call log of the run'), 'curatedWithModelDate': (date, 'call log of the run'), 'citekey': (citekey, 'vault'),
        'nodeTypeId': ('assigned when the page is written to the vault', ''), 'nodeInstanceId': ('assigned when the page is written to the vault', '')}
    return [(k, *rows[k]) for k in PROPERTY_ORDER]


def properties_table(rows):
    out = ['> [!info]- Properties', '>', '> | Property | Value | Source |', '> | --- | --- | --- |']
    out += [f'> | `{k}` | {cell(v)} | {cell(src)} |' for k, v, src in rows]
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ AI use (GAMER key elements)
STEP = {
    'picost': ('extracted findings from the PDF', 'quotes located by script; second read'),
    'recheck': ('second read of the findings', 'compared with the first read by script'),
    'adjudicate': ('settled read disagreements', 'person spot-checks'),
    'checks_vision': ('looked at finding crops', 'disputes to another model'),
    'checks_opus': ('settled crop disputes', 'person spot-checks'),
    'draft_r0': ('drafted nodes', 'writing-rules script; detail check by another model'),
    'draft_r1': ('revised nodes', 'same checks'), 'draft_vote': ('voted between drafts', 'same checks'), 'draft_tie': ('settled a split vote', 'same checks'),
    'draft_check': ('checked node details', 'flagged nodes go to a person'), 'draft_rework': ('fixed low-scoring EVDs', 'decision models rescore'),
    'qs': ('rated quality signals and TRIPOD items', 'quote found in PDF by script; verifier models score it'),
    'qs_adjudicate': ('settled rating disagreements', 'person reviews'),
    'quote_check': ('read quote screenshots', 'compared with quote text by script'),
    'src_write': ('wrote this page', 'script checks numbers, quotes, links, tables; Neon judges Findings'),
    'src_judge': ('judged Findings bullets', 'verdicts are audit flags for a person'),
}
PAGE_TASK = {'src_write': 'wrote the prose', 'src_judge': 'judged the Findings bullets', 'qs': 'rated the two tables', 'qs_adjudicate': 'rated the two tables'}


def ai_use_table(calls, human, extra_note=''):
    """One row per model: its task on this page and in the pipeline, version and date, prompt ids, effort, human oversight and how its output was verified. Key elements of the GAMER checklist
    (tool and version, purpose, prompts, who reviewed, how verified; the nine items are answered for the project in pipeline/provenance/AI-disclosure.md)."""
    by = {}
    for c in calls: by.setdefault(c['model_id'], []).append(c)
    rows = []
    for mid, cs in by.items():
        steps = list(dict.fromkeys(c['step'] for c in cs)); dates = sorted({c['ts_utc'][:10] for c in cs}); eff = ', '.join(sorted({str(c.get('effort')) for c in cs if c.get('effort')})) or 'n/a'
        prompts = ', '.join(sorted({Path(c['prompt_file']).stem for c in cs if c.get('prompt_file')})) or 'n/a'
        here = '; '.join(dict.fromkeys(PAGE_TASK[s] for s in steps if s in PAGE_TASK)) or 'made the nodes this page links to'
        pipe = ', '.join(dict.fromkeys(STEP[s][0] for s in steps if s in STEP)) or 'n/a'; ver = '; '.join(dict.fromkeys(STEP[s][1] for s in steps if s in STEP)) or 'n/a'
        rows.append((cs[0]['model'], here, pipe, f"`{mid}`, {dates[0] if len(dates) == 1 else dates[0] + ' to ' + dates[-1]}", prompts, eff, human, ver))
    rows.append(('Scripts (no model)', 'built the tables from data; cut the crops from the PDF', 'checks',
                 '`write_src.py`, `src_sections.py`, `src_crops.py`', 'n/a', 'n/a', human, 'tests in selftest.py; checks listed in the audit'))
    models = ', '.join(dict.fromkeys(r[0] for r in rows[:-1])); when = sorted({c['ts_utc'][:10] for c in calls})
    out = [f"> [!info]- AI use: {models} · {when[0] if when else ''} · {human}", '>',
           '> | Model | Task on this page | Task in the pipeline | Version and date (UTC) | Prompt ids | Effort | Human oversight | Verification |', '> | --- | --- | --- | --- | --- | --- | --- | --- |']
    out += [f'> | {" | ".join(cell(x) for x in r)} |' for r in rows]
    out += ['>', f"> Key elements of the GAMER checklist (tool and version, purpose, prompts, who reviewed, how verified). The nine GAMER items for the project are answered in [[pipeline/provenance/AI-disclosure|full AI disclosure (GAMER)]]; the unedited responses are in `pipeline/runs/<run>/responses/`.{extra_note}"]
    return '\n'.join(out) + '\n', models, (when[0] if when else '')

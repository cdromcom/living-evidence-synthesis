#!/usr/bin/env python3
"""Rows of the ABOUT tab for the review workbook: the pipeline step by step (1a, 1b, ...), each with a bold goal phrase, the explanation, and a real example from the run
(JP, 2026-11-27). run_to_gsheet.py calls steps(d, M); each row is (id, bold goal phrase, explanation, example text, example image path). No model calls; the examples are read from the run folder."""
import json, re
from pathlib import Path
import config as C, column_notes as CN


def _j(p):
    p = Path(p); return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None


def _ex(d, M):
    """Pick one paper and finding per example from the run's own files. A missing file or key leaves that example empty."""
    ex = {}; P = M['papers']
    def safe(name, fn):
        try: ex[name] = fn()
        except Exception: ex[name] = None
    A = next((k for k in P if all((d / k / f).exists() for f in ('picost.json', 'checks.json', 'drafts.json', 'quality_signals.json'))), None)
    if not A: return ex
    short = lambda k: k.split('-et-al')[0] + ' et al. ' + (re.search(r'(20\d\d)', k) or [None, ''])[1]
    ps = {f['id']: f for f in _j(d / A / 'picost.json')['findings']}
    F = next((f for f in ps.values() if f.get('tier') == 'primary' and f.get('spans') and (d / A / 'highlights' / f"{f['id']}_s1_p{f['spans'][0].get('pdf_page')}.png").exists()), None)
    if not F: return ex
    fid = F['id']; sp = F['spans'][0]; who = f"{short(A)}, finding {fid}"
    ex['A'] = A; ex['F'] = F
    ex['who'] = who
    pf = P[A]['preflight']
    safe('1a', lambda: f"{short(A)}: {pf['pages']} pages, text layer {'present' if pf.get('text_layer') else 'absent'}, {pf.get('size_mb')} MB, about {pf.get('chars_per_page')} characters per page; printed page numbers taken from the PDF {'page labels' if pf.get('printed_page_source') == 'label' else 'page offset' if pf.get('printed_page_source') == 'offset' else 'page map'}.")
    safe('1b', lambda: f"{who} ({F['tier']}): {F['statement']}\nWhy this tier: {F.get('tier_reason', '')}")
    safe('1c', lambda: f"{who}\nPopulation: {F.get('P', '')}\nIntervention: {F.get('I', '')}\nComparator: {F.get('C', '')}\nOutcome: {F.get('O', '')}\nStudy design: {F.get('S', '')}\nTimeframe: {F.get('T', '')}\nFirst number: {F['numbers'][0].get('label')} = {F['numbers'][0].get('value')} {F['numbers'][0].get('unit', '')} (PDF page {F['numbers'][0].get('pdf_page')}, {F['numbers'][0].get('table_or_figure')}, row {F['numbers'][0].get('row')}, column {F['numbers'][0].get('column')}).")
    ex['2a_img'] = d / A / 'highlights' / f"{fid}_s1_p{sp.get('pdf_page')}.png"
    safe('2a', lambda: f"{who}, quote 1 (verbatim): \"{sp['text']}\"\nFound on PDF page {sp.get('pdf_page')} (printed page {sp.get('printed_page')}); {len(sp.get('bbox', []))} word boxes drawn. Image below: the highlighted page.")
    def two_b():
        for k in P:
            pj = _j(d / k / 'picost.json')
            for f in (pj or {}).get('findings', []):
                if 'number_not_in_pdf_text' in f.get('flags', []) or 'number_not_in_numbers_list' in f.get('flags', []):
                    return f"{short(k)}, finding {f['id']}: flags {', '.join(f['flags'])}. Statement: {f['statement'][:230]}"
    safe('2b', two_b)
    def two_c():
        for k in P:
            fl = P[k].get('flagged') or []
            if not fl: continue
            pj = {f['id']: f for f in _j(d / k / 'picost.json')['findings']}
            fx = next((pj[i] for i in fl if len(pj[i].get('flags', [])) > 1), pj[fl[0]])
            return f"{short(k)}, finding {fx['id']}: flags {', '.join(fx.get('flags', []))}. {len(fl)} of {len(pj)} findings of this paper were sent to the recheck."
    safe('2c', two_c)
    qc = _j(d / 'stage_quote_check.json') or {}
    ex['3a_img'] = d / A / 'quote_crops' / f"{fid}_s1.png"
    def three_a():
        r = qc.get(f"{A}__qc__{fid}__1"); v = json.loads(r['text']); return f"{who}, quote 1. The printed text on the screenshot: \"{v['printed']}\"\nSol's answer: the quote equals the print = {v['a_equals_print']}; differences listed: {v['a_differences'] or 'none'}; changes the meaning = {v['a_changes_meaning']}. Image below: the screenshot Sol read."
    safe('3a', three_a)
    def three_b():
        mc = M['stage_log']['quote_check'].get('meaning_changed') or []
        x = mc[0]; return f"{x[0]} et al., finding {x[1]}, quote {x[2]}: Sol listed these differences from the print: {x[3]}. This marks the finding for the recheck. (Run summary: {M['stage_log']['quote_check']['summary']['checked']} quotes read, {M['stage_log']['quote_check']['summary']['equals print']} equal to the print, {M['stage_log']['quote_check']['summary']['meaning changed']} with a changed meaning.)"
    safe('3b', three_b)
    def recheck():
        for k in P:
            dis = P[k].get('disagreements') or []; adj = {x['id']: x for x in (P[k].get('adjudication') or {}).get('adjudications', [])}
            rc = {x['id']: x for x in (P[k].get('recheck') or {}).get('findings', [])}; pj = {f['id']: f for f in _j(d / k / 'picost.json')['findings']}
            for i in dis:
                if i in adj and i in rc: return k, i, pj[i], rc[i], adj[i]
    r_ = recheck(); ex['rc'] = r_
    if r_:
        k, i, f, rc, a = r_; nm = lambda L: '; '.join(str(n.get('value')) for n in L.get('numbers', [])[:4])
        ex['4a'] = f"{short(k)}, finding {i}, first four numbers.\nNeon: {nm(f)}\nSol (blind): {nm(rc)}"
        ex['4b'] = f"{short(k)}, finding {i}: the two lists of numbers differ, so the finding is marked 'different' in the Rechecks tab. In {short(k)}, {len(P[k].get('disagreements') or [])} of {len(P[k].get('flagged') or [])} rechecked findings differ."
        fld = (a.get('fields') or [{}])[0]
        ex['4c'] = f"{short(k)}, finding {i}: verdict {a['verdict']} (A = Neon, B = Sol). First field: Neon wrote {fld.get('a')}, Sol wrote {fld.get('b')}; the PDF says {fld.get('correct')} (page {fld.get('pdf_page')}, {fld.get('table_or_figure')}, row {fld.get('row')}). Reason: {a.get('reason', '')[:330]}"
    ex['5a_img'] = d / A / 'crops' / f"{fid}.png"
    ch = {v['id']: v for v in _j(d / A / 'checks.json')}; cf = ch.get(fid)
    def five_b():
        q = lambda m: ', '.join(f"{a} {b:.2f}" for a, b in m.items() if not a.startswith('_'))
        dm = cf['dm']; names = {'perplexity': 'Perplexity Decider 1.3', 'liquid': CN.LQ, 'baseten': 'Baseten bison-1'}
        return f"{who}\n" + '\n'.join(f"{names.get(k, k)}: {q(v)}" for k, v in dm.items()) + f"\nMean per question: {q(cf['summary']['means'])}\nScore (lowest mean) {cf['summary']['score']}, spread between models {cf['summary']['spread']}."
    safe('5b', five_b)
    safe('5a', lambda: f"{who}: a crop of the page showing the highlighted quote and the text around it (image below). Sol and the decision models read this crop.")
    safe('5c', lambda: f"{who}: Sol says {cf['sol']['overall']}. Whole quote visible: {cf['sol']['whole_quote']}; quote matches: {cf['sol']['quote_matches']}; numbers match: {cf['sol']['numbers_match']}; direction right: {cf['sol']['direction_right']}. Reason: {cf['sol']['reason'][:260]}")
    def five_cv():
        for k in P:
            for v in (_j(d / k / 'checks.json') or []):
                if (v.get('sol') or {}).get('overall') == 'cannot_verify': return f"{short(k)}, finding {v['id']}: Sol answered cannot verify. Reason: {v['sol']['reason']} The finding goes to you; its final result in the sheet is '{v.get('final')}'."
    safe('5d', five_cv)
    def five_e():
        for k in P:
            for v in (_j(d / k / 'checks.json') or []):
                if v.get('dispute'): return f"{short(k)}, finding {v['id']}: a dispute was opened ({'; '.join(v.get('why_vision', []))[:120] or 'see the Checks tab'}). Sol said {v['sol']['overall']}; {CN.VD} said {(v.get('opus') or {}).get('overall')}; final result {v.get('final')}."
    safe('5e', five_e)
    dd = _j(d / A / 'drafts.json')['finals']; nid = 'E-' + fid; nd = dd.get(nid)
    safe('6a', lambda: f"{who}, EVD node {nid} (author {nd['author']}; {nd['how']}): {nd['node']['statement']}")
    def six_b():
        w = nd['writing_rules']; return f"{nid}: {w['chars']} characters (limit 247, length ok = {w['length_ok']}); parentheses ok = {w['parentheses_ok']}; capital-letter words ok = {w['caps_ok']}; numbers in the statement that are not on the finding's card: {', '.join(w['numbers_not_on_card']) or 'none'}; overall pass = {w['pass']}."
    safe('6b', six_b)
    def six_c():
        c = nd['detail_check']; return f"{nid}, checked by {c['checker'].capitalize()} (own draft = {c['own_draft']}); overall {c.get('overall')}.\nDetail 1: \"{c['details'][0]['detail']}\" = {c['details'][0]['verdict']}, from the PDF words \"{c['details'][0]['words'][:120]}\"\nDetail 2: \"{c['details'][1]['detail']}\" = {c['details'][1]['verdict']}"
    safe('6c', six_c)
    def six_d():
        for k in P:
            for n_, f in ((_j(d / k / 'drafts.json') or {}).get('finals') or {}).items():
                rw = f.get('rework')
                if rw: return f"{short(k)}, {n_}: decision-model score {rw['dm_before']['score']:.3f} before, {rw['dm_after']['score']:.3f} after. Verdict {rw['verdict']}; accepted = {rw.get('accepted')}.\nBefore: {rw['original']}\nAfter: {rw.get('proposal', '')}"
    safe('6d', six_d)
    q = _j(d / A / 'quality_signals.json'); raw = [r for r in q['raw'] if r.get('crop') and r.get('quote_found')]
    r0 = next((r for r in raw if r['rater'] == 'neon' and r['signal'] == 'construct-validity'), raw[0] if raw else None)
    if r0:
        ex['7a_img'] = r0['crop']
        ex['7a'] = f"{short(A)}, signal {r0['signal']}: {r0['rater'].capitalize()} rated '{r0['rating']}' (confidence {r0.get('confidence')}) at {r0['locator']}.\nQuote: \"{r0['quote'][:260]}\" Image below: the highlighted quote."
        ex['7b'] = f"{short(A)}, signal {r0['signal']}: the quote was located in the PDF = {r0['quote_found']}, source '{r0.get('quote_source')}' (the model gives the first and last words, code copies the exact text from the PDF); PDF page {r0.get('pdf_page')}."
    def seven_c():
        for a in q['aggregate']:
            if a['status'] == 'fallback':
                rs = {r['rater']: r for r in q['raw'] if r['signal'] == a['signal']}
                return f"{short(A)}, signal {a['signal']}: Neon rated '{rs['neon']['rating']}' with confidence {rs['neon'].get('confidence')}; Sol then rated blind '{rs['sol']['rating']}' with confidence {rs['sol'].get('confidence')}. Status: {a['agreement']}."
    safe('7c', seven_c)
    def seven_d():
        for k in P:
            qq = _j(d / k / 'quality_signals.json')
            for a in (qq or {}).get('aggregate', []):
                if a['status'] == 'needs_human':
                    rs = [r for r in qq['raw'] if r['signal'] == a['signal']]; return f"{short(k)}, signal {a['signal']}: " + '; '.join(f"{r['rater'].capitalize()} '{r['rating']}', confidence {r.get('confidence')}" for r in rs) + f". Status: {a['agreement']}."
    safe('7d', seven_d)
    def seven_e():
        from qs_export import STORE
        st = json.loads(Path(STORE).read_text(encoding='utf-8'))['papers']
        for k in P:
            ck = ((M['stage_log'].get('qs_code_checks') or {}).get('papers') or {}).get(k)
            if not ck: continue
            it = {i['id']: i for i in st[ck['citekey']]['provenance']}; fl = next(i for i in it.values() if i['status'] == 'flag')
            return f"{short(k)}: {ck['items']} checks. Retraction check ({it['retraction']['tool']}, {it['retraction']['status']}): {it['retraction']['result']}\nA flagged check ({fl['id']}, {fl['tool']}): {fl['result'][:240]}"
    safe('7e', seven_e)
    V = _j(d / 'verification.json') or []
    import collections; cnt = collections.Counter(x['ntype'] for x in V)
    safe('8a', lambda: f"This run: {len(V)} items: " + ', '.join(f"{n} {t}" for t, n in cnt.most_common()) + '. Types: PICOST = one slot of a finding, QUOTE = a quote against the printed text, QUALITY = a quality rating, QUE, CLM and CVT = drafted question rewording, claim and caveat.')
    def eight_b():
        for x in V:
            if x['paper'] == A and x['ntype'] == 'PICOST' and x.get('sonnet_called'):
                s = x['scores']; return f"{short(A)}, {x['nid']} (\"{x['text'][:90]}\"): Perplexity {s.get('perplexity', 0):.2f}, {CN.LQ} {s.get('liquid', 0):.2f}" + (f", Baseten bison-1 {x['shadow_bison']:.2f} (scored beside the vote in this run)" if x.get('shadow_bison') is not None else '') + (f", {CN.LQ} on the screenshot {s['liquid_image']:.2f}" if s.get('liquid_image') is not None else '') + '.'
    safe('8b', eight_b)
    import lives_verify as LV
    jx = next((x for x in V if x['paper'] == A and x['ntype'] in ('CLM', 'CVT') and x.get('sonnet_called') and LV.human_flag(x)), None)
    if jx:
        s = jx['scores']
        ex['8c'] = f"{short(A)}, {jx['ntype']} {jx['nid']}: \"{jx['text'][:150]}\"\nDecision models: Perplexity {s['perplexity']:.2f}, {CN.LQ} {s['liquid']:.2f}. The judge ({jx['judge']}) scored {s['sonnet']:g}: {jx['reasons'].get('sonnet', '')[:230]}"
        ex['8e'] = f"{short(A)}, {jx['ntype']} {jx['nid']}: {LV.human_flag(jx)}. Result in the sheet: {jx['majority'].replace('fail', 'not supported')}."
    def eight_d():
        N = _j(d / 'numbers_check.json'); x = N['flagged'][0]; return f"{short(x['paper'])}, finding {x['id']}: of {len(x['numbers'])} numbers, {', '.join(x['not_on_cited_pages'])} was not in the text of the cited page ({', '.join(map(str, x['pages']))}). The scan of the page screenshots for this digit string found it: {', '.join(x['result'])} (match score {x['found'][0]:.2f} against a control of {x['control'][0]:.3f}). Run total: {N['checked_findings']} findings checked, {len(N['flagged'])} had a number missing from the page text."
    safe('8d', eight_d)
    def img8d():
        N = _j(d / 'numbers_check.json'); x = N['flagged'][0]; return x['images'][0]
    safe('8d_img', img8d)
    ex['8d_img'] = ex.get('8d_img')
    src = Path(C.VAULT) / 'pipeline/misc/src-test-2026-11-27'
    def src_a():
        a = next(src.glob('*.audit.json')); j = json.loads(a.read_text(encoding='utf-8')); ex['_src'] = j
        return f"Test page for {short(A)}, from run {j['run_id']} (this run has no SRC page yet): written by {j['model']['display']} ({j['model']['mode']} mode, prompt {j['prompt']['id']}), status '{j['status']}'. The page has {j['summary']['summary_words']} summary words and {j['summary']['embeds'].get('resolved', 0)} embedded figures."
    safe('9a', src_a)
    if ex.get('_src'):
        s = ex['_src']['summary']; fl = ex['_src']['flags_for_human_examination']
        ex['9b'] = f"Same test page: {s['numbers']['found_in_paper']} numbers found in the paper, {s['quotes']['located']} quotes located, {s['quote_page_mismatch']} quote with a wrong page, {s['cited_numbers']['ok']} cited numbers on the cited page, {s['cited_numbers']['not_on_cited_page']} not on the cited page, {s['cited_numbers']['uncited']} without a citation; writing rules pass = {s['writing_rules_pass']}."
        ex['9c'] = f"Same test page: Neon judges each Findings bullet against its EVD node and the extraction. Verdicts saved in this test file: {len(ex['_src']['judge'].get('verdicts', {}))} (the judge batch was not yet run for it)."
        ex['9d'] = f"Same test page: {s['flags_for_human_examination']} flags. First: {fl[0]['kind']}: {fl[0]['what']}"
    return ex


def steps(d, M):
    RR = C.ROLES; D = C.role_display; ex = _ex(d, M); g = lambda k: ex.get(k) or ''; I = lambda k: ex.get(k) or None
    many = lambda lst: ' and '.join(D(a) for a in lst)
    cascade = len(RR['raters']) == 1 and RR.get('qs_fallback') and not C.PIPE.get('quality_signals', {}).get('max_accuracy')
    draft_txt = (f"critique and revision by {many(RR.get('critics') or RR['authors'])}; votes between the versions by {many(RR['voters'])}, with {D(RR['tiebreak'])} breaking a tie" if RR.get('voters') else "no critique round, vote or tie-break; the first draft is final")
    S = []
    def add(k, lead, rest, t='', im=None): S.append((k, lead, rest, t, im))
    add('1', 'Step 1: read each paper and extract its questions and findings.', f"{D(RR['extract'])} does the reading (stage picost). The substeps below follow the order in which the pipeline runs.")
    add('1a', 'Check each PDF before any model reads it.', "The pipeline counts pages, checks that the PDF has a text layer (a scanned PDF has none and is flagged no_text_layer), reads the page labels so that a PDF page can be turned into the printed journal page, and joins supplements if there are any.", g('1a'))
    add('1b', "Extract the paper's questions and its findings in three tiers.", f"{D(RR['extract'])} reads the PDF and lists the questions (from the Abstract and Introduction) and the findings. Primary: answers a question directly. Secondary: qualifies a primary finding. Tertiary: other context. Each finding gets a one-sentence statement and a reason for its tier.", g('1b'))
    add('1c', 'Fill the PICOST slots and list every number with its location.', "For each finding the model writes Population, Intervention, Comparator, Outcome, Study design and Timeframe, lists each number with its page, table or figure, row and column, and copies the quoted spans (the exact words that support the finding).", g('1c'))
    add('2', 'Step 2: check the quotes and numbers with code only.', 'No model is used in this step. PyMuPDF finds every quoted span in the PDF text, boxes it and checks the numbers. Findings that look doubtful are flagged.')
    add('2a', 'Find each quoted span in the PDF and draw its highlight.', "PyMuPDF searches the PDF text for each quote, records the page where it was found (found, or span_not_found / span_on_other_page if it was not where the model said), and draws a box around each word.", g('2a'), I('2a_img') and (ex['2a_img'], 500))
    add('2b', 'Repair page numbers and find gaps in the numbers list.', "Code corrects the model's mistakes instead of flagging them: a quote that is not in the PDF text is replaced by the PDF's own words when at least 90% of its letters and digits match one stretch of one page; every quote gets the page where it was found, and every page gets its printed number from the page map; a number that is not on its cited page moves to the page that has it. Then it compares the numbers of each statement with the Numbers list and flags number_not_in_pdf_text (fewer than half of its numbers are in the PDF text), number_not_in_numbers_list and numbers_list_entry_without_location.", g('2b'))
    add('2c', 'Flag the findings that need a second look.', "A finding is sent to the recheck when it has a flag: multi_page (its quotes are on more than one page), span_not_found, number_not_in_pdf_text, number_not_in_numbers_list, numbers_list_entry_without_location, no_text_layer, medium_confidence (only when that option is on) or quote_differs_from_print (step 3b). All flags are listed in the Flags row below.", g('2c'))
    add('3', 'Step 3: read every quote on its screenshot (quote_check stage).', f"{CN.QCD} reads a screenshot of each quote and compares it with the quote text.")
    add('3a', 'Compare each quote with its printed text on the screenshot.', f"Sol is shown the screenshot with the quote highlighted, TEXT A (the quote as the extraction model wrote it) and TEXT B (the PDF text layer at that spot, which can lose superscripts and symbols). It transcribes the highlighted print, then lists every difference of A and of B from the print and says whether a difference changes the meaning. This step runs for every quote that was found in the PDF.", g('3a'), I('3a_img') and (ex['3a_img'], 440))
    add('3b', 'Flag a finding whose quote differs in meaning from the print.', "A quote whose differences change the meaning marks its finding for the recheck (flag quote_differs_from_print). A small typographic difference does not.", g('3b'))
    add('4', 'Step 4: read the flagged findings a second time and settle disagreements.', f"{D(RR['recheck'])} re-reads flagged findings blind, and {D(RR['adjudicate'])} decides when {C.short(RR['recheck'])} and {C.short(RR['extract'])} disagree. The Rechecks tab shows both lists.")
    add('4a', 'Extract the flagged findings again, without seeing the first extraction.', f"{D(RR['recheck'])} reads the PDF and writes its own version of each flagged finding (statement, PICOST, numbers with locations).", g('4a'))
    add('4b', 'Compare the two versions by code.', "Code compares the numbers of the two versions (the function conflict() in lives_run.py). Findings where they conflict are marked 'different' in the Rechecks tab; the others 'agrees'.", g('4b'))
    add('4c', 'Decide each disagreement against the PDF.', f"{D(RR['adjudicate'])} sees both versions (as A and B) and the PDF. For each field it gives the right value with the page, table, row and column, and a verdict: A, B, or neither.", g('4c'))
    add('5', 'Step 5: check every finding against its crop and score it with three decision models (checks stage).', f"Three decision models, Perplexity Decider 1.3 (pplx-decider-v1.3, text only), {CN.LQ} (reads text and images) and Baseten bison-1 (text only), score every finding on relevancy, fidelity, numbers found in the source and table cell matches. {D(RR['vision_check'])} looks at a crop of every finding: pass, not matched or cannot verify (cannot verify goes to you).")
    add('5a', 'Make a crop of the page region around each finding.', "Code cuts the highlighted quote and the text around it from the page (and merges the two pages when the evidence crosses a page break). The Findings tab shows the same crop.", g('5a'), I('5a_img') and (ex['5a_img'], 440))
    add('5b', 'Score each finding on four questions with the three decision models.', "Each model answers: is the finding relevant to the question, is the statement faithful to the quote, are its numbers in the source, do the table cells match. The score of a finding is its lowest question mean; the spread is the gap between models.", g('5b'))
    add('5c', 'Let Sol look at the crop and say whether the finding is right.', f"{D(RR['vision_check'])} sees the crop and answers: whole quote visible, quote matches, numbers match, direction right, then pass, not matched or cannot verify.", g('5c'))
    add('5d', 'Send the findings Sol cannot verify to you.', "Cannot verify means the crop does not show enough (a cut-off table, missing column headers). These findings are marked in the Checks tab for you to look at; the model does not guess.", g('5d'))
    add('5e', 'Settle a dispute between the decision models and Sol.', f"When Sol says pass and the decision-model checks do not, or the reverse, that is a dispute; {D(RR['vision_dispute'])} looks at the same crop and gives a second opinion; the result column shows the outcome.", g('5e'))
    add('6', 'Step 6: draft the graph nodes (draft stage).', f"First draft of each primary EVD by {many(RR['authors'])}; {draft_txt}. Everything else (QUE, CLM, CVT and the other tiers) is drafted once by {D(RR['authors'][0])}.")
    add('6a', 'Write the first draft of each EVD, QUE, CLM and CVT.', f"{many(RR['authors'])} writes the statement from the finding's card (statement, PICOST, numbers, quotes). The Drafts tab shows the winning text.", g('6a'))
    add('6b', 'Check each draft against the writing rules by code.', "Code checks length (at most 247 characters), one or two parentheses and no brackets, no all-capital words, no em dash, a link to its question, and that each number in the statement is on the finding's card.", g('6b'))
    add('6c', 'Check each detail of the draft against the PDF words.', f"{many(RR.get('node_check') or RR['authors'])} splits each EVD, CLM and CVT into its details and marks each as supported or not by the PDF words it quotes (a model that did not write the node when there is a choice).", g('6c'))
    add('6d', 'Correct an EVD whose decision-model score is below 0.60.', f"The three decision models score the drafted EVD. If the score is below 0.60, {D(RR['evd_rework'])} lists each number's source, proposes a correction and lists the exact changes; the models score the result again and the rewrite is used only if it reproduces from the listed changes.", g('6d'))
    add('7', 'Step 7: rate quality signals and TRIPOD-LLM items (qs stage).', ("Quality signals and TRIPOD-LLM rows: " + f"{many(RR['raters'])} ({C.role_effort(RR['raters'][0], 'high')} effort) rates every row and reports its confidence; a rating with low confidence is rated again, blind, by {D(RR['qs_fallback'])} ({C.role_effort(RR['qs_fallback'], 'high')} effort); if that rating is also low confidence the row is marked needs_human for you. (Procedure chosen by JP on 2026-11-27, pending validation.)" if cascade else f"Quality signals: {many(RR['raters'])} rate every row at {C.role_effort(RR['raters'][0], 'high')} effort and " + ('two of three decide.' if len(RR['raters']) >= 3 else 'a third model decides the disagreements.')))
    add('7a', 'Rate each quality signal with a quote and a confidence.', f"{many(RR['raters'])} reads the paper and gives, for each signal, a rating, a confidence (high, medium, low), the first and last words of a supporting quote and where it is.", g('7a'), I('7a_img') and (ex['7a_img'], 440))
    add('7b', 'Locate each quote in the PDF by code.', "Code finds the first and last words in the PDF, copies the exact text between them, and records the page. A quote that cannot be found is shown as NO in the Quote found column.", g('7b'))
    add('7c', 'Rate again, blind, the rows with low confidence.', f"{D(RR['qs_fallback'])} rates the rows that the first rater marked low confidence, without seeing the first rating; the sheet shows both.", g('7c'))
    add('7d', 'Mark the rows where both raters have low confidence for you.', "If the second rating also has low confidence or no valid answer, the row is marked needs_human and you decide.", g('7d'))
    add('7e', 'Run the checks that need no model (qs_code_checks).', "Code-only checks with a date and source each: retraction (OpenAlex, Crossref), authors' track record, self-citation, retracted references, open-access listing (DOAJ), citation counts, PubPeer comments, peer-review status, every link and DOI in the PDF (live link check plus Internet Archive), code and data repositories, FAIR scores, registration, funding and affiliations, and scripted statistical checks.", g('7e'))
    add('8', 'Step 8: verify with a cascade of models and code (verify stage).', f"Perplexity Decider 1.3, {CN.LQ} and Baseten bison-1 first judge every PICOST slot (with page 1 and the Methods pages), question rewording (QUE), claim (CLM), caveat (CVT) and quality rating; {CN.JD} judges an item unless all three agree (it is not the extraction model, {D(RR['extract'])}); {CN.QCD} reads the screenshot of every quote (quote check); {CN.LQ} also looks for the digits of each quote and for statement numbers missing from the PDF text on the screenshots. Quotes without digits are checked by {CN.QCD}. The tabs Verification, Numbers check and Revisions to note show the results.")
    add('8a', 'Build the list of items to verify.', "Every PICOST slot, quote, question rewording, claim, caveat and quality rating becomes one item with its text and the crop or passages it rests on.", g('8a'))
    add('8b', 'Score each item with the three decision models.', f"Perplexity Decider 1.3 and Baseten bison-1 read text only; {CN.LQ} reads text and up to 8 images and compares the digits of each quote with the screenshot. A score is 0 to 1; below 0.5 counts as not supported.", g('8b'))
    add('8c', 'Ask the judge only when the decision models do not all agree.', f"{CN.JD} judges an item unless all three decision models agree; it does not judge the work of its own model (items by Neon go to Sol, items by Sol go to Neon, and a quality rating goes to the one of the two that did not rate it). It gives a score and a one-sentence reason.", g('8c'))
    add('8d', 'Search the screenshots for numbers that are not in the PDF text.', "For each finding, any number of the statement that is not in the text of the cited pages is searched for on the screenshots of those pages (a scanned or image table has no text layer). A control string is scored for comparison. Results are in the Numbers check tab.", g('8d'), I('8d_img') and (ex['8d_img'], 440))
    add('8e', 'Mark the items that need a human look.', "An item gets a human-examination flag when the judge scored it below 0.75 or gave no answer, when a decision model scored it below 0.5 and the judge did not pass it, or when the judge and the majority of the decision models disagree. Items are queued: claims first, then caveats, then a 25% random sample of quality ratings, then question rewordings.", g('8e'))
    add('9', 'Step 9: write the SRC page of the paper and check it (write_src.py).', f"The SRC (source) page is written by {D(RR['src_writer'])} from the run's findings, drafted nodes and PDF text, in batch mode, then checked. Nothing is written to the vault until you validate it.")
    add('9a', 'Write the SRC page.', f"{D(RR['src_writer'])} writes the summary, the Findings bullets (each linked to its EVD node) and the tables from the run's own files.", g('9a'))
    add('9b', 'Check the page by code.', "Writing rules, every number of the page found in the paper, every quote located (and on the page cited), links to nodes resolve, embeds resolve, tables compared with the table parsers, and summary length.", g('9b'))
    add('9c', 'Judge each Findings bullet against its EVD node.', f"{D(RR['src_judge'])} reads each bullet with its EVD node and the extraction and says whether the bullet is supported.", g('9c'))
    add('9d', 'List what a person should examine.', "Every check that did not pass becomes a flag for human examination in the audit file for the page (for example a sentence with a number but no table, figure or page citation).", g('9d'))
    add('10', 'Step 10: you review the sheet.', 'You review this sheet. Your labels become the ground truth for the accuracy numbers.')
    add('10a', 'Label the Findings and Quote checks tabs.', "Say whether the tier, statement and numbers of each finding are right, whether each quote is correct, and add findings that were missed.")
    add('10b', 'Look at the items the cascade marked for you.', "Open the Verification tab (queue order, flags) and the Numbers check tab; the cannot-verify findings and needs_human quality ratings are for you.")
    return S

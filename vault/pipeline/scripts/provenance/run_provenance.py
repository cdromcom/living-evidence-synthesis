#!/usr/bin/env python3
"""Run every provenance check that applies to one paper and print a short summary. With --write, merge the items into
pipeline/provenance/provenance-quality-signals.json (see store.py).
  python3 run_provenance.py --pdf PATH --citekey KEY [--doi DOI] [--title TITLE] [--vendors "OpenAI,Anthropic,Google"] [--write]
Another program can call collect(pdf_path, citekey, doi=None, title=None, vendors=()) and gets the list of items back."""
import argparse, re, sys, time, unicodedata
from pathlib import Path
import _http, store, link_check, openalex, crossref, doaj, opencitations, pubpeer, code_checker, data_checker, fair_checker, registry_check, howfairis_check
from store import make_item

LAST_RUN = {}


def plain(s: str) -> str:
    """Result text rules: no em dashes, and none of the words fail/failed."""
    s = (s or '').replace('—', ', ').replace('–', '-')
    return re.sub(r'\bfail(?:ed|s|ure|ures|ing)?\b', 'did not work', s, flags=re.I)


def item(*a, **k):
    it = make_item(*a, **k); it['result'] = plain(it['result']); it['detail'] = plain(it['detail']); return it


def guarded(item_id, label, tool, fn):
    """Run one check; if it raises, return an 'unavailable' item with the error so the other checks still run."""
    try: return fn()
    except Exception as e:  # a check must never stop the run
        return [item(item_id, label, tool, 'unavailable', f'This check could not be completed ({type(e).__name__}).', str(e)[:200])]


def first_page_doi(text: str):
    t = unicodedata.normalize('NFKC', text)
    for m in re.finditer(r'\b10\.\d{4,9}/[^\s<>"]+', t):
        d = link_check.clean_url(m.group(0)).rstrip('.').lower()
        return d
    return None


def sentence_list(xs, n=3): return '; '.join(xs[:n]) + (f' (and {len(xs) - n} more)' if len(xs) > n else '')


# ---------- item builders ----------
def items_openalex(oa, vendors):
    out = []
    if not oa.get('found'):
        why = f"The paper was not found in OpenAlex (tried: {', '.join(t['route'] for t in oa['how']['tried']) or 'no identifier'})."
        for iid, lab in (('retraction', 'Retraction status'), ('author-track-record', 'Author track record'), ('self-citation', 'Self-citation'),
                         ('references-retracted', 'Retracted references'), ('funding-affiliations', 'Funding and affiliations')):
            out.append(item(iid, lab, 'OpenAlex', 'unavailable', why))
        return out
    cr = oa.get('crossref') or {}; url = oa.get('url') or ''
    # retraction
    oa_r = oa.get('is_retracted_openalex'); cr_r = cr.get('retracted_by_crossref') if cr.get('found') else None
    notices = (cr.get('notices_pointing_here') or []) + (cr.get('updates_on_record') or [])
    cr_text = ('Crossref has no record of this DOI (arXiv DOIs are registered with DataCite), so only OpenAlex was checked' if '10.48550' in (oa.get('doi') or '').lower() else 'Crossref could not be read for this DOI') if cr_r is None \
        else f"Crossref lists {'a retraction or withdrawal notice' if cr_r else 'no retraction or withdrawal notice'}"
    res = f"OpenAlex marks the paper as {'retracted' if oa_r else 'not retracted'}; {cr_text}."

    if cr_r is not None and notices: res = res.rstrip('.') + f"; Crossref shows {len(notices)} update notice(s) of type {', '.join(sorted({n['kind'] for n in notices}))}."
    out.append(item('retraction', 'Retraction status', 'OpenAlex and Crossref', 'flag' if (oa_r or cr_r) else 'ok', res,
                    'Checked is_retracted in OpenAlex, and update-to, updated-by, relation and notices that point at the DOI in Crossref (this includes the Retraction Watch data Crossref serves).' if cr_r is not None else 'Only OpenAlex answered.',
                    url, oa.get('http_status'), oa.get('response_sha256'), {'openalex_is_retracted': oa_r, 'crossref': {k: v for k, v in cr.items() if k not in ('authors',)}}))
    # author track record
    atr = oa['author_track_record']; ms = atr.get('matches', [])
    if not atr.get('checked'):
        out.append(item('author-track-record', 'Author track record', 'OpenAlex', 'unavailable', 'The author retraction search could not be run.', atr.get('error') or '', atr.get('meta', {}).get('url', ''), None, None, atr))
    else:
        by_work = {}
        for m in ms: by_work.setdefault(m['doi'] or m['title'], []).append(m)
        conf = [m for m in ms if m['evidence'] == 'confirmed']; poss = [m for m in ms if m['evidence'] == 'possible_name_clash']; diff = [m for m in ms if m['evidence'] == 'different_person']
        ign = atr.get('ignored_notices', [])
        tail = f" {len(ign)} letter, editorial, erratum or retraction-notice record(s) were ignored." if ign else ''
        if conf: status, res = 'flag', f"{len(conf)} retracted work(s) are matched to authors of this paper with an ORCID that is the same on both records, for example '{conf[0]['title'][:70]}' ({conf[0]['year']}, {conf[0]['author']})."
        elif poss:
            w = by_work[next(iter(by_work))]
            status = 'flag'; res = f"OpenAlex matches {len(by_work)} retracted work(s) to author(s) of this paper, but no ORCID could be compared (the retracted work has none for that author, or it is not in Crossref), so this is a possible name clash and needs a person to check: '{poss[0]['title'][:70]}' ({poss[0]['year']})."
        elif diff: status, res = 'ok', f"OpenAlex matched {len(diff)} retracted work(s) by name, but the ORCIDs differ, so they are different people."
        else: status, res = 'ok', f"OpenAlex lists no retracted research works for the {atr['authors_with_id']} authors with an OpenAlex id."
        det = tail.strip()
        if poss: det = ('; '.join(f"'{k[:60]}' lists {len(v)} author(s) of this paper ({', '.join(x['author'] for x in v)})" for k, v in by_work.items()) + '. ' + det).strip()
        out.append(item('author-track-record', 'Author track record', 'OpenAlex and Crossref ORCIDs', status, res + tail if status != 'flag' or conf else res, det, atr['meta']['url'], atr['meta']['http_status'], atr['meta']['response_sha256'],
                        {**atr, 'orcid_on_openalex_authors': f"{oa['orcid_count']} of {len(oa['authors'])}"}))
    # self-citation and retracted references
    rs = oa['reference_scan']; c0 = (rs['calls'] or [{}])[0]
    if not rs['references']: out.append(item('self-citation', 'Self-citation', 'OpenAlex', 'unavailable', 'OpenAlex lists no referenced works for this paper.', '', url))
    else: out.append(item('self-citation', 'Self-citation', 'OpenAlex', 'ok', f"{rs['self_citations']} of {rs['with_author_metadata']} references with author data ({round(100 * (rs['rate'] or 0))}%) share at least one author with this paper.",
                          f"OpenAlex lists {rs['references']} references; {rs['with_author_metadata']} had author metadata.", c0.get('url', ''), c0.get('http_status'), c0.get('response_sha256'), {k: v for k, v in rs.items() if k != 'calls'}))
    if rs['references']:
        rr = rs['retracted']
        out.append(item('references-retracted', 'Retracted references', 'OpenAlex', 'flag' if rr else 'ok',
                        (f"{len(rr)} of {rs['references']} references are marked retracted in OpenAlex: " + sentence_list([f"'{r['title'][:60]}' ({r['year']}, {r['doi']})" for r in rr])) if rr else f"None of the {rs['references']} references is marked retracted in OpenAlex.",
                        '', c0.get('url', ''), c0.get('http_status'), c0.get('response_sha256'), {'retracted': rr, 'references': rs['references']}))
    else: out.append(item('references-retracted', 'Retracted references', 'OpenAlex', 'unavailable', 'OpenAlex lists no referenced works for this paper.'))
    # funding and affiliations
    co, vh = oa['company_affiliations'], oa['vendor_affiliations']
    parts = [f"{len(co)} author affiliation(s) typed company" + (f" ({sentence_list([c['author'] + ' at ' + c['institution'] for c in co])})" if co else ''),
             (f"funders listed by OpenAlex: {', '.join(oa['funders'])}" if oa['funders'] else 'OpenAlex lists no funders'),
             (f"{len(oa['grants'])} grant(s) listed" if oa['grants'] else 'no grants listed')]
    if vh: parts.append('author affiliation matches a developer of a model the paper evaluates: ' + sentence_list([f"{h['author']} ({h['vendor']})" for h in vh]))
    out.append(item('funding-affiliations', 'Funding and affiliations', 'OpenAlex', 'flag' if vh else 'ok', '; '.join(parts) + '.', 'Facts as recorded by OpenAlex. Vendor names compared: ' + (', '.join(vendors) or 'none given') + '.', url, oa.get('http_status'), oa.get('response_sha256'),
                    {'authors': oa['authors'], 'company_affiliations': co, 'vendor_affiliations': vh, 'funders': oa['funders'], 'grants': oa['grants'], 'vendors_compared': list(vendors)}))
    return out


def item_peer_review(oa):
    if not oa.get('found'): return item('peer-review-status', 'Peer-review status', 'OpenAlex and Crossref', 'unavailable', 'The paper was not found in OpenAlex, so its publication status is not known.')
    pubs = oa['published_versions']
    if oa['is_preprint']:
        if pubs: return item('peer-review-status', 'Peer-review status', 'OpenAlex and Crossref', 'ok', f"This is a preprint ({oa['journal']}) and a published version was found: {pubs[0].get('venue') or ''} {pubs[0].get('doi') or pubs[0].get('url')}.", 'Found through OpenAlex locations, Crossref is-preprint-of, or an exact title and first-author search.', oa['url'], oa['http_status'], oa['response_sha256'], {'published_versions': pubs})
        return item('peer-review-status', 'Peer-review status', 'OpenAlex and Crossref', 'flag', f"This is a preprint ({oa['journal']}) and no published version was found in OpenAlex or Crossref.", 'A journal version may exist under a different title.', oa['url'], oa['http_status'], oa['response_sha256'], {'published_versions': []})
    return item('peer-review-status', 'Peer-review status', 'OpenAlex and Crossref', 'ok', f"Published as {oa['pubType']} in {oa['journal']} ({oa['publication_year']}), a venue of type {oa['source_type']} in OpenAlex.", '', oa['url'], oa['http_status'], oa['response_sha256'], {'type': oa['openalex_type'], 'source_type': oa['source_type']})


def items_citations(oa, doi):
    out = []
    d = doaj.listed(oa.get('issn') or []) if oa.get('found') and not oa.get('is_preprint') else None
    if d is None: out.append(item('doaj', 'DOAJ listing', 'DOAJ', 'unavailable', 'A preprint or an unknown venue has no journal ISSN to look up in DOAJ.'))
    elif d.get('doajListed') is None: out.append(item('doaj', 'DOAJ listing', 'DOAJ', 'unavailable', 'The DOAJ lookup did not return an answer.', d.get('error') or '', d.get('url', ''), d.get('http_status'), d.get('response_sha256'), d))
    else: out.append(item('doaj', 'DOAJ listing', 'DOAJ', 'ok', f"The journal ({oa.get('journal')}) is {'listed' if d['doajListed'] else 'not listed'} in the Directory of Open Access Journals.", '', d.get('url', ''), d.get('http_status'), d.get('response_sha256'), d))
    oc = opencitations.count(doi) if doi else {'citationCount': None, 'error': 'no DOI'}
    n_oa = oa.get('citationCount_openalex') if oa.get('found') else None
    if oc.get('citationCount') is None and n_oa is None: out.append(item('citations', 'Citation counts', 'OpenCitations and OpenAlex', 'unavailable', 'No citation count could be read.', oc.get('error') or ''))
    else: out.append(item('citations', 'Citation counts', 'OpenCitations and OpenAlex', 'ok', f"OpenCitations counts {oc.get('citationCount') if oc.get('citationCount') is not None else 'no value for'} citations and OpenAlex counts {n_oa}.", 'Counts differ between sources because each indexes different references.', oc.get('url', ''), oc.get('http_status'), oc.get('response_sha256'), {'opencitations': oc.get('citationCount'), 'openalex': n_oa}))
    return out


def item_pubpeer(doi):
    if not doi: return item('pubpeer', 'PubPeer', 'PubPeer', 'unavailable', 'PubPeer is searched by DOI and this paper has none.')
    p = pubpeer.comments(doi)
    cnt = p['pubpeerCommentCount']
    if cnt is None: res = f"Search link: {p['pubpeer_search_url']}. The comment count could not be read (HTTP {p['http_status']}); {p['label']}."
    else: res = f"PubPeer lists {cnt} comment(s) for this DOI (HTTP {p['http_status']}); search link: {p['pubpeer_search_url']}. Count source: {p['label']}."
    return item('pubpeer', 'PubPeer', 'PubPeer (unofficial endpoint)', 'unavailable' if cnt is None else ('flag' if cnt else 'ok'), res, f"Checked {p['checked_utc']}. The link is the safe result; the count comes from an unofficial endpoint.", p['pubpeer_search_url'], p['http_status'], p['response_sha256'], p)


def link_sentence(r):
    bits = [f"HTTP {r.get('http_status')}" if r.get('http_status') else 'no HTTP answer']
    if r.get('doi'): bits = ['DOI is registered' if r.get('doi_registered') else 'DOI is not registered' if r.get('doi_registered') is False else 'DOI could not be checked']
    if r.get('redirects'): bits.append(f"{len(r['redirects'])} redirect(s)")
    if r.get('label') == 'redirect-to-login': bits.append('ends on a login page')
    if r.get('label') == 'blocked': bits.append('the site refuses automated requests, so it could not be verified')
    if r.get('label') == 'unreachable': bits.append('no connection could be made after two attempts (may be temporary)')
    if r.get('label') == 'dead' and r.get('dns_failure'): bits[0] = 'the domain name does not resolve'
    wb = r.get('wayback')
    if wb is not None: bits.append('Wayback Machine has a snapshot' + (f" from {wb['snapshot_time'][:8]}" if wb.get('snapshot_time') else '') if wb.get('has_snapshot') else 'no Wayback Machine snapshot')
    return f"{r['url'][:110]}: " + ', '.join(bits) + f". Class: {r['class']}, {'reference list' if r['in_references'] else 'main text'}."


def items_links(results, ex):
    out = []; stmts = link_check.availability_statements(ex['body_text'] or ex['text'])
    n = len(results); dead = [r for r in results if r['label'] == 'dead']; login = [r for r in results if r['label'] == 'redirect-to-login']; blocked = [r for r in results if r['label'] == 'blocked']
    redirected = [r for r in results if r.get('redirects')]; wb = sum(1 for r in results if r.get('wayback') and r['wayback'].get('has_snapshot'))
    body = [r for r in results if not r['in_references']]
    res = f"{n} links and DOIs found ({len(body)} in the main text, {n - len(body)} in the reference list); {len(dead)} dead" + (f" ({', '.join(r['url'][:45] for r in dead[:3])})" if dead else '') + f", {len(login)} redirected to a login page, {len(blocked)} blocked to automated requests, {len([x for x in results if x['label'] == 'unreachable'])} unreachable, {len(redirected)} redirected."
    if stmts: res += f" {len(stmts)} availability statement(s) found: " + sentence_list([f"{s['kind']}: '{s['sentence'][:110]}'" for s in stmts], 2)
    out.append(item('links', 'Links and DOIs in the PDF', 'PyMuPDF, doi.org, archive.org', 'flag' if (dead or login or stmts) else 'ok', res,
                    f"Wayback Machine snapshots exist for {wb} of the {n} links. DOI links are checked with the doi.org handle API and are not looked up in the Wayback Machine unless they are not registered.", '', None, None,
                    {'total': n, 'main_text': len(body), 'reference_list': n - len(body), 'dead': [r['url'] for r in dead], 'login': [r['url'] for r in login], 'blocked': [r['url'] for r in blocked], 'availability_statements': stmts,
                     'references_start_page': ex.get('references_start_page')}))
    for i, r in enumerate(results, 1):
        wbd = r.get('wayback') or {}
        out.append(item(f'link-{i}', f"Link {i}: {r['class']}", 'requests, archive.org', r['status'], link_sentence(r), 'Redirect chain: ' + ' > '.join(r.get('redirects') or []) + f" > {r.get('final_url')}" if r.get('redirects') else (f"Final URL: {r.get('final_url')}" if r.get('final_url') and r.get('final_url') != r['url'] else ''),
                        r['url'], r.get('http_status'), r.get('response_sha256'), {k: r.get(k) for k in ('error', 'dns_failure', 'url', 'doi', 'class', 'label', 'final_url', 'redirects', 'check_method', 'page', 'in_references', 'sources', 'doi_registered', 'repaired_from', 'wayback')}))
    return out


def items_code(results, paper_date):
    body = [r for r in results if not r['in_references'] and r['class'] == 'code repository']
    repos, seen = [], set()
    for r in body:
        p = code_checker.parse_repo(r['url'])
        if p and p not in seen: seen.add(p); repos.append(r['url'])
    if not repos:
        refs = [r['url'] for r in results if r['in_references'] and r['class'] == 'code repository']
        det = f"Code repository links appear only in the reference list ({', '.join(refs[:3])}); those are cited work, not this paper's code." if refs else ''
        return [item('code-repo', 'Code repository', 'GitHub API, Software Heritage, Zenodo', 'flag', 'No code repository link was found in the main text of the PDF.', det),
                item('fair-code', 'Code FAIR indicators', 'GitHub API, Software Heritage, Zenodo, howfairis', 'unavailable', 'There is no code repository to assess.')]
    checks = [code_checker.check(u, paper_date) for u in repos[:4]]
    res = ' '.join(code_checker.summarize(c) for c in checks)
    bad = [c for c in checks if c.get('exists') is not True or c.get('empty') or not c.get('license') or c.get('license') == 'NOASSERTION' or (c.get('dates') or {}).get('created_after_paper')]
    c0 = checks[0]
    out = [item('code-repo', 'Code repository', 'GitHub API, Software Heritage, Zenodo', 'flag' if bad else 'ok', res, 'Checked with the GitHub REST API, GitLab API, Software Heritage and Zenodo APIs. A pinned dependency file lists exact versions.', c0.get('repo_url', ''), c0.get('http_status'), c0.get('response_sha256'), {'repositories': checks})]
    crit = []
    for c in checks:
        if c.get('exists') is not True: crit.append({'repo': c['repo_url'], 'checked': False}); continue
        sh, z = c.get('software_heritage') or {}, c.get('zenodo') or {}
        crit.append({'repo': c['repo_url'], 'checked': True, 'public': bool(c.get('public')), 'licence': bool(c.get('license') and c['license'] != 'NOASSERTION'), 'archived_with_identifier': bool(sh.get('archived') or z.get('archived')),
                     'archived_on_zenodo_with_doi': bool(z.get('archived')), 'citation_cff': bool(c.get('citation_cff')), 'readme_instructions': bool((c.get('readme') or {}).get('has_instructions')), 'release_or_tag': bool(c.get('releases') or c.get('tags'))})
    hf = None
    if Path(howfairis_check.PY).exists(): hf = [howfairis_check.check(c['repo_url']) for c in checks[:1] if c.get('exists')]
    sents = []
    for k in crit:
        if not k['checked']: sents.append(f"{k['repo']} could not be assessed.")
        else:
            met = [n for n in ('public', 'licence', 'archived_with_identifier', 'citation_cff', 'readme_instructions', 'release_or_tag') if k[n]]
            sents.append(f"{k['repo']} meets {len(met)} of 6 indicators (public, licence, archived, CITATION.cff, README instructions, release or tag): " + (', '.join(met) or 'none') + '.')
    sents.append('howfairis second opinion: ' + (f"{hf[0].get('top/code-quality-fair')} of 5." if hf and hf[0].get('top/code-quality-fair') is not None else ('not run (its virtual environment is not installed; optional).' if not Path(howfairis_check.PY).exists() else f"not available this time ({(hf[0].get('error') if hf else 'no repository')}); optional.")))
    out.append(item('fair-code', 'Code FAIR indicators', 'GitHub API, Software Heritage, Zenodo, howfairis', 'unavailable' if not any(k['checked'] for k in crit) else ('ok' if all(k.get('licence') and k.get('archived_with_identifier') for k in crit if k['checked']) else 'flag'),
                    ' '.join(sents), 'Indicators are read directly from the repository; howfairis is optional.', c0.get('repo_url', ''), None, None, {'indicators': crit, 'howfairis': hf}))
    return out


def items_data(results):
    cands = [r for r in results if not r['in_references'] and r['class'] == 'data repository']
    gh_hint = [r for r in results if not r['in_references'] and r['class'] == 'code repository' and link_check.data_hint(r.get('context'))]
    urls = [r['url'] for r in cands][:3]
    if not urls and not gh_hint:
        return [item('data-repo', 'Data repository', 'DataCite, Zenodo, OSF, Hugging Face, Dryad', 'flag', 'No dataset link or data repository was found in the main text of the PDF.'),
                item('fair-data', 'Data FAIR indicators', 'FAIR-Checker, DataCite', 'unavailable', 'There is no dataset link to assess.', '', '', None, None, {'fuji': fair_checker.fuji_probe()})]
    checks = [data_checker.check(u) for u in urls]; sents = [data_checker.summarize(c) for c in checks]
    for r in gh_hint[:2]:
        sents.append(f"{r['url']} is a code host and the text near it mentions data: no persistent identifier for any data held there.")
    nopid = [c for c in checks if not c['persistent_identifier']['has']]
    out = [item('data-repo', 'Data repository', 'DataCite, Zenodo, OSF, Hugging Face, Dryad', 'flag' if (nopid or gh_hint) else 'ok', ' '.join(sents), '', urls[0] if urls else gh_hint[0]['url'], None, None, {'datasets': checks, 'github_hosted_data_hints': [r['url'] for r in gh_hint]})]
    fcs = [fair_checker.check(u) for u in urls[:3]]; fuji = fair_checker.fuji_probe(); sents = []
    for f in fcs:
        if not f.get('assessed'): sents.append(f"FAIR-Checker could not assess {f['url']} ({f.get('error')})."); continue
        g = f['groups']
        sents.append(f"{f['url']}: " + ', '.join(f"{g[k]['name']} {g[k]['score'] if g[k]['complete'] else 'n/a'} of {g[k]['max']}" for k in 'FAIR') + f" (FAIR-Checker total {f['raw_total']} of {f['raw_max']}).")
    sents.append('F-UJI was skipped: ' + (fuji['note'] or 'available') if not fuji['available_without_key'] else 'F-UJI answered.')
    out.append(item('fair-data', 'Data FAIR indicators', 'FAIR-Checker, DataCite', 'unavailable' if not fcs or not any(f.get('assessed') for f in fcs) else 'ok', ' '.join(sents) if urls else 'Only GitHub-hosted data was found; FAIR-Checker was not run on a code repository.',
                    'Scores are FAIR-Checker metrics (0 to 2 each) grouped by letter, with no top-up added. FAIR-Checker reads page metadata, so repositories that serve little machine-readable metadata score low.', urls[0] if urls else '', fcs[0].get('http_status') if fcs else None, fcs[0].get('response_sha256') if fcs else None, {'fair_checker': fcs, 'fuji': fuji}))
    return out


def item_registration(ex, paper_date):
    r = registry_check.check(ex['body_text'], [l for l in ex['links'] if not l['in_references']], paper_date)
    regs = r['registrations']
    if not regs: return item('registration', 'Registration', 'OSF, ClinicalTrials.gov, PROSPERO', 'unavailable', 'No registration identifier (OSF, ClinicalTrials.gov NCT, PROSPERO CRD, ISRCTN, AsPredicted) was found in the main text, so no registration check was possible.', '', '', None, None, r)
    sents = []
    for g in regs:
        d = g.get('registration_date')
        sents.append(f"{g['registry']} {g['id']}: " + (f"{g.get('date_label', 'date')} {d[:10]}" + (f", {'after' if g.get('after_publication') else 'before'} the paper date {paper_date}" if g.get('after_publication') is not None else '') if d else f"link only ({g['url']})") + '.')
    if r['stated_collection_years']: sents.append('The text states data collection in ' + ', '.join(sorted({str(y['year']) for y in r['stated_collection_years']})) + '.')
    return item('registration', 'Registration', 'OSF, ClinicalTrials.gov, PROSPERO', 'flag' if any(g.get('after_publication') or g.get('year_after_stated_collection') for g in regs) else 'ok', ' '.join(sents), '', regs[0].get('url', ''), regs[0].get('http_status'), regs[0].get('response_sha256'), r)


# ---------- main entry ----------
def collect(pdf_path, citekey, doi=None, title=None, vendors=()):
    t0 = time.time(); _http.reset_stats(); vendors = [v.strip() for v in vendors if v.strip()]
    ex = link_check.extract(pdf_path)
    doi = (doi or '').strip() or None
    found_doi = doi or first_page_doi(ex['first_page'])
    arxiv = openalex.extract_arxiv_id(ex['first_page'])
    title = title or ex.get('pdf_title')
    author = (re.match(r'[a-z]+', citekey) or [None])[0]   # first author's family name, taken from the citekey
    oa = openalex.lookup(found_doi, title, author, arxiv, vendors)
    doi_final = oa.get('doi') if oa.get('found') else found_doi
    paper_date = oa.get('publication_date') if oa.get('found') else None
    items = []
    items += guarded('retraction', 'OpenAlex checks', 'OpenAlex', lambda: items_openalex(oa, vendors))
    items += [guarded('peer-review-status', 'Peer-review status', 'OpenAlex', lambda: [item_peer_review(oa)])[0]]
    items += guarded('doaj', 'DOAJ and citations', 'DOAJ', lambda: items_citations(oa, doi_final))
    items += [guarded('pubpeer', 'PubPeer', 'PubPeer', lambda: [item_pubpeer(doi_final)])[0]]
    results = link_check.check_all(ex['links'])
    items += guarded('links', 'Links', 'link_check', lambda: items_links(results, ex))
    items += guarded('code-repo', 'Code', 'code_checker', lambda: items_code(results, paper_date))
    items += guarded('data-repo', 'Data', 'data_checker', lambda: items_data(results))
    items += [guarded('registration', 'Registration', 'registry_check', lambda: [item_registration(ex, paper_date)])[0]]
    order = ['retraction', 'author-track-record', 'self-citation', 'references-retracted', 'doaj', 'citations', 'pubpeer', 'peer-review-status', 'links']
    rank = lambda i: (order.index(i['id']) if i['id'] in order else (len(order) + int(i['id'][5:]) if i['id'].startswith('link-') else len(order) + 10000 + ['code-repo', 'data-repo', 'fair-code', 'fair-data', 'registration', 'funding-affiliations'].index(i['id']) if i['id'] in ['code-repo', 'data-repo', 'fair-code', 'fair-data', 'registration', 'funding-affiliations'] else 99999))
    items.sort(key=rank)
    LAST_RUN.update(requests=_http.STATS['requests'], cache_hits=_http.STATS['cache_hits'], seconds=round(time.time() - t0, 1), title=oa.get('title') or title, doi=doi_final,
                    how=(oa.get('how') or {}).get('route'), links=len(results))
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--pdf', required=True); ap.add_argument('--citekey', required=True); ap.add_argument('--doi'); ap.add_argument('--title')
    ap.add_argument('--vendors', default=''); ap.add_argument('--write', action='store_true', help='merge the items into provenance-quality-signals.json')
    a = ap.parse_args()
    pdf = str(Path(a.pdf).expanduser())
    items = collect(pdf, a.citekey, a.doi, a.title, a.vendors.split(','))
    for it in items:
        if it['id'].startswith('link-') and it['status'] != 'flag': continue    # the 'links' summary covers links that are fine or only blocked
        print(f"[{it['status']:^11}] {it['id']}: {it['result']}")
    print(f"\n{len(items)} items; {LAST_RUN['requests']} network requests ({LAST_RUN['cache_hits']} from cache) in {LAST_RUN['seconds']} s; paper found by {LAST_RUN['how']}: {LAST_RUN['doi']}")
    if a.write:
        p = store.write(a.citekey, items, LAST_RUN['title'], LAST_RUN['doi']); print('written to', p)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Registrations named in a paper: OSF (api.osf.io), ClinicalTrials.gov (API v2), PROSPERO (link only), AsPredicted and ISRCTN (link only).
Compares the registration date with the paper's publication date and with any data-collection year the text states.
  python3 registry_check.py paper.pdf"""
import json, re, sys
from _http import request_json_meta

NCT = re.compile(r'\bNCT\d{8}\b'); CRD = re.compile(r'\bCRD\d{8,12}\b'); ISRCTN = re.compile(r'\bISRCTN\d{8}\b')
OSF = re.compile(r'(?:osf\.io/|10\.17605/OSF\.IO/)([a-z0-9]{5})\b', re.I); ASP = re.compile(r'aspredicted\.org/(?:blind\.php\?x=)?([A-Za-z0-9_]{4,12})', re.I)
COLLECT = re.compile(r'\b(?:data|participants|records|papers|reviews|searches|search|trials?|samples?)\b[^.]{0,80}?\b(?:collected|gathered|conducted|performed|retrieved|accessed|generated|recruited|enrolled|run|searched)\b[^.]{0,80}?\b((?:19|20)\d{2})\b', re.I)


def find_ids(text: str, links=()) -> list:
    """Registration identifiers found in the body text and link URLs. Each: {registry, id, url}."""
    blob = text + '\n' + '\n'.join(l['url'] for l in links); out = {}
    for m in NCT.finditer(blob): out[('ClinicalTrials.gov', m.group(0))] = f'https://clinicaltrials.gov/study/{m.group(0)}'
    for m in CRD.finditer(blob): out[('PROSPERO', m.group(0))] = f'https://www.crd.york.ac.uk/PROSPERO/view/{m.group(0)}'
    for m in ISRCTN.finditer(blob): out[('ISRCTN', m.group(0))] = f'https://www.isrctn.com/{m.group(0)}'
    for m in OSF.finditer(blob): out[('OSF', m.group(1).lower())] = f'https://osf.io/{m.group(1).lower()}'
    for m in ASP.finditer(blob): out[('AsPredicted', m.group(1))] = f'https://aspredicted.org/{m.group(1)}'
    return [{'registry': k[0], 'id': k[1], 'url': v} for k, v in out.items()]


def stated_collection_years(text: str) -> list:
    flat = re.sub(r'\s+', ' ', text)
    return [{'year': int(m.group(1)), 'snippet': flat[max(0, m.start() - 20): m.end() + 20]} for m in COLLECT.finditer(flat)][:5]


def check_one(r: dict) -> dict:
    out = {**r, 'registration_date': None, 'checked_by': 'link only'}
    if r['registry'] == 'OSF':
        d, err, meta = request_json_meta('GET', f"https://api.osf.io/v2/registrations/{r['id']}/")
        kind = 'registration'
        if d is None and err == 'not found':
            d, err, meta = request_json_meta('GET', f"https://api.osf.io/v2/nodes/{r['id']}/"); kind = 'project (not a registration)'
        out.update(http_status=meta['http_status'], response_sha256=meta['response_sha256'], api_url=meta['url'], error=err)
        if d:
            a = d['data']['attributes']
            out.update(checked_by='api.osf.io', osf_kind=kind, title=a.get('title'), public=a.get('public'), registration_date=(a.get('date_registered') or a.get('date_created') or '')[:10] or None,
                       date_label='date registered' if kind == 'registration' else 'date created')
    elif r['registry'] == 'ClinicalTrials.gov':
        d, err, meta = request_json_meta('GET', f"https://clinicaltrials.gov/api/v2/studies/{r['id']}", params={'fields': 'NCTId|BriefTitle|StudyFirstSubmitDate|StartDate|OverallStatus'})
        out.update(http_status=meta['http_status'], response_sha256=meta['response_sha256'], api_url=meta['url'], error=err)
        if d:
            sm = d['protocolSection']['statusModule']
            out.update(checked_by='clinicaltrials.gov API v2', title=d['protocolSection']['identificationModule'].get('briefTitle'), registration_date=sm.get('studyFirstSubmitDate'),
                       study_start=(sm.get('startDateStruct') or {}).get('date'), overall_status=sm.get('overallStatus'), date_label='first submitted')
    return out


def check(text: str, links=(), paper_date=None) -> dict:
    regs = [check_one(r) for r in find_ids(text, links)]
    years = stated_collection_years(text)
    for r in regs:
        d = r.get('registration_date')
        r['after_publication'] = bool(d and paper_date and d[:10] > paper_date[:10]) if d and paper_date else None
        ys = [y['year'] for y in years]
        r['year_after_stated_collection'] = bool(d and ys and int(d[:4]) > min(ys)) if d and ys else None
    return {'registrations': regs, 'stated_collection_years': years, 'paper_date': paper_date}


if __name__ == '__main__':
    import link_check
    ex = link_check.extract(sys.argv[1]); print(json.dumps(check(ex['body_text'], ex['links']), indent=1))

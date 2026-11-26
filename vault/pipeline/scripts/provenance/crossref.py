#!/usr/bin/env python3
"""Crossref checks for one DOI: update notices (retraction, correction, expression of concern; includes the Retraction Watch data Crossref serves),
relations such as is-preprint-of, and per-author ORCIDs.   python3 crossref.py 10.1016/j.jclinepi.2024.111533"""
import json, re, sys
from urllib.parse import quote
from _http import request_json_meta

API = 'https://api.crossref.org'
RETRACT_WORDS = ('retraction', 'withdrawal', 'removal')


def norm_doi(doi): return re.sub(r'^https?://(dx\.)?doi\.org/', '', (doi or '').strip()).lower()


def parse_updates(msg: dict) -> list:
    """Collect update-type statements from a Crossref work message. Each item: {kind, source, doi, via}."""
    out = []
    for field in ('update-to', 'updated-by'):
        for u in msg.get(field) or []:
            out.append({'kind': (u.get('type') or '').lower(), 'source': u.get('source'), 'doi': u.get('DOI'), 'via': field, 'label': u.get('label')})
    for k, vals in (msg.get('relation') or {}).items():
        if 'retract' in k.lower() or k in ('is-corrected-by', 'has-correction'):
            for v in vals: out.append({'kind': k, 'source': None, 'doi': v.get('id'), 'via': 'relation', 'label': None})
    return out


def is_retraction_kind(kind): return any(w in (kind or '') for w in RETRACT_WORDS) or 'retract' in (kind or '')


def check(doi: str) -> dict:
    doi = norm_doi(doi)
    d, err, meta = request_json_meta('GET', f'{API}/works/{quote(doi, safe="/")}')
    res = {'doi': doi, 'found': bool(d), 'error': err, 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256'], 'url': meta['url']}
    if not d: return res
    m = d['message']
    ups = parse_updates(m)
    # notices that point at this DOI (this is where Crossref serves Retraction Watch records)
    n, _, m2 = request_json_meta('GET', f'{API}/works', params={'filter': f'updates:{doi}', 'rows': 20, 'select': 'DOI,type,title,update-to,issued'})
    notices = []
    for it in ((n or {}).get('message') or {}).get('items', []):
        for u in it.get('update-to') or []:
            if (u.get('DOI') or '').lower() == doi:
                notices.append({'notice_doi': it.get('DOI'), 'kind': (u.get('type') or '').lower(), 'source': u.get('source'), 'title': (it.get('title') or [''])[0][:120]})
    title = (m.get('title') or [''])[0]
    rel = m.get('relation') or {}
    res.update({'title': title, 'type': m.get('type'), 'issued': (m.get('issued') or {}).get('date-parts', [[None]])[0],
                'updates_on_record': ups, 'notices_pointing_here': notices,
                'retracted_by_crossref': any(is_retraction_kind(x['kind']) for x in ups + notices) or title.lower().startswith('retracted:'),
                'is_preprint_of': [v.get('id') for v in rel.get('is-preprint-of', [])],
                'has_preprint': [v.get('id') for v in rel.get('has-preprint', [])],
                'authors': [{'family': a.get('family'), 'given': a.get('given'), 'orcid': re.sub(r'^https?://orcid.org/', '', a.get('ORCID') or '') or None} for a in m.get('author') or []],
                'funders': [{'name': f.get('name'), 'doi': f.get('DOI'), 'awards': f.get('award')} for f in m.get('funder') or []],
                'notice_query_status': m2['http_status'], 'notice_query_sha256': m2['response_sha256']})
    return res


def orcid_for_family(cr: dict, family: str):
    """ORCID that Crossref lists for the author with this family name on this work, or None."""
    fam = (family or '').lower()
    for a in cr.get('authors') or []:
        if (a.get('family') or '').lower() == fam and a.get('orcid'): return a['orcid']
    return None


if __name__ == '__main__':
    r = check(sys.argv[1]); r.pop('authors', None); print(json.dumps(r, indent=1))

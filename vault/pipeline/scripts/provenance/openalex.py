#!/usr/bin/env python3
"""OpenAlex: licence, open-access status, publication type, citations, retraction flag, ORCID coverage, author retractions, self-citation rate.
  python3 openalex.py 10.2196/59258        (prints JSON with the vault's frontmatter field names)"""
import json, re, sys
from _http import request_json
API = 'https://api.openalex.org'
TYPES = {'article': 'journal-article', 'preprint': 'preprint', 'book-chapter': 'book-chapter', 'review': 'journal-article', 'dissertation': 'thesis'}


def mine_ids(aids): return set(aids)


def lookup(doi: str) -> dict:
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi.strip())
    w, err = request_json('GET', f'{API}/works/https://doi.org/{doi}')
    if not w: return {'doi': doi, 'error': err}
    loc = w.get('primary_location') or {}; src = loc.get('source') or {}; auth = w.get('authorships') or []
    aids = [a['author']['id'].rsplit('/', 1)[-1] for a in auth if a.get('author', {}).get('id')]
    orcid = sum(1 for a in auth if a.get('author', {}).get('orcid'))
    retr, retr_list = None, []
    if aids:
        d, _ = request_json('GET', f"{API}/works", params={'filter': 'authorships.author.id:' + '|'.join(aids[:50]) + ',is_retracted:true', 'per-page': 5,
                                                          'select': 'title,publication_year,authorships'})
        retr = (d or {}).get('meta', {}).get('count')
        for r in (d or {}).get('results', []):
            hit = [x['author']['display_name'] for x in r.get('authorships', []) if (x.get('author', {}).get('id') or '').rsplit('/', 1)[-1] in mine_ids(aids)]
            retr_list.append({'title': (r.get('title') or '')[:100], 'year': r.get('publication_year'), 'matched_author': hit})
    refs = [r.rsplit('/', 1)[-1] for r in (w.get('referenced_works') or [])]
    selfc = checked = 0; mine = set(aids)
    for i in range(0, len(refs), 50):
        d, _ = request_json('GET', f"{API}/works", params={'filter': 'openalex_id:' + '|'.join(refs[i:i + 50]), 'select': 'id,authorships', 'per-page': 50})
        for r in (d or {}).get('results', []):
            ids = {a['author']['id'].rsplit('/', 1)[-1] for a in r.get('authorships', []) if a.get('author', {}).get('id')}
            if ids: checked += 1; selfc += bool(ids & mine)
    stype = src.get('type'); ptype = TYPES.get(w.get('type'), w.get('type'))
    if w.get('type') == 'article' and stype == 'repository': ptype = 'preprint'
    return {'doi': doi, 'title': w.get('title'), 'license': loc.get('license'), 'license_source': f"OpenAlex (primary location: {src.get('display_name')})",
            'oa_status': (w.get('open_access') or {}).get('oa_status'), 'pubType': ptype, 'journal': src.get('display_name'), 'publisher': src.get('host_organization_name'),
            'issn': src.get('issn') or ([src['issn_l']] if src.get('issn_l') else []), 'is_in_doaj_per_openalex': src.get('is_in_doaj'),
            'citationCount_openalex': w.get('cited_by_count'), 'is_retracted': w.get('is_retracted'),
            'authorTrackRecordChecked': f'{orcid} of {len(auth)} authors (ORCID on record); {len(aids)} with an OpenAlex id', 'retracted_works_matched_by_author_id': retr, 'retracted_works': retr_list,
            'authorTrackRecord': None if retr is None else ('clean' if retr == 0 else 'NEEDS HUMAN CHECK: OpenAlex matched retracted work(s) to an author id; name clashes are common, verify it is the same person'),
            'selfCitationRate': round(selfc / checked, 3) if checked else None, 'selfCitationChecked': f'{checked} of {len(refs)} references had author metadata'}


if __name__ == '__main__':
    print(json.dumps(lookup(sys.argv[1]), indent=1))

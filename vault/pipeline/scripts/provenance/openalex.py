#!/usr/bin/env python3
"""OpenAlex: find the paper (by DOI, arXiv id or exact title), then report licence, open-access status, type, citations, retraction flag,
author track record (ORCID-checked), self-citation, retracted references, published version of a preprint, affiliations and funders.
  python3 openalex.py 10.2196/59258
  python3 openalex.py --title "Generative Adversarial Reviews: When LLMs Become the Critic" --author Bougie"""
import argparse, difflib, json, re, sys
from _http import request_json_meta
import crossref

API = 'https://api.openalex.org'
TYPES = {'article': 'journal-article', 'preprint': 'preprint', 'book-chapter': 'book-chapter', 'review': 'journal-article', 'dissertation': 'thesis'}
# work types that are comments on or notices about other works, never "a retracted work by the author"
NOTICE_TYPES = {'letter', 'editorial', 'erratum', 'peer-review', 'retraction', 'paratext'}
NOTICE_TITLE = re.compile(r'^\s*(letter\s+re\b|re:|retraction\s*(notice|:)|notice of retraction|withdrawal\s*(notice|:)|expression of concern|erratum|corrigendum|correction\s+to|comment on|reply to)', re.I)
WORK_SELECT = ('id,doi,title,display_name,publication_year,publication_date,type,is_retracted,cited_by_count,open_access,primary_location,locations,'
               'authorships,referenced_works,awards,funders')


def short_id(u): return (u or '').rsplit('/', 1)[-1]
def clean_doi(doi): return re.sub(r'^https?://(dx\.)?doi\.org/', '', (doi or '').strip())
def norm_orcid(o): return re.sub(r'^https?://orcid.org/', '', o or '').strip().upper() or None


# ---------- decision logic (unit tested offline) ----------
def is_notice(work_type, title) -> bool:
    """True for letters, editorials, errata, peer-review reports and retraction notices: these are not retracted research by the author."""
    return (work_type or '') in NOTICE_TYPES or bool(NOTICE_TITLE.match(title or ''))


def classify_author_match(paper_orcid, hit_orcid) -> str:
    """'confirmed' when both ORCIDs exist and are equal, 'different_person' when both exist and differ, otherwise 'possible_name_clash'."""
    a, b = norm_orcid(paper_orcid), norm_orcid(hit_orcid)
    if a and b: return 'confirmed' if a == b else 'different_person'
    return 'possible_name_clash'


def norm_title(t): return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]+', ' ', (t or '').lower())).strip()


def title_similarity(a, b) -> float: return difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def title_match(query_title, cand_title, query_author, cand_authors, threshold=0.95) -> dict:
    """Accept only a very close title AND a matching first author (family name of query_author equals the last word of the candidate's first author)."""
    sim = title_similarity(query_title, cand_title)
    fam = norm_title(query_author).split(' ')[-1] if query_author else ''
    first = norm_title(cand_authors[0]).split(' ') if cand_authors else []
    author_ok = bool(fam) and fam in first
    return {'similarity': round(sim, 3), 'author_ok': author_ok, 'accepted': sim >= threshold and author_ok}


def extract_arxiv_id(text):
    m = re.search(r'arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?', text or '', re.I) or re.search(r'10\.48550/arXiv\.(\d{4}\.\d{4,5})', text or '', re.I)
    return m.group(1) if m else None


def published_versions(work, own_doi):
    """Locations of an OpenAlex work that are journal/conference versions with a DOI different from the work's own."""
    out = []
    for loc in work.get('locations') or []:
        src = loc.get('source') or {}
        doi = clean_doi(loc.get('landing_page_url') or '') if 'doi.org' in (loc.get('landing_page_url') or '') else None
        if src.get('type') in ('journal', 'conference') or loc.get('version') == 'publishedVersion':
            if (doi and doi.lower() != (own_doi or '').lower()) or (not doi and src.get('type') == 'journal'):
                out.append({'venue': src.get('display_name'), 'doi': doi, 'url': loc.get('landing_page_url'), 'version': loc.get('version')})
    return out


def affiliation_facts(authorships, vendors=()):
    """Authors with an institution typed 'company', and authors whose affiliation names match a model developer from `vendors`."""
    companies, vendor_hits = [], []
    for a in authorships:
        name = (a.get('author') or {}).get('display_name')
        insts = [i.get('display_name') or '' for i in a.get('institutions') or []] + list(a.get('raw_affiliation_strings') or [])
        for i in a.get('institutions') or []:
            if i.get('type') == 'company': companies.append({'author': name, 'institution': i.get('display_name'), 'country': i.get('country_code')})
        for v in vendors:
            v = v.strip()
            if v and any(re.search(r'(?<![\w-])' + re.escape(v) + r'(?![\w-])', s, re.I) for s in insts): vendor_hits.append({'author': name, 'vendor': v})
    return companies, vendor_hits


# ---------- lookup ----------
def get_work(doi=None, title=None, first_author=None, arxiv_id=None):
    """Returns (work or None, how, meta). how records which route found it and, for titles, the match scores."""
    tried = []
    ids = []
    if doi: ids.append(('doi', clean_doi(doi)))
    if arxiv_id and not (doi and '10.48550' in doi.lower()): ids.append(('arxiv', f'10.48550/arXiv.{arxiv_id}'))
    for how, d in ids:
        w, err, meta = request_json_meta('GET', f'{API}/works/https://doi.org/{d}', params={'select': WORK_SELECT})
        tried.append({'route': how, 'doi': d, 'result': 'found' if w else err})
        if w: return w, {'route': how, 'tried': tried}, meta
    if title:
        d, err, meta = request_json_meta('GET', f'{API}/works', params={'search': title, 'per-page': 5, 'select': WORK_SELECT + ',relevance_score'})
        best = None
        for c in (d or {}).get('results', []):
            m = title_match(title, c.get('title') or '', first_author, [(a.get('author') or {}).get('display_name') or '' for a in c.get('authorships') or []])
            m['openalex_relevance_score'] = c.get('relevance_score')
            if best is None or m['similarity'] > best[1]['similarity']: best = (c, m)
        tried.append({'route': 'title', 'result': best[1] if best else (err or 'no results')})
        if best and best[1]['accepted']: return best[0], {'route': 'title', 'tried': tried, 'match': best[1]}, meta
        return None, {'route': None, 'tried': tried}, meta
    return None, {'route': None, 'tried': tried}, {'url': None, 'http_status': None, 'response_sha256': None}


def author_track_record(authorships, paper_cr):
    aids = [short_id(a['author']['id']) for a in authorships if (a.get('author') or {}).get('id')]
    out = {'authors_with_id': len(aids), 'matches': [], 'ignored_notices': [], 'checked': False}
    if not aids: return out
    d, err, meta = request_json_meta('GET', f'{API}/works', params={'filter': 'authorships.author.id:' + '|'.join(aids[:50]) + ',is_retracted:true', 'per-page': 50,
                                                                    'select': 'id,doi,title,publication_year,type,authorships'})
    out.update(meta={k: meta[k] for k in ('url', 'http_status', 'response_sha256')}, error=err)
    if d is None: return out
    out['checked'] = True; out['count_returned_by_openalex'] = (d.get('meta') or {}).get('count')
    mine = {short_id(a['author']['id']): a['author'] for a in authorships if (a.get('author') or {}).get('id')}
    for r in d.get('results', []):
        rec = {'title': (r.get('title') or '')[:120], 'year': r.get('publication_year'), 'doi': r.get('doi'), 'type': r.get('type')}
        if is_notice(r.get('type'), r.get('title')): out['ignored_notices'].append(rec); continue
        hit_cr = None
        for ra in r.get('authorships') or []:
            aid = short_id((ra.get('author') or {}).get('id'))
            if aid not in mine: continue
            fam = (ra['author'].get('display_name') or '').split(' ')[-1]
            paper_orcid = crossref.orcid_for_family(paper_cr or {}, fam) or norm_orcid(mine[aid].get('orcid'))
            if hit_cr is None and r.get('doi'): hit_cr = crossref.check(clean_doi(r['doi']))
            hit_orcid = crossref.orcid_for_family(hit_cr or {}, fam)
            out['matches'].append({**rec, 'author': mine[aid].get('display_name'), 'openalex_author_id': aid, 'paper_orcid': paper_orcid, 'retracted_work_orcid': hit_orcid,
                                   'evidence': classify_author_match(paper_orcid, hit_orcid)})
    return out


def reference_scan(refs, mine):
    """Fetch every referenced work once: author ids for self-citation and is_retracted for retracted references."""
    selfc = checked = 0; retracted = []; calls = []
    for i in range(0, len(refs), 50):
        d, err, meta = request_json_meta('GET', f'{API}/works', params={'filter': 'openalex_id:' + '|'.join(refs[i:i + 50]), 'per-page': 50,
                                                                         'select': 'id,authorships,is_retracted,title,publication_year,doi'})
        calls.append({k: meta[k] for k in ('url', 'http_status', 'response_sha256')})
        for r in (d or {}).get('results', []):
            ids = {short_id(a['author']['id']) for a in r.get('authorships', []) if (a.get('author') or {}).get('id')}
            if ids: checked += 1; selfc += bool(ids & mine)
            if r.get('is_retracted'): retracted.append({'title': (r.get('title') or '')[:140], 'year': r.get('publication_year'), 'doi': r.get('doi')})
    return {'references': len(refs), 'with_author_metadata': checked, 'self_citations': selfc, 'rate': round(selfc / checked, 3) if checked else None,
            'retracted': retracted, 'calls': calls}


def lookup(doi=None, title=None, first_author=None, arxiv_id=None, vendors=()) -> dict:
    w, how, meta = get_work(doi, title, first_author, arxiv_id)
    if not w: return {'doi': clean_doi(doi) if doi else None, 'found': False, 'how': how, 'error': 'paper not found in OpenAlex'}
    own_doi = clean_doi(w.get('doi'))
    loc = w.get('primary_location') or {}; src = loc.get('source') or {}; auth = w.get('authorships') or []
    cr = crossref.check(own_doi) if own_doi else {'found': False}
    atr = author_track_record(auth, cr)
    refs = [short_id(r) for r in (w.get('referenced_works') or [])]
    mine = {short_id(a['author']['id']) for a in auth if (a.get('author') or {}).get('id')}
    rs = reference_scan(refs, mine)
    stype = src.get('type'); ptype = TYPES.get(w.get('type'), w.get('type'))
    if w.get('type') == 'article' and stype == 'repository': ptype = 'preprint'
    companies, vendor_hits = affiliation_facts(auth, vendors)
    is_pre = ptype == 'preprint' or 'arxiv' in own_doi.lower()
    pubv = published_versions(w, own_doi)
    for x in cr.get('is_preprint_of') or []: pubv.append({'venue': None, 'doi': x, 'url': f'https://doi.org/{x}', 'version': 'crossref is-preprint-of'})
    if is_pre and not pubv and w.get('title'):
        t = w.get('title'); fa = ((auth[0].get('author') or {}).get('display_name') if auth else None)
        d, _, _m = request_json_meta('GET', f'{API}/works', params={'search': t, 'filter': 'type:article', 'per-page': 5, 'select': 'id,doi,title,authorships,primary_location'})
        for c in (d or {}).get('results', []):
            tm = title_match(t, c.get('title') or '', (fa or '').split(' ')[-1], [(x.get('author') or {}).get('display_name') or '' for x in c.get('authorships') or []])
            if tm['accepted'] and clean_doi(c.get('doi')).lower() != own_doi.lower(): pubv.append({'venue': ((c.get('primary_location') or {}).get('source') or {}).get('display_name'),
                                                                                                   'doi': clean_doi(c.get('doi')), 'url': c.get('doi'), 'version': 'title match ' + str(tm['similarity'])})
    return {'found': True, 'how': how, 'doi': own_doi, 'openalex_id': short_id(w.get('id')), 'title': w.get('title'), 'publication_year': w.get('publication_year'),
            'publication_date': w.get('publication_date'), 'url': meta.get('url'), 'http_status': meta.get('http_status'), 'response_sha256': meta.get('response_sha256'),
            'license': loc.get('license'), 'license_source': f"OpenAlex (primary location: {src.get('display_name')})", 'oa_status': (w.get('open_access') or {}).get('oa_status'),
            'pubType': ptype, 'openalex_type': w.get('type'), 'source_type': stype, 'journal': src.get('display_name'), 'publisher': src.get('host_organization_name'),
            'issn': src.get('issn') or ([src['issn_l']] if src.get('issn_l') else []), 'is_in_doaj_per_openalex': src.get('is_in_doaj'),
            'citationCount_openalex': w.get('cited_by_count'), 'is_retracted_openalex': w.get('is_retracted'), 'crossref': cr,
            'author_track_record': atr, 'reference_scan': rs, 'is_preprint': is_pre, 'published_versions': pubv,
            'authors': [{'name': (a.get('author') or {}).get('display_name'), 'orcid': norm_orcid((a.get('author') or {}).get('orcid')),
                         'institutions': [{'name': i.get('display_name'), 'type': i.get('type')} for i in a.get('institutions') or []]} for a in auth],
            'orcid_count': sum(1 for a in auth if (a.get('author') or {}).get('orcid')), 'company_affiliations': companies, 'vendor_affiliations': vendor_hits,
            'grants': [{'funder': g.get('funder_display_name') or (g.get('funder') or {}).get('display_name') if isinstance(g.get('funder'), dict) else g.get('funder_display_name'),
                       'award_id': g.get('funder_award_id') or g.get('award_id'), 'raw': {k: v for k, v in g.items() if k not in ('id',)}} for g in (w.get('awards') or [])],
            'funders': [f.get('display_name') for f in (w.get('funders') or [])]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('doi', nargs='?'); ap.add_argument('--title'); ap.add_argument('--author'); ap.add_argument('--arxiv')
    ap.add_argument('--vendors', default=''); a = ap.parse_args()
    print(json.dumps(lookup(a.doi, a.title, a.author, a.arxiv, [v for v in a.vendors.split(',') if v]), indent=1, default=str))

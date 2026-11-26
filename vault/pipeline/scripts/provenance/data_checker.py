#!/usr/bin/env python3
"""Dataset checks. For a dataset URL or DOI: persistent identifier present, DataCite record (licence from rightsList, resource type, creators,
related identifiers, size, access conditions), and host-specific checks for Zenodo, OSF, Hugging Face and Dryad through their public APIs.
Data hosted only on GitHub, GitLab or a personal site is reported as "no persistent identifier".
  python3 data_checker.py https://zenodo.org/records/10456789"""
import json, re, sys
from urllib.parse import quote, urlparse
from _http import request_json_meta

PID_HOSTS = ('zenodo.org', 'figshare.com', 'datadryad.org', 'osf.io', 'huggingface.co', 'dataverse', 'data.mendeley.com', 'physionet.org', 'openneuro.org', 'kaggle.com', 'doi.org')
NO_PID_HOSTS = ('github.com', 'gitlab.com', 'bitbucket.org', 'github.io', 'raw.githubusercontent.com', 'gist.github.com', 'codeberg.org')
DOI_RE = re.compile(r'10\.\d{4,9}/[^\s"<>]+', re.I)


# ---------- decision logic (unit tested offline) ----------
def host_kind(url: str) -> str:
    h = urlparse(url if '://' in url else 'https://' + url).netloc.lower().removeprefix('www.')
    for name in ('zenodo.org', 'osf.io', 'huggingface.co', 'datadryad.org'):
        if h == name or h.endswith('.' + name): return name
    if any(h == x or h.endswith('.' + x) for x in NO_PID_HOSTS): return 'code host (no persistent identifier)'
    if h in ('doi.org', 'dx.doi.org'): return 'doi.org'
    if any(x in h for x in PID_HOSTS): return h
    return 'other site'


def find_doi(url: str):
    m = DOI_RE.search(url)
    if m: return m.group(0).rstrip('.,;)').lower()
    m = re.search(r'zenodo\.org/(?:records?|deposit)/(\d+)', url)
    return f'10.5281/zenodo.{m.group(1)}' if m else None


def persistent_identifier(url: str, doi) -> dict:
    kind = host_kind(url)
    if doi: return {'has': True, 'kind': 'DOI', 'value': doi}
    if kind.startswith('code host') or kind == 'other site': return {'has': False, 'kind': None, 'note': 'no persistent identifier (hosted on a code host or a personal or institutional site)'}
    return {'has': False, 'kind': None, 'note': 'hosted on a data repository but no DOI was found in the link'}


def summarize_datacite(attrs: dict) -> dict:
    rights = [{'rights': r.get('rights'), 'uri': r.get('rightsUri'), 'spdx': r.get('rightsIdentifier')} for r in attrs.get('rightsList') or []]
    access = [r['uri'] for r in rights if r.get('uri') and 'semantics' in r['uri']]
    return {'licence': [r['spdx'] or r['rights'] or r['uri'] for r in rights if (r['spdx'] or r['rights'] or r['uri']) and 'semantics' not in (r['uri'] or '')],
            'access_conditions': access, 'rights_list': rights,
            'resource_type': (attrs.get('types') or {}).get('resourceTypeGeneral'), 'resource_type_text': (attrs.get('types') or {}).get('resourceType'),
            'creators': [c.get('name') for c in attrs.get('creators') or []][:10], 'creator_count': len(attrs.get('creators') or []),
            'related_identifiers': [{'type': r.get('relationType'), 'id': r.get('relatedIdentifier')} for r in attrs.get('relatedIdentifiers') or []][:15],
            'sizes': attrs.get('sizes') or [], 'formats': attrs.get('formats') or [], 'publisher': attrs.get('publisher'), 'publication_year': attrs.get('publicationYear'),
            'version': attrs.get('version'), 'title': ((attrs.get('titles') or [{}])[0]).get('title')}


# ---------- network ----------
def datacite(doi):
    d, err, meta = request_json_meta('GET', f'https://api.datacite.org/dois/{quote(doi, safe="/")}')
    base = {'url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256']}
    if d: return {'registered_with_datacite': True, **base, **summarize_datacite(d['data']['attributes'])}
    ra, _, _m = request_json_meta('GET', f'https://doi.org/doiRA/{quote(doi, safe="/")}')
    agency = (ra or [{}])[0].get('RA') if isinstance(ra, list) and ra else None
    return {'registered_with_datacite': False, 'registration_agency': agency, 'error': err, **base}


def check_zenodo(rec_id):
    d, err, meta = request_json_meta('GET', f'https://zenodo.org/api/records/{rec_id}')
    out = {'host': 'zenodo.org', 'url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256'], 'error': err}
    if d:
        m = d.get('metadata') or {}; files = d.get('files') or []
        out.update(title=m.get('title'), access_right=m.get('access_right'), license=(m.get('license') or {}).get('id'), resource_type=(m.get('resource_type') or {}).get('type'),
                   publication_date=m.get('publication_date'), version=m.get('version'), file_count=len(files), total_bytes=sum(f.get('size', 0) for f in files),
                   concept_doi=d.get('conceptdoi'), doi=d.get('doi'), creators=len(m.get('creators') or []), related=[r.get('identifier') for r in m.get('related_identifiers') or []][:10])
    return out


def check_osf(oid):
    d, err, meta = request_json_meta('GET', f'https://api.osf.io/v2/nodes/{oid}/')
    out = {'host': 'osf.io', 'url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256'], 'error': err}
    if d:
        a = d['data']['attributes']
        out.update(title=a.get('title'), public=a.get('public'), category=a.get('category'), date_created=(a.get('date_created') or '')[:10], tags=a.get('tags'))
        i, _, _m = request_json_meta('GET', f'https://api.osf.io/v2/nodes/{oid}/identifiers/')
        out['dois'] = [x['attributes']['value'] for x in (i or {}).get('data', []) if x['attributes'].get('category') == 'doi']
        lic, _, _m2 = request_json_meta('GET', f'https://api.osf.io/v2/nodes/{oid}/license/')
        out['license'] = ((lic or {}).get('data') or {}).get('attributes', {}).get('name')
    return out


def check_hf(path):
    d, err, meta = request_json_meta('GET', f'https://huggingface.co/api/datasets/{path}')
    out = {'host': 'huggingface.co', 'url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256'], 'error': err}
    if d:
        card = d.get('cardData') or {}
        out.update(private=d.get('private'), gated=d.get('gated'), license=card.get('license'), created=(d.get('createdAt') or '')[:10], last_modified=(d.get('lastModified') or '')[:10],
                   file_count=len(d.get('siblings') or []), revision=d.get('sha'), tags=[t for t in d.get('tags') or [] if t.startswith('license:')])
    return out


def check_dryad(doi):
    d, err, meta = request_json_meta('GET', f'https://datadryad.org/api/v2/datasets/{quote("doi:" + doi, safe="")}')
    out = {'host': 'datadryad.org', 'url': meta['url'], 'http_status': meta['http_status'], 'response_sha256': meta['response_sha256'], 'error': err}
    if d: out.update(title=d.get('title'), license=d.get('license'), storage_bytes=d.get('storageSize'), publication_date=d.get('publicationDate'), status=d.get('versionStatus'), identifier=d.get('identifier'))
    return out


def check(url: str) -> dict:
    kind = host_kind(url); doi = find_doi(url)
    for prefix, name in (('10.5281/zenodo', 'zenodo.org'), ('10.17605/osf.io', 'osf.io'), ('10.5061/dryad', 'datadryad.org')):
        if kind == 'doi.org' and doi and doi.startswith(prefix): kind = name   # a DOI link to one of the supported repositories
    out = {'input': url, 'host_kind': kind, 'doi': doi, 'persistent_identifier': persistent_identifier(url, doi)}
    if doi: out['datacite'] = datacite(doi)
    if kind == 'zenodo.org':
        m = re.search(r'zenodo\.org/(?:records?|deposit)/(\d+)', url) or re.search(r'10\.5281/zenodo\.(\d+)', url)
        if m: out['host_check'] = check_zenodo(m.group(1))
    elif kind == 'osf.io':
        m = re.search(r'osf\.io/([a-z0-9]{5})\b', url, re.I) or re.search(r'10\.17605/OSF\.IO/([a-z0-9]{5})', url, re.I)
        if m: out['host_check'] = check_osf(m.group(1).lower())
    elif kind == 'huggingface.co':
        m = re.search(r'huggingface\.co/datasets/([^/?#]+/[^/?#]+|[^/?#]+)', url)
        if m: out['host_check'] = check_hf(m.group(1))
    elif kind == 'datadryad.org' and doi: out['host_check'] = check_dryad(doi)
    return out


def summarize(c: dict) -> str:
    pid = c['persistent_identifier']; bits = []
    bits.append(f"{c['input']} has a persistent identifier ({pid['value']})" if pid['has'] else f"{c['input']}: {pid['note']}")
    dc = c.get('datacite')
    if dc and dc.get('registered_with_datacite'):
        bits.append('licence ' + (', '.join(dc['licence']) if dc['licence'] else 'not stated in the DataCite record'))
        bits.append(f"resource type {dc.get('resource_type')}")
    elif dc: bits.append(f"DOI is not in DataCite (registration agency {dc.get('registration_agency')})")
    return '; '.join(bits) + '.'


if __name__ == '__main__':
    c = check(sys.argv[1]); print(json.dumps(c, indent=1)); print(summarize(c))

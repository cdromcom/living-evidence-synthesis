#!/usr/bin/env python3
"""DOAJ: is the journal listed in the Directory of Open Access Journals (by ISSN).   python3 doaj.py 2291-9694 [more ISSNs]"""
import json, sys
from _http import request_json


def listed(issns) -> dict:
    for i in issns:
        d, err = request_json('GET', f'https://doaj.org/api/search/journals/issn:{i}')
        if d is None: return {'doajListed': None, 'error': err}
        if d.get('total'): return {'doajListed': True, 'doaj_title': d['results'][0]['bibjson']['title'], 'issn_matched': i}
    return {'doajListed': False}


if __name__ == '__main__':
    print(json.dumps(listed(sys.argv[1:]), indent=1))

#!/usr/bin/env python3
"""OpenCitations citation count for a DOI (the vault's citationCountSource).   python3 opencitations.py 10.2196/59258"""
import json, sys
from _http import request_json_meta


def count(doi: str) -> dict:
    d, err, meta = request_json_meta('GET', f'https://api.opencitations.net/index/v2/citation-count/doi:{doi}')
    if d: return {'citationCount': int(d[0]['count']), 'citationCountSource': 'OpenCitations', **meta}
    return {'citationCount': None, 'error': err, **meta}


if __name__ == '__main__':
    print(json.dumps(count(sys.argv[1]), indent=1))

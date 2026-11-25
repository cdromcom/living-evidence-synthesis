#!/usr/bin/env python3
"""OpenCitations citation count for a DOI (the vault's citationCountSource).   python3 opencitations.py 10.2196/59258"""
import json, sys
from _http import request_json


def count(doi: str) -> dict:
    d, err = request_json('GET', f'https://api.opencitations.net/index/v2/citation-count/doi:{doi}')
    return {'citationCount': int(d[0]['count']), 'citationCountSource': 'OpenCitations'} if d else {'citationCount': None, 'error': err}


if __name__ == '__main__':
    print(json.dumps(count(sys.argv[1]), indent=1))

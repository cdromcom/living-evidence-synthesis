#!/usr/bin/env python3
"""Run every provenance check for one paper and print the frontmatter fields they suggest. Writes nothing to the vault.
  python3 run_provenance.py --doi 10.2196/59258 [--code https://github.com/o/r] [--data URL]"""
import argparse, json
import openalex, doaj, opencitations, pubpeer, howfairis_check, fair_checker

ap = argparse.ArgumentParser(); ap.add_argument('--doi', required=True); ap.add_argument('--code'); ap.add_argument('--data'); a = ap.parse_args()
out = {'openalex': openalex.lookup(a.doi)}
out['doaj'] = doaj.listed(out['openalex'].get('issn') or [])
out['opencitations'] = opencitations.count(a.doi)
out['pubpeer'] = pubpeer.comments(a.doi)
hf = howfairis_check.check(a.code) if a.code else None
if hf: out['howfairis'] = hf
if a.data: out['fair_checker'] = fair_checker.check(a.data, bool(hf and hf.get('license_found')))
print(json.dumps(out, indent=1))

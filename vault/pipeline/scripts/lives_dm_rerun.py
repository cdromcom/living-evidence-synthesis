#!/usr/bin/env python3
"""One-off (JP, 2026-11-26): rerun the earlier Liquid d1-ultra decision-model results with d1.2-ultra so the two can be compared. Keeps the old scores. Usage: lives_dm_rerun.py RUN [RUN...]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lives_run as LR, lives_stages as S, lives_verify as V, decision_models as dm

dm.load_env()


def rerun_checks(M):
    """Decision-model checks stage (relevancy, fidelity, numbers in source, table cell matches), Liquid part only, with the current model id."""
    n = 0
    for ck, p in M.m['papers'].items():
        f_ = M.dir / ck / 'checks.json'
        if p.get('failed') or not f_.exists(): continue
        rows = json.loads(f_.read_text(encoding='utf-8')); fs, ps_ = S.final_findings(M, ck); S.QS[ck] = ps_.get('questions', []); by = {f['id']: f for f in fs}
        for v in rows:
            f = by.get(v['id'])
            if not f: continue
            r, e = dm.decide('liquid', S.dm_state(M, f, S.QS.get(ck)), S.dm_questions(M, table=S.rests_on_table(f)))
            ans = {k: x.get('noul') for k, x in ((r or {}).get('answers') or {}).items()}
            if 'dm_liquid_d1_ultra' not in v: v['dm_liquid_d1_ultra'] = (v.get('dm') or {}).get('liquid')
            v['dm_liquid_d12'] = ans; v['dm_liquid_model'] = dm.MODELS['liquid']; n += 1
        f_.write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    return n


if __name__ == '__main__':
    for run in sys.argv[1:]:
        M = LR.Manifest(run); print(run, 'checks rerun:', rerun_checks(M), 'findings;', 'verification rerun:', len(V.rerun_liquid_text(M)), 'items;', 'model', dm.MODELS['liquid'])

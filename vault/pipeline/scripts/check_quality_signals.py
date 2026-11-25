#!/usr/bin/env python3
"""List source pages that lack a quality-signal tag the web app reads (see pipeline/skills/Quality-signals-spec.md).
Read-only. Usage: python3 pipeline/scripts/check_quality_signals.py"""
import os, re
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
REQUIRED = ['appraisal/construct-validity', 'appraisal/internal-validity', 'appraisal/external-validity', 'appraisal/statistical-rigor',
            'trust/reproducibility', 'rigor/baseline-adequacy', 'rigor/human-baseline', 'rigor/train-dev-test', 'rigor/ablation-experiments',
            'rigor/prompt-engineering', 'rigor/confidence-intervals', 'rigor/chance-corrected-metrics', 'rigor/multiple-comparisons',
            'rigor/data-leakage', 'top/study-registration', 'top/study-protocol', 'top/code-transparency', 'top/data-transparency',
            'top/code-check', 'top/repository-check', 'transparency/effect-size', 'transparency/exact-p-values',
            'integrity/ethical-approval', 'integrity/funding-disclosure', 'integrity/coi-disclosure', 'integrity/spin']
def tags(p):
    t = p.read_text(encoding='utf-8'); m = re.match(r'---\n(.*?)\n---', t, re.S)
    if not m: return None
    mm = re.search(r'^tags:\s*\n((?:\s+- .*\n?)+)', m.group(1) + '\n', re.M)
    return [x.strip()[2:].strip().strip('"\'') for x in mm.group(1).splitlines() if x.strip().startswith('- ')] if mm else []
bad = 0
for p in sorted((VAULT / 'sysrev/dgraph/source').glob('@*.md')):
    tg = tags(p)
    if tg is None: print(f'{p.name}: no frontmatter'); bad += 1; continue
    missing = [r for r in REQUIRED if not any(t.startswith(r + '/') for t in tg)]
    if missing: print(f'{p.name}: missing {len(missing)}: ' + ', '.join(missing[:6]) + (' ...' if len(missing) > 6 else '')); bad += 1
print(f'{bad} source page(s) with missing signals')

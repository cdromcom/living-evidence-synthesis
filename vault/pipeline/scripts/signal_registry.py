#!/usr/bin/env python3
"""One place that says which tag each quality signal writes on a source page, which tool checks apply to it, and how to find a paper's vault citekey (JP, 2026-11-26).
Used by check_quality_signals.py, qs_export.py and the review sheet, so the lists cannot drift apart."""
import json, os, re
from pathlib import Path
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
SRC_DIRS = [VAULT / 'sysrev' / 'dgraph' / 'source', VAULT / 'source']   # source pages live in either folder (JP moved some on 2026-11-26)
SRC_DIR = SRC_DIRS[0]
LABELS = VAULT / 'pipeline' / 'templates' / 'quality-signal-labels.json'

# processor signal id -> tag prefix on the source page (Quality-signals-spec.md)
SIGNAL_TAGS = {
    'construct-validity': 'appraisal/construct-validity', 'internal-validity': 'appraisal/internal-validity', 'external-validity': 'appraisal/external-validity',
    'statistical-rigor': 'appraisal/statistical-rigor', 'reproducibility': 'trust/reproducibility',
    'baseline-adequacy': 'rigor/baseline-adequacy', 'human-baseline': 'rigor/human-baseline', 'train-dev-test': 'rigor/train-dev-test',
    'ablation-experiments': 'rigor/ablation-experiments', 'prompt-engineering': 'rigor/prompt-engineering', 'confidence-intervals': 'rigor/confidence-intervals',
    'chance-corrected-metrics': 'rigor/chance-corrected-metrics', 'multiple-comparisons': 'rigor/multiple-comparisons', 'data-leakage': 'rigor/data-leakage',
    'statistical-power': 'rigor/statistical-power', 'sample-size-estimation': 'rigor/sample-size-estimation', 'study-type': 'rigor/study-type',
    'effect-size': 'transparency/effect-size', 'exact-p-values': 'transparency/exact-p-values', 'spin': 'integrity/spin',
    'registration': 'top/study-registration', 'protocol': 'top/study-protocol', 'ethical-approval': 'integrity/ethical-approval',
    'funding-disclosure': 'integrity/funding-disclosure', 'coi-disclosure': 'integrity/coi-disclosure', 'code-check': 'top/code-check', 'data-repo-check': 'top/repository-check',
}
# signals that scripts, not models, produce (tag prefix as above)
TOOL_SIGNAL_TAGS = {'code-quality-fair': 'top/code-quality-fair', 'data-quality-fair': 'top/data-quality-fair', 'statistic-accuracy': 'forensic/statistic-accuracy', 'ai-writing-check': 'integrity/ai-writing-check'}
# provenance item ids (provenance/store.py) that bear on each signal
TOOL_CHECKS = {
    'registration': ['registration', 'links'], 'protocol': ['registration', 'links'], 'code-check': ['code-repo', 'links'], 'code-quality-fair': ['fair-code', 'code-repo'],
    'data-repo-check': ['data-repo', 'links'], 'data-quality-fair': ['fair-data', 'data-repo'], 'funding-disclosure': ['funding-affiliations'], 'coi-disclosure': ['funding-affiliations'],
    'statistic-accuracy': ['stat-checks'], 'reproducibility': ['code-repo', 'links'], 'prompt-engineering': ['links'],
}
OPTIONAL_TAGS = {'rigor/statistical-power'}   # only written when the paper has a power analysis (Quality-signals-spec.md)
REQUIRED = sorted(set(SIGNAL_TAGS.values()) - OPTIONAL_TAGS)


def labels():
    d = json.loads(LABELS.read_text(encoding='utf-8')) if LABELS.exists() else {'rows': []}
    return {r['id']: r['label'] for r in d.get('rows', [])}


def label_for(sig):
    if sig.startswith('tripod-'):
        import tripod_items; return tripod_items.label(sig)
    return labels().get(sig) or {'data-repo-check': 'Dataset check', 'sample-size-estimation': 'Sample-size estimation', 'study-type': 'Study type'}.get(sig) or sig.replace('-', ' ').capitalize()


def vault_tags(citekey):
    """{tag prefix: value} from the source page's frontmatter tags (the curated values on the live site)."""
    p = next((d / f'@{citekey}.md' for d in SRC_DIRS if (d / f'@{citekey}.md').exists()), None)
    if not p: return {}
    t = p.read_text(encoding='utf-8'); m = re.match(r'---\n(.*?)\n---', t, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        mm = re.match(r'\s+-\s+"?([a-z\-]+/[a-z0-9\-]+)/([^"\s]+)"?\s*$', line)
        if mm: out[mm.group(1)] = mm.group(2)
    return out


def resolve_citekey(folder_name, title='', year=''):
    """Vault citekey for a run folder such as 'Sarol-et-al-2024-Assessing-citation-integrity' (first author, year, title words)."""
    first = re.match(r'([A-Za-zÀ-ɏ]+)', folder_name).group(1).lower(); ym = re.search(r'(20\d\d)', folder_name) or re.search(r'(20\d\d)', str(year)); yr = ym.group(1) if ym else ''
    words = {w for w in re.findall(r'[a-z]{4,}', (title or folder_name).lower())}; best = (0, None)
    for p in [q for d in SRC_DIRS for q in d.glob('@*.md')]:
        ck = p.stem[1:]
        if not ck.lower().startswith(first) or (yr and yr not in ck): continue
        score = sum(1 for w in words if w in ck.lower()) + 0.5
        if score > best[0]: best = (score, ck)
    return best[1]


def vault_tripod(citekey):
    """{signal id: rating} from the curated TRIPOD-LLM table on the source page (written by older Claude models in 2026), in the new rating words."""
    import signals_common as sc, tripod_items as TI
    p = next((d / f'@{citekey}.md' for d in SRC_DIRS if (d / f'@{citekey}.md').exists()), None)
    if not p: return {}
    out = {}
    for r in sc.parse_table(sc.section(p.read_text(encoding='utf-8'), 'TRIPOD-LLM reporting'), 'TRIPOD', citekey):
        if r['row'] in TI.ITEMS and r['rating_icon'] in TI.ICON_TO_RATING: out[f"tripod-{r['row']}"] = TI.ICON_TO_RATING[r['rating_icon']]
    return out

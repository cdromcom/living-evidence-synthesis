#!/usr/bin/env python3
"""Statistical accuracy checks on a paper's own text (Quality signals, row "Statistical accuracy"). Cheap, scripted, no model calls. Each finding is a CLUE for a person, not a verdict.
  python3 stat_checks.py                       all source PDFs -> pipeline/misc/evd-validation/stat-checks/
  python3 stat_checks.py --only @citekey       one paper
  python3 stat_checks.py selftest              planted-error self-test
  python3 stat_checks.py grim 3.47 25 [2]      GRIM test of one mean (mean, n, decimals)
Checks
  1 PERCENT   three or more percentages in one sentence or table row that look like parts of 100% but add up to a value away from 100 (beyond rounding)
  2 GRIM      a reported mean with its sample size where no whole-number total can produce that mean (applies only to whole-number data such as Likert ratings or counts)
  3 SAMPLE    a sample size (participants, papers, trials...) stated in the abstract that never appears in the paper body, or methods and results that share no number for the same unit
Pages: printed page where the PDF prints one, else "PDF p. N" (fine for preprints)."""
import argparse, csv, math, os, re, sys
from pathlib import Path
import fitz
import pdf_pages as pp
VAULT = Path(os.environ.get('LIVES_VAULT') or Path(__file__).resolve().parents[2])
OUT = VAULT / 'pipeline' / 'misc' / 'evd-validation' / 'stat-checks'

def num(s): return float(s.replace(',', ''))

# ---------- GRIM ----------
def grim_ok(mean: float, n: int, dec: int) -> bool:
    """True if some whole-number total T gives round(T/n, dec) == mean (half up). GRIM is informative only when n < 10**dec."""
    if n <= 0: return True
    lo = math.floor((mean - 0.5 * 10 ** -dec) * n); hi = math.ceil((mean + 0.5 * 10 ** -dec) * n)
    for t in range(lo, hi + 1):
        if abs(math.floor(t / n * 10 ** dec + 0.5) / 10 ** dec - mean) < 1e-9: return True
    return False

# ---------- page text, sections ----------
def pages_text(doc): return [pp.page_text(p) for p in doc]

HEAD = {'abstract': r'^\s*abstract\b', 'intro': r'^\s*(?:1\.?\s*)?introduction\b', 'methods': r'^\s*(?:\d\.?\s*)?(?:materials and methods|methods?|methodology|experimental (?:setup|design)|study design)\b',
        'results': r'^\s*(?:\d\.?\s*)?(?:results?|findings|experiments and results)\b', 'discussion': r'^\s*(?:\d\.?\s*)?(?:discussion|conclusions?|limitations)\b'}

def sectioned(pages):
    """[(section, page_index, text_line)] using the first heading of each kind; text before any heading is 'abstract' on page 1, else 'other'."""
    lines = [(i, l) for i, t in enumerate(pages) for l in t.splitlines()]
    cur = 'abstract' if pages else 'other'; out = []; seen = set()
    for i, l in lines:
        for name, rx in HEAD.items():
            if re.match(rx, l, re.I) and len(l) < 60 and (name not in seen or name in ('results', 'methods', 'discussion')):
                cur = name; seen.add(name); break
        out.append((cur, i, l))
    return out

def chunks(rows):
    """Sentences (lines joined within a section and page) plus each raw line, so tables and prose both get checked. Yields (section, page_index, text)."""
    buf, key = [], None
    def flush():
        if buf:
            text = ' '.join(buf)
            for sent in re.split(r'(?<=[.;])\s+(?=[A-Z(\[])', text):
                if 8 < len(sent) < 600: yield (key[0], key[1], sent)
    for sec, i, l in rows:
        if (sec, i) != key:
            yield from flush(); buf = []; key = (sec, i)
        buf.append(l.strip())
        if len(l) < 400: yield (sec, i, l)
    yield from flush()

def page_label(pm, i): 
    r = pm[i] if i < len(pm) else None
    return f"p. {r['printed']}" if r and r['printed'] and r['source'] != 'pdf-position' else f"PDF p. {i + 1}"

# ---------- 1 PERCENT ----------
PCT = re.compile(r'(\d{1,3}(?:\.\d+)?)\s*%')
SKIP_PCT = re.compile(r'\bCI\b|confidence interval|\bIQR\b|\bSD\b|range|\d\s*%?\s*[\u2013\u2014-]\s*\d+(?:\.\d+)?\s*%|\d%\s*e\s*\d|\b(?:below|above|than|versus|vs\.?|from|increase[sd]?|decrease[sd]?|improve[sd]?|gain|drop|up to|at least|over|under)\b', re.I)
def check_percent(rows, pm):
    out = []; seen = set()
    for sec, i, chunk in chunks(rows):
        if True:
            if SKIP_PCT.search(chunk): continue   # confidence intervals, ranges, comparisons and "below/above" lists are not parts of one whole
            vals = [num(m) for m in PCT.findall(chunk)]
            if len(vals) < 3 or len(vals) > 12: continue
            s = sum(vals); dec = max((len(v.split('.')[1]) if '.' in v else 0) for v in PCT.findall(chunk))
            tol = len(vals) * 0.5 * 10 ** -dec + 0.05
            if 95.0 <= s <= 105.0 and abs(s - 100) > tol and (chunk, round(s, 2)) not in seen:
                seen.add((chunk, round(s, 2)))
                out.append(dict(check='PERCENT', page=page_label(pm, i), section=sec, finding=f"{' + '.join(f'{v:g}%' for v in vals)} = {s:.1f}%, not 100% (rounding allows about ±{tol:.1f}). Only a problem if these are parts of one whole.", text=chunk.strip()[:160]))
    return out

# ---------- 2 GRIM ----------
MEAN_SD = re.compile(r'(?<![\d.])(\d{1,3}\.(\d{1,2}))\s*\(\s*(?:SD\s*[=:]?\s*)?\d+\.\d+\s*\)')
MEAN_WORD = re.compile(r'\b(?:mean|average|avg\.?|M)\b[^0-9\n]{0,30}?(?<![\d.])(\d{1,3}\.(\d{1,2}))(?![\d%])', re.I)
NVAL = re.compile(r'\b[nN]\s*=\s*(\d[\d,]*)')
def check_grim(rows, pm):
    out = []
    for sec, i, line in chunks(rows):
        ns = [int(x.replace(',', '')) for x in NVAL.findall(line)] or [int(m.group(1).replace(',', '')) for m in NOUN.finditer(line)]
        if len(set(ns)) != 1: continue   # no n, or several different n in one line: ambiguous, skip
        n = ns[0]
        for rx in (MEAN_SD, MEAN_WORD):
            for m in rx.finditer(line):
                mean, dec = float(m.group(1)), len(m.group(2))
                if 10 ** dec <= n or n < 2: continue   # GRIM is only informative when n is smaller than 10^decimals
                if not grim_ok(mean, n, dec):
                    out.append(dict(check='GRIM', page=page_label(pm, i), section=sec, finding=f"mean {mean} with n = {n} is not reachable with whole-number data. Applies only if the measure is whole-number (ratings, counts).", text=line.strip()[:160]))
    return out

# ---------- 3 SAMPLE ----------
UNITS = r'(participants?|patients?|subjects?|raters?|reviewers?|annotators?|experts?|papers?|articles?|manuscripts?|abstracts?|trials?|RCTs?|studies|reviews?|systematic reviews|documents?|samples?|questions?|prompts?|cases?|reports?|submissions?|respondents?|students?|physicians?|clinicians?)'
NOUN = re.compile(r'(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d+)\s+(?:\w+\s+){0,2}?' + UNITS + r'\b', re.I)
def unit_key(u):
    u = u.lower(); u = {'studies': 'study', 'rcts': 'trial', 'rct': 'trial'}.get(u, u)
    u = u[:-1] if u.endswith('s') and u not in ('analysis',) else u
    return {'participant': 'participant', 'subject': 'participant', 'respondent': 'participant', 'patient': 'participant', 'student': 'participant', 'article': 'paper', 'manuscript': 'paper', 'submission': 'paper'}.get(u, u)
def check_sample(rows, pm):
    seen = {}   # unit -> {section: {number: first (page, text)}}
    for sec, i, line in chunks(rows):
        for m in NOUN.finditer(line):
            n = int(m.group(1).replace(',', ''))
            if n < 3 or 1900 <= n <= 2100: continue   # years and tiny counts
            seen.setdefault(unit_key(m.group(2)), {}).setdefault(sec, {}).setdefault(n, (i, line.strip()[:140]))
    out = []
    for unit, secs in seen.items():
        ab = secs.get('abstract', {}); body = {n for s, d in secs.items() if s != 'abstract' for n in d}
        for n, (i, txt) in ab.items():
            if n >= 10 and body and n not in body:
                out.append(dict(check='SAMPLE', page=page_label(pm, i), section='abstract', finding=f"abstract says {n} {unit}s; the body mentions {', '.join(str(x) for x in sorted(body)[:6])} but never {n}.", text=txt))
        me, rs = {n for n in secs.get('methods', {})}, {n for n in secs.get('results', {})}
        if len(me) >= 2 and len(rs) >= 2 and not (me & rs):
            i = next(iter(secs['results'].values()))[0]
            out.append(dict(check='SAMPLE', page=page_label(pm, i), section='methods vs results', finding=f"{unit}s: methods give {sorted(me)[:5]}, results give {sorted(rs)[:5]}; no number in common (may be different subsets).", text=''))
    return out

EXAMINED = {'PERCENT': 0, 'GRIM': 0, 'SAMPLE': 0}

def run(doc):
    pm = pp.page_map(doc); rows = sectioned(pages_text(doc))
    for _, _, c in chunks(rows):   # how much each check had to work with, so "no findings" is not mistaken for "not looked at"
        if len(PCT.findall(c)) >= 3 and not SKIP_PCT.search(c): EXAMINED['PERCENT'] += 1
        if (MEAN_SD.search(c) or MEAN_WORD.search(c)) and (NVAL.search(c) or NOUN.search(c)): EXAMINED['GRIM'] += 1
        if NOUN.search(c): EXAMINED['SAMPLE'] += 1
    return check_percent(rows, pm) + check_grim(rows, pm) + check_sample(rows, pm)

def selftest():
    """Planted errors the checks must catch, and clean text they must leave alone."""
    pm = [{'printed': None, 'source': None}]
    def rows(*ls): return [(sec, 0, t) for sec, t in ls]
    bad = rows(('abstract', 'We enrolled 120 participants and compared two prompts.'), ('methods', 'Of the 118 participants, 40% were novices, 35% were intermediate and 20% were experts.'),
               ('results', 'Mean satisfaction was 3.47 (SD 0.9) among 25 raters.'), ('results', 'A total of 118 participants completed the study.'))
    good = rows(('abstract', 'We enrolled 118 participants.'), ('methods', 'Of the 118 participants, 40% were novices, 35% were intermediate and 25% were experts.'), ('results', 'Mean satisfaction was 3.48 (SD 0.9) among 25 raters.'))
    got = {f['check'] for f in check_percent(bad, pm) + check_grim(bad, pm) + check_sample(bad, pm)}
    clean = check_percent(good, pm) + check_grim(good, pm) + check_sample(good, pm)
    print('catches planted PERCENT, GRIM, SAMPLE:', got == {'PERCENT', 'GRIM', 'SAMPLE'}, got); print('clean text flagged nothing:', not clean, clean)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('args', nargs='*'); ap.add_argument('--only'); ap.add_argument('--outdir', default=str(OUT)); a = ap.parse_args()
    if a.args[:1] == ['selftest']: selftest(); return
    if a.args[:1] == ['grim']:
        m, n = float(a.args[1]), int(a.args[2]); d = int(a.args[3]) if len(a.args) > 3 else len(a.args[1].split('.')[1])
        print(f"mean {m} n {n}: {'consistent' if grim_ok(m, n, d) else 'NOT possible with whole-number data'}" + ('' if 10 ** d > n else ' (n is large for this many decimals, so the test cannot fail)')); return
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True); allrows = []
    for p in sorted((VAULT / 'sysrev' / 'dgraph' / 'source').glob('@*.md')):
        ck = p.stem
        if a.only and ck.lstrip('@') != a.only.lstrip('@'): continue
        pdf = pp.resolve_pdf(ck)
        if not pdf: print('no PDF:', ck); continue
        for f in run(fitz.open(pdf)): allrows.append({'citekey': ck, **f})
    with open(out / 'stat-checks.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['citekey', 'check', 'page', 'section', 'finding', 'text'], delimiter='\t'); w.writeheader(); w.writerows(allrows)
    by = {}
    for r in allrows: by.setdefault(r['citekey'], []).append(r)
    md = ['# Statistical accuracy checks (scripted clues for a person to check)', '', 'Checks: PERCENT sums, GRIM means, SAMPLE size agreement. A finding is a clue, not a verdict. See `pipeline/scripts/stat_checks.py`.', '']
    for ck, rs in sorted(by.items()):
        md += [f'## {ck}', ''] + [f"- **{r['check']}** ({r['page']}, {r['section']}): {r['finding']}" + (f" Text: “{r['text']}”" if r['text'] else '') for r in rs] + ['']
    (out / 'stat-checks.md').write_text('\n'.join(md), encoding='utf-8')
    c = {}
    for r in allrows: c[r['check']] = c.get(r['check'], 0) + 1
    md.insert(3, f"Examined across all papers: {EXAMINED['PERCENT']} percentage groups, {EXAMINED['GRIM']} mean-with-n passages, {EXAMINED['SAMPLE']} passages naming a sample size. A paper with no finding below simply had nothing flagged.\n")
    (out / 'stat-checks.md').write_text('\n'.join(md), encoding='utf-8')
    print(f"Examined: {EXAMINED}")
    print(f"{len(by)} papers with findings, {len(allrows)} findings: {c}; wrote {out}/stat-checks.md")

if __name__ == '__main__': main()

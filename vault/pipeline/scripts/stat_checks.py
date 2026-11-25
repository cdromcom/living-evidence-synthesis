#!/usr/bin/env python3
"""Statistical accuracy checks on a paper's own text (Quality signals, row "Statistical accuracy"). Cheap, scripted, no model calls. Each finding is a CLUE for a person, not a verdict.
  python3 stat_checks.py                       all source PDFs -> pipeline/misc/evd-validation/stat-checks/
  python3 stat_checks.py --only @citekey       one paper
  python3 stat_checks.py selftest              planted-error self-test
  python3 stat_checks.py grim 3.47 25 [2]      GRIM test of one mean (mean, n, decimals)
Checks
  1 PERCENT   three or more percentages in one sentence or table row that look like parts of 100% but add up to a value away from 100 (beyond rounding)
  2 GRIM      a reported mean with its sample size where no whole-number total can produce that mean (applies only to whole-number data such as Likert ratings or counts)
  4 INTERVAL  a point estimate that falls outside its own confidence interval
  5 RATIO     "a of b (p%)" where p is not 100*a/b
  6 METRIC    F1 that does not follow from the precision and recall in the same passage; kappa that does not follow from observed and chance agreement, or exceeds agreement
  7 EFFECT    effect sizes outside the possible range or above 3 (d); values more than 3 SD from the mean of the same kind across all papers
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


# ---------- 4 INTERVAL: point estimate inside its confidence interval ----------
def norm_text(t): return t.replace('−', '-').replace('–', '-').replace('—', '-')
CI = re.compile(r'(-?\d*\.?\d+)\s*%?\s*[\(\[]\s*(?:\d{2}\s*%\s*)?(?:CI|confidence interval)\s*[:=,]?\s*(-?\d*\.?\d+)\s*%?\s*(?:to|-|,|;|\be\b)\s*(-?\d*\.?\d+)\s*%?\s*[\)\]]', re.I)
def decs(x): return len(x.split('.')[1]) if '.' in x else 0
def check_interval(rows, pm):
    out = []; seen = set()
    for sec, i, c in chunks(rows):
        c = norm_text(c)
        for m in CI.finditer(c):
            est, lo, hi = float(m.group(1)), float(m.group(2)), float(m.group(3)); tol = 0.5 * 10 ** -max(decs(m.group(1)), decs(m.group(2)), decs(m.group(3)))
            if lo > hi: lo, hi = hi, lo
            if not (lo - tol <= est <= hi + tol) and (m.group(0), i) not in seen:
                seen.add((m.group(0), i)); out.append(dict(check='INTERVAL', page=page_label(pm, i), section=sec, finding=f"estimate {m.group(1)} is outside its own interval {m.group(2)} to {m.group(3)}. (A lost minus sign in the PDF text can cause this: look at the page.)", text=m.group(0)[:160]))
    return out

# ---------- 5 RATIO: "a of b (p%)" ----------
RATIO = re.compile(r'(\d[\d,]*)\s*(?:/|of|out of)\s*(\d[\d,]*)\s*[\(\[]\s*(\d+(?:\.\d+)?)\s*%')
def check_ratio(rows, pm):
    out = []; seen = set()
    for sec, i, c in chunks(rows):
        for m in RATIO.finditer(norm_text(c)):
            a, b, p = num(m.group(1)), num(m.group(2)), float(m.group(3)); tol = 0.5 * 10 ** -decs(m.group(3)) + 0.05
            if b <= 0 or (m.group(0), i) in seen: continue
            seen.add((m.group(0), i))
            if a > b or abs(100 * a / b - p) > tol:
                out.append(dict(check='RATIO', page=page_label(pm, i), section=sec, finding=f"{m.group(1)} of {m.group(2)} is {100 * a / b:.1f}%, the text says {m.group(3)}%.", text=m.group(0)[:160]))
    return out

# ---------- 6 METRIC: F1 from precision and recall; kappa from observed and chance agreement; kappa cannot exceed agreement ----------
VAL = r'(-?\d*\.\d+|\d+(?:\.\d+)?)\s*(%?)'
def frac(v, pct): 
    x = float(v); return x / 100 if (pct or x > 1.0) else x
def grab(c, words, wlen=24):
    m = re.search(r'(?:' + words + r')\D{0,%d}?' % wlen + VAL, c, re.I)
    return (frac(m.group(1), m.group(2)), m.group(1)) if m else None
def check_metric(rows, pm):
    out = []
    for sec, i, c in chunks(rows):
        c = norm_text(c)
        P, R, F = grab(c, r'precision'), grab(c, r'recall'), grab(c, r'\bF-?1(?:[- ]score)?\b|F-measure')
        if P and R and F and P[0] + R[0] > 0:
            exp = 2 * P[0] * R[0] / (P[0] + R[0]); tol = 0.015 + 0.5 * 10 ** -decs(F[1])
            if abs(exp - F[0]) > tol and 0 <= F[0] <= 1:
                out.append(dict(check='METRIC', page=page_label(pm, i), section=sec, finding=f"F1 {F[1]} does not match precision {P[1]} and recall {R[1]} (they give {exp:.2f}). Fine if the F1 is a macro or micro average over classes.", text=c[:160]))
        K, PO, PE = grab(c, r'kappa|κ|cohen'), grab(c, r'observed agreement|\bp_?o\b'), grab(c, r'expected agreement|chance agreement|\bp_?e\b')
        if K and PO and PE and PE[0] < 1:
            exp = (PO[0] - PE[0]) / (1 - PE[0])
            if abs(exp - K[0]) > 0.02 + 0.5 * 10 ** -decs(K[1]): out.append(dict(check='METRIC', page=page_label(pm, i), section=sec, finding=f"kappa {K[1]} does not match observed agreement {PO[1]} and chance agreement {PE[1]} (they give {exp:.2f}).", text=c[:160]))
        A = grab(c, r'accuracy|agreement')
        if K and A and not PO and 0 < K[0] <= 1 and K[0] > A[0] + 0.02 and A[0] <= 1:
            out.append(dict(check='METRIC', page=page_label(pm, i), section=sec, finding=f"kappa {K[1]} is larger than the accuracy or agreement {A[1]} in the same passage; kappa cannot exceed observed agreement.", text=c[:160]))
    return out

# ---------- 7 EFFECT: impossible or implausible effect sizes; unusual values against the other papers ----------
EFF = {'d': re.compile(r"(?:cohen'?s\s*)?\b(?:d|g)\s*=\s*(-?\d*\.\d+)", re.I), 'r': re.compile(r'\br\s*=\s*(-?\d*\.\d+)'), 'kappa': re.compile(r'(?:kappa|κ)\s*[=:]?\s*(-?\d*\.\d+)', re.I)}
EFFECT_VALUES = []   # (type, value, citekey-less location) collected across papers for the cross-paper outlier pass
def check_effect(rows, pm):
    out = []
    for sec, i, c in chunks(rows):
        c = norm_text(c)
        for typ, rx in EFF.items():
            for m in rx.finditer(c):
                v = float(m.group(1)); EFFECT_VALUES.append((typ, v, page_label(pm, i), c[:120]))
                if typ == 'd' and abs(v) > 3: out.append(dict(check='EFFECT', page=page_label(pm, i), section=sec, finding=f"standardized effect {v:g} is very large (above 3 in magnitude; typical published effects are under 1).", text=m.group(0)))
                if typ in ('r', 'kappa') and abs(v) > 1: out.append(dict(check='EFFECT', page=page_label(pm, i), section=sec, finding=f"{typ} = {v:g} is outside the possible range -1 to 1.", text=m.group(0)))
    return out

def outliers_across_papers(by_paper):
    """Flag effect sizes more than 3 SD from the mean of the same kind across all papers (needs 15 or more values of that kind). Our corpus stands in for 'the literature' until a larger one is available."""
    import statistics
    res = []
    for typ in EFF:
        vals = [(ck, v, pg, tx) for ck, items in by_paper.items() for (t, v, pg, tx) in items if t == typ]
        if len(vals) < 15: continue
        mu = statistics.mean(v for _, v, _, _ in vals); sd = statistics.pstdev(v for _, v, _, _ in vals)
        if sd == 0: continue
        for ck, v, pg, tx in vals:
            if abs(v - mu) > 3 * sd: res.append(dict(citekey=ck, check='EFFECT', page=pg, section='', finding=f"{typ} = {v:g} is more than 3 SD from the mean ({mu:.2f}, SD {sd:.2f}) of the {len(vals)} {typ} values in these papers.", text=tx))
    return res

EXAMINED = {'PERCENT': 0, 'GRIM': 0, 'SAMPLE': 0, 'INTERVAL': 0, 'RATIO': 0, 'METRIC': 0, 'EFFECT': 0}

def run(doc):
    pm = pp.page_map(doc); rows = sectioned(pages_text(doc))
    for _, _, c in chunks(rows):   # how much each check had to work with, so "no findings" is not mistaken for "not looked at"
        if len(PCT.findall(c)) >= 3 and not SKIP_PCT.search(c): EXAMINED['PERCENT'] += 1
        if (MEAN_SD.search(c) or MEAN_WORD.search(c)) and (NVAL.search(c) or NOUN.search(c)): EXAMINED['GRIM'] += 1
        if NOUN.search(c): EXAMINED['SAMPLE'] += 1
        cn = norm_text(c)
        EXAMINED['INTERVAL'] += len(CI.findall(cn)); EXAMINED['RATIO'] += len(RATIO.findall(cn)); EXAMINED['EFFECT'] += sum(len(r.findall(cn)) for r in EFF.values())
        if re.search(r'precision', cn, re.I) and re.search(r'recall', cn, re.I) or re.search(r'kappa|\u03ba', cn, re.I): EXAMINED['METRIC'] += 1
    return check_percent(rows, pm) + check_grim(rows, pm) + check_sample(rows, pm) + check_interval(rows, pm) + check_ratio(rows, pm) + check_metric(rows, pm) + check_effect(rows, pm)

def selftest():
    """Planted errors the checks must catch, and clean text they must leave alone."""
    pm = [{'printed': None, 'source': None}]
    def rows(*ls): return [(sec, 0, t) for sec, t in ls]
    bad = rows(('abstract', 'We enrolled 120 participants and compared two prompts.'), ('methods', 'Of the 118 participants, 40% were novices, 35% were intermediate and 20% were experts.'),
               ('results', 'Mean satisfaction was 3.47 (SD 0.9) among 25 raters.'), ('results', 'A total of 118 participants completed the study.'))
    good = rows(('abstract', 'We enrolled 118 participants.'), ('methods', 'Of the 118 participants, 40% were novices, 35% were intermediate and 25% were experts.'), ('results', 'Mean satisfaction was 3.48 (SD 0.9) among 25 raters.'))
    bad += rows(('results', 'The odds were 2.4 (95% CI 0.5 to 1.9) overall.'), ('results', 'Accuracy was 31 of 40 (82%).'), ('results', 'Precision was 0.80, recall 0.60 and F1 0.90.'),
                ('results', 'Observed agreement 0.90, chance agreement 0.50, kappa 0.60.'), ('results', 'The effect was large (d = 4.2).'))
    good += rows(('results', 'The odds were 1.2 (95% CI 0.5 to 1.9) overall.'), ('results', 'Accuracy was 31 of 40 (77.5%).'), ('results', 'Precision was 0.80, recall 0.60 and F1 0.69.'),
                 ('results', 'Observed agreement 0.90, chance agreement 0.50, kappa 0.80.'), ('results', 'The effect was moderate (d = 0.6).'))
    allc = lambda r: check_percent(r, pm) + check_grim(r, pm) + check_sample(r, pm) + check_interval(r, pm) + check_ratio(r, pm) + check_metric(r, pm) + check_effect(r, pm)
    got = {f['check'] for f in allc(bad)}; clean = allc(good)
    print('catches planted PERCENT, GRIM, SAMPLE, INTERVAL, RATIO, METRIC, EFFECT:', got == {'PERCENT', 'GRIM', 'SAMPLE', 'INTERVAL', 'RATIO', 'METRIC', 'EFFECT'}, got); print('clean text flagged nothing:', not clean, clean)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('args', nargs='*'); ap.add_argument('--only'); ap.add_argument('--outdir', default=str(OUT)); a = ap.parse_args()
    if a.args[:1] == ['selftest']: selftest(); return
    if a.args[:1] == ['grim']:
        m, n = float(a.args[1]), int(a.args[2]); d = int(a.args[3]) if len(a.args) > 3 else len(a.args[1].split('.')[1])
        print(f"mean {m} n {n}: {'consistent' if grim_ok(m, n, d) else 'NOT possible with whole-number data'}" + ('' if 10 ** d > n else ' (n is large for this many decimals, so the test cannot fail)')); return
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True); allrows = []; EFF_BY = {}
    for p in sorted((VAULT / 'sysrev' / 'dgraph' / 'source').glob('@*.md')):
        ck = p.stem
        if a.only and ck.lstrip('@') != a.only.lstrip('@'): continue
        pdf = pp.resolve_pdf(ck)
        if not pdf: print('no PDF:', ck); continue
        EFFECT_VALUES.clear()
        for f in run(fitz.open(pdf)): allrows.append({'citekey': ck, **f})
        EFF_BY[ck] = list(EFFECT_VALUES)
    allrows += [dict(r) for r in outliers_across_papers(EFF_BY)]
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
    md.insert(3, f"Examined across all papers: {EXAMINED['PERCENT']} percentage groups, {EXAMINED['GRIM']} mean-with-n passages, {EXAMINED['SAMPLE']} passages naming a sample size, {EXAMINED['INTERVAL']} estimates with a confidence interval, {EXAMINED['RATIO']} 'a of b (p%)' ratios, {EXAMINED['METRIC']} passages with F1 or kappa inputs, {EXAMINED['EFFECT']} effect-size values. A paper with no finding below simply had nothing flagged.\n")
    (out / 'stat-checks.md').write_text('\n'.join(md), encoding='utf-8')
    print(f"Examined: {EXAMINED}")
    print(f"{len(by)} papers with findings, {len(allrows)} findings: {c}; wrote {out}/stat-checks.md")

if __name__ == '__main__': main()

"""More forensic checks for stat_checks.py (JP, 2026-11-25). Each function takes (rows, pm) and returns (findings, examined). Helpers come from stat_checks via bind().
  PROP       accuracy-like value times N must be a whole count (GRIM for proportions)
  CIP        p value and 95% CI must agree about the null
  MONO       pass@k, hit-rate@k and recall@k must not fall as k rises
  DELTA      "from a to b (+c points)" arithmetic and direction words
  SDBOUND    an SD cannot exceed the maximum possible for the stated range (Bhatia-Davis); a proportion's SD is bounded by sqrt(p(1-p))
  STATCHECK  recompute p from t, F, chi-square, z and df and compare with the reported p
  GRIMMER    a mean and SD must be reachable with whole-number data (ratings, counts)
  CONFUSION  precision, recall, F1, accuracy, kappa recomputed from TP, FP, FN, TN counts in the text
  MACRO      an average row of a table equals the mean of the rows above it
All are clues, not verdicts."""
import math, re
H = {}
def bind(g): H.update(g)
def pl(pm, i): return H['page_label'](pm, i)
def nt(t): return H['norm_text'](t)
def decs(x): return len(x.split('.')[1]) if '.' in x else 0

# ---------- PROP ----------
ACC = re.compile(r'\b(accuracy|correct(?:ly)?|hit rate|success rate|pass rate|agreement|recall|sensitivity|specificity|precision)\b[^.;\d]{0,25}?(\d{1,3}(?:\.\d+)?)\s*(%?)', re.I)
def prop_ok(p, n, dec):
    """Is there a whole k with round(k/n, dec) == p ? p is a fraction, dec the decimals of the fraction."""
    lo, hi = math.floor((p - 0.5 * 10 ** -dec) * n), math.ceil((p + 0.5 * 10 ** -dec) * n)
    return any(abs(math.floor(k / n * 10 ** dec + 0.5) / 10 ** dec - p) < 1e-9 for k in range(max(lo, 0), min(hi, n) + 1))
def check_prop(rows, pm):
    out, ex = [], 0; seen = set()
    for sec, i, c in H['chunks'](rows):
        c = nt(c); ns = {int(x.replace(',', '')) for x in H['NVAL'].findall(c)} or {int(m.group(1).replace(',', '')) for m in H['NOUN'].finditer(c)}
        if len(ns) != 1 or len(c) > 300 or len(re.findall(r'\d\s*%', c)) > 3: continue
        n = ns.pop()
        if n < 10 or n > 5000: continue
        for m in ACC.finditer(c):
            if re.search(r'[\d%]\s*$', c[:m.start()]): continue   # the number before the word is the one the word labels
            raw, pct = m.group(2), m.group(3) == '%'
            v = float(raw); frac = v / 100 if pct else v
            if not (0 <= frac <= 1) or (not pct and '.' not in raw): continue
            dec = decs(raw) + (2 if pct else 0); ex += 1
            if (m.group(0), n, i) in seen: continue
            seen.add((m.group(0), n, i))
            if not prop_ok(frac, n, dec):
                out.append(dict(check='PROP', page=pl(pm, i), section=sec, finding=f"{m.group(1)} {raw}{'%' if pct else ''} cannot be a whole count out of n = {n} (nearest possible: {round(frac * n) / n * (100 if pct else 1):.{decs(raw)}f}). Fine if it is an average over runs, folds or raters.", text=c[:160]))
    return out, ex

# ---------- CIP ----------
CIP_RX = re.compile(r'(-?\d*\.?\d+)\s*%?\s*[\(\[]\s*(?:(\d{2})\s*%\s*)?(?:CI|confidence interval)\s*[:=,]?\s*(-?\d*\.?\d+)\s*%?\s*(?:to|-|,|;|\be\b)\s*(-?\d*\.?\d+)\s*%?\s*[\)\]][^.;]{0,60}?\bp\s*([<=>≤])\s*(\d*\.\d+)', re.I)
RATIO_WORDS = re.compile(r'\b(?:odds ratio|OR|risk ratio|relative risk|RR|hazard ratio|HR|rate ratio|IRR)\b')
def check_cip(rows, pm):
    out, ex = [], 0
    for sec, i, c in H['chunks'](rows):
        c = nt(c)
        for m in CIP_RX.finditer(c):
            lvl = int(m.group(2) or 95)
            if lvl != 95: continue
            lo, hi = sorted([float(m.group(3)), float(m.group(4))]); p = float(m.group(6)); op = m.group(5); ex += 1
            null = 1.0 if RATIO_WORDS.search(c) else 0.0
            excludes = not (lo <= null <= hi)
            sig = (p <= 0.05) if op in '<=≤' else (p >= 0.05 and False)   # p > .05 means not significant
            if op == '>': sig = False
            if op == '=' and p > 0.05: sig = False
            if op in '<≤' and p > 0.05: continue   # "p < .10" says nothing about .05
            if excludes != sig:
                out.append(dict(check='CIP', page=pl(pm, i), section=sec, finding=f"95% CI {m.group(3)} to {m.group(4)} {'excludes' if excludes else 'includes'} {null:g} but p {op} {m.group(6)} says {'significant' if sig else 'not significant'}.", text=m.group(0)[:160]))
    return out, ex

# ---------- MONO ----------
MONO_RX = re.compile(r'\b(pass|hit|recall|HR|top|acc|accuracy|success)\s*(?:rate\s*)?@\s*(\d+)\b[^@\d]{0,18}?(\d{1,3}(?:\.\d+)?)\s*(%?)', re.I)
def check_mono(rows, pm):
    out, ex = mono_tables(rows, pm)
    for sec, i, c in H['chunks'](rows):
        c = nt(c); by = {}
        for m in MONO_RX.finditer(c): by.setdefault(m.group(1).lower(), []).append((int(m.group(2)), float(m.group(3)), m.group(3)))
        for name, items in by.items():
            if len(items) < 2: continue
            ex += 1; items.sort()
            for (k1, v1, r1), (k2, v2, r2) in zip(items, items[1:]):
                if k2 > k1 and v2 < v1 - 1e-9:
                    out.append(dict(check='MONO', page=pl(pm, i), section=sec, finding=f"{name}@{k2} = {r2} is lower than {name}@{k1} = {r1}; this measure cannot fall as k grows (unless the models or runs differ).", text=c[:160])); break
    return out, ex


HEADK = re.compile(r'\b(pass|hit|recall|HR|top|acc|accuracy|success)\s*(?:rate\s*)?@\s*(\d+)\b', re.I)
def mono_tables(rows, pm):
    """Table form: a header line with several name@k labels, then data rows whose last cells follow the header order."""
    out, ex = [], 0
    for j, (sec, i, l) in enumerate(rows):
        hs = [(m.group(1).lower(), int(m.group(2))) for m in HEADK.finditer(l)]
        if len(hs) < 2 or len({n for n, _ in hs}) != 1 or re.search(r'\d', HEADK.sub('', l)): continue   # a header has the labels and no other numbers
        ks = [k for _, k in hs]
        if ks != sorted(ks): continue
        for sec2, i2, l2 in rows[j + 1:j + 16]:
            if i2 != i: break
            cells = [float(x) for x in re.findall(r'(?<![\w.@])(-?\d*\.\d+|\d+)(?![\w.])', l2)]
            if len(cells) < len(ks): continue
            v = cells[-len(ks):]; ex += 1
            for a, b, ka, kb in zip(v, v[1:], ks, ks[1:]):
                if b < a - 1e-9:
                    out.append(dict(check='MONO', page=pl(pm, i), section=sec, finding=f"in this table row {hs[0][0]}@{kb} = {b:g} is lower than {hs[0][0]}@{ka} = {a:g}; the measure cannot fall as k grows (unless the cells belong to different columns).", text=l2.strip()[:160])); break
    return out, ex

# ---------- DELTA ----------
NUMR = r'(-?\d+(?:\.\d+)?)'
DELTA_A = re.compile(r'\bfrom\s+' + NUMR + r'\s*%?\s+to\s+' + NUMR + r'\s*%?\s*[\(\[]\s*([+-]?\s*\d+(?:\.\d+)?)\s*(percentage points?|points?|pp|%)?', re.I)
DELTA_B = re.compile(r'\b(improv\w*|increas\w*|rose|gain\w*|drop\w*|decreas\w*|fell|declin\w*|reduc\w*)\b[^.;]{0,30}?\bby\s+' + NUMR + r'\s*(percentage points?|points?|pp|%)[^.;]{0,25}?\bfrom\s+' + NUMR + r'\s*%?\s+to\s+' + NUMR, re.I)
UP = re.compile(r'improv|increas|rose|gain', re.I)
def check_delta(rows, pm):
    out, ex = [], 0; seen = set()
    for sec, i, c in H['chunks'](rows):
        c = nt(c)
        cands = []
        for m in DELTA_A.finditer(c): cands.append((float(m.group(1)), float(m.group(2)), float(m.group(3).replace(' ', '')), (m.group(4) or '').lower(), None, m.group(0)))
        for m in DELTA_B.finditer(c): cands.append((float(m.group(4)), float(m.group(5)), float(m.group(2)), m.group(3).lower(), m.group(1), m.group(0)))
        for a, b, d, unit, verb, text in cands:
            if (text, i) in seen: continue
            seen.add((text, i)); ex += 1; tol = 0.15 + 0.5 * 10 ** -decs(str(abs(d)))
            absd, rel = b - a, (100 * (b - a) / a if a else float('inf'))
            ok = abs(abs(absd) - abs(d)) <= tol or abs(abs(rel) - abs(d)) <= max(tol, 0.6)
            wrongdir = verb is not None and ((UP.search(verb) is not None) != (b > a))
            if not ok or wrongdir:
                out.append(dict(check='DELTA', page=pl(pm, i), section=sec, finding=(f"from {a:g} to {b:g} is {absd:+.2f} points ({rel:+.1f}% relative), but the text says {d:g}{' ' + unit if unit else ''}." if not ok else f"the text says '{verb}' but the value goes from {a:g} to {b:g}."), text=text[:160]))
    return out, ex

# ---------- SDBOUND ----------
MSD = re.compile(r'(?<![\d.])(\d+(?:\.\d+)?)\s*(?:±|\+/-|\+-)\s*(\d+(?:\.\d+)?)|(?<![\d.])(\d+(?:\.\d+)?)\s*[\(\[]\s*(?:SD|s\.d\.|std)?\s*[=:]?\s*(\d+\.\d+)\s*[\)\]]', re.I)
METRIC01 = re.compile(r'\b(accuracy|precision|recall|F-?1|AUC|agreement|kappa|score|hit rate|pass@\d+)\b', re.I)
def check_sdbound(rows, pm):
    out, ex = [], 0; seen = set()
    for sec, i, c in H['chunks'](rows):
        c = nt(c)
        if not MSD.search(c): continue
        lo = hi = None
        for rx in H['RANGE']:
            m = rx.search(c)
            if m and int(m.group(1)) in (0, 1) and int(m.group(1)) < int(m.group(2)) <= 1000: lo, hi = float(m.group(1)), float(m.group(2)); break
        for m in MSD.finditer(c):
            mean = float(m.group(1) or m.group(3)); sd = float(m.group(2) or m.group(4))
            l, h = lo, hi
            if h is None and METRIC01.search(c): l, h = (0.0, 1.0) if mean <= 1.0 else (0.0, 100.0)
            if h is None or not (l <= mean <= h): continue
            ex += 1; bound = math.sqrt(max((h - mean) * (mean - l), 0)) * 1.42
            if sd > bound + 1e-9 and (m.group(0), i) not in seen:
                seen.add((m.group(0), i)); out.append(dict(check='SDBOUND', page=pl(pm, i), section=sec, finding=f"SD {sd:g} is larger than any data between {l:g} and {h:g} can give at mean {mean:g} (limit about {bound:.3g}).", text=m.group(0)[:160]))
    return out, ex

# ---------- STATCHECK ----------
TEST = re.compile(r'\b(t|F|z|r|χ\s*2|χ2|chi[- ]?square[d]?|chi2|X2)\s*(?:\(\s*(\d+(?:\.\d+)?)(?:\s*,\s*(\d+(?:\.\d+)?))?(?:\s*,\s*N\s*=\s*\d+)?\s*\))?\s*=\s*(-?\d*\.?\d+)\s*[,;]?\s*(?:\(?\s*)?p\s*([<=>≤≥])\s*(\.\d+|0\.\d+|\d+(?:\.\d+)?)', re.I)
def pcalc(kind, v, d1, d2):
    from scipy import stats
    if kind == 't': return 2 * stats.t.sf(abs(v), d1)
    if kind == 'f': return stats.f.sf(abs(v), d1, d2)
    if kind == 'z': return 2 * stats.norm.sf(abs(v))
    if kind == 'chi': return stats.chi2.sf(abs(v), d1)
    if kind == 'r':
        t = v * math.sqrt(d1 / max(1e-12, 1 - v * v)); return 2 * stats.t.sf(abs(t), d1)
def check_statcheck(rows, pm):
    out, ex = [], 0; seen = set()
    try: import scipy  # noqa
    except Exception: return out, ex
    for sec, i, c in H['chunks'](rows):
        c = nt(c)
        for m in TEST.finditer(c):
            k = m.group(1).lower().replace(' ', ''); kind = 'chi' if k.startswith(('χ', 'chi', 'x2')) else k
            d1 = float(m.group(2)) if m.group(2) else None; d2 = float(m.group(3)) if m.group(3) else None
            if kind in ('t', 'chi', 'r') and d1 is None: continue
            if kind == 'f' and (d1 is None or d2 is None): continue
            v = float(m.group(4)); op, praw = m.group(5), m.group(6); p = float(praw if praw.startswith(('0', '1')) else '0' + praw)
            if kind == 'r' and abs(v) >= 1: continue
            ex += 1
            if (m.group(0), i) in seen or re.search(r'one[- ](?:tailed|sided)', c, re.I): continue
            seen.add((m.group(0), i)); h = 0.5 * 10 ** -decs(m.group(4))
            try: pa, pb = pcalc(kind, abs(v) + h, d1, d2), pcalc(kind, max(abs(v) - h, 0), d1, d2)
            except Exception: continue
            lo, hi = min(pa, pb), max(pa, pb); ptol = 0.5 * 10 ** -decs(praw)
            if op == '=': bad = not (lo - ptol <= p <= hi + ptol); sigrep, sigcalc = p < 0.05, (lo + hi) / 2 < 0.05
            elif op in '<≤': bad = lo > p + ptol; sigrep, sigcalc = True, lo < 0.05
            else: bad = hi < p - ptol; sigrep, sigcalc = False, hi < 0.05
            if bad:
                out.append(dict(check='STATCHECK', page=pl(pm, i), section=sec, finding=f"{m.group(1)}{'(' + m.group(2) + (',' + m.group(3) if m.group(3) else '') + ')' if m.group(2) else ''} = {m.group(4)} gives p about {(lo + hi) / 2:.3g}, but the text says p {op} {praw}" + (" (this changes whether p is below .05)." if sigrep != sigcalc else "."), text=m.group(0)[:160]))
    return out, ex

# ---------- GRIMMER ----------
def grimmer_ok(mean, sd, n, dec_m, dec_s):
    """True if whole-number data of size n can have this (rounded) mean and SD. Uses the sum of squares: Q = (n-1)s^2 + T^2/n must be a whole number with Q = T (mod 2)."""
    if n < 2: return True
    hm, hs = 0.5 * 10 ** -dec_m, 0.5 * 10 ** -dec_s
    for T in range(math.ceil((mean - hm) * n - 1e-9), math.floor((mean + hm) * n + 1e-9) + 1):
        lo = (n - 1) * max(sd - hs, 0) ** 2 + T * T / n; hi = (n - 1) * (sd + hs) ** 2 + T * T / n
        for Q in range(math.ceil(lo - 1e-9), math.floor(hi + 1e-9) + 1):
            if (Q - T) % 2 == 0 and Q * n >= T * T - 1e-9: return True
    return False
MSD2 = re.compile(r'(?<![\d.])(\d{1,3}\.(\d{1,2}))\s*[\(\[]\s*(?:SD\s*[=:]?\s*)?(\d+\.(\d{1,3}))\s*[\)\]]|(?<![\d.])(\d{1,3}\.(\d{1,2}))\s*(?:±|\+/-)\s*(\d+\.(\d{1,3}))')
INTCUE = re.compile(r'\b(likert|rating|ratings|rated|scored|score[sd]?|count|counts|number of|items?|points?)\b', re.I)
def check_grimmer(rows, pm):
    out, ex = [], 0; seen = set()
    for sec, i, c in H['chunks'](rows):
        c = nt(c)
        ns = [int(x.replace(',', '')) for x in H['NVAL'].findall(c)] or [int(m.group(1).replace(',', '')) for m in H['NOUN'].finditer(c)]
        if len(set(ns)) != 1 or not INTCUE.search(c) or len(MSD2.findall(c)) > 2 or len(c) > 400: continue
        n = ns[0]
        if n < 5 or n > 300: continue
        for m in MSD2.finditer(c):
            g = m.groups(); mean, dm, sd, ds = (float(g[0]), len(g[1]), float(g[2]), len(g[3])) if g[0] else (float(g[4]), len(g[5]), float(g[6]), len(g[7]))
            ex += 1
            if (m.group(0), i) in seen: continue
            seen.add((m.group(0), i))
            if not grim_ok_local(mean, n, dm) or not grimmer_ok(mean, sd, n, dm, ds):
                out.append(dict(check='GRIMMER', page=pl(pm, i), section=sec, finding=f"mean {mean:g} and SD {sd:g} with n = {n} cannot come from whole-number data. Applies only if the scores are whole numbers (ratings, counts).", text=m.group(0)[:160]))
    return out, ex
def grim_ok_local(mean, n, dec): return H['grim_ok'](mean, n, dec) if 10 ** dec > n else True

# ---------- CONFUSION ----------
CM = {k: re.compile(r'\b' + k + r'\s*[=:]\s*(\d[\d,]*)', re.I) for k in ('TP', 'FP', 'FN', 'TN')}
def check_confusion(rows, pm):
    out, ex = [], 0; seen = set()
    for sec, i, c in H['chunks'](rows):
        c = nt(c); v = {}
        for k, rx in CM.items():
            m = rx.search(c)
            if m: v[k] = int(m.group(1).replace(',', ''))
        if len(v) < 3 or c[:80] in seen: continue
        seen.add(c[:80]); tp, fp, fn = v.get('TP'), v.get('FP'), v.get('FN'); tn = v.get('TN')
        if None in (tp, fp, fn): continue
        calc = {'precision': tp / (tp + fp) if tp + fp else None, 'recall': tp / (tp + fn) if tp + fn else None}
        if calc['precision'] and calc['recall']: calc['f1'] = 2 * calc['precision'] * calc['recall'] / (calc['precision'] + calc['recall'])
        if tn is not None:
            N = tp + fp + fn + tn; calc['accuracy'] = (tp + tn) / N
            pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / N ** 2; calc['kappa'] = ((tp + tn) / N - pe) / (1 - pe) if pe < 1 else None
        for name, rx in (('precision', 'precision'), ('recall', 'recall|sensitivity'), ('f1', r'F-?1'), ('accuracy', 'accuracy'), ('kappa', 'kappa|κ')):
            g = H['grab'](c, rx)
            if g is None or calc.get(name) is None: continue
            ex += 1
            if abs(g[0] - calc[name]) > 0.015 + 0.5 * 10 ** -decs(g[1]):
                out.append(dict(check='CONFUSION', page=pl(pm, i), section=sec, finding=f"{name} {g[1]} does not match the counts given (TP {tp}, FP {fp}, FN {fn}" + (f", TN {tn}" if tn is not None else '') + f"), which give {calc[name]:.3f}.", text=c[:160]))
    return out, ex

# ---------- MACRO (table rows) ----------
CELL = re.compile(r'(?<![\w.@])(-?\d*\.\d+|\d+)(?![\w.])')
def check_macro(rows, pm):
    out, ex = [], 0
    lines = [(sec, i, l) for sec, i, l in rows]
    for j, (sec, i, l) in enumerate(lines):
        if not re.match(r'\s*(?:macro[- ]?(?:avg|average)?|mean|average|avg\.?|overall mean)\b', l, re.I) or len(l) > 80 or re.search(r'weighted|micro|std|stdev|variance|table|figure|@', l, re.I): continue
        vals = [float(x) for x in CELL.findall(l)]
        k = len(vals)
        if k < 1 or k > 8 or not any('.' in x for x in CELL.findall(l)): continue
        prev = []
        for sec2, i2, l2 in reversed(lines[max(0, j - 12):j]):
            if i2 != i: break
            if re.search(r'\b(macro|mean|average|avg|micro|weighted|total|overall)\b', l2, re.I): break
            v2 = [float(x) for x in CELL.findall(l2)]
            if len(v2) != k: break
            prev.append(v2)
        if len(prev) < 3: continue
        ex += 1
        for c in range(k):
            col = [r[c] for r in prev]; mu = sum(col) / len(col); tol = 0.02 * max(1.0, abs(mu)) + 0.5 * 10 ** -2
            if abs(mu - vals[c]) > tol:
                out.append(dict(check='MACRO', page=pl(pm, i), section=sec, finding=f"the average row says {vals[c]:g} in column {c + 1}, but the {len(prev)} rows above average {mu:.3g} (unweighted).", text=l.strip()[:160])); break
    return out, ex
CHECKS = [check_prop, check_cip, check_mono, check_delta, check_sdbound, check_statcheck, check_grimmer, check_confusion, check_macro]
